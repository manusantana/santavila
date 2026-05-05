#!/usr/bin/env python3
"""
Consolidaciones pendientes:
  - vera-silla   (3→1, opción Modelo)
  - brunei-mesa  (8→1, opción Tamaño)
  - capri-mesa   (10→2: redondas + cuadradas, opción Tablero/Configuración)

Uso:
  python3 consolidate_remaining.py --dry-run
  python3 consolidate_remaining.py
  python3 consolidate_remaining.py --group vera-silla
"""

import csv, json, os, re, sys, time, urllib.request
from pathlib import Path
from collections import defaultdict

TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN")
if not TOKEN:
    raise RuntimeError("Set SHOPIFY_ACCESS_TOKEN before running this script.")
SHOP  = "mueblesexterior.myshopify.com"
API   = f"https://{SHOP}/admin/api/2026-01/graphql.json"

DRY_RUN    = "--dry-run" in sys.argv
ONLY_GROUP = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == "--group"), None)

# ── Label cleanup ──────────────────────────────────────────────────────────────

# Brunei: "80X80 Tablero Hpl Gd" → "80×80 HPL GD"
def clean_brunei(raw):
    s = raw.strip()
    s = re.sub(r"(\d+)X(\d+)", lambda m: f"{m.group(1)}×{m.group(2)}", s)
    s = re.sub(r"\s*Tablero\s*", " ", s, flags=re.I)
    s = re.sub(r"\bHpl\b", "HPL", s)
    s = re.sub(r"\bGd\b", "GD", s)
    return s.strip()

# Capri cuadradas: "70X70 Pie Simple Tablero Hpl" → "70×70 · HPL"
CAPRI_LABEL_MAP = {
    "70X70 Pie Simple Tablero Hpl":        "70×70 · HPL",
    "70X70 Pie Simple Tablero Hpl Gd":     "70×70 · HPL GD",
    "80X80 Pie Simple Tablero Hpl":        "80×80 · HPL",
    "80X80 Pie Simple Tablero Hpl Gd":     "80×80 · HPL GD",
    "120X80 Pie Doble Tablero Hpl":        "120×80 · HPL",
    "120X80 Pie Doble Tablero Hpl Gd":     "120×80 · HPL GD",
    "120X80 Pie Doble alto Tablero Hpl":   "120×80 pie alto · HPL",
    "120X80 Pie Doble alto Tablero Hpl Gd":"120×80 pie alto · HPL GD",
    "Diam. 90 Table Hpl Table Top":        "HPL",
    "Diam. 90 Table Hpl Table Top Gd":     "HPL GD",
}

# ── GraphQL helper ─────────────────────────────────────────────────────────────

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:400])
    return data["data"]

def gql_retry(query, variables=None, retries=3):
    for attempt in range(retries):
        try:
            return gql(query, variables)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(3)
            else:
                raise

# ── Shopify mutations ──────────────────────────────────────────────────────────

def option_update(product_id, option_id, option_name, value_id, value_name):
    data = gql_retry("""
    mutation productOptionUpdate(
      $productId: ID!, $option: OptionUpdateInput!,
      $optionValuesToUpdate: [OptionValueUpdateInput!]
    ) {
      productOptionUpdate(
        productId: $productId, option: $option,
        optionValuesToUpdate: $optionValuesToUpdate,
        variantStrategy: LEAVE_AS_IS
      ) {
        userErrors { field message code }
        product { options { id name optionValues { id name } } }
      }
    }
    """, {
        "productId": product_id,
        "option": {"id": option_id, "name": option_name},
        "optionValuesToUpdate": [{"id": value_id, "name": value_name}],
    })
    errs = data["productOptionUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(", ".join(f"{e['field']}: {e['message']}" for e in errs))

def variants_bulk_create(product_id, opt_id, variants_data):
    """variants_data: list of {label, price, sku}"""
    variants = [
        {"optionValues": [{"optionId": opt_id, "name": v["label"]}],
         "price": str(v["price"]),
         "inventoryItem": {"sku": v["sku"]}}
        for v in variants_data
    ]
    data = gql_retry("""
    mutation productVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
      productVariantsBulkCreate(productId: $productId, variants: $variants) {
        productVariants { id title }
        userErrors { field message }
      }
    }
    """, {"productId": product_id, "variants": variants})
    errs = data["productVariantsBulkCreate"]["userErrors"]
    if errs:
        raise RuntimeError(", ".join(f"{e['field']}: {e['message']}" for e in errs))
    return data["productVariantsBulkCreate"]["productVariants"]

def copy_images(from_prods, to_product_id):
    count = 0
    for p in from_prods:
        for img_edge in p["images"]["edges"]:
            src = img_edge["node"]["src"]
            try:
                gql_retry("""
                mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
                  productCreateMedia(productId: $productId, media: $media) {
                    media { ... on MediaImage { id } }
                    mediaUserErrors { field message }
                  }
                }
                """, {"productId": to_product_id,
                      "media": [{"originalSource": src, "mediaContentType": "IMAGE"}]})
                count += 1
            except Exception:
                pass
    return count

def update_title(product_id, title):
    gql_retry("""
    mutation productUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id title }
        userErrors { field message }
      }
    }
    """, {"input": {"id": product_id, "title": title}})

def delete_product(product_id):
    gql_retry("""
    mutation productDelete($input: ProductDeleteInput!) {
      productDelete(input: $input) {
        deletedProductId userErrors { field message }
      }
    }
    """, {"input": {"id": product_id}})

# ── Consolidate one group ──────────────────────────────────────────────────────

def consolidate(products, option_name, new_title, label_fn):
    """
    products: list of Shopify product nodes, already enriched with _label and _price.
    Sorted cheapest first = primary.
    """
    primary     = products[0]
    secondaries = products[1:]
    opt         = primary["options"][0]
    opt_id      = opt["id"]
    value_id    = opt["optionValues"][0]["id"]

    print(f"\n{'─'*72}")
    print(f"  Grupo principal: {primary['title'][:60]}")
    if new_title:
        print(f"  Nuevo título:    {new_title}")
    for p in products:
        marker = "★" if p is primary else " "
        print(f"  {marker} €{p['_price']:7.2f}  {p['_label']:45} {p['handle'][-20:]}")

    if DRY_RUN:
        return

    # 1. Rename option + existing value
    option_update(primary["id"], opt_id, option_name, value_id, primary["_label"])
    print(f"  ✓ Opción → '{option_name}': '{primary['_label']}'")
    time.sleep(0.5)

    # 2. Create variants for secondaries
    variants_data = [{"label": p["_label"], "price": p["_price"],
                      "sku": p["variants"]["edges"][0]["node"]["inventoryItem"].get("sku","")}
                     for p in secondaries]
    created = variants_bulk_create(primary["id"], opt_id, variants_data)
    print(f"  ✓ {len(created)} variantes creadas: {[v['title'] for v in created]}")
    time.sleep(0.5)

    # 3. Copy images
    imgs = copy_images(secondaries, primary["id"])
    if imgs:
        print(f"  ✓ {imgs} imágenes copiadas")
    time.sleep(0.3)

    # 4. Update title
    if new_title:
        update_title(primary["id"], new_title)
        print(f"  ✓ Título → '{new_title}'")
    time.sleep(0.3)

    # 5. Delete secondaries
    for p in secondaries:
        delete_product(p["id"])
        print(f"  ✓ Borrado: {p['handle'][-45:]}")
        time.sleep(0.3)

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("Cargando datos de Shopify...")

    # Build hash → (csv_handle, label)
    hash_to = {}
    with open(Path(__file__).parent / "balliu_shopify_products.csv") as f:
        for row in csv.DictReader(f):
            sku = row.get("Variant SKU","")
            m = re.search(r"_([0-9A-Fa-f]{8})$", sku)
            if m:
                hash_to[m.group(1).lower()] = (row.get("Handle",""), row.get("Option1 Value","").strip())

    # Fetch all Balliu products
    all_prods, cursor = [], None
    while True:
        data = gql_retry("""
        query($cursor: String) {
          products(first: 100, after: $cursor, query: "vendor:Balliu") {
            edges { node {
              id handle title
              options { id name optionValues { id name } }
              variants(first:1) { edges { node { id price inventoryItem { sku } } } }
              images(first: 10) { edges { node { id src } } }
            }}
            pageInfo { hasNextPage endCursor }
          }
        }
        """, {"cursor": cursor})
        all_prods.extend(data["products"]["edges"])
        pi = data["products"]["pageInfo"]
        if not pi["hasNextPage"]: break
        cursor = pi["endCursor"]

    # Group by csv_handle
    by_csv = defaultdict(list)
    for e in all_prods:
        p = e["node"]
        m = re.search(r"-([0-9a-f]{8})(?:-\d+)?$", p["handle"])
        hval = m.group(1) if m else None
        csv_handle, raw_label = hash_to.get(hval, ("",""))
        p["_csv_handle"] = csv_handle
        p["_raw_label"]  = raw_label
        p["_price"]      = float(p["variants"]["edges"][0]["node"]["price"])
        by_csv[csv_handle].append(p)

    if DRY_RUN:
        print("🔍 MODO DRY-RUN — no se realizan cambios\n")

    groups_to_run = ["vera-silla", "brunei-mesa", "capri-redondas", "capri-cuadradas"]
    if ONLY_GROUP:
        groups_to_run = [ONLY_GROUP]

    ok = fail = 0

    for group_key in groups_to_run:
        try:
            if group_key == "vera-silla":
                prods = sorted(by_csv["vera-silla"], key=lambda x: x["_price"])
                for p in prods:
                    p["_label"] = p["_raw_label"].strip() or "Estándar"
                consolidate(prods, "Modelo",
                            "Silla exterior resina · estilo funcional",
                            lambda r: r)

            elif group_key == "brunei-mesa":
                prods = sorted(by_csv["brunei-mesa"], key=lambda x: x["_price"])
                for p in prods:
                    p["_label"] = clean_brunei(p["_raw_label"])
                consolidate(prods, "Tamaño",
                            "Mesa exterior aluminio rectangular · Brunei",
                            clean_brunei)

            elif group_key == "capri-redondas":
                all_capri = by_csv["capri-mesa"]
                prods = sorted(
                    [p for p in all_capri if "Diam" in p["_raw_label"]],
                    key=lambda x: x["_price"]
                )
                if len(prods) < 2:
                    print(f"\n  [capri-redondas] Solo {len(prods)} producto(s) — skip")
                    continue
                for p in prods:
                    p["_label"] = CAPRI_LABEL_MAP.get(p["_raw_label"], p["_raw_label"])
                consolidate(prods, "Tablero",
                            "Mesa exterior aluminio redonda · Santavila Capri",
                            lambda r: r)

            elif group_key == "capri-cuadradas":
                all_capri = by_csv["capri-mesa"]
                prods = sorted(
                    [p for p in all_capri if "Diam" not in p["_raw_label"]],
                    key=lambda x: x["_price"]
                )
                if len(prods) < 2:
                    print(f"\n  [capri-cuadradas] Solo {len(prods)} producto(s) — skip")
                    continue
                for p in prods:
                    p["_label"] = CAPRI_LABEL_MAP.get(p["_raw_label"], p["_raw_label"])
                consolidate(prods, "Configuración",
                            "Mesa exterior aluminio · Santavila Capri",
                            lambda r: r)

            ok += 1
        except Exception as e:
            print(f"\n  ✗ ERROR en {group_key}: {e}")
            fail += 1

    print(f"\n{'='*72}")
    print(f"Completado: {ok} grupos OK | {fail} errores")

if __name__ == "__main__":
    main()
