#!/usr/bin/env python3
"""
Auditoría de fichas de producto (Shopify Admin GraphQL) para SEO/GEO y Google Merchant.
Mide por producto: longitud de descripción, meta description SEO, marca (vendor),
código de barras (GTIN) en variantes, imagen. Resume y exporta CSV de los que fallan.

Uso: python3 scripts/audit_products.py   (usa SHOPIFY_ACCESS_TOKEN de .env vía config.py)
"""
import csv
import os
import re
import sys
import json
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHORT_WORDS = 30  # umbral "descripción corta"

QUERY = """
query($cursor: String) {
  products(first: 200, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      handle title status productType vendor
      descriptionHtml
      seo { description }
      featuredImage { url }
      variants(first: 100) { nodes { barcode } }
    }
  }
}
"""


def gql(cursor):
    body = json.dumps({"query": QUERY, "variables": {"cursor": cursor}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]["products"]


def words(html):
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"&[a-z]+;", " ", text)
    return len(text.split())


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("ERROR: SHOPIFY_ACCESS_TOKEN vacío (.env)")
    products, cursor = [], None
    while True:
        page = gql(cursor)
        products.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    rows = []
    for p in products:
        w = words(p["descriptionHtml"])
        variants = p["variants"]["nodes"]
        no_barcode = sum(1 for v in variants if not (v.get("barcode") or "").strip())
        rows.append({
            "handle": p["handle"],
            "title": p["title"],
            "status": p["status"],
            "type": p.get("productType") or "",
            "vendor": p.get("vendor") or "",
            "desc_words": w,
            "seo_desc": "sí" if (p.get("seo") or {}).get("description") else "NO",
            "image": "sí" if p.get("featuredImage") else "NO",
            "variants": len(variants),
            "variants_sin_gtin": no_barcode,
        })

    active = [r for r in rows if r["status"] == "ACTIVE"]
    def pct(n, d): return f"{100*n/d:.0f}%" if d else "0%"

    print(f"\n{'='*70}\nAUDITORÍA DE FICHAS — {SHOP}\n{'='*70}")
    print(f"Productos totales: {len(rows)}  ·  ACTIVE: {len(active)}  ·  "
          f"DRAFT/otros: {len(rows)-len(active)}")
    print(f"\n--- Sobre productos ACTIVE ({len(active)}) ---")
    empty = [r for r in active if r["desc_words"] == 0]
    short = [r for r in active if 0 < r["desc_words"] < SHORT_WORDS]
    ok    = [r for r in active if r["desc_words"] >= SHORT_WORDS]
    print(f"Descripción VACÍA:        {len(empty):>4}  ({pct(len(empty),len(active))})")
    print(f"Descripción CORTA (<{SHORT_WORDS}p): {len(short):>4}  ({pct(len(short),len(active))})")
    print(f"Descripción OK (≥{SHORT_WORDS}p):    {len(ok):>4}  ({pct(len(ok),len(active))})")
    no_seo = [r for r in active if r["seo_desc"] == "NO"]
    no_vendor = [r for r in active if not r["vendor"]]
    no_img = [r for r in active if r["image"] == "NO"]
    gtin = [r for r in active if r["variants_sin_gtin"] > 0]
    print(f"\nSin meta description SEO:  {len(no_seo):>4}  ({pct(len(no_seo),len(active))})")
    print(f"Sin marca (vendor):        {len(no_vendor):>4}  ({pct(len(no_vendor),len(active))})")
    print(f"Sin imagen destacada:      {len(no_img):>4}  ({pct(len(no_img),len(active))})")
    print(f"Con variantes sin GTIN:    {len(gtin):>4}  ({pct(len(gtin),len(active))})")

    # Reparto por tipo de los que necesitan descripción
    need = empty + short
    by_type = {}
    for r in need:
        by_type[r["type"] or "(sin tipo)"] = by_type.get(r["type"] or "(sin tipo)", 0) + 1
    if by_type:
        print(f"\n--- Fichas que necesitan descripción ({len(need)}) por tipo ---")
        for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {n:>4}  {t}")

    # CSV
    out = os.path.join(ROOT, "auditoria_fichas_report.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        for r in sorted(rows, key=lambda r: (r["status"] != "ACTIVE", r["desc_words"])):
            wtr.writerow(r)
    print(f"\n💾 CSV completo en {out}")


if __name__ == "__main__":
    main()
