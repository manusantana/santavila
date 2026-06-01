#!/usr/bin/env python3
"""Saca datos detallados de una lista de handles → content/descriptions/thin_products.json
para poder redactar descripciones precisas. Solo lee, no escribe."""
import json, os, sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "content", "descriptions", "thin_products.json")

HANDLES = [
 "tumbona-carmen-tablillas","tumbona-lola-tablillas","mesa-exterior-aluminio-hpl-120x80-capri-doble",
 "balliu-parasol-para-terraza-acrilico-236bd5f0","balliu-parasol-para-terraza-82e48b2d",
 "balliu-parasol-para-terraza-f1ed8b8b","balliu-parasol-para-terraza-acrilico-c8dd492d",
 "balliu-mesa-exterior-5d0fb586","balliu-mesa-exterior-140-18090-cm-e4ec7d7c",
 "balliu-mesa-exterior-hpl-140-180100-cm-8e073aab","balliu-colchoneta-para-tumbona-0e9a3256",
 "balliu-funda-protectora-exterior-686cc405","balliu-funda-protectora-exterior-acrilico-a1c16324",
 "balliu-funda-protectora-exterior-6f6d4953","balliu-funda-protectora-exterior-340b2844",
 "balliu-cojin-exterior-523e5ae9","balliu-mesa-alta-exterior-hpl-94512eab",
 "balliu-pie-de-parasol-c2147052","balliu-base-de-parasol-3ee8b72d",
 "balliu-silla-exterior-sin-brazos-estilo-contemporaneo-53-cm-cd07e7d6",
 "set-rinconera-exterior-hpl-moderno-sofa-de-esquina-mesa-de-centro",
 "set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-3",
 "set-rinconera-exterior-hpl-elegante-sofa-de-esquina-mesa-de-centro",
 "set-rinconera-exterior-hpl-sofisticado-sofa-de-esquina-mesa-de-centro",
 "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4",
 "set-jardin-3-plazas-urbano-sofa-3-plazas-2-sillones-mesa","base-de-parasol-25-kg",
 "set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa",
 "set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-4",
 "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-3",
 "set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro",
]

Q = """
query($h: String!) {
  productByHandle(handle: $h) {
    handle title productType vendor tags descriptionHtml
    seo { title description }
    featuredImage { altText }
    options { name values }
    priceRangeV2 { minVariantPrice { amount currencyCode } maxVariantPrice { amount } }
    metafields(first: 25) { nodes { namespace key value type } }
    variants(first: 50) { nodes { title sku price selectedOptions { name value } } }
  }
}
"""

def gql(h):
    body = json.dumps({"query": Q, "variables": {"h": h}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    if "errors" in d: sys.exit(f"GraphQL error en {h}: {d['errors']}")
    return d["data"]["productByHandle"]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
data = {}
for h in HANDLES:
    p = gql(h)
    if not p:
        print(f"⚠️  no encontrado: {h}"); continue
    data[h] = p
    print(f"✓ {h}")
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n💾 {len(data)} fichas → {OUT}")
