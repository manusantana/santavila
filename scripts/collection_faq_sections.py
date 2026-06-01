#!/usr/bin/env python3
"""
Mueve la FAQ de colección al final del listado, sin tocar el contenido (data):
- Crea 2 secciones liquid que parten collection.description por '<h2>Preguntas frecuentes</h2>'
  · sections/collection-intro.liquid  → intro (parte previa)
  · sections/collection-faq.liquid    → FAQ (parte posterior), renderizada tras el grid
- Edita templates/collection.json: quita el bloque de texto manual y añade ambas secciones
  en el orden: titulo → intro → grid → FAQ.
Backup antes. DRY-RUN salvo --apply.
"""
import json, os, sys, datetime, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
THEME = "188231123268"
SHOP = "mueblesexterior.myshopify.com"

def token():
    for line in open(os.path.join(ROOT, ".env.local"), encoding="utf-8"):
        if line.startswith("SHOPIFY_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("token .env.local no encontrado")
TOKEN = token()

def api(method, key, value=None):
    url = f"https://{SHOP}/admin/api/2026-01/themes/{THEME}/assets.json"
    body = None
    if method == "GET":
        url += "?asset%5Bkey%5D=" + urllib.parse.quote(key)
    else:
        body = json.dumps({"asset": {"key": key, "value": value}}).encode()
    req = urllib.request.Request(url, data=body, method=method,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:500]}"); raise

SEP = "<h2>Preguntas frecuentes</h2>"

INTRO_LIQUID = (
 "{%- assign _intro = collection.description | split: '" + SEP + "' | first -%}\n"
 "{%- if _intro != blank -%}\n"
 "  <div class=\"page-width\" style=\"max-width:760px;margin-inline:auto;text-align:center;padding-block:0 16px;\">\n"
 "    {{ _intro }}\n"
 "  </div>\n"
 "{%- endif -%}\n"
 "{% schema %}\n{\"name\":\"Collection intro\",\"settings\":[]}\n{% endschema %}\n"
)
FAQ_LIQUID = (
 "{%- assign _parts = collection.description | split: '" + SEP + "' -%}\n"
 "{%- if _parts.size > 1 -%}\n"
 "  <div class=\"page-width\" style=\"max-width:820px;margin-inline:auto;padding-block:40px;\">\n"
 "    " + SEP + "{{ _parts | last }}\n"
 "  </div>\n"
 "{%- endif -%}\n"
 "{% schema %}\n{\"name\":\"Collection FAQ\",\"settings\":[]}\n{% endschema %}\n"
)

# 1) Leer y respaldar el template
tpl_raw = api("GET", "templates/collection.json")["asset"]["value"]
bdir = os.path.join(ROOT, "content", "theme_backups"); os.makedirs(bdir, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
open(os.path.join(bdir, f"collection.json.{ts}.bak"), "w", encoding="utf-8").write(tpl_raw)
tpl = json.loads(tpl_raw)

# 2) Quitar el bloque de texto manual de la cabecera (el que no es el título)
head = tpl["sections"]["section"]
removed = []
for bid in list(head.get("blocks", {})):
    if "collection.title" not in head["blocks"][bid].get("settings", {}).get("text", ""):
        del head["blocks"][bid]
        removed.append(bid)
head["block_order"] = [b for b in head.get("block_order", []) if b not in removed]
print("Bloques manuales retirados de la cabecera:", removed)

# 3) Añadir las dos secciones nuevas y reordenar
tpl["sections"]["collection-intro"] = {"type": "collection-intro", "settings": {}}
tpl["sections"]["collection-faq"] = {"type": "collection-faq", "settings": {}}
new_order = []
for s in tpl["order"]:
    new_order.append(s)
    if s == "section":
        new_order.append("collection-intro")
    if s == "main":
        new_order.append("collection-faq")
# dedupe preservando orden
seen = set(); tpl["order"] = [x for x in new_order if not (x in seen or seen.add(x))]
print("Orden resultante:", tpl["order"])

if APPLY:
    # Crear primero las secciones liquid (deben existir antes de referenciarlas)
    api("PUT", "sections/collection-intro.liquid", INTRO_LIQUID)
    api("PUT", "sections/collection-faq.liquid", FAQ_LIQUID)
    print("✓ secciones liquid creadas")
    api("PUT", "templates/collection.json", json.dumps(tpl, ensure_ascii=False))
    print("✅ template actualizado: titulo → intro → grid → FAQ")
else:
    print("ℹ️ Dry-run. Backup guardado. Ejecuta con --apply.")
