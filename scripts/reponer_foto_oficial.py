#!/usr/bin/env python3
"""Repone la FOTO OFICIAL del proveedor en las 6 fichas ACTIVE que estan sin ninguna imagen.

No borra nada (estan a 0 media): solo crea. Dry-run por defecto; --apply para subir.
"""
import json,os,sys,time,urllib.request,mimetypes

ROOT="/Users/sergio/Personal/19 - IA/00-Google Antigravity/12 - ULP Santavila"
SP=os.path.dirname(os.path.abspath(__file__))
TOKEN=[l.split("=",1)[1].strip() for l in open(os.path.join(ROOT,".envlocal"))
       if l.startswith("SHOPIFY_ACCESS_TOKEN")][0]
URL="https://mueblesexterior.myshopify.com/admin/api/2025-01/graphql.json"

# handle -> (fichero local, alt en espanol)
FICHAS={
 "set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa":(
   os.path.join(SP,"set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa.jpg"),
   "Set de jardín de cuerda trenzada greige con sofá de 3 plazas, dos sillones y mesa de centro redonda, con cojines en crudo"),
 "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa":(
   os.path.join(SP,"set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa.jpg"),
   "Set de jardín de cuerda trenzada gris con sofá de 2 plazas, dos sillones y mesa de centro redonda, con cojines en azul claro"),
 "set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-5":(
   os.path.join(ROOT,"images_optimized/1739543673_ACAPULCO-8.jpg"),
   "Set de jardín de aluminio blanco con sofá de 3 plazas, dos sillones y mesa de centro de tablero blanco, con cojines gris claro"),
 "set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-2":(
   os.path.join(SP,"set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-2.jpg"),
   "Set de jardín de aluminio blanco con sofá de 2 plazas, dos sillones y mesa de centro, con cojines en arena"),
 "set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4":(
   os.path.join(SP,"set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4.jpg"),
   "Set de jardín de aluminio antracita con sofá de 2 plazas, dos sillones y mesa de centro de tablero gris, con cojines gris claro"),
 "pergola-aluminio-para-jardin-300300250-cm":(
   os.path.join(SP,"pergola-aluminio-para-jardin-300300250-cm.jpg"),
   "Pérgola de aluminio blanco de 300x300x250 cm con cubierta de lona sobre el césped de un jardín"),
}

def gql(q,v=None):
    ult=None
    for intento in range(5):                      # la API corta la conexion de vez en cuando
        try:
            req=urllib.request.Request(URL,data=json.dumps({"query":q,"variables":v or {}}).encode(),
                headers={"X-Shopify-Access-Token":TOKEN,"Content-Type":"application/json"})
            r=json.load(urllib.request.urlopen(req,timeout=45))
            if r.get("errors"): raise SystemExit(f"GraphQL: {r['errors']}")
            return r["data"]
        except SystemExit: raise
        except Exception as e:
            ult=e; time.sleep(2+2*intento)
    raise SystemExit(f"red: {ult}")

Q_PROD="query($h:String!){productByHandle(handle:$h){id title status mediaCount{count}}}"
M_STAGED="""mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
 stagedTargets{url resourceUrl parameters{name value}} userErrors{message}}}"""
M_CREATE="""mutation($pid:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$pid,media:$media){
 media{... on MediaImage{id status}} mediaUserErrors{message}}}"""
M_DELETE="""mutation($pid:ID!,$ids:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$ids){
 deletedMediaIds mediaUserErrors{message}}}"""
Q_STATUS="""query($id:ID!){product(id:$id){mediaCount{count} media(first:10){nodes{
 ... on MediaImage{id status image{width height}}}}}}"""

def post_multipart(url,params,path):
    boundary="----santavila"+str(int(time.time()))
    body=b""
    for p in params:
        body+=f'--{boundary}\r\nContent-Disposition: form-data; name="{p["name"]}"\r\n\r\n{p["value"]}\r\n'.encode()
    fn=os.path.basename(path)
    ct=mimetypes.guess_type(fn)[0] or "application/octet-stream"
    body+=f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fn}"\r\nContent-Type: {ct}\r\n\r\n'.encode()
    body+=open(path,"rb").read()+f"\r\n--{boundary}--\r\n".encode()
    req=urllib.request.Request(url,data=body,headers={"Content-Type":f"multipart/form-data; boundary={boundary}"})
    return urllib.request.urlopen(req).getcode()

APPLY="--apply" in sys.argv
print(f"{'APLICANDO' if APPLY else 'DRY-RUN (usa --apply para subir)'}\n")
hechos=[]
for handle,(path,alt) in FICHAS.items():
    p=gql(Q_PROD,{"h":handle})["productByHandle"]
    if not p: print(f"✗ no encontrado: {handle}"); continue
    n=p["mediaCount"]["count"]
    kb=os.path.getsize(path)//1024
    print(f"== {p['title'][:58]}")
    print(f"   {p['status']} · media ahora: {n} · sube: {os.path.basename(path)} ({kb} KB)")
    print(f"   alt: {alt[:96]}")
    if n>0:
        st=gql(Q_STATUS,{"id":p["id"]})["product"]["media"]["nodes"]
        malas=[x["id"] for x in st if x.get("status")=="FAILED"]
        buenas=[x for x in st if x.get("status")=="READY"]
        if buenas:
            print("   ✓ ya tiene imagen READY -> SE SALTA\n"); continue
        if malas and APPLY:
            gql(M_DELETE,{"pid":p["id"],"ids":malas})
            print(f"   limpiados {len(malas)} media FAILED")
        elif malas:
            print(f"   [dry-run] limpiaria {len(malas)} media FAILED")
    if not APPLY: print(); continue
    t=gql(M_STAGED,{"input":[{"filename":os.path.basename(path),"mimeType":"image/jpeg",
        "httpMethod":"POST","resource":"IMAGE"}]})["stagedUploadsCreate"]["stagedTargets"][0]
    code=post_multipart(t["url"],t["parameters"],path)
    print(f"   subida HTTP {code}")
    r=gql(M_CREATE,{"pid":p["id"],"media":[{"originalSource":t["resourceUrl"],
        "alt":alt,"mediaContentType":"IMAGE"}]})["productCreateMedia"]
    if r["mediaUserErrors"]: print("   ✗",r["mediaUserErrors"]); continue
    for _ in range(20):
        time.sleep(3)
        st=gql(Q_STATUS,{"id":p["id"]})["product"]
        nodes=st["media"]["nodes"]
        if nodes and all(x.get("status")=="READY" for x in nodes):
            im=nodes[0].get("image") or {}
            print(f"   ✓ READY · {st['mediaCount']['count']} media · {im.get('width')}x{im.get('height')}\n")
            hechos.append(handle); break
    else:
        print("   ⚠ no llego a READY en el tiempo previsto\n")

if APPLY: print(f"REPUESTAS: {len(hechos)} de {len(FICHAS)}")
