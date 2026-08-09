#!/usr/bin/env python3
"""Guia GEO: pergola de aluminio (striking distance 'pergola 250x300', pos 13,9).

Crea el articulo OCULTO y lo programa para el lunes 2026-08-11 10:00 Madrid via
GraphQL publishDate (el REST published_at coerciona fechas futuras a 'ahora').

Dry-run por defecto; --apply para crear+programar.
"""

import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN  # noqa: E402
from upload_images import gql  # noqa: E402

SHOP = "mueblesexterior.myshopify.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
PUBLISH_AT_UTC = "2026-08-11T08:00:00Z"  # 10:00 Europe/Madrid

HANDLE = "pergola-de-aluminio-medidas-altura-y-cuanta-sombra-da"
TITLE = "Pérgola de aluminio: medidas, altura y cuánta sombra da"
SUMMARY = "Guía para elegir pérgola de aluminio: qué cabe bajo una 300×300 cm, por qué importan los 250 cm de altura, anclaje, viento y cuándo conviene frente al parasol."
META_TITLE = "Pérgola de aluminio: medidas, altura y sombra"
META_DESC = "Qué cabe bajo una pérgola de 300×300 cm, por qué importan los 250 cm de altura, cómo plantear el anclaje y cuándo elegir pérgola o parasol."

PDP = "/products/pergola-aluminio-para-jardin-300300250-cm"
G_CHILL = "/blogs/news/como-montar-un-chill-out-en-la-terraza-ideas-y-medidas"
G_BASES = "/blogs/news/base-de-parasol-que-peso-necesitas-y-como-elegirla"
G_MAT = "/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico"
G_MESAS = "/blogs/news/como-elegir-mesa-de-exterior-medidas-comensales-y-espacio-necesario"

BODY = f"""
<p><strong>Una pérgola de 300×300 cm cubre unos 9 m² de sombra: espacio para un comedor de seis, una zona de sofá con sillones o un par de tumbonas con paso alrededor. Los 250 cm de altura dan circulación cómoda y sensación de amplitud, y la estructura de aluminio aguanta a la intemperie con un mantenimiento mínimo.</strong> La clave antes de comprar no es el catálogo: es marcar la huella en tu suelo y comprobar el anclaje.</p>

<h2>¿Qué cabe bajo una pérgola de 300×300 cm?</h2>
<table>
  <thead>
    <tr><th>Uso</th><th>¿Cabe bien?</th><th>Observaciones</th></tr>
  </thead>
  <tbody>
    <tr><td>Comedor para 6</td><td>Sí</td><td>Mesa de 140-180 cm con sillas y paso; revisa medidas en la <a href="{G_MESAS}">guía de mesas</a></td></tr>
    <tr><td>Zona de sofá</td><td>Sí</td><td>Sofá de 3 plazas + 2 sillones + mesa de centro, el clásico chill out</td></tr>
    <tr><td>Dos tumbonas</td><td>Sí</td><td>Con mesa auxiliar entre ambas y paso libre</td></tr>
    <tr><td>Comedor para 8-10</td><td>Justo</td><td>La mesa cabe, pero el paso alrededor queda apretado: valora dejar parte fuera</td></tr>
  </tbody>
</table>
<p>La regla práctica de siempre: <strong>marca los 3×3 metros en el suelo</strong> (cinta o tiza) y comprueba que sigues circulando con 60-70 cm de paso libre por donde te mueves a diario, especialmente junto a pared, barandilla o piscina.</p>

<h2>La altura: por qué importan los 250 cm</h2>
<p>Una pérgola baja agobia y una demasiado alta pierde intimidad y protege peor del sol rasante. Los <strong>250 cm de altura</strong> son un punto de equilibrio: paso holgado bajo la estructura, aire para que el calor no se acumule y proporción correcta con muebles de exterior estándar. Si vas a colgar algo (una lámpara portátil, textiles), descuenta su vuelo de esa altura.</p>

<h2>Aluminio: la estructura que menos pide</h2>
<p>En exterior real —sol fuerte, lluvia, cambios de temperatura— el aluminio combina tres cosas difíciles de juntar: <strong>ligereza, resistencia a la corrosión y mantenimiento casi nulo</strong> (agua y jabón). La madera exige tratamiento periódico y el acero mal protegido acaba marcando óxido en el suelo. Tienes la comparativa completa en la <a href="{G_MAT}">guía de materiales de exterior</a>.</p>

<h2>Anclaje y viento: lo que decide que dure</h2>
<p>Una pérgola es una vela grande: <strong>ánclala siempre a suelo firme siguiendo las instrucciones del fabricante</strong>, y no la des por instalada hasta que las cuatro patas estén fijadas. Si el modelo lleva techo textil, recógelo con rachas fuertes y en invierno, igual que harías con un parasol. Y si tu terraza no admite anclaje, quizá tu sombra sea móvil: mira la <a href="{G_BASES}">guía de bases de parasol</a>.</p>

<h2>¿Pérgola o parasol?</h2>
<p>En corto: la <strong>pérgola</strong> define una habitación exterior fija, estable y con más superficie de sombra; el <strong>parasol</strong> es flexible, se mueve siguiendo el sol y se guarda en un armario. Si la zona tiene un uso claro y diario (comedor, salón exterior), la pérgola gana; si el uso cambia o no puedes anclar, empieza por un <a href="/collections/parasoles">parasol</a> bien lastrado.</p>

<h2>Bajo la pérgola: la zona completa</h2>
<p>Nuestra <a href="{PDP}">pérgola de aluminio de 300×300×250 cm</a> está pensada justo para eso: fijar la zona de sombra sobre el comedor o el salón de exterior. Para componer lo que va debajo —pieza principal, mesa y textiles— tienes el paso a paso en la <a href="{G_CHILL}">guía del chill out</a>.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Cuánta sombra da una pérgola de 300×300 cm?</h3>
<p>Unos 9 m² en proyección vertical. A primera y última hora, con el sol bajo, la sombra se desplaza: si buscas sombra a una hora concreta, oriéntala pensando en ese momento del día.</p>
<h3>¿Necesita obra la instalación?</h3>
<p>No necesita obra mayor, pero sí anclaje a suelo firme según las instrucciones del fabricante. Es un montaje en casa metódico: mejor entre dos personas y comprobando la huella y los puntos de fijación antes de empezar.</p>
<h3>¿Puede quedarse fuera todo el año?</h3>
<p>La estructura de aluminio, sí: resiste lluvia y sol sin oxidarse. Los elementos textiles conviene recogerlos con rachas fuertes y fuera de temporada, siempre limpios y secos.</p>
<h3>¿Qué mantenimiento tiene?</h3>
<p>Mínimo: limpieza con agua y jabón suave, revisión del apriete de la tornillería al inicio de temporada y los cuidados básicos de cualquier mueble de exterior que recogemos en la <a href="/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada">guía de mantenimiento</a>.</p>
"""


def rest(method, path, payload=None):
    req = urllib.request.Request(f"https://{SHOP}/admin/api/2026-01/{path}",
        data=json.dumps(payload).encode() if payload else None, method=method,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    return json.load(urllib.request.urlopen(req, timeout=120))


def main():
    words = len(re.sub(r"<[^>]+>", " ", BODY).split())
    print(("APLICAR" if APPLY else "DRY-RUN"), "·", HANDLE, "·", words, "palabras")
    assert "<h2>Preguntas frecuentes</h2>" in BODY
    if not APPLY:
        return
    blog_id = rest("GET", "blogs.json?handle=news")["blogs"][0]["id"]
    existing = rest("GET", f"blogs/{blog_id}/articles.json?handle={HANDLE}")["articles"]
    if existing:
        raise SystemExit("ya existe, aborto (usar update manual)")
    art = {
        "title": TITLE, "handle": HANDLE, "author": "Equipo Santavila",
        "body_html": BODY.strip(), "summary_html": f"<p>{SUMMARY}</p>",
        "published": False,
        "tags": "GEO, guía de compra, pérgolas, sombra",
        "metafields": [
            {"namespace": "global", "key": "title_tag", "value": META_TITLE, "type": "single_line_text_field"},
            {"namespace": "global", "key": "description_tag", "value": META_DESC, "type": "single_line_text_field"},
        ],
    }
    created = rest("POST", f"blogs/{blog_id}/articles.json", {"article": art})["article"]
    print("creado id", created["id"])

    # imagen destacada
    import base64
    att = base64.b64encode(open(os.path.join(ROOT, "images_generated/pergola/02_ambiente_jardin.jpg"), "rb").read()).decode()
    rest("PUT", f"blogs/{blog_id}/articles/{created['id']}.json", {"article": {
        "id": created["id"],
        "image": {"attachment": att, "alt": "Pérgola de aluminio blanca con techo de lona en un jardín encalado"}}})
    print("imagen destacada OK")

    # programar publicacion (GraphQL publishDate)
    res = gql('''mutation($id: ID!, $article: ArticleUpdateInput!){
      articleUpdate(id: $id, article: $article){ article{ isPublished publishedAt } userErrors{ field message } } }''',
      {"id": f"gid://shopify/Article/{created['id']}", "article": {"isPublished": False, "publishDate": PUBLISH_AT_UTC}})["articleUpdate"]
    if res["userErrors"]:
        raise SystemExit(res["userErrors"])
    print("programado ->", res["article"]["publishedAt"])


if __name__ == "__main__":
    main()
