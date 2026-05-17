#!/usr/bin/env python3
"""
consolidate_balliu_sillas.py

Familia 5 · Sillas Balliu.

10 productos ACTIVE consolidados (~168 variantes) + 5 productos DRAFT (legacy +
Silla Greta + 2 duplicados Bruna misteriosos) + 1 DRAFT nuevo (Bruna 197,73€).

Decisiones del dueño (2026-05-17):
  - Bimba 3 colores (Blanco/Negro/Tórtola), patrón B/Prestige.
  - Duna 3 colores, patrón B/Prestige.
  - Selva 2 colores (Blanco/Arena) — no añadir nota "para más colores consultar".
  - Bruna: 2 productos (sin brazos / con brazos) consolidados con Color B/T.
  - Vera: 1 producto con Configuración(3) × Color(2) = 6 variantes.
  - Venus: 1 producto con Brazos (sin/con) = 2 variantes (solo Tórtola, sin opción Color).
  - Silla Etna / Etna Alta / Taburete Etna: Chasis(3) × Tejido(16) = 48 variantes c/u.
  - Mila: Chasis(2) × Tejido(2 Blanco/Ceniza) = 4 variantes.
  - Taburete Etna: precio Excel (186,62€), no web (188,63€).
  - Silla Greta y Bruna 197,73€ → DRAFT pendiente confirmar.
  - Naming Opción C + sufijo " · <Modelo>".

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
REPORT_CSV = BASE / "consolidate_balliu_sillas_report.csv"

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"

ONLINE_STORE_PUB = "gid://shopify/Publication/317589619012"
SHOP_PUB         = "gid://shopify/Publication/317589717316"

PAUSE_THRESHOLD = 200
PAUSE_SECONDS = 2.0
LEGACY_TAG = "legacy-balliu-consolidado-2026-05"
PENDING_TAG = "pendiente-confirmar-proveedor"


# ─── HELPERS ──────────────────────────────────────────────────────────────────

COLOR_SLUGS = {"Tórtola": "TORTOLA", "Gris oscuro": "GRIS-OSC",
               "Verde claro": "VERDE-CLARO", "Verde oscuro": "VERDE-OSC",
               "Azul celeste": "AZUL-CEL", "Azul marino": "AZUL-MAR",
               "Azul acero": "AZUL-ACERO", "Marrón oscuro": "MARRON-OSC"}


def slug(text: str) -> str:
    if text in COLOR_SLUGS: return COLOR_SLUGS[text]
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


def gql(token, query, variables=None):
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

def mf_base(modelo, sku_orig, espacios, envio="m"):
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


def mf_variant(sku_orig):
    return [{"namespace": "santavila", "key": "proveedor_sku_original",
             "type": "single_line_text_field", "value": sku_orig}]


# ─── CONSTANTES ───────────────────────────────────────────────────────────────

SERIE_00_FULL = ["Azul", "Amarillo", "Naranja", "Verde claro", "Blanco",
                 "Natural", "Capuchino", "Caqui", "Marrón oscuro", "Arena",
                 "Verde oscuro", "Azul celeste", "Ceniza", "Azul marino",
                 "Gris oscuro", "Azul acero"]
CHASIS_ALU3 = ["Blanco", "Tórtola", "Aluminio"]
CHASIS_MILA = ["Blanco", "Aluminio"]
TEJIDOS_MILA = ["Blanco", "Ceniza"]

ESPACIOS_HOSTE = ["jardin", "terraza", "hosteleria", "balcon"]


# ─── PRODUCTS ─────────────────────────────────────────────────────────────────

PRODUCTS: list[dict] = [
    # 1. Bimba
    {
        "name": "bimba",
        "winner_handle": "balliu-silla-exterior-resina-estilo-clasico-57-cm-8164cc65",
        "title": "Silla exterior resina · estilo clásico · Bimba",
        "envio_tag": "envio:m",
        "needs_reset_options": True,
        "options": [{"name": "Color", "values": ["Blanco", "Negro", "Tórtola"]}],
        "price_fn": lambda c: 102.03 if c == "Blanco" else 103.56,
        "sku_fn": lambda c: f"SV-BIMBA-{slug(c)}",
        "var_sku_orig_fn": lambda c: (
            "BALLIU_BIMBA_SILLA_BLANCA_8164CC65" if c == "Blanco"
            else "BALLIU_BIMBA_SILLA_NEGRA_5F329445"),
        "product_metafields": mf_base("Bimba", "BALLIU_BIMBA_SILLA_*", ESPACIOS_HOSTE, "m"),
    },

    # 2. Duna
    {
        "name": "duna",
        "winner_handle": "balliu-silla-exterior-resina-estilo-minimalista-484cbea0",
        "title": "Silla exterior resina · estilo minimalista · Duna",
        "envio_tag": "envio:m",
        "needs_reset_options": True,
        "options": [{"name": "Color", "values": ["Blanco", "Negro", "Tórtola"]}],
        "price_fn": lambda c: 77.39 if c == "Blanco" else 81.76,
        "sku_fn": lambda c: f"SV-DUNA-{slug(c)}",
        "var_sku_orig_fn": lambda c: (
            "BALLIU_DUNA_SILLA_BLANCA_484CBEA0" if c == "Blanco"
            else "BALLIU_DUNA_SILLA_COLOR_NEGRO_TORT_611D28CC"),
        "product_metafields": mf_base("Duna", "BALLIU_DUNA_SILLA_*", ESPACIOS_HOSTE, "m"),
    },

    # 3. Selva (silla)
    {
        "name": "selva_silla",
        "winner_handle": "balliu-silla-exterior-resina-estilo-funcional-0b607ec7",
        "title": "Silla exterior resina apilable · Selva",
        "envio_tag": "envio:m",
        "needs_reset_options": True,
        "options": [{"name": "Color", "values": ["Blanco", "Arena"]}],
        "price_fn": lambda c: 33.50 if c == "Blanco" else 40.52,
        "sku_fn": lambda c: f"SV-SELVA-SILLA-{slug(c)}",
        "var_sku_orig_fn": lambda c: (
            "BALLIU_SELVA_SILLA_BLANCA_0B607EC7" if c == "Blanco"
            else "BALLIU_SELVA_SILLA_COLOR_5FDA60B0"),
        "product_metafields": mf_base("Selva (silla)", "BALLIU_SELVA_SILLA_*", ESPACIOS_HOSTE, "m"),
    },

    # 4. Bruna (Brazos × Color = 4)
    {
        "name": "bruna",
        "winner_handle": "balliu-silla-exterior-sin-brazos-resina-estilo-contemporaneo-49-cm-af080e9c",
        "title": "Silla exterior resina · Bruna",
        "envio_tag": "envio:m",
        "needs_reset_options": True,
        "options": [
            {"name": "Brazos", "values": ["Sin brazos", "Con brazos"]},
            {"name": "Color", "values": ["Blanco", "Tórtola"]},
        ],
        "price_fn": lambda b, c: 70.81 if b == "Sin brazos" else 84.19,
        "sku_fn": lambda b, c: f"SV-BRUNA-{slug(b)}-{slug(c)}",
        "var_sku_orig_fn": lambda b, c: (
            "BALLIU_BRUNA_SILLA_SIN_BRAZOS_AF080E9C" if b == "Sin brazos"
            else "BALLIU_BRUNA_SILLA_CON_BRAZOS_D52BECC5"),
        "product_metafields": mf_base("Bruna", "BALLIU_BRUNA_SILLA_*", ESPACIOS_HOSTE, "m"),
    },

    # 5. Vera (Configuración × Color = 6)
    {
        "name": "vera",
        "winner_handle": "balliu-silla-exterior-sin-brazos-resina-estilo-funcional-daabcdaf",
        "title": "Silla exterior resina · Vera",
        "envio_tag": "envio:m",
        "needs_reset_options": True,
        "options": [
            {"name": "Configuración", "values": ["Sin brazos", "Con brazos", "Sillón L"]},
            {"name": "Color", "values": ["Blanco", "Tórtola"]},
        ],
        "price_fn": lambda cf, co: {"Sin brazos": 77.97, "Con brazos": 79.76, "Sillón L": 115.08}[cf],
        "sku_fn": lambda cf, co: f"SV-VERA-{slug(cf)}-{slug(co)}",
        "var_sku_orig_fn": lambda cf, co: {
            "Sin brazos": "BALLIU_VERA_SILLA_SIN_BRAZOS_DAABCDAF",
            "Con brazos": "BALLIU_VERA_SILLA_CON_BRAZOS_75353330",
            "Sillón L":   "BALLIU_VERA_SILLA_L_CON_BRAZOS_51F30794",
        }[cf],
        "product_metafields": mf_base("Vera", "BALLIU_VERA_SILLA_*", ESPACIOS_HOSTE, "m"),
    },

    # 6. Venus (Brazos = 2, solo Tórtola)
    {
        "name": "venus",
        "winner_handle": "balliu-silla-exterior-sin-brazos-estilo-contemporaneo-53-cm-cd07e7d6",
        "title": "Silla exterior resina · Venus",
        "envio_tag": "envio:m",
        "options": [{"name": "Brazos", "values": ["Sin brazos", "Con brazos"]}],
        "price_fn": lambda b: 65.42 if b == "Sin brazos" else 70.71,
        "sku_fn": lambda b: f"SV-VENUS-{slug(b)}",
        "var_sku_orig_fn": lambda b: (
            "BALLIU_SILLA_VENUS_SIN_BRAZOS_CD07E7D6" if b == "Sin brazos"
            else "BALLIU_SILLA_VENUS_CON_BRAZOS_C654C52F"),
        "product_metafields": mf_base("Venus", "BALLIU_SILLA_VENUS_*", ESPACIOS_HOSTE, "m"),
    },

    # 7. Silla Etna (Chasis × Tejido = 48)
    {
        "name": "silla_etna",
        "winner_handle": "balliu-silla-exterior-con-brazos-aluminio-estilo-elegante-56-cm-5c88bd77",
        "title": "Silla exterior aluminio · tejido Balliu · Etna",
        "envio_tag": "envio:m",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda ch, co: 181.89,
        "sku_fn": lambda ch, co: f"SV-ETNA-SILLA-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda ch, co: "BALLIU_ETNA_SILLA_CON_BRAZOS_5C88BD77",
        "product_metafields": mf_base("Etna (silla)", "BALLIU_ETNA_SILLA_CON_BRAZOS_5C88BD77",
                                     ESPACIOS_HOSTE, "m"),
    },

    # 8. Silla Etna Alta (Chasis × Tejido = 48)
    {
        "name": "silla_etna_alta",
        "winner_handle": "balliu-silla-exterior-con-brazos-aluminio-estilo-elegante-56-cm-eaf4a34a",
        "title": "Silla exterior aluminio alta · tejido Balliu · Etna Alta",
        "envio_tag": "envio:m",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda ch, co: 190.20,
        "sku_fn": lambda ch, co: f"SV-ETNA-ALTA-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda ch, co: "BALLIU_ETNA_SILLA_ALTA_CON_BRAZOS_EAF4A34A",
        "product_metafields": mf_base("Etna Alta", "BALLIU_ETNA_SILLA_ALTA_CON_BRAZOS_EAF4A34A",
                                     ESPACIOS_HOSTE, "m"),
    },

    # 9. Taburete Etna (Chasis × Tejido = 48)
    {
        "name": "taburete_etna",
        "winner_handle": "balliu-taburete-exterior-aluminio-estilo-elegante-56-cm-a66b4a0a",
        "title": "Taburete exterior aluminio · tejido Balliu · Etna",
        "envio_tag": "envio:m",
        "options": [
            {"name": "Chasis", "values": CHASIS_ALU3},
            {"name": "Color tejido", "values": SERIE_00_FULL},
        ],
        "price_fn": lambda ch, co: 186.62,
        "sku_fn": lambda ch, co: f"SV-ETNA-TAB-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda ch, co: "BALLIU_ETNA_SILLA_TABURETE_ETNA_AL_A66B4A0A",
        "product_metafields": mf_base("Etna Taburete", "BALLIU_ETNA_SILLA_TABURETE_ETNA_AL_A66B4A0A",
                                     ESPACIOS_HOSTE, "m"),
    },

    # 10. Mila (Chasis × Tejido = 4)
    {
        "name": "mila",
        "winner_handle": "balliu-silla-exterior-con-brazos-aluminio-estilo-elegante-58-cm-bc0c02ec",
        "title": "Silla exterior aluminio · tejido Balliu · Mila",
        "envio_tag": "envio:m",
        "options": [
            {"name": "Chasis", "values": CHASIS_MILA},
            {"name": "Color tejido", "values": TEJIDOS_MILA},
        ],
        "price_fn": lambda ch, co: 97.88,
        "sku_fn": lambda ch, co: f"SV-MILA-{slug(ch)}-{slug(co)}",
        "var_sku_orig_fn": lambda ch, co: "BALLIU_MILA_SILLA_CON_BRAZOS_BC0C02EC",
        "product_metafields": mf_base("Mila", "BALLIU_MILA_SILLA_CON_BRAZOS_BC0C02EC",
                                     ESPACIOS_HOSTE, "m"),
    },
]


# ─── DRAFTS existentes ───────────────────────────────────────────────────────

DRAFTS_EXISTING = [
    ("balliu-silla-exterior-con-brazos-estilo-contemporaneo-53-cm-c654c52f",
     "Venus con brazos — variante del consolidado"),
    ("balliu-silla-exterior-aluminio-estilo-contemporaneo-afd89221",
     "Silla Greta — no figura en web del proveedor"),
    ("balliu-silla-exterior-con-brazos-resina-estilo-funcional-94b6e5b5",
     "Bruna ? (113,80€ sin coste) — duplicado pendiente confirmar"),
    ("balliu-silla-exterior-con-brazos-resina-estilo-funcional-94b6e5b5-2",
     "Bruna ? (89,95€) — duplicado pendiente confirmar"),
]


# ─── DRAFTS nuevos ───────────────────────────────────────────────────────────

DRAFTS_NEW = [
    {
        "name": "bruna_misterio_draft",
        "new_handle": "silla-exterior-resina-bruna-precio-alto-pendiente",
        "title": "Silla exterior resina · Bruna (variante 197,73€) — pendiente confirmar",
        "tags": ["Balliu", "envio:m", PENDING_TAG, LEGACY_TAG],
        "options": [{"name": "Variante", "values": ["Pendiente confirmar"]}],
        "variants_data": [("Pendiente confirmar", 197.73,
                           "BALLIU_BRUNA_SILLA_CON_BRAZ_94B6E5B5 (Excel r169)")],
        "modelo": "Bruna ¿L? (pendiente)",
        "espacios": ESPACIOS_HOSTE,
    },
]


# ─── EXPAND VARIANTS ──────────────────────────────────────────────────────────

def expand_variants(product):
    from itertools import product as iproduct
    option_names = [o["name"] for o in product["options"]]
    option_values = [o["values"] for o in product["options"]]
    out = []
    for combo in iproduct(*option_values):
        opts = dict(zip(option_names, combo))
        price = product["price_fn"](*combo)
        sku = product["sku_fn"](*combo)
        sku_orig = product["var_sku_orig_fn"](*combo)
        out.append({"option_values": opts, "price": round(price, 2),
                    "sku": sku, "metafields": mf_variant(sku_orig)})
    return out


# ─── SHOPIFY OPS ──────────────────────────────────────────────────────────────

def backup_products(token, handles):
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = BACKUP_DIR / f"sillas_{timestamp}.json"
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
        except Exception as e: print(f"   ✗ {h}: {e}")
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
    return out_path


def find_product(token, handle):
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


def reset_options(token, prod):
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


def create_product_new(token, p, status="DRAFT"):
    inp = {"title": p["title"], "handle": p.get("new_handle"),
           "productType": p.get("product_type", "Silla"), "status": status,
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


def clean_tags(current, envio_tag=None, *, legacy=False):
    new = [t for t in current if not t.startswith("envio:")
           and t not in ("match-rojo", "match-verde", "match-amarillo")]
    if envio_tag: new.append(envio_tag)
    if legacy and LEGACY_TAG not in new: new.append(LEGACY_TAG)
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

    errs = create_variants(token, pid, variants)
    if errs:
        print(f"   ✗ variants: {errs[:2]}")
        results.append({"name": p["name"], "status": "ERROR_VARIANTS", "errors": str(errs)[:300]})
        return

    print(f"   ✓ {len(variants)} variantes")
    results.append({"name": p["name"], "title": p["title"], "status": "OK",
                    "product_id": pid, "n_variants": len(variants)})


def process_drafts_existing(token, dry, results):
    print("\n─── Pasar a DRAFT productos legacy/duplicados ───")
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
    print("\n─── Crear productos DRAFT nuevos ───")
    for d in DRAFTS_NEW:
        print(f"\n▶ DRAFT NEW — {d['name']}: {d['title']}")
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
                "tags": d["tags"], "product_type": "Silla",
                "product_metafields": mf_base(d["modelo"], d["variants_data"][0][2], d["espacios"], "m"),
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
        handles = [p["winner_handle"] for p in targets] + [h for h, _ in DRAFTS_EXISTING]
        backup_products(token, handles)

    results = []
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
