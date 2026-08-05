#!/usr/bin/env python3
"""PDP 2.0 batch 10 (2026-08-05): amplia las 10 fichas de 80-119 palabras con mas
señales GSC (fuente: content/descriptions/fichas_80_119_con_senales_20260805.json).

A diferencia de tandas anteriores NO reescribe: INSERTA 1-2 parrafos a medida
(uso real + enlace interno a guia/coleccion/hub) antes de la "Ficha técnica",
o al final si no la hay. Dry-run por defecto; --apply para aplicar.
"""

import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from upload_images import gql  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv

G_TUMBONAS = "/blogs/news/tumbona-de-aluminio-resina-o-madera-cual-elegir-para-exterior"
G_MESAS = "/blogs/news/como-elegir-mesa-de-exterior-medidas-comensales-y-espacio-necesario"
G_MANT = "/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada"
G_TERRAZA = "/blogs/news/como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales"
G_BASES = "/blogs/news/base-de-parasol-que-peso-necesitas-y-como-elegirla"
HUB = "/collections/tumbonas-de-resina"

EXTRAS = {
    "balliu-tumbona-de-exterior-resina-75-cm-aca076ae": (
        "<p>Con sus 75 cm de ancho, la Lola ofrece más superficie de descanso que una tumbona "
        "estándar, y su resina aguanta cloro, salitre y sol directo, por lo que rinde igual junto "
        "a la piscina que en zonas de playa. Si dudas entre materiales, revisa la "
        f"<a href=\"{G_TUMBONAS}\">guía de tumbonas por material</a> o compara todos los modelos "
        f"en la colección de <a href=\"{HUB}\">tumbonas de resina</a>.</p>"
    ),
    "balliu-mesa-exterior-140-18090-cm-e4ec7d7c": (
        "<p>La Atlanta pasa de mesa de diario a mesa de invitados sin mover nada más que su "
        "extensión, algo que en terrazas ajustadas evita tener una mesa grande ocupando sitio "
        "todo el año. Antes de decidir formato, comprueba comensales y paso libre alrededor con "
        f"la <a href=\"{G_MESAS}\">guía de medidas de mesa de exterior</a>.</p>"
    ),
    "balliu-mesa-exterior-resina-70-cm-33ce1613": (
        "<p>El tablero Werzalit no absorbe agua ni se decolora con el sol, y su formato compacto "
        "—redondo o cuadrado— encaja en balcones y terrazas pequeñas donde una mesa grande no "
        f"cabe. Si el espacio es justo, la <a href=\"{G_TERRAZA}\">guía para amueblar una terraza "
        "pequeña</a> te ayuda a elegir medida sin saturar el paso.</p>"
    ),
    "balliu-mesa-auxiliar-exterior-resina-48-cm-35554775": (
        "<p>Colocada junto a una tumbona resuelve el apoyo de bebida, libro y protector solar sin "
        "estorbar el paso, y al ser apilable se recoge en segundos al final del día. Es el "
        f"complemento natural de la línea Eva Pro de la colección de <a href=\"{HUB}\">tumbonas "
        "de resina</a>.</p>"
    ),
    "balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e": (
        "<p>Su altura de mesa de centro la sitúa a la medida natural frente a un sofá de "
        "exterior, y el HPL admite vasos fríos, salpicaduras y limpieza con paño húmedo sin "
        "resentirse. Si estás montando la zona completa, tienes los sofás y conjuntos en la "
        "colección de <a href=\"/collections/sillones-de-exterior\">sofás de exterior</a>.</p>"
    ),
    "balliu-tumbona-de-exterior-con-ruedas-aluminio-58-cm-9064b7b9": (
        "<p>Pesa poco y rueda: la Iris está pensada para perseguir el sol alrededor de la "
        "piscina sin esfuerzo y guardarse igual de rápido. El textil seca en minutos y se "
        "sustituye por guías cuando toque renovarlo. Para comparar aluminio frente a resina, "
        f"mira la <a href=\"{G_TUMBONAS}\">guía de tumbonas por material</a>.</p>"
    ),
    "balliu-mini-tumbona-de-exterior-madera-59-cm-fa211c70": (
        "<p>Plegada apenas ocupa, así que es de las pocas tumbonas que caben en un balcón y se "
        "guardan en un armario en invierno. La madera pide un cuidado mínimo pero constante: "
        f"tienes la pauta por temporada en la <a href=\"{G_MANT}\">guía de mantenimiento</a> y "
        f"más ideas de aprovechamiento en la <a href=\"{G_TERRAZA}\">guía de terrazas pequeñas</a>.</p>"
    ),
    "balliu-mesa-exterior-hpl-140-180100-cm-8e073aab": (
        "<p>Con 100 cm de fondo, la Java deja sitio real para fuentes y bandejas en el centro de "
        "la mesa, algo que se agradece en comidas largas de verano. Repasa cuántos comensales "
        f"caben de verdad y el paso alrededor en la <a href=\"{G_MESAS}\">guía de mesas de "
        "exterior</a>.</p>"
    ),
    "set-rinconera-exterior-hpl-elegante-sofa-de-esquina-mesa-de-centro": (
        "<p>La composición en L aprovecha la esquina y libera el centro de la terraza, así que "
        "es una de las formas más eficientes de sentar a varias personas en poco espacio. "
        f"Complétala con un parasol bien lastrado —la <a href=\"{G_BASES}\">guía de bases de "
        "parasol</a> te dice qué peso necesitas— y la zona queda resuelta.</p>"
    ),
    "balliu-mesa-auxiliar-exterior-resina-48-cm-de421a42": (
        "<p>Sus 48×48 cm caben entre dos tumbonas sin cortar el paso, y el acabado texturizado "
        "en mate disimula bien el uso intensivo y la limpieza frecuente. Va a juego con la línea "
        f"Eva Pro de la colección de <a href=\"{HUB}\">tumbonas de resina</a>.</p>"
    ),
}

GET = """query($h:String!){ productByHandle(handle:$h){ id handle descriptionHtml } }"""
SET = """mutation($input: ProductInput!){ productUpdate(input: $input){
  product{ id } userErrors{ field message } } }"""


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())


def insert_extra(html, extra):
    idx = html.find("Ficha técnica")
    if idx == -1:
        return html.rstrip() + extra
    tag_start = html.rfind("<", 0, idx)
    if tag_start == -1:
        tag_start = idx
    return html[:tag_start] + extra + html[tag_start:]


def main():
    backup = {}
    print("APLICAR" if APPLY else "DRY-RUN")
    for handle, extra in EXTRAS.items():
        p = gql(GET, {"h": handle})["productByHandle"]
        if not p:
            print(f"✗ {handle}: no encontrado")
            continue
        if extra[:80] in p["descriptionHtml"]:
            print(f"• {handle}: ya ampliada, salto")
            continue
        backup[handle] = {"id": p["id"], "descriptionHtml": p["descriptionHtml"]}
        new_html = insert_extra(p["descriptionHtml"], extra)
        print(f"• {handle}: {words(p['descriptionHtml'])} -> {words(new_html)} palabras")
        if APPLY:
            res = gql(SET, {"input": {"id": p["id"], "descriptionHtml": new_html}})["productUpdate"]
            if res["userErrors"]:
                print(f"  ⚠️ {res['userErrors']}")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = os.path.join(ROOT, "content", "descriptions", f"backup_pdp_batch10_{ts}.json")
    json.dump(backup, open(bpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("💾", bpath)
    print("✅ Aplicado" if APPLY else "ℹ️ Dry-run (nada tocado)")


if __name__ == "__main__":
    main()
