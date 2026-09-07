#!/usr/bin/env python3
"""
Elige, para cada ficha de la fase 3, la mejor foto ANCLA: el packshot del proveedor.

Por que hace falta: en Balliu casi ninguna foto de ambiente sirve de ancla — salen 2 unidades de
un producto que se vende suelto, sillas que no se venden, piscinas y villas. El packshot sobre
fondo liso es la unica foto que muestra EL producto y nada mas.

Deteccion: un packshot de catalogo tiene el marco exterior casi blanco y con poca varianza. Se
puntua por (blancura del borde) y se desempata por resolucion. Devuelve tambien las candidatas
para poder mirarlas: la maquina PROPONE, la vista humana decide.

    python3 scripts/anclas_balliu.py --json <salida>
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

T = os.environ.get("TMPDIR", "/tmp")
fs = json.load(open(os.path.join(T, "balliu.json")))

def descarga(url, p):
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        subprocess.run(["curl", "-sL", "--retry", "3", "--max-time", "90", "-o", p, url], check=False)
    try: return Image.open(p).convert("RGB")
    except Exception: return None

def score(im):
    """Marco de 6 % del borde: media y desviacion. Fondo de catalogo -> media alta, sigma baja."""
    a = np.asarray(im.resize((260, 260), Image.LANCZOS)).astype(float)
    m = np.ones((260, 260), bool); b = 16
    m[b:-b, b:-b] = False
    borde = a[m]
    return borde.mean(), borde.std()

out = []
for i, f in enumerate(fs):
    d = os.path.join(T, "bal", str(i)); os.makedirs(d, exist_ok=True)
    cands = []
    for j, im in enumerate(f["imgs"]):
        o = descarga(im["url"], os.path.join(d, f"{j}.jpg"))
        if o is None: continue
        mu, sd = score(o)
        if mu > 232 and sd < 26:              # fondo liso y claro = packshot de catalogo
            cands.append({"j": j, "w": o.size[0], "h": o.size[1], "mu": round(mu, 1),
                          "sd": round(sd, 1), "url": im["url"]})
    cands.sort(key=lambda c: -c["w"])
    out.append({"i": i, "handle": f["handle"], "title": f["title"], "price": f["price"],
                "sku": f["sku"], "opciones": f["opciones"], "n_img": len(f["imgs"]),
                "packshots": cands})
    marca = "  " if cands else "!!"
    print(f"{marca} [{i:2d}] {f['price']:7.0f} | {len(cands)} packshot(s) "
          f"{[c['w'] for c in cands][:4]} | {f['title'][:54]}")

sin = [o for o in out if not o["packshots"]]
print(f"\nfichas SIN packshot detectado: {len(sin)}  -> hay que mirarlas a mano")
if "--json" in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index("--json")+1], "w"), ensure_ascii=False, indent=1)
