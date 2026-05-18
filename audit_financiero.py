#!/usr/bin/env python3
"""
audit_financiero.py

Auditoría financiera completa de la tienda Shopify Santavila.
Detecta productos con márgenes insuficientes o pérdidas.

Fuentes:
  - Excel Santavila.xlsx hoja "20260508 -Todos "
  - Shopify GraphQL API (productos ACTIVE)

Output: audit_financiero.csv + resumen en consola
"""
from __future__ import annotations

import csv
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

import openpyxl

# ──────────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
XLSX = BASE / "Santavila.xlsx"
TODOS_SHEET = "20260508 -Todos "
OUTPUT_CSV = BASE / "audit_financiero.csv"
ENV_FILE = BASE / ".envlocal"

SHOP = "mueblesexterior.myshopify.com"
API_URL = f"https://{SHOP}/admin/api/2026-01/graphql.json"

# Parámetros de negocio
IVA = 1.21
SHOPIFY_FEE_PCT = 0.021
SHOPIFY_FEE_FIXED = 0.30
FREE_SHIPPING_THRESHOLD = 500.0

SHIPPING_RATES = {
    "envio:xs": 9.95,
    "envio:m": 29.95,
    "envio:l": 57.95,
}

ALERT_LEVELS = {
    "CRITICO": "🔴 CRÍTICO",
    "ALERTA":  "🟠 ALERTA",
    "AVISO":   "🟡 AVISO",
    "OK":      "🟢 OK",
    "SIN_COSTE": "⚫ SIN_COSTE",
}

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def load_token() -> str:
    token = None
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("SHOPIFY_ACCESS_TOKEN="):
                token = line.split("=", 1)[1].strip()
                break
    if not token:
        print("ERROR: no se encontró SHOPIFY_ACCESS_TOKEN en .envlocal", file=sys.stderr)
        sys.exit(1)
    return token


def shopify_query(token: str, query: str, variables: dict | None = None, retries: int = 3) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        },
        method="POST",
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
                if "errors" in data:
                    raise RuntimeError(f"GraphQL errors: {data['errors']}")
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 2 ** attempt
                print(f"  [rate-limit] esperando {wait}s…", file=sys.stderr)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Máximo de reintentos alcanzado")


# ──────────────────────────────────────────────
# CARGA EXCEL
# ──────────────────────────────────────────────

def load_excel() -> dict[str, dict]:
    """
    Devuelve dict keyed by SKU (col C) con:
      handle, sku, cost_net, pvp_iva, psy_price, margen_e, margen_pct, carrier_cost
    Filas sin handle o SKU se ignoran.
    """
    print("Cargando Excel…")
    wb = openpyxl.load_workbook(str(XLSX), read_only=True, data_only=True)
    ws = wb[TODOS_SHEET]

    rows_by_sku: dict[str, dict] = {}
    rows_by_handle: dict[str, dict] = {}

    for i, row in enumerate(ws.iter_rows(min_row=3, values_only=True)):
        # Col A=0, B=1 handle, C=2 sku, D=3 nombre,
        # E=4 coste_neto_sin_iva, F=5 pvp_con_iva, G=6 psy_price,
        # H=7 margen_e, I=8 margen_pct, K=10 coste_envio
        if len(row) < 11:
            continue
        handle = row[1]
        sku = row[2]
        if not handle and not sku:
            continue

        handle = str(handle).strip() if handle else ""
        sku = str(sku).strip() if sku else ""

        def safe_float(v):
            if v is None:
                return None
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        record = {
            "handle": handle,
            "sku": sku,
            "cost_net": safe_float(row[4]),       # E: coste neto sin IVA
            "pvp_iva": safe_float(row[5]),         # F: PVP con IVA
            "psy_price": safe_float(row[6]),       # G: precio psicológico
            "margen_e": safe_float(row[7]),        # H: margen €
            "margen_pct": safe_float(row[8]),      # I: margen %
            "carrier_cost": safe_float(row[10]),   # K: coste envío transporte
        }
        if sku:
            rows_by_sku[sku] = record
        if handle:
            rows_by_handle[handle] = record

    wb.close()
    print(f"  Excel: {len(rows_by_sku)} SKUs, {len(rows_by_handle)} handles cargados")
    return rows_by_sku, rows_by_handle


# ──────────────────────────────────────────────
# CARGA SHOPIFY
# ──────────────────────────────────────────────

PRODUCTS_QUERY = """
query getProducts($cursor: String) {
  products(first: 50, after: $cursor, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        title
        handle
        tags
        variants(first: 100) {
          edges {
            node {
              id
              sku
              price
              compareAtPrice
              inventoryItem {
                unitCost { amount currencyCode }
              }
            }
          }
        }
      }
    }
  }
}
"""


def load_shopify_products(token: str) -> list[dict]:
    """Descarga todos los productos ACTIVE de Shopify con sus variantes."""
    print("Descargando productos Shopify…")
    products = []
    cursor = None
    page = 0

    while True:
        page += 1
        variables = {"cursor": cursor} if cursor else {}
        data = shopify_query(token, PRODUCTS_QUERY, variables)
        page_data = data["data"]["products"]

        for edge in page_data["edges"]:
            prod = edge["node"]
            tags = [t.strip().lower() for t in prod.get("tags", [])]
            variants = []
            for ve in prod["variants"]["edges"]:
                v = ve["node"]
                cost_raw = None
                if v.get("inventoryItem") and v["inventoryItem"].get("unitCost"):
                    cost_raw = v["inventoryItem"]["unitCost"]["amount"]
                variants.append({
                    "variant_id": v["id"],
                    "sku": (v.get("sku") or "").strip(),
                    "price": float(v["price"]) if v.get("price") else 0.0,
                    "compare_at_price": float(v["compareAtPrice"]) if v.get("compareAtPrice") else None,
                    "shopify_cost": float(cost_raw) if cost_raw else None,
                })
            products.append({
                "product_id": prod["id"],
                "title": prod["title"],
                "handle": prod["handle"],
                "tags": tags,
                "variants": variants,
            })

        print(f"  Página {page}: {len(page_data['edges'])} productos (total={len(products)})")

        if not page_data["pageInfo"]["hasNextPage"]:
            break
        cursor = page_data["pageInfo"]["endCursor"]
        time.sleep(0.3)

    print(f"  Total Shopify: {len(products)} productos ACTIVE")
    return products


# ──────────────────────────────────────────────
# AUDITORÍA POR VARIANTE
# ──────────────────────────────────────────────

def get_shipping_category(tags: list[str]) -> tuple[str, float | None]:
    """Devuelve (categoria_tag, tarifa_cobrada_cliente)."""
    for tag in tags:
        if tag in SHIPPING_RATES:
            return tag, SHIPPING_RATES[tag]
    return "sin_tag", None


def classify_alert(net_margin_e: float | None, net_margin_pct: float | None,
                    price: float, cost_net: float | None, has_cost: bool) -> str:
    if not has_cost:
        return "SIN_COSTE"
    if cost_net is not None and price < cost_net * IVA:
        return "CRITICO"
    if net_margin_e is not None and net_margin_e < 0:
        return "CRITICO"
    if net_margin_pct is None:
        return "SIN_COSTE"
    if net_margin_pct < 10.0:
        return "ALERTA"
    if net_margin_pct < 20.0:
        return "AVISO"
    return "OK"


def audit_variant(
    handle: str,
    sku: str,
    titulo: str,
    price: float,
    shopify_cost: float | None,
    tags: list[str],
    excel_row: dict | None,
) -> dict:
    """Calcula márgenes y nivel de alerta para una variante."""

    # ── Coste neto ──
    cost_net = None
    fuente_cost = "ninguna"
    notas_list = []

    if excel_row is not None:
        xls_cost = excel_row.get("cost_net")
        if xls_cost is not None and xls_cost > 0:
            cost_net = xls_cost
            fuente_cost = "excel"
    if cost_net is None and shopify_cost is not None and shopify_cost > 0:
        cost_net = shopify_cost
        fuente_cost = "shopify"

    has_cost = cost_net is not None

    # ── Coste de transporte (carrier) ──
    carrier_cost = 0.0
    if excel_row is not None:
        xls_carrier = excel_row.get("carrier_cost")
        if xls_carrier is not None:
            carrier_cost = float(xls_carrier)
    # Si no hay Excel, asumimos 0

    # ── Categoría envío y tarifa cobrada ──
    cat_envio, shipping_rate = get_shipping_category(tags)

    if shipping_rate is None:
        # Sin tag de envío: usamos tarifa M como estimación conservadora
        shipping_rate = SHIPPING_RATES["envio:m"]
        notas_list.append("sin tag envío, estimado M")

    # ── Cálculos financieros ──
    net_revenue = price / IVA
    shopify_fee = price * SHOPIFY_FEE_PCT + SHOPIFY_FEE_FIXED

    if price < FREE_SHIPPING_THRESHOLD:
        # Escenario A: cliente paga envío
        escenario = "A_cliente_paga"
        if has_cost:
            margin = net_revenue - cost_net - shopify_fee + (shipping_rate - carrier_cost)
        else:
            margin = None
    else:
        # Escenario B: envío gratis, Santavila absorbe
        escenario = "B_envio_gratis"
        if has_cost:
            margin = net_revenue - cost_net - shopify_fee - carrier_cost
        else:
            margin = None

    net_margin_e = margin
    net_margin_pct = (margin / net_revenue * 100) if (margin is not None and net_revenue > 0) else None
    gross_margin_pct = ((net_revenue - cost_net) / net_revenue * 100) if (has_cost and net_revenue > 0) else None

    nivel = classify_alert(net_margin_e, net_margin_pct, price, cost_net, has_cost)

    if nivel == "CRITICO" and has_cost and price < cost_net * IVA:
        notas_list.append(f"precio ({price:.2f}€) < coste*IVA ({cost_net * IVA:.2f}€)")
    if nivel == "CRITICO" and net_margin_e is not None and net_margin_e < 0:
        notas_list.append(f"margen neto negativo: {net_margin_e:.2f}€")

    def fmt(v, decimals=2):
        if v is None:
            return ""
        return f"{v:.{decimals}f}"

    return {
        "handle": handle,
        "sku": sku,
        "titulo": titulo,
        "categoria_envio": cat_envio,
        "price": fmt(price),
        "cost_net": fmt(cost_net),
        "fuente_cost": fuente_cost,
        "gross_margin_%": fmt(gross_margin_pct),
        "net_margin_%": fmt(net_margin_pct),
        "net_margin_€": fmt(net_margin_e),
        "carrier_cost": fmt(carrier_cost, 0),
        "shopify_fee": fmt(shopify_fee),
        "escenario": escenario,
        "nivel_alerta": nivel,
        "notas": "; ".join(notas_list),
        # valores numéricos para ordenar
        "_net_margin_e": net_margin_e,
        "_net_margin_pct": net_margin_pct,
        "_price": price,
    }


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    token = load_token()
    excel_by_sku, excel_by_handle = load_excel()
    products = load_shopify_products(token)

    print("\nAuditando variantes…")
    rows = []
    unmatched_skus = []

    for prod in products:
        tags = prod["tags"]
        for var in prod["variants"]:
            sku = var["sku"]
            handle = prod["handle"]
            titulo = prod["title"]
            price = var["price"]
            shopify_cost = var["shopify_cost"]

            # Buscar en Excel: primero por SKU, luego por handle
            excel_row = excel_by_sku.get(sku) or excel_by_handle.get(handle)
            if excel_row is None:
                unmatched_skus.append(sku or handle)

            result = audit_variant(
                handle=handle,
                sku=sku,
                titulo=titulo,
                price=price,
                shopify_cost=shopify_cost,
                tags=tags,
                excel_row=excel_row,
            )
            rows.append(result)

    # ── Guardar CSV ──
    CSV_COLS = [
        "handle", "sku", "titulo", "categoria_envio",
        "price", "cost_net", "fuente_cost",
        "gross_margin_%", "net_margin_%", "net_margin_€",
        "carrier_cost", "shopify_fee", "escenario", "nivel_alerta", "notas",
    ]
    with open(str(OUTPUT_CSV), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nCSV guardado: {OUTPUT_CSV}")

    # ── Estadísticas ──
    total = len(rows)
    dist: dict[str, list] = {k: [] for k in ALERT_LEVELS}

    for r in rows:
        dist[r["nivel_alerta"]].append(r)

    print("\n" + "═" * 70)
    print("  AUDITORÍA FINANCIERA SANTAVILA — RESUMEN")
    print("═" * 70)
    print(f"  Total variantes analizadas: {total}")
    print(f"  Productos sin match en Excel: {len(unmatched_skus)}")
    print()
    print("  DISTRIBUCIÓN POR NIVEL:")
    for key, label in ALERT_LEVELS.items():
        count = len(dist[key])
        pct = count / total * 100 if total else 0
        bar = "█" * int(pct / 2)
        print(f"    {label:22s}  {count:4d}  ({pct:5.1f}%)  {bar}")

    # ── CRÍTICOS ──
    criticos = sorted(dist["CRITICO"], key=lambda r: (r["_net_margin_e"] or 0))
    print(f"\n{'─'*70}")
    print(f"  🔴 CRÍTICOS ({len(criticos)} variantes)")
    print(f"{'─'*70}")
    if criticos:
        print(f"  {'Handle / SKU':<45} {'Price':>8} {'Cost':>8} {'Margin€':>9}  Notas")
        print(f"  {'-'*45} {'-'*8} {'-'*8} {'-'*9}")
        for r in criticos:
            id_str = (r['sku'] or r['handle'])[:44]
            print(f"  {id_str:<45} {r['price']:>8} {r['cost_net']:>8} {r['net_margin_€']:>9}  {r['notas']}")
    else:
        print("  (ninguno)")

    # ── ALERTAS ──
    alertas = sorted(dist["ALERTA"], key=lambda r: (r["_net_margin_pct"] or 0))
    print(f"\n{'─'*70}")
    print(f"  🟠 ALERTAS — margen neto 0-10% ({len(alertas)} variantes)")
    print(f"{'─'*70}")
    if alertas:
        print(f"  {'Handle / SKU':<45} {'Price':>8} {'Margin%':>8} {'Margin€':>9}")
        print(f"  {'-'*45} {'-'*8} {'-'*8} {'-'*9}")
        for r in alertas:
            id_str = (r['sku'] or r['handle'])[:44]
            print(f"  {id_str:<45} {r['price']:>8} {r['net_margin_%']:>8} {r['net_margin_€']:>9}")
    else:
        print("  (ninguno)")

    # ── TOP 10 MÁS PREOCUPANTES ──
    def sort_key(r):
        nivel_order = {"CRITICO": 0, "ALERTA": 1, "AVISO": 2, "SIN_COSTE": 3, "OK": 4}
        order = nivel_order.get(r["nivel_alerta"], 5)
        margin = r["_net_margin_e"] if r["_net_margin_e"] is not None else 9999
        return (order, margin)

    preocupantes = [r for r in rows if r["nivel_alerta"] in ("CRITICO", "ALERTA", "AVISO")]
    preocupantes_sorted = sorted(preocupantes, key=sort_key)[:10]

    print(f"\n{'─'*70}")
    print(f"  TOP 10 PRODUCTOS MÁS PREOCUPANTES")
    print(f"{'─'*70}")
    print(f"  {'#':<3} {'Nivel':<12} {'Handle / SKU':<38} {'Price':>8} {'Cost':>8} {'Gross%':>7} {'Net%':>7} {'Net€':>9}")
    print(f"  {'-'*3} {'-'*12} {'-'*38} {'-'*8} {'-'*8} {'-'*7} {'-'*7} {'-'*9}")
    for i, r in enumerate(preocupantes_sorted, 1):
        id_str = (r['sku'] or r['handle'])[:37]
        nivel_short = r['nivel_alerta']
        print(
            f"  {i:<3} {nivel_short:<12} {id_str:<38} "
            f"{r['price']:>8} {r['cost_net']:>8} "
            f"{r['gross_margin_%']:>7} {r['net_margin_%']:>7} {r['net_margin_€']:>9}"
        )

    # ── SIN COSTE ──
    sin_coste = dist["SIN_COSTE"]
    print(f"\n{'─'*70}")
    print(f"  ⚫ SIN_COSTE — sin datos de coste ({len(sin_coste)} variantes)")
    if sin_coste:
        for r in sin_coste[:20]:
            id_str = (r['sku'] or r['handle'])[:60]
            print(f"    {id_str} | precio={r['price']}")
        if len(sin_coste) > 20:
            print(f"    … y {len(sin_coste) - 20} más (ver CSV)")

    print(f"\n{'═'*70}")
    print(f"  CSV completo: {OUTPUT_CSV}")
    print("═" * 70 + "\n")


if __name__ == "__main__":
    main()
