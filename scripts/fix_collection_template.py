#!/usr/bin/env python3
"""
Edita templates/collection.json del tema publicado (Dwell):
- Bloque de cabecera (intro): renderiza SOLO la parte previa a la FAQ.
- Nueva sección al final: renderiza la FAQ (lo posterior al <h2>Preguntas frecuentes</h2>).
Usa solo filtros Liquid (split) — sin tags. Hace BACKUP antes. DRY-RUN por defecto.
  .venv/bin/python scripts/fix_collection_template.py            # dry-run (muestra y guarda backup)
  .venv/bin/python scripts/fix_collection_template.py --apply     # escribe el tema
"""
import json, os, sys, copy, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
THEME = "188231123268"
SHOP = "mueblesexterior.myshopify.com"
KEY = "templates/collection.json"

def token():
    for line in open(os.path.join(ROOT, ".env.local"), encoding="utf-8"):
        if line.startswith("SHOPIFY_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("token .env.local no encontrado")

TOKEN = token()
SEP = "<h2>Preguntas frecuentes</h2>"
INTRO_LIQUID = "{{ closest.collection.description | split: '" + SEP + "' | first }}"
FAQ_LIQUID = "{{ closest.collection.description | split: '" + SEP + "' | last | prepend: '" + SEP + "' }}"

def api(method, body=None):
    url = f"https://{SHOP}/admin/api/2026-01/themes/{THEME}/assets.json"
    if method == "GET":
        url += "?asset%5Bkey%5D=" + urllib.parse.quote(KEY)
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} body: {e.read().decode()[:600]}")
        raise

import urllib.parse
asset = api("GET")["asset"]["value"]
tpl = json.loads(asset)

# Backup
bdir = os.path.join(ROOT, "content", "theme_backups"); os.makedirs(bdir, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
bpath = os.path.join(bdir, f"collection.json.{ts}.bak")
open(bpath, "w", encoding="utf-8").write(asset)
print(f"💾 Backup → {bpath}")

# 1) Intro: localizar el bloque de texto que NO es el título (contiene la descripción)
head = tpl["sections"]["section"]
intro_block_id = None
for bid, b in head.get("blocks", {}).items():
    txt = b.get("settings", {}).get("text", "")
    if "collection.title" not in txt:   # el que no es el H1
        intro_block_id = bid
if not intro_block_id:
    sys.exit("No encuentro el bloque de intro (solo está el título). Añádelo primero en el editor.")
print(f"Bloque intro detectado: {intro_block_id}")
head["blocks"][intro_block_id]["settings"]["text"] = INTRO_LIQUID

# 2) Nueva sección FAQ al final (clon de la cabecera, un bloque de texto con la FAQ)
faq_section = copy.deepcopy(head)
faq_block = copy.deepcopy(head["blocks"][intro_block_id])
faq_block["settings"]["text"] = FAQ_LIQUID
faq_section["blocks"] = {"faq_text": faq_block}
faq_section["block_order"] = ["faq_text"]
faq_section["name"] = "Collection FAQ"
faq_section["settings"]["padding-block-start"] = 40
faq_section["settings"]["padding-block-end"] = 40
faq_section["settings"]["horizontal_alignment"] = "center"
tpl["sections"]["faq"] = faq_section
if "faq" not in tpl["order"]:
    tpl["order"].append("faq")   # al final, tras 'main'

print("Orden de secciones resultante:", tpl["order"])
print("\nINTRO (arriba) →", INTRO_LIQUID)
print("FAQ (abajo)   →", FAQ_LIQUID)

if APPLY:
    api("PUT", {"asset": {"key": KEY, "value": json.dumps(tpl, ensure_ascii=False)}})
    print("\n✅ Plantilla actualizada en el tema publicado.")
else:
    print("\nℹ️ Dry-run. Ejecuta con --apply para escribir.")
