#!/usr/bin/env python3
"""Sube los creativos RRSS (lote 1) a Shopify Files y guarda las URLs del CDN.

Reutiliza el flujo stagedUploadsCreate de upload_images.py, pero termina en
fileCreate (Archivos genericos, no media de producto).

Uso:
  .venv/bin/python scripts/upload_social_files_20260803.py

Salida: content/social/cdn_urls.json  { "pin-01-...": "https://cdn.shopify.com/..." }
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from upload_images import gql, staged_upload, upload_to_s3  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOCIAL = os.path.join(ROOT, "content", "social")
OUT_JSON = os.path.join(SOCIAL, "cdn_urls.json")

FILES = sorted(
    [os.path.join(SOCIAL, "pins", f) for f in os.listdir(os.path.join(SOCIAL, "pins")) if f.endswith(".png")]
    + [
        os.path.join(SOCIAL, "ig", "carrusel-01", f)
        for f in os.listdir(os.path.join(SOCIAL, "ig", "carrusel-01"))
        if f.endswith(".png")
    ]
)

FILE_CREATE = """
mutation fileCreate($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files { id fileStatus }
    userErrors { field message }
  }
}
"""

FILE_QUERY = """
query file($id: ID!) {
  node(id: $id) {
    ... on MediaImage { fileStatus image { url } }
  }
}
"""


def main():
    urls = {}
    for path in FILES:
        name = os.path.basename(path)
        # el slide-XX.png del carrusel necesita nombre unico en Files
        if name.startswith("slide-"):
            name = "carrusel-01-" + name
        target = staged_upload(name, os.path.getsize(path))
        upload_to_s3(target, path)
        data = gql(FILE_CREATE, {
            "files": [{
                "originalSource": target["resourceUrl"],
                "contentType": "IMAGE",
                "alt": f"Santavila RRSS lote 1 - {name}",
            }]
        })
        errs = data["fileCreate"]["userErrors"]
        if errs:
            raise SystemExit(f"fileCreate error en {name}: {errs}")
        fid = data["fileCreate"]["files"][0]["id"]

        url = None
        for _ in range(20):
            node = gql(FILE_QUERY, {"id": fid})["node"]
            if node and node.get("fileStatus") == "READY" and node.get("image"):
                url = node["image"]["url"]
                break
            time.sleep(2)
        if not url:
            raise SystemExit(f"El archivo {name} no llego a READY")
        key = os.path.splitext(name)[0]
        urls[key] = url
        print(f"{key} -> {url}")

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2, ensure_ascii=False)
    print("\nGuardado en", OUT_JSON)


if __name__ == "__main__":
    main()
