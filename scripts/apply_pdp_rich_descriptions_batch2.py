#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 2 de descripciones ricas para sofas y conjuntos sofa.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch2.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch2.py --apply
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


def html(*parts):
    return "".join(parts)


def p(text):
    return f"<p>{text}</p>"


def h2(text):
    return f"<h2>{text}</h2>"


def ul(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def sofa_body(plazas, style, size, use_case, decision):
    return html(
        p(f"<strong>Sofá de terraza de {plazas} plazas en estilo {style}, con medidas {size}, pensado para crear una zona de descanso exterior cómoda sin complicar la distribución.</strong> Encaja en {use_case}, especialmente cuando se quiere una pieza principal clara y fácil de combinar con mesa auxiliar, sillones o cojines de exterior."),
        p("Antes de comprar, conviene medir el ancho real disponible, el fondo de paso y la apertura de puertas cercanas. En una terraza, el tamaño del sofá no se valora solo por el ancho: también importa dejar espacio para sentarse, limpiar y moverse alrededor sin desplazar todos los muebles."),
        h2("Detalles clave"),
        ul([
            f"<strong>Formato:</strong> sofá exterior de {plazas} plazas.",
            f"<strong>Medidas:</strong> {size}.",
            f"<strong>Estilo:</strong> {style}.",
            "<strong>Uso recomendado:</strong> terraza, jardín, porche, patio o ático.",
            "<strong>Mantenimiento:</strong> limpiar la estructura con suavidad y guardar textiles secos cuando no se usen.",
        ]),
        p(decision),
    )


def set_body(plazas, style, title_size, decision):
    return html(
        p(f"<strong>Set de jardín de estilo {style} con sofá de {plazas} plazas, dos sillones y mesa, pensado para montar una zona de conversación exterior completa.</strong> Es una solución práctica para terraza, jardín o porche cuando quieres comprar la composición ya coordinada, sin tener que elegir cada pieza por separado."),
        p("El conjunto funciona bien como salón exterior: el sofá actúa como asiento principal, los sillones permiten recibir visitas y la mesa de centro aporta superficie para bebidas, libros o aperitivos. Antes de decidir, mide la huella total del set y deja paso alrededor para sentarse, levantarse y limpiar con comodidad."),
        h2("Detalles clave"),
        ul([
            f"<strong>Incluye:</strong> sofá de {plazas} plazas, dos sillones y mesa.",
            f"<strong>Estilo:</strong> {style}.",
            f"<strong>Referencia de familia:</strong> {title_size}.",
            "<strong>Uso recomendado:</strong> terraza media o amplia, jardín, porche o patio.",
            "<strong>Consejo:</strong> comprueba fondo útil y paso libre antes de colocarlo junto a pared o barandilla.",
        ]),
        p(decision),
    )


PRODUCTS = {
    "sofa-terraza-2-plazas-estilo-contemporaneo-13370-cm": {
        "body": sofa_body(
            "2",
            "contemporáneo",
            "133×70 cm",
            "terrazas compactas, patios estrechos o porches donde un sofá de dos plazas debe ocupar poco fondo",
            "Elige este sofá si buscas una pieza de 2 plazas algo más amplia que los modelos de 120-130 cm, pero todavía fácil de ubicar. Si quieres tumbarte o recibir a más personas, puede interesarte subir a un sofá de 3 plazas.",
        ),
        "seo": "Sofá terraza 2 plazas contemporáneo de 133×70 cm. Sofá exterior compacto para terraza, porche, patio o ático.",
    },
    "sofa-terraza-3-plazas-estilo-moderno-18770-cm": {
        "body": sofa_body(
            "3",
            "moderno",
            "187×70 cm",
            "terrazas medianas, jardines y zonas lounge que necesitan más asiento sin demasiado fondo",
            "Elige este sofá si quieres pasar de una zona para dos personas a un asiento principal más generoso. La medida de 187 cm permite crear un salón exterior sin llegar a formatos muy profundos.",
        ),
        "seo": "Sofá terraza 3 plazas moderno de 187×70 cm para jardín, porche o zona lounge exterior.",
    },
    "sofa-terraza-3-plazas-estilo-contemporaneo-18583-cm": {
        "body": sofa_body(
            "3",
            "contemporáneo",
            "185×83 cm",
            "terrazas medianas, porches y jardines donde se busca un sofá principal cómodo y visualmente ligero",
            "Elige este sofá si necesitas tres plazas y puedes reservar algo más de fondo para sentarte con comodidad. Si el espacio es estrecho, compara antes con modelos de fondo 70 cm.",
        ),
        "seo": "Sofá exterior 3 plazas contemporáneo de 185×83 cm para terraza, jardín o porche.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-16269-cm": {
        "body": sofa_body(
            "2",
            "contemporáneo",
            "162×69 cm",
            "terrazas alargadas, balcones amplios y zonas de estar donde interesa un sofá ancho pero poco profundo",
            "Elige este sofá si quieres más anchura que un dos plazas compacto sin ganar demasiado fondo. Es buena opción cuando el paso delante del sofá es limitado pero necesitas una presencia visual mayor.",
        ),
        "seo": "Sofá terraza 2 plazas contemporáneo de 162×69 cm. Sofá exterior ancho y poco profundo para terraza o porche.",
    },
    "sofa-terraza-3-plazas-estilo-contemporaneo-215104-cm": {
        "body": sofa_body(
            "3",
            "contemporáneo",
            "215×104 cm",
            "terrazas amplias, porches grandes y salones exteriores donde el sofá será la pieza protagonista",
            "Elige este sofá si tienes espacio suficiente y buscas una zona lounge amplia. Por sus 215 cm de ancho y 104 cm de fondo, no es la opción más adecuada para balcones o pasos estrechos.",
        ),
        "seo": "Sofá exterior 3 plazas contemporáneo de 215×104 cm para terraza amplia, jardín o porche grande.",
    },
    "sofa-terraza-2-plazas-estilo-elegante-13170-cm": {
        "body": sofa_body(
            "2",
            "elegante",
            "131×70 cm",
            "terrazas compactas, patios y porches donde se quiere una pieza sobria y fácil de combinar",
            "Elige este sofá si buscas una medida equilibrada para dos personas y una estética más calmada. Si necesitas una zona de reunión completa, combínalo con dos sillones o valora un conjunto de jardín.",
        ),
        "seo": "Sofá exterior 2 plazas elegante de 131×70 cm para terraza, jardín, patio o porche.",
    },
    "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa": {
        "body": set_body(
            "2",
            "moderno",
            "set con sofá 2 plazas",
            "Elige este set si quieres una zona exterior completa para conversar y descansar sin construir la composición pieza a pieza. Si tu terraza es pequeña, mide especialmente el espacio que ocupan los sillones frente al sofá.",
        ),
        "seo": "Set jardín moderno con sofá 2 plazas, dos sillones y mesa. Conjunto exterior para terraza, jardín o porche.",
    },
    "set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa": {
        "body": set_body(
            "3",
            "contemporáneo",
            "set con sofá 3 plazas",
            "Elige este set si buscas un salón exterior amplio para reuniones, comidas informales o descanso. Necesita más superficie que un sofá suelto, pero resuelve la zona completa de una vez.",
        ),
        "seo": "Set jardín contemporáneo con sofá 3 plazas, dos sillones y mesa para terraza amplia, jardín o porche.",
    },
    "set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-4": {
        "body": set_body(
            "3",
            "sofisticado",
            "set con sofá 3 plazas",
            "Elige este conjunto si la zona exterior será un salón protagonista y quieres una composición amplia con estética cuidada. En espacios estrechos puede funcionar mejor un sofá de 2 plazas con piezas auxiliares.",
        ),
        "seo": "Set jardín sofisticado con sofá 3 plazas, dos sillones y mesa. Salón exterior para terraza, jardín o porche amplio.",
    },
    "set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-3": {
        "body": set_body(
            "2",
            "elegante",
            "set con sofá 2 plazas",
            "Elige este set si quieres una zona de estar exterior equilibrada, con asiento principal, dos plazas individuales y mesa de apoyo. Para balcones estrechos, revisa antes medidas y paso libre.",
        ),
        "seo": "Set jardín elegante con sofá 2 plazas, dos sillones y mesa. Conjunto exterior para terraza, patio o porche.",
    },
}


GET = """
query($h:String!) {
  productByHandle(handle: $h) {
    id
    handle
    title
    status
    productType
    vendor
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
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 2 ({len(PRODUCTS)} fichas)\n")

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
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch2_{ts}.json")
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
