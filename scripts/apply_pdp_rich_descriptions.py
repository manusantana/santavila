#!/usr/bin/env python3
"""
Sprint PDP 2.0: descripciones ricas para productos con señales reales en GSC.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions.py --apply
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


PRODUCTS = {
    "banco-jardin-con-mesa-integrada-220-cm": {
        "body": html(
            p("<strong>Banco de jardín con mesa integrada de 220 cm para crear una zona exterior funcional sin montar un comedor completo.</strong> Es una pieza práctica para jardín, terraza amplia, porche, casa rural o zona de merienda donde se quiere combinar asiento y superficie de apoyo en un solo mueble."),
            p("Encaja especialmente bien si buscas un banco con mesa incorporada: permite sentarse, apoyar bebidas, comer algo informal o crear un punto de reunión en exterior sin depender de mesa y sillas separadas. Por su formato alargado, conviene medir el espacio libre y dejar paso alrededor para sentarse y levantarse con comodidad."),
            h2("Detalles clave"),
            ul([
                "<strong>Formato:</strong> banco exterior con mesa integrada.",
                "<strong>Medida:</strong> 220 cm de largo.",
                "<strong>Uso recomendado:</strong> jardín, terraza amplia, porche, patio o casa rural.",
                "<strong>Ideal para:</strong> comidas informales, descanso, reuniones y zonas comunes al aire libre.",
                "<strong>Mantenimiento:</strong> limpiar con paño suave y revisar el estado del mueble antes de cada temporada.",
            ]),
            p("Si dudas entre este banco y una mesa de comedor exterior, elige esta opción cuando quieras una composición compacta, estable y siempre montada. Si necesitas mover las sillas a menudo o cambiar la distribución, una mesa independiente puede darte más flexibilidad."),
        ),
        "seo": "Banco de jardín con mesa integrada de 220 cm. Banco con mesa incorporada para terraza, porche, patio o casa rural.",
    },
    "pergola-aluminio-para-jardin-300300250-cm": {
        "body": html(
            p("<strong>Pérgola de aluminio para jardín y terraza, con medidas 300×300×250 cm, pensada para crear una zona de sombra fija sobre comedor, sofá exterior o rincón de descanso.</strong> Es una alternativa interesante para quien busca una pérgola 250x300 o una estructura cercana a 300 x 250 cm y necesita valorar encaje, altura y uso real antes de comprar."),
            p("La estructura de aluminio resulta adecuada para exterior porque combina ligereza, resistencia a la corrosión y bajo mantenimiento. Aun así, como en cualquier pérgola, conviene revisar anclaje, exposición al viento, ubicación y espacio libre alrededor. La medida debe comprobarse en el suelo antes de instalarla, especialmente si va junto a pared, barandilla, piscina o paso habitual."),
            h2("Detalles clave"),
            ul([
                "<strong>Medidas visibles:</strong> 300×300×250 cm.",
                "<strong>Material:</strong> aluminio para uso exterior.",
                "<strong>Uso recomendado:</strong> jardín, terraza, patio o zona de comedor exterior.",
                "<strong>Función:</strong> aportar sombra y ordenar una zona de estar al aire libre.",
                "<strong>Consejo:</strong> medir paso, altura útil y puntos de fijación antes de decidir ubicación.",
            ]),
            p("Elige esta pérgola si quieres una zona exterior más definida que con un parasol. Si necesitas una sombra móvil o tienes mucho viento, revisa también opciones de parasol bien lastrado y soluciones desmontables."),
        ),
        "seo": "Pérgola de aluminio 300×300×250 cm para jardín o terraza. Opción para búsquedas de pérgola 250x300 y sombra exterior.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm": {
        "body": html(
            p("<strong>Sofá de terraza de 2 plazas y 120×78 cm, pensado para balcones amplios, áticos y terrazas compactas donde se quiere crear una zona lounge sin ocupar demasiado fondo.</strong> Su medida de 120 cm lo convierte en una opción útil para búsquedas como sofá terraza 120 cm, donde el usuario necesita comprobar si la pieza cabe de verdad."),
            p("Funciona bien como asiento principal en una terraza pequeña, acompañado de una mesa auxiliar, una butaca ligera o una alfombra exterior. Antes de comprar, mide el ancho disponible, el fondo de paso y la apertura de puertas. En espacios ajustados, la diferencia entre un sofá de 120 cm y uno de 140-150 cm puede ser decisiva para poder circular o limpiar cómodamente."),
            h2("Detalles clave"),
            ul([
                "<strong>Formato:</strong> sofá exterior de 2 plazas.",
                "<strong>Medida:</strong> 120×78 cm.",
                "<strong>Estilo:</strong> contemporáneo y fácil de combinar.",
                "<strong>Uso recomendado:</strong> terraza, balcón amplio, porche o ático.",
                "<strong>Combina con:</strong> mesa auxiliar, sillón ligero o cojines de exterior.",
            ]),
            p("Elige este sofá si priorizas una zona de estar compacta. Si buscas tumbarte o recibir a más personas, puede interesarte un sofá de 3 plazas o una composición con sillones adicionales."),
        ),
        "seo": "Sofá terraza 120 cm de 2 plazas para exterior. Diseño contemporáneo para balcón amplio, ático, porche o terraza compacta.",
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm": {
        "body": html(
            p("<strong>Sofá exterior de 2 plazas y 130×90 cm, una medida equilibrada para quien busca más presencia que un sofá compacto sin pasar a un formato grande.</strong> Es una buena opción para búsquedas como sofá exterior 130 cm, donde importa tanto el ancho como el fondo real que ocupa en la terraza."),
            p("Su formato de 2 plazas encaja en terrazas medianas, porches, patios y zonas chill out donde se quiere un asiento cómodo y visualmente ordenado. La profundidad de 90 cm pide algo más de espacio que otros sofás compactos, así que conviene comprobar si queda paso suficiente delante y a los lados. Si lo acompañas con mesa de centro, deja margen para sentarse sin mover todos los muebles."),
            h2("Detalles clave"),
            ul([
                "<strong>Formato:</strong> sofá de exterior de 2 plazas.",
                "<strong>Medida:</strong> 130×90 cm.",
                "<strong>Estilo:</strong> contemporáneo para salones exteriores actuales.",
                "<strong>Uso recomendado:</strong> terraza, jardín, porche o zona de descanso.",
                "<strong>Antes de comprar:</strong> medir fondo útil y paso delante del sofá.",
            ]),
            p("Elige este sofá si quieres una pieza principal para una zona lounge pequeña o media. Si el espacio es muy estrecho, valora el sofá de 120 cm; si quieres recibir más personas, mira sofás de 3 plazas o conjuntos completos."),
        ),
        "seo": "Sofá exterior 130 cm de 2 plazas para terraza, jardín o porche. Sofá contemporáneo 130×90 cm para zona lounge.",
    },
    "balliu-tumbona-de-exterior-resina-28ff014d": {
        "body": html(
            p("<strong>Tumbona Balliu de exterior en resina para jardín, piscina y zonas de descanso donde se busca una pieza práctica, fácil de limpiar y preparada para uso frecuente.</strong> Es una ficha relevante para búsquedas de tumbonas de resina, tumbonas jardín resina y tumbona Balliu, especialmente cuando el usuario compara mantenimiento y resistencia antes de comprar."),
            p("La resina es una opción habitual en piscina y terrazas porque no se oxida, se limpia con facilidad y suele resultar más ligera que otros materiales. La clave está en usarla correctamente: evitar abrasivos, limpiar con agua y jabón suave y no dejar suciedad acumulada durante semanas. En zonas de mucho sol o cloro, conviene revisar color, textura y estado general al inicio y final de temporada."),
            h2("Detalles clave"),
            ul([
                "<strong>Material:</strong> resina para exterior.",
                "<strong>Marca:</strong> Balliu.",
                "<strong>Uso recomendado:</strong> piscina, jardín, terraza y espacios de descanso.",
                "<strong>Ventaja práctica:</strong> limpieza sencilla y buen encaje en uso intensivo.",
                "<strong>Mantenimiento:</strong> agua, jabón suave y secado antes de guardar o cubrir.",
            ]),
            p("Elige esta tumbona si priorizas facilidad de mantenimiento y uso frecuente. Si buscas una estética más cálida, puede interesarte comparar con madera; si necesitas máxima ligereza, revisa también tumbonas de aluminio."),
        ),
        "seo": "Tumbona Balliu de exterior en resina para jardín, piscina y terraza. Tumbona de resina fácil de limpiar y mantener.",
    },
    "set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro": {
        "body": html(
            p("<strong>Set rinconera exterior contemporáneo con sofá de esquina y mesa de centro, pensado para crear un salón al aire libre amplio y ordenado.</strong> Es una solución interesante para búsquedas como rinconera terraza, rinconera jardín o sofá de esquina exterior, donde el objetivo no es solo sentarse, sino aprovechar una zona completa de reunión."),
            p("La composición de esquina ayuda a delimitar el espacio y puede funcionar muy bien en terrazas medianas o grandes, porches y jardines. Antes de decidir, mide la huella completa del conjunto, la apertura de puertas, el paso alrededor y el espacio para mover la mesa de centro. En terrazas pequeñas, una rinconera puede saturar rápido si bloquea el acceso o deja poco espacio para limpiar."),
            h2("Detalles clave"),
            ul([
                "<strong>Incluye:</strong> sofá de esquina y mesa de centro.",
                "<strong>Estilo:</strong> contemporáneo para exterior.",
                "<strong>Uso recomendado:</strong> terraza amplia, jardín, porche o patio.",
                "<strong>Ideal para:</strong> zona lounge, reuniones y descanso al aire libre.",
                "<strong>Mantenimiento:</strong> limpiar estructura con suavidad y guardar textiles secos cuando no se usen.",
            ]),
            p("Elige esta rinconera si quieres una zona exterior protagonista y tienes espacio suficiente. Si tu terraza es estrecha, puede funcionar mejor un sofá de 2 plazas con sillones o piezas modulares más ligeras."),
        ),
        "seo": "Rinconera de terraza con sofá de esquina y mesa de centro. Set exterior contemporáneo para jardín, porche o patio amplio.",
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
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 1 ({len(PRODUCTS)} fichas)\n")

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
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch1_{ts}.json")
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
