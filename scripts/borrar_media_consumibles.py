#!/usr/bin/env python3
"""Borra de Shopify los media listados en un _plan.json (auditoria 22-08-2026).

Motivo: la DEROGACION de consumibles (03-08-2026, Sergio: "nada de comida ni bebida")
dejo 8 imagenes de comida/bebida vivas en fichas ACTIVE, mas 1 macro de tejido
(prohibido por §15: el macro extremo empuja al modelo a inventar la trama).

Seguridad:
  - Cada imagen se descarga ANTES a images_generated/_BORRADAS_.../  -> es reversible.
  - Dry-run por defecto. Con --apply borra de verdad.
  - Verifica el mediaCount antes y despues de cada ficha.
"""
import json, sys, urllib.request, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://mueblesexterior.myshopify.com/admin/api/2025-01/graphql.json"
APPLY = "--apply" in sys.argv
TOKEN = None
for line in open(os.path.join(ROOT, ".envlocal"), encoding="utf-8"):
    if line.startswith("SHOPIFY_ACCESS_TOKEN="):
        TOKEN = line.split("=", 1)[1].strip()

def gql(q, v=None):
    req = urllib.request.Request(API, data=json.dumps({"query": q, "variables": v or {}}).encode(),
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())

D = os.path.join(ROOT, "images_generated", "_BORRADAS_consumibles_20260822")
plan = json.load(open(os.path.join(D, "_plan.json")))

Q_COUNT = 'query($id:ID!){product(id:$id){handle mediaCount{count}}}'
M_DEL = '''mutation($pid:ID!,$ids:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$ids){
  deletedMediaIds mediaUserErrors{field message} userErrors{field message}}}'''

porficha = {}
for p in plan:
    porficha.setdefault(p["productId"], []).append(p)

for pid, items in porficha.items():
    h = items[0]["handle"]
    antes = gql(Q_COUNT, {"id": pid})["data"]["product"]["mediaCount"]["count"]
    print(f"== {h[:56]}   media antes={antes}  a borrar={len(items)}")
    for it in items:
        print(f"     - {it['alt'][:88]}")
        if not os.path.exists(it["backup"]):
            sys.exit(f"   ABORTA: falta el backup {it['backup']}")
    if not APPLY:
        print("   [dry-run] no se borra nada"); continue
    r = gql(M_DEL, {"pid": pid, "ids": [i["mediaId"] for i in items]})
    d = r["data"]["productDeleteMedia"]
    errs = (d.get("mediaUserErrors") or []) + (d.get("userErrors") or [])
    if errs:
        print(f"   ERROR: {errs}"); continue
    despues = gql(Q_COUNT, {"id": pid})["data"]["product"]["mediaCount"]["count"]
    print(f"   borrados {len(d['deletedMediaIds'])}  ->  media ahora={despues}")

if not APPLY:
    print("\n(dry-run: repite con --apply)")
