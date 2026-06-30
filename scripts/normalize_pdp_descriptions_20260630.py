#!/usr/bin/env python3
"""
Saneamiento de descripciones de producto ACTIVE (Santavila) — 2026-06-30.

NO reescribe la copy de fabricante (que es buena y específica). Solo corrige dos
defectos de migración:
  1) Ligaduras tipográficas heredadas de PDF: ﬁ→fi, ﬂ→fl, ﬀ→ff, ﬃ→ffi, ﬄ→ffl.
  2) Fragmentos de specs sueltos al final (<p>Tablero</p><p>HPL</p>... <p>Dimensiones: ...</p>)
     se convierten en un bloque "Ficha técnica" estructurado (h2 + ul) más citable.

Conservador: solo toca el sufijo final de <p> cortos que parecen specs; el resto
del HTML se deja intacto. Por defecto dry-run.

  .venv/bin/python scripts/normalize_pdp_descriptions_20260630.py            # dry-run
  .venv/bin/python scripts/normalize_pdp_descriptions_20260630.py --apply    # aplica
  .venv/bin/python scripts/normalize_pdp_descriptions_20260630.py --show H    # ver before/after de un handle
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
SHOW = None
if "--show" in sys.argv:
    SHOW = sys.argv[sys.argv.index("--show") + 1]

LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}

# Etiquetas estructurales que NO son material en sí, sino cabecera del bloque de specs.
STRUCT_LABELS = {"tablero", "tablillas", "estructura", "asiento", "respaldo"}
# Palabras que delatan una línea de material/acabado (para clasificar como fragmento).
MATERIAL_HINT = re.compile(
    r"\b(aluminio|hpl|resina|werzalit|madera|acero|tejido|acr[ií]lico|n[áa]utico|"
    r"polipropileno|textil|fibra|cemento|hormig[óo]n|classic|mate|texturizado|cepillado)\b",
    re.I,
)


def fix_ligatures(text):
    for k, v in LIGATURES.items():
        text = text.replace(k, v)
    return text


def split_paragraphs(html):
    """Devuelve lista de (inner_text, raw_block) para cada <p>...</p> de nivel superior.
    Si hay <ul>/<h2>, los trata como bloques opacos que rompen el sufijo de specs."""
    # Tokeniza en bloques <p>..</p>, <ul>..</ul>, <h2>..</h2>, etc.
    # finditer + group(0): findall con grupo de captura devolvería solo el nombre de la etiqueta.
    return [m.group(0) for m in re.finditer(r"<(p|ul|ol|h2|h3|div)[^>]*>.*?</\1>", html, re.S | re.I)]


def inner(block):
    return re.sub(r"<[^>]+>", " ", block).strip()


def is_spec_fragment(block):
    """True si el bloque es un <p> corto que parece spec suelta o la línea Dimensiones."""
    if not re.match(r"^\s*<p[ >]", block, re.I):
        return False
    txt = inner(block)
    low = txt.lower()
    if low.startswith("dimensiones") or low.startswith("peso:") or low.startswith("diámetro") or low.startswith("diametro"):
        return True
    # corto, sin punto final, y o bien etiqueta estructural o material
    words = txt.split()
    if len(words) <= 6 and not txt.endswith("."):
        if low in STRUCT_LABELS or MATERIAL_HINT.search(txt):
            return True
    return False


def build_ficha(frag_texts):
    """Construye <h2>Ficha técnica</h2><ul>... a partir de los textos de fragmentos."""
    materiales = []
    dimensiones = None
    for t in frag_texts:
        low = t.lower()
        if low.startswith("dimensiones") or low.startswith("diámetro") or low.startswith("diametro") or low.startswith("peso:"):
            # normaliza: quita prefijo "Dimensiones:" redundante y "Peso: N/D"
            val = re.sub(r"^\s*Dimensiones\s*:?\s*", "", t, flags=re.I).strip()
            # elimina segmentos "Peso: N/D kg" o "Alto: N/D"
            parts = [s.strip() for s in val.split("|")]
            parts = [s for s in parts if not re.search(r":\s*N/?D", s, re.I)]
            val = " | ".join(parts)
            if val:
                dimensiones = val
        elif low in STRUCT_LABELS:
            continue  # cabecera vacía, se ignora
        else:
            # material/acabado real
            if t not in materiales:
                materiales.append(t)
    items = []
    if materiales:
        items.append(f"<strong>Materiales y acabados:</strong> {', '.join(materiales)}.")
    if dimensiones:
        items.append(f"<strong>Dimensiones:</strong> {dimensiones}.")
    if not items:
        return ""
    return "<h2>Ficha técnica</h2><ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def normalize(html):
    if not html:
        return html, False
    original = html
    html = fix_ligatures(html)
    blocks = split_paragraphs(html)
    if not blocks:
        return html, html != original
    # Encuentra el sufijo maximal de fragmentos de spec al final.
    n = len(blocks)
    i = n
    while i > 0 and is_spec_fragment(blocks[i - 1]):
        i -= 1
    if i == n:
        # no hay fragmentos; solo posible fix de ligadura
        return html, html != original
    frag_blocks = blocks[i:]
    frag_texts = [inner(b) for b in frag_blocks]
    ficha = build_ficha(frag_texts)
    # Reconstruye: parte el html en (antes del primer fragmento) + ficha.
    # Localiza dónde empieza el primer fragmento dentro del html.
    first_frag = frag_blocks[0]
    idx = html.rfind(first_frag)
    if idx == -1:
        return html, html != original
    head = html[:idx].rstrip()
    new_html = head + ("" if not ficha else ficha)
    return new_html, new_html != original


GET = """
query($c:String){products(first:200,after:$c){pageInfo{hasNextPage endCursor}nodes{id handle title status productType descriptionHtml seo{description}}}}
"""
SET = """
mutation($input:ProductInput!){productUpdate(input:$input){product{id handle}userErrors{field message}}}
"""


def gql(query, variables, attempts=3):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    data = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            break
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def words(value):
    return len(re.sub(r"<[^>]+>", " ", value or "").split())


def fetch_all_active():
    out = []
    c = None
    while True:
        pg = gql(GET, {"c": c})["products"]
        out += [p for p in pg["nodes"] if p["status"] == "ACTIVE"]
        if not pg["pageInfo"]["hasNextPage"]:
            break
        c = pg["pageInfo"]["endCursor"]
    return out


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacio")
    active = fetch_all_active()

    if SHOW:
        p = next((x for x in active if x["handle"] == SHOW), None)
        if not p:
            sys.exit(f"no encontrado: {SHOW}")
        new, changed = normalize(p["descriptionHtml"])
        print(f"### {p['title']}  ({p['handle']})  changed={changed}")
        print("\n--- ANTES ---\n" + re.sub(r"\s+", " ", p["descriptionHtml"]))
        print("\n--- DESPUÉS ---\n" + re.sub(r"\s+", " ", new))
        return

    changes = []
    for p in active:
        new, changed = normalize(p["descriptionHtml"])
        if changed:
            changes.append((p, new))

    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN'} - normalización descripciones ACTIVE")
    print(f"Productos a tocar: {len(changes)} / {len(active)} ACTIVE\n")
    for p, new in changes:
        print(f"- {p['handle']:<58} {words(p['descriptionHtml']):>3}p -> {words(new):>3}p")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = os.path.join(ROOT, "content", "descriptions")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"backup_normalize_descriptions_{ts}.json")
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump({p["handle"]: {"id": p["id"], "title": p["title"], "descriptionHtml": p["descriptionHtml"]} for p, _ in changes}, fh, ensure_ascii=False, indent=2)
    print(f"\nBackup -> {backup_path}")

    if APPLY:
        print("\nAplicando (solo descriptionHtml; status y SEO intactos)...")
        errs = 0
        for p, new in changes:
            try:
                res = gql(SET, {"input": {"id": p["id"], "descriptionHtml": new}})["productUpdate"]
            except Exception as exc:
                print(f"X {p['handle']}: {exc}")
                errs += 1
                continue
            if res["userErrors"]:
                print(f"! {p['handle']}: {res['userErrors']}")
                errs += 1
            else:
                print(f"OK {p['handle']}")
        print(f"\nAplicado - errores: {errs}")
    else:
        print("\nRevisa con --show <handle> y aplica con --apply.")


if __name__ == "__main__":
    main()
