#!/usr/bin/env python3
"""
Toma 5 · MEDIDAS — overlay determinista (NO IA) sobre el packshot de un producto Santavila.

Dibuja las cotas de ancho y alto con la tipografía de marca (JetBrains Mono) y líneas ink,
detectando el contorno REAL del producto para que las cotas lo cubran de extremo a extremo.

Por qué la detección automática (lección 2026-07-23):
  Medir el bounding box "a ojo" produjo una cota de ancho que se quedaba corta (no llegaba
  al reposabrazos). El truco fiable en los packshots de fondo bone: el producto es NEUTRO
  (gris/antracita, R≈B) mientras que el fondo Y LA SOMBRA son CÁLIDOS (R−B alto). Filtrando
  por neutralidad se obtiene el contorno del mueble sin que la sombra lo contamine.

Uso:
  python3 scripts/overlay_medidas_producto.py --img packshot.png --ancho 72 --alto 75 \
      [--out medidas.png] [--lado-alto izq|dcha] [--bbox x0,y0,x1,y1]

Reglas (rol §fotógrafo):
  - Dato VERIFICADO siempre (título/ficha/metafield). Nunca inventar una cota.
  - Etiquetar explícito "Ancho · N cm" / "Alto · N cm": "72×75" es ambiguo por sí solo.
  - Máx. 3 cotas. Si no hay dato de fondo, NO se dibuja.
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

INK = (35, 37, 29)      # #23251D
BONE = (247, 244, 236)  # pastilla de la etiqueta
ALPHA = 190             # ~75 %

WOFF2 = "node_modules/@shopify/cli/dist/assets/hydrogen/virtual-routes/assets/jetbrainsmono-variable-font.woff2"


def load_font(size, workdir):
    """JetBrains Mono (marca). Requiere `brotli` para descomprimir el woff2; si no, Menlo."""
    ttf = os.path.join(workdir, "jetbrainsmono.ttf")
    src = os.path.join(os.getcwd(), WOFF2)
    if not os.path.exists(ttf) and os.path.exists(src):
        try:
            from fontTools.ttLib import TTFont
            f = TTFont(src)
            f.flavor = None
            f.save(ttf)
        except Exception as e:
            print(f"  aviso: no se pudo convertir JetBrains Mono ({e}); se usa Menlo", file=sys.stderr)
    for p in (ttf, "/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/SFNSMono.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size), os.path.basename(p)
            except Exception:
                continue
    return ImageFont.load_default(), "default"


def detectar_bbox(im, step=3):
    """Contorno del producto por NEUTRALIDAD de tono (fondo bone y sombra son cálidos)."""
    W, H = im.size
    px = im.load()
    minx, miny, maxx, maxy = W, H, 0, 0
    for y in range(0, H, step):
        for x in range(0, W, step):
            r, g, b = px[x, y]
            warm = r - b
            luma = 0.299 * r + 0.587 * g + 0.114 * b
            neutral = warm < 12 and abs(g - b) < 14
            dark = luma < 95
            if neutral or dark:
                if dark and warm > 20:       # sombra: oscura PERO cálida -> fuera
                    continue
                minx, maxx = min(minx, x), max(maxx, x)
                miny, maxy = min(miny, y), max(maxy, y)
    if maxx <= minx or maxy <= miny:
        raise SystemExit("No se pudo detectar el producto: pasa --bbox x0,y0,x1,y1 a mano.")
    return minx, miny, maxx, maxy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", required=True, help="packshot de origen (Toma 1)")
    ap.add_argument("--ancho", type=int, required=True, help="cota horizontal en cm (dato VERIFICADO)")
    ap.add_argument("--alto", type=int, required=True, help="cota vertical en cm (dato VERIFICADO)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--lado-alto", choices=["izq", "dcha"], default="izq",
                    help="lado donde va la cota vertical; elige el lado LIMPIO (la sombra suele caer a la dcha)")
    ap.add_argument("--bbox", default=None, help="x0,y0,x1,y1 para forzar el contorno")
    args = ap.parse_args()

    out = args.out or os.path.splitext(args.img)[0] + "-medidas.png"
    workdir = os.path.dirname(os.path.abspath(args.img)) or "."

    im = Image.open(args.img).convert("RGB")
    W, H = im.size

    if args.bbox:
        x0, y0, x1, y1 = [int(v) for v in args.bbox.split(",")]
    else:
        x0, y0, x1, y1 = detectar_bbox(im)
    print(f"bbox producto: x[{x0}-{x1}] y[{y0}-{y1}]  ({x1-x0}x{y1-y0} px)")

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    fs = int(W * 0.024)
    font, fname = load_font(fs, workdir)
    print(f"fuente: {fname} ({fs} px)")

    line = INK + (ALPHA,)
    lw = max(3, W // 900)
    gap = int(W * 0.026)
    cap = int(W * 0.015)

    def label(cx, cy, text, vertical=False):
        bb = dr.textbbox((0, 0), text, font=font)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pad = int(fs * 0.35)
        if vertical:
            tile = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
            td = ImageDraw.Draw(tile)
            td.rounded_rectangle([0, 0, tw + 2 * pad, th + 2 * pad], radius=pad, fill=BONE + (235,))
            td.text((pad - bb[0], pad - bb[1]), text, font=font, fill=INK + (255,))
            tile = tile.rotate(90, expand=True)
            ov.alpha_composite(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)))
        else:
            dr.rounded_rectangle([cx - tw / 2 - pad, cy - th / 2 - pad, cx + tw / 2 + pad, cy + th / 2 + pad],
                                 radius=pad, fill=BONE + (235,))
            dr.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), text, font=font, fill=INK + (255,))

    # Cota ANCHO — horizontal bajo el producto, de extremo a extremo REAL
    yb = min(y1 + gap, H - int(W * 0.045))
    dr.line([(x0, yb), (x1, yb)], fill=line, width=lw)
    dr.line([(x0, yb - cap), (x0, yb + cap)], fill=line, width=lw)
    dr.line([(x1, yb - cap), (x1, yb + cap)], fill=line, width=lw)
    label((x0 + x1) // 2, yb, f"Ancho · {args.ancho} cm")

    # Cota ALTO — vertical en el lado limpio
    if args.lado_alto == "izq":
        xv = max(x0 - gap - int(W * 0.02), int(W * 0.045))
    else:
        xv = min(x1 + gap + int(W * 0.02), W - int(W * 0.045))
    dr.line([(xv, y0), (xv, y1)], fill=line, width=lw)
    dr.line([(xv - cap, y0), (xv + cap, y0)], fill=line, width=lw)
    dr.line([(xv - cap, y1), (xv + cap, y1)], fill=line, width=lw)
    label(xv, (y0 + y1) // 2, f"Alto · {args.alto} cm", vertical=True)

    Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").save(out)
    print(f"guardado: {out}  {W}x{H}")


if __name__ == "__main__":
    main()
