#!/usr/bin/env python3
"""FUENTE DE VERDAD de un producto: handle -> proveedor, SKU, nombre real,
variante exacta, foto original y cotas reales.

Es el PASO 0 del skill: antes de generar nada, se consulta aqui.

Uso:
  python3 scripts/fuente_verdad_producto.py <handle>
  python3 scripts/fuente_verdad_producto.py --todos      # vuelca el mapa completo
  python3 scripts/fuente_verdad_producto.py --cobertura  # que fichas ACTIVE tienen dato y cuales no

Fuentes que consolida (todas ya existentes en el repo):
  Santavila.xlsx  hoja '20260508 -Todos' (+ Hevea/Balliu) -> handle, SKU, nombre del proveedor
  proveedores_raw/hevea/*.csv              -> SKU -> Imagen + Ancho/Fondo/Alto REALES + Descripcion
  proveedores_raw/balliu/_sku_mapping.json -> SKU -> producto + VARIANTE exacta
  balliu_smart_mapping.json                -> handle -> FOTO OFICIAL Balliu + galeria + variante
  proveedores_raw/balliu/_catalogo_2025_texto.txt -> ficha tecnica del catalogo
  images_cutout/<handle>.png               -> recorte de la pieza suelta (CONOCIMIENTO, no publicar)

REGLA: si un handle sale SIN foto oficial, NO se genera nada para el. Se anota y se pide el dato.
"""
import csv,json,glob,sys,os
try: import openpyxl
except ImportError: sys.exit("falta openpyxl: pip3 install openpyxl")

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def cargar():
    wb=openpyxl.load_workbook("Santavila.xlsx", read_only=True)
    h2sku={}
    # la hoja consolidada trae Hevea + Balliu juntos; las otras dos son el respaldo
    hojas=[s for s in wb.sheetnames if s.strip()=="20260508 -Todos"]+["Hevea","Balliu"]
    for sn in hojas:
        rows=list(wb[sn].iter_rows(values_only=True))
        hdr=None
        for i,r in enumerate(rows[:5]):          # la cabecera no siempre esta en la fila 1
            c=[str(x or "") for x in r]
            if "Handle Shopify" in c: hdr,ini=c,i+1; break
        if not hdr: continue
        iH,iS,iP=hdr.index("Handle Shopify"),hdr.index("SKU"),hdr.index("Producto")
        for r in rows[ini:]:
            if not r[iH]: continue
            h=str(r[iH]).strip()
            fila=(str(r[0] or ""),str(r[iS]),str(r[iP]))
            if fila not in h2sku.setdefault(h,[]): h2sku[h].append(fila)
    # OJO: un mismo SKU puede aparecer en varios CSV con imagenes DISTINTAS (p.ej. 557-1563 apunta
    # a "mesa centro 120" y a "dounvil 3 plazas": son productos distintos). Guardar solo la ultima
    # devolvia la foto de otro producto en silencio -> se guardan TODAS y se avisa.
    # Un mismo SKU puede corresponder a DOS PRODUCTOS DISTINTOS del proveedor. Caso real
    # (20-08-2026): 557-010884 es a la vez "LUNA-44 SET MESAS CENTRO 80+60" (435 EUR) y
    # "BRANDON-7 SET SOFA 2 PLAZAS" (3.865 EUR). Quedarse con el primero devolvia la foto de
    # unas mesas para la ficha de un sofa de 4.679 EUR. Ahora se guardan TODOS los candidatos
    # con su coste exworks y se desempata por el COSTE REAL de la variante en Shopify.
    sku2cands={}
    for f in sorted(glob.glob("proveedores_raw/hevea/*.csv")):
        try:
            for row in csv.DictReader(open(f,encoding="utf-8",errors="replace")):
                s=(row.get("SKU") or "").strip()
                if not (s and row.get("Imagen")): continue
                prod=(row.get("Producto") or "").strip()
                img=row["Imagen"].strip()
                cands=sku2cands.setdefault(s,[])
                if any(c["producto"]==prod and c["img"]==img for c in cands): continue
                def num(x):
                    try: return float(str(x).replace(",",".").strip())
                    except Exception: return None
                cands.append({"producto":prod,"img":img,
                              "ancho":row.get("Ancho (cm)") or None,
                              "fondo":row.get("Fondo (cm)") or None,
                              "alto":row.get("Alto (cm)") or None,
                              "descripcion":(row.get("Descripción") or "").strip(),
                              "exworks":num(next((row[k] for k in row
                                    if k and "exworks" in k.lower() and row[k]),None))})
        except Exception: pass
    # coste real de cada handle, para desempatar
    h2cost={}
    try:
        est=json.load(open("_estado_tienda.json"))
        for p in (est if isinstance(est,list) else est.get("products",[])):
            for v in p.get("variants",[]):
                if v.get("cost") is not None: h2cost[p["handle"]]=float(v["cost"]); break
    except Exception: pass
    sku2img={}
    for s,cands in sku2cands.items():
        base=dict(cands[0]); base["otras_img"]=[c["img"] for c in cands[1:] if c["img"]!=base["img"]]
        base["_cands"]=cands
        sku2img[s]=base
    sku2var={}
    try:
        for m in json.load(open("proveedores_raw/balliu/_sku_mapping.json"))["mapping"]:
            sku2var[m["sku"]]=(m["producto"],m["variante"])
    except Exception: pass
    # FOTO OFICIAL de Balliu por handle (faltaba: dejaba 55 fichas sin referencia de QA)
    balliu={}
    try:
        for x in json.load(open("balliu_smart_mapping.json")):
            balliu[x["shopify_handle"]]=x
    except Exception: pass
    # una MISMA foto sirve a varios handles (10 mesas HPL de medidas distintas comparten imagen):
    # esa foto NO identifica la variante -> hay que avisarlo o se genera fiel a la foto equivocada
    compartida={}
    for h,x in balliu.items():
        if x.get("primary_image"): compartida.setdefault(x["primary_image"],[]).append(h)
    for x in balliu.values():
        x["_comparten"]=sorted(compartida.get(x.get("primary_image"),[]))
    return h2sku,sku2img,sku2var,balliu,h2cost

def cutout(handle):
    """Recorte del producto SUELTO en images_cutout/. TOMA DE CONOCIMIENTO:
    sirve para entender la geometria de la pieza aislada, no para publicar."""
    p=os.path.join("images_cutout",handle+".png")
    return p if os.path.exists(p) else None

TIPOLOGIAS=("tumbona","silla","sillon","sillón","mesa","butaca","taburete","parasol","sofa","sofá",
            "banco","reposapies","reposapiés","cama","balinesa","funda","pie","base","modulo","módulo")

def catalogo_balliu(producto):
    """Texto de la ficha del producto en el catalogo general de Balliu 2025.

    El mapping trae 'Eva Pro Tumbona' y el catalogo titula 'Eva Pro': comparar la cadena
    entera no acertaba NUNCA (0 de 459). Se quita el sufijo de tipologia antes de buscar.
    """
    f="proveedores_raw/balliu/_catalogo_2025_texto.txt"
    if not os.path.exists(f) or not producto: return None
    nombre=producto.split("·")[0].split("|")[0].strip()
    pal=[p for p in nombre.split() if p.lower() not in TIPOLOGIAS]
    if not pal: return None
    base=" ".join(pal).lower()
    txt=open(f,encoding="utf-8",errors="replace").read().split("\n")
    mejor=None
    for i,l in enumerate(txt):
        if l.strip().lower()!=base: continue
        blq=[x.strip() for x in txt[i+1:i+26] if x.strip()]
        cand=" ".join(blq[:14])
        if mejor is None or len(cand)>len(mejor): mejor=cand   # varias entradas: la mas informativa
    return mejor or None

def ficha(handle,h2sku,sku2img,sku2var,balliu,h2cost=None):
    out=[]
    for prov,sku,prod in h2sku.get(handle,[]):
        d={"proveedor":prov,"sku":sku,"producto":prod}
        if sku in sku2img:
            e=dict(sku2img[sku]); e.pop("_cands",None); e.pop("producto",None)
            d.update(e)   # el nombre viene del Excel; sku2img solo aporta foto, cotas y texto
        if sku in sku2var:
            d["variante"]=sku2var[sku][1]
            d["catalogo"]=catalogo_balliu(sku2var[sku][0])
        out.append(d)
    # DESEMPATE de SKU compartido por DOS PRODUCTOS del proveedor (caso 557-010884, 20-08-2026):
    # gana el candidato cuyo coste exworks se parece al COSTE REAL de la variante en Shopify.
    if len(out)>1 and h2cost and handle in h2cost:
        c=h2cost[handle]
        cands=[]
        for d in out:
            for x in sku2img.get(d.get("sku",""),{}).get("_cands",[]):
                if x["producto"]==d["producto"] and x.get("exworks"): cands.append((d,x))
        if len(cands)>1:
            err=sorted(cands,key=lambda t:abs(t[1]["exworks"]-c)/c)
            e0=abs(err[0][1]["exworks"]-c)/c; e1=abs(err[1][1]["exworks"]-c)/c
            if e0<=0.35 and e0<e1/2:                     # claramente mejor que el siguiente
                g,x=err[0]
                g.update({k:x[k] for k in ("img","ancho","fondo","alto","descripcion")})
                g["otras_img"]=[y["img"] for _,y in err[1:] if y["img"]!=x["img"]]
                g["_desempate"]=(f"coste real {c:.0f} EUR vs exworks {x['exworks']:.0f} "
                                 f"(el otro candidato, {err[1][0]['producto'][:28]}, cuesta {err[1][1]['exworks']:.0f})")
                out=[g]

    b=balliu.get(handle)
    if b:                                        # Balliu: la foto oficial vive aqui, no en el Excel
        if not out: out=[{"proveedor":"Balliu","sku":"","producto":b.get("shopify_title","")}]
        for d in out:
            if not d.get("img") and b.get("primary_image"): d["img"]=b["primary_image"]
            d.setdefault("variante",b.get("variant_option"))
            d["galeria"]=b.get("gallery_images") or []
            d["slug_balliu"]=b.get("balliu_slug")
            d["comparten"]=[h for h in b.get("_comparten",[]) if h!=handle]
    for d in out: d["cutout"]=cutout(handle)
    return out

def imprimir(d):
    print(f"\n  proveedor : {d['proveedor']}")
    if d.get("sku"):      print(f"  SKU       : {d['sku']}")
    print(f"  producto  : {d['producto']}")
    if d.get("variante"): print(f"  VARIANTE  : {d['variante']}")
    if d.get("img"):      print(f"  foto real : {d['img']}")
    else:                 print(f"  foto real : *** NO HAY *** -> NO se genera nada. Pedir el dato.")
    if d.get("_desempate"):
        print(f"  ✓ SKU duplicado en el proveedor, resuelto por {d['_desempate']}")
    if d.get("otras_img"):
        print(f"  ⚠️  ESE SKU APUNTA A {len(d['otras_img'])+1} IMAGENES DISTINTAS en los CSV del proveedor.")
        print(f"      Puede que sean piezas del mismo lote... o productos distintos. CONFIRMAR cual es.")
        for u in d["otras_img"][:4]: print(f"        tambien: {u}")
    if d.get("comparten"):
        n=len(d["comparten"])
        print(f"  ⚠️  ESA FOTO LA COMPARTEN {n+1} FICHAS -> NO identifica esta variante.")
        print(f"      Antes de generar hay que confirmar con Sergio que la foto es de ESTA medida/acabado.")
        for h in d["comparten"][:6]: print(f"        tambien: {h}")
        if n>6: print(f"        ... y {n-6} mas")
    if d.get("galeria") and len(d["galeria"])>1:
        print(f"  galeria   : {len(d['galeria'])} fotos del proveedor")
        for g in d["galeria"][1:6]: print(f"              {g}")
    if d.get("ancho"):    print(f"  cotas     : ancho {d['ancho']} · fondo {d['fondo']} · alto {d['alto']} cm")
    else:                 print(f"  cotas     : *** NO HAY *** -> sin toma de medidas (nunca deducir de la foto)")
    if d.get("descripcion"): print(f"  descripcion: {d['descripcion'][:200]}")
    if d.get("catalogo"):  print(f"  catalogo  : {d['catalogo'][:260]}")
    if d.get("cutout"):    print(f"  cutout    : {d['cutout']}  (conocimiento de la pieza suelta, NO publicar)")

def cobertura(h2sku,sku2img,sku2var,balliu,h2cost=None):
    import datetime
    SNAP="_estado_imagenes.json"
    mt=datetime.date.fromtimestamp(os.path.getmtime(SNAP))
    dias=(datetime.date.today()-mt).days
    print(f"FUENTE: {SNAP}  ·  snapshot del {mt}  ({dias} dias)")
    if dias>14:
        print(f"⚠️  El snapshot tiene {dias} dias: una ficha puede haber cambiado de estado o de fotos.")
        print( "    Refrescalo con scripts/auditoria_imagenes.py antes de fiarte de estas cifras.\n")
    est=json.load(open(SNAP))
    act=[p for p in est if p["status"]=="ACTIVE"]
    sin_foto=[];sin_cotas=0;ok=0;foto_compartida=[]
    for p in act:
        r=ficha(p["handle"],h2sku,sku2img,sku2var,balliu,h2cost)
        if r and any(d.get("img") for d in r):
            ok+=1
            if any(d.get("comparten") for d in r): foto_compartida.append(p["handle"])
        else: sin_foto.append((p["handle"],p["title"],p["vendor"]))
        if not (r and any(d.get("ancho") for d in r)): sin_cotas+=1
    print(f"ACTIVE: {len(act)}  ·  con foto oficial: {ok}  ·  SIN foto: {len(sin_foto)}  ·  sin cotas: {sin_cotas}")
    print(f"de las {ok} con foto, {len(foto_compartida)} usan una foto COMPARTIDA con otra ficha:")
    print(f"  esa foto NO identifica la variante -> confirmar con Sergio antes de generar.")
    print(f"  fichas listas de verdad (foto propia + identificada): {ok-len(foto_compartida)}")
    print("\nSIN FOTO OFICIAL (no se puede generar nada para estas):")
    for h,t,v in sin_foto: print(f"  [{v}] {h}\n        {t}")

if __name__=="__main__":
    h2sku,sku2img,sku2var,balliu,h2cost=cargar()
    if "--cobertura" in sys.argv:
        cobertura(h2sku,sku2img,sku2var,balliu,h2cost); sys.exit()
    if "--todos" in sys.argv:
        todos=set(h2sku)|set(balliu)
        print(json.dumps({h:ficha(h,h2sku,sku2img,sku2var,balliu,h2cost) for h in sorted(todos)},ensure_ascii=False,indent=1))
        sys.exit()
    if len(sys.argv)<2: sys.exit(__doc__)
    r=ficha(sys.argv[1],h2sku,sku2img,sku2var,balliu,h2cost)
    if not r: sys.exit(f"handle no encontrado en NINGUNA fuente: {sys.argv[1]}  -> no se genera nada")
    for d in r: imprimir(d)