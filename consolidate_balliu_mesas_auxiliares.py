#!/usr/bin/env python3
"""
consolidate_balliu_mesas_auxiliares.py

Sub-piloto 3d · Familia 3 (Mesas) — Mesa auxiliar.

7 productos ACTIVE consolidados + 5 productos DRAFT (duplicados Prestige, HPL_GD,
Werzalit, Olimpia Esquinera, Greta).

Decisiones del dueño (2026-05-17):
  - Patrón "Blanco / Prestige" para Eva Pro Mini/BCN, Noa aux, Mini Mesa:
    Blanco más barato; resto de colores = precio Prestige.
  - Olimpia aux tela: precio Excel (157,63 €), no precio web.
  - Naming refinado: Opción C + sufijo " · <Modelo>" para identificar.
  - HPL Gran Densidad y Werzalit no figuran en web actual → DRAFT.
  - Olimpia Esquinera no figura en web → DRAFT.
  - Mesa Greta no figura en web → DRAFT.

Modos: --dry-run (default), --apply, --only NAME, --skip-publish, --skip-backup.
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
REPORT_CSV = BASE / "consolidate_balliu_mesas_auxiliares_report.csv"

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"

ONLINE_STORE_PUB = "gid://shopify/Publication/317589619012"
SHOP_PUB         = "gid://shopify/Publication/317589717316"

PAUSE_THRESHOLD = 200
PAUSE_SECONDS = 2.0
LEGACY_TAG = "legacy-balliu-consolidado-2026-05"


# ─── HELPERS ──────────────────────────────────────────────────────────────────

COLOR_SLUGS = {
    "Tórtola": "TORTOLA",
    "Gris oscuro": "GRIS-OSC",
    "Gris Oscuro": "GRIS-OSC",
    "Verde claro": "VERDE-CLARO",
    "Verde oscuro": "VERDE-OSC",
    "Azul celeste": "AZUL-CEL",
    "Azul marino": "AZUL-MAR",
    "Azul acero": "AZUL-ACERO",
    "Marrón oscuro": "MARRON-OSC",
}


def slug(text: str) -> str:
    if text in COLOR_SLUGS:
        return COLOR_SLUGS[text]
    s = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode()
    s = s.upper().replace('(', '').replace(')', '').replace(' ', '-')
    s = re.sub(r'-+', '-', s).strip('-')
    return s


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
            req = urllib.request.Request(
                API, data=payload,
                headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
            )
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
                time.sleep(float(e.headers.get("Retry-After", 2)))
                continue
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            last_err = str(e)
        time.sleep(1.5 * attempt)
    raise RuntimeError(f"GraphQL falló: {last_err}")


# ─── METAFIELDS ───────────────────────────────────────────────────────────────

def mf_base(modelo: str, sku_orig: str, espacios: list[str], envio: str = "m"):
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
    return [
        {"namespace": "santavila", "key": "proveedor_sku_original",
         "type": "single_line_text_field", "value": sku_orig},
    ]


# ─── CONSTANTES DE OPCIONES ───────────────────────────────────────────────────

SERIE_00_FULL = ["Azul", "Amarillo", "Naranja", "Verde claro", "Blanco",
                 "Natural", "Capuchino", "Caqui", "Marrón oscuro", "Arena",
                 "Verde oscuro", "Azul celeste", "Ceniza", "Azul marino",
                 "Gris oscuro", "Azul acero"]
CHASIS_ALU3 = ["Blanco", "Tórtola", "Aluminio"]
COLORES_HPL = ["Gris", "Blanco", "Moonwalk", "Skyline", "Prado"]

# Modelos resina (Blanco vs Prestige según color)
COLORES_EVA_PRO = ["Blanco", "Arena", "Bronce", "Gris oscuro", "Tórtola"]
COLORES_NOA = ["Antracita", "Arena", "Blanco", "Madera", "Tórtola"]
COLORES_MINI = ["Blanco", "Arena", "Bronce", "Gris oscuro", "Madera"]


def precio_blanco_o_prestige(color, blanco_p, prestige_p):
    return blanco_p if color == "Blanco" else prestige_p


# ─── PRODUCTOS CONSOLIDADOS (ACTIVE) ──────────────────────────────────────────

PRODUCTS: list[dict] = [
    # 1. Eva Pro Mini
    {
        "name": "eva_pro_mini",
        "winner_handle": "balliu-mesa-auxiliar-exterior-resina-48-cm-de421a42",
        "title": "Mesa auxiliar exterior resina · 48×48 cm · Eva Pro Mini",
        "envio_tag": "envio:m",
        "options": [{"name": "Color", "values": COLORES_EVA_PRO}],
        "price_fn": lambda color: precio_blanco_o_prestige(color, 33.43, 34.41),
        "sku_fn": lambda color: f"SV-EVAPROMINI-{slug(color)}",
        "var_sku_orig_fn": lambda color: (
            "BALLIU_EVA_PRO_MINI_MESA_AU_COLOR_BLANCO_DE421A42" if color == "Blanco"
            else "BALLIU_EVA_PRO_MINI_MESA_AU_COLOR_NATURAL_PR_911A77BA"
        ),
        "product_metafields": mf_base(
            "Eva Pro Mini",
            "BALLIU_EVA_PRO_MINI_MESA_AU_*_DE421A42/911A77BA",
            ["terraza", "balcon", "piscina"],
            "m",
        ),
    },
    # 2. Eva Pro BCN
    {
        "name": "eva_pro_bcn",
        "winner_handle": "balliu-mesa-auxiliar-exterior-resina-48-cm-35554775",
        "title": "Mesa auxiliar exterior resina · 48×48 cm · Eva Pro BCN",
        "envio_tag": "envio:m",
        "options": [{"name": "Color", "values": COLORES_EVA_PRO}],
        "price_fn": lambda color: precio_blanco_o_prestige(color, 35.99, 37.79),
        "sku_fn": lambda color: f"SV-EVAPROBCN-{slug(color)}",
        "var_sku_orig_fn": lambda color: (
            "BALLIU_EVA_PRO_BCN_MESA_AUX_COLOR_BLANCO_35554775" if color == "Blanco"
            else "BALLIU_EVA_PRO_BCN_MESA_AUX_COLOR_NATURAL_PR_25CD2EDE"
        ),
        "product_metafields": mf_base(
            "Eva Pro BCN",
            "BALLIU_EVA_PRO_BCN_MESA_AUX_*_35554775/25CD2EDE",
            ["terraza", "balcon", "piscina"],
            "m",
        ),
    },
    # 3. Olimpia aux tela (Chasis × Color tejido = 48 variantes)
    {
        "name": "olimpia_aux_tela",
        "winner_handle": "balliu-mesa-auxiliar-exterior-aluminio-54-cm-6c7a42d9",
        "title": "Mesa auxiliar exterior aluminio · 48×48 cm tejido · Olimpia",
        "envio_tag": "envio:m",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda chasis, color: 157.63,
        "sku_fn": lambda chasis, color: f"SV-OLIMPIAAUX-{slug(chasis)}-{slug(color)}",
        "var_sku_orig_fn": lambda chasis, color: "BALLIU_OLIMPIA_MESA_AUXILIA_TELA_BALLIU_6C7A42D9",
        "product_metafields": mf_base(
            "Olimpia Mesa Auxiliar",
            "BALLIU_OLIMPIA_MESA_AUXILIA_TELA_BALLIU_6C7A42D9",
            ["terraza", "jardin", "piscina", "hosteleria"],
            "m",
        ),
    },
    # 4. Olimpia aux CENTRAL HPL standard (Chasis × Color tablero = 15)
    {
        "name": "olimpia_central_hpl",
        "winner_handle": "balliu-mesa-auxiliar-exterior-aluminio-54-cm-19d3d0ee",
        "title": "Mesa de centro exterior · aluminio HPL 74×54 cm · Olimpia Central",
        "envio_tag": "envio:m",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda chasis, color: 227.18,
        "sku_fn": lambda chasis, color: f"SV-OLIMPIACENTRAL-{slug(chasis)}-{slug(color)}",
        "var_sku_orig_fn": lambda chasis, color: "BALLIU_OLIMPIA_MESA_AUXILIA_CENTRAL_TABLERO__19D3D0EE",
        "product_metafields": mf_base(
            "Olimpia Mesa Central",
            "BALLIU_OLIMPIA_MESA_AUXILIA_CENTRAL_TABLERO__19D3D0EE",
            ["terraza", "jardin", "piscina", "hosteleria"],
            "m",
        ),
    },
    # 5. Noa aux (Color = 5)
    {
        "name": "noa_aux",
        "winner_handle": "balliu-mesa-auxiliar-exterior-aluminio-90b11e5b",
        "title": "Mesa auxiliar exterior aluminio · Ø42 cm · Noa",
        "envio_tag": "envio:m",
        "options": [{"name": "Color", "values": COLORES_NOA}],
        "price_fn": lambda color: precio_blanco_o_prestige(color, 130.24, 136.98),
        "sku_fn": lambda color: f"SV-NOAUX-{slug(color)}",
        "var_sku_orig_fn": lambda color: (
            "BALLIU_NOA_MESA_AUXILIAR_COLOR_BLANCO_90B11E5B" if color == "Blanco"
            else "BALLIU_NOA_MESA_AUXILIAR_COLOR_NATURAL_PR_27CE9446"
        ),
        "product_metafields": mf_base(
            "Noa Mesa Auxiliar",
            "BALLIU_NOA_MESA_AUXILIAR_*_90B11E5B/27CE9446",
            ["jardin", "piscina", "atico"],
            "m",
        ),
    },
    # 6. Etna aux HPL standard — 15 variantes. Werzalit y HPL_GD se sacan a DRAFT.
    {
        "name": "etna_aux_hpl",
        "winner_handle": "balliu-mesa-auxiliar-exterior-aluminio-60-cm-9c991818",
        "title": "Mesa auxiliar exterior · aluminio HPL 45×45 cm · Etna",
        "envio_tag": "envio:m",
        "needs_reset_options": True,  # ya tiene opción "Tablero" con 3 valores
        "options": [
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tablero", "values": COLORES_HPL},
        ],
        "price_fn": lambda chasis, color: 167.00,
        "sku_fn": lambda chasis, color: f"SV-ETNAUX-{slug(chasis)}-{slug(color)}",
        "var_sku_orig_fn": lambda chasis, color: "BALLIU_ETNA_MESA_AUXILIAR_TABLERO_HPL_C5331CE8",
        "product_metafields": mf_base(
            "Etna Mesa Auxiliar",
            "BALLIU_ETNA_MESA_AUXILIAR_TABLERO_HPL_C5331CE8",
            ["terraza", "jardin", "hosteleria"],
            "m",
        ),
    },
    # 7. Mini Mesa (Mini Prestige) — Color = 5
    {
        "name": "mini_prestige",
        "winner_handle": "balliu-mesa-exterior-5d0fb586",
        "title": "Mesa auxiliar exterior resina decorativa · 48×48 cm · Mini Prestige",
        "envio_tag": "envio:m",  # OJO: estaba con envio:l, lo corregimos
        "options": [{"name": "Color", "values": COLORES_MINI}],
        "price_fn": lambda color: precio_blanco_o_prestige(color, 27.66, 29.17),
        "sku_fn": lambda color: f"SV-MINIPRESTIGE-{slug(color)}",
        "var_sku_orig_fn": lambda color: (
            "BALLIU_MINI_MESA_COLOR_BLANCO_5D0FB586" if color == "Blanco"
            else "BALLIU_MINI_MESA_COLOR_NATURAL_PR_1CF4D3D5"
        ),
        "product_metafields": mf_base(
            "Mini Prestige",
            "BALLIU_MINI_MESA_*_5D0FB586/1CF4D3D5",
            ["terraza", "balcon"],
            "m",
        ),
    },
]


# ─── DRAFTS — productos existentes a pasar a DRAFT con tag legacy ────────────

DRAFTS_EXISTING = [
    {"handle": "balliu-mesa-auxiliar-exterior-resina-48-cm-911a77ba",
     "reason": "Duplicado Eva Pro Mini Prestige — consolidado en winner"},
    {"handle": "balliu-mesa-auxiliar-exterior-resina-48-cm-25cd2ede",
     "reason": "Duplicado Eva Pro BCN Prestige — consolidado en winner"},
    {"handle": "balliu-mesa-auxiliar-exterior-aluminio-54-cm-9e2a2ecb",
     "reason": "Olimpia Central HPL Gran Densidad — no figura en web del proveedor"},
    {"handle": "balliu-mesa-auxiliar-exterior-aluminio-54-cm-5ad43bf2",
     "reason": "Olimpia Esquinera HPL — no figura en web del proveedor"},
    {"handle": "balliu-mesa-auxiliar-exterior-aluminio-54-cm-2ad5a2df",
     "reason": "Olimpia Esquinera HPL GD — no figura en web del proveedor"},
    {"handle": "balliu-mesa-auxiliar-exterior-aluminio-27ce9446",
     "reason": "Duplicado Noa Prestige — consolidado en winner"},
    {"handle": "balliu-mesa-exterior-aluminio-9e30ca7f",
     "reason": "Mesa Greta — no figura en web del proveedor"},
    {"handle": "balliu-mesa-exterior-1cf4d3d5",
     "reason": "Duplicado Mini Prestige Prestige — consolidado en winner"},
]


# ─── DRAFTS NUEVOS — Etna aux Werzalit y HPL_GD ──────────────────────────────

DRAFTS_NEW = [
    {
        "name": "etna_aux_hpl_gd_draft",
        "new_handle": "mesa-auxiliar-exterior-aluminio-hpl-gd-45x45-etna",
        "title": "Mesa auxiliar exterior · aluminio HPL Gran Densidad 45×45 cm · Etna",
        "tags": ["Balliu", "envio:m", "pendiente-confirmar-proveedor", LEGACY_TAG],
        "options": [{"name": "Tablero", "values": ["HPL Gran Densidad"]}],
        "variants": [{
            "option_values": {"Tablero": "HPL Gran Densidad"},
            "price": 175.06,
            "sku": "SV-ETNAUX-HPL-GD",
            "metafields": mf_variant("BALLIU_ETNA_MESA_AUXILIAR_TABLERO_HPL_GD_7664D255"),
        }],
        "product_metafields": mf_base(
            "Etna Mesa Auxiliar (HPL GD)",
            "BALLIU_ETNA_MESA_AUXILIAR_TABLERO_HPL_GD_7664D255",
            ["terraza", "jardin", "hosteleria"],
            "m",
        ),
    },
    {
        "name": "etna_aux_werzalit_draft",
        "new_handle": "mesa-auxiliar-exterior-aluminio-werzalit-60-etna",
        "title": "Mesa auxiliar exterior · aluminio Werzalit Ø60 cm · Etna",
        "tags": ["Balliu", "envio:m", "pendiente-confirmar-proveedor", LEGACY_TAG],
        "options": [{"name": "Tablero", "values": ["Werzalit Ø60"]}],
        "variants": [{
            "option_values": {"Tablero": "Werzalit Ø60"},
            "price": 157.84,
            "sku": "SV-ETNAUX-WERZALIT-60",
            "metafields": mf_variant("BALLIU_ETNA_MESA_AUXILIAR_DIAMETRO_60_WERZ_9C991818"),
        }],
        "product_metafields": mf_base(
            "Etna Mesa Auxiliar (Werzalit Ø60)",
            "BALLIU_ETNA_MESA_AUXILIAR_DIAMETRO_60_WERZ_9C991818",
            ["terraza", "jardin", "hosteleria"],
            "m",
        ),
    },
]


# ─── COMBINACIONES ────────────────────────────────────────────────────────────

def expand_variants(product: dict) -> list[dict]:
    from itertools import product as iproduct
    option_names = [o["name"] for o in product["options"]]
    option_values = [o["values"] for o in product["options"]]
    out = []
    for combo in iproduct(*option_values):
        opts = dict(zip(option_names, combo))
        price = product["price_fn"](*combo)
        sku = product["sku_fn"](*combo)
        var_sku_orig = product["var_sku_orig_fn"](*combo)
        out.append({
            "option_values": opts,
            "price": round(price, 2),
            "sku": sku,
            "metafields": mf_variant(var_sku_orig),
        })
    return out


# ─── SHOPIFY OPS ──────────────────────────────────────────────────────────────

def backup_products(token: str, handles: list[str]) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = BACKUP_DIR / f"mesas_auxiliares_{timestamp}.json"
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
            if p:
                snap.append(p); print(f"   ✓ {h}")
            else:
                print(f"   · {h} no encontrado")
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
    """Borra todas las variantes salvo 1 y todas las opciones existentes."""
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


def create_options(token: str, pid: str, options: list[dict]):
    opts_input = [{"name": o["name"], "values": [{"name": v} for v in o["values"]]} for o in options]
    r = gql(token, '''mutation($pid:ID!,$opts:[OptionCreateInput!]!){
        productOptionsCreate(productId:$pid, options:$opts){userErrors{field message code}}
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


def create_product_new(token: str, p: dict, status: str = "DRAFT"):
    inp = {"title": p["title"], "handle": p.get("new_handle"),
           "productType": p.get("product_type", "Mesa"), "status": status,
           "tags": p.get("tags", [])}
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


def clean_tags(current: list[str], envio_tag: str | None, *, legacy: bool = False) -> list[str]:
    new = [t for t in current if not t.startswith("envio:")
           and t not in ("match-rojo", "match-verde", "match-amarillo")]
    if envio_tag: new.append(envio_tag)
    if legacy and LEGACY_TAG not in new: new.append(LEGACY_TAG)
    seen, out = set(), []
    for t in new:
        if t not in seen: seen.add(t); out.append(t)
    return out


# ─── ORQUESTACIÓN ─────────────────────────────────────────────────────────────

def process_consolidado(token: str, p: dict, dry: bool, results: list):
    variants = expand_variants(p)
    print(f"\n▶ {p['name']} — {p['title']}")
    print(f"   plan: {len(variants)} variantes en winner={p['winner_handle']}")
    if dry:
        for v in variants[:3]:
            print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
        if len(variants) > 3: print(f"     · …y {len(variants)-3} más")
        results.append({"name": p["name"], "title": p["title"], "status": "DRY_RUN",
                        "n_variants": len(variants)})
        return

    winner = find_product(token, p["winner_handle"])
    if not winner:
        print(f"   ✗ winner no encontrado")
        results.append({"name": p["name"], "status": "ERROR", "errors": "winner no encontrado"})
        return
    pid = winner["id"]

    # Reset opciones legacy si toca
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


def process_drafts_existing(token: str, dry: bool, results: list):
    print("\n─── Pasar a DRAFT productos existentes ───")
    for d in DRAFTS_EXISTING:
        h = d["handle"]
        print(f"\n▶ DRAFT — {h}  ({d['reason']})")
        if dry:
            results.append({"name": h, "title": d["reason"], "status": "DRY_DRAFT"})
            continue
        prod = find_product(token, h)
        if not prod:
            print("   · no encontrado")
            results.append({"name": h, "status": "MISSING"})
            continue
        tags = clean_tags(prod["tags"], None, legacy=True)
        errs = update_product(token, prod["id"], tags=tags, status="DRAFT")
        if errs:
            print(f"   ✗ {errs}")
            results.append({"name": h, "status": "ERROR_DRAFT", "errors": str(errs)})
        else:
            print("   ✓ pasado a DRAFT")
            results.append({"name": h, "status": "DRAFTED"})


def process_drafts_new(token: str, dry: bool, results: list):
    print("\n─── Crear productos DRAFT nuevos (Etna Werzalit / HPL_GD) ───")
    for p in DRAFTS_NEW:
        print(f"\n▶ DRAFT NEW — {p['name']}: {p['title']}")
        print(f"   handle: {p['new_handle']}  · {len(p['variants'])} variante(s)")
        if dry:
            for v in p["variants"]:
                print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
            results.append({"name": p["name"], "title": p["title"], "status": "DRY_RUN",
                            "n_variants": len(p["variants"])})
            continue
        existing = find_product(token, p["new_handle"])
        if existing:
            print(f"   · ya existía: {existing['id']}")
            pid = existing["id"]
        else:
            pid, errs = create_product_new(token, p, status="DRAFT")
            if errs:
                print(f"   ✗ create: {errs}")
                results.append({"name": p["name"], "status": "ERROR_CREATE", "errors": str(errs)})
                continue
            print(f"   ✓ creado DRAFT: {pid}")
        errs = create_options(token, pid, p["options"])
        if errs:
            msgs = " ".join(e.get("message", "") for e in errs).lower()
            if not ("already" in msgs or "exists" in msgs):
                print(f"   ✗ options: {errs}")
                results.append({"name": p["name"], "status": "ERROR_OPTIONS", "errors": str(errs)})
                continue
        errs = create_variants(token, pid, p["variants"])
        if errs:
            print(f"   ✗ variants: {errs[:2]}")
            results.append({"name": p["name"], "status": "ERROR_VARIANTS", "errors": str(errs)[:300]})
            continue
        print(f"   ✓ {len(p['variants'])} variante(s) DRAFT")
        results.append({"name": p["name"], "title": p["title"], "status": "OK_DRAFT",
                        "product_id": pid, "n_variants": len(p["variants"])})


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

    if not dry and not args.skip_backup:
        handles = ([p["winner_handle"] for p in targets]
                   + [d["handle"] for d in DRAFTS_EXISTING])
        backup_products(token, handles)

    results: list[dict] = []
    for p in targets:
        process_consolidado(token, p, dry, results)

    if not args.only:
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
