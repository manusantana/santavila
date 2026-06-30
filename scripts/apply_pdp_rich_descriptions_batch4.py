#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 4 de descripciones ricas para sillones de exterior.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch4.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch4.py --apply
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


def p(text):
    return f"<p>{text}</p>"


def h2(text):
    return f"<h2>{text}</h2>"


def ul(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def armchair_body(style, size, angle, decision):
    return (
        p(
            f"<strong>Sillón de exterior de estilo {style}, con medidas {size}, pensado para completar una zona de descanso en terraza, jardín, porche o patio.</strong> {angle}"
        )
        + p(
            "Un sillón suelto ayuda a modular el espacio mejor que un conjunto cerrado: puedes usarlo como asiento individual, combinarlo con un sofá exterior o crear una pequeña zona de lectura junto a una mesa auxiliar. Antes de comprar, conviene medir ancho, fondo real y paso alrededor, especialmente si va junto a una puerta, barandilla o mesa de centro."
        )
        + h2("Detalles clave")
        + ul(
            [
                "<strong>Formato:</strong> sillón individual de exterior.",
                f"<strong>Medidas:</strong> {size}.",
                f"<strong>Estilo:</strong> {style}.",
                "<strong>Uso recomendado:</strong> terraza, jardín, porche, patio, ático o zona lounge.",
                "<strong>Mantenimiento:</strong> limpiar con suavidad y guardar o cubrir textiles siempre secos.",
            ]
        )
        + p(decision)
    )


PRODUCTS = {
    "sillon-exterior-estilo-urbano-6670-cm": {
        "body": armchair_body(
            "urbano",
            "66×70 cm",
            "Por su huella contenida, encaja bien cuando necesitas asiento cómodo sin cargar visualmente una terraza media o un rincón de porche.",
            "Elige este sillón si buscas una pieza individual compacta y fácil de integrar. Si quieres una sensación de descanso más envolvente, revisa modelos con más fondo o brazos más amplios.",
        ),
        "seo": "Sillón exterior urbano de 66×70 cm para terraza, jardín o porche. Asiento individual compacto y fácil de combinar.",
    },
    "sillon-exterior-estilo-elegante-80104-cm": {
        "body": armchair_body(
            "elegante",
            "80×104 cm",
            "Su fondo generoso lo orienta a zonas lounge donde se prioriza comodidad y presencia sobre una huella muy compacta.",
            "Elige este sillón si tienes espacio suficiente y quieres una butaca exterior protagonista. Para balcones estrechos, comprueba bien el fondo de 104 cm antes de decidir.",
        ),
        "seo": "Sillón exterior elegante de 80×104 cm para zona lounge, jardín amplio, terraza o porche.",
    },
    "sillon-exterior-estilo-moderno-7085-cm": {
        "body": armchair_body(
            "moderno",
            "70×85 cm",
            "Es una medida equilibrada para sumar una plaza extra sin llegar al volumen de los sillones más profundos.",
            "Elige este sillón si quieres un asiento individual versátil para combinar con sofá, mesa baja o reposapiés. Si el espacio es mínimo, revisa modelos de fondo inferior.",
        ),
        "seo": "Sillón exterior moderno de 70×85 cm para terraza, jardín o porche. Butaca individual versátil.",
    },
    "sillon-exterior-estilo-versatil-6470-cm": {
        "body": armchair_body(
            "versátil",
            "64×70 cm",
            "Funciona especialmente bien en terrazas contenidas, patios pequeños o composiciones donde necesitas varios asientos sin saturar el paso.",
            "Elige este sillón si buscas una pieza manejable para espacios ajustados. Si quieres un efecto más lounge, puedes acompañarlo con una mesa auxiliar o reposapiés.",
        ),
        "seo": "Sillón exterior versátil de 64×70 cm para terraza pequeña, patio, jardín o porche.",
    },
    "sillon-exterior-estilo-versatil-76100-cm": {
        "body": armchair_body(
            "versátil",
            "76×100 cm",
            "Su fondo amplio invita a un uso más relajado, adecuado para porches y terrazas donde el asiento individual debe resultar cómodo durante más tiempo.",
            "Elige este sillón si quieres una butaca exterior cómoda y con buena presencia. Si hay poco paso delante, compara antes con opciones de fondo 70-85 cm.",
        ),
        "seo": "Sillón exterior versátil de 76×100 cm para terraza, jardín, porche o zona lounge.",
    },
    "sillon-exterior-estilo-versatil-7783-cm": {
        "body": armchair_body(
            "versátil",
            "77×83 cm",
            "La combinación de ancho y fondo medio permite usarlo tanto como pieza independiente como dentro de una composición con sofá exterior.",
            "Elige este sillón si buscas equilibrio entre comodidad y ocupación. Es una buena medida para completar un salón exterior sin llegar a piezas muy profundas.",
        ),
        "seo": "Sillón exterior versátil de 77×83 cm para salón exterior, terraza, porche o jardín.",
    },
    "sillon-exterior-estilo-envolvente-7582-cm": {
        "body": armchair_body(
            "envolvente",
            "75×82 cm",
            "El enfoque envolvente ayuda a crear una sensación de asiento recogido, útil para zonas de conversación o lectura al aire libre.",
            "Elige este sillón si buscas una butaca exterior cómoda sin un fondo excesivo. Combina bien con mesa baja, sofá de dos plazas o rincón de porche.",
        ),
        "seo": "Sillón exterior envolvente de 75×82 cm para terraza, jardín, porche o zona de lectura.",
    },
    "sillon-exterior-estilo-estilizado-7069-cm": {
        "body": armchair_body(
            "estilizado",
            "70×69 cm",
            "Su proporción compacta y ligera ayuda a sumar asiento sin que la terraza parezca más llena de lo necesario.",
            "Elige este sillón si buscas un asiento individual visualmente ligero. Para descanso prolongado, revisa si prefieres un modelo con más fondo o apoyo.",
        ),
        "seo": "Sillón exterior estilizado de 70×69 cm para terraza, patio, porche o jardín compacto.",
    },
    "sillon-exterior-estilo-contemporaneo-68115-cm": {
        "body": armchair_body(
            "contemporáneo",
            "68×115 cm",
            "Tiene una huella profunda, pensada para quien quiere una postura más descansada en una pieza individual.",
            "Elige este sillón si priorizas comodidad y fondo de asiento. No es la opción más práctica para terrazas estrechas o zonas con mucho tránsito.",
        ),
        "seo": "Sillón exterior contemporáneo de 68×115 cm para terraza amplia, jardín o porche lounge.",
    },
    "sillon-exterior-estilo-versatil-58100-cm": {
        "body": armchair_body(
            "versátil",
            "58×100 cm",
            "Combina ancho contenido con fondo amplio, una solución interesante cuando quieres descanso sin ocupar demasiado lateralmente.",
            "Elige este sillón si necesitas una pieza estrecha pero cómoda. Mide el fondo disponible, porque los 100 cm requieren espacio delante para moverse bien.",
        ),
        "seo": "Sillón exterior versátil de 58×100 cm para terraza estrecha, patio, jardín o porche.",
    },
    "sillon-exterior-estilo-versatil-7685-cm": {
        "body": armchair_body(
            "versátil",
            "76×85 cm",
            "Es una medida cómoda para un asiento individual que debe convivir con mesa de centro, sofá o más sillones.",
            "Elige este sillón si quieres una butaca equilibrada para exterior. Puede funcionar solo o como parte de una zona lounge más completa.",
        ),
        "seo": "Sillón exterior versátil de 76×85 cm para terraza, jardín, patio o porche.",
    },
    "sillon-exterior-estilo-elegante-6590-cm": {
        "body": armchair_body(
            "elegante",
            "65×90 cm",
            "Su ancho moderado y fondo cómodo permiten crear una plaza individual cuidada sin ocupar tanto como una butaca grande.",
            "Elige este sillón si buscas una pieza elegante para completar un rincón de exterior. Si necesitas máxima ligereza visual, compara con modelos de fondo menor.",
        ),
        "seo": "Sillón exterior elegante de 65×90 cm para terraza, porche, patio o jardín.",
    },
    "sillon-exterior-estilo-elegante-6578-cm": {
        "body": armchair_body(
            "elegante",
            "65×78 cm",
            "Es una opción más contenida para sumar asiento en una terraza sin renunciar a una imagen cuidada.",
            "Elige este sillón si necesitas equilibrio entre estilo y tamaño. Encaja bien en composiciones con mesa baja o como pareja de sillones frente a un sofá.",
        ),
        "seo": "Sillón exterior elegante de 65×78 cm para terraza, patio, porche o jardín.",
    },
    "sillon-exterior-bicolor-estilo-bicolor-7376-cm": {
        "body": armchair_body(
            "bicolor",
            "73×76 cm",
            "El acabado bicolor añade presencia visual y ayuda a diferenciar la pieza dentro de una zona lounge o de conversación.",
            "Elige este sillón si quieres un asiento individual con más contraste estético. Si buscas una composición muy neutra, revisa antes el resto de colores de tu terraza.",
        ),
        "seo": "Sillón exterior bicolor de 73×76 cm para terraza, jardín o porche. Butaca individual con contraste visual.",
    },
    "sillon-exterior-estilo-elegante-7275-cm": {
        "body": armchair_body(
            "elegante",
            "72×75 cm",
            "Su formato medio permite usarlo en pareja, junto a una mesa auxiliar o como apoyo a un sofá de exterior.",
            "Elige este sillón si buscas una pieza elegante y fácil de ubicar. Para una zona de descanso más profunda, valora modelos con mayor fondo.",
        ),
        "seo": "Sillón exterior elegante de 72×75 cm para terraza, jardín, porche o patio.",
    },
    "sillon-exterior-aluminio-estilo-envolvente-9890-cm": {
        "body": armchair_body(
            "envolvente",
            "98×90 cm",
            "El formato amplio y el uso de aluminio lo sitúan como una pieza protagonista para salones exteriores con más superficie.",
            "Elige este sillón si quieres una butaca exterior amplia, cómoda y con presencia. Antes de comprar, confirma que el ancho de 98 cm no reduce demasiado el paso.",
        ),
        "seo": "Sillón exterior aluminio envolvente de 98×90 cm para terraza amplia, jardín o porche.",
    },
}


GET = """
query($h:String!) {
  productByHandle(handle: $h) {
    id handle title status productType vendor tags descriptionHtml
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
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN},
    )
    data = None
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


def words(value):
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = re.sub(r"&[a-z]+;", " ", text)
    return len(text.split())


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacio")

    backup = {}
    products = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 4 ({len(PRODUCTS)} fichas)\n")

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
            "status": product["status"],
            "productType": product["productType"],
            "vendor": product["vendor"],
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
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch4_{ts}.json")
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
                    {"input": {"id": product["id"], "descriptionHtml": payload["body"], "seo": {"description": payload["seo"]}}},
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
