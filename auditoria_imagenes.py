#!/usr/bin/env python3
"""
auditoria_imagenes.py  —  AUDITORÍA EN PROFUNDIDAD imagen ↔ producto.

Solo lectura. No modifica Shopify ni los archivos locales.

Produce:
  _estado_imagenes.json          → estado LIVE de imágenes por producto (Shopify)
  auditoria_imagenes_report.csv  → fila por producto: cobertura + asociación
  auditoria_imagenes_orphans.csv → imágenes locales NO asociadas a ningún producto
  auditoria_imagenes.json        → dump estructurado completo
y un RESUMEN por stdout.

Lógica de asociación (determinista, sin fuzzy salvo donde se marca):
  1. CDN match      → un archivo local cuyo nombre aparece en la galería viva de
                       un producto está, con certeza, asociado a ese producto.
  2. cutout/handle  → images_cutout/<handle>.png → producto <handle> (exacto).
  3. balliu slug    → nombre local = basename de URL en balliu_smart_mapping
                       (primary/gallery) o en balliu_catalog → slug → handle.
  4. hevea nombre   → token del nombre del archivo (BRANDON, DIVA…) = campo
                       'producto' de _excel_precios → handle(s). [fuzzy: marcado]
"""
from __future__ import annotations
import ast, json, os, re, sys, time, urllib.error, urllib.request, csv, collections
from pathlib import Path

BASE = Path(__file__).resolve().parent
SHOP = "mueblesexterior.myshopify.com"  # dominio interno; santavila.com es el público
API_TMPL = "https://{shop}/admin/api/2026-01/graphql.json"

try:
    from PIL import Image  # type: ignore
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

# ---------- folders ----------
PRODUCT_DIRS = {
    "balliu":       BASE / "images_balliu",
    "balliu_nuevas":BASE / "images_balliu" / "nuevas",
    "hevea_opt":    BASE / "images_optimized",
    "cutout":       BASE / "images_cutout",
    "lifestyle":    BASE / "images_lifestyle",
}
NONPRODUCT_DIRS = {
    "marca":        BASE / "imagen-corporativa",
    "theme":        BASE / "design_handoff_shopify_theme" / "assets",
    "extension":    BASE / "imgs-downloader-extension",
}
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif")


def read_token() -> str:
    for fname in (".envlocal", ".env.local", ".env"):
        p = BASE / fname
        if not p.exists():
            continue
        m = re.search(r"^SHOPIFY_ACCESS_TOKEN=(.*)$", p.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit("✗ SHOPIFY_ACCESS_TOKEN no encontrado")


def detect_shop() -> str:
    for fname in (".envlocal", ".env.local", ".env"):
        p = BASE / fname
        if not p.exists():
            continue
        m = re.search(r"(?:SHOPIFY_SHOP|SHOP|SHOPIFY_STORE)\w*=([^\s]+)", p.read_text(encoding="utf-8"))
        if m:
            v = m.group(1).strip().strip('"').strip("'")
            if "myshopify" in v:
                return v.replace("https://", "").replace("http://", "").rstrip("/")
    return SHOP


def gql(token: str, shop: str, query: str, variables=None) -> dict:
    api = API_TMPL.format(shop=shop)
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    for attempt in range(1, 7):
        try:
            req = urllib.request.Request(
                api, data=payload,
                headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                method="POST")
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.loads(r.read())
            if data.get("errors"):
                raise RuntimeError(json.dumps(data["errors"])[:400])
            return data["data"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(float(e.headers.get("Retry-After", 2))); continue
            sys.stderr.write(f"HTTP {e.code}: {e.read()[:300]}\n"); time.sleep(1.5*attempt)
        except Exception as ex:
            sys.stderr.write(f"retry {attempt}: {ex}\n"); time.sleep(1.5*attempt)
    raise RuntimeError("GraphQL falló tras reintentos")


Q = """
query($cursor: String) {
  products(first: 50, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      handle title status productType vendor
      mediaCount { count }
      media(first: 25) {
        nodes {
          mediaContentType
          ... on MediaImage { image { url width height } }
        }
      }
    }
  }
}
"""


def fetch_live(token, shop):
    out, cursor = [], None
    while True:
        d = gql(token, shop, Q, {"cursor": cursor})
        conn = d["products"]
        for n in conn["nodes"]:
            media = []
            for m in n["media"]["nodes"]:
                img = (m or {}).get("image") or {}
                media.append({
                    "type": m.get("mediaContentType"),
                    "url": img.get("url"),
                    "w": img.get("width"), "h": img.get("height"),
                })
            out.append({
                "handle": n["handle"], "title": n["title"], "status": n["status"],
                "type": n.get("productType") or "", "vendor": n.get("vendor") or "",
                "mediaCount": (n.get("mediaCount") or {}).get("count", 0),
                "media": media,
            })
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
    return out


# ---------- normalización de nombres ----------
def cdn_basename(url: str) -> str:
    """Basename del archivo en una URL de CDN Shopify, decodificando _XX y quitando ?v=."""
    if not url:
        return ""
    b = url.split("?")[0].rsplit("/", 1)[-1]
    # Shopify reemplaza chars por _<hex hex...>; para el match basta lowercase + quitar sufijos uuid
    b = b.lower()
    b = re.sub(r"_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "", b)  # uuid de dedupe
    return b


def norm(name: str) -> str:
    n = name.lower()
    n = re.sub(r"\.(jpg|jpeg|png|webp|gif|avif)$", "", n)
    n = n.replace("-scaled", "")
    n = re.sub(r"_c3_[0-9a-f]{2}|_20|_[0-9a-f]{8}-[0-9a-f-]{27}", "", n)  # encoded shopify
    n = re.sub(r"[^a-z0-9]", "", n)
    return n


def main():
    token = read_token()
    shop = detect_shop()
    sys.stderr.write(f"→ Shopify: {shop}\n")
    live = fetch_live(token, shop)
    (BASE / "_estado_imagenes.json").write_text(json.dumps(live, ensure_ascii=False, indent=1))

    # índice: norm(cdn filename) -> set(handles) que usan ese archivo vivo
    cdn_index = collections.defaultdict(set)
    for p in live:
        for m in p["media"]:
            bn = cdn_basename(m["url"])
            if bn:
                cdn_index[norm(bn)].add(p["handle"])

    live_by_handle = {p["handle"]: p for p in live}
    handles = set(live_by_handle)

    # ---------- mapeos balliu ----------
    smart = json.load(open(BASE/"balliu_smart_mapping.json"))
    catalog = json.load(open(BASE/"balliu_catalog.json"))
    # basename(img balliu) -> slug
    balliu_imgbn_to_slug = {}
    for slug, e in catalog.items():
        for u in e.get("images", []) or []:
            balliu_imgbn_to_slug[norm(os.path.basename(u.split("?")[0]))] = slug
    # slug -> set(handles)
    slug_to_handles = collections.defaultdict(set)
    # basename(primary/gallery) -> set(handles)
    balliu_imgbn_to_handles = collections.defaultdict(set)
    for e in smart:
        h = e["shopify_handle"]
        if e.get("balliu_slug"):
            slug_to_handles[e["balliu_slug"]].add(h)
        for key in ("primary_image", "gallery_images"):
            v = e.get(key)
            if not v:
                continue
            urls = []
            if isinstance(v, str) and v.strip().startswith("["):
                try: urls = ast.literal_eval(v)
                except Exception: urls = []
            elif isinstance(v, str):
                urls = [v]
            for u in urls:
                balliu_imgbn_to_handles[norm(os.path.basename(u.split("?")[0]))].add(h)

    # ---------- proveedor por handle (excel) ----------
    excel = json.load(open(BASE/"_excel_precios.json"))
    handle_prov = {r["handle"]: r.get("proveedor") for r in excel if r.get("handle")}
    # token producto hevea (BRANDON) -> handles
    hevea_tok_to_handles = collections.defaultdict(set)
    for r in excel:
        if (r.get("proveedor") or "").lower() != "hevea":
            continue
        prod = (r.get("producto") or "")
        h = r.get("handle")
        if not h:
            continue
        for tok in re.findall(r"[A-Za-zÁÉÍÓÚÑ]{4,}", prod):
            hevea_tok_to_handles[tok.lower()].add(h)

    # ---------- inventario local ----------
    def dims(fp):
        if not HAVE_PIL:
            return (None, None)
        try:
            with Image.open(fp) as im:
                return im.size
        except Exception:
            return (None, None)

    local = []
    for cat, d in PRODUCT_DIRS.items():
        if not d.exists():
            continue
        for f in sorted(os.listdir(d)):
            fp = d / f
            if not fp.is_file() or fp.suffix.lower() not in IMG_EXT:
                continue
            w, h = dims(fp)
            local.append({
                "folder": cat, "file": f, "path": str(fp.relative_to(BASE)),
                "stem": os.path.splitext(f)[0], "bytes": fp.stat().st_size,
                "w": w, "h": h, "matches": [], "method": None,
            })

    # ---------- asociación ----------
    for im in local:
        nstem = norm(im["stem"])
        matched, method = set(), None
        # 1. CDN (ya subida) — certeza
        if nstem in cdn_index:
            matched |= cdn_index[nstem]; method = "cdn_live"
        # 2. cutout por handle
        if not matched and im["folder"] == "cutout":
            if im["stem"] in handles:
                matched.add(im["stem"]); method = "handle_exacto"
        if not matched and im["folder"] == "lifestyle":
            # lifestyle: nombre tipo <slug>_cutout / damasco_v5...
            base = re.split(r"_(cutout|rmbg|isnet|v\d|escala|set)", im["stem"])[0]
            for h in handles:
                if norm(base) and norm(base) in norm(h):
                    matched.add(h)
            if matched: method = "lifestyle_aprox"
        # 3. balliu por slug/imagen
        if not matched and im["folder"] in ("balliu", "balliu_nuevas"):
            if nstem in balliu_imgbn_to_handles:
                matched |= balliu_imgbn_to_handles[nstem]; method = "balliu_img"
            elif nstem in balliu_imgbn_to_slug:
                slug = balliu_imgbn_to_slug[nstem]
                matched |= slug_to_handles.get(slug, set()); method = "balliu_slug"
        # 4. hevea por token de nombre
        if not matched and im["folder"] == "hevea_opt":
            toks = re.findall(r"[A-Za-z]{4,}", im["stem"])
            cands = set()
            for t in toks:
                cands |= hevea_tok_to_handles.get(t.lower(), set())
            if cands:
                matched |= cands; method = "hevea_token(fuzzy)"
        im["matches"] = sorted(matched)
        im["method"] = method

    # imágenes asociadas por handle
    handle_local = collections.defaultdict(list)
    for im in local:
        for h in im["matches"]:
            handle_local[h].append(im["path"])

    # ---------- salidas ----------
    # report por producto
    rows = []
    for p in live:
        h = p["handle"]
        rows.append({
            "handle": h, "vendor": p["vendor"] or handle_prov.get(h, ""),
            "type": p["type"], "status": p["status"],
            "live_media": p["mediaCount"],
            "local_assoc": len(handle_local.get(h, [])),
            "local_files": " | ".join(handle_local.get(h, [])),
        })
    with open(BASE/"auditoria_imagenes_report.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    # orphans
    orphans = [im for im in local if not im["matches"]]
    with open(BASE/"auditoria_imagenes_orphans.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["folder","file","bytes","w","h"]); w.writeheader()
        for im in orphans:
            w.writerow({k: im[k] for k in ("folder","file","bytes","w","h")})

    # dump
    json.dump({"live": live, "local": local,
               "nonproduct": {k: (len([x for x in os.listdir(v) if (v/x).suffix.lower() in IMG_EXT]) if v.exists() else 0)
                              for k,v in NONPRODUCT_DIRS.items()}},
              open(BASE/"auditoria_imagenes.json","w"), ensure_ascii=False, indent=1)

    # ---------- resumen ----------
    by_media = collections.Counter(p["mediaCount"] for p in live)
    by_vendor = collections.Counter((p["vendor"] or handle_prov.get(p["handle"],"?")) for p in live)
    no_media = [p for p in live if p["mediaCount"] == 0]
    one_media = [p for p in live if p["mediaCount"] == 1]
    method_counts = collections.Counter(im["method"] for im in local)
    folder_counts = collections.Counter(im["folder"] for im in local)
    res_buckets = collections.Counter()
    for im in local:
        if im["w"]:
            mx = max(im["w"], im["h"] or 0)
            res_buckets["≤800" if mx<=800 else "801-1200" if mx<=1200 else "1201-2000" if mx<=2000 else ">2000"] += 1
        else:
            res_buckets["desconocida"] += 1

    P = print
    P("\n================  RESUMEN AUDITORÍA IMÁGENES  ================")
    P(f"PIL/Pillow disponible (medir resolución): {HAVE_PIL}")
    P(f"\nPRODUCTOS LIVE: {len(live)}  | por vendor: {dict(by_vendor)}")
    P(f"Distribución nº imágenes/producto (live): {dict(sorted(by_media.items()))}")
    P(f"  · Productos SIN imagen (0): {len(no_media)}")
    P(f"  · Productos con SOLO 1 imagen: {len(one_media)}")
    P(f"\nIMÁGENES LOCALES (carpetas de producto): {len(local)}  por carpeta: {dict(folder_counts)}")
    P(f"Resolución (lado mayor px): {dict(res_buckets)}")
    P(f"Método de asociación: {dict(method_counts)}")
    P(f"Imágenes locales SIN asociar (orphans): {len(orphans)}")
    P(f"Productos con ≥1 imagen local asociada: {len([h for h in handle_local if h in handles])}")
    P(f"\nNO-producto (marca/tema/extensión): "
      + ", ".join(f"{k}={len([x for x in os.listdir(v) if (v/x).suffix.lower() in IMG_EXT])}" for k,v in NONPRODUCT_DIRS.items() if v.exists()))
    P("\n--- Productos SIN imagen (handle | vendor | type | status) ---")
    for p in no_media:
        P(f"  {p['handle']}  | {p['vendor']} | {p['type']} | {p['status']}")
    P("\nArchivos escritos: _estado_imagenes.json, auditoria_imagenes_report.csv, "
      "auditoria_imagenes_orphans.csv, auditoria_imagenes.json")


if __name__ == "__main__":
    main()
