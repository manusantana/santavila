#!/usr/bin/env python3
"""
consolidate_balliu_mesas_centro.py

Sub-piloto 3c · Familia 3 (Mesas) — Mesa de centro exterior aluminio HPL.

Estado actual en Shopify:
  - balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e
    ACTIVE · 2 variantes "Tablero Hpl" / "Tablero Hpl Gd"
    SKUs BALLIU_ETNA_MESA_CENTRAL_* · 349,90 € / 421,95 €.

Origen proveedor: Etna Mesa Central (110×60×44.5 cm).

Decisiones del dueño (2026-05-17):
  - HPL Gran Densidad NO aparece en web actual del proveedor → producto DRAFT
    separado, pendiente confirmación con proveedor.
  - Chasis (3 colores: Blanco, Tórtola, Aluminio) → opción visible.
  - Color tablero HPL (5: Gris, Blanco, Moonwalk, Skyline, Prado) → opción visible.
  - Mismo precio para todas las combinaciones HPL standard (362,44 € IVA).
  - Naming Opción C: "Mesa de centro exterior · aluminio HPL 110×60 cm".

Resultado:
  - 1 producto ACTIVE consolidado: Chasis(3) × Color tablero(5) = 15 variantes a 362,44 €.
  - 1 producto DRAFT (HPL Gran Densidad) creado nuevo, 1 sola variante a 421,95 €
    pendiente confirmación con proveedor.

Modos: --dry-run (default), --apply, --skip-publish, --skip-backup.
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
REPORT_CSV = BASE / "consolidate_balliu_mesas_centro_report.csv"

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
                API,
                data=payload,
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


# ─── PLAN ─────────────────────────────────────────────────────────────────────

WINNER_HANDLE = "balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e"

CHASIS = ["Blanco", "Tórtola", "Aluminio"]
TABLEROS_HPL = ["Gris", "Blanco", "Moonwalk", "Skyline", "Prado"]

PRECIO_HPL = 362.44       # Excel row 251 col F (PVP IVA)
PRECIO_HPL_GD = 421.95    # Excel row 252 col F (PVP IVA)

CONSOLIDADO = {
    "name": "mesa_centro_hpl",
    "winner_handle": WINNER_HANDLE,
    "title": "Mesa de centro exterior · aluminio HPL 110×60 cm",
    "envio_tag": "envio:m",
    "options": [
        {"name": "Chasis", "values": CHASIS},
        {"name": "Color tablero", "values": TABLEROS_HPL},
    ],
    "variants": [
        {
            "option_values": {"Chasis": ch, "Color tablero": tb},
            "price": PRECIO_HPL,
            "sku": f"SV-MESACENTRO-{slug(ch)}-{slug(tb)}",
            "metafields": mf_variant("BALLIU_ETNA_MESA_CENTRAL_TABLERO_HPL_510B363E"),
        }
        for ch in CHASIS for tb in TABLEROS_HPL
    ],
    "product_metafields": mf_base(
        "Etna Mesa Central",
        "BALLIU_ETNA_MESA_CENTRAL_TABLERO_HPL_510B363E",
        ["terraza", "salon-exterior", "balcon", "jardin"],
        "m",
    ),
}

DRAFT_HPL_GD = {
    "name": "mesa_centro_hpl_gd_draft",
    "new_handle": "mesa-de-centro-exterior-aluminio-hpl-gd-110x60",
    "title": "Mesa de centro exterior · aluminio HPL Gran Densidad 110×60 cm",
    "product_type": "Mesa",
    "tags": ["Balliu", "envio:m", "pendiente-confirmar-proveedor", LEGACY_TAG],
    "options": [
        {"name": "Tablero", "values": ["HPL Gran Densidad"]},
    ],
    "variants": [
        {
            "option_values": {"Tablero": "HPL Gran Densidad"},
            "price": PRECIO_HPL_GD,
            "sku": "SV-MESACENTRO-HPL-GD",
            "metafields": mf_variant("BALLIU_ETNA_MESA_CENTRAL_TABLERO_HPL_GD_BC53F712"),
        },
    ],
    "product_metafields": mf_base(
        "Etna Mesa Central (HPL GD)",
        "BALLIU_ETNA_MESA_CENTRAL_TABLERO_HPL_GD_BC53F712",
        ["terraza", "salon-exterior", "balcon", "jardin"],
        "m",
    ),
}


# ─── SHOPIFY OPS ──────────────────────────────────────────────────────────────

def backup_products(token: str, handles: list[str]) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = BACKUP_DIR / f"mesas_centro_{timestamp}.json"
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
                snap.append(p)
                print(f"   ✓ {h}")
            else:
                print(f"   · {h} no encontrado")
        except Exception as e:
            print(f"   ✗ {h}: {e}")
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
    return out_path


def find_product(token: str, handle: str) -> dict | None:
    r = gql(token, '''query($h: String!){ productByHandle(handle:$h){
        id handle status tags
        options{id name optionValues{id name}}
        variants(first:100){edges{node{id title}}}
    } }''', {"h": handle})
    return r.get("productByHandle")


def update_product(token, pid, *, title=None, tags=None, product_metafields=None, status=None):
    inp = {"id": pid}
    if title is not None:
        inp["title"] = title
    if tags is not None:
        inp["tags"] = tags
    if product_metafields:
        inp["metafields"] = product_metafields
    if status:
        inp["status"] = status
    r = gql(
        token,
        'mutation($input: ProductInput!){productUpdate(input:$input){product{id} userErrors{field message}}}',
        {"input": inp},
    )
    return r["productUpdate"]["userErrors"]


def delete_options_keep_one(token: str, prod: dict) -> list:
    """Para reset de opciones legacy: borra todas las variantes salvo una,
    luego borra todas las opciones existentes con strategy:POSITION."""
    variants = [e["node"] for e in prod["variants"]["edges"]] if False else []
    # Refetch with variants
    r = gql(token, '''query($id:ID!){product(id:$id){
        variants(first:100){edges{node{id}}}
        options{id name}
    }}''', {"id": prod["id"]})
    p = r["product"]
    v_ids = [e["node"]["id"] for e in p["variants"]["edges"]]
    errs = []
    # Borrar todas salvo la primera
    if len(v_ids) > 1:
        delete = gql(token, '''mutation($pid:ID!,$ids:[ID!]!){
            productVariantsBulkDelete(productId:$pid, variantsIds:$ids){
                userErrors{field message}
            }
        }''', {"pid": prod["id"], "ids": v_ids[1:]})
        if delete["productVariantsBulkDelete"]["userErrors"]:
            errs += delete["productVariantsBulkDelete"]["userErrors"]
    # Borrar todas las opciones con POSITION (deja Title default)
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
        productOptionsCreate(productId:$pid, options:$opts){
            userErrors{field message code}
        }
    }''', {"pid": pid, "opts": opts_input})
    return r["productOptionsCreate"]["userErrors"]


def create_variants(token: str, pid: str, variants: list[dict]):
    vs = []
    for v in variants:
        ov = [{"optionName": k, "name": val} for k, val in v["option_values"].items()]
        vi = {
            "optionValues": ov,
            "price": f"{v['price']:.2f}",
            "inventoryItem": {"sku": v["sku"], "tracked": False},
        }
        if v.get("metafields"):
            vi["metafields"] = v["metafields"]
        vs.append(vi)
    r = gql(token, '''mutation($pid:ID!,$vars:[ProductVariantsBulkInput!]!){
        productVariantsBulkCreate(productId:$pid, variants:$vars, strategy:REMOVE_STANDALONE_VARIANT){
            userErrors{field message code}
        }
    }''', {"pid": pid, "vars": vs})
    return r["productVariantsBulkCreate"]["userErrors"]


def create_product_new(token: str, p: dict, status: str = "DRAFT"):
    inp = {
        "title": p["title"],
        "handle": p.get("new_handle"),
        "productType": p.get("product_type", "Mesa"),
        "status": status,
        "tags": p.get("tags", []),
    }
    if p.get("product_metafields"):
        inp["metafields"] = p["product_metafields"]
    r = gql(
        token,
        'mutation($input:ProductInput!){productCreate(input:$input){product{id handle} userErrors{field message}}}',
        {"input": inp},
    )
    errs = r["productCreate"]["userErrors"]
    if errs:
        return None, errs
    return r["productCreate"]["product"]["id"], []


def publish_product(token: str, pid: str):
    r = gql(token, '''mutation($id:ID!,$input:[PublicationInput!]!){
        publishablePublish(id:$id, input:$input){userErrors{field message}}
    }''', {"id": pid, "input": [{"publicationId": ONLINE_STORE_PUB}, {"publicationId": SHOP_PUB}]})
    return r["publishablePublish"]["userErrors"]


def clean_tags(current: list[str], envio_tag: str | None) -> list[str]:
    new = [t for t in current if not t.startswith("envio:") and t not in ("match-rojo", "match-verde")]
    if envio_tag:
        new.append(envio_tag)
    seen, out = set(), []
    for t in new:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


# ─── ORQUESTACIÓN ─────────────────────────────────────────────────────────────

def process_consolidado(token: str, dry: bool, results: list):
    p = CONSOLIDADO
    print(f"\n▶ CONSOLIDADO — {p['title']}")
    print(f"   plan: {len(p['variants'])} variantes (Chasis × Color tablero) en winner={p['winner_handle']}")

    if dry:
        for v in p["variants"][:3]:
            print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
        if len(p["variants"]) > 3:
            print(f"     · …y {len(p['variants'])-3} más")
        results.append({"name": p["name"], "title": p["title"], "status": "DRY_RUN",
                        "n_variants": len(p["variants"])})
        return

    winner = find_product(token, p["winner_handle"])
    if not winner:
        results.append({"name": p["name"], "status": "ERROR",
                        "errors": "winner no encontrado"})
        return
    pid = winner["id"]

    # El producto actual ya tiene una opción "Tablero" con 2 valores Hpl/Hpl Gd.
    # Hay que limpiar variantes y opciones antiguas antes de aplicar las nuevas.
    legacy_opts = [o for o in (winner.get("options") or []) if o["name"] not in ("Title", "Chasis", "Color tablero")]
    if legacy_opts:
        print(f"   · resetear opciones legacy: {[o['name'] for o in legacy_opts]}")
        errs = delete_options_keep_one(token, winner)
        if errs:
            print(f"   ✗ delete options: {errs}")
            results.append({"name": p["name"], "status": "ERROR_DELETE_OPTS", "errors": str(errs)})
            return

    tags = clean_tags(winner["tags"], p["envio_tag"])
    errs = update_product(
        token, pid, title=p["title"], tags=tags,
        product_metafields=p["product_metafields"], status="ACTIVE",
    )
    if errs:
        print(f"   ✗ update: {errs}")
        results.append({"name": p["name"], "status": "ERROR_UPDATE", "errors": str(errs)})
        return

    errs = create_options(token, pid, p["options"])
    if errs:
        msgs = " ".join(e.get("message", "") for e in errs).lower()
        if "already" in msgs or "exists" in msgs:
            print("   · options ya existían")
        else:
            print(f"   ✗ options: {errs}")
            results.append({"name": p["name"], "status": "ERROR_OPTIONS", "errors": str(errs)})
            return

    errs = create_variants(token, pid, p["variants"])
    if errs:
        print(f"   ✗ variants: {errs[:2]}")
        results.append({"name": p["name"], "status": "ERROR_VARIANTS",
                        "errors": str(errs)[:300]})
        return

    print(f"   ✓ {len(p['variants'])} variantes")
    results.append({"name": p["name"], "title": p["title"], "status": "OK",
                    "product_id": pid, "n_variants": len(p["variants"])})


def process_draft_hpl_gd(token: str, dry: bool, results: list):
    p = DRAFT_HPL_GD
    print(f"\n▶ DRAFT — {p['title']}")
    print(f"   handle nuevo: {p['new_handle']}  · {len(p['variants'])} variante(s)")
    if dry:
        for v in p["variants"]:
            print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
        results.append({"name": p["name"], "title": p["title"], "status": "DRY_RUN",
                        "n_variants": len(p["variants"])})
        return

    existing = find_product(token, p["new_handle"])
    if existing:
        print(f"   · ya existía: {existing['id']}")
        pid = existing["id"]
    else:
        pid, errs = create_product_new(token, p, status="DRAFT")
        if errs:
            print(f"   ✗ create: {errs}")
            results.append({"name": p["name"], "status": "ERROR_CREATE", "errors": str(errs)})
            return
        print(f"   ✓ creado DRAFT: {pid}")

    errs = create_options(token, pid, p["options"])
    if errs:
        msgs = " ".join(e.get("message", "") for e in errs).lower()
        if not ("already" in msgs or "exists" in msgs):
            print(f"   ✗ options: {errs}")
            results.append({"name": p["name"], "status": "ERROR_OPTIONS", "errors": str(errs)})
            return

    errs = create_variants(token, pid, p["variants"])
    if errs:
        print(f"   ✗ variants: {errs[:2]}")
        results.append({"name": p["name"], "status": "ERROR_VARIANTS",
                        "errors": str(errs)[:300]})
        return

    print(f"   ✓ {len(p['variants'])} variante(s) en DRAFT")
    results.append({"name": p["name"], "title": p["title"], "status": "OK_DRAFT",
                    "product_id": pid, "n_variants": len(p["variants"])})


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--skip-publish", action="store_true")
    parser.add_argument("--skip-backup", action="store_true")
    args = parser.parse_args()

    dry = not args.apply
    print("════ MODO DRY-RUN ════\n" if dry else "════ MODO APPLY ════\n")

    token = read_token()

    if not dry and not args.skip_backup:
        backup_products(token, [CONSOLIDADO["winner_handle"]])

    results: list[dict] = []
    process_consolidado(token, dry, results)
    process_draft_hpl_gd(token, dry, results)

    if not dry and not args.skip_publish:
        print("\n─── Publicar consolidado ACTIVE en Online Store + Shop ───")
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
