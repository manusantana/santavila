# BACKLOG_SANTAVILA.md

**Snapshot:** 2026-05-06
**Base:** hallazgos de [`AUDITORIA_SANTAVILA.md`](AUDITORIA_SANTAVILA.md) + estructura de fases de [`../../plan_santavila_shopify/plan_santavila.md`](../../plan_santavila_shopify/plan_santavila.md).

## Cómo leer este backlog

Cada tarea tiene un **ID estable** (`F0-01`, `F1-02`…) que se puede citar en commits, PRs, mensajes y los otros documentos del proyecto. Los campos de cada ficha:

| Campo | Significado |
|-------|-------------|
| **Prioridad** | P0 (urgente, bloquea otras tareas) · P1 (importante, fase actual) · P2 (medio plazo) · P3 (mejora) |
| **Impacto** | Alto / Medio / Bajo — efecto sobre conversión, percepción de marca o eficiencia operativa |
| **Dificultad** | Baja (1-2 h) · Media (medio día) · Alta (varios días) |
| **Riesgo** | Probabilidad de romper algo en producción si se ejecuta mal |
| **Dependencia** | IDs de tareas que deben completarse antes |
| **Requiere** | `Admin` (UI Shopify) · `Theme` (código Liquid/JSON) · `Datos` (metafields/CSV) · `Contenido` (texto/imagen) · `App` |
| **Validación** | Cómo confirmar que la tarea está bien cerrada antes de pasar a la siguiente |

**Regla operativa global:** ningún cambio en producción sin validación previa. Todo lo de theme se prueba primero en theme duplicado (`shopify theme push --unpublished`).

---

## FASE 0 — Limpieza urgente (Semana 1)

> Objetivo: dejar de parecer "Shopify con productos cargados" sin tocar arquitectura todavía. Solo cambios visibles que se ejecutan rápido y dan percepción de marca seria.

### F0-01 · Auditar y eliminar `compareAtPrice` permanente en todos los productos

- **Prioridad:** P0
- **Impacto:** Alto (toda la tienda parece "siempre rebajada")
- **Dificultad:** Media (script + criterio comercial)
- **Riesgo:** Bajo si se hace producto a producto; medio si se hace en bulk
- **Dependencia:** —
- **Requiere:** Datos · Admin
- **Archivos:** script Python nuevo (`audit_compare_at_price.py`) + Admin Shopify
- **Pasos:**
  1. Listar todos los productos con `variants.compareAtPrice IS NOT NULL` vía Admin GraphQL.
  2. Determinar criterio: ¿`price` actual es el real Santavila y `compareAtPrice` era el "PVP recomendado" del proveedor? Si sí: vaciar `compareAtPrice` salvo en productos que estén realmente en campaña.
  3. Pasar `compareAtPrice → null` en bulk con `productVariantsBulkUpdate`.
- **Validación:** abrir 5 PDPs aleatorios, confirmar que el precio se renderea sin tachado y sin etiqueta "Sale" / "Oferta".
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.1#1` — BRANDON-1 con `compareAtPrice=980`, `price=809.92`.

### F0-02 · Mover proveedor real a metafield interno y unificar `vendor = "Santavila"`

- **Prioridad:** P0
- **Impacto:** Alto (vendor se renderea en muchos themes)
- **Dificultad:** Media
- **Riesgo:** Medio — puede romper integraciones que filtran por vendor
- **Dependencia:** F1-01 (necesita el metafield `santavila.proveedor` ya creado)
- **Requiere:** Datos · Admin
- **Pasos:**
  1. Crear metafield `santavila.proveedor` (tipo `single_line_text_field` o referencia a metaobject `sv_supplier`).
  2. Para cada producto: copiar valor actual de `vendor` (Hevea/Balliu) a `santavila.proveedor`.
  3. Actualizar `vendor = "Santavila"` en todos los productos.
- **Validación:** filtro de catálogo en home/PLP no muestra "Hevea" ni "Balliu" como vendor visible. Filtros internos de exportación siguen funcionando vía metafield.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.5` — vendor hoy = Hevea/Balliu, expuesto.

### F0-03 · Limpiar tags expuestos al cliente

- **Prioridad:** P0
- **Impacto:** Alto
- **Dificultad:** Baja
- **Riesgo:** Bajo (tags solo afectan filtrado y URL)
- **Dependencia:** F0-02 (proveedor ya en metafield)
- **Requiere:** Datos · Admin
- **Pasos:**
  1. Eliminar tags `Hevea` y `Balliu` (235 productos afectados).
  2. Eliminar tag `hostelería` de PDP visible al cliente residencial — si interesa para B2B, mover a metafield `santavila.uso_recomendado` con valor opcional `"hostelería"`.
  3. Investigar origen de `match-verde / match-rojo / match-amarillo` (probable app B2B). Si son internos: añadir prefijo `internal-` o moverlos a un namespace de metafields.
- **Validación:** filtro `tag:Hevea` y `tag:Balliu` devuelve 0 productos. PLP no muestra opciones de filtro con esos nombres.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.1#3` y `#2`.

### F0-04 · Normalizar `productType` a 8-10 valores limpios

- **Prioridad:** P1
- **Impacto:** Medio
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Datos · Admin
- **Pasos:**
  1. Mapear los 21 productTypes actuales a un set canónico: `Sofá`, `Sillón`, `Mesa`, `Mesa centro`, `Mesa comedor`, `Silla`, `Tumbona`, `Parasol`, `Conjunto`, `Reposapiés`, `Banco`, `Funda`, `Accesorio`, `Pérgola`, `Cama balinesa`, `Balancín`.
  2. Ejecutar `productUpdate` en bulk para los productos con `productType` no canónico (`Sofa`→`Sofá`, `Accesorios`→`Accesorio`, etc.).
- **Validación:** `query{ products }` agregado por `productType` muestra ≤16 valores únicos sin duplicados ortográficos.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.2 Consistencia`.

### F0-05 · Corregir typo "Sofas" → "Sofás" + alinear handle/title

- **Prioridad:** P1
- **Impacto:** Medio (H1 + URL + visibilidad SEO)
- **Dificultad:** Baja
- **Riesgo:** Medio (cambiar handle requiere redirect 301)
- **Dependencia:** —
- **Requiere:** Admin · Contenido
- **Pasos:**
  1. Renombrar título de colección `sillones-de-exterior` de `"Sofas de exterior"` a `"Sofás de exterior"`.
  2. Cambiar handle de `sillones-de-exterior` a `sofas-de-exterior` (más coherente con el título).
  3. Crear redirect 301: `/collections/sillones-de-exterior` → `/collections/sofas-de-exterior`.
- **Validación:** abrir URL antigua, confirmar 301 a la nueva. H1 sin typo.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.1#7`.

### F0-06 · Añadir ALT a los 71 productos sin texto alternativo en imagen principal

- **Prioridad:** P1
- **Impacto:** Medio (accesibilidad + SEO de imagen)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Datos · Admin
- **Pasos:**
  1. Identificar los 71 productos vía query Admin.
  2. ALT = título del producto (es lo que ya hace Hevea correctamente).
  3. Bulk update con `productImageUpdate`.
- **Validación:** query devuelve 0 productos sin `featuredImage.altText`.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.6 ALT`.

### F0-07 · Localizar los 2 productos sin imagen principal y resolver

- **Prioridad:** P0
- **Impacto:** Alto (no se pueden vender sin imagen)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Datos · Contenido
- **Pasos:** identificar handles, decidir caso a caso (asignar imagen del proveedor / pasar a DRAFT / borrar).
- **Validación:** query `products(first:250) { ... featuredImage { url } }` devuelve `featuredImage` en 100 % de los ACTIVE.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.1`.

### F0-08 · Auditar y resolver los 4 productos en DRAFT

- **Prioridad:** P1
- **Impacto:** Medio (limpieza de catálogo)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Admin · Contenido
- **Pasos:** ya listados en `PROYECTO.md`: 2× Parasol acrílico (sospecha duplicado), Cojín exterior, Limpiador. Decidir publicar / fusionar / borrar.
- **Validación:** 0 productos en DRAFT salvo casos justificados.

### F0-09 · Pull del theme actual a local

- **Prioridad:** P0 (bloquea Fase 0 visible)
- **Impacto:** Alto (sin theme local no se puede auditar ni cambiar nada visual)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Theme · CLI
- **Pasos:**
  1. Crear directorio `theme/` en la raíz del proyecto.
  2. `shopify theme list --store mueblesexterior.myshopify.com` para identificar theme activo.
  3. `shopify theme pull --theme=<id> --path=theme/`.
  4. Añadir `theme/` al gitignore o decidir si versionarlo (recomendado: versionarlo).
- **Validación:** `theme/templates/`, `theme/sections/`, `theme/snippets/`, `theme/config/settings_data.json` existen localmente.

### F0-10 · Auditar footer y eliminar textos en inglés

- **Prioridad:** P1
- **Impacto:** Alto (footer aparece en cada página)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** F0-09
- **Requiere:** Theme · Contenido
- **Pasos:** revisar `theme/sections/footer.liquid` + locales `theme/locales/es.json` y eliminar todo string en inglés (típicamente "FREE SHIPPING TO MAINLAND SPAIN" o similares heredados del theme base).
- **Validación:** página rendereada en `?preview_theme_id=<>` no muestra ningún string en inglés.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.2 Idioma`.

### F0-11 · Crear página "Entrega" con texto base del plan

- **Prioridad:** P1
- **Impacto:** Alto (confianza en ticket alto)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Admin · Contenido
- **Pasos:** crear página handle `entrega` en Admin, copiar texto base de `plan_santavila.md §13.2`, añadir info específica: "Envío gratuito a península para pedidos > 900 €" (condición Hevea, validar para Balliu antes de publicar).
- **Validación:** `/pages/entrega` accesible, texto sin lorem ipsum, contiene plazo, condiciones, contacto.

### F0-12 · Crear página "Garantía"

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Baja
- **Riesgo:** Bajo (cuidado con prometer cobertura no validada)
- **Dependencia:** —
- **Requiere:** Admin · Contenido
- **Pasos:** texto base `plan_santavila.md §13.3`. Aclarar: garantía = la del proveedor (Hevea: 3 años confirmado; Balliu: pendiente confirmar).
- **Validación:** `/pages/garantia` activa, texto coherente con condiciones reales por proveedor.

### F0-13 · Crear página "Mantenimiento" con guías por material

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media (contenido editorial)
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Admin · Contenido
- **Pasos:** una página padre `mantenimiento` + secciones por material (aluminio, madera, HPL, cuerda, tejidos, cojines, parasoles).
- **Validación:** `/pages/mantenimiento` con bloques navegables por material.

### F0-14 · Crear página "Contacto" con WhatsApp visible

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** decisión: ¿hay WhatsApp comercial?
- **Requiere:** Admin · Contenido
- **Pasos:** página `/pages/contacto` con email `hola@santavila.com`, formulario, horario, número WhatsApp si se confirma.
- **Validación:** página renderea, formulario manda email a `hola@santavila.com`.

### F0-15 · Sustituir todas las etiquetas "Oferta" por badges de valor

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Media (theme)
- **Riesgo:** Bajo
- **Dependencia:** F0-01 (eliminar `compareAtPrice`), F0-09 (theme local)
- **Requiere:** Theme
- **Pasos:** en `theme/snippets/product-card-badge.liquid` (o el equivalente del theme actual), eliminar lógica de "On sale" / "Ahorra" y reemplazar por badges renderados desde metafields propios cuando se creen (`santavila.fabricado_espana`, `santavila.producto_hero`, `santavila.envio_gratis`).
- **Validación:** ningún producto muestra badge "Oferta". Productos con metafield correspondiente muestran el badge nuevo.

### F0-16 · Crear barra de confianza global (header o top)

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F0-09
- **Requiere:** Theme · Contenido
- **Pasos:** crear sección `sv-trust-bar.liquid` con 5 mensajes (`plan_santavila.md §6.2 Bloque 2`): proveedores españoles, entrega península, plazo hasta 1 mes, garantía proveedor, asesoramiento humano. Sección activable desde el editor.
- **Validación:** barra visible en header de todas las páginas rendereadas.

### F0-17 · Revisar nombres de producto sin formato canónico

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Baja
- **Riesgo:** Bajo (cambio de title puede afectar SEO si ya hay tráfico — no urgente)
- **Dependencia:** —
- **Requiere:** Datos · Admin
- **Pasos:** identificar productos cuyo título no siga el patrón `[Tipo] [rasgo] · [estilo] | [medida]`. Detectado: `Reposapiés exterior · 73×46×40 cm` (le falta separador antes de la medida). Normalizar.
- **Validación:** muestreo aleatorio de 30 productos, ≥27 cumplen el patrón.

---

## FASE 1 — Modelo de datos Shopify (Semanas 1-2)

> Objetivo: estructurar el catálogo. Sin esto las Fases 2-7 no pueden existir.

### F1-01 · Crear los 32 metafield definitions del namespace `santavila`

- **Prioridad:** P0
- **Impacto:** Alto (palanca de todo)
- **Dificultad:** Media
- **Riesgo:** Bajo si se hace en Admin (los metafields no rompen nada, solo añaden campo)
- **Dependencia:** revisar `DATA_MODEL_SANTAVILA.md` y validar tipos
- **Requiere:** Admin · Datos
- **Pasos:** crear cada definición vía Admin → Settings → Custom data → Products. Lista completa en [`DATA_MODEL_SANTAVILA.md`](DATA_MODEL_SANTAVILA.md).
- **Validación:** `query { metafieldDefinitions(first:100, ownerType:PRODUCT, namespace:"santavila") }` devuelve 32 entries.

### F1-02 · Crear los 8 metaobject definitions `sv_*`

- **Prioridad:** P0
- **Impacto:** Alto
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01 (algunos metafields referencian metaobjects)
- **Requiere:** Admin · Datos
- **Pasos:** crear `sv_supplier`, `sv_material_guide`, `sv_delivery_type`, `sv_warranty_policy`, `sv_collection_story`, `sv_space_solution`, `sv_faq`, `sv_care_guide` con los campos definidos en [`DATA_MODEL_SANTAVILA.md`](DATA_MODEL_SANTAVILA.md).
- **Validación:** `query { metaobjectDefinitions(first:50) }` devuelve 8 definitions.

### F1-03 · Poblar `sv_supplier` con Hevea y Balliu

- **Prioridad:** P0
- **Impacto:** Alto
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** F1-02
- **Requiere:** Admin · Contenido
- **Pasos:** crear 2 entradas con: nombre interno, origen, provincia (validar), plazo estándar, contacto operativo, condiciones (envío gratuito >900€ Hevea — Balliu por validar), score inicial = 3, notas internas. Datos de Hevea ya documentados en `PROYECTO.md §3 Hevea`.
- **Validación:** los 2 metaobjects creados, accesibles vía API.

### F1-04 · Plantilla maestra de importación CSV

- **Prioridad:** P1
- **Impacto:** Alto (operativa de altas y enriquecimiento masivo)
- **Dificultad:** Media
- **Riesgo:** Medio (importación mal configurada puede sobreescribir datos)
- **Dependencia:** F1-01, F1-02
- **Requiere:** Datos
- **Pasos:** crear `templates/santavila_product_master.csv` con todas las columnas (handle, title, productType, vendor=Santavila, tags + 32 metafields santavila.*, description). Validar con un producto piloto.
- **Validación:** importar 1 producto piloto, verificar que se rellenan los 32 metafields.

### F1-05 · Migración masiva: poblar metafields desde Santavila.xlsx

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Alta
- **Riesgo:** Medio
- **Dependencia:** F1-01, F1-02, F1-03, F1-04
- **Requiere:** Datos · Script
- **Pasos:** script Python (`migrate_xlsx_to_metafields.py`) que toma `Santavila.xlsx` y CSVs proveedor, mapea a metafields y ejecuta `productUpdate` en bulk. Empezar con 20 productos héroe, luego escalar.
- **Validación:** muestreo de 20 productos: 100 % tiene `santavila.proveedor`, `santavila.plazo_max_dias`, `santavila.material_estructura`, `santavila.uso_recomendado`, `santavila.estado_enriquecimiento`.

### F1-06 · Marcar 20 productos héroe iniciales

- **Prioridad:** P1
- **Impacto:** Alto (palanca para home y PLPs)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** F1-01
- **Requiere:** Datos · Admin · criterio comercial
- **Pasos:** criterio combinado: margen alto + foto buena + plazo corto + ficha ya rica. Activar metafield `santavila.producto_hero=true` en 20 productos.
- **Validación:** `query` con filtro `metafield: santavila.producto_hero=true` devuelve 20 productos.

### F1-07 · Score producto: calcular puntuación 1-5 por SKU

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01, F1-05
- **Requiere:** Datos · Script
- **Pasos:** script que calcula score (peso: margen 25%, calidad visual 20%, plazo 20%, diferenciación 15%, SEO 10%, colección 10%) y guarda en `santavila.score_producto`. Mecánica detallada en `plan_santavila.md §14.2`.
- **Validación:** todos los productos tienen score 1-5. Distribución coherente.

### F1-08 · Definir y rellenar `santavila.estado_enriquecimiento` para todos los productos

- **Prioridad:** P1
- **Impacto:** Medio
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** F1-01
- **Requiere:** Datos
- **Pasos:** valores `pendiente / en_progreso / revisado / completo`. Marcar inicial: los 20 héroe = `revisado`, resto = `pendiente`.
- **Validación:** todos los productos tienen valor; la query agregada por estado da una distribución útil.

---

## FASE 2 — PDP premium (Semanas 2-4)

> Objetivo: convertir fichas en páginas de venta. Construye sobre F1.

### F2-01 · Crear template `product.premium.json`

- **Prioridad:** P0
- **Impacto:** Alto
- **Dificultad:** Alta
- **Riesgo:** Medio (un template mal hecho rompe PDPs)
- **Dependencia:** F0-09, F1-01
- **Requiere:** Theme · Datos
- **Pasos:** template JSON que ensambla las nuevas secciones `sv-product-trust-panel`, `sv-product-materials`, `sv-product-delivery`, `sv-product-warranty`, `sv-product-care`, `sv-product-faq`, `sv-compatible-products`. Detalle en [`THEME_PLAN_SANTAVILA.md`](THEME_PLAN_SANTAVILA.md).
- **Validación:** asignar a 1 producto piloto, comparar con PDP estándar. Confirmar rendimiento mobile.

### F2-02 · Sección `sv-product-trust-panel` (módulo de confianza junto al precio)

- **Prioridad:** P0
- **Impacto:** Alto
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01 (metafields plazo, garantía, entrega, asesoramiento)
- **Requiere:** Theme
- **Pasos:** snippet Liquid que lee `santavila.plazo_min_dias`, `santavila.plazo_max_dias`, `santavila.tipo_entrega`, `santavila.garantia_resumen` y renderiza 4-5 líneas con iconos. Texto base `plan_santavila.md §8.3`.
- **Validación:** se ve junto al precio en mobile y desktop, con datos reales del SKU.

### F2-03 · Sección `sv-product-materials` (materiales explicados)

- **Prioridad:** P1
- **Impacto:** Medio-Alto
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-02 (`sv_material_guide`), F1-05 (metafields material poblados)
- **Requiere:** Theme · Contenido
- **Pasos:** sección que lee `santavila.material_estructura`, `santavila.material_superficie`, `santavila.material_textil` y para cada material muestra info del metaobject `sv_material_guide` (descripción, ventajas, cuidados).
- **Validación:** PDP de un producto con aluminio + HPL muestra dos paneles, cada uno con su info.

### F2-04 · Sección `sv-product-delivery`

- **Prioridad:** P0
- **Impacto:** Alto
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01, F0-11
- **Requiere:** Theme
- **Pasos:** lee plazo, tipo de entrega, montaje, subida; texto explicativo + link a `/pages/entrega`. Mensaje literal del plan §8.5 "Bloque Entrega".
- **Validación:** PDP muestra plazo concreto y enlaza a página entrega.

### F2-05 · Sección `sv-product-warranty`

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Media
- **Riesgo:** Medio (cuidado con prometer cobertura)
- **Dependencia:** F1-01, F1-02 (`sv_warranty_policy`), F0-12
- **Requiere:** Theme
- **Pasos:** lee `santavila.garantia_resumen` + (si existe) referencia a `sv_warranty_policy` → muestra duración + procedimiento.
- **Validación:** PDP de Hevea muestra "3 años garantía" + link.

### F2-06 · Sección `sv-product-care` (mantenimiento)

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-02 (`sv_care_guide`), F0-13
- **Requiere:** Theme · Contenido

### F2-07 · Sección `sv-product-faq`

- **Prioridad:** P2
- **Impacto:** Medio (también SEO si hay schema)
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-02 (`sv_faq`)
- **Requiere:** Theme · Contenido
- **Pasos:** acordeón con FAQs específicas + FAQs comunes por familia. Schema.org FAQPage cuando proceda.

### F2-08 · Sección `sv-compatible-products` (cross-sell curado)

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01 (`santavila.coleccion_santavila`)
- **Requiere:** Theme
- **Pasos:** mostrar productos de la misma `coleccion_santavila` filtrados por compatibilidad (no aleatorios). Si vacío, fallback a Search & Discovery.

### F2-09 · Bloque "Por qué esta pieza" + "Encaja si"

- **Prioridad:** P2
- **Impacto:** Medio (mejora redacción)
- **Dificultad:** Media (contenido editorial)
- **Riesgo:** Bajo
- **Dependencia:** F1-01 (metafield `santavila.por_que` y `santavila.encaja_si`)
- **Requiere:** Theme · Contenido
- **Pasos:** reescribir descripción de los 20 héroe con esta estructura. Guía de redacción en `plan_santavila.md §8.5`.

### F2-10 · CTA secundario de asesoramiento en PDP

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** F0-14 (página contacto / WhatsApp activo)
- **Requiere:** Theme
- **Pasos:** botón secundario debajo del "Añadir al carrito" tipo "¿Dudas con esta pieza? Te ayudamos por WhatsApp".

---

## FASE 3 — Home y PLP (Mes 2)

### F3-01 · Rediseñar home con bloques del plan

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Alta
- **Riesgo:** Medio
- **Dependencia:** F0-15, F0-16, F1-06, F2-01
- **Requiere:** Theme · Contenido
- **Pasos:** ensamblar `index.json` con `sv-hero-premium`, `sv-trust-bar`, `sv-shop-by-space`, `sv-featured-collections`, `sv-why-santavila`, productos héroe, `sv-material-grid`, `sv-advice-block`, `sv-professionals-block`, `sv-editorial-guides`. Estructura completa en [`THEME_PLAN_SANTAVILA.md`](THEME_PLAN_SANTAVILA.md).
- **Validación:** test de 10 segundos (`plan §4.2`): el usuario debe entender qué vende, por qué confiar, dónde entrega, qué estilo y cómo pedir ayuda.

### F3-02 · Crear colecciones por espacio (7 colecciones)

- **Prioridad:** P1
- **Impacto:** Alto
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01 (`santavila.espacio_principal`), F1-05
- **Requiere:** Admin · Datos
- **Pasos:** colecciones smart (rules) sobre metafield: Terraza, Ático, Jardín, Porche, Balcón, Patio, Piscina. Cada una con `seo.title`, `seo.description`, `descriptionHtml` editorial.
- **Validación:** las 7 colecciones existen, tienen >= 10 productos cada una y descripción ≥ 200 caracteres.

### F3-03 · Crear colecciones por material (5)

- **Prioridad:** P1
- **Impacto:** Medio-Alto
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01 (`santavila.material_estructura`), F1-05
- **Requiere:** Admin · Datos
- **Pasos:** Aluminio, Madera, HPL, Cuerda, Tejidos exteriores. Smart collections + descripción + SEO.

### F3-04 · Reescribir las 7 colecciones existentes con descripción + SEO

- **Prioridad:** P1
- **Impacto:** Alto (SEO + UX PLP)
- **Dificultad:** Media (contenido editorial)
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Admin · Contenido
- **Pasos:** para cada colección actual (Tumbonas, Mesas de exterior, Sofás, Sillas, Parasoles, Accesorios, Frontpage si se mantiene): descripción ≥ 250 caracteres + SEO title (60 char) + SEO description (155 char) + bloque guía de compra (`plan §7.4`).
- **Validación:** las 7 colecciones devuelven `seo.title NOT NULL` y `descriptionHtml LENGTH > 250`.
- **Hallazgo origen:** `AUDITORIA_SANTAVILA.md §1.6 Colecciones`.

### F3-05 · Crear template `collection.premium.json` con bloques de ayuda

- **Prioridad:** P2
- **Impacto:** Medio-Alto
- **Dificultad:** Alta
- **Riesgo:** Medio
- **Dependencia:** F0-09, F3-04
- **Requiere:** Theme
- **Pasos:** template con secciones `sv-collection-hero`, accesos rápidos por uso, filtros, productos, `sv-collection-guide`, FAQs, enlaces internos a materiales/espacios.

### F3-06 · Configurar filtros nativos Search & Discovery

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F1-01, F1-05
- **Requiere:** Admin
- **Pasos:** activar filtros sobre los metafields filtrables (precio, material, plazo, espacio, plazas, color cuando exista, uso cubierto, mantenimiento). Lista en `plan §7.3`.

---

## FASE 4 — Dirección visual IA (Mes 2, paralelo a F3)

### F4-01 · Definir guía visual Santavila

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** —
- **Requiere:** Contenido
- **Pasos:** documento en `docs/santavila/GUIA_VISUAL.md` con paleta (`plan §11.4`), tipografía (`§11.5`), referencias (`§11.3`), do/don't.

### F4-02 · Prompts Higgsfield base + variantes por espacio

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** F4-01
- **Requiere:** Contenido
- **Pasos:** copiar prompts del `plan §12` a `docs/santavila/prompts_higgsfield.md`. Generar lote inicial: 7 espacios × 2 variantes = 14 imágenes hero.

### F4-03 · Banco de imágenes hero

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media (curación + iteración)
- **Riesgo:** Bajo
- **Dependencia:** F4-02
- **Requiere:** Contenido · IA
- **Pasos:** generar y curar; subir a `images_lifestyle/santavila/`. Dimensiones para hero: 2880×1620, 1920×1080, 1200×675.

### F4-04 · Imágenes para colecciones (PLP hero)

- **Prioridad:** P3
- **Impacto:** Medio
- **Dificultad:** Media
- **Dependencia:** F4-01, F3-02, F3-03
- **Requiere:** Contenido

---

## FASE 5 — SEO y contenido (Meses 2-4)

### F5-01 · Crear 5 guías SEO base

- **Prioridad:** P2
- **Impacto:** Medio (tráfico orgánico mid-tail)
- **Dificultad:** Alta (contenido)
- **Riesgo:** Bajo
- **Dependencia:** F4-03
- **Requiere:** Admin · Contenido
- **Pasos:** "Cómo elegir un sofá exterior", "Qué material es mejor para muebles de exterior", "Cómo amueblar una terraza pequeña", "Aluminio vs madera en exterior", "Medidas recomendadas para comedor exterior". 1500-2500 palabras cada una.

### F5-02 · Páginas por espacio (7)

- **Prioridad:** P2
- **Impacto:** Medio-Alto
- **Dificultad:** Media
- **Dependencia:** F1-02 (`sv_space_solution`)
- **Requiere:** Admin · Contenido

### F5-03 · Páginas por material (5)

- **Prioridad:** P3
- **Impacto:** Medio
- **Dificultad:** Media
- **Dependencia:** F1-02 (`sv_material_guide`)
- **Requiere:** Admin · Contenido

### F5-04 · Schema markup avanzado en PDP

- **Prioridad:** P2
- **Impacto:** Medio (rich snippets)
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F2-01, F1-05
- **Requiere:** Theme
- **Pasos:** Product, BreadcrumbList, FAQPage (cuando hay FAQs reales).

### F5-05 · Optimizar handles/title de los 235 productos

- **Prioridad:** P3
- **Impacto:** Medio
- **Dificultad:** Alta
- **Riesgo:** Medio (necesita 301)
- **Dependencia:** F1-05
- **Requiere:** Admin · Datos · Redirects
- **Pasos:** identificar handles con prefijo `balliu-` (expone proveedor) — quitar prefijo, crear redirects.

---

## FASE 6 — Profesionales (Meses 3-4)

### F6-01 · Página `/pages/profesionales`

- **Prioridad:** P2
- **Impacto:** Medio (canal B2B ligero)
- **Dificultad:** Media
- **Dependencia:** F0-09
- **Requiere:** Admin · Theme · Contenido

### F6-02 · Formulario profesionales

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Media
- **Riesgo:** Bajo
- **Dependencia:** F6-01
- **Requiere:** Theme o app de formularios
- **Pasos:** campos según `plan §18.2`. Email a `hola@santavila.com`. Auto-respuesta.

### F6-03 · Catálogo PDF para profesionales (opcional)

- **Prioridad:** P3
- **Impacto:** Bajo-Medio
- **Dificultad:** Alta
- **Dependencia:** F1-05, F4-03
- **Requiere:** Contenido · Script

---

## FASE 7 — Operativa y automatizaciones (Meses 3-6)

### F7-01 · Shopify Flow: pedido creado → etiquetar por proveedor

- **Prioridad:** P2
- **Impacto:** Medio (operativa interna)
- **Dificultad:** Baja
- **Riesgo:** Bajo
- **Dependencia:** F0-02, F1-01
- **Requiere:** Admin · App Flow
- **Pasos:** trigger `Order created` → leer `lineItems[].product.metafield.santavila.proveedor` → tag pedido `proveedor:hevea` o `proveedor:balliu`.

### F7-02 · Shopify Flow: alerta plazo largo (>21 días)

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Baja
- **Dependencia:** F1-05 (plazo poblado)
- **Requiere:** Admin · App Flow

### F7-03 · Shopify Flow: alerta pedido premium (>1.000 €)

- **Prioridad:** P2
- **Impacto:** Medio
- **Dificultad:** Baja
- **Dependencia:** —
- **Requiere:** Admin · App Flow

### F7-04 · Shopify Flow: producto creado → tag `pendiente_enriquecimiento`

- **Prioridad:** P2
- **Impacto:** Medio (operativa)
- **Dificultad:** Baja
- **Dependencia:** F1-01
- **Requiere:** Admin · App Flow

### F7-05 · Score proveedor: revisión semanal

- **Prioridad:** P3
- **Impacto:** Medio
- **Dificultad:** Media
- **Dependencia:** F1-02 (`sv_supplier`)
- **Requiere:** Datos · Operativa
- **Pasos:** template Excel/script que actualiza el score del metaobject `sv_supplier` con OTIF, incidencias, calidad de dato, respuesta, garantía, margen, plazo (criterios `plan §14.3`).

### F7-06 · Dashboard interno SKUs

- **Prioridad:** P3
- **Impacto:** Medio
- **Dificultad:** Media
- **Dependencia:** F1-05, F1-07
- **Requiere:** Datos · Excel/herramienta
- **Pasos:** vista en `Santavila.xlsx` o nuevo doc que muestre por SKU: estado_enriquecimiento, score, prioridad_comercial, margen, plazo, ventas (cuando haya datos).

---

## Resumen por fase

| Fase | Tareas | P0 | P1 | P2 | P3 | Esfuerzo total |
|------|--------|----|----|----|----|----------------|
| F0 — Limpieza | 17 | 5 | 9 | 2 | 1 | Semana 1 |
| F1 — Datos | 8 | 3 | 4 | 1 | 0 | Semanas 1-2 |
| F2 — PDP | 10 | 3 | 3 | 4 | 0 | Semanas 2-4 |
| F3 — Home/PLP | 6 | 0 | 4 | 2 | 0 | Mes 2 |
| F4 — Visual IA | 4 | 0 | 0 | 3 | 1 | Mes 2 (paralelo) |
| F5 — SEO | 5 | 0 | 0 | 4 | 1 | Meses 2-4 |
| F6 — Profesionales | 3 | 0 | 0 | 2 | 1 | Meses 3-4 |
| F7 — Operativa | 6 | 0 | 0 | 4 | 2 | Meses 3-6 |
| **Total** | **59** | **11** | **20** | **22** | **6** | **6 meses** |

**Hitos:**
- **Semana 1:** F0 completa → la tienda deja de parecer Shopify sin pulir.
- **Semana 2:** F1 hasta F1-06 → modelo de datos vivo, 20 héroe marcados y enriquecidos.
- **Semana 4:** F2-01 a F2-04 → primera PDP premium piloto en producción para 1 producto héroe.
- **Mes 2:** F3-01 a F3-04 → home y PLPs principales rediseñadas.
- **Mes 3:** F2 al 100 % en los 20 héroe + F4 banco IA inicial.
- **Mes 6:** F5-F7 maduros, score producto/proveedor, automatizaciones Flow.
