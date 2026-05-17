#!/usr/bin/env python3
"""
consolidate_balliu_tumbonas.py

Consolida la familia "tumbona" Balliu siguiendo el patrón validado con parasoles.
Documentado en docs/santavila/consolidacion-catalogo.md (Familia 2).

19 productos Shopify resultantes con ~390 variantes:
  - 14 modelos de tumbona principal (Eva Pro, Eva Pro T, Eva RG, Eva RTG,
    Carmen, Carmen T, Lola, Lola T, Noa, Olimpia, Etna, Etna Alta, Iris, Marina)
  - 3 mini tumbonas (Cannes, Bristol, Marina)
  - 1 colchoneta (3 tejidos)
  - 1 producto a DRAFT (Alba — no existe en la web del proveedor)

Convenciones (heredadas del piloto parasoles, decisiones del dueño 2026-05-17):
  - Naming Opción C: sin nombre del proveedor visible al cliente.
  - SKU derivado por variante: `SV-<MODELO>-<CHASIS>-<COLOR>` o similar.
  - Metafields para preservar info del proveedor.
  - Chasis con 5 colores reales (Blanco + 4 Prestige). El precio depende
    solo de si el chasis es "Blanco" o cualquier otro ("Prestige" = más caro).
  - 16 colores de tejido como option visible al cliente, mismo precio.

Modos:
  --dry-run (default), --apply, --only NAME, --skip-delete, --skip-publish, --skip-backup.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
BACKUP_DIR = BASE / "backups"
REPORT_CSV = BASE / "consolidate_balliu_tumbonas_report.csv"

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"

ONLINE_STORE_PUB = "gid://shopify/Publication/317589619012"
SHOP_PUB         = "gid://shopify/Publication/317589717316"

PAUSE_THRESHOLD = 200
PAUSE_SECONDS = 2.0


# ─── COLORES ──────────────────────────────────────────────────────────────────

SERIE_00_FULL = ["Azul", "Amarillo", "Naranja", "Verde claro", "Blanco",
                 "Natural", "Capuchino", "Caqui", "Marrón oscuro", "Arena",
                 "Verde oscuro", "Azul celeste", "Ceniza", "Azul marino",
                 "Gris oscuro", "Azul acero"]

SERIE_00_CODES = {"Azul": "01/00", "Amarillo": "02/00", "Naranja": "03/00",
                  "Verde claro": "04/00", "Blanco": "07/00", "Natural": "10/00",
                  "Capuchino": "12/00", "Caqui": "16/00", "Marrón oscuro": "21/00",
                  "Arena": "30/00", "Verde oscuro": "32/00", "Azul celeste": "36/00",
                  "Ceniza": "38/00", "Azul marino": "40/00", "Gris oscuro": "50/00",
                  "Azul acero": "61/00"}

# Chasis: cada modelo define los suyos. "Blanco" siempre primero (es el precio base).
CHASIS_EVA_PRO_NOA  = ["Blanco", "Arena", "Bronce", "Gris Oscuro", "Tórtola"]
CHASIS_CARMEN_LOLA  = ["Blanco", "Arena", "Bronce", "Gris Oscuro", "Madera"]
CHASIS_NOA          = ["Antracita", "Arena", "Blanco", "Madera", "Tórtola"]
CHASIS_EVA_RG       = ["Blanco", "Arena"]
CHASIS_ALUMINIO_3   = ["Blanco", "Tórtola", "Aluminio"]       # Olimpia, Etna, Etna Alta, Mini Cannes
CHASIS_ALUMINIO_2   = ["Blanco", "Aluminio"]                  # Mini Marina


COLOR_SLUGS = {
    "Verde claro":     "VERDE-CLARO",
    "Verde oscuro":    "VERDE-OSC",
    "Azul celeste":    "AZUL-CEL",
    "Azul marino":     "AZUL-MAR",
    "Azul acero":      "AZUL-ACERO",
    "Marrón oscuro":   "MARRON-OSC",
    "Gris oscuro":     "GRIS-OSC",
    "Gris Oscuro":     "GRIS-OSC",
}


def slug(text: str) -> str:
    if text in COLOR_SLUGS:
        return COLOR_SLUGS[text]
    s = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode()
    s = s.upper().replace('(', '').replace(')', '').replace(' ', '-')
    s = re.sub(r'-+', '-', s).strip('-')
    return s


def chasis_es_blanco(chasis: str) -> bool:
    return chasis == "Blanco"


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def read_token() -> str:
    for fname in (".env.local", ".envlocal", ".env"):
        p = BASE / fname
        if not p.exists(): continue
        env = p.read_text(encoding="utf-8")
        m = re.search(r"^SHOPIFY_ACCESS_TOKEN=(.*)$", env, re.M)
        if m: return m.group(1).strip().strip('"').strip("'")
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
                time.sleep(float(e.headers.get("Retry-After", 2))); continue
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            last_err = str(e)
        time.sleep(1.5 * attempt)
    raise RuntimeError(f"GraphQL falló: {last_err}")


# ─── PRODUCTOS ────────────────────────────────────────────────────────────────

def mf_base(modelo: str, sku_orig: str, espacios: list[str], envio: str = "l"):
    """Metafields del producto comunes a todas las tumbonas."""
    return [
        {"namespace": "santavila", "key": "proveedor_modelo", "type": "single_line_text_field", "value": modelo},
        {"namespace": "santavila", "key": "proveedor_grupo", "type": "single_line_text_field", "value": "G1"},
        {"namespace": "santavila", "key": "proveedor_sku_original", "type": "single_line_text_field", "value": sku_orig},
        {"namespace": "santavila", "key": "espacio_principal", "type": "list.single_line_text_field",
         "value": json.dumps(espacios)},
        {"namespace": "santavila", "key": "envio_categoria", "type": "single_line_text_field", "value": envio},
    ]


def mf_color(color: str):
    """Metafield de variante con el código de color del proveedor."""
    return [{"namespace": "santavila", "key": "color_codigo_proveedor",
             "type": "single_line_text_field", "value": SERIE_00_CODES.get(color, "")}]


# Patrón estándar de tumbona "tela" con chasis (Blanco vs Prestige) + 16 colores
def make_tela(name, winner_handle, title, chasis_values, blanco_price, prestige_price,
              sku_modelo, proveedor_modelo, sku_orig, espacios, mini=False):
    sku_prefix = f"SV-{sku_modelo}"
    return {
        "name": name,
        "winner_handle": winner_handle,
        "title": title,
        "options": [
            {"name": "Chasis", "values": chasis_values},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda chasis, color: blanco_price if chasis_es_blanco(chasis) else prestige_price,
        "sku_fn": lambda chasis, color: f"{sku_prefix}-{slug(chasis)}-{slug(color)}",
        "envio_tag": "envio:m" if mini else "envio:l",
        "product_metafields": mf_base(proveedor_modelo, sku_orig, espacios, "m" if mini else "l"),
        "variant_metafields_fn": lambda chasis, color: mf_color(color),
    }


# Patrón "tablillas" (sin tejido, solo chasis)
def make_tablillas(name, winner_handle, title, chasis_values, blanco_price, prestige_price,
                   sku_modelo, proveedor_modelo, sku_orig, espacios):
    sku_prefix = f"SV-{sku_modelo}-T"
    return {
        "name": name,
        "winner_handle": winner_handle,
        "create_new": winner_handle is None,
        "new_handle": f"tumbona-{sku_modelo.lower()}-tablillas" if winner_handle is None else None,
        "product_type": "Tumbona" if winner_handle is None else None,
        "title": title,
        "options": [{"name": "Chasis", "values": chasis_values}],
        "price_fn": lambda chasis: blanco_price if chasis_es_blanco(chasis) else prestige_price,
        "sku_fn": lambda chasis: f"{sku_prefix}-{slug(chasis)}",
        "envio_tag": "envio:l",
        "product_metafields": mf_base(proveedor_modelo, sku_orig, espacios),
    }


# Patrón con ruedas (Olimpia, Etna, Etna Alta): Ruedas × Chasis × Color
def make_con_ruedas(name, winner_handle, title, chasis_values, sin_ruedas_price, con_ruedas_price,
                    sku_modelo, proveedor_modelo, sku_orig, espacios):
    sku_prefix = f"SV-{sku_modelo}"
    return {
        "name": name,
        "winner_handle": winner_handle,
        "title": title,
        "options": [
            {"name": "Ruedas", "values": ["No", "Sí"]},
            {"name": "Chasis", "values": chasis_values},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda ruedas, chasis, color: (
            con_ruedas_price if ruedas == "Sí" else sin_ruedas_price
        ),
        "sku_fn": lambda ruedas, chasis, color: (
            f"{sku_prefix}-{'R' if ruedas == 'Sí' else 'SR'}-{slug(chasis)}-{slug(color)}"
        ),
        "envio_tag": "envio:l",
        "product_metafields": mf_base(proveedor_modelo, sku_orig, espacios),
        "variant_metafields_fn": lambda ruedas, chasis, color: mf_color(color),
    }


PRODUCTS = [
    # ─── EVA PRO ─────────────────────────────────────────────────────────────
    make_tela(
        name="eva_pro_tela",
        winner_handle="balliu-tumbona-de-exterior-resina-b19af1ea",
        title="Tumbona resina · respaldo regulable Ø73 cm tela",
        chasis_values=CHASIS_EVA_PRO_NOA,
        blanco_price=228.44, prestige_price=242.13,
        sku_modelo="EVAPRO", proveedor_modelo="Eva Pro",
        sku_orig="BALLIU_EVA_PRO_TUMBONA_CHASIS_BLANCO_TE_B19AF1EA + variantes",
        espacios=["jardin", "piscina", "terraza"],
    ),
    make_tablillas(
        name="eva_pro_tablillas",
        winner_handle="balliu-tumbona-de-exterior-resina-923110d9",
        title="Tumbona resina · respaldo regulable Ø73 cm tablillas (Mario Eskenazi)",
        chasis_values=CHASIS_EVA_PRO_NOA,
        blanco_price=219.66, prestige_price=242.13,
        sku_modelo="EVAPRO", proveedor_modelo="Eva Pro T",
        sku_orig="BALLIU_EVA_PRO_TUMBONA_CHASIS_BLANCO_TA_923110D9 + Prestige",
        espacios=["jardin", "piscina", "terraza"],
    ),
    # ─── EVA RG / RTG ────────────────────────────────────────────────────────
    {
        "name": "eva_rg",
        "winner_handle": "balliu-tumbona-de-exterior-resina-73-cm-d369d964",
        "title": "Tumbona resina playa · 73 cm tela",
        "options": [
            {"name": "Chasis", "values": CHASIS_EVA_RG},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda chasis, color: 184.83 if chasis == "Blanco" else 192.27,
        "sku_fn": lambda chasis, color: f"SV-EVARG-{slug(chasis)}-{slug(color)}",
        "envio_tag": "envio:l",
        "product_metafields": mf_base(
            "Eva RG",
            "BALLIU_EVA_RG_TUMBONA_CHASIS_BLANCO_TE_D369D964 + Arena",
            ["jardin", "piscina"],
        ),
        "variant_metafields_fn": lambda chasis, color: mf_color(color),
    },
    {
        "name": "eva_rtg",
        "winner_handle": "balliu-tumbona-de-exterior-resina-73-cm-0648657b",
        "title": "Tumbona resina jardín · 73 cm tablillas",
        "options": [{"name": "Chasis", "values": ["Blanco"]}],
        "price_fn": lambda chasis: 190.14,
        "sku_fn": lambda chasis: f"SV-EVARTG-{slug(chasis)}",
        "envio_tag": "envio:l",
        "product_metafields": mf_base(
            "Eva RTG",
            "BALLIU_EVA_RTG_TUMBONA_CHASIS_BLANCO_TA_0648657B",
            ["jardin"],
        ),
    },
    # ─── CARMEN ──────────────────────────────────────────────────────────────
    make_tela(
        name="carmen_tela",
        winner_handle="balliu-tumbona-de-exterior-resina-75-cm-009e68e4",
        title="Tumbona resina · respaldo regulable 75 cm tela",
        chasis_values=CHASIS_CARMEN_LOLA,
        blanco_price=183.23, prestige_price=188.28,
        sku_modelo="CARMEN", proveedor_modelo="Carmen",
        sku_orig="BALLIU_CARMEN_TUMBONA_CHASIS_BLANCO_TE_009E68E4 + variantes",
        espacios=["jardin", "piscina", "terraza"],
    ),
    make_tablillas(
        name="carmen_tablillas",
        winner_handle=None,
        title="Tumbona resina · respaldo regulable 75 cm tablillas",
        chasis_values=CHASIS_CARMEN_LOLA,
        blanco_price=209.03, prestige_price=219.66,
        sku_modelo="CARMEN", proveedor_modelo="Carmen T",
        sku_orig="BALLIU_CARMEN_TUMBONA_CHASIS_BLANCO_TA_ADD04DFC + Prestige",
        espacios=["jardin", "piscina"],
    ),
    # ─── LOLA ────────────────────────────────────────────────────────────────
    make_tela(
        name="lola_tela",
        winner_handle="balliu-tumbona-de-exterior-resina-75-cm-aca076ae",
        title="Tumbona resina · respaldo regulable playa 75 cm tela",
        chasis_values=CHASIS_CARMEN_LOLA,
        blanco_price=182.17, prestige_price=187.74,
        sku_modelo="LOLA", proveedor_modelo="Lola",
        sku_orig="BALLIU_LOLA_TUMBONA_CHASIS_BLANCO_TE_ACA076AE + variantes",
        espacios=["piscina", "jardin"],
    ),
    make_tablillas(
        name="lola_tablillas",
        winner_handle=None,
        title="Tumbona resina · respaldo regulable playa 75 cm tablillas",
        chasis_values=CHASIS_CARMEN_LOLA,
        blanco_price=208.76, prestige_price=212.34,
        sku_modelo="LOLA", proveedor_modelo="Lola T",
        sku_orig="BALLIU_LOLA_TUMBONA_CHASIS_BLANCO_TA_3D8CA52F + Prestige",
        espacios=["piscina", "jardin"],
    ),
    # ─── NOA ─────────────────────────────────────────────────────────────────
    make_tela(
        name="noa",
        winner_handle="balliu-tumbona-de-exterior-resina-28ff014d",
        title="Tumbona resina premium · respaldo regulable",
        chasis_values=CHASIS_NOA,
        blanco_price=400.68, prestige_price=419.31,
        sku_modelo="NOA", proveedor_modelo="Noa",
        sku_orig="BALLIU_NOA_TUMBONA_CHASIS_BLANCO_TE_28FF014D + Prestige",
        espacios=["jardin", "atico", "piscina"],
    ),
    # ─── OLIMPIA / ETNA / ETNA ALTA ─────────────────────────────────────────
    make_con_ruedas(
        name="olimpia",
        winner_handle="balliu-tumbona-de-exterior-sin-ruedas-aluminio-da3f5c24",
        title="Tumbona aluminio · respaldo regulable con/sin ruedas",
        chasis_values=CHASIS_ALUMINIO_3,
        sin_ruedas_price=535.45, con_ruedas_price=587.56,
        sku_modelo="OLIMPIA", proveedor_modelo="Olimpia",
        sku_orig="BALLIU_OLIMPIA_TUMBONA_SIN/CON_RUEDAS_*",
        espacios=["jardin", "piscina", "hosteleria"],
    ),
    make_con_ruedas(
        name="etna",
        winner_handle="balliu-tumbona-de-exterior-aluminio-36870d09",
        title="Tumbona aluminio · respaldo regulable",
        chasis_values=CHASIS_ALUMINIO_3,
        sin_ruedas_price=426.44, con_ruedas_price=470.48,
        sku_modelo="ETNA", proveedor_modelo="Etna",
        sku_orig="BALLIU_ETNA_TUMBONA_TELA_BALLIU_36870D09 + CON",
        espacios=["jardin", "piscina", "hosteleria"],
    ),
    make_con_ruedas(
        name="etna_alta",
        winner_handle="balliu-tumbona-de-exterior-aluminio-d08586c1",
        title="Tumbona aluminio alta · respaldo regulable acceso fácil",
        chasis_values=CHASIS_ALUMINIO_3,
        sin_ruedas_price=463.07, con_ruedas_price=496.21,
        sku_modelo="ETNAALTA", proveedor_modelo="Etna Alta",
        sku_orig="BALLIU_ETNA_ALTA_TUMBONA_AL_TELA_BALLIU_D08586C1 + CON",
        espacios=["hosteleria", "jardin"],
    ),
    # ─── IRIS / MARINA ───────────────────────────────────────────────────────
    {
        "name": "iris",
        "winner_handle": "balliu-tumbona-de-exterior-con-ruedas-aluminio-58-cm-9064b7b9",
        "title": "Tumbona aluminio · con ruedas integradas 58 cm",
        "options": [{"name": "Color tejido", "values": SERIE_00_FULL}],
        "price_fn": lambda color: 628.76,
        "sku_fn": lambda color: f"SV-IRIS-{slug(color)}",
        "envio_tag": "envio:l",
        "product_metafields": mf_base("Iris", "BALLIU_IRIS_TUMBONA_CON_RUEDAS_9064B7B9", ["jardin", "piscina"]),
        "variant_metafields_fn": lambda color: mf_color(color),
    },
    {
        "name": "marina",
        "winner_handle": "balliu-tumbona-de-exterior-aluminio-68-cm-f7ab4da8",
        "title": "Tumbona aluminio apilable · 68 cm",
        "options": [{"name": "Color tejido", "values": SERIE_00_FULL}],
        "price_fn": lambda color: 323.76,
        "sku_fn": lambda color: f"SV-MARINA-{slug(color)}",
        "envio_tag": "envio:l",
        "product_metafields": mf_base("Marina", "BALLIU_MARINA_TUMBONA_TELA_BALLIU_F7AB4DA8", ["jardin", "piscina"]),
        "variant_metafields_fn": lambda color: mf_color(color),
    },
    # ─── MINI TUMBONAS ───────────────────────────────────────────────────────
    {
        "name": "mini_cannes",
        "winner_handle": "balliu-mini-tumbona-de-exterior-aluminio-62-cm-5a6f53eb",
        "title": "Mini tumbona aluminio plegable · 62 cm",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALUMINIO_3},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda chasis, color: 262.28,
        "sku_fn": lambda chasis, color: f"SV-CANNES-{slug(chasis)}-{slug(color)}",
        "envio_tag": "envio:m",
        "product_metafields": mf_base("Mini Cannes", "BALLIU_CANNES_MINI_TUMBONA_*_5A6F53EB", ["balcon", "playa"], "m"),
        "variant_metafields_fn": lambda chasis, color: mf_color(color),
    },
    {
        "name": "mini_bristol",
        "winner_handle": "balliu-mini-tumbona-de-exterior-madera-59-cm-fa211c70",
        "title": "Mini tumbona madera teca plegable · 59 cm",
        "options": [{"name": "Color tejido", "values": SERIE_00_FULL}],
        "price_fn": lambda color: 304.51,
        "sku_fn": lambda color: f"SV-BRISTOL-{slug(color)}",
        "envio_tag": "envio:m",
        "product_metafields": mf_base("Mini Bristol", "BALLIU_BRISTOL_MINI_TUMBONA_*_FA211C70", ["balcon", "playa"], "m"),
        "variant_metafields_fn": lambda color: mf_color(color),
    },
    {
        "name": "mini_marina",
        "winner_handle": "balliu-mini-tumbona-de-exterior-aluminio-57-cm-98ab84ce",
        "title": "Mini tumbona aluminio apilable · 57 cm",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALUMINIO_2},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda chasis, color: 213.34,
        "sku_fn": lambda chasis, color: f"SV-MINIMARINA-{slug(chasis)}-{slug(color)}",
        "envio_tag": "envio:m",
        "product_metafields": mf_base("Mini Marina", "BALLIU_MARINA_MINI_TUMBONA_*_98AB84CE", ["balcon", "playa"], "m"),
        "variant_metafields_fn": lambda chasis, color: mf_color(color),
    },
    # ─── COLCHONETA ──────────────────────────────────────────────────────────
    {
        "name": "colchoneta",
        "winner_handle": "balliu-colchoneta-para-tumbona-0e9a3256",
        "title": "Colchoneta para tumbona",
        "options": [{"name": "Tejido", "values": ["Tela Balliu", "Acrílico", "Dry Feel"]}],
        "price_fn": lambda tejido: {
            "Tela Balliu": 115.55, "Acrílico": 131.37, "Dry Feel": 190.88,
        }[tejido],
        "sku_fn": lambda tejido: f"SV-COLCHONETA-{slug(tejido)}",
        "envio_tag": "envio:xs",
        "product_metafields": mf_base("Colchoneta Dry Feel", "BALLIU_COLCHONETA_TUMBONA_*", ["jardin", "piscina"], "xs"),
    },
    # ─── ALBA (a DRAFT, no se modifica) ──────────────────────────────────────
    {
        "name": "alba",
        "winner_handle": "balliu-tumbona-de-exterior-20620134",
        "action": "draft_only",  # marca para no crear variantes, solo pasar a DRAFT
        "title": "Tumbona Alba (DRAFT — pendiente verificar con proveedor)",
    },
]


# ─── COMBINACIONES ────────────────────────────────────────────────────────────

def expand_variants(product: dict) -> list[dict]:
    if product.get("action") == "draft_only":
        return []
    from itertools import product as iproduct
    option_names = [o["name"] for o in product["options"]]
    option_values = [o["values"] for o in product["options"]]
    out = []
    for combo in iproduct(*option_values):
        opts = dict(zip(option_names, combo))
        if product.get("exclude_fn") and product["exclude_fn"](*combo):
            continue
        price = product["price"] if "price" in product else product["price_fn"](*combo)
        sku = product["sku_fn"](*combo) if "sku_fn" in product else product["base_sku"]
        v_mf = None
        if "variant_metafields_fn" in product:
            v_mf = product["variant_metafields_fn"](*combo)
        entry = {"option_values": opts, "price": round(price, 2), "sku": sku}
        if v_mf:
            entry["metafields"] = v_mf
        out.append(entry)
    return out


# ─── OPERACIONES SHOPIFY ──────────────────────────────────────────────────────

def backup_products(token: str, handles: list[str]) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = BACKUP_DIR / f"tumbonas_{timestamp}.json"
    snap = []
    print(f"📦 Backup de {len(handles)} productos en {out_path.name}…")
    for h in handles:
        try:
            r = gql(token, '''query($h: String!){ productByHandle(handle:$h){
                id handle title status tags
                variants(first:100){edges{node{id sku price selectedOptions{name value}}}}
                options{name values}
            } }''', {"h": h})
            p = r.get("productByHandle")
            if p:
                snap.append(p); print(f"   ✓ {h}")
            else:
                print(f"   · {h} no encontrado")
        except Exception as e:
            print(f"   ✗ {h}: {e}")
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
    return out_path


def find_product(token: str, handle: str) -> dict | None:
    r = gql(token, '''query($h: String!){ productByHandle(handle:$h){
        id handle status tags options{id name optionValues{id name}} variants(first:100){edges{node{id title}}}
    } }''', {"h": handle})
    return r.get("productByHandle")


def update_product(token: str, pid: str, title: str, envio_tag: str | None,
                   current_tags: list[str], product_metafields: list | None = None,
                   status: str | None = None):
    new_tags = [t for t in current_tags if not t.startswith("envio:")]
    if envio_tag: new_tags.append(envio_tag)
    seen, dedup = set(), []
    for t in new_tags:
        if t not in seen: seen.add(t); dedup.append(t)
    inp = {"id": pid, "title": title, "tags": dedup}
    if product_metafields: inp["metafields"] = product_metafields
    if status: inp["status"] = status
    r = gql(token, 'mutation($input: ProductInput!){productUpdate(input:$input){product{id} userErrors{field message}}}',
            {"input": inp})
    return r["productUpdate"]["userErrors"]


def create_options(token: str, pid: str, options: list[dict]):
    opts_input = [{"name": o["name"], "values": [{"name": v} for v in o["values"]]} for o in options]
    r = gql(token, '''mutation($pid:ID!,$opts:[OptionCreateInput!]!){
        productOptionsCreate(productId:$pid, options:$opts){
            userErrors{field message code}
        }
    }''', {"pid": pid, "opts": opts_input})
    return r["productOptionsCreate"]["userErrors"]


def create_variants(token: str, pid: str, variants: list[dict]):
    vs = []
    for v in variants:
        ov = [{"optionName": k, "name": val} for k, val in v["option_values"].items()]
        vi = {"optionValues": ov, "price": f"{v['price']:.2f}",
              "inventoryItem": {"sku": v["sku"], "tracked": False}}
        if v.get("metafields"): vi["metafields"] = v["metafields"]
        vs.append(vi)
    errs_all = []
    for i in range(0, len(vs), 100):
        batch = vs[i:i+100]
        r = gql(token, '''mutation($pid:ID!,$vars:[ProductVariantsBulkInput!]!){
            productVariantsBulkCreate(productId:$pid, variants:$vars, strategy:REMOVE_STANDALONE_VARIANT){
                userErrors{field message code}
            }
        }''', {"pid": pid, "vars": batch})
        errs = r["productVariantsBulkCreate"]["userErrors"]
        if errs: errs_all.extend(errs)
    return errs_all


def create_product_new(token: str, p: dict):
    inp = {
        "title": p["title"],
        "handle": p.get("new_handle"),
        "productType": p.get("product_type", "Tumbona"),
        "status": "ACTIVE",
        "tags": [p.get("envio_tag", "envio:l")],
    }
    if p.get("product_metafields"): inp["metafields"] = p["product_metafields"]
    r = gql(token, 'mutation($input:ProductInput!){productCreate(input:$input){product{id handle} userErrors{field message}}}',
            {"input": inp})
    errs = r["productCreate"]["userErrors"]
    if errs: return None, errs
    return r["productCreate"]["product"]["id"], []


def publish_product(token: str, pid: str):
    r = gql(token, '''mutation($id:ID!,$input:[PublicationInput!]!){
        publishablePublish(id:$id, input:$input){userErrors{field message}}
    }''', {"id": pid, "input": [{"publicationId": ONLINE_STORE_PUB}, {"publicationId": SHOP_PUB}]})
    return r["publishablePublish"]["userErrors"]


# ─── ORQUESTACIÓN ─────────────────────────────────────────────────────────────

def process_product(token: str, p: dict, dry_run: bool, results: list):
    name = p["name"]
    print(f"\n▶ {name} — {p['title']}")

    if p.get("action") == "draft_only":
        if dry_run:
            print(f"   [DRY] pasaría a DRAFT: {p['winner_handle']}")
            results.append({"name": name, "status": "DRY_DRAFT"}); return
        winner = find_product(token, p["winner_handle"])
        if not winner:
            print(f"   ✗ no encontrado"); return
        errs = update_product(token, winner["id"], p["title"], None, winner["tags"], status="DRAFT")
        if errs:
            print(f"   ✗ {errs}")
            results.append({"name": name, "status": "ERROR_DRAFT", "errors": str(errs)})
        else:
            print(f"   ✓ pasado a DRAFT")
            results.append({"name": name, "status": "DRAFTED"})
        return

    variants = expand_variants(p)
    print(f"   plan: {len(variants)} variantes")
    if dry_run:
        opts = [(o['name'], len(o['values'])) for o in p['options']]
        print(f"   options: {opts}")
        for v in variants[:3]:
            print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
        if len(variants) > 3: print(f"     · …y {len(variants)-3} más")
        results.append({"name": name, "title": p["title"], "status": "DRY_RUN",
                        "n_variants": len(variants)})
        return

    # Crear producto nuevo si toca
    if p.get("create_new"):
        existing = find_product(token, p["new_handle"]) if p.get("new_handle") else None
        if existing:
            print(f"   · ya existía: {existing['id']}")
            pid = existing["id"]
        else:
            pid, errs = create_product_new(token, p)
            if errs:
                print(f"   ✗ create: {errs}")
                results.append({"name": name, "status": "ERROR_CREATE", "errors": str(errs)}); return
            print(f"   ✓ creado: {pid}")
    else:
        winner = find_product(token, p["winner_handle"])
        if not winner:
            results.append({"name": name, "status": "ERROR", "errors": f"winner no encontrado"}); return
        pid = winner["id"]
        # Update título + tags + metafields
        errs = update_product(token, pid, p["title"], p.get("envio_tag"),
                              winner["tags"], p.get("product_metafields"))
        if errs:
            print(f"   ✗ update: {errs}")
            results.append({"name": name, "status": "ERROR", "errors": str(errs)}); return

    # Options
    errs = create_options(token, pid, p["options"])
    if errs:
        msgs = " ".join(e.get("message", "") for e in errs).lower()
        if "already" in msgs or "exists" in msgs:
            print(f"   · options ya existían")
        else:
            print(f"   ✗ options: {errs}")
            results.append({"name": name, "status": "ERROR_OPTIONS", "errors": str(errs)}); return

    # Variantes
    errs = create_variants(token, pid, variants)
    if errs:
        print(f"   ✗ variants: {errs[:2]}")
        results.append({"name": name, "status": "ERROR_VARIANTS", "errors": str(errs)[:300]}); return

    print(f"   ✓ {len(variants)} variantes")
    results.append({"name": name, "title": p["title"], "status": "OK",
                    "product_id": pid, "n_variants": len(variants)})


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--only", help="Procesar solo este producto")
    parser.add_argument("--skip-publish", action="store_true")
    parser.add_argument("--skip-backup", action="store_true")
    args = parser.parse_args()

    dry = not args.apply
    print("════ MODO DRY-RUN ════\n" if dry else "════ MODO APPLY ════\n")

    targets = PRODUCTS
    if args.only:
        targets = [p for p in PRODUCTS if p["name"] == args.only]
        if not targets:
            sys.exit(f"✗ no existe producto con name={args.only}")

    token = read_token()

    if not args.skip_backup and not dry:
        handles = [p["winner_handle"] for p in targets if p.get("winner_handle")]
        backup_products(token, handles)

    results = []
    print("─── Procesar productos ───")
    for p in targets:
        process_product(token, p, dry, results)

    if not dry and not args.skip_publish:
        print("\n─── Publicar al Online Store + Shop ───")
        for r in results:
            if r.get("status") == "OK" and r.get("product_id"):
                errs = publish_product(token, r["product_id"])
                print(f"   {'✓' if not errs else '✗'} {r['name']}")
                time.sleep(0.3)

    # Reporte
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        cols = ["name", "title", "status", "n_variants", "product_id", "errors"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in results:
            w.writerow({c: r.get(c, "") for c in cols})
    print(f"\n✓ Reporte: {REPORT_CSV}")


if __name__ == "__main__":
    main()
