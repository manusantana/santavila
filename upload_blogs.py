"""
Sube 6 artículos de blog a la tienda Shopify de Muebles Exterior.
Blog destino: News (id: 119723065668)
"""
import json
import urllib.request
import urllib.error
from config import SHOPIFY_ACCESS_TOKEN

SHOP = "mueblesexterior.myshopify.com"
BLOG_ID = 119723065668
API_VERSION = "2026-01"
BASE_URL = f"https://{SHOP}/admin/api/{API_VERSION}/blogs/{BLOG_ID}/articles.json"

ARTICLES = [
    {
        "title": "Cómo elegir muebles de exterior que duren: aluminio, teca o ratán sintético",
        "summary_html": "Guía completa para elegir el material más adecuado para tu terraza o jardín: aluminio, teca y ratán sintético, ventajas de cada uno y cuándo elegir cada opción.",
        "body_html": """
<h2>Invertir en mobiliario de exterior es una decisión a largo plazo</h2>
<p>Elegir el material equivocado puede suponer cambiar los muebles en dos o tres temporadas; el correcto puede durar décadas sin apenas mantenimiento. En esta guía te explicamos las diferencias entre los tres materiales más usados en terrazas y jardines.</p>

<h2>El aluminio: ligereza y resistencia sin compromiso</h2>
<p>El aluminio es el material rey del mueble de exterior moderno. Su resistencia a la corrosión lo hace ideal para climas costeros o húmedos, y su bajo peso facilita reorganizar el espacio sin esfuerzo. Los perfiles de aluminio de alta calidad —lacados en polvo— mantienen el color temporada tras temporada sin oxidarse ni desconcharse. Es también el material más empleado en hostelería por su durabilidad y facilidad de limpieza.</p>

<h2>La teca: calidez natural con personalidad propia</h2>
<p>La madera de teca es uno de los materiales más valorados en jardinería de lujo. Su alto contenido en aceites naturales la hace resistente al agua y a los insectos sin necesidad de tratamientos constantes. Con el tiempo adquiere un tono plateado muy apreciado en el diseño contemporáneo. Su mantenimiento es mínimo: un lijado superficial anual y, si se desea recuperar el tono original, una mano de aceite de teca.</p>

<h2>El ratán sintético: comodidad y estética mediterránea</h2>
<p>El ratán sintético (o PE ratán) imita la apariencia del mimbre natural con una durabilidad muy superior. No se deforma ni decolora con el sol, soporta la lluvia sin absorberse y es muy fácil de limpiar. Es el material favorito para ambientes lounges, terrazas de hotel y zonas de relax al aire libre.</p>

<h2>¿Cuál elegir?</h2>
<ul>
  <li><strong>Clima húmedo o costero:</strong> aluminio.</li>
  <li><strong>Estética cálida y natural:</strong> teca.</li>
  <li><strong>Zona lounge o chill-out:</strong> ratán sintético.</li>
</ul>
<p>Lo ideal para la mayoría de terrazas y jardines es combinar dos de ellos: estructura de aluminio con tapizado o textilene, o mesa de teca con sillas de aluminio.</p>
""",
        "tags": "guía de compra, aluminio, teca, ratán sintético, materiales exterior",
    },
    {
        "title": "Guía de mantenimiento de muebles de exterior: cómo prepararlos para cada temporada",
        "summary_html": "Todo lo que necesitas saber para preparar tus muebles de exterior en primavera y guardarlos correctamente en otoño.",
        "body_html": """
<h2>Preparación de primavera: bienvenida a la temporada</h2>

<h3>Aluminio y estructura metálica</h3>
<p>Limpia con agua tibia y jabón neutro. Evita los limpiadores abrasivos o los estropajos metálicos. Comprueba las uniones y tornillos; si los hay, apriétalos. Revisa los tapones de plástico de las patas —protegen el suelo y evitan el desgaste.</p>

<h3>Cojines y tapizados</h3>
<p>Los tejidos de exterior (acrílico, olefin, textilene) admiten limpieza con agua y jabón. Para manchas resistentes, usa una solución de lejía diluida al 10%. Deja secar completamente al aire antes de colocar sobre los muebles. Comprueba cremalleras y costuras.</p>

<h3>Superficies de teca o madera</h3>
<p>Si la madera está gris por la oxidación natural, una lijada suave con papel de lija de grano fino 120 y una mano de aceite de teca restauran el color original. Si prefieres el tono plateado, simplemente límpiala con agua y jabón.</p>

<h3>Parasoles y pérgolas</h3>
<p>Despliega el parasol y comprueba que el mecanismo abre y cierra sin trabas. Revisa la tela en busca de roces o puntos débiles. Limpia con esponja húmeda y deja secar.</p>

<h2>Mantenimiento de otoño-invierno: cómo guardar correctamente</h2>
<ul>
  <li>Limpia todo antes de guardar (la suciedad y humedad aceleran el deterioro).</li>
  <li>Guarda los cojines en bolsas de almacenaje o en interiores.</li>
  <li>Apila las sillas en grupos y cúbrelas con fundas de exterior transpirables.</li>
  <li>Si no tienes espacio para guardar los muebles, cúbrelos con fundas específicas y asegúralas contra el viento.</li>
  <li>Los parasoles deben guardarse desmontados y en su funda original.</li>
</ul>
<p><strong>Consejo extra:</strong> los muebles de aluminio y materiales sintéticos pueden permanecer al exterior todo el año sin problemas; simplemente protégelos de las heladas si vives en zonas de interior con temperatura muy baja.</p>
""",
        "tags": "mantenimiento, limpieza, temporada, cuidados exterior",
    },
    {
        "title": "5 ideas para decorar tu terraza este verano: del estilo mediterráneo al diseño minimalista",
        "summary_html": "Inspiración para decorar tu terraza o jardín: cinco estilos que combinan estética, funcionalidad y resistencia para cualquier espacio exterior.",
        "body_html": """
<h2>Tu terraza es una habitación más</h2>
<p>Merece el mismo cuidado y personalidad. Tanto si tienes un amplio jardín como una pequeña terraza urbana, hay un estilo y una distribución perfecta para ti.</p>

<h2>1. Mediterráneo clásico: blanco, rattan y plantas</h2>
<p>Elige muebles con estructura de aluminio blanco y tapizado en tonos crudos o beige. Combínalos con macetas de terracota, plantas aromáticas (lavanda, romero, buganvilla) y tejidos de rayas. Una mesa central de madera natural o teca cierra el conjunto.</p>

<h2>2. Lounge moderno: tonos oscuros y formas bajas</h2>
<p>Los sofás y chaise longues de ratán sintético en color grafito o antracita crean un ambiente sofisticado y relajado. Añade una mesa de centro de aluminio y cristal, iluminación LED ambiental y cojines en tonos tierra (terracota, arena, marrón chocolate).</p>

<h2>3. Minimalista escandinavo: geometría limpia y madera</h2>
<p>Mesas y sillas de aluminio con líneas rectas, acabado en color gris claro o blanco mate. Complementa con madera de teca o acacia para los tableros o las banquetas. Pocos elementos, bien elegidos.</p>

<h2>4. Hostelería y espacio público: funcional y durable</h2>
<p>Para bares, restaurantes o espacios comunitarios, lo importante es la apilabilidad, la resistencia y la facilidad de limpieza. Las sillas de aluminio con asiento de textilene o polipropileno son la solución ideal: ligeras, no se oxidan y aguantan el uso intensivo.</p>

<h2>5. Jardín familiar: espacio para comer, jugar y relajarse</h2>
<p>Una mesa grande extensible para las comidas en familia, sillas apilables para cuando hay más invitados, y un set de lounge en un rincón para los momentos de relax. Añade un parasol de pie o una pérgola para las tardes de verano.</p>
""",
        "tags": "decoración, inspiración, estilo mediterráneo, minimalista, lounge, terraza",
    },
    {
        "title": "Muebles de exterior para hostelería: qué buscar y por qué la calidad marca la diferencia",
        "summary_html": "Guía para responsables de bares, restaurantes y hoteles sobre qué características son imprescindibles en el mobiliario de terraza profesional.",
        "body_html": """
<h2>En hostelería, el mobiliario trabaja más que en ningún otro entorno</h2>
<p>Muchas horas de uso diario, exposición continua a los elementos, clientes de todo tipo. Una mala elección puede costar caro —en reposiciones, en imagen y en pérdida de reservas.</p>

<h2>Durabilidad ante todo</h2>
<p>El aluminio con acabado en polvo electrostático es el estándar en hostelería de calidad. No se oxida, no requiere pintura y mantiene el color durante años. Busca perfiles con un grosor mínimo de 2 mm y soldaduras reforzadas en los puntos de carga.</p>

<h2>Apilabilidad: clave para la logística diaria</h2>
<p>Las sillas apilables reducen el espacio de almacenamiento y facilitan la organización al abrir y cerrar el local. Un buen diseño apilable permite apilar hasta 8-10 sillas sin riesgo de daño.</p>

<h2>Tapizados técnicos: textilene y acrílico</h2>
<p>Los tapizados de exterior para uso profesional deben ser resistentes a los rayos UV, lavables, de secado rápido y difíciles de rasgar. El textilene (malla de PVC trenzado) y los tejidos acrílicos de alta densidad son los más utilizados en hostelería exigente.</p>

<h2>Mesas con tablero adecuado</h2>
<p>Para hostelería, los tableros de aluminio, HPL (laminado de alta presión) o porcelana son los más recomendados: resistentes a los arañazos, impermeables y fáciles de limpiar. El cristal templado es una opción estética válida pero requiere más cuidado.</p>

<h2>Normativa y peso</h2>
<p>Consulta siempre la normativa local sobre terrazas y veladores en tu municipio. En muchos casos hay restricciones de peso o altura. Los muebles de aluminio son la opción más práctica en este sentido.</p>
""",
        "tags": "hostelería, restaurante, bar, terraza profesional, veladores",
    },
    {
        "title": "Tendencias en muebles de exterior para 2025: materiales, colores y diseños que marcan el año",
        "summary_html": "Las claves del diseño de exterior en 2025: sostenibilidad, colores tierra, formas orgánicas e integración interior-exterior.",
        "body_html": """
<h2>Color: de los neutros al verde salvia</h2>
<p>El blanco y el gris siguen siendo los favoritos por su versatilidad, pero este año el verde salvia, el terracota y el beige cálido ganan protagonismo. Son colores que conectan con la naturaleza y envejecen bien visualmente.</p>

<h2>Formas orgánicas y curvas</h2>
<p>El diseño recto y geométrico deja paso a formas más redondeadas y orgánicas, tanto en sillas como en sofás y mesas. Las curvas suavizan el espacio exterior y generan una sensación más acogedora.</p>

<h2>Sostenibilidad y materiales reciclados</h2>
<p>Los consumidores valoran cada vez más el origen de los materiales. El aluminio reciclado, los tejidos fabricados con plástico recuperado del océano y la madera de teca con certificación FSC son tendencia tanto en diseño residencial como en hostelería.</p>

<h2>Integración interior-exterior</h2>
<p>Los salones y las terrazas se funden: mismas paletas de color, materiales similares, misma altura de asiento. El mueble de exterior ya no parece "de exterior" —tiene la calidad y el aspecto del mueble de interior.</p>

<h2>Iluminación integrada</h2>
<p>Las mesas con iluminación LED solar integrada en la base o en el tablero, y los sofás con carga USB en los brazos, son cada vez más habituales en proyectos de interiorismo exterior.</p>
""",
        "tags": "tendencias 2025, diseño exterior, sostenibilidad, colores, materiales",
    },
    {
        "title": "Cómo aprovechar al máximo una terraza pequeña: muebles, distribución y trucos visuales",
        "summary_html": "Guía práctica para terrazas y balcones urbanos: qué muebles elegir, cómo distribuirlos y trucos para ganar amplitud visual en espacios reducidos.",
        "body_html": """
<h2>Tener una terraza pequeña no significa renunciar a disfrutarla</h2>
<p>Con los muebles adecuados, una buena distribución y algunos trucos visuales, cualquier espacio —aunque sea de 4 o 6 m²— puede convertirse en un rincón agradable para desayunar, leer o tomar algo por las tardes.</p>

<h2>Elige muebles a escala</h2>
<p>El error más frecuente en terrazas pequeñas es colocar muebles demasiado grandes. Una mesa cuadrada de 60×60 cm con dos sillas es suficiente para un balcón urbano. Los muebles de aluminio son especialmente útiles aquí por su ligereza: puedes moverlos o guardarlos en segundos.</p>

<h2>Muebles plegables y apilables: tus mejores aliados</h2>
<p>Las sillas y mesas plegables permiten tener más capacidad cuando hace falta y guardar espacio cuando no. Elige modelos que se vean bien incluso cuando están plegados —hay diseños que funcionan como elemento decorativo en la pared.</p>

<h2>Distribución: el perímetro, tu amigo</h2>
<p>Coloca los muebles pegados a la pared o barandilla, dejando libre el centro. Esto amplía visualmente el espacio y facilita el paso. Un sofá o banco esquinero aprovecha el rincón más muerto de la terraza.</p>

<h2>Trucos visuales para ganar amplitud</h2>
<ul>
  <li>Usa colores claros o neutros: el blanco, el beige y el gris claro amplían visualmente.</li>
  <li>Los muebles de líneas finas y patas visibles ocupan menos espacio visual que los de base maciza.</li>
  <li>Un espejo exterior duplica la sensación de amplitud.</li>
  <li>Las plantas verticales o en pared añaden vida sin ocupar suelo.</li>
</ul>

<h2>Iluminación para alargar las tardes</h2>
<p>Una tira LED en el perímetro o una lámpara de exterior inalámbrica (recargable, sin cables) transforma la terraza de noche sin necesidad de instalación eléctrica.</p>
""",
        "tags": "terraza pequeña, balcón, espacio reducido, distribución, decoración urbana",
    },
]


def create_article(article: dict) -> dict:
    payload = json.dumps({"article": article}).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=payload,
        headers={
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    print(f"Subiendo {len(ARTICLES)} artículos al blog {BLOG_ID}...\n")
    for i, article in enumerate(ARTICLES, 1):
        try:
            result = create_article(article)
            art = result["article"]
            print(f"  ✅ [{i}/{len(ARTICLES)}] {art['title']}")
            print(f"       → https://mueblesexterior.myshopify.com/blogs/news/{art['handle']}\n")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            print(f"  ❌ [{i}/{len(ARTICLES)}] Error en '{article['title']}': {e.code} — {body}\n")

    print("Proceso completado.")


if __name__ == "__main__":
    main()
