#!/usr/bin/env python3
"""
1. Lee shopify_products.csv y extrae todas las URLs de imagen.
2. Comprueba el tamaño de cada imagen vía HTTP HEAD (sin descargar).
3. Descarga y comprime solo las que superan MAX_SIZE_MB.
4. Guarda las imágenes optimizadas en la carpeta images_optimized/.
5. Genera shopify_products_optimized.csv con las URLs actualizadas
   apuntando a las imágenes locales (para subir manualmente a Shopify).
"""

import csv
import io
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("ERROR: Instala Pillow con:  pip3 install pillow requests")

# ── Configuración ────────────────────────────────────────────
INPUT_CSV      = "shopify_products.csv"
OUTPUT_CSV     = "shopify_products_optimized.csv"
OUTPUT_DIR     = Path("images_optimized")
MAX_SIZE_MB    = 2.0        # Comprimir si la imagen supera este tamaño
MAX_PX         = 2000       # Lado máximo en píxeles tras redimensionar
JPEG_QUALITY   = 85         # Calidad JPEG (0-100)
TIMEOUT        = 20         # Segundos de timeout por petición
# ─────────────────────────────────────────────────────────────

OUTPUT_DIR.mkdir(exist_ok=True)
MAX_BYTES = int(MAX_SIZE_MB * 1024 * 1024)

HEADERS = {"User-Agent": "Mozilla/5.0"}


def http_head_size(url):
    """Devuelve el Content-Length en bytes o None si no está disponible."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            cl = r.headers.get("Content-Length")
            return int(cl) if cl else None
    except Exception:
        return None


def download_bytes(url):
    """Descarga la imagen y devuelve los bytes."""
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def compress_image(data, filename):
    """
    Abre la imagen desde bytes, redimensiona si es necesario y guarda
    como JPEG optimizado. Devuelve la ruta local del archivo resultante.
    """
    img = Image.open(io.BytesIO(data)).convert("RGB")

    # Redimensionar si algún lado supera MAX_PX
    w, h = img.size
    if max(w, h) > MAX_PX:
        ratio = MAX_PX / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    out_path = OUTPUT_DIR / (Path(filename).stem + ".jpg")
    img.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return out_path


def fmt_mb(n):
    return f"{n / 1024 / 1024:.1f} MB" if n else "?"


def main():
    # Leer CSV y extraer URLs únicas con sus handles
    rows = []
    url_to_local = {}   # url → ruta local o url original
    seen_urls = {}      # url → primera fila que la usa

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)
            url = row.get("Image Src", "").strip()
            if url and url not in seen_urls:
                seen_urls[url] = row["Handle"]

    print(f"Imágenes únicas encontradas: {len(seen_urls)}\n")
    print(f"{'#':<4} {'Tamaño':<10} {'Acción':<12} URL")
    print("─" * 90)

    large = []
    ok    = []
    error = []

    for i, (url, handle) in enumerate(seen_urls.items(), 1):
        size = http_head_size(url)
        label_size = fmt_mb(size) if size else "desconocido"

        if size is None or size > MAX_BYTES:
            tag = "⬇ DESCARGA" if size and size > MAX_BYTES else "⚠ SIN DATO"
            print(f"{i:<4} {label_size:<10} {tag:<12} {url[-70:]}")
            large.append(url)
        else:
            print(f"{i:<4} {label_size:<10} {'✓ OK':<12} {url[-70:]}")
            ok.append(url)
            url_to_local[url] = url   # se queda igual

    print(f"\n── Resumen ──────────────────────────────────────────")
    print(f"  OK (≤ {MAX_SIZE_MB} MB):   {len(ok)}")
    print(f"  A comprimir:  {len(large)}")
    print()

    if not large:
        print("Ninguna imagen supera el límite. No es necesario comprimir.")
        return

    # Descargar y comprimir las grandes
    print("Comprimiendo imágenes...")
    for url in large:
        filename = url.split("/")[-1] or "image"
        try:
            data = download_bytes(url)
            original_mb = len(data) / 1024 / 1024
            out_path = compress_image(data, filename)
            final_mb = out_path.stat().st_size / 1024 / 1024
            url_to_local[url] = str(out_path)
            print(f"  ✓ {filename[:50]:<50}  {original_mb:.1f} MB → {final_mb:.1f} MB  →  {out_path.name}")
        except Exception as e:
            url_to_local[url] = url   # si falla, dejamos la URL original
            print(f"  ✗ {filename[:50]:<50}  ERROR: {e}")

    # Generar CSV actualizado
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            url = row.get("Image Src", "").strip()
            if url in url_to_local:
                row = dict(row)
                row["Image Src"] = url_to_local[url]
            writer.writerow(row)

    print(f"\n✓ CSV actualizado guardado en: {OUTPUT_CSV}")
    print(f"✓ Imágenes comprimidas en:     {OUTPUT_DIR}/")
    print()
    print("SIGUIENTE PASO:")
    print("  1. Ve a Shopify → Contenido → Archivos")
    print("  2. Sube todas las imágenes de la carpeta images_optimized/")
    print("  3. Copia las nuevas URLs de Shopify y actualiza los productos")
    print("     (o usa la app 'Matrixify' para reimportar con las rutas locales)")


if __name__ == "__main__":
    main()
