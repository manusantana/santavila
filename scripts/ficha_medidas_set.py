#!/usr/bin/env python3
"""
Toma de MEDIDAS para un SET — overlay determinista (NO IA).

Un conjunto no tiene "un ancho": tiene el de cada pieza. En vez de dibujar una cota sobre el
packshot (que seria falsa), esta ficha lista las medidas de cada pieza y la composicion del lote,
con la tipografia de marca. TODAS las cifras deben venir del catalogo del proveedor: si no hay
dato verificado, la fila no se escribe.

Uso:
  from ficha_medidas_set import ficha_medidas
  ficha_medidas("01_packshot.jpg",
                [("Sofa 3 plazas","220 x 90 x 90 cm"), ("Sillon (x2)","98 x 90 x 90 cm")],
                "1 sofa de 3 plazas   ·   2 sillones",
                "06_medidas.jpg")
"""
import importlib.util, os
from PIL import Image, ImageDraw
import numpy as np

_ov = None
def _font(size):
    global _ov
    if _ov is None:
        aqui = os.path.dirname(os.path.abspath(__file__))
        spec = importlib.util.spec_from_file_location("ov", os.path.join(aqui, "overlay_medidas_producto.py"))
        _ov = importlib.util.module_from_spec(spec)
        try: spec.loader.exec_module(_ov)
        except SystemExit: pass
    return _ov.load_font(size, "/tmp")[0]

INK=(35,37,29); GRIS=(112,114,106); LIN=(203,196,184); BONE=(242,238,230)

def _encuadre(src, W, M, bbox=None):
    """Contorno del producto. Reutiliza el detector por NEUTRALIDAD de overlay_medidas_producto,
    que ya distingue producto (gris neutro) de fondo y sombra (calidos) — detectarlo por
    luminancia se tragaba el suelo entero. Si el recorte sale demasiado alto, se quita aire POR
    ARRIBA: abajo estan las patas y su sombra de contacto."""
    _font(10)                      # fuerza la carga del modulo del overlay
    if bbox: x0,y0,x1,y1 = bbox
    else:
        x0,y0,x1,y1 = _ov.detectar_bbox(src, step=6)
    m = 130
    x0,y0 = max(0,x0-m), max(0,y0-m)
    x1,y1 = min(src.width,x1+m), min(src.height,y1+m)
    disp = W - 2*M; maxH = int(W*0.45)
    if (y1-y0)*disp/(x1-x0) > maxH:
        y0 = max(0, y1 - int((x1-x0)*maxH/disp))
    return src.crop((x0,y0,x1,y1))

def ficha_medidas(packshot, filas, incluye, salida, nota_pie="ancho x fondo x alto", preview=None, bbox=None):
    src = Image.open(packshot).convert("RGB")
    W, M = 2400, 110
    pack = _encuadre(src, W, M, bbox)
    ph = int((W-2*M) * pack.height / pack.width)
    pack = pack.resize((W-2*M, ph), Image.LANCZOS)
    total = 110 + ph + 120 + 48 + len(filas)*112 + 60 + 118 + 76 + 60
    y = max(90, (W-total)//2)
    lz = Image.new("RGB",(W,W),BONE); d = ImageDraw.Draw(lz)
    d.text((M,y),"MEDIDAS DE CADA PIEZA",font=_font(48),fill=INK); y += 110
    lz.paste(pack,(M,y)); y += ph + 120
    d.line([(M,y),(W-M,y)],fill=INK,width=3); y += 48
    for nombre, cota in filas:
        d.text((M,y),nombre,font=_font(46),fill=INK)
        f = _font(46); d.text((W-M-d.textlength(cota,font=f), y), cota, font=f, fill=INK)
        y += 112; d.line([(M,y-30),(W-M,y-30)],fill=LIN,width=2)
    d.text((M,y),nota_pie,font=_font(32),fill=GRIS); y += 118
    d.text((M,y),"EL CONJUNTO INCLUYE",font=_font(38),fill=INK); y += 76
    d.text((M,y),incluye,font=_font(44),fill=INK)
    lz.save(salida, quality=95)
    if preview: lz.resize((760,760),Image.LANCZOS).save(preview, quality=93)
    return salida
