#!/usr/bin/env python3
"""FUENTE DE VERDAD de un producto: handle -> proveedor, SKU, nombre real,
variante exacta, foto original y cotas reales.

Es el PASO 0 del skill: antes de generar nada, se consulta aqui.

Uso:
  python3 scripts/fuente_verdad_producto.py <handle>
  python3 scripts/fuente_verdad_producto.py --todos      # vuelca el mapa completo

Fuentes que consolida (todas ya existentes en el repo):
  Santavila.xlsx  hojas Hevea/Balliu -> handle, SKU, nombre del proveedor
  proveedores_raw/hevea/*.csv        -> SKU -> Imagen + Ancho/Fondo/Alto REALES
  proveedores_raw/balliu/_sku_mapping.json -> SKU -> producto + VARIANTE exacta
"""
import csv,json,glob,sys,os
try: import openpyxl
except ImportError: sys.exit("falta openpyxl: pip3 install openpyxl")

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def cargar():
    wb=openpyxl.load_workbook("Santavila.xlsx", read_only=True)
    h2sku={}
    for sn in ("Hevea","Balliu"):
        rows=list(wb[sn].iter_rows(values_only=True))
        hdr=[str(c or "") for c in rows[0]]
        iH,iS,iP=hdr.index("Handle Shopify"),hdr.index("SKU"),hdr.index("Producto")
        for r in rows[1:]:
            if r[iH]: h2sku.setdefault(str(r[iH]).strip(),[]).append((sn,str(r[iS]),str(r[iP])))
    sku2img={}
    for f in glob.glob("proveedores_raw/hevea/*.csv"):
        try:
            for row in csv.DictReader(open(f,encoding="utf-8",errors="replace")):
                s=(row.get("SKU") or "").strip()
                if s and row.get("Imagen"):
                    sku2img[s]={"img":row["Imagen"].strip(),"ancho":row.get("Ancho (cm)"),
                                "fondo":row.get("Fondo (cm)"),"alto":row.get("Alto (cm)"),
                                "descripcion":(row.get("Descripción") or "").strip()}
        except Exception: pass
    sku2var={}
    try:
        for m in json.load(open("proveedores_raw/balliu/_sku_mapping.json"))["mapping"]:
            sku2var[m["sku"]]=(m["producto"],m["variante"])
    except Exception: pass
    return h2sku,sku2img,sku2var

def cutout(handle):
    """Recorte del producto SUELTO en images_cutout/. TOMA DE CONOCIMIENTO:
    sirve para entender la geometria de la pieza aislada, no para publicar."""
    p=os.path.join("images_cutout",handle+".png")
    return p if os.path.exists(p) else None

def catalogo_balliu(producto):
    """Texto de la ficha del producto en el catalogo general de Balliu 2025."""
    f="proveedores_raw/balliu/_catalogo_2025_texto.txt"
    if not os.path.exists(f) or not producto: return None
    txt=open(f,encoding="utf-8",errors="replace").read().split("\n")
    nombre=producto.split("·")[0].split("|")[0].strip()
    for i,l in enumerate(txt):
        if l.strip().lower()==nombre.lower():
            blq=[x.strip() for x in txt[i:i+26] if x.strip()]
            return " ".join(blq[:14])
    return None

def ficha(handle,h2sku,sku2img,sku2var):
    out=[]
    for prov,sku,prod in h2sku.get(handle,[]):
        d={"proveedor":prov,"sku":sku,"producto":prod}
        if sku in sku2img: d.update(sku2img[sku])
        if sku in sku2var:
            d["variante"]=sku2var[sku][1]
            d["catalogo"]=catalogo_balliu(sku2var[sku][0])
        d["cutout"]=cutout(handle)
        out.append(d)
    return out

if __name__=="__main__":
    h2sku,sku2img,sku2var=cargar()
    if "--todos" in sys.argv:
        print(json.dumps({h:ficha(h,h2sku,sku2img,sku2var) for h in h2sku},ensure_ascii=False,indent=1))
        sys.exit()
    if len(sys.argv)<2: sys.exit(__doc__)
    r=ficha(sys.argv[1],h2sku,sku2img,sku2var)
    if not r: sys.exit(f"handle no encontrado en Santavila.xlsx: {sys.argv[1]}")
    for d in r:
        print(f"\n  proveedor : {d['proveedor']}")
        print(f"  SKU       : {d['sku']}")
        print(f"  producto  : {d['producto']}")
        if d.get("variante"): print(f"  VARIANTE  : {d['variante']}")
        if d.get("img"):      print(f"  foto real : {d['img']}")
        if d.get("ancho"):    print(f"  cotas     : ancho {d['ancho']} · fondo {d['fondo']} · alto {d['alto']} cm")
        if d.get("descripcion"): print(f"  descripcion: {d['descripcion'][:200]}")
        if d.get("catalogo"):  print(f"  catalogo  : {d['catalogo'][:260]}")
        if d.get("cutout"):    print(f"  cutout    : {d['cutout']}  (conocimiento de la pieza suelta, NO publicar)")
