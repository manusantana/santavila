# AUDITORIA_SANTAVILA.md

**Snapshot:** 2026-05-06
**Fuente principal:** Shopify Admin GraphQL API (`mueblesexterior.myshopify.com`) vía plugin oficial Shopify, autenticado como `hola@santavila.com`.
**Documentos cruzados:** `plan_santavila.md`, `PROYECTO.md`, `Santavila.xlsx` (hojas Hevea/Balliu/Seguimiento), CSVs de proveedores en `proveedores_raw/hevea/`.
**Limitaciones de acceso declaradas:** scope OAuth actual = `read_products,write_products,read_files,write_files`. **Sin acceso a:** `pages`, `shopLocales`, `themes` (necesitan `read_content`, `read_locales`, `read_themes`). **Sin acceso a:** Analytics, Markets, configuración de checkout, lista de apps instaladas.

---

## 1.1 Diagnóstico ejecutivo

### Situación actual

Santavila tiene los **fundamentos comerciales** funcionando: dominio propio (`santavila.com`) con SSL, 235 productos publicados (231 ACTIVE, 4 DRAFT), catálogo bilateral cubriendo dos proveedores españoles (Balliu 120, Hevea 115), nombres de producto en español con un patrón consistente del tipo `"Sofá terraza aluminio 2 plazas · estilo contemporáneo | 166×90 cm"`, descripciones HTML con estructura mínima (párrafos + bullets + medidas) y SEO title/description rellenados al 100 %. Pricing en EUR, IVA incluido, peso en kilogramos, zona horaria CEST y país ES.

**Pero la tienda todavía es una "Shopify con productos cargados"**, no una marca premium. La estructura de catálogo está al nivel de proveedor (siete colecciones por **tipo de mueble** — `tumbonas`, `mesas`, `sillas-de-exterior`, `parasoles`, `accesorios`, `sillones-de-exterior`, `frontpage`), sin colecciones por **espacio** (terraza, ático, jardín…), sin colecciones por **material** (aluminio, madera, HPL…), sin colecciones Santavila propias y sin área para profesionales. El **modelo de datos** es plano: 0 metafields en namespace `santavila`, 0 metaobjects definidos. La información de producto crítica para ticket alto (plazo, garantía, mantenimiento, montaje, número de bultos, peso real) **no existe como dato estructurado** — vive en el HTML libre de la descripción cuando vive.

### Principales problemas (ordenados por impacto)

1. **Descuentos permanentes en todos los productos.** Muestra real en BRANDON-1 (handle `sillon-exterior-aluminio-estilo-envolvente-9890-cm`): `compareAtPrice = 980 €`, `price = 809.92 €`. Esto pinta toda la tienda como "rebajada permanentemente" — exactamente lo que el plan pide evitar.
2. **Etiquetas `match-verde / match-rojo / match-amarillo` aplicadas a 120 productos Balliu.** Probablemente sistema interno de la app B2B "Wholesale Pricing Discount B2B" (mencionada en `README.md`). Si son visibles al cliente final desde el theme, contaminan la percepción.
3. **Vendor real (`Balliu`, `Hevea`) expuesto en tags visibles** — los tags suelen rendear en filtros y/o en URL de filtrado. Contradice el posicionamiento de marca: el cliente debe ver Santavila, no a sus proveedores.
4. **Cero metafields propios.** Sin namespace `santavila`. La información de plazo, garantía, montaje, materiales, espacio recomendado, mantenimiento, peso real, número de bultos no es filtrable, ni reusable, ni exportable de forma estructurada.
5. **Cero metaobjects.** Sin guías de material, sin "Espacio", sin políticas de garantía estructuradas, sin proveedor como entidad.
6. **Colecciones sin texto útil ni SEO.** Las 7 colecciones tienen `descriptionHtml=""`, `seo.title=null`, `seo.description=null`. Una PLP así rinde como rejilla de productos; no ayuda a decidir, ni captura tráfico orgánico.
7. **Typo visible:** colección con título `"Sofas de exterior"` (sin tilde) y handle `sillones-de-exterior` — desalineación entre handle y title, y typo ortográfico en el título visible.
8. **Inconsistencias en `productType`.** Se ve `Sofá` y `Sofa`, `Accesorios` y `Accesorio` simultáneamente. Hay 21 productTypes distintos para 235 productos: dispersión que daña filtrado y consistencia.
9. **71 productos sin ALT en imagen principal y 2 productos sin imagen principal.** Daña accesibilidad y SEO de imagen.
10. **Peso del producto = 0 kg en BRANDON-1** (en `inventoryItem.measurement.weight`). Probablemente generalizado: dato logístico crítico vacío.
11. **Descripciones con jerga interna** ("hostelería y contract"). El plan pide tono sereno, sin tecnicismos ni anglicismos del sector.
12. **Sin dato `vendor` real estructurado en metafield.** El campo `vendor` de Shopify se está usando para guardar el proveedor (Balliu/Hevea), pero ese campo se renderea en muchos themes como nombre comercial. Tendría que estar siempre `vendor = "Santavila"` y la identidad del proveedor en un metafield interno (`santavila.proveedor`).
13. **Falta página "Entrega", "Garantía", "Mantenimiento", "Profesionales".** No tengo acceso al recurso `pages` por scope, pero el plan documental y la falta de menús dedicados sugieren que no existen — y sin esas páginas la PDP no puede enlazar a información de confianza profunda.
14. **Sin productos héroe marcados.** No hay manera de distinguir "producto fuerte" (margen + foto + plazo + ficha) de un producto medio. Toda la home tendría que mostrar lo mejor; ahora cualquier orden por SKU sirve por igual.
15. **Sin estado de enriquecimiento.** No hay manera de saber qué SKUs están "completos para vender premium" y cuáles están "subidos a Shopify pero pendientes de redacción".

### Principales oportunidades

1. **Diferenciación clara en un nicho mal cubierto.** Sklum es bazar; Kave Home no es especialista en exterior; Gandia Blasco/Kettal/Vondom son inaccesibles; Leroy/IKEA no son aspiracionales. Santavila puede ocupar el hueco "exterior premium accesible mediterráneo" sin competidor directo en el segmento medio español.
2. **Catálogo ya consolidado** (235 productos, 2 proveedores, fotos base, precios en EUR con IVA). No hay que partir de cero.
3. **Plataforma sólida.** Shopify con dominio propio, SSL, plugin oficial Shopify AI Toolkit instalado, MCP funcionando, automatización vía Shopify Flow disponible.
4. **Dato fuente de tarifas controlado.** Existe `Santavila.xlsx` con hojas Hevea/Balliu, plus seguimiento histórico Hevea ya regenerable con un único script (`update_hevea_seguimiento.py`). Esa rigurosidad operativa permite escalar.
5. **Imágenes de proveedor + cutouts ya procesados** (49 + 48 PNGs en `images_optimized/` y `images_cutout/`). Punto de partida visual sin coste.
6. **IA visual disponible** (Higgsfield, FLUX.1-schnell). Permite generar el banco de imágenes de ambiente con dirección de marca propia sin shooting.
7. **Margen por SKU controlado.** Permite priorizar comercialmente por margen real, no por intuición.

### Riesgos

1. **Reputacional / legal:** prometer "fabricado en España" de forma genérica si no está validado SKU a SKU. Riesgo real de reclamaciones por etiquetado.
2. **Operativo:** entrega de hasta 30 días sin promesa explícita en PDP. Cliente puede esperar 7-10 días por defecto y disparar incidencia.
3. **Reputacional:** descuentos permanentes acumulados. Si el cliente ve `compareAtPrice` siempre tachado, asume que el "precio real" es el barato y el otro es ficticio. Daña confianza y entra en zona gris regulatoria (LSSI, Ley de Comercio).
4. **Riesgo de migración inversa:** si el plan se ejecuta a medias (por ejemplo, se crean los metafields pero no se rellenan, o se crean colecciones nuevas pero sin texto), la tienda queda peor que antes — más lenta, con páginas vacías y sin coherencia. Hay que comprometerse a terminar las fases.
5. **Dependencia de proveedor.** Si Hevea o Balliu reorganizan SKUs (ya pasó: 32 SKUs reasignados entre marzo y abril 2026), el catálogo se rompe en silencio. La auditoría a proveedor (email ya redactado) es crítica.
6. **Score B2B `match-*` de fuente desconocida.** Si esos tags vienen de una app, una desinstalación los deja huérfanos. Hay que entender el origen antes de tocarlos.

### Prioridades

| # | Prioridad | Acción | Razón |
|---|-----------|--------|-------|
| 1 | P0 | Eliminar `compareAtPrice` permanente — auditar todos los productos | Daña percepción premium en todas las páginas a la vez |
| 2 | P0 | Auditar y limpiar tags expuestos al cliente (`Hevea`, `Balliu`, `match-*`, `hostelería`) | Expone proveedor y datos internos |
| 3 | P0 | Mover `vendor` Shopify a `"Santavila"` y crear `santavila.proveedor` interno | Coherencia de marca + filtrado interno por proveedor |
| 4 | P1 | Crear modelo de datos `santavila.*` (32 metafields) + 8 metaobjects `sv_*` | Sin dato estructurado no hay PDP premium ni filtros ni automatización |
| 5 | P1 | Crear páginas `Entrega`, `Garantía`, `Mantenimiento`, `Profesionales` | Confianza para ticket alto |
| 6 | P1 | Reescribir colecciones (descripción + SEO + handle/title coherente) | PLP capta tráfico orgánico y ayuda a decidir |
| 7 | P2 | Crear colecciones por **espacio** y por **material** | Arquitectura ecommerce Santavila vs ordenación de proveedor |
| 8 | P2 | Marcar 20 productos héroe + score interno por SKU | Permite priorizar visualmente |
| 9 | P2 | Plantilla PDP premium por familia (sofá / mesa / silla / tumbona / parasol / set) | Reduce miedo a comprar |
| 10 | P3 | Banco de imágenes IA con dirección Santavila | Independencia visual de proveedor |

---

## 1.2 Auditoría de marca

### Claim
**Estado:** ausente en metadata pública (description vacío, no hay tagline detectable vía API).
**Recomendación según `plan_santavila.md`:** `"Diseño español para vivir fuera."`
**Riesgo:** la home, el `<meta name="description">` y los OG tags son hoy genéricos o derivados del nombre de la tienda. Una búsqueda de marca en Google muestra solo "Santavila" sin propuesta diferenciadora.

### Tono
**Muestra real (BRANDON-1):**
> *"El sillón está fabricado íntegramente en aluminio con estructura tubular reforzada y acabado termo-lacado de alta resistencia… Apto para uso residencial y proyectos de hostelería y contract (hoteles, restaurantes, terrazas de establecimientos)."*

Bien: lenguaje técnico preciso, no "marketinés", medidas claras.
Mal: empieza con `"El sillón"` (sin nombre propio, suena a manual de proveedor traducido), incluye **"hostelería y contract"** que es jerga interna B2B inadecuada para cliente residencial premium, y el formato repite el patrón mecánicamente en cada producto sin variación.

### Idioma
**Estado:** español al 100 % en lo auditado. Muestra de 235 productos: 0 títulos en inglés/francés con formato slash detectado, 0 productos con palabras como "armchair", "table", "outdoor", "garden". Buen punto de partida.
**Riesgo no verificado:** sin acceso a `pages` ni a `themes` no puedo confirmar si en el footer, en correos transaccionales, en el theme o en la barra de envío hay textos en inglés tipo "FREE SHIPPING TO MAINLAND SPAIN" (mencionado en el plan como ejemplo concreto). Asumir que **al menos un texto en inglés sigue vivo** — verificar manualmente.

### Consistencia
- **productType:** 21 valores para 235 productos. Variaciones detectadas: `Sofá`/`Sofa`, `Accesorios`/`Accesorio`. Hay que normalizar a 8-10 valores limpios.
- **Tags:** mezcla de tipo (sofá, sillón), material (aluminio, HPL), uso (terraza, jardín, hostelería), atributo (2 plazas, 3 plazas, conjunto sofá, bicolor) y proveedor (Hevea, Balliu). **No es taxonomía**: es un saco mixto. Hostelería como tag visible no tiene sentido para B2C residencial.
- **Títulos:** patrón `[Tipo] [rasgo] · [estilo] | [medida]` aplicado en mayoría — bien. Excepción: `Reposapiés exterior · 73×46×40 cm` (sin "·" antes de medida).

### Textos genéricos
La descripción tipo de BRANDON-1 termina con un bloque idéntico para todos los productos similares ("Resistente a rayos UV, lluvia y humedad", "Apto para uso residencial y proyectos de hostelería y contract", "Transporte sencillo y montaje sin herramientas especiales"). Esto contradice el principio del plan: cada PDP debe responder al miedo específico de ese producto.

### Premium percibido
**Negativo:** descuento permanente, vendor expuesto, tags B2B visibles, colecciones sin descripción.
**Positivo:** dominio propio con SSL, fotos cutout para Hevea, descripciones técnicas correctas, naming en español con patrón.
**Veredicto:** la tienda hoy aparenta "ecommerce serio que aún no ha terminado el setup", no "marca especialista premium accesible".

### Confianza
- **Falta:** página de entrega, página de garantía, página de mantenimiento, contacto WhatsApp, claim sobre proveedores españoles, plazos visibles, garantía visible.
- **Hay:** dominio propio, email de contacto (`hola@santavila.com`), SSL, IVA incluido en precios.

---

## 1.3 Auditoría UX/UI

> Limitación: no tengo acceso a `themes` ni puedo navegar visualmente. Esta auditoría es **estructural** (basada en la API). Una pasada visual en navegador queda pendiente.

### Home
- **Sin acceso al theme** no puedo confirmar bloques. La colección `frontpage` tiene 8 productos asociados — **demasiado pocos para construir una home con productos héroe + colecciones por espacio + bloque editorial + barra de confianza** según el plan.
- **Riesgo alto:** la home actual está hoy probablemente armada con la sección "Productos destacados" tirando de `frontpage` y poco más. Es una home de "tienda nueva".

### Menú
- Sin acceso a `menus`. Pero la estructura de colecciones (7 colecciones por tipo + Home page) sugiere un menú simple del estilo:
  - Inicio · Tumbonas · Mesas · Sofás · Sillas · Parasoles · Accesorios
- **Falta** según plan: Espacios · Materiales · Profesionales · Inspiración · Ayuda.

### Navegación
- Estructura plana. Sin breadcrumbs lógicos por espacio o material.

### Footer
- Sin acceso al theme; lo declaro como **PENDIENTE de inspección visual**.
- Riesgo: textos de envío en inglés, links muertos, ausencia de páginas legales obligatorias (Política de privacidad, Aviso legal, Condiciones de venta, RGPD).

### Colecciones (PLP)
- 0 de 7 con descripción. 0 de 7 con SEO title/description.
- Una PLP pelada (rejilla + filtros automáticos) **no convierte para ticket alto** — el cliente premium quiere narrativa, no rejilla.

### PDP
- **Tiene:** título, descripción HTML con bullets, imágenes con ALT (mayoría), precio + comparado, variantes.
- **No tiene:** plazo visible junto al precio, garantía visible junto al precio, módulo "Encaja si", módulo "Materiales y mantenimiento" estructurado, FAQs específicos, productos compatibles curados (no aleatorios), CTA de asesoramiento.
- **Tiene mal:** `compareAtPrice` permanente, peso = 0 kg.

### Carrito
- Sin acceso al theme ni al checkout. **PENDIENTE.**

### Páginas de ayuda
- Sin acceso a `pages`. Hipótesis razonable: faltan o son las que vienen por defecto del theme (Política de envío genérica del theme). **Riesgo alto.**

### Mobile
- Sin acceso a inspección visual. **PENDIENTE.**

### Jerarquía visual
- Limitada por el theme. El theme actual concreto es desconocido por scope. Hay que pull del theme antes de planificar layout.

### CTAs
- En PDP: "Añadir al carrito" estándar. Sin CTA secundario de asesoramiento (WhatsApp / formulario).

---

## 1.4 Auditoría ecommerce

### Categorías
- **7 colecciones** vs ~25 sugeridas por el plan (8 colecciones principales + 7 espacios + 5 materiales + 6 profesionales + ayuda). Falta el ~70 % del esqueleto.
- Las 7 que existen son por **tipo de mueble** (sofá, mesa, silla, tumbona, parasol, accesorios). No hay por uso, espacio, material o proyecto.

### Filtros
- Sin acceso al theme no puedo confirmar qué filtros se renderean. Si el theme usa filtros nativos Shopify (Search & Discovery), los filtros disponibles serán los que `vendor` y `tag` permitan. **Hipótesis:** filtros pobres y poco útiles dada la mezcla de tags.

### Badges
- Etiqueta "Oferta" / "Sale" presumiblemente activa en todos los productos por el `compareAtPrice`. **Lo más urgente del Fase 0.**
- No hay badges propios tipo "Fabricado en España" / "Entrega 7-15 días" / "Producto héroe" / "Bajo pedido".

### Promociones
- No detecto bloques de promo de campaña. Solo el descuento estructural.

### Cross-sell
- Metafields detectados: `shopify--discovery--product_recommendation.related_products` y `complementary_products`. Eso es la base de Shopify Search & Discovery.
- **No tengo evidencia de que estén poblados.** Es esperable que estén vacíos.

### Información logística
- No hay "Entrega España península" visible globalmente.
- No hay plazo por producto como dato estructurado.
- No hay umbral de envío gratuito documentado en API (Hevea ofrece envío gratis >900 € en península, condición que el plan describe pero no hay metafield para guardarla).

### Garantía
- No hay metafield. No hay metaobject. No hay página dedicada (probable). No hay módulo en PDP.

### Devoluciones
- Sin acceso a `policies`. **PENDIENTE.**

### Asesoramiento
- No detecto formulario de asesoramiento, ni link a WhatsApp. **PENDIENTE de verificar visual.**

### Confianza
- Globalmente: ausente como sistema. Existe punto a punto (SSL, IVA, dominio) pero sin construcción narrativa.

---

## 1.5 Auditoría Shopify

### Theme actual
- Sin scope `read_themes` no puedo identificar el theme. Necesario para planificar cambios. Lo marcamos como **PENDIENTE** y proponemos `shopify theme pull` como paso 0 del backlog técnico.

### Templates / sections / snippets
- Sin acceso al código del theme. **PENDIENTE.**

### Settings
- Detectado vía `shop`: `taxesIncluded=true`, `currencyCode=EUR`, `weightUnit=KILOGRAMS`, `timezoneAbbreviation=CEST`, `billingAddress.country=Spain`. Configuración base correcta para España.

### Locales
- Sin scope `read_locales`. **PENDIENTE.** Habría que confirmar:
  - Idiomas activos (probablemente `es` solo, según el plan).
  - Si hay `en` por accidente — hay que desactivarlo.

### Metafields
- 0 metafield definitions en namespace `santavila`.
- Detectados: namespaces de Shopify auto (`shopify--discovery--product_recommendation`, `shopify--discovery--product_search_boost`) y uno de Google Shopping (`mm-google-shopping`).
- En el producto BRANDON-1 hay 2 metafields aplicados: `global.title_tag`, `global.description_tag` (ambos con copia del SEO title y description). **Redundantes** con `seo.title` y `seo.description` nativos — relics típicos de plantilla histórica de Shopify, no críticos.

### Metaobjects
- 0 definiciones. Greenfield total.

### Navegación
- Sin acceso a `menus` (requiere `read_content` o `read_navigation`). **PENDIENTE.**

### Productos
- 235 productos, 231 ACTIVE, 4 DRAFT. 21 productTypes (con duplicidades por capitalización/acentos).
- Vendor real Balliu/Hevea — **debería pasar a metafield interno.**

### Colecciones
- 7 colecciones (incluyendo `frontpage` automática). Todas sin `descriptionHtml` y sin SEO.

### Policies
- Sin acceso a `shopPolicies`. **PENDIENTE.**

### Redirects
- Sin acceso por scope. **PENDIENTE.** Cuando se reescriban handles (ej. `sillones-de-exterior` con título "Sofas" → `sofas-de-exterior` con título "Sofás"), hay que crear redirects 301.

### Apps instaladas
- Sin scope `read_apps`. Hipótesis basada en `README.md`:
  - "Wholesale Pricing Discount B2B" (mencionada explícitamente).
  - Probablemente Shopify Search & Discovery (los metafields `shopify--discovery--*` están auto-creados por esa app oficial).
  - Probable Google & YouTube channel app (los `mm-google-shopping.*` metafields lo sugieren).

---

## 1.6 Auditoría SEO base

### Titles
- Productos: 100 % rellenos (235/235). Buen baseline.
- Colecciones: 0 % rellenos (0/7 con `seo.title`). Crítico.

### Meta descriptions
- Productos: rellenos pero a partir de un truncado del primer párrafo de la descripción, no copy SEO específico. Aceptable de partida, pero subóptimo.
- Colecciones: 0 % rellenas. Crítico.

### H1
- No tengo acceso al renderado HTML real. En Shopify estándar, H1 = `product.title` para PDP y `collection.title` para PLP. Los títulos de colección como "Sofas de exterior" (sin tilde) son por tanto el H1 actual — typo SEO crítico.

### URLs
- Handles de producto: pattern `[descriptor]-[medida]-cm`, prefijo del proveedor para Balliu (`balliu-tumbona-de-exterior-resina-923110d9`) — **prefijo "balliu-" expone proveedor en URL**.
- Handles de colección: legibles, en español, sin acentos. Pero `sillones-de-exterior` mostrando "Sofas de exterior" descuelga handle/H1.

### Indexabilidad
- Sin acceso a sitemap ni robots por API. **PENDIENTE.** Con dominio propio activo, asumir indexabilidad estándar Shopify hasta confirmar que no hay `password_page` activo.

### Categorías prioritarias
- Faltan: "Sofás de exterior", "Mesas comedor exterior", "Tumbonas de exterior", "Parasoles de terraza", "Muebles exterior aluminio", "Muebles para terraza", "Muebles para ático", "Muebles fabricados en España" (este último solo si se valida por SKU).

### Textos pobres
- 0 caracteres en `descriptionHtml` de las 7 colecciones.
- Descripciones de producto repiten bullets idénticos entre productos similares (no añade valor SEO único).

### ALT de imágenes
- 71 productos sin ALT en imagen principal. Crítico para accesibilidad y SEO de imagen.

### Schema
- Sin acceso al theme. Shopify theme estándar suele tener schema Product, Organization y BreadcrumbList. **PENDIENTE de verificar.** Schema FAQ y HowTo pendientes (no hay datos para alimentar todavía).

### Enlaces internos
- Sin descripción de colección, sin páginas de espacio, sin guías de compra → ausencia de tejido de enlaces internos. La autoridad SEO de la home no se distribuye por la arquitectura.

---

## 1.7 Auditoría de datos de producto

> Verificación basada en BRANDON-1 + esquema vacío de metafield definitions. Asumimos comportamiento generalizado a todo el catálogo.

| Dato | ¿Existe? | Cómo |
|------|---------|------|
| Proveedor | ✓ | Campo nativo `vendor` (Hevea / Balliu) — pero **expuesto al cliente** |
| Plazo mínimo (días) | ✗ | No existe como dato estructurado |
| Plazo máximo (días) | ✗ | No existe |
| Tipo de entrega | ✗ | No existe |
| Garantía | ✗ | No existe estructurada (sí mencionada genéricamente en HTML) |
| Material | parcial | A veces como tag (`aluminio`, `HPL`) — no estructurado, no completo |
| Medidas | parcial | Sólo en HTML libre dentro de la descripción, en el título y en el handle. **No filtrable.** No hay `ancho_cm`, `fondo_cm`, `alto_cm` separados |
| Peso | ✗ | `inventoryItem.weight = 0` en BRANDON-1 — vacío |
| Bultos | ✗ | No existe |
| Uso recomendado | parcial | Solo como tag (`terraza`, `jardín`) |
| Espacio recomendado | ✗ | No existe (terraza, ático, porche, jardín, balcón, piscina, patio) |
| Mantenimiento | parcial | En HTML libre, no estructurado |
| Margen interno | externo | Vive en `Santavila.xlsx` y en `tarifas_consolidadas.xlsx`, **no sincronizado a Shopify** |
| Prioridad comercial | ✗ | No existe |
| Estado de enriquecimiento | ✗ | No existe — no se puede saber qué productos están listos para destacar |

### Conclusión

**El catálogo está cargado pero no estructurado.** La información sí existe en algún sitio (el .xlsx, el HTML, las tarifas, los handles) pero no está en el lugar correcto (metafields filtrables, metaobjects reusables) ni completa. Sin esta capa, no se puede:

- mostrar plazo real en PDP,
- filtrar por material en PLP,
- crear PLPs por espacio,
- automatizar etiquetado por margen / plazo,
- priorizar productos héroe,
- generar feed Google Shopping con dato real,
- dar a Higgsfield datos de medida y material para generar imágenes coherentes.

Esto es la pieza de palanca: sin Fase 1 (modelo de dato), las Fases 2-7 son cosmética.

---

## Resumen ejecutivo en 5 frases

1. **La tienda está al nivel de "Shopify con productos cargados"**, con catálogo bien poblado pero sin estructura ecommerce ni capa de marca.
2. **El bloqueador estratégico es el modelo de datos**: 0 metafields propios, 0 metaobjects, todo el dato útil disperso en HTML libre y Excel externo.
3. **El bloqueador percepción premium son tres cosas concretas**: descuentos permanentes en todos los productos, vendor real expuesto en tags y URL, falta total de descripción + SEO en colecciones.
4. **La oportunidad está en el hueco de mercado** (premium accesible mediterráneo español) y en los activos ya disponibles (catálogo + dominio + dato de margen + Higgsfield + plugin Shopify oficial).
5. **El orden correcto es Fase 0 (limpieza visible) → Fase 1 (dato) → Fase 2 (PDP)**, no rediseñar la home antes que el resto.
