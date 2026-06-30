#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 3 de descripciones ricas para sofas, conjuntos y bancos.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch3.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch3.py --apply
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


def sofa_body(plazas, style, size, use_case, decision):
    return (
        p(f"<strong>Sofá de terraza de {plazas} plazas en estilo {style}, con medidas {size}, pensado para crear una zona exterior cómoda y bien proporcionada.</strong> Encaja en {use_case}, sobre todo si buscas una pieza principal que ordene la zona lounge sin obligarte a montar un conjunto completo.")
        + p("Antes de comprar, mide ancho, fondo útil y paso alrededor. En exterior no basta con que el sofá quepa: también debe quedar espacio para sentarse, limpiar, abrir puertas cercanas y combinarlo con mesa auxiliar, sillones o cojines sin saturar la terraza.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Formato:</strong> sofá exterior de {plazas} plazas.",
            f"<strong>Medidas:</strong> {size}.",
            f"<strong>Estilo:</strong> {style}.",
            "<strong>Uso recomendado:</strong> terraza, jardín, porche, patio o ático.",
            "<strong>Mantenimiento:</strong> limpieza suave y textiles siempre secos antes de guardar o cubrir.",
        ])
        + p(decision)
    )


def set_body(plazas, style, decision):
    return (
        p(f"<strong>Set de jardín de estilo {style} con sofá de {plazas} plazas, dos sillones y mesa, diseñado para crear una zona de conversación exterior completa.</strong> Es una opción útil para terraza, porche o jardín cuando quieres una composición coordinada sin escoger cada pieza por separado.")
        + p("El sofá funciona como asiento principal, los sillones dan flexibilidad para recibir visitas y la mesa central permite apoyar bebidas, libros o aperitivos. Antes de comprar, marca la huella del conjunto en el suelo y comprueba que queda paso suficiente para sentarse, levantarse y limpiar sin moverlo todo.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Incluye:</strong> sofá de {plazas} plazas, dos sillones y mesa.",
            f"<strong>Estilo:</strong> {style}.",
            "<strong>Uso recomendado:</strong> terraza media o amplia, jardín, patio o porche.",
            "<strong>Ideal para:</strong> zona lounge, reuniones y descanso al aire libre.",
            "<strong>Consejo:</strong> revisa fondo útil y apertura de puertas antes de colocarlo.",
        ])
        + p(decision)
    )


def bench_body(size, decision):
    return (
        p(f"<strong>Banco de exterior de {size} para añadir asiento funcional en jardín, terraza, porche o patio sin ocupar tanto como un conjunto completo.</strong> Es una pieza sencilla para crear un punto de descanso, acompañar una mesa de exterior o completar una zona de entrada, comedor o sombra.")
        + p("Los bancos funcionan muy bien cuando quieres asiento lineal y una distribución limpia. Antes de comprar, mide el largo disponible, el paso delante del banco y la distancia respecto a mesa, pared o barandilla. Si va a estar a pleno sol o lluvia, conviene revisar limpieza, secado y protección de temporada.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Medida principal:</strong> {size}.",
            "<strong>Formato:</strong> banco de exterior.",
            "<strong>Uso recomendado:</strong> jardín, terraza, porche, patio o zona de comedor exterior.",
            "<strong>Ventaja práctica:</strong> aporta asiento sin complicar la composición.",
            "<strong>Mantenimiento:</strong> limpiar con suavidad y revisar estabilidad al inicio de temporada.",
        ])
        + p(decision)
    )


PRODUCTS = {
    "sofa-terraza-2-plazas-estilo-estilizado-14383-cm": {
        "body": sofa_body("2", "estilizado", "143×83 cm", "terrazas medianas y porches donde se busca un sofá de dos plazas con más presencia que los modelos compactos", "Elige este sofá si quieres una pieza de dos plazas cómoda y visualmente ligera. Si el paso es estrecho, comprueba bien el fondo de 83 cm antes de decidir."),
        "seo": "Sofá terraza 2 plazas estilizado de 143×83 cm para exterior. Sofá cómodo para terraza, jardín o porche.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-15082-cm": {
        "body": sofa_body("2", "contemporáneo", "150×82 cm", "terrazas y patios donde un sofá de dos plazas debe ser protagonista sin llegar a formato de tres plazas", "Elige este sofá si buscas un dos plazas amplio para estar cómodo. Para balcones estrechos, puede ser mejor una medida menor o piezas más ligeras."),
        "seo": "Sofá terraza 2 plazas contemporáneo de 150×82 cm para jardín, patio, porche o terraza.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-145100-cm": {
        "body": sofa_body("2", "contemporáneo", "145×100 cm", "zonas lounge donde se prioriza fondo y comodidad frente a una huella muy compacta", "Elige este sofá si quieres sentarte con más sensación de descanso. No es la mejor opción si necesitas dejar mucho paso delante o tienes una terraza estrecha."),
        "seo": "Sofá exterior 2 plazas contemporáneo de 145×100 cm para zona lounge, terraza o porche.",
    },
    "sofa-terraza-3-plazas-estilo-sofisticado-212100-cm": {
        "body": sofa_body("3", "sofisticado", "212×100 cm", "terrazas amplias, jardines y porches donde el sofá será la pieza principal del salón exterior", "Elige este sofá si tienes espacio generoso y quieres tres plazas reales con presencia. Para espacios compactos, conviene bajar a dos plazas o elegir menor fondo."),
        "seo": "Sofá terraza 3 plazas sofisticado de 212×100 cm para jardín, porche o terraza amplia.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-164104-cm": {
        "body": sofa_body("2", "contemporáneo", "164×104 cm", "terrazas amplias o porches donde se quiere un sofá de dos plazas ancho y profundo", "Elige este sofá si buscas comodidad y una huella generosa para dos personas. Si la terraza es estrecha, compara antes con sofás de fondo 70-85 cm."),
        "seo": "Sofá exterior 2 plazas contemporáneo de 164×104 cm para terraza amplia, jardín o porche.",
    },
    "set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-2": {
        "body": set_body("3", "contemporáneo", "Elige este set si quieres resolver una zona lounge completa para varias personas. Necesita más superficie que un sofá suelto, pero da una composición coherente desde el primer día."),
        "seo": "Set jardín contemporáneo con sofá 3 plazas, dos sillones y mesa para terraza amplia o jardín.",
    },
    "set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-3": {
        "body": set_body("3", "contemporáneo", "Elige este conjunto si buscas un salón exterior amplio con estética actual. Si el espacio es justo, mide bien la distancia entre sofá, sillones y mesa."),
        "seo": "Conjunto jardín contemporáneo con sofá 3 plazas, dos sillones y mesa para exterior.",
    },
    "set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-3": {
        "body": set_body("3", "sofisticado", "Elige este set si quieres una zona exterior protagonista, cómoda y con imagen cuidada. En terrazas pequeñas puede resultar demasiado voluminoso."),
        "seo": "Set jardín sofisticado con sofá 3 plazas, dos sillones y mesa para terraza, porche o jardín.",
    },
    "set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-5": {
        "body": set_body("2", "elegante", "Elige este set si quieres una composición equilibrada para cuatro personas sentadas de forma flexible. Para balcones estrechos, revisa el espacio que ocupan los sillones frente al sofá."),
        "seo": "Set jardín elegante con sofá 2 plazas, dos sillones y mesa para terraza, patio o porche.",
    },
    "set-jardin-3-plazas-elegante-sofa-3-plazas-2-sillones-mesa-2": {
        "body": set_body("3", "elegante", "Elige este conjunto si necesitas más capacidad de asiento y una imagen sobria para terraza o jardín. Si quieres una composición más ligera, valora un sofá de 2 plazas."),
        "seo": "Set jardín elegante con sofá 3 plazas, dos sillones y mesa para salón exterior amplio.",
    },
    "banco-de-exterior-150-cm": {
        "body": bench_body("150 cm", "Elige este banco si necesitas una pieza versátil para dos o tres personas, según uso y espacio. Puede funcionar junto a una mesa o como asiento independiente en una zona de paso o sombra."),
        "seo": "Banco de exterior 150 cm para jardín, terraza o porche. Asiento funcional para comedor exterior o zona de descanso.",
    },
    "banco-de-exterior-108-cm": {
        "body": bench_body("108 cm", "Elige este banco si buscas una solución más compacta para terraza pequeña, patio o rincón de jardín. Es útil cuando una pieza de 150 cm ocuparía demasiado."),
        "seo": "Banco de exterior 108 cm compacto para jardín, terraza, patio o porche. Asiento exterior funcional.",
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
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 3 ({len(PRODUCTS)} fichas)\n")

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
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch3_{ts}.json")
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
