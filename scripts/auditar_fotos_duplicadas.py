#!/usr/bin/env python3
"""Detecta fichas ACTIVE que comparten foto principal (dHash perceptual 256 bits).

Uso:  python3 scripts/auditar_fotos_duplicadas.py [--umbral 12]

Detecta el mismo contenido aunque cambie el nombre de fichero, el sufijo UUID de
Shopify o la compresion. Ejecutar tras cada carga de productos nueva.
"""
import json,urllib.request,os,ssl,sys,tempfile
from PIL import Image

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN=[l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".envlocal"),encoding="utf-8")
       if l.startswith("SHOPIFY_ACCESS_TOKEN=")][0]
API="https://mueblesexterior.myshopify.com/admin/api/2025-01/graphql.json"
UMBRAL=int(sys.argv[sys.argv.index("--umbral")+1]) if "--umbral" in sys.argv else 12

def gql(q,v=None):
    r=urllib.request.Request(API,data=json.dumps({"query":q,"variables":v or {}}).encode(),
        headers={"Content-Type":"application/json","X-Shopify-Access-Token":TOKEN})
    return json.load(urllib.request.urlopen(r))

Q="""query($c:String){products(first:250,query:"status:active",after:$c){pageInfo{hasNextPage endCursor}
 nodes{handle title mediaCount{count} priceRangeV2{maxVariantPrice{amount}}
 media(first:1){nodes{... on MediaImage{image{url}}}}}}}"""

prods=[];c=None
while True:
    d=gql(Q,{"c":c})["data"]["products"]
    prods+=d["nodes"]
    if not d["pageInfo"]["hasNextPage"]: break
    c=d["pageInfo"]["endCursor"]
print(f"fichas ACTIVE: {len(prods)}")

def dhash(path,s=16):
    im=Image.open(path).convert("L").resize((s+1,s))
    px=list(im.getdata()); h=0
    for r in range(s):
        for col in range(s):
            h=(h<<1)|(1 if px[r*(s+1)+col]>px[r*(s+1)+col+1] else 0)
    return h

ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
tmp=tempfile.mkdtemp(); H={}
for i,p in enumerate(prods):
    m=p["media"]["nodes"]
    if not m: continue
    u=(m[0].get("image") or {}).get("url")
    if not u: continue
    f=os.path.join(tmp,f"{i:03d}.jpg")
    try:
        req=urllib.request.Request(u+("&" if "?" in u else "?")+"width=256",
                                   headers={"User-Agent":"Mozilla/5.0"})
        open(f,"wb").write(urllib.request.urlopen(req,context=ctx,timeout=30).read())
        H[i]=dhash(f)
    except Exception: pass
print(f"imagenes analizadas: {len(H)}")

dist=lambda a,b: bin(a^b).count("1")
idx=sorted(H); usados=set(); grupos=[]
for a in idx:
    if a in usados: continue
    g=[a]
    for b in idx:
        if b<=a or b in usados: continue
        if dist(H[a],H[b])<=UMBRAL: g.append(b); usados.add(b)
    if len(g)>1: usados.add(a); grupos.append(g)

print(f"\nGRUPOS que comparten foto principal (Hamming <= {UMBRAL}): {len(grupos)}")
for g in sorted(grupos,key=lambda x:-len(x)):
    print(f"\n== {len(g)} fichas")
    for i in g:
        p=prods[i]
        print(f"   {p['priceRangeV2']['maxVariantPrice']['amount']:>8} € · media {p['mediaCount']['count']:2d}"
              f" · {p['title'][:56]}\n            {p['handle']}")
if not grupos: print("  ninguno — cada ficha tiene su propia foto principal")
