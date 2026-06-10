#!/usr/bin/env python3
"""
Reescribe en profundidad el CUERPO de los 5 posts (el de materiales ya está ampliado).
Texto experto, citable, con tablas, listas, enlaces internos y FAQ. Tono Santavila
(sereno, experto, preciso; sin promesas no verificadas). Backup + DRY-RUN salvo --apply.
"""
import json, os, sys, re, datetime, urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
GQL = f"https://{SHOP}/admin/api/2026-01/graphql.json"

def gql(q):
    req = urllib.request.Request(GQL, data=json.dumps({"query": q}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    return json.load(urllib.request.urlopen(req, timeout=40))

def rest(method, path, payload=None):
    url = f"https://{SHOP}/admin/api/2026-01/{path}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:400]}"); raise

# ───────────────────────── CUERPOS ─────────────────────────

MANTENIMIENTO = """<p><strong>Mantener los muebles de exterior es sencillo si adaptas el cuidado a cada material y sigues el ritmo de las estaciones: limpieza regular con agua y jabón neutro, protección frente al sol y la humedad, y un buen almacenaje en los meses fríos.</strong> El aluminio y los sintéticos apenas piden trabajo; la madera y los cojines necesitan algo más de atención. Esta guía resume qué hacer con cada material y cómo preparar tu mobiliario para cada temporada para que dure muchos más años.</p>

<h2>Mantenimiento por material (lo esencial)</h2>
<table>
  <thead><tr><th>Material</th><th>Limpieza</th><th>Frecuencia</th><th>Evita</th></tr></thead>
  <tbody>
    <tr><td>Aluminio lacado</td><td>Agua tibia + jabón neutro, paño suave</td><td>Cada 1-2 meses</td><td>Estropajos metálicos, abrasivos</td></tr>
    <tr><td>Resina / polipropileno</td><td>Agua y jabón; manchas con bicarbonato</td><td>Cada 1-2 meses</td><td>Disolventes agresivos</td></tr>
    <tr><td>Ratán sintético (PE)</td><td>Cepillo suave + agua jabonosa; aclarar</td><td>Cada 1-2 meses</td><td>Hidrolimpiadora a presión alta</td></tr>
    <tr><td>Teca / madera</td><td>Agua y jabón; aceite de teca si quieres tono dorado</td><td>Limpieza mensual · aceite 1-2/año</td><td>Lejía pura, lijado agresivo</td></tr>
    <tr><td>Textilene / cuerda</td><td>Agua jabonosa, secar al aire</td><td>Según uso</td><td>Secadora, plancha</td></tr>
    <tr><td>Cojines (acrílico/olefin)</td><td>Agua y jabón; manchas con lejía diluida al 10%</td><td>Según uso</td><td>Guardarlos húmedos</td></tr>
  </tbody>
</table>

<h2>¿Cómo se limpia el aluminio de exterior?</h2>
<p>Basta agua tibia con jabón neutro y un paño suave. Evita los limpiadores abrasivos y los estropajos metálicos, que rayan el lacado. Aprovecha para revisar uniones y tornillería y apretar lo que esté flojo, y comprueba los tapones de plástico de las patas: protegen el suelo y evitan desgaste. El aluminio lacado no se oxida, así que su mantenimiento es mínimo.</p>

<h2>¿Cómo cuidar la madera y la teca en el exterior?</h2>
<p>La teca puede seguir dos caminos. Si te gusta su <strong>tono dorado original</strong>, una vez al año lija suavemente con grano fino (120) y aplica una mano de aceite de teca. Si prefieres la <strong>pátina gris plateada</strong> natural —igual de protectora—, basta con limpiarla con agua y jabón. En ambos casos, evita la lejía pura y el lijado agresivo. La madera de acacia se cuida igual, con aceite específico al inicio y al final de temporada.</p>

<h2>¿Cómo lavo los cojines y tejidos de exterior?</h2>
<p>Los tejidos técnicos (acrílico teñido en masa, olefin, textilene) admiten agua y jabón. Para manchas resistentes, una solución de <strong>lejía diluida al 10%</strong> suele funcionar sin dañar el color en acrílicos de calidad (prueba antes en una zona oculta). La regla de oro: <strong>deja secar siempre completamente al aire</strong> antes de guardarlos o de volver a colocarlos, porque la humedad atrapada es la causa nº1 de moho y malos olores. Revisa cremalleras y costuras al inicio de temporada.</p>

<h2>Calendario de mantenimiento por temporada</h2>
<h3>Primavera — puesta a punto</h3>
<ul>
  <li>Limpieza general de estructuras según material (tabla de arriba).</li>
  <li>Lavado de cojines y fundas; secado completo al aire.</li>
  <li>Revisión de tornillería, mecanismos de parasol y tapones de patas.</li>
  <li>Aceitado de la teca si quieres recuperar el tono dorado.</li>
</ul>
<h3>Verano — uso y prevención</h3>
<ul>
  <li>Cierra los parasoles con viento fuerte para no dañar varillas ni tela.</li>
  <li>Guarda los cojines bajo techo cuando no se usen o en días de lluvia.</li>
  <li>Un repaso rápido con paño húmedo evita que el polvo y el polen se incrusten.</li>
</ul>
<h3>Otoño-invierno — almacenaje correcto</h3>
<ul>
  <li>Limpia todo <strong>antes</strong> de guardar: la suciedad y la humedad aceleran el deterioro.</li>
  <li>Cojines en bolsas de almacenaje o en interior.</li>
  <li>Apila las sillas y cúbrelas con <a href="/collections/accesorios">fundas de exterior transpirables</a>, bien sujetas contra el viento.</li>
  <li>Guarda los parasoles desmontados y en su funda.</li>
</ul>
<p><strong>Consejo:</strong> el aluminio y los sintéticos pueden quedarse fuera todo el año; solo protégelos de las heladas si vives en zonas de interior con temperaturas muy bajas. La madera y los cojines agradecen resguardo.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Puedo dejar los muebles de exterior fuera todo el invierno?</h3>
<p>El aluminio lacado y los sintéticos (resina, ratán PE) aguantan bien la intemperie todo el año. Conviene usar fundas y, en zonas de heladas fuertes, resguardar la madera y guardar siempre los cojines en seco.</p>
<h3>¿Cada cuánto hay que aplicar aceite de teca?</h3>
<p>Una o dos veces al año si quieres mantener el tono dorado. Si dejas que la teca envejezca a gris plateado, no necesita aceite: solo limpieza con agua y jabón.</p>
<h3>¿Cómo quito el moho de los cojines de exterior?</h3>
<p>Cepilla en seco, lava con agua jabonosa y, si persiste, usa lejía diluida al 10% en tejidos acrílicos. Lo más importante es secarlos por completo al aire y guardarlos siempre secos.</p>
<h3>¿Se puede usar hidrolimpiadora?</h3>
<p>Con cuidado y a baja presión en aluminio o resina. En ratán sintético y tejidos evita la presión alta, porque puede deshilachar la fibra o dañar las costuras.</p>"""

IDEAS = """<p><strong>Para decorar una terraza con criterio, elige primero un estilo (mediterráneo, lounge, minimalista, familiar o de hostelería), define una paleta de 2-3 colores y trabaja capas: muebles, textiles, plantas e iluminación.</strong> Una terraza es una habitación más: merece la misma intención que el salón. Aquí tienes cinco estilos que funcionan, con su paleta, materiales y piezas clave para que copies el que encaje con tu espacio.</p>

<h2>1. Mediterráneo clásico: blanco, fibras y plantas</h2>
<p>El estilo más atemporal para el clima español. Parte de muebles con <strong>estructura de aluminio blanco</strong> y tapizados en crudo o beige, y súmale textura natural: cojines de algodón, una mesa de madera o teca y mucha planta. Las macetas de terracota con aromáticas (lavanda, romero, buganvilla) y los tejidos de rayas cierran el conjunto.</p>
<ul>
  <li><strong>Paleta:</strong> blanco, crudo, terracota, verde planta.</li>
  <li><strong>Piezas:</strong> <a href="/collections/sillones-de-exterior">sofá o sillones</a> claros + mesa de centro de madera.</li>
  <li><strong>Encaja en:</strong> terrazas y porches con luz, casas de costa.</li>
</ul>

<h2>2. Lounge contemporáneo: tonos oscuros y formas bajas</h2>
<p>Para crear ambiente de "chill out". Los sofás y chaise longues de <strong>ratán sintético en grafito o antracita</strong> aportan sofisticación; combínalos con una mesa de centro baja, iluminación cálida indirecta y cojines en tonos tierra (terracota, arena, marrón chocolate). Menos piezas, más confort.</p>
<ul>
  <li><strong>Paleta:</strong> antracita, grafito, tierra, dorado tenue.</li>
  <li><strong>Piezas:</strong> <a href="/collections/sillones-de-exterior">conjunto lounge</a> + <a href="/collections/parasoles">parasol</a> para sombra.</li>
  <li><strong>Encaja en:</strong> áticos, terrazas amplias, zonas de noche.</li>
</ul>

<h2>3. Minimalista escandinavo: geometría limpia y madera</h2>
<p>Líneas rectas, poca pieza y mucho aire. Mesas y sillas de <strong>aluminio en gris claro o blanco mate</strong>, combinadas con tableros o detalles de teca o acacia. La clave es la contención: pocos elementos, bien elegidos, y una paleta casi monocroma con la madera como único acento cálido.</p>
<ul>
  <li><strong>Paleta:</strong> blanco, gris claro, madera natural.</li>
  <li><strong>Piezas:</strong> <a href="/collections/mesas">mesa de líneas rectas</a> + <a href="/collections/sillas-de-exterior">sillas ligeras</a>.</li>
  <li><strong>Encaja en:</strong> terrazas urbanas, espacios pequeños.</li>
</ul>

<h2>4. Funcional para hostelería y uso intensivo</h2>
<p>Cuando el mobiliario trabaja muchas horas, priman <strong>apilabilidad, resistencia y limpieza fácil</strong>. Las sillas de aluminio con asiento de textilene o polipropileno son la solución: ligeras, no se oxidan y aguantan el uso continuo. Mesas con tablero HPL para resistir arañazos y agua. Si tienes un bar o restaurante, te interesa nuestra guía específica de <a href="/blogs/news/muebles-de-exterior-para-hosteleria-que-buscar-y-por-que-la-calidad-marca-la-diferencia">muebles de exterior para hostelería</a>.</p>

<h2>5. Jardín familiar: comer, jugar y relajarse</h2>
<p>El reto es combinar zonas. Una <strong>mesa grande, idealmente extensible</strong>, para las comidas; sillas apilables para cuando hay invitados; y un rincón lounge para el relax. Añade sombra con un <a href="/collections/parasoles">parasol</a> de pie o una pérgola, y materiales que aguanten el trajín diario (aluminio, resina, HPL).</p>

<h2>¿Cómo elijo mi estilo?</h2>
<p>Mira primero la <strong>luz y el tamaño</strong> de tu espacio: los tonos claros y las piezas ligeras agrandan las terrazas pequeñas; los tonos oscuros y las formas bajas dan recogimiento a las amplias. Después elige una paleta de 2-3 colores y repítela en muebles, cojines y maceteros. La coherencia es lo que hace que una terraza parezca "decorada" y no improvisada.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Qué colores agrandan una terraza pequeña?</h3>
<p>Los claros y neutros (blanco, beige, gris claro) amplían visualmente, sobre todo combinados con muebles de líneas finas y patas a la vista. Reserva los tonos oscuros para terrazas amplias.</p>
<h3>¿Qué plantas funcionan mejor en una terraza al sol?</h3>
<p>Aromáticas mediterráneas (lavanda, romero), buganvilla, olivo en maceta y suculentas: resisten el sol y necesitan poco riego, ideales para el clima español.</p>
<h3>¿Cómo creo una zona chill out sin obras?</h3>
<p>Con un conjunto lounge bajo, una alfombra de exterior, iluminación cálida inalámbrica y un parasol o vela de sombra. No necesitas instalación eléctrica si usas lámparas recargables.</p>"""

HOSTELERIA = """<p><strong>El mejor mobiliario de exterior para hostelería combina estructura de aluminio con recubrimiento en polvo, sillas apilables, tapizados técnicos (textilene o acrílico) y tableros resistentes como HPL o compacto.</strong> En un bar o restaurante el mueble trabaja más que en ninguna casa: muchas horas de uso, exposición continua y clientes de todo tipo. Elegir barato sale caro en reposiciones, imagen y reseñas. Esto es lo que de verdad importa al comprar.</p>

<h2>Durabilidad: aluminio con recubrimiento en polvo</h2>
<p>El estándar de la hostelería de calidad es el <strong>aluminio lacado al horno (recubrimiento en polvo electrostático)</strong>: no se oxida, no hay que repintarlo y mantiene el color durante años. Fíjate en <strong>perfiles de grosor suficiente</strong> y soldaduras reforzadas en los puntos de carga (uniones de patas y respaldo), que son los que primero fallan con el uso intensivo.</p>

<h2>Apilabilidad: logística diaria</h2>
<p>Abrir y cerrar terraza cada día exige sillas que se apilen sin dañarse y ocupen poco. Una buena silla apilable permite agrupar varias unidades de forma estable, agiliza la limpieza del suelo y libera espacio de almacén. Es un detalle que se nota cada jornada.</p>

<h2>Tapizados técnicos: textilene y acrílico</h2>
<p>Para uso profesional, el tejido debe ser <strong>resistente a los rayos UV, lavable, de secado rápido y difícil de rasgar</strong>. Los dos más usados:</p>
<ul>
  <li><strong>Textilene</strong> (malla de fibra recubierta): transpirable, secado casi inmediato, muy fácil de limpiar. Perfecto para sillas de uso continuo.</li>
  <li><strong>Acrílico teñido en masa</strong> (tipo Sunbrella): mayor confort y excelente resistencia al color bajo el sol, ideal para cojines de zona lounge.</li>
</ul>

<h2>Tableros de mesa: qué aguanta el uso intensivo</h2>
<table>
  <thead><tr><th>Tablero</th><th>Resistencia</th><th>Notas</th></tr></thead>
  <tbody>
    <tr><td>HPL / compacto</td><td>Muy alta (sol, agua, arañazos, calor)</td><td>El más recomendado para terrazas; no se decolora</td></tr>
    <tr><td>Aluminio</td><td>Alta</td><td>Ligero y sin óxido; acabados variados</td></tr>
    <tr><td>Porcelánico / Dekton</td><td>Muy alta</td><td>Premium, muy resistente; más peso</td></tr>
    <tr><td>Cristal templado</td><td>Media</td><td>Estético pero pide más cuidado y limpieza</td></tr>
  </tbody>
</table>

<h2>Peso y normativa de veladores</h2>
<p>Consulta siempre la <strong>ordenanza municipal de terrazas y veladores</strong>: muchos ayuntamientos regulan dimensiones, colores, peso y tipo de mobiliario, e incluso exigen apilado o retirada a determinada hora. El aluminio, por su ligereza, suele ser la opción más práctica para montar y desmontar a diario.</p>

<h2>Coste total, no solo precio</h2>
<p>Una silla más cara que dura cinco temporadas sale más barata que una económica que se repone cada año, sin contar el coste de imagen de una terraza con muebles desgastados. Valora la <strong>disponibilidad de recambios</strong> (cojines, fundas, tapas de patas) y la facilidad de reposición de unidades sueltas para mantener el conjunto uniforme.</p>

<h2>Checklist rápido de compra para hostelería</h2>
<ul>
  <li>Estructura de aluminio con recubrimiento en polvo.</li>
  <li>Sillas apilables y ligeras.</li>
  <li>Tapizado textilene/acrílico, lavable y de secado rápido.</li>
  <li>Tablero HPL, compacto o porcelánico.</li>
  <li>Recambios disponibles y posibilidad de reponer unidades.</li>
  <li>Cumple la normativa de veladores de tu municipio.</li>
</ul>
<p>Explora opciones aptas para uso profesional en nuestras colecciones de <a href="/collections/sillas-de-exterior">sillas</a> y <a href="/collections/mesas">mesas de exterior</a>.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Qué material es mejor para una terraza de bar?</h3>
<p>Aluminio con recubrimiento en polvo para la estructura, tapizado textilene o acrílico, y tablero HPL o compacto. Es la combinación que mejor aguanta el uso intensivo, el sol y la lluvia con un mantenimiento mínimo.</p>
<h3>¿Las sillas apilables aguantan el uso profesional?</h3>
<p>Sí, si son de aluminio de calidad con soldaduras reforzadas. La apilabilidad además facilita la limpieza diaria y el almacenaje, claves en hostelería.</p>
<h3>¿Cómo mantengo el mobiliario de una terraza comercial?</h3>
<p>Limpieza frecuente con agua y jabón neutro, secado de tapizados, revisión periódica de tornillería y uso de fundas fuera de servicio. Tener recambios evita que una pieza dañada rompa la uniformidad del conjunto.</p>"""

TENDENCIAS = """<p><strong>Las tendencias en muebles de exterior para 2026 giran en torno a cuatro ejes: colores tierra y verdes naturales, formas orgánicas y curvas, materiales sostenibles, y la integración total entre interior y exterior.</strong> El mueble de jardín ha dejado de ser "de jardín": hoy se busca que tenga la misma calidad, confort y estética que el de dentro. Repasamos lo que marca el año y, sobre todo, cómo aplicarlo sin que tu terraza pase de moda en una temporada.</p>

<h2>Color: del neutro al verde salvia y los tonos tierra</h2>
<p>El blanco y el gris siguen siendo base por su versatilidad, pero ganan protagonismo el <strong>verde salvia, el terracota y el beige cálido</strong>. Son colores que conectan con la naturaleza, envejecen bien visualmente y combinan con plantas y materiales naturales. La fórmula segura: una base neutra en los muebles y el color a través de cojines y textiles, más fáciles de renovar.</p>

<h2>Formas orgánicas y líneas suaves</h2>
<p>El diseño recto y muy geométrico deja paso a <strong>curvas y formas redondeadas</strong> en sillas, sofás y mesas. Suavizan el espacio, resultan más acogedoras y se integran mejor con la vegetación. Es una tendencia estética, pero también de confort: los respaldos envolventes sientan mejor.</p>

<h2>Sostenibilidad y materiales con historia</h2>
<p>El origen del material importa cada vez más. Crecen el <strong>aluminio reciclado</strong>, los <strong>tejidos hechos con plástico recuperado</strong> y la <strong>madera de teca con certificación FSC</strong>. Más allá de la moda, son decisiones que alargan la vida del producto y reducen su impacto, algo que valoran tanto el cliente residencial como los proyectos de hostelería.</p>

<h2>Integración interior-exterior</h2>
<p>Salón y terraza se funden: misma paleta, materiales afines y la misma altura y confort de asiento. El sofá de exterior ya no "parece de exterior"; tiene el aspecto y la comodidad del de interior, con la diferencia de que sus tejidos y estructuras están preparados para el sol y la lluvia. Es la tendencia de fondo que explica casi todas las demás.</p>

<h2>Modularidad y espacios flexibles</h2>
<p>Los <strong>conjuntos modulares</strong> ganan terreno porque se adaptan: hoy un rincón en L, mañana dos sofás separados. Permiten aprovechar mejor terrazas de cualquier tamaño y reconfigurar el espacio según el momento (comida, relax, reunión).</p>

<h2>Iluminación y pequeños extras</h2>
<p>Mesas con <strong>iluminación LED solar</strong> integrada, lámparas recargables sin cables y detalles como carga USB en sofás aparecen cada vez más en interiorismo exterior. Aportan ambiente nocturno sin obras ni instalación eléctrica.</p>

<h2>Cómo seguir la tendencia sin pasarte</h2>
<p>La clave es separar lo <strong>duradero</strong> de lo <strong>renovable</strong>. Invierte en muebles de estructura neutra y calidad (aluminio, ratán sintético, teca) que durarán años, y deja que la tendencia entre por lo barato de cambiar: cojines, textiles, maceteros e iluminación. Así actualizas el look cada temporada sin rehacer la terraza entera.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Qué colores se llevan en muebles de exterior en 2026?</h3>
<p>Verde salvia, terracota y beige cálido como protagonistas, sobre una base de neutros (blanco, gris, arena). Lo más práctico es aplicar el color de tendencia en cojines y textiles, no en el mueble.</p>
<h3>¿Merece la pena el mueble de exterior "estilo interior"?</h3>
<p>Sí, si sus materiales están preparados para la intemperie (aluminio, tejidos de exterior, tableros HPL). Ganas confort y estética sin renunciar a la resistencia.</p>
<h3>¿Qué es un conjunto modular y para quién es?</h3>
<p>Un set de piezas que se recolocan a voluntad (esquinas, sofás sueltos, pufs). Es ideal si quieres flexibilidad o si tu terraza cambia de uso a lo largo del día.</p>"""

TERRAZA = """<p><strong>Para aprovechar una terraza pequeña, elige muebles a escala (mesas de 60 cm, sillas ligeras), prioriza piezas plegables, apilables o multifunción, coloca todo en el perímetro dejando el centro libre, y usa colores claros y patas finas para ganar amplitud visual.</strong> Aunque tengas 4 o 6 m², con la distribución adecuada puedes crear un rincón perfecto para desayunar, leer o tomar algo al atardecer. Estos son los principios que mejor funcionan.</p>

<h2>Mide y elige muebles a escala</h2>
<p>El error más común es meter muebles demasiado grandes. Antes de comprar, mide y deja paso de circulación. Como referencia:</p>
<table>
  <thead><tr><th>Espacio</th><th>Propuesta que funciona</th></tr></thead>
  <tbody>
    <tr><td>Balcón (3-4 m²)</td><td>Mesa auxiliar o bistró Ø50-60 cm + 2 sillas ligeras o plegables</td></tr>
    <tr><td>Terraza pequeña (5-8 m²)</td><td>Mesa 60×60 / 70×70 cm + 2-4 sillas, o un sofá de 2 plazas compacto</td></tr>
    <tr><td>Rincón estrecho</td><td>Banco o sofá esquinero + mesa de centro pequeña</td></tr>
  </tbody>
</table>
<p>El <a href="/collections/mesas">aluminio</a> es especialmente útil aquí por su ligereza: mueves o guardas las piezas en segundos.</p>

<h2>Plegables, apilables y multifunción: tus aliados</h2>
<p>Las <strong>sillas y mesas plegables</strong> dan capacidad extra cuando hay visita y se guardan cuando no. Las <strong>apilables</strong> liberan suelo en un gesto. Y los muebles <strong>multifunción</strong> (un baúl que hace de banco y guarda cojines, mesas nido que se separan) son oro en pocos metros. Elige modelos que se vean bien incluso plegados.</p>

<h2>Distribución: el perímetro es tu amigo</h2>
<p>Coloca los muebles pegados a la pared o la barandilla y deja el <strong>centro libre</strong>: amplía visualmente y facilita el paso. Un <a href="/collections/sillones-de-exterior">sofá o banco esquinero</a> rescata el rincón más desaprovechado y ofrece mucho asiento ocupando poco. Evita "islas" en mitad de la terraza.</p>

<h2>Trucos visuales para ganar amplitud</h2>
<ul>
  <li><strong>Colores claros:</strong> blanco, beige y gris claro agrandan; reserva el oscuro para un solo acento.</li>
  <li><strong>Patas finas y a la vista:</strong> los muebles que "respiran" ocupan menos espacio visual que los de base maciza.</li>
  <li><strong>Vertical, no horizontal:</strong> jardineras de pared, estanterías y plantas colgantes añaden vida sin robar suelo.</li>
  <li><strong>Un espejo de exterior:</strong> duplica la sensación de luz y profundidad.</li>
  <li><strong>Suelo continuo:</strong> un mismo pavimento o losetas tipo deck unifican y estiran el espacio.</li>
</ul>

<h2>Sombra e iluminación sin obras</h2>
<p>Para el sol, un <a href="/collections/parasoles">parasol</a> de tamaño contenido (o de pared/voladizo) o una vela de sombra resuelven sin ocupar suelo. Para la noche, una tira LED en el perímetro o una lámpara recargable sin cables alargan las tardes sin necesidad de instalación eléctrica. La luz cálida e indirecta hace que un espacio pequeño se sienta acogedor.</p>

<h2>Plantas: verde sin estorbar</h2>
<p>Apuesta por <strong>jardineras estrechas</strong>, macetas colgantes y plantas en altura. Las aromáticas mediterráneas y las trepadoras en celosía aportan intimidad y frescor sin comerse el suelo útil.</p>

<h2>Preguntas frecuentes</h2>
<h3>¿Qué muebles caben en una terraza de 4 m²?</h3>
<p>Una mesa bistró de Ø50-60 cm con dos sillas ligeras o plegables, o un banco estrecho con una mesa auxiliar. Prioriza piezas que se plieguen o se muevan con facilidad.</p>
<h3>¿Mejor mesa redonda o cuadrada en poco espacio?</h3>
<p>La redonda facilita el paso al no tener esquinas y suele encajar mejor en rincones; la cuadrada se arrima a la pared y aprovecha bien los balcones estrechos. Depende de la forma de tu terraza.</p>
<h3>¿Cómo gano sensación de amplitud?</h3>
<p>Colores claros, muebles de patas finas pegados al perímetro, decoración vertical y, si puedes, un espejo de exterior y un suelo continuo. Mantener el centro despejado es lo que más se nota.</p>"""

POSTS = {
 "guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada": MANTENIMIENTO,
 "5-ideas-para-decorar-tu-terraza-este-verano-del-estilo-mediterraneo-al-diseno-minimalista": IDEAS,
 "muebles-de-exterior-para-hosteleria-que-buscar-y-por-que-la-calidad-marca-la-diferencia": HOSTELERIA,
 "tendencias-en-muebles-de-exterior-para-2025-materiales-colores-y-disenos-que-marcan-el-ano": TENDENCIAS,
 "como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales": TERRAZA,
}

def num(g): return g.split("/")[-1]
data = gql("{ blogs(first:5){ nodes{ id handle articles(first:50){ nodes{ id handle body } } } } }")
idx = {}
for b in data["data"]["blogs"]["nodes"]:
    for a in b["articles"]["nodes"]:
        idx[a["handle"]] = (num(b["id"]), num(a["id"]), a["body"])

backup = {}
print(f"{'APLICAR' if APPLY else 'DRY-RUN'} — {len(POSTS)} cuerpos\n")
for handle, body in POSTS.items():
    if handle not in idx:
        print(f"✗ {handle}: no encontrado"); continue
    blog_id, art_id, cur = idx[handle]
    backup[handle] = {"article_id": art_id, "body": cur}
    wo = len(re.sub(r"<[^>]+>", " ", cur or "").split())
    wn = len(re.sub(r"<[^>]+>", " ", body).split())
    print(f"• {handle[:45]:<45} {wo}→{wn}p")
    if APPLY:
        rest("PUT", f"blogs/{blog_id}/articles/{art_id}.json", {"article": {"id": int(art_id), "body_html": body}})

bdir = os.path.join(ROOT, "content", "descriptions"); os.makedirs(bdir, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
json.dump(backup, open(os.path.join(bdir, f"backup_blog_bodies_{ts}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n💾 Backup ({ts})")
print("✅ Aplicado" if APPLY else "ℹ️ Dry-run. --apply para escribir.")
