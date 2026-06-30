#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 7 para cerrar familias menores bajo 80 palabras.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch7.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch7.py --apply
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
    "set-losas-cemento-para-base-de-parasol",
    "silla-exterior-estilo-contemporaneo",
    "mesa-comedor-exterior-hpl-15090-cm",
    "balancin-jardin-exterior-148194-cm",
    "silla-exterior-estilo-estilizado",
    "mesa-comedor-exterior-hpl-10090-cm",
    "mesa-comedor-exterior-hpl-13590-cm",
    "set-rinconera-exterior-sofisticado-sofa-de-esquina-mesa-de-centro",
    "balliu-pie-de-parasol-c2147052",
    "balliu-base-de-parasol-3ee8b72d",
    "balliu-funda-protectora-exterior-340b2844",
    "balliu-funda-protectora-exterior-acrilico-a1c16324",
    "balliu-funda-protectora-exterior-6f6d4953",
    "balliu-silla-exterior-sin-brazos-resina-estilo-funcional-daabcdaf",
    "balliu-mini-tumbona-de-exterior-aluminio-57-cm-98ab84ce",
    "balliu-funda-protectora-exterior-686cc405",
    "balliu-mobiliario-exterior-resina-28-cm-6264905d",
    "balliu-silla-exterior-resina-estilo-funcional-0b607ec7",
    "balliu-mesa-exterior-5d0fb586",
    "balliu-mesa-exterior-aluminio-7070-cm-1b61e6b6",
    "balliu-mesa-exterior-aluminio-75-cm-dd745448",
    "balliu-silla-exterior-resina-estilo-minimalista-484cbea0",
]


def p(text):
    return f"<p>{text}</p>"


def h2(text):
    return f"<h2>{text}</h2>"


def ul(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def size_from(title):
    match = re.search(r"([0-9]+(?:×[0-9]+)?(?:/[0-9]+)?\s?cm|Ø[0-9]+(?:/Ø[0-9]+)?\s?cm)", title)
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
    if "cemento" in lower or "hormigón" in lower or "hormigon" in lower:
        bits.append("cemento/hormigón")
    return " y ".join(bits)


def chair_body(title):
    size = size_from(title)
    material = material_from(title)
    size_text = f" de {size}" if size else ""
    material_text = f" en {material}" if material else ""
    material_detail = material if material else "diseño para uso exterior"
    return (
        p(f"<strong>Silla de exterior{size_text}{material_text}, pensada para completar comedor, terraza, jardín o zona auxiliar al aire libre.</strong> Es una pieza práctica cuando necesitas asientos fáciles de mover, combinar y repetir sin montar un conjunto lounge completo.")
        + p("Antes de comprar, revisa el espacio disponible alrededor de la mesa, el paso entre sillas y si necesitas apilabilidad o bajo mantenimiento. En exterior conviene pensar tanto en la comodidad como en la facilidad de limpieza y almacenaje de temporada.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> silla individual de exterior.",
            f"<strong>Medida o familia:</strong> {size or 'formato exterior'}.",
            f"<strong>Material destacado:</strong> {material_detail}.",
            "<strong>Uso recomendado:</strong> terraza, jardín, comedor exterior, patio o alojamiento turístico.",
            "<strong>Mantenimiento:</strong> limpieza suave y secado antes de guardar o cubrir.",
        ])
        + p("Elige esta silla si buscas una pieza funcional para uso diario en exterior. Si va a estar siempre a la intemperie, revisa también peso, estabilidad y facilidad de mover varias unidades.")
    )


def table_body(title, product_type):
    size = size_from(title)
    material = material_from(title)
    label = "mesa de comedor exterior" if product_type == "Mesa comedor" else "mesa exterior"
    material_text = f" en {material}" if material else ""
    material_detail = material if material else "diseño para uso exterior"
    return (
        p(f"<strong>{label.capitalize()}{' de ' + size if size else ''}{material_text}, pensada para crear una zona práctica de comida, apoyo o reunión al aire libre.</strong> Encaja en terrazas, jardines y porches donde la mesa debe aportar superficie útil sin complicar la distribución.")
        + p("Antes de comprar, mide no solo el tablero: deja espacio para sillas, paso alrededor y apertura de puertas o accesos cercanos. En mesas de exterior también conviene valorar facilidad de limpieza, estabilidad y si el tamaño se adapta al número real de personas que la usarán.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Formato:</strong> {label}.",
            f"<strong>Medida principal:</strong> {size or 'según variante'}.",
            f"<strong>Material destacado:</strong> {material_detail}.",
            "<strong>Uso recomendado:</strong> terraza, jardín, patio, porche o comedor exterior.",
            "<strong>Consejo:</strong> comprueba paso libre con sillas ocupadas antes de decidir.",
        ])
        + p("Elige esta mesa si quieres una superficie estable y fácil de integrar en exterior. Para espacios estrechos, prioriza medidas compactas y recorridos cómodos alrededor.")
    )


def cover_body(title):
    material = material_from(title)
    material_detail = material if material else "tejido protector para exterior"
    target = "tumbona" if "tumbona" in title.lower() else "mueble exterior"
    return (
        p(f"<strong>Funda protectora para {target}, pensada para ayudar a conservar mejor el mobiliario exterior cuando no se está usando.</strong> Es un accesorio útil para reducir suciedad, polvo y exposición directa durante pausas de uso, especialmente en terrazas, patios y jardines.")
        + p("La funda no sustituye al mantenimiento, pero facilita proteger la pieza entre temporadas o en periodos de lluvia y poco uso. Antes de comprar, revisa medidas, forma del mueble y que la funda quede ajustada sin forzar costuras ni dejar bolsas de agua.")
        + h2("Detalles clave")
        + ul([
            "<strong>Formato:</strong> funda protectora de exterior.",
            f"<strong>Material o familia:</strong> {material_detail}.",
            f"<strong>Uso recomendado:</strong> proteger {target} en terraza, jardín o porche.",
            "<strong>Consejo:</strong> colocar siempre sobre superficies limpias y secas.",
            "<strong>Mantenimiento:</strong> ventilar y secar antes de guardar.",
        ])
        + p("Elige esta funda si quieres una capa adicional de protección para el día a día. Si el mueble queda expuesto mucho tiempo, combina funda, limpieza periódica y revisión de humedad.")
    )


def parasol_body(title):
    material = material_from(title)
    size = size_from(title)
    is_base = "base" in title.lower() or "pie" in title.lower()
    subject = "base o pie de parasol" if is_base else "parasol exterior"
    material_detail = material if material else "diseño para uso exterior"
    return (
        p(f"<strong>{subject.capitalize()}{' de ' + size if size else ''}, pensado para completar una zona de sombra en terraza, jardín o patio.</strong> Es una pieza auxiliar importante porque condiciona estabilidad, uso cómodo y seguridad del conjunto.")
        + p("Antes de comprar, revisa compatibilidad con el mástil o el parasol, peso, superficie donde irá colocado y exposición al viento. En exterior no basta con que encaje: también debe poder moverse, limpiarse y mantenerse estable según el uso previsto.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Formato:</strong> {subject}.",
            f"<strong>Medida o peso:</strong> {size or 'según modelo'}.",
            f"<strong>Material destacado:</strong> {material_detail}.",
            "<strong>Uso recomendado:</strong> terraza, jardín, patio, piscina o zona de comedor exterior.",
            "<strong>Consejo:</strong> comprobar compatibilidad y estabilidad antes de instalar.",
        ])
        + p("Elige esta pieza si necesitas completar una zona de sombra con criterio práctico. Para zonas expuestas, revisa siempre las recomendaciones de uso frente a viento.")
    )


def lounger_body(title, product_type):
    material = material_from(title)
    size = size_from(title)
    material_text = f" en {material}" if material else ""
    material_detail = material if material else "diseño para uso exterior"
    return (
        p(f"<strong>{product_type} exterior{' de ' + size if size else ''}{material_text}, pensada para crear una zona de descanso al aire libre en terraza, jardín o piscina.</strong> Es una pieza útil cuando se busca relax individual sin ocupar tanto como una tumbona grande.")
        + p("Antes de elegir, mide el largo disponible, el paso lateral y si necesitas mover varias unidades con frecuencia. En mobiliario de descanso exterior conviene valorar peso, plegado, apilabilidad y facilidad de limpieza según el uso real.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Formato:</strong> {product_type.lower()} de exterior.",
            f"<strong>Medida principal:</strong> {size or 'según modelo'}.",
            f"<strong>Material destacado:</strong> {material_detail}.",
            "<strong>Uso recomendado:</strong> piscina, terraza, jardín, solárium o alojamiento turístico.",
            "<strong>Mantenimiento:</strong> limpiar con suavidad y dejar secar antes de guardar.",
        ])
        + p("Elige esta pieza si quieres añadir descanso individual en poco espacio. Para uso intensivo, revisa movilidad, estabilidad y comodidad de acceso.")
    )


def generic_body(title, product_type):
    material = material_from(title)
    size = size_from(title)
    material_detail = material if material else "diseño para uso exterior"
    return (
        p(f"<strong>{title}, pensado para completar una zona exterior con una pieza práctica y coherente con el resto del mobiliario.</strong> Encaja en terrazas, jardines o porches donde cada elemento debe sumar uso real sin complicar la distribución.")
        + p("Antes de comprar, revisa medidas, ubicación y mantenimiento. En exterior conviene dejar paso suficiente, evitar acumulación de humedad y comprobar que el producto encaja con el uso previsto: descanso, apoyo, sombra, comedor o protección.")
        + h2("Detalles clave")
        + ul([
            f"<strong>Tipo:</strong> {product_type}.",
            f"<strong>Medida principal:</strong> {size or 'según modelo'}.",
            f"<strong>Material destacado:</strong> {material_detail}.",
            "<strong>Uso recomendado:</strong> terraza, jardín, patio o porche.",
            "<strong>Mantenimiento:</strong> limpieza suave y revisión al inicio de temporada.",
        ])
        + p("Elige esta pieza si resuelve una necesidad concreta dentro de tu zona exterior. Si tienes poco espacio, mide primero la huella completa y el paso alrededor.")
    )


def rinconera_body(title):
    return (
        p("<strong>Set rinconera exterior de estilo sofisticado con sofá de esquina y mesa de centro, pensado para crear una zona lounge amplia y bien definida.</strong> Es una composición útil cuando quieres aprovechar una esquina, ordenar varios asientos y resolver el salón exterior con una sola familia de piezas.")
        + p("Antes de comprar, mide los dos lados de la rinconera, el paso frontal y la posición de puertas, barandillas o accesos. En este tipo de conjunto es importante comprobar la huella completa, porque la comodidad depende tanto del asiento como del espacio libre alrededor.")
        + h2("Detalles clave")
        + ul([
            "<strong>Incluye:</strong> sofá de esquina y mesa de centro.",
            "<strong>Formato:</strong> conjunto rinconera para exterior.",
            "<strong>Estilo:</strong> sofisticado.",
            "<strong>Uso recomendado:</strong> terraza amplia, jardín, porche o patio.",
            "<strong>Consejo:</strong> marcar la planta en el suelo antes de decidir.",
        ])
        + p("Elige esta rinconera si quieres una zona exterior protagonista para reuniones y descanso. Si el espacio es irregular o estrecho, puede convenir una composición modular más ligera.")
    )


def payload_for(product):
    title = product["title"]
    product_type = product["productType"]
    if product_type == "Silla":
        body = chair_body(title)
    elif product_type in ("Mesa", "Mesa comedor"):
        body = table_body(title, product_type)
    elif product_type == "Funda":
        body = cover_body(title)
    elif product_type == "Parasol":
        body = parasol_body(title)
    elif product_type == "Conjunto rinconera":
        body = rinconera_body(title)
    elif product_type in ("Mini tumbona", "Mobiliario exterior"):
        body = lounger_body(title, product_type)
    else:
        body = generic_body(title, product_type)
    seo = seo_for(title, product_type)
    return {"body": body, "seo": seo}


def seo_for(title, product_type):
    clean = re.sub(r"\s+", " ", title.replace("·", "").strip())
    if product_type == "Conjunto rinconera":
        return f"{clean} para terraza o jardín. Rinconera exterior con sofá de esquina y mesa de centro."[:155]
    if product_type == "Mobiliario exterior":
        return f"{clean} para terraza, jardín o porche. Pieza auxiliar de exterior funcional."[:155]
    if product_type == "Accesorios":
        return f"{clean} para estabilizar parasoles en terraza, jardín o patio."[:155]
    if product_type == "Parasol":
        return f"{clean} para completar una zona de sombra en terraza, jardín o patio."[:155]
    if product_type == "Funda":
        return f"{clean} para proteger mobiliario exterior en terraza, jardín o porche."[:155]
    return f"{clean} para terraza, jardín o porche. {product_type} funcional para exterior."[:155]


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
        headers={"Content-Type": "application/json", "X-ShopIFY-Access-Token": SHOPIFY_ACCESS_TOKEN},
    )
    # Header keys are case-insensitive, but keep the canonical spelling for clarity.
    req.add_header("X-Shopify-Access-Token", SHOPIFY_ACCESS_TOKEN)
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
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 7 ({len(HANDLES)} fichas)\n")

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
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch7_{ts}.json")
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
