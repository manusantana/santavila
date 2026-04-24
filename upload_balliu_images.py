#!/usr/bin/env python3
"""
Descarga imágenes de balliuexport.com y las sube a los productos Shopify
correspondientes según balliu_image_mapping.json.

Uso: python3 upload_balliu_images.py [--dry-run]
"""

import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

from config import SHOPIFY_ACCESS_TOKEN as TOKEN
SHOP  = "mueblesexterior.myshopify.com"
API   = f"https://{SHOP}/admin/api/2026-01/graphql.json"
BASE  = Path(__file__).parent
IMG_DIR = BASE / "images_balliu"
IMG_DIR.mkdir(exist_ok=True)

DRY_RUN = "--dry-run" in sys.argv

# ── GraphQL helper ─────────────────────────────────────────────────────────────

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:300])
    return data["data"]

# ── Download image ─────────────────────────────────────────────────────────────

def download_image(url, dest_path):
    req = urllib.request.Request(url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MueblesBot/1.0)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest_path, "wb") as f:
        f.write(data)
    return len(data)

# ── Staged upload ──────────────────────────────────────────────────────────────

def staged_upload(filename, file_size):
    data = gql("""
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
    """, {"input": [{"filename": filename, "mimeType": "image/jpeg",
                     "fileSize": str(file_size), "resource": "IMAGE", "httpMethod": "POST"}]})
    errs = data["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(", ".join(e["message"] for e in errs))
    return data["stagedUploadsCreate"]["stagedTargets"][0]

def upload_to_s3(target, file_path):
    file_bytes = Path(file_path).read_bytes()
    boundary   = b"----BalliuBoundary"
    parts = []
    for p in target["parameters"]:
        parts.append(b"--" + boundary + b"\r\nContent-Disposition: form-data; name=\""
                     + p["name"].encode() + b"\"\r\n\r\n" + p["value"].encode() + b"\r\n")
    parts.append(b"--" + boundary + b"\r\nContent-Disposition: form-data; name=\"file\"; filename=\""
                 + Path(file_path).name.encode() + b"\"\r\nContent-Type: image/jpeg\r\n\r\n"
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

# ── Shopify product helpers ────────────────────────────────────────────────────

def product_has_images(product_id):
    data = gql("""
        query($id: ID!) {
          product(id: $id) {
            images(first: 5) { edges { node { src } } }
          }
        }
    """, {"id": product_id})
    edges = data["product"]["images"]["edges"]
    return len(edges) > 0

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

# ── main ───────────────────────────────────────────────────────────────────────

def main():
    with open(BASE / "balliu_image_mapping.json") as f:
        mapping = json.load(f)

    # Filter valid entries (score > 0)
    valid = [m for m in mapping if m.get("score", 0) > 0 and m.get("image")]
    skipped = len(mapping) - len(valid)

    print(f"Total entradas: {len(mapping)} | Válidas: {len(valid)} | Omitidas (sin match): {skipped}")
    if DRY_RUN:
        print("🔍 MODO DRY-RUN\n")
    print()

    # Deduplicate: same image URL → download once
    url_to_path = {}
    for item in valid:
        url = item["image"]
        if url not in url_to_path:
            ext = url.split(".")[-1].split("?")[0]
            fname = f"balliu_{item['balliu_slug'][:50]}.{ext}"
            url_to_path[url] = IMG_DIR / fname

    # Step 1: Download all images
    print(f"── Descargando {len(url_to_path)} imágenes únicas ─────────────────────\n")
    cdn_map = {}  # url → shopify CDN url
    downloaded = 0
    for i, (url, local_path) in enumerate(url_to_path.items(), 1):
        label = f"[{i}/{len(url_to_path)}] {local_path.name[:50]:<52}"
        if local_path.exists():
            print(f"{label} (ya existe)")
        elif DRY_RUN:
            print(f"{label} (dry-run)")
            continue
        else:
            try:
                size = download_image(url, local_path)
                print(f"{label} ✓ ({size // 1024} KB)")
                downloaded += 1
            except Exception as e:
                print(f"{label} ✗ {str(e)[:60]}")
                continue

    if DRY_RUN:
        print("\n── DRY-RUN: mostrando matches ──────────────────────────────────────\n")
        for item in valid:
            print(f"  {item['shopify_title'][:45]:45} score={item['score']} → {item['balliu_title'][:35]}")
        return

    # Step 2: Upload images to Shopify CDN
    print(f"\n── Subiendo imágenes al CDN de Shopify ────────────────────────────────\n")
    for i, (url, local_path) in enumerate(url_to_path.items(), 1):
        if not local_path.exists():
            continue
        label = f"[{i}/{len(url_to_path)}] {local_path.name[:50]:<52}"
        if url in cdn_map:
            print(f"{label} (ya subida)")
            continue
        try:
            target  = staged_upload(local_path.name, local_path.stat().st_size)
            cdn_url = upload_to_s3(target, local_path)
            cdn_map[url] = cdn_url
            print(f"{label} ✓")
        except Exception as e:
            print(f"{label} ✗ {str(e)[:80]}")
        time.sleep(0.3)

    # Step 3: Attach images to products
    print(f"\n── Adjuntando imágenes a productos ({len(valid)} asignaciones) ───────────\n")
    ok = 0
    for item in valid:
        cdn_url = cdn_map.get(item["image"])
        if not cdn_url:
            print(f"  ⚠ Sin CDN URL: {item['shopify_handle'][:60]}")
            continue
        try:
            if product_has_images(item["shopify_id"]):
                print(f"  ✓ {item['shopify_title'][:55]} (ya tiene imagen)")
                ok += 1
                continue
            create_product_media(item["shopify_id"], cdn_url)
            print(f"  ✓ {item['shopify_title'][:55]} → {item['balliu_title'][:30]}")
            ok += 1
        except Exception as e:
            print(f"  ✗ {item['shopify_handle'][:55]}: {str(e)[:80]}")
        time.sleep(0.3)

    print(f"\n✅ Completado: {ok}/{len(valid)} productos actualizados.")
    print(f"   Imágenes en: {IMG_DIR}")

if __name__ == "__main__":
    main()
