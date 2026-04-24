#!/usr/bin/env python3
"""
Sube imágenes optimizadas a Shopify CDN y actualiza los productos.
Uso: python3 upload_images.py
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

from config import SHOPIFY_ACCESS_TOKEN as TOKEN
SHOP  = "mueblesexterior.myshopify.com"
API   = f"https://{SHOP}/admin/api/2026-01/graphql.json"
BASE  = Path(__file__).parent

# ── GraphQL helper ────────────────────────────────────────────────────────────

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:300])
    return data["data"]

# ── Staged upload ─────────────────────────────────────────────────────────────

def staged_upload(filename, file_size):
    data = gql("""
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets {
              url
              resourceUrl
              parameters { name value }
            }
            userErrors { field message }
          }
        }
    """, {"input": [{
        "filename":   filename,
        "mimeType":   "image/jpeg",
        "fileSize":   str(file_size),
        "resource":   "IMAGE",
        "httpMethod": "POST",
    }]})
    errs = data["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(", ".join(e["message"] for e in errs))
    return data["stagedUploadsCreate"]["stagedTargets"][0]

def upload_to_s3(target, file_path):
    file_bytes = Path(file_path).read_bytes()
    boundary   = b"----FormBoundary7MA4YWxkTrZu0gW"

    body_parts = []
    for p in target["parameters"]:
        body_parts.append(
            b"--" + boundary + b"\r\n"
            b'Content-Disposition: form-data; name="' + p["name"].encode() + b'"\r\n\r\n'
            + p["value"].encode() + b"\r\n"
        )
    body_parts.append(
        b"--" + boundary + b"\r\n"
        b'Content-Disposition: form-data; name="file"; filename="' + Path(file_path).name.encode() + b'"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        + file_bytes + b"\r\n"
    )
    body_parts.append(b"--" + boundary + b"--\r\n")
    body = b"".join(body_parts)

    req = urllib.request.Request(
        target["url"],
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode()}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            pass
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"S3 {e.code}: {e.read()[:200]}")
    return target["resourceUrl"]

# ── Product helpers ───────────────────────────────────────────────────────────

def get_product_by_handle(handle):
    data = gql("""
        query($handle: String!) {
          productByHandle(handle: $handle) {
            id
            images(first: 20) {
              edges { node { id src } }
            }
          }
        }
    """, {"handle": handle})
    return data.get("productByHandle")

def create_product_media(product_id, cdn_url):
    data = gql("""
        mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media {
              ... on MediaImage {
                id
                image { url }
              }
            }
            mediaUserErrors { field message }
          }
        }
    """, {
        "productId": product_id,
        "media": [{"originalSource": cdn_url, "mediaContentType": "IMAGE"}],
    })
    errs = data["productCreateMedia"]["mediaUserErrors"]
    if errs:
        raise RuntimeError(", ".join(e["message"] for e in errs))
    return data["productCreateMedia"]["media"]

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    csv_path = BASE / "shopify_products_optimized.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Build map: local_img_path → [handles]
    image_map = {}
    for row in rows:
        img = row.get("Image Src", "").strip()
        if not img.startswith("images_optimized/"):
            continue
        local = BASE / img
        if not local.exists():
            print(f"⚠ No existe: {img}")
            continue
        if img not in image_map:
            image_map[img] = []
        handle = row.get("Handle", "").strip()
        if handle and handle not in image_map[img]:
            image_map[img].append(handle)

    print(f"\nImágenes a subir: {len(image_map)}\n")

    cdn_map = {}
    for i, (img_path, handles) in enumerate(image_map.items(), 1):
        local = BASE / img_path
        filename = local.name
        file_size = local.stat().st_size
        label = f"[{i}/{len(image_map)}] {filename[:48]:<48}"
        sys.stdout.write(f"{label} ")
        sys.stdout.flush()
        try:
            target  = staged_upload(filename, file_size)
            cdn_url = upload_to_s3(target, local)
            cdn_map[img_path] = cdn_url
            print("✓")
        except Exception as e:
            print(f"✗  {str(e)[:80]}")

    print(f"\n── Actualizando productos ({len(cdn_map)} imágenes subidas) ────────────\n")

    done = set()
    for img_path, handles in image_map.items():
        cdn_url = cdn_map.get(img_path)
        if not cdn_url:
            continue
        for handle in handles:
            key = (handle, img_path)
            if key in done:
                continue
            done.add(key)
            try:
                product = get_product_by_handle(handle)
                if not product:
                    print(f"  ⚠ No encontrado: {handle}")
                    continue
                filename = Path(img_path).name
                already  = any(filename in e["node"]["src"] for e in product["images"]["edges"])
                if already:
                    print(f"  ✓ {handle[:70]} (ya tiene imagen)")
                    continue
                create_product_media(product["id"], cdn_url)
                print(f"  ✓ {handle[:70]}")
                time.sleep(0.3)  # rate limit
            except Exception as e:
                print(f"  ✗ {handle[:60]}: {str(e)[:100]}")

    print("\n✅ Completado.\n")

if __name__ == "__main__":
    main()
