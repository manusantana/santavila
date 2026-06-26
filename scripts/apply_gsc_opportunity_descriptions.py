#!/usr/bin/env python3
"""
Aplica el lote GEO Sprint 1 sobre productos con oportunidad real en GSC.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_gsc_opportunity_descriptions.py

Para aplicar:
  .venv/bin/python scripts/apply_gsc_opportunity_descriptions.py --apply
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv


def ul(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def body(opening, bullets, closing):
    return f"<p><strong>{opening}</strong></p>" + ul(bullets) + f"<p>{closing}</p>"


PRODUCTS = {
    "pergola-aluminio-para-jardin-300300250-cm": {
        "body": body(
            "Pérgola de aluminio para jardín y terraza, indicada para quien busca una pérgola 250x300 o una solución cercana a 300 x 250 cm con estructura resistente y estética limpia.",
            [
                "<strong>Uso recomendado:</strong> zonas de sombra en jardín, terraza o patio.",
                "<strong>Material:</strong> estructura de aluminio para exterior.",
                "<strong>Medidas visibles en la ficha:</strong> 300/300/250 cm.",
                "<strong>Ventaja práctica:</strong> crea una zona protegida para comedor, sofá o rincón de descanso.",
            ],
            "Es una opción útil para búsquedas por medida como “pérgola 250x300” o “pérgola 300 x 250”, donde el cliente ya compara encaje, material y uso exterior antes de decidir.",
        ),
        "seo": "Pérgola de aluminio para jardín y terraza, medida 300/300/250 cm. Ideal para búsquedas de pérgola 250x300 o 300 x 250 con estructura exterior.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm": {
        "body": body(
            "Sofá de terraza de 2 plazas y 120 cm, pensado para balcones amplios, terrazas compactas y zonas de estar exteriores donde cada centímetro cuenta.",
            [
                "<strong>Formato:</strong> sofá exterior de 2 plazas.",
                "<strong>Medida clave:</strong> 120 cm de ancho, una búsqueda habitual para terrazas pequeñas.",
                "<strong>Estilo:</strong> contemporáneo, fácil de integrar con mesas auxiliares y sillones.",
                "<strong>Uso recomendado:</strong> terraza, jardín, porche o ático.",
            ],
            "Si buscas un sofá terraza 120 cm, esta ficha concentra la medida, el formato y el uso exterior en una pieza compacta para crear una zona cómoda sin saturar el espacio.",
        ),
        "seo": "Sofá de terraza 2 plazas de 120 cm para exterior. Diseño contemporáneo para terraza, jardín, porche o ático con formato compacto.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm": {
        "body": body(
            "Sofá de exterior de 2 plazas y 130 cm, una medida equilibrada para terrazas donde se necesita más presencia que un sofá compacto sin pasar a formatos grandes.",
            [
                "<strong>Formato:</strong> sofá exterior de 2 plazas.",
                "<strong>Medida clave:</strong> 130 cm de ancho.",
                "<strong>Estilo:</strong> contemporáneo, para salones exteriores actuales.",
                "<strong>Uso recomendado:</strong> terraza, jardín, porche o zona chill out.",
            ],
            "Para búsquedas como “sofá exterior 130 cm”, esta opción permite comparar rápidamente tamaño, uso y estilo antes de elegir el conjunto de terraza.",
        ),
        "seo": "Sofá exterior de 2 plazas y 130 cm, estilo contemporáneo. Para terraza, jardín, porche o zona chill out al aire libre.",
    },
    "banco-jardin-con-mesa-integrada-220-cm": {
        "body": body(
            "Banco de jardín con mesa integrada de 220 cm, una solución práctica para comer, conversar o descansar al aire libre sin montar muebles separados.",
            [
                "<strong>Formato:</strong> banco con mesa incorporada.",
                "<strong>Medida clave:</strong> 220 cm.",
                "<strong>Uso recomendado:</strong> jardín, terraza amplia, porche o casa rural.",
                "<strong>Ventaja práctica:</strong> asiento y superficie de apoyo en una sola pieza.",
            ],
            "Encaja muy bien con búsquedas de intención clara como “banco con mesa incorporada” o “banco con mesa”, donde el usuario quiere una pieza funcional y estable para exterior.",
        ),
        "seo": "Banco de jardín con mesa integrada de 220 cm. Banco con mesa incorporada para jardín, terraza, porche o casa rural.",
    },
    "balliu-tumbona-de-exterior-resina-28ff014d": {
        "body": body(
            "Tumbona de exterior de resina Balliu para jardín, piscina y zonas de descanso con uso intensivo.",
            [
                "<strong>Material:</strong> resina para exterior.",
                "<strong>Uso recomendado:</strong> piscina, jardín, terraza y espacios profesionales.",
                "<strong>Búsquedas relacionadas:</strong> tumbona Balliu, tumbona de resina y tumbona jardín resina.",
                "<strong>Ventaja práctica:</strong> mantenimiento sencillo y buena adaptación a espacios al aire libre.",
            ],
            "Dentro del cluster de tumbonas Balliu, esta ficha ayuda a responder consultas comparativas donde importan material, resistencia exterior y facilidad de limpieza.",
        ),
        "seo": "Tumbona Balliu de exterior en resina para jardín, piscina y terraza. Mantenimiento sencillo y uso intensivo al aire libre.",
    },
    "balliu-tumbona-de-exterior-resina-75-cm-009e68e4": {
        "body": body(
            "Tumbona de exterior Balliu en resina de 75 cm, pensada para zonas de piscina, jardín y terrazas donde se busca una pieza resistente y fácil de mantener.",
            [
                "<strong>Material:</strong> resina para exterior.",
                "<strong>Medida clave:</strong> 75 cm.",
                "<strong>Uso recomendado:</strong> piscina, jardín, terraza y alojamiento turístico.",
                "<strong>Búsquedas relacionadas:</strong> tumbona Balliu, tumbona resina exterior y tumbona jardín resina.",
            ],
            "La medida de 75 cm facilita comparar comodidad y encaje en espacios de descanso, especialmente cuando se buscan tumbonas de resina para exterior.",
        ),
        "seo": "Tumbona Balliu de exterior en resina de 75 cm para jardín, piscina y terraza. Resistente, cómoda y fácil de mantener.",
    },
    "balliu-tumbona-de-exterior-aluminio-d08586c1": {
        "body": body(
            "Tumbona de exterior Balliu con estructura de aluminio, orientada a jardín, piscina y espacios donde se prioriza ligereza y resistencia a la intemperie.",
            [
                "<strong>Material:</strong> aluminio para exterior.",
                "<strong>Uso recomendado:</strong> terraza, jardín, piscina y hostelería.",
                "<strong>Búsquedas relacionadas:</strong> tumbona Balliu, tumbona aluminio exterior y tumbona profesional.",
                "<strong>Ventaja práctica:</strong> estructura ligera para moverla con facilidad.",
            ],
            "Es la alternativa natural dentro del cluster Balliu cuando el usuario compara resina frente a aluminio para equipar una zona de solárium o descanso exterior.",
        ),
        "seo": "Tumbona Balliu de exterior en aluminio para jardín, piscina, terraza y hostelería. Ligera, resistente y fácil de mover.",
    },
    "base-de-parasol-25-kg": {
        "body": body(
            "Base de parasol de 25 kg para estabilizar sombrillas y parasoles de exterior en terraza, jardín o patio.",
            [
                "<strong>Peso:</strong> 25 kg.",
                "<strong>Función:</strong> base para parasol o base para sombrilla de exterior.",
                "<strong>Uso recomendado:</strong> terraza, jardín y balcón amplio.",
                "<strong>Ventaja práctica:</strong> aporta sujeción al mástil y ayuda a evitar movimientos con viento ligero.",
            ],
            "La ficha responde a búsquedas como “base parasol”, “base para sombrilla” y “base de parasol 25 kg”, con el peso y el uso principal visibles desde el primer bloque.",
        ),
        "seo": "Base de parasol de 25 kg para sombrilla exterior. Sujeción estable para terraza, jardín o patio. Base para parasol compacta.",
    },
}


GET = """
query($h:String!) {
  productByHandle(handle: $h) {
    id
    handle
    title
    productType
    tags
    descriptionHtml
    seo { title description }
    options { name values }
    priceRangeV2 {
      minVariantPrice { amount currencyCode }
      maxVariantPrice { amount currencyCode }
    }
  }
}
"""

SET = """
mutation($input:ProductInput!) {
  productUpdate(input:$input) {
    product { id handle title }
    userErrors { field message }
  }
}
"""


def gql(query, variables, attempts=3):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        },
    )
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                data = json.load(response)
            break
        except Exception as exc:
            last_error = exc
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacío")

    backup = {}
    products = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - {len(PRODUCTS)} fichas GSC\n")

    for handle, payload in PRODUCTS.items():
        try:
            product = gql(GET, {"h": handle})["productByHandle"]
        except Exception as exc:
            print(f"✗ {handle}: error leyendo ({exc})")
            errors += 1
            continue

        if not product:
            print(f"✗ {handle}: no encontrado")
            errors += 1
            continue

        products[handle] = product
        backup[handle] = {
            "id": product["id"],
            "title": product["title"],
            "productType": product["productType"],
            "tags": product["tags"],
            "options": product["options"],
            "priceRangeV2": product["priceRangeV2"],
            "descriptionHtml": product["descriptionHtml"],
            "seo": product.get("seo"),
        }

        print(f"• {handle}")
        print(f"  title: {product['title']}")
        print(f"  words: {words(product['descriptionHtml'])}->{words(payload['body'])}")
        print(f"  meta: {payload['seo']}")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = os.path.join(ROOT, "content", "descriptions")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"backup_gsc_opportunities_{ts}.json")
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)

    print(f"\nBackup de lo actual -> {backup_path}")

    if APPLY:
        print("\nAplicando cambios...")
        for handle, product in products.items():
            payload = PRODUCTS[handle]
            try:
                result = gql(
                    SET,
                    {
                        "input": {
                            "id": product["id"],
                            "descriptionHtml": payload["body"],
                            "seo": {"description": payload["seo"]},
                        }
                    },
                )["productUpdate"]
            except Exception as exc:
                print(f"✗ {handle}: error aplicando ({exc})")
                errors += 1
                continue
            if result["userErrors"]:
                print(f"⚠ {handle}: userErrors: {result['userErrors']}")
                errors += 1
            else:
                print(f"✓ {handle}")

    print(f"{'Aplicado' if APPLY else 'Dry-run completado'} · errores: {errors}")
    if not APPLY:
        print("Revisa el dry-run y ejecuta con --apply para publicar.")


if __name__ == "__main__":
    main()
