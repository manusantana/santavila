#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 5 de descripciones ricas para mesas de centro,
tumbonas y reposapies.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch5.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch5.py --apply
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


def table_body(size, height, material, angle, decision):
    material_line = f" con tablero {material}" if material else ""
    return (
        p(
            f"<strong>Mesa de centro exterior de {size} y altura {height}{material_line}, pensada para completar una zona lounge en terraza, jardín o porche.</strong> {angle}"
        )
        + p(
            "En una zona exterior, la mesa de centro no solo sirve de apoyo: también ordena la distancia entre sofá, sillones y paso. Antes de comprar, mide el hueco libre alrededor y deja espacio suficiente para sentarse, levantarse y limpiar sin mover toda la composición."
        )
        + h2("Detalles clave")
        + ul(
            [
                "<strong>Formato:</strong> mesa de centro para exterior.",
                f"<strong>Medida principal:</strong> {size}.",
                f"<strong>Altura:</strong> {height}.",
                f"<strong>Material destacado:</strong> {material or 'acabado exterior'}." ,
                "<strong>Uso recomendado:</strong> zona lounge, terraza, porche, jardín o patio.",
            ]
        )
        + p(decision)
    )


def footrest_body(size, style, angle, decision):
    return (
        p(
            f"<strong>Reposapiés exterior de {size}, pensado para ampliar la comodidad de un sillón o sofá de terraza sin añadir una pieza demasiado compleja.</strong> {angle}"
        )
        + p(
            "Un reposapiés permite convertir un asiento individual en una zona de descanso más relajada, y también puede funcionar como apoyo auxiliar cuando no se está usando. Antes de comprar, comprueba que queda paso suficiente delante del asiento y que la altura encaja con la postura que buscas."
        )
        + h2("Detalles clave")
        + ul(
            [
                "<strong>Formato:</strong> reposapiés para exterior.",
                f"<strong>Medidas:</strong> {size}.",
                f"<strong>Estilo:</strong> {style}.",
                "<strong>Uso recomendado:</strong> terraza, jardín, porche, patio o zona lounge.",
                "<strong>Mantenimiento:</strong> limpieza suave y textiles siempre secos antes de cubrir o guardar.",
            ]
        )
        + p(decision)
    )


def lounger_body(kind, material, angle, decision):
    return (
        p(
            f"<strong>Tumbona de exterior {kind}, pensada para crear una zona de descanso junto a piscina, jardín, terraza o solárium.</strong> {angle}"
        )
        + p(
            "Antes de elegir una tumbona, conviene revisar el uso real: tomar el sol, leer, descansar tras el baño o equipar una zona de piscina con varias unidades. También importa medir el largo disponible y dejar paso lateral para moverse, limpiar y colocar una mesa auxiliar si hace falta."
        )
        + h2("Detalles clave")
        + ul(
            [
                "<strong>Formato:</strong> tumbona individual de exterior.",
                f"<strong>Material o familia:</strong> {material}.",
                "<strong>Uso recomendado:</strong> piscina, jardín, terraza, solárium o alojamiento turístico.",
                "<strong>Consejo de compra:</strong> revisa peso, movilidad y apilabilidad si vas a mover varias unidades.",
                "<strong>Mantenimiento:</strong> limpiar con productos suaves y dejar secar antes de guardar o cubrir.",
            ]
        )
        + p(decision)
    )


PRODUCTS = {
    "mesa-de-centro-exterior-hpl-70-cm-altura-45-cm": {
        "body": table_body("70 cm", "45 cm", "HPL", "Su formato compacto encaja bien cuando necesitas una mesa auxiliar baja sin saturar el paso entre asientos.", "Elige esta mesa si quieres una pieza pequeña y práctica para apoyar bebidas, libros o decoración. Para salones exteriores grandes puede quedarse corta como centro principal."),
        "seo": "Mesa de centro exterior HPL de 70 cm y altura 45 cm para terraza, jardín o porche.",
    },
    "mesa-de-centro-exterior-125-cm-altura-42-cm": {
        "body": table_body("125 cm", "42 cm", "", "El largo de 125 cm funciona bien frente a sofás amplios o composiciones con varios asientos.", "Elige esta mesa si necesitas una superficie generosa para una zona lounge. Si el espacio es estrecho, mide bien el paso a ambos lados."),
        "seo": "Mesa de centro exterior de 125 cm y altura 42 cm para sofá de terraza, jardín o porche.",
    },
    "mesa-de-centro-exterior-hpl-90-cm-altura-40-cm": {
        "body": table_body("90 cm", "40 cm", "HPL", "Es una medida equilibrada para zonas de estar de tamaño medio, con buena superficie sin ocupar tanto como las mesas de 120 cm.", "Elige esta mesa si buscas equilibrio entre apoyo y ligereza visual. Encaja especialmente bien con sofás de dos plazas o pareja de sillones."),
        "seo": "Mesa de centro exterior HPL de 90 cm y altura 40 cm para terraza, jardín o porche.",
    },
    "mesa-de-centro-exterior-hpl-120-cm-altura-40-cm-2": {
        "body": table_body("120 cm", "40 cm", "HPL", "Su superficie amplia ayuda a ordenar salones exteriores con sofá y sillones alrededor.", "Elige esta mesa si quieres una pieza central para reuniones y uso diario. En terrazas pequeñas puede resultar demasiado larga."),
        "seo": "Mesa de centro exterior HPL de 120 cm y altura 40 cm para salón exterior.",
    },
    "mesa-de-centro-exterior-125-cm-altura-38-cm": {
        "body": table_body("125 cm", "38 cm", "", "La altura más baja crea una sensación lounge relajada frente a sofás y rinconeras.", "Elige esta mesa si priorizas una composición baja y cómoda. Comprueba que la altura encaja con tus asientos para no tener que inclinarte demasiado."),
        "seo": "Mesa de centro exterior de 125 cm y altura 38 cm para terraza lounge o jardín.",
    },
    "mesa-de-centro-exterior-120-cm-altura-41-cm": {
        "body": table_body("120 cm", "41 cm", "", "Es una mesa de centro amplia para acompañar sofás de exterior, rinconeras o composiciones con varias plazas.", "Elige esta mesa si tienes una zona de estar de tamaño medio o grande. Para balcones y pasos estrechos, valora medidas inferiores."),
        "seo": "Mesa de centro exterior de 120 cm y altura 41 cm para jardín, terraza o porche.",
    },
    "mesa-de-centro-exterior-90-cm-altura-40-cm-2": {
        "body": table_body("90 cm", "40 cm", "", "La medida de 90 cm es manejable y suficiente para apoyar lo cotidiano sin dominar la composición.", "Elige esta mesa si quieres una pieza versátil para sofá de dos plazas, sillones o una terraza media. Si recibes a menudo, quizá prefieras 120 cm."),
        "seo": "Mesa de centro exterior de 90 cm y altura 40 cm para terraza, jardín o patio.",
    },
    "mesa-de-centro-exterior-90-cm-altura-41-cm": {
        "body": table_body("90 cm", "41 cm", "", "Su altura ligeramente superior puede resultar cómoda junto a asientos con cojines más altos.", "Elige esta mesa si buscas apoyo accesible sin una pieza demasiado grande. Mide la distancia con el sofá para mantener una circulación cómoda."),
        "seo": "Mesa de centro exterior de 90 cm y altura 41 cm para zona lounge exterior.",
    },
    "mesa-de-centro-exterior-hpl-135-cm-altura-40-cm": {
        "body": table_body("135 cm", "40 cm", "HPL", "Es una opción amplia para composiciones exteriores grandes, especialmente si la mesa será el centro visual del conjunto.", "Elige esta mesa si tienes un sofá largo, rinconera o varios sillones alrededor. No es la mejor opción para terrazas estrechas."),
        "seo": "Mesa de centro exterior HPL de 135 cm y altura 40 cm para terraza amplia o jardín.",
    },
    "mesa-de-centro-exterior-hpl-120-cm-altura-40-cm": {
        "body": table_body("120 cm", "40 cm", "HPL", "El tablero HPL y la medida de 120 cm la orientan a un uso frecuente en salones exteriores completos.", "Elige esta mesa si quieres una superficie estable y amplia para una zona lounge. En espacios pequeños, revisa primero modelos de 70 o 90 cm."),
        "seo": "Mesa de centro exterior HPL de 120 cm y altura 40 cm para terraza o jardín.",
    },
    "mesa-de-centro-exterior-90-cm-altura-40-cm": {
        "body": table_body("90 cm", "40 cm", "", "Es una medida muy util para completar una zona de estar sin bloquear recorridos.", "Elige esta mesa si buscas una pieza sencilla y fácil de colocar. Puede funcionar frente a sofá, entre sillones o como apoyo en un porche."),
        "seo": "Mesa de centro exterior de 90 cm y altura 40 cm para jardín, terraza o porche.",
    },
    "mesa-de-centro-exterior-120-cm-altura-40-cm-2": {
        "body": table_body("120 cm", "40 cm", "", "Su tamaño permite usarla como apoyo principal en reuniones, comidas informales o momentos de descanso al aire libre.", "Elige esta mesa si tienes suficiente superficie y quieres una mesa central protagonista. Si necesitas movilidad, compara antes peso y dimensiones."),
        "seo": "Mesa de centro exterior de 120 cm y altura 40 cm para salón exterior o terraza.",
    },
    "reposapies-exterior-504540-cm": {
        "body": footrest_body("50×45×40 cm", "compacto", "Por su tamaño contenido, resulta fácil de mover y de colocar junto a sillones individuales.", "Elige este reposapiés si quieres sumar comodidad sin ocupar demasiado. Para sofás grandes, puede interesar una medida más ancha."),
        "seo": "Reposapiés exterior compacto de 50×45×40 cm para sillón, terraza, jardín o porche.",
    },
    "reposapies-exterior-734640-cm": {
        "body": footrest_body("73×46×40 cm", "versátil", "La anchura de 73 cm da una superficie más cómoda para acompañar butacas amplias.", "Elige este reposapiés si buscas apoyo generoso sin llegar a una pieza muy voluminosa. Va bien con sillones lounge y zonas de lectura."),
        "seo": "Reposapiés exterior de 73×46×40 cm para terraza, jardín, porche o zona lounge.",
    },
    "reposapies-exterior-855043-cm-2": {
        "body": footrest_body("85×50×43 cm", "amplio", "Su tamaño permite un apoyo más desahogado y puede integrarse en composiciones lounge de mayor presencia.", "Elige este reposapiés si quieres completar un sillón profundo o un sofá exterior. En terrazas pequeñas, mide bien el fondo total con el asiento."),
        "seo": "Reposapiés exterior amplio de 85×50×43 cm para sofá o sillón de terraza.",
    },
    "reposapies-exterior-bicolor-704544-cm": {
        "body": footrest_body("70×45×44 cm", "bicolor", "El acabado bicolor añade contraste y lo hace útil cuando quieres que el apoyo también participe visualmente en el conjunto.", "Elige este reposapiés si quieres comodidad con un punto decorativo. Revisa que combine con cojines, estructura y mesa de tu zona exterior."),
        "seo": "Reposapiés exterior bicolor de 70×45×44 cm para terraza, jardín o porche.",
    },
    "reposapies-exterior-605040-cm": {
        "body": footrest_body("60×50×40 cm", "equilibrado", "La proporción intermedia permite usarlo como apoyo cómodo sin ocupar tanto como los modelos más anchos.", "Elige este reposapiés si buscas una pieza fácil de integrar con sillones de tamaño medio. Es práctico para zonas lounge compactas."),
        "seo": "Reposapiés exterior de 60×50×40 cm para sillón de terraza, jardín o porche.",
    },
    "reposapies-exterior-855043-cm": {
        "body": footrest_body("85×50×43 cm", "amplio", "Es una medida cómoda para completar asientos con más fondo y crear una postura de descanso más relajada.", "Elige este reposapiés si quieres una pieza amplia para uso frecuente. Si el paso es estrecho, comprueba el conjunto sillón más reposapiés antes de comprar."),
        "seo": "Reposapiés exterior de 85×50×43 cm para zona lounge, terraza, jardín o porche.",
    },
    "balliu-tumbona-de-exterior-resina-923110d9": {
        "body": lounger_body("de resina con diseño de tablillas", "resina Balliu", "Es una opción práctica para quien busca una tumbona resistente al uso frecuente y fácil de limpiar.", "Elige esta tumbona si priorizas mantenimiento sencillo y estética de tablillas. Para una sensación más textil, revisa modelos con superficie de tela."),
        "seo": "Tumbona exterior resina Balliu Eva Pro T con diseño de tablillas para piscina, jardín o terraza.",
    },
    "balliu-tumbona-de-exterior-resina-b19af1ea": {
        "body": lounger_body("de resina con superficie textil", "resina y tela Balliu", "La superficie de tela aporta una sensación de uso más flexible que una tumbona completamente rígida.", "Elige esta tumbona si buscas una opción cómoda para piscina o jardín con mantenimiento sencillo. Si necesitas máxima robustez visual, compara con modelos de tablillas."),
        "seo": "Tumbona exterior resina Balliu Eva Pro con tela para piscina, terraza, jardín o solárium.",
    },
    "balliu-tumbona-de-exterior-sin-ruedas-aluminio-da3f5c24": {
        "body": lounger_body("de aluminio sin ruedas", "aluminio Balliu", "El aluminio la orienta a espacios donde se busca una pieza ligera visualmente y apta para uso exterior frecuente.", "Elige esta tumbona si quieres una pieza de aluminio para terraza o piscina y no necesitas moverla constantemente con ruedas."),
        "seo": "Tumbona exterior aluminio Balliu Olimpia sin ruedas para piscina, terraza o jardín.",
    },
    "balliu-tumbona-de-exterior-aluminio-36870d09": {
        "body": lounger_body("de aluminio", "aluminio Balliu", "Es una tumbona pensada para zonas de descanso donde se valora una estructura ligera y una imagen limpia.", "Elige esta tumbona si quieres aluminio para piscina, terraza o jardín. Si el usuario necesita más facilidad de acceso, revisa también la versión alta."),
        "seo": "Tumbona exterior aluminio Balliu Etna para piscina, jardín, terraza o solárium.",
    },
    "tumbona-de-exterior": {
        "body": lounger_body("para descanso diario", "exterior", "Es una pieza sencilla para crear una zona de sol o relax sin montar un conjunto completo.", "Elige esta tumbona si buscas una solución directa para descansar al aire libre. Antes de comprar, revisa medidas, movilidad y espacio para circular alrededor."),
        "seo": "Tumbona de exterior para terraza, jardín, piscina o solárium. Descanso al aire libre.",
    },
    "balliu-tumbona-de-exterior-resina-75-cm-009e68e4": {
        "body": lounger_body("de resina de 75 cm con superficie textil", "resina y tela Balliu", "La anchura de 75 cm ayuda a ofrecer una zona de descanso cómoda sin perder el enfoque práctico de la resina.", "Elige esta tumbona si buscas una pieza Balliu de resina para piscina, jardín o terraza con apoyo textil y mantenimiento sencillo."),
        "seo": "Tumbona exterior resina Balliu Carmen de 75 cm con tela para piscina, jardín o terraza.",
    },
    "balliu-tumbona-de-exterior-aluminio-d08586c1": {
        "body": lounger_body("de aluminio alta y de acceso fácil", "aluminio Balliu", "La altura facilita sentarse y levantarse, algo importante en hoteles, piscinas o usuarios que prefieren no quedar tan cerca del suelo.", "Elige esta tumbona si priorizas comodidad de acceso y estructura de aluminio. Es especialmente interesante para uso frecuente o zonas con varias tumbonas."),
        "seo": "Tumbona exterior aluminio alta Balliu Etna Alta de acceso fácil para piscina o terraza.",
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
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 5 ({len(PRODUCTS)} fichas)\n")

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
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch5_{ts}.json")
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
