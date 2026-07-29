#!/usr/bin/env python3
"""
Publica en Shopify la galería generada de un producto (masters locales de `images_generated/`).

Flujo (rol §7.4 / FLUJO_IMAGEN_PRODUCTO paso 7):
  stagedUploadsCreate -> POST de los bytes -> productCreateMedia -> espera READY
  -> productReorderMedia (orden de la receta) -> borra los media antiguos (con backup de IDs).

Por defecto DRY-RUN. Con --apply ejecuta de verdad.

  python3 scripts/publicar_galeria_producto.py                 # dry-run de todo
  python3 scripts/publicar_galeria_producto.py --apply          # sube todo
  python3 scripts/publicar_galeria_producto.py --solo brandon   # una sola ficha

Seguridad:
  - Los IDs de los media eliminados se guardan en `images_generated/_backup_media_borrados.json`
    (permite revertir si hiciera falta).
  - Si alguna imagen nueva no llega a READY, NO se borra nada de esa ficha.
"""
import json, os, sys, time, uuid, urllib.request, mimetypes

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2025-01/graphql.json"
APPLY = "--apply" in sys.argv
SOLO = None
if "--solo" in sys.argv:
    SOLO = sys.argv[sys.argv.index("--solo") + 1]

TOKEN = None
for line in open(os.path.join(ROOT, ".envlocal"), encoding="utf-8"):
    if line.startswith("SHOPIFY_ACCESS_TOKEN="):
        TOKEN = line.split("=", 1)[1].strip()

# carpeta -> (handle, {fichero: alt en español})
# TANDA 2026-07-29 (activa)
GALERIAS = {
    "dounvil2p": ("set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-2", {
        "01_packshot.jpg": "Set de jardín contemporáneo de aluminio blanco con sofá de 2 plazas, dos sillones con aspa lateral y mesa de centro de lamas, cojines color arena",
        "02_ambiente_exterior_rioja.jpg": "Set de jardín blanco en una terraza de piedra sobre los viñedos de La Rioja, con la Sierra de Cantabria al fondo",
        "03_ambiente_interior_calado.jpg": "Sofá y sillones de exterior en una sala abovedada de piedra arenisca, con el arco abierto al viñedo",
        "04_asmr_aspa.jpg": "Detalle del aspa en X de aluminio blanco mate del lateral del sillón sobre la trama del cojín color arena",
        "05_asmr_vino_uvas.jpg": "Copa de vino tinto joven y un racimo de uvas con el polvillo intacto sobre la mesa de lamas blanca",
    }),
}

# TANDA 2026-07-28 D (ya publicada)
GALERIAS_TANDA_D = {
    "odin3p": ("set-jardin-3-plazas-elegante-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín elegante de aluminio antracita con sofá de 3 plazas, dos sillones de brazo plano y mesa de centro de lamas, cojines gris claro",
        "02_ambiente_exterior_segovia.jpg": "Set de jardín antracita en una terraza de sillar granítico castellana, con lavanda en pilón de piedra y la sierra de Guadarrama al fondo",
        "03_ambiente_interior_soportal.jpg": "Sofá y sillones de exterior bajo el soportal de arcos de granito de una casona castellana, abierto al pinar",
        "04_asmr_brazo.jpg": "Detalle del brazo plano de aluminio antracita mate del sofá junto a la trama del cojín gris claro",
        "05_asmr_botijo.jpg": "Botijo de barro sudando agua fría sobre la mesa de lamas, con el cerco húmedo y un vaso de agua al lado",
    }),
    "manhattan3p": ("set-jardin-3-plazas-urbano-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín urbano de aluminio blanco con sofá de 3 plazas, dos sillones de base voladiza y mesa de centro de lamas, cojines gris claro",
        "02_ambiente_exterior_sevilla.jpg": "Set de jardín blanco en una azotea sevillana de suelo de ladrillo, con jazmín en tinaja y la Giralda sobre los tejados",
        "03_ambiente_interior_celosia.jpg": "Sofá y sillones de exterior en una sala encalada sevillana, con una celosía de ladrillo dibujando la luz sobre el suelo",
        "04_asmr_perfil.jpg": "Detalle del brazo plano blanco del sillón y su base voladiza de aluminio, con la sombra dura del sol andaluz",
        "05_asmr_gazpacho.jpg": "Vaso alto de gazpacho helado con la condensación resbalando sobre las lamas blancas de la mesa, junto a un cuenco de picatostes",
    }),
}

# TANDA 2026-07-28 C (ya publicada)
GALERIAS_TANDA_C = {
    "dounvil3p": ("set-jardin-3-plazas-elegante-sofa-3-plazas-2-sillones-mesa-2", {
        "01_packshot.jpg": "Set de jardín elegante de aluminio antracita con sofá de 3 plazas, dos sillones con aspa lateral y mesa de centro de lamas, cojines azul grisáceo",
        "02_ambiente_exterior_costadamorte.jpg": "Set de jardín antracita en una terraza de granito de la Costa da Morte, con tojo en flor, brezo y el Atlántico rompiendo abajo",
        "03_ambiente_interior_galeria.jpg": "Sofá y sillones de exterior en una galería acristalada gallega de carpintería blanca, con el mar y las rocas al otro lado del cristal",
        "04_asmr_aspa.jpg": "Detalle del aspa en X de aluminio antracita mate del lateral del sillón junto a la costura del cojín azul grisáceo",
        "05_asmr_albarino.jpg": "Copa de albariño frío con condensación y un plato de berberechos con limón sobre la mesa de lamas",
    }),
    "acapulco3p": ("set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-5", {
        "01_packshot.jpg": "Set de jardín contemporáneo de aluminio blanco con sofá de 3 plazas, dos sillones y mesa de centro con tablero de cristal, cojines gris claro",
        "02_ambiente_exterior_valencia.jpg": "Set de jardín blanco en una terraza valenciana de suelo de barro, con persianas de esparto, romero y un naranjo en tinaja",
        "03_ambiente_interior_porche.jpg": "Sofá y sillones de exterior en un porche valenciano encalado con persiana de esparto y suelo de barro, abierto al jardín",
        "04_asmr_cristal.jpg": "Detalle del canto del tablero de cristal de la mesa apoyado en el perfil de aluminio blanco mate",
        "05_asmr_horchata.jpg": "Vaso de horchata fría con fartons sobre el tablero de cristal de la mesa de centro",
    }),
}

# TANDA 2026-07-28 B (ya publicada)
GALERIAS_TANDA_B = {
    "diva2p": ("set-jardin-bicolor-2-plazas-bicolor-sofa-2-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín bicolor de aluminio gris tórtola con sofá de 2 plazas, dos sillones de lamas antracita y mesa de centro, cojines crudo",
        "02_ambiente_exterior_cordoba.jpg": "Set de jardín bicolor en un patio cordobés encalado, con macetas de geranios en la pared y un limonero en tinaja",
        "03_ambiente_interior_zaguan.jpg": "Sofá y sillones de exterior en el zaguán abovedado de una casa cordobesa, con suelo de barro y reja de forja al patio",
        "04_asmr_lamas.jpg": "Detalle del lateral del sillón: lamas de aluminio antracita encajadas en el marco gris tórtola",
        "05_asmr_naranjas.jpg": "Naranjas partidas y un vaso de zumo recién exprimido sobre el tablero de madera de la mesa de centro",
    }),
    "albania2p": ("set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-4", {
        "01_packshot.jpg": "Set de jardín elegante de aluminio antracita con sofá de 2 plazas, dos sillones de travesaño en V y mesa de centro de lamas, cojines crudo",
        "02_ambiente_exterior_asturias.jpg": "Set de jardín antracita en una terraza asturiana sobre el puerto pesquero, con las casas del pueblo y las barcas al fondo",
        "03_ambiente_interior_porche.jpg": "Sofá y sillones de exterior en el porche de columnas de piedra de una casona asturiana, abierto al prado y al mar",
        "04_asmr_travesano.jpg": "Detalle del travesaño diagonal en V de aluminio antracita del sillón junto a la costura del cojín crudo",
        "05_asmr_sidra.jpg": "Vaso ancho de sidra natural recién escanciada junto a un plato de queso y pan sobre la mesa de lamas",
    }),
}

# TANDA 2026-07-28 A (ya publicada, se conserva como referencia)
GALERIAS_TANDA_A = {
    "brandon2p": ("set-jardin-aluminio-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín contemporáneo de aluminio antracita con sofá de 2 plazas, dos sillones y dos mesas nido redondas, tapizado gris",
        "02_ambiente_exterior_bilbao.jpg": "Set de jardín de aluminio antracita en la terraza de hormigón de un loft de Bilbao, con la ría al fondo",
        "03_ambiente_interior_loft.jpg": "Sofá de 2 plazas y sillones de exterior en un loft acristalado de Bilbao, con suelo de hormigón pulido y pared de ladrillo",
        "04_asmr_chenille.jpg": "Detalle del brazo del sofá: tejido gris jaspeado de chenille y perfil de aluminio antracita mate",
        "05_asmr_cerveza.jpg": "Cerveza fría con condensación y un plato de aceitunas sobre la mesa nido redonda de tablero cerámico gris",
    }),
    "diva3p": ("set-jardin-bicolor-3-plazas-bicolor-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín bicolor con sofá de 3 plazas, dos sillones y mesa de centro, aluminio blanco con lamas antracita y cojines crudo",
        "02_ambiente_exterior_ibiza.jpg": "Set de jardín bicolor en el patio encalado de una casa payesa de Ibiza, con sabina y suelo de grava clara",
        "03_ambiente_interior_payes.jpg": "Sofá de 3 plazas y sillones de exterior en un salón ibicenco encalado con techo de troncos de sabina",
        "04_asmr_lamas.jpg": "Detalle del lateral del sillón: lamas de aluminio antracita encajadas en el marco blanco junto al cojín crudo",
        "05_asmr_granada.jpg": "Granada partida y vaso de agua con hielo sobre el tablero blanco de la mesa de centro",
    }),
    "yina2p": ("set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín moderno de cuerda trenzada gris con sofá de 2 plazas, dos sillones y mesa redonda, cojines azul claro",
        "02_ambiente_exterior_cadiz.jpg": "Set de jardín de cuerda con cojines azules en la azotea de una casa de Cádiz, con la catedral y el Atlántico al fondo",
        "03_ambiente_interior_gaditano.jpg": "Sofá y sillones de cuerda en un salón gaditano de baldosa hidráulica, con el balcón abierto al mar",
        "04_asmr_cuerda.jpg": "Detalle del trenzado de cuerda gris del respaldo curvo del sillón junto al cojín azul claro",
        "05_asmr_tinto_verano.jpg": "Vaso de tinto de verano con hielo y limón junto a un plato de almendras sobre la mesa redonda de cuerda",
    }),
    "damasco2p": ("set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín elegante de aluminio gris tórtola con sofá de 2 plazas, dos sillones de cuerda beige y mesa de centro, cojines crudo",
        "02_ambiente_exterior_cortijo.jpg": "Set de jardín tórtola en la terraza de un cortijo contemporáneo de la campiña sevillana, junto a un olivo",
        "03_ambiente_interior_galeria.jpg": "Sofá y sillones de exterior en la galería de arcos encalados de un cortijo andaluz, abierta al olivar",
        "04_asmr_cuerda.jpg": "Detalle del trenzado de cuerda beige del lateral del sillón sobre el perfil de aluminio gris tórtola",
        "05_asmr_queso.jpg": "Tabla de queso curado, pan de pueblo y un cuenco de aceite de oliva sobre la mesa de centro de lamas",
    }),
    "bellagio2p": ("set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-3", {
        "01_packshot.jpg": "Set de jardín elegante de aluminio blanco de líneas rectas con sofá de 2 plazas, dos sillones y mesa de centro, cojines gris claro",
        "02_ambiente_exterior_cabodegata.jpg": "Set de jardín blanco en la terraza de una casa cúbica encalada de Cabo de Gata, con agave, chumbera y el mar al fondo",
        "03_ambiente_interior_hornacinas.jpg": "Sofá y sillones de exterior en una sala encalada almeriense con hornacinas de piedra y suelo de microcemento",
        "04_asmr_perfil.jpg": "Detalle del perfil de aluminio blanco de sección cuadrada del sillón junto a la costura del cojín gris claro",
        "05_asmr_tomate_raf.jpg": "Tomates raf partidos, aceitera de cristal y pan de pueblo sobre la mesa de centro blanca",
    }),
    "balinesa": ("balliu-cama-balinesa-exterior-aluminio-estilo-minimalista-198-cm-dcaf71d8", {
        "01_packshot.jpg": "Cama balinesa de exterior de aluminio blanco con cubierta integrada y dos paneles laterales de tejido náutico, 198 cm",
        "02_ambiente_exterior_mallorca.jpg": "Cama balinesa blanca junto a la piscina de una casa de piedra mallorquina, entre pinos y muro de piedra seca",
        "03_ambiente_interior_porche.jpg": "Cama balinesa bajo el porche abovedado de una villa mallorquina, abierto a la piscina",
        "04_asmr_tejido.jpg": "Detalle del poste de aluminio blanco y la trama del tejido náutico del panel lateral",
        "05_medidas.png": "Medidas de la cama balinesa de exterior: 198 cm de ancho y 200 cm de alto",
    }),
}

# TANDA 2026-07-26 (ya publicada, se conserva como referencia)
GALERIAS_PUBLICADAS = {
    "brandon": ("set-jardin-aluminio-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín contemporáneo de aluminio antracita con sofá de 3 plazas, dos sillones y mesa, tapizado gris",
        "02_ambiente_exterior_cantabria.jpg": "Set de jardín de aluminio antracita en una terraza de granito de la costa cántabra, con hortensias",
        "03_ambiente_interior_galeria.jpg": "Sofá de 3 plazas y sillones de exterior en una galería acristalada del norte, con vistas al prado y al mar",
        "04_asmr_material.jpg": "Detalle del brazo del sofá: tejido gris jaspeado y perfil de aluminio antracita mate con gotas de lluvia",
        "05_asmr_cafe.jpg": "Taza de café humeante sobre la mesa auxiliar de tablero cerámico del set de jardín",
    }),
    "yina": ("set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Set de jardín contemporáneo de cuerda trenzada greige con sofá de 3 plazas, dos sillones y mesa redonda, cojines crudo",
        "02_ambiente_exterior_porxada.jpg": "Set de jardín de cuerda y cojines crudo en una porxada menorquina de piedra marés con olivos",
        "03_ambiente_interior_payesa.jpg": "Sofá y sillones de cuerda en el salón de una casa payesa encalada, con las puertas abiertas al olivar",
        "04_asmr_cuerda.jpg": "Detalle del trenzado de cuerda del respaldo y el cojín crudo del sofá de exterior",
        "05_asmr_vino_higos.jpg": "Copa de vino blanco e higos partidos sobre la mesa de cuerda con tablero cerámico",
    }),
    "albania": ("set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-3", {
        "01_packshot.jpg": "Set de jardín de aluminio gris con sofá de 3 plazas, dos sillones y mesa baja, cojines verde salvia",
        "02_ambiente_exterior_pergola.jpg": "Set de jardín con cojines verde salvia bajo una pérgola de cañizo en una casa de huerta levantina",
        "03_ambiente_interior_porche.jpg": "Sofá y sillones de exterior en un porche cubierto encalado, con las puertas abiertas al limonero",
        "04_asmr_material.jpg": "Detalle del travesaño de aluminio del sillón y la trama real del cojín verde salvia",
        "05_asmr_te_helado.jpg": "Vaso de té helado con menta sobre la mesa de lamas de aluminio, bajo la sombra del cañizo",
    }),
    "rinconera": ("set-rinconera-exterior-hpl-sofisticado-sofa-de-esquina-mesa-de-centro", {
        "01_packshot.jpg": "Conjunto rinconera de exterior de aluminio blanco con tableros HPL y cojines arena, sofá de esquina y mesa de centro",
        "02_ambiente_exterior_costablanca.jpg": "Rinconera de exterior blanca sobre tarima de madera en la terraza de una villa de la Costa Blanca con piscina",
        "03_ambiente_interior_porche.jpg": "Sofá rinconero de exterior en un porche cubierto de microcemento abierto a la piscina",
        "04_asmr_hpl.jpg": "Detalle del canto del tablero HPL con su línea oscura y el perfil de aluminio blanco mate",
        "05_asmr_limonada_sandia.jpg": "Jarra de limonada con hielo y sandía sobre la mesa de centro HPL de la rinconera",
    }),
    "sofa3p_brandon": ("sofa-terraza-aluminio-3-plazas-estilo-contemporaneo-22090-cm", {
        "01_packshot.jpg": "Sofá de terraza de 3 plazas de aluminio antracita con tapizado gris, 220x90 cm",
        "02_ambiente_exterior_azotea_madrid.jpg": "Sofá de terraza de 3 plazas en una azotea de finca noble de Madrid al atardecer, con olivo y lavanda",
        "03_ambiente_interior_galeria_madrid.jpg": "Sofá de exterior de 3 plazas en la galería acristalada de un piso madrileño, con suelo de terrazo",
        "04_asmr_vermut.jpg": "Vermut con hielo y almendras marcona junto al brazo del sofá, sobre los tejados de Madrid",
        "05_medidas.png": "Medidas del sofá de terraza de 3 plazas: 220 cm de ancho y 90 cm de alto",
    }),
    "pergola": ("pergola-aluminio-para-jardin-300300250-cm", {
        "01_packshot.jpg": "Pérgola de jardín de aluminio blanco con toldo corredero de lona, 300x300x250 cm",
        "02_ambiente_jardin.jpg": "Pérgola de aluminio blanco sobre tarima en un jardín de grava con seto y olivo, proyectando su sombra",
        "03_bajo_la_pergola.jpg": "Vista desde debajo de la pérgola: la lona a contraluz y la sombra que crea sobre la tarima",
        "04_asmr_perfil_carril.jpg": "Detalle del perfil de aluminio blanco de la pérgola con el carril del toldo corredero",
        "05_medidas.png": "Medidas de la pérgola de aluminio: 300 cm de ancho y 250 cm de alto",
    }),
}


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    if "errors" in d:
        raise RuntimeError(d["errors"])
    return d["data"]


Q_PROD = """query($h:String!){ products(first:1, query:$h){ nodes{ id handle title
  media(first:30){ nodes{ id ... on MediaImage { image{url} } } } } } }"""

M_STAGED = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
  stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }"""

M_CREATE = """mutation($pid:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$pid, media:$media){
  media{ ... on MediaImage { id status } } mediaUserErrors{ field message } } }"""

Q_STATUS = """query($id:ID!){ product(id:$id){ mediaCount{count}
  media(first:30){ nodes{ id status ... on MediaImage { image{ url width height } } } } } }"""

M_REORDER = """mutation($id:ID!,$moves:[MoveInput!]!){ productReorderMedia(id:$id, moves:$moves){
  job{ id done } userErrors{ field message } } }"""

M_DELETE = """mutation($pid:ID!,$ids:[ID!]!){ productDeleteMedia(productId:$pid, mediaIds:$ids){
  deletedMediaIds mediaUserErrors{ field message } } }"""


def post_multipart(url, params, filepath):
    boundary = uuid.uuid4().hex
    ctype = mimetypes.guess_type(filepath)[0] or "image/jpeg"
    parts = []
    for p in params:
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode())
    fn = os.path.basename(filepath)
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{fn}\"\r\nContent-Type: {ctype}\r\n\r\n".encode())
    parts.append(open(filepath, "rb").read())
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(parts)
    req = urllib.request.Request(url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.status


def publicar(slug, handle, alts):
    d = gql(Q_PROD, {"h": f"handle:{handle}"})["data"] if False else gql(Q_PROD, {"h": f"handle:{handle}"})
    nodes = d["products"]["nodes"]
    if not nodes:
        print(f"  ✗ producto no encontrado: {handle}")
        return None
    p = nodes[0]
    viejos = [m["id"] for m in p["media"]["nodes"]]
    carpeta = os.path.join(ROOT, "images_generated", slug)
    ficheros = sorted(f for f in os.listdir(carpeta) if f.lower().endswith((".jpg", ".png")))
    print(f"\n== {slug} -> {p['title']}")
    print(f"   producto: {p['id']}  media actuales: {len(viejos)}")
    for f in ficheros:
        print(f"   + {f}  ({os.path.getsize(os.path.join(carpeta,f))//1024} KB)  alt: {alts.get(f,'(SIN ALT)')[:70]}")
    if not APPLY:
        print("   [dry-run] no se sube nada")
        return None

    # 1) staged uploads
    inputs = [{"filename": f, "mimeType": mimetypes.guess_type(f)[0] or "image/jpeg",
               "resource": "IMAGE", "httpMethod": "POST",
               "fileSize": str(os.path.getsize(os.path.join(carpeta, f)))} for f in ficheros]
    targets = gql(M_STAGED, {"input": inputs})["stagedUploadsCreate"]
    if targets["userErrors"]:
        raise RuntimeError(targets["userErrors"])
    media_inputs = []
    for f, t in zip(ficheros, targets["stagedTargets"]):
        st = post_multipart(t["url"], t["parameters"], os.path.join(carpeta, f))
        print(f"   subido {f}: HTTP {st}")
        media_inputs.append({"originalSource": t["resourceUrl"], "mediaContentType": "IMAGE",
                             "alt": alts.get(f, "")})

    # 2) crear media
    res = gql(M_CREATE, {"pid": p["id"], "media": media_inputs})["productCreateMedia"]
    if res["mediaUserErrors"]:
        raise RuntimeError(res["mediaUserErrors"])
    nuevos = [m["id"] for m in res["media"]]
    print(f"   creados {len(nuevos)} media")

    # 3) esperar READY
    for intento in range(40):
        time.sleep(4)
        st = gql(Q_STATUS, {"id": p["id"]})["product"]
        estados = {m["id"]: m["status"] for m in st["media"]["nodes"]}
        pend = [i for i in nuevos if estados.get(i) != "READY"]
        if not pend:
            print("   todas READY")
            break
        print(f"   esperando READY... faltan {len(pend)}")
    else:
        print("   ✗ no todas llegaron a READY -> NO se borra nada")
        return {"handle": handle, "producto": p["id"], "borrados": [], "aviso": "timeout READY"}

    # 4) reordenar: los nuevos primero, en el orden de la receta
    moves = [{"id": mid, "newPosition": str(i)} for i, mid in enumerate(nuevos)]
    r = gql(M_REORDER, {"id": p["id"], "moves": moves})["productReorderMedia"]
    if r["userErrors"]:
        raise RuntimeError(r["userErrors"])
    time.sleep(4)

    # 5) borrar los antiguos
    dl = gql(M_DELETE, {"pid": p["id"], "ids": viejos})["productDeleteMedia"]
    if dl["mediaUserErrors"]:
        raise RuntimeError(dl["mediaUserErrors"])
    print(f"   borrados {len(dl['deletedMediaIds'])} media antiguos")

    fin = gql(Q_STATUS, {"id": p["id"]})["product"]
    print(f"   RESULTADO: mediaCount={fin['mediaCount']['count']}  pos0={fin['media']['nodes'][0]['image']['url'][-40:]}")
    return {"handle": handle, "producto": p["id"], "borrados": viejos, "nuevos": nuevos}


if __name__ == "__main__":
    backup = []
    for slug, (handle, alts) in GALERIAS.items():
        if SOLO and slug != SOLO:
            continue
        try:
            r = publicar(slug, handle, alts)
            if r:
                backup.append(r)
        except Exception as e:
            print(f"   ✗ ERROR en {slug}: {e}")
    if backup:
        path = os.path.join(ROOT, "images_generated", "_backup_media_borrados.json")
        prev = json.load(open(path)) if os.path.exists(path) else []
        json.dump(prev + backup, open(path, "w"), ensure_ascii=False, indent=1)
        print(f"\nbackup de IDs -> {path}")
    if not APPLY:
        print("\n(dry-run: repite con --apply para publicar)")
