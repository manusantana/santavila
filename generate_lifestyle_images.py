#!/usr/bin/env python3
"""
Genera imágenes lifestyle para productos de exterior usando:
  1. rembg  → elimina el fondo de la foto original
  2. FLUX.1-schnell (HF) → genera imagen lifestyle completa
  3. Shopify API → sube la imagen al producto

Uso:
  python3 generate_lifestyle_images.py              # todos los productos
  python3 generate_lifestyle_images.py sillon       # filtra por handle
  python3 generate_lifestyle_images.py --dry-run    # solo muestra prompts, no genera
"""

import csv, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path
from io import BytesIO

try:
    from PIL import Image
    from rembg import remove as rembg_remove
    HAS_REMBG = True
except ImportError:
    HAS_REMBG = False
    print("⚠ rembg no instalado — se omitirá el recorte de fondo")

# ── Configuración ─────────────────────────────────────────────────────────────

BASE        = Path(__file__).parent
from config import HF_TOKEN
from config import SHOPIFY_ACCESS_TOKEN as SHOPIFY_TOKEN
SHOP        = "mueblesexterior.myshopify.com"
SHOPIFY_API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
HF_URL      = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
OUTPUT_DIR  = BASE / "images_lifestyle"
OUTPUT_DIR.mkdir(exist_ok=True)

# Estilo visual consistente para toda la tienda
STYLE_SUFFIX = (
    "mediterranean outdoor terrace, warm afternoon sunlight, "
    "natural wood decking, terracotta pots with plants, "
    "photorealistic, high quality, 4k, lifestyle photography"
)

# ── Helpers HTTP ──────────────────────────────────────────────────────────────

def shopify_gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(SHOPIFY_API, data=payload,
        headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(str(data["errors"])[:300])
    return data["data"]

def hf_generate(prompt, output_path):
    payload = json.dumps({
        "inputs": prompt,
        "parameters": {"num_inference_steps": 4, "width": 1024, "height": 768}
    }).encode()
    req = urllib.request.Request(HF_URL, data=payload,
        headers={"Authorization": f"Bearer {HF_TOKEN}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        img_bytes = r.read()
    with open(output_path, "wb") as f:
        f.write(img_bytes)
    return output_path

# ── Generación de prompt ──────────────────────────────────────────────────────

def build_prompt(title, product_type, description_text=""):
    """Construye un prompt lifestyle específico para cada tipo de producto."""
    type_lower = product_type.lower() if product_type else ""

    if "sillón" in type_lower or "sillon" in type_lower:
        scene = "single modern outdoor armchair on a sunny terrace"
    elif "sofá" in type_lower or "sofa" in type_lower:
        scene = "modern outdoor sofa on a spacious terrace"
    elif "conjunto" in type_lower or "set" in type_lower:
        scene = "complete outdoor lounge set on a large sunny terrace"
    elif "rinconera" in type_lower:
        scene = "outdoor corner sofa set on a rooftop terrace"
    elif "mesa comedor" in type_lower:
        scene = "outdoor dining table on a terrace with chairs around it"
    elif "mesa" in type_lower:
        scene = "outdoor coffee table on a terrace"
    elif "tumbona" in type_lower:
        scene = "outdoor sun lounger by a swimming pool"
    elif "parasol" in type_lower:
        scene = "large outdoor parasol over a terrace dining area"
    elif "pérgola" in type_lower or "pergola" in type_lower:
        scene = "elegant outdoor pergola in a garden"
    elif "banco" in type_lower:
        scene = "outdoor bench in a garden setting"
    elif "balancín" in type_lower:
        scene = "outdoor hanging swing chair in a garden"
    elif "silla" in type_lower:
        scene = "modern outdoor dining chair on a restaurant terrace"
    else:
        scene = "modern outdoor furniture on a sunny terrace"

    # Extraer material del título si lo hay
    material = ""
    title_lower = title.lower()
    if "aluminio" in title_lower:
        material = "aluminum frame furniture, "
    elif "hpl" in title_lower:
        material = "HPL top furniture, "

    prompt = f"{scene}, {material}professional product photography, {STYLE_SUFFIX}"
    return prompt

# ── Pipeline principal ────────────────────────────────────────────────────────

def get_product_info(handle):
    data = shopify_gql("""
        query($handle: String!) {
          productByHandle(handle: $handle) {
            id
            title
            productType
            images(first: 5) { edges { node { id src } } }
          }
        }
    """, {"handle": handle})
    return data.get("productByHandle")

def upload_lifestyle_image(product_id, image_path):
    """Sube imagen vía staged upload y la adjunta al producto."""
    file_bytes = Path(image_path).read_bytes()
    filename   = Path(image_path).name
    file_size  = len(file_bytes)

    # Staged upload
    data = shopify_gql("""
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
    """, {"input": [{"filename": filename, "mimeType": "image/jpeg",
                     "fileSize": str(file_size), "resource": "IMAGE",
                     "httpMethod": "POST"}]})
    target = data["stagedUploadsCreate"]["stagedTargets"][0]

    # Upload a S3
    boundary = b"----LifestyleBoundary"
    parts = []
    for p in target["parameters"]:
        parts.append(b"--" + boundary + b"\r\nContent-Disposition: form-data; name=\""
                     + p["name"].encode() + b"\"\r\n\r\n" + p["value"].encode() + b"\r\n")
    parts.append(b"--" + boundary + b"\r\nContent-Disposition: form-data; name=\"file\"; filename=\""
                 + filename.encode() + b"\"\r\nContent-Type: image/jpeg\r\n\r\n"
                 + file_bytes + b"\r\n")
    parts.append(b"--" + boundary + b"--\r\n")
    body = b"".join(parts)

    req = urllib.request.Request(target["url"], data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode()}"})
    urllib.request.urlopen(req, timeout=60).close()
    cdn_url = target["resourceUrl"]

    # Adjuntar al producto
    data = shopify_gql("""
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
        raise RuntimeError(str(errs))
    return cdn_url

def process_product(handle, product_type=None, dry_run=False):
    product = get_product_info(handle)
    if not product:
        print(f"  ⚠ No encontrado: {handle}")
        return False

    title   = product["title"]
    ptype   = product_type or product.get("productType", "")
    prompt  = build_prompt(title, ptype)
    out_file = OUTPUT_DIR / f"{handle[:60]}_lifestyle.jpg"

    print(f"\n  Título : {title}")
    print(f"  Prompt : {prompt[:100]}...")

    if dry_run:
        return True

    # Generar imagen
    print(f"  Generando...", end=" ", flush=True)
    try:
        hf_generate(prompt, out_file)
        print(f"✓ ({out_file.stat().st_size // 1024} KB)")
    except Exception as e:
        print(f"✗ {e}")
        return False

    # Subir a Shopify
    print(f"  Subiendo a Shopify...", end=" ", flush=True)
    try:
        upload_lifestyle_image(product["id"], out_file)
        print("✓")
    except Exception as e:
        print(f"✗ {e}")
        return False

    return True

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    args     = sys.argv[1:]
    dry_run  = "--dry-run" in args
    filters  = [a for a in args if not a.startswith("--")]

    if dry_run:
        print("🔍 MODO DRY-RUN — solo muestra prompts, no genera imágenes\n")

    # Leer productos del CSV
    csv_path = BASE / "shopify_products_optimized.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Solo primera fila de cada producto (tiene Handle)
    handles_seen = set()
    products = []
    for row in rows:
        h = row.get("Handle", "").strip()
        t = row.get("Type", "").strip()
        if h and h not in handles_seen:
            handles_seen.add(h)
            if not filters or any(f in h for f in filters):
                products.append((h, t))

    print(f"Productos a procesar: {len(products)}\n")
    ok = 0
    for i, (handle, ptype) in enumerate(products, 1):
        print(f"[{i}/{len(products)}] {handle[:65]}")
        if process_product(handle, ptype, dry_run=dry_run):
            ok += 1
        if not dry_run:
            time.sleep(1)  # rate limit HF

    print(f"\n✅ Completado: {ok}/{len(products)} productos procesados.")
    print(f"   Imágenes guardadas en: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
