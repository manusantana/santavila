#!/usr/bin/env python3
"""
Sprint PDP 2.0: batch 6 de descripciones ricas para los sofas y conjuntos
sofa restantes bajo 80 palabras.

Por defecto no escribe nada:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch6.py

Para aplicar:
  .venv/bin/python scripts/apply_pdp_rich_descriptions_batch6.py --apply
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
    "sofa-terraza-3-plazas-estilo-elegante-22069-cm",
    "sofa-terraza-3-plazas-estilo-contemporaneo-19685-cm",
    "sofa-terraza-2-plazas-estilo-moderno-128115-cm",
    "sofa-terraza-3-plazas-estilo-contemporaneo-188115-cm",
    "sofa-terraza-2-plazas-estilo-contemporaneo-13785-cm",
    "sofa-terraza-3-plazas-estilo-contemporaneo-18590-cm",
    "sofa-terraza-3-plazas-estilo-contemporaneo-19882-cm",
    "sofa-terraza-3-plazas-estilo-contemporaneo-19085-cm",
    "sofa-terraza-2-plazas-estilo-elegante-15085-cm",
    "sofa-terraza-3-plazas-estilo-sofisticado-17578-cm",
    "sofa-terraza-bicolor-2-plazas-estilo-bicolor-14076-cm",
    "sofa-terraza-3-plazas-estilo-sofisticado-19475-cm",
    "sofa-terraza-bicolor-3-plazas-estilo-bicolor-20076-cm",
    "sofa-terraza-2-plazas-estilo-envolvente-13575-cm",
    "sofa-terraza-aluminio-3-plazas-estilo-contemporaneo-22090-cm",
    "sofa-terraza-aluminio-2-plazas-estilo-contemporaneo-16690-cm",
    "set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-2",
    "set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-4",
    "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-2",
    "set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa",
    "set-jardin-3-plazas-elegante-sofa-3-plazas-2-sillones-mesa",
    "set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-2",
    "set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-2",
    "set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa",
    "set-jardin-aluminio-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa",
    "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-3",
    "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4",
    "set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-4",
    "set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-3",
    "set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa",
    "set-jardin-3-plazas-urbano-sofa-3-plazas-2-sillones-mesa",
]


def p(text):
    return f"<p>{text}</p>"


def h2(text):
    return f"<h2>{text}</h2>"


def ul(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def title_bits(title):
    plazas = re.search(r"([23]) plazas", title)
    style = re.search(r"estilo ([^|]+)", title)
    if not style:
        style = re.search(r"·\s*([^|]+)\|", title)
    size = re.search(r"\|\s*([0-9]+×[0-9]+ cm)", title)
    return {
        "plazas": plazas.group(1) if plazas else "2",
        "style": (style.group(1).strip() if style else "contemporáneo").replace("bicolor", "bicolor"),
        "size": size.group(1) if size else "",
        "aluminio": "aluminio" in title.lower(),
        "bicolor": "bicolor" in title.lower(),
    }


def sofa_payload(title):
    bits = title_bits(title)
    plazas = bits["plazas"]
    style = bits["style"]
    size = bits["size"]
    material_note = " La estructura de aluminio suma ligereza visual y encaja bien en composiciones actuales." if bits["aluminio"] else ""
    color_note = " El acabado bicolor aporta contraste y ayuda a que la pieza tenga más presencia dentro del conjunto." if bits["bicolor"] else ""
    depth_note = "Si el fondo es generoso, revisa especialmente el paso delante del sofá y la distancia con mesa de centro o puertas cercanas."
    body = (
        p(
            f"<strong>Sofá de terraza de {plazas} plazas en estilo {style}, con medidas {size}, pensado para crear una zona lounge cómoda en exterior.</strong>{material_note}{color_note} Es una pieza principal para jardín, terraza o porche cuando quieres ordenar el descanso alrededor de un sofá y no de sillas sueltas."
        )
        + p(
            "Antes de comprar, mide ancho, fondo útil y recorrido alrededor. En exterior no basta con que el sofá quepa: también debe quedar espacio para sentarse, levantarse, limpiar y combinarlo con mesa baja, sillones, reposapiés o cojines sin saturar la zona."
        )
        + h2("Detalles clave")
        + ul(
            [
                f"<strong>Formato:</strong> sofá exterior de {plazas} plazas.",
                f"<strong>Medidas:</strong> {size}.",
                f"<strong>Estilo:</strong> {style}.",
                "<strong>Uso recomendado:</strong> terraza, jardín, porche, patio o ático.",
                "<strong>Mantenimiento:</strong> limpieza suave y textiles siempre secos antes de guardar o cubrir.",
            ]
        )
        + p(
            f"Elige este sofá si buscas una pieza de {plazas} plazas para hacer más confortable una zona exterior. {depth_note}"
        )
    )
    seo_parts = [f"Sofá terraza {plazas} plazas"]
    if bits["aluminio"]:
        seo_parts.append("aluminio")
    seo_parts.append(f"estilo {style}")
    seo = f"{' '.join(seo_parts)} de {size} para jardín, terraza o porche."
    return {"body": body, "seo": seo[:155]}


def set_payload(title):
    bits = title_bits(title)
    plazas = bits["plazas"]
    style = bits["style"]
    material_note = " La estructura de aluminio ayuda a mantener una imagen ligera y actual." if bits["aluminio"] else ""
    body = (
        p(
            f"<strong>Set de jardín de estilo {style} con sofá de {plazas} plazas, dos sillones y mesa, diseñado para resolver una zona de conversación exterior completa.</strong>{material_note} Es una opción útil para terraza, porche o jardín cuando quieres una composición coordinada sin escoger cada pieza por separado."
        )
        + p(
            "El sofá funciona como asiento principal, los sillones dan flexibilidad para recibir visitas y la mesa central permite apoyar bebidas, libros o aperitivos. Antes de comprar, marca la huella del conjunto en el suelo y comprueba que queda paso suficiente para sentarse, levantarse y limpiar sin moverlo todo."
        )
        + h2("Detalles clave")
        + ul(
            [
                f"<strong>Incluye:</strong> sofá de {plazas} plazas, dos sillones y mesa.",
                f"<strong>Estilo:</strong> {style}.",
                "<strong>Uso recomendado:</strong> terraza media o amplia, jardín, patio o porche.",
                "<strong>Ideal para:</strong> reuniones, descanso al aire libre y salón exterior.",
                "<strong>Consejo:</strong> revisa fondo útil, paso alrededor y apertura de puertas antes de colocarlo.",
            ]
        )
        + p(
            "Elige este set si quieres una solución completa para varias personas y una estética coherente desde el primer día. Si el espacio es estrecho, puede ser mejor combinar piezas sueltas o un sofá de menor tamaño."
        )
    )
    seo = f"Set jardín {style} con sofá {plazas} plazas, dos sillones y mesa para terraza, porche o jardín."
    return {"body": body, "seo": seo[:155]}


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


def payload_for(product):
    if product["productType"] == "Sofá":
        return sofa_payload(product["title"])
    if product["productType"] == "Conjunto sofá":
        return set_payload(product["title"])
    raise ValueError(f"Tipo no esperado: {product['productType']}")


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacio")

    backup = {}
    products = {}
    payloads = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - PDP rich batch 6 ({len(HANDLES)} fichas)\n")

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

        try:
            payload = payload_for(product)
        except Exception as exc:
            print(f"✗ {handle}: error generando texto ({exc})")
            errors += 1
            continue

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
    backup_path = os.path.join(backup_dir, f"backup_pdp_rich_batch6_{ts}.json")
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
