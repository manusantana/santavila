#!/usr/bin/env python3
"""Refactor de nombres Familias 1 (Parasoles) y 2 (Tumbonas)
   Aplicar regla Opción C + Modelo (introducida en sub-piloto 3d).
   También pasa a DRAFT 4 productos legacy sin modelo metafield.
"""
import os, json, time, urllib.request, sys, re
from pathlib import Path

env = {}
ROOT = Path("/Users/manusantanameneses/Documents/Workspace/Santavila")
for line in open(ROOT / '.env.local'):
    line=line.strip()
    if '=' in line and not line.startswith('#'):
        k,v=line.split('=',1); env[k]=v.strip().strip('"').strip("'")
TOKEN = env['SHOPIFY_ACCESS_TOKEN']
URL = 'https://mueblesexterior.myshopify.com/admin/api/2026-01/graphql.json'
def gql(q,v=None):
    for a in range(5):
        try:
            req=urllib.request.Request(URL,data=json.dumps({'query':q,'variables':v or {}}).encode(),
              headers={'X-Shopify-Access-Token':TOKEN,'Content-Type':'application/json'})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read())
                if d.get('errors'):
                    raise RuntimeError(json.dumps(d['errors'], ensure_ascii=False))
                return d['data']
        except Exception as e:
            if a == 4: raise
            time.sleep(1.5*(a+1))

# Mapeo handle → nuevo título
RENAMES = [
    # ─── PARASOLES (8) ───
    ("balliu-parasol-para-terraza-aluminio-300-cm-0ceba8e7",
     "Parasol cuadrado exterior · aluminio 300×300 cm · Brisa"),
    ("balliu-parasol-para-terraza-acrilico-236bd5f0",
     "Parasol exterior acrílico · Ø200 cm · Pamela acrílico"),
    ("balliu-parasol-para-terraza-82e48b2d",
     "Parasol exterior tela · Ø200 cm · Pamela tela"),
    ("balliu-parasol-para-terraza-acrilico-c8dd492d",
     "Parasol exterior acrílico · Ø200/Ø250 cm · Ocean acrílico"),
    ("balliu-parasol-para-terraza-f1ed8b8b",
     "Parasol exterior tela · Ø200/Ø250 cm · Ocean tela"),
    ("parasol-cuadrado-200x200",
     "Parasol cuadrado exterior · aluminio 200×200 cm · Ágora"),
    ("balliu-parasol-para-terraza-aluminio-300-cm-6c1e1224",
     "Parasol lateral exterior · aluminio 300×300 cm · Roma"),
    ("balliu-parasol-para-terraza-aluminio-300-cm-3b7e77d1",
     "Parasol redondo exterior · aluminio Ø300 cm · Garbí"),

    # ─── TUMBONAS / MINI / COLCHONETA (16) ───
    ("balliu-colchoneta-para-tumbona-0e9a3256",
     "Colchoneta exterior para tumbona"),
    ("balliu-mini-tumbona-de-exterior-aluminio-57-cm-98ab84ce",
     "Mini tumbona exterior aluminio apilable · 57 cm · Marina"),
    ("balliu-mini-tumbona-de-exterior-aluminio-62-cm-5a6f53eb",
     "Mini tumbona exterior aluminio plegable · 62 cm · Cannes"),
    ("balliu-mini-tumbona-de-exterior-madera-59-cm-fa211c70",
     "Mini tumbona exterior madera teca plegable · 59 cm · Bristol"),
    ("balliu-tumbona-de-exterior-aluminio-d08586c1",
     "Tumbona exterior aluminio alta · acceso fácil · Etna Alta"),
    ("balliu-tumbona-de-exterior-aluminio-68-cm-f7ab4da8",
     "Tumbona exterior aluminio apilable · 68 cm · Marina"),
    ("balliu-tumbona-de-exterior-con-ruedas-aluminio-58-cm-9064b7b9",
     "Tumbona exterior aluminio · con ruedas 58 cm · Iris"),
    ("balliu-tumbona-de-exterior-aluminio-36870d09",
     "Tumbona exterior aluminio · Etna"),
    ("balliu-tumbona-de-exterior-sin-ruedas-aluminio-da3f5c24",
     "Tumbona exterior aluminio · con/sin ruedas · Olimpia"),
    ("balliu-tumbona-de-exterior-resina-73-cm-0648657b",
     "Tumbona exterior resina jardín · 73 cm tablillas · Eva RTG"),
    ("balliu-tumbona-de-exterior-resina-73-cm-d369d964",
     "Tumbona exterior resina playa · 73 cm tela · Eva RG"),
    ("balliu-tumbona-de-exterior-resina-28ff014d",
     "Tumbona exterior resina · Noa"),
    ("tumbona-carmen-tablillas",
     "Tumbona exterior resina · 75 cm tablillas · Carmen T"),
    ("balliu-tumbona-de-exterior-resina-75-cm-009e68e4",
     "Tumbona exterior resina · 75 cm tela · Carmen"),
    ("tumbona-lola-tablillas",
     "Tumbona exterior resina playa · 75 cm tablillas · Lola T"),
    ("balliu-tumbona-de-exterior-resina-75-cm-aca076ae",
     "Tumbona exterior resina playa · 75 cm tela · Lola"),
    ("balliu-tumbona-de-exterior-resina-923110d9",
     "Tumbona exterior resina · Ø73 cm tablillas · Eva Pro T"),
    ("balliu-tumbona-de-exterior-resina-b19af1ea",
     "Tumbona exterior resina · Ø73 cm tela · Eva Pro"),
]

# Legacy a DRAFT (sin metafield modelo)
DRAFTS_LEGACY = [
    "parasol-para-terraza-300-cm",
    "parasol-para-terraza-300-cm-2",
    "parasol-para-terraza-350-cm",
    "tumbona-de-exterior",
]

DRY = "--apply" not in sys.argv
print("════ MODO DRY-RUN ════\n" if DRY else "════ MODO APPLY ════\n")

# Backup
if not DRY:
    bk = ROOT / "backups" / f"refactor_nombres_{time.strftime('%Y%m%d-%H%M%S')}.json"
    bk.parent.mkdir(exist_ok=True)
    snap = []
    for h, _ in RENAMES + [(h2, '') for h2 in DRAFTS_LEGACY]:
        try:
            r = gql('query($h:String!){productByHandle(handle:$h){id handle title status tags}}',{"h":h})
            if r.get('productByHandle'): snap.append(r['productByHandle'])
        except Exception as e: print(f"   ✗ backup {h}: {e}")
    bk.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
    print(f"📦 Backup: {bk.name}  ({len(snap)} productos)\n")

# Rename
print(f"─── Refactor de {len(RENAMES)} nombres ───")
results = []
for h, new_title in RENAMES:
    r = gql('query($h:String!){productByHandle(handle:$h){id title}}', {"h": h})
    p = r.get('productByHandle')
    if not p:
        print(f"  ✗ {h}  NO ENCONTRADO"); continue
    if p['title'] == new_title:
        print(f"  · {h}  ya tiene el título correcto"); continue
    print(f"  {h}")
    print(f"     antes:  {p['title']!r}")
    print(f"     nuevo:  {new_title!r}")
    if DRY:
        results.append((h, "DRY", new_title)); continue
    u = gql('mutation($input:ProductInput!){productUpdate(input:$input){product{id title} userErrors{field message}}}',
            {"input":{"id":p["id"], "title":new_title}})
    errs = u["productUpdate"]["userErrors"]
    if errs:
        print(f"     ✗ {errs}")
        results.append((h, "ERROR", str(errs)))
    else:
        print(f"     ✓ aplicado")
        results.append((h, "OK", new_title))

# Legacy DRAFTs
print(f"\n─── Pasar a DRAFT {len(DRAFTS_LEGACY)} productos legacy sin modelo ───")
for h in DRAFTS_LEGACY:
    r = gql('query($h:String!){productByHandle(handle:$h){id status tags title}}', {"h": h})
    p = r.get('productByHandle')
    if not p:
        print(f"  · {h}  no encontrado"); continue
    print(f"  {h}  ({p['title']!r})")
    if DRY:
        print(f"     [DRY] pasaría a DRAFT")
        continue
    new_tags = [t for t in p['tags'] if not t.startswith("envio:") and t not in ("match-rojo","match-verde","match-amarillo")]
    if "legacy-balliu-consolidado-2026-05" not in new_tags: new_tags.append("legacy-balliu-consolidado-2026-05")
    u = gql('mutation($input:ProductInput!){productUpdate(input:$input){product{id} userErrors{field message}}}',
            {"input":{"id":p["id"], "status":"DRAFT", "tags":new_tags}})
    errs = u["productUpdate"]["userErrors"]
    print(f"     {'✓' if not errs else '✗'} {errs or 'pasado a DRAFT'}")

print(f"\n=== Resumen ===")
print(f"  Renames procesados: {len([r for r in results if r[1] in ('DRY','OK')])}")
print(f"  Errores: {len([r for r in results if r[1] == 'ERROR'])}")
