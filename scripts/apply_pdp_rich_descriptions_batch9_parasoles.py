#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 9 — fichas ricas para los 4 parasoles DRAFT que son modelos
reales pendientes de publicar (no duplicados de migracion).

Solo toca estos 4 handles. NO publica: deja el status DRAFT como esta.
Descripciones ancladas en los datos reales de cada producto (medida, material,
estructura, tejido, vendor); no se inventan especificaciones no confirmadas.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch9_parasoles.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch9_parasoles.py --apply
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


# --- Cuerpos hand-authored, anclados en datos reales de cada parasol ---

def agora_body():
    return (
        p("<strong>Parasol cuadrado de exterior de aluminio de 200×200 cm, modelo Ágora, pensado para crear una zona de sombra estable en terraza, balcón o jardín.</strong> Es una buena opción cuando quieres cubrir una mesa cuadrada o un rincón de descanso sin recurrir a un parasol de gran diámetro.")
        + p("Antes de comprar, mide la superficie a cubrir y deja margen para mover sillas bajo la sombra. La estructura es de acero inoxidable con mástil central fijo y 8 varillas de fibra de vidrio, una combinación pensada para aguantar el uso continuado en exterior. Recuerda que la base no está incluida y se pide aparte según el peso que necesites.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> parasol cuadrado de exterior con mástil central fijo.",
            "<strong>Medida:</strong> 200 × 200 cm.",
            "<strong>Estructura:</strong> acero inoxidable y 8 varillas de fibra de vidrio.",
            "<strong>Tejido:</strong> a elegir entre acrílico (6 colores) y tela Balliu (3 colores), resistente al desgarro y a la decoloración por el sol.",
            "<strong>Uso recomendado:</strong> terraza, balcón, jardín o zona de comedor exterior.",
            "<strong>Importante:</strong> base no incluida — pídela aparte según superficie y exposición al viento.",
        ])
        + p("Elige el Ágora si buscas un parasol cuadrado proporcionado para mesas de hasta cuatro plazas. En zonas expuestas al viento, prioriza una base de peso suficiente y recógelo cuando no esté en uso.")
    )


def viena_body():
    return (
        p("<strong>Parasol de exterior de Ø300 cm para terraza y jardín, pensado para aportar amplia sombra sobre una mesa o una zona de estar al aire libre.</strong> Su diámetro de 3 metros cubre con holgura una mesa redonda o un grupo de sillas, manteniendo una línea sobria y funcional.")
        + p("Antes de comprar, comprueba el espacio libre alrededor para abrirlo por completo y la base que vas a usar, ya que condiciona la estabilidad. Está preparado para uso exterior durante todo el año: resiste rayos UV, lluvia y humedad, y su montaje no requiere herramientas especiales, así que es fácil de instalar y recoger por temporada.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> parasol de terraza de diámetro grande.",
            "<strong>Medida:</strong> Ø300 cm.",
            "<strong>Resistencia:</strong> preparado frente a rayos UV, lluvia y humedad para exterior todo el año.",
            "<strong>Montaje:</strong> sencillo, sin herramientas especiales, y fácil de transportar.",
            "<strong>Uso recomendado:</strong> terraza, jardín, porche o zona de comedor exterior.",
            "<strong>Importante:</strong> base no incluida — elige el peso según superficie y viento.",
        ])
        + p("Elige este parasol Ø300 si necesitas cubrir una mesa amplia o una zona de descanso con un diseño elegante y resistente. Para zonas ventosas, combínalo con una base de peso adecuado y recógelo en episodios de viento fuerte.")
    )


def caracas_body():
    return (
        p("<strong>Parasol de exterior de Ø300 cm para terraza y jardín, una opción ajustada de precio para conseguir sombra efectiva sin renunciar a color y estilo.</strong> Encaja bien en terrazas dinámicas y modernas donde quieras una pieza práctica y resolutiva para el día a día.")
        + p("Antes de comprar, mide la zona a cubrir y revisa el espacio para abrirlo del todo, además de la base que vas a emplear. Está preparado para uso exterior durante todo el año: resiste rayos UV, lluvia y humedad, y se monta sin herramientas especiales, lo que facilita instalarlo, moverlo y guardarlo entre temporadas.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> parasol de terraza de diámetro grande, opción económica.",
            "<strong>Medida:</strong> Ø300 cm.",
            "<strong>Resistencia:</strong> preparado frente a rayos UV, lluvia y humedad para exterior todo el año.",
            "<strong>Montaje:</strong> sencillo, sin herramientas especiales, y fácil de transportar.",
            "<strong>Uso recomendado:</strong> terraza, balcón amplio, jardín o zona de descanso exterior.",
            "<strong>Importante:</strong> base no incluida — elige el peso según superficie y viento.",
        ])
        + p("Elige este parasol Ø300 si buscas la mayor sombra por precio para una terraza moderna. Para zonas expuestas, acompáñalo de una base estable y recógelo cuando no esté en uso.")
    )


def samson_body():
    return (
        p("<strong>Parasol de exterior de Ø350 cm para terraza y jardín, pensado para cubrir zonas amplias de comedor o descanso al aire libre.</strong> Su gran diámetro de 3,5 metros ofrece una cobertura generosa, ideal cuando una sola sombra debe proteger a varias personas o una mesa grande.")
        + p("Antes de comprar, asegúrate de contar con espacio suficiente para abrirlo por completo y una base robusta acorde a su tamaño, ya que a mayor diámetro mayor es la importancia de la estabilidad. Está preparado para uso exterior durante todo el año: resiste rayos UV, lluvia y humedad, y combina resistencia con un diseño moderno.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> parasol de terraza de gran diámetro.",
            "<strong>Medida:</strong> Ø350 cm.",
            "<strong>Resistencia:</strong> preparado frente a rayos UV, lluvia y humedad para exterior todo el año.",
            "<strong>Cobertura:</strong> amplia, para zonas de comedor o descanso de varias plazas.",
            "<strong>Uso recomendado:</strong> terraza grande, jardín, porche o zona de comedor exterior.",
            "<strong>Importante:</strong> base no incluida — usa una base de peso suficiente para su tamaño.",
        ])
        + p("Elige este parasol Ø350 si necesitas la máxima cobertura para una zona amplia. Por su diámetro, prioriza siempre una base pesada y estable y recógelo en episodios de viento fuerte.")
    )


BODIES = {
    "parasol-cuadrado-200x200": (
        agora_body(),
        "Parasol cuadrado de exterior de aluminio 200x200 cm, modelo Ágora, para terraza, balcón o jardín. Base no incluida.",
    ),
    "parasol-para-terraza-300-cm": (
        viena_body(),
        "Parasol de exterior Ø300 cm para terraza y jardín. Amplia sombra, resistente a UV, lluvia y humedad, montaje sin herramientas.",
    ),
    "parasol-para-terraza-300-cm-2": (
        caracas_body(),
        "Parasol de exterior Ø300 cm para terraza y jardín, opción económica. Sombra efectiva, resistente a UV, lluvia y humedad.",
    ),
    "parasol-para-terraza-350-cm": (
        samson_body(),
        "Parasol de exterior Ø350 cm para terraza y jardín. Gran cobertura para comedor o descanso, resistente a UV, lluvia y humedad.",
    ),
}

HANDLES = list(BODIES.keys())

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
    payloads = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 9 parasoles ({len(HANDLES)} fichas)\n")

    for handle in HANDLES:
        try:
            product = gql(GET, {"h": handle})["productByHandle"]
        except Exception as exc:
            print(f"X {handle}: error leyendo ({exc})")
            errors += 1
            continue
        if not product:
            print(f"X {handle}: no encontrado")
            errors += 1
            continue
        if product["productType"] != "Parasol":
            print(f"X {handle}: tipo inesperado '{product['productType']}' (esperado Parasol) - SALTADO por seguridad")
            errors += 1
            continue
        body, seo = BODIES[handle]
        products[handle] = product
        payloads[handle] = {"body": body, "seo": seo}
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
        print(f"- {handle}")
        print(f"  title: {product['title']}  [{product['status']}]")
        print(f"  words: {words(product['descriptionHtml'])}->{words(body)}")
        print(f"  meta: {seo}")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = os.path.join(ROOT, "content", "descriptions")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch9_parasoles_{ts}.json")
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)
    print(f"\nBackup de lo actual -> {backup_path}")

    if APPLY:
        print("\nAplicando cambios (status DRAFT NO se modifica)...")
        for handle, product in products.items():
            payload = payloads[handle]
            try:
                result = gql(
                    SET,
                    {"input": {"id": product["id"], "descriptionHtml": payload["body"], "seo": {"description": payload["seo"]}}},
                )["productUpdate"]
            except Exception as exc:
                print(f"X {handle}: error aplicando ({exc})")
                errors += 1
                continue
            if result["userErrors"]:
                print(f"! {handle}: userErrors: {result['userErrors']}")
                errors += 1
            else:
                print(f"OK {handle}")

    print(f"\n{'Aplicado' if APPLY else 'Dry-run completado'} - errores: {errors}")
    if not APPLY:
        print("Revisa el dry-run y ejecuta con --apply para escribir (siguen en DRAFT).")


if __name__ == "__main__":
    main()
