#!/usr/bin/env python3
"""
Añade JSON-LD FAQPage a los artículos del blog (solo schema, sin HTML visible),
parseando article.content por '<h2>Preguntas frecuentes</h2>'. Crea la sección
sections/article-faq-schema.liquid y la añade a templates/article.json. Backup + --apply.
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
        print(f"HTTP {e.code}: {e.read().decode()[:400]}"); raise

SECTION = r"""{%- assign _parts = article.content | split: '<h2>Preguntas frecuentes</h2>' -%}
{%- if _parts.size > 1 -%}
  {%- assign _faq = _parts | last -%}
  {%- assign _items = _faq | split: '<h3>' -%}
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{%- assign _first = true -%}{%- for _it in _items -%}{%- if _it contains '</h3>' -%}{%- assign _q = _it | split: '</h3>' | first | strip_html | strip -%}{%- assign _a = _it | split: '</h3>' | last | split: '<p>' | last | split: '</p>' | first | strip_html | strip -%}{%- unless _first %},{% endunless -%}{%- assign _first = false -%}{"@type":"Question","name":{{ _q | json }},"acceptedAnswer":{"@type":"Answer","text":{{ _a | json }}}}{%- endif -%}{%- endfor -%}]}
  </script>
{%- endif -%}
{% schema %}
{"name":"Article FAQ schema","settings":[]}
{% endschema %}
"""

# Backup + editar template
tpl_raw = api("GET", "templates/article.json")["asset"]["value"]
bdir = os.path.join(ROOT, "content", "theme_backups"); os.makedirs(bdir, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
open(os.path.join(bdir, f"article.json.{ts}.bak"), "w", encoding="utf-8").write(tpl_raw)
tpl = json.loads(tpl_raw)
tpl["sections"]["article-faq"] = {"type": "article-faq-schema", "settings": {}}
if "article-faq" not in tpl["order"]:
    tpl["order"].append("article-faq")
print("Orden resultante:", tpl["order"])

if APPLY:
    api("PUT", "sections/article-faq-schema.liquid", SECTION)
    api("PUT", "templates/article.json", json.dumps(tpl, ensure_ascii=False))
    print("✅ Sección creada y añadida a la plantilla de artículo.")
else:
    print("ℹ️ Dry-run. Backup guardado. --apply para escribir.")
