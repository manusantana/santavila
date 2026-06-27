#!/usr/bin/env python3
"""
Sprint GEO 4: crea/refuerza guias citables en el blog.

Dry-run por defecto:
  .venv/bin/python scripts/apply_geo_guides.py

Aplicar:
  .venv/bin/python scripts/apply_geo_guides.py --apply
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
API_VERSION = "2026-01"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
AUTHOR = "Equipo Santavila"
BLOG_HANDLE = "news"


GUIDES = {
    "tumbona-de-aluminio-resina-o-madera-cual-elegir-para-exterior": {
        "title": "Tumbona de aluminio, resina o madera: cuál elegir para exterior",
        "summary": "Comparativa práctica para elegir tumbona de exterior según material: aluminio, resina, madera/teca, textilene, piscina, costa, peso, mantenimiento y uso.",
        "meta_title": "Tumbona de aluminio, resina o madera: cuál elegir",
        "meta_description": "Compara tumbonas de aluminio, resina y madera para exterior: piscina, costa, peso, mantenimiento, comodidad, textilene y uso recomendado.",
        "body_html": """
<p><strong>Para la mayoría de jardines, piscinas y terrazas, una tumbona de aluminio con textilene o una tumbona de resina exterior suele ser la opción más práctica.</strong> El aluminio pesa poco y no se oxida como el acero; la resina es muy fácil de limpiar y funciona muy bien junto a piscina; la madera aporta más calidez visual, pero exige más mantenimiento y pesa más.</p>

<h2>Comparativa rápida de tumbonas por material</h2>
<table>
  <thead>
    <tr><th>Material</th><th>Ventaja principal</th><th>Mantenimiento</th><th>Peso</th><th>Mejor uso</th></tr>
  </thead>
  <tbody>
    <tr><td>Aluminio + textilene</td><td>Ligereza, resistencia al óxido y secado rápido</td><td>Bajo</td><td>Ligero</td><td>Piscina, terraza, uso frecuente y mover a menudo</td></tr>
    <tr><td>Resina / polipropileno exterior</td><td>Limpieza sencilla y buena relación uso/precio</td><td>Muy bajo</td><td>Ligero-medio</td><td>Piscina, alquiler turístico, hostelería y uso intensivo</td></tr>
    <tr><td>Madera / teca</td><td>Calidez estética y presencia premium</td><td>Medio-alto</td><td>Medio-pesado</td><td>Porche, jardín cuidado o terraza con estética natural</td></tr>
    <tr><td>Acero tratado</td><td>Robustez estructural</td><td>Medio-alto</td><td>Pesado</td><td>Zonas protegidas, mejor si no hay salitre</td></tr>
    <tr><td>Ratán sintético PE</td><td>Aspecto lounge y mantenimiento bajo</td><td>Bajo</td><td>Medio</td><td>Zona chill-out o porche cubierto</td></tr>
  </tbody>
</table>

<h2>Tumbonas de aluminio: ligeras y muy prácticas</h2>
<p>El aluminio lacado o pintado en polvo es uno de los materiales más cómodos para una <a href="/collections/tumbonas">tumbona de exterior</a>. No se oxida como el acero, pesa poco y permite mover la pieza para buscar sol, sombra o guardarla al final del día. En muchas tumbonas se combina con textilene, una malla técnica que seca rápido y evita depender siempre de cojines.</p>
<p>Su punto débil no suele ser la lluvia, sino la calidad del acabado y el cuidado en costa. En zonas con salitre conviene limpiar con más frecuencia, especialmente uniones, tornillos y zonas donde se acumule polvo. Si quieres una tumbona fácil de mover y de estética limpia, el aluminio suele ser la primera opción.</p>

<h2>Tumbonas de resina: piscina, limpieza y uso intensivo</h2>
<p>La resina de exterior y el polipropileno son muy prácticos cuando la prioridad es limpiar rápido, resistir humedad y equipar varias piezas sin complicarse. Por eso son habituales en piscinas, alojamientos turísticos y zonas de uso intensivo. No se oxidan, no absorben agua como una madera sin tratar y se limpian con agua y jabón suave.</p>
<p>La clave está en que sea resina apta para exterior, con buena formulación y protección frente al sol. Una resina pobre puede decolorarse o volverse quebradiza antes. Si buscas bajo mantenimiento, precio contenido y facilidad de reposición, la resina tiene mucho sentido.</p>

<h2>Tumbonas de madera o teca: calidez, pero más cuidado</h2>
<p>La madera cambia por completo la lectura de una zona de descanso: aporta textura, calidez y una presencia más decorativa. La teca es especialmente apreciada en exterior por sus aceites naturales y su estabilidad, pero no es “sin mantenimiento”. Con el sol puede evolucionar hacia una pátina gris plateada; si quieres conservar el tono dorado, tendrás que limpiar y aplicar protector o aceite específico de forma periódica.</p>
<p>En tumbonas, la madera también pesa más. Eso puede ser positivo si quieres una pieza estable en un porche, pero incómodo si vas a moverla cada día alrededor de la piscina. Para exposición dura, conviene revisar drenaje, ventilación y evitar humedad estancada.</p>

<h2>¿Qué material elegir junto a una piscina?</h2>
<p>Junto a piscina, prioriza materiales que no absorban agua, se limpien rápido y soporten cloro, crema solar y humedad frecuente. Aluminio con textilene y resina exterior suelen ser las opciones más sencillas. La madera puede funcionar, pero pide más atención: limpieza, secado y protector si quieres mantener aspecto.</p>
<p>También importa el detalle práctico: ruedas, respaldo reclinable, apilabilidad y si la superficie se seca rápido antes de sentarte. Una tumbona muy bonita que retiene humedad o cuesta mover acaba usándose menos.</p>

<h2>¿Qué material funciona mejor en costa?</h2>
<p>En costa, el salitre acelera el desgaste de acabados y tornillería. El aluminio lacado y la resina exterior funcionan bien si se limpian de forma periódica para retirar sal. Evita acero mal protegido y revisa uniones. Si eliges madera, asume limpieza y mantenimiento más constantes.</p>
<p>La recomendación prudente es no pensar solo en el material principal: mira también tornillos, ruedas, bisagras, remaches y mecanismos de reclinado. En una tumbona, esas piezas trabajan mucho.</p>

<h2>Comodidad: estructura, respaldo y tejido importan tanto como el material</h2>
<p>Una buena tumbona no se elige solo por material. Revisa número de posiciones del respaldo, altura, anchura, curvatura, presencia de ruedas y si necesitas colchoneta. El textilene o malla técnica puede resultar muy práctico porque ofrece soporte y seca rápido; una tumbona rígida de resina puede necesitar colchoneta para largas siestas.</p>
<p>Si vas a leer o usarla muchas horas, prioriza respaldo regulable. Si será para piscina y cambios rápidos de sitio, prioriza ligereza y ruedas. Si será una pieza decorativa fija, puedes permitirte más peso y material cálido.</p>

<h2>Checklist antes de comprar una tumbona</h2>
<ul>
  <li>¿La vas a mover a diario o quedará fija?</li>
  <li>¿Estará junto a piscina, en costa o bajo porche?</li>
  <li>¿Necesitas ruedas o apilabilidad?</li>
  <li>¿El respaldo se reclina en varias posiciones?</li>
  <li>¿La superficie seca rápido tras lluvia o baño?</li>
  <li>¿Necesita colchoneta para ser cómoda?</li>
  <li>¿Puedes limpiarla y guardarla sin esfuerzo?</li>
</ul>

<h2>Cómo decidir según tu caso</h2>
<ul>
  <li><strong>Piscina familiar:</strong> resina exterior o aluminio con textilene.</li>
  <li><strong>Terraza donde mueves muebles a menudo:</strong> aluminio ligero.</li>
  <li><strong>Alojamiento turístico:</strong> resina o aluminio por limpieza y reposición.</li>
  <li><strong>Porche decorativo:</strong> madera/teca si aceptas mantenimiento.</li>
  <li><strong>Costa:</strong> aluminio lacado o resina, limpiando salitre con frecuencia.</li>
</ul>

<h2>Fuentes y criterio técnico</h2>
<p>Esta guía se ha redactado contrastando criterios de materiales de exterior, resistencia del aluminio frente al óxido, uso de resinas y polietileno en mobiliario outdoor, recomendaciones de mantenimiento de teca y guías editoriales sobre durabilidad real frente a sol, lluvia, cloro y uso frecuente. La recomendación final se adapta al catálogo y al uso real en terrazas, jardines y piscinas españolas.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Es mejor una tumbona de aluminio o de resina?</h3>
<p>Depende del uso. El aluminio suele ser más ligero y premium; la resina es muy práctica, fácil de limpiar y buena para piscina o uso intensivo. Ambas son buenas opciones si están preparadas para exterior.</p>
<h3>¿La tumbona de aluminio se oxida?</h3>
<p>El aluminio no se oxida como el acero, aunque puede deteriorarse el acabado si se descuida. En costa conviene limpiar salitre y revisar uniones y tornillería.</p>
<h3>¿Una tumbona de madera puede quedarse fuera?</h3>
<p>Puede quedarse fuera si la madera es adecuada para exterior y se mantiene bien, pero requiere más cuidado que aluminio o resina. Evita humedad estancada y sigue las indicaciones del fabricante.</p>
<h3>¿Qué tumbona es mejor para piscina?</h3>
<p>Para piscina suelen funcionar muy bien la resina exterior y el aluminio con textilene, porque no absorben agua, se limpian rápido y son fáciles de mover.</p>
<h3>¿Necesito colchoneta para una tumbona?</h3>
<p>No siempre. Las tumbonas con textilene pueden ser cómodas sin colchoneta; las superficies rígidas de resina o madera suelen agradecer una colchoneta si vas a usarlas durante mucho tiempo.</p>
""",
    },
    "como-elegir-mesa-de-exterior-medidas-comensales-y-espacio-necesario": {
        "title": "Cómo elegir mesa de exterior: medidas, comensales y espacio necesario",
        "summary": "Guía práctica para elegir una mesa de exterior según número de comensales, forma, espacio disponible, paso, sillas y material del tablero.",
        "meta_title": "Cómo elegir mesa de exterior: medidas y comensales",
        "meta_description": "Guía para elegir mesa de exterior: medidas por comensales, espacio necesario para sillas, mesas redondas, rectangulares, extensibles y HPL.",
        "body_html": """
<p><strong>Para elegir una mesa de exterior, calcula primero cuántas personas la usarán a diario y cuánto espacio libre tienes alrededor para sacar sillas y circular.</strong> Como orientación, una mesa de 60-70 cm sirve para 2 personas, 120 cm para 4, 160-180 cm para 6 y 200-240 cm para 8, siempre ajustando según forma, tipo de silla y espacio real de terraza.</p>

<h2>Respuesta rápida: medidas orientativas por comensales</h2>
<table>
  <thead>
    <tr><th>Comensales</th><th>Mesa redonda</th><th>Mesa rectangular/cuadrada</th><th>Uso recomendado</th></tr>
  </thead>
  <tbody>
    <tr><td>2 personas</td><td>60-70 cm diámetro</td><td>60x60 o 70x70 cm</td><td>Balcón, café, desayuno o terraza pequeña</td></tr>
    <tr><td>4 personas</td><td>90-100 cm diámetro</td><td>120x70/80 cm aprox.</td><td>Comedor compacto de terraza</td></tr>
    <tr><td>6 personas</td><td>120-140 cm diámetro</td><td>160-180x90 cm aprox.</td><td>Comedor exterior familiar</td></tr>
    <tr><td>8 personas</td><td>150 cm o más, si hay espacio</td><td>200-240x90/100 cm aprox.</td><td>Jardín, porche amplio o comidas largas</td></tr>
    <tr><td>Uso variable</td><td>Redonda extensible si existe</td><td>Extensible 140/200, 160/240 o similar</td><td>Día a día compacto e invitados puntuales</td></tr>
  </tbody>
</table>
<p>Estas medidas no son una ley exacta: cambian con el ancho de las sillas, si tienen brazos, el grosor de las patas y si quieres poner fuentes, paneras o decoración en el centro. Para comprar con seguridad, mide siempre la terraza completa y simula la mesa con cinta en el suelo.</p>

<h2>La medida que más se olvida: espacio para mover sillas</h2>
<p>Una mesa no ocupa solo lo que mide el tablero. También necesita zona para sacar la silla, sentarse y pasar detrás. En interior se suele recomendar alrededor de 90 cm libres como referencia cómoda alrededor de la mesa; en una terraza pequeña puedes bajar esa ambición, pero entonces conviene usar sillas ligeras, plegables o sin brazos.</p>
<p>Si el paso queda justo, no fuerces una mesa grande. Es mejor una mesa de 120 cm cómoda que una de 160 cm que obliga a mover las sillas cada vez. En balcones, mira también la guía de <a href="/blogs/news/como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales">cómo amueblar una terraza pequeña o balcón</a>.</p>

<h2>Mesa redonda, rectangular, cuadrada o extensible</h2>
<p>La forma de la mesa cambia mucho la sensación de espacio. Una redonda facilita la conversación y evita esquinas, por eso funciona bien en terrazas pequeñas o zonas de paso. Una rectangular aprovecha mejor paredes, porches largos y comedores para 6 u 8 personas. Una cuadrada es muy práctica para 2 o 4, pero puede quedarse corta si quieres servir platos al centro.</p>
<p>Las mesas extensibles son la opción más lógica cuando hay dos vidas: uso diario de 2-4 personas e invitados algunos fines de semana. La clave es comprobar también la medida abierta, no solo cerrada. Si abierta bloquea la puerta o el paso, la extensión será más teórica que útil.</p>

<h2>Cómo elegir según el espacio real</h2>
<ul>
  <li><strong>Balcón estrecho:</strong> mesa plegable, abatible o redonda de 60-70 cm.</li>
  <li><strong>Terraza pequeña:</strong> mesa redonda de 90 cm o rectangular de 120 cm, con sillas ligeras.</li>
  <li><strong>Porche familiar:</strong> rectangular de 160-180 cm o extensible.</li>
  <li><strong>Jardín amplio:</strong> 200-240 cm si comes habitualmente con 8 personas.</li>
  <li><strong>Hostelería o alquiler:</strong> formatos repetibles, fáciles de limpiar y mover.</li>
</ul>

<h2>Sillas: el tablero no lo decide todo</h2>
<p>Dos mesas de la misma medida pueden admitir distinto número de personas según las sillas. Una silla sin brazos ocupa menos y entra mejor bajo el tablero. Una silla con brazos es más cómoda para sobremesa, pero exige más ancho y puede chocar con el faldón o la estructura de la mesa.</p>
<p>Antes de comprar, revisa tres cosas: ancho de silla, altura de asiento y si los brazos entran bajo la mesa. Como referencia ergonómica, la distancia entre asiento y tablero suele ser cómoda cuando deja margen suficiente para piernas sin que el usuario coma demasiado alto o encajado.</p>

<h2>Materiales de tablero para exterior</h2>
<p>En <a href="/collections/mesas">mesas de exterior</a>, el tablero recibe platos, vasos, sol, humedad y limpieza frecuente. Por eso el material importa mucho. El HPL es una opción muy práctica para exterior porque resiste bien el uso diario y se limpia con facilidad. El aluminio es ligero y cómodo en estructuras. La madera aporta calidez, pero exige más cuidado y puede cambiar de color con el sol.</p>
<p>Si la mesa estará a pleno sol, cerca de piscina o en costa, revisa la <a href="/blogs/news/que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol">guía de muebles resistentes a lluvia y sol</a> y la <a href="/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico">guía de materiales</a>. Para mantenimiento, la pauta básica está en la guía de <a href="/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada">limpieza de muebles de exterior</a>.</p>

<h2>Altura de mesa: comedor, auxiliar o alta</h2>
<p>Una mesa de comedor exterior suele rondar la altura de una mesa de comedor interior. Es la más cómoda para comer sentado con silla estándar. Una mesa auxiliar sirve para apoyar bebidas, libros o aperitivo junto a un sofá, pero no sustituye bien a una mesa de comedor. Una mesa alta funciona para uso tipo barra, terraza de hostelería o aperitivo de pie, pero no es lo más cómodo para comidas largas.</p>
<p>Elige altura según uso, no solo por estética. Si la terraza será un comedor real, compra mesa de comedor. Si será zona lounge, prioriza mesa de centro o auxiliar. Si será una zona social rápida, una mesa alta puede tener sentido.</p>

<h2>Checklist antes de comprar una mesa de exterior</h2>
<ul>
  <li>¿Cuántas personas comen a diario y cuántas solo ocasionalmente?</li>
  <li>¿Hay espacio para sacar sillas sin bloquear puerta o paso?</li>
  <li>¿Las sillas elegidas caben bajo la mesa?</li>
  <li>¿La mesa abierta, si es extensible, sigue dejando paso?</li>
  <li>¿El tablero soporta el uso real: comida, sol, humedad y limpieza?</li>
  <li>¿Puedes moverla o cubrirla cuando haga falta?</li>
  <li>¿Entra por ascensor, escalera, puerta y acceso a terraza?</li>
</ul>

<h2>Errores habituales al elegir mesa de exterior</h2>
<ul>
  <li><strong>Comprar solo por número de plazas:</strong> una mesa “para 6” puede ser incómoda con sillas anchas.</li>
  <li><strong>Olvidar el paso:</strong> el tablero cabe, pero las personas no circulan.</li>
  <li><strong>Elegir una extensible enorme:</strong> si abierta no cabe, no resolverá las comidas con invitados.</li>
  <li><strong>No pensar en el viento:</strong> manteles, parasoles y objetos ligeros condicionan el uso real.</li>
  <li><strong>Ignorar el mantenimiento:</strong> un tablero bonito puede no ser el más cómodo si necesita demasiado cuidado.</li>
</ul>

<h2>Fuentes y criterio técnico</h2>
<p>Esta guía se ha redactado contrastando medidas estándar de mesas de comedor, recomendaciones de espacio libre alrededor de la mesa, criterios de ancho por comensal y guías editoriales sobre mesas para espacios pequeños. La recomendación final se adapta a uso exterior: terraza real, sillas que se mueven, viento, sol, limpieza y necesidad de guardar o cubrir fuera de temporada.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Qué medida de mesa exterior necesito para 4 personas?</h3>
<p>Como orientación, una mesa rectangular de unos 120x70/80 cm o una redonda de 90-100 cm suele funcionar para 4 personas. Si las sillas tienen brazos o quieres servir al centro, conviene algo más de margen.</p>
<h3>¿Qué mesa exterior elijo para 6 personas?</h3>
<p>Para 6 personas, una mesa rectangular de 160-180 cm suele ser una medida cómoda. En redonda, 120-140 cm puede funcionar, siempre que haya espacio suficiente alrededor.</p>
<h3>¿Mesa redonda o rectangular para terraza pequeña?</h3>
<p>La redonda suele facilitar el paso y la conversación en espacios compactos. La rectangular aprovecha mejor una pared o un porche alargado. Si el espacio es muy estrecho, valora una plegable.</p>
<h3>¿Cuánto espacio dejo alrededor de la mesa?</h3>
<p>Lo ideal es dejar espacio para sacar sillas y circular. Como referencia cómoda, unos 90 cm alrededor funcionan bien; si no cabe, reduce tamaño de mesa o usa sillas plegables o sin brazos.</p>
<h3>¿Merece la pena una mesa extensible de exterior?</h3>
<p>Sí, si cerrada encaja en el uso diario y abierta sigue dejando paso. Es buena solución para quien come normalmente 2-4 personas y recibe invitados puntuales.</p>
""",
    },
    "como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales": {
        "title": "Cómo amueblar una terraza pequeña o balcón: medidas, muebles y distribución",
        "summary": "Guía práctica para elegir muebles de exterior en terrazas pequeñas y balcones: medidas, distribución, mesas, sillas, sombra, almacenaje y errores a evitar.",
        "meta_title": "Cómo amueblar una terraza pequeña o balcón",
        "meta_description": "Guía para amueblar una terraza pequeña o balcón: medidas, distribución, muebles plegables, mesas compactas, sillas, sombra y almacenaje.",
        "body_html": """
<p><strong>Para amueblar una terraza pequeña o balcón, empieza midiendo el espacio útil, define un solo uso principal y elige muebles ligeros, plegables, apilables o multifunción.</strong> En espacios compactos funciona mejor una mesa de 60-70 cm con dos sillas, un banco perimetral con almacenaje o una mesa auxiliar, dejando siempre un paso cómodo y evitando llenar el suelo con piezas decorativas.</p>

<h2>Antes de comprar: mide tres cosas</h2>
<p>En una terraza grande puedes corregir sobre la marcha. En un balcón, 10 cm cambian todo. Antes de elegir muebles, mide el ancho real, el fondo útil y el punto más estrecho de paso: puerta, barandilla, desagüe, aire acondicionado, maceteros fijos o armarios exteriores.</p>
<ul>
  <li><strong>Espacio útil:</strong> mide solo la zona donde puedes pisar y colocar muebles.</li>
  <li><strong>Apertura de puerta:</strong> comprueba que la puerta no choque con mesa, sillas o banco.</li>
  <li><strong>Acceso:</strong> asegúrate de que el mueble entra por ascensor, escalera, pasillo y puerta.</li>
</ul>
<p>Un truco muy fiable es marcar en el suelo la huella de cada pieza con cinta de carrocero o cartón. Si tienes que girarte de lado para pasar, el mueble es demasiado grande para uso diario.</p>

<h2>Medidas orientativas para no equivocarte</h2>
<table>
  <thead>
    <tr><th>Espacio</th><th>Mejor uso</th><th>Muebles recomendados</th><th>Evita</th></tr>
  </thead>
  <tbody>
    <tr><td>Balcón estrecho, menos de 120 cm de fondo</td><td>Café, lectura o apoyo</td><td>Mesa plegable, dos sillas plegables, taburete o mesa auxiliar</td><td>Sofás profundos y mesas con cuatro sillas</td></tr>
    <tr><td>Balcón de 120-160 cm de fondo</td><td>Bistró para 2 personas</td><td>Mesa redonda 60-70 cm, sillas ligeras, maceteros verticales</td><td>Piezas pesadas que bloqueen el paso</td></tr>
    <tr><td>Terraza pequeña 4-6 m²</td><td>Comedor pequeño o rincón lounge</td><td>Mesa compacta, banco perimetral, dos sillones o sillas apilables</td><td>Intentar comedor y sofá a la vez</td></tr>
    <tr><td>Terraza 6-10 m²</td><td>Comedor 2-4 o zona de estar</td><td>Mesa extensible compacta, sillas apilables, sofá 2 plazas</td><td>Rinconeras grandes sin zona de paso</td></tr>
  </tbody>
</table>
<p>Como referencia de ergonomía, en comedor se suele recomendar dejar espacio alrededor de la mesa para sacar sillas y circular. En balcones esto no siempre es posible, así que la decisión correcta puede ser bajar escala: mesa bistró, mesa de pared, banco o mesa auxiliar.</p>

<h2>Elige un uso principal: comer, descansar o tener plantas</h2>
<p>El error habitual en una terraza pequeña es quererlo todo: comedor, sofá, tumbona, bar, plantas y almacenaje. Funciona mejor elegir una prioridad y que el resto acompañe. Si quieres desayunar fuera, manda la mesa. Si quieres leer, manda una butaca cómoda. Si quieres recibir, manda un banco o dos sillas ligeras.</p>
<p>Para comer a diario, mira <a href="/collections/mesas">mesas de exterior</a> compactas y sillas que puedan recogerse. Para crear zona de estar, prioriza <a href="/collections/sillones-de-exterior">sillones de exterior</a> o un sofá pequeño antes que una mesa grande. Para un balcón estrecho, una mesa auxiliar puede ser más útil que una mesa de comedor.</p>

<h2>Mesas para terraza pequeña: redonda, cuadrada o plegable</h2>
<p>Una mesa redonda de 60-70 cm suele funcionar bien para dos personas porque no tiene esquinas y permite moverse mejor. Una mesa cuadrada aprovecha mejor la pared si la vas a arrimar. Una mesa plegable o abatible es la opción más flexible si el balcón también sirve para tender, pasar o cuidar plantas.</p>
<p>Si quieres comer fuera con frecuencia, evita tableros demasiado pequeños: para dos platos, vasos y algo de centro, 60 cm es el mínimo razonable. Si solo quieres café, portátil o aperitivo, una mesa auxiliar puede bastar.</p>

<h2>Sillas: mejor ligeras, apilables o plegables</h2>
<p>En espacios pequeños, las <a href="/collections/sillas-de-exterior">sillas de exterior</a> deben poder moverse sin esfuerzo. Las apilables son ideales si recibes gente de vez en cuando; las plegables van mejor cuando necesitas liberar el balcón a diario. Las sillas con brazos son más cómodas, pero ocupan más ancho y pueden no entrar bien bajo la mesa.</p>
<p>Si dudas, compra primero para el uso real de cada día, no para el día excepcional. Dos sillas cómodas y una mesa correcta suelen rendir más que cuatro sillas apretadas que obligan a mover todo cada vez.</p>

<h2>Bancos y rincones: aprovechar el perímetro</h2>
<p>Cuando la planta es cuadrada o hay una pared libre, un banco pegado al perímetro puede dar más asiento con menos desorden visual. Si además tiene almacenaje, ayuda a guardar cojines, fundas o pequeños accesorios. La clave es no cerrar todos los lados: deja una entrada clara y un centro respirable.</p>
<p>En una terraza muy pequeña, un banco en L puede funcionar si la esquina queda realmente libre. Si invade la puerta o bloquea el desagüe, mejor dos sillas sueltas.</p>

<h2>Almacenaje y verticalidad: libera el suelo</h2>
<p>Las terrazas pequeñas se saturan rápido cuando todo vive en el suelo. Usa pared, barandilla o esquinas para plantas, iluminación o pequeños accesorios. Las estanterías de exterior, maceteros verticales y mesas nido ayudan a conservar superficie libre.</p>
<p>Con plantas y jardineras, sé prudente: reparte peso, evita colgar piezas inestables hacia la calle y comprueba que el drenaje no moleste a vecinos o pavimento. Si el edificio tiene normas de comunidad, conviene revisarlas antes de fijar elementos a fachada o barandilla.</p>

<h2>Sombra, viento y privacidad</h2>
<p>En balcones, un parasol grande no siempre es buena idea. Puede ocupar demasiado, ser incómodo con viento o necesitar una base que robe suelo. Valora opciones proporcionales: un parasol pequeño bien lastrado, una vela de sombra si la instalación lo permite, cortinas exteriores o plantas altas en maceteros estables.</p>
<p>Si eliges <a href="/collections/parasoles">parasol</a>, ciérralo siempre con viento o cuando no estés en casa. En espacios pequeños, seguridad y proporción importan más que estética.</p>

<h2>Materiales recomendados para balcones y terrazas pequeñas</h2>
<p>El aluminio lacado y la resina son buenas opciones porque pesan poco y se limpian fácil. El HPL funciona muy bien en tableros compactos. La madera aporta calidez, pero pide más cuidado y suele pesar más. Si hay costa, piscina o mucho sol, revisa nuestra <a href="/blogs/news/que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol">guía de muebles resistentes a lluvia y sol</a> y la <a href="/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico">guía de materiales</a>.</p>

<h2>Checklist rápido antes de comprar</h2>
<ul>
  <li>¿Has medido fondo, ancho y apertura de puerta?</li>
  <li>¿El mueble entra por el acceso de casa?</li>
  <li>¿Puedes sentarte y levantarte sin mover tres piezas?</li>
  <li>¿Queda paso libre para regar, limpiar y salir?</li>
  <li>¿Las sillas se pliegan, apilan o entran bajo la mesa?</li>
  <li>¿Hay solución para sombra sin comprometer seguridad?</li>
  <li>¿Puedes guardar cojines secos o protegerlos?</li>
</ul>

<h2>Errores habituales en terrazas pequeñas</h2>
<ul>
  <li><strong>Comprar por foto, no por medidas:</strong> una escena bonita puede estar hecha en un espacio más grande.</li>
  <li><strong>Elegir demasiadas piezas pequeñas:</strong> puede crear más ruido que un conjunto sencillo.</li>
  <li><strong>Bloquear la puerta:</strong> si abrir y cerrar cuesta, dejarás de usar la terraza.</li>
  <li><strong>Olvidar el viento:</strong> textiles, parasoles y maceteros deben estar pensados para exterior real.</li>
  <li><strong>No prever almacenaje:</strong> cojines, fundas y accesorios necesitan un lugar seco.</li>
</ul>

<h2>Fuentes y criterio técnico</h2>
<p>Esta guía se ha redactado contrastando criterios de distribución de mobiliario, medidas de paso y comedor, recomendaciones editoriales para balcones pequeños y soluciones habituales de mobiliario plegable, apilable y multifunción. La recomendación se adapta a terrazas españolas reales: balcones estrechos, viento, sol, comunidad de vecinos y necesidad de limpiar sin mover toda la terraza.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Qué mesa cabe mejor en un balcón estrecho?</h3>
<p>Normalmente una mesa plegable, abatible o redonda de 60-70 cm. Si el fondo es muy justo, una mesa auxiliar o de pared puede ser más cómoda que una mesa de comedor.</p>
<h3>¿Es mejor silla plegable o apilable?</h3>
<p>La plegable es mejor si necesitas liberar espacio a diario. La apilable funciona muy bien cuando tienes algo más de fondo y quieres guardar varias sillas juntas.</p>
<h3>¿Puedo poner un sofá en una terraza pequeña?</h3>
<p>Sí, si no bloquea la puerta ni elimina el paso. En 4-6 m² suele funcionar mejor un sofá de 2 plazas o un banco perimetral que una rinconera grande.</p>
<h3>¿Qué colores hacen que una terraza pequeña parezca más amplia?</h3>
<p>Los tonos claros, neutros y materiales ligeros ayudan visualmente. También funciona repetir pocos colores y evitar demasiadas piezas decorativas en el suelo.</p>
<h3>¿Qué hago si quiero plantas pero no tengo espacio?</h3>
<p>Usa verticalidad: pared, esquina o barandilla, siempre con fijaciones estables y buen drenaje. Evita cargar una sola zona con maceteros pesados.</p>
""",
    },
    "guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada": {
        "title": "Cómo limpiar y mantener muebles de exterior por temporada",
        "summary": "Guía práctica para limpiar aluminio, resina, HPL, ratán sintético, madera, cojines y parasoles de exterior sin dañar materiales ni acabados.",
        "meta_title": "Cómo limpiar y mantener muebles de exterior",
        "meta_description": "Guía de mantenimiento de muebles de exterior: limpieza de aluminio, resina, HPL, ratán sintético, madera, cojines y parasoles por temporada.",
        "body_html": """
<p><strong>Para mantener muebles de exterior durante más tiempo, la regla base es limpiar con agua y jabón suave, aclarar bien, dejar secar al aire y adaptar el cuidado al material.</strong> Lo que más acorta la vida de una terraza no suele ser la lluvia puntual, sino la suciedad acumulada, el salitre, guardar textiles húmedos, usar productos abrasivos o dejar parasoles abiertos con viento.</p>

<h2>Mantenimiento rápido por material</h2>
<table>
  <thead>
    <tr><th>Material</th><th>Limpieza recomendada</th><th>Frecuencia orientativa</th><th>Evita</th></tr>
  </thead>
  <tbody>
    <tr><td>Aluminio lacado</td><td>Paño suave, agua y jabón neutro</td><td>Cada 1-2 meses; más en costa</td><td>Estropajos duros, golpes en el lacado</td></tr>
    <tr><td>Resina / polipropileno</td><td>Agua, jabón suave y aclarado</td><td>Cada 1-2 meses o tras uso intensivo</td><td>Disolventes, calor directo, abrasivos</td></tr>
    <tr><td>HPL</td><td>Paño húmedo y jabón neutro</td><td>Cuando haya manchas o uso de mesa</td><td>Estropajos metálicos, limpiadores muy agresivos</td></tr>
    <tr><td>Ratán sintético PE</td><td>Cepillo suave, agua jabonosa y aclarado</td><td>Cada 1-2 meses</td><td>Presión alta y suciedad entre el trenzado</td></tr>
    <tr><td>Teca y madera</td><td>Cepillo suave, agua y jabón; protector si quieres mantener color</td><td>Limpieza mensual en temporada</td><td>Lejía pura, lijado agresivo, humedad estancada</td></tr>
    <tr><td>Cojines y textiles</td><td>Manchas cuanto antes, jabón suave y secado completo</td><td>Según uso y antes de guardar</td><td>Guardarlos húmedos, secadora si la etiqueta no lo permite</td></tr>
    <tr><td>Parasoles</td><td>Tela seca, estructura limpia y funda fuera de temporada</td><td>Inicio y final de temporada</td><td>Dejarlos abiertos con viento</td></tr>
  </tbody>
</table>

<h2>Aluminio lacado: poco mantenimiento, pero limpieza regular</h2>
<p>El aluminio lacado es una de las estructuras más agradecidas para exterior porque no se oxida como el acero y pesa poco. Para mantenerlo, basta limpiar polvo, polen, salitre o restos orgánicos con agua, jabón neutro y un paño suave. En <a href="/collections/sillas-de-exterior">sillas de exterior</a>, sillones y mesas, revisa también tornillos, uniones y tapones de patas al inicio de temporada.</p>
<p>En costa conviene limpiar con más frecuencia. El salitre no convierte el aluminio en acero, pero sí ensucia uniones, tornillería y acabados. Si aparece una marca, actúa con suavidad antes de subir a productos más fuertes.</p>

<h2>Resina, polipropileno y ratán sintético: limpiar sin abrasivos</h2>
<p>La resina y el polipropileno de exterior se limpian bien con agua y jabón suave. Son materiales prácticos para <a href="/collections/tumbonas">tumbonas</a>, sillas de piscina y uso diario porque no absorben agua como una madera sin tratar. Para manchas de comida, crema solar o polvo acumulado, limpia pronto y aclara para que no queden restos.</p>
<p>El ratán sintético necesita un paso más: retirar suciedad entre el trenzado. Usa cepillo suave, no uno metálico, y evita la presión alta porque puede forzar fibras, costuras o uniones. Si el mueble combina fibra sintética y estructura metálica, seca bien las zonas de unión.</p>

<h2>HPL: el tablero fácil, si no lo rayas</h2>
<p>El HPL es muy práctico en <a href="/collections/mesas">mesas de exterior</a> porque tolera bien el uso diario, la humedad y las manchas habituales de comida. Su mantenimiento debe ser sencillo: paño húmedo, jabón neutro y aclarado. La norma general es no tratarlo como una encimera indestructible: evita cortar directamente encima, arrastrar piezas ásperas o usar estropajos metálicos.</p>
<p>Si hay una mancha persistente, actúa rápido y prueba primero en una zona discreta. Esta guía mantiene una recomendación prudente porque no todos los tableros HPL tienen el mismo acabado ni la misma clase de uso exterior.</p>

<h2>Madera y teca: decidir entre tono dorado o pátina gris</h2>
<p>La teca y otras maderas aptas para exterior pueden durar muchos años, pero no se cuidan igual que el aluminio o la resina. La teca tiene aceites naturales y envejece hacia una pátina gris plateada cuando queda expuesta al sol. Ese cambio de color puede ser normal; no significa por sí solo que el mueble esté dañado.</p>
<p>Si quieres mantener un tono más cálido, necesitarás limpieza y protector o aceite específico según indique el fabricante. Si aceptas la pátina gris, el mantenimiento baja, pero sigue siendo importante retirar suciedad, evitar humedad estancada y no cubrir madera húmeda con fundas sin ventilación. Para elegir material antes de comprar, revisa la <a href="/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico">guía de materiales para muebles de exterior</a>.</p>

<h2>Cojines, colchonetas y textiles: secar bien es media vida</h2>
<p>Los textiles de exterior resisten mejor que un tejido interior, pero no son impermeables eternos ni conviene guardarlos mojados. Para manchas comunes, limpia cuanto antes con agua y jabón suave, aclara y deja secar completamente al aire antes de guardar. En tejidos técnicos, fabricantes como Sunbrella publican instrucciones específicas por tipo de mancha y producto; por eso conviene mirar siempre la etiqueta del tejido concreto.</p>
<p>Si aparece moho, no improvises con productos fuertes directamente sobre toda la pieza. Cepilla o retira suciedad superficial, prueba cualquier solución en una zona oculta y prioriza secado completo. La humedad atrapada dentro de un arcón o bajo una funda es una de las causas más habituales de malos olores.</p>

<h2>Parasoles: la limpieza importa, pero el viento importa más</h2>
<p>Un parasol de exterior se estropea muchas veces por viento, no por falta de limpieza. Cierra siempre el parasol cuando no estés usando la terraza, con viento fuerte o si te vas de casa. Limpia la tela en seco primero para quitar polvo, usa agua jabonosa suave si hace falta y deja secar abierto antes de guardarlo en funda.</p>
<p>Revisa varillas, manivela, inclinación y base al principio de temporada. Una base insuficiente o un parasol abierto con rachas puede dañar tanto la tela como el mecanismo.</p>

<h2>Calendario de cuidado por temporada</h2>
<h3>Primavera: puesta a punto</h3>
<ul>
  <li>Limpia estructuras, tableros y asientos con jabón suave.</li>
  <li>Revisa tornillos, patas, tapones, mecanismos de parasol y fundas.</li>
  <li>Lava fundas o cojines siguiendo la etiqueta y deja secar al aire.</li>
  <li>Aplica protector a la madera si quieres conservar tono cálido.</li>
</ul>
<h3>Verano: mantenimiento ligero</h3>
<ul>
  <li>Retira polvo, polen, cloro o salitre con limpiezas cortas.</li>
  <li>Guarda cojines secos cuando no se usen varios días.</li>
  <li>Cierra parasoles con viento o al terminar el día.</li>
  <li>Limpia manchas de comida, bebida o crema solar cuanto antes.</li>
</ul>
<h3>Otoño e invierno: guardar sin humedad</h3>
<ul>
  <li>Limpia y seca antes de cubrir o almacenar.</li>
  <li>Usa fundas transpirables si los muebles quedan fuera.</li>
  <li>No guardes cojines húmedos en arcones cerrados.</li>
  <li>Eleva o separa piezas de madera si el suelo acumula agua.</li>
</ul>

<h2>Errores que conviene evitar</h2>
<ul>
  <li><strong>Usar productos abrasivos como primera opción:</strong> pueden rayar lacados, HPL, resina o fibras.</li>
  <li><strong>Guardar textiles húmedos:</strong> favorece olor, moho y manchas.</li>
  <li><strong>Cubrir muebles sucios:</strong> la suciedad queda atrapada y acelera deterioro.</li>
  <li><strong>Usar presión alta sin criterio:</strong> puede dañar trenzados, madera, costuras y juntas.</li>
  <li><strong>Dejar parasoles abiertos:</strong> una racha fuerte puede doblar varillas o romper mecanismos.</li>
</ul>

<h2>Fuentes y criterio técnico</h2>
<p>Esta guía se ha redactado contrastando recomendaciones de fabricantes de textiles de exterior, guías de cuidado de mobiliario de polietileno de alta densidad, referencias sobre teca y criterios generales de limpieza por material. La recomendación final se adapta al uso real en terrazas españolas: sol fuerte, polvo, salitre, piscina, viento y periodos largos sin uso.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Cuál es la forma más segura de limpiar muebles de exterior?</h3>
<p>Empieza siempre por agua, jabón neutro y paño o cepillo suave. Aclara bien y deja secar. Solo sube a productos específicos si el fabricante del material lo permite.</p>
<h3>¿Puedo usar hidrolimpiadora?</h3>
<p>Mejor evitar presión alta en madera, ratán sintético, textiles y costuras. En superficies duras puede usarse con mucha distancia y baja presión, pero para mantenimiento normal suele bastar una manguera y limpieza suave.</p>
<h3>¿Cada cuánto debo limpiar los muebles si vivo cerca del mar?</h3>
<p>En costa conviene limpiar con más frecuencia, especialmente tras días de viento o temporal. El objetivo es retirar salitre de uniones, patas, tornillería, textiles y tableros antes de que se acumule.</p>
<h3>¿Hay que aceitar siempre la teca?</h3>
<p>No siempre. El aceite o protector ayuda a conservar el tono dorado, pero si aceptas la pátina gris natural puedes limitarte a limpieza suave y buen secado. Sigue la indicación del fabricante de la pieza.</p>
<h3>¿Cómo guardo cojines de exterior en invierno?</h3>
<p>Guárdalos limpios y completamente secos, en interior o en una bolsa/funda transpirable. Evita arcones cerrados si los cojines conservan humedad.</p>
""",
    },
    "como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico": {
        "title": "Aluminio, resina, HPL o madera: qué material elegir para muebles de exterior",
        "summary": "Comparativa práctica de materiales para muebles de exterior: aluminio, resina, HPL, teca, acacia, ratán sintético, acero y textiles.",
        "meta_title": "Aluminio, resina, HPL o madera: qué material elegir",
        "meta_description": "Compara aluminio, resina, HPL, teca, acacia, ratán sintético y textiles para muebles de exterior: resistencia, mantenimiento y uso recomendado.",
        "body_html": """
<p><strong>Para la mayoría de terrazas en España, la combinación más equilibrada suele ser estructura de aluminio lacado, tablero HPL o resina de exterior según la pieza, y textiles preparados para intemperie.</strong> La madera aporta calidez y puede durar muchos años si es adecuada, pero exige más cuidado. El ratán sintético funciona bien cuando es fibra PE sobre estructura resistente. El material correcto depende de exposición al sol, lluvia, costa, piscina, peso y mantenimiento que estés dispuesto a hacer.</p>

<h2>Comparativa rápida de materiales de exterior</h2>
<table>
  <thead>
    <tr><th>Material</th><th>Resistencia exterior</th><th>Mantenimiento</th><th>Peso</th><th>Uso recomendado</th></tr>
  </thead>
  <tbody>
    <tr><td>Aluminio lacado</td><td>Alta: no se oxida como el acero</td><td>Bajo</td><td>Ligero</td><td>Sofás, sillas, mesas y estructuras</td></tr>
    <tr><td>Resina / polipropileno exterior</td><td>Alta si tiene protección UV</td><td>Muy bajo</td><td>Ligero</td><td>Tumbonas, sillas, piscina y uso intensivo</td></tr>
    <tr><td>HPL compacto o tablero HPL</td><td>Muy alta en tableros adecuados</td><td>Bajo</td><td>Medio</td><td>Mesas de comedor y auxiliares</td></tr>
    <tr><td>Ratán sintético PE</td><td>Alta si la fibra es de calidad</td><td>Bajo</td><td>Ligero-medio</td><td>Sofás, sillones y conjuntos lounge</td></tr>
    <tr><td>Teca</td><td>Alta por su densidad y aceites naturales</td><td>Medio</td><td>Pesado</td><td>Mesas, bancos y piezas premium</td></tr>
    <tr><td>Acacia u otras maderas</td><td>Media-alta si están tratadas</td><td>Medio-alto</td><td>Medio</td><td>Zonas cubiertas o exposición moderada</td></tr>
    <tr><td>Acero</td><td>Variable: necesita buena protección</td><td>Medio-alto</td><td>Pesado</td><td>Piezas robustas, mejor en zonas protegidas</td></tr>
    <tr><td>Textiles de exterior</td><td>Alta si son acrílicos, olefin o similares</td><td>Medio</td><td>Ligero</td><td>Cojines, colchonetas, parasoles y toldos</td></tr>
  </tbody>
</table>

<h2>Aluminio lacado: el material más fácil para empezar bien</h2>
<p>El aluminio es uno de los materiales más prácticos para muebles de exterior porque no se oxida como el acero y pesa poco. En una terraza real eso importa: puedes mover una silla, desplazar una tumbona o reorganizar un conjunto sin pelearte con el mueble. Además, el acabado lacado o pintado en polvo ayuda a proteger la superficie y mantener el color.</p>
<p>Su punto débil no es la lluvia, sino la calidad del acabado y el cuidado en ambientes salinos. En costa conviene limpiarlo con más frecuencia para retirar salitre. Para el día a día, basta agua, jabón neutro y un paño suave. Es una buena base para <a href="/collections/sillas-de-exterior">sillas de exterior</a>, <a href="/collections/sillones-de-exterior">sofás de exterior</a> y mesas.</p>

<h2>Resina y polipropileno: resistencia sencilla para piscina y uso diario</h2>
<p>La resina de exterior y el polipropileno son materiales muy agradecidos cuando buscas poco mantenimiento. No se oxidan, no absorben agua como una madera sin tratar y se limpian fácilmente. Por eso son habituales en <a href="/collections/tumbonas">tumbonas de piscina</a>, sillas apilables y accesorios.</p>
<p>La clave está en la protección UV y en el espesor/calidad de la pieza. Una resina pobre puede decolorarse o volverse quebradiza antes; una resina exterior bien formulada aguanta mucho mejor sol, cloro y limpieza frecuente. Evita productos abrasivos y fuentes de calor directo.</p>

<h2>HPL: la mejor respuesta para tableros de mesa</h2>
<p>El HPL es un laminado de alta presión fabricado con capas y resinas termoestables. En mobiliario exterior interesa especialmente para tableros de mesa porque ofrece una superficie estable, fácil de limpiar y resistente al uso diario. La norma EN 438 contempla diferentes clases de HPL, incluyendo compactos y grados para exterior, así que no todo HPL es igual: conviene que el tablero esté pensado para intemperie.</p>
<p>En una <a href="/collections/mesas">mesa de exterior</a>, el HPL es útil porque soporta platos, vasos, manchas y humedad mejor que muchos tableros decorativos convencionales. Para mantenerlo, usa paño húmedo y jabón neutro; evita estropajos duros o limpiadores agresivos que puedan marcar la superficie.</p>

<h2>Ratán sintético: estética cálida, mejor si es PE y con buena estructura</h2>
<p>El ratán natural no es la mejor opción para quedar expuesto a lluvia y sol. Lo que se suele vender como ratán de exterior normalmente es fibra sintética, a menudo polietileno (PE), trenzada sobre una estructura de aluminio o metal protegido. Esa combinación permite una estética más cálida que el metal liso con mantenimiento bajo.</p>
<p>Si eliges ratán sintético, revisa tres cosas: que la fibra sea apta para exterior, que la estructura no se oxide y que los cojines estén preparados para intemperie. La limpieza debe ser suave, retirando polvo de las zonas trenzadas para que no se acumule suciedad.</p>

<h2>Teca: muy duradera, pero no es “sin mantenimiento”</h2>
<p>La teca es una madera densa, con aceites naturales y buena estabilidad para exterior. Puede durar muchos años y envejecer hacia una pátina gris plateada. Ese cambio de color no significa necesariamente que el mueble esté fallando: es parte del envejecimiento natural de la madera expuesta.</p>
<p>La pregunta real es estética y de cuidado. Si quieres mantener el tono dorado, tendrás que limpiar y aplicar protector o aceite específico de forma periódica. Si aceptas el tono gris, el mantenimiento baja, pero sigue siendo recomendable limpiar y evitar acumulación de humedad o suciedad. Es una buena opción para quien busca calidez premium y acepta más cuidado que con aluminio o resina.</p>

<h2>Acacia y otras maderas: bonitas, pero mejor con exposición controlada</h2>
<p>La acacia y otras maderas usadas en exterior pueden funcionar bien si están tratadas, pero normalmente requieren más atención que la teca y se comportan mejor en porches, terrazas cubiertas o zonas con exposición moderada. Si quedan a pleno sol y lluvia todo el año, pueden agrietarse, perder color o necesitar aceites con más frecuencia.</p>
<p>Si quieres madera por estética pero buscas bajo mantenimiento, valora combinar estructura de aluminio con detalles de madera o elegir HPL con acabado visual cálido.</p>

<h2>Textiles de exterior: el material que más depende del cuidado</h2>
<p>Los textiles técnicos de exterior, como acrílicos teñidos en masa, olefin o tejidos similares, están diseñados para resistir mejor la decoloración y la humedad que un textil interior. Aun así, no son mágicos: el agua estancada, la suciedad acumulada y guardar cojines húmedos acortan su vida.</p>
<p>La recomendación prudente es limpiar manchas cuanto antes con agua y jabón suave, aclarar bien y dejar secar al aire. En tejidos de alto rendimiento, fabricantes especializados como Sunbrella publican instrucciones específicas para manchas y limpieza profunda; aun así, antes de usar lejía u otros productos, conviene comprobar la etiqueta del tejido concreto.</p>

<h2>Acero: robusto, pero exige protección frente al óxido</h2>
<p>El acero puede ser muy resistente estructuralmente, pero en exterior necesita una protección excelente: galvanizado, pintura en polvo o tratamientos anticorrosión. Si esa capa se raya o se deteriora, puede aparecer óxido. Por eso, para terrazas descubiertas y zonas de costa, el aluminio suele ser más cómodo.</p>
<p>El acero tiene sentido en piezas pesadas o zonas protegidas, pero no suele ser la primera recomendación si quieres mover muebles a menudo o reducir mantenimiento.</p>

<h2>Qué material elegir según tu caso</h2>
<ul>
  <li><strong>Terraza a pleno sol:</strong> aluminio lacado, HPL y textiles con protección UV.</li>
  <li><strong>Piscina:</strong> resina, aluminio y cojines de secado rápido.</li>
  <li><strong>Costa:</strong> aluminio lacado, HPL y resina, con limpieza frecuente contra salitre.</li>
  <li><strong>Porche cubierto:</strong> puedes permitirte más madera o ratán sintético decorativo.</li>
  <li><strong>Uso intensivo o alquiler turístico:</strong> resina, aluminio y HPL por limpieza y reposición sencilla.</li>
  <li><strong>Máxima calidez visual:</strong> teca o madera tratada, asumiendo mantenimiento.</li>
</ul>

<h2>Cómo combinar materiales sin equivocarte</h2>
<p>Una buena terraza no tiene que estar hecha de un solo material. Una combinación muy razonable es estructura de aluminio, tablero HPL, cojines de exterior y algún detalle cálido en madera o fibra sintética. Así ganas resistencia donde más importa y textura donde el mueble se ve y se toca.</p>
<p>Si todavía dudas entre resistencia y exposición, empieza por la guía <a href="/blogs/news/que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol">qué muebles de exterior aguantan mejor la lluvia y el sol</a> y revisa la página de <a href="/pages/mantenimiento">cuidado y mantenimiento</a>.</p>

<h2>Fuentes y criterio técnico</h2>
<p>Esta guía se ha redactado contrastando criterios de mantenimiento de textiles de exterior, referencias sobre HPL y norma EN 438, documentación sobre ratán sintético de polietileno y referencias técnicas generales sobre teca y su envejecimiento natural. La recomendación final se adapta al catálogo y al uso real en terrazas españolas.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Cuál es el material con menos mantenimiento?</h3>
<p>Para la mayoría de casos, aluminio lacado, resina exterior y HPL son los materiales más fáciles de mantener. Requieren limpieza suave y periódica, pero no aceites ni tratamientos frecuentes como algunas maderas.</p>
<h3>¿Qué material aguanta mejor cerca del mar?</h3>
<p>Aluminio lacado, resina exterior y HPL suelen funcionar muy bien en costa si se limpian con frecuencia para retirar salitre. Evita acero mal protegido y revisa tornillería y uniones.</p>
<h3>¿HPL es mejor que madera para una mesa de exterior?</h3>
<p>Depende de lo que busques. HPL suele ser más práctico y fácil de limpiar para uso diario; la madera aporta más calidez visual, pero pide más mantenimiento y acepta mejor una exposición controlada.</p>
<h3>¿Ratán natural o ratán sintético para exterior?</h3>
<p>Para exterior descubierto, es preferible ratán sintético apto para intemperie, especialmente fibra PE sobre estructura resistente. El ratán natural es más delicado frente a humedad y sol.</p>
<h3>¿Puedo dejar cojines de exterior siempre fuera?</h3>
<p>Pueden resistir mejor que textiles interiores, pero duran más si los guardas secos cuando no los uses durante varios días. Evita guardarlos húmedos y limpia manchas cuanto antes.</p>
""",
    },
    "que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol": {
        "title": "Qué muebles de exterior aguantan mejor la lluvia y el sol",
        "summary": "Guía práctica para elegir muebles de exterior resistentes a lluvia, sol, humedad, salitre y cloro.",
        "meta_title": "Qué muebles de exterior aguantan mejor lluvia y sol",
        "meta_description": "Guía para elegir muebles de exterior resistentes a lluvia y sol: aluminio, resina, HPL, madera, textiles, costa, piscina y mantenimiento.",
        "body_html": """
<p><strong>Los muebles de exterior que mejor aguantan la lluvia y el sol suelen combinar estructura de aluminio, resina de exterior, tableros HPL o madera adecuada para intemperie, siempre con textiles preparados para exterior y un mantenimiento sencillo.</strong> La clave no es solo el material: también importan el acabado, el drenaje, la ventilación, la exposición al viento y cómo se guardan cojines y parasoles cuando no se usan.</p>

<h2>Respuesta rápida: mejores materiales para lluvia y sol</h2>
<table>
  <thead>
    <tr><th>Material</th><th>Lluvia y humedad</th><th>Sol y UV</th><th>Mantenimiento</th><th>Mejor uso</th></tr>
  </thead>
  <tbody>
    <tr><td>Aluminio lacado</td><td>Muy alto: no se oxida</td><td>Alto: buen lacado conserva color</td><td>Bajo</td><td>Sofás, sillas, mesas y estructuras</td></tr>
    <tr><td>Resina exterior</td><td>Muy alto: no absorbe agua</td><td>Alto si tiene protección UV</td><td>Muy bajo</td><td>Tumbonas, sillas, accesorios y piscina</td></tr>
    <tr><td>HPL</td><td>Muy alto: tablero estable</td><td>Muy alto: no se deforma fácilmente</td><td>Bajo</td><td>Mesas de comedor y auxiliares</td></tr>
    <tr><td>Teca y maderas aptas</td><td>Alto si la madera es adecuada</td><td>Alto, con cambio natural de color</td><td>Medio</td><td>Mesas, bancos y piezas cálidas</td></tr>
    <tr><td>Acero no tratado</td><td>Bajo: puede oxidarse</td><td>Medio</td><td>Alto</td><td>Solo si está bien protegido</td></tr>
    <tr><td>Textiles de exterior</td><td>Medio-alto si secan rápido</td><td>Alto si son UV</td><td>Medio</td><td>Cojines, colchonetas y parasoles</td></tr>
  </tbody>
</table>

<h2>Aluminio: la opción más equilibrada para clima español</h2>
<p>El aluminio lacado es una de las mejores bases para muebles de exterior porque no se oxida, pesa poco y requiere muy poco mantenimiento. Funciona especialmente bien en <a href="/collections/sillas-de-exterior">sillas de exterior</a>, sofás, sillones y estructuras de mesas. Si tu terraza recibe lluvia ocasional, sol fuerte o humedad ambiental, el aluminio evita muchos problemas habituales del acero o de maderas poco adecuadas.</p>
<p>El punto importante es el acabado: un lacado de calidad protege mejor el color y la superficie. Aun así, conviene limpiar polvo, salitre o restos orgánicos con agua y jabón neutro, sobre todo en zonas de costa.</p>

<h2>Resina: práctica para piscina, tumbonas y uso intensivo</h2>
<p>La resina de exterior es muy resistente al agua y fácil de limpiar, por eso aparece tanto en <a href="/collections/tumbonas">tumbonas</a>, sillas apilables y piezas de piscina. No se oxida, no necesita aceites y puede moverse con facilidad. Para que aguante bien el sol, busca resina con protección UV y evita dejarla cerca de fuentes de calor directo.</p>
<p>En zonas con cloro, salitre o mucho polvo, basta una limpieza periódica con jabón suave. Esa sencillez la convierte en una opción muy lógica para casas de verano, alojamientos turísticos y terrazas que se usan a diario.</p>

<h2>HPL: el tablero más cómodo para mesas de exterior</h2>
<p>El HPL, o laminado de alta presión, es uno de los materiales más interesantes para <a href="/collections/mesas">mesas de exterior</a>. Resiste humedad, sol, manchas y uso diario mejor que muchos tableros convencionales. Si buscas una mesa para comer fuera todo el verano, apoyar vasos, platos, macetas o portátiles, el HPL ofrece una superficie estable y fácil de limpiar.</p>
<p>Su mantenimiento es directo: paño húmedo, jabón neutro y evitar estropajos abrasivos. Para familias, terrazas de hostelería o porches con uso frecuente, suele ser una decisión segura.</p>

<h2>Madera: bonita, duradera si es la adecuada, pero pide más cuidado</h2>
<p>No toda la madera sirve para exterior. La teca y otras maderas preparadas para intemperie pueden durar muchos años, pero cambian de tono con el sol y agradecen mantenimiento periódico. Si quieres conservar un color cálido, tendrás que aplicar aceite o tratamiento específico. Si aceptas que envejezca hacia un gris natural, el trabajo baja bastante.</p>
<p>La madera aporta una estética más cálida que el aluminio o la resina, pero no es la opción más despreocupada. Para decidir con más detalle, puedes consultar nuestra <a href="/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico">guía de materiales para muebles de exterior</a>.</p>

<h2>Textiles, cojines y parasoles: resistentes, pero no invencibles</h2>
<p>Los textiles de exterior están preparados para sol y humedad, pero duran mucho más si se guardan secos cuando no se usan durante varios días. En cojines y colchonetas, busca tejidos desenfundables o de secado rápido. En <a href="/collections/parasoles">parasoles</a>, la tela acrílica suele conservar mejor el color que el poliéster cuando recibe muchas horas de sol.</p>
<p>La regla sencilla: si hay viento fuerte, cierra el parasol; si el cojín está húmedo, no lo guardes cerrado; si viene una semana de lluvia, protege o retira textiles.</p>

<h2>Si vives cerca del mar</h2>
<p>En costa, el salitre acelera el desgaste. Prioriza aluminio lacado, resina exterior, HPL y tornillería adecuada. Limpia con más frecuencia, especialmente después de temporales o días de viento. El objetivo es retirar sal antes de que se acumule en uniones, patas y superficies.</p>

<h2>Si tienes piscina</h2>
<p>El cloro y la humedad constante hacen que la resina, el aluminio y el HPL sean opciones muy prácticas. Para tumbonas y mesas auxiliares junto a la piscina, busca materiales que no absorban agua, se limpien rápido y no se oxiden. Evita guardar textiles húmedos en arcones cerrados.</p>

<h2>Cómo alargar la vida de cualquier mueble exterior</h2>
<ul>
  <li><strong>Limpieza regular:</strong> agua, jabón neutro y paño suave.</li>
  <li><strong>Secado:</strong> no guardes cojines ni fundas húmedas.</li>
  <li><strong>Viento:</strong> cierra parasoles y asegura piezas ligeras.</li>
  <li><strong>Invierno:</strong> usa fundas transpirables o guarda textiles bajo techo.</li>
  <li><strong>Revisión:</strong> aprieta tornillos y revisa uniones al inicio de temporada.</li>
</ul>
<p>Para una pauta por material, revisa nuestra página de <a href="/pages/mantenimiento">cuidado y mantenimiento de muebles de exterior</a>.</p>

<h2>Qué elegir según tu situación</h2>
<ul>
  <li><strong>Terraza muy soleada:</strong> aluminio lacado, HPL y textiles con protección UV.</li>
  <li><strong>Jardín con lluvia frecuente:</strong> aluminio, resina y HPL.</li>
  <li><strong>Piscina:</strong> resina, aluminio y textiles de secado rápido.</li>
  <li><strong>Costa:</strong> aluminio lacado, resina y limpieza regular contra salitre.</li>
  <li><strong>Máxima calidez estética:</strong> madera apta para exterior, asumiendo mantenimiento.</li>
</ul>

<h2>Preguntas frecuentes</h2>
<h3>¿Puedo dejar los muebles de exterior siempre fuera?</h3>
<p>Sí, si son de materiales preparados para intemperie como aluminio lacado, resina, HPL o madera adecuada. Aun así, conviene proteger textiles, cerrar parasoles y usar fundas transpirables en periodos largos sin uso.</p>
<h3>¿Qué material se oxida menos en exterior?</h3>
<p>El aluminio no se oxida como el acero, por eso es una de las opciones más seguras para exterior. La resina y el HPL tampoco se oxidan porque no son metales.</p>
<h3>¿Qué muebles aguantan mejor el sol fuerte?</h3>
<p>El aluminio lacado, el HPL, la resina con protección UV y los textiles acrílicos o específicos de exterior suelen aguantar muy bien el sol. La madera puede resistir, pero cambia de color con el tiempo.</p>
<h3>¿Qué hago si mis muebles están cerca de una piscina?</h3>
<p>Limpia restos de cloro con agua y jabón suave, elige materiales que no absorban humedad y guarda los cojines secos. Resina, aluminio y HPL son especialmente prácticos en zonas de piscina.</p>
<h3>¿Necesito fundas para muebles de exterior?</h3>
<p>No siempre, pero ayudan mucho si el mueble va a estar semanas sin uso. Lo ideal es usar fundas transpirables y cubrir siempre los muebles limpios y secos.</p>
""",
    }
}


def request(method, path, payload=None, attempts=3):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        },
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:800]
            raise RuntimeError(f"HTTP {exc.code} {method} {path}: {detail}") from exc
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)


def get_blog_id():
    data = request("GET", f"blogs.json?handle={urllib.parse.quote(BLOG_HANDLE)}")
    blogs = data.get("blogs", [])
    if not blogs:
        raise RuntimeError(f"No encuentro blog handle={BLOG_HANDLE}")
    return blogs[0]["id"]


def get_article(blog_id, handle):
    data = request("GET", f"blogs/{blog_id}/articles.json?handle={urllib.parse.quote(handle)}")
    articles = data.get("articles", [])
    return articles[0] if articles else None


def text_words(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())


def main():
    if not SHOPIFY_ACCESS_TOKEN:
        sys.exit("SHOPIFY_ACCESS_TOKEN vacío")

    blog_id = get_blog_id()
    backup = {}
    errors = 0
    print(f"{'MODO APLICAR' if APPLY else 'DRY-RUN (no escribe)'} - {len(GUIDES)} guías GEO en blog {BLOG_HANDLE}\n")

    for handle, guide in GUIDES.items():
        try:
            current = get_article(blog_id, handle)
        except Exception as exc:
            print(f"✗ {handle}: error leyendo ({exc})")
            errors += 1
            continue

        backup[handle] = current
        action = "update" if current else "create"
        print(f"• {handle}: {action}")
        print(f"  title: {guide['title']}")
        print(f"  words: {text_words(current.get('body_html') if current else '')}->{text_words(guide['body_html'])}")
        print(f"  meta: {guide['meta_description']}")

        if not APPLY:
            continue

        article = {
            "title": guide["title"],
            "handle": handle,
            "author": AUTHOR,
            "body_html": guide["body_html"].strip(),
            "summary_html": f"<p>{guide['summary']}</p>",
            "published": True,
            "tags": "GEO, guía de compra, mantenimiento, materiales",
            "metafields": [
                {
                    "namespace": "global",
                    "key": "title_tag",
                    "value": guide["meta_title"],
                    "type": "single_line_text_field",
                },
                {
                    "namespace": "global",
                    "key": "description_tag",
                    "value": guide["meta_description"],
                    "type": "single_line_text_field",
                },
            ],
        }
        try:
            if current:
                article["id"] = current["id"]
                request("PUT", f"blogs/{blog_id}/articles/{current['id']}.json", {"article": article})
            else:
                request("POST", f"blogs/{blog_id}/articles.json", {"article": article})
        except Exception as exc:
            print(f"  ⚠️ {exc}")
            errors += 1

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(ROOT, "content", "descriptions", f"backup_geo_guides_{ts}.json")
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=2)

    print(f"\nBackup -> {backup_path}")
    print(f"{'Aplicado' if APPLY else 'Dry-run'} · errores: {errors}")


if __name__ == "__main__":
    main()
