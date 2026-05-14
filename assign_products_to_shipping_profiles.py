#!/usr/bin/env python3
"""
assign_products_to_shipping_profiles.py

Asigna las variantes de los 225 productos clasificados (XS / M / L) a sus
Shipping Profiles correspondientes vía Admin GraphQL API 2026-01.

Pre-requisitos:
  - El usuario ha creado 3 Shipping Profiles vacíos en Admin
    (Settings → Shipping → Custom shipping rates → Create new profile).
  - Los productos ya tienen tag envio:xs|m|l (ejecutado por apply_shipping_categories.py).

Flujo de uso (en este orden):

  # 1. Listar profiles existentes para identificar IDs
  python3 assign_products_to_shipping_profiles.py --list

  # 2. Dry-run: muestra qué variantes asignaría a cada profile
  python3 assign_products_to_shipping_profiles.py --by-name

  # O bien, especificando IDs explícitos (útil si los nombres son ambiguos):
  python3 assign_products_to_shipping_profiles.py \
      --map xs=gid://shopify/DeliveryProfile/123,m=gid://shopify/DeliveryProfile/456,l=gid://shopify/DeliveryProfile/789

  # 3. Apply real
  python3 assign_products_to_shipping_profiles.py --by-name --apply

Notas:
  - Una variante solo puede estar en UN profile a la vez. Al asociar al custom,
    Shopify la disocia automáticamente del General. Reversible.
  - --by-name busca matching laxo: profile cuyo nombre contenga "xs", "m" o "l".
    Si tienes varios profiles con esas letras (ej. "Premium L"), usa --map.

Output: assign_shipping_profiles_report.csv
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
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPORT_CSV = BASE / "assign_shipping_profiles_report.csv"

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"

PAUSE_THRESHOLD = 200
PAUSE_SECONDS = 2.0
BATCH_SIZE = 50  # variantes por mutación


def read_token() -> str:
    for fname in (".env.local", ".envlocal", ".env"):
        p = BASE / fname
        if not p.exists():
            continue
        env = p.read_text(encoding="utf-8")
        m = re.search(r"^SHOPIFY_ACCESS_TOKEN=(.*)$", env, re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit("✗ SHOPIFY_ACCESS_TOKEN no encontrado en .env.local / .envlocal / .env")


_throttle = {"available": 2000.0}


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    last_err = None
    for attempt in range(1, 6):
        try:
            req = urllib.request.Request(
                API,
                data=payload,
                headers={
                    "X-Shopify-Access-Token": token,
                    "Content-Type": "application/json",
                },
                method="POST",
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
            body = e.read().decode("utf-8", errors="replace")[:500]
            last_err = f"HTTP {e.code}: {body}"
            if e.code == 429:
                wait = float(e.headers.get("Retry-After", 2))
                time.sleep(wait)
                continue
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            last_err = str(e)
        time.sleep(1.5 * attempt)
    raise RuntimeError(f"GraphQL falló tras reintentos: {last_err}")


# ── Listar profiles ──────────────────────────────────────────────────────────

QUERY_PROFILES = """
query {
  deliveryProfiles(first: 25) {
    edges {
      node {
        id
        name
        default
        profileItems(first: 1) { edges { node { id } } }
      }
    }
  }
}
"""


def list_profiles(token: str) -> list[dict]:
    data = gql(token, QUERY_PROFILES)
    return [e["node"] for e in data["deliveryProfiles"]["edges"]]


# ── Obtener variantes por tag ────────────────────────────────────────────────

QUERY_PRODUCTS_BY_TAG = """
query($q: String!, $cursor: String) {
  products(first: 100, after: $cursor, query: $q) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        handle
        title
        tags
        variants(first: 50) {
          edges { node { id sku } }
        }
      }
    }
  }
}
"""


def fetch_variants_by_category(token: str, cat: str) -> list[dict]:
    """Devuelve [{variant_id, product_handle, sku}] para todos los productos
    con tag envio:<cat>."""
    out = []
    cursor = None
    # Las comillas simples son necesarias porque el ':' del valor confundiría al parser.
    q = f"tag:'envio:{cat}'"
    while True:
        data = gql(token, QUERY_PRODUCTS_BY_TAG, {"q": q, "cursor": cursor})
        page = data["products"]
        for e in page["edges"]:
            p = e["node"]
            for ve in p["variants"]["edges"]:
                v = ve["node"]
                out.append({
                    "variant_id": v["id"],
                    "sku": v["sku"],
                    "handle": p["handle"],
                    "title": p["title"],
                })
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return out


# ── Asignar variantes a profile ──────────────────────────────────────────────

MUTATION_PROFILE_UPDATE = """
mutation($id: ID!, $profile: DeliveryProfileInput!) {
  deliveryProfileUpdate(id: $id, profile: $profile) {
    profile { id name }
    userErrors { field message }
  }
}
"""


def assign_to_profile(token: str, profile_id: str, variant_ids: list[str]) -> list[str]:
    """Asocia variant_ids al profile. Devuelve lista de errores (vacía si OK)."""
    errors_all = []
    for i in range(0, len(variant_ids), BATCH_SIZE):
        batch = variant_ids[i:i + BATCH_SIZE]
        data = gql(token, MUTATION_PROFILE_UPDATE, {
            "id": profile_id,
            "profile": {"variantsToAssociate": batch},
        })
        errs = data["deliveryProfileUpdate"]["userErrors"]
        if errs:
            errors_all.extend(errs)
            print(f"  ✗ batch {i//BATCH_SIZE+1}: {json.dumps(errs, ensure_ascii=False)}")
    return errors_all


# ── Resolución de mapping ────────────────────────────────────────────────────

def resolve_by_name(profiles: list[dict]) -> dict:
    """Detecta profiles XS/M/L por nombre. Devuelve {xs: id, m: id, l: id}."""
    out = {}
    # Excluir el profile default ("General shipping rates")
    customs = [p for p in profiles if not p.get("default")]
    for cat in ("xs", "m", "l"):
        candidates = []
        for p in customs:
            name = p["name"].lower()
            # Reglas de matching loose
            if cat == "xs" and ("xs" in name or "accesori" in name or "peque" in name):
                candidates.append(p)
            elif cat == "m" and (re.search(r"\bm\b", name) or "mediano" in name or "medium" in name):
                candidates.append(p)
            elif cat == "l" and (re.search(r"\bl\b", name) or "voluminoso" in name or "grande" in name or "large" in name):
                candidates.append(p)
        if len(candidates) == 1:
            out[cat] = candidates[0]["id"]
        elif len(candidates) > 1:
            print(f"⚠ Múltiples candidatos para '{cat}': {[c['name'] for c in candidates]}")
            print("   Usa --map para especificar IDs explícitos.")
            return {}
        else:
            print(f"⚠ No se encontró profile para '{cat}'.")
            return {}
    return out


def parse_map(s: str) -> dict:
    out = {}
    for part in s.split(","):
        k, v = part.split("=", 1)
        out[k.strip().lower()] = v.strip()
    return out


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="Solo lista los profiles existentes y sale")
    parser.add_argument("--by-name", action="store_true", help="Auto-detecta XS/M/L por nombre del profile")
    parser.add_argument("--map", default=None, help="Mapeo explícito xs=ID,m=ID,l=ID")
    parser.add_argument("--apply", action="store_true", help="Aplica (default: dry-run)")
    args = parser.parse_args()

    token = read_token()

    if args.list:
        profiles = list_profiles(token)
        print(f"\n{len(profiles)} delivery profiles encontrados:\n")
        for p in profiles:
            tag = " (default)" if p.get("default") else ""
            print(f"  {p['id']}  ·  {p['name']}{tag}")
        return

    # Resolver mapping
    if args.map:
        mapping = parse_map(args.map)
    elif args.by_name:
        profiles = list_profiles(token)
        print("\nProfiles existentes:")
        for p in profiles:
            tag = " (default)" if p.get("default") else ""
            print(f"  · {p['name']}{tag}  →  {p['id']}")
        mapping = resolve_by_name(profiles)
        if not mapping:
            sys.exit(1)
        print("\nDetectado automáticamente:")
        for cat, pid in mapping.items():
            print(f"  envio:{cat}  →  {pid}")
    else:
        sys.exit("Usa --list, --by-name o --map. Ejecuta con --help.")

    # Buscar variantes por cada categoría
    print("\nObteniendo variantes por tag…")
    plan = {}
    for cat in ("xs", "m", "l"):
        vs = fetch_variants_by_category(token, cat)
        plan[cat] = vs
        print(f"  envio:{cat}  →  {len(vs)} variantes")

    # Reporte
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["categoria", "profile_id", "variant_id", "sku", "handle", "title"])
        for cat, vs in plan.items():
            for v in vs:
                w.writerow([cat, mapping[cat], v["variant_id"], v["sku"], v["handle"], v["title"]])
    print(f"\n✓ Reporte: {REPORT_CSV}")

    if not args.apply:
        print("\n[DRY-RUN] No se ha tocado Shopify. Para aplicar: añade --apply.\n")
        return

    # Aplicar
    print("\nAsignando variantes a sus profiles…")
    for cat in ("xs", "m", "l"):
        vs = plan[cat]
        pid = mapping[cat]
        if not vs:
            print(f"  envio:{cat}: 0 variantes, nada que hacer.")
            continue
        print(f"  envio:{cat}: asignando {len(vs)} variantes a {pid} …")
        errors = assign_to_profile(token, pid, [v["variant_id"] for v in vs])
        if errors:
            print(f"    ✗ {len(errors)} errores")
        else:
            print(f"    ✓ OK")

    print("\nVerifica en Admin: cada profile debería mostrar el número correspondiente de productos.")


if __name__ == "__main__":
    main()
