#!/usr/bin/env python3
"""
AUDITORIA DE LO PUBLICADO — que hay hoy en las fichas activas de Santavila.

Nace de la pregunta de Sergio (20-08-2026): "tenemos algo creado que este mal?".
Hasta ahora, cada criterio nuevo obligaba a volver a mirar las fichas ya publicadas a mano.
Esto lo hace de una pasada y deja un informe reproducible.

Comprueba, ficha ACTIVE a ficha ACTIVE:
  · sin ninguna imagen               (no se puede vender)
  · una sola imagen                  (galeria pendiente)
  · imagenes duplicadas dentro de la ficha (misma imagen subida dos veces)
  · alt vacio                        (accesibilidad y SEO)
  · resolucion < 2000 px             (por debajo del minimo de la receta)
  · media en estado != READY         (Shopify la rechazo en silencio)
  · foto compartida con otra ficha   (no identifica esta variante)

  python3 scripts/auditar_galerias.py            # informe en pantalla
  python3 scripts/auditar_galerias.py --json     # ademas escribe docs/santavila/_auditoria_galerias.json
"""
import os, sys, json, urllib.request, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cargar_env():
    for l in open(os.path.join(ROOT, ".envlocal")):
        if "=" in l and not l.strip().startswith("#"):
            k, v = l.strip().split("=", 1)
            os.environ.setdefault(k, v.strip().strip("\"'"))

def gql(q, v=None):
    tok = os.environ.get("SHOPIFY_ADMIN_TOKEN") or os.environ.get("SHOPIFY_ACCESS_TOKEN")
    shop = os.environ.get("SHOPIFY_STORE", "mueblesexterior.myshopify.com").replace("https://", "")
    r = urllib.request.Request(f"https://{shop}/admin/api/2025-01/graphql.json",
        data=json.dumps({"query": q, "variables": v or {}}).encode(),
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))["data"]

Q = """query($after:String){ products(first:100, query:"status:active", after:$after){
  pageInfo{hasNextPage endCursor}
  nodes{ handle title
    priceRangeV2{maxVariantPrice{amount}}
    media(first:30){ nodes{ ... on MediaImage { id status alt image{ url width height } } } } } } }"""

def recoger():
    out, cur = [], None
    while True:
        d = gql(Q, {"after": cur})["products"]
        out += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]: break
        cur = d["pageInfo"]["endCursor"]
    return out

def clave(url):
    """Identifica la imagen por su nombre de fichero en el CDN, sin la version."""
    return url.split("?")[0].rsplit("/", 1)[-1]

def main():
    cargar_env()
    prods = recoger()
    compartidas = collections.defaultdict(list)
    for p in prods:
        for m in p["media"]["nodes"]:
            if m.get("image"): compartidas[clave(m["image"]["url"])].append(p["handle"])

    fallos = collections.defaultdict(list)
    for p in prods:
        h, t = p["handle"], p["title"]
        precio = float(p["priceRangeV2"]["maxVariantPrice"]["amount"])
        med = [m for m in p["media"]["nodes"] if m.get("image")]
        ficha = {"handle": h, "titulo": t, "precio": precio, "n": len(med)}
        if not med:
            fallos["sin_imagen"].append(ficha); continue
        if len(med) == 1: fallos["una_sola_imagen"].append(ficha)
        vistas = collections.Counter(clave(m["image"]["url"]) for m in med)
        if any(c > 1 for c in vistas.values()): fallos["duplicadas_dentro"].append(ficha)
        n_alt = sum(1 for m in med if not (m.get("alt") or "").strip())
        if n_alt: fallos["alt_vacio"].append({**ficha, "alt_vacios": n_alt})
        chicas = [m for m in med if min(m["image"]["width"], m["image"]["height"]) < 2000]
        if chicas: fallos["baja_resolucion"].append({**ficha, "cuantas": len(chicas),
                    "min_px": min(min(m["image"]["width"], m["image"]["height"]) for m in chicas)})
        no_ready = [m for m in med if m.get("status") != "READY"]
        if no_ready: fallos["no_ready"].append({**ficha, "cuantas": len(no_ready)})
        comp = [k for k in vistas if len(set(compartidas[k])) > 1]
        if comp: fallos["foto_compartida"].append({**ficha, "cuantas": len(comp)})

    print(f"\nFICHAS ACTIVAS: {len(prods)}\n" + "="*64)
    titulos = {
        "sin_imagen":       "SIN NINGUNA IMAGEN — no se puede vender",
        "una_sola_imagen":  "UNA SOLA IMAGEN — galeria pendiente",
        "duplicadas_dentro":"IMAGENES DUPLICADAS dentro de la misma ficha",
        "no_ready":         "MEDIA QUE NO LLEGO A READY — Shopify la rechazo",
        "baja_resolucion":  "POR DEBAJO DE 2000 px",
        "alt_vacio":        "TEXTO ALTERNATIVO VACIO",
        "foto_compartida":  "FOTO COMPARTIDA CON OTRA FICHA — no identifica la variante",
    }
    for k in titulos:
        v = fallos[k]
        print(f"\n{titulos[k]}: {len(v)}")
        if not v: continue
        v.sort(key=lambda x: -x["precio"])
        euros = sum(x["precio"] for x in v)
        print(f"   valor de catalogo afectado: {euros:,.0f} EUR".replace(",", "."))
        for x in v[:8]:
            extra = ""
            if "alt_vacios" in x: extra = f"  ({x['alt_vacios']} de {x['n']} sin alt)"
            elif "cuantas" in x:  extra = f"  ({x['cuantas']} de {x['n']})"
            if "min_px" in x:     extra += f"  min {x['min_px']} px"
            print(f"   {x['precio']:8,.0f} EUR  {x['n']:2} img  {x['titulo'][:52]}{extra}".replace(",", "."))
        if len(v) > 8: print(f"   ... y {len(v)-8} mas")

    con5 = [p for p in prods if len([m for m in p['media']['nodes'] if m.get('image')]) >= 5]
    print("\n" + "="*64)
    print(f"FICHAS CON GALERIA COMPLETA (>=5 imagenes): {len(con5)} de {len(prods)}")

    if "--json" in sys.argv:
        dest = os.path.join(ROOT, "docs", "santavila", "_auditoria_galerias.json")
        json.dump({"total_activas": len(prods), "con_galeria_completa": len(con5),
                   "fallos": fallos}, open(dest, "w"), ensure_ascii=False, indent=1)
        print(f"\n-> {dest}")

if __name__ == "__main__":
    main()
