#!/usr/bin/env python3
"""LIMPIEZA de ficheros intermedios de images_generated/ (22-08-2026).

Borra SOLO lo que es verificablemente reproducible o esta muerto:
  · `_raw*`        capturas a 1024 px ANTES del upscale. Solo se borra si en la MISMA
                   carpeta existe un master numerado (01_, 02_...) de >=2000 px.
  · `_RETIRADA_*`  tomas de consumible apartadas cuando Sergio derogo la comida
                   (03-08-2026). Ya estan documentadas en el JOURNAL.

NO toca, y hay que dejarlo en paz:
  · los masters numerados, aunque su dict en el publicador sea de una tanda antigua;
  · `_foto_oficial_proveedor.*` y `_foto_catalogo_*` -> son la REFERENCIA DE FIDELIDAD,
    lo unico que permite auditar despues si el mueble se respeto;
  · `images_generated/brand/`   -> referenciada por theme/templates/product.json;
  · `images_generated/leisa/` y `tumbona/` -> SIGUEN publicadas en Shopify;
  · `_BORRADAS_consumibles_20260822/` -> backup reversible del borrado de hoy;
  · los .csv/.json de la raiz -> o los usa un script, o son evidencia citada en el JOURNAL.

Dry-run por defecto. Con --apply borra.
"""
import os, sys, glob, json
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "images_generated")
APPLY = "--apply" in sys.argv

def tiene_master(d):
    for f in os.listdir(d):
        if f[:2].isdigit() and f[2:3] == "_":
            try:
                w, h = Image.open(os.path.join(d, f)).size
                if min(w, h) >= 2000:
                    return True
            except Exception:
                pass
    return False

borrar, saltados, libera = [], [], 0
for p in sorted(glob.glob(os.path.join(BASE, "*", "_raw*"))):
    if tiene_master(os.path.dirname(p)):
        borrar.append(p); libera += os.path.getsize(p)
    else:
        saltados.append(p)          # huerfano: sin master no hay de donde rehacerlo
for p in sorted(glob.glob(os.path.join(BASE, "*", "_RETIRADA_*"))):
    borrar.append(p); libera += os.path.getsize(p)

print(f"a borrar : {len(borrar)} ficheros  ({libera/1e6:.1f} MB)")
print(f"saltados : {len(saltados)} (intermedio SIN master -> no se puede rehacer)")
for s in saltados:
    print("   conservado:", os.path.relpath(s, ROOT))
if not APPLY:
    print("\n[dry-run] repite con --apply")
    sys.exit()
for p in borrar:
    os.remove(p)
json.dump([os.path.relpath(p, ROOT) for p in borrar],
          open(os.path.join(BASE, "_limpieza_20260822.json"), "w"), indent=1)
print(f"\nborrados {len(borrar)} ficheros · liberados {libera/1e6:.1f} MB")
print("registro -> images_generated/_limpieza_20260822.json")
