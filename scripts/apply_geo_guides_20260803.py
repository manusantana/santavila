#!/usr/bin/env python3
"""Guias GEO agosto 2026: bases de parasol (cluster GSC) + chill out (trendy B2C).

Mismo patron que apply_geo_guides.py (REST articles + metafields title/description,
FAQ separada por '<h2>Preguntas frecuentes</h2>' para el schema FAQPage del tema).

Dry-run por defecto; --apply para publicar.
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

SHOP = "mueblesexterior.myshopify.com"
API_VERSION = "2026-01"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
AUTHOR = "Equipo Santavila"
BLOG_HANDLE = "news"

FAQ_SEP = "<h2>Preguntas frecuentes</h2>"

GUIDES = {
    "base-de-parasol-que-peso-necesitas-y-como-elegirla": {
        "title": "Base de parasol: qué peso necesitas y cómo elegirla",
        "summary": "Guía para elegir base de parasol o sombrilla: peso orientativo según diámetro, bases de cemento y losas, tubo compatible y qué hacer con el viento.",
        "meta_title": "Base de parasol: qué peso necesitas (25, 40 kg o losas)",
        "meta_description": "Cuántos kilos necesita la base según el diámetro del parasol, cuándo usar losas de cemento, cómo comprobar el tubo compatible y qué hacer con viento.",
        "body_html": """
<p><strong>Como referencia rápida: para un parasol de mástil central de unos 2 metros en una terraza protegida, una base de unos 25 kg suele ser suficiente; a partir de Ø250-300 cm conviene subir de peso, y un parasol excéntrico pide mucho más lastre, normalmente en forma de losas sobre su cruceta.</strong> Son valores orientativos: revisa siempre la recomendación del fabricante de tu parasol y la exposición al viento de tu terraza.</p>

<h2>Cuántos kilos necesita la base según el parasol</h2>
<table>
  <thead>
    <tr><th>Parasol</th><th>Peso orientativo de la base</th><th>Observaciones</th></tr>
  </thead>
  <tbody>
    <tr><td>Mástil central hasta Ø200 cm</td><td>Desde 25 kg</td><td>Terraza o balcón protegido del viento</td></tr>
    <tr><td>Mástil central Ø250-300 cm</td><td>40 kg o más</td><td>Cuanta más tela, más «vela» hace el parasol</td></tr>
    <tr><td>Excéntrico (brazo lateral)</td><td>Losas de lastre sobre la cruceta</td><td>El brazo multiplica la palanca: necesita mucho más peso</td></tr>
    <tr><td>Cualquiera en zona ventosa</td><td>Sube un escalón de peso</td><td>Y cierra el parasol siempre que no estés</td></tr>
  </tbody>
</table>
<p>La lógica es sencilla: la base trabaja contra la palanca que hace la tela con el viento. Un parasol grande abierto es una vela, y un excéntrico además desplaza todo ese empuje fuera del punto de apoyo. Por eso una <a href="/products/base-de-parasol-25-kg">base de parasol de 25 kg</a> va bien para un parasol central de terraza, mientras que un excéntrico se asegura con un <a href="/products/set-losas-cemento-para-base-de-parasol">set de losas de cemento</a> colocado sobre su cruceta.</p>

<h2>Tipos de base: cemento, losas y bases con relleno</h2>
<p>Las <strong>bases macizas de cemento u hormigón</strong> son las más habituales: peso constante, sin mantenimiento y estabilidad inmediata. Las <strong>losas de lastre</strong> se usan sobre la cruceta de los parasoles excéntricos y permiten sumar peso por módulos. Existen también bases <strong>rellenables de agua o arena</strong>, más ligeras de transportar, aunque su peso final suele ser menor que el de una base maciza equivalente.</p>
<p>Si te estás planteando <strong>hacer una base de cemento casera</strong>, ten en cuenta lo que suele fallar: el peso queda mal repartido, no hay protección para el suelo ni para el tubo, y moverla se convierte en un problema. Una base fabricada reparte el peso, sujeta el mástil con apriete regulable y suele incluir protección para no rayar el suelo — por lo que cuesta, rara vez compensa el bricolaje.</p>

<h2>Comprueba el tubo: que el mástil encaje de verdad</h2>
<p>Antes de comprar, mira dos datos: el <strong>diámetro del mástil</strong> de tu parasol y el <strong>rango de diámetros que admite la base</strong> (muchas incluyen casquillos reductores o apriete regulable). Un mástil que baila dentro de la base desgasta el tubo y resta estabilidad; uno que no entra, directamente no sirve. Encontrarás ambos datos en la ficha de cada producto.</p>

<h2>Viento: la regla que evita sustos</h2>
<p>Ninguna base sustituye a la prudencia: <strong>cierra el parasol cuando no estés y siempre que haya rachas</strong>. La mayoría de daños no ocurren con el parasol en uso, sino abierto y sin vigilancia. Fuera de temporada, guarda el parasol seco o protégelo con funda, y revisa el apriete del mástil al inicio de cada temporada. Tienes la pauta completa en la <a href="/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada">guía de mantenimiento por temporada</a>.</p>

<h2>Y el parasol, ¿cuál?</h2>
<p>Si todavía estás eligiendo parasol, en la colección de <a href="/collections/parasoles">parasoles de exterior</a> tienes desde modelos de terraza de Ø200 cm hasta parasoles de aluminio de Ø300 cm como el <a href="/products/balliu-parasol-para-terraza-aluminio-300-cm-3b7e77d1">Garbí</a>. Cuanto mayor el diámetro, más sombra — y más base necesitarás.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Vale una base de 25 kg para un parasol de 3 metros?</h3>
<p>Como norma general, no: a partir de Ø250-300 cm conviene una base de 40 kg o más, y en zonas con viento, subir otro escalón. La base de 25 kg está pensada para parasoles de mástil central de terraza en torno a los 2 metros.</p>
<h3>¿Qué base necesita un parasol excéntrico?</h3>
<p>Los excéntricos no se sujetan bien con una base central clásica: el brazo lateral hace mucha palanca. Lo habitual es lastrarlos con losas de cemento colocadas sobre su cruceta, sumando los kilos que indique el fabricante.</p>
<h3>¿Mejor base maciza o rellenable de agua/arena?</h3>
<p>La maciza de cemento da peso constante y no requiere nada; la rellenable es más cómoda de transportar, pero suele alcanzar menos peso real. Para uso fijo en terraza, la maciza es la opción más despreocupada.</p>
<h3>¿Cómo evito que el parasol se mueva o gire en la base?</h3>
<p>Comprueba que el diámetro del mástil encaja en el rango de la base y usa el apriete o los casquillos reductores incluidos. Un mástil bien apretado no gira ni traquetea con la brisa.</p>
""",
    },
    "como-montar-un-chill-out-en-la-terraza-ideas-y-medidas": {
        "title": "Cómo montar un chill out en la terraza: ideas, muebles y medidas",
        "summary": "Guía práctica para crear una zona chill out en terraza o jardín: qué pieza principal elegir (sofá, set o cama balinesa), medidas reales, sombra y mantenimiento.",
        "meta_title": "Chill out en la terraza: ideas, muebles y medidas",
        "meta_description": "Cómo crear un chill out en tu terraza: sofá, set de jardín o cama balinesa, medidas y paso libre, mesa de centro, sombra con parasol o pérgola y cuidados.",
        "body_html": """
<p><strong>Para montar un chill out que se use de verdad, empieza por el espacio: mide la zona y el paso libre, elige una sola pieza protagonista —sofá, set de jardín o cama balinesa—, acompáñala de una mesa baja y resuelve la sombra.</strong> Es mejor una composición contenida y cómoda que llenar la terraza de piezas que luego estorban.</p>

<h2>1. Mide antes de enamorarte</h2>
<p>Marca en el suelo la huella de la pieza que te gusta y comprueba que sigues pasando con comodidad: como referencia, deja al menos 60-70 cm de paso libre en las zonas de circulación. Si la terraza es pequeña o es un balcón, te ayudará la <a href="/blogs/news/como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales">guía para amueblar una terraza pequeña</a> antes de decidir.</p>

<h2>2. La pieza protagonista</h2>
<p><strong>Sofá o conjunto de sofá.</strong> Es la opción más versátil. Un <a href="/collections/sillones-de-exterior">sofá de exterior</a> de 2 plazas funciona desde unos 120 cm de ancho; si tienes sitio, un <a href="/products/set-jardin-aluminio-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa">set de jardín con sofá de 3 plazas, dos sillones y mesa</a> resuelve la zona entera de una vez, con estructura de aluminio que aguanta a la intemperie.</p>
<p><strong>Cama balinesa.</strong> Si buscas el efecto «resort», la cama balinesa es la pieza con más presencia: una superficie amplia para tumbarse a la sombra de su propio techo de tela. En catálogo tienes la <a href="/products/balliu-cama-balinesa-exterior-aluminio-estilo-sofisticado-160-cm-2bd3a7a4">balinesa de aluminio de 160 cm</a> y la <a href="/products/balliu-cama-balinesa-exterior-aluminio-estilo-minimalista-198-cm-dcaf71d8">minimalista de 198 cm</a>. Eso sí: exige espacio real — mide la huella completa antes.</p>
<p><strong>Rincón de siesta.</strong> Si el hueco es alargado (junto a piscina o en un lateral), un par de <a href="/collections/tumbonas">tumbonas</a> con una mesa auxiliar entre ambas crea un chill out lineal con menos fondo que un sofá.</p>

<h2>3. La mesa: baja y a mano</h2>
<p>Un chill out sin superficie de apoyo se queda cojo. Una <a href="/collections/mesas">mesa de centro de exterior</a> a la altura del asiento (35-45 cm) es la medida natural para vasos, libros y bandejas; si el espacio es mínimo, una mesa auxiliar pequeña junto al reposabrazos cumple la misma función ocupando la mitad.</p>

<h2>4. La sombra decide cuántas horas lo usas</h2>
<p>Sin sombra, el chill out se usa al amanecer y de noche; con ella, todo el día. Las dos vías sin obra son el <strong>parasol</strong> —flexible y que puedes cerrar y mover; calcula bien su <a href="/blogs/news/base-de-parasol-que-peso-necesitas-y-como-elegirla">base según el diámetro</a>— y la <strong>pérgola de aluminio</strong>, como la de <a href="/products/pergola-aluminio-para-jardin-300300250-cm">300×300 cm y 250 cm de altura</a>, que define la «habitación exterior» de forma estable. La cama balinesa trae su propia sombra de serie.</p>

<h2>5. Que aguante fuera todo el año</h2>
<p>Para no rehacer la inversión cada verano, prioriza estructuras de <strong>aluminio</strong> (no se oxida y pesa poco) y tejidos técnicos de exterior, y dales el cuidado mínimo: cojines secos y guardados fuera de temporada, limpieza suave y nada de fundas sobre muebles húmedos. La pauta corta está en la <a href="/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada">guía de mantenimiento</a> y la comparativa de materiales en la <a href="/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico">guía de materiales</a>.</p>

<h2>Tres composiciones que funcionan</h2>
<table>
  <thead>
    <tr><th>Espacio</th><th>Composición</th><th>Claves</th></tr>
  </thead>
  <tbody>
    <tr><td>Balcón o terraza compacta</td><td>Sofá 2 plazas + mesa auxiliar</td><td>Piezas ligeras, paso libre de 60-70 cm</td></tr>
    <tr><td>Terraza mediana</td><td>Set de jardín (sofá + 2 sillones + mesa) + parasol</td><td>Todo resuelto en una compra, sombra móvil</td></tr>
    <tr><td>Jardín o zona de piscina</td><td>Cama balinesa o 2 tumbonas + mesa auxiliar</td><td>Efecto resort, sombra propia o pérgola</td></tr>
  </tbody>
</table>

<h2>Preguntas frecuentes</h2>
<h3>¿Cuánto espacio necesito para un chill out?</h3>
<p>Con unos 2×2 metros ya montas un rincón con sofá de 2 plazas y mesa auxiliar. Un set completo con sofá de 3 plazas y sillones pide en torno a 3×3 metros, y una cama balinesa necesita su huella más espacio de acceso alrededor.</p>
<h3>¿Sofá, set de jardín o cama balinesa?</h3>
<p>Sofá si quieres flexibilidad y poco fondo; set de jardín si prefieres la zona resuelta de una vez con asientos para varias personas; balinesa si el objetivo es tumbarse y crear un punto focal tipo resort y tienes espacio de sobra.</p>
<h3>¿Qué muebles pueden quedarse fuera todo el año?</h3>
<p>Las estructuras de aluminio con tejidos técnicos de exterior aguantan la intemperie sin oxidarse. Los cojines, mejor guardarlos secos fuera de temporada o protegerlos con funda, siempre sobre el mueble limpio y seco.</p>
<h3>¿Cómo doy sombra sin hacer obra?</h3>
<p>Parasol con la base adecuada a su diámetro (flexible y desmontable) o pérgola de aluminio anclada (estable y definitiva, sin albañilería mayor). La cama balinesa incorpora su propio techo de tela.</p>
""",
    },
}


def request(method, path, payload=None):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/{path}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def get_blog_id():
    return request("GET", f"blogs.json?handle={BLOG_HANDLE}")["blogs"][0]["id"]


def get_article(blog_id, handle):
    arts = request("GET", f"blogs/{blog_id}/articles.json?handle={urllib.parse.quote(handle)}")["articles"]
    return arts[0] if arts else None


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())


def main():
    blog_id = get_blog_id()
    backup = {}
    print("APLICAR" if APPLY else "DRY-RUN")
    for handle, g in GUIDES.items():
        current = get_article(blog_id, handle)
        backup[handle] = current
        print(f"• {handle}: {'update' if current else 'create'} · {words(g['body_html'])} palabras")
        assert FAQ_SEP in g["body_html"], "falta separador FAQ"
        if not APPLY:
            continue
        article = {
            "title": g["title"],
            "handle": handle,
            "author": AUTHOR,
            "body_html": g["body_html"].strip(),
            "summary_html": f"<p>{g['summary']}</p>",
            "published": True,
            "tags": "GEO, guía de compra, chill out, parasoles",
            "metafields": [
                {"namespace": "global", "key": "title_tag", "value": g["meta_title"], "type": "single_line_text_field"},
                {"namespace": "global", "key": "description_tag", "value": g["meta_description"], "type": "single_line_text_field"},
            ],
        }
        if current:
            article["id"] = current["id"]
            request("PUT", f"blogs/{blog_id}/articles/{current['id']}.json", {"article": article})
        else:
            request("POST", f"blogs/{blog_id}/articles.json", {"article": article})
        print("  publicado")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = os.path.join(ROOT, "content", "descriptions", f"backup_guias_{ts}.json")
    json.dump(backup, open(bpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("💾", bpath)


if __name__ == "__main__":
    main()
