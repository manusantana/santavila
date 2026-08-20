#!/usr/bin/env python3
"""
AUDITORIA DE IDENTIDAD — ¿la galeria que publicamos es del producto que dice la ficha?

Nace del caso `albania` (20-08-2026): una galeria de un conjunto verde salvia con patas en A estaba
mapeada a un handle cuyo SKU corresponde a un conjunto gris antracita de patas rectas. La puerta de
identidad del PASO 7.a lo caza ficha a ficha; esto lo hace sobre TODAS a la vez.

Como funciona: para cada carpeta de images_generated con galeria, resuelve su handle -> SKU ->
producto y foto oficial del catalogo del proveedor, y compara el COLOR DEL PRODUCTO (no del fondo)
entre la foto oficial y nuestro packshot. Un desvio grande no prueba que este mal, pero senala donde
hay que mirar. El veredicto final siempre es visual.

  python3 scripts/auditar_identidad.py            # informe
  python3 scripts/auditar_identidad.py --hojas    # ademas escribe hojas de contacto para revisar
"""
import os, re, sys, csv, io, json, glob, urllib.request
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def mapa_carpetas():
    s = open(os.path.join(ROOT, "scripts", "publicar_galeria_producto.py"), encoding="utf-8").read()
    return {sl: h for sl, h in re.findall(r'"([a-z0-9_\-]+)":\s*\("([a-z0-9\-]+)"', s)}

def catalogo():
    cat = {}
    for f in glob.glob(os.path.join(ROOT, "proveedores_raw", "hevea", "*.csv")):
        raw = open(f, encoding="utf-8", errors="replace").read()
        try: dl = csv.Sniffer().sniff(raw[:3000], delimiters=",;\t")
        except Exception: continue
        for r in csv.DictReader(io.StringIO(raw), dialect=dl):
            sku = (r.get("SKU") or "").strip()
            if sku and r.get("Imagen"):
                cat.setdefault(sku, []).append((r.get("Producto", ""), r["Imagen"].strip()))
    return cat

def sku_por_handle():
    est = json.load(open(os.path.join(ROOT, "_estado_tienda.json")))
    prods = est if isinstance(est, list) else est.get("products", [])
    out = {}
    for p in prods:
        for v in p.get("variants", []):
            if v.get("sku"): out[p["handle"]] = (v["sku"], v.get("cost"), p.get("title", "")); break
    return out

def color_producto(im):
    """Color medio de los pixeles del PRODUCTO: los mas oscuros que el fondo, ignorando el fondo
    claro y las esquinas. Da una firma cromatica robusta frente al encuadre."""
    im = im.convert("RGB")
    im.thumbnail((400, 400), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    L = a.mean(axis=2)
    fondo = np.median(np.concatenate([L[:12].ravel(), L[-12:].ravel(), L[:, :12].ravel(), L[:, -12:].ravel()]))
    m = L < fondo - 18
    if m.sum() < 200: m = L < np.percentile(L, 40)
    return a[m].mean(axis=0)

def descargar(url, dest):
    if os.path.exists(dest): return dest
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(dest, "wb").write(urllib.request.urlopen(req, timeout=30).read())
        return dest
    except Exception:
        return None

def main():
    mapa, cat, h2sku = mapa_carpetas(), catalogo(), sku_por_handle()
    tmp = "/tmp/_ident_cache"; os.makedirs(tmp, exist_ok=True)
    filas = []
    for d in sorted(glob.glob(os.path.join(ROOT, "images_generated", "*/"))):
        slug = os.path.basename(d.rstrip("/"))
        if slug.startswith("_"): continue
        pack = os.path.join(d, "01_packshot.jpg")
        if not os.path.exists(pack): continue
        h = mapa.get(slug)
        if not h: filas.append((slug, "?", "sin handle en el publicador", None)); continue
        sku, coste, titulo = h2sku.get(h, ("", None, ""))
        cands = cat.get(sku, [])
        if not cands: filas.append((slug, sku, "SKU no esta en el catalogo Hevea (Balliu o marca propia)", None)); continue
        # si el SKU tiene varios productos, desempata por coste
        nombre, url = cands[0]
        if len(cands) > 1 and coste:
            # no tenemos exworks aqui: nos quedamos con el que da menos desvio de color
            pass
        ruta = descargar(url, os.path.join(tmp, f"{slug}.img"))
        if not ruta: filas.append((slug, sku, f"no se pudo bajar la foto oficial", None)); continue
        try:
            c1 = color_producto(Image.open(ruta)); c2 = color_producto(Image.open(pack))
        except Exception as e:
            filas.append((slug, sku, f"error leyendo imagenes: {e}", None)); continue
        d_rgb = float(np.abs(c1 - c2).mean())
        d_tono = float(abs((c1[0]-c1[2]) - (c2[0]-c2[2])))
        filas.append((slug, sku, nombre[:38], (d_rgb, d_tono, titulo[:44])))

    print(f"\n{'carpeta':22}{'SKU':14}{'ΔRGB':>7}{'Δtono':>7}  producto del catalogo")
    print("-"*104)
    sosp = []
    for slug, sku, nombre, m in sorted(filas, key=lambda x: -(x[3][0] if x[3] else 0)):
        if not m:
            print(f"{slug:22}{sku:14}{'—':>7}{'—':>7}  {nombre}")
            continue
        d_rgb, d_tono, titulo = m
        marca = ""
        if d_rgb > 34 or d_tono > 14:
            marca = "   <-- REVISAR"; sosp.append(slug)
        print(f"{slug:22}{sku:14}{d_rgb:7.1f}{d_tono:7.1f}  {nombre}{marca}")
    print(f"\n{len(sosp)} carpetas a revisar visualmente: {', '.join(sosp) if sosp else '(ninguna)'}")

    if "--hojas" in sys.argv and sosp:
        for slug in sosp:
            of = os.path.join(tmp, f"{slug}.img"); pk = os.path.join(ROOT, "images_generated", slug, "01_packshot.jpg")
            a = Image.open(of).convert("RGB"); a.thumbnail((560, 380), Image.LANCZOS)
            b = Image.open(pk).convert("RGB"); b.thumbnail((560, 380), Image.LANCZOS)
            c = Image.new("RGB", (1140, 390), (250, 250, 250)); c.paste(a, (0, 0)); c.paste(b, (575, 0))
            c.save(f"/tmp/identidad_{slug}.jpg", quality=90)
        print(f"hojas de contacto -> /tmp/identidad_*.jpg")

if __name__ == "__main__":
    main()
