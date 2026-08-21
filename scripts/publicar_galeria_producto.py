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
#
# ############################################################################
# RECETA VIGENTE (31-07-2026) — ver .claude/skills/santavila-imagen-producto/SKILL.md
#   01 packshot bone
#   02 ambiente EXTERIOR
#   03 ambiente INTERIOR (mismo habitat, otro momento)
#   04 ASMR de FEATURE verificable   <- costura, union, herraje REAL, nudo, canto
#   05 ASMR de consumible            <- o medidas, si el PASO 0 dio cota verificada
#   La ficha queda SIEMPRE con 5 media.
#
# ⛔ NO COPIES los dict de las tandas de abajo como plantilla: varios llevan tomas
#    que hoy estan PROHIBIDAS y quedan como registro historico, no como ejemplo.
#      "04_asmr_suspension"  -> grilletes INVENTADOS (fallo A8, ya retirado)
#      "05_asmr_textil_hoja" / "04_asmr_lona" / "04_asmr_tejido"
#                            -> macro de TRAMA de tejido: el modelo la fabrica.
#    Ninguna toma cuya superficie dominante sea el TEJIDO, a ninguna escala.
# ############################################################################
#
# TANDA 2026-08 · Brandon 3 pl. (5.249 EUR) — verificada con el skill v4
# NO publicar hasta el "ok" explicito de Sergio (PASO 6) y la puerta de identidad (PASO 7.a).
# TANDA 2026-08-21 A · piezas sueltas ODIN (3 fichas, 2.535 EUR)
# Cotas CONFIRMADAS POR DOBLE FUENTE (CSV maestro Hevea == catalogo PDF pag. 33).
# Acabado: cada pieza en el de SU foto oficial -> ODIN-3 antracita, ODIN-2 y ODIN-1 blancos.
# La mesa de centro sale en las fotos del proveedor y NO se vende: se retiro de la imagen.
# TANDA 2026-08-21 B · piezas sueltas DAMASCO y ACAPULCO (4 fichas, 4.389 EUR)
# Cotas CONFIRMADAS POR DOBLE FUENTE (CSV maestro Hevea == catalogo PDF, pags. 35 y 33).
# ACAPULCO-2 NO entra: su unica foto oficial la ocupa una persona sentada y, al retirarla,
# el modelo reconstruyo el asiento como una pieza continua cuando el real lleva DOS cojines.
# TANDA 2026-08-21 C · piezas sueltas CLOE y HASTON (3 fichas, 3.563 EUR)
# Cotas CONFIRMADAS POR DOBLE FUENTE (CSV maestro Hevea == catalogo PDF, pags. 41 y 32).
# Habitats nuevos: C12 Altea (Cloe, blanco y cuerda gris) y C13 carmen del Albaicin (Haston, salvia).
# TANDA 2026-08-21 D · piezas sueltas DIVA BICOLOR y ALBANIA (4 fichas, 4.854 EUR)
# Cotas del CSV maestro Hevea (estas dos series no figuran en el PDF con sus cotas).
# Acabados: cada SKU con el de SU foto oficial -> Diva-3 blanco, Diva-2 tortola,
# Albania-3 verde salvia sobre gris claro, Albania-1 antracita.
# NO entran: Albania-2 (persona sentada -> el asiento salio de una pieza cuando lleva DOS
# cojines) ni Diva-1 (su unica foto lo muestra de espaldas: no hay cara frontal que usar).
# TANDA 2026-08-21 E · piezas sueltas LEISA, DOUNVIL y MANHATAN (6 fichas, 5.057 EUR)
# Cotas del CSV maestro Hevea. Habitat nuevo: C14 Cuenca (Leisa).
# NO entran: Dounvil-3 (1.175) y Manhatan-2 (715), ambas con persona sentada en su unica foto.
# TANDA 2026-08-21 F · BELLAGIO y CUPRA (3 fichas, 5.699 EUR)
# El set BELLAGIO-8 es la ficha de mayor ticket que quedaba sin galeria (3.449 EUR).
# Composicion verificada en el catalogo (pag. 37): 2xA + C + D = dos sillones, sofa de
# 3 plazas y mesa de centro. Los DOS REPOSAPIES que salen en la foto del proveedor NO
# entran en el lote: se retiraron de la imagen.
# El set no tiene cotas en el CSV -> no lleva imagen de medidas (nunca se deduce de la foto).
# TANDA 2026-08-21 G · mesas de centro, banco y reposapies (4 fichas, 1.855 EUR)
# Cotas confirmadas por doble fuente (CSV maestro Hevea == catalogo PDF).
# Cada pieza va al habitat de SU familia: la mesa bicolor con Diva (Ibiza), la Saipros-120
# con Odin (Segovia) y el reposapies Cloe con Cloe (Altea).
# TANDA 2026-08-21 H · las cuatro mesas de centro que quedaban (4 fichas, 1.556 EUR)
# Todas salian acompanadas en la foto del proveedor (sofa detras, plantas o vajilla encima,
# y en un caso una persona sentada al fondo): se aislo la mesa sin tocar su geometria.
# NO entran: banco Gulliver (424) y silla Janeiro (200) — sus fotos de catalogo son montajes
# con recortes superpuestos, no sirven como referencia.
# TANDA 2026-08-21 I · reposapies y mesa Bellagio (4 fichas, 1.562 EUR)
# Los tres reposapies estaban en fotos COMPARTIDAS con su sillon (el proveedor no los
# fotografia solos): se aislo cada uno sin tocar su geometria y cada uno va al habitat de
# su familia. Cotas confirmadas por doble fuente.
# TANDA 2026-08-21 J · BOLONIA XL, desbloqueada por la regla "siempre catalogo" (3 fichas, 4.708 EUR)
# El CSV decia 215/164/80 y el catalogo 200/141/78. Sergio: manda el catalogo. Las cotas
# dibujadas son las del PDF (pag. 30). OJO: el TITULO de Shopify aun lleva la del CSV -> es SEO.
#
# Ademas, el CSV asigna a BOLONIA XL-3 (sofa de 3 plazas) la foto de un sofa de DOS plazas:
# la misma pieza que XL-2. Para el 3 plazas se uso la foto oficial del SET XL-8, donde si
# aparece el sofa de tres plazas real (3 cojines de respaldo y 3 de asiento).
# TANDA 2026-08-21 K · piezas sueltas y sillas de comedor (4 fichas, 1.845 EUR)
# HASTON-1 (559) NO entra: su unica foto la ocupa una modelo sentada en el sillon.
# TANDA 2026-08-21 L · accesorios Balliu (3 fichas, 496 EUR)
# NINGUNO tiene cotas en el catalogo -> ninguno lleva imagen de medidas. Solo packshot y
# ambiente: la regla es que una cota no se deduce nunca de la foto.
# MESA MUNDRA (585) a cuarentena: su foto oficial la rodean cuatro sillas y NO se puede
# contar cuantas patas tiene. No se publica un mueble cuya estructura no se puede verificar.
# TANDA 2026-08-21 M · mesa 90 y las dos fundas que quedaban (3 fichas, 646 EUR)
# La funda de parasol acrilico (37) NO entra: el catalogo le asigna la foto de una funda de
# TUMBONA. Foto equivocada, no hay producto que anclar.
GALERIAS_FUNDAS = {
    "mesa90_blanca": ("mesa-de-centro-exterior-90-cm-altura-40-cm-2", {
        "01_packshot.jpg": "Mesa de centro de exterior de aluminio blanco con tablero de lamas, 90x50x40 cm, sobre fondo neutro",
        "02_ambiente_rioja.jpg": "Mesa de centro blanca sola en una terraza de piedra arenisca sobre los vinedos de La Rioja, con la Sierra de Cantabria al fondo",
        "05_medidas.jpg": "Medidas de la mesa de centro: 90 cm de ancho y 40 de alto. Se vende solo la mesa",
    }),
    "funda_sofa": ("balliu-funda-protectora-exterior-6f6d4953", {
        "01_packshot.jpg": "Funda protectora de exterior gris puesta sobre un sillon, con su faldon ajustado y la lengueta de sujecion, sobre fondo neutro",
        "02_ambiente_galicia.jpg": "Sillon cubierto con su funda protectora gris en una terraza de granito gallega en una manana de lluvia, con el tojo en flor y las gotas perlando la tela",
    }),
    "funda_silla": ("balliu-funda-protectora-exterior-340b2844", {
        "01_packshot.jpg": "Funda protectora de exterior gris oscuro puesta sobre una pila de sillas, con sus costuras y su caida, sobre fondo neutro",
        "02_ambiente_cortijo.jpg": "Sillas apiladas y cubiertas con su funda protectora bajo los arcos encalados del porche de un cortijo sevillano al final de la temporada, con el olivo y el rastrojo dorado al fondo",
    }),
}

GALERIAS_ACCESORIOS = {
    "funda_tumbona": ("balliu-funda-protectora-exterior-686cc405", {
        "01_packshot.jpg": "Funda protectora de exterior gris puesta sobre una tumbona, con sus costuras y el faldon ajustado, sobre fondo neutro",
        "02_ambiente_cantabrico.jpg": "Tumbona cubierta con su funda protectora gris en una terraza de granito del Cantabrico en una manana de otono, con las hortensias pasadas y el mar gris al fondo",
    }),
    "base_parasol": ("balliu-base-de-parasol-3ee8b72d", {
        "01_packshot.jpg": "Base de parasol de hormigon gris de forma redonda con tubo de acero y pomo de apriete, sobre fondo neutro",
        "02_ambiente_jardin.jpg": "Base de parasol de hormigon sola sobre la grava de un jardin, junto a un seto de boj y un muro de piedra, con su sombra marcada al sol",
    }),
    "venus_silla": ("balliu-silla-exterior-sin-brazos-estilo-contemporaneo-53-cm-cd07e7d6", {
        "01_packshot.jpg": "Silla de exterior Venus sin brazos, de polipropileno color tortola, con respaldo de aros entrelazados y patas conicas, sobre fondo neutro",
        "02_ambiente_cordoba.jpg": "Silla Venus color tortola sola en un patio cordobes, con geranios en macetas de barro colgadas del muro encalado, reja de forja y suelo de barro",
    }),
}

GALERIAS_SUELTAS_SILLAS = {
    "haston2_sofa": ("sofa-terraza-2-plazas-estilo-moderno-128115-cm", {
        "01_packshot.jpg": "Sofa de terraza Haston de 2 plazas con respaldo alto, estructura de aluminio tortola y cojines beige, 128x62x115 cm, sobre fondo neutro",
        "02_ambiente_carmen.jpg": "Sofa Haston de 2 plazas de respaldo alto en el jardin de un carmen del Albaicin granadino, junto a una alberca de piedra, con cipreses y setos de mirto",
        "05_medidas.jpg": "Medidas del sofa Haston de 2 plazas: 128 cm de ancho y 115 de alto. Se vende solo el sofa; la mesa y los cojines decorativos no se incluyen",
    }),
    "leisa1_sillon": ("sillon-exterior-estilo-versatil-7685-cm", {
        "01_packshot.jpg": "Sillon de exterior Leisa con estructura de aluminio antracita y cojines gris claro, 76x80x85 cm, sobre fondo neutro",
        "02_ambiente_cuenca.jpg": "Sillon Leisa antracita en una terraza de piedra sobre el casco viejo de Cuenca, con las casas colgadas y la hoz del Huecar al fondo",
        "05_medidas.jpg": "Medidas del sillon Leisa: 76 cm de ancho y 85 de alto. Se vende solo el sillon",
    }),
    "corcega_silla": ("silla-exterior-estilo-contemporaneo", {
        "01_packshot.jpg": "Silla de exterior Corcega apilable, de aluminio antracita con asiento y respaldo de textileno oscuro, 55x50x90 cm, sobre fondo neutro",
        "02_ambiente_segovia.jpg": "Silla Corcega antracita sola en una terraza de sillar granitico de Segovia, con lavanda en un pilon de piedra y la sierra de Guadarrama al fondo",
        "05_medidas.jpg": "Medidas de la silla Corcega: 55 cm de ancho y 90 de alto. Se vende solo la silla",
    }),
    "avalon_silla": ("sillon-exterior-estilo-versatil-58100-cm", {
        "01_packshot.jpg": "Silla de exterior Avalon apilable, de aluminio blanco con asiento y respaldo de textileno blanco, 58x57x100 cm, sobre fondo neutro",
        "02_ambiente_valencia.jpg": "Silla Avalon blanca sola en una terraza valenciana de suelo de barro, con persiana de esparto, romero y un naranjo en tinaja",
        "05_medidas.jpg": "Medidas de la silla Avalon: 58 cm de ancho y 100 de alto. Se vende solo la silla",
    }),
}

GALERIAS_BOLONIA_XL = {
    "bolxl3_sofa": ("sofa-terraza-3-plazas-estilo-contemporaneo-215104-cm", {
        "01_packshot.jpg": "Sofa de terraza Bolonia XL de 3 plazas en aluminio azul marino con brazos de marco abierto y base de patin, cojines azul lavanda, 200x84x104 cm, sobre fondo neutro",
        "02_ambiente_cadaques.jpg": "Sofa Bolonia XL de 3 plazas en una terraza de Cadaques, sobre laja de pizarra, con muro encalado, postigos de lamas azules, buganvilla y la bahia con los llauts",
        "05_medidas.jpg": "Medidas del sofa Bolonia XL de 3 plazas segun el catalogo del fabricante: 200 cm de ancho y 104 de alto. Se vende solo el sofa",
    }),
    "bolxl2_sofa": ("sofa-terraza-2-plazas-estilo-contemporaneo-164104-cm", {
        "01_packshot.jpg": "Sofa de terraza Bolonia XL de 2 plazas en aluminio azul marino con brazos de marco abierto y base de patin, cojines azul lavanda, 141x84x104 cm, sobre fondo neutro",
        "02_ambiente_cadaques.jpg": "Sofa Bolonia XL de 2 plazas en una terraza de Cadaques, con olivo en tinaja, postigos de lamas azules, buganvilla y las barcas de la bahia al fondo",
        "04_asmr_brazo.jpg": "Detalle de la esquina soldada del brazo de aluminio azul marino del sofa Bolonia XL, junto al canto del cojin azul lavanda",
        "05_medidas.jpg": "Medidas del sofa Bolonia XL de 2 plazas segun el catalogo del fabricante: 141 cm de ancho y 104 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "bolxl1_sillon": ("sillon-exterior-estilo-elegante-80104-cm", {
        "01_packshot.jpg": "Sillon de exterior Bolonia XL en aluminio azul marino con brazo de marco abierto y base de patin, cojines azul lavanda, 78x84x104 cm, sobre fondo neutro",
        "02_ambiente_cadaques.jpg": "Sillon Bolonia XL en una terraza de Cadaques, sobre laja de pizarra, junto a un olivo en tinaja y con los llauts fondeados en la bahia",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio azul marino del sillon Bolonia XL y del acolchado acanalado del cojin de respaldo",
        "05_medidas.jpg": "Medidas del sillon Bolonia XL segun el catalogo del fabricante: 78 cm de ancho y 104 de alto. Se vende solo el sillon",
    }),
}

GALERIAS_REPOSAPIES = {
    "bellagio4_mesa": ("mesa-de-centro-exterior-125-cm-altura-38-cm", {
        "01_packshot.jpg": "Mesa de centro de exterior Bellagio de aluminio antracita con tablero de lamas y patas curvadas, 125x60x38 cm, sobre fondo neutro",
        "02_ambiente_cabodegata.jpg": "Mesa de centro Bellagio antracita sola en la terraza encalada de una casa de Cabo de Gata, entre agaves y chumberas, con el mar al fondo",
        "05_medidas.jpg": "Medidas de la mesa de centro Bellagio: 125 cm de ancho y 38 de alto. Se vende solo la mesa",
    }),
    "std55bic_repo": ("reposapies-exterior-bicolor-704544-cm", {
        "01_packshot.jpg": "Reposapies de exterior bicolor con estructura de aluminio tortola, lamas oscuras en el lateral y cojin claro, 70x45x44 cm, sobre fondo neutro",
        "02_ambiente_ibiza.jpg": "Reposapies bicolor solo en la terraza de una casa payesa de Ibiza, sobre grava clara, con muros de cal y una sabina",
        "05_medidas.jpg": "Medidas del reposapies bicolor: 70 cm de ancho y 44 de alto. Se vende solo el reposapies",
    }),
    "std55xl_repo": ("reposapies-exterior-855043-cm", {
        "01_packshot.jpg": "Reposapies de exterior Standard XL con estructura de aluminio antracita y cojin gris claro, 85x50x43 cm, sobre fondo neutro",
        "02_ambiente_puerto.jpg": "Reposapies Standard XL antracita solo en una terraza de piedra sobre un puerto pesquero asturiano, con reja de forja y las barcas abajo",
        "05_medidas.jpg": "Medidas del reposapies Standard XL: 85 cm de ancho y 43 de alto. Se vende solo el reposapies",
    }),
    "std5_repo": ("reposapies-exterior-605040-cm", {
        "01_packshot.jpg": "Reposapies de exterior Standard con estructura de aluminio tortola y cojin verde claro, 60x50x40 cm, sobre fondo neutro",
        "02_ambiente_cortijo.jpg": "Reposapies Standard solo bajo los arcos encalados de un cortijo de la campina sevillana, con un olivo viejo y los trigales al fondo",
        "05_medidas.jpg": "Medidas del reposapies Standard: 60 cm de ancho y 40 de alto. Se vende solo el reposapies",
    }),
}

GALERIAS_MESAS_2 = {
    "univ120_mesa": ("mesa-de-centro-exterior-120-cm-altura-40-cm-2", {
        "01_packshot.jpg": "Mesa de centro de exterior Universal de aluminio antracita con tablero de lamas, 120x60x40 cm, sobre fondo neutro",
        "02_ambiente_pirineo.jpg": "Mesa de centro antracita sola en una terraza de pizarra del Pirineo aragones, con muro de piedra seca, lavanda y los picos al fondo",
        "05_medidas.jpg": "Medidas de la mesa de centro Universal: 120 cm de ancho y 40 de alto. Se vende solo la mesa",
    }),
    "hpl120_mesa": ("mesa-de-centro-exterior-hpl-120-cm-altura-40-cm-2", {
        "01_packshot.jpg": "Mesa de centro de exterior de aluminio antracita con tablero HPL efecto cemento, 120x60x40 cm, sobre fondo neutro",
        "02_ambiente_segovia.jpg": "Mesa de centro antracita con tablero de cemento sola en una terraza de sillar granitico de Segovia, con lavanda en un pilon de piedra y la sierra al fondo",
        "05_medidas.jpg": "Medidas de la mesa de centro HPL: 120 cm de ancho y 40 de alto. Se vende solo la mesa",
    }),
    "saipros90_mesa": ("mesa-de-centro-exterior-90-cm-altura-41-cm", {
        "01_packshot.jpg": "Mesa de centro de exterior Saipros de aluminio blanco con tablero de lamas, 90x50x41 cm, sobre fondo neutro",
        "02_ambiente_valencia.jpg": "Mesa de centro Saipros blanca sola en una terraza valenciana de suelo de barro, con persiana de esparto, romero y un naranjo en tinaja",
        "05_medidas.jpg": "Medidas de la mesa de centro Saipros: 90 cm de ancho y 41 de alto. Se vende solo la mesa",
    }),
    "hpl90_mesa": ("mesa-de-centro-exterior-hpl-90-cm-altura-40-cm", {
        "01_packshot.jpg": "Mesa de centro de exterior de aluminio blanco con tablero HPL claro, 90x50x40 cm, sobre fondo neutro",
        "02_ambiente_sevilla.jpg": "Mesa de centro blanca con tablero HPL sola en una azotea sevillana de suelo de ladrillo, con jazmin en tinaja y la Giralda sobre los tejados",
        "05_medidas.jpg": "Medidas de la mesa de centro HPL: 90 cm de ancho y 40 de alto. Se vende solo la mesa",
    }),
}

GALERIAS_MESAS_BANCOS = {
    "mesa135_bicolor": ("mesa-de-centro-exterior-hpl-135-cm-altura-40-cm", {
        "01_packshot.jpg": "Mesa de centro de exterior bicolor con estructura de aluminio blanco y tablero de lamas antracita, 135x60x40 cm, sobre fondo neutro",
        "02_ambiente_ibiza.jpg": "Mesa de centro bicolor sola en la terraza de una casa payesa de Ibiza, sobre grava clara, con muros de cal y una sabina",
        "05_medidas.jpg": "Medidas de la mesa de centro bicolor: 135 cm de ancho y 40 de alto. Se vende solo la mesa",
    }),
    "saipros120_mesa": ("mesa-de-centro-exterior-120-cm-altura-41-cm", {
        "01_packshot.jpg": "Mesa de centro de exterior Saipros de aluminio antracita con tablero de lamas, 120x60x41 cm, sobre fondo neutro",
        "02_ambiente_segovia.jpg": "Mesa de centro Saipros antracita sola en una terraza de sillar granitico de Segovia, con lavanda en un pilon de piedra y la sierra al fondo",
        "05_medidas.jpg": "Medidas de la mesa de centro Saipros: 120 cm de ancho y 41 de alto. Se vende solo la mesa",
    }),
    "sevilla_banco": ("banco-de-exterior-108-cm", {
        "01_packshot.jpg": "Banco de exterior Sevilla de aluminio blanco con respaldo de tres lamas horizontales y asiento gris, 108x42x88 cm, sobre fondo neutro",
        "02_ambiente_jardin.jpg": "Banco Sevilla blanco en un jardin de grava con seto de boj, un olivo en tinaja de barro y un muro de piedra",
        "05_medidas.jpg": "Medidas del banco Sevilla: 108 cm de ancho y 88 de alto. Se vende solo el banco",
    }),
    "cloe5_repo": ("reposapies-exterior-504540-cm", {
        "01_packshot.jpg": "Reposapies de exterior Cloe con estructura de tubo redondo blanco y cojin blanco crudo, 50x45x40 cm, sobre fondo neutro",
        "02_ambiente_altea.jpg": "Reposapies Cloe solo en una terraza encalada de Altea, junto a una calle empedrada que baja al mar, con buganvilla y la cupula de teja azul",
        "05_medidas.jpg": "Medidas del reposapies Cloe: 50 cm de ancho y 40 de alto. Se vende solo el reposapies",
    }),
}

GALERIAS_BELLAGIO_CUPRA = {
    "bellagio8_set": ("set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-3", {
        "01_packshot.jpg": "Conjunto de jardin Bellagio en aluminio antracita con sofa de 3 plazas, dos sillones y mesa de centro, con cojines azul claro, sobre fondo neutro",
        "02_ambiente_cabodegata.jpg": "Conjunto Bellagio antracita en la terraza encalada de una casa cubica de Cabo de Gata, entre agaves y chumberas, con el mar arido al fondo",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio antracita del sofa Bellagio junto al canto del cojin azul claro",
    }),
    "bellagio1_sillon": ("sillon-exterior-estilo-envolvente-7582-cm", {
        "01_packshot.jpg": "Sillon de exterior Bellagio en aluminio antracita con tirante diagonal y base de patin, cojines gris azulado, 75x75x82 cm, sobre fondo neutro",
        "02_ambiente_cabodegata.jpg": "Sillon Bellagio antracita en la terraza encalada de una casa de Cabo de Gata, entre agaves y chumberas, con el mar al fondo",
        "05_medidas.jpg": "Medidas del sillon Bellagio: 75 cm de ancho y 82 de alto. Se vende solo el sillon",
    }),
    "cupra2_sofa": ("sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm", {
        "01_packshot.jpg": "Sofa de terraza Cupra de 2 plazas en aluminio blanco con brazos de marco abierto y base de patin, cojines gris claro, 130x75x90 cm, sobre fondo neutro",
        "02_ambiente_toledo.jpg": "Sofa Cupra de 2 plazas en la terraza de un cigarral toledano, con muro de mamposteria, olivos viejos y el Tajo y la ciudad al fondo",
        "04_asmr_brazo.jpg": "Detalle del brazo de marco abierto de aluminio blanco del sofa Cupra en su union con la base de patin",
        "05_medidas.jpg": "Medidas del sofa Cupra de 2 plazas: 130 cm de ancho y 90 de alto. Se vende solo el sofa",
    }),
}

GALERIAS_LEISA_DOUNVIL_MANHATAN = {
    "leisa3_sofa": ("sofa-terraza-3-plazas-estilo-contemporaneo-19685-cm", {
        "01_packshot.jpg": "Sofa de terraza Leisa de 3 plazas con brazos de aluminio antracita sobre chasis blanco y cojines gris claro, 196x80x85 cm, sobre fondo neutro",
        "02_ambiente_cuenca.jpg": "Sofa Leisa de 3 plazas en una terraza de piedra sobre el casco viejo de Cuenca, con las casas colgadas y la hoz del Huecar al fondo",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio antracita del sofa Leisa en su encuentro con el travesano blanco del chasis",
        "05_medidas.jpg": "Medidas del sofa Leisa de 3 plazas: 196 cm de ancho y 85 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "leisa2_sofa": ("sofa-terraza-2-plazas-estilo-contemporaneo-13785-cm", {
        "01_packshot.jpg": "Sofa de terraza Leisa de 2 plazas con chasis de aluminio blanco y cojines gris marengo, 137x80x85 cm, sobre fondo neutro",
        "02_ambiente_cuenca.jpg": "Sofa Leisa de 2 plazas en una terraza de piedra sobre el casco viejo de Cuenca, con las casas colgadas y la hoz del Huecar al fondo",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio blanco del sofa Leisa junto a la costura del cojin gris marengo",
        "05_medidas.jpg": "Medidas del sofa Leisa de 2 plazas: 137 cm de ancho y 85 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "dounvil2_sofa": ("sofa-terraza-2-plazas-estilo-elegante-15085-cm", {
        "01_packshot.jpg": "Sofa de terraza Dounvil de 2 plazas con chasis de aluminio blanco y cojines arena, 150x80x85 cm, sobre fondo neutro",
        "02_ambiente_rioja.jpg": "Sofa Dounvil de 2 plazas en una terraza de piedra arenisca sobre los vinedos de La Rioja, con la Sierra de Cantabria al fondo",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio blanco del sofa Dounvil en su union con la pata, junto al canto del cojin arena",
        "05_medidas.jpg": "Medidas del sofa Dounvil de 2 plazas: 150 cm de ancho y 85 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "dounvil1_sillon": ("sillon-exterior-estilo-moderno-7085-cm", {
        "01_packshot.jpg": "Sillon de exterior Dounvil con chasis de aluminio antracita y cojines gris claro, 70x80x85 cm, sobre fondo neutro",
        "02_ambiente_costadamorte.jpg": "Sillon Dounvil antracita sobre las rocas de granito de la Costa da Morte, entre tojo en flor y brezo, con el Atlantico rompiendo abajo",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio antracita del sillon Dounvil junto al cojin gris claro",
        "05_medidas.jpg": "Medidas del sillon Dounvil: 70 cm de ancho y 85 de alto. Se vende solo el sillon; el reposapies no se incluye",
    }),
    "manhatan3_sofa": ("sofa-terraza-3-plazas-estilo-moderno-18770-cm", {
        "01_packshot.jpg": "Sofa de terraza Manhatan de 3 plazas en aluminio blanco con brazos planos y base voladiza, cojines gris claro, 187x66x70 cm, sobre fondo neutro",
        "02_ambiente_sevilla.jpg": "Sofa Manhatan de 3 plazas blanco en una azotea sevillana de suelo de ladrillo, con jazmin en tinaja y la Giralda sobre los tejados",
        "04_asmr_brazo.jpg": "Detalle del brazo plano de aluminio blanco del sofa Manhatan y del quiebro de su base voladiza",
        "05_medidas.jpg": "Medidas del sofa Manhatan de 3 plazas: 187 cm de ancho y 70 de alto. Se vende solo el sofa; la mesa y los cojines decorativos no se incluyen",
    }),
    "manhatan1_sillon": ("sillon-exterior-estilo-urbano-6670-cm", {
        "01_packshot.jpg": "Sillon de exterior Manhatan en aluminio antracita con brazo plano y base voladiza, cojines gris claro, 66x66x70 cm, sobre fondo neutro",
        "02_ambiente_pirineo.jpg": "Sillon Manhatan antracita en una terraza de pizarra del Pirineo aragones, con muro de piedra seca, lavanda y los picos al fondo",
        "05_medidas.jpg": "Medidas del sillon Manhatan: 66 cm de ancho y 70 de alto. Se vende solo el sillon",
    }),
}

GALERIAS_DIVA_ALBANIA = {
    "diva3_sofa": ("sofa-terraza-bicolor-3-plazas-estilo-bicolor-20076-cm", {
        "01_packshot.jpg": "Sofa de terraza Diva bicolor de 3 plazas con estructura de aluminio blanco, laterales de lamas antracita y cojines blanco crudo, 200x70x76 cm, sobre fondo neutro",
        "02_ambiente_ibiza.jpg": "Sofa Diva bicolor de 3 plazas en la terraza de una casa payesa de Ibiza, con muros de cal de aristas redondeadas, pergola de sabina y grava clara",
        "04_asmr_lamas.jpg": "Detalle de las lamas horizontales antracita del lateral del sofa Diva, donde se encuentran con el montante de aluminio blanco",
        "05_medidas.jpg": "Medidas del sofa Diva bicolor de 3 plazas: 200 cm de ancho y 76 de alto. Se vende solo el sofa",
    }),
    "diva2_sofa": ("sofa-terraza-bicolor-2-plazas-estilo-bicolor-14076-cm", {
        "01_packshot.jpg": "Sofa de terraza Diva bicolor de 2 plazas con estructura de aluminio tortola, laterales de lamas marron oscuro y cojines crudo con ribete, 140x70x76 cm, sobre fondo neutro",
        "02_ambiente_cordoba.jpg": "Sofa Diva bicolor de 2 plazas en un patio cordobes, con geranios en macetas de barro colgadas del muro, reja de forja y un limonero en tinaja",
        "04_asmr_lamas.jpg": "Detalle de las lamas horizontales marron oscuro del lateral del sofa Diva, donde se encuentran con el montante de aluminio tortola",
        "05_medidas.jpg": "Medidas del sofa Diva bicolor de 2 plazas: 140 cm de ancho y 76 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "albania3_sofa": ("sofa-terraza-3-plazas-estilo-sofisticado-212100-cm", {
        "01_packshot.jpg": "Sofa de terraza Albania de 3 plazas con estructura de aluminio gris claro y patas en A, tapiceria verde salvia, 212x70x100 cm, sobre fondo neutro",
        "02_ambiente_huerta.jpg": "Sofa Albania de 3 plazas bajo una pergola de canizo en la huerta de Murcia, con suelo de gres arena, muro encalado, un limonero en tinaja y el limonar al fondo",
        "04_asmr_pata.jpg": "Detalle de la pata en A de aluminio gris claro del sofa Albania, en el encuentro de la diagonal con el brazo",
        "05_medidas.jpg": "Medidas del sofa Albania de 3 plazas: 212 cm de ancho y 100 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "albania1_sillon": ("sillon-exterior-estilo-versatil-76100-cm", {
        "01_packshot.jpg": "Sillon de exterior Albania con estructura de aluminio antracita y patas en A, cojines gris claro, 76x70x100 cm, sobre fondo neutro",
        "02_ambiente_puerto.jpg": "Sillon Albania antracita en una terraza de piedra sobre un puerto pesquero asturiano, con reja de forja, las casas de colores y las barcas abajo",
        "04_asmr_pata.jpg": "Detalle de la pata en A de aluminio antracita del sillon Albania, en el encuentro de la diagonal con el brazo",
        "05_medidas.jpg": "Medidas del sillon Albania: 76 cm de ancho y 100 de alto. Se vende solo el sillon; el reposapies no se incluye",
    }),
}

GALERIAS_CLOE_HASTON = {
    "cloe2_sofa": ("sofa-terraza-2-plazas-estilo-contemporaneo-16269-cm", {
        "01_packshot.jpg": "Sofa de terraza Cloe de 2 plazas con estructura de tubo redondo blanco, laterales de cuerda gris trenzada y cojines blanco crudo, 162x64x69 cm, sobre fondo neutro",
        "02_ambiente_altea.jpg": "Sofa Cloe de 2 plazas en una terraza encalada de Altea, con la cupula de teja azul, buganvilla y el Mediterraneo al fondo",
        "04_asmr_cuerda.jpg": "Detalle de la cuerda gris enrollada en vertical sobre el tubo blanco del lateral del sofa Cloe",
        "05_medidas.jpg": "Medidas del sofa Cloe de 2 plazas: 162 cm de ancho y 69 de alto. Se vende solo el sofa",
    }),
    "cloe1_sillon": ("sillon-exterior-estilo-estilizado-7069-cm", {
        "01_packshot.jpg": "Sillon de exterior Cloe con estructura de tubo redondo blanco, laterales de cuerda gris trenzada y cojines blanco crudo, 70x64x69 cm, sobre fondo neutro",
        "02_ambiente_altea.jpg": "Sillon Cloe en una terraza encalada de Altea, junto a una calle empedrada que baja al mar, con buganvilla y la cupula de teja azul",
        "04_asmr_cuerda.jpg": "Detalle del encuentro entre el tubo blanco del sillon Cloe, el panel de cuerda gris y el canto del cojin crudo",
        "05_medidas.jpg": "Medidas del sillon Cloe: 70 cm de ancho y 69 de alto. Se vende solo el sillon",
    }),
    "haston3_sofa": ("sofa-terraza-3-plazas-estilo-contemporaneo-188115-cm", {
        "01_packshot.jpg": "Sofa de terraza Haston de 3 plazas con respaldo alto, estructura de aluminio blanco y cojines verde salvia claro, 188x62x115 cm, sobre fondo neutro",
        "02_ambiente_carmen.jpg": "Sofa Haston de respaldo alto en el jardin de un carmen del Albaicin granadino, junto a una alberca de piedra, con cipreses y setos de mirto",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio blanco del sofa Haston en su union con la pata inclinada, junto al cojin verde salvia",
        "05_medidas.jpg": "Medidas del sofa Haston de 3 plazas: 188 cm de ancho y 115 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
}

GALERIAS_DAMASCO_ACAPULCO = {
    "damasco3_sofa": ("sofa-terraza-3-plazas-estilo-sofisticado-19475-cm", {
        "01_packshot.jpg": "Sofa de terraza Damasco de 3 plazas con estructura de aluminio antracita, brazos forrados de cuerda beige y cojines gris claro, 194x79x75 cm, sobre fondo neutro",
        "02_ambiente_cortijo.jpg": "Sofa Damasco de 3 plazas en la terraza de caliza de un cortijo de la campina sevillana, bajo arcos encalados, con un olivo viejo y los trigales al fondo",
        "04_asmr_cuerda.jpg": "Detalle de la cuerda beige enrollada en el brazo del sofa Damasco, donde termina contra el montante de aluminio antracita",
        "05_medidas.jpg": "Medidas del sofa Damasco de 3 plazas: 194 cm de ancho y 75 de alto. Se vende solo el sofa",
    }),
    "damasco2_sofa": ("sofa-terraza-2-plazas-estilo-envolvente-13575-cm", {
        "01_packshot.jpg": "Sofa de terraza Damasco de 2 plazas con estructura de aluminio antracita, brazos forrados de cuerda beige y cojines gris claro, 135x79x75 cm, sobre fondo neutro",
        "02_ambiente_cortijo.jpg": "Sofa Damasco de 2 plazas en la terraza de caliza de un cortijo de la campina sevillana, con un olivo en tinaja de barro y los campos dorados al fondo",
        "04_asmr_cuerda.jpg": "Detalle del cordaje vertical del lateral del sofa Damasco, tensado sobre el marco de aluminio antracita",
        "05_medidas.jpg": "Medidas del sofa Damasco de 2 plazas: 135 cm de ancho y 75 de alto. Se vende solo el sofa",
    }),
    "acapulco3_sofa": ("sofa-terraza-3-plazas-estilo-moderno-18570-cm", {
        "01_packshot.jpg": "Sofa de terraza Acapulco de 3 plazas en aluminio blanco con brazos de marco abierto y cojines gris claro, 185x66x70 cm, sobre fondo neutro",
        "02_ambiente_valencia.jpg": "Sofa Acapulco de 3 plazas blanco en una terraza valenciana de suelo de barro, con persiana de esparto, un naranjo en tinaja y romero",
        "04_asmr_brazo.jpg": "Detalle del brazo de marco abierto de aluminio blanco del sofa Acapulco, en la union del travesano con el montante",
        "05_medidas.jpg": "Medidas del sofa Acapulco de 3 plazas: 185 cm de ancho y 70 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "acapulco1_sillon": ("sillon-exterior-estilo-versatil-6470-cm", {
        "01_packshot.jpg": "Sillon de exterior Acapulco en aluminio antracita con brazos de marco abierto y cojines gris claro, 64x66x70 cm, sobre fondo neutro",
        "02_ambiente_salamanca.jpg": "Sillon Acapulco antracita en una azotea de Salamanca, sobre suelo de piedra de Villamayor y con las torres de la catedral al fondo",
        "04_asmr_brazo.jpg": "Detalle del brazo de marco abierto de aluminio antracita del sillon Acapulco junto al canto del cojin gris",
        "05_medidas.jpg": "Medidas del sillon Acapulco: 64 cm de ancho y 70 de alto. Se vende solo el sillon; el reposapies no se incluye",
    }),
}

GALERIAS_ODIN_PIEZAS = {
    "odin3_sofa": ("sofa-terraza-3-plazas-estilo-sofisticado-17578-cm", {
        "01_packshot.jpg": "Sofa de terraza Odin de 3 plazas en aluminio antracita con brazos de marco abierto y cojines gris claro, 175x66x78 cm, sobre fondo neutro",
        "02_ambiente_segovia.jpg": "Sofa Odin de 3 plazas en una terraza de sillar granitico de Segovia, con lavanda en un pilon de piedra, el pinar y la sierra de Guadarrama al fondo",
        "04_asmr_brazo.jpg": "Detalle del brazo plano de aluminio antracita del sofa Odin y su cordon de soldadura, junto a la trama del cojin gris",
        "05_medidas.jpg": "Medidas del sofa Odin de 3 plazas: 175 cm de ancho y 78 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "odin2_sofa": ("sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm", {
        "01_packshot.jpg": "Sofa de terraza Odin de 2 plazas en aluminio blanco con brazos de marco abierto y cojines gris claro, 120x66x78 cm, sobre fondo neutro",
        "02_ambiente_lanzarote.jpg": "Sofa Odin de 2 plazas blanco en una terraza de Lanzarote, con suelo de picon negro, muro encalado y una higuera en su zoco de piedra volcanica",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio blanco del sofa Odin y del vivo cosido del cojin gris claro",
        "05_medidas.jpg": "Medidas del sofa Odin de 2 plazas: 120 cm de ancho y 78 de alto. Se vende solo el sofa; la mesa de centro no se incluye",
    }),
    "odin1_sillon": ("sillon-exterior-estilo-elegante-6578-cm", {
        "01_packshot.jpg": "Sillon de exterior Odin en aluminio blanco con brazos de marco abierto y cojines gris claro, 65x66x78 cm, sobre fondo neutro",
        "02_ambiente_lanzarote.jpg": "Sillon Odin blanco en una terraza de Lanzarote, con suelo de picon negro, muro encalado y una higuera en su zoco de piedra volcanica",
        "04_asmr_brazo.jpg": "Detalle de la esquina redondeada del brazo de aluminio blanco del sillon Odin y del canto del cojin gris",
        "05_medidas.jpg": "Medidas del sillon Odin: 65 cm de ancho y 78 de alto. Se vende solo el sillon; la mesa de centro no se incluye",
    }),
}

GALERIAS_ALBANIA8 = {
    "albania8": ("set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-4", {
        "01_packshot.jpg": "Conjunto de jardin Albania de 3 plazas en aluminio gris claro con patas en A y tapiceria verde salvia: sofa, dos sillones y mesa de centro, sobre fondo neutro",
        "03_ambiente_interior_porche.jpg": "Sofa y sillones Albania verde salvia en un porche encalado con vigas de madera, alfombra de fibra y un olivo, abierto al campo",
        "04_asmr_material.jpg": "Detalle del perfil de aluminio gris claro del sillon Albania y del canto del cojin verde salvia",
        "05_medidas.jpg": "Medidas del conjunto Albania de 3 plazas: sofa 212x70x100 cm y sillon 76x70x100 cm. Incluye sofa, dos sillones y mesa de centro",
    }),
}

GALERIAS_YINA_PIEZAS = {
    "yina_sillon": ("sillon-exterior-estilo-versatil-7783-cm", {
        "01_packshot.jpg": "Sillon de exterior Yina con respaldo y brazos de cuerda trenzada gris sobre aluminio antracita y cojines crudo, 77x72x83 cm, sobre fondo neutro",
        "02_ambiente_porxada.jpg": "Sillon Yina de cuerda gris bajo una porxada de piedra de mares menorquina, junto a un olivo viejo y con el mar al fondo, con una manta de lino sobre el brazo",
        "03_medidas.jpg": "Medidas del sillon Yina: 77 cm de ancho por 72 de fondo y 83 de alto. Se vende solo el sillon",
    }),
    "yina_sofa2p": ("sofa-terraza-2-plazas-estilo-estilizado-14383-cm", {
        "01_packshot.jpg": "Sofa de terraza Yina de 2 plazas con respaldo de cuerda trenzada gris sobre aluminio antracita y cojines azul grisaceo, 143x72x83 cm, sobre fondo neutro",
        "02_ambiente_porxada.jpg": "Sofa Yina de 2 plazas con cojines azul grisaceo bajo una porxada de piedra menorquina, junto a un olivo y con el mar al fondo",
        "03_medidas.jpg": "Medidas del sofa Yina de 2 plazas: 143 cm de ancho por 72 de fondo y 83 de alto. Se vende solo el sofa",
    }),
    "yina_sofa3p": ("sofa-terraza-3-plazas-estilo-contemporaneo-18583-cm", {
        "01_packshot.jpg": "Sofa de terraza Yina de 3 plazas con respaldo de cuerda trenzada gris sobre aluminio antracita y cojines crudo, 185x72x83 cm, sobre fondo neutro",
        "02_ambiente_porxada.jpg": "Sofa Yina de 3 plazas bajo una porxada de piedra de mares menorquina, junto a un olivo viejo y con el mar al fondo, con una manta de lino sobre el asiento",
        "03_medidas.jpg": "Medidas del sofa Yina de 3 plazas: 185 cm de ancho por 72 de fondo y 83 de alto. Se vende solo el sofa",
    }),
    "yina_mesa": ("mesa-de-centro-exterior-hpl-70-cm-altura-45-cm", {
        "01_packshot.jpg": "Mesa de centro Yina redonda de 70 cm con faldon de cuerda trenzada gris y tablero HPL gris oscuro, sobre fondo neutro",
        "02_ambiente_porxada.jpg": "Mesa de centro Yina de cuerda trenzada sobre el suelo de piedra de una porxada menorquina, con el olivo y el mar detras",
        "03_medidas.jpg": "Medidas de la mesa de centro Yina: 70 cm de diametro por 45 cm de alto. Se vende sola la mesa",
    }),
    "yina_repo": ("reposapies-exterior-734640-cm", {
        "01_packshot.jpg": "Reposapies de exterior Yina con panel lateral de cuerda trenzada gris sobre aluminio antracita y cojin crudo, 73x46x40 cm, sobre fondo neutro",
        "02_ambiente_porxada.jpg": "Reposapies Yina de cuerda gris sobre el suelo de piedra de una porxada menorquina, con una manta de lino y el mar al fondo",
        "03_medidas.jpg": "Medidas del reposapies Yina: 73 cm de ancho por 46 de fondo y 40 de alto. Se vende solo el reposapies",
    }),
}

GALERIAS_RESCATE_3 = {
    "sidney": ("balancin-jardin-exterior-148194-cm", {
        "01_packshot.jpg": "Balancin de jardin Sidney de estructura blanca en A con toldo y colchon azul pizarra y cojin blanco, 148x194 cm, sobre fondo neutro",
        "02_ambiente_exterior_alpujarra.jpg": "Balancin blanco en una terraza de piedra de la Alpujarra granadina, con muro de mamposteria, suelo de barro y las terrazas de la sierra al fondo",
        "03_ambiente_interior_porche_encalado.jpg": "Balancin blanco bajo un porche encalado de vigas de madera y suelo de laja, abierto a la sierra",
        "04_medidas.jpg": "Medidas del balancin Sidney: 148 cm de ancho por 194 de fondo y 207 de alto, con toldo y colchon",
    }),
}

GALERIAS_RESCATE_2 = {
    "diva2p": ("set-jardin-bicolor-2-plazas-bicolor-sofa-2-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Conjunto de jardin Diva bicolor de 2 plazas: sofa, dos sillones y mesa de centro de lamas, estructura antracita y tapiceria crudo, sobre fondo neutro",
        "02_ambiente_exterior_cordoba.jpg": "Conjunto Diva bicolor en un patio cordobes encalado, con macetas de geranios en la pared, celosia de forja y un limonero en tinaja",
        "03_ambiente_interior_zaguan.jpg": "Sofa y sillones Diva bicolor en un zaguan abovedado de suelo de barro, con la reja abierta al patio",
        "04_asmr_lamas.jpg": "Detalle de las lamas de aluminio antracita del respaldo del sillon Diva y del canto del cojin crudo",
    }),
    "acapulco3p": ("set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-5", {
        "01_packshot.jpg": "Conjunto de jardin Acapulco de 3 plazas en aluminio blanco con cojines gris claro y mesa de centro de cristal, sobre fondo neutro",
        "02_ambiente_exterior_valencia.jpg": "Conjunto Acapulco blanco en una terraza valenciana de suelo de barro, con persianas de esparto, romero y un naranjo en tinaja",
        "03_ambiente_interior_porche.jpg": "Sofa y sillones Acapulco blancos bajo un porche encalado con persiana de esparto, abierto al jardin",
        "04_asmr_cristal.jpg": "Detalle del canto del tablero de cristal de la mesa de centro Acapulco sobre la estructura de aluminio blanco",
    }),
    "odin3p": ("set-jardin-3-plazas-elegante-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Conjunto de jardin Odin de 3 plazas en aluminio antracita con cojines gris claro y mesa de centro, sobre fondo neutro",
        "02_ambiente_exterior_segovia.jpg": "Conjunto Odin antracita en una terraza de sillar de granito en Segovia, con lavanda en un pilon y el pinar y la sierra de Guadarrama al fondo",
        "03_ambiente_interior_soportal.jpg": "Sofa y sillones Odin bajo un soportal de arcos de granito con vigas de castano",
        "04_asmr_brazo.jpg": "Detalle del brazo de aluminio antracita del sillon Odin y su union con el cojin gris claro",
        "05_medidas.jpg": "Medidas del conjunto Odin de 3 plazas: sofa 175x66x78 cm, sillon 65x66x78 cm y mesa de centro 120x60x41 cm",
    }),
    "dounvil2p": ("set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-2", {
        "01_packshot.jpg": "Conjunto de jardin Dounvil de 2 plazas en aluminio blanco con aspa en el lateral y cojines color arena, sobre fondo neutro",
        "02_ambiente_exterior_rioja.jpg": "Conjunto Dounvil blanco en una terraza de piedra arenisca sobre los vinedos de La Rioja, con la Sierra de Cantabria al fondo",
        "03_ambiente_interior_calado.jpg": "Sofa y sillones Dounvil en una sala abovedada de arenisca con un arco abierto al vinedo",
        "04_asmr_aspa.jpg": "Detalle del aspa de aluminio blanco del lateral del sillon Dounvil y del canto del cojin color arena",
    }),
    "acapulco2p": ("set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4", {
        "01_packshot.jpg": "Conjunto de jardin Acapulco de 2 plazas en aluminio antracita con cojines gris claro y mesa de centro, sobre fondo neutro",
        "02_ambiente_exterior_azotea_salamanca.jpg": "Conjunto Acapulco antracita en una azotea de Salamanca al atardecer, con parapeto de sillar y las torres de la catedral en piedra dorada al fondo",
        "03_ambiente_interior_soportal_piedra.jpg": "Sofa y sillones Acapulco bajo el soportal de arcos de piedra dorada de un patio salmantino, con macetas de geranios",
        "04_asmr_aluminio_antracita.jpg": "Detalle del perfil de aluminio antracita mate del sofa Acapulco y el canto del cojin gris claro con la luz rasante de la tarde",
    }),
}

GALERIAS_RESCATE_1 = {
    "yina": ("set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Conjunto de jardin Yina de 3 plazas: sofa, dos sillones y mesa de centro redonda con respaldos de cuerda trenzada gris y cojines crudo, sobre fondo neutro",
        "02_ambiente_exterior_porxada.jpg": "Conjunto Yina de cuerda gris con cojines crudo en una porxada de piedra de mares menorquina, entre olivos en tinaja y con el mar al fondo",
        "03_ambiente_interior_payesa.jpg": "Sofa y sillones Yina en una sala payesa encalada con vigas de madera y cortina de lino abierta al olivar",
        "04_asmr_cuerda.jpg": "Detalle de la cuerda trenzada gris del respaldo del sillon Yina y su union con el perfil de aluminio antracita",
        "05_medidas.jpg": "Medidas del conjunto Yina de 3 plazas: sofa 185x72x83 cm y sillon 77x72x83 cm. Incluye sofa, dos sillones y mesa de centro",
    }),
    "yina2p": ("set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Conjunto de jardin Yina de 2 plazas: sofa, dos sillones y mesa de centro redonda con respaldos de cuerda gris y cojines azul celeste, sobre fondo neutro",
        "02_ambiente_exterior_cadiz.jpg": "Conjunto Yina de 2 plazas con cojines azules en una azotea encalada de Cadiz, con geranios y la catedral y el Atlantico al fondo",
        "03_ambiente_interior_gaditano.jpg": "Sofa y sillones Yina de cojines azules en un salon de baldosa hidraulica con el balcon abierto al mar",
        "04_asmr_cuerda.jpg": "Detalle de la cuerda trenzada del respaldo del sillon Yina sobre el perfil de aluminio antracita",
        "05_medidas.jpg": "Medidas del conjunto Yina de 2 plazas: sofa 143x72x83 cm y sillon 77x72x83 cm. Incluye sofa, dos sillones y mesa de centro",
    }),
    "bellagio2p": ("set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-3", {
        "01_packshot.jpg": "Conjunto de jardin Bellagio de 2 plazas en aluminio blanco: sofa, dos sillones y mesa de centro, con cojines gris claro, sobre fondo neutro",
        "02_ambiente_exterior_cabodegata.jpg": "Conjunto Bellagio blanco en una terraza encalada del Cabo de Gata, entre agaves y chumberas, con el mar arido al fondo",
        "03_ambiente_interior_hornacinas.jpg": "Sofa y sillones Bellagio blancos en una sala encalada con hornacinas de piedra y suelo de microcemento",
        "04_asmr_perfil.jpg": "Detalle del perfil de aluminio blanco del sofa Bellagio y el canto del cojin gris claro",
        "05_medidas.jpg": "Medidas del conjunto Bellagio de 2 plazas: sofa 150x75 cm, sillon 75x75 cm y mesa de centro 125x60x38 cm",
    }),
}

GALERIAS_BRANDON_PIEZAS = {
    "brandon2p_sofa": ("sofa-terraza-aluminio-2-plazas-estilo-contemporaneo-16690-cm", {
        "01_packshot.jpg": "Sofa de terraza Brandon de 2 plazas en aluminio antracita con tapiceria gris de jacquard, 166x90x90 cm, sobre fondo neutro",
        "02_ambiente_azotea_madrid.jpg": "Sofa de 2 plazas gris en una azotea de Madrid, con muro de piedra y los tejados de pizarra con buhardillas al fondo, y una manta de lino sobre el brazo",
        "03_ambiente_mirador.jpg": "Sofa de 2 plazas gris en el mirador acristalado de un piso madrileno, con molduras, suelo de terrazo y los tejados de teja y las torres de la ciudad al fondo",
        "04_detalle_aluminio.jpg": "Detalle del codo del tubo de aluminio antracita del sofa Brandon, con su lacado mate granulado y el tejido gris desenfocado detras",
        "05_medidas.jpg": "Medidas del sofa de 2 plazas Brandon: 166 cm de ancho por 90 de fondo y 90 de alto. Se vende solo el sofa",
    }),
    "brandon1_sillon": ("sillon-exterior-aluminio-estilo-envolvente-9890-cm", {
        "01_packshot.jpg": "Sillon de exterior Brandon en aluminio antracita con tapiceria gris de jacquard y brazos envolventes, 98x90x90 cm, sobre fondo neutro",
        "02_ambiente_azotea_madrid.jpg": "Sillon gris en una azotea del Madrid antiguo, con parapeto encalado y los tejados de teja arabe y una torre con chapitel de pizarra al fondo",
        "03_ambiente_mirador.jpg": "Sillon gris en el mirador acristalado de un piso madrileno, con molduras, suelo de terrazo, un geranio en maceta de barro y los tejados de la ciudad al fondo",
        "04_detalle_aluminio.jpg": "Detalle del codo del tubo de aluminio antracita del sillon Brandon, con su lacado mate granulado y el tejido gris desenfocado detras",
        "05_medidas.jpg": "Medidas del sillon Brandon: 98 cm de ancho por 90 de fondo y 90 de alto. Se vende solo el sillon",
    }),
}

GALERIAS_BRANDON_7 = {
    "brandon7_2026-08": ("set-jardin-aluminio-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Conjunto de jardin Brandon 7 de aluminio antracita: sofa de 2 plazas, dos sillones y dos mesas de centro redondas, con tapiceria gris de jacquard",
        "02_ambiente_la_concha.jpg": "Conjunto de jardin antracita en una terraza de piedra sobre la bahia de La Concha en San Sebastian, con la isla de Santa Clara y el monte Urgull al fondo",
        "03_ambiente_interior_donostia.jpg": "Sofa de 2 plazas y las dos mesas redondas en una sala de piso donostiarra con molduras, suelo de espiga de roble y balcon abierto a la bahia",
        "04_detalle_aluminio.jpg": "Detalle del codo del tubo de aluminio antracita del sillon, con su lacado mate granulado y el tejido gris desenfocado detras",
        "05_medidas.jpg": "Medidas de cada pieza: sofa de 2 plazas 166x90x90 cm, sillon 98x90x90 cm y mesas de centro de 80 y 60 cm de diametro por 40 cm de alto",
    }),
}

GALERIAS_BOLONIA_XL8 = {
    "bolonia_xl8_2026-08": ("set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-2", {
        "01_packshot.jpg": "Conjunto de jardin Bolonia XL-8 de aluminio azul marino: sofa de 3 plazas, dos sillones y mesa de centro de listones, con cojines azul lavanda",
        "02_ambiente_exterior_cadaques.jpg": "Conjunto de jardin azul marino en una terraza de laja de pizarra en Cadaques, entre cal blanca, postigos azules y buganvilla, con las barcas fondeadas en la bahia",
        "03_ambiente_interior_casa_cadaques.jpg": "Sofa de 3 plazas y mesa de centro azul marino en una sala encalada de casa de pescadores, con vigas de madera, suelo de barro cocido y la ventana abierta al mar",
        "04_detalle_brazo_patin.jpg": "Detalle de la esquina donde el brazo de aluminio azul marino mate se une con la pata delantera inclinada del sillon, junto al canto del cojin azul lavanda",
        "05_medidas.jpg": "Medidas de cada pieza del conjunto: sofa de 3 plazas 200x84x104 cm, sillon 78x84x104 cm y mesa de centro 125x65x42 cm",
    }),
}

GALERIAS_BRANDON_3P = {
    "brandon3p_2026-08": ("set-jardin-aluminio-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa", {
        "01_packshot.jpg": "Conjunto de jardin de 3 plazas de aluminio antracita: sofa de 3 plazas, dos sillones y dos mesas nido, con tapiceria gris de jacquard tono sobre tono",
        "02_ambiente_exterior_casona.jpg": "Conjunto de jardin gris en la terraza de losa de piedra de una casona de mamposteria del norte de Espana, entre hortensias azules en flor",
        "03_ambiente_interior_galeria.jpg": "Sofa de 3 plazas y sillon de exterior con las dos mesas nido en la galeria acristalada de una casona de piedra, con las hortensias al otro lado del cristal",
        "04_asmr_mesas_canto.jpg": "Detalle del canto fino de los tableros de cemento gris de las dos mesas nido y de sus patas cilindricas de aluminio antracita",
        "05_ambiente_mesas_terraza.jpg": "Las dos mesas nido delante del sofa de 3 plazas en la terraza de losa de piedra, con las hortensias azules de la casona detras",
    }),
}

# TANDA 2026-07-29 D (historica)
GALERIAS = {
    "acapulco2p": ("set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4", {
        "01_packshot.jpg": "Conjunto de jardín de 2 plazas de aluminio antracita: sofá de 2 plazas, dos sillones y mesa de centro, con cojines gris claro",
        "02_ambiente_exterior_azotea_salamanca.jpg": "Conjunto de jardín antracita en una azotea de Salamanca al atardecer, con las torres de la catedral en piedra dorada al fondo",
        "03_ambiente_interior_soportal_piedra.jpg": "Conjunto de jardín antracita bajo el soportal de arcos de piedra dorada de un patio salmantino, con macetas de geranios",
        "04_asmr_aluminio_antracita.jpg": "Detalle del perfil de aluminio antracita mate del sofá y el canto del cojín gris claro, con la luz rasante del atardecer",
        "05_asmr_sandia.jpg": "Media sandía cortada y un vaso de agua sobre la mesa de centro del conjunto, con la sombra larga de la tarde",
    }),
    "sidney": ("balancin-jardin-exterior-148194-cm", {
        "01_packshot.jpg": "Balancín de jardín de estructura blanca en A con toldo y colchón azul pizarra y cojín blanco, 148x194 cm",
        "02_ambiente_exterior_alpujarra.jpg": "Balancín blanco en una terraza de piedra de la Alpujarra granadina, bajo una morera y con Sierra Nevada al fondo",
        "03_ambiente_interior_porche_encalado.jpg": "Balancín blanco bajo el porche encalado de una casa alpujarreña, con vigas de madera y suelo de laja",
        "04_asmr_suspension.jpg": "Detalle del herraje de suspensión del balancín: los grilletes cromados colgando del travesaño de aluminio blanco",
        "05_asmr_textil_hoja.jpg": "Detalle de la trama del tejido azul pizarra del asiento y el cojín blanco, con una hoja seca de morera caída encima",
    }),
}

# TANDA 2026-07-29 C (ya publicada)
GALERIAS_TANDA_29C = {
    "sofa22069": ("sofa-terraza-3-plazas-estilo-elegante-22069-cm", {
        "01_packshot.jpg": "Sofá de terraza de 3 plazas de aluminio blanco con laterales de cuerda gris y cojines crudo, 220 cm",
        "02_ambiente_exterior_malaga.jpg": "Sofá de terraza blanco en la terraza encalada de una casa malagueña, con buganvilla sobre el muro y el Mediterráneo al fondo",
        "03_ambiente_interior_ventana.jpg": "Sofá de exterior en una sala encalada con la ventana de madera abierta al mar",
        "04_asmr_cuerda.jpg": "Detalle de la cuerda gris enrollada en el tubo de aluminio blanco del lateral del sofá",
        "05_vista_frontal.jpg": "Vista frontal del sofá de terraza de 3 plazas: 220 cm de ancho, laterales de cuerda y cojines crudo",
    }),
    "parasol_roma": ("balliu-parasol-para-terraza-aluminio-300-cm-6c1e1224", {
        "01_packshot.jpg": "Parasol lateral de exterior de aluminio blanco con lona cuadrada antracita y base de placas de piedra, 300x300 cm",
        "02_ambiente_terraza.jpg": "Parasol lateral antracita dando sombra a una mesa en una terraza de piedra entre pinos, con el Mediterráneo al fondo",
        "03_bajo_el_parasol.jpg": "Vista desde debajo del parasol: las varillas blancas radiando bajo la lona antracita y la terraza soleada más allá",
        "04_asmr_lona.jpg": "Detalle de la varilla de aluminio blanco y la lona antracita tensada, con el sol atravesando la trama del tejido",
        "05_asmr_manivela.jpg": "Detalle de la manivela de apertura y el herraje del mástil de aluminio blanco, con la sombra del parasol cruzando el suelo",
    }),
}

# TANDA 2026-07-29 B (ya publicada)
GALERIAS_TANDA_29B = {
    "balinesa160": ("balliu-cama-balinesa-exterior-aluminio-estilo-sofisticado-160-cm-2bd3a7a4", {
        "01_packshot.jpg": "Cama balinesa de exterior de aluminio blanco, tumbona doble baja con dos respaldos reclinables independientes, 160 cm",
        "02_ambiente_exterior_dehesa.jpg": "Cama balinesa blanca junto a la piscina de una finca de la dehesa extremeña, entre encinas y hierba dorada",
        "03_ambiente_interior_porche.jpg": "Cama balinesa bajo el porche encalado de una casa de campo extremeña, con vigas de castaño y vistas a la dehesa",
        "04_asmr_toalla.jpg": "Detalle de la esquina del colchón y el perfil de aluminio blanco, con una toalla de lino enrollada y la sombra moteada de la encina",
        "05_perfil.jpg": "Vista de perfil de la cama balinesa con los respaldos planos: altura del colchón y base de aluminio blanco",
    }),
    "manhattan2p": ("set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-3", {
        "01_packshot.jpg": "Set de jardín contemporáneo de aluminio antracita con sofá de 2 plazas, dos sillones de base voladiza y mesa de centro de lamas, cojines gris claro",
        "02_ambiente_exterior_pirineo.jpg": "Set de jardín antracita en una terraza de pizarra del Pirineo aragonés, con muro de piedra seca, lavanda y los picos al fondo",
        "03_ambiente_interior_galeria.jpg": "Sofá y sillones de exterior en la galería acristalada de una casa pirenaica de piedra, con el ventanal abierto al pinar y la montaña",
        "04_asmr_perfil.jpg": "Detalle del brazo plano antracita del sillón y su base voladiza de aluminio, con la trama del cojín gris claro",
        "05_asmr_melocoton.jpg": "Melocotón partido y un vaso de agua fría con condensación sobre la mesa de lamas, con la montaña desenfocada al fondo",
    }),
}

# TANDA 2026-07-29 A (ya publicada)
GALERIAS_TANDA_29A = {
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
    # ⛔⛔ ATENCION — ESTE MAPEO ES EL FALLO A0. NO LO REACTIVES SIN COMPROBAR EL HANDLE.
    # La carpeta se llama "albania" pero este handle es el del BELLAGIO 3 pl. (3.449 EUR), que es
    # OTRO MUEBLE. Durante dias esa ficha mostro 5 fotos de un producto que no era el que vende.
    # El nombre de la carpeta NO identifica el producto: antes de publicar, ejecuta
    #   python3 scripts/fuente_verdad_producto.py <handle>
    # y compara su foto oficial con el packshot. Ver AUDITORIA_FIDELIDAD_2026-07-29.md, caso A0.
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
    # SOLO los ficheros del diccionario, y en su orden. Antes se subia TODO lo que
    # hubiera en la carpeta: rechazadas, comparadores de QA y ficheros de trabajo,
    # casi todos sin alt. El dry-run del 19-08 lo caz\u00f3 con 30 ficheros en vez de 5.
    ficheros = list(alts.keys())
    faltan = [f for f in ficheros if not os.path.exists(os.path.join(carpeta, f))]
    if faltan:
        print(f"  \u2717 faltan ficheros declarados en el diccionario: {faltan}")
        return None
    sin_alt = [f for f in ficheros if not alts.get(f)]
    if sin_alt:
        print(f"  \u2717 sin alt: {sin_alt} -- no se publica")
        return None
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


REG = os.path.join(ROOT, "docs", "santavila", "_verificaciones.json")


def anotar_verificacion(entradas):
    """Deja constancia de QUE se publico y con que caracteristicas medibles.

    Nace del 20-08-2026. Sergio: "no puede ser que tengamos que volver atras". Cada vez que
    aparecia un criterio nuevo habia que ir a mirar a mano las fichas ya publicadas, porque no
    quedaba registro. Con este fichero, un criterio nuevo se comprueba sobre el registro (o con
    scripts/auditar_galerias.py contra la tienda) en vez de a ojo, ficha por ficha.
    """
    from PIL import Image
    prev = json.load(open(REG)) if os.path.exists(REG) else {}
    for e in entradas:
        imgs = []
        for f in e["ficheros"]:
            ruta = os.path.join(ROOT, "images_generated", e["slug"], f)
            if not os.path.exists(ruta):
                continue
            w, h = Image.open(ruta).size
            imgs.append({"fichero": f, "px": f"{w}x{h}", "mp": round(w*h/1e6, 1),
                         "alt_len": len(e["alts"].get(f, ""))})
        prev[e["handle"]] = {"fecha": e["fecha"], "carpeta": e["slug"],
                             "n_imagenes": len(imgs), "imagenes": imgs}
    json.dump(prev, open(REG, "w"), ensure_ascii=False, indent=1)
    print(f"\nregistro de verificacion -> {REG}")


if __name__ == "__main__":
    backup = []
    # ACTIVA: la tanda del Brandon 3 pl. (las de abajo son historicas y NO se publican)
    ACTIVA = GALERIAS_FUNDAS
    registro = []
    for slug, (handle, alts) in ACTIVA.items():
        if SOLO and slug != SOLO:
            continue
        try:
            r = publicar(slug, handle, alts)
            if r:
                backup.append(r)
                registro.append({"handle": handle, "slug": slug, "alts": alts,
                                 "ficheros": list(alts.keys()),
                                 "fecha": time.strftime("%Y-%m-%d")})
        except Exception as e:
            print(f"   ✗ ERROR en {slug}: {e}")
    if registro:
        anotar_verificacion(registro)
    if backup:
        path = os.path.join(ROOT, "images_generated", "_backup_media_borrados.json")
        prev = json.load(open(path)) if os.path.exists(path) else []
        json.dump(prev + backup, open(path, "w"), ensure_ascii=False, indent=1)
        print(f"\nbackup de IDs -> {path}")
    if not APPLY:
        print("\n(dry-run: repite con --apply para publicar)")
