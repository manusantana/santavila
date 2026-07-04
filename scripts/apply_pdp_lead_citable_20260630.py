#!/usr/bin/env python3
"""
Añade una apertura citable (respuesta directa en negrita) a las fichas ACTIVE que
todavía abren con prosa — Santavila · 2026-06-30.

REGLA DURA: 0 invención. El lead se compone SOLO con hechos ya presentes en la ficha:
  - tipo (productType) · material (título/desc) · modelo (título) · medida (TAL CUAL en el título)
No se parsea el handle (poco fiable: "7070" ≠ Ø70). Si el título no trae medida, el lead no la inventa.

Antepone <p><strong>LEAD</strong></p> y conserva intacta la descripción existente.
Solo toca fichas sin apertura en negrita (las que ya la tienen se saltan).

  .venv/bin/python scripts/apply_pdp_lead_citable_20260630.py            # dry-run
  .venv/bin/python scripts/apply_pdp_lead_citable_20260630.py --show H   # ver before/after
  .venv/bin/python scripts/apply_pdp_lead_citable_20260630.py --apply    # aplica
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
SHOW = sys.argv[sys.argv.index("--show") + 1] if "--show" in sys.argv else None


def size_from_title(title):
    m = re.findall(r"Ø?\d{2,3}(?:[×x/]\d{2,3})?\s*cm|Ø\s*\d{2,3}", title)
    return m[0].replace("x", "×").strip() if m else None


def model_from_title(title):
    segs = re.split(r"[·|]", title)
    last = segs[-1].strip()
    if last and not re.search(r"\d|cm|plazas|estilo|bicolor", last, re.I) and 0 < len(last.split()) <= 2:
        return last
    return None


def material_of(title, desc):
    t = (title + " " + desc).lower()
    if "hpl" in t:
        return "hpl"
    if "aluminio" in t:
        return "aluminio"
    if "resina" in t or "polipropileno" in t:
        return "resina"
    if "madera" in t or "teca" in t:
        return "madera"
    return None


MAT_STR = {"aluminio": "de aluminio", "resina": "de resina", "hpl": "con tablero HPL", "madera": "de madera"}

# (noun, género, cláusula de uso) por productType
FAM = {
    "Sofá": ("Sofá de exterior", "o", "pensado para crear una zona de descanso al aire libre en terraza, porche o jardín"),
    "Sofa": ("Sofá de exterior", "o", "pensado para crear una zona de descanso al aire libre en terraza, porche o jardín"),
    "Conjunto sofá": ("Conjunto de sofá de exterior", "o", "pensado para resolver una zona de estar completa en terraza, porche o jardín"),
    "Conjunto rinconera": ("Conjunto rinconera de exterior", "o", "pensado para una zona lounge amplia en terraza o jardín"),
    "Sillón": ("Sillón de exterior", "o", "pensado para sumar un asiento cómodo en terraza, porche o jardín"),
    "Reposapiés": ("Reposapiés de exterior", "o", "pensado para completar un asiento lounge en terraza o jardín"),
    "Cama balinesa": ("Cama balinesa de exterior", "a", "pensada para descansar y tumbarse al aire libre en jardín, porche o zona de piscina"),
    "Banco": ("Banco de exterior", "o", "pensado para asiento en jardín, porche o terraza"),
    "Balancín": ("Balancín de exterior", "o", "pensado para relax al aire libre en jardín o porche"),
    "Tumbona": ("Tumbona de exterior", "a", "pensada para descansar en piscina, terraza o jardín"),
    "Mini tumbona": ("Tumbona compacta de exterior", "a", "pensada para descansar en poco espacio, en piscina, terraza o balcón"),
    "Silla": ("Silla de exterior", "a", "pensada para completar comedor o zona de estar en terraza y jardín"),
    "Parasol": ("Parasol de exterior", "o", "para completar una zona de sombra en terraza, jardín o patio"),
    "Mobiliario exterior": (None, "o", "pensado como pieza auxiliar en terraza, jardín o porche"),
}


def noun_for(product):
    ptype = product["productType"]
    title = product["title"].lower()
    if ptype == "Mesa":
        if "auxiliar" in title:
            return ("Mesa auxiliar de exterior", "a", "pensada como mesa de apoyo junto a asientos o tumbonas en exterior")
        if "centro" in title:
            return ("Mesa de centro de exterior", "a", "pensada como mesa de apoyo en una zona lounge de exterior")
        return ("Mesa de exterior", "a", "pensada para crear una superficie útil en terraza, jardín o porche")
    if ptype in ("Mesa centro",):
        return ("Mesa de centro de exterior", "a", "pensada como mesa de apoyo en una zona lounge de exterior")
    if ptype in ("Mesa comedor",):
        return ("Mesa de comedor de exterior", "a", "pensada para comer al aire libre en terraza, jardín o porche")
    if ptype == "Mobiliario exterior":
        # taburete u otros: intenta nombrar por el título
        if "taburete" in title:
            return ("Taburete de exterior", "o", "pensado para asiento o apoyo auxiliar en exterior")
        return ("Pieza de mobiliario de exterior", "a", "pensada como complemento en terraza, jardín o porche")
    return FAM.get(ptype, (None, "o", "pensado para uso en terraza, jardín o porche"))


def build_lead(product):
    title = product["title"]
    desc = product["descriptionHtml"] or ""
    noun, gen, uso = noun_for(product)
    if not noun:
        return None
    mat = material_of(title, desc)
    size = size_from_title(title)
    model = model_from_title(title)
    parts = [noun]
    if mat:
        parts.append(MAT_STR[mat])
    if size:
        parts.append(f"de {size}")
    lead = " ".join(parts)
    if model:
        lead += f", modelo {model}"
    lead += f", {uso}."
    # Mayúscula inicial ya viene del noun.
    return f"<p><strong>{lead}</strong></p>"


GET = """
query($c:String){products(first:120,after:$c){pageInfo{hasNextPage endCursor}nodes{
  id handle status productType title descriptionHtml}}}
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


def is_bold_open(h):
    return bool(re.match(r"\s*<p>\s*<strong>", h or ""))


def fetch_active():
    out, c = [], None
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
    active = fetch_active()
    targets = [p for p in active if not is_bold_open(p["descriptionHtml"])]

    if SHOW:
        p = next((x for x in active if x["handle"] == SHOW), None)
        if not p:
            sys.exit("no encontrado")
        lead = build_lead(p)
        combined = re.sub(r"\s+", " ", (lead or "") + p["descriptionHtml"])[:600]
        print(f"### {p['title']}  [{p['productType']}]")
        print(f"\nLEAD nuevo:\n{lead}")
        print(f"\nquedaría:\n{combined}")
        return

    plan, skip = [], []
    for p in targets:
        lead = build_lead(p)
        if not lead:
            skip.append(p["handle"]); continue
        if lead in (p["descriptionHtml"] or ""):
            continue
        plan.append((p, lead + p["descriptionHtml"]))

    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN'} - apertura citable")
    print(f"Fichas sin apertura: {len(targets)} · con lead generado: {len(plan)} · sin plantilla de familia: {len(skip)}")
    if skip:
        print("  (saltadas por no tener familia mapeada):", skip)
    for p, _ in plan:
        print(f"  + {p['productType']:<16} {p['handle']}")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = os.path.join(ROOT, "content", "descriptions", f"backup_pdp_lead_{ts}.json")
    with open(bpath, "w", encoding="utf-8") as fh:
        json.dump({p["handle"]: {"id": p["id"], "descriptionHtml": p["descriptionHtml"]} for p, _ in plan}, fh, ensure_ascii=False, indent=2)
    print(f"Backup -> {bpath}")

    if APPLY:
        print("\nAplicando (antepone lead; conserva el resto)...")
        errs = 0
        for p, new in plan:
            try:
                res = gql(SET, {"input": {"id": p["id"], "descriptionHtml": new}})["productUpdate"]
            except Exception as exc:
                print(f"X {p['handle']}: {exc}"); errs += 1; continue
            if res["userErrors"]:
                print(f"! {p['handle']}: {res['userErrors']}"); errs += 1
        print(f"Aplicado - errores: {errs}")
    else:
        print("\nRevisa con --show <handle> y aplica con --apply.")


if __name__ == "__main__":
    main()
