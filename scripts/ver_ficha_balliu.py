#!/usr/bin/env python3
"""Monta un mosaico con TODAS las imagenes de una ficha, numeradas, para elegir el ancla y
cazar piezas fantasma antes de generar. Uso: ver_ficha_balliu.py <indice-en-balliu.json> <salida>"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw

t = os.environ.get("TMPDIR", "/tmp")
fs = json.load(open(os.path.join(t, "balliu.json")))
f = fs[int(sys.argv[1])]
sal = sys.argv[2]
d = os.path.join(t, "bal", str(sys.argv[1])); os.makedirs(d, exist_ok=True)

print(f"{f['title']}  ·  {f['price']:.0f} EUR  ·  SKU {f['sku']}")
print("  opciones:", {k: (v if len(v) <= 6 else v[:6] + ['...']) for k, v in f['opciones'].items()})
print("  handle:", f['handle'])

ims = []
for i, im in enumerate(f["imgs"]):
    p = os.path.join(d, f"{i}.jpg")
    if not os.path.exists(p):
        subprocess.run(["curl", "-sL", "--retry", "3", "--max-time", "90", "-o", p, im["url"]], check=False)
    try: o = Image.open(p).convert("RGB")
    except Exception: continue
    print(f"   [{i}] {o.size[0]}x{o.size[1]}  {im['alt'][:70]}")
    ims.append((i, o))

H, cols = 380, 4
th = []
for i, o in ims:
    r = o.resize((round(o.width * H / o.height), H), Image.LANCZOS)
    dr = ImageDraw.Draw(r); dr.rectangle([0, 0, 46, 34], fill=(200, 30, 30))
    dr.text((14, 8), str(i), fill=(255, 255, 255))
    th.append(r)
rows = (len(th) + cols - 1) // cols
rw = max(sum(x.width for x in th[r*cols:(r+1)*cols]) for r in range(rows))
c = Image.new("RGB", (rw, H * rows), "white")
for r in range(rows):
    x = 0
    for im in th[r*cols:(r+1)*cols]:
        c.paste(im, (x, r*H)); x += im.width
c.save(sal, quality=86)
print("->", sal, c.size)
