#!/usr/bin/env python3
"""
Contorno REAL del producto en un packshot de fondo bone.

Por que existe (leccion 21-08-2026): el detector por NEUTRALIDAD de
overlay_medidas_producto.py da el bbox al borde de la imagen cuando el fondo
lleva vineta/degradado o cuando el producto es BLANCO (blanco tambien es
neutro). Resultado: la cota de alto arrancaba del borde superior y la de ancho
se pasaba de largo -> una medida que el cliente lee y se cree.

Metodo: el fondo es un degradado suave; se estima su color POR FILA y POR
COLUMNA con la mediana de los bordes, y es producto lo que se separa de esa
estimacion mas que el umbral. La sombra de contacto queda fuera porque su
desviacion es baja y ademas se exige una masa minima por fila/columna.

  python3 scripts/bbox_producto.py <img> [--umbral 18] [--hoja /tmp/x.jpg]
"""
import sys, numpy as np
from PIL import Image, ImageDraw

def bbox(path, umbral=40, min_frac=0.06):
    """Contorno del producto en un packshot bone.

    Cuatro detectores fallaron antes que este (21-08-2026):
      · neutralidad (R~B) a secas   -> el fondo con vineta la rompe a trozos
      · fondo por mediana de bordes -> el bone lleva vineta (198 en esquina, 252 bajo
                                       el foco) y marcaba medio cuadro
      · umbral global de luminancia -> la vineta cae bajo el umbral y arrastra el borde
      · solo oscuridad local        -> el cojin claro del sillon BLANCO no la supera,
                                       y la cota de alto cortaba el respaldo
    Lo que si se cumple siempre: el fondo es, en su vecindad, lo MAS CLARO y lo mas
    CALIDO. Se estiman las dos cosas con un maximo local (que salta por encima del
    producto) y es producto lo que queda por debajo en cualquiera de las dos.
    """
    from PIL import ImageFilter
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)
    L = a @ [0.299, 0.587, 0.114]
    D = a[:, :, 0] - a[:, :, 2]                   # calidez: el bone ronda +11, el gris ~0
    h, w = L.shape
    k = 24

    def fondo_de(canal, desp=0.0):
        ch = Image.fromarray(np.clip(canal + desp, 0, 255).astype(np.uint8))
        ch = ch.resize((w // k, h // k), Image.BILINEAR)
        ch = ch.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2))
        return np.asarray(ch.resize((w, h), Image.BILINEAR)).astype(float) - desp

    mask = ((fondo_de(L) - L) > umbral) | ((fondo_de(D, 128) - D) > 16)
    # El corte se toma sobre el MAXIMO de cada eje, no sobre el tamano de la imagen:
    # un sofa bajo y largo y un sillon alto y estrecho reparten su masa de forma muy
    # distinta, y un porcentaje fijo del cuadro dejaba entrar la sombra blanda.
    sf, sc = mask.sum(axis=1), mask.sum(axis=0)
    filas = sf > max(8, sf.max() * min_frac)
    cols  = sc > max(8, sc.max() * min_frac)
    ys, xs = np.where(filas)[0], np.where(cols)[0]
    if not len(ys) or not len(xs): return None
    # margen del 1%: el detector subestima siempre un poco (el borde iluminado del
    # producto se confunde con el fondo) y una cota CORTA enganya mas que una larga
    mx, my = round(w * 0.01), round(h * 0.01)
    return (max(0, int(xs[0]) - mx), max(0, int(ys[0]) - my),
            min(w - 1, int(xs[-1]) + mx), min(h - 1, int(ys[-1]) + my))

if __name__ == "__main__":
    p = sys.argv[1]
    u = int(sys.argv[sys.argv.index("--umbral")+1]) if "--umbral" in sys.argv else 40
    mf = float(sys.argv[sys.argv.index("--masa")+1]) if "--masa" in sys.argv else 0.06
    b = bbox(p, u, mf)
    im = Image.open(p).convert("RGB")
    print(f"{b[0]},{b[1]},{b[2]},{b[3]}   ({b[2]-b[0]}x{b[3]-b[1]} px de {im.size[0]}x{im.size[1]})")
    if "--hoja" in sys.argv:
        d = ImageDraw.Draw(im); d.rectangle(b, outline=(220,40,40), width=8)
        im.resize((900,900)).save(sys.argv[sys.argv.index("--hoja")+1], quality=92)
