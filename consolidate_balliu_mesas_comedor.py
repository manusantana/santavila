#!/usr/bin/env python3
"""
consolidate_balliu_mesas_comedor.py

Sub-piloto 3a · Familia 3 (Mesas) — Mesa comedor.

9 productos ACTIVE consolidados (~240 variantes) + 7 DRAFT nuevos (HPL_GD y variantes
no-web por modelo) + ~28 productos planos legacy pasados a DRAFT.

Decisiones del dueño (2026-05-17, confirmadas tras ver capturas web Balliu):
  - HPL Gran Densidad: NUNCA como opción visible. Siempre DRAFT separado.
  - Brunei: matriz 4 tamaños × 3 chasis × 5 HPL std = 60 variantes ACTIVE.
  - Altea: solo 2 tamaños (70×70 / 80×80) × 2 chasis (Blanco/Tórtola) × 5 HPL std,
    como la web muestra. Resto a DRAFT.
  - Capri Doble: producto APARTE (no variante del Capri principal).
  - Nora: dimensión web (72×72), no Excel (Ø70).
  - Sofia: NO está en web → todo DRAFT.
  - Atlanta 240×90, Java/Capri/Altea HPL_GD, Ágata 120×80/180×90 → DRAFT.
  - Naming Opción C + sufijo " · <Modelo>" (regla 3d).

Modos: --dry-run, --apply, --only NAME, --skip-publish, --skip-backup.
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
REPORT_CSV = BASE / "consolidate_balliu_mesas_comedor_report.csv"

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"

ONLINE_STORE_PUB = "gid://shopify/Publication/317589619012"
SHOP_PUB         = "gid://shopify/Publication/317589717316"

PAUSE_THRESHOLD = 200
PAUSE_SECONDS = 2.0
LEGACY_TAG = "legacy-balliu-consolidado-2026-05"
PENDING_TAG = "pendiente-confirmar-proveedor"


# ─── HELPERS ──────────────────────────────────────────────────────────────────

COLOR_SLUGS = {
    "Tórtola": "TORTOLA",
    "Ø70 cm":   "D70",
    "Ø80 cm":   "D80",
    "Ø90 cm":   "D90",
    "70×70 cm": "70X70",
    "80×80 cm": "80X80",
    "120×80 cm":"120X80",
    "130×80 cm":"130X80",
    "160×90 cm":"160X90",
    "190×90 cm":"190X90",
    "140/180×90 cm":  "140-180X90",
    "200/260×100 cm": "200-260X100",
    "140/180×100 cm": "140-180X100",
}


def slug(text: str) -> str:
    if text in COLOR_SLUGS:
        return COLOR_SLUGS[text]
    s = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode()
    s = s.upper().replace('(', '').replace(')', '').replace(' ', '-').replace('×','X').replace('/','-')
    s = re.sub(r'-+', '-', s).strip('-')
    return s


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
            if ts: _throttle["available"] = ts.get("currentlyAvailable", 0)
            if _throttle["available"] < PAUSE_THRESHOLD: time.sleep(PAUSE_SECONDS)
            return data["data"]
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:400]
            last_err = f"HTTP {e.code}: {body}"
            if e.code == 429: time.sleep(float(e.headers.get("Retry-After", 2))); continue
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            last_err = str(e)
        time.sleep(1.5 * attempt)
    raise RuntimeError(f"GraphQL falló: {last_err}")


# ─── METAFIELDS ───────────────────────────────────────────────────────────────

def mf_base(modelo: str, sku_orig: str, espacios: list[str], envio: str = "l"):
    return [
        {"namespace": "santavila", "key": "proveedor_modelo",
         "type": "single_line_text_field", "value": modelo},
        {"namespace": "santavila", "key": "proveedor_grupo",
         "type": "single_line_text_field", "value": "G1"},
        {"namespace": "santavila", "key": "proveedor_sku_original",
         "type": "single_line_text_field", "value": sku_orig},
        {"namespace": "santavila", "key": "espacio_principal",
         "type": "list.single_line_text_field", "value": json.dumps(espacios)},
        {"namespace": "santavila", "key": "envio_categoria",
         "type": "single_line_text_field", "value": envio},
    ]


def mf_variant(sku_orig: str):
    return [{"namespace": "santavila", "key": "proveedor_sku_original",
             "type": "single_line_text_field", "value": sku_orig}]


# ─── OPCIONES ─────────────────────────────────────────────────────────────────

CHASIS_ALU3 = ["Blanco", "Tórtola", "Aluminio"]
CHASIS_ALU2 = ["Blanco", "Tórtola"]                # Altea, Ágata, Nora
COLORES_HPL = ["Gris", "Blanco", "Moonwalk", "Skyline", "Prado"]


# ─── PRODUCTOS ACTIVE CONSOLIDADOS ────────────────────────────────────────────
# Cada entrada usa la lambda price_fn / sku_fn con argumentos posicionales según
# el orden de las options.

PRODUCTS: list[dict] = [
    # ───── 1. SELVA · Werzalit (1 chasis, sin opción visible) ─────
    {
        "name": "selva",
        "winner_handle": "balliu-mesa-exterior-resina-70-cm-33ce1613",
        "title": "Mesa exterior resina · Werzalit · Selva",
        "envio_tag": "envio:l",
        "options": [{"name": "Tamaño", "values": ["Ø70 cm", "Ø80 cm", "Ø90 cm",
                                                   "70×70 cm", "80×80 cm", "120×80 cm"]}],
        "price_fn": lambda t: {
            "Ø70 cm": 181.58, "Ø80 cm": 188.93, "Ø90 cm": 221.12,
            "70×70 cm": 220.24, "80×80 cm": 243.88, "120×80 cm": 315.80,
        }[t],
        "sku_fn": lambda t: f"SV-SELVA-{slug(t)}",
        "var_sku_orig_fn": lambda t: {
            "Ø70 cm":  "BALLIU_SELVA_MESA_DIAMETRO_70_WERZ_33CE1613",
            "Ø80 cm":  "BALLIU_SELVA_MESA_DIAMETRO_80_WERZ_EB565C3E",
            "Ø90 cm":  "BALLIU_SELVA_MESA_DIAMETRO_90_WERZ_871DF608",
            "70×70 cm":"BALLIU_SELVA_MESA_70_X_70_WERZALIT_7AB14C9A",
            "80×80 cm":"BALLIU_SELVA_MESA_80_X_80_WERZALIT_1A5A5005",
            "120×80 cm":"BALLIU_SELVA_MESA_120_X_80_WERZALI_747885BD",
        }[t],
        "product_metafields": mf_base(
            "Selva", "BALLIU_SELVA_MESA_*", ["jardin", "terraza", "balcon"], "l"),
    },

    # ───── 2. BRUNEI · 4 tamaños × 3 chasis × 5 HPL = 60 (ya consolidado 8v) ─────
    {
        "name": "brunei",
        "winner_handle": "balliu-mesa-exterior-aluminio-8080-cm-ef580ae2",
        "title": "Mesa exterior aluminio · HPL · Brunei",
        "envio_tag": "envio:l",
        "needs_reset_options": True,
        "options": [
            {"name": "Tamaño", "values": ["80×80 cm", "130×80 cm", "160×90 cm", "190×90 cm"]},
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda t, ch, co: {
            "80×80 cm": 478.77, "130×80 cm": 637.92, "160×90 cm": 768.74, "190×90 cm": 943.15,
        }[t],
        "sku_fn": lambda t, ch, co: f"SV-BRUNEI-{slug(t)}-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda t, ch, co: {
            "80×80 cm":  "BALLIU_BRUNEI_MESA_80X80_TABLERO_HP_EF580AE2",
            "130×80 cm": "BALLIU_BRUNEI_MESA_130X80_TABLERO_H_DF7C872B",
            "160×90 cm": "BALLIU_BRUNEI_MESA_160X90_TABLERO_H_11303F43",
            "190×90 cm": "BALLIU_BRUNEI_MESA_190X90_TABLERO_H_4D2D1E60",
        }[t],
        "product_metafields": mf_base(
            "Brunei", "BALLIU_BRUNEI_MESA_*_HPL", ["jardin", "terraza", "hosteleria"], "l"),
    },

    # ───── 3. ATLANTA extensible · 2 tamaños × 3 chasis × 5 HPL = 30 ─────
    {
        "name": "atlanta",
        "winner_handle": "balliu-mesa-exterior-140-18090-cm-e4ec7d7c",
        "title": "Mesa extensible exterior aluminio · HPL · Atlanta",
        "envio_tag": "envio:l",
        "options": [
            {"name": "Tamaño", "values": ["140/180×90 cm", "200/260×100 cm"]},
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda t, ch, co: {
            "140/180×90 cm": 1274.08, "200/260×100 cm": 1669.81,
        }[t],
        "sku_fn": lambda t, ch, co: f"SV-ATLANTA-{slug(t)}-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda t, ch, co: {
            "140/180×90 cm":   "BALLIU_ATLANTA_MESA_140_180X90_EXTEN_E4EC7D7C",
            "200/260×100 cm":  "BALLIU_ATLANTA_MESA_200_260X100_EXTE_9D798E50",
        }[t],
        "product_metafields": mf_base(
            "Atlanta", "BALLIU_ATLANTA_MESA_*_EXTEN", ["jardin", "terraza", "hosteleria"], "l"),
    },

    # ───── 4. JAVA extensible · 2 tamaños × 3 chasis × 5 HPL = 30 ─────
    {
        "name": "java",
        "winner_handle": "balliu-mesa-exterior-hpl-140-180100-cm-8e073aab",
        "title": "Mesa extensible exterior aluminio · HPL · Java",
        "envio_tag": "envio:l",
        "options": [
            {"name": "Tamaño", "values": ["140/180×100 cm", "200/260×100 cm"]},
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda t, ch, co: {
            "140/180×100 cm": 1573.34, "200/260×100 cm": 2016.97,
        }[t],
        "sku_fn": lambda t, ch, co: f"SV-JAVA-{slug(t)}-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda t, ch, co: {
            "140/180×100 cm":   "BALLIU_MESA_JAVA_140_180X100_EXTE_8E073AAB",
            "200/260×100 cm":   "BALLIU_MESA_JAVA_200_260X100_EXTE_23187EA9",
        }[t],
        "product_metafields": mf_base(
            "Java", "BALLIU_MESA_JAVA_*_EXTE", ["jardin", "terraza", "hosteleria"], "l"),
    },

    # ───── 5. CAPRI · 5 tamaños × 3 chasis × 5 HPL = 75 ─────
    {
        "name": "capri",
        "winner_handle": "balliu-mesa-exterior-aluminio-7070-cm-724b0db0",
        "title": "Mesa exterior aluminio · HPL · Capri",
        "envio_tag": "envio:l",
        "needs_reset_options": True,
        "options": [
            {"name": "Tamaño", "values": ["Ø70 cm", "Ø80 cm", "Ø90 cm", "70×70 cm", "80×80 cm"]},
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda t, ch, co: {
            "Ø70 cm": 349.19, "Ø80 cm": 387.14, "Ø90 cm": 389.84,
            "70×70 cm": 378.43, "80×80 cm": 406.34,
        }[t],
        "sku_fn": lambda t, ch, co: f"SV-CAPRI-{slug(t)}-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda t, ch, co: {
            "Ø70 cm":  "BALLIU_DIAM_70_MESA_TABLERO_HPL_451E7BA8",
            "Ø80 cm":  "BALLIU_DIAM_80_MESA_TABLERO_HPL_65E3CA13",
            "Ø90 cm":  "BALLIU_CAPRI_MESA_DIAM_90_TABLE_HP_22901F1B",
            "70×70 cm":"BALLIU_CAPRI_MESA_70X70_PIE_SIMPLE_724B0DB0",
            "80×80 cm":"BALLIU_CAPRI_MESA_80X80_PIE_SIMPLE_2A80CB3A",
        }[t],
        "product_metafields": mf_base(
            "Capri", "BALLIU_CAPRI_MESA_*_HPL", ["jardin", "terraza", "hosteleria"], "l"),
    },

    # ───── 6. CAPRI DOBLE 120×80 · 3 chasis × 5 HPL = 15 ─────
    {
        "name": "capri_doble",
        "new_handle": "mesa-exterior-aluminio-hpl-120x80-capri-doble",
        "create_new": True,
        "title": "Mesa exterior aluminio · HPL 120×80 cm · Capri Doble",
        "envio_tag": "envio:l",
        "product_type": "Mesa",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda ch, co: 531.53,
        "sku_fn": lambda ch, co: f"SV-CAPRI-DOBLE-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda ch, co: "BALLIU_CAPRI_MESA_120X80_PIE_DOBLE_5C848C82",
        "product_metafields": mf_base(
            "Capri Doble", "BALLIU_CAPRI_MESA_120X80_PIE_DOBLE_5C848C82",
            ["jardin", "terraza", "hosteleria"], "l"),
    },

    # ───── 7. ALTEA · 2 tamaños × 2 chasis × 5 HPL = 20 ─────
    # Web muestra solo HPL std. Excel solo tiene 70×70 HPL_GD y 80×80 HPL+HPL_GD.
    # Decisión dueño: precio 70×70 HPL = 421,43€ (precio mín del rango web 421,43-481,68€).
    {
        "name": "altea",
        "winner_handle": "balliu-mesa-exterior-aluminio-7070-cm-1b61e6b6",
        "title": "Mesa exterior aluminio · HPL · Altea",
        "envio_tag": "envio:l",
        "options": [
            {"name": "Tamaño", "values": ["70×70 cm", "80×80 cm"]},
            {"name": "Chasis", "values": CHASIS_ALU2},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda t, ch, co: {"70×70 cm": 421.43, "80×80 cm": 422.17}[t],
        "sku_fn": lambda t, ch, co: f"SV-ALTEA-{slug(t)}-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda t, ch, co: {
            "70×70 cm": "BALLIU_ALTEA_MESA_70_X_70_HPL_*",
            "80×80 cm": "BALLIU_ALTEA_MESA_80_X_80_HPL_A05618AD",
        }[t],
        "product_metafields": mf_base(
            "Altea", "BALLIU_ALTEA_MESA_*_HPL", ["jardin", "terraza", "hosteleria"], "l"),
    },

    # ───── 8. ÁGATA 75×75 · 2 chasis = 2 ─────
    {
        "name": "agata",
        "winner_handle": "balliu-mesa-exterior-aluminio-75-cm-dd745448",
        "title": "Mesa exterior aluminio · 75×75 cm · Ágata",
        "envio_tag": "envio:l",
        "options": [{"name": "Color", "values": ["Blanco", "Aluminio"]}],
        "price_fn": lambda c: 347.39,
        "sku_fn": lambda c: f"SV-AGATA-{slug(c)}",
        "var_sku_orig_fn": lambda c: "BALLIU_AGATA_MESA_70X70_ENCIMERA_A_DD745448",
        "product_metafields": mf_base(
            "Ágata", "BALLIU_AGATA_MESA_70X70_ENCIMERA_A_DD745448",
            ["jardin", "terraza"], "l"),
    },

    # ───── 9. NORA 72×72 · 2 chasis = 2 ─────
    {
        "name": "nora",
        "winner_handle": "balliu-mesa-exterior-aluminio-72-cm-72514f40",
        "title": "Mesa exterior aluminio · 72×72 cm · Nora",
        "envio_tag": "envio:l",
        "options": [{"name": "Color", "values": ["Blanco", "Aluminio"]}],
        "price_fn": lambda c: 224.10,
        "sku_fn": lambda c: f"SV-NORA-{slug(c)}",
        "var_sku_orig_fn": lambda c: "BALLIU_NORA_MESA_DIAMETRO_70_ALUM_72514F40",
        "product_metafields": mf_base(
            "Nora", "BALLIU_NORA_MESA_DIAMETRO_70_ALUM_72514F40",
            ["jardin", "terraza", "balcon"], "l"),
    },
]


# ─── DRAFTS — productos existentes a pasar a DRAFT con tag legacy ────────────

DRAFTS_EXISTING = [
    # Selva legacy (5 productos planos sobran tras consolidar a 1)
    ("balliu-mesa-exterior-resina-80-cm-eb565c3e", "Selva Ø80 — variante del consolidado"),
    ("balliu-mesa-exterior-resina-90-cm-871df608", "Selva Ø90 — variante del consolidado"),
    ("balliu-mesa-exterior-resina-7070-cm-7ab14c9a", "Selva 70×70 — variante del consolidado"),
    ("balliu-mesa-exterior-resina-8080-cm-1a5a5005", "Selva 80×80 — variante del consolidado"),
    ("balliu-mesa-exterior-resina-12080-cm-747885bd", "Selva 120×80 — variante del consolidado"),
    # Atlanta 240×90 (no en web)
    ("balliu-mesa-exterior-hpl-24090-cm-78358691", "Atlanta 240×90 HPL — no figura en web"),
    ("balliu-mesa-exterior-hpl-24090-cm-d4e471c5", "Atlanta 240×90 HPL GD — no figura en web"),
    ("balliu-mesa-exterior-200-260100-cm-9d798e50", "Atlanta 200/260×100 — variante del consolidado"),
    # Java legacy (3 sobran tras consolidar a 1)
    ("balliu-mesa-exterior-hpl-140-180100-cm-e5e3bb40", "Java 140/180×100 HPL GD — no figura en web"),
    ("balliu-mesa-exterior-hpl-200-260100-cm-23187ea9", "Java 200/260×100 — variante del consolidado"),
    ("balliu-mesa-exterior-hpl-200-260100-cm-4a63be2f", "Java 200/260×100 HPL GD — no figura en web"),
    # Capri legacy (4 DIAM + 1 Capri Ø90 sobran)
    ("balliu-mesa-exterior-aluminio-90-cm-22901f1b", "Capri Ø90 — variante del consolidado"),
    ("balliu-mesa-exterior-hpl-451e7ba8", "Capri Ø70 HPL — variante del consolidado"),
    ("balliu-mesa-exterior-hpl-3adfe773", "Capri Ø70 HPL GD — no figura en web"),
    ("balliu-mesa-exterior-hpl-65e3ca13", "Capri Ø80 HPL — variante del consolidado"),
    ("balliu-mesa-exterior-hpl-1b4f3962", "Capri Ø80 HPL GD — no figura en web"),
    # Altea legacy (5 sobran)
    ("balliu-mesa-exterior-aluminio-8080-cm-a05618ad", "Altea 80×80 HPL — variante del consolidado"),
    ("balliu-mesa-exterior-aluminio-8080-cm-0a3ee957", "Altea 80×80 HPL GD — no figura en web"),
    ("balliu-mesa-exterior-aluminio-80-cm-50525e0b", "Altea Ø80 HPL — no figura en web"),
    ("balliu-mesa-exterior-aluminio-80-cm-b06218ca", "Altea Ø80 HPL GD — no figura en web"),
    ("balliu-mesa-exterior-aluminio-12080-cm-bf75a33d", "Altea 120×80 HPL — no figura en web"),
    # Ágata legacy
    ("balliu-mesa-exterior-aluminio-75-cm-d7ab6e04", "Ágata 120×80 HPL GD — no figura en web"),
    ("balliu-mesa-exterior-aluminio-75-cm-c0092e17", "Ágata L 180×90 — no figura en web"),
    # Sofia (todo DRAFT, no está en web)
    ("balliu-mesa-exterior-hpl-7070-cm-9d14e31f", "Sofia 70×70 HPL — modelo no en web (Sofia)"),
    ("balliu-mesa-exterior-hpl-7070-cm-146f72ca", "Sofia 70×70 HPL — modelo no en web (Sofia)"),
    ("balliu-mesa-exterior-hpl-8080-cm-1a2fe7b5", "Sofia 80×80 HPL — modelo no en web (Sofia)"),
    ("balliu-mesa-exterior-hpl-8080-cm-96593887", "Sofia 80×80 HPL GD — modelo no en web (Sofia)"),
    ("balliu-mesa-exterior-hpl-7070-cm-f6074154", "Sofia 70×70 HPL GD — modelo no en web (Sofia)"),
]


# ─── DRAFTS nuevos — HPL Gran Densidad por modelo (pendiente confirmar) ──────

DRAFTS_NEW = [
    # Brunei HPL_GD (4 tamaños)
    {
        "name": "brunei_hpl_gd_draft",
        "new_handle": "mesa-exterior-aluminio-hpl-gd-brunei",
        "title": "Mesa exterior aluminio · HPL Gran Densidad · Brunei",
        "tags": ["Balliu", "envio:l", PENDING_TAG, LEGACY_TAG],
        "options": [{"name": "Tamaño", "values": ["80×80 cm", "130×80 cm", "160×90 cm", "190×90 cm"]}],
        "variants_data": [
            ("80×80 cm",  540.25, "BALLIU_BRUNEI_MESA_80X80_TABLERO_HP_FCE3B8BD"),
            ("130×80 cm", 737.34, "BALLIU_BRUNEI_MESA_130X80_TABLERO_H_5068224E"),
            ("160×90 cm", 892.79, "BALLIU_BRUNEI_MESA_160X90_TABLERO_H_C39E3349"),
            ("190×90 cm", 1123.45, "BALLIU_BRUNEI_MESA_190X90_TABLERO_H_7FCC116E"),
        ],
        "modelo": "Brunei (HPL GD)",
        "espacios": ["jardin", "terraza", "hosteleria"],
    },
    # Java HPL_GD (2 tamaños)
    {
        "name": "java_hpl_gd_draft",
        "new_handle": "mesa-extensible-exterior-aluminio-hpl-gd-java",
        "title": "Mesa extensible exterior aluminio · HPL Gran Densidad · Java",
        "tags": ["Balliu", "envio:l", PENDING_TAG, LEGACY_TAG],
        "options": [{"name": "Tamaño", "values": ["140/180×100 cm", "200/260×100 cm"]}],
        "variants_data": [
            ("140/180×100 cm", 1593.26, "BALLIU_MESA_JAVA_140_180X100_EXTE_E5E3BB40"),
            ("200/260×100 cm", 2296.36, "BALLIU_MESA_JAVA_200_260X100_EXTE_4A63BE2F"),
        ],
        "modelo": "Java (HPL GD)",
        "espacios": ["jardin", "terraza", "hosteleria"],
    },
    # Capri HPL_GD (5 tamaños)
    {
        "name": "capri_hpl_gd_draft",
        "new_handle": "mesa-exterior-aluminio-hpl-gd-capri",
        "title": "Mesa exterior aluminio · HPL Gran Densidad · Capri",
        "tags": ["Balliu", "envio:l", PENDING_TAG, LEGACY_TAG],
        "options": [{"name": "Tamaño", "values": ["Ø70 cm", "Ø80 cm", "Ø90 cm", "70×70 cm", "80×80 cm"]}],
        "variants_data": [
            ("Ø70 cm",  387.59, "BALLIU_DIAM_70_MESA_TABLERO_HPL_GD_3ADFE773"),
            ("Ø80 cm",  439.24, "BALLIU_DIAM_80_MESA_TABLERO_HPL_GD_1B4F3962"),
            ("Ø90 cm",  442.82, "BALLIU_CAPRI_MESA_DIAM_90_TABLE_HP_6C6DFD1C"),
            ("70×70 cm",432.27, "BALLIU_CAPRI_MESA_70X70_PIE_SIMPLE_A0A23F40"),
            ("80×80 cm",426.10, "BALLIU_CAPRI_MESA_80X80_PIE_SIMPLE_8CA835FF"),
        ],
        "modelo": "Capri (HPL GD)",
        "espacios": ["jardin", "terraza", "hosteleria"],
    },
    # Capri Doble HPL_GD + pie alto (3 variantes)
    {
        "name": "capri_doble_extras_draft",
        "new_handle": "mesa-exterior-aluminio-hpl-gd-120x80-capri-doble",
        "title": "Mesa exterior aluminio · HPL GD / pie alto · Capri Doble 120×80",
        "tags": ["Balliu", "envio:l", PENDING_TAG, LEGACY_TAG],
        "options": [{"name": "Tablero/Pie", "values": [
            "HPL Gran Densidad", "HPL pie alto", "HPL Gran Densidad pie alto"]}],
        "variants_data": [
            ("HPL Gran Densidad",       622.93, "BALLIU_CAPRI_MESA_120X80_PIE_DOBLE_798DCADF"),
            ("HPL pie alto",            605.18, "BALLIU_CAPRI_MESA_120X80_PIE_DOBLE_3C3BF077"),
            ("HPL Gran Densidad pie alto", 666.49, "BALLIU_CAPRI_MESA_120X80_PIE_DOBLE_05C442CF"),
        ],
        "modelo": "Capri Doble (extras)",
        "espacios": ["jardin", "terraza", "hosteleria"],
    },
    # Altea variantes restantes (5)
    {
        "name": "altea_extras_draft",
        "new_handle": "mesa-exterior-aluminio-altea-extras",
        "title": "Mesa exterior aluminio · variantes extras · Altea",
        "tags": ["Balliu", "envio:l", PENDING_TAG, LEGACY_TAG],
        "options": [{"name": "Configuración", "values": [
            "70×70 HPL Gran Densidad", "80×80 HPL Gran Densidad",
            "Ø80 HPL", "Ø80 HPL Gran Densidad", "120×80 HPL"]}],
        "variants_data": [
            ("70×70 HPL Gran Densidad", 480.94, "BALLIU_ALTEA_MESA_70_X_70_HPL_GD_1B61E6B6"),
            ("80×80 HPL Gran Densidad", 481.68, "BALLIU_ALTEA_MESA_80_X_80_HPL_GD_0A3EE957"),
            ("Ø80 HPL",                 381.97, "BALLIU_ALTEA_MESA_DIAM_80_HPL_50525E0B"),
            ("Ø80 HPL Gran Densidad",   392.86, "BALLIU_ALTEA_MESA_DIAM_80_HPL_GD_B06218CA"),
            ("120×80 HPL",              673.68, "BALLIU_ALTEA_MESA_120_X_80_HPL_BF75A33D"),
        ],
        "modelo": "Altea (extras)",
        "espacios": ["jardin", "terraza", "hosteleria"],
    },
    # Ágata variantes restantes (2)
    {
        "name": "agata_extras_draft",
        "new_handle": "mesa-exterior-aluminio-agata-extras",
        "title": "Mesa exterior aluminio · variantes extras · Ágata",
        "tags": ["Balliu", "envio:l", PENDING_TAG, LEGACY_TAG],
        "options": [{"name": "Configuración", "values": [
            "120×80 HPL Gran Densidad", "180×90 encimera aluminio"]}],
        "variants_data": [
            ("120×80 HPL Gran Densidad",   686.15, "BALLIU_AGATA_MESA_120_X_80_HPL_GD_D7AB6E04"),
            ("180×90 encimera aluminio",   504.03, "BALLIU_AGATA_MESA_180_X_90_ENCIMER_C0092E17"),
        ],
        "modelo": "Ágata L (extras)",
        "espacios": ["jardin", "terraza"],
    },
]


# ─── EXPAND VARIANTS ──────────────────────────────────────────────────────────

def expand_variants(product: dict) -> list[dict]:
    from itertools import product as iproduct
    option_names = [o["name"] for o in product["options"]]
    option_values = [o["values"] for o in product["options"]]
    out = []
    for combo in iproduct(*option_values):
        opts = dict(zip(option_names, combo))
        price = product["price_fn"](*combo)
        sku = product["sku_fn"](*combo)
        sku_orig = product["var_sku_orig_fn"](*combo)
        out.append({
            "option_values": opts,
            "price": round(price, 2),
            "sku": sku,
            "metafields": mf_variant(sku_orig),
        })
    return out


# ─── SHOPIFY OPS ──────────────────────────────────────────────────────────────

def backup_products(token: str, handles: list[str]) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = BACKUP_DIR / f"mesas_comedor_{timestamp}.json"
    snap = []
    print(f"📦 Backup de {len(handles)} productos en {out_path.name}…")
    for h in handles:
        try:
            r = gql(token, '''query($h:String!){productByHandle(handle:$h){
                id handle title status tags
                variants(first:100){edges{node{id sku price selectedOptions{name value}}}}
                options{name values}
            }}''', {"h": h})
            p = r.get("productByHandle")
            if p: snap.append(p); print(f"   ✓ {h}")
            else: print(f"   · {h} no encontrado")
        except Exception as e:
            print(f"   ✗ {h}: {e}")
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
    return out_path


def find_product(token: str, handle: str) -> dict | None:
    r = gql(token, '''query($h:String!){productByHandle(handle:$h){
        id handle status tags
        options{id name optionValues{id name}}
        variants(first:100){edges{node{id title}}}
    }}''', {"h": handle})
    return r.get("productByHandle")


def update_product(token, pid, *, title=None, tags=None, product_metafields=None, status=None):
    inp = {"id": pid}
    if title is not None: inp["title"] = title
    if tags is not None: inp["tags"] = tags
    if product_metafields: inp["metafields"] = product_metafields
    if status: inp["status"] = status
    r = gql(token, 'mutation($input:ProductInput!){productUpdate(input:$input){product{id} userErrors{field message}}}',
            {"input": inp})
    return r["productUpdate"]["userErrors"]


def reset_options(token: str, prod: dict) -> list:
    r = gql(token, '''query($id:ID!){product(id:$id){
        variants(first:100){edges{node{id}}}
        options{id name}
    }}''', {"id": prod["id"]})
    p = r["product"]
    v_ids = [e["node"]["id"] for e in p["variants"]["edges"]]
    errs = []
    if len(v_ids) > 1:
        d = gql(token, '''mutation($pid:ID!,$ids:[ID!]!){
            productVariantsBulkDelete(productId:$pid, variantsIds:$ids){userErrors{field message}}
        }''', {"pid": prod["id"], "ids": v_ids[1:]})
        if d["productVariantsBulkDelete"]["userErrors"]:
            errs += d["productVariantsBulkDelete"]["userErrors"]
    if p["options"]:
        opt_ids = [o["id"] for o in p["options"]]
        d = gql(token, '''mutation($pid:ID!,$ids:[ID!]!){
            productOptionsDelete(productId:$pid, options:$ids, strategy:POSITION){
                userErrors{field message code}
            }
        }''', {"pid": prod["id"], "ids": opt_ids})
        if d["productOptionsDelete"]["userErrors"]:
            errs += d["productOptionsDelete"]["userErrors"]
    return errs


def create_options(token, pid, options):
    opts_input = [{"name": o["name"], "values": [{"name": v} for v in o["values"]]} for o in options]
    r = gql(token, '''mutation($pid:ID!,$opts:[OptionCreateInput!]!){
        productOptionsCreate(productId:$pid, options:$opts){userErrors{field message code}}
    }''', {"pid": pid, "opts": opts_input})
    return r["productOptionsCreate"]["userErrors"]


def create_variants(token, pid, variants):
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


def create_product_new(token, p, status="ACTIVE"):
    inp = {"title": p["title"], "handle": p.get("new_handle"),
           "productType": p.get("product_type", "Mesa"), "status": status,
           "tags": p.get("tags", [])}
    if p.get("product_metafields"): inp["metafields"] = p["product_metafields"]
    r = gql(token, 'mutation($input:ProductInput!){productCreate(input:$input){product{id handle} userErrors{field message}}}',
            {"input": inp})
    errs = r["productCreate"]["userErrors"]
    if errs: return None, errs
    return r["productCreate"]["product"]["id"], []


def publish_product(token, pid):
    r = gql(token, '''mutation($id:ID!,$input:[PublicationInput!]!){
        publishablePublish(id:$id, input:$input){userErrors{field message}}
    }''', {"id": pid, "input": [{"publicationId": ONLINE_STORE_PUB}, {"publicationId": SHOP_PUB}]})
    return r["publishablePublish"]["userErrors"]


def clean_tags(current, envio_tag=None, *, legacy=False, pending=False):
    new = [t for t in current if not t.startswith("envio:")
           and t not in ("match-rojo", "match-verde", "match-amarillo")]
    if envio_tag: new.append(envio_tag)
    if legacy and LEGACY_TAG not in new: new.append(LEGACY_TAG)
    if pending and PENDING_TAG not in new: new.append(PENDING_TAG)
    seen, out = set(), []
    for t in new:
        if t not in seen: seen.add(t); out.append(t)
    return out


# ─── ORQUESTACIÓN ─────────────────────────────────────────────────────────────

def process_consolidado(token, p, dry, results):
    variants = expand_variants(p)
    print(f"\n▶ {p['name']} — {p['title']}")
    print(f"   plan: {len(variants)} variantes")
    if dry:
        for v in variants[:3]:
            print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
        if len(variants) > 3: print(f"     · …y {len(variants)-3} más")
        results.append({"name": p["name"], "title": p["title"], "status": "DRY_RUN",
                        "n_variants": len(variants)})
        return

    if p.get("create_new"):
        existing = find_product(token, p["new_handle"]) if p.get("new_handle") else None
        if existing:
            print(f"   · ya existía: {existing['id']}"); pid = existing["id"]
        else:
            inp = {"title": p["title"], "handle": p.get("new_handle"),
                   "productType": p.get("product_type", "Mesa"), "status": "ACTIVE",
                   "tags": [p.get("envio_tag", "envio:l"), "Balliu"]}
            if p.get("product_metafields"): inp["metafields"] = p["product_metafields"]
            r = gql(token, 'mutation($input:ProductInput!){productCreate(input:$input){product{id handle} userErrors{field message}}}',
                    {"input": inp})
            errs = r["productCreate"]["userErrors"]
            if errs:
                print(f"   ✗ create: {errs}")
                results.append({"name": p["name"], "status": "ERROR_CREATE", "errors": str(errs)})
                return
            pid = r["productCreate"]["product"]["id"]
            print(f"   ✓ creado: {pid}")
    else:
        winner = find_product(token, p["winner_handle"])
        if not winner:
            print(f"   ✗ winner no encontrado")
            results.append({"name": p["name"], "status": "ERROR", "errors": "winner no encontrado"})
            return
        pid = winner["id"]
        if p.get("needs_reset_options"):
            legacy_opts = [o for o in (winner.get("options") or []) if o["name"] != "Title"]
            if legacy_opts:
                print(f"   · resetear opciones legacy: {[o['name'] for o in legacy_opts]}")
                errs = reset_options(token, winner)
                if errs:
                    print(f"   ✗ reset: {errs}")
                    results.append({"name": p["name"], "status": "ERROR_RESET", "errors": str(errs)})
                    return
        tags = clean_tags(winner["tags"], p["envio_tag"])
        errs = update_product(token, pid, title=p["title"], tags=tags,
                              product_metafields=p["product_metafields"], status="ACTIVE")
        if errs:
            print(f"   ✗ update: {errs}")
            results.append({"name": p["name"], "status": "ERROR_UPDATE", "errors": str(errs)})
            return

    errs = create_options(token, pid, p["options"])
    if errs:
        msgs = " ".join(e.get("message", "") for e in errs).lower()
        if not ("already" in msgs or "exists" in msgs):
            print(f"   ✗ options: {errs}")
            results.append({"name": p["name"], "status": "ERROR_OPTIONS", "errors": str(errs)})
            return
        print("   · options ya existían")

    errs = create_variants(token, pid, variants)
    if errs:
        print(f"   ✗ variants: {errs[:2]}")
        results.append({"name": p["name"], "status": "ERROR_VARIANTS", "errors": str(errs)[:300]})
        return

    print(f"   ✓ {len(variants)} variantes")
    results.append({"name": p["name"], "title": p["title"], "status": "OK",
                    "product_id": pid, "n_variants": len(variants)})


def process_drafts_existing(token, dry, results):
    print("\n─── Pasar a DRAFT productos planos legacy ───")
    for h, reason in DRAFTS_EXISTING:
        print(f"\n▶ DRAFT — {h}  ({reason})")
        if dry:
            results.append({"name": h, "title": reason, "status": "DRY_DRAFT"})
            continue
        prod = find_product(token, h)
        if not prod:
            print("   · no encontrado"); results.append({"name": h, "status": "MISSING"}); continue
        tags = clean_tags(prod["tags"], None, legacy=True)
        errs = update_product(token, prod["id"], tags=tags, status="DRAFT")
        if errs:
            print(f"   ✗ {errs}")
            results.append({"name": h, "status": "ERROR_DRAFT", "errors": str(errs)})
        else:
            print("   ✓ pasado a DRAFT")
            results.append({"name": h, "status": "DRAFTED"})


def process_drafts_new(token, dry, results):
    print("\n─── Crear productos DRAFT nuevos (HPL_GD / extras por modelo) ───")
    for d in DRAFTS_NEW:
        print(f"\n▶ DRAFT NEW — {d['name']}: {d['title']}")
        print(f"   handle: {d['new_handle']}  · {len(d['variants_data'])} variante(s)")
        if dry:
            for opt_val, price, _ in d["variants_data"]:
                print(f"     · {opt_val}  {price}€")
            results.append({"name": d["name"], "title": d["title"], "status": "DRY_RUN",
                            "n_variants": len(d["variants_data"])})
            continue
        existing = find_product(token, d["new_handle"])
        if existing:
            print(f"   · ya existía: {existing['id']}"); pid = existing["id"]
        else:
            p_create = {
                "title": d["title"], "new_handle": d["new_handle"],
                "tags": d["tags"], "product_type": "Mesa",
                "product_metafields": mf_base(d["modelo"], d["variants_data"][0][2], d["espacios"], "l"),
            }
            pid, errs = create_product_new(token, p_create, status="DRAFT")
            if errs:
                print(f"   ✗ create: {errs}")
                results.append({"name": d["name"], "status": "ERROR_CREATE", "errors": str(errs)})
                continue
            print(f"   ✓ creado DRAFT: {pid}")
        errs = create_options(token, pid, d["options"])
        if errs:
            msgs = " ".join(e.get("message", "") for e in errs).lower()
            if not ("already" in msgs or "exists" in msgs):
                print(f"   ✗ options: {errs}")
                results.append({"name": d["name"], "status": "ERROR_OPTIONS", "errors": str(errs)})
                continue
        opt_name = d["options"][0]["name"]
        variants = [{
            "option_values": {opt_name: opt_val},
            "price": price,
            "sku": f"SV-{d['name'].upper().replace('_DRAFT','')}-{slug(opt_val)}"[:50],
            "metafields": mf_variant(sku_orig),
        } for opt_val, price, sku_orig in d["variants_data"]]
        errs = create_variants(token, pid, variants)
        if errs:
            print(f"   ✗ variants: {errs[:2]}")
            results.append({"name": d["name"], "status": "ERROR_VARIANTS", "errors": str(errs)[:300]})
            continue
        print(f"   ✓ {len(variants)} variante(s) DRAFT")
        results.append({"name": d["name"], "title": d["title"], "status": "OK_DRAFT",
                        "product_id": pid, "n_variants": len(variants)})


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--only", help="Procesar solo este producto consolidado")
    parser.add_argument("--skip-publish", action="store_true")
    parser.add_argument("--skip-backup", action="store_true")
    parser.add_argument("--skip-drafts", action="store_true")
    args = parser.parse_args()

    dry = not args.apply
    print("════ MODO DRY-RUN ════\n" if dry else "════ MODO APPLY ════\n")

    targets = PRODUCTS
    if args.only:
        targets = [p for p in PRODUCTS if p["name"] == args.only]
        if not targets:
            sys.exit(f"✗ no existe producto con name={args.only}")

    token = read_token()

    if not dry and not args.skip_backup:
        handles = ([p.get("winner_handle") for p in targets if p.get("winner_handle")]
                   + [h for h, _ in DRAFTS_EXISTING])
        backup_products(token, [h for h in handles if h])

    results: list[dict] = []
    for p in targets:
        process_consolidado(token, p, dry, results)

    if not args.only and not args.skip_drafts:
        process_drafts_existing(token, dry, results)
        process_drafts_new(token, dry, results)

    if not dry and not args.skip_publish:
        print("\n─── Publicar consolidados ACTIVE ───")
        for r in results:
            if r.get("status") == "OK" and r.get("product_id"):
                errs = publish_product(token, r["product_id"])
                print(f"   {'✓' if not errs else '✗'} {r['name']}: {errs or ''}")
                time.sleep(0.3)

    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        cols = ["name", "title", "status", "n_variants", "product_id", "errors"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in results:
            w.writerow({c: r.get(c, "") for c in cols})
    print(f"\n✓ Reporte: {REPORT_CSV}")


if __name__ == "__main__":
    main()
