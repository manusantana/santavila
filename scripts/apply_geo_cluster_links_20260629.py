#!/usr/bin/env python3
"""
Sprint GEO 2026-06-29: refuerzo de enlazado interno por señales GSC.

Dry-run por defecto:
  .venv/bin/python scripts/apply_geo_cluster_links_20260629.py

Aplicar:
  .venv/bin/python scripts/apply_geo_cluster_links_20260629.py --apply
"""
import datetime
import json
import os
import re
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

START = "<!-- sv-gsc-links-20260629:start -->"
END = "<!-- sv-gsc-links-20260629:end -->"

BLOCKS = {
    "tumbona-de-aluminio-resina-o-madera-cual-elegir-para-exterior": {
        "label": "tumbonas Balliu y resina",
        "before": r"<h2>Preguntas frecuentes</h2>",
        "html": """
<h2>Modelos de tumbona que ya reciben señales en Google</h2>
<p>Si estás comparando por material, las búsquedas actuales de Santavila apuntan sobre todo a tumbonas Balliu y tumbonas de resina para jardín o piscina. Para empezar por productos concretos, revisa la <a href="/products/balliu-tumbona-de-exterior-resina-28ff014d">tumbona Balliu de resina</a>, la <a href="/products/balliu-tumbona-de-exterior-resina-75-cm-009e68e4">tumbona Balliu de resina de 75 cm</a> y la <a href="/products/balliu-tumbona-de-exterior-aluminio-d08586c1">tumbona Balliu de aluminio</a>. Si prefieres comparar todo el catálogo, entra en la colección de <a href="/collections/tumbonas">tumbonas de exterior</a>.</p>
""",
    },
    "que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol": {
        "label": "sombra, parasoles y pérgola",
        "before": r"<h2>Preguntas frecuentes</h2>",
        "html": """
<h2>Sol intenso: sombra, parasol y pérgola</h2>
<p>Cuando el problema principal es el sol directo, el mueble no trabaja solo: también importan la sombra y la estabilidad de la instalación. Para una zona fija, la <a href="/products/pergola-aluminio-para-jardin-300300250-cm">pérgola de aluminio 250x300</a> es la opción más estructural. Para sombra flexible, revisa la colección de <a href="/collections/parasoles">parasoles de jardín y terraza</a> y acompáñalos con una <a href="/products/base-de-parasol-25-kg">base de parasol de 25 kg</a> o un <a href="/products/balliu-pie-de-parasol-c2147052">pie de parasol de 40 kg</a> si necesitas más estabilidad.</p>
""",
    },
    "como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales": {
        "label": "terraza pequeña y medidas con demanda",
        "before": r"<h2>Preguntas frecuentes</h2>",
        "html": """
<h2>Productos compactos que encajan en búsquedas reales</h2>
<p>Para una terraza pequeña con zona de descanso, las búsquedas ya muestran interés por sofás de medida contenida. Puedes comparar el <a href="/products/sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm">sofá de exterior de 120 cm</a> y el <a href="/products/sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm">sofá de exterior de 130 cm</a>. Si quieres asiento y apoyo en una sola pieza, el <a href="/products/banco-jardin-con-mesa-integrada-220-cm">banco de jardín con mesa incorporada</a> resuelve comidas informales sin sumar una mesa independiente.</p>
""",
    },
    "como-elegir-mesa-de-exterior-medidas-comensales-y-espacio-necesario": {
        "label": "banco con mesa y mesas compactas",
        "before": r"<h2>Preguntas frecuentes</h2>",
        "html": """
<h2>Alternativa compacta: banco con mesa incorporada</h2>
<p>Si buscas una solución de comedor exterior que no dependa de mesa y sillas separadas, el <a href="/products/banco-jardin-con-mesa-integrada-220-cm">banco de jardín con mesa incorporada de 220 cm</a> puede ser más fácil de ubicar en porches, patios o zonas de jardín. Es una opción interesante cuando quieres sentarte a comer o tomar algo sin montar un comedor exterior completo.</p>
""",
    },
    "guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada": {
        "label": "fundas, base y parasol",
        "before": r"<h2>Preguntas frecuentes</h2>",
        "html": """
<h2>Accesorios que ayudan al mantenimiento</h2>
<p>El mantenimiento mejora mucho cuando proteges cada pieza en los periodos de poco uso. Para textiles y sofás, revisa la <a href="/products/balliu-funda-protectora-exterior-6f6d4953">funda protectora para sofá exterior</a>; para tumbonas, la <a href="/products/balliu-funda-protectora-exterior-686cc405">funda protectora para tumbona exterior</a>. En sombra, comprueba que el parasol esté bien lastrado con una <a href="/products/base-de-parasol-25-kg">base de parasol</a> adecuada antes de dejarlo montado.</p>
""",
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
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:800]
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


def with_block(body, block):
    wrapped = f"{START}\n{block['html'].strip()}\n{END}"
    existing = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if existing.search(body or ""):
        return existing.sub(wrapped, body)
    before = block["before"]
    match = re.search(before, body or "")
    if match:
        return body[: match.start()] + wrapped + "\n\n" + body[match.start() :]
    return (body or "").rstrip() + "\n\n" + wrapped


def text_words(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacio")

    blog_id = get_blog_id()
    backup = {}
    updates = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - enlaces GSC en {len(BLOCKS)} guias\n")

    for handle, block in BLOCKS.items():
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

        old_body = article.get("body_html") or ""
        new_body = with_block(old_body, block)
        changed = old_body != new_body
        backup[handle] = article
        updates[handle] = (article, new_body)
        print(f"• {handle}")
        print(f"  cluster: {block['label']}")
        print(f"  words: {text_words(old_body)}->{text_words(new_body)}")
        print(f"  changed: {'si' if changed else 'no'}")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(ROOT, "content", "descriptions", f"backup_geo_cluster_links_{ts}.json")
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)
    print(f"\nBackup -> {backup_path}")

    if APPLY:
        print("\nAplicando cambios...")
        for handle, (article, new_body) in updates.items():
            payload = {
                "article": {
                    "id": article["id"],
                    "body_html": new_body,
                }
            }
            try:
                request("PUT", f"blogs/{blog_id}/articles/{article['id']}.json", payload)
                print(f"✓ {handle}")
            except Exception as exc:
                print(f"✗ {handle}: error aplicando ({exc})")
                errors += 1

    print(f"{'Aplicado' if APPLY else 'Dry-run'} · errores: {errors}")
    if not APPLY:
        print("Revisa el dry-run y ejecuta con --apply para publicar.")


if __name__ == "__main__":
    main()
