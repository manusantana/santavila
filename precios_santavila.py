#!/usr/bin/env python3
"""
precios_santavila.py  —  Herramienta AUTORITATIVA de precios (audita + blinda + aplica)

Fuente de verdad: Santavila.xlsx, hoja "20260508 -Todos "
  B=Handle  C=SKU  E=Coste neto (SIN IVA)  G=Precio Venta Psicológico (CON IVA 21%)=objetivo

REGLA DE ORO (NO negociable): el precio NETO (precio / 1.21) NUNCA puede ser < coste.
Nunca vender por debajo de coste. La guardia es FAIL-CLOSED: si no se conoce el coste,
NO se aplica el cambio (salvo --allow-no-cost explícito por SKU).

MODOS
  --audit                       Audita TODO y escribe precios_auditoria.csv (no toca nada).
  --set-price SKU=PRECIO ...    Fija precio de variantes (por SKU). Guardado, fail-closed.
  --set-cost  SKU=COSTE ...     Fija coste (unitCost, sin IVA). Guardado (avisa si induce pérdida).
  --backfill-costs              Rellena coste desde Excel donde sea fiable y CONSISTENTE.
  --allow-no-cost               Permite --set-price aunque no se conozca coste (úsalo a sabiendas).
  --apply                       Sin esta bandera, todo es DRY-RUN (no escribe en Shopify).

EJEMPLOS
  python3 precios_santavila.py --audit
  python3 precios_santavila.py --set-price SV-ALTEA-70X70-BLANCO-GRIS=480.95            # dry
  python3 precios_santavila.py --set-price SV-ALTEA-70X70-BLANCO-GRIS=480.95 --apply    # aplica
"""
from __future__ import annotations
import argparse, csv, json, re, sys, time, unicodedata, urllib.error, urllib.request
from collections import defaultdict
from pathlib import Path
import openpyxl

BASE = Path(__file__).resolve().parent
XLSX = BASE / "Santavila.xlsx"
SHEET = "20260508 -Todos "
SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
IVA = 1.21
REPORT = BASE / "precios_auditoria.csv"
CACHE = BASE / "_estado_tienda.json"


# ───────────────────────── infraestructura ─────────────────────────
def read_token() -> str:
    for fn in (".envlocal", ".env.local", ".env"):
        p = BASE / fn
        if p.exists():
            m = re.search(r"^SHOPIFY_ACCESS_TOKEN=(.*)$", p.read_text(encoding="utf-8"), re.M)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    sys.exit("✗ SHOPIFY_ACCESS_TOKEN no encontrado en .envlocal")


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    for attempt in range(1, 7):
        try:
            req = urllib.request.Request(
                API, data=payload,
                headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                method="POST")
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.loads(r.read())
            if data.get("errors"):
                raise RuntimeError(json.dumps(data["errors"])[:300])
            return data["data"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(float(e.headers.get("Retry-After", 2))); continue
            time.sleep(1.5 * attempt)
        except Exception:
            time.sleep(1.5 * attempt)
    raise RuntimeError("GraphQL falló tras reintentos")


def net(price):       # precio neto (sin IVA) a partir de precio con IVA
    return None if price is None else round(price / IVA, 4)


def norm(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = s.replace("×", "x")
    return re.sub(r"[^a-z0-9]", "", s)


def family(handle):
    """Familia de un handle = sin el hash final de 8 hex (los handles consolidados
    comparten familia: balliu-base-de-parasol-3ee8b72d → balliu-base-de-parasol)."""
    if not handle:
        return handle
    return re.sub(r"-[0-9a-f]{8}$", "", handle)


# ───────────────────────── carga de datos ─────────────────────────
def load_excel():
    wb = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)
    ws = wb[SHEET]
    rows = []
    for r in ws.iter_rows(min_row=3, values_only=True):
        handle, sku, prod, coste, _pf, psy = r[1], r[2], r[3], r[4], r[5], r[6]
        if not (handle or sku or prod):
            continue
        prod = str(prod).strip() if prod else ""
        segs = [x.strip() for x in prod.split("|")]
        size_prod = norm(segs[-1]) if len(segs) > 1 else ""
        h = str(handle).strip() if handle else None
        rows.append({
            "handle": h, "family": family(h),
            "sku": str(sku).strip() if sku else None,
            "producto": prod,
            "coste_E": float(coste) if isinstance(coste, (int, float)) else None,
            "psy_G": float(psy) if isinstance(psy, (int, float)) else None,
            "_size": size_prod,
        })
    by_sku, by_handle, by_family = defaultdict(list), defaultdict(list), defaultdict(list)
    for r in rows:
        if r["sku"]:
            by_sku[r["sku"]].append(r)
        if r["handle"]:
            by_handle[r["handle"]].append(r)
        if r["family"]:
            by_family[r["family"]].append(r)
    return rows, by_sku, by_handle, by_family


Q_PRODUCTS = """
query($cursor: String) {
  products(first: 40, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id handle title status
      variants(first: 250) {
        nodes {
          id sku title price compareAtPrice inventoryQuantity
          selectedOptions { name value }
          inventoryItem { unitCost { amount } }
        }
      }
    }
  }
}"""


def fetch_store(token):
    products, cursor = [], None
    while True:
        conn = gql(token, Q_PRODUCTS, {"cursor": cursor})["products"]
        for p in conn["nodes"]:
            vs = []
            for v in p["variants"]["nodes"]:
                uc = (v.get("inventoryItem") or {}).get("unitCost")
                vs.append({
                    "id": v["id"], "sku": (v.get("sku") or "").strip(),
                    "price": float(v["price"]) if v.get("price") is not None else None,
                    "cost": float(uc["amount"]) if uc and uc.get("amount") else None,
                    "stock": v.get("inventoryQuantity"),
                    "options": {o["name"]: o["value"] for o in (v.get("selectedOptions") or [])},
                })
            products.append({"id": p["id"], "handle": p["handle"], "title": p["title"],
                             "status": p["status"], "variants": vs})
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
    return products


def load_store(token, use_cache=False):
    if use_cache and CACHE.exists():
        return json.loads(CACHE.read_text())
    store = fetch_store(token)
    CACHE.write_text(json.dumps(store, ensure_ascii=False, indent=2))
    return store


# ───────────────────────── matching de IDENTIDAD (para precio≠G) ─────────────────────────
# Identidad = ¿qué fila del Excel ES esta variante? SOLO por SKU/talla. NUNCA por precio
# (usar el precio para identificar haría que precio==psy_G siempre y nunca detectaríamos
# una infravaloración). SKU_SIZE se excluye de la identidad por poco fiable (caso base 25/30kg).
def variant_size(v):
    for k in ("Tamaño", "Diámetro", "Diametro", "Peso", "Medida", "Tamano"):
        if k in v["options"]:
            return norm(v["options"][k])
    return ""


def match(handle, v, by_sku, by_handle):
    sku = v["sku"]
    if sku in by_sku and len(by_sku[sku]) == 1:
        return by_sku[sku][0], "EXACT_SKU"
    rows = by_handle.get(handle, [])
    if not rows:
        return None, "SIN_FUENTE"
    ex_sizes = defaultdict(list)
    for r in rows:
        ex_sizes[r["_size"]].append(r)
    szn = variant_size(v)
    if szn and szn in ex_sizes and len(ex_sizes[szn]) == 1:
        return ex_sizes[szn][0], "SIZE_MATCH"
    if len(rows) == 1 and szn == "" and not rows[0]["_size"]:
        return rows[0], "COLOR_ONLY"
    return None, ("AMBIGUOUS" if szn else "SIN_FUENTE")


# ───────────────────────── resolución de COSTE (para guardia anti-pérdida) ─────────────
# Para el coste SÍ vale usar el precio como clave (las telas comparten precio+coste de su
# chasis). Devolvemos SIEMPRE costes plausibles; el "floor" usa el MÁXIMO (conservador).
def _unique_cost_by_price(rows, price):
    if price is None:
        return None
    cands = {round(r["coste_E"], 2) for r in rows
             if r["psy_G"] is not None and abs(r["psy_G"] - price) < 0.01 and r["coste_E"] is not None}
    return cands.pop() if len(cands) == 1 else None


def candidate_costs(handle, v, by_sku, by_handle, by_family):
    """Todos los costes plausibles (sin IVA) de una variante, con su fuente.
    Cada vía SOLO aporta si es inequívoca; SKU_SIZE además exige consistencia net>=coste."""
    out = {}  # source -> cost
    sku = v["sku"]
    if sku in by_sku and len({round(r["coste_E"], 2) for r in by_sku[sku] if r["coste_E"] is not None}) == 1:
        c = next(r["coste_E"] for r in by_sku[sku] if r["coste_E"] is not None)
        out["EXACT_SKU"] = round(c, 2)
    rows = by_handle.get(handle, [])
    if rows:
        ex_sizes = defaultdict(list)
        for r in rows:
            ex_sizes[r["_size"]].append(r)
        szn = variant_size(v)
        if szn and szn in ex_sizes:
            cs = {round(r["coste_E"], 2) for r in ex_sizes[szn] if r["coste_E"] is not None}
            if len(cs) == 1:
                out["SIZE_MATCH"] = cs.pop()
        cph = _unique_cost_by_price(rows, v["price"])
        if cph is not None:
            out["PRICE_IN_HANDLE"] = cph
    fam = by_family.get(family(handle), [])
    cpf = _unique_cost_by_price(fam, v["price"])
    if cpf is not None:
        out["PRICE_IN_FAMILY"] = cpf
    # SKU_SIZE (talla embebida en SKU Excel) SOLO si es consistente (no implica pérdida)
    if rows:
        szn = variant_size(v)
        if szn and len(szn) >= 3:
            hits = [r for r in rows if szn in norm(r["sku"]) and r["coste_E"] is not None]
            cs = {round(r["coste_E"], 2) for r in hits}
            if len(cs) == 1:
                c = cs.pop()
                if v["price"] is None or net(v["price"]) >= c - 0.01:
                    out["SKU_SIZE"] = c
    return out


def resolve_cost(handle, v, by_sku, by_handle, by_family):
    """Mejor coste (para informe/backfill), por fiabilidad. Vivo > SKU > talla > precio."""
    if v["cost"] is not None:
        return v["cost"], "live"
    cands = candidate_costs(handle, v, by_sku, by_handle, by_family)
    for src in ("EXACT_SKU", "SIZE_MATCH", "PRICE_IN_HANDLE", "PRICE_IN_FAMILY", "SKU_SIZE"):
        if src in cands:
            return cands[src], src
    return None, None


def cost_floor(handle, v, by_sku, by_handle, by_family):
    """Suelo CONSERVADOR para la guardia: el coste vivo si existe; si no, el MÁXIMO de
    todos los costes plausibles (peor caso → nunca subestima el suelo)."""
    if v["cost"] is not None:
        return v["cost"]
    cands = candidate_costs(handle, v, by_sku, by_handle, by_family)
    return max(cands.values()) if cands else None


# ───────────────────────── auditoría ─────────────────────────
def audit(store, by_sku, by_handle, by_family):
    out, dup_store = [], defaultdict(list)
    for p in store:
        for v in p["variants"]:
            dup_store[v["sku"]].append((p["handle"], p["id"]))
            row, conf = match(p["handle"], v, by_sku, by_handle)
            exp_g = row["psy_G"] if row else None
            eff_cost, cost_src = resolve_cost(p["handle"], v, by_sku, by_handle, by_family)
            # ¿el precio coincide con algún psy_G de la FAMILIA? → es una config reconocida
            # (la identidad COLOR_ONLY/SIZE pudo apuntar a una fila hermana) → no es infra/sobre.
            fam_rows = by_family.get(family(p["handle"]), [])
            price_is_known_config = any(
                r["psy_G"] is not None and abs(v["price"] - r["psy_G"]) < 0.01 for r in fam_rows)
            status = []
            if eff_cost is not None and net(v["price"]) < eff_cost - 0.01:
                status.append("BAJO_COSTE")
            if exp_g is not None and abs(v["price"] - exp_g) > 0.01 and not price_is_known_config:
                status.append("INFRA" if v["price"] < exp_g else "SOBRE")
            if row is None:
                status.append("SIN_FUENTE")
            margin = round((net(v["price"]) - eff_cost) / net(v["price"]) * 100, 1) if eff_cost else None
            out.append({
                "handle": p["handle"], "sku": v["sku"], "status": p["status"],
                "price": v["price"], "neto": net(v["price"]),
                "cost_live": v["cost"], "cost_eff": eff_cost, "cost_src": cost_src,
                "margen_pct": margin, "psy_G": exp_g, "conf": conf,
                "estado": "OK" if not status else "+".join(status),
                "options": json.dumps(v["options"], ensure_ascii=False), "stock": v["stock"],
            })
    dups = {k: v for k, v in dup_store.items() if len({h for h, _ in v}) > 1}
    return out, dups


def print_audit(out, dups):
    below = [r for r in out if "BAJO_COSTE" in r["estado"]]
    infra = [r for r in out if "INFRA" in r["estado"]]
    sobre = [r for r in out if "SOBRE" in r["estado"]]
    sinf = [r for r in out if r["conf"] in ("SIN_FUENTE", "AMBIGUOUS")]
    nocost = [r for r in out if r["cost_eff"] is None]
    active_nocost = [r for r in nocost if r["status"] == "ACTIVE"]
    print("\n" + "=" * 70)
    print(f"AUDITORÍA DE PRECIOS — {len(out)} variantes")
    print("=" * 70)
    print(f"  🔴 BAJO COSTE (precio neto < coste): {len(below)}   ← PÉRDIDA, crítico")
    for r in below:
        print(f"       {r['handle']} / {r['sku']}  {r['price']}€ neto={r['neto']:.2f} < coste {r['cost_eff']} [{r['cost_src']}]")
    print(f"  🟠 INFRAVALORADO vs Col G (identidad fiable): {len(infra)}")
    for r in infra:
        print(f"       {r['handle']} / {r['sku']}  {r['price']}€ → G {r['psy_G']}€")
    print(f"  🟡 SOBREVALORADO vs Col G (identidad fiable): {len(sobre)}  (suele ser escalonado por color)")
    print(f"  ⚪ SIN fuente Excel (talla/color añadido): {len(sinf)}")
    print(f"  ℹ️  sin coste resoluble: {len(nocost)}  (de ellas ACTIVE: {len(active_nocost)})")
    print(f"  🔁 SKU duplicados en >1 producto: {len(dups)}")
    for sku, hs in list(dups.items())[:20]:
        print(f"       {sku} → {sorted({h for h, _ in hs})}")
    print(f"\n  CSV completo → {REPORT.name}")
    if not below:
        print("\n  ✅ NINGUNA variante por debajo de coste con los costes conocidos.")


def write_csv(out):
    cols = ["handle", "sku", "status", "price", "neto", "cost_live", "cost_eff",
            "cost_src", "margen_pct", "psy_G", "conf", "estado", "stock", "options"]
    with open(REPORT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(out, key=lambda x: (x["estado"] == "OK", x["handle"])):
            w.writerow(r)


# ───────────────────────── escritura (guardada) ─────────────────────────
MUT_PRICE = """
mutation($pid: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $pid, variants: $variants) {
    productVariants { id sku price }
    userErrors { field message }
  }
}"""
MUT_COST = """
mutation($pid: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $pid, variants: $variants) {
    productVariants { id sku inventoryItem { unitCost { amount } } }
    userErrors { field message }
  }
}"""


def index_store_by_sku(store):
    idx = defaultdict(list)
    for p in store:
        for v in p["variants"]:
            idx[v["sku"]].append((p, v))
    return idx


def _resolve_targets(idx, sku):
    """Devuelve (lista de (p,v), error|None). ABORTA si el SKU apunta a >1 producto."""
    hits = idx.get(sku, [])
    if not hits:
        return [], "no encontrado en tienda"
    handles = {p["handle"] for p, _ in hits}
    if len(handles) > 1:
        return [], f"SKU AMBIGUO: apunta a {len(handles)} productos {sorted(handles)} — desambigua a mano"
    return hits, None


def apply_prices(token, store, by_sku, by_handle, by_family, assignments, dry, allow_no_cost):
    idx = index_store_by_sku(store)
    per_product = defaultdict(list)
    blocked = []
    for sku, newp in assignments.items():
        hits, err = _resolve_targets(idx, sku)
        if err:
            print(f"  ⛔ {sku}: {err}"); blocked.append(sku); continue
        for (p, v) in hits:
            floor = cost_floor(p["handle"], v, by_sku, by_handle, by_family)
            if floor is None:
                if not allow_no_cost:
                    print(f"  ⛔ BLOQUEADO {sku}: coste DESCONOCIDO → no puedo garantizar net≥coste "
                          f"(usa --allow-no-cost si estás seguro)")
                    blocked.append(sku); continue
                print(f"  ⚠ {sku}: sin coste conocido, aplicando por --allow-no-cost")
            elif net(newp) < floor - 0.001:
                print(f"  ⛔ BLOQUEADO {sku}: precio {newp}€ → neto {net(newp):.2f} < coste {floor} (sería pérdida)")
                blocked.append(sku); continue
            print(f"  {'[DRY] ' if dry else '✏️  '}{sku}: {v['price']}€ → {newp}€  (neto {net(newp):.2f}, coste {floor})")
            per_product[p["id"]].append({"id": v["id"], "price": str(newp)})
    if blocked:
        print(f"\n  ⛔ {len(blocked)} SKU bloqueados (no se aplican): {blocked}")
    if dry:
        print("\n  (DRY-RUN — añade --apply para escribir)"); return
    for pid, vs in per_product.items():
        res = gql(token, MUT_PRICE, {"pid": pid, "variants": vs})
        errs = res["productVariantsBulkUpdate"]["userErrors"]
        print(f"  {'✗ '+str(errs) if errs else '✓ '+str(len(vs))+' precios'} en {pid}")


def apply_costs(token, store, assignments, dry):
    """Fija coste. Guardia: avisa y OMITE si el coste dejaría el precio actual a pérdida
    (net(precio) < coste) — eso indica un mal emparejamiento, no un coste real."""
    idx = index_store_by_sku(store)
    per_product = defaultdict(list)
    skipped = []
    for sku, c in assignments.items():
        hits, err = _resolve_targets(idx, sku)
        if err:
            print(f"  ⛔ {sku}: {err}"); skipped.append(sku); continue
        for (p, v) in hits:
            if v["price"] is not None and net(v["price"]) < c - 0.01:
                print(f"  ⚠ OMITIDO {sku}: coste {c} > neto del precio actual {net(v['price']):.2f} "
                      f"(precio {v['price']}€) → emparejamiento sospechoso, no escribo")
                skipped.append(sku); continue
            print(f"  {'[DRY] ' if dry else '✏️  '}{sku}: coste {v['cost']} → {c}")
            per_product[p["id"]].append({"id": v["id"], "inventoryItem": {"cost": str(c)}})
    if skipped:
        print(f"\n  ⚠ {len(skipped)} omitidos por la guardia: {skipped}")
    if dry:
        print("\n  (DRY-RUN — añade --apply para escribir)"); return
    for pid, vs in per_product.items():
        res = gql(token, MUT_COST, {"pid": pid, "variants": vs})
        errs = res["productVariantsBulkUpdate"]["userErrors"]
        print(f"  {'✗ '+str(errs) if errs else '✓ '+str(len(vs))+' costes'} en {pid}")


def backfill_costs(token, store, by_sku, by_handle, by_family, dry):
    """Rellena coste para variantes sin coste vivo usando resolve_cost (vías inequívocas
    y consistentes). apply_costs aplica además la guardia de emparejamiento."""
    assign, by_src = {}, defaultdict(int)
    for p in store:
        for v in p["variants"]:
            if v["cost"] is not None:
                continue
            c, src = resolve_cost(p["handle"], v, by_sku, by_handle, by_family)
            if c is not None and src != "live":
                assign[v["sku"]] = round(c, 2)
                by_src[src] += 1
    print(f"  Backfill (sin coste vivo): {len(assign)} variantes  fuentes={dict(by_src)}")
    apply_costs(token, store, assign, dry)


def parse_assignments(items):
    out = {}
    for it in items:
        k, _, val = it.partition("=")
        out[k.strip()] = round(float(val), 2)
    return out


# ───────────────────────── main ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--set-price", nargs="+", default=[])
    ap.add_argument("--set-cost", nargs="+", default=[])
    ap.add_argument("--backfill-costs", action="store_true")
    ap.add_argument("--allow-no-cost", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--use-cache", action="store_true")
    args = ap.parse_args()
    dry = not args.apply

    token = read_token()
    _, by_sku, by_handle, by_family = load_excel()
    writing = bool(args.set_price or args.set_cost or args.backfill_costs)
    store = load_store(token, use_cache=args.use_cache and not writing)

    if args.audit or not writing:
        out, dups = audit(store, by_sku, by_handle, by_family)
        write_csv(out)
        print_audit(out, dups)
    if args.set_cost:
        print("\n── Fijar costes ──")
        apply_costs(token, store, parse_assignments(args.set_cost), dry)
    if args.backfill_costs:
        print("\n── Backfill de costes ──")
        backfill_costs(token, store, by_sku, by_handle, by_family, dry)
    if args.set_price:
        print("\n── Fijar precios (guardia anti-pérdida fail-closed) ──")
        apply_prices(token, store, by_sku, by_handle, by_family,
                     parse_assignments(args.set_price), dry, args.allow_no_cost)


if __name__ == "__main__":
    main()
