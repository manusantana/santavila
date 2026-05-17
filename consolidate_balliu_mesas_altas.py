#!/usr/bin/env python3
"""
consolidate_balliu_mesas_altas.py

Sub-piloto 3b · Familia 3 (Mesas) — Mesa alta exterior aluminio HPL.

Estado actual en Shopify (6 productos planos, todos ACTIVE, 1 variante c/u):
  - balliu-mesa-alta-exterior-hpl-45c511e9   Ø70 HPL
  - balliu-mesa-alta-exterior-hpl-f99491ce   Ø70 HPL GD
  - balliu-mesa-alta-exterior-hpl-a3352658   60×60 HPL GD
  - balliu-mesa-alta-exterior-hpl-a3352658-2 60×60 HPL (mal etiquetado como GD)
  - balliu-mesa-alta-exterior-hpl-94512eab   70×70 HPL
  - balliu-mesa-alta-exterior-hpl-5d74130e   70×70 HPL GD

Decisiones del dueño (2026-05-17):
  - Ø70 no existe en la web actual de Balliu → DRAFT (no se elimina).
  - HPL GD no aparece en la web actual de Balliu → DRAFT.
  - Chasis "Aluminio" va solo como descripción, no como opción.
  - Precios desde Excel pestaña `20260508 -Todos ` columna F (IVA).
  - Naming Opción C, sin nombre del modelo proveedor (Capri Alta).

Resultado:
  - 1 producto ACTIVE consolidado (winner = 94512eab):
      "Mesa alta exterior · aluminio HPL 110 cm"
      Opción Tamaño = [60×60 cm, 70×70 cm]  → 2 variantes activas.
  - 5 productos pasados a DRAFT con tag `legacy-balliu-consolidado-2026-05`.

Modos: --dry-run (default), --apply, --skip-publish, --skip-backup.
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
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
BACKUP_DIR = BASE / "backups"
REPORT_CSV = BASE / "consolidate_balliu_mesas_altas_report.csv"

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"

ONLINE_STORE_PUB = "gid://shopify/Publication/317589619012"
SHOP_PUB         = "gid://shopify/Publication/317589717316"

PAUSE_THRESHOLD = 200
PAUSE_SECONDS = 2.0
LEGACY_TAG = "legacy-balliu-consolidado-2026-05"


# ─── HELPERS ──────────────────────────────────────────────────────────────────

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
    return [
        {"namespace": "santavila", "key": "proveedor_sku_original",
         "type": "single_line_text_field", "value": sku_orig},
    ]


# ─── PLAN ─────────────────────────────────────────────────────────────────────

WINNER_HANDLE = "balliu-mesa-alta-exterior-hpl-94512eab"

CONSOLIDADO = {
    "name": "mesa_alta_hpl",
    "winner_handle": WINNER_HANDLE,
    "title": "Mesa alta exterior · aluminio HPL 110 cm",
    "envio_tag": "envio:l",
    "options": [
        {"name": "Tamaño", "values": ["60×60 cm", "70×70 cm"]},
    ],
    "variants": [
        {
            "option_values": {"Tamaño": "60×60 cm"},
            "price": 456.69,
            "sku": "SV-MESAALTA-60-HPL",
            "metafields": mf_variant("BALLIU_60X60_MESA_ALTA_TABLERO_HPL_A3352658"),
        },
        {
            "option_values": {"Tamaño": "70×70 cm"},
            "price": 528.46,
            "sku": "SV-MESAALTA-70-HPL",
            "metafields": mf_variant("BALLIU_70X70_MESA_ALTA_TABLERO_HPL_94512EAB"),
        },
    ],
    "product_metafields": mf_base(
        "Capri Alta",
        "BALLIU_*_MESA_ALTA_TABLERO_HPL_*",
        ["terraza", "balcon", "jardin", "hosteleria"],
        "l",
    ),
}

DRAFTS = [
    {"handle": "balliu-mesa-alta-exterior-hpl-45c511e9",
     "reason": "Ø70 cm — no figura en web actual del proveedor"},
    {"handle": "balliu-mesa-alta-exterior-hpl-f99491ce",
     "reason": "Ø70 cm HPL GD — no figura en web actual del proveedor"},
    {"handle": "balliu-mesa-alta-exterior-hpl-a3352658",
     "reason": "60×60 HPL GD — no figura en web actual del proveedor"},
    {"handle": "balliu-mesa-alta-exterior-hpl-5d74130e",
     "reason": "70×70 HPL GD — no figura en web actual del proveedor"},
    {"handle": "balliu-mesa-alta-exterior-hpl-a3352658-2",
     "reason": "Duplicado 60×60 — consolidado en producto winner"},
]


# ─── SHOPIFY OPS ──────────────────────────────────────────────────────────────

def backup_products(token: str, handles: list[str]) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = BACKUP_DIR / f"mesas_altas_{timestamp}.json"
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


def update_product(
    token: str, pid: str, *, title: str | None = None, tags: list[str] | None = None,
    product_metafields: list | None = None, status: str | None = None,
):
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


def publish_product(token: str, pid: str):
    r = gql(token, '''mutation($id:ID!,$input:[PublicationInput!]!){
        publishablePublish(id:$id, input:$input){userErrors{field message}}
    }''', {"id": pid, "input": [{"publicationId": ONLINE_STORE_PUB}, {"publicationId": SHOP_PUB}]})
    return r["publishablePublish"]["userErrors"]


def clean_tags(current: list[str], envio_tag: str | None, *, legacy: bool = False) -> list[str]:
    new = [t for t in current if not t.startswith("envio:") and t != "match-rojo"]
    if envio_tag:
        new.append(envio_tag)
    if legacy and LEGACY_TAG not in new:
        new.append(LEGACY_TAG)
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
    print(f"   plan: {len(p['variants'])} variantes en winner={p['winner_handle']}")

    if dry:
        for v in p["variants"]:
            print(f"     · {v['option_values']}  {v['price']}€  sku={v['sku']}")
        results.append({"name": p["name"], "title": p["title"], "status": "DRY_RUN",
                        "n_variants": len(p["variants"])})
        return

    winner = find_product(token, p["winner_handle"])
    if not winner:
        results.append({"name": p["name"], "status": "ERROR",
                        "errors": "winner no encontrado"})
        return
    pid = winner["id"]

    tags = clean_tags(winner["tags"], p["envio_tag"], legacy=False)
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
            results.append({"name": p["name"], "status": "ERROR_OPTIONS",
                            "errors": str(errs)})
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


def process_drafts(token: str, dry: bool, results: list):
    print("\n─── Pasar a DRAFT productos sin web del proveedor ───")
    for d in DRAFTS:
        h = d["handle"]
        print(f"\n▶ DRAFT — {h}  ({d['reason']})")
        if dry:
            results.append({"name": h, "title": d["reason"], "status": "DRY_DRAFT"})
            continue
        prod = find_product(token, h)
        if not prod:
            print(f"   · no encontrado")
            results.append({"name": h, "status": "MISSING"})
            continue
        tags = clean_tags(prod["tags"], None, legacy=True)
        errs = update_product(token, prod["id"], tags=tags, status="DRAFT")
        if errs:
            print(f"   ✗ {errs}")
            results.append({"name": h, "status": "ERROR_DRAFT", "errors": str(errs)})
        else:
            print(f"   ✓ pasado a DRAFT")
            results.append({"name": h, "status": "DRAFTED"})


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
        all_handles = [CONSOLIDADO["winner_handle"]] + [d["handle"] for d in DRAFTS]
        backup_products(token, all_handles)

    results: list[dict] = []
    process_consolidado(token, dry, results)
    process_drafts(token, dry, results)

    if not dry and not args.skip_publish:
        print("\n─── Publicar consolidado en Online Store + Shop ───")
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
