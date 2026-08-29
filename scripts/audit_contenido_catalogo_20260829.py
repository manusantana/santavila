#!/usr/bin/env python3
"""Auditoria de CONTENIDO del catalogo: titulos, SEO, descripciones, alt de imagenes,
galerias, handles y GTIN. Salida: resumen en consola + CSV por producto + JSON de detalle.
Solo lectura."""
import csv, json, os, re, sys, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from upload_images import gql
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = '''query($c:String){ products(first:50, after:$c){ pageInfo{hasNextPage endCursor}
 nodes{ id handle title status vendor productType tags seo{title description} descriptionHtml
   featuredImage{ altText }
   media(first:25){ nodes{ ... on MediaImage{ image{ altText url width height } } } }
   variants(first:50){ nodes{ title sku barcode image{ altText } } } } } }'''
rows=[]; cur=None
while True:
    d=gql(Q,{"c":cur})["products"]; rows+=d["nodes"]
    if not d["pageInfo"]["hasNextPage"]: break
    cur=d["pageInfo"]["endCursor"]
def words(h): return len(re.sub(r"<[^>]+>"," ",h or "").split())
def strip(h): return " ".join(re.sub(r"<[^>]+>"," ",h or "").split())
active=[p for p in rows if p["status"]=="ACTIVE"]; draft=[p for p in rows if p["status"]=="DRAFT"]
out=[]; alt_counter=collections.Counter(); title_counter=collections.Counter()
for p in active:
    imgs=[m["image"] for m in p["media"]["nodes"] if m and m.get("image")]
    alts=[(i.get("altText") or "").strip() for i in imgs]
    fn_like=lambda a: bool(re.search(r"\.(jpe?g|png|webp)$|\d{3,}x\d{3,}|_\d{2,}|^[a-z0-9_\-]+$", a)) if a else False
    n_empty=sum(1 for a in alts if not a)
    n_fnlike=sum(1 for a in alts if a and fn_like(a))
    n_short=sum(1 for a in alts if a and len(a)<15)
    small=sum(1 for i in imgs if (i.get("width") or 0)<1000 and (i.get("height") or 0)<1000)
    for a in alts:
        if a: alt_counter[a]+=1
    title_counter[p["title"].strip().lower()]+=1
    desc=p["descriptionHtml"] or ""
    seo=p["seo"] or {}
    vs=p["variants"]["nodes"]
    out.append({
      "handle":p["handle"],"title":p["title"],"title_len":len(p["title"]),
      "title_convencion":"·" in p["title"],
      "handle_hash":bool(re.search(r"-[0-9a-f]{8}$",p["handle"])),
      "seo_title":bool(seo.get("title")),"seo_title_len":len(seo.get("title") or ""),
      "meta_desc":bool(seo.get("description")),"meta_len":len(seo.get("description") or ""),
      "desc_words":words(desc),"desc_ficha_tecnica":"Ficha técnica" in desc,"desc_h2":"<h2" in desc,
      "desc_lista":"<ul" in desc or "<li" in desc,"desc_tabla":"<table" in desc,
      "n_imgs":len(imgs),"alt_vacios":n_empty,"alt_tipo_fichero":n_fnlike,"alt_cortos":n_short,
      "imgs_pequenas":small,"featured_alt":bool((p.get("featuredImage") or {}).get("altText")),
      "n_variantes":len(vs),"var_sin_barcode":sum(1 for v in vs if not v.get("barcode")),
      "var_sin_sku":sum(1 for v in vs if not v.get("sku")),"var_sin_imagen":sum(1 for v in vs if not v.get("image")),
      "vendor":p["vendor"],"tipo":p["productType"],"n_tags":len(p["tags"]),
    })
N=len(out)
def pct(n): return f"{n} ({100*n/N:.0f}%)"
tot_imgs=sum(o["n_imgs"] for o in out); tot_alt_empty=sum(o["alt_vacios"] for o in out)
tot_alt_fn=sum(o["alt_tipo_fichero"] for o in out); tot_small=sum(o["imgs_pequenas"] for o in out)
dup_alts=[(a,c) for a,c in alt_counter.most_common(8) if c>3]
dup_titles=[(t,c) for t,c in title_counter.items() if c>1]
print(f"AUDITORIA CONTENIDO CATALOGO — {datetime.date.today()} — ACTIVE {N} · DRAFT {len(draft)}")
print("\n== TITULOS ==")
print(" con convención '·' (modelo · medida · nombre):", pct(sum(o['title_convencion'] for o in out)))
print(" >70 chars (se truncan en SERP):", pct(sum(o['title_len']>70 for o in out)))
print(" <25 chars (poco descriptivos):", pct(sum(o['title_len']<25 for o in out)))
print(" duplicados exactos:", len(dup_titles), dup_titles[:3])
print(" con SEO title propio:", pct(sum(o['seo_title'] for o in out)))
print(" handles con hash hex (-xxxxxxxx):", pct(sum(o['handle_hash'] for o in out)))
print("\n== META DESCRIPTION ==")
print(" con meta:", pct(sum(o['meta_desc'] for o in out)), "| >160 chars:", sum(o['meta_len']>160 for o in out), "| <70 chars:", sum(0<o['meta_len']<70 for o in out))
print("\n== DESCRIPCIONES ==")
for lo,hi,lab in ((0,80,"<80p"),(80,120,"80-119p"),(120,200,"120-199p"),(200,9999,"≥200p")):
    print(f"  {lab:>8}: {pct(sum(lo<=o['desc_words']<hi for o in out))}")
print(" con 'Ficha técnica':", pct(sum(o['desc_ficha_tecnica'] for o in out)), "| con H2:", pct(sum(o['desc_h2'] for o in out)), "| con lista:", pct(sum(o['desc_lista'] for o in out)), "| con tabla:", pct(sum(o['desc_tabla'] for o in out)))
print("\n== IMAGENES Y ALT ==")
print(f" imágenes totales: {tot_imgs} · media/producto {tot_imgs/N:.1f}")
print(" productos con 1 sola imagen:", pct(sum(o['n_imgs']<=1 for o in out)), "| con ≥3:", pct(sum(o['n_imgs']>=3 for o in out)))
print(f" ALT vacío: {tot_alt_empty}/{tot_imgs} ({100*tot_alt_empty/max(tot_imgs,1):.0f}%) · productos con algún alt vacío: {pct(sum(o['alt_vacios']>0 for o in out))}")
print(f" ALT tipo nombre-de-fichero/código: {tot_alt_fn} · ALT <15 chars: {sum(o['alt_cortos'] for o in out)}")
print(" ALT más repetidos (mismo texto en muchas imágenes):", dup_alts[:5])
print(f" imágenes <1000px: {tot_small}/{tot_imgs} ({100*tot_small/max(tot_imgs,1):.0f}%)")
print(" imagen destacada sin alt:", pct(sum(not o['featured_alt'] for o in out)))
print("\n== VARIANTES ==")
print(" productos con variantes sin GTIN:", pct(sum(o['var_sin_barcode']>0 for o in out)), "| sin SKU:", pct(sum(o['var_sin_sku']>0 for o in out)), "| variante sin imagen:", pct(sum(o['var_sin_imagen']>0 for o in out)))
print("\n== TAXONOMIA ==")
print(" tipos de producto distintos:", len(set(o['tipo'] for o in out)), "| sin tipo:", sum(not o['tipo'] for o in out), "| sin vendor:", sum(not o['vendor'] for o in out), "| sin tags:", sum(o['n_tags']==0 for o in out))
print(" vendors:", collections.Counter(o['vendor'] for o in out).most_common(5))
ts=datetime.date.today().isoformat()
with open(os.path.join(ROOT,"content","descriptions",f"auditoria_contenido_{ts}.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("\nCSV:", f"content/descriptions/auditoria_contenido_{ts}.csv")
