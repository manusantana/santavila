#!/usr/bin/env python3
"""
Optimiza los 6 posts del blog 'news':
- Los 6: SEO title (global.title_tag) + meta description (global.description_tag) + autor real.
- Post de materiales: además, cuerpo ampliado (~900 palabras, tabla + FAQ).
Backup previo. DRY-RUN salvo --apply.
"""
import json, os, sys, re, datetime, urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
AUTHOR = "Equipo Santavila"
GQL = f"https://{SHOP}/admin/api/2026-01/graphql.json"

def gql(q):
    req = urllib.request.Request(GQL, data=json.dumps({"query": q}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    return json.load(urllib.request.urlopen(req, timeout=40))

def rest(method, path, payload=None):
    url = f"https://{SHOP}/admin/api/2026-01/{path}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:400]}"); raise

MATERIALS_BODY = """<p><strong>¿Qué material de muebles de exterior dura más? En resumen: la teca es el más longevo (décadas) pero el más caro y exige aceitado; el aluminio es el de mejor relación resistencia-mantenimiento y no se oxida; y el ratán sintético sobre estructura de aluminio es el más cómodo y equilibrado para una terraza mediterránea.</strong> Elegir el material equivocado puede obligarte a cambiar los muebles en dos o tres temporadas; el correcto dura años casi sin cuidados. Abajo lo comparamos en lo que de verdad importa: clima, mantenimiento, peso y presupuesto.</p>
<h2>Tabla comparativa: aluminio vs. teca vs. ratán sintético</h2>
<table>
  <thead><tr><th>Criterio</th><th>Aluminio</th><th>Teca</th><th>Ratán sintético (PE)</th></tr></thead>
  <tbody>
    <tr><td>Resistencia a lluvia/humedad</td><td>Muy alta (no se oxida)</td><td>Muy alta (aceites naturales)</td><td>Alta (fibra impermeable)</td></tr>
    <tr><td>Resistencia al sol/UV</td><td>Alta (puede calentarse)</td><td>Alta (vira a gris si no se trata)</td><td>Alta si es PE de calidad</td></tr>
    <tr><td>Mantenimiento</td><td>Mínimo</td><td>Medio-alto (aceite de teca)</td><td>Bajo</td></tr>
    <tr><td>Peso</td><td>Muy ligero</td><td>Pesado</td><td>Ligero</td></tr>
    <tr><td>Durabilidad</td><td>10-20 años</td><td>20-40 años</td><td>8-15 años</td></tr>
    <tr><td>Precio</td><td>€€</td><td>€€€€</td><td>€€-€€€</td></tr>
  </tbody>
</table>
<h2>¿Es mejor el aluminio para muebles de exterior?</h2>
<p>El aluminio es la opción más equilibrada para la mayoría de terrazas y jardines. No se oxida, es muy ligero (se mueve y se guarda con facilidad) y apenas necesita mantenimiento: basta un paño húmedo. Su acabado lacado permite colores duraderos. El único matiz es que, a pleno sol, la superficie metálica puede calentarse, algo que se resuelve con cojines o textileno. Es la base estructural de gran parte de nuestro <a href="/collections/sillas-de-exterior">catálogo de sillas</a> y <a href="/collections/sillones-de-exterior">sofás de exterior</a>.</p>
<h2>¿Merece la pena la teca para exterior?</h2>
<p>La teca es la madera noble por excelencia para intemperie: sus aceites naturales la hacen muy resistente a la humedad y los insectos, y bien cuidada dura décadas. A cambio, es la opción más cara y la que más mantenimiento pide: si quieres conservar su tono dorado hay que aplicar aceite de teca una o dos veces al año; si la dejas envejecer, adquiere una pátina gris plateada igualmente protegida. Ideal si buscas calidez natural y una inversión a muy largo plazo.</p>
<h2>¿Qué es el ratán sintético y cómo se comporta?</h2>
<p>El ratán sintético es fibra de polietileno (PE) tejida sobre una estructura de aluminio. A diferencia del ratán natural, es impermeable y resistente a los rayos UV, así que aguanta a la intemperie sin pudrirse. Aporta la estética mediterránea del trenzado con un mantenimiento bajo y mucha comodidad al combinarse con cojines. La clave de calidad está en que la fibra sea PE (no PVC) y la estructura de aluminio: así evitas decoloración y óxido. Lo encontrarás en buena parte de nuestras <a href="/collections/tumbonas">tumbonas</a> y conjuntos.</p>
<h2>¿Cuál elegir según tu caso?</h2>
<ul>
  <li><strong>Quieres olvidarte del mantenimiento:</strong> aluminio.</li>
  <li><strong>Buscas calidez natural y una inversión para décadas:</strong> teca.</li>
  <li><strong>Priorizas confort y estética mediterránea con poco cuidado:</strong> ratán sintético sobre aluminio.</li>
  <li><strong>Vives cerca del mar:</strong> aluminio lacado o ratán sintético de PE (la teca aguanta, pero el aluminio sin tratar de baja calidad puede sufrir; elige lacados de calidad).</li>
  <li><strong>Necesitas mover los muebles a menudo:</strong> aluminio o ratán sintético (ligeros).</li>
</ul>
<p>¿Tienes claro el material pero no la pieza? Explora nuestras <a href="/collections/mesas">mesas</a>, <a href="/collections/tumbonas">tumbonas</a> y <a href="/collections/parasoles">parasoles</a>, o escríbenos desde la <a href="/pages/contacto">página de contacto</a> y te asesoramos.</p>
<h2>Preguntas frecuentes</h2>
<h3>¿Qué material de muebles de exterior aguanta mejor la lluvia?</h3>
<p>La teca y el aluminio son los que mejor resisten la lluvia: la teca por sus aceites naturales y el aluminio porque no se oxida. El ratán sintético de PE también es impermeable; el ratán natural, en cambio, no debe quedar expuesto a la lluvia.</p>
<h3>¿Aluminio o ratán sintético para una terraza a pleno sol?</h3>
<p>Ambos resisten bien el sol. El aluminio puede calentarse en la superficie metálica, así que conviene usar cojines o textileno; el ratán sintético de calidad (PE) no se decolora y resulta más fresco al tacto. Para sol intenso, prioriza acabados con protección UV.</p>
<h3>¿La teca necesita mantenimiento?</h3>
<p>Sí, si quieres mantener su tono dorado: aplica aceite de teca una o dos veces al año. Si prefieres no hacer nada, la teca envejece hasta un gris plateado natural que sigue protegiendo la madera. En ningún caso se pudre con facilidad.</p>
<h3>¿Cuál es el mejor material si vivo cerca del mar?</h3>
<p>El aluminio lacado de calidad y el ratán sintético de PE son las mejores opciones en ambientes salinos, porque no se oxidan ni se degradan con la humedad. La teca también aguanta muy bien el clima costero.</p>"""

# handle -> {title, meta, body(optional)}
POSTS = {
 "como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico": {
   "title": "Aluminio, teca o ratán: qué muebles de exterior duran más",
   "meta": "Comparamos aluminio, teca y ratán sintético para muebles de exterior: resistencia, mantenimiento y cuál elegir según tu terraza, clima y presupuesto.",
   "body": MATERIALS_BODY,
 },
 "guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada": {
   "title": "Cómo limpiar y mantener muebles de exterior por temporada",
   "meta": "Guía de mantenimiento de muebles de exterior: cómo limpiar aluminio, madera, resina y cojines y prepararlos para cada temporada para que duren más.",
 },
 "5-ideas-para-decorar-tu-terraza-este-verano-del-estilo-mediterraneo-al-diseno-minimalista": {
   "title": "5 ideas para decorar tu terraza este verano",
   "meta": "5 ideas para decorar tu terraza, del estilo mediterráneo al minimalista: muebles, textiles y distribución para crear un exterior bonito y funcional.",
 },
 "muebles-de-exterior-para-hosteleria-que-buscar-y-por-que-la-calidad-marca-la-diferencia": {
   "title": "Muebles de exterior para hostelería: qué buscar",
   "meta": "Cómo elegir muebles de exterior para hostelería: resistencia, materiales y mantenimiento, y por qué la calidad marca la diferencia en terrazas de bares y restaurantes.",
 },
 "tendencias-en-muebles-de-exterior-para-2025-materiales-colores-y-disenos-que-marcan-el-ano": {
   "title": "Tendencias en muebles de exterior 2026: materiales y colores",
   "meta": "Tendencias en muebles de exterior 2026: materiales sostenibles, tonos tierra, formas orgánicas y diseño que difumina interior y exterior. Inspírate para tu terraza.",
 },
 "como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales": {
   "title": "Cómo amueblar una terraza pequeña: muebles y trucos",
   "meta": "Cómo aprovechar al máximo una terraza pequeña: muebles, distribución y trucos visuales para ganar espacio y crear una zona exterior cómoda y bonita.",
 },
}

def num(gid): return gid.split("/")[-1]

# Mapear handle -> (blog_num, article_num, body_actual)
data = gql("{ blogs(first:5){ nodes{ id handle articles(first:50){ nodes{ id handle body } } } } }")
idx = {}
for b in data["data"]["blogs"]["nodes"]:
    for a in b["articles"]["nodes"]:
        idx[a["handle"]] = (num(b["id"]), num(a["id"]), a["body"])

backup = {}
print(f"{'APLICAR' if APPLY else 'DRY-RUN'} — {len(POSTS)} posts (autor: {AUTHOR})\n")
for handle, p in POSTS.items():
    if handle not in idx:
        print(f"✗ {handle}: no encontrado"); continue
    blog_id, art_id, cur_body = idx[handle]
    backup[handle] = {"article_id": art_id, "body": cur_body}
    w_old = len(re.sub(r"<[^>]+>", " ", cur_body or "").split())
    art = {"id": int(art_id), "author": AUTHOR, "metafields": [
        {"namespace": "global", "key": "title_tag", "value": p["title"], "type": "single_line_text_field"},
        {"namespace": "global", "key": "description_tag", "value": p["meta"], "type": "single_line_text_field"},
    ]}
    note = "SEO+autor"
    if "body" in p:
        art["body_html"] = p["body"]
        w_new = len(re.sub(r"<[^>]+>", " ", p["body"]).split())
        note = f"SEO+autor+cuerpo {w_old}→{w_new}p"
    print(f"• {handle[:45]:<45} [{note}]")
    if APPLY:
        res = rest("PUT", f"blogs/{blog_id}/articles/{art_id}.json", {"article": art})
        if "article" not in res:
            print(f"   ⚠️ respuesta inesperada: {str(res)[:200]}")

# Backup
bdir = os.path.join(ROOT, "content", "descriptions"); os.makedirs(bdir, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
json.dump(backup, open(os.path.join(bdir, f"backup_blog_{ts}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n💾 Backup de cuerpos actuales guardado ({ts})")
print("✅ Aplicado" if APPLY else "ℹ️ Dry-run. Ejecuta con --apply.")
