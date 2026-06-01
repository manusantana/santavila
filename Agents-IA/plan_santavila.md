# plan_santavila.md

**Proyecto:** Santavila — ecommerce Shopify de mobiliario exterior premium accesible  
**Mercado inicial:** España península  
**Estado actual:** catálogo, categorías y precios subidos en Shopify  
**Objetivo del plan:** transformar Santavila de una tienda-catálogo en una marca ecommerce premium, especialista en mobiliario exterior español, con una experiencia de compra clara, confiable y preparada para escalar.

---

## ⚙️ Estado de ejecución — SEO/GEO (actualizado 2026-05-31)

> Registro vivo de lo ejecutado con Claude Code. Detalle técnico de apps/tokens y conexión Google en `Agents-IA/PROYECTO.md`. Informes en la raíz: `GEO-AUDIT-REPORT.md`, `KEYWORD-RESEARCH.md`, `SEO-BASELINE.md`.

### Hecho ✅
- **Auditoría GEO/SEO** inicial → `GEO-AUDIT-REPORT.md` (GEO Score ≈37/100; mayores carencias: citabilidad, autoridad de marca, E-E-A-T; base técnica fuerte).
- **Keyword research** ES (Google Autocomplete) → `KEYWORD-RESEARCH.md`. Aprendizaje: el genérico lo dominan IKEA/Leroy/Jysk; Santavila gana en long-tail por **material/espacio** + **contenido informacional**.
- **Google conectado** (OAuth aislado): Search Console (sitemap enviado + baseline en `SEO-BASELINE.md`), GA4 y Merchant. Scripts en `scripts/` (ejecutar con `.venv/bin/python`).
- **Merchant auditado** — cuenta correcta = **`5781655181`** (santavila.com): **0 productos rechazados, feed sano**. El "problema del GTIN" era **falsa alarma** (Google acepta mobiliario sin GTIN si hay marca). Único aviso real: `language_mismatch` (~668) por **Mercados de Shopify** internacionales publicando en inglés → pendiente ajustar en Shopify → Mercados.
- **Fichas de producto:** 31 descripciones vacías/cortas **reescritas** (citables) + meta descriptions vía API. Carmen/Lola/Capri corregidas con datos reales de Balliu + **imágenes oficiales subidas** (Carmen, Lola, Capri Doble, Parasol Ágora). Cojín 40×40 sin imagen → **DRAFT**.
- **Colecciones (Bloque 1.1):** las 6 (sillas, sofás, tumbonas, mesas, parasoles, accesorios) con **intro + FAQ + SEO title + meta description** (antes 0 texto).
- **Tema conectado** (Dwell 3.5.1) y editado: creadas `sections/collection-intro.liquid` y `sections/collection-faq.liquid`; `templates/collection.json` muestra ahora **intro arriba + FAQ al final del listado**, dinámico por colección. Backups en `content/theme_backups/`.

### Pendiente (orden sugerido)
- **FAQPage schema (JSON-LD)** para las FAQ de colección/producto (rich results) — aprovechando el acceso al tema.
- **Bloque 1.2 — Blog:** publicar el post de materiales ya optimizado (`content/blog/materiales-aluminio-teca-ratan.md`) + optimizar los otros 5 posts (rankean en pos 4-10).
- **Bloque 1.3 — Página "Sobre Santavila"** (NAP Vigo, historia, confianza → E-E-A-T).
- **Autoridad de marca** (categoría más baja, 12/100): reseñas (Judge.me → AggregateRating), Google Business Profile, perfiles (Trustpilot/Pinterest/YouTube).
- **De tu lado (no-código):** ajustar **Mercados de Shopify** (dejar solo ES/EUR/español → caen los avisos de idioma) y poner **Nombre de empresa visible = Santavila** en Merchant (la razón social `Ubicuo Libres Pensadores S.L.` se mantiene como dato legal).

### Notas para trabajar en paralelo
- **Dos apps/tokens Shopify** (ver `PROYECTO.md` §2): `.env` (`shpca_…`) = **catálogo**; `.env.local` (`shpat_…`) = **tema/código** (read/write_themes). Los scripts de catálogo usan `config.py` → `.env`.
- Cuentas Google: Merchant `5781655181`, GA4 `393664201`, GSC `sc-domain:santavila.com`. **Ignorar** la cuenta Merchant `515612993` (de la agencia, controlada).
- Todos los cambios de catálogo/colección se aplicaron con **backup previo** (`content/descriptions/`), reversibles.

---

## 0. Decisiones de partida

Estas decisiones se toman como base del plan:

| Área | Decisión actual |
|---|---|
| Plataforma | Shopify |
| Mercado inicial | España península |
| Proveedores actuales | 2 |
| Catálogo activo | +200 productos/SKUs |
| Margen | Controlado por SKU |
| Plazo máximo de entrega | Hasta 1 mes |
| Entrega | Solo transporte |
| Montaje | No incluido |
| Subida a vivienda | No incluida salvo que se acuerde aparte |
| Garantía | La garantía real será la del proveedor |
| Marketing de pago | No es prioridad inmediata |
| Fotografía | Base de proveedor, enriquecida con IA |
| Herramientas disponibles | Claude Code, Antigravity, Shopify AI Toolkit, MCP Shopify, Higgsfield AI |

### Decisión crítica de comunicación

Aunque el proyecto se apoye en proveedores españoles, **Santavila no debe prometer “fabricado en España” de forma genérica si no está validado por SKU**.

La fórmula segura será:

> **Mobiliario exterior seleccionado de proveedores españoles.**

Y, en los productos donde esté confirmado:

> **Fabricado en España.**

Esto evita problemas de confianza, legales y reputacionales.

---

## 1. Diagnóstico ejecutivo

Santavila tiene una oportunidad real, pero todavía no debe comportarse como una tienda que simplemente enseña productos. El sector de mobiliario exterior premium accesible no se gana solo por catálogo ni por precio. Se gana por una mezcla de:

- confianza,
- estética,
- claridad logística,
- selección,
- ficha de producto superior,
- origen,
- asesoramiento,
- sensación de marca seria.

La tienda actual debe evolucionar desde:

> “Shopify con productos cargados”

hacia:

> “Marca especialista en exterior español para terrazas, jardines, áticos, porches y vivienda real.”

La oportunidad no está en vender más barato que Sklum ni en parecer una firma de diseño inaccesible. La oportunidad está en ocupar un espacio intermedio:

> **Exterior premium accesible, español, mediterráneo, claro y bien explicado.**

---

## 2. Posicionamiento de marca

### 2.1 Territorio recomendado

**Mediterráneo contemporáneo con criterio español.**

Santavila debe unir dos ideas:

1. **Deseo:** exterior bonito, sereno, mediterráneo, contemporáneo.
2. **Confianza:** proveedor español, producto claro, materiales explicados, entrega transparente.

No debe posicionarse como:

- bazar de jardín,
- marketplace infinito,
- tienda de descuentos,
- marca de lujo inaccesible,
- catálogo genérico de proveedor.

Debe posicionarse como:

> **La forma seria y bonita de amueblar el exterior de una vivienda española.**

### 2.2 Claim principal recomendado

> **Diseño español para vivir fuera.**

### 2.3 Concepto creativo

> **El exterior bien vivido.**

Este concepto permite trabajar home, campañas, colecciones, contenido, B2B, guías y asesoramiento.

### 2.4 Propuesta de valor

> Santavila selecciona mobiliario exterior de proveedores españoles, con diseño mediterráneo contemporáneo, materiales preparados para el uso exterior y una experiencia de compra clara en lo que más importa: medidas, entrega, garantía, mantenimiento y servicio.

### 2.5 Frase de diferenciación

> No somos una tienda más de jardín. Somos una marca especialista en exterior para viviendas reales: terrazas, áticos, porches, jardines y espacios donde se vive fuera de verdad.

### 2.6 Tono de voz

Santavila debe hablar de forma:

- serena,
- experta,
- cálida,
- precisa,
- nada exagerada,
- nada “marketiniana”,
- nada low-cost.

Ejemplo de tono incorrecto:

> Descubre la máxima elegancia y sofisticación para transformar tu terraza en un oasis de ensueño.

Ejemplo de tono correcto:

> Sofá exterior con estructura de aluminio, cojines desenfundables y tejido preparado para uso exterior. Una pieza cómoda, ligera y fácil de mantener para terrazas, porches y jardines.

---

## 3. Principios estratégicos

### 3.1 Menos catálogo, más criterio

Aunque haya más de 200 SKUs, la tienda no debe mostrar sensación de almacén. Debe mostrar selección.

Acción:

- definir productos héroe,
- definir productos secundarios,
- ocultar o rebajar visibilidad de productos con baja calidad visual, bajo margen o plazo poco competitivo,
- crear colecciones Santavila, no solo categorías del proveedor.

### 3.2 No competir por descuento permanente

Los descuentos permanentes dañan la percepción premium. Puede haber campaña, pero no toda la tienda debe parecer en oferta.

Acción:

- revisar todos los precios tachados,
- reservar ofertas solo para campaña real,
- cambiar “Oferta” por etiquetas de valor cuando proceda:
  - Envío peninsular incluido,
  - Fabricado en España,
  - Entrega 7-15 días,
  - Ideal terraza,
  - Bajo pedido,
  - Colección completa.

### 3.3 La logística debe ser parte del producto

El usuario de ticket alto no compra solo el mueble. Compra tranquilidad.

Acción:

- mostrar plazo por producto,
- explicar “solo transporte” de forma clara,
- no prometer montaje,
- crear página de entrega muy bien explicada,
- mostrar “Entrega en España península” en todo el sitio.

### 3.4 La ficha de producto es la principal página de venta

La PDP debe ser la mayor prioridad tras la limpieza inicial.

Acción:

- crear plantilla premium por familia,
- incluir módulos de confianza,
- incluir materiales, mantenimiento, medidas, entrega, garantía y asesoramiento.

### 3.5 IA sí, pero con control de marca

La IA debe usarse para:

- generar escenas,
- mejorar contexto visual,
- crear inspiración,
- enriquecer fichas,
- crear guías,
- apoyar campañas.

No debe usarse para:

- inventar características,
- alterar proporciones reales,
- cambiar materiales,
- mostrar usos no recomendados,
- prometer ambientes imposibles,
- crear imágenes que luego generen reclamaciones.

---

## 4. Auditoría UX/UI actual

### 4.1 Problemas prioritarios detectados

1. Mezcla de español e inglés.
2. Home demasiado genérica.
3. Claims insuficientes.
4. Promoción excesiva.
5. Footer poco trabajado.
6. Colecciones con naming inconsistente.
7. Productos con nombres demasiado técnicos o traducidos.
8. Falta de promesa clara de entrega.
9. Falta de promesa clara de garantía.
10. Falta de asesoramiento visible.
11. Falta de arquitectura por uso real.
12. Falta de páginas de materiales.
13. Falta de página para profesionales.
14. Falta de dirección visual propia.
15. Fichas de producto todavía insuficientes para ticket premium.

### 4.2 Criterio de mejora

La tienda debe pasar el “test de 10 segundos”:

En menos de 10 segundos el usuario debe entender:

- qué vende Santavila,
- por qué es diferente,
- si entrega en su zona,
- si el producto es fiable,
- si puede pedir ayuda,
- qué tipo de estilo tiene la marca.

---

## 5. Arquitectura ecommerce recomendada

### 5.1 Menú principal

```txt
Inicio
Colecciones
Espacios
Materiales
Profesionales
Inspiración
Ayuda
```

### 5.2 Colecciones

```txt
Salones de exterior
Comedores de exterior
Sillas y sillones
Mesas de exterior
Tumbonas y relax
Parasoles y sombra
Bancos y auxiliares
Accesorios
```

### 5.3 Espacios

```txt
Terrazas
Áticos
Jardines
Porches
Balcones
Patios
Piscina
Hostelería pequeña
```

### 5.4 Materiales

```txt
Aluminio
Madera
HPL
Cuerda
Textilene
Tejidos exteriores
Cojines
Sombrillas y lonas
```

### 5.5 Ayuda

```txt
Entrega
Garantía
Devoluciones
Mantenimiento
Medidas
Contacto
Preguntas frecuentes
```

### 5.6 Profesionales

```txt
Interioristas
Arquitectos
Hoteles boutique
Restaurantes
Casas rurales
Presupuesto para proyectos
```

---

## 6. Home ideal

### 6.1 Objetivo de la home

La home no debe ser un escaparate de productos sueltos. Debe construir marca, confianza y dirección.

Debe transmitir:

1. estilo,
2. especialización,
3. origen español,
4. claridad logística,
5. facilidad de decisión.

### 6.2 Estructura recomendada

#### Bloque 1 — Hero

**Claim:**

> Diseño español para vivir fuera.

**Subclaim:**

> Mobiliario exterior seleccionado de proveedores españoles para terrazas, jardines, áticos y porches. Diseño sereno, materiales preparados para exterior y entrega en España península.

**CTA principal:**

> Ver colecciones

**CTA secundario:**

> Te ayudamos con tu terraza

#### Bloque 2 — Barra de confianza

```txt
Proveedores españoles
Entrega en península
Hasta 1 mes según producto
Garantía del proveedor
Asesoramiento humano
```

#### Bloque 3 — Compra por espacio

- Terrazas
- Jardines
- Áticos
- Porches
- Balcones
- Piscina

#### Bloque 4 — Colecciones principales

- Salones de exterior
- Comedores de exterior
- Tumbonas y relax
- Sombra y parasoles

#### Bloque 5 — Por qué Santavila

Título:

> Exterior con criterio.

Contenido:

- Selección curada.
- Proveedores españoles.
- Producto explicado sin letra pequeña.
- Materiales pensados para exterior.
- Entrega clara en España península.

#### Bloque 6 — Productos héroe

Mostrar solo productos fuertes:

- buen margen,
- buena foto,
- plazo razonable,
- ficha completa,
- valor estético.

#### Bloque 7 — Materiales

Crear accesos:

- aluminio,
- madera,
- HPL,
- cuerda,
- tejidos exteriores.

#### Bloque 8 — Asesoramiento

Título:

> ¿No sabes por dónde empezar?

Texto:

> Cuéntanos las medidas de tu terraza, jardín o porche y te ayudamos a elegir piezas que encajen por estilo, uso y presupuesto.

CTA:

> Pedir asesoramiento

#### Bloque 9 — Profesionales

Título:

> Proyectos para profesionales.

Texto:

> Trabajamos con interioristas, arquitectos, hoteles boutique, casas rurales y restaurantes que buscan mobiliario exterior con criterio, plazos claros y atención directa.

CTA:

> Ver área profesional

#### Bloque 10 — Contenido editorial

- Cómo elegir sofá exterior.
- Cómo amueblar un ático.
- Qué material aguanta mejor el sol.
- Guía de medidas para terraza.

---

## 7. PLP — páginas de colección

### 7.1 Objetivo de una PLP

Una página de colección no debe ser una rejilla de productos. Debe ayudar a decidir.

### 7.2 Estructura recomendada

1. Hero de colección.
2. Descripción útil.
3. Accesos rápidos por uso.
4. Filtros.
5. Productos.
6. Bloque de ayuda.
7. Guía de compra.
8. FAQs.
9. Enlaces internos a materiales y espacios.

### 7.3 Filtros necesarios

```txt
Precio
Disponibilidad
Plazo de entrega
Material
Color
Medidas
Número de plazas
Espacio recomendado
Uso cubierto / no cubierto
Nivel de mantenimiento
Proveedor
Garantía
Colección Santavila
```

### 7.4 Ejemplo para colección “Sofás de exterior”

Título:

> Sofás de exterior para terrazas, jardines y porches.

Texto:

> Selección de sofás exteriores de proveedores españoles, pensados para crear zonas de descanso cómodas y duraderas al aire libre. Filtra por medida, material, número de plazas y plazo de entrega.

Subcategorías:

- Sofás 2 plazas
- Sofás 3 plazas
- Sofás modulares
- Conjuntos de exterior
- Sofás para terraza pequeña
- Sofás para porche cubierto

---

## 8. PDP — ficha de producto premium

### 8.1 Objetivo

La ficha debe reducir miedo.

En mobiliario exterior premium, el usuario duda por:

- tamaño,
- material,
- resistencia,
- entrega,
- garantía,
- montaje,
- devolución,
- si quedará bien,
- si el precio está justificado.

La PDP debe responder a todo esto.

### 8.2 Estructura superior

1. Galería con imagen ambiente.
2. Imagen de detalle de material.
3. Imagen con escala o medidas.
4. Nombre claro.
5. Precio.
6. Plazo de entrega.
7. Tipo de entrega.
8. Garantía.
9. CTA principal.
10. CTA secundario de asesoramiento.

### 8.3 Módulo de confianza junto al precio

Ejemplo:

```txt
Entrega en España península
Plazo estimado: 15-30 días
Entrega mediante transporte
Garantía según proveedor
Asesoramiento disponible por WhatsApp
```

### 8.4 Información obligatoria

Cada producto debe incluir:

- medidas completas,
- materiales,
- mantenimiento,
- uso recomendado,
- si requiere montaje,
- qué incluye,
- número de bultos,
- peso si está disponible,
- garantía,
- origen/proveedor español,
- plazo,
- condiciones de entrega.

### 8.5 Bloques de contenido

#### Bloque “Por qué esta pieza”

Explicar en 3-5 líneas por qué existe ese producto en Santavila.

#### Bloque “Encaja si…”

Ejemplo:

```txt
Encaja si buscas un sofá exterior cómodo para una terraza amplia, porche o zona de piscina. Recomendado para espacios donde se quiera una pieza protagonista sin sensación pesada.
```

#### Bloque “Materiales y mantenimiento”

Explicar el comportamiento del material.

#### Bloque “Entrega”

Explicar sin ambigüedad:

```txt
Este producto se entrega en España península mediante transporte. No incluye montaje ni subida especial salvo indicación expresa. El plazo estimado es de hasta 30 días según disponibilidad del proveedor.
```

#### Bloque “Garantía”

```txt
Garantía ofrecida por el proveedor. La cobertura concreta puede variar por familia de producto y se indicará en la documentación del pedido.
```

#### Bloque “Completa el espacio”

No hacer cross-sell aleatorio. Mostrar piezas compatibles:

- mesa auxiliar,
- sillón,
- parasol,
- tumbona,
- comedor,
- cojines,
- producto de la misma colección estética.

---

## 9. Sistema de datos Shopify

El dato estructurado es la base de todo. Sin dato, no hay filtros buenos, no hay PDP premium, no hay automatización y no hay escalabilidad.

### 9.1 Metafields de producto recomendados

Namespace sugerido: `santavila`

| Campo | Tipo | Uso |
|---|---|---|
| `santavila.proveedor` | referencia/metaobject o texto | proveedor |
| `santavila.fabricado_espana` | boolean | indicar si realmente está fabricado en España |
| `santavila.proveedor_espanol` | boolean | indicar proveedor español |
| `santavila.provincia_origen` | texto | origen cuando se pueda comunicar |
| `santavila.plazo_min_dias` | número | plazo mínimo |
| `santavila.plazo_max_dias` | número | plazo máximo |
| `santavila.tipo_entrega` | lista | transporte, especial, bajo consulta |
| `santavila.montaje_incluido` | boolean | en principio false |
| `santavila.subida_incluida` | boolean | en principio false |
| `santavila.garantia_resumen` | texto | garantía visible |
| `santavila.garantia_detalle` | rich text | detalle de garantía |
| `santavila.material_estructura` | texto/lista | aluminio, madera, acero, etc. |
| `santavila.material_superficie` | texto/lista | HPL, cerámica, madera, etc. |
| `santavila.material_textil` | texto/lista | cojines, cuerda, tejido |
| `santavila.uso_recomendado` | lista | terraza, jardín, porche, piscina |
| `santavila.uso_cubierto` | boolean/lista | cubierto, descubierto, ambos |
| `santavila.nivel_mantenimiento` | lista | bajo, medio, alto |
| `santavila.medidas_resumen` | texto | resumen visible |
| `santavila.ancho_cm` | número | filtro |
| `santavila.fondo_cm` | número | filtro |
| `santavila.alto_cm` | número | filtro |
| `santavila.peso_kg` | número | logística |
| `santavila.numero_bultos` | número | logística |
| `santavila.dimensiones_bultos` | texto | logística |
| `santavila.estilo` | lista | contemporáneo, mediterráneo, natural |
| `santavila.espacio_principal` | lista | ático, terraza, porche, jardín |
| `santavila.coleccion_santavila` | referencia/metaobject | colección propia |
| `santavila.producto_hero` | boolean | destacar |
| `santavila.exclude_feed` | boolean | excluir de feed si no conviene |
| `santavila.margen_porcentaje` | número decimal | uso interno |
| `santavila.margen_euros` | número decimal | uso interno |
| `santavila.prioridad_comercial` | lista | alta, media, baja |
| `santavila.estado_enriquecimiento` | lista | pendiente, revisado, completo |

### 9.2 Metaobjects recomendados

#### `sv_material_guide`

Para guías reutilizables de materiales.

Campos:

- nombre,
- descripción,
- ventajas,
- cuidados,
- recomendado para,
- no recomendado para,
- imagen,
- icono.

#### `sv_delivery_type`

Para tipos de entrega.

Campos:

- nombre,
- descripción,
- incluye,
- no incluye,
- plazo estimado,
- condiciones.

#### `sv_warranty_policy`

Para garantías por proveedor o familia.

Campos:

- proveedor,
- familia,
- duración,
- cobertura,
- exclusiones,
- procedimiento.

#### `sv_supplier`

Para proveedor.

Campos:

- nombre interno,
- origen,
- provincia,
- plazo estándar,
- contacto operativo,
- condiciones,
- score proveedor,
- notas internas.

#### `sv_collection_story`

Para colecciones Santavila.

Campos:

- nombre,
- claim,
- descripción,
- estilo,
- espacios recomendados,
- productos asociados,
- imagen hero.

#### `sv_space_solution`

Para páginas por espacio.

Campos:

- espacio,
- problema que resuelve,
- recomendaciones,
- medidas orientativas,
- productos recomendados,
- imagen.

#### `sv_faq`

Para preguntas frecuentes reutilizables.

Campos:

- pregunta,
- respuesta,
- familia,
- producto,
- visibilidad.

#### `sv_care_guide`

Para mantenimiento.

Campos:

- material,
- frecuencia,
- limpieza,
- evitar,
- recomendaciones.

---

## 10. Naming de productos

### 10.1 Problema actual

Muchos productos tienen nombres demasiado técnicos, mezclados con inglés o con traducción literal.

### 10.2 Sistema recomendado

Formato:

```txt
[Tipo de producto] [rasgo principal] · [material/uso] | [medida]
```

Ejemplos:

```txt
Sofá exterior 3 plazas · aluminio y cuerda | 196 cm
Mesa comedor exterior · tablero HPL | 150×90 cm
Tumbona exterior regulable · estructura ligera
Parasol terraza · diámetro 300 cm
```

### 10.3 No usar

- nombres en inglés,
- nombres excesivamente largos,
- nombres de proveedor sin sentido,
- títulos tipo “Outdoor armchair versatile style”,
- nombres repetidos sin diferenciación.

---

## 11. Sistema visual y dirección artística

### 11.1 Dirección visual

Santavila debe verse como:

- mediterránea,
- española,
- calmada,
- cálida,
- contemporánea,
- real,
- premium sin exceso.

### 11.2 Evitar

- resort tropical,
- lujo exagerado,
- mansiones irreales,
- renders fríos,
- saturación de color,
- imágenes genéricas de proveedor sin dirección,
- escenas que no parezcan España.

### 11.3 Referencias de ambiente

- ático en Madrid o Valencia,
- terraza en costa mediterránea,
- porche en vivienda gallega o andaluza,
- patio con cal, piedra y sombra,
- jardín familiar premium,
- casa rural cuidada,
- hotel boutique pequeño,
- restaurante con patio elegante.

### 11.4 Paleta sugerida

```txt
Base cálida: #F7F2EA
Arena: #D8C7AE
Terracota suave: #B87555
Verde oliva: #6F765D
Carbón suave: #252525
Blanco cal: #FAF8F3
Azul sombra: #A9B7BD
```

### 11.5 Tipografía

Recomendación:

- Serif elegante para titulares si el theme lo permite.
- Sans limpia para texto y ecommerce.

Ejemplo:

- Titulares: Cormorant Garamond / Canela-like / Playfair Display si se quiere algo más accesible.
- Texto/UI: Inter / Neue Haas / Plus Jakarta Sans.

### 11.6 Fotografía generada con IA

La IA debe generar:

- escenas de contexto,
- fondos,
- inspiración,
- campañas,
- guías,
- visuales editoriales.

Debe evitar generar:

- producto distinto al real,
- estructura incorrecta,
- medidas engañosas,
- colores inexistentes,
- promesas visuales que no se correspondan con el SKU.

---

## 12. Prompt base para Higgsfield AI

```txt
Create a premium Mediterranean outdoor furniture scene for a Spanish ecommerce brand called Santavila.

Scene:
A realistic Spanish terrace / garden / porch with soft Mediterranean light, natural shadows, warm stone, limewashed walls, olive trees, neutral textiles, calm elegant styling, and a believable residential setting.

Style:
Premium accessible, contemporary Mediterranean, understated, warm, editorial ecommerce, realistic, not luxury mansion, not tropical resort, not generic stock photo.

Product:
Keep the outdoor furniture piece visually accurate, with correct proportions, materials and color. Do not alter the structure, scale or design of the furniture. The product must remain commercially truthful.

Mood:
Quiet elegance, lived-in but clean, Spanish outdoor lifestyle, calm summer afternoon, natural textures, no excessive decoration.

Output:
High-end ecommerce hero image, realistic photography, natural shadows, suitable for Shopify homepage and product storytelling.
```

### Variantes por espacio

#### Terraza urbana

```txt
Spanish urban rooftop terrace, 20-30 square meters, warm evening light, planters, ceramic floor, soft shadows, calm premium atmosphere.
```

#### Porche

```txt
Covered Spanish porch, natural stone floor, white limewashed wall, olive tree, soft linen textiles, warm neutral palette.
```

#### Jardín

```txt
Mediterranean garden in Spain, gravel and natural stone, restrained vegetation, calm premium outdoor living area, realistic residential scale.
```

#### Hotel boutique

```txt
Small boutique hotel patio in Spain, refined outdoor seating, warm stone, quiet hospitality atmosphere, elegant but not ostentatious.
```

---

## 13. Sistema de confianza

### 13.1 Bloques globales

Estos mensajes deben estar en home, PDP, PLP, carrito y ayuda.

```txt
Entrega en España península
Proveedores españoles
Plazo máximo estimado: hasta 30 días
Garantía según proveedor
Asesoramiento humano
```

### 13.2 Página “Entrega”

Debe explicar:

- dónde se entrega,
- qué incluye el transporte,
- qué no incluye,
- plazos,
- productos bajo pedido,
- cómo se comunica la entrega,
- qué hacer si llega dañado,
- condiciones de producto voluminoso,
- contacto.

Texto base:

> Realizamos entregas en España península mediante transporte. El servicio estándar no incluye montaje ni subida especial a vivienda salvo indicación expresa. Cada producto muestra su plazo estimado de entrega, que puede variar según proveedor y disponibilidad, con un máximo habitual de hasta 30 días.

### 13.3 Página “Garantía”

Debe explicar:

- garantía legal,
- garantía del proveedor,
- diferencias por producto,
- procedimiento de incidencia,
- fotos necesarias,
- plazos de comunicación,
- exclusiones.

Texto base:

> Los productos Santavila cuentan con la garantía correspondiente ofrecida por cada proveedor y conforme a la normativa aplicable. La cobertura concreta puede variar según familia de producto, material y fabricante. Ante cualquier incidencia, centralizamos la gestión para ayudarte con el proveedor.

### 13.4 Página “Mantenimiento”

Crear guías por material:

- aluminio,
- madera,
- HPL,
- cuerda,
- tejidos,
- cojines,
- parasoles.

---

## 14. Roadmap operativo

### 14.1 Proceso de alta de producto

```txt
1. Producto recibido del proveedor
2. Revisión de margen por SKU
3. Validación de plazo
4. Validación de garantía
5. Validación de fotos
6. Asignación de categoría
7. Asignación de espacio
8. Asignación de materiales
9. Enriquecimiento de descripción
10. Creación de módulos PDP
11. Revisión SEO
12. Revisión visual
13. Publicación
14. Control semanal
```

### 14.2 Score de producto

Cada SKU debe tener una puntuación interna de 1 a 5:

| Criterio | Peso |
|---|---|
| Margen | 25% |
| Calidad visual | 20% |
| Plazo | 20% |
| Diferenciación | 15% |
| Potencial SEO | 10% |
| Potencial colección | 10% |

Acciones:

- Score 4-5: producto destacado.
- Score 3: producto visible.
- Score 2: producto revisable.
- Score 1: ocultar o no promocionar.

### 14.3 Score de proveedor

Cada proveedor debe evaluarse semanal o mensualmente:

| Criterio | Descripción |
|---|---|
| OTIF | entregas a tiempo y completas |
| Incidencias | daños, errores, reclamaciones |
| Calidad de dato | stock, fotos, fichas, medidas |
| Respuesta | velocidad de atención |
| Garantía | facilidad de gestión |
| Margen | rentabilidad |
| Plazo | cumplimiento real |

### 14.4 Incidencias

Crear protocolo:

```txt
1. Cliente comunica incidencia
2. Pedir fotos del embalaje
3. Pedir fotos del daño
4. Pedir número de pedido
5. Registrar SKU y proveedor
6. Contactar proveedor
7. Resolver con sustitución, reparación, abono o compensación
8. Marcar incidencia en score proveedor
```

---

## 15. Shopify Flow — automatizaciones recomendadas

### 15.1 Pedido creado

Trigger:

```txt
Order created
```

Condiciones:

- proveedor,
- importe,
- plazo,
- familia,
- producto voluminoso.

Acciones:

- etiquetar pedido por proveedor,
- enviar email interno,
- crear tarea,
- avisar si plazo > 21 días,
- avisar si importe > 1.000€,
- avisar si producto requiere validación manual.

### 15.2 Producto con bajo stock

Trigger:

```txt
Inventory quantity changed
```

Acciones:

- etiquetar como “stock bajo”,
- ocultar del feed si procede,
- avisar a responsable,
- cambiar mensaje de PDP si el plazo aumenta.

### 15.3 Producto enriquecido pendiente

Trigger:

```txt
Product created
```

Acciones:

- añadir tag `pendiente_enriquecimiento`,
- revisar metafields obligatorios,
- no publicar hasta completar datos críticos.

### 15.4 Pedido con producto de plazo largo

Trigger:

```txt
Order created
```

Condición:

```txt
plazo_max_dias > 21
```

Acciones:

- tag `plazo_largo`,
- email interno,
- email personalizado al cliente,
- seguimiento a los 7 días.

### 15.5 Pedido premium

Trigger:

```txt
Order created
```

Condición:

```txt
order_total > 1000
```

Acciones:

- revisión manual,
- contacto humano,
- confirmar entrega,
- seguimiento postventa.

---

## 16. SEO sin inversión publicitaria inicial

Como ahora no hay presupuesto de marketing, el foco debe ser:

1. arquitectura,
2. contenido,
3. indexación,
4. fichas enriquecidas,
5. categorías transaccionales,
6. guías de compra.

### 16.1 Categorías prioritarias

```txt
Sofás de exterior
Sofás de terraza
Conjuntos de jardín
Mesas de exterior
Mesas comedor exterior
Sillas de exterior
Tumbonas de exterior
Parasoles de terraza
Muebles para ático
Muebles para terraza
Muebles para porche
Muebles de exterior fabricados en España
```

### 16.2 Guías prioritarias

```txt
Cómo elegir un sofá exterior
Cómo amueblar una terraza pequeña
Qué material es mejor para muebles de exterior
Aluminio vs madera en exterior
Cómo cuidar cojines de exterior
Medidas recomendadas para comedor exterior
Cómo elegir una tumbona
Cómo crear una zona chill out en terraza
Cómo amueblar un ático
Muebles de exterior para casas rurales y hoteles boutique
```

### 16.3 Páginas por espacio

```txt
Muebles para terraza
Muebles para ático
Muebles para jardín
Muebles para porche
Muebles para balcón
Muebles para piscina
Muebles para patio
```

### 16.4 Páginas por material

```txt
Muebles exterior aluminio
Muebles exterior madera
Mesas exterior HPL
Muebles exterior cuerda
Tejidos para exterior
```

---

## 17. CRO — conversión

### 17.1 KPIs base

Aunque no haya ads, medir:

- sesiones,
- tasa de conversión,
- add to cart,
- view item,
- begin checkout,
- scroll PDP,
- clic en WhatsApp/contacto,
- búsquedas internas,
- productos más vistos,
- productos con abandono,
- categorías más vistas,
- productos sin interacción.

### 17.2 Eventos recomendados

```txt
view_item
select_item
add_to_cart
begin_checkout
purchase
click_whatsapp
click_delivery_info
click_warranty_info
click_material_guide
click_professional_form
newsletter_signup
```

### 17.3 Mejoras CRO prioritarias

1. CTA claro.
2. Plazo visible.
3. Garantía visible.
4. Entrega visible.
5. Fotos de contexto.
6. Medidas claras.
7. WhatsApp visible.
8. FAQs en PDP.
9. Cross-sell coherente.
10. Colecciones por espacio.

---

## 18. Área profesionales

Aunque el foco inicial sea residencial, se debe crear una base B2B ligera.

### 18.1 Página “Profesionales”

Contenido:

- para quién es,
- qué ofrecemos,
- proveedores españoles,
- presupuesto por proyecto,
- asesoramiento,
- documentación técnica,
- condiciones según volumen,
- contacto directo.

### 18.2 Formulario

Campos:

```txt
Nombre
Empresa
Tipo de profesional
Email
Teléfono
Provincia
Tipo de proyecto
Presupuesto aproximado
Fecha objetivo
Productos de interés
Mensaje
```

### 18.3 Profesionales objetivo

- interioristas,
- arquitectos,
- paisajistas,
- hoteles boutique,
- casas rurales,
- restaurantes,
- promotores pequeños,
- estudios de decoración.

---

## 19. Backlog priorizado

## Fase 0 — Limpieza urgente | Semana 1

Objetivo: dejar de parecer Shopify sin pulir.

Tareas:

- Unificar idioma español.
- Cambiar “FREE SHIPPING TO MAINLAND SPAIN” por “Envío a España península”.
- Revisar menú.
- Revisar footer.
- Eliminar textos genéricos en inglés.
- Revisar nombres de productos.
- Revisar etiquetas “Oferta”.
- Crear claim principal.
- Crear barra de confianza.
- Crear página de entrega.
- Crear página de garantía.
- Crear página de contacto real.
- Añadir WhatsApp o contacto visible.
- Revisar legal, privacidad y condiciones.

## Fase 1 — Modelo de dato | Semanas 1-2

Objetivo: estructurar catálogo.

Tareas:

- Crear metafields.
- Crear metaobjects.
- Crear plantilla maestra de importación.
- Clasificar +200 SKUs.
- Añadir margen por SKU como dato interno.
- Asignar proveedor.
- Asignar plazo.
- Asignar garantía.
- Asignar material.
- Asignar espacio.
- Asignar prioridad comercial.
- Marcar productos héroe.

## Fase 2 — PDP premium | Semanas 2-4

Objetivo: convertir fichas en páginas de venta.

Tareas:

- Crear template PDP por familia.
- Añadir bloque de entrega.
- Añadir bloque de garantía.
- Añadir bloque de materiales.
- Añadir mantenimiento.
- Añadir “encaja si”.
- Añadir medidas.
- Añadir FAQs.
- Añadir productos compatibles.
- Añadir CTA de asesoramiento.
- Revisar 20 productos héroe primero.

## Fase 3 — Home y PLP | Mes 2

Objetivo: cambiar percepción de marca.

Tareas:

- Rediseñar home.
- Crear compra por espacio.
- Crear colecciones principales.
- Crear PLP para sofás, mesas, sillas, tumbonas y parasoles.
- Añadir textos SEO útiles.
- Añadir filtros.
- Añadir bloques de ayuda.
- Añadir enlaces internos.

## Fase 4 — Dirección visual IA | Mes 2

Objetivo: dejar de depender visualmente del proveedor.

Tareas:

- Definir guía visual.
- Crear prompts Higgsfield.
- Generar escenas por espacio.
- Crear banco de imágenes hero.
- Crear imágenes para guías.
- Crear imágenes de colección.
- Revisar que no alteren el producto real.
- Crear sistema de assets.

## Fase 5 — SEO y contenido | Meses 2-4

Objetivo: captar tráfico orgánico y mejorar confianza.

Tareas:

- Crear guías de compra.
- Crear páginas por espacio.
- Crear páginas por material.
- Crear contenido de mantenimiento.
- Crear comparativas.
- Crear enlaces internos.
- Optimizar títulos y metadescripciones.
- Preparar rich snippets donde proceda.

## Fase 6 — Profesionales | Meses 3-4

Objetivo: abrir canal B2B ligero.

Tareas:

- Crear página profesionales.
- Crear formulario.
- Crear condiciones.
- Crear proceso interno de presupuesto.
- Crear email automático.
- Crear catálogo PDF simple si procede.
- Crear base de contactos profesionales.

## Fase 7 — Optimización operativa | Meses 3-6

Objetivo: que el modelo no se rompa por dentro.

Tareas:

- Score proveedor.
- Score producto.
- Revisión semanal de catálogo.
- Control de incidencias.
- Control de márgenes.
- Control de plazos.
- Automatizaciones Shopify Flow.
- Dashboard interno de SKUs.

---

## 20. Prompt para Claude Code / Antigravity / Shopify AI Toolkit

```txt
Actúa como Senior Shopify Ecommerce Architect, UX Lead y Theme Developer especializado en tiendas premium de mobiliario.

Contexto:
Santavila.com es una tienda Shopify de mobiliario exterior premium accesible para España península. Actualmente ya tiene más de 200 productos/SKUs subidos, 2 proveedores españoles, margen por SKU, entrega solo transporte, plazo máximo de hasta 30 días y garantía dependiente del proveedor. No hay presupuesto de marketing de pago en esta fase, por lo que el foco está en UX, UI, arquitectura, CRO, SEO base, estructura de datos y experiencia premium.

Objetivo:
Transformar Santavila de una tienda-catálogo en una marca ecommerce premium especialista en exterior español, con diseño mediterráneo contemporáneo, información de producto clara y una experiencia de compra confiable.

Restricciones:
- No usar headless en esta fase.
- No inventar información de producto.
- No prometer montaje.
- No prometer subida a vivienda.
- No prometer fabricación española si no está validada por SKU.
- No abusar de descuentos permanentes.
- No romper el checkout nativo de Shopify.
- Mantener compatibilidad con el theme actual salvo que se indique lo contrario.
- Trabajar con metafields, metaobjects, Liquid, secciones del theme y Shopify Flow cuando proceda.

Prioridades:
1. Auditoría técnica del theme y contenido actual.
2. Unificar idioma español.
3. Crear arquitectura ecommerce: Colecciones, Espacios, Materiales, Profesionales, Inspiración y Ayuda.
4. Crear estructura de metafields y metaobjects.
5. Crear template PDP premium por familia.
6. Crear home premium con claim, confianza, espacios, colecciones, materiales y asesoramiento.
7. Crear PLP enriquecidas con texto útil, filtros y bloques de ayuda.
8. Crear sistema de confianza: entrega, garantía, mantenimiento y contacto.
9. Preparar SEO base.
10. Preparar automatizaciones Shopify Flow para pedidos, proveedores, plazos e incidencias.

Entregables:
- Auditoría del estado actual.
- Lista de cambios priorizados.
- Propuesta de estructura de theme.
- Esquema de metafields.
- Esquema de metaobjects.
- Templates Liquid/JSON necesarios.
- Backlog por fases.
- Cambios aplicables con mínimo riesgo.
- Instrucciones de validación antes de publicar.

Criterio de calidad:
La tienda debe parecer una marca especialista premium, no un catálogo de proveedor. En menos de 10 segundos el usuario debe entender qué vende Santavila, por qué confiar, dónde entrega, qué estilo tiene y cómo pedir ayuda.
```

---

## 21. Prompt para enriquecer productos

```txt
Actúa como ecommerce copywriter experto en mobiliario exterior premium.

Producto:
[PEGAR DATOS DEL PRODUCTO]

Marca:
Santavila — mobiliario exterior seleccionado de proveedores españoles para terrazas, jardines, áticos y porches.

Tono:
Sereno, experto, cálido, preciso, premium accesible. No exagerado. No low-cost. No usar frases vacías como “máxima elegancia” o “sofisticación incomparable”.

Objetivo:
Crear una ficha de producto que ayude a comprar reduciendo dudas sobre uso, medidas, materiales, entrega, garantía y mantenimiento.

No inventes:
- materiales,
- garantía,
- fabricación,
- medidas,
- montaje,
- resistencia,
- certificaciones,
- stock,
- plazo.

Devuelve:
1. Nombre de producto optimizado.
2. Descripción corta.
3. Descripción larga.
4. Bloque “Por qué esta pieza”.
5. Bloque “Encaja si…”.
6. Materiales.
7. Mantenimiento.
8. Entrega.
9. Garantía.
10. FAQs.
11. Meta title.
12. Meta description.
13. Texto ALT para imágenes.
14. Tags recomendados.
15. Metafields que faltan.
```

---

## 22. Prompt para revisión de catálogo

```txt
Actúa como Ecommerce Manager y Category Manager de Santavila.

Te voy a pasar un CSV/Excel exportado de Shopify con productos de mobiliario exterior.

Objetivo:
Clasificar, priorizar y sanear el catálogo para que la tienda no parezca un almacén, sino una marca premium curada.

Analiza cada SKU por:
- margen,
- precio,
- proveedor,
- plazo,
- categoría,
- material,
- calidad del nombre,
- calidad de imagen,
- potencial comercial,
- potencial SEO,
- si debe ser producto héroe,
- si debe ocultarse,
- si debe excluirse de feed,
- si necesita enriquecimiento.

Devuelve:
1. Problemas detectados.
2. Productos héroe.
3. Productos secundarios.
4. Productos a revisar.
5. Productos a ocultar.
6. Cambios de nombre.
7. Categorías sugeridas.
8. Espacios sugeridos.
9. Metafields faltantes.
10. Acciones en Shopify.
```

---

## 23. Checklist de publicación de producto

Antes de publicar un producto, debe cumplir:

```txt
[ ] Nombre en español
[ ] Categoría correcta
[ ] Colección correcta
[ ] Espacio recomendado
[ ] Material principal
[ ] Medidas completas
[ ] Plazo de entrega
[ ] Tipo de entrega
[ ] Garantía
[ ] Mantenimiento
[ ] Proveedor asignado
[ ] Margen validado
[ ] Imagen principal correcta
[ ] Imagen ambiente o IA validada
[ ] Descripción reescrita
[ ] SEO title
[ ] SEO description
[ ] ALT de imágenes
[ ] Cross-sell coherente
[ ] No hay promesas no verificadas
```

---

## 24. Decisiones pendientes

Todavía quedan decisiones que conviene cerrar:

1. Confirmar si todos los productos son realmente fabricados en España o solo de proveedores españoles.
2. Definir si se puede comunicar provincia de fabricación.
3. Confirmar condiciones exactas de garantía de cada proveedor.
4. Confirmar si algún proveedor permite entrega especial o montaje bajo presupuesto.
5. Confirmar si habrá WhatsApp comercial.
6. Confirmar si se usará financiación o pago fraccionado.
7. Confirmar si se quiere newsletter.
8. Confirmar si se quiere área profesional desde fase 1 o fase 2.
9. Confirmar theme actual y límites de personalización.
10. Confirmar si se va a usar app de filtros avanzada o solo filtros nativos.
11. Confirmar si se usará Shopify Markets solo para España península o preparado para Portugal más adelante.
12. Confirmar si se va a crear catálogo PDF para profesionales.
13. Confirmar política de devoluciones para producto voluminoso.
14. Confirmar si el envío está incluido en todos los productos o solo algunos.
15. Confirmar si hay productos bajo pedido y cómo se comunica.

---

## 25. Orden recomendado inmediato

### Esta semana

1. Auditoría completa del theme.
2. Limpieza de idioma.
3. Revisión de menú.
4. Revisión de footer.
5. Revisión de claims.
6. Creación de páginas de entrega, garantía y mantenimiento.
7. Creación de plantilla maestra de datos.
8. Selección de 20 productos héroe.
9. Redacción de 5 PDP premium piloto.
10. Definición visual para IA.

### Próximas 2 semanas

1. Crear metafields.
2. Crear metaobjects.
3. Enriquecer 50 SKUs prioritarios.
4. Rediseñar home.
5. Rediseñar PDP.
6. Crear PLP de sofás, mesas, sillas, tumbonas y parasoles.
7. Crear página “Profesionales”.
8. Crear 3 guías SEO.

### Primer mes

1. Tener una tienda coherente visualmente.
2. Tener los productos principales bien explicados.
3. Tener entrega y garantía claras.
4. Tener arquitectura por espacio.
5. Tener sistema de datos escalable.
6. Tener primeras imágenes IA controladas.
7. Tener base SEO correcta.
8. Tener proceso operativo con proveedores.

---

## 26. Resultado esperado

Al terminar esta primera fase, Santavila debe dejar de parecer una tienda Shopify con productos cargados y empezar a parecer:

> una marca española especializada en mobiliario exterior, con estética propia, criterio de selección, datos claros, producto bien explicado y una experiencia de compra que reduce riesgo.

Ese es el punto de partida real para después activar marketing, SEO más fuerte, profesionales, internacionalización y escalado.
