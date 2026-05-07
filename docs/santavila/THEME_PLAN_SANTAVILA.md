# THEME_PLAN_SANTAVILA.md

**Snapshot:** 2026-05-06
**Estado actual:** theme activo no inspeccionado (limitación: scope `read_themes` no concedido). El plan asume tener el theme local tras `shopify theme pull` (tarea **F0-09** del backlog).

## Convenciones del theme

- **Prefijo de fichero propio:** todo lo nuevo va con `sv-` (sections, snippets, templates) para no confundirse con lo que viene del theme base.
- **Carpeta de trabajo local:** `theme/` en la raíz del repo (versionado en git).
- **Idioma:** todos los textos en `theme/locales/es.default.json`. **Nada hard-codeado en español dentro de Liquid.** Ello permite añadir `pt.json` cuando se abra Markets a Portugal (decisión pendiente §24 plan).
- **Settings de sección:** todos los textos en `presets[].settings`, traducibles.
- **Compatibilidad:** el theme actual NO debe romperse mientras se rola el nuevo. Se duplica el theme con `shopify theme push --unpublished --theme="Santavila Premium WIP"` y se prueba con `?preview_theme_id=…` antes de publicar.

## Cómo se conecta este plan con el resto

- Cada sección **lee metafields** definidos en [`DATA_MODEL_SANTAVILA.md`](DATA_MODEL_SANTAVILA.md). Se documenta cuáles abajo.
- Cada sección/template/snippet aparece como tarea en [`BACKLOG_SANTAVILA.md`](BACKLOG_SANTAVILA.md) con su ID (Fx-yy).
- **Nada se crea sin metafield correspondiente vivo.** Una sección que lea `santavila.plazo_max_dias` no se programa hasta que F1-01 + F1-05 estén completos.

---

## 1. Secciones (19)

### Globales / transversales

#### `sv-trust-bar` — barra de confianza

- **Objetivo:** mensajes de confianza fijos visibles en todas las páginas (entrega península, proveedores españoles, plazo máximo, garantía proveedor, asesoramiento humano).
- **Dónde se usa:** `theme/layout/theme.liquid` justo debajo del header, o como sección global.
- **Datos:** estáticos via settings de sección (5 ítems editables: icono + texto + link opcional).
- **Metafields:** ninguno (estático).
- **Dificultad:** Baja.
- **Backlog ID:** F0-16.
- **Archivos:** `theme/sections/sv-trust-bar.liquid` + entrada en `theme/locales/es.default.json`.

#### `sv-whatsapp-cta` — botón flotante

- **Objetivo:** acceso WhatsApp persistente (decisión pendiente: ¿hay número comercial?).
- **Dónde:** `theme.liquid`, abajo a la derecha en mobile y desktop.
- **Datos:** número configurable, mensaje pre-rellenado por contexto (en PDP incluye nombre producto vía Liquid).
- **Metafields:** ninguno.
- **Dificultad:** Baja.
- **Backlog ID:** F0-14, F2-10.
- **Archivos:** `theme/snippets/sv-whatsapp-cta.liquid` (es snippet, no sección — ver §3).

### Home

#### `sv-hero-premium`

- **Objetivo:** hero principal de la home con claim, subclaim, CTA principal y secundario.
- **Dónde:** `index.json` (template home), bloque 1.
- **Datos:**
  - Imagen (mobile + desktop, 2880×1620 y 1080×1620 vertical).
  - Claim editable (default: "Diseño español para vivir fuera").
  - Subclaim.
  - CTA primario (default: "Ver colecciones" → `/collections/all`).
  - CTA secundario (default: "Te ayudamos con tu terraza" → `/pages/contacto`).
- **Metafields:** ninguno.
- **Dificultad:** Media.
- **Backlog ID:** F3-01.
- **Archivos:** `theme/sections/sv-hero-premium.liquid`.

#### `sv-shop-by-space`

- **Objetivo:** rejilla de 6 tarjetas (Terrazas, Áticos, Jardines, Porches, Balcones, Piscina) con imagen + link a la página de espacio.
- **Dónde:** home, bloque 3.
- **Datos:** imagen por tarjeta + link.
- **Metafields:** ninguno (los espacios son páginas/colecciones gestionadas aparte).
- **Dificultad:** Media.
- **Backlog ID:** F3-01.
- **Archivos:** `theme/sections/sv-shop-by-space.liquid`.

#### `sv-featured-collections`

- **Objetivo:** 4 colecciones principales destacadas (Salones de exterior, Comedores, Tumbonas y relax, Sombra y parasoles).
- **Dónde:** home, bloque 4.
- **Datos:** referencias a 4 colecciones.
- **Dificultad:** Baja.
- **Backlog ID:** F3-01.

#### `sv-why-santavila`

- **Objetivo:** título "Exterior con criterio" + 5 puntos diferenciales (selección curada, proveedores españoles, producto explicado, materiales pensados para exterior, entrega clara).
- **Dónde:** home, bloque 5.
- **Datos:** estáticos via settings.
- **Dificultad:** Baja.
- **Backlog ID:** F3-01.

#### `sv-material-grid`

- **Objetivo:** 5 accesos a páginas de material (Aluminio, Madera, HPL, Cuerda, Tejidos exteriores).
- **Dónde:** home, bloque 7.
- **Datos:** referencias a páginas/colecciones de material.
- **Metaobjects:** `sv_material_guide` (para imagen e icono cuando esté).
- **Dificultad:** Media.
- **Backlog ID:** F3-01 + F4-04.

#### `sv-advice-block`

- **Objetivo:** bloque "¿No sabes por dónde empezar?" → CTA pedir asesoramiento.
- **Dónde:** home, bloque 8.
- **Datos:** texto editable + link a contacto.
- **Dificultad:** Baja.
- **Backlog ID:** F3-01.

#### `sv-professionals-block`

- **Objetivo:** bloque "Proyectos para profesionales" en home → área profesionales.
- **Dónde:** home, bloque 9.
- **Datos:** texto editable + link a `/pages/profesionales`.
- **Dificultad:** Baja.
- **Backlog ID:** F3-01, F6-01.

#### `sv-editorial-guides`

- **Objetivo:** 4 tarjetas con guías de compra (Cómo elegir sofá, Amueblar ático, Material que aguanta sol, Guía de medidas).
- **Dónde:** home, bloque 10.
- **Datos:** referencias a páginas de blog o pages.
- **Dificultad:** Baja.
- **Backlog ID:** F3-01 + F5-01.

### Producto (PDP)

#### `sv-product-trust-panel`

- **Objetivo:** panel de confianza pegado al precio: plazo, tipo entrega, garantía, asesoramiento.
- **Dónde:** template `product.premium.json`, en bloque principal junto al `<form>` de carrito.
- **Datos:** lee del producto:
  - `santavila.plazo_min_dias` y `santavila.plazo_max_dias` → texto "Entrega 7-15 días".
  - `santavila.tipo_entrega` → texto "Mediante transporte".
  - `santavila.montaje_incluido` (false → "Sin montaje incluido").
  - `santavila.subida_incluida` (false → "Sin subida especial").
  - `santavila.garantia_resumen` → "Garantía: 3 años".
  - link "Asesoramiento por WhatsApp" → `wa.me/...`.
- **Dificultad:** Media (Liquid + diseño icono+texto).
- **Backlog ID:** F2-02.

#### `sv-product-materials`

- **Objetivo:** explicar los materiales del producto leyendo del metaobject `sv_material_guide`.
- **Dónde:** PDP, debajo de la galería + descripción.
- **Datos:**
  - lee `santavila.material_estructura/superficie/textil` (listas).
  - para cada valor, busca el metaobject `sv_material_guide` con `material_clave = valor`.
  - renderea: nombre, descripción corta, ventajas, cuidados.
- **Dificultad:** Alta (joins en Liquid son tediosos; opción: helper en snippet).
- **Backlog ID:** F2-03.

#### `sv-product-delivery`

- **Objetivo:** explicar la entrega de este producto en concreto + link a página entrega.
- **Datos:**
  - `santavila.tipo_entrega` → joins con `sv_delivery_type` (incluye/no incluye/condiciones).
  - `santavila.plazo_min_dias`, `santavila.plazo_max_dias` → línea explícita.
  - `santavila.proveedor` → si necesario, "Distribuye proveedor X" (decisión: por defecto no mostrar).
- **Dificultad:** Media.
- **Backlog ID:** F2-04.

#### `sv-product-warranty`

- **Objetivo:** bloque garantía en PDP.
- **Datos:**
  - `santavila.garantia_resumen` (fallback texto).
  - `santavila.garantia_detalle` → metaobject `sv_warranty_policy` con duración, cobertura, exclusiones, procedimiento.
  - link a `/pages/garantia`.
- **Dificultad:** Media.
- **Backlog ID:** F2-05.

#### `sv-product-care`

- **Objetivo:** bloque mantenimiento.
- **Datos:** `santavila.material_estructura` → `sv_care_guide` (frecuencia, limpieza, productos a evitar).
- **Dificultad:** Media.
- **Backlog ID:** F2-06.

#### `sv-product-faq`

- **Objetivo:** acordeón de preguntas frecuentes específicas + comunes por familia.
- **Datos:**
  - lee metaobjects `sv_faq` filtrados por `producto = current` o `familia = product.type`.
  - schema.org FAQPage cuando hay 2+ FAQs.
- **Dificultad:** Media.
- **Backlog ID:** F2-07.

#### `sv-compatible-products`

- **Objetivo:** "Completa el espacio" — productos compatibles curados.
- **Datos:**
  - `santavila.coleccion_santavila` → `sv_collection_story.productos` filtrando el actual.
  - fallback: si vacío → Shopify `complementary_products` o `related_products` (auto).
- **Dificultad:** Media.
- **Backlog ID:** F2-08.

### Colección (PLP)

#### `sv-collection-hero`

- **Objetivo:** hero de PLP con título, descripción editorial y guía rápida.
- **Datos:** `collection.descriptionHtml` (rica), `collection.image`, `collection.metafields` opcionales.
- **Dificultad:** Media.
- **Backlog ID:** F3-04, F3-05.

#### `sv-collection-guide`

- **Objetivo:** "Cómo elegir [tipo]" debajo de la rejilla de productos.
- **Datos:** rich text desde `collection.metafields.santavila.guia_compra` (nuevo metafield de COLLECTION — añadir al data model en iteración futura) o desde la `descriptionHtml` segmentada.
- **Dificultad:** Media.
- **Backlog ID:** F3-05.

### Páginas dedicadas

#### `sv-space-page`

- **Objetivo:** plantilla de "Muebles para [espacio]" — terraza, ático, jardín, etc.
- **Datos:** lee metaobject `sv_space_solution` con problema/recomendaciones/medidas/productos.
- **Dificultad:** Media.
- **Backlog ID:** F5-02.

#### `sv-material-page`

- **Objetivo:** plantilla de "Muebles exterior [material]" — aluminio, madera, HPL.
- **Datos:** `sv_material_guide` + `sv_care_guide`.
- **Dificultad:** Media.
- **Backlog ID:** F5-03.

---

## 2. Templates (14)

| Template | Objetivo | Secciones que ensambla | Dificultad | Backlog |
|----------|----------|------------------------|-----------|---------|
| `index.json` | Home premium | sv-hero-premium · sv-trust-bar (opcional duplicado) · sv-shop-by-space · sv-featured-collections · sv-why-santavila · featured-product (los 20 héroe) · sv-material-grid · sv-advice-block · sv-professionals-block · sv-editorial-guides | Alta | F3-01 |
| `product.premium.json` | PDP base premium (la usan los productos sin family específica) | sv-product-trust-panel · galería · descripción · sv-product-materials · sv-product-delivery · sv-product-warranty · sv-product-care · sv-product-faq · sv-compatible-products | Alta | F2-01 |
| `product.sofa.json` | PDP especializada para sofás/conjuntos | igual + módulo "número de plazas" + bloque dimensiones específicas | Alta | F2-01 (variante) |
| `product.table.json` | PDP especializada para mesas (centro, comedor) | igual + énfasis en dimensiones tablero (`material_superficie`) y compatibilidad sillas | Alta | F2-01 (variante) |
| `product.chair.json` | PDP especializada para sillas y sillones | igual + apilable sí/no, peso individual | Media | F2-01 (variante) |
| `product.sunbed.json` | PDP especializada para tumbonas | igual + posiciones reclinado, cojín incluido | Media | F2-01 (variante) |
| `collection.premium.json` | PLP premium genérica | sv-collection-hero · facetas (filtros nativos) · grid productos · sv-collection-guide · sv-product-faq (bloque general) · enlaces internos | Alta | F3-05 |
| `collection.space.json` | PLP por espacio | sv-collection-hero (con datos del `sv_space_solution`) · grid · recomendaciones · CTA asesoramiento | Media | F3-02 |
| `collection.material.json` | PLP por material | sv-collection-hero · `sv_material_guide` · grid · `sv_care_guide` resumen · enlaces | Media | F3-03 |
| `page.delivery.json` | Página entrega | hero · texto plan §13.2 · FAQs · contacto | Baja | F0-11 |
| `page.warranty.json` | Página garantía | hero · texto plan §13.3 · políticas por proveedor (lista de `sv_warranty_policy`) | Baja | F0-12 |
| `page.care.json` | Página mantenimiento | navegación por material · `sv_care_guide` · CTA contacto | Media | F0-13 |
| `page.professionals.json` | Página profesionales | hero · qué ofrecemos · `sv_supplier` (proveedores) · formulario | Media | F6-01 |
| `page.inspiration.json` | Página inspiración / editorial hub | grid de guías · espacios · materiales · imágenes Higgsfield | Media | F5-01 + F4-03 |

> **Sobre las variantes por familia:** Shopify permite asignar template específico por producto (`Templates → product.sofa`). El equipo de catálogo decide en Admin a qué template pertenece cada producto. Cuando una familia no justifica un template propio (≤10 productos), se usa `product.premium.json`.

---

## 3. Snippets (9)

Snippets transversales reutilizables. Todos viven en `theme/snippets/sv-*.liquid`.

| Snippet | Objetivo | Datos | Usado por | Dificultad |
|---------|----------|-------|-----------|-----------|
| `sv-badge-list.liquid` | Renderea badges de un producto: "Fabricado en España", "Producto héroe", "Bajo pedido" según metafields | product.metafields.santavila.fabricado_espana, .producto_hero, lista de tags `bajo_pedido` | product cards, hero PDP, PLP grid | Baja |
| `sv-delivery-summary.liquid` | Mini-resumen entrega: 1 línea con plazo y tipo | product.metafields.santavila.plazo_min_dias/plazo_max_dias/tipo_entrega | sv-product-trust-panel, product card en cross-sell | Baja |
| `sv-warranty-summary.liquid` | Mini-resumen garantía: 1 línea | product.metafields.santavila.garantia_resumen | sv-product-trust-panel | Baja |
| `sv-material-summary.liquid` | Lista de materiales del producto formateada | product.metafields.santavila.material_estructura/superficie/textil + sv_material_guide.nombre_visible | sv-product-materials, sv-product-trust-panel | Media |
| `sv-product-score.liquid` | Mini-indicador de score interno (solo Admin/staff) | product.metafields.santavila.score_producto + check de `customer.tags contains 'staff'` | PDP staff debug | Baja |
| `sv-whatsapp-cta.liquid` | Botón WhatsApp con texto contextual | settings.whatsapp_number + product (si en PDP) o page.title | theme.liquid (flotante), PDP, página contacto | Baja |
| `sv-measurements.liquid` | Bloque de medidas: ancho × fondo × alto cm + iconos | product.metafields.santavila.ancho_cm/fondo_cm/alto_cm/peso_kg/numero_bultos | PDP, PLP card en hover | Media |
| `sv-care-icons.liquid` | Iconos de cuidado: lavable, no usar lejía, etc. | sv_care_guide.cuidados | sv-product-care | Media |
| `sv-trust-icons.liquid` | Iconos de confianza (envío, devoluciones, garantía, asesoramiento) reutilizables | settings | sv-trust-bar, footer, página entrega | Baja |

---

## 4. Cambios al theme base (no son sv-* propios pero hay que tocar)

| Archivo | Qué hay que cambiar | Razón | Backlog |
|---------|---------------------|-------|---------|
| `theme/locales/es.default.json` | Eliminar todo string en inglés. Auditar línea por línea | F0-10 | F0-10 |
| `theme/sections/header.liquid` | Insertar `sv-trust-bar` debajo del header. Asegurar menú con nuevas secciones (Espacios, Materiales, Profesionales, Inspiración, Ayuda) | F0-16 + F3-01 | F0-16 |
| `theme/sections/footer.liquid` | Auditar enlaces, eliminar inglés, asegurar links a `/pages/entrega`, `/pages/garantia`, `/pages/mantenimiento`, `/pages/contacto`, `/pages/profesionales`, política de privacidad y aviso legal | F0-10 | F0-10 |
| `theme/snippets/product-card.liquid` (o equivalente) | Llamar a `sv-badge-list` y `sv-measurements` | Mostrar info premium en grid | F2-01 |
| `theme/snippets/product-card-badge.liquid` | Eliminar lógica "On sale" / "Ahorra X%" | F0-15 | F0-15 |
| `theme/layout/theme.liquid` | Incluir `sv-whatsapp-cta` flotante | F0-14 | F0-14 |

---

## 5. Roadmap técnico del theme

```
Semana 1
├── F0-09 · pull theme local + git commit base
├── F0-10 · auditar locales/es.json + footer/header (limpieza inglés)
├── F0-15 · eliminar lógica de "Oferta" en product-card-badge
├── F0-16 · sv-trust-bar (sección global)
└── F0-14 · sv-whatsapp-cta (snippet flotante)

Semana 2
├── F1-01 · F1-02 · F1-03 (modelo de datos en Admin — sin tocar theme)
└── F2-01 inicio · scaffold product.premium.json con sv-product-trust-panel

Semana 3-4
├── F2-02 sv-product-trust-panel (ya con datos reales)
├── F2-03 sv-product-materials (joins con sv_material_guide)
├── F2-04 sv-product-delivery
├── F2-05 sv-product-warranty
└── Test en 1 producto piloto (BRANDON-1) → validar conversión

Mes 2
├── F3-01 home (index.json + secciones home: sv-hero-premium, sv-shop-by-space, sv-featured-collections, sv-why-santavila, sv-material-grid, sv-advice-block, sv-professionals-block, sv-editorial-guides)
├── F3-04 reescribir descripciones de las 7 colecciones
├── F3-05 collection.premium.json
└── F3-02/F3-03 colecciones por espacio y material (Admin) → asignar template collection.space.json / .material.json

Mes 3
├── F2-06/07/08 (care, faq, compatible-products) en producción
├── F5-02 page.space.json + paginación de espacios
└── F5-03 page.material.json

Mes 4-6
├── F6 (profesionales) y F7 (Flow) — independientes del theme en gran parte
└── F5 (SEO content) — alimenta `page.inspiration.json`
```

---

## 6. Reglas de calidad técnica

### Performance

- **Imágenes con `image_url` y srcset.** Nunca `<img src="{{ image | img_url }}">` sin srcset.
- **Lazy loading** en todas las imágenes secundarias (`loading="lazy"`).
- **Liquid joins moderados.** Si una sección tiene >3 niveles de `for` anidados sobre metaobjects, refactorizar a snippet con `assign` y `find`.
- **Tamaño de hero:** WebP con fallback JPG. Hero principal <300 KB.

### Accesibilidad

- ALT en todas las imágenes (auto desde `featuredImage.altText` cuando existe; fallback a `product.title`).
- Contrastes WCAG AA en paleta Santavila.
- Roles ARIA en acordeones (FAQ, materials).
- Focus visible en todos los CTAs.

### SEO

- H1 único por página (= título de producto / colección / página).
- Schema.org Product en PDP, BreadcrumbList, FAQPage condicional.
- OG tags en todas las páginas (Open Graph + Twitter Card). Imagen OG por defecto = `featured_image` o, si no existe, hero de la marca.

### Editor de Shopify

- Toda sección **`sv-*` debe ser activable/desactivable** desde el editor.
- Settings de sección agrupados con headers descriptivos.
- Defaults sensatos para que la sección renderee algo aunque esté recién insertada.

---

## 7. Limitaciones declaradas

- **No conocemos el theme actual.** Hasta `F0-09` (pull) no podemos decidir si el theme base es Dawn, Sense, un theme premium comprado, o un fork. La estrategia "secciones `sv-*` desacopladas" mitiga el riesgo: si un día se cambia de theme base, las `sv-*` se mueven con relativa facilidad.
- **No conocemos el listado de apps instaladas.** Si hay app de filtros tipo "Globo Filter" o "Boost AI", afecta a F3-06. Verificar con primera oportunidad de acceder a Admin.
- **No conocemos qué FAQ schema renderea hoy el theme**. Riesgo de duplicar marcado si el theme ya emite FAQ schema en otra sección.
- **No conocemos la versión de la API de la storefront** que usa el theme. Métodos como `metaobject` en Liquid requieren versión >= 2024-04. Validar antes de F2-03.

---

## 8. Resumen ejecutivo en 5 frases

1. **19 secciones, 14 templates, 9 snippets** — todos con prefijo `sv-` para no contaminar el theme base.
2. **Cada pieza tiene un metafield/metaobject que la alimenta** — sin Fase 1 (modelo de datos) viva, ningún componente premium se programa.
3. **El orden técnico es:** pull theme → limpieza visible (F0) → modelo de datos (F1) → PDP premium (F2) → home y PLP (F3) → contenido y SEO (F5).
4. **La PDP es la mayor inversión técnica** y la primera que entrega ROI: 1 producto piloto con `product.premium.json` debe estar online en producción al final de la semana 4.
5. **Riesgo conocido:** sin acceso al theme actual no se puede confirmar lenguaje de plantilla (Liquid version), apps de filtros, ni schema preexistente. La estrategia `sv-*` desacoplada reduce el blast radius de cualquier sorpresa.
