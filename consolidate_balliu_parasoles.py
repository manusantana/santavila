#!/usr/bin/env python3
"""
consolidate_balliu_parasoles.py

Consolida los 15 productos planos de la familia "parasol" Balliu en 10 productos
con variantes ricas (color, diámetro, faldón, punta de mástil) según se define en
docs/santavila/auditoria-balliu-parasoles.md.

Fases:
  1. Backup JSON de los 15 productos actuales en `backups/parasoles_<timestamp>.json`.
  2. Para cada producto ganador (8 modelos + 2 accesorios):
     - Actualizar título canónico.
     - Crear options (color, diámetro, faldón, punta) vía productOptionsCreate.
     - Crear variantes vía productVariantsBulkCreate.
     - Aplicar tag envio:l (o envio:m si se decide reclasificar).
     - Eliminar la variante "Default Title" automática.
  3. Eliminar los 4 duplicados puros (productDelete).
  4. Publicar los 10 ganadores en Online Store + Shop.
  5. Reporte CSV con resultado de cada paso.

Modos:
  --dry-run (default)  → no toca Shopify, imprime plan completo y genera reporte.
  --apply              → aplica los cambios reales.
  --only NAME          → procesa solo el producto con ese name interno
                         (pamela_acrilico, pamela_balliu, ocean_acrilico, ocean_balliu,
                          agora, brisa, garbi, roma, pie, base).
  --skip-delete        → no elimina duplicados (más seguro al ejecutar por primera vez).
  --skip-publish       → no publica al Online Store.
  --skip-backup        → omite backup (no recomendado).

Requisitos:
  - openpyxl instalado.
  - .env.local con SHOPIFY_ACCESS_TOKEN (scope write_products + write_publications).
  - Productos ganadores ya existentes en Shopify (este script NO crea Ágora desde cero
    en v1 — usa --only agora con flag especial para crearlo).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
import unicodedata
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
BACKUP_DIR = BASE / "backups"
REPORT_CSV = BASE / "consolidate_balliu_parasoles_report.csv"

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"

ONLINE_STORE_PUB = "gid://shopify/Publication/317589619012"
SHOP_PUB         = "gid://shopify/Publication/317589717316"

PAUSE_THRESHOLD = 200
PAUSE_SECONDS = 2.0


# ─── DEFINICIÓN DECLARATIVA DE LOS 10 PRODUCTOS ────────────────────────────────

# Listas de colores — nombres limpios para el cliente.
# El código del proveedor (96/07, 07/00) vive en el metafield de variante.
# Como cada producto solo usa UNA serie, no hay colisión entre Blanco serie 96 y
# Blanco serie 00 dentro del mismo producto. Excepción: Ágora (ver v2).
SERIE_96 = ["Antracita", "Arena", "Azul", "Blanco", "Crudo", "Mineral"]
SERIE_96_CODES = {"Antracita": "96/42", "Arena": "96/30", "Azul": "96/01",
                  "Blanco": "96/07", "Crudo": "96/08", "Mineral": "96/28"}

SERIE_00_FULL = ["Azul", "Amarillo", "Naranja", "Verde claro", "Blanco",
                 "Natural", "Capuchino", "Caqui", "Marrón oscuro", "Arena",
                 "Verde oscuro", "Azul celeste", "Ceniza", "Azul marino",
                 "Gris oscuro", "Azul acero"]
SERIE_00_CODES = {"Azul": "01/00", "Amarillo": "02/00", "Naranja": "03/00",
                  "Verde claro": "04/00", "Blanco": "07/00",
                  "Natural": "10/00", "Capuchino": "12/00", "Caqui": "16/00",
                  "Marrón oscuro": "21/00", "Arena": "30/00", "Verde oscuro": "32/00",
                  "Azul celeste": "36/00", "Ceniza": "38/00", "Azul marino": "40/00",
                  "Gris oscuro": "50/00", "Azul acero": "61/00"}
SERIE_00_LIMITED_FOR_250 = ["Blanco", "Caqui", "Gris oscuro"]

# Ágora — único producto donde sí hay 2 "Blanco" (serie 96 y serie 00) → diferenciar.
AGORA_COLORS = {
    "Antracita":      (96, "96/42", 426.22),
    "Arena":          (96, "96/30", 426.22),
    "Azul":           (96, "96/01", 426.22),
    "Blanco acrílico": (96, "96/07", 426.22),
    "Crudo":          (96, "96/08", 426.22),
    "Mineral":        (96, "96/28", 426.22),
    "Blanco tela":    (0,  "07/00", 404.20),
    "Caqui":          (0,  "16/00", 404.20),
    "Gris oscuro":    (0,  "50/00", 404.20),
}

# Brisa/Garbí — 3 colores serie 00
BRISA_GARBI_COLORS = ["Blanco", "Caqui", "Gris oscuro"]

# Roma — 3 colores serie 96
ROMA_COLORS = ["Antracita", "Blanco", "Mineral"]


# ─── HELPERS PARA SKUs DERIVADOS ──────────────────────────────────────────────

COLOR_SLUGS = {
    "Blanco acrílico": "BLANCO-ACR",   # solo Ágora
    "Blanco tela":     "BLANCO-TELA",  # solo Ágora
    "Gris oscuro":     "GRIS-OSC",
    "Verde claro":     "VERDE-CLARO",
    "Verde oscuro":    "VERDE-OSC",
    "Azul celeste":    "AZUL-CEL",
    "Azul marino":     "AZUL-MAR",
    "Azul acero":      "AZUL-ACERO",
    "Marrón oscuro":   "MARRON-OSC",
}


def slug(text: str) -> str:
    """Slug ASCII en mayúsculas, sin acentos ni paréntesis."""
    if text in COLOR_SLUGS:
        return COLOR_SLUGS[text]
    s = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode()
    s = s.upper().replace('(', '').replace(')', '').replace(' ', '-')
    s = re.sub(r'-+', '-', s).strip('-')
    return s


def color_code(color: str, serie: int) -> str:
    """Devuelve el código del proveedor para un color, según la serie del producto.
    serie=96 → acrílico (códigos 96/XX). serie=0 → tela Balliu (códigos XX/00)."""
    if serie == 96:
        return SERIE_96_CODES.get(color, "")
    return SERIE_00_CODES.get(color, "")


PRODUCTS = [
    # 1) Pamela acrílico
    {
        "name": "pamela_acrilico",
        "winner_handle": "balliu-parasol-para-terraza-acrilico-236bd5f0",
        "duplicates_to_delete": [
            "balliu-parasol-para-terraza-acrilico-236bd5f0-2",
            "balliu-parasol-para-terraza-acrilico-236bd5f0-3",
        ],
        "title": "Parasol exterior acrílico · mástil regulable Ø200 cm",
        "base_sku": "BALLIU_PARASOL_TELA_ACRILICA_236BD5F0",
        "options": [
            {"name": "Color", "values": SERIE_96},
            {"name": "Punta de mástil", "values": ["Cónica", "Plana"]},
            {"name": "Faldón", "values": ["Sí", "No"]},
        ],
        "price": 413.19,
        "envio_tag": "envio:l",
        "sku_fn": lambda color, punta, faldon: (
            f"SV-PAMELA-ACR-{slug(color)}-{slug(punta)[:3]}-{'F' if faldon=='Sí' else 'NF'}"
        ),
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Pamela"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_PARASOL_TELA_ACRILICA_236BD5F0"},
            {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
             "value": '["terraza", "atico"]'},
        ],
        "variant_metafields_fn": lambda color, punta, faldon: [
            {"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": color_code(color, 96)}
        ],
    },
    # 2) Pamela tela Balliu
    {
        "name": "pamela_balliu",
        "winner_handle": "balliu-parasol-para-terraza-82e48b2d",
        "duplicates_to_delete": [
            "balliu-parasol-para-terraza-82e48b2d-2",
            "balliu-parasol-para-terraza-82e48b2d-3",
        ],
        "title": "Parasol exterior · mástil regulable 16 colores Ø200 cm",
        "base_sku": "BALLIU_PARASOL_TELA_BALLIU_82E48B2D",
        "options": [
            {"name": "Color", "values": SERIE_00_FULL},
            {"name": "Punta de mástil", "values": ["Cónica", "Plana"]},
            {"name": "Faldón", "values": ["Sí", "No"]},
        ],
        "price": 384.37,
        "envio_tag": "envio:l",
        "sku_fn": lambda color, punta, faldon: (
            f"SV-PAMELA-BAL-{slug(color)}-{slug(punta)[:3]}-{'F' if faldon=='Sí' else 'NF'}"
        ),
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Pamela"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_PARASOL_TELA_BALLIU_82E48B2D"},
            {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
             "value": '["terraza", "hosteleria"]'},
        ],
        "variant_metafields_fn": lambda color, punta, faldon: [
            {"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": color_code(color, 0)}
        ],
    },
    # 3) Ocean acrílico (combina dos SKUs por diámetro)
    {
        "name": "ocean_acrilico",
        "winner_handle": "balliu-parasol-para-terraza-acrilico-c8dd492d",  # actualmente Ø250
        "duplicates_to_delete": [],
        "title": "Parasol exterior acrílico · Ø200 / Ø250 cm",
        "base_sku": "BALLIU_PARASOL_TELA_ACRILICA_25_C8DD492D",
        "options": [
            {"name": "Diámetro", "values": ["200 cm", "250 cm"]},
            {"name": "Color", "values": SERIE_96},
            {"name": "Faldón", "values": ["Sí", "No"]},
        ],
        "price_fn": lambda diam, color, faldon: 398.10 if diam == "200 cm" else 414.67,
        "sku_fn": lambda diam, color, faldon: (
            f"SV-OCEAN-ACR-{slug(diam.replace(' cm',''))}-{slug(color)}-{'F' if faldon=='Sí' else 'NF'}"
        ),
        "envio_tag": "envio:l",
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Ocean"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_PARASOL_TELA_ACRILICA_236BD5F0 (Ø200) + BALLIU_PARASOL_TELA_ACRILICA_25_C8DD492D (Ø250)"},
            {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
             "value": '["jardin", "terraza"]'},
        ],
        "variant_metafields_fn": lambda diam, color, faldon: [
            {"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": color_code(color, 96)}
        ],
    },
    # 4) Ocean tela Balliu (Ø250 limitado a 3 colores)
    {
        "name": "ocean_balliu",
        "winner_handle": "balliu-parasol-para-terraza-f1ed8b8b",  # actualmente Ø250
        "duplicates_to_delete": [],
        "title": "Parasol exterior · 16 colores Ø200 / Ø250 cm",
        "base_sku": "BALLIU_PARASOL_TELA_BALLIU_250__F1ED8B8B",
        "options": [
            {"name": "Diámetro", "values": ["200 cm", "250 cm"]},
            {"name": "Color", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda diam, color: 304.13 if diam == "200 cm" else 381.54,
        "sku_fn": lambda diam, color: (
            f"SV-OCEAN-BAL-{slug(diam.replace(' cm',''))}-{slug(color)}"
        ),
        # Excluir combinaciones Ø250 × color no disponible
        "exclude_fn": lambda diam, color: (
            diam == "250 cm" and color not in SERIE_00_LIMITED_FOR_250
        ),
        "envio_tag": "envio:l",
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Ocean"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_PARASOL_TELA_BALLIU_82E48B2D (Ø200) + BALLIU_PARASOL_TELA_BALLIU_250__F1ED8B8B (Ø250)"},
            {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
             "value": '["jardin", "hosteleria"]'},
        ],
        "variant_metafields_fn": lambda diam, color: [
            {"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": color_code(color, 0)}
        ],
    },
    # 5) Ágora — crear desde cero (pendiente v2)
    {
        "name": "agora",
        "winner_handle": None,
        "create_new": True,
        "duplicates_to_delete": [],
        "title": "Parasol cuadrado · 200×200 cm",
        "base_sku": "BALLIU_PARASOL_TELA_ACRILICA_236BD5F0",
        "options": [{"name": "Color", "values": list(AGORA_COLORS.keys())}],
        "price_fn": lambda color: AGORA_COLORS[color][2],
        "sku_fn": lambda color: f"SV-AGORA-{slug(color)}",
        "envio_tag": "envio:l",
    },
    # 6) Brisa
    {
        "name": "brisa",
        "winner_handle": "balliu-parasol-para-terraza-aluminio-300-cm-0ceba8e7",
        "duplicates_to_delete": [],
        "title": "Parasol cuadrado · aluminio 300×300 cm",
        "base_sku": "BALLIU_BRISA_PARASOL_PARASOL_TELA_BAL_0CEBA8E7",
        "options": [{"name": "Color", "values": BRISA_GARBI_COLORS}],
        "price": 1045.32,
        "envio_tag": "envio:l",
        "sku_fn": lambda color: f"SV-BRISA-{slug(color)}",
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Brisa"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_BRISA_PARASOL_PARASOL_TELA_BAL_0CEBA8E7"},
            {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
             "value": '["jardin", "piscina", "porche"]'},
        ],
        "variant_metafields_fn": lambda color: [
            {"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": color_code(color, 0)}
        ],
    },
    # 7) Garbí
    {
        "name": "garbi",
        "winner_handle": "balliu-parasol-para-terraza-aluminio-300-cm-3b7e77d1",
        "duplicates_to_delete": [],
        "title": "Parasol redondo · aluminio Ø300 cm",
        "base_sku": "BALLIU_GARBI_PARASOL_DIAM_300_CM_TELA_3B7E77D1",
        "options": [{"name": "Color", "values": BRISA_GARBI_COLORS}],
        "price": 1045.32,
        "envio_tag": "envio:l",
        "sku_fn": lambda color: f"SV-GARBI-{slug(color)}",
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Garbí"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_GARBI_PARASOL_DIAM_300_CM_TELA_3B7E77D1"},
            {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
             "value": '["jardin", "piscina"]'},
        ],
        "variant_metafields_fn": lambda color: [
            {"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": color_code(color, 0)}
        ],
    },
    # 8) Roma
    {
        "name": "roma",
        "winner_handle": "balliu-parasol-para-terraza-aluminio-300-cm-6c1e1224",
        "duplicates_to_delete": [],
        "title": "Parasol lateral · aluminio 300×300 cm",
        "base_sku": "BALLIU_ROMA_PARASOL_300X300_CM_6C1E1224",
        "options": [{"name": "Color", "values": ROMA_COLORS}],
        "price": 1897.36,
        "envio_tag": "envio:l",
        "sku_fn": lambda color: f"SV-ROMA-{slug(color)}",
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Roma"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_ROMA_PARASOL_300X300_CM_6C1E1224"},
            {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
             "value": '["terraza", "atico"]'},
        ],
        "variant_metafields_fn": lambda color: [
            {"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": color_code(color, 96)}
        ],
    },
    # 9) Pies de parasol
    {
        "name": "pie",
        "winner_handle": "balliu-pie-de-parasol-c2147052",
        "duplicates_to_delete": [],
        "absorb_as_variant": [
            {"handle": "balliu-pie-de-parasol-fab3cac6", "option_value": "RE"},
        ],
        "title": "Pie de parasol · 40 kg",
        "base_sku": "BALLIU_PIE_PARASOL_40_KG_C2147052",
        "options": [{"name": "Acabado", "values": ["Estándar", "RE"]}],
        "price_fn": lambda acabado: 164.14 if acabado == "Estándar" else 126.88,
        "sku_fn": lambda acabado: f"SV-PIE-40KG-{slug(acabado)}",
        "envio_tag": "envio:m",
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Pie 40 kg"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_PIE_PARASOL_40_KG_C2147052 (Est.) + BALLIU_PIE_PARASOL_40_KG_RE_FAB3CAC6 (RE)"},
        ],
    },
    # 10) Bases de hormigón (PRECIOS INVERTIDOS según decisión del dueño)
    {
        "name": "base",
        "winner_handle": "balliu-base-de-parasol-3ee8b72d",
        "duplicates_to_delete": [],
        "absorb_as_variant": [
            {"handle": "balliu-base-de-parasol-890a4cd4", "option_value": "30 kg"},
        ],
        "title": "Base de hormigón para parasol",
        "base_sku": "BALLIU_BASE_HORMIGON_25_KG_3EE8B72D",
        "options": [{"name": "Peso", "values": ["25 kg", "30 kg"]}],
        "price_fn": lambda peso: 51.23 if peso == "25 kg" else 102.16,
        "sku_fn": lambda peso: f"SV-BASE-{slug(peso.replace(' ',''))}",
        "envio_tag": "envio:m",
        "product_metafields": [
            {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": "Base de hormigón"},
            {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
            {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field",
             "value": "BALLIU_BASE_HORMIGON_25_KG_3EE8B72D + BALLIU_BASE_HORMIGON_30_KG_890A4CD4"},
        ],
    },
]


# ─── HELPERS ───────────────────────────────────────────────────────────────────

def read_token() -> str:
    for fname in (".env.local", ".envlocal", ".env"):
        p = BASE / fname
        if not p.exists():
            continue
        env = p.read_text(encoding="utf-8")
        m = re.search(r"^SHOPIFY_ACCESS_TOKEN=(.*)$", env, re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit("✗ SHOPIFY_ACCESS_TOKEN no encontrado")


_throttle = {"available": 2000.0}


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    last_err = None
    for attempt in range(1, 6):
        try:
            req = urllib.request.Request(API, data=payload,
                headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            if data.get("errors"):
                raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
            ts = data.get("extensions", {}).get("cost", {}).get("throttleStatus", {})
            if ts:
                _throttle["available"] = ts.get("currentlyAvailable", 0)
            if _throttle["available"] < PAUSE_THRESHOLD:
                time.sleep(PAUSE_SECONDS)
            return data["data"]
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:400]
            last_err = f"HTTP {e.code}: {body}"
            if e.code == 429:
                wait = float(e.headers.get("Retry-After", 2))
                time.sleep(wait); continue
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            last_err = str(e)
        time.sleep(1.5 * attempt)
    raise RuntimeError(f"GraphQL falló: {last_err}")


# ─── COMBINACIONES DE VARIANTES ────────────────────────────────────────────────

def expand_variants(product: dict) -> list[dict]:
    """Genera las combinaciones de variantes a partir de las options.
    Devuelve lista de dicts {options: {name: value}, price, sku}."""
    from itertools import product as iproduct
    option_names = [o["name"] for o in product["options"]]
    option_values = [o["values"] for o in product["options"]]
    out = []
    for combo in iproduct(*option_values):
        opts = dict(zip(option_names, combo))
        # Exclusión por reglas del producto
        exclude_fn = product.get("exclude_fn")
        if exclude_fn and exclude_fn(*combo):
            continue
        # Precio
        if "price" in product:
            price = product["price"]
        else:
            price = product["price_fn"](*combo)
        # SKU
        if "sku_fn" in product:
            sku = product["sku_fn"](*combo)
        else:
            sku = product["base_sku"]
        # Metafields de variante (si la función está definida)
        v_metafields = None
        if "variant_metafields_fn" in product:
            v_metafields = product["variant_metafields_fn"](*combo)
        entry = {"option_values": opts, "price": round(price, 2), "sku": sku}
        if v_metafields:
            entry["metafields"] = v_metafields
        out.append(entry)
    return out


# ─── BACKUP ────────────────────────────────────────────────────────────────────

def backup_products(token: str, handles: list[str]) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = BACKUP_DIR / f"parasoles_{timestamp}.json"
    snap = []
    print(f"📦 Backup de {len(handles)} productos en {out_path.name} …")
    for h in handles:
        try:
            r = gql(token, '''query($h: String!){ productByHandle(handle:$h){
                id handle title vendor productType status tags
                variants(first:100){ edges{ node{
                  id sku price compareAtPrice inventoryItem{ id tracked unitCost{amount} }
                  selectedOptions{ name value }
                } } }
                options{ id name values }
                resourcePublications(first:10){ edges{ node{ publication{ id name } } } }
                media(first:50){ edges{ node{ ... on MediaImage { id image { url altText } } } } }
            } }''', {"h": h})
            p = r["productByHandle"]
            if p:
                snap.append(p)
                print(f"   ✓ {h}")
            else:
                print(f"   ✗ {h} (no encontrado)")
        except Exception as e:
            print(f"   ✗ {h} error: {e}")
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
    print(f"   → {len(snap)} productos guardados\n")
    return out_path


# ─── OPERACIONES SOBRE UN PRODUCTO GANADOR ────────────────────────────────────

def find_product(token: str, handle: str) -> dict | None:
    r = gql(token, '''query($h: String!){ productByHandle(handle:$h){
        id handle title vendor status
        options{ id name values position }
        variants(first:100){ edges{ node{ id title selectedOptions{ name value } } } }
        tags
    } }''', {"h": handle})
    return r["productByHandle"]


def update_title_and_tags(token: str, product_id: str, title: str, envio_tag: str | None,
                          current_tags: list[str], product_metafields: list | None = None):
    new_tags = [t for t in current_tags if not t.startswith("envio:")]
    if envio_tag:
        new_tags.append(envio_tag)
    seen, dedup = set(), []
    for t in new_tags:
        if t not in seen:
            seen.add(t); dedup.append(t)
    input_data = {"id": product_id, "title": title, "tags": dedup}
    if product_metafields:
        input_data["metafields"] = product_metafields
    r = gql(token, '''mutation($input: ProductInput!){
        productUpdate(input:$input){ product{id title tags} userErrors{field message} }
    }''', {"input": input_data})
    return r["productUpdate"]["userErrors"]


def delete_existing_variants(token: str, product_id: str, variant_ids: list[str]):
    """Elimina variantes existentes (típicamente la 'Default Title')."""
    if not variant_ids:
        return []
    r = gql(token, '''mutation($pid: ID!, $ids: [ID!]!){
        productVariantsBulkDelete(productId:$pid, variantsIds:$ids){
            product{id} userErrors{field message}
        }
    }''', {"pid": product_id, "ids": variant_ids})
    return r["productVariantsBulkDelete"]["userErrors"]


def create_options(token: str, product_id: str, options: list[dict]):
    """Añade las options al producto. Si ya existen, falla — usar --force para limpiar antes."""
    opts_input = [
        {"name": o["name"], "values": [{"name": v} for v in o["values"]]}
        for o in options
    ]
    r = gql(token, '''mutation($pid: ID!, $opts: [OptionCreateInput!]!){
        productOptionsCreate(productId:$pid, options:$opts){
            product{id options{name values}} userErrors{field message code}
        }
    }''', {"pid": product_id, "opts": opts_input})
    return r["productOptionsCreate"]["userErrors"]


def create_variants(token: str, product_id: str, variants: list[dict]):
    """Crea variantes vía productVariantsBulkCreate."""
    variants_input = []
    for v in variants:
        opt_values = [{"optionName": k, "name": val} for k, val in v["option_values"].items()]
        variant_input = {
            "optionValues": opt_values,
            "price": f"{v['price']:.2f}",
            "inventoryItem": {"sku": v["sku"], "tracked": False},
        }
        if v.get("metafields"):
            variant_input["metafields"] = v["metafields"]
        variants_input.append(variant_input)
    # Si son muchas, batch de 100
    errors_all = []
    BATCH = 100
    for i in range(0, len(variants_input), BATCH):
        batch = variants_input[i:i+BATCH]
        r = gql(token, '''mutation($pid: ID!, $vars: [ProductVariantsBulkInput!]!){
            productVariantsBulkCreate(productId:$pid, variants:$vars, strategy:REMOVE_STANDALONE_VARIANT){
                productVariants{id sku price selectedOptions{name value}}
                userErrors{field message code}
            }
        }''', {"pid": product_id, "vars": batch})
        errs = r["productVariantsBulkCreate"]["userErrors"]
        if errs:
            errors_all.extend(errs)
    return errors_all


def delete_product(token: str, product_id: str):
    r = gql(token, '''mutation($id: ID!){
        productDelete(input:{id:$id}){ deletedProductId userErrors{field message} }
    }''', {"id": product_id})
    return r["productDelete"]["userErrors"]


def publish_product(token: str, product_id: str, pub_ids: list[str]):
    r = gql(token, '''mutation($id: ID!, $input: [PublicationInput!]!){
        publishablePublish(id:$id, input:$input){ userErrors{field message} }
    }''', {"id": product_id, "input": [{"publicationId": p} for p in pub_ids]})
    return r["publishablePublish"]["userErrors"]


# ─── ORQUESTACIÓN ──────────────────────────────────────────────────────────────

def process_product(token: str, p: dict, dry_run: bool, results: list):
    name = p["name"]
    print(f"\n▶ {name} — {p['title']}")
    variants = expand_variants(p)
    print(f"   plan: {len(variants)} variantes")
    if dry_run:
        print(f"   options: {[(o['name'], len(o['values'])) for o in p['options']]}")
        for v in variants[:3]:
            print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
        if len(variants) > 3:
            print(f"     · …y {len(variants)-3} más")
        results.append({"name": name, "title": p["title"], "status": "DRY_RUN",
                        "n_variants": len(variants), "errors": ""})
        return

    if p.get("create_new"):
        print(f"   ⚠ create_new=True para {name} — NO implementado en v1. Saltar.")
        results.append({"name": name, "title": p["title"], "status": "SKIPPED_NEW",
                        "n_variants": len(variants), "errors": "create_new pendiente v2"})
        return

    if not p.get("winner_handle"):
        results.append({"name": name, "status": "ERROR", "errors": "sin winner_handle"})
        return

    winner = find_product(token, p["winner_handle"])
    if not winner:
        results.append({"name": name, "status": "ERROR", "errors": f"winner no encontrado: {p['winner_handle']}"})
        return

    # Update título + tags + metafields del producto
    errs = update_title_and_tags(token, winner["id"], p["title"], p.get("envio_tag"),
                                  winner["tags"], p.get("product_metafields"))
    if errs:
        print(f"   ✗ update title: {errs}")
        results.append({"name": name, "status": "ERROR", "errors": str(errs)}); return

    # Crear options
    errs = create_options(token, winner["id"], p["options"])
    if errs:
        print(f"   ✗ create options: {errs}")
        results.append({"name": name, "status": "ERROR_OPTIONS", "errors": str(errs)}); return

    # Crear variantes (REMOVE_STANDALONE_VARIANT elimina la default automáticamente)
    errs = create_variants(token, winner["id"], variants)
    if errs:
        print(f"   ✗ create variants: {errs[:2]}")
        results.append({"name": name, "status": "ERROR_VARIANTS", "errors": str(errs)[:300]}); return

    print(f"   ✓ {len(variants)} variantes creadas")
    results.append({"name": name, "title": p["title"], "status": "OK",
                    "winner_id": winner["id"], "n_variants": len(variants), "errors": ""})


def delete_duplicates(token: str, p: dict, dry_run: bool, results: list):
    handles = list(p.get("duplicates_to_delete", []))
    # Productos absorbidos como variante también se eliminan
    for absorb in p.get("absorb_as_variant", []):
        handles.append(absorb["handle"])
    for h in handles:
        prod = find_product(token, h)
        if not prod:
            print(f"   · {h}: ya no existe")
            continue
        if dry_run:
            print(f"   [DRY] eliminaría {h} ({prod['id']})")
            results.append({"name": f"delete:{h}", "status": "DRY_RUN"})
            continue
        errs = delete_product(token, prod["id"])
        if errs:
            print(f"   ✗ delete {h}: {errs}")
            results.append({"name": f"delete:{h}", "status": "ERROR", "errors": str(errs)})
        else:
            print(f"   ✓ eliminado {h}")
            results.append({"name": f"delete:{h}", "status": "DELETED"})


def publish_all(token: str, products: list, dry_run: bool):
    for p in products:
        if not p.get("winner_handle"):
            continue
        prod = find_product(token, p["winner_handle"])
        if not prod:
            continue
        if dry_run:
            print(f"   [DRY] publicaría {p['name']} en Online Store + Shop")
            continue
        errs = publish_product(token, prod["id"], [ONLINE_STORE_PUB, SHOP_PUB])
        if errs:
            print(f"   ✗ publish {p['name']}: {errs}")
        else:
            print(f"   ✓ publicado {p['name']}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Aplica cambios (default: dry-run)")
    parser.add_argument("--only", help="Procesar solo este producto (name interno)")
    parser.add_argument("--skip-delete", action="store_true")
    parser.add_argument("--skip-publish", action="store_true")
    parser.add_argument("--skip-backup", action="store_true")
    args = parser.parse_args()

    dry = not args.apply
    if dry:
        print("════ MODO DRY-RUN — no se toca Shopify ════\n")
    else:
        print("════ MODO APPLY — cambios reales en producción ════\n")

    target_products = PRODUCTS
    if args.only:
        target_products = [p for p in PRODUCTS if p["name"] == args.only]
        if not target_products:
            sys.exit(f"✗ no existe producto con name={args.only}")

    token = read_token()

    # Backup
    if not args.skip_backup and not dry:
        all_handles = []
        for p in target_products:
            if p.get("winner_handle"):
                all_handles.append(p["winner_handle"])
            all_handles.extend(p.get("duplicates_to_delete", []))
            for a in p.get("absorb_as_variant", []):
                all_handles.append(a["handle"])
        backup_products(token, all_handles)

    results = []

    # Procesar cada ganador
    print("─── 1. Crear variantes en productos ganadores ───")
    for p in target_products:
        process_product(token, p, dry, results)

    # Eliminar duplicados + absorbidos
    if not args.skip_delete:
        print("\n─── 2. Eliminar duplicados y productos absorbidos ───")
        for p in target_products:
            delete_duplicates(token, p, dry, results)

    # Publicar
    if not args.skip_publish:
        print("\n─── 3. Publicar al Online Store + Shop ───")
        publish_all(token, target_products, dry)

    # Reporte
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        cols = ["name", "title", "status", "n_variants", "winner_id", "errors"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in results:
            w.writerow({c: r.get(c, "") for c in cols})
    print(f"\n✓ Reporte: {REPORT_CSV}")

    if dry:
        print("\nPara aplicar realmente:")
        print("   python3 consolidate_balliu_parasoles.py --apply")
        print("Recomendación: primero un producto piloto:")
        print("   python3 consolidate_balliu_parasoles.py --apply --only brisa --skip-delete")


if __name__ == "__main__":
    main()
