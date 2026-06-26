#!/usr/bin/env python3
"""
Sprint GEO 2: crea/refuerza paginas de confianza comercial.

Dry-run por defecto:
  .venv/bin/python scripts/apply_trust_pages.py

Aplicar en Shopify:
  .venv/bin/python scripts/apply_trust_pages.py --apply
"""
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API_VERSION = "2026-01"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv


PAGES = {
    "sobre-santavila": {
        "title": "Sobre Santavila",
        "body_html": """
<p><strong>Santavila es una tienda española de mobiliario de exterior para terrazas, jardines, porches y espacios al aire libre que necesitan piezas bonitas, resistentes y fáciles de elegir.</strong></p>
<p>Seleccionamos muebles de exterior con una idea muy concreta: que una terraza pueda funcionar como un salón más de la casa. Por eso priorizamos materiales adecuados para clima español, medidas claras, fotografías útiles y asesoramiento humano antes de la compra.</p>
<h2>Qué seleccionamos</h2>
<ul>
  <li><strong>Sofás, sillones y rinconeras de exterior</strong> para crear zonas lounge completas.</li>
  <li><strong>Mesas, sillas y bancos</strong> para comedor exterior, jardín y porche.</li>
  <li><strong>Tumbonas, parasoles y accesorios</strong> para piscina, áticos y terrazas soleadas.</li>
</ul>
<h2>Cómo trabajamos</h2>
<p>Trabajamos con proveedores especializados en mobiliario de exterior, revisando materiales, medidas, uso recomendado y disponibilidad antes de publicar cada producto. Cuando una ficha no está clara, preferimos simplificarla y explicarla con lenguaje directo.</p>
<h2>Atención real</h2>
<p>Si tienes dudas sobre medidas, materiales, mantenimiento o composición de tu terraza, puedes escribirnos desde la <a href="/pages/contacto">página de contacto</a> o por email en <a href="mailto:hola@santavila.com">hola@santavila.com</a>. Respondemos con criterio práctico, no con respuestas automáticas.</p>
<h2>Para quién es Santavila</h2>
<p>Para quien quiere comprar muebles de exterior online en España con más tranquilidad: saber qué incluye cada set, qué material conviene para sol y lluvia, cómo mantenerlo y qué esperar de la entrega.</p>
""",
    },
    "envio": {
        "title": "Entrega y envío",
        "body_html": """
<p><strong>En Santavila trabajamos con entregas de mobiliario de exterior de gran volumen, por eso cada pedido se prepara según disponibilidad, tamaño del producto y destino.</strong></p>
<h2>Plazo orientativo</h2>
<p>La entrega estimada puede llegar hasta 30 días según disponibilidad del proveedor, volumen del pedido y ruta logística. En productos grandes o conjuntos completos, este margen nos permite coordinar transporte con más seguridad.</p>
<h2>Antes de comprar</h2>
<ul>
  <li>Revisa medidas del producto y acceso a tu vivienda, terraza o jardín.</li>
  <li>Comprueba si el embalaje puede entrar por portal, ascensor, escalera o puerta exterior.</li>
  <li>Si tienes una entrega compleja, escríbenos antes de comprar y revisamos el caso contigo.</li>
</ul>
<h2>Recepción del pedido</h2>
<p>Al recibir el pedido, revisa el estado de los bultos antes de firmar. Si ves golpes, roturas o señales claras de transporte, indícalo en el albarán y contacta con nosotros cuanto antes con fotografías.</p>
<h2>Montaje</h2>
<p>Muchos productos están pensados para montaje sencillo en casa con instrucciones. Si un producto necesita una consideración especial, lo indicaremos en la ficha o te lo confirmaremos durante la atención previa.</p>
<h2>Dudas de entrega</h2>
<p>Para preguntas sobre plazos, acceso, bultos o destino, contacta en <a href="mailto:hola@santavila.com">hola@santavila.com</a> o desde <a href="/pages/contacto">contacto</a>.</p>
""",
    },
    "garantia": {
        "title": "Garantía",
        "body_html": """
<p><strong>Todos los productos de Santavila cuentan con la garantía legal aplicable en España y la cobertura correspondiente frente a defectos de fabricación.</strong></p>
<h2>Qué cubre</h2>
<p>La garantía cubre defectos de fabricación o problemas de conformidad existentes en el producto, siempre que se haya usado de forma normal y siguiendo las indicaciones de cuidado y montaje.</p>
<h2>Qué no cubre</h2>
<ul>
  <li>Daños por uso inadecuado, golpes, montaje incorrecto o manipulación no indicada.</li>
  <li>Desgaste normal por uso exterior, exposición solar, humedad o limpieza agresiva.</li>
  <li>Daños causados por viento fuerte, temporales o falta de sujeción en parasoles y piezas ligeras.</li>
</ul>
<h2>Cómo gestionar una incidencia</h2>
<p>Escríbenos a <a href="mailto:hola@santavila.com">hola@santavila.com</a> con número de pedido, descripción del problema y fotografías claras. Revisaremos el caso y te indicaremos los siguientes pasos.</p>
<h2>Consejo práctico</h2>
<p>Guarda embalajes y documentación durante los primeros días tras la entrega. En incidencias de transporte o piezas dañadas, ayuda a resolver el caso con más rapidez.</p>
""",
    },
    "mantenimiento": {
        "title": "Cuidado y mantenimiento de muebles de exterior",
        "body_html": """
<p><strong>Un mueble de exterior dura más cuando se limpia con suavidad, se protege en episodios de viento o lluvia intensa y se guardan cojines y textiles cuando no se usan durante largos periodos.</strong></p>
<h2>Aluminio</h2>
<p>Limpia con agua, jabón neutro y un paño suave. Evita estropajos abrasivos o productos agresivos. El aluminio es ligero y no se oxida, pero conviene retirar salitre, polvo y restos orgánicos de forma periódica.</p>
<h2>Resina</h2>
<p>La resina es fácil de mantener: agua, jabón suave y aclarado. Para piscina o costa, limpia con más frecuencia para retirar cloro o sal. Evita fuentes de calor directo sobre la superficie.</p>
<h2>HPL</h2>
<p>El tablero HPL resiste muy bien el uso exterior. Limpia con paño húmedo y jabón neutro. Para manchas persistentes, actúa pronto y evita productos que puedan rayar el acabado.</p>
<h2>Cojines y textiles</h2>
<p>Aunque estén preparados para exterior, recomendamos guardarlos secos cuando no se usen durante varios días, especialmente fuera de temporada. No los guardes húmedos para evitar olores o moho.</p>
<h2>Parasoles y viento</h2>
<p>Cierra siempre el parasol con viento fuerte o cuando no estés en casa. Usa una base adecuada al diámetro y a la exposición del espacio.</p>
<h2>Antes de guardar</h2>
<ul>
  <li>Limpia y seca cada pieza.</li>
  <li>Revisa tornillos o uniones si el mueble se ha movido mucho.</li>
  <li>Usa funda transpirable cuando el mueble vaya a estar semanas sin uso.</li>
</ul>
<h2>Guías relacionadas</h2>
<p>Para una pauta más completa por temporada, consulta la guía <a href="/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada">cómo limpiar y mantener muebles de exterior</a>. Si estás eligiendo muebles nuevos y quieres priorizar resistencia, consulta también la guía <a href="/blogs/news/que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol">qué muebles de exterior aguantan mejor la lluvia y el sol</a>.</p>
""",
    },
}


def request(method, path, body=None, attempts=3):
    url = f"https://{SHOP}/admin/api/{API_VERSION}{path}"
    payload = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=payload,
        method=method,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        },
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                if response.status == 204:
                    return {}
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:800]
            raise RuntimeError(f"HTTP {exc.code} {method} {path}: {detail}") from exc
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)


def get_page(handle):
    data = request("GET", f"/pages.json?handle={urllib.parse.quote(handle)}")
    pages = data.get("pages", [])
    return pages[0] if pages else None


def compact_page(page):
    if not page:
        return None
    return {
        "id": page.get("id"),
        "handle": page.get("handle"),
        "title": page.get("title"),
        "body_html": page.get("body_html"),
        "published_at": page.get("published_at"),
        "updated_at": page.get("updated_at"),
    }


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacío")

    backup = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - {len(PAGES)} páginas de confianza\n")

    for handle, payload in PAGES.items():
        try:
            current = get_page(handle)
        except Exception as exc:
            print(f"✗ {handle}: error leyendo ({exc})")
            errors += 1
            continue

        backup[handle] = compact_page(current)
        action = "update" if current else "create"
        print(f"• {handle}: {action}")
        print(f"  title: {payload['title']}")
        print(f"  words: {len(payload['body_html'].split())}")

        if not APPLY:
            continue

        page_payload = {
            "title": payload["title"],
            "handle": handle,
            "body_html": payload["body_html"].strip(),
            "published": True,
        }
        try:
            if current:
                request("PUT", f"/pages/{current['id']}.json", {"page": {"id": current["id"], **page_payload}})
            else:
                request("POST", "/pages.json", {"page": page_payload})
        except Exception as exc:
            print(f"  ⚠️ {exc}")
            errors += 1

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(ROOT, "content", "descriptions", f"backup_trust_pages_{ts}.json")
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)

    print(f"\nBackup -> {backup_path}")
    print(f"{'Aplicado' if APPLY else 'Dry-run'} · errores: {errors}")


if __name__ == "__main__":
    main()
