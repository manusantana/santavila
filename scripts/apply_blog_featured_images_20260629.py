#!/usr/bin/env python3
"""
Añade imagen destacada a guías GEO del blog y alt text descriptivo.

Dry-run por defecto:
  .venv/bin/python scripts/apply_blog_featured_images_20260629.py

Aplicar:
  .venv/bin/python scripts/apply_blog_featured_images_20260629.py --apply
"""
import base64
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API_VERSION = "2026-01"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
BLOG_HANDLE = "news"
ONLY = None
if "--only" in sys.argv:
    idx = sys.argv.index("--only")
    if idx + 1 < len(sys.argv):
        ONLY = sys.argv[idx + 1]

IMAGES = {
    "tumbona-de-aluminio-resina-o-madera-cual-elegir-para-exterior": {
        "path": "images_balliu/Tumbona-Etna_Mesa-auxiliar-Etna_C.jpg",
        "alt": "Tumbonas de exterior Balliu en jardín con mesa auxiliar junto a piscina",
    },
    "que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol": {
        "path": "images_balliu/balliu-eva-pro-pamela-sun-umbrella-outdoor-furniture-mobiliario-terraza-jardin-01-scaled.jpg",
        "alt": "Tumbonas y parasol de exterior junto al mar para protegerse del sol",
    },
    "como-elegir-mesa-de-exterior-medidas-comensales-y-espacio-necesario": {
        "path": "images_balliu/Atlanta_Silla-Etna_blanco2.jpg",
        "alt": "Mesa de exterior con sillas en porche mediterráneo",
    },
    "guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada": {
        "path": "content/images/blog/mantenimiento-tumbona-piscina-cubierta-20260629.png",
        "alt": "Tumbona de exterior junto a piscina protegida con funda",
    },
    "como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales": {
        "path": None,
        "alt": "Terraza pequeña amueblada con piezas compactas y distribución funcional",
    },
}


def request(method, path, payload=None, attempts=3):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        },
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:1000]
            raise RuntimeError(f"HTTP {exc.code} {method} {path}: {detail}") from exc
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)


def get_blog_id():
    data = request("GET", f"blogs.json?handle={urllib.parse.quote(BLOG_HANDLE)}")
    blogs = data.get("blogs", [])
    if not blogs:
        raise RuntimeError(f"No encuentro blog handle={BLOG_HANDLE}")
    return blogs[0]["id"]


def get_article(blog_id, handle):
    data = request("GET", f"blogs/{blog_id}/articles.json?handle={urllib.parse.quote(handle)}")
    articles = data.get("articles", [])
    return articles[0] if articles else None


def image_payload(spec, existing_image):
    if spec["path"]:
        path = os.path.join(ROOT, spec["path"])
        with open(path, "rb") as fh:
            encoded = base64.b64encode(fh.read()).decode()
        return {
            "attachment": encoded,
            "filename": os.path.basename(path),
            "alt": spec["alt"],
        }
    if existing_image and existing_image.get("src"):
        return {
            "src": existing_image["src"],
            "alt": spec["alt"],
        }
    return None


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacio")

    blog_id = get_blog_id()
    backup = {}
    updates = {}
    errors = 0
    targets = {ONLY: IMAGES[ONLY]} if ONLY else IMAGES
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - imagen destacada en {len(targets)} guias\n")

    for handle, spec in targets.items():
        try:
            article = get_article(blog_id, handle)
        except Exception as exc:
            print(f"✗ {handle}: error leyendo ({exc})")
            errors += 1
            continue
        if not article:
            print(f"✗ {handle}: no encontrado")
            errors += 1
            continue
        existing = article.get("image")
        payload = image_payload(spec, existing)
        if not payload:
            print(f"✗ {handle}: sin imagen existente ni path local")
            errors += 1
            continue
        backup[handle] = {
            "id": article["id"],
            "handle": article["handle"],
            "title": article["title"],
            "image": existing,
        }
        updates[handle] = (article, payload)
        print(f"• {handle}")
        print(f"  title: {article['title']}")
        print(f"  actual: {existing.get('src') if existing else 'sin imagen'}")
        print(f"  accion: {'actualizar alt existente' if not spec['path'] else 'subir imagen local'}")
        print(f"  alt: {spec['alt']}")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(ROOT, "content", "descriptions", f"backup_blog_featured_images_{ts}.json")
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)
    print(f"\nBackup -> {backup_path}")

    if APPLY:
        print("\nAplicando cambios...")
        for handle, (article, payload) in updates.items():
            try:
                request(
                    "PUT",
                    f"blogs/{blog_id}/articles/{article['id']}.json",
                    {"article": {"id": article["id"], "image": payload}},
                )
                print(f"✓ {handle}")
            except Exception as exc:
                print(f"✗ {handle}: error aplicando ({exc})")
                errors += 1

    print(f"{'Aplicado' if APPLY else 'Dry-run'} · errores: {errors}")
    if not APPLY:
        print("Revisa el dry-run y ejecuta con --apply para publicar.")


if __name__ == "__main__":
    main()
