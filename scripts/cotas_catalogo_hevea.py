#!/usr/bin/env python3
"""
Extrae del catalogo PDF de Hevea las COTAS de cada pieza y la FORMULA de composicion de cada set.

Por que existe: los CSV del proveedor no traen medidas para los SETS ("xx"), pero el catalogo si:
cada serie lleva sus pictogramas ("A- BOLONIA XL - 1 / an 78 x f 84 x al 104 cm") y una tabla de
tarifas con la formula ("2XA+C+D BOLONIA XL-8 SET SOFA 3 PLAZAS ... 3890"). Con las dos cosas se
sabe que entra en un lote y cuanto mide cada pieza, sin deducir nada de una foto.

  python3 scripts/cotas_catalogo_hevea.py                 # informe por serie
  python3 scripts/cotas_catalogo_hevea.py --json          # escribe docs/santavila/_cotas_hevea.json
  python3 scripts/cotas_catalogo_hevea.py BOLONIA         # solo una serie
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "proveedores_raw", "hevea", "OK-h26-09-ENE_BAJA (1).pdf")

RE_PIEZA  = re.compile(r"^([A-Z])-\s*([A-ZÁÉÍÓÚÑ0-9 /\-]+?)\s*-?\s*(\d+)?$")
RE_MEDIDA = re.compile(r"an\s*(\d+)\s*x\s*f\s*(\d+)\s*x\s*al\s*(\d+)\s*cm", re.I)
RE_DIAM   = re.compile(r"di\s*(\d+)\s*Ø?\s*x\s*al\s*(\d+)\s*cm", re.I)
RE_TARIFA = re.compile(r"^([0-9xXA-Z+ ]+?)\s+([A-ZÁÉÍÓÚÑ0-9 \-/]+?)\s+(?:SET\s+)?[A-Z]{0,2}\d{3,5}")

def paginas():
    try: from pypdf import PdfReader
    except ImportError: from PyPDF2 import PdfReader
    for i, p in enumerate(PdfReader(PDF).pages):
        yield i + 1, (p.extract_text() or "")

def extraer():
    series = {}
    for n, texto in paginas():
        lineas = [l.strip() for l in texto.split("\n") if l.strip()]
        serie = None
        for l in lineas:
            if l.upper().startswith("SERIE "):
                serie = l.replace("SERIE", "").strip().replace("SOFÁ ", "").replace("SOFA ", "")
                series.setdefault(serie, {"pagina": n, "piezas": [], "medidas": [], "sets": []})
            if serie is None:
                continue
            s = series[serie]
            for m in RE_MEDIDA.finditer(l):
                s["medidas"].append(f"{m.group(1)} x {m.group(2)} x {m.group(3)} cm")
            for m in RE_DIAM.finditer(l):
                s["medidas"].append(f"{m.group(1)} cm Ø x {m.group(2)} cm")
            for trozo in re.split(r"\s{2,}", l):
                mm = re.match(r"^([A-Z])-\s*(.+)$", trozo.strip())
                if mm and len(mm.group(2)) < 40:
                    s["piezas"].append(f"{mm.group(1)}- {mm.group(2).strip()}")
            if re.match(r"^\d?[xX]?[A-Z](\s*\+\s*[A-Z0-9x ]+)+\s", l):
                s["sets"].append(l[:110])
    return series

def main():
    if not os.path.exists(PDF):
        sys.exit(f"no encuentro el catalogo: {PDF}")
    series = extraer()
    filtro = next((a.upper() for a in sys.argv[1:] if not a.startswith("--")), None)
    for nombre, s in sorted(series.items()):
        if filtro and filtro not in nombre.upper(): continue
        if not s["medidas"] and not s["sets"]: continue
        print(f"\n=== {nombre}   (pagina {s['pagina']})")
        for p in dict.fromkeys(s["piezas"]): print(f"   {p}")
        for m in dict.fromkeys(s["medidas"]): print(f"      {m}")
        for st in dict.fromkeys(s["sets"]): print(f"   SET  {st}")
    if "--json" in sys.argv:
        dest = os.path.join(ROOT, "docs", "santavila", "_cotas_hevea.json")
        json.dump(series, open(dest, "w"), ensure_ascii=False, indent=1)
        print(f"\n-> {dest}")

if __name__ == "__main__":
    main()
