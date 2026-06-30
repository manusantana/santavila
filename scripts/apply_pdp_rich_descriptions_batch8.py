#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 8 para optimizar fichas aceptables (80-119 palabras)
con señales comerciales claras: parasoles/bases, tumbonas Balliu y mesas de apoyo.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch8.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch8.py --apply
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

HANDLES = [
    "mesa-de-centro-exterior-120-cm-altura-40-cm",
    "balliu-parasol-para-terraza-f1ed8b8b",
    "base-de-parasol-25-kg",
    "balliu-tumbona-de-exterior-aluminio-68-cm-f7ab4da8",
    "balliu-colchoneta-para-tumbona-0e9a3256",
    "balliu-parasol-para-terraza-acrilico-236bd5f0",
    "balliu-parasol-para-terraza-acrilico-c8dd492d",
    "balliu-parasol-para-terraza-aluminio-300-cm-6c1e1224",
    "balliu-parasol-para-terraza-aluminio-300-cm-0ceba8e7",
    "balliu-tumbona-de-exterior-resina-75-cm-aca076ae",
    "balliu-tumbona-de-exterior-resina-73-cm-0648657b",
    "balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e",
]


def p(text):
    return f"<p>{text}</p>"


def h2(text):
    return f"<h2>{text}</h2>"


def ul(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def clean_title(title):
    return re.sub(r"\s+", " ", title.replace("·", "").strip())


def size_from(title):
    match = re.search(r"(Ø?[0-9]+(?:×[0-9]+)?(?:/[Ø0-9×]+)?\s?cm|[0-9]+(?:-[0-9]+)?×[0-9]+\s?cm)", title)
    return match.group(1).replace(" ", "") if match else ""


def material_from(title):
    lower = title.lower()
    bits = []
    if "aluminio" in lower:
        bits.append("aluminio")
    if "hpl" in lower:
        bits.append("HPL")
    if "resina" in lower:
        bits.append("resina")
    if "acrílico" in lower or "acrilico" in lower:
        bits.append("acrílico")
    if "tela" in lower or "tejido" in lower:
        bits.append("tejido exterior")
    return " y ".join(bits)


def parasol_body(title):
    lower = title.lower()
    size = size_from(title)
    material = material_from(title) or "materiales para uso exterior"
    kind = "parasol lateral" if "lateral" in lower else "parasol exterior"
    shape_note = "formato cuadrado" if "cuadrado" in lower else "formato redondo" if "redondo" in lower or "ø" in lower else "formato de sombra"
    return (
        p(f"<strong>{title}, pensado para crear sombra útil en terraza, jardín, piscina o zona de comedor exterior.</strong> Es una pieza clave cuando el espacio recibe sol directo y necesitas proteger mesa, tumbonas o zona lounge sin ocupar más mobiliario del necesario.")
        + p("Antes de elegir, revisa diámetro o huella de apertura, base compatible, orientación del sol y exposición al viento. En parasoles de exterior conviene valorar tanto la cobertura de sombra como la estabilidad y la facilidad de plegado al terminar el uso.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Formato:</strong> {kind} ({shape_note}).",
            f"<strong>Medida:</strong> {size or 'según variante disponible'}.",
            f"<strong>Material destacado:</strong> {material}.",
            "<strong>Uso recomendado:</strong> terraza, jardín, patio, piscina o comedor exterior.",
            "<strong>Consejo:</strong> combinar siempre con una base adecuada y cerrar en días de viento.",
        ])
        + p("Elige este parasol si buscas una solución de sombra sencilla y flexible. Para zonas muy expuestas, prioriza estabilidad, peso de base y una ubicación donde pueda cerrarse con facilidad.")
    )


def base_body(title):
    size = size_from(title)
    return (
        p(f"<strong>{title}, pensada para dar estabilidad al parasol en terrazas, patios y jardines.</strong> Es un accesorio pequeño en apariencia, pero decisivo para que la zona de sombra funcione con seguridad y no dependa solo del peso del mástil.")
        + p("Antes de comprar, confirma el diámetro compatible del tubo, el peso necesario según el parasol y la superficie donde irá colocada. En exterior también importa que la base se pueda mover, limpiar y ubicar sin bloquear pasos habituales.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> base para parasol.",
            f"<strong>Peso o medida:</strong> {size or '25 kg'}.",
            "<strong>Uso recomendado:</strong> parasoles en terraza, jardín, patio o zona de piscina.",
            "<strong>Consejo:</strong> ajustar bien el mástil y evitar usar el parasol abierto con viento fuerte.",
            "<strong>Mantenimiento:</strong> limpiar la superficie y revisar fijaciones al inicio de temporada.",
        ])
        + p("Elige esta base si necesitas completar un parasol con una sujeción estable. Si el parasol es grande o queda en una zona abierta, revisa si conviene aumentar peso o usar una solución específica.")
    )


def lounger_body(title):
    lower = title.lower()
    size = size_from(title)
    material = material_from(title) or "diseño para uso exterior"
    is_pad = "colchoneta" in lower
    if is_pad:
        return (
            p(f"<strong>{title}, pensada para mejorar la comodidad de una tumbona exterior sin cambiar la estructura principal.</strong> Es un complemento útil para zonas de piscina, solárium, terraza o jardín donde se busca más confort en sesiones largas de descanso.")
            + p("Antes de elegir, revisa compatibilidad de medidas, grosor, sistema de sujeción y facilidad de secado. En textiles de exterior conviene evitar humedad retenida y guardar o proteger la pieza cuando no se use durante varios días.")
            + h2("Detalles clave")
            + ul([
                "<strong>Formato:</strong> colchoneta para tumbona exterior.",
                f"<strong>Material destacado:</strong> {material}.",
                "<strong>Uso recomendado:</strong> piscina, jardín, terraza, hotel o alojamiento turístico.",
                "<strong>Consejo:</strong> comprobar largo y ancho de la tumbona antes de comprar.",
                "<strong>Mantenimiento:</strong> ventilar, limpiar con suavidad y dejar secar antes de guardar.",
            ])
            + p("Elige esta colchoneta si quieres ganar confort sin sustituir la tumbona. Si la zona está muy expuesta, combínala con funda o almacenaje protegido entre usos.")
        )
    return (
        p(f"<strong>{title}, diseñada para descanso exterior en piscina, terraza, jardín o solárium.</strong> Es una tumbona adecuada cuando necesitas una pieza resistente, fácil de integrar y orientada a uso frecuente al aire libre.")
        + p("Antes de comprar, mide el largo disponible, el paso lateral y el espacio necesario para moverla o apilarla. En tumbonas de exterior conviene valorar material, peso, facilidad de limpieza y si se usará en entorno residencial, hotelero o cerca de piscina.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> tumbona exterior.",
            f"<strong>Medida o ancho:</strong> {size or 'según modelo'}.",
            f"<strong>Material destacado:</strong> {material}.",
            "<strong>Uso recomendado:</strong> piscina, jardín, terraza, solárium o alojamiento turístico.",
            "<strong>Mantenimiento:</strong> limpieza suave, secado y protección fuera de temporada.",
        ])
        + p("Elige esta tumbona si buscas una zona de relax práctica y repetible. Para uso intensivo, revisa apilabilidad, ruedas, recambios textiles y facilidad de limpieza diaria.")
    )


def table_body(title):
    size = size_from(title)
    material = material_from(title) or "materiales para exterior"
    return (
        p(f"<strong>{title}, pensada como superficie de apoyo para sofás, sillones, tumbonas o zonas lounge de exterior.</strong> Es una mesa práctica cuando necesitas tener cerca bebidas, libros, textiles o pequeños objetos sin montar un comedor completo.")
        + p("Antes de comprar, revisa altura, largo, paso alrededor y proporción frente al sofá o conjunto principal. En mesas de centro para exterior conviene valorar limpieza del tablero, estabilidad y resistencia al uso cotidiano en terraza, jardín o porche.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> mesa de centro exterior.",
            f"<strong>Medida principal:</strong> {size or 'según modelo'}.",
            f"<strong>Material destacado:</strong> {material}.",
            "<strong>Uso recomendado:</strong> zona lounge, terraza, jardín, porche o piscina.",
            "<strong>Consejo:</strong> dejar paso cómodo entre asiento y mesa para no saturar el espacio.",
        ])
        + p("Elige esta mesa si quieres completar una zona de descanso con una pieza útil y discreta. Para espacios pequeños, prioriza medidas compactas y circulación cómoda alrededor.")
    )


def payload_for(product):
    title = product["title"]
    product_type = product["productType"]
    if product_type == "Parasol":
        body = parasol_body(title)
    elif product_type == "Accesorios":
        body = base_body(title)
    elif product_type == "Tumbona":
        body = lounger_body(title)
    elif product_type in ("Mesa", "Mesa centro"):
        body = table_body(title)
    else:
        body = table_body(title)
    return {"body": body, "seo": seo_for(title, product_type)}


def seo_for(title, product_type):
    title = clean_title(title)
    if product_type == "Parasol":
        return f"{title} para sombra en terraza, jardín o piscina. Revisa medida, base compatible y uso exterior."[:155]
    if product_type == "Accesorios":
        return f"{title} para estabilizar parasoles en terraza, jardín o patio. Base práctica para uso exterior."[:155]
    if product_type == "Tumbona":
        return f"{title} para piscina, jardín o terraza. Descanso exterior con criterios de medida, material y mantenimiento."[:155]
    return f"{title} para terraza, jardín o porche. Mesa de apoyo exterior con medida y material pensados para uso diario."[:155]


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
    payloads = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 8 ({len(HANDLES)} fichas)\n")

    for handle in HANDLES:
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
        payload = payload_for(product)
        products[handle] = product
        payloads[handle] = payload
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
        print(f"  type: {product['productType']}")
        print(f"  words: {words(product['descriptionHtml'])}->{words(payload['body'])}")
        print(f"  meta: {payload['seo']}")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = os.path.join(ROOT, "content", "descriptions")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch8_{ts}.json")
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)
    print(f"\nBackup de lo actual -> {backup_path}")

    if APPLY:
        print("\nAplicando cambios...")
        for handle, product in products.items():
            payload = payloads[handle]
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
