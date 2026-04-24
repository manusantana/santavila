#!/usr/bin/env python3
"""
Fase 1: Re-scrape todas las páginas de Balliu → obtener TODAS las imágenes (no solo 5)
Fase 2: Mapeo inteligente: usa el hash del handle de Shopify → CSV → variante (individual/doble/triple)
         → elige imagen específica por tamaño de la web de Balliu
Fase 3: Descarga todas las imágenes nuevas
Fase 4: Sube galería completa (no solo 1 imagen) a cada producto de Shopify

Uso: python3 balliu_full_images.py [--scrape-only] [--dry-run]
"""

import csv, json, re, sys, time, urllib.request, urllib.error
from pathlib import Path

from config import SHOPIFY_ACCESS_TOKEN as TOKEN
SHOP  = "mueblesexterior.myshopify.com"
API   = f"https://{SHOP}/admin/api/2026-01/graphql.json"
BASE  = Path(__file__).parent
IMG_DIR = BASE / "images_balliu"
IMG_DIR.mkdir(exist_ok=True)

SCRAPE_ONLY = "--scrape-only" in sys.argv
DRY_RUN     = "--dry-run"     in sys.argv

# ── Non-product images to exclude ─────────────────────────────────────────────
EXCLUDE_PATTERNS = [
    "Icono-", "favicon", "14001_", "9001_", "new-logo", "logo-",
    "blanc.jpg", "Tortola-898280", "110-307-Aluminio",
    "-balliu-parasoles", "-balliu-sombrillas",
    "Silla-Etna-Blanco-ceniza",   # fabric swatch shown in sidebar
    "aura-cama-balinesa-blanco",  # suggested product shown on other pages
    "carmen-tumbona", "roma-parasol", "olimpia-s-ruedas", "nora-mesa",
    # WordPress certification logos
    "ENAC_CAST",
    # Color selector swatches (small images, but block by name pattern)
    "2019_jmf",
]

# WordPress thumbnail dimension suffixes to strip (keep originals only)
# An image is a thumbnail if its filename ends with -{W}x{H}.ext
# BUT: Balliu originals look like name-800x614-N.jpg  (800x614 is PART of the name)
# WordPress creates: name-800x614-N-100x100.jpg  (additional suffix)
# So: exclude if contains TWO dimension patterns, OR ends with standard WP sizes
WP_THUMB_SIZES = {
    "100x100","50x50","80x61","80x53","80x50","80x67",
    "250x250","150x150","300x230","400x307","400x263","400x250",
    "600x461","600x395","600x375","768x589","768x506","768x480",
}

def is_thumbnail(fname):
    m = re.findall(r"-(\d+x\d+)", fname)
    if not m:
        return False
    # If last dimension in filename is a known WP thumb size → it's a thumbnail
    return m[-1] in WP_THUMB_SIZES

def is_excluded(url):
    fname = url.split("/")[-1]
    if is_thumbnail(fname):
        return True
    for pat in EXCLUDE_PATTERNS:
        if pat in url:
            return True
    return False


# ── HTTP helpers ───────────────────────────────────────────────────────────────

def fetch(url, timeout=15):
    req = urllib.request.Request(url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MueblesBot/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:300])
    return data["data"]


# ── Phase 1: Re-scrape all Balliu pages ───────────────────────────────────────

def scrape_product_images(url):
    """
    Return list of unique full-size product image URLs from a Balliu product page.
    Uses WooCommerce data-large_image attributes (actual gallery, not related products).
    """
    html = fetch(url)
    seen, result = set(), []

    # Primary: WooCommerce gallery images (data-large_image)
    gallery = re.findall(r'data-large_image="(https://www\.balliuexport\.com/[^"]+)"', html)
    for img in gallery:
        img = img.replace(r"\/", "/").split("?")[0]
        if img not in seen and not is_excluded(img):
            seen.add(img)
            result.append(img)

    # Secondary: WooCommerce variation images (embedded JSON "large" key)
    var_large = re.findall(r'"large"\s*:\s*"(https:\\/\\/www\\.balliuexport\\.com\\/[^"]+)"', html)
    for img in var_large:
        img = img.replace(r"\/", "/").split("?")[0]
        if img not in seen and not is_excluded(img):
            seen.add(img)
            result.append(img)

    return result


def rescrape_catalog():
    print("── Fase 1: Re-scraping catálogo Balliu (todas las imágenes) ───────────\n")
    with open(BASE / "balliu_catalog.json") as f:
        catalog = json.load(f)

    updated = 0
    for i, (slug, prod) in enumerate(catalog.items(), 1):
        url = prod["url"]
        label = f"[{i:02d}/{len(catalog)}] {slug[:55]:<57}"
        try:
            imgs = scrape_product_images(url)
            old_count = len(prod["images"])
            prod["images"] = imgs
            diff = len(imgs) - old_count
            mark = f"+{diff}" if diff > 0 else str(diff)
            print(f"{label} {len(imgs):3d} imgs ({mark})")
            updated += 1
        except Exception as e:
            print(f"{label} ✗ {str(e)[:50]}")
        time.sleep(0.5)   # polite delay

    catalog_path = BASE / "balliu_catalog_full.json"
    with open(catalog_path, "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"\nGuardado: {catalog_path} ({updated} productos)")
    return catalog


# ── Phase 2: Smart mapping ─────────────────────────────────────────────────────

# Size keyword → filename fragment (for Balliu image filenames)
SIZE_KEYWORDS = {
    "individual": ["1p", "individual"],
    "doble":      ["2p", "doble"],
    "triple":     ["3p", "triple"],
    "1 plaza":    ["1p", "individual"],
    "2 plazas":   ["2p", "doble"],
    "3 plazas":   ["3p", "triple"],
}

def find_size_image(images, variant_option):
    """
    Given a variant option string (e.g. "Individual Acrílico") and a list of
    image URLs, return the image that best matches the size keyword.
    Falls back to first image if no match.
    """
    if not variant_option:
        return images[0] if images else None
    opt_lower = variant_option.lower()
    for kw, fragments in SIZE_KEYWORDS.items():
        if kw in opt_lower:
            for img in images:
                fname_lower = img.split("/")[-1].lower()
                if any(frag in fname_lower for frag in fragments):
                    return img
    return images[0] if images else None


def build_hash_to_variant():
    """Read CSV → {lowercase_hash: (csv_handle, option_value)}"""
    mapping = {}
    csv_path = BASE / "balliu_shopify_products.csv"
    if not csv_path.exists():
        return mapping
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row.get("Variant SKU", "")
            opt = row.get("Option1 Value", "")
            csv_handle = row.get("Handle", "")
            if not sku:
                continue
            m = re.search(r"_([0-9A-Fa-f]{8})$", sku)
            if m:
                mapping[m.group(1).lower()] = (csv_handle, opt)
    return mapping


# CSV handle → Balliu catalog slug (complete manual mapping)
CSV_HANDLE_TO_SLUG = {
    "etna-sofa":                       "sofa-etna",
    "olimpia-sofa":                    "sofa-olimpia",
    "etna-tumbona":                    "tumbona-de-aluminio-etna",
    "etna-alta-tumbona-alta":          "tumbona-de-aluminio-etna-alta",
    "olimpia-tumbona":                 "tumbona-con-ruedas-olimpia",
    "marina-tumbona":                  "tumbona-apilable-marina",
    "marina-mini-tumbona":             "mini-tumbona-apilable-marina",
    "cannes-mini-tumbona":             "mini-tumbona-plegable-cannes",
    "bristol-mini-tumbona":            "mini-tumbona-plegable-bristol",
    "eva-pro-tumbona":                 "tumbona-de-resina-eva-pro",
    "eva-rg-tumbona":                  "tumbona-de-playa-evarg",
    "eva-rtg-tumbona":                 "tumbona-de-jardin-de-resina-evartg",
    "noa-tumbona":                     "tumbona-de-resina-noa",
    "lola-tumbona":                    "tumbona-para-playa-lola",
    "carmen-tumbona":                  "tumbona-de-resina-carmen",
    "iris-tumbona":                    "tumbona-iris",
    "bruna-silla":                     "silla-de-resina-bruna",
    "bruna-silla-con-brazos":          "silla-de-resina-con-reposabrazos-bruna",
    "etna-silla":                      "silla-de-aluminio-modelo-etna",
    "mila-silla":                      "silla-de-aluminio-mila",
    "duna-silla":                      "silla-duna",
    "bimba-silla":                     "silla-bimba",
    "vera-silla":                      "silla-vera",
    "silla-venus":                     "silla-de-resina-venus",
    "selva-silla":                     "silla-de-resina-modelo-selva",
    "agata-mesa":                      "mesa-de-aluminio-agata",
    "altea-mesa":                      "mesa-de-aluminio-modelo-altea",
    "atlanta-mesa":                    "mesa-extensible-de-aluminio-atlanta",
    "brunei-mesa":                     "mesa-de-aluminio-brunei",
    "capri-mesa":                      "mesa-de-aluminio-capri",
    "60x60-mesa-alta":                 "mesa-de-aluminio-capri-alta",
    "70x70-mesa-alta":                 "mesa-de-aluminio-capri-alta",
    "diam-70-mesa-alta":               "mesa-de-aluminio-capri-alta",
    "diam-70-mesa":                    "etna-mesa-central",
    "diam-80-mesa":                    "etna-mesa-central",
    "etna-mesa-auxiliar":              "mesa-auxiliar-de-aluminio-modelo-etna",
    "etna-mesa-central":               "etna-mesa-central",
    "mesa-java":                       "mesa-de-aluminio-modelo-java",
    "noa-mesa-auxiliar":               "mesa-auxiliar-de-resina-noa",
    "nora-mesa":                       "mesa-de-aluminio-nora",
    "olimpia-mesa-auxiliar":           "mesa-auxiliar-de-aluminio-olimpia",
    "selva-mesa":                      "mesa-selva",
    "eva-pro-bcn-mesa-auxiliar":       "mesa-auxiliar-eva-pro-bcn",
    "eva-pro-mini-mesa-auxiliar":      "mesa-mini-eva-pro",
    "mini-mesa":                       "mesa-auxiliar-mini-prestige",
    "parasol":                         "parasol-agora",
    "brisa-parasol":                   "parasol-brisa",
    "garbi-parasol":                   "parasol-garbi",
    "roma-parasol":                    "parasol-roma",
    "base-hormigon-25-kg":             "base-de-hormigon-para-parasol",
    "base-hormigon-30-kg":             "base-de-hormigon-para-parasol",
    "pie-parasol-40-kg":               "base-parasol-40",
    "pie-parasol-40-kg-recubrimiento-plastico": "base-parasol-40",
    "colchoneta-tumbona":              "colchoneta-para-tumbona",
    "funda-silla":                     "funda-para-sillas-de-exterior",
    "funda-sofa":                      "funda-sofa-individual-olimpia",
    "funda-tumbona":                   "funda-protectora-para-2-tumbonas",
    "producto-limpiador":              "limpiador-para-tumbona",
    "pasarela-resina":                 "pasarela-de-resina-para-playa",
    "pasarela-resina-reciclada-100":   "pasarela-de-resina-para-playa",
    "weguard-caja-de-seguridad":       "caja-de-seguridad-weguard-para-tumbona",
    "aura-cama-balinesa":              None,   # not in scraped catalog
    "alma-cama-balinesa":              None,
    "greta-silla":                     None,
    "greta-mesa":                      None,
    "sofia-mesa":                      None,
    "cojin-40x40":                     None,
    "alba-tumbona":                    None,
    "funda-parasol":                   None,
}


def build_smart_mapping(catalog):
    """
    Build an enhanced mapping: for every Shopify Balliu product,
    find the Balliu slug + ALL images + primary image for this variant.
    Returns list of {shopify_id, shopify_handle, balliu_slug, primary_image, all_images}
    """
    print("\n── Fase 2: Construyendo mapeo inteligente ─────────────────────────────\n")

    # Load original image mapping for slug↔shopify cross-reference
    with open(BASE / "balliu_image_mapping.json") as f:
        base_map = json.load(f)

    hash_to_variant = build_hash_to_variant()
    print(f"  Variantes CSV cargadas: {len(hash_to_variant)}")

    slug_lookup = {}  # shopify_id → {slug, score}
    for item in base_map:
        if item.get("balliu_slug"):
            slug_lookup[item["shopify_id"]] = item["balliu_slug"]

    # Fetch all Balliu Shopify products from API
    all_products = []
    cursor = None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        data = gql(f"""{{
            products(first: 100{after}, query: "vendor:Balliu") {{
                edges {{ node {{
                    id handle title
                    images(first: 10) {{ edges {{ node {{ id src }} }} }}
                }} }}
                pageInfo {{ hasNextPage endCursor }}
            }}
        }}""")
        edges = data["products"]["edges"]
        all_products.extend(edges)
        pi = data["products"]["pageInfo"]
        if not pi["hasNextPage"]:
            break
        cursor = pi["endCursor"]

    print(f"  Productos Shopify Balliu: {len(all_products)}")

    smart_map = []
    for edge in all_products:
        p = edge["node"]
        pid     = p["id"]
        handle  = p["handle"]
        title   = p["title"]
        current_imgs = [e["node"]["src"] for e in p["images"]["edges"]]

        # Extract hash from handle
        m = re.search(r"-([0-9a-f]{8})(?:-\d+)?$", handle)
        hash_val = m.group(1) if m else None

        # Get variant option from CSV
        variant_opt = hash_to_variant.get(hash_val, "") if hash_val else ""

        # Get Balliu slug
        balliu_slug = slug_lookup.get(pid)

        # Get images for this slug
        all_imgs  = catalog.get(balliu_slug, {}).get("images", []) if balliu_slug else []
        prim_img  = find_size_image(all_imgs, variant_opt) if all_imgs else None

        smart_map.append({
            "shopify_id":      pid,
            "shopify_handle":  handle,
            "shopify_title":   title,
            "hash":            hash_val,
            "variant_option":  variant_opt,
            "balliu_slug":     balliu_slug,
            "primary_image":   prim_img,
            "gallery_images":  all_imgs,
            "current_imgs":    len(current_imgs),
        })

    # Show summary
    with_primary = sum(1 for x in smart_map if x["primary_image"])
    with_gallery = sum(1 for x in smart_map if x["gallery_images"])
    print(f"  Con imagen primaria: {with_primary}/{len(smart_map)}")
    print(f"  Con galería completa: {with_gallery}/{len(smart_map)}")

    # Save
    out = BASE / "balliu_smart_mapping.json"
    with open(out, "w") as f:
        json.dump(smart_map, f, indent=2, ensure_ascii=False)
    print(f"\nGuardado: {out}")
    return smart_map


# ── Phase 3: Download images ───────────────────────────────────────────────────

def download_all_images(smart_map):
    print("\n── Fase 3: Descargando imágenes ───────────────────────────────────────\n")
    all_urls = set()
    for item in smart_map:
        for img in item["gallery_images"]:
            all_urls.add(img)

    print(f"  URLs únicas a descargar: {len(all_urls)}\n")
    url_to_path = {}
    downloaded = 0

    for i, url in enumerate(sorted(all_urls), 1):
        fname = url.split("/")[-1]
        dest  = IMG_DIR / fname
        url_to_path[url] = dest
        label = f"[{i:03d}/{len(all_urls)}] {fname[:60]:<62}"
        if dest.exists():
            print(f"{label} (ya existe)")
            continue
        if DRY_RUN:
            print(f"{label} (dry-run)")
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            dest.write_bytes(data)
            print(f"{label} ✓ ({len(data)//1024} KB)")
            downloaded += 1
        except Exception as e:
            print(f"{label} ✗ {str(e)[:50]}")
        time.sleep(0.2)

    print(f"\nDescargadas: {downloaded} nuevas | Total en disco: {len(list(IMG_DIR.iterdir()))}")
    return url_to_path


# ── Phase 4: Upload to Shopify ─────────────────────────────────────────────────

def staged_upload(filename, file_size, mime="image/jpeg"):
    data = gql("""
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
    """, {"input": [{"filename": filename, "mimeType": mime,
                     "fileSize": str(file_size), "resource": "IMAGE", "httpMethod": "POST"}]})
    errs = data["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(", ".join(e["message"] for e in errs))
    return data["stagedUploadsCreate"]["stagedTargets"][0]


def upload_to_s3(target, file_bytes, filename):
    boundary = b"----BalliuBoundary2"
    parts = []
    for p in target["parameters"]:
        parts.append(b"--" + boundary + b"\r\nContent-Disposition: form-data; name=\""
                     + p["name"].encode() + b"\"\r\n\r\n" + p["value"].encode() + b"\r\n")
    ext = filename.rsplit(".", 1)[-1].lower()
    mime = "image/png" if ext == "png" else "image/webp" if ext == "webp" else "image/jpeg"
    parts.append(b"--" + boundary + b"\r\nContent-Disposition: form-data; name=\"file\"; filename=\""
                 + filename.encode() + b"\"\r\nContent-Type: " + mime.encode() + b"\r\n\r\n"
                 + file_bytes + b"\r\n")
    parts.append(b"--" + boundary + b"--\r\n")
    body = b"".join(parts)
    req = urllib.request.Request(target["url"], data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode()}"})
    try:
        urllib.request.urlopen(req, timeout=60).close()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"S3 {e.code}: {e.read()[:200]}")
    return target["resourceUrl"]


def create_product_media(product_id, cdn_url):
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


def upload_images_to_shopify(smart_map, url_to_path):
    print("\n── Fase 4: Subiendo imágenes al CDN y adjuntando a productos ──────────\n")

    # Upload unique images to CDN first
    cdn_cache = {}   # local_path → cdn_url
    unique_paths = set()
    for item in smart_map:
        for img_url in item["gallery_images"]:
            local = url_to_path.get(img_url)
            if local and local.exists():
                unique_paths.add(local)

    print(f"  Subiendo {len(unique_paths)} imágenes únicas al CDN...\n")
    for i, path in enumerate(sorted(unique_paths), 1):
        if path in cdn_cache:
            continue
        label = f"  [{i:03d}/{len(unique_paths)}] {path.name[:60]:<62}"
        if DRY_RUN:
            cdn_cache[path] = f"https://cdn.shopify.com/dry-run/{path.name}"
            print(f"{label} (dry-run)")
            continue
        try:
            file_bytes = path.read_bytes()
            ext  = path.suffix.lower()
            mime = "image/png" if ext == ".png" else "image/webp" if ext == ".webp" else "image/jpeg"
            target  = staged_upload(path.name, len(file_bytes), mime)
            cdn_url = upload_to_s3(target, file_bytes, path.name)
            cdn_cache[path] = cdn_url
            print(f"{label} ✓")
        except Exception as e:
            print(f"{label} ✗ {str(e)[:80]}")
        time.sleep(0.3)

    # Assign images to products
    print(f"\n  Adjuntando imágenes a {len(smart_map)} productos...\n")
    ok = skip = fail = 0
    for item in smart_map:
        pid   = item["shopify_id"]
        title = item["shopify_title"][:50]
        var   = item.get("variant_option","") or "—"
        slug  = item.get("balliu_slug","—") or "—"

        if not item["gallery_images"]:
            print(f"  ⚠ {title[:55]:57} sin imágenes en catálogo")
            skip += 1
            continue

        # Skip if already has enough images
        if item["current_imgs"] >= len(item["gallery_images"]):
            print(f"  ✓ {title[:55]:57} ya tiene {item['current_imgs']} imgs (OK)")
            skip += 1
            continue

        # Determine upload order: primary image first, then rest
        primary = item["primary_image"]
        gallery = item["gallery_images"]
        ordered = ([primary] + [x for x in gallery if x != primary]) if primary else gallery

        uploaded = 0
        for img_url in ordered:
            local = url_to_path.get(img_url)
            if not local or not local.exists():
                continue
            cdn_url = cdn_cache.get(local)
            if not cdn_url:
                continue
            if DRY_RUN:
                uploaded += 1
                continue
            try:
                create_product_media(pid, cdn_url)
                uploaded += 1
            except Exception as e:
                pass  # silently skip duplicates
            time.sleep(0.2)

        if uploaded:
            print(f"  ✓ {title[:45]:47} var={var[:18]:20} +{uploaded} imgs ({slug[:25]})")
            ok += 1
        else:
            print(f"  ✗ {title[:55]:57} sin CDN URLs disponibles")
            fail += 1

    print(f"\n✅ Completado: {ok} actualizados | {skip} omitidos | {fail} errores")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # Phase 1: Rescrape
    catalog_full_path = BASE / "balliu_catalog_full.json"
    if catalog_full_path.exists() and not ("--rescrape" in sys.argv):
        print(f"Usando catálogo existente: {catalog_full_path}")
        print("(Añade --rescrape para re-extraer la web)\n")
        with open(catalog_full_path) as f:
            catalog = json.load(f)
    else:
        catalog = rescrape_catalog()

    if SCRAPE_ONLY:
        print("--scrape-only: terminando tras fase 1.")
        return

    # Phase 2: Smart mapping
    smart_mapping_path = BASE / "balliu_smart_mapping.json"
    if smart_mapping_path.exists() and not ("--remap" in sys.argv):
        print(f"Usando mapeo existente: {smart_mapping_path}")
        print("(Añade --remap para reconstruir el mapeo)\n")
        with open(smart_mapping_path) as f:
            smart_map = json.load(f)
    else:
        smart_map = build_smart_mapping(catalog)

    # Phase 3: Download
    url_to_path = download_all_images(smart_map)

    if DRY_RUN:
        print("\n── DRY-RUN: muestra de asignaciones ─────────────────────────────────\n")
        for item in smart_map[:20]:
            prim = item["primary_image"]
            prim_name = prim.split("/")[-1] if prim else "—"
            print(f"  {item['shopify_title'][:45]:47} var={item.get('variant_option',''):20} → {prim_name}")
        return

    # Phase 4: Upload
    upload_images_to_shopify(smart_map, url_to_path)


if __name__ == "__main__":
    main()
