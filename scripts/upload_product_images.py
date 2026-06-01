#!/usr/bin/env python3
"""
Sube imágenes a productos que no tienen foto, desde URL pública de Balliu.
Por defecto DRY-RUN. Con --apply ejecuta. Solo añade imagen si el producto no tiene ya una destacada.

  python3 scripts/upload_product_images.py            # dry-run
  python3 scripts/upload_product_images.py --apply     # sube de verdad
"""
import json, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
APPLY = "--apply" in sys.argv

# handle -> (url_imagen_publica, alt_text)
IMAGES = {
 "tumbona-carmen-tablillas": (
   "https://www.balliuexport.com/wp-content/uploads/2023/12/carmen-t-blanco-800x614-1.jpg",
   "Tumbona de exterior de resina blanca con tablillas y respaldo reclinable, para jardín y piscina"),
 "tumbona-lola-tablillas": (
   "https://www.balliuexport.com/wp-content/uploads/2023/12/lola-t-tumbona-blanco-800x614-2.jpg",
   "Tumbona de exterior de resina blanca con tablillas, tipo playa, para piscina y jardín"),
 "mesa-exterior-aluminio-hpl-120x80-capri-doble": (
   "https://www.balliuexport.com/wp-content/uploads/2020/02/capri-mesa-doble-aluminio-800x614-1.jpg",
   "Mesa de exterior de aluminio con tablero HPL y pie doble, 120x80 cm"),
 "parasol-cuadrado-200x200": (
   "https://www.balliuexport.com/wp-content/uploads/2023/12/agora-parasol-800x614-1.jpg",
   "Parasol cuadrado de exterior de aluminio 200x200 cm con tela arena, para terraza y balcón"),
}

def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    if "errors" in d: raise RuntimeError(d["errors"])
    return d["data"]

GET = """query($h:String!){ productByHandle(handle:$h){ id handle featuredImage{url} mediaCount{count} } }"""
ADD = """mutation($pid:ID!,$media:[CreateMediaInput!]!){
  productCreateMedia(productId:$pid, media:$media){
    media{ ... on MediaImage { id image{url} } }
    mediaUserErrors{ field message }
  }
}"""

def main():
    if not SHOPIFY_ACCESS_TOKEN: sys.exit("SHOPIFY_ACCESS_TOKEN vacío")
    print(f"{'APLICAR' if APPLY else 'DRY-RUN'} — {len(IMAGES)} imágenes\n")
    for h,(url,alt) in IMAGES.items():
        p = gql(GET, {"h":h})["productByHandle"]
        if not p: print(f"✗ {h}: no encontrado"); continue
        has = bool(p.get("featuredImage"))
        print(f"• {h}: {'YA tiene imagen → SE OMITE' if has else 'sin imagen → añadir'}")
        if has or not APPLY: continue
        res = gql(ADD, {"pid":p["id"], "media":[{"originalSource":url,"alt":alt,"mediaContentType":"IMAGE"}]})["productCreateMedia"]
        ue = res["mediaUserErrors"]
        if ue: print(f"    ⚠️ {ue}")
        else: print(f"    ✅ subida: {res['media']}")
    if not APPLY: print("\nEjecuta con --apply para subir.")

if __name__ == "__main__":
    main()
