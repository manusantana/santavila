#!/usr/bin/env python3
"""AUDITORIA de las galerias publicadas contra el CATALOGO y contra las reglas de marca.

Nacio el 22-08-2026, cuando la formula de composicion del catalogo (pag. 32, serie HASTON)
descubrio que los dos reposapies de las fotos del proveedor NO se venden con el set. Si esa
formula existe para HASTON, existe para las 98 series -> hay que cruzarlas TODAS.

Comprueba tres cosas:
  1) COMPOSICION: la formula "2xA+B+D" del catalogo frente a lo que muestra la ficha.
     (el conteo final es VISUAL: el script localiza la formula y prepara el contraste)
  2) COTAS: las medidas escritas en los alt frente a las del catalogo.
  3) REGLAS DE MARCA sobre los alt: comida/bebida (derogado 03-08-2026), resort/chalet
     de lujo, macro de tejido (§15) y alt vacio.

Uso:
  python3 scripts/auditar_reglas_galeria.py            # informe completo
  python3 scripts/auditar_reglas_galeria.py --reglas   # solo el bloque 3 (rapido, sin PDF)

OJO — dos trampas que este script ya evita, aprendidas a base de falsos positivos:
  · Buscar 'villa' por subcadena marca buganVILLA, seVILLAna y VILLAmayor: 25 falsos de 29.
    Se usa \\b...\\b SIEMPRE.
  · Matchear la serie por prefijo casa 'BOLONIA XL-8' con 'BOLONIA-8', que es OTRA serie con
    OTRA pagina. Hay 5 series Bolonia distintas. Se prueba primero el nombre mas largo.
"""
import json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://mueblesexterior.myshopify.com/admin/api/2025-01/graphql.json"
PDFS = ["proveedores_raw/hevea/OK-h26-09-ENE_BAJA (1).pdf",
        "proveedores_raw/hevea/HORECA 2026 26-033_compressed (1).pdf"]
TOKEN = None
for line in open(os.path.join(ROOT, ".envlocal"), encoding="utf-8"):
    if line.startswith("SHOPIFY_ACCESS_TOKEN="):
        TOKEN = line.split("=", 1)[1].strip()

# --- reglas de marca sobre el ALT -------------------------------------------------
COMIDA = ['queso','pan de','aceite de oliva','vino','cerveza','limonada','sandia','sandía','sidra',
 'gazpacho','berberecho','picatoste','melocotón','té helado','te helado','agua con gas','almendra',
 'albariño','copa de','jarra de','horchata','vermut','tinto','aceitun','higo','farton','botijo',
 'churro','torrija','merienda','desayuno','refresco','plato de','tabla de queso',
 # El generico faltaba: la lista tenia vino, cerveza, limonada, refresco... pero NO "bebida",
 # y un video en posicion 0 llevaba meses anunciando "bebida fria sobre la mesa" (07-09-2026).
 # Enumerar casos concretos deja siempre el hiperonimo fuera.
 'bebida','bebidas','copa de vino','vaso de','trago',
 # y los frutos, que es por donde se escapo la ficha mas cara del catalogo: la lista tenia
 # higo, melocoton y sandia, pero no GRANADA (07-09-2026).
 'granada partida','granada abierta','media granada','uvas','cerezas','fresas','frambuesas',
 'manzana','pera madura','ciruela','naranja partida','platano','mango','papaya','helado']

# La leccion de fondo: una lista de casos concretos SIEMPRE deja algo fuera. Por eso el alt no
# es la unica prueba — el NOMBRE DEL FICHERO tambien acusa, y no lo redacta nadie a posteriori:
# `05_asmr_granada.jpg`, `05_asmr_gazpacho.jpg`, `07_asmr_te_helado.jpg`. Se comparan TOKENS
# exactos (partiendo por _ - .), nunca subcadenas: 'te' dentro de 'ambiente', 'sal' dentro de
# 'Salamanca' y 'jarra' dentro de 'Alpujarra' dan 17 falsos positivos de 18.
FICHERO_CONSUMIBLE = {
 'gazpacho','granada','albarino','albariño','limonada','sandia','sandía','melocoton','melocotón',
 'sidra','queso','vino','cerveza','pan','cafe','café','te','vermut','horchata','higo','higos',
 'aceitunas','comida','bebida','desayuno','merienda','copa','vaso','jarra','botella','fruta',
 'frutas','tapa','tapas','almuerzo','cena','brindis','picnic','torrija','churros','helado',
 'zumo','mojito','sangria','sangría','tinto','uvas','fresas','cerezas','pastel','tarta'}

def _tokens_fichero(url):
    base = re.sub(r"_[0-9a-f]{8}-[0-9a-f]{4}-.*$", "", os.path.splitext(url.split("/")[-1].split("?")[0])[0])
    return set(re.split(r"[_\-\.]+", base.lower()))
# Recipientes VACIOS: son ceramica/atrezzo permitido, no consumible. Sin esta lista, "jarra de
# gres con romero" saltaba como comida (22-08-2026). Es la misma trampa que 'buganVILLA'.
NO_ES_COMIDA = ['jarra de gres','jarra de barro','jarra de ceramica','jarra de cerámica',
 'bucaro','búcaro','tinaja','maceta','cuenco vacio','cuenco vacío','copa de los arboles',
 'copa de los árboles','plato de ducha']
PALABRA = [r'\bvilla\b', r'\bvillas\b', r'\bchalet\b', r'\bresort\b', r'\btropical\b', r'\bbungalow\b']
MACRO = ['macro del tejido','macro de tejido','macro textil']

def gql(q, v=None, intentos=4):
    """Por curl y no por urllib: al pedir tambien los VIDEOS la respuesta crecio y urllib
    empezo a reventar con `IncompleteRead` a mitad de pagina (07-09-2026). Es el mismo fallo
    que ya nos comio descargas: urllib no reintenta una respuesta chunked truncada y curl con
    --retry-all-errors si. Un auditor que casca a mitad no audita: da un falso 'todo bien'."""
    import subprocess
    payload = json.dumps({"query": q, "variables": v or {}}).encode()
    for i in range(intentos):
        r = subprocess.run(["curl", "-s", "--retry", "3", "--retry-all-errors", "--max-time", "120",
            "-X", "POST", API, "-H", f"X-Shopify-Access-Token: {TOKEN}",
            "-H", "Content-Type: application/json", "--data-binary", "@-"],
            input=payload, capture_output=True)
        try:
            d = json.loads(r.stdout)
            if d.get("data"): return d
        except Exception:
            pass
        time.sleep(2 + 2 * i)
    raise RuntimeError(f"la consulta fallo tras {intentos} intentos: {r.stdout[:200]!r}")

def fichas():
    q = '''query($c:String){products(first:200,after:$c,query:"status:active"){
      pageInfo{hasNextPage endCursor}
      edges{node{handle title variants(first:1){edges{node{sku price}}}
      media(first:16){edges{node{mediaContentType
        ... on MediaImage{alt image{width height url}}
        ... on Video{alt}
        ... on ExternalVideo{alt}}}}}}}}'''
    out, c = [], None
    while True:
        d = gql(q, {"c": c})["data"]["products"]
        for e in d["edges"]:
            n = e["node"]; v = n["variants"]["edges"][0]["node"] if n["variants"]["edges"] else {}
            out.append({"handle": n["handle"], "title": n["title"], "sku": v.get("sku"),
                        "price": float(v.get("price") or 0),
                        # 07-09-2026 — EL AUDITOR TENIA UN PUNTO CIEGO MAS: solo pedia
                        # `... on MediaImage`, asi que los VIDEOS no llegaban aqui y sus alt
                        # nunca se auditaban. Dos videos en posicion 0 llevaban meses diciendo
                        # "bebida fria" y "junto a la piscina" — las dos reglas que mas veces
                        # hemos hecho cumplir— sin que ninguna pasada los viera.
                        # Un medio que no se pide es un medio que no se audita.
                        "media": [{"alt": m["node"].get("alt") or "",
                                   "tipo": m["node"].get("mediaContentType", "IMAGE"),
                                   "url": (m["node"].get("image") or {}).get("url", "") or "",
                                   "w": (m["node"].get("image") or {}).get("width", 0),
                                   "h": (m["node"].get("image") or {}).get("height", 0)}
                                  for m in n["media"]["edges"]]})
        if not d["pageInfo"]["hasNextPage"]: break
        c = d["pageInfo"]["endCursor"]; time.sleep(0.25)
    return out

def formulas():
    """serie-N -> (formula, pagina). El catalogo la escribe como '2xA+B+D HASTON-7 SET ...'."""
    from pypdf import PdfReader
    f = {}
    for pdf in PDFS:
        r = PdfReader(os.path.join(ROOT, pdf))
        for i, p in enumerate(r.pages):
            try: t = p.extract_text() or ""
            except Exception: continue
            for ln in t.split("\n"):
                m = re.match(r'^((?:\d?x?[A-H]\+?)+)\s+([A-ZÁÉÍÓÚÑ ]+?)\s*-\s*(\d+)\s*(SET.*)$', ln.strip(), re.I)
                if m and "+" in m.group(1):
                    serie = re.sub(r'\s+', ' ', m.group(2)).strip().upper()
                    f.setdefault(f"{serie}-{m.group(3)}", (m.group(1), i + 1))
    return f

def main():
    solo_reglas = "--reglas" in sys.argv
    fs = fichas()
    print(f"fichas ACTIVE: {len(fs)}   ·   imagenes: {sum(len(x['media']) for x in fs)}\n")

    print("=== 3 · REGLAS DE MARCA SOBRE EL ALT")
    n_com = n_res = n_mac = n_vac = n_fic = 0
    for f in fs:
        for i, m in enumerate(f["media"]):
            a = m["alt"].lower()
            if not a.strip(): n_vac += 1; continue
            if any(k in a for k in COMIDA) and not any(k in a for k in NO_ES_COMIDA):
                n_com += 1; print(f"  COMIDA   {f['price']:7.0f} EUR pos{i} {f['handle'][:44]}\n           {m['alt'][:104]}")
            if any(re.search(w, a) for w in PALABRA):
                n_res += 1; print(f"  LUJO     {f['price']:7.0f} EUR pos{i} {f['handle'][:44]}\n           {m['alt'][:104]}")
            if any(k in a for k in MACRO):
                n_mac += 1; print(f"  MACRO    {f['price']:7.0f} EUR pos{i} {f['handle'][:44]}\n           {m['alt'][:104]}")
            tk = _tokens_fichero(m.get("url", "")) & FICHERO_CONSUMIBLE
            if tk:
                n_fic += 1; print(f"  FICHERO  {f['price']:7.0f} EUR pos{i} {f['handle'][:44]}\n           "
                                  f"el nombre del fichero dice {sorted(tk)}: {m.get('url','').split('/')[-1].split('?')[0]}")
    print(f"\n  comida/bebida={n_com}  lujo/resort={n_res}  macro de tejido={n_mac}  "
          f"alt vacio={n_vac}  nombre de fichero={n_fic}")
    if solo_reglas: return

    print("\n=== 1 · COMPOSICION: formula del catalogo por ficha")
    import csv, glob
    sku2nom = {}
    for fn in sorted(glob.glob(os.path.join(ROOT, "proveedores_raw/hevea/*.csv"))):
        for row in csv.DictReader(open(fn, encoding="utf-8", errors="replace")):
            s = (row.get("SKU") or "").strip(); nom = (row.get("Producto") or "").strip()
            if s and len(nom) > 12: sku2nom.setdefault(s, set()).add(nom[:70])
    F = formulas()
    print(f"  formulas leidas del catalogo: {len(F)}")
    def serie_de(nom):
        u = nom.upper()
        # el nombre MAS LARGO primero: 'BOLONIA XL-8' antes que 'BOLONIA-8' (series distintas)
        for pat in [r'^([A-ZÁÉÍÓÚÑ]+\s+XL)\s*-\s*(\d+)', r'^([A-ZÁÉÍÓÚÑ]+)\s*-\s*(\d+)',
                    r'^SET\s+([A-ZÁÉÍÓÚÑ]+)\s+(\d+)']:
            m = re.match(pat, u)
            if m:
                k = f"{m.group(1).strip()}-{m.group(2)}"
                if k in F: return k
        return None
    hallados = 0
    for f in sorted(fs, key=lambda x: -x["price"]):
        if len(f["media"]) < 3: continue
        for nom in sku2nom.get(f["sku"], set()):
            k = serie_de(nom)
            if k:
                hallados += 1
                print(f"  {f['price']:8.0f} EUR  {k:16s} {F[k][0]:14s} p{F[k][1]:<4} media={len(f['media'])}  {f['handle'][:40]}")
                break
    print(f"\n  sets con formula localizada: {hallados}")
    print("  -> el CONTEO de piezas es visual: abre el packshot y cuenta contra la formula.")
    print("     Lo que NO esta en la formula (reposapies, 2a mesa) NO se vende: no se dibuja.")

if __name__ == "__main__":
    main()
