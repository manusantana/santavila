#!/usr/bin/env python3
"""FASE 0 del plan de cierre — borra imagenes DUPLICADAS EXACTAS de las fichas Balliu.

Origen: la migracion dejo la misma foto subida varias veces con distinto sufijo de Shopify.
Una mesa llegaba a tener 12 duplicados de 25 imagenes.

CRITERIO — y aqui esta la leccion (22-08-2026):
  El primer criterio fue "mismo nombre de fichero + mismas dimensiones". PARECIA seguro y daba
  57 duplicados. Al verificar por MD5 del contenido real, **7 de esos 57 eran imagenes
  DISTINTAS** con el mismo nombre y el mismo tamano (`397-CAPRI`, `180-CAPRI-scaled`,
  `DSC_0360-scaled`, `jmf2012_jml1499-scaled`).
  -> Solo se borra con **hash del fichero identico**. Nunca por nombre.

Seguridad:
  - Se conserva SIEMPRE la primera aparicion; se borran las repeticiones posteriores.
  - Verificado antes: ninguna variante de Balliu tiene imagen asignada, asi que borrar no
    rompe ninguna variante.
  - No hace falta backup del fichero: la imagen identica sigue en la ficha. Se guarda el
    registro de IDs por si hay que auditar.
  - Dry-run por defecto. Con --apply borra.
"""
import json, os, sys, urllib.request, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://mueblesexterior.myshopify.com/admin/api/2025-01/graphql.json"
APPLY = "--apply" in sys.argv
TOKEN = None
for line in open(os.path.join(ROOT, ".envlocal"), encoding="utf-8"):
    if line.startswith("SHOPIFY_ACCESS_TOKEN="):
        TOKEN = line.split("=", 1)[1].strip()

def gql(q, v=None, intentos=4):
    for i in range(intentos):
        try:
            req = urllib.request.Request(API, data=json.dumps({"query": q, "variables": v or {}}).encode(),
                headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=60).read())
        except Exception:
            if i == intentos - 1: raise
            time.sleep(2 * (i + 1))

datos = json.load(open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "dupreal.json")))
real, falsos = datos["real"], datos["falsos"]

porficha = {}
for r in real:
    porficha.setdefault((r["pid"], r["h"], r["pr"]), []).append(r["id"])

Q = 'query($id:ID!){product(id:$id){handle mediaCount{count}}}'
M = '''mutation($pid:ID!,$ids:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$ids){
  deletedMediaIds mediaUserErrors{message} userErrors{message}}}'''

print(f"duplicados EXACTOS (hash identico): {len(real)} en {len(porficha)} fichas")
print(f"falsos positivos NO tocados       : {len(falsos)}\n")
tot = 0
for (pid, h, pr), ids in sorted(porficha.items(), key=lambda x: -len(x[1])):
    antes = gql(Q, {"id": pid})["data"]["product"]["mediaCount"]["count"]
    print(f"== {h[:52]}  {pr:.0f} EUR   media={antes}  borrar={len(ids)}")
    if not APPLY:
        continue
    r = gql(M, {"pid": pid, "ids": ids})["data"]["productDeleteMedia"]
    errs = (r.get("mediaUserErrors") or []) + (r.get("userErrors") or [])
    if errs:
        print(f"   ERROR: {errs}"); continue
    time.sleep(1)
    despues = gql(Q, {"id": pid})["data"]["product"]["mediaCount"]["count"]
    tot += len(r["deletedMediaIds"])
    print(f"   borrados {len(r['deletedMediaIds'])} -> media={despues}")

if APPLY:
    reg = os.path.join(ROOT, "images_generated", "_duplicados_balliu_20260822.json")
    json.dump(real, open(reg, "w"), indent=1)
    print(f"\nTOTAL borrados: {tot}\nregistro -> {os.path.relpath(reg, ROOT)}")
else:
    print("\n[dry-run] repite con --apply")
