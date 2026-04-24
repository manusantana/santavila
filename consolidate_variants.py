#!/usr/bin/env python3
"""
Consolida productos Balliu con el mismo diseño (distintas variantes de tamaño/color)
en un único producto Shopify con variantes.

18 grupos definidos. Proceso por grupo:
  1. Renombrar opción "Title" → nombre descriptivo, valor "Default Title" → etiqueta limpia
  2. Crear variantes adicionales (precio + SKU de los productos secundarios)
  3. Mover imágenes de los secundarios al producto principal
  4. Actualizar título del producto principal si es necesario
  5. Borrar los productos secundarios

Uso:
  python3 consolidate_variants.py --dry-run   # solo muestra el plan
  python3 consolidate_variants.py             # ejecuta
  python3 consolidate_variants.py --group etna-sofa  # solo un grupo
"""

import csv, json, re, sys, time, urllib.request
from pathlib import Path

from config import SHOPIFY_ACCESS_TOKEN as TOKEN
SHOP  = "mueblesexterior.myshopify.com"
API   = f"https://{SHOP}/admin/api/2026-01/graphql.json"

DRY_RUN    = "--dry-run"  in sys.argv
ONLY_GROUP = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == "--group"), None)

# ── 18 consolidation groups ────────────────────────────────────────────────────
# sort_by: "price_asc" (cheapest = primary), "price_desc", "sku_asc"
GROUPS = [
    # Sofás
    {"csv_handle": "etna-sofa",
     "option_name": "Tamaño",
     "new_title":   "Sofá exterior aluminio · estilo contemporáneo | 77 cm",
     "sort_by":     "price_asc"},
    {"csv_handle": "olimpia-sofa",
     "option_name": "Tamaño",
     "new_title":   "Sofá exterior aluminio · estilo elegante | 62 cm",
     "sort_by":     "price_asc"},
    # Tumbonas aluminio
    {"csv_handle": "olimpia-tumbona",
     "option_name": "Ruedas",
     "new_title":   "Tumbona de exterior aluminio Olimpia",
     "sort_by":     "price_asc"},
    {"csv_handle": "etna-tumbona",
     "option_name": "Ruedas",
     "new_title":   "Tumbona de exterior aluminio Etna",
     "sort_by":     "price_asc"},
    {"csv_handle": "etna-alta-tumbona-alta",
     "option_name": "Ruedas",
     "new_title":   "Tumbona de exterior aluminio Etna Alta",
     "sort_by":     "price_asc"},
    # Tumbonas resina - color chasis
    {"csv_handle": "eva-rg-tumbona",
     "option_name": "Color chasis",
     "new_title":   None,
     "sort_by":     "price_asc"},
    {"csv_handle": "noa-tumbona",
     "option_name": "Color chasis",
     "new_title":   None,
     "sort_by":     "price_asc"},
    # Tumbonas resina - configuración chasis+tejido
    {"csv_handle": "carmen-tumbona",
     "option_name": "Configuración",
     "new_title":   None,
     "sort_by":     "price_asc"},
    {"csv_handle": "lola-tumbona",
     "option_name": "Configuración",
     "new_title":   None,
     "sort_by":     "price_asc"},
    # Sillas - color
    {"csv_handle": "duna-silla",
     "option_name": "Color",
     "new_title":   None,
     "sort_by":     "price_asc"},
    {"csv_handle": "bimba-silla",
     "option_name": "Color",
     "new_title":   None,
     "sort_by":     "price_asc"},
    {"csv_handle": "selva-silla",
     "option_name": "Color",
     "new_title":   None,
     "sort_by":     "price_asc"},
    # Sillas - brazos
    {"csv_handle": "bruna-silla",
     "option_name": "Brazos",
     "new_title":   "Silla exterior resina · estilo contemporáneo | 49 cm",
     "sort_by":     "price_asc"},
    # Accesorios
    {"csv_handle": "colchoneta-tumbona",
     "option_name": "Tejido",
     "new_title":   "Colchoneta para tumbona",
     "sort_by":     "price_asc"},
    {"csv_handle": "funda-sofa",
     "option_name": "Tamaño",
     "new_title":   "Funda protectora para sofá exterior",
     "sort_by":     "price_asc"},
    {"csv_handle": "funda-tumbona",
     "option_name": "Pack",
     "new_title":   "Funda protectora para tumbona exterior",
     "sort_by":     "price_asc"},
    # Mesas - tablero
    {"csv_handle": "etna-mesa-central",
     "option_name": "Tablero",
     "new_title":   None,
     "sort_by":     "price_asc"},
    {"csv_handle": "etna-mesa-auxiliar",
     "option_name": "Tablero",
     "new_title":   None,
     "sort_by":     "price_asc"},
]

# ── GraphQL helpers ────────────────────────────────────────────────────────────

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:400])
    return data["data"]

# ── Load CSV hash → variant label ──────────────────────────────────────────────

def load_csv_labels():
    mapping = {}
    with open(Path(__file__).parent / "balliu_shopify_products.csv") as f:
        for row in csv.DictReader(f):
            sku = row.get("Variant SKU", "")
            m = re.search(r"_([0-9A-Fa-f]{8})$", sku)
            if m:
                mapping[m.group(1).lower()] = row.get("Option1 Value", "").strip()
    return mapping

# ── Fetch all Balliu products ──────────────────────────────────────────────────

def fetch_all_balliu():
    QUERY = """
    query($cursor: String) {
      products(first: 100, after: $cursor, query: "vendor:Balliu") {
        edges { node {
          id handle title
          options { id name values optionValues { id name } }
          variants(first: 3) { edges { node {
            id title price
            inventoryItem { id sku }
          }}}
          images(first: 10) { edges { node { id src } } }
        }}
        pageInfo { hasNextPage endCursor }
      }
    }
    """
    all_products, cursor = [], None
    while True:
        data = gql(QUERY, {"cursor": cursor})
        all_products.extend(data["products"]["edges"])
        pi = data["products"]["pageInfo"]
        if not pi["hasNextPage"]: break
        cursor = pi["endCursor"]
    return all_products

# ── Shopify mutations ──────────────────────────────────────────────────────────

def options_update(product_id, option_id, option_name, value_id, value_name):
    """Rename the option and its single existing value."""
    data = gql("""
    mutation productOptionUpdate(
      $productId: ID!,
      $option: OptionUpdateInput!,
      $optionValuesToUpdate: [OptionValueUpdateInput!]
    ) {
      productOptionUpdate(
        productId: $productId,
        option: $option,
        optionValuesToUpdate: $optionValuesToUpdate,
        variantStrategy: LEAVE_AS_IS
      ) {
        userErrors { field message code }
        product { options { id name values optionValues { id name } } }
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
    return data["productOptionUpdate"]["product"]

def variant_bulk_create(product_id, variants):
    """Create multiple variants at once."""
    data = gql("""
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

def product_update_title(product_id, title):
    data = gql("""
    mutation productUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id title }
        userErrors { field message }
      }
    }
    """, {"input": {"id": product_id, "title": title}})
    errs = data["productUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(", ".join(e["message"] for e in errs))

def create_media(product_id, cdn_url):
    data = gql("""
    mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
      productCreateMedia(productId: $productId, media: $media) {
        media { ... on MediaImage { id } }
        mediaUserErrors { field message }
      }
    }
    """, {"productId": product_id,
          "media": [{"originalSource": cdn_url, "mediaContentType": "IMAGE"}]})
    errs = data["productCreateMedia"]["mediaUserErrors"]
    if errs:
        raise RuntimeError(", ".join(e["message"] for e in errs))

def product_delete(product_id):
    data = gql("""
    mutation productDelete($input: ProductDeleteInput!) {
      productDelete(input: $input) {
        deletedProductId
        userErrors { field message }
      }
    }
    """, {"input": {"id": product_id}})
    errs = data["productDelete"]["userErrors"]
    if errs:
        raise RuntimeError(", ".join(e["message"] for e in errs))
    return data["productDelete"]["deletedProductId"]

# ── Clean variant label from CSV option value ──────────────────────────────────

def clean_label(raw):
    """Return the CSV Option1 Value as-is (already descriptive enough)."""
    return raw.strip() or "Estándar"

# ── Main consolidation logic ───────────────────────────────────────────────────

def consolidate_group(group, products_by_handle, csv_labels):
    csv_handle  = group["csv_handle"]
    option_name = group["option_name"]
    new_title   = group["new_title"]
    sort_by     = group.get("sort_by", "price_asc")

    prods = products_by_handle.get(csv_handle, [])
    if len(prods) < 2:
        print(f"  [{csv_handle}] Solo {len(prods)} producto(s) — skip")
        return

    # Attach CSV label and sort
    for p in prods:
        variant_node = p["variants"]["edges"][0]["node"]
        h = p.get("_hash")
        p["_label"] = clean_label(csv_labels.get(h, ""))
        p["_price"] = float(variant_node["price"])
        p["_variant_id"] = variant_node["id"]
        p["_sku"]   = variant_node["inventoryItem"].get("sku", "")

    prods.sort(key=lambda x: x["_price"])  # cheapest first = primary

    primary    = prods[0]
    secondaries = prods[1:]

    print(f"\n{'─'*70}")
    print(f"  Grupo: {csv_handle}  ({len(prods)}x → 1)")
    print(f"  Principal: {primary['title']}")
    print(f"    handle: {primary['handle'][-30:]}")
    for p in prods:
        marker = "★" if p is primary else " "
        print(f"  {marker} {p['_label']:35} €{p['_price']:.2f}  {p['_sku'][-12:]}")
    if new_title:
        print(f"  Nuevo título: {new_title}")

    if DRY_RUN:
        return

    # ── Step 1: rename option + existing value on primary ──────────────────────
    opt      = primary["options"][0]
    opt_id   = opt["id"]
    value_id = opt["optionValues"][0]["id"]
    options_update(primary["id"], opt_id, option_name, value_id, primary["_label"])
    print(f"  ✓ Opción renombrada → '{option_name}': '{primary['_label']}'")
    time.sleep(0.5)

    # ── Step 2: create variants for secondaries ────────────────────────────────
    new_variants = []
    for p in secondaries:
        new_variants.append({
            "optionValues": [{"optionId": opt_id, "name": p["_label"]}],
            "price": str(p["_price"]),
            "inventoryItem": {"sku": p["_sku"]},
        })
    created = variant_bulk_create(primary["id"], new_variants)
    print(f"  ✓ {len(created)} variantes creadas: {[v['title'] for v in created]}")
    time.sleep(0.5)

    # ── Step 3: copy images from secondaries to primary ────────────────────────
    imgs_copied = 0
    for p in secondaries:
        for img_edge in p["images"]["edges"]:
            src = img_edge["node"]["src"]
            try:
                create_media(primary["id"], src)
                imgs_copied += 1
            except Exception:
                pass
    if imgs_copied:
        print(f"  ✓ {imgs_copied} imágenes copiadas al producto principal")
    time.sleep(0.3)

    # ── Step 4: update title if needed ────────────────────────────────────────
    if new_title:
        product_update_title(primary["id"], new_title)
        print(f"  ✓ Título actualizado: '{new_title}'")
    time.sleep(0.3)

    # ── Step 5: delete secondaries ─────────────────────────────────────────────
    for p in secondaries:
        product_delete(p["id"])
        print(f"  ✓ Borrado: {p['handle'][-40:]}")
        time.sleep(0.3)

# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    print("Cargando datos de Shopify...")
    all_prods = fetch_all_balliu()
    csv_labels = load_csv_labels()

    from collections import defaultdict
    hash_to_csvhandle = {}
    with open(Path(__file__).parent / "balliu_shopify_products.csv") as f:
        for row in csv.DictReader(f):
            sku = row.get("Variant SKU", "")
            m = re.search(r"_([0-9A-Fa-f]{8})$", sku)
            if m:
                hash_to_csvhandle[m.group(1).lower()] = row.get("Handle", "")

    products_by_csvhandle = defaultdict(list)
    for edge in all_prods:
        p = edge["node"]
        m = re.search(r"-([0-9a-f]{8})(?:-\d+)?$", p["handle"])
        hash_val = m.group(1) if m else None
        p["_hash"] = hash_val
        csv_h = hash_to_csvhandle.get(hash_val, "??")
        products_by_csvhandle[csv_h].append(p)

    target_groups = GROUPS
    if ONLY_GROUP:
        target_groups = [g for g in GROUPS if g["csv_handle"] == ONLY_GROUP]
        if not target_groups:
            print(f"Grupo '{ONLY_GROUP}' no encontrado.")
            return

    if DRY_RUN:
        print("🔍 MODO DRY-RUN — no se realizan cambios\n")

    ok = fail = 0
    for group in target_groups:
        try:
            consolidate_group(group, products_by_csvhandle, csv_labels)
            ok += 1
        except Exception as e:
            print(f"\n  ✗ ERROR en {group['csv_handle']}: {e}")
            fail += 1

    print(f"\n{'='*70}")
    print(f"Completado: {ok} grupos OK | {fail} errores")

if __name__ == "__main__":
    main()
