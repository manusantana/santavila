#!/usr/bin/env python3
"""Guia GEO: ¿Parasol o pergola? (cierra el cluster de sombra; delta 2026-08-16).

Crea el articulo OCULTO y lo programa para lunes 2026-08-18 10:00 Madrid.
Dry-run por defecto; --apply para crear+programar.
"""

import base64
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN  # noqa: E402
from upload_images import gql  # noqa: E402

SHOP = "mueblesexterior.myshopify.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
PUBLISH_AT_UTC = "2026-08-18T08:00:00Z"

HANDLE = "parasol-o-pergola-que-sombra-te-conviene"
TITLE = "¿Parasol o pérgola? Qué sombra te conviene"
SUMMARY = "Comparativa práctica entre parasol y pérgola: superficie de sombra, movilidad, anclaje, viento y coste, con los casos en los que conviene cada uno."
META_TITLE = "¿Parasol o pérgola? Qué sombra te conviene"
META_DESC = "Parasol o pérgola: cuánta sombra da cada uno, qué pide su instalación, cómo se llevan con el viento y en qué casos conviene cada opción."

PDP_PERGOLA = "/products/pergola-aluminio-para-jardin-300300250-cm"
G_PERGOLA = "/blogs/news/pergola-de-aluminio-medidas-altura-y-cuanta-sombra-da"
G_BASES = "/blogs/news/base-de-parasol-que-peso-necesitas-y-como-elegirla"
G_CHILL = "/blogs/news/como-montar-un-chill-out-en-la-terraza-ideas-y-medidas"
COL_PARASOLES = "/collections/parasoles"

BODY = f"""
<p><strong>En corto: elige parasol si necesitas sombra flexible —moverla con el sol, guardarla en invierno o no puedes anclar nada al suelo—, y pérgola si la zona tiene un uso fijo y diario, como el comedor o el salón de exterior, y puedes anclarla.</strong> El parasol es la sombra que se adapta; la pérgola, la que convierte un rincón en habitación.</p>

<h2>Comparativa rápida</h2>
<table>
  <thead>
    <tr><th></th><th>Parasol</th><th>Pérgola</th></tr>
  </thead>
  <tbody>
    <tr><td>Superficie de sombra</td><td>Según diámetro: de Ø200 a Ø300 cm</td><td>Mayor y constante: una 300×300 cm cubre ~9 m²</td></tr>
    <tr><td>Movilidad</td><td>Total: se mueve, se cierra, se guarda</td><td>Ninguna: es una estructura fija</td></tr>
    <tr><td>Instalación</td><td>Base con peso adecuado, sin obra</td><td>Anclaje a suelo firme según fabricante</td></tr>
    <tr><td>Con viento</td><td>Se cierra siempre que no estés</td><td>Estructura anclada; el textil se recoge con rachas</td></tr>
    <tr><td>Invierno</td><td>Se guarda o se enfunda</td><td>Se queda montada (aluminio sin problema)</td></tr>
    <tr><td>Inversión inicial</td><td>Menor</td><td>Mayor, pensada a años vista</td></tr>
  </tbody>
</table>

<h2>Cuándo conviene un parasol</h2>
<p>El <a href="{COL_PARASOLES}">parasol</a> gana cuando la sombra tiene que adaptarse a ti: <strong>balcones y terrazas pequeñas</strong> donde una estructura fija se comería el espacio, zonas de <strong>piscina</strong> donde el sol se persigue a lo largo del día, viviendas de <strong>alquiler</strong> donde no puedes anclar nada, o simplemente cuando quieres resolver la sombra con la menor inversión. Su único requisito serio es la base: revisa la <a href="{G_BASES}">guía de pesos de base de parasol</a>, porque un parasol grande con base corta es el clásico susto de agosto.</p>

<h2>Cuándo conviene una pérgola</h2>
<p>La pérgola compensa cuando la zona tiene <strong>uso fijo y diario</strong>: el comedor de exterior donde se come cada día, el salón donde cae la sobremesa. Define el espacio, da sombra constante sobre más metros y no hay que abrirla ni cerrarla. A cambio pide <strong>anclaje a suelo firme</strong> y quedarse donde la montas. Las medidas, la altura y lo que cabe debajo lo tienes al detalle en la <a href="{G_PERGOLA}">guía de la pérgola de aluminio</a>, y el modelo de referencia es nuestra <a href="{PDP_PERGOLA}">pérgola de 300×300×250 cm</a>.</p>

<h2>La combinación que mejor funciona</h2>
<p>En jardines con más de una zona, la respuesta no suele ser una u otra, sino ambas: <strong>pérgola sobre el comedor</strong> (uso fijo, sombra constante) y <strong>parasol móvil</strong> para la zona de tumbonas o la piscina (sombra que sigue al sol). Si estás componiendo la zona entera, la <a href="{G_CHILL}">guía del chill out</a> te ayuda a decidir qué va debajo de cada sombra.</p>

<h2>Los errores que vemos más</h2>
<p>Tres clásicos fáciles de evitar: un <strong>parasol grande con base pequeña</strong> (el diámetro manda sobre los kilos), una <strong>pérgola sin anclar</strong> "de momento" (una racha la convierte en vela), y elegir pérgola en un espacio que aún no tiene uso definido — ahí es mejor empezar con parasol y decidir con la terraza ya vivida.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Qué da más sombra, un parasol o una pérgola?</h3>
<p>A igualdad de metros, la pérgola: una 300×300 cm proyecta unos 9 m² constantes, mientras que un parasol grande de Ø300 cm ronda los 7 m² y su sombra se desplaza con el sol. La ventaja del parasol es que puedes mover esa sombra donde haga falta.</p>
<h3>¿Qué aguanta mejor el viento?</h3>
<p>Ninguno "aguanta" sin precauciones: el parasol se cierra siempre que no estés delante, y la pérgola debe estar anclada y con el textil recogido en rachas fuertes. La diferencia es que la pérgola bien anclada no depende de que te acuerdes.</p>
<h3>¿Puedo poner una pérgola en un balcón?</h3>
<p>En general no es su sitio: pide anclaje, altura libre y una huella que pocos balcones tienen. Para balcón, la respuesta práctica es un parasol con la base adecuada o un toldo (que ya es tema de comunidad de vecinos).</p>
<h3>¿Cuál sale más barato?</h3>
<p>El parasol requiere menos inversión inicial y crece por piezas (parasol + base). La pérgola es una compra mayor pensada a años vista: se amortiza cuando la zona se usa a diario, no como extra ocasional.</p>
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
    if rest("GET", f"blogs/{blog_id}/articles.json?handle={HANDLE}")["articles"]:
        raise SystemExit("ya existe, aborto")
    art = {
        "title": TITLE, "handle": HANDLE, "author": "Equipo Santavila",
        "body_html": BODY.strip(), "summary_html": f"<p>{SUMMARY}</p>",
        "published": False,
        "tags": "GEO, guía de compra, parasoles, pérgolas, sombra",
        "metafields": [
            {"namespace": "global", "key": "title_tag", "value": META_TITLE, "type": "single_line_text_field"},
            {"namespace": "global", "key": "description_tag", "value": META_DESC, "type": "single_line_text_field"},
        ],
    }
    created = rest("POST", f"blogs/{blog_id}/articles.json", {"article": art})["article"]
    print("creado id", created["id"])
    att = base64.b64encode(open(os.path.join(ROOT, "images_generated/parasol_roma/03_bajo_el_parasol.jpg"), "rb").read()).decode()
    rest("PUT", f"blogs/{blog_id}/articles/{created['id']}.json", {"article": {
        "id": created["id"],
        "image": {"attachment": att, "alt": "Vista bajo un parasol de aluminio en una terraza de piedra frente al mar"}}})
    print("imagen destacada OK")
    res = gql('''mutation($id: ID!, $article: ArticleUpdateInput!){
      articleUpdate(id: $id, article: $article){ article{ isPublished publishedAt } userErrors{ field message } } }''',
      {"id": f"gid://shopify/Article/{created['id']}", "article": {"isPublished": False, "publishDate": PUBLISH_AT_UTC}})["articleUpdate"]
    if res["userErrors"]:
        raise SystemExit(res["userErrors"])
    print("programado ->", res["article"]["publishedAt"])


if __name__ == "__main__":
    main()
