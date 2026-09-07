#!/usr/bin/env python3
"""
Inventario de la FASE 3 (Balliu): las fichas cuya PRIMERA imagen esta en baja resolucion.

Por que la primera y no "todas": la estrategia decidida por Sergio el 22-08-2026 es **anadir**
ambiente al principio y **conservar** las fotos de acabado del proveedor, aunque sean de 800 px.
En Balliu esas fotos pequenas son la unica informacion real de variante que existe (hasta 96
combinaciones de color/chasis/tejido en una ficha). Asi que lo que hay que arreglar es la
imagen que VENDE en el listado, no la galeria entera.

OJO con el conteo: un media de tipo VIDEO devuelve width=0 en `... on MediaImage`, y eso hacia
que dos fichas Hevea con galeria completa a 4096 px se colaran en la lista. Se filtra por
mediaContentType == IMAGE.

    python3 scripts/inventario_balliu.py            # tabla
    python3 scripts/inventario_balliu.py --json f   # vuelca a fichero
"""
import json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://mueblesexterior.myshopify.com/admin/api/2025-01/graphql.json"
TOKEN = next(l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".envlocal"),encoding="utf-8")
             if l.startswith("SHOPIFY_ACCESS_TOKEN="))

Q = '''query($c:String){products(first:100,after:$c,query:"status:active"){
  pageInfo{hasNextPage endCursor}
  edges{node{handle title descriptionHtml
    options{name values}
    variants(first:1){edges{node{sku price}}}
    media(first:30){edges{node{ mediaContentType ... on MediaImage{ alt image{url width height} } }}}}}}}'''

def gql(q, v=None):
    """Transporte por curl, NO por urllib: con 100 productos y 30 media cada uno la respuesta pasa
    de 100 KB y urllib corta con `IncompleteRead` de forma reproducible en este entorno. curl con
    --retry-all-errors lo reintenta solo."""
    body = json.dumps({"query": q, "variables": v or {}})
    r = subprocess.run(["curl", "-s", "--retry", "4", "--retry-all-errors", "--max-time", "120",
                        "-X", "POST", API,
                        "-H", f"X-Shopify-Access-Token: {TOKEN}",
                        "-H", "Content-Type: application/json",
                        "--data-binary", "@-"],
                       input=body.encode(), capture_output=True)
    if r.returncode or not r.stdout:
        raise RuntimeError(f"curl fallo ({r.returncode}): {r.stderr.decode()[:200]}")
    d = json.loads(r.stdout)
    if "errors" in d:
        raise RuntimeError(json.dumps(d["errors"])[:300])
    return d

def main():
    out, c = [], None
    while True:
        d = gql(Q, {"c": c})["data"]["products"]
        for e in d["edges"]:
            n = e["node"]
            v = n["variants"]["edges"][0]["node"] if n["variants"]["edges"] else {}
            imgs = [{"url": (m["node"].get("image") or {}).get("url"),
                     "w": (m["node"].get("image") or {}).get("width", 0),
                     "h": (m["node"].get("image") or {}).get("height", 0),
                     "alt": m["node"].get("alt") or ""}
                    for m in n["media"]["edges"] if m["node"]["mediaContentType"] == "IMAGE"]
            out.append({"handle": n["handle"], "title": n["title"],
                        "sku": v.get("sku"), "price": float(v.get("price") or 0),
                        "opciones": {o["name"]: o["values"] for o in n["options"]},
                        "imgs": imgs})
        if not d["pageInfo"]["hasNextPage"]: break
        c = d["pageInfo"]["endCursor"]; time.sleep(0.25)

    # el trabajo de la fase 3: primera IMAGEN por debajo de 2.000 px
    faltan = [f for f in out if f["imgs"] and f["imgs"][0]["w"] < 2000]
    faltan.sort(key=lambda f: -f["price"])
    print(f"ACTIVE: {len(out)}   ·   con la primera imagen <2000 px: {len(faltan)}"
          f"   ·   valor: {round(sum(f['price'] for f in faltan)):,} EUR".replace(",", "."))
    for f in faltan:
        mejor = max(f["imgs"], key=lambda i: i["w"])
        ejes = " ".join(f"{k}({len(v)})" for k, v in f["opciones"].items() if k != "Title")
        print(f"{f['price']:7.0f} | {len(f['imgs']):2d} img | mejor {mejor['w']:4d}px | "
              f"{f['title'][:52]:52s} | {ejes[:34]:34s} | {f['handle']}")
    if "--json" in sys.argv:
        json.dump(faltan, open(sys.argv[sys.argv.index("--json")+1], "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
