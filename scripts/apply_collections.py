#!/usr/bin/env python3
"""
Aplica intro + FAQ + SEO title + meta description a las 6 colecciones principales.
Backup previo + DRY-RUN por defecto.
  python3 scripts/apply_collections.py            # dry-run
  python3 scripts/apply_collections.py --apply     # aplica
"""
import json, os, sys, datetime, re, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv

GUIA = "/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico"

def faq(pairs):
    h = "<h2>Preguntas frecuentes</h2>"
    for q, a in pairs:
        h += f"<h3>{q}</h3><p>{a}</p>"
    return h

# handle -> (seo_title, meta_description, body_html)
C = {}

C["sillas-de-exterior"] = (
 "Sillas de exterior: aluminio, resina y apilables",
 "Sillas de exterior resistentes al sol y la lluvia para jardín, terraza y hostelería. En aluminio y resina, con o sin brazos y modelos apilables.",
 "<p><strong>Las sillas de exterior de Santavila están pensadas para resistir el sol, la lluvia y el uso diario en jardín, terraza, balcón y hostelería.</strong> Encontrarás modelos en <strong>aluminio</strong> —ligero y que no se oxida— y en <strong>resina</strong> de alta resistencia, fáciles de limpiar y muchos de ellos apilables para ganar espacio. Con o sin brazos y en acabados neutros que combinan con cualquier ambiente.</p>"
 + faq([
   ("¿Qué silla de exterior aguanta mejor la lluvia?", "El aluminio lacado y la resina son las opciones más resistentes a la lluvia: no se oxidan ni se deterioran con la humedad. La madera sin tratar es la menos recomendable a la intemperie."),
   ("¿Las sillas de exterior son apilables?", "Muchos de nuestros modelos de resina y aluminio son apilables, lo que facilita guardarlos y ganar espacio fuera de temporada. Lo indicamos en cada ficha de producto."),
   ("¿Mejor aluminio o resina?", f"El aluminio es más ligero, duradero y elegante; la resina es más económica y muy resistente al agua. Te lo explicamos en detalle en nuestra <a href=\"{GUIA}\">guía de materiales</a>."),
 ]))

C["sillones-de-exterior"] = (
 "Sofás de exterior de aluminio | 2 y 3 plazas y rinconeras",
 "Sofás y sillones de exterior en aluminio con cojines resistentes. Modelos de 2 y 3 plazas, rinconeras y conjuntos para jardín y terraza.",
 "<p><strong>Los sofás y sillones de exterior de Santavila convierten tu terraza o jardín en un salón al aire libre, con estructura de aluminio resistente a la intemperie y cojines de exterior.</strong> Elige entre <strong>sofás de 2 y 3 plazas</strong>, <strong>rinconeras de esquina</strong> y <strong>conjuntos completos</strong>. Si buscas por medida, empieza por el <a href=\"/products/sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm\">sofá terraza 120 cm</a> o el <a href=\"/products/sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm\">sofá exterior 130 cm</a>.</p>"
 + faq([
   ("¿Cuántas plazas necesito?", "Para un balcón o terraza pequeña, un sofá de 2 plazas es ideal; para un salón exterior amplio, elige un sofá de 3 plazas o una rinconera de esquina, que aprovecha mejor el espacio."),
   ("¿Los cojines resisten la intemperie?", "Los cojines son de tejido para exterior, preparados para el sol y la humedad. Aun así, recomendamos guardarlos secos fuera de temporada o usar una funda protectora para alargar su vida."),
   ("¿Qué estructura es más resistente?", "El aluminio es la mejor opción: no se oxida, es ligero y apenas necesita mantenimiento, por lo que aguanta perfectamente todo el año en exterior."),
 ]))

C["tumbonas"] = (
 "Tumbonas de exterior: aluminio y resina, reclinables",
 "Tumbonas de exterior para jardín y piscina en aluminio y resina. Modelos reclinables, con ruedas y resistentes al sol, la humedad y el cloro.",
 "<p><strong>Las tumbonas de exterior de Santavila están diseñadas para el descanso en el jardín y junto a la piscina, resistiendo el sol, la humedad y el cloro.</strong> Disponibles en <strong>aluminio</strong> y en <strong>resina</strong>, muchas con <strong>respaldo reclinable</strong> y <strong>ruedas integradas</strong>. Para comparar rápido, revisa la <a href=\"/products/balliu-tumbona-de-exterior-resina-28ff014d\">tumbona Balliu de resina</a>, la <a href=\"/products/balliu-tumbona-de-exterior-resina-75-cm-009e68e4\">tumbona de resina de 75 cm</a> y la <a href=\"/products/balliu-tumbona-de-exterior-aluminio-d08586c1\">tumbona de aluminio</a>.</p>"
 + faq([
   ("¿Tumbona de aluminio o de resina?", "El aluminio aporta un acabado más premium y ligereza; la resina es muy resistente, económica y fácil de limpiar. Ambas soportan bien la intemperie y el cloro de la piscina."),
   ("¿Las tumbonas se reclinan?", "Varios modelos incorporan respaldo reclinable en varias posiciones para ajustar la postura, y algunos llevan ruedas para desplazarlos con comodidad."),
   ("¿Aguantan el agua de la piscina?", "Sí. Tanto la resina como el aluminio lacado resisten el cloro y la humedad sin oxidarse ni deteriorarse, por lo que son ideales para zonas de piscina."),
 ]))

C["mesas"] = (
 "Mesas de exterior: extensibles, HPL y aluminio",
 "Mesas de exterior en aluminio con tablero HPL: de comedor, auxiliares, altas y extensibles. Resistentes al sol y el agua para jardín, terraza y hostelería.",
 "<p><strong>Las mesas de exterior de Santavila combinan estructura de aluminio que no se oxida con tablero HPL, un laminado de alta presión que resiste el sol, el agua y los arañazos sin perder color.</strong> Encontrarás <strong>mesas de comedor</strong>, <strong>auxiliares</strong>, <strong>altas</strong> y <strong>extensibles</strong>. Para una solución compacta de asiento y apoyo, mira también el <a href=\"/products/banco-jardin-con-mesa-integrada-220-cm\">banco de jardín con mesa incorporada</a>.</p>"
 + faq([
   ("¿Qué es el tablero HPL?", "El HPL (laminado de alta presión) es un material muy resistente al sol, el agua, el calor y los arañazos, ideal para exterior y uso intensivo. No se decolora ni se deforma con la humedad."),
   ("¿Qué medida de mesa según el número de comensales?", "Como orientación: una mesa de 120 cm acoge a unas 4 personas, una de 160-180 cm a 6, y las extensibles permiten pasar de uso diario a recibir invitados sin ocupar espacio de más."),
   ("¿Tenéis mesas extensibles?", "Sí, disponemos de mesas extensibles de aluminio con tablero HPL que amplían su longitud cuando necesitas más sitio, perfectas para comedores de jardín y hostelería."),
 ]))

C["parasoles"] = (
 "Parasoles de jardín y terraza: acrílico y aluminio",
 "Parasoles y sombrillas de exterior para jardín y terraza, con mástil de aluminio y tela acrílica o de poliéster. Distintos diámetros y colores.",
 "<p><strong>Los parasoles y sombrillas de Santavila te dan sombra de calidad en jardín, terraza y hostelería, con mástil de aluminio y tejidos preparados para el exterior.</strong> Elige entre <strong>tela acrílica</strong> —mayor resistencia al sol y a la decoloración— o <strong>poliéster</strong>, en varios diámetros. Recuerda añadir una <a href=\"/products/base-de-parasol-25-kg\">base de parasol de 25 kg</a>; si buscas sombra fija por medida, revisa la <a href=\"/products/pergola-aluminio-para-jardin-300300250-cm\">pérgola 250x300</a>.</p>"
 + faq([
   ("¿Tela acrílica o de poliéster?", "La tela acrílica resiste mejor el sol y conserva el color más tiempo, ideal si el parasol está muchas horas expuesto. El poliéster es una opción más económica con buena protección solar."),
   ("¿Necesito una base para el parasol?", "Sí. Para que aguante con seguridad necesitas una base acorde al diámetro del parasol; encontrarás <a href=\"/collections/accesorios\">bases y pies de parasol</a> en nuestra sección de accesorios."),
   ("¿Qué diámetro elijo?", "Un Ø200 cm cubre una mesa pequeña o un par de tumbonas; para una mesa de comedor o más sombra, elige Ø250 cm o superior."),
 ]))

C["accesorios"] = (
 "Accesorios de exterior: bases, cojines y fundas",
 "Accesorios para muebles de exterior: bases y pies de parasol, cojines, colchonetas y fundas protectoras resistentes al agua para jardín y terraza.",
 "<p><strong>Completa tus muebles de exterior con los accesorios de Santavila: bases y pies de parasol, cojines, colchonetas para tumbona y fundas protectoras.</strong> Piezas pensadas para aportar comodidad y para <strong>proteger y alargar la vida</strong> de tu mobiliario. Para estabilizar sombrillas, empieza por la <a href=\"/products/base-de-parasol-25-kg\">base para sombrilla de 25 kg</a>.</p>"
 + faq([
   ("¿Qué base de parasol necesito?", "Depende del diámetro del parasol y de la exposición al viento: como referencia, 25-30 kg para parasoles pequeños o protegidos y 40 kg o más para diámetros grandes o zonas con viento."),
   ("¿Las fundas protectoras son impermeables?", "Sí, están fabricadas en tejido resistente al agua que protege el mueble del sol, la lluvia y el polvo cuando no se usa, evitando la decoloración."),
   ("¿Los cojines y colchonetas son aptos para exterior?", "Sí, usan tejidos preparados para la intemperie. Aun así, para que duren más, recomendamos guardarlos secos fuera de temporada."),
 ]))

def gql(query, variables, attempts=3):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
            break
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)
    if "errors" in d: raise RuntimeError(d["errors"])
    return d["data"]

GET = """query($h:String!){ collectionByHandle(handle:$h){ id descriptionHtml seo{title description} } }"""
SET = """mutation($input:CollectionInput!){ collectionUpdate(input:$input){ collection{id handle} userErrors{field message} } }"""

def words(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())

def main():
    if not SHOPIFY_ACCESS_TOKEN: sys.exit("SHOPIFY_ACCESS_TOKEN vacío")
    print(f"{'APLICAR' if APPLY else 'DRY-RUN'} — {len(C)} colecciones\n")
    backup, errors = {}, 0
    for h, (stitle, meta, body) in C.items():
        try:
            col = gql(GET, {"h": h})["collectionByHandle"]
        except Exception as e:
            print(f"✗ {h}: error ({e})"); errors += 1; continue
        if not col:
            print(f"✗ {h}: no encontrada"); errors += 1; continue
        backup[h] = {"id": col["id"], "descriptionHtml": col["descriptionHtml"], "seo": col.get("seo")}
        print(f"• {h}: {words(col['descriptionHtml'])}→{words(body)} palabras + meta")
        if APPLY:
            inp = {"id": col["id"], "descriptionHtml": body, "seo": {"title": stitle, "description": meta}}
            res = gql(SET, {"input": inp})["collectionUpdate"]
            if res["userErrors"]: print(f"    ⚠️ {res['userErrors']}"); errors += 1
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = os.path.join(ROOT, "content", "descriptions", f"backup_collections_{ts}.json")
    os.makedirs(os.path.dirname(bpath), exist_ok=True)
    json.dump(backup, open(bpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n💾 Backup → {bpath}")
    print(f"{'✅ Aplicado' if APPLY else 'ℹ️ Dry-run'} · errores: {errors}")

if __name__ == "__main__":
    main()
