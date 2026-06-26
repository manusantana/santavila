#!/usr/bin/env python3
"""
Sprint GEO 1.3: reescritura anti-duplicado para PDPs de alto valor.

Objetivo:
- Reducir similitud con textos de proveedor Hevea.
- Mejorar intención de búsqueda en rinconeras y sets bicolor.
- Mantener textos anclados a datos visibles: título, SKU, tipo, opciones y precio.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_desduplicated_descriptions.py

Para aplicar:
  .venv/bin/python scripts/apply_desduplicated_descriptions.py --apply
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
    "set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro": {
        "body": body(
            "Rinconera de terraza con sofá de esquina y mesa de centro para montar un salón exterior completo sin comprar piezas sueltas.",
            [
                "<strong>Incluye:</strong> sofá rinconero de exterior y mesa de centro.",
                "<strong>Formato:</strong> set de esquina, pensado para aprovechar mejor una terraza o jardín amplio.",
                "<strong>Uso recomendado:</strong> zona lounge, porche, patio o comedor exterior informal.",
                "<strong>Por qué elegirla:</strong> resuelve asiento y apoyo en una sola composición, con estética contemporánea.",
            ],
            "Si buscas una rinconera de jardín o un sofá de esquina exterior, esta opción encaja cuando quieres crear una zona de reunión cómoda, visualmente ordenada y lista para uso diario al aire libre.",
        ),
        "seo": "Rinconera de terraza con sofá de esquina y mesa de centro. Set exterior para jardín, porche o patio amplio.",
    },
    "set-rinconera-exterior-hpl-moderno-sofa-de-esquina-mesa-de-centro": {
        "body": body(
            "Set rinconera exterior HPL de estilo moderno, con sofá de esquina y mesa de centro para terrazas grandes que necesitan una pieza protagonista.",
            [
                "<strong>Incluye:</strong> sofá de esquina y mesa de centro con tablero HPL.",
                "<strong>Material destacado:</strong> HPL en la mesa, adecuado para exterior por su resistencia al uso diario.",
                "<strong>Uso recomendado:</strong> jardín, terraza amplia, ático o zona chill out.",
                "<strong>Ventaja práctica:</strong> el formato en L concentra muchas plazas sin ocupar el centro del espacio.",
            ],
            "Es una rinconera de jardín pensada para quien compara sets de exterior por distribución, material de mesa y capacidad real de reunión, no solo por imagen.",
        ),
        "seo": "Set rinconera exterior HPL moderno con sofá de esquina y mesa de centro. Para jardín, terraza amplia o ático.",
    },
    "set-rinconera-exterior-hpl-elegante-sofa-de-esquina-mesa-de-centro": {
        "body": body(
            "Rinconera exterior HPL de línea elegante, diseñada para crear una zona de estar amplia con sofá de esquina y mesa de centro.",
            [
                "<strong>Incluye:</strong> sofá rinconero y mesa de centro con tablero HPL.",
                "<strong>Formato:</strong> composición de esquina para ordenar el espacio y liberar paso.",
                "<strong>Uso recomendado:</strong> terraza, jardín, porche o casa con zona exterior de uso frecuente.",
                "<strong>Decisión de compra:</strong> adecuada si buscas amplitud, apoyo central y un acabado más cuidado.",
            ],
            "La ficha responde a búsquedas como rinconera terraza o set rinconera exterior, donde el cliente necesita entender de un vistazo qué incluye y para qué espacio tiene sentido.",
        ),
        "seo": "Rinconera exterior HPL elegante con sofá de esquina y mesa de centro. Set para terraza, jardín o porche.",
    },
    "set-rinconera-exterior-hpl-sofisticado-sofa-de-esquina-mesa-de-centro": {
        "body": body(
            "Conjunto rinconera exterior HPL en blanco y beige, con sofá de esquina y mesa de centro para crear un ambiente luminoso en terraza o jardín.",
            [
                "<strong>Incluye:</strong> sofá de esquina y mesa de centro HPL.",
                "<strong>Acabado visible:</strong> combinación blanco-beige, fácil de integrar en exteriores actuales.",
                "<strong>Uso recomendado:</strong> terraza grande, porche cubierto, jardín o zona lounge.",
                "<strong>Ventaja práctica:</strong> formato rinconero para ganar asientos y mantener una circulación cómoda.",
            ],
            "Es una alternativa para quien busca un sofá de esquina exterior con presencia decorativa, pero también una composición funcional para recibir visitas al aire libre.",
        ),
        "seo": "Conjunto rinconera exterior HPL blanco-beige con sofá de esquina y mesa. Para terraza grande, jardín o porche.",
    },
    "set-jardin-bicolor-3-plazas-bicolor-sofa-3-plazas-2-sillones-mesa": {
        "body": body(
            "Set de jardín bicolor con sofá de 3 plazas, dos sillones y mesa: una composición completa para terrazas donde se quiere más capacidad sin perder orden visual.",
            [
                "<strong>Incluye:</strong> sofá exterior de 3 plazas, 2 sillones y mesa de centro.",
                "<strong>Estilo:</strong> acabado bicolor, pensado para dar contraste sin recargar el espacio.",
                "<strong>Uso recomendado:</strong> jardín, terraza amplia, porche o zona de reunión familiar.",
                "<strong>Ideal para:</strong> quienes buscan un sofá bicolor de exterior con conjunto coordinado.",
            ],
            "Frente a comprar cada pieza por separado, este set jardín bicolor facilita montar una zona lounge coherente, con asientos suficientes para reuniones y una mesa central de apoyo.",
        ),
        "seo": "Set jardín bicolor con sofá 3 plazas, 2 sillones y mesa. Sofá exterior bicolor para terraza, porche o jardín.",
    },
    "set-jardin-bicolor-2-plazas-bicolor-sofa-2-plazas-2-sillones-mesa": {
        "body": body(
            "Conjunto de jardín bicolor con sofá de 2 plazas, dos sillones y mesa, pensado para terrazas medianas que necesitan un salón exterior completo.",
            [
                "<strong>Incluye:</strong> sofá exterior de 2 plazas, 2 sillones y mesa de centro.",
                "<strong>Formato:</strong> set compacto con cuatro asientos principales y apoyo central.",
                "<strong>Estilo:</strong> diseño bicolor para aportar contraste en espacios exteriores modernos.",
                "<strong>Uso recomendado:</strong> terraza, jardín, patio, ático o porche.",
            ],
            "Encaja si buscas un sofá bicolor exterior pero prefieres una solución ya coordinada, con sillones y mesa incluidos para recibir visitas sin improvisar mobiliario.",
        ),
        "seo": "Conjunto jardín bicolor con sofá 2 plazas, 2 sillones y mesa. Set exterior compacto para terraza o jardín.",
    },
}


GET = """
query($h:String!) {
  productByHandle(handle: $h) {
    id
    handle
    title
    productType
    vendor
    tags
    descriptionHtml
    seo { title description }
    options { name values }
    variants(first: 5) {
      nodes { sku title }
    }
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
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        },
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                data = json.load(response)
            break
        except Exception:
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
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - {len(PRODUCTS)} PDPs anti-duplicado\n")

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

        backup[handle] = {
            "id": product["id"],
            "title": product["title"],
            "productType": product["productType"],
            "vendor": product["vendor"],
            "tags": product["tags"],
            "options": product["options"],
            "variants": product["variants"]["nodes"],
            "priceRangeV2": product["priceRangeV2"],
            "descriptionHtml": product["descriptionHtml"],
            "seo": product.get("seo"),
        }

        print(f"• {handle}")
        print(f"  title: {product['title']}")
        print(f"  vendor/type: {product['vendor']} / {product['productType']}")
        print(f"  words: {words(product['descriptionHtml'])}->{words(payload['body'])}")
        print(f"  meta: {payload['seo']}")

        if APPLY:
            res = gql(
                SET,
                {
                    "input": {
                        "id": product["id"],
                        "descriptionHtml": payload["body"],
                        "seo": {"description": payload["seo"]},
                    }
                },
            )["productUpdate"]
            if res["userErrors"]:
                print(f"  ⚠️ {res['userErrors']}")
                errors += 1

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(ROOT, "content", "descriptions", f"backup_desduplicated_{ts}.json")
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)

    print(f"\nBackup -> {backup_path}")
    print(f"{'Aplicado' if APPLY else 'Dry-run'} · errores: {errors}")


if __name__ == "__main__":
    main()
