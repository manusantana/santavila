#!/usr/bin/env python3
"""
Reescribe descripciones (y meta description SEO) de las 31 fichas finas/vacías.
Seguridad: hace BACKUP de lo actual antes de tocar nada y por defecto va en DRY-RUN.

  python3 scripts/apply_descriptions.py            # dry-run: muestra qué haría
  python3 scripts/apply_descriptions.py --apply     # aplica de verdad (con backup previo)

Texto anclado a datos reales (material/medidas/uso del título y opciones).
Sin códigos de proveedor en cara al cliente (criterio Opción C).
"""
import json, os, sys, datetime, urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv

UL = lambda items: "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def block(opening, bullets, closing=""):
    html = f"<p><strong>{opening}</strong></p>"
    # segunda frase del párrafo va dentro del opening; bullets aparte
    html += UL(bullets)
    if closing:
        html += f"<p>{closing}</p>"
    return html

# handle -> (body_html, meta_description)
D = {}

D["tumbona-carmen-tablillas"] = (
 "<p><strong>Tumbona de exterior en resina de polipropileno con diseño de tablillas, respaldo reclinable en 5 posiciones y ruedas integradas para moverla sin esfuerzo.</strong> Pensada para descansar en el jardín o junto a la piscina, su estructura de tablillas resiste el sol, la lluvia y el cloro sin oxidarse, y favorece la ventilación y el secado rápido. Está fabricada con polipropileno reciclado y es totalmente reciclable.</p>"
 + UL([
   "<strong>Material:</strong> resina de polipropileno reciclado (reciclable), apta para intemperie.",
   "<strong>Respaldo:</strong> reclinable en 5 posiciones.",
   "<strong>Movilidad:</strong> ruedas integradas en el chasis.",
   "<strong>Ancho:</strong> 75 cm.",
   "<strong>Acabados:</strong> blanco, arena, bronce, gris oscuro y madera.",
   "<strong>Uso recomendado:</strong> jardín y piscina.",
   "<strong>Mantenimiento:</strong> limpieza con agua y jabón suave; compatible con colchoneta Dry Feel.",
 ]),
 "Tumbona de exterior en resina con tablillas, respaldo reclinable en 5 posiciones y ruedas. Resiste sol, lluvia y cloro. Para jardín y piscina.")

D["tumbona-lola-tablillas"] = (
 "<p><strong>Tumbona de exterior en resina de polipropileno con tablillas, de líneas tipo playa, con respaldo reclinable en 5 posiciones y ruedas integradas.</strong> Ideal para la piscina y el jardín, su estructura de tablillas resiste los rayos UV, la humedad y el cloro sin oxidarse y se seca con rapidez. Fabricada con polipropileno reciclado y totalmente reciclable.</p>"
 + UL([
   "<strong>Material:</strong> resina de polipropileno reciclado (reciclable), apta para intemperie.",
   "<strong>Respaldo:</strong> reclinable en 5 posiciones.",
   "<strong>Movilidad:</strong> ruedas integradas en el chasis.",
   "<strong>Ancho:</strong> 75 cm.",
   "<strong>Acabados:</strong> blanco, arena, bronce, gris oscuro y madera.",
   "<strong>Uso recomendado:</strong> piscina y jardín.",
   "<strong>Mantenimiento:</strong> limpieza con agua y jabón suave; compatible con colchoneta Dry Feel.",
 ]),
 "Tumbona de exterior en resina con tablillas tipo playa, respaldo reclinable en 5 posiciones y ruedas. Resiste sol, cloro y humedad. Piscina y jardín.")

D["mesa-exterior-aluminio-hpl-120x80-capri-doble"] = (
 "<p><strong>Mesa de exterior con estructura de aluminio reforzado de doble soporte y tablero HPL de 120×80 cm, diseñada para un uso intensivo en jardín, terraza y hostelería.</strong> El doble pie aporta gran estabilidad y deja libre el espacio para las piernas; el tablero HPL aguanta el sol, el agua y los arañazos sin perder color y el aluminio no se oxida. Incluye tornillería de acero inoxidable y tapones regulables para nivelarla en suelos irregulares.</p>"
 + UL([
   "<strong>Material:</strong> estructura de aluminio reforzado con tornillería de acero inoxidable + tablero HPL.",
   "<strong>Medidas del tablero:</strong> 120 × 80 cm.",
   "<strong>Base:</strong> doble soporte, para mayor estabilidad.",
   "<strong>Acabados:</strong> chasis en blanco, tórtola o aluminio; tablero en gris, blanco, Moonwalk, Skyline o Prado.",
   "<strong>Extras:</strong> tapones regulables para suelos irregulares.",
   "<strong>Uso recomendado:</strong> jardín, terraza y hostelería.",
   "<strong>Mantenimiento:</strong> limpieza con paño húmedo; mínimo mantenimiento.",
 ]),
 "Mesa de exterior de aluminio reforzado con pie doble y tablero HPL 120×80 cm. Estable, sin óxido, con tapones regulables. Jardín, terraza y hostelería.")

# --- Parasoles ---
D["balliu-parasol-para-terraza-acrilico-236bd5f0"] = (
 "<p><strong>Parasol de exterior de Ø200 cm con tela acrílica, pensado para terrazas y áticos.</strong> La tela acrílica ofrece una resistencia al sol y a la decoloración superior a la del poliéster, manteniendo el color temporada tras temporada. Disponible con punta de mástil cónica o plana y con o sin faldón decorativo.</p>"
 + UL([
   "<strong>Tela:</strong> acrílica de alta resistencia UV.",
   "<strong>Diámetro:</strong> Ø200 cm.",
   "<strong>Opciones:</strong> 6 colores · punta cónica o plana · con o sin faldón.",
   "<strong>Uso recomendado:</strong> terraza y ático.",
   "<strong>Mantenimiento:</strong> cerrar con viento fuerte; limpiar con agua y jabón suave.",
 ]),
 "Parasol de terraza Ø200 cm en tela acrílica de alta resistencia UV. Punta cónica o plana, con o sin faldón. 6 colores. Para terraza y ático.")

D["balliu-parasol-para-terraza-82e48b2d"] = (
 "<p><strong>Parasol de exterior de Ø200 cm en tela de poliéster, una opción versátil para terrazas y espacios de hostelería.</strong> Disponible en una amplia gama de 16 colores para combinar con cualquier ambiente, con punta de mástil cónica o plana y faldón opcional. Buena protección solar a un precio contenido.</p>"
 + UL([
   "<strong>Tela:</strong> poliéster para exterior.",
   "<strong>Diámetro:</strong> Ø200 cm.",
   "<strong>Opciones:</strong> 16 colores · punta cónica o plana · con o sin faldón.",
   "<strong>Uso recomendado:</strong> terraza y hostelería.",
   "<strong>Mantenimiento:</strong> recoger con viento; limpiar con agua y jabón suave.",
 ]),
 "Parasol de terraza Ø200 cm en tela de poliéster, disponible en 16 colores. Punta cónica o plana, faldón opcional. Para terraza y hostelería.")

D["balliu-parasol-para-terraza-f1ed8b8b"] = (
 "<p><strong>Parasol de exterior en tela de poliéster, disponible en Ø200 y Ø250 cm para cubrir desde una mesa pequeña hasta un comedor de jardín.</strong> Se ofrece en 16 colores, así que es fácil integrarlo en cualquier terraza o zona de hostelería. La opción de Ø250 cm da más sombra para mesas grandes.</p>"
 + UL([
   "<strong>Tela:</strong> poliéster para exterior.",
   "<strong>Diámetros:</strong> Ø200 cm y Ø250 cm.",
   "<strong>Colores:</strong> 16 disponibles.",
   "<strong>Uso recomendado:</strong> jardín y hostelería.",
   "<strong>Mantenimiento:</strong> recoger con viento; limpiar con agua y jabón suave.",
 ]),
 "Parasol de exterior en poliéster, Ø200 o Ø250 cm, en 16 colores. Más sombra para mesas grandes. Para jardín y hostelería.")

D["balliu-parasol-para-terraza-acrilico-c8dd492d"] = (
 "<p><strong>Parasol de exterior con tela acrílica, disponible en Ø200 y Ø250 cm, para jardín y terraza.</strong> La tela acrílica resiste mejor el sol y conserva el color más tiempo que el poliéster, ideal si el parasol está expuesto muchas horas. La medida de Ø250 cm aporta sombra extra para mesas grandes, con faldón opcional.</p>"
 + UL([
   "<strong>Tela:</strong> acrílica de alta resistencia UV.",
   "<strong>Diámetros:</strong> Ø200 cm y Ø250 cm.",
   "<strong>Opciones:</strong> 6 colores · con o sin faldón.",
   "<strong>Uso recomendado:</strong> jardín y terraza.",
   "<strong>Mantenimiento:</strong> cerrar con viento fuerte; limpiar con agua y jabón suave.",
 ]),
 "Parasol de exterior en tela acrílica Ø200 o Ø250 cm, alta resistencia UV. 6 colores, faldón opcional. Para jardín y terraza.")

# --- Mesas ---
D["balliu-mesa-exterior-5d0fb586"] = (
 "<p><strong>Mesa auxiliar de exterior en resina decorativa de 48×48 cm, perfecta como mesa de apoyo en terrazas y balcones.</strong> La resina resiste el sol y la humedad sin oxidarse, y su formato compacto y ligero permite colocarla junto a una tumbona o un sofá y moverla con facilidad.</p>"
 + UL([
   "<strong>Material:</strong> resina decorativa para exterior.",
   "<strong>Medidas:</strong> 48 × 48 cm.",
   "<strong>Acabados:</strong> blanco, arena, bronce, gris oscuro y madera.",
   "<strong>Uso recomendado:</strong> terraza y balcón.",
   "<strong>Mantenimiento:</strong> limpieza con agua y jabón suave.",
 ]),
 "Mesa auxiliar de exterior en resina decorativa 48×48 cm para terraza y balcón. Resistente y ligera. Disponible en 5 acabados.")

D["balliu-mesa-exterior-140-18090-cm-e4ec7d7c"] = (
 "<p><strong>Mesa extensible de exterior con estructura de aluminio y tablero HPL, pensada para jardín, terraza y hostelería.</strong> El sistema extensible permite pasar de un uso diario a recibir invitados, y el tablero HPL aguanta sol, agua y arañazos sin perder color. El aluminio no se oxida y mantiene la mesa ligera y estable.</p>"
 + UL([
   "<strong>Material:</strong> estructura de aluminio + tablero HPL.",
   "<strong>Tamaños:</strong> 140/180 × 90 cm y 200/260 × 100 cm (extensible).",
   "<strong>Acabados:</strong> chasis en blanco, tórtola o aluminio; tablero en 5 colores.",
   "<strong>Uso recomendado:</strong> jardín, terraza y hostelería.",
   "<strong>Mantenimiento:</strong> limpieza con paño húmedo.",
 ]),
 "Mesa extensible de exterior en aluminio con tablero HPL (140/180×90 o 200/260×100 cm). No se oxida y resiste sol y agua. Jardín y hostelería.")

D["balliu-mesa-exterior-hpl-140-180100-cm-8e073aab"] = (
 "<p><strong>Mesa extensible de exterior de gran formato, con estructura de aluminio y tablero HPL, ideal para comedores de jardín y hostelería.</strong> Se extiende para sentar a más comensales cuando hace falta, y el tablero HPL resiste el sol, la lluvia y el uso intensivo sin deteriorarse. El aluminio garantiza ligereza y cero óxido.</p>"
 + UL([
   "<strong>Material:</strong> estructura de aluminio + tablero HPL.",
   "<strong>Tamaños:</strong> 140/180 × 100 cm y 200/260 × 100 cm (extensible).",
   "<strong>Acabados:</strong> chasis en blanco, tórtola o aluminio; tablero en 5 colores.",
   "<strong>Uso recomendado:</strong> jardín, terraza y hostelería.",
   "<strong>Mantenimiento:</strong> limpieza con paño húmedo.",
 ]),
 "Mesa extensible de exterior de aluminio con tablero HPL (140/180×100 o 200/260×100 cm). Resistente al sol y la lluvia. Jardín y hostelería.")

D["balliu-mesa-alta-exterior-hpl-94512eab"] = (
 "<p><strong>Mesa alta de exterior con estructura de aluminio y tablero HPL, perfecta para crear una zona tipo cóctel en terraza, balcón o local de hostelería.</strong> Su altura facilita usarla de pie o con taburetes altos. El aluminio no se oxida y el tablero HPL resiste el sol, el agua y los arañazos del uso diario.</p>"
 + UL([
   "<strong>Material:</strong> estructura de aluminio + tablero HPL.",
   "<strong>Tamaños:</strong> 60 × 60 cm y 70 × 70 cm · altura 110 cm.",
   "<strong>Uso recomendado:</strong> terraza, balcón, jardín y hostelería.",
   "<strong>Mantenimiento:</strong> limpieza con paño húmedo.",
 ]),
 "Mesa alta de exterior de aluminio con tablero HPL, altura 110 cm (60×60 o 70×70 cm). Resistente y sin óxido. Terraza, balcón y hostelería.")

# --- Silla ---
D["balliu-silla-exterior-sin-brazos-estilo-contemporaneo-53-cm-cd07e7d6"] = (
 "<p><strong>Silla de exterior en resina de estilo contemporáneo, disponible con o sin brazos, para jardín, terraza, balcón y hostelería.</strong> La resina resiste el sol y la humedad sin oxidarse y se limpia en un momento. Es ligera y apilable, lo que facilita ganar espacio cuando no se usa.</p>"
 + UL([
   "<strong>Material:</strong> resina de alta resistencia para exterior.",
   "<strong>Medidas:</strong> 59 cm (largo) × 53 cm (ancho) × 36 cm (alto de asiento) · 5 kg.",
   "<strong>Opciones:</strong> con brazos o sin brazos.",
   "<strong>Uso recomendado:</strong> jardín, terraza, balcón y hostelería.",
   "<strong>Mantenimiento:</strong> limpieza con agua y jabón suave; apilable.",
 ]),
 "Silla de exterior en resina, con o sin brazos, para jardín, terraza y hostelería. Resistente, ligera y apilable. Limpieza fácil.")

# --- Accesorios ---
D["balliu-colchoneta-para-tumbona-0e9a3256"] = (
 "<p><strong>Colchoneta de exterior para tumbona que añade confort y un acabado cuidado a tu zona de descanso.</strong> Disponible en distintos tejidos de exterior —incluido acrílico y Dry Feel de secado rápido— pensados para resistir el sol y la humedad. Aporta amortiguación sobre la tumbona sin renunciar a la resistencia a la intemperie.</p>"
 + UL([
   "<strong>Tejidos:</strong> tela de exterior, acrílico y Dry Feel (secado rápido), según versión.",
   "<strong>Uso recomendado:</strong> jardín y piscina, sobre tumbona.",
   "<strong>Mantenimiento:</strong> limpiar con agua y jabón suave; dejar secar al aire.",
 ]),
 "Colchoneta de exterior para tumbona en tejidos resistentes (acrílico, Dry Feel). Más confort en jardín y piscina. Fácil mantenimiento.")

D["balliu-funda-protectora-exterior-686cc405"] = (
 "<p><strong>Funda protectora de exterior para tumbona que prolonga la vida del mueble frente al sol, la lluvia y el polvo.</strong> Tejido resistente al agua que evita la decoloración y la suciedad cuando la tumbona no está en uso. Disponible en packs para cubrir varias piezas a la vez.</p>"
 + UL([
   "<strong>Para:</strong> tumbonas de exterior.",
   "<strong>Packs:</strong> 2, 12 o 24 unidades.",
   "<strong>Función:</strong> protección frente a sol, lluvia y polvo.",
   "<strong>Mantenimiento:</strong> dejar secar antes de guardar; limpiar con paño húmedo.",
 ]),
 "Funda protectora de exterior para tumbona, tejido resistente al agua. Protege del sol, la lluvia y el polvo. Packs de 2, 12 o 24 unidades.")

D["balliu-funda-protectora-exterior-acrilico-a1c16324"] = (
 "<p><strong>Funda protectora de exterior en tejido acrílico para parasol, con alta resistencia al sol y al agua.</strong> El acrílico protege el parasol cerrado de la lluvia y los rayos UV, evitando que la tela pierda color durante los meses de menos uso.</p>"
 + UL([
   "<strong>Para:</strong> parasoles de exterior.",
   "<strong>Material:</strong> tejido acrílico resistente al agua y a los rayos UV.",
   "<strong>Función:</strong> protección del parasol cerrado.",
   "<strong>Mantenimiento:</strong> limpiar con paño húmedo; guardar seca.",
 ]),
 "Funda protectora de exterior en acrílico para parasol. Resistente al agua y a los rayos UV, evita la decoloración. Protege el parasol cerrado.")

D["balliu-funda-protectora-exterior-6f6d4953"] = (
 "<p><strong>Funda protectora de exterior para sofá, disponible para módulos individuales, dobles y triples.</strong> Tejido resistente al agua que protege el sofá del sol, la lluvia y el polvo cuando no se usa, ayudando a conservar tapizados y estructura temporada tras temporada.</p>"
 + UL([
   "<strong>Para:</strong> sofás de exterior.",
   "<strong>Tamaños:</strong> sofá individual, doble y triple.",
   "<strong>Función:</strong> protección frente a sol, lluvia y polvo.",
   "<strong>Mantenimiento:</strong> dejar secar antes de guardar; limpiar con paño húmedo.",
 ]),
 "Funda protectora de exterior para sofá (individual, doble o triple). Tejido resistente al agua. Protege del sol, la lluvia y el polvo.")

D["balliu-funda-protectora-exterior-340b2844"] = (
 "<p><strong>Funda protectora de exterior para proteger tus muebles de jardín del sol, la lluvia y el polvo.</strong> Tejido resistente al agua que evita la decoloración y mantiene el mueble limpio cuando no está en uso, alargando su vida útil entre temporadas.</p>"
 + UL([
   "<strong>Para:</strong> muebles de exterior (silla/sillón).",
   "<strong>Material:</strong> tejido resistente al agua.",
   "<strong>Función:</strong> protección frente a sol, lluvia y polvo.",
   "<strong>Mantenimiento:</strong> dejar secar antes de guardar.",
 ]),
 "Funda protectora de exterior resistente al agua para muebles de jardín. Protege del sol, la lluvia y el polvo y alarga su vida útil.")

D["balliu-cojin-exterior-523e5ae9"] = (
 "<p><strong>Cojín de exterior de 40×40 cm para añadir color y confort a sillas, sofás y bancos de jardín.</strong> Relleno y tejido preparados para el exterior, que resisten la humedad y el uso diario. Una forma sencilla de renovar el ambiente de la terraza.</p>"
 + UL([
   "<strong>Medidas:</strong> 40 × 40 cm.",
   "<strong>Uso recomendado:</strong> sillas, sofás y bancos de exterior.",
   "<strong>Mantenimiento:</strong> limpiar con paño húmedo; guardar seco fuera de temporada.",
 ]),
 "Cojín de exterior 40×40 cm para sillas, sofás y bancos de jardín. Tejido y relleno resistentes a la humedad. Aporta color y confort.")

# --- Bases / pies de parasol ---
D["balliu-pie-de-parasol-c2147052"] = (
 "<p><strong>Pie de parasol de 40 kg que aporta la estabilidad necesaria para sujetar con seguridad parasoles de terraza y jardín.</strong> Su peso evita vuelcos con viento moderado y sirve de base firme para mástiles estándar. Disponible en acabado estándar y RE.</p>"
 + UL([
   "<strong>Peso:</strong> 40 kg.",
   "<strong>Acabados:</strong> estándar y RE.",
   "<strong>Función:</strong> base de sujeción para parasol.",
   "<strong>Uso recomendado:</strong> terraza y jardín.",
 ]),
 "Pie de parasol de 40 kg para sujetar con estabilidad parasoles de terraza y jardín. Evita vuelcos con viento moderado. Acabados estándar y RE.")

D["balliu-base-de-parasol-3ee8b72d"] = (
 "<p><strong>Base de hormigón para parasol, disponible en 25 y 30 kg, que asegura la sujeción del mástil con un peso firme y duradero.</strong> El hormigón ofrece una base estable y resistente a la intemperie, ideal para mantener el parasol fijo en terrazas y jardines.</p>"
 + UL([
   "<strong>Material:</strong> hormigón.",
   "<strong>Pesos:</strong> 25 kg y 30 kg.",
   "<strong>Función:</strong> base de sujeción para parasol.",
   "<strong>Uso recomendado:</strong> terraza y jardín.",
 ]),
 "Base de hormigón para parasol de 25 o 30 kg. Sujeción firme y resistente a la intemperie para terraza y jardín.")

D["base-de-parasol-25-kg"] = (
 "<p><strong>Base de parasol de 25 kg, el complemento esencial para mantener tu sombrilla de exterior estable y segura.</strong> Compacta y resistente, ofrece un punto de anclaje firme para el mástil y evita que el parasol se mueva o vuelque con viento ligero. Fácil de colocar y reubicar.</p>"
 + UL([
   "<strong>Peso:</strong> 25 kg.",
   "<strong>Función:</strong> base de sujeción para parasol/sombrilla.",
   "<strong>Uso recomendado:</strong> terraza y jardín.",
   "<strong>Ventaja:</strong> compacta y fácil de reubicar.",
 ]),
 "Base de parasol de 25 kg para sombrillas de exterior. Sujeción estable y segura, compacta y fácil de colocar. Para terraza y jardín.")

# --- Conjuntos (Hevea) — sin códigos de proveedor ---
def set_desc(opening, incluye, material, uso, meta):
    return (f"<p><strong>{opening}</strong></p>"
            + UL([
                f"<strong>Incluye:</strong> {incluye}.",
                f"<strong>Material:</strong> {material}.",
                f"<strong>Uso recomendado:</strong> {uso}.",
                "<strong>Mantenimiento:</strong> estructura, limpieza con paño húmedo; cojines, guardar secos fuera de temporada.",
            ]), meta)

D["set-rinconera-exterior-hpl-moderno-sofa-de-esquina-mesa-de-centro"] = set_desc(
 "Conjunto rinconera de exterior de gran formato y estilo moderno, con sofá de esquina y mesa de centro de tablero HPL, ideal para terrazas amplias. Crea un salón al aire libre que combina amplitud, comodidad y materiales resistentes a la intemperie.",
 "sofá de esquina + mesa de centro con tablero HPL",
 "estructura preparada para exterior, cojines de exterior y tablero HPL resistente al sol y la humedad",
 "terrazas y jardines amplios",
 "Conjunto rinconera de exterior moderno: sofá de esquina + mesa de centro con tablero HPL. Amplio y resistente, para terrazas grandes.")

D["set-rinconera-exterior-hpl-elegante-sofa-de-esquina-mesa-de-centro"] = set_desc(
 "Conjunto rinconera de exterior de diseño elegante, con sofá de esquina amplio y mesa de centro de tablero HPL. Su línea contemporánea y sus materiales resistentes garantizan confort y durabilidad en jardines y terrazas.",
 "sofá de esquina + mesa de centro con tablero HPL",
 "estructura preparada para exterior, cojines de exterior y tablero HPL resistente al sol y la humedad",
 "jardín y terraza",
 "Conjunto rinconera de exterior elegante: sofá de esquina + mesa de centro HPL. Confort y durabilidad para jardín y terraza.")

D["set-rinconera-exterior-hpl-sofisticado-sofa-de-esquina-mesa-de-centro"] = set_desc(
 "Conjunto rinconera de exterior de estilo sofisticado en blanco y beige, con sofá de esquina y mesa de centro de tablero HPL. Optimiza el espacio exterior y crea un ambiente amplio, cómodo y de aire actual.",
 "sofá de esquina + mesa de centro con tablero HPL (blanco-beige)",
 "estructura preparada para exterior, cojines de exterior y tablero HPL resistente al sol y la humedad",
 "terraza y jardín",
 "Conjunto rinconera de exterior sofisticado (blanco-beige): sofá de esquina + mesa de centro HPL. Amplio y cómodo para terraza.")

D["set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro"] = set_desc(
 "Conjunto rinconera de exterior de estilo contemporáneo, con sofá de esquina y mesa de centro, diseñado para crear un salón al aire libre amplio y acogedor. Su estructura resistente y sus líneas actuales aportan comodidad y elegancia en jardines y terrazas.",
 "sofá de esquina + mesa de centro",
 "estructura preparada para exterior y cojines de exterior",
 "jardín y terraza",
 "Conjunto rinconera de exterior contemporáneo: sofá de esquina + mesa de centro. Salón al aire libre amplio y acogedor.")

D["set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa-3"] = set_desc(
 "Conjunto de jardín de 2 plazas y estilo contemporáneo, con sofá de 2 plazas, dos sillones y mesa de centro. Una composición equilibrada y acogedora, pensada para terrazas que buscan confort y un diseño actual.",
 "sofá de 2 plazas + 2 sillones + mesa de centro",
 "estructura preparada para exterior y cojines de exterior",
 "terrazas y jardines",
 "Conjunto de jardín 2 plazas contemporáneo: sofá 2 plazas + 2 sillones + mesa de centro. Equilibrado y acogedor para terraza.")

D["set-jardin-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa"] = set_desc(
 "Conjunto de jardín de 2 plazas y estilo contemporáneo, formado por sofá de 2 plazas, dos sillones y mesa de centro. Composición armoniosa y moderna, ideal para crear una zona de estar exterior cómoda y con personalidad.",
 "sofá de 2 plazas + 2 sillones + mesa de centro",
 "estructura preparada para exterior y cojines de exterior",
 "terrazas y jardines",
 "Conjunto de jardín 2 plazas contemporáneo: sofá 2 plazas + 2 sillones + mesa de centro. Zona de estar exterior cómoda y moderna.")

D["set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4"] = set_desc(
 "Conjunto de jardín de 2 plazas y estilo moderno, con sofá de 2 plazas, dos sillones y mesa de centro. Una composición equilibrada para crear terrazas acogedoras y funcionales sin renunciar al diseño.",
 "sofá de 2 plazas + 2 sillones + mesa de centro",
 "estructura preparada para exterior y cojines de exterior",
 "terrazas y jardines",
 "Conjunto de jardín 2 plazas moderno: sofá 2 plazas + 2 sillones + mesa de centro. Terraza acogedora y funcional.")

D["set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-3"] = set_desc(
 "Conjunto de jardín de 2 plazas y estilo moderno, con sofá de 2 plazas, dos sillones y mesa de centro. Un conjunto funcional y armonioso, perfecto para crear un ambiente exterior acogedor.",
 "sofá de 2 plazas + 2 sillones + mesa de centro",
 "estructura preparada para exterior y cojines de exterior",
 "terrazas y jardines",
 "Conjunto de jardín 2 plazas moderno: sofá 2 plazas + 2 sillones + mesa de centro. Ambiente exterior acogedor y funcional.")

D["set-jardin-3-plazas-urbano-sofa-3-plazas-2-sillones-mesa"] = set_desc(
 "Conjunto de jardín de 3 plazas y estilo urbano, con sofá de 3 plazas, dos sillones y mesa de centro. Una solución amplia para zonas de estar exteriores donde prima el confort y un diseño de aire urbano.",
 "sofá de 3 plazas + 2 sillones + mesa de centro",
 "estructura preparada para exterior y cojines de exterior",
 "terrazas y jardines amplios",
 "Conjunto de jardín 3 plazas urbano: sofá 3 plazas + 2 sillones + mesa de centro. Amplio y confortable para terrazas grandes.")

D["set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-4"] = set_desc(
 "Conjunto de jardín de 3 plazas y estilo contemporáneo, con sofá de 3 plazas, dos sillones y mesa de centro. Una composición amplia pensada para aportar confort, resistencia y estilo en terrazas actuales.",
 "sofá de 3 plazas + 2 sillones + mesa de centro",
 "estructura preparada para exterior y cojines de exterior",
 "terrazas y jardines amplios",
 "Conjunto de jardín 3 plazas contemporáneo: sofá 3 plazas + 2 sillones + mesa de centro. Confort y estilo para terrazas amplias.")

def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    if "errors" in d: raise RuntimeError(d["errors"])
    return d["data"]

GET = """query($h:String!){ productByHandle(handle:$h){ id handle descriptionHtml seo{description title} } }"""
SET = """mutation($input:ProductInput!){ productUpdate(input:$input){ product{id handle} userErrors{field message} } }"""

def words(html):
    import re
    return len(re.sub(r"<[^>]+>"," ", html or "").split())

def main():
    if not SHOPIFY_ACCESS_TOKEN: sys.exit("SHOPIFY_ACCESS_TOKEN vacío")
    backup = {}
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} — {len(D)} fichas\n")
    errors = 0
    for h,(body,meta) in D.items():
        try:
            p = gql(GET, {"h":h})["productByHandle"]
        except Exception as e:
            print(f"✗ {h}: error leyendo ({e})"); errors+=1; continue
        if not p:
            print(f"✗ {h}: no encontrado"); errors+=1; continue
        backup[h] = {"id":p["id"], "descriptionHtml":p["descriptionHtml"], "seo":p.get("seo")}
        print(f"• {h}: {words(p['descriptionHtml'])}→{words(body)} palabras")
        if APPLY:
            inp = {"id":p["id"], "descriptionHtml":body, "seo":{"description":meta}}
            res = gql(SET, {"input":inp})["productUpdate"]
            ue = res["userErrors"]
            if ue: print(f"    ⚠️ userErrors: {ue}"); errors+=1
    # Backup siempre (también en dry-run, sirve de snapshot previo)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = os.path.join(ROOT, "content", "descriptions", f"backup_{ts}.json")
    json.dump(backup, open(bpath,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n💾 Backup de lo ACTUAL → {bpath}")
    print(f"{'✅ Aplicado' if APPLY else 'ℹ️ Dry-run completado'} · errores: {errors}")
    if not APPLY:
        print("Revisa y, si ok, ejecuta con --apply")

if __name__ == "__main__":
    main()
