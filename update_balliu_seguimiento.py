#!/usr/bin/env python3
"""
update_balliu_seguimiento.py

Genera (o regenera) dos hojas en Santavila.xlsx con el seguimiento de tarifas
de Balliu, leyendo todos los PDFs con prefijo YYYYMMDD en proveedores_raw/balliu/.

Diferencias con Hevea:
  - Fuente: PDFs (no CSVs). Se parsean con pdfplumber por coordenadas.
  - Balliu sólo da COSTE sin IVA. El PVP se calcula como Coste × 1,21 (sólo IVA).
  - Identificación por (Producto, Variante, Grupo, Ord) — Balliu repite algunos
    nombres (p. ej. Capri Mesa 60X60... aparece 2 veces con precios distintos).

Idempotente: ejecutar varias veces produce el mismo resultado.
NO toca las hojas existentes "Todos", "Hevea", "Balliu", "Hevea Histórico",
"Hevea Seguimiento". Sí regenera "Balliu Histórico" y "Balliu Seguimiento".

PDFs sin prefijo de fecha (catálogo, fichas, etc.) se ignoran. Snapshots
descartados se mueven a `proveedores_raw/balliu/_archived/`.

Requiere: pip install openpyxl pdfplumber
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import openpyxl
import pdfplumber
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule

BASE = Path(__file__).parent
XLSX = BASE / "Santavila.xlsx"
BALLIU_DIR = BASE / "proveedores_raw" / "balliu"

DATE_PREFIX_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})(?:\s|\s*-)")
GROUP_RE = re.compile(r"^G[1-4]$")
PRICE_TOKEN_RE = re.compile(r"^[\d\.]+,\d{2}$")
IVA = 1.21

# ── Extracción de tarifa desde PDF ───────────────────────────────────────────

def find_dated_pdfs(folder):
    out = []
    skipped = []
    for p in folder.glob("*.pdf"):
        m = DATE_PREFIX_RE.match(p.name)
        if not m:
            continue
        try:
            datetime.strptime(f"{m.group(1)}{m.group(2)}{m.group(3)}", "%Y%m%d")
        except ValueError:
            skipped.append(p.name)
            continue
        date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        out.append((date_str, p))
    if skipped:
        print(f"⚠ PDFs con fecha inválida en el nombre, ignorados: {skipped}", file=sys.stderr)
    return sorted(out)


def group_lines(words, y_tol=3):
    out = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if out and abs(w["top"] - out[-1][0]["top"]) < y_tol:
            out[-1].append(w)
        else:
            out.append([w])
    return out


def parse_line(line_words, x_var=200):
    """Producto = X<x_var. Resto: clasificar por valor (G[1-4] / número / texto)."""
    cols = {"producto": [], "variante": [], "grupo": [], "precio": []}
    for w in line_words:
        t = w["text"]
        if w["x0"] < x_var:
            cols["producto"].append(t)
        elif GROUP_RE.match(t):
            cols["grupo"].append(t)
        elif PRICE_TOKEN_RE.match(t):
            cols["precio"].append(t)
        elif t == "€":
            pass
        else:
            cols["variante"].append(t)
    return {k: " ".join(v).strip() for k, v in cols.items()}


def parse_price(s):
    if not s:
        return None
    s = s.replace("€", "").strip()
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def extract_tarifa(pdf_path):
    """Devuelve lista de dicts {producto, variante, grupo, precio} en orden visual."""
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for pg_idx, page in enumerate(pdf.pages):
            words = page.extract_words(use_text_flow=False, keep_blank_chars=False)
            lines = group_lines(words)
            if not lines:
                continue

            header_idx = None
            for li, ln in enumerate(lines[:8]):
                texts = [w["text"] for w in ln]
                if "Producto" in texts and "Grupo" in texts:
                    header_idx = li
                    break
            if header_idx is None:
                continue

            page_data = []
            page_only = []
            for li, ln in enumerate(lines):
                if li <= header_idx:
                    continue
                top = ln[0]["top"]
                p = parse_line(ln)
                if not p["producto"] and not p["variante"] and not p["grupo"]:
                    continue
                tiene_grupo = bool(GROUP_RE.match(p["grupo"]))
                tiene_precio = bool(p["precio"])
                if tiene_grupo and tiene_precio:
                    page_data.append({
                        "top": top,
                        "producto_inline": p["producto"] or None,
                        "variante": p["variante"],
                        "grupo": p["grupo"],
                        "precio": parse_price(p["precio"]),
                    })
                elif p["producto"] and not tiene_grupo and not tiene_precio:
                    page_only.append({"top": top, "producto": p["producto"]})

            # Bloques (cuántas filas pertenecen al mismo producto, según geometría PDF)
            tables = page.extract_tables() or []
            block_sizes = []
            for table in tables:
                current = 0
                for row in table:
                    cell = row[0] if len(row) > 0 else None
                    if cell is not None:
                        if current > 0:
                            block_sizes.append(current)
                        current = 1
                    else:
                        current += 1
                if current > 0:
                    block_sizes.append(current)

            if sum(block_sizes) != len(page_data):
                print(f"⚠ Página {pg_idx+1} de {pdf_path.name}: descuadre bloques({sum(block_sizes)}) vs DATA({len(page_data)})", file=sys.stderr)
                # Fallback: tratar cada DATA como su propio bloque
                block_sizes = [1] * len(page_data)

            di = 0
            for size in block_sizes:
                block = page_data[di:di + size]
                di += size
                producto = next((d["producto_inline"] for d in block if d["producto_inline"]), None)
                if not producto and block:
                    top_min = min(d["top"] for d in block)
                    top_max = max(d["top"] for d in block)
                    margin = 30
                    candidatos = [o for o in page_only
                                  if top_min - margin <= o["top"] <= top_max + margin]
                    if candidatos:
                        centro = (top_min + top_max) / 2
                        producto = min(candidatos, key=lambda o: abs(o["top"] - centro))["producto"]
                if not producto:
                    producto = "(SIN PRODUCTO)"
                for d in block:
                    rows.append({
                        "producto": producto,
                        "variante": d["variante"],
                        "grupo": d["grupo"],
                        "precio": d["precio"],
                    })
    return rows


def assign_ord(rows):
    """Asigna número de orden 1..N a cada (producto, variante, grupo) repetida.
    Balliu lista algunos productos con el mismo nombre y variante varias veces;
    el orden de aparición permite distinguirlos."""
    seen = defaultdict(int)
    for r in rows:
        k = (r["producto"], r["variante"], r["grupo"])
        seen[k] += 1
        r["ord"] = seen[k]
    return rows


# ── Construcción del modelo ──────────────────────────────────────────────────

def build_data(snapshots):
    """
    snapshots: lista [(fecha, rows)] ordenada por fecha asc.
    rows: lista de {producto, variante, grupo, precio, ord}.
    Devuelve dict clave -> {producto, variante, grupo, ord, fechas: {fecha: precio}}.
    """
    products = defaultdict(lambda: {"producto": None, "variante": None, "grupo": None, "ord": None, "fechas": {}})
    for fecha, rows in sorted(snapshots, key=lambda x: x[0]):
        for r in rows:
            key = (r["producto"], r["variante"], r["grupo"], r["ord"])
            products[key]["producto"] = r["producto"]
            products[key]["variante"] = r["variante"]
            products[key]["grupo"] = r["grupo"]
            products[key]["ord"] = r["ord"]
            products[key]["fechas"][fecha] = r["precio"]
    return products


# ── Estilos compartidos ──────────────────────────────────────────────────────

BALLIU_BLUE = "0B5394"   # un poco más oscuro para distinguir de Hevea (1F4E79)
ROW_A = "DDEEFF"
ROW_B = "EEF5FF"
TOTAL_BG = "F5F5DC"

THIN = Side(style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

BLOCKS = "▁▂▃▄▅▆▇█"

def sparkline_text(values):
    nums = [v for v in values if v is not None]
    if len(nums) < 2:
        return ""
    mn, mx = min(nums), max(nums)
    if mx == mn:
        return BLOCKS[3] * len(values)
    rng = mx - mn
    out = ""
    for v in values:
        if v is None:
            out += " "
        else:
            idx = int((v - mn) / rng * (len(BLOCKS) - 1))
            out += BLOCKS[idx]
    return out


# ── Hoja "Balliu Histórico" (long) ───────────────────────────────────────────

HEADERS_HIST = [
    "Proveedor", "Producto", "Variante", "Grupo", "Fecha",
    "Coste neto exworks €", "PVP con IVA €",
    "Δ Coste €", "Δ Coste %",
]
WIDTHS_HIST = [10, 32, 38, 8, 12, 18, 16, 12, 12]


def variante_display(v, ord_, has_dups):
    """Si la (producto, variante, grupo) está duplicada, indica el orden con #N
    en TODAS sus instancias (también la #1) para que el usuario vea desde la
    primera fila que existen duplicados."""
    return f"{v} (#{ord_})" if has_dups else v


def write_historico(wb, products):
    if "Balliu Histórico" in wb.sheetnames:
        del wb["Balliu Histórico"]
    ws = wb.create_sheet("Balliu Histórico")

    for ci, h in enumerate(HEADERS_HIST, 1):
        c = ws.cell(row=1, column=ci, value=h)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=BALLIU_BLUE)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"

    for ci, w in enumerate(WIDTHS_HIST, 1):
        ws.column_dimensions[get_column_letter(ci)].width = w

    thick_top = Side(style="medium", color=BALLIU_BLUE)
    border_group_top = Border(left=THIN, right=THIN, top=thick_top, bottom=THIN)

    # Detectar ord_max por clave (prod, var, grp) para mostrar #N solo cuando hay duplicados
    ord_max = defaultdict(int)
    for k in products:
        prod, var, grp, ord_ = k
        ord_max[(prod, var, grp)] = max(ord_max[(prod, var, grp)], ord_)

    sorted_keys = sorted(products.keys(), key=lambda k: (k[0], k[1], k[2], k[3]))
    rn = 2
    group_idx = 0
    for key in sorted_keys:
        prod, var, grp, ord_ = key
        info = products[key]
        prev_precio = None
        group_idx += 1
        group_color = ROW_A if group_idx % 2 == 0 else ROW_B
        var_disp = variante_display(var, ord_, ord_max[(prod, var, grp)] > 1)
        fechas_ord = sorted(info["fechas"].keys())
        for i_fecha, fecha in enumerate(fechas_ord):
            precio = info["fechas"][fecha]
            pvp = round(precio * IVA, 2) if precio is not None else None
            d_precio = (precio - prev_precio) if (precio is not None and prev_precio is not None) else None
            d_precio_pct = (d_precio / prev_precio * 100) if (d_precio is not None and prev_precio) else None

            row_vals = [
                "Balliu", prod, var_disp, grp, fecha,
                precio, pvp,
                d_precio, d_precio_pct,
            ]
            fill = PatternFill("solid", fgColor=group_color)
            row_border = border_group_top if i_fecha == 0 else BORDER
            es_primera = (i_fecha == 0)
            for ci, val in enumerate(row_vals, 1):
                c = ws.cell(row=rn, column=ci, value=val)
                c.fill = fill
                c.border = row_border
                if ci in (1, 2, 3, 4) and es_primera:
                    c.font = Font(size=9, bold=True, color=BALLIU_BLUE)
                else:
                    c.font = Font(size=9)
                if ci in (6, 7):
                    c.number_format = '€ #,##0.00'
                    c.alignment = Alignment(horizontal="right", vertical="center")
                elif ci == 8:
                    c.number_format = '+€ #,##0.00;-€ #,##0.00;"—"'
                    c.alignment = Alignment(horizontal="right", vertical="center")
                elif ci == 9:
                    c.number_format = '+0.0"%";-0.0"%";"—"'
                    c.alignment = Alignment(horizontal="right", vertical="center")
                elif ci == 5:
                    c.alignment = Alignment(horizontal="center", vertical="center")
                elif ci == 4:
                    c.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    c.alignment = Alignment(horizontal="left", vertical="center")
            rn += 1
            prev_precio = precio

    last_row = rn - 1
    if last_row >= 2:
        ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS_HIST))}{last_row}"
    return last_row - 1


# ── Hoja "Balliu Seguimiento" (wide) ─────────────────────────────────────────

HEADERS_SEG = [
    "Proveedor", "Producto", "Variante", "Grupo",
    "1ª aparición", "Última aparición", "Estado",
    "Coste actual €", "PVP con IVA €",
    "Δ Coste %\nvs anterior", "Δ Coste %\nvs origen",
    "Nº subidas", "Tendencia",
]
WIDTHS_SEG = [10, 32, 38, 8, 13, 13, 16, 14, 14, 14, 14, 11, 14]


def write_seguimiento(wb, snapshots, products):
    if "Balliu Seguimiento" in wb.sheetnames:
        del wb["Balliu Seguimiento"]
    ws = wb.create_sheet("Balliu Seguimiento")

    fechas = [f for f, _ in snapshots]
    primera_fecha = fechas[0] if fechas else "—"
    ultima_fecha = fechas[-1] if fechas else "—"

    title = ws.cell(row=1, column=1, value="Balliu — Seguimiento de tarifas")
    title.font = Font(bold=True, color="FFFFFF", size=14)
    title.fill = PatternFill("solid", fgColor=BALLIU_BLUE)
    title.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADERS_SEG))
    ws.row_dimensions[1].height = 30

    ws.cell(row=2, column=1,
            value=f"Última actualización: {ultima_fecha}  │  Fuente: proveedores_raw/balliu/*.pdf  │  PVP = Coste × 1,21 (IVA)"
            ).font = Font(italic=True, color="666666", size=10)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(HEADERS_SEG))

    ws.cell(row=3, column=1,
            value=f"Fechas en seguimiento: {' · '.join(fechas)}  ({len(fechas)} snapshots)"
            ).font = Font(italic=True, color="666666", size=10)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=len(HEADERS_SEG))

    HEADER_ROW = 5
    for ci, h in enumerate(HEADERS_SEG, 1):
        c = ws.cell(row=HEADER_ROW, column=ci, value=h)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=BALLIU_BLUE)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    ws.row_dimensions[HEADER_ROW].height = 38

    for ci, w in enumerate(WIDTHS_SEG, 1):
        ws.column_dimensions[get_column_letter(ci)].width = w

    ord_max = defaultdict(int)
    for k in products:
        prod, var, grp, ord_ = k
        ord_max[(prod, var, grp)] = max(ord_max[(prod, var, grp)], ord_)

    sorted_keys = sorted(products.keys(), key=lambda k: (k[0], k[1], k[2], k[3]))
    rn = HEADER_ROW + 1
    for key in sorted_keys:
        prod, var, grp, ord_ = key
        info = products[key]
        var_disp = variante_display(var, ord_, ord_max[(prod, var, grp)] > 1)
        fechas_app = sorted(info["fechas"].keys())
        primera_app, ultima_app = fechas_app[0], fechas_app[-1]

        if ultima_app != ultima_fecha:
            estado = "DESCATALOGADO"
        elif primera_app != primera_fecha:
            estado = "NUEVO"
        else:
            estado = "ACTIVO"

        precio = info["fechas"][ultima_app]
        pvp = round(precio * IVA, 2) if precio is not None else None

        d_pct_anterior = None
        if len(fechas_app) >= 2:
            penult = info["fechas"][fechas_app[-2]]
            if penult and precio is not None:
                d_pct_anterior = (precio - penult) / penult * 100

        d_pct_origen = None
        primero = info["fechas"][primera_app]
        if primero and precio is not None and len(fechas_app) >= 2:
            d_pct_origen = (precio - primero) / primero * 100

        precios_serie = [info["fechas"][f] for f in fechas_app]
        n_subidas = sum(
            1 for i in range(1, len(precios_serie))
            if precios_serie[i] is not None and precios_serie[i-1] is not None
            and precios_serie[i] > precios_serie[i-1]
        )
        tendencia = sparkline_text(precios_serie)

        row_vals = [
            "Balliu", prod, var_disp, grp,
            primera_app, ultima_app, estado,
            precio, pvp,
            d_pct_anterior, d_pct_origen,
            n_subidas, tendencia,
        ]
        fill = PatternFill("solid", fgColor=ROW_A if rn % 2 == 0 else ROW_B)
        for ci, val in enumerate(row_vals, 1):
            c = ws.cell(row=rn, column=ci, value=val)
            c.fill = fill
            c.border = BORDER
            c.font = Font(size=9)

            if ci in (8, 9):
                c.number_format = '€ #,##0.00'
                c.alignment = Alignment(horizontal="right", vertical="center")
            elif ci in (10, 11):
                c.number_format = '+0.0"%";-0.0"%";"—"'
                c.alignment = Alignment(horizontal="right", vertical="center")
                if val is not None:
                    if val > 0.5:
                        c.font = Font(size=9, color="9C0006", bold=True)
                    elif val < -0.5:
                        c.font = Font(size=9, color="2E7D32", bold=True)
            elif ci == 12:
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif ci == 13:
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.font = Font(name="Menlo", size=12, color=BALLIU_BLUE)
            elif ci in (5, 6):
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif ci == 7:
                c.alignment = Alignment(horizontal="center", vertical="center")
                if estado == "NUEVO":
                    c.font = Font(size=9, color="2E7D32", bold=True)
                elif estado == "DESCATALOGADO":
                    c.font = Font(size=9, color="666666", italic=True)
                else:
                    c.font = Font(size=9, color="2E7D32")
            elif ci == 4:
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")
        rn += 1

    last_data = rn - 1

    total_row = rn
    label = ws.cell(row=total_row, column=2, value="TOTAL / MEDIA")
    label.font = Font(bold=True, size=10)
    label.fill = PatternFill("solid", fgColor=TOTAL_BG)
    label.alignment = Alignment(horizontal="right", vertical="center")
    label.border = BORDER

    def total_cell(col_idx, formula, fmt):
        c = ws.cell(row=total_row, column=col_idx, value=formula)
        c.number_format = fmt
        c.font = Font(bold=True, size=10)
        c.fill = PatternFill("solid", fgColor=TOTAL_BG)
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.border = BORDER

    for ci in (8, 9):
        col = get_column_letter(ci)
        total_cell(ci, f"=SUM({col}{HEADER_ROW+1}:{col}{last_data})", '€ #,##0.00')
    for ci in (10, 11):
        col = get_column_letter(ci)
        total_cell(ci, f"=AVERAGE({col}{HEADER_ROW+1}:{col}{last_data})", '+0.0"%";-0.0"%";"—"')
    col_n = get_column_letter(12)
    total_cell(12, f"=SUM({col_n}{HEADER_ROW+1}:{col_n}{last_data})", '0')

    ws.auto_filter.ref = f"A{HEADER_ROW}:{get_column_letter(len(HEADERS_SEG))}{last_data}"
    ws.freeze_panes = "E6"

    # Color scale sobre Δ Coste % vs origen (col 11) — más rojo cuanto más sube
    delta_col = get_column_letter(11)
    ws.conditional_formatting.add(
        f"{delta_col}{HEADER_ROW+1}:{delta_col}{last_data}",
        ColorScaleRule(
            start_type="num", start_value="-20", start_color="63BE7B",
            mid_type="num",   mid_value="0",    mid_color="FFEB84",
            end_type="num",   end_value="80",   end_color="F8696B",
        )
    )

    return last_data - HEADER_ROW


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not XLSX.exists():
        sys.exit(f"No existe {XLSX}")
    if not BALLIU_DIR.exists():
        sys.exit(f"No existe {BALLIU_DIR}")

    print(f"Leyendo PDFs de {BALLIU_DIR.relative_to(BASE)}...")
    pdfs = find_dated_pdfs(BALLIU_DIR)
    if not pdfs:
        sys.exit("No se encontraron PDFs con prefijo YYYYMMDD")

    snapshots = []
    for fecha, path in pdfs:
        rows = extract_tarifa(path)
        rows = assign_ord(rows)
        snapshots.append((fecha, rows))
        print(f"  {fecha}: {len(rows)} filas  ({path.name})")

    products = build_data(snapshots)
    print(f"\n{len(products)} combinaciones únicas (Producto+Variante+Grupo+Ord)")

    print(f"\nAbriendo {XLSX.name}...")
    wb = openpyxl.load_workbook(XLSX)
    print(f"  Hojas existentes: {wb.sheetnames}")

    n_hist = write_historico(wb, products)
    print(f"\n✓ 'Balliu Histórico' regenerado — {n_hist} filas")

    n_seg = write_seguimiento(wb, snapshots, products)
    print(f"✓ 'Balliu Seguimiento' regenerado — {n_seg} filas")

    wb.save(XLSX)
    print(f"\n✅ {XLSX.name} actualizado")
    print(f"   Hojas finales: {wb.sheetnames}")


if __name__ == "__main__":
    main()
