#!/usr/bin/env python3
"""
Genera FAQ por ficha de producto (metafield santavila.faq, JSON) — Santavila · 2026-06-30.

REGLA DURA: 0 invención. Cada respuesta procede de una fuente documentada de Santavila:
  - /pages/envio, /pages/garantia, /pages/mantenimiento
  - guías del blog (lluvia/sol, tumbona por material, mesa por comensales)
  - el dato real del propio producto (material, medida, "apilable"/"posiciones" si consta)

4 FAQ por ficha (2 de familia/material + garantía + envío). Condicionales
(apilable / respaldo regulable) SOLO si la descripción del producto ya lo menciona.

Por defecto dry-run. Escribe metafield con --apply. Backup del valor previo.

  .venv/bin/python scripts/apply_pdp_faq_20260630.py               # dry-run
  .venv/bin/python scripts/apply_pdp_faq_20260630.py --show HANDLE  # ver FAQ de una ficha
  .venv/bin/python scripts/apply_pdp_faq_20260630.py --apply        # escribe metafield
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

# ------------------- Bloques de respuesta (todos con fuente documentada) -------------------
Q_ENVIO = ("¿Cuánto tarda en llegar el pedido?",
    "La entrega estimada puede llegar hasta 30 días, según disponibilidad del proveedor, "
    "volumen del pedido y ruta logística. En productos grandes o conjuntos completos, ese "
    "margen permite coordinar el transporte con más seguridad.")
Q_GARANTIA = ("¿Qué garantía tiene?",
    "Todos los productos cuentan con la garantía legal aplicable en España y cobertura frente "
    "a defectos de fabricación, con un uso normal y siguiendo las indicaciones de cuidado y "
    "montaje. Las incidencias se gestionan en hola@santavila.com con el número de pedido y fotografías.")
Q_MONTAJE = ("¿Viene montado o hay que montarlo?",
    "Muchos productos están pensados para un montaje sencillo en casa con instrucciones. Si una "
    "pieza necesita una consideración especial, se indica en la ficha o se confirma en la atención "
    "previa a la compra.")

MAT = {
    "aluminio": ("¿Aguanta la lluvia y el sol? ¿Cómo se limpia?",
        "Sí. El aluminio lacado no se oxida, pesa poco y necesita muy poco mantenimiento. Límpialo "
        "con agua, jabón neutro y un paño suave, evitando estropajos abrasivos, y retira salitre o "
        "polvo de forma periódica."),
    "resina": ("¿Aguanta la lluvia y el sol? ¿Cómo se limpia?",
        "Sí. La resina de exterior no absorbe agua y es muy fácil de mantener: agua, jabón suave y "
        "aclarado. Cerca de piscina o costa, límpiala con más frecuencia para retirar cloro o sal, y "
        "evita el calor directo sobre la superficie."),
    "hpl": ("¿El tablero HPL resiste el exterior? ¿Cómo se limpia?",
        "Sí. El tablero HPL resiste muy bien el uso exterior y no se deforma con facilidad. Límpialo "
        "con un paño húmedo y jabón neutro; ante manchas persistentes, actúa pronto y evita productos "
        "que puedan rayar el acabado."),
}

Q_COJINES = ("¿Los cojines y textiles aguantan la lluvia?",
    "Los textiles están preparados para exterior, pero recomendamos guardarlos secos cuando no se "
    "usen durante varios días, especialmente fuera de temporada. No los guardes húmedos, para evitar "
    "olores o moho.")
Q_TUMBONA_MAT = ("¿Es mejor una tumbona de resina o de aluminio?",
    "Ambas van muy bien en exterior: la de aluminio (a menudo con textilene) es ligera, no se oxida y "
    "seca rápido, ideal para mover a diario; la de resina es muy fácil de limpiar y rinde muy bien en "
    "piscina, alquiler turístico y hostelería.")
Q_TUMBONA_PISCINA = ("¿Sirve para piscina o uso profesional/hostelería?",
    "Sí. Resina y aluminio funcionan muy bien junto a piscina y en uso intensivo; cerca de piscina o "
    "costa conviene limpiar con más frecuencia para retirar cloro o sal.")
Q_PARASOL_BASE = ("¿Incluye la base o el pie?",
    "No. La base no está incluida y se pide aparte, eligiendo el peso según el diámetro del parasol y "
    "la exposición al viento del espacio.")
Q_PARASOL_VIENTO = ("¿Qué hago con viento fuerte?",
    "Cierra siempre el parasol con viento fuerte o cuando no estés en casa, y usa una base adecuada al "
    "diámetro y a la exposición. Ten en cuenta que la garantía no cubre daños por viento o falta de sujeción.")


def q_comensales(size_cm):
    base = ("Como orientación, una mesa de 60-70 cm sirve para 2 personas, 120 cm para 4, 160-180 cm "
            "para 6 y 200-240 cm para 8; deja unos 90 cm libres alrededor para sacar las sillas y mide "
            "la terraza completa.")
    if size_cm:
        return ("¿Para cuántas personas es esta mesa?",
                f"Esta mesa mide {size_cm}. " + base)
    return ("¿Para cuántas personas es esta mesa?", base)


# ------------------- Detección de material / familia -------------------
def material_of(title, ptype):
    t = (title + " " + ptype).lower()
    if "hpl" in t and ptype in ("Mesa", "Mesa centro", "Mesa comedor"):
        return "hpl"
    if "aluminio" in t:
        return "aluminio"
    if "resina" in t or "polipropileno" in t:
        return "resina"
    if "hpl" in t:
        return "hpl"
    return None


TAPIZADO = {"Sofá", "Sofa", "Conjunto sofá", "Sillón", "Conjunto rinconera", "Reposapiés",
            "Cama balinesa", "Banco", "Banco con mesa", "Balancín"}
MESAS = {"Mesa", "Mesa centro", "Mesa comedor", "Pérgola"}
DINING = {"Mesa comedor"}
TUMBONAS = {"Tumbona", "Mini tumbona"}
SILLAS = {"Silla"}
PARASOLES = {"Parasol"}


def size_from_text(text):
    # devuelve la mayor medida en cm que aparezca (para orientar comensales)
    nums = [int(n) for n in re.findall(r"(\d{2,3})\s*(?:cm|×|x|/)", text)]
    nums += [int(n) for n in re.findall(r"(\d{2,3})\s*cm", text)]
    if not nums:
        return None
    m = max(nums)
    return f"{m} cm" if m >= 40 else None


def build_faq(product):
    title = product["title"]
    ptype = product["productType"] or ""
    desc = (product["descriptionHtml"] or "").lower()
    opts = " ".join(v for o in product.get("options", []) for v in o.get("values", []))
    mat = material_of(title, ptype)
    faqs = []

    # 1-2 de familia/material
    if ptype in TUMBONAS:
        faqs += [Q_TUMBONA_MAT, Q_TUMBONA_PISCINA]
    elif ptype in PARASOLES:
        faqs += [Q_PARASOL_BASE, Q_PARASOL_VIENTO]
    elif ptype in TAPIZADO:
        if mat:
            faqs.append(MAT[mat])
        faqs.append(Q_COJINES)
    elif ptype in MESAS:
        if mat:
            faqs.append(MAT[mat])
        if ptype in DINING or (ptype == "Mesa"):
            size = size_from_text(title + " " + opts)
            faqs.append(q_comensales(size))
    elif ptype in SILLAS:
        if mat:
            faqs.append(MAT[mat])
        # condicional apilable (solo si la ficha lo documenta)
        if "apilable" in desc or "apilar" in desc:
            faqs.append(("¿Se pueden apilar?",
                "Sí, su diseño apilable permite optimizar el espacio y guardarlas con facilidad cuando no se usan."))
    else:  # fundas / accesorios / mobiliario / otros
        if mat:
            faqs.append(MAT[mat])

    # condicional respaldo regulable (tumbonas/tapizados que lo documenten)
    m = re.search(r"regulable en (\w+) posiciones|(\w+) posiciones", desc)
    if m and ptype in (TUMBONAS | TAPIZADO):
        nposiciones = (m.group(1) or m.group(2))
        faqs.append(("¿El respaldo es reclinable?",
            f"Sí, su respaldo es regulable en {nposiciones} posiciones para ajustar la postura de descanso."))

    # rellenar hasta 4 con universales, sin duplicar
    for q in (Q_GARANTIA, Q_ENVIO, Q_MONTAJE):
        if len(faqs) >= 4:
            break
        if q not in faqs:
            faqs.append(q)

    # cap 4, dedup preservando orden
    seen, out = set(), []
    for q, a in faqs:
        if q in seen:
            continue
        seen.add(q)
        out.append({"q": q, "a": a})
        if len(out) == 4:
            break
    return out


GET = """
query($c:String){products(first:120,after:$c){pageInfo{hasNextPage endCursor}nodes{
  id handle title status productType descriptionHtml
  options{name values}
  metafield(namespace:"santavila",key:"faq"){value}
}}}
"""
SET = """
mutation($mf:[MetafieldsSetInput!]!){metafieldsSet(metafields:$mf){userErrors{field message}}}
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

    if SHOW:
        p = next((x for x in active if x["handle"] == SHOW), None)
        if not p:
            sys.exit("no encontrado")
        faqs = build_faq(p)
        print(f"### {p['title']}  [{p['productType']}]  ({len(faqs)} FAQ)")
        for f in faqs:
            print(f"\nQ: {f['q']}\nA: {f['a']}")
        return

    plan, backup = [], {}
    dist = {}
    for p in active:
        faqs = build_faq(p)
        plan.append((p, faqs))
        dist[len(faqs)] = dist.get(len(faqs), 0) + 1
        backup[p["handle"]] = {"id": p["id"], "faq_previo": (p.get("metafield") or {}).get("value")}

    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN'} - FAQ PDP · {len(plan)} fichas ACTIVE")
    print("Distribución de nº de FAQ por ficha:", {k: dist[k] for k in sorted(dist)})
    faltan = [p["handle"] for p, f in plan if len(f) < 3]
    if faltan:
        print(f"⚠ fichas con <3 FAQ ({len(faltan)}):", faltan[:10])

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = os.path.join(ROOT, "content", "descriptions", f"backup_pdp_faq_{ts}.json")
    with open(bpath, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)
    print(f"Backup valor previo -> {bpath}")

    if APPLY:
        print("\nEscribiendo metafield santavila.faq (json)...")
        errs = 0
        for p, faqs in plan:
            mf = [{"ownerId": p["id"], "namespace": "santavila", "key": "faq",
                   "type": "json", "value": json.dumps(faqs, ensure_ascii=False)}]
            try:
                res = gql(SET, {"mf": mf})["metafieldsSet"]
            except Exception as exc:
                print(f"X {p['handle']}: {exc}"); errs += 1; continue
            if res["userErrors"]:
                print(f"! {p['handle']}: {res['userErrors']}"); errs += 1
        print(f"Aplicado - errores: {errs}")
    else:
        print("\nRevisa con --show <handle> y aplica con --apply.")


if __name__ == "__main__":
    main()
