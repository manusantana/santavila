#!/usr/bin/env python3
"""
Reescribe sections/collection-faq.liquid para que, además de la FAQ visible,
emita JSON-LD FAQPage (parseando <h3>pregunta</h3><p>respuesta</p>).
Backup de la sección actual antes. DRY-RUN salvo --apply.
"""
import json, os, sys, datetime, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
THEME = "188231123268"
SHOP = "mueblesexterior.myshopify.com"
KEY = "sections/collection-faq.liquid"

def token():
    for line in open(os.path.join(ROOT, ".env.local"), encoding="utf-8"):
        if line.startswith("SHOPIFY_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("token .env.local no encontrado")
TOKEN = token()

def api(method, value=None):
    url = f"https://{SHOP}/admin/api/2026-01/themes/{THEME}/assets.json"
    body = None
    if method == "GET":
        url += "?asset%5Bkey%5D=" + urllib.parse.quote(KEY)
    else:
        body = json.dumps({"asset": {"key": KEY, "value": value}}).encode()
    req = urllib.request.Request(url, data=body, method=method,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:500]}"); raise

NEW = r"""{%- assign _parts = collection.description | split: '<h2>Preguntas frecuentes</h2>' -%}
{%- if _parts.size > 1 -%}
  {%- assign _faq = _parts | last -%}
  <div class="page-width" style="max-width:820px;margin-inline:auto;padding-block:40px;">
    <h2>Preguntas frecuentes</h2>{{ _faq }}
  </div>
  {%- assign _items = _faq | split: '<h3>' -%}
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{%- assign _first = true -%}{%- for _it in _items -%}{%- if _it contains '</h3>' -%}{%- assign _q = _it | split: '</h3>' | first | strip_html | strip -%}{%- assign _a = _it | split: '</h3>' | last | split: '<p>' | last | split: '</p>' | first | strip_html | strip -%}{%- unless _first %},{% endunless -%}{%- assign _first = false -%}{"@type":"Question","name":{{ _q | json }},"acceptedAnswer":{"@type":"Answer","text":{{ _a | json }}}}{%- endif -%}{%- endfor -%}]}
  </script>
{%- endif -%}
{% schema %}
{"name":"Collection FAQ","settings":[]}
{% endschema %}
"""

cur = api("GET")["asset"]["value"]
bdir = os.path.join(ROOT, "content", "theme_backups"); os.makedirs(bdir, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
open(os.path.join(bdir, f"collection-faq.liquid.{ts}.bak"), "w", encoding="utf-8").write(cur)
print(f"💾 Backup de la sección actual guardado ({ts})")

if APPLY:
    api("PUT", NEW)
    print("✅ collection-faq.liquid actualizado con JSON-LD FAQPage")
else:
    print("ℹ️ Dry-run. Contenido nuevo:\n")
    print(NEW)
