# JOURNAL — Santavila / Transformación ecommerce

> Bitácora de ejecución del plan documentado en [`../../Agents-IA/plan_santavila.md`](../../Agents-IA/plan_santavila.md).
> Una entrada por hito. Cada entrada deja claro: **qué se hizo, qué hay que tener en cuenta y qué bloquea lo siguiente.**

---

## Cómo se usa este journal

- Entradas **en orden cronológico inverso** (lo más reciente arriba).
- Cada entrada lleva: fecha, paso del flujo (ver [`../../Agents-IA/INDEX.md`](../../Agents-IA/INDEX.md)), qué se ejecutó, entregables, hallazgos clave, prioridades vivas, decisiones pendientes y siguiente paso recomendado.
- Cuando el paso siguiente se ejecuta, se añade una entrada nueva arriba — **no se reescribe la anterior**.

---

## 2026-06-15 · CONTACTO a medida (nivel top, según estrategia) + memoria del PDF

El dueño recordó que YA tenemos el PDF de estrategia/competencia (`docs/Santavila como líder…pdf`). Guardado en memoria [[santavila_strategy_docs]] para no volver a buscar en web. Clave aplicada: tono **consultivo y cálido**, **asesoría humana = pilar de marca**.

### Nueva sección `santavila-contact.liquid` (reemplaza main-page + form genérico)
- **Mantiene el texto del dueño** intacto (`{{ page.content }}`) como intro centrada (serif + lead).
- **Canales**: Email (hola@santavila.com), WhatsApp (setting `whatsapp`; oculto si vacío), Chat en directo (Shopify Inbox). Tarjetas con icono, hover, honestas. SIN teléfono (no lo tenemos).
- **Canal de Proyectos/Profesionales** (el 20% B2B que la estrategia subraya): callout "¿Un proyecto o varias piezas?" → mailto con asunto.
- **Formulario real** `{% raw %}{% form 'contact' %}{% endraw %}` (Nombre, Email, Teléfono opcional, Mensaje) con inputs redondeados (radio 10), botón pill, feedback ok/err, enlace a privacidad.
- **Atajos de ayuda**: Envíos, Devoluciones, Condiciones, Privacidad.
- Móvil: canales primero (1 toque), luego formulario. `page.contact.json` → solo `santavila_contact`.
- Settings editables: eyebrow, email, whatsapp, chat on/off. **Pendiente dueño: rellenar nº WhatsApp.**

### Nota: 422 de Shopify por `default:""` en setting de texto → se quita el default (text settings no admiten default en blanco).

---

## 2026-06-15 · HOTSPOTS móvil — el quick-add se renderizaba roto → navegar a la ficha

El dueño confirmó que en móvil, al tocar un punto, abría "una cajita modal rota abajo".

**Causa:** en móvil `product-hotspot.js` llama a `#openQuickAddModal()` (quick-add nativo de Dwell). Ese modal en `≤749px` es `position:fixed; margin:auto 0 0 0` **sin `width`** → un `<dialog>` con ancho `fit-content` que queda como una cajita abajo-izquierda.

**Fix (fiable, no a ciegas):** en `product-hotspot.js`, `handleHotspotClick` en móvil/táctil ahora **navega a la ficha del producto** (`data-product-url` del bloque, con fallback a `productLink`) en vez de abrir el modal. Es determinista y la lista "Comprar el conjunto" de abajo cubre la compra del look completo. Desktop sigue con el popover.

---

## 2026-06-15 · MÓVIL 2ª ronda — menú hamburguesa, redondez global, hotspots

Tras probar en móvil el dueño reportó: menú hamburguesa con letras gigantes y "falta info"; campos/botón de contacto sin redondez; Shop the look no se ve.

### Menú hamburguesa (drawer)
- **Letras gigantes:** Dwell ponía el 1er nivel a `var(--menu-font-2xl--size)`. Override en `santavila-header.css`: sans, 18px/500 (parent 15px, child 14px), `text-transform:none`, alto de ítem ≈52px.
- **"Falta info":** añadido **pie de marca** en `header-drawer.liquid` (`.sv-drawer-foot`): Mi cuenta · Buscar · Contacto y ayuda + 3 valores (Fabricado en España · Fácil de montar · Atención personalizada). El menú es `main-menu` (mismas 7 categorías que escritorio); con la letra corregida se ven todas.

### Redondez de marca GLOBAL (ajustes de Dwell estaban a 0)
- `button_border_radius_primary` y `_secondary`: **0 → 100** (pill). Era el default de Dwell; alguien lo había puesto a 0. Ahora **todos** los botones del tema son pill nativamente (incluido el de contacto, 404, etc.), no solo los forzados por CSS.
- `inputs_border_radius`: **0 → 10** → todos los campos de texto (contacto, newsletter, búsqueda, descuento) con la redondez de marca.
- Resuelve el feedback del contacto ("campos y botón con la redondez de siempre") y da coherencia en toda la tienda.

### Shop the look (hotspots) en móvil
- El home SÍ tiene imagen (`bolonia-xl-1.jpg`) + 3 hotspots, pero en horizontal quedaba una franja fina con los puntos amontonados (y: 20/40/52). Fix en `santavila-hotspots.css`: en ≤749px la imagen pasa a **4/5 (vertical)**. La lista de productos de abajo (1 col + "Comprar el conjunto") es la vía de compra robusta en móvil.
- **PENDIENTE de verificar en móvil real:** que al tocar un punto se abra el **quick-add** (es JS nativo de Dwell, no comprobable por CSS). Si no abre, ajustar `product-hotspot.js`.

### Confirmado bien por el dueño en móvil
Home, contacto (salvo redondez, ya corregida), colecciones y producto se ven bien. Tráfico ~95% móvil → foco máximo aquí.

---

## 2026-06-15 · AUDITORÍA MÓVIL COMPLETA (≤749px) — 5 auditores en paralelo + fixes

**Estado:** ✅ Fixes reales + pulido aplicados (10 archivos, subidos 200 + verificados idénticos). Base sólida confirmada: sin desbordamientos masivos, heroes en `svh`, rejillas que colapsan.

**Método:** 5 subagentes auditaron en paralelo el código responsive (no visual; el preview anónimo sirve el live) de: Header/announcement · Home A (hero, manifesto, scenarios, featured, product-row) · Home B (materials, spain, editorial, services, newsletter, hotspots) · PDP · Colección+Footer+Upsell.

### Fallos REALES corregidos
- **Tarjeta de producto compartida** (`santavila-components.css`): `.sv-pcard__name` 23px fijo → 19px en ≤749px (descuadraba rejillas en home/colección/upsell). `.sv-pcard__foot` → `flex-wrap:wrap` y `.sv-pcard__ship` deja de ser `nowrap` (precio + envío se solapaban en 2-col a 375px). **Un fix arregla 3 zonas.**
- **Panel de filtros de colección** (`santavila-collection-grid.liquid`): `min-width:240px` + `position:absolute left:0` anclado al chip → **scroll horizontal** cuando el chip estaba a la derecha. Fix: en ≤749px el panel se ancla a la fila completa (`.sv-facets{position:relative}`, `.sv-facet{position:static}`, panel `left:0;right:0;min-width:0`).
- **Hero home** (`santavila-hero.liquid`): breakpoint 680→749px; padding-top y mínimo del título (54→40px) reducidos para no exceder `100svh`; flecha "Descubre" oculta en móvil (solapaba los CTAs).
- **Barra sticky PDP** (`santavila-product.liquid`): `padding-bottom: env(safe-area-inset-bottom)` (home-indicator iPhone); CTA más compacto a ≤560px; **swatches 32→40px** y pills de variante ~44px de área táctil en móvil.

### Pulido aplicado
- Footer: enlaces con `padding-block` (área táctil) + 1 columna en ≤480px.
- Editorial: colapso a 1 col 620→749px. · Services: 1 col en ≤480px. · `.sv-prow__head` (scenarios + product-row): `flex-wrap:wrap`. · Hero colección: padding-top mínimo 120→92px.

### Pendiente de verificar EN TU MÓVIL (no por código)
- **Hotspots / Shop the Look:** en ≤749px el popover se oculta y el toque debe abrir el **quick-add nativo** de Dwell. Si al tocar un punto no pasa nada en móvil real, hay que ajustar el JS. Único punto potencialmente bloqueante no verificable por CSS.
- Deuda menor (no rompe): token `--ann-h` huérfano; `santavila-product.css` apunta al PDP nativo (no a `.sv-pdp`, código muerto); announcement 10.5px y truncado por elipsis (ok para los 3 textos actuales).

---

## 2026-06-15 · CARRITO — afinado (alineación de fila, hueco del resumen, raya única) + MONEDA UE

**Estado:** ✅ Implementado lo del tema. ⏳ El símbolo € a la derecha depende de un ajuste **global** que cambia el dueño a mano.

### Afinado del carrito (2ª pasada sobre feedback con captura)
- **Fila desalineada (texto arriba, no centrado con la imagen):** la imagen ocupaba 2 filas del grid y el sobrante caía en la fila del error. → **Fix:** fila a **una sola línea** (`grid-template-areas: 'media details quantity price'`), miniatura **cuadrada 96px** product-fit, `align-items: center` → todo centrado vertical con la imagen.
- **Hueco enorme sobre el panel "SANTAVILA" (derecha):** `.cart-summary__inner` tenía `grid-row: 2 / -1` (empezaba en la fila 2 del subgrid → fila del título vacía). → **Fix:** se **aplana** toda la cadena `subgrid`/`--extend` de Dwell (`.cart-summary`, `--extend`, `__inner` a `display:block`/`flex`, `grid-row:auto`), resumen pegado arriba y sticky en `.cart-page__summary`.
- **Doble raya ("raya, espacio, raya") bajo el panel:** el panel tenía borde inferior y `.cart-actions` borde superior. → **Fix:** divisor **único** = borde inferior del panel; se quita `border-top` de `.cart-actions`.

### MONEDA — formato España/UE (afecta a TODA la tienda)
- **Problema:** mostraba `€9.418,00 EUR` (símbolo a la izquierda + "EUR"). Convención correcta: **`9.418,00 €`** (símbolo a la derecha; o palabra EUR sin símbolo, nunca ambos).
- **`money_format` es global y NO editable por API** (PUT /shop.json → **406**; sin mutación GraphQL). → El dueño lo cambia en **Ajustes → Datos de la tienda → Moneda → Editar formato**:
  - HTML sin divisa: `{{amount_with_comma_separator}}&nbsp;€`
  - HTML con divisa: `{{amount_with_comma_separator}}&nbsp;EUR`
- **Lado tema (hecho):** desactivado `currency_code_enabled_cart_items` y `cart_total` en `settings_data.json` (ya estaban los de product). Así el carrito no duplica "EUR"; en cuanto se ajuste el formato global mostrará `9.418,00 €`.
- Regla guardada en memoria [[pricing_currency_format_eu]] + `GUIA_DISENO §3b`.

---

## 2026-06-15 · CARRITO — rediseño integral del sistema (tipografía + alineación + resumen)

**Estado:** ✅ Implementado. El dueño señaló (con captura) "un desastre de tipografías, tamaños y alineaciones" en `/cart`. Se rehace el sistema, no más parches.

### Causas raíz diagnosticadas (en el markup de Dwell)
- **Precios con dos tipografías:** el precio **unitario** (bajo el título) hereda `cart-primary-typography` y el de **línea** (derecha) usa `cart-secondary-typography` → dos familias del tema. → **Fix:** TODOS los importes forzados a `var(--sans)` + `tabular-nums`.
- **Texto "flotando arriba" / imagen desalineada:** la fila (`.cart-items__table-row`) usa `align-items: start` con imagen de 7.5rem. → **Fix:** en la página, `align-items: center` + columnas `92px | 1fr | auto | auto` + divisores `1px var(--line)` y ritmo `24px`.
- **Hueco enorme sobre "Descuento" (derecha):** `.cart-page__summary` usaba `subgrid` + `align-self: stretch` (se estiraba). → **Fix:** `display:block` + `align-self:start` + `position:sticky; top:20px`. Resumen pegado arriba y que sigue al hacer scroll (escala con 1 o 200 líneas).
- **Tamaños sin criterio:** jerarquía fijada → título serif 18px · variantes sans 13px muted · precio línea 16px/600 · total 27px/700 tabular.

### Añadido
- **Panel de marca** al inicio del resumen (llena el hueco que pedía el dueño): eyebrow "Santavila" + lead serif + 3 valores **honestos** (Fabricado en España · Fácil de montar en casa, sin instaladores · Atención personalizada: email, WhatsApp y chat). Oculto en el drawer.
- Resumen como **tarjeta** (`--paper-2` + borde + `--radius-media`).

### Archivos
- `assets/santavila-cart.css` — reescrito entero (sistema unificado, 8 bloques).
- `snippets/cart-summary.liquid` — panel `.sv-cart-brand` antes de `.cart-totals`.
- Subidos vía Asset API (200) + verificado local↔remoto idéntico (md5).

---

## 2026-06-15 · CARRITO — franja de confianza + upsell "Completa el conjunto"

**Estado:** ✅ Implementado. Arranca con `related`; el "completa el conjunto" real necesita config del dueño.

### Franja de confianza (cart-summary)
Bajo los botones de pago: entrega "hasta 30 días según disponibilidad", "pago 100% seguro · garantía legal", "devolución por desistimiento legal". Honesto, reduce ansiedad antes de pagar.

### Upsell (nueva sección `santavila-cart-upsell`, en /cart)
- Reemplaza el `product-list` genérico (colección "all") por productos relacionados con el producto del carrito, con la **tarjeta santavila-product-card** (product-fit).
- **Iteración 1 (fetch dinámico, descartada 2026-06-15):** usaba el componente `product-recommendations` de Dwell (fetch a `/recommendations/products` + `morphSection`). **No mostraba nada para sets/bundles**: `related` venía vacío para el "Set jardín" y el fetch JS añadía fragilidad.
- **Iteración 2 (ACTUAL, server-side robusto):** la sección recorre `cart.items.first.product.collections`, toma la primera colección no-`frontpage` con >1 producto y renderiza hasta N tarjetas (excluyendo el propio). **Sin JS, sin API → siempre se ve.** Verificado: el "Set jardín" está en `sillones-de-exterior` (88 productos) → muestra 4 sofás.
- **Para el "Completa el conjunto" REAL** (cojines/mesa/parasol para un sofá, en vez de "más de lo mismo"): configurar **Productos complementarios** en la app **Search & Discovery** (gratis de Shopify). Convierte 3–5× en carrito (investigación). Pendiente del dueño.

---

## 2026-06-15 · LEGAL — aceptación de políticas + enlaces legales

**Estado:** ✅ Implementado. Pendiente confirmación visual del dueño.

### Contexto
Por RGPD + comercio electrónico (España): el cliente debe **aceptar** privacidad + condiciones de venta antes de comprar, y las políticas deben ser **accesibles**.

### Hecho
- **Las políticas YA existen con contenido** en Shopify (Aviso legal, Privacidad, Condiciones de venta, Devoluciones, Envío, Contacto) — no se redacta nada legal aquí.
- **Checkbox obligatorio en el carrito** (`cart-summary.liquid`, página /cart + drawer): "He leído y acepto la [política de privacidad] y las [condiciones de venta]" con enlaces reales. JS (`santavila-cart.js`) **deshabilita "Finalizar compra" y el pago acelerado hasta marcarlo**. Robusto al re-render AJAX (cart:update + MutationObserver, sin IDs duplicados).
- **Enlaces legales fijos en el footer** (`sv-ft__legal`): Aviso legal · Privacidad · Condiciones · Devoluciones · Envío → URLs `/policies/...` reales.

### Límite honesto (técnico/legal)
El checkbox del TEMA cubre el flujo normal (carrito → pagar). NO es infalible al 100%: un cliente que vaya directo a `/checkout` por URL podría saltárselo, porque el **checkout de Shopify no es editable sin Shopify Plus**. Para 100% blindado: Shopify Plus (checkout UI extensions) o app de consentimiento. Recomendable validar con asesoría legal.

---

## 2026-06-14 · CARRITO — revestido con estilo Santavila

**Estado:** ✅ Capa de estilo aplicada. Falta confirmación VISUAL del dueño + (opcional) mensajes de envío/confianza y upsell.

### Hallazgo
El **carrito y el cart drawer usaban el estilo de Dwell** (no había sección ni capa Santavila). Heredaban las fuentes/colores de marca (vía tokens globales) pero el **layout/botones específicos** eran de Dwell → incoherencia con el resto.

### Hecho
- Nueva capa **`assets/santavila-cart.css`** (cargada en theme.liquid) sobre las clases de Dwell:
  - **"Finalizar compra"** → pill de marca (fondo ink, hover sage-deep), `.shopify-payment-button` pill.
  - **Totales**: titular serif, importes sans **tabular**; nota de IVA en mono.
  - **Líneas**: títulos de producto serif, precios tabular, variantes en `--ink-3`.
  - **Imágenes del carrito** → **product-fit** (contain sobre blanco), coherente con PDP/tarjetas.
  - Descuentos y botones secundarios con redondeo/tipografía de marca.
- Solo estilo; la fontanería de Dwell (cantidades, AJAX, descuentos, checkout) intacta.

### Pendiente
- Confirmación visual del dueño (página /cart + abrir el drawer).
- Opcional (mejora): mensaje de **entrega honesto** ("hasta 30 días…") + **pago seguro** en el carrito, y **upsell "completa el conjunto"** (cross-sell, convierte 3–5× en carrito).

---

## 2026-06-14 · Revisión de la COLECCIÓN

**Estado:** ✅ Auditada. Estaba casi perfecta; solo se ajustó la banda de ayuda.

### Hallazgos
- **Grid** (`santavila-collection-grid`): EXCELENTE — filtros faceted (chips + contador + price range), "Limpiar", contador de productos, **Ordenar** (sort), grid product-fit (tarjeta compartida), **"Cargar más"** (paginación), estado vacío honesto ("No hay productos… Quitar filtros"). No tocar.
- **Hero** (`santavila-collection-hero`): MUY BIEN — imagen (s.image o `collection.image`), **migas de pan** (Inicio/Colecciones/Título, bueno SEO), título, e **intro de la descripción SEO** de la colección (corta antes del FAQ). No tocar.
- **FAQ** (`santavila-collection-faq`): bien diseñada — **extrae las preguntas de `collection.description`** (`<h3>P</h3><p>R</p>`) y **NO se muestra si la colección no tiene FAQ** (degradación elegante, cero claims inventados). No tocar.

### Corregido
- **Banda de ayuda** (`.sv-cband`): CTA **"Hablar con un experto"** (sobre-promete + caía a `#`) → **"Escríbenos"** con destino real **`mailto:hola@santavila.com`**; el CTA solo se muestra si tiene enlace. Texto ya honesto ("atención personalizada, sin compromiso").

### Pendiente del dueño (datos, no técnico)
- Imagen de cada **colección** (Shopify admin → la usa el hero). · Imagen opcional de la banda. · FAQ por colección (añadir `<h3>/<p>` en la descripción) si se quiere.

---

## 2026-06-14 · Auditoría y saneamiento del HOME

**Estado:** ✅ Estructura y honestidad saneadas (2 subagentes auditaron las 11 secciones). Pendiente: imágenes del dueño ([`IMAGENES_HOME_PENDIENTES.md`](IMAGENES_HOME_PENDIENTES.md)).

### Honestidad (corregido)
- **Materiales**: fuera "Teca **FSC**", "**Anticorrosión** real", "**Cero plástico**" (greenwashing sin respaldo); intro reescrito.
- **Profesionales (B2B)**: claims no confirmados (doc técnica, packs, volumen) + CTA a `#` → **sección quitada del home** (reactivable como /profesionales si hay oferta real).
- **Destacada**: placeholder "Colección Cala" + "muestras de tejido" (no confirmado) → reconfigurada a **Sofás de exterior** (88 productos, la categoría más fuerte) con copy honesto y CTA real.

### Bugs / CTAs
- **Newsletter**: el mensaje éxito/error estaba FUERA del `{% form %}` → nunca se mostraba. Movido dentro.
- **CTAs rotos a `#`**: hero CTA2, manifiesto, "ver toda la tienda" → `/collections/all`; **4 escenarios** enlazados a su colección (Áticos→Sofás, Balcón→Sillas, Jardín→Tumbonas, Comedores→Mesas).
- **Editorial**: mantenida (habrá blog); cabecera solo si hay destino + tarjetas no-clicables hasta que existan los artículos.

### Pendiente del dueño
Imágenes de ambiente (hero, 4 escenarios, destacada, materiales, editorial) — documentado. + nº WhatsApp + envío gratis (Excel).

---

## 2026-06-14 · Shop the Look — mejoras de conversión (investigación aplicada)

**Estado:** ✅ Implementadas las 2 de mayor impacto (tras investigar competidores — ver [`INVESTIGACION_SHOP_THE_LOOK.md`](INVESTIGACION_SHOP_THE_LOOK.md)).

### Qué se construyó (en `sections/product-hotspots.liquid` + `santavila-hotspots.css`)
1. **Lista de productos del look** bajo la imagen (numerada, reutiliza los mismos productos de los puntos): foto product-fit + nombre serif + precio real. Garantiza que el 100% vea/compre las piezas aunque no descubra los puntos (clave en móvil). Grid responsive (1 col en móvil).
2. **Botón "Comprar el conjunto completo"**: JS recoge los `selected_or_first_available_variant.id` de todos los productos disponibles del look y hace `POST /cart/add.js` con todos → redirige a /cart. Palanca de AOV (benchmarks +15–39%).

### Técnico
- Itera `section.blocks | where: 'type', '_hotspot-product'` para la lista y los IDs del bundle. Solo estilo/markup Santavila; la fontanería de hotspots de Dwell intacta.
- Validado (Liquid+JS+CSS+schema), Asset API 200, dev == disco.

### Pendiente (Tier 1/2 restante, si se quiere)
- Variantes en botones dentro del quick-add · precio tachado en popover · puntos numerados vinculados a la lista · página dedicada "Ambientes" por escenario · lazy-load/WebP.

---

## 2026-06-14 · Shop the Look (hotspots) — revestido + activado

**Estado:** ✅ Disponible en cualquier página + demo clonada en el home del dev.

### Qué se hizo (petición dueño)
- Revisada la función nativa de Dwell ya presente en el tema: `sections/product-hotspots.liquid`, `blocks/_hotspot-product.liquid`, `assets/product-hotspot.js`. Atributos documentados en [`GUIA_DISENO.md`](GUIA_DISENO.md) §8.
  - Sección: imagen de ambiente, ancho/alto, overlay, `hotspot_color`/`bullseye_color`, color_scheme, tipografía popover.
  - Bloque por punto: `product` + `x-position`/`y-position` (0–100 %). Popover con foto + precio real + quick-add. Desktop popover / móvil quick-add modal.
- **Revestimiento Santavila** `assets/santavila-hotspots.css` (cargado en theme.liquid): popover tarjeta papel + redondeo + sombra, título serif, precio sans tabular, punto con pulso sage. Solo estilo; fontanería intacta.
- **Clonado el del live** (`bolonia-xl-1.jpg` + 3 productos: sofá 3 plazas, set jardín, mesa de centro) al **home del dev** tras "Escenarios" (id `santavila_shop_the_look`).

### Cómo reutilizarlo
Añadir la sección "Shop the Look" en cualquier página desde el editor → elegir imagen de ambiente → añadir bloques de producto y colocar cada punto (x/y) sobre su producto.

### Verificación
Asset API 200 (css/theme.liquid/index.json); re-pull confirma sección + css en remoto.

---

## 2026-06-14 · Auditoría de coherencia (todas las páginas) + GUÍA DE DISEÑO

**Estado:** ✅ Auditoría hecha, claims corregidos y guía documentada ([`GUIA_DISENO.md`](GUIA_DISENO.md)).

### Qué se revisó (home, colección, contacto, PDP)
- **Honestidad:** NO hay reseñas/prensa/testimonios falsos en home ni colección (limpio). Corregido:
  - Home `santavila_services` s4: "**Teléfono** y WhatsApp" → "**Email, WhatsApp y chat**".
  - `santavila-spain` default: "en cada pieza indicamos la provincia de fabricación / proveedores verificados" → "Diseño y fabricación en España, con proveedores nacionales…". ⚠️ La **lista de 5 provincias** del home sigue: PENDIENTE confirmar con el dueño cuáles son reales.
  - `santavila-services` schema: etiqueta de icono "Asesoría" → "Atención".
- **Anchos:** coherentes — todas las secciones usan `.sv-container`; los `max-width` que hay son en `ch` (legibilidad de texto), no estrechan rejillas. (El de los sellos ya se quitó.)
- **Imágenes:** ambiente = `cover` (OK); **tarjetas de producto = `cover`** (recortan) → incoherente con el product-fit de la PDP. PENDIENTE de decisión del dueño aplicar `contain` a las tarjetas.

### Entregable
- **`GUIA_DISENO.md`**: estándares vivos (honestidad, tono, anchos, imágenes producto/ambiente, PDP, swatches, precio, tokens, animaciones, operativa). Referencia para no desviarse.

### Pendiente (dueño)
- Provincias reales de fabricación · aplicar contain a tarjetas de producto (sí/no) · nº WhatsApp · envío gratis (Excel).

---

## 2026-06-14 · PDP — alineación DEFINITIVA: contain + stretch

**Estado:** ✅ Aplicado y sincronizado.

### Clave que faltaba (feedback dueño)
La imagen debe ser **PRODUCT-FIT (no recortar por los lados)** Y estar alineada con la columna. El intento previo usó `object-fit: cover` (recorta/amplía → mesa gigante). La combinación correcta es **`contain` + `stretch`**:
- `align-items: stretch` + `.sv-pdp__gallery` flex + `.sv-gal` `flex:1` + stage/slide `height:100%` → el contenedor se iguala a la altura de la columna (alineación total).
- **`object-fit: contain`** → la foto se ve **completa, nunca recortada**.
- Fondo del visor `#fff` (las fotos de producto son sobre blanco → se funden).
- Quitado el hover-zoom (recortaba, contradecía el product-fit). Móvil: proporción natural.

### Efecto secundario conocido
Con columna muy alta + foto muy horizontal (ambiente), puede quedar banda blanca arriba/abajo. Aceptable (prioridad: no recortar). Si molesta, opciones: limitar altura o fondo por tipo de foto.

---

## 2026-06-14 · PDP — alineación foto↔columna + nota precio "lento al inicio"

**Estado:** ✅ Alineación aplicada y sincronizada. Precio lento = hidratación/preview (no es bug).

### Alineación (feedback dueño: la foto queda más corta que la columna de compra)
- `.sv-pdp__grid` → `align-items: stretch` + `1.3fr 1fr`; `.sv-pdp__gallery` flex column; `.sv-gal` `flex:1`; `.sv-gal__stage` y `.sv-gal__slide.is-active` a `height:100%` (object-fit cover) → la foto principal **se estira a la altura exacta de la columna de compra**. En móvil se resetea a aspect-ratio natural.
- Nota: en productos con columna muy corta la foto podría quedar baja; revisar si aparece algún caso.

### Precio "cacheado/lento las primeras veces" (diagnóstico)
- NO es un bug ni hay caché que limpiar. Causas: (1) **hidratación** de los web components (variant-picker / product-price cargan como módulos con prioridad baja; hasta que hidratan, los primeros clics solo marcan el radio); (2) el **preview** `?preview_theme_id` va al origen sin caché de CDN → cada Section Rendering tarda más que en producción.
- En el tema publicado será notablemente más fluido. Mejora opcional posible: actualización de precio client-side instantánea (sin esperar al fetch) — pendiente de decisión (añade complejidad).

---

## 2026-06-13 · PDP — VALIDACIÓN de precio por variante (crítico)

**Estado:** ✅ Validado (datos + mecanismo + E2E). Bug de la sticky bar corregido. Falta confirmación visual del dueño.

### Por qué (petición dueño)
"Asegúrate de que la variante tiene el precio correcto; no vender a precio incorrecto."

### Hallazgos
- **43 de 243 productos tienen precio VARIABLE por variante** (rangos grandes: una mesa 478,95 €→945 €; otra 1.575 €→2.019 €). El riesgo es real, no teórico.
- **Mecanismo Dwell (confirmado por código):** el variant-picker dispara `variant:update` (bubbles) → el bloque `product-price` lo escucha en su `.shopify-section` y reemplaza `[ref="priceContainer"]` buscando `product-price[data-block-id=…]` en el HTML re-fetcheado. En la PDP custom, price y variant-picker están en la **misma** `.shopify-section` con id de bloque consistente → **se actualiza correctamente**.
- **E2E (datos reales):** pedir `?variant=ID` devuelve el precio EXACTO de esa variante (478,95 / 945 / 181,95 / 315,95 — todos OK).

### Bug encontrado y corregido
- La **barra sticky** tenía el precio en Liquid (estático = primera variante) → en productos de precio variable habría mostrado un precio engañoso al cambiar de variante. **Fix:** JS escucha `variant:update` en la sección y clona el precio real del bloque principal a la sticky (también al cargar). 

### Verificación
Liquid + JSON + balance JS/CSS OK; Asset API 200; dev == disco.

### Pendiente
- Confirmación VISUAL del dueño en un producto de precio variable (cambiar tamaño y ver precio + sticky).

---

## 2026-06-12 · PDP — swatches de color LIMPIOS + ocultar "retiro"

**Estado:** ✅ Aplicado y sincronizado (dev == disco).

### Feedback dueño (captura): "muchos círculos queda feo / horrible" + "¿qué es el retiro?"
- **Color**: los círculos dentro de botones de texto quedaban recargados. **HALLAZGO técnico:** la Admin API NO permite asignar `swatch.color` por mutation (no existe el campo en `OptionValueUpdateInput` en 2024-10/2025-01/04/07; solo `linkedMetafieldValue`). Los swatches nativos se gestionan en **Configuración → Swatches** (global, admite **foto real de tela**) o vía metaobjects+linkedMetafield (complejo, por producto).
- **Solución entregada (tema):** swatches **LIMPIOS** = el botón ES el círculo de color (oculto texto y pill), nombre del color elegido junto al título (JS `.sv-sw-name`, event-delegation robusto a re-render) + tooltip `title`. Mapa de color por nombre (orientativo). Visualmente como la nativa.
- **"El retiro no está disponible"** = aviso de recogida en tienda (pickup) de Dwell. Oculto vía CSS (`pickup-availability-component`, `[class*="pickup-availability"]`) — Santavila es envío, no recogida.

### Límite / nota
- Mapa de color cubre los nombres de Balliu; un valor sin color cae a círculo `--bone` (productos solo-color OK; si hubiera tallas, revisar).
- **Fidelidad real de color** = Configuración → Swatches con las fotos/hex reales de las telas Balliu (global, 1 vez). Pendiente de las telas reales del dueño.

### Verificación
Liquid + JSON + balance JS/CSS OK; Asset API 200; re-pull diff = dev == disco.

---

## 2026-06-12 · PDP — feedback (captura): galería alineada + sellos humanos + color

**Estado:** ✅ Aplicado y sincronizado (dev == disco). Color = solución de tema (orientativa); fidelidad real pendiente.

### Feedback del dueño (con capturas) y solución
1. **Galería desalineada** (la foto principal más corta que la columna; las miniaturas sobresalían) → **rail de miniaturas en `position:absolute` con `top/bottom:0`**, igualado a la altura exacta de la foto principal; scroll interno si hay muchas (nunca sobresale). Móvil: rail horizontal debajo.
2. **Sellos "parecen muy IA"** → reducidos de **6 a 3** (Hecho en España · Garantía legal · Detrás hay personas) con **copy humano**, título "Compra con tranquilidad" sin eyebrow. Rejilla centrada (max-width 1040).
3. **Color en botones de texto** (no convertía; el dueño quiere swatches como Sklum) → Dwell solo pinta swatch si el valor tiene `swatch.color` (dato de Shopify, ausente). Solución inmediata: **mapa de color en el tema** (`:has(input[value="…"])` → círculo de color antes del nombre) + `variant_style: buttons`. Seguro: valor sin mapa → círculo 0px (no se ve).

### Honestidad / límites
- Los colores del mapa son **ORIENTATIVOS** (aproximados por nombre). Fidelidad 100% = imágenes/hex reales de las telas Balliu cargadas como **swatches nativos de Shopify** (Settings → Swatches) — pendiente, idealmente con las fichas reales de tela.
- El mapa cubre los nombres vistos (Balliu); otros productos con otros nombres degradan a texto sin romper.

### Verificación
Liquid + JSON válidos; subida Asset API (200×3); re-pull diff = dev idéntico a disco.

### Pendiente
- **Colores fieles** (telas reales) · importe envío gratis (Excel) · nº WhatsApp.

---

## 2026-06-12 · PDP — feedback dueño: galería 1-foto + recorte + pago informativo

**Estado:** ✅ Aplicado y sincronizado (dev == disco). Pendiente SOLO de colores (esperando captura del dueño).

### Feedback del dueño y decisiones
- **Galería interminable** (apilaba las 10 fotos en grid) → **visor de 1 foto principal grande + miniaturas que la cambian** (clic) + lightbox para ampliar + carga diferida. Se elimina el modelo grid/mosaico y el setting `gallery_columns`.
- **PDP demasiado larga/"interminable y fea"** → recortada a lo esencial: **producto → Por qué Santavila (highlights) → Confianza (sellos)**. Quitadas del template (siguen disponibles como presets reactivables): promise, emocional, servicios/usps (duplicaba sellos), acordeones, recomendaciones.
- **"Más opciones de pago" llevaba directo a comprar** → eliminado el bloque `accelerated-checkout` (dynamic checkout). En su lugar, **collapse informativo** "Métodos de pago aceptados" con los iconos reales (`payment_type_svg_tag`) + texto "pago 100% seguro". NOTA: esto también quita los botones tipo Shop Pay (suben conversión) — reactivar si el dueño los quiere.
- Producto de 1 foto: validado por el dueño (bien).

### Técnico
- Shopify exige que toda sección de `sections` esté en `order` (422 si no) → las secciones recortadas se ELIMINAN del template (no basta sacarlas del order).
- JS galería: miniatura → `setActive` (toggle `.is-active` en slide+thumb); se retira el IntersectionObserver de scroll. Lightbox intacto.
- Validado (Liquid+JSON), subido Asset API (200), re-pull diff = dev idéntico a disco.

### Pendiente
- **Colores** (esperando captura del dueño) · importe envío gratis · nº WhatsApp.

---

## 2026-06-12 · PDP nivel-10 — CIERRE (reveals + variant-picker + tipografía)

**Estado:** ✅ Terminado, validado y sincronizado (re-pull + diff = dev idéntico a disco). PDP nivel-10 cerrada.

### Qué se añadió (todo seguro y degradable)
- **Reveals al scroll (CSS PURO)** en `santavila-components.css`: `@keyframes sv-rise-in` + `animation-timeline: view()`, envuelto en `@supports (animation-timeline: view())` y `prefers-reduced-motion: no-preference`. Aplica a bloques de contenido (promise, highlights items/feats, emocional, sellos, acordeones, servicios). **Sin soporte o con reduced-motion → contenido visible normal; nunca depende de JS.**
- **Variant-picker**: dropdowns con tipografía de marca (`--sans`), radio 12px y altura 48px. Selectores defensivos (no rompen si la estructura difiere).
- **Tipografía fina**: `text-wrap: balance` en el H1 del producto.

### Verificación
Balance Liquid + schema JSON OK; llaves CSS balanceadas (44=44); subida Asset API (200×2); `diff -rq` dev vs disco = idéntico salvo triviales (markets.json, orden de claves index.json).

### Enlace de revisión (dueño, logueado en admin)
- Editor: `https://mueblesexterior.myshopify.com/admin/themes/189114876228/editor`
- PDP directa (10 fotos): `https://santavila.com/products/balliu-silla-exterior-con-brazos-aluminio-estilo-elegante-56-cm-eaf4a34a?preview_theme_id=189114876228`

### Pendiente (datos del negocio, no técnico)
- Importe envío gratis (Excel de costes) · nº de WhatsApp.

---

## 2026-06-12 · Auditoría nivel-10 PDP (2/2): estética + conversión

**Estado:** ✅ Aplicado, validado y sincronizado en dev (re-pull + diff = idéntico a disco). Revisión íntegra OK.

### Mejoras aplicadas (todas seguras: hover/spacing/jerarquía; sin JS frágil ni animaciones que oculten contenido)
- **Galería:**
  - Zoom suave al hover sobre la foto (scale 1.045, solo `hover:hover`).
  - Indicador "ampliar" (lupa) en la esquina de cada imagen ampliable (`:has()` + data-uri SVG; degrada sin romper si el navegador no soporta `:has`).
  - **Mosaico editorial**: la última foto impar ocupa el ancho completo en el stage 2-up (clase `sv-gal--grid`, solo desktop). `gallery_columns` ahora se castea a int (`| plus: 0`).
- **Columna de compra:**
  - Precio con `tabular-nums` (cifras alineadas).
  - CTA add-to-cart: sombra al hover + micro-scale en `:active`.
  - Barra sticky: sombra superior para despegarla del contenido.
- **Confianza (sellos):** elevación sutil al hover (borde sage + translateY).
- **Highlights:** hover-zoom en la imagen, coherente con galería y cards de home.

### Decisión consciente (no romper)
NO se añadieron animaciones de entrada por scroll que pongan el contenido en `opacity:0` dependiendo de JS (violaría "contenido visible sin JS" y es lo más propenso a romperse). Si se quiere ese nivel de "wow", la vía segura es scroll-driven CSS puro (`animation-timeline: view()`), que degrada a contenido visible — pendiente de decisión del dueño.

### Verificación
Balance Liquid + schema JSON OK en los 3 archivos; subida por Asset API (200); re-pull + `diff -rq` confirma dev == disco salvo trivialidades (markets.json, orden de claves en index.json).

### Pendiente
- Importe envío gratis (del Excel de costes) y nº de WhatsApp.
- Si el dueño lo quiere: reveals scroll-driven CSS-puras; pulido del variant-picker de Dwell.

---

## 2026-06-12 · Auditoría nivel-10 PDP (1/2): saneamiento de claims falsos

**Estado:** ✅ Aplicado y subido a dev (Asset API, 200). Pendiente: 2 datos del dueño (importe envío gratis, contactos) y mejoras estéticas (parte 2).

### Por qué (la prioridad real del nivel-10)
La PDP estaba llena de **afirmaciones inventadas** que chocan con la regla de no falsear nada y con riesgo legal (reseñas/prensa falsas = publicidad engañosa). Antes de pulir estética, había que sanear. Ver [[santavila_facts]].

### Decisiones del dueño (2026-06-12)
- **Atención:** email, **WhatsApp** y **chat (Shopify Inbox, se activará)**. NO teléfono.
- **Envío:** gratis **desde un importe** (umbral pendiente de confirmar). Mientras tanto, solo se afirma el plazo.
- **Reseñas:** sin reales aún → fuera nombres ficticios, estrellas y "Verificada". Prueba social genérica/honesta.
- **Prensa:** sustituir medios inventados por **sellos reales**.

### Qué se saneó
- **Cabecera PDP:** eliminado el rating de estrellas inventado (bloque `review` fuera de la cabecera y del `product.json`). Trust row: envío sin "lo gestionamos nosotros" (es deslocalizado), atención por "email, WhatsApp y chat".
- **Emocional:** eliminada la reseña ficticia (Marta G.); reconvertida a statement de marca a pantalla completa + texto de apoyo. 100% honesto.
- **Social → reescrita como "Confianza":** fuera prensa inventada (El País/AD/Elle Decor…), testimonios ficticios y UGC vacío. Ahora 6 **sellos reales** (Hecho en España, Pago seguro, Garantía legal, Devolución legal, Atención personalizada, Fácil de montar) + bloque "Qué incluye" sin nº de bultos inventado.
- **Servicios + Acordeones (`.liquid` y `product.json`):** envío "deslocalizado (proveedor logístico externo)", quitado "Envío gratis a península", "asesoría"→"atención personalizada", teléfono→email/WhatsApp/chat.

### Vía técnica
Subida **archivo por archivo vía Asset API** (no `--only`), con validación previa de balance Liquid + schema JSON. Lección [[shopify_push_path_trap]].

### Pendiente (para cerrar honestidad)
- **Importe del envío gratis** (umbral €) → para añadir el claim "envío gratis desde X".
- **Email de contacto + número/enlace de WhatsApp** → para enlazar la atención.
- Parte 2: mejoras estéticas/conversión nivel-10 (jerarquía, galería, microinteracciones).

---

## 2026-06-12 · 🚨 INCIDENCIA: PDP "sin producto" — 5 archivos nunca llegaron al tema dev

**Estado:** ✅ Resuelto. Causa raíz encontrada y archivos re-subidos vía Asset API (todos 200).

### Síntoma (dueño)
"Te has cargado el announcement y cuando entras en una página de producto no se ve el producto."

### Causa raíz (la importante)
El tema vive en **`theme/`**, no en la raíz del repo. Hice los `shopify theme push --only ...` **desde la raíz, sin `--path theme`**. El CLI avisó "doesn't seem like you're running this command in a theme directory", resolvió `sections/...` contra la raíz (no existen ahí), **subió 0 archivos y aun así imprimió "pushed successfully"**.
Consecuencia: el tema dev #189114876228 quedó **sin 5 archivos** (404 confirmado vía Asset API):
`sections/santavila-product.liquid`, `sections/header-announcements.liquid`, `sections/header-group.json`, `assets/santavila-header.css`, `assets/santavila-product.css`.
Como `templates/product.json` apunta a `santavila-product` y **el archivo de la sección no existía → la PDP se renderizaba vacía** ("no se ve el producto"). El announcement, igual.

### Diagnóstico ejecutado
- `shopify theme pull --path /tmp/devtheme` + `diff -rq` → reveló los archivos disk-only.
- Asset API `GET assets.json?asset[key]=...` → 404 en los 5; 200 en santavila-tokens.css (ese sí estaba).
- Confirmado que el preview anónimo (`?preview_theme_id=`) **siempre sirve el tema live**, no el dev → no sirve para verificar; hay que mirar vía Asset API / editor.

### Solución
- Subidos los 5 archivos vía **Asset API (PUT)**, leyendo de `theme/…` (determinista). Verificado 200 en los 5.
- Re-pull + `diff -rq`: remoto == disco salvo trivialidades (`config/markets.json` y orden de claves en `index.json` — sin efecto en render).
- Validado: Liquid de la PDP balanceado (if 14/14, for 3/3, case 1/1, unless 1/1) y schema JSON válido.

### Lección (memoria [[shopify_push_path_trap]])
`push`/`pull`/`dev` SIEMPRE con `--path theme`. Nunca fiarse del "success": verificar existencia real vía Asset API.

---

## 2026-06-12 · Fix galería 1-imagen + announcement SLIDER (ñ resuelta)

**Estado:** ✅ Aplicado y subido a dev theme #189114876228 (push token, theme dev parado).

### Qué se ejecutó (feedback dueño con captura)
- **Galería adaptativa por nº de fotos** (`product.media.size`): si el producto tiene **1 sola imagen** → `.sv-gal--single` (sin rail de miniaturas, 1 columna, slide cuadrado a ancho completo). Arregla la foto "partida en dos / a media anchura con hueco" que se veía en productos de 1 imagen. Con ≥2 fotos sigue el rail + columnas (`gallery_columns`).
- **Announcement convertido en SLIDER** de 3 mensajes que rotan (auto-play nativo de Dwell, `blocks.size > 1`, speed 4s):
  1. `FABRICADO EN ESPAÑA` → 2. `FÁCIL DE MONTAR EN CASA` → 3. `ATENCIÓN PERSONALIZADA` → vuelve a empezar.
- **Flechas chevron de Dwell ocultas** (`slideshow-arrows`/`.slideshow-control { display:none }`): rota solo, sin controles; slides a ancho completo y centrados.

### Cómo se resolvió la "ñ" (España sin ñ → "ESPANA")
- Causa raíz: el `text-transform: uppercase` sobre la fuente mono se comía la Ñ.
- Fix: el texto se escribe **ya en mayúsculas con Ñ explícita** (U+00D1) y el bloque va con **`case: none`** → no hay `text-transform`, el carácter Ñ se pasa tal cual a la fuente y se renderiza. Mantiene el look uppercase del README sin el bug.
- Bonus: cada mensaje es corto → entra en **una sola línea** (con `nowrap` + elipsis de respaldo). Resuelve el salto a 2 líneas.

### Decisión de copy
- Se simplificó "Atención personalizada para tu terraza" → **"ATENCIÓN PERSONALIZADA"** (el dueño dijo "con atención personalizada sobra"). Sin claims inventados — ver [[santavila_facts]].

### Pendiente
- Confirmación visual del dueño del slider + galería 1-imagen.

---

## 2026-06-12 · PDP nivel-10 — galería bespoke + sticky qty

**Estado:** ✅ Construida, schema-válida y en dev theme (push token + verificación API). Falta confirmación VISUAL del dueño (theme dev se atascó).

### Qué se ejecutó (feedback dueño: Zara Home/Sklum/Westwing)
- **Galería bespoke** (`product.media`): rail vertical de miniaturas (clic→scroll+activo), **stage 2 fotos por fila** (setting `gallery_columns`), vídeo soportado. Reemplaza la galería de Dwell (perdemos su auto-sync por variante; aceptado).
- **Lightbox full-screen** (prev/next, contador, teclado, clic-fuera) → arregla el zoom "fuera de contexto".
- **Sticky add-to-cart con stepper de cantidad**: setea la cantidad real del form de Dwell antes de proxy-clicar el add. Carrito intacto.

### Hallazgos / incidencias
- `range` de Shopify exige **≥3 valores** (min/max/step) → para 1–2 usar `select`.
- **theme dev se atasca con su fichero `.tmp` al guardar rápido** ("contains illegal characters" / 500). Solución: parar theme dev + `theme push` por token (estable). Confirmado en memoria [[shopify_two_auth_rails]].

### Pendiente
- Confirmación visual del dueño (re-activar theme dev OAuth o revisar shareable link).
- Specs metafields + reseñas (app) con su OK.

---

## 2026-06-12 · PDP nivel-10 — pulido UI (tags, guía medidas, sticky bar)

**Estado:** ✅ Pulido UI aplicado y verificado en render local.

### Qué se ejecutó
- **Tags de galería** honestos (Hecho en España, badge metafield, "Pocas unidades" si inventory<=6).
- **Guía de medidas (modal `<dialog>`)** con setting richtext `size_guide`; enlace bajo variantes; cierre botón/fuera/Esc.
- **Sticky add-to-cart bar** propio (thumb+nombre+precio+CTA) que **proxy-clica el add-to-cart real de Dwell** (al perder de vista la buy-box vía IntersectionObserver). Carrito intacto.

### Pendiente (con tu OK / apps)
- Specs estructuradas → metafields `santavila.*` (toca productos).
- Reseñas reales → app (Judge.me).
- Galería rail+stage 100% fiel (miniatura vídeo, contador) — opcional.

---

## 2026-06-12 · PDP nivel-10 — sección de producto bespoke (validada)

**Estado:** 🔄 Foundation validada (carrito vivo). Sigue el pulido de conversión.
**Decisión dueño:** buy-box bespoke máximo techo. Referencias: Sklum, Zara Home, Westwing (Westwing analizado vía WebFetch; los otros 403 bot).

### Hallazgo clave (desbloquea todo)
- Una **sección propia** puede reusar los bloques reales de Dwell con `{%- content_for 'block', type: 'X', id: 'Y', closest.product: closest.product -%}` (galería, review, price, variant-picker, buy-buttons). → maquetado 100% propio + carrito/variantes/Shop Pay intactos. Los ids del content_for deben existir como bloques en product.json. Verificado: HTTP 200, carrito vivo.

### Qué se ejecutó
- `sections/santavila-product.liquid`: columna de compra bespoke (rating, H1 serif, USP metafield, precio grande+IVA, escasez real por inventory, trust row honesto, iconos de pago reales) + bloques Dwell por content_for. product.json: `main` → `santavila_product`.

### Síntesis de conversión (referencias)
- Above-the-fold que vende: precio prominente, swatches visibles, escasez real, plazo claro, add-to-cart enorme, trust + iconos de pago, atención personalizada. Specs estructuradas (metafields, pendiente). Prueba social (reseñas/app, pendiente).

### Siguiente (pulido nivel-10)
- Galería rail+stage fiel (tags, zoom, contador) · specs estructuradas (metafields `santavila.*`) · reseñas reales (app) · micro-UX · guía de medidas modal · sticky bar afinado.

---

## 2026-06-12 · Limpieza de claims falsos + espaciado (feedback dueño)

**Estado:** ✅ Corregido y verificado en render local.

### Qué se ejecutó
- **CRÍTICO — claims inventados eliminados de TODO el tema** (announcement, home services, PDP buy column + USPs + acordeones, featured, collection band): "enviado en 24h", "7–10 días", "30 días de prueba en casa", "SeQura / a plazos", "garantía 3/5 años", "asesoría humana".
- **Hechos reales (dueño 2026-06-12):** envío **deslocalizado** (un tercero lo gestiona), recepción **3–5 días** laborables península. Sin prueba 30 días. Sin financiación confirmada. Garantía → "garantía legal" (sin años inventados). "Asesoría humana" → **"Atención personalizada"**. Guardado en memoria `santavila_facts` como regla DURA.
- **Espaciado apretado:** `.sv-section` padding-block `clamp(64,10vw,150)` → `clamp(40,5vw,76)` (el dueño veía demasiado hueco en blanco entre secciones).

### Decisiones pendientes / a confirmar
- **Conflicto de plazo de envío:** el dueño dice 3–5 días; `Agents-IA/plan_santavila.md` decía "hasta 30 días según proveedor". Confirmar cuál es canónico.
- **Casing** (mayúsculas/minúsculas): el dueño nota mezcla; revisar con ejemplos concretos.

### Siguiente
- Pase nivel-10 de la PDP (referencia Sklum del dueño): conversión, cercanía a la venta, columna de compra bespoke.

---

## 2026-06-12 · Fase 8 — PDP completa (estructura + contenido)

**Estado:** ✅ Estructura completa y verificada en render local (HTTP 200, carrito intacto). Falta pase de calidad "nivel-10" (lo hará el dueño con referencias tipo Sklum).

### Qué se ejecutó
- Buy column: reordenada al README (rating→H1→precio→IVA/BNPL→variantes→add-to-cart→risk-remover) reusando bloques de Dwell + text blocks de valor.
- Secciones bespoke: `santavila-pdp-promise`, `-highlights` (3 beneficios + 3 características), `-emotional` (sage-900 + review), `-accordions` (medidas/envío/devoluciones/FAQ), `-social` (prensa + 3 testimonios + UGC + qué incluye). Company USPs reusando `santavila-services`. Related = product-recommendations de Dwell.

### Hallazgos clave
- **El `text` block de Dwell es richtext sanitizado**: elimina `class`, `<div>`, `<span>` y Liquid al inicio. → No sirve para chips/USP con clases. Pendiente nivel-10: columna de compra bespoke propia.
- **NO mezclar `theme dev` (OAuth) con `theme push` (token)** sobre el mismo dev theme: chocan y theme dev muestra "Failed to Upload" (500). Con theme dev activo, sincronizar SOLO guardando archivos (hot-reload).

### Siguiente
- **Pase nivel-10 de la PDP** (cercanía a la venta, conversión, referencias del dueño): columna de compra bespoke (USP, BNPL real, chips, guía de medidas modal, sticky bar afinado), galería rail+stage fiel, micro-UX.

---

## 2026-06-12 · Fase 8a (pase 1) — PDP restyle sobre Dwell

**Estado:** 🔄 En curso (primer pase aplicado y verificado en render local).
**Arquitectura (confirmada por el dueño):** reestilizar `product-information` de Dwell (galería + columna de compra con su carrito/variantes/Shop Pay/sticky-bar nativos) + bloques bespoke + galería/contenido a medida. NO hand-roll del form.

### Qué se ejecutó
- Reconocimiento: Dwell trae todo el core funcionando (gallery carousel+thumbnails, `product-details` sticky, `product-form-component`, add-to-cart, y **sticky-add-to-cart bar nativo**). Clases reales mapeadas.
- `assets/santavila-product.css`: H1 serif, precio prominente, add-to-cart pill ≥56px, swatches 44px, media redondeada (--radius-media), sticky bar en papel+blur.
- `product.json`: galería rail vertical + media_radius 14; título serif.

### Siguiente
- 8a (sig): bloques bespoke en la columna (USP 1 línea, línea BNPL SeQura, "IVA incluido · envío gratis", risk-remover "30 días", chips USP).
- 8b: promise + beneficios + características + emocional + review. 8c: acordeones (medidas/specs, envío, devoluciones, FAQ) + guía de medidas. 8d: social proof + related + sticky bar afinado.
- Recordatorio: sin montaje a domicilio.

---

## 2026-06-12 · Patrón de altura de hero (token --hero-h)

**Estado:** ✅ Aplicado y verificado en render local.

### Qué se ejecutó (feedback del dueño)
- Heroes con altura inconsistente (home 100svh, colección 56vh). Definido patrón común por **token**: `--hero-h: 100svh` (pantalla completa) y `--hero-h-secondary: 80svh` (casi completa, deja asomar el grid). `svh` = estable en móvil.
- Home usa `--hero-h`; colección usa `--hero-h-secondary`. Selector "Pantalla completa / Casi completa" por instancia. Decisión del dueño: home entera + colección casi entera.

### Siguiente
- Más revisión visual de la tienda con el dueño; luego Fase 8 (PDP).

---

## 2026-06-12 · Colección — fix hero + FAQ bespoke (full-width + JSON-LD)

**Estado:** ✅ Aplicado y verificado en render local (theme dev OAuth activo).

### Qué se ejecutó (feedback del dueño)
- **Hero volcaba toda la `collection.description`** (intro + `<h2>Preguntas frecuentes</h2>` + FAQ) → salía un "título pequeño" (h2) y la FAQ dentro del hero. Fix: el hero corta antes del primer `<h2>`, limpia HTML y trunca → solo la intro.
- **FAQ recuperada como sección bespoke** (`santavila-collection-faq.liquid`): parsea pares pregunta/respuesta de la descripción, acordeones on-brand a ancho completo (heading sticky izq + acordeones dcha), y emite **JSON-LD FAQPage** (SEO/GEO). Se oculta si no hay FAQ. collection.json: hero + grid + FAQ.

### Hallazgos / método
- **QA visual ahora vía inspección del render local** (`curl http://127.0.0.1:9292/...`) con theme dev (OAuth). Permite verificar estructura real (encabezados en hero, acordeones, JSON-LD) aunque no pixeles.
- Las capturas headless con Chrome NO funcionaron aquí; además un `pkill` amplio cerró el Chrome del dueño (error, registrado en memoria `no_broad_process_kill`).

### Siguiente
- Más revisión de colección con el dueño (vía su ojo + inspección local). Luego Fase 8 (PDP).

---

## 2026-06-12 · Revisión colección — UX de filtros + radio global + sin FAQ

**Estado:** ✅ Aplicado (`37a0324`). Pendiente verificación visual del dueño.
**Quién/qué:** revisión del dueño sobre la colección + Claude (Opus 4.8).

### Qué se ejecutó (feedback del dueño)
- **Filtros apelotonados → desplegables por faceta**: cada filtro (`Material ▾`, `Precio ▾`, `Disponibilidad ▾`…) abre un panel con checkboxes, contador por opción, contador de activos en el chip, "Limpiar" y caret animado. JS: cierra al abrir otro / clic fuera / Esc. Mucho mejor UX que los chips planos.
- **Radio de imagen global**: nuevo token `--radius-media: 14px` aplicado a TODAS las cards/media (pcard, escenarios, destacada, materiales, editorial, banda). Patrón de diseño consistente. Heroes full-bleed sin radio (a propósito). Footer payicon conserva 4px.
- **FAQ fuera de sitio** (estrecha, en Accesorios) → eliminada de `collection.json`. La colección queda hero + grid limpio.

### Hallazgos clave / honestidad
- **No puedo verificar visualmente el dev theme por curl** (el `preview_theme_id` exige sesión de admin; el muro de contraseña bloquea el render anónimo). Solo valido sintaxis/schema en `theme push`. Por eso se colaron detalles de UX (filtros apelotonados, FAQ) que el dueño sí vio. **Para QA visual: el dueño revisa o reactivamos `theme dev` (OAuth) en ciclos de iteración.**

### Prioridades vivas
- Verificación visual del dueño de la colección revisada.
- Metafields `santavila.*` + Search & Discovery → activan los filtros de marca (material, quick ship).

### Siguiente paso recomendado
- Cerrar la revisión de colección con el dueño; luego **Fase 8 — PDP**.

---

## 2026-06-12 · Rediseño tema — Fase 7 (plantilla de Colección)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Completada (`35975df`). Pendiente verificación visual del dueño.
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8). Decisión: bespoke + filtros nativos de Shopify.

### Qué se ejecutó
- **Card compartida (DRY):** `snippets/santavila-product-card.liquid` (home + colección). El CSS `.sv-pcard*` se movió a `santavila-components.css` (global, disponible en ambas plantillas). `santavila-product-row.liquid` ahora hace `render` del snippet.
- **`santavila-collection-hero.liquid`:** hero 56vh — breadcrumb mono (Inicio / Colecciones / título), H1 serif = `collection.title`, descripción (`collection.description` o override); imagen de colección o degradado sage; bajo el header transparente.
- **`santavila-collection-grid.liquid`:** filter bar **sticky** (top = `--header-height`) con chips desde `collection.filters` (faceted, Search & Discovery), popover de **precio** (min/max), **orden** nativo (`sort_by` preservando filtros) + contador; grid 3 col con la card Santavila; **banda editorial** intercalada (`grid-column:1/-1`, solo en página 1); **"Cargar más"** con mejora progresiva AJAX (append sin recarga; fallback a navegación si falla JS).
- **`collection.json`:** hero + grid Santavila + `collection-faq` (se conserva por su JSON-LD/SEO).

### Hallazgos clave
- Filtrado server-side Shopify-native vía `collection.filters` (URLs `url_to_add`/`url_to_remove`) + `paginate`. Robusto y SEO-friendly; el AJAX de "Cargar más" es solo mejora progresiva.
- Los chips de **marca** (material, Quick ship) sólo aparecerán cuando existan los **metafields `santavila.*` + configuración de Search & Discovery**. El grid los renderiza automáticamente en cuanto existan (ahora muestra los filtros nativos: disponibilidad, precio, opciones).

### Prioridades vivas
- Configurar Search & Discovery + metafields para los filtros de marca.
- Imágenes (hero de colección, banda editorial) — cliente.
- Verificación visual del dueño en una colección real.

### Siguiente paso recomendado
- **Fase 8**: Ficha de producto (PDP) — la "Perfect Product Page" del README (la más rica: galería, columna de compra sticky, acordeones, social proof, sticky add-to-cart). Recordar: **sin montaje a domicilio** ([[santavila_no_assembly]]).

---

## 2026-06-12 · Revisión home — modelo self-assembly + pulido

**Estado:** ✅ Correcciones aplicadas y pusheadas al dev theme.
**Quién/qué:** revisión del dueño sobre la home + Claude (Opus 4.8).

### Qué se ejecutó
- **CRÍTICO — modelo de negocio:** Santavila **NO ofrece montaje a domicilio** (self-assembly: el cliente lo monta en casa). Eliminado de todo el proyecto:
  - **Tema:** announcement ("Fabricado en España · **Fácil de montar en casa** · Asesoría humana…") y sección Servicios (col. montaje → "Fácil de montar en casa / llega en pocos bultos con instrucciones ilustradas; lo montas tú").
  - **Handoff:** `README.md` (nota de modelo destacada + línea Servicios + ejemplo metafield `assembly`) y los 3 prototipos (`Santavila Tienda/Coleccion/Producto.html`, este último con 2 referencias de envío).
  - `Agents-IA/*` ya estaba correcto ("no incluye montaje") — el error venía solo del handoff de diseño. Regla en memoria `santavila_no_assembly`.
- **Announcement a una sola línea**: eliminado el límite de 680px de Dwell; `nowrap` + elipsis en `santavila-header.css` (antes saltaba a 2 líneas).
- **Pulido de composición**: `text-wrap: pretty` en párrafos y `balance` en titulares de todas las secciones (`santavila-components.css`) → rag limpio, sin huérfanas ni "saltitos".

### Hallazgos clave
- El handoff de diseño **contradecía** el modelo de negocio ya documentado en el plan. Lección: validar copy del handoff contra `Agents-IA/plan_santavila.md`.

### Siguiente paso recomendado
- Verificación visual del dueño (announcement en una línea, alineación). Luego **Fase 7** (plantilla de Colección).

---

## 2026-06-12 · Rediseño tema — Fase 6 (cierre de la HOME)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Home 100% Santavila (`6a0aaec` + `381e53a`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8). Premisa: la mejor tienda de decoración exterior del mundo (Shopify-native, responsive, cero errores de maquetado).

### Qué se ejecutó
**6a — cuerpo de la home** (`6a0aaec`)
- `santavila-editorial.liquid`: revista 1 card grande + 2 pequeñas (bloques de artículo).
- `santavila-pro.liquid`: Profesionales, reutiliza el componente global `.sv-feat` (espejado) + botón sage.
- `santavila-services.liquid`: 4 columnas (icono por `select` + título + texto).
- `santavila-newsletter.liquid`: sage-900 + `{% form 'customer' %}` real con estados éxito/error.
- `index.json`: insertadas en orden README y **eliminadas las 7 secciones demo de Dwell** → la home renderiza solo las 11 secciones Santavila.

**6b — footer** (`381e53a`)
- `santavila-footer.liquid`: marca (logo del tema + eslogan + social en pills) · 3 columnas por `link_list` (menús reales colecciones/información/condiciones) · copyright + **iconos de pago reales** (`shop.enabled_payment_types | payment_type_svg_tag`).
- `footer-group.json`: reemplazado el footer de Dwell + email-signup redundante por la sección Santavila.

### Hallazgos clave
- `tag: null` no es válido en el schema de una sección (debe ser string u omitirse). En bloques sí se permite.
- Reutilizar clases CSS entre secciones funciona porque Dwell agrega todos los `{% stylesheet %}` en un único CSS global (Profesionales reusa `.sv-feat` del destacado).
- El footer de Dwell ya traía menús reales (colecciones, footer, información) → el footer bespoke los reaprovecha vía `link_list`.

### Prioridades vivas
- **Imágenes**: hero, escenarios, destacada, materiales, editorial — pendientes de foto del cliente (empty-states con fondo bone/sage cuidados).
- **Contenido**: nav del header y columnas del footer dependen de menús + colecciones por escenario; data model de metafields `santavila.*` para cards/PDP/filtros.

### Siguiente paso recomendado
- **Fase 7**: plantilla de **Colección** (`collection.json`): hero de colección, filter bar sticky (Search & Discovery), grid 3 col con banda editorial intercalada. Luego **Ficha de producto (PDP)** — la más compleja (Perfect Product Page).

---

## 2026-06-12 · Rediseño tema — Fase 5 (Materiales + Fabricado en España)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Completada (`fd6c452`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8). Premisa: "la mejor tienda online de home del mundo".

### Qué se ejecutó
- `sections/santavila-materials.liquid`: bloque oscuro sage-900 (scheme-5), media + lista de 4 materiales en bloques repetibles (swatch de color, nombre, descripción, tag mono) con hover de sangrado. Copy: cuerda náutica / aluminio termolacado / teca FSC / piedra y hormigón.
- `sections/santavila-spain.liquid`: banda bone centrada (scheme-4) con el arco SVG de marca (un único gesto), H2 serif, texto y provincias en chips mono pill (textarea, una por línea).
- `templates/index.json`: insertadas tras "Lo más deseado". Sincronizado con `theme push` (token).

### Hallazgos clave
- Las secciones con esquema no-default (dark/bone) deben fijar `background-color: var(--color-background)` y `color: var(--color-foreground)` en su wrapper: la clase `.color-scheme-N` define las CSS vars pero no pinta el fondo del elemento por sí sola.

### Prioridades vivas
- Imágenes reales (hero, escenarios, destacada, materiales) — foto del cliente.
- Data model de metafields `santavila.*` (alimenta cards, badges, plazos, filtros).

### Siguiente paso recomendado
- **Fase 6**: Editorial "El exterior bien vivido" (1 card grande + 2 pequeñas) + Profesionales (CTA sage) + Servicios (4 columnas) + Newsletter + Footer, cerrando la home. Después: plantillas de Colección y Ficha de producto (PDP).

---

## 2026-06-12 · Rediseño tema — Fase 4 ("Lo más deseado")

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Completada (`dbc2a22`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8).

### Qué se ejecutó
- `sections/santavila-product-row.liquid`: grid de product cards con **datos reales** (loop sobre colección). Card de marca: media 4/5 + hover zoom, badge opcional (`metafield santavila.badge`), categoría mono (`product.type`), nombre serif, precio `money_without_trailing_zeros` + compare_at tachado, plazo desde `santavila.lead_time_type/label` (Quick ship / Bajo pedido en arcilla), swatches desde `value.swatch.color`. Corazón de favoritos opcional (off; requiere app wishlist).
- `templates/index.json`: insertada tras la destacada, colección `frontpage` (8 productos), 4 columnas.
- Sincronizado al dev theme con `theme push` (token) — flujo de preview elegido por el dueño.

### Hallazgos clave
- La colección `frontpage` ("Home page") tiene 8 productos → el grid renderiza 4 reales.
- Catálogo sin metafields `santavila.*` todavía → badge/plazo/swatches degradan a vacío. Cuando se cree el data model (README) las cards se completan solas.

### Prioridades vivas
- Data model de producto (metafields `santavila.*`: material, lead_time, origin, warranty, scenario, product_usp, badge) — alimenta cards, PDP y filtros.
- Imágenes reales del hero/escenarios/destacada (foto cliente).

### Siguiente paso recomendado
- **Fase 5**: Materiales (bloque oscuro sage-900: media + 4 materiales con swatch) y/o "Fabricado en España" (banda bone con arco + provincias).

---

## 2026-06-12 · Rediseño tema — Fase 3 (banda editorial home)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Fase 3 completada (`a0a8d16`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8) · Shopify CLI 3.94.3.

### Qué se ejecutó
- `assets/santavila-components.css`: primitivas compartidas del design system (botones pill `sv-btn` + variantes, `sv-ulink`, `sv-eyebrow`, `sv-container`, `sv-section`). El hero se refactorizó para consumirlas.
- `sections/santavila-manifesto.liquid`: statement serif a 2 columnas (parte destacada + continuación atenuada) + párrafo + ulink.
- `sections/santavila-scenarios.liquid`: header + 4 cards de escenario (bloques repetibles: imagen, número mono, nombre serif con flecha en hover, enlace). Áticos y terrazas / Balcón / Jardín y porche / Comedores.
- `sections/santavila-featured.liquid`: Colección Cala (media 4/4.6 con tag, eyebrow, H2, 3 métricas: desde 779€ / 7-10 días / 5 años, CTAs).
- `templates/index.json`: las 3 secciones insertadas tras el hero.

### Entregables
- 3 secciones nuevas + `santavila-components.css` (todas bajo `theme/`).

### Hallazgos clave
- **Límite de 25 caracteres** en el `name` de un `{% schema %}` (y de presets/bloques). "Santavila Colección destacada" (29) rompía el build → renombrado a "Santavila Destacada".
- **La sesión OAuth de `shopify theme dev` caduca entre fases** ("CLI credentials are invalid") y corta la sincronización. Workaround robusto sin re-login: `shopify theme push --theme 189114876228 --nodelete` con `SHOPIFY_CLI_THEME_TOKEN` (el token `shpat_` SÍ vale para push/validación de schema). El push valida el schema antes de subir. Preview por navegador con el shareable link `?preview_theme_id=189114876228`.

### Prioridades vivas
- Imágenes reales (image_picker) de hero / escenarios / destacada: pendientes de foto del cliente (mientras, degradado/bone de marca).
- Enlaces de los 4 escenarios → dependen de crear las colecciones por escenario.

### Decisiones pendientes
- ¿Mantener `theme dev` (OAuth, hot-reload pero re-login cada sesión) o flujo `theme push` por token + shareable link (estable, sin hot-reload)?

### Siguiente paso recomendado
- **Fase 4**: "Lo más deseado" (grid de 4 product cards) o Materiales (bloque oscuro), siguiendo el orden del README.

---

## 2026-06-11 · Rediseño del tema (Dwell) — Fases 0–2

**Paso del flujo:** Theme rebuild — rama `redesign`, tema base **Dwell 3.5.1**.
**Estado:** 🔄 En curso (Fases 0, 1, 2 ✅; siguen 3+).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8) · Shopify CLI 3.94.3.

### Qué se ejecutó

**Setup**
- `git pull` (merge limpio de 7 commits de origin, sin conflictos → `474da1d`).
- `shopify theme pull --live` del tema publicado a `theme/` (423 archivos). Baseline commiteado (`619c772`).
- Token de `.envlocal` regenerado a `shpat_…` (app nueva, client_id `1b30f2bd…`) con `read_themes`/`write_themes`. Sigue con read/write de products+files (scripts Python intactos). Desapareció `HF_TOKEN` del `.envlocal`.
- Dev theme de trabajo **#189114876228** (`shopify theme dev`). El live es **#188231123268** — NUNCA se le hace push.

**Fase 0 — Cimientos de tokens** (`6e9247e`)
- `assets/santavila-tokens.css`: paleta exacta de `store.css :root` + reasigna las 4 familias base de Dwell → Hanken (body) / Cormorant (heading+subheading) / JetBrains Mono (accent). Se propaga a presets, botones, carrito y búsqueda.
- `layout/theme.liquid`: Google Fonts (preconnect + display=swap) y carga de los CSS de marca tras `color-schemes`.
- `config/settings_data.json`: 7 color schemes remapeados a la paleta de marca (paper, sage, sage-900, bone, arcilla).

**Fase 1 — Announcement + Header** (`1266528`, `f061556`)
- Announcement: 3 mensajes `·` en un bloque (scheme-5 sage-900, JetBrains Mono uppercase, 11.5px / 0.14em).
- Header: layout logo-izq / nav-centro / iconos-dcha, sticky always, papel translúcido + blur 16px en sólido, nav en Hanken con subrayado en hover. Conserva cart/search/drawer de Dwell.

**Fase 2 — Hero + header transparente** (`0188013`)
- `sections/santavila-hero.liquid`: sección bespoke OS 2.0 (100svh, eyebrow + H1 "El exterior, bien vivido." con em, sello rotatorio textPath, 2 CTAs pill, indicador "Descubre"). Degradado sage si no hay foto.
- Header transparente encendido en home (logo blanco/nav sobre hero → sólido papel al scroll).

### Entregables
- `theme/assets/santavila-tokens.css`, `theme/assets/santavila-header.css`, `theme/sections/santavila-hero.liquid`.
- `theme/layout/theme.liquid`, `theme/config/settings_data.json`, `theme/sections/header-group.json`, `theme/templates/index.json` (modificados).

### Hallazgos clave
- Colores → por **settings de Dwell** (color schemes); fuentes → por **CSS** (no garantizadas en la librería de Shopify). Sobrescribir 4 vars de fuente viste toda la fontanería.
- `theme dev` local (127.0.0.1) **no** funciona con token Admin API por la contraseña de escaparate → se usa **login OAuth del CLI** + `--store-password`. Preview por navegador (preview_theme_id / editor) funciona siempre con sesión admin.
- La conmutación de logo blanco↔verde y el header transparente son **nativos** de Dwell (settings), no requieren JS propio.

### Prioridades vivas
- Verificación visual fina del hero bajo el header transparente (posición/offset) en navegador.
- Nav del header: los 7 labels del README (Colecciones, Áticos y terrazas, Balcón…) son **contenido** del menú `main-menu` en Admin → Navegación; dependen de que existan las colecciones por escenario.

### Decisiones pendientes
- Reponer `HF_TOKEN` en `.envlocal` si se usan los scripts de imágenes.
- Crear colecciones por escenario + reescribir menú `main-menu`.

### Siguiente paso recomendado
- **Fase 3**: Manifesto + Escenarios (4 cards) + Colección destacada, siguiendo el orden del README (`design_handoff_shopify_theme/README.md`).

---

## 2026-05-18 · Costes Shopify + sync Hevea completo

**Paso del flujo:** Pricing — costes unitarios y datos de proveedor sincronizados.
**Estado:** ✅ Completado.
**Quién:** sesión interactiva con dueño · scripts `set_unit_costs.py` + `sync_hevea_full.py`.

### Qué se hizo

**1. Costes BRUNEI + Capri fijados en Shopify** (`set_unit_costs.py --apply`):
- 89 variantes actualizadas con coste real por variante (fin de los falsos CRÍTICO del auditor).
- BRUNEI: 80×80=257.19€ · 130×80=342.68€ · 160×90=412.95€ · 190×90=506.65€
- Capri cuadrada: 70×70=203.29€ · 80×80=218.28€
- Técnica: `productVariantsBulkUpdate` con `inventoryItem.cost` (scope `write_products`, no necesita `write_inventory`).

**2. Sync completo Hevea CSV → Excel + Shopify** (`sync_hevea_full.py --apply`):
- Fuente de verdad: `proveedores_raw/hevea/20260507 ▶️CSV hevea 07_05_25.csv` (110 SKUs únicos).
- **Excel** (hoja `20260508 -Todos `): 47 filas actualizadas — carrier_cost corregido (regla: <500€ IVA → 50€, ≥500€ → 0€).
- **Shopify**: 106 productos actualizados — price (PSY), compareAtPrice, unitCost, descriptionHtml (descripción + tabla dimensiones).
- 3 SKUs duplicados en CSV omitidos para revisión manual: `557-010147`, `557-010884`, `557-1563`.
- Bug corregido en compareAtPrice: solo se activa cuando `pvp_iva > psy` (precio rebajado real). Segunda pasada eliminó ~100 compareAtPrice que eran menores que el price.

**3. ACAPULCO-3 corregido manualmente** (SKU `557-010147`, handle `sofa-terraza-3-plazas-estilo-moderno-18570-cm`):
- El sofá había sido subido a 819€ durante la auditoría basándose en un coste incorrecto (523€).
- Datos correctos del CSV: exworks=599€, pvp=950 sin IVA → pvp_iva=1149.50€ → PSY=1150€.
- Shopify: **819€ → 1150€**, coste **523€ → 599€**, compareAtPrice eliminado.
- Excel fila 86: handle corregido a `sofa-terraza-3-plazas-estilo-moderno-18570-cm`.
- Excel fila 90 (ACAPULCO-8 set, mismo SKU): datos restaurados (coste=1440€, pvp=2764.85€, psy=2765€).

### Pendiente · SKUs duplicados en CSV

| SKU | Producto A | Producto B |
|---|---|---|
| `557-010147` | ACAPULCO-3 sofá 3P (exworks=599) | ACAPULCO-8 set 3P (exworks=1440) |
| `557-010884` | LUNA-44 (handle desconocido) | BRANDON-7 set (handle a verificar) |
| `557-1563` | Mesa centro 120cm (×2 versiones) | — |

Hevea debe asignar SKUs únicos a estos productos. Mientras tanto los handles en Shopify/Excel son correctos pero el CSV no se puede usar como fuente de verdad para ellos.

### Entregables

- `set_unit_costs.py` — setea unitCost para cualquier handle/psy del Excel
- `sync_hevea_full.py` — sync completo CSV→Excel→Shopify para Hevea; reutilizable

---

## 2026-05-18 · Auditoría financiera completa + corrección precio sofá

**Paso del flujo:** Pricing — revisión de márgenes post-shipping.
**Estado:** ✅ Auditoría ejecutada. ✅ Corrección aplicada. ⏳ Costes pendientes de completar en Shopify.
**Quién:** sesión interactiva con dueño · script `audit_financiero.py`.

### Qué se hizo

Auditoría de 1.596 variantes / 177 productos ACTIVOS: márgenes netos con coste real de producto + comisión Shopify Payments (2.1%+0.30€) + coste de envío real según categoría XS/M/L.

**Resultado:**
- **CRÍTICO real: 0** — los 16 flags CRÍTICO eran falsos positivos (coste estimado por promedio de handle en Excel vs coste real por variante).
- **AVISO real: 1** → sofá 789€ con margen 17.2% (coste verificado en Shopify: 523€).
- **SIN_COSTE: 202 variantes** (7 handles) sin coste en Shopify ni en Excel — no auditables hasta completar datos.

**Corrección ejecutada:**
- `sofa-terraza-3-plazas-estilo-moderno-18570-cm`: precio **789€ → 819€** (compareAtPrice 850€ mantenido). Margen neto resultante: ~20.1%.

### Falsos positivos detectados — causa raíz

| Handle | Variantes | Coste estimado (avg) | Coste real (Excel) | Margen real |
|---|---|---|---|---|
| BRUNEI 80×80 (ef580ae2) | 15 var · 478.95€ | 411€ | 257€ | ~40% ✅ |
| BRUNEI 130×80 (ef580ae2) | 15 var · 639€ | 411€ | 343€ | ~32% ✅ |
| Capri Ø70 (724b0db0) | 15 var · 349.95€ | 273€ | ~203€ | ~37% ✅ |
| Capri 70×70 (724b0db0) | 15 var · 378.95€ | 273€ | ~203€ | ~33% ✅ |
| Base parasol 25kg (3ee8b72d) | 1 var · 51.95€ | 54.88€ (cruzado) | ~27€ | ~36% ✅ |

El auditor usa la media de costes del handle Excel cuando Shopify no tiene el coste individual. Para eliminar estos falsos positivos: **meter costes reales por variante en Shopify Admin → Productos → Variante → Coste por artículo**.

### SIN_COSTE — pendiente

| Handle | Variantes | Rango precio |
|---|---|---|
| Tumbona resina (b19af1ea) | 80 | 228–242€ |
| Parasol acrílico (236bd5f0) | 24 | 399€ |
| Parasol (82e48b2d) | 64 | 384€ |
| Parasol cuadrado 200×200 | 9 | 399–426€ |
| Tumbona Carmen tablillas | 5 | 199–219€ |
| Tumbona Lola tablillas | 5 | 199–212€ |
| Mesa Capri Doble 120×80 | 15 | 535€ |

### Entregables

- `audit_financiero.py` — script reutilizable para futuras auditorías
- `audit_financiero.csv` — 1.596 filas con margen neto por variante

---

## 2026-05-18 · Categorías de envío aplicadas + metafield definition creada

**Paso del flujo:** Shipping — categorización volumétrica XS/M/L.
**Estado:** ✅ Metafield + tags aplicados. ⏳ Tarifas en Admin pendientes (manual).
**Quién:** sesión interactiva con dueño · script `apply_shipping_categories.py`.

### Qué se hizo

1. **Metafield definition creada via API**: `santavila.envio_categoria` (single_line_text_field, choices: xs/m/l). Id: `gid://shopify/MetafieldDefinition/319933219140`.

2. **`apply_shipping_categories.py --apply`** — Clasifica los 225 handles únicos del Excel en XS/M/L y aplica metafield + tag `envio:xs|m|l`:
   - **72 actualizados · 149 sin cambios · 4 no encontrados** (DRAFTs eliminados).
   - Distribución final: XS=6 · M=87 · L=132.

3. **Bug corregido** en `categorize()`: sets de sofás y rinconeras con "mesa de centro" en el nombre se clasificaban como M → añadida regla prioritaria para "sofa"/"rinconera" → L. 6 sets corregidos.

### Reglas de clasificación aplicadas

| Categoría | Criterio |
|---|---|
| XS | cojín, funda, limpiador |
| M | silla/sillón individual, taburete, reposapiés, mesa auxiliar/centro/baja/lateral, mesa ≤80cm, accesorio resina, parasol <250cm |
| L | sofá, rinconera, tumbona, mesa grande, conjunto, parasol ≥250cm, default |

### Estado final — Tarifas configuradas en Shopify Admin

Perfiles creados y tarifas verificadas:

| Perfil | Productos | Tarifa España |
|---|---|---|
| Envío XS - Accesorios | 10 | 9,95€ plano + gratis >500€ |
| Envío M - Mediano | 70 | 29,95€ plano + gratis >500€ |
| Envío L - Voluminoso | 105 | 57,95€ plano + gratis >500€ |
| Perfil general (fallback) | todos los demás | 57,95€ (€0–€499) + gratis ≥€500 |

"Gestionar envío dividido" activado.

3 productos ACTIVE no estaban en el Excel (fuera del alcance del script) → etiquetados manualmente y pendientes de mover a perfil L/M:
- `set-jardin-contemporaneo-sofa-2-plazas-2-sillones-mesa` → L
- `sofa-terraza-3-plazas-estilo-moderno-18570-cm` → L
- `mesa-de-centro-exterior-120-cm-altura-40-cm` → M

---

## 2026-05-18 · Precios psicológicos aplicados a TODO el catálogo activo

**Paso del flujo:** Pricing — redondeo psicológico.
**Estado:** ✅ Aplicado en producción.
**Quién:** sesión interactiva con dueño · scripts `fill_psy_column.py` + `sync_all_psy_prices.py`.

### Qué se hizo

1. **`fill_psy_column.py --apply`** — Rellena col G "Precio Venta Psicológico (con IVA 21%)" en la hoja `20260508 -Todos ` de `Santavila.xlsx`. 281 filas procesadas con las reglas segmentadas por price bruto.

2. **`sync_all_psy_prices.py --apply`** — Aplica precios psicológicos a todos los productos con `status:active` de Shopify:
   - **177 productos · 1.479 variantes actualizadas · 0 errores.**
   - Fuente `excel_col_G` para los 263 SKUs con correspondencia única en el Excel (productos originales Balliu).
   - Fuente `psy(shopify)` para los ~1.216 SKUs `SV-*` (consolidados) y Hevea sin correspondencia única.
   - Delta agregado en catálogo: **−0,60%** (normal — umbral-trick baja precios justo por encima de 150/200/300/450 €).

### Reglas de redondeo aplicadas

| Segmento (price bruto) | Precio | CompareAt |
|---|---|---|
| < 50 € | termina en .95 | × 1.30, entero |
| 50–500 € | termina en .95; si en [umbral, umbral×1.05] → umbral − 0.10 | × 1.10, misma lógica |
| > 500 € | entero con terminación 0/5/9 (ceil) | × 1.10, múltiplo más limpio en [psy×1.05, psy×1.12] |

### Decisiones tomadas

- **Solo productos `status:active`**: los DRAFTs y pendientes-proveedor se excluyen automáticamente.
- **SKUs duplicados en Excel** (mismo handle+sku en múltiples filas): excluidos del mapping → se aplica `psy(shopify)` sobre el precio actual de Shopify. Afecta a 8 SKUs (principalmente conjuntos Hevea y un caso EVA PRO con dato incorrecto en fila 130).
- **Reporte**: `psy_prices_report.csv` con columnas `fuente/price_antes/price_despues/compare_antes/compare_despues/status`.

---

## 2026-05-17 · Repaso final — precios, nombres y limpieza legacy

**Paso del flujo:** Cierre y QA tras consolidar Familias 1, 2, 3 y 5.
**Estado:** ✅ Aplicado en producción.
**Quién:** sesión interactiva con dueño · scripts ad-hoc.

### Repaso de precios — 0 discrepancias

Cruce automático Excel pestaña `20260508 -Todos ` col F (PVP IVA) ↔ Shopify para los **1.444 variantes con SKU `SV-*`** (productos consolidados). Resultado:

- ✅ **512 variantes-base** matchean exactamente con Excel (±0,05 €).
- ✅ **931 variantes derivadas** (Chasis × Color, Tamaño × Color, etc.) comparten precio con la variante base.
- ✅ **0 discrepancias**. Catalogación totalmente sincronizada con el Excel maestro.

### Productos legacy adicionales pasados a DRAFT

Detectados durante el repaso (productos ACTIVE Balliu sin consolidar todavía):

- **Pasarelas resina B2B** (2 productos): no encaja con el perfil residencial. Tags: `producto-b2b`, `pendiente-confirmar-proveedor`, `legacy-balliu-consolidado-2026-05`.
- **Eva Pro tumbonas legacy** (3 productos): duplicados de la consolidación Familia 2 (`ddeeef3f`, `b19af1ea con 73-cm`, `32a6c0ea con 73-cm`).
- **Parasoles legacy sin modelo** (3 productos): `parasol-para-terraza-300-cm`, `-300-cm-2`, `-350-cm`.
- **Tumbona legacy sin modelo** (1 producto): `tumbona-de-exterior`.

**Total**: 9 productos legacy pasados a DRAFT.

### Refactor de nombres — Familias 1 y 2

Aplicada regla **"Opción C + sufijo Modelo"** (introducida en sub-piloto 3d) retroactivamente a Familias 1 Parasoles y 2 Tumbonas. Script: [`refactor_nombres_balliu_familias_1_2.py`](../../refactor_nombres_balliu_familias_1_2.py).

**26 productos renombrados.** Ejemplos:

| Antes | Después |
|---|---|
| Parasol cuadrado · aluminio 300×300 cm | **Parasol cuadrado exterior · aluminio 300×300 cm · Brisa** |
| Parasol exterior · 16 colores Ø200 cm | **Parasol exterior tela · Ø200 cm · Pamela tela** |
| Parasol exterior acrílico · mástil regulable Ø200 cm | **Parasol exterior acrílico · Ø200 cm · Pamela acrílico** |
| Tumbona resina · respaldo regulable Ø73 cm tablillas (Mario Eskenazi) | **Tumbona exterior resina · Ø73 cm tablillas · Eva Pro T** |
| Tumbona resina premium · respaldo regulable | **Tumbona exterior resina · Noa** |
| Mini tumbona aluminio plegable · 62 cm | **Mini tumbona exterior aluminio plegable · 62 cm · Cannes** |

**Limpiezas aplicadas:**
- Quitado `(Mario Eskenazi)` del título Eva Pro T (queda para descripción).
- Quitado `premium` de Noa.
- Quitado `16 colores` (no es atributo de producto) — cambiado a `tela` cuando aplica.
- Añadido `exterior` consistentemente.
- Pamela y Ocean diferenciados con sufijo `tela`/`acrílico` ya que el mismo modelo se vende en dos materiales.

### Ágora — verificada y completada

`parasol-cuadrado-200x200` (Ágora, 9 variantes ACTIVE) **no tenía tag `Balliu`** y por eso no aparecía en mis listados anteriores. Corregido: tags `Balliu`, `envio:l` añadidos.

### Backup

`backups/refactor_nombres_<timestamp>.json` con snapshot previo de todos los productos renombrados.

### Siguientes pasos

- **Hevea**: auditoría completa (115 SKUs en pestaña `Hevea`).
- **Familia 7 estimada**: Camas balinesas, Sofás Olimpia/Etna, Fundas protectoras, Cojines, Weguard (productos ACTIVE legacy sin consolidar que el dueño decidirá si consolidar).
- **Imágenes por variante** (todas las familias).

---

## 2026-05-17 · Familia 5 cerrada — Sillas Balliu (10 consolidados / 168 variantes + 5 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 5 (Sillas)
**Estado:** ✅ Aplicado en producción · 10 consolidados publicados en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_sillas.py`

### Qué se ejecutó

Inspección Excel + Shopify + web Balliu de 21 SKUs sillas/taburetes/sillones repartidos en 11 modelos. WebFetch a 12 modelos para confirmar matriz.

### Decisiones del dueño aplicadas

1. **Patrón Blanco/Prestige** para Bimba, Duna (3 colores: Blanco/Negro/Tórtola).
2. **Selva** solo 2 colores (Blanco/Arena), sin la nota "para más colores consultar".
3. **Venus** sin opción Color (solo Tórtola en web → regla UX N=1).
4. **Vera** consolidado con opciones [Configuración(3) × Color(2)] = 6 variantes.
5. **Bruna** consolidado con [Brazos(2) × Color(2)] = 4 variantes.
6. **Silla/Etna Alta/Taburete Etna**: Chasis(3) × Tejido Balliu(16) = 48 variantes c/u, precio único.
7. **Mila** con Chasis(2) × Tejido(2) = 4 variantes.
8. **Taburete Etna**: precio Excel (186,62€), no web (188,63€).
9. **Silla Greta** y **Bruna 197,73€ misteriosa** → DRAFT con tag `pendiente-confirmar-proveedor`.

### Resultado (10 ACTIVE + 5 DRAFT)

| # | ACTIVE | Variantes | Precio (€) |
|---|---|---|---|
| 1 | Silla exterior resina · estilo clásico · **Bimba** | 3 (Color B/N/T) | 102,03 / 103,56 |
| 2 | Silla exterior resina · estilo minimalista · **Duna** | 3 (Color B/N/T) | 77,39 / 81,76 |
| 3 | Silla exterior resina apilable · **Selva** | 2 (Color B/A) | 33,50 / 40,52 |
| 4 | Silla exterior resina · **Bruna** | 4 (Brazos × Color) | 70,81 / 84,19 |
| 5 | Silla exterior resina · **Vera** | 6 (Configuración × Color) | 77,97 / 79,76 / 115,08 |
| 6 | Silla exterior resina · **Venus** | 2 (Brazos) | 65,42 / 70,71 |
| 7 | Silla exterior aluminio · tejido Balliu · **Etna** | **48** (Chasis × Tejido 16) | 181,89 |
| 8 | Silla exterior aluminio alta · tejido Balliu · **Etna Alta** | **48** | 190,20 |
| 9 | Taburete exterior aluminio · tejido Balliu · **Etna** | **48** | 186,62 |
| 10 | Silla exterior aluminio · tejido Balliu · **Mila** | 4 (Chasis 2 × Tejido 2) | 97,88 |

**Total ACTIVE: 10 productos · 168 variantes.**

**DRAFT (5):**
- 4 existentes: Venus con brazos (consolidado), Silla Greta (no en web), 2 duplicados Bruna misteriosos.
- 1 nuevo: `silla-exterior-resina-bruna-precio-alto-pendiente` (197,73€) — `pendiente-confirmar-proveedor`.

### Hallazgo Bruna misteriosa

El SKU `BALLIU_BRUNA_SILLA_CON_BRAZ_94B6E5B5` aparece dos veces en Excel con precios muy distintos (89,55€ y 197,73€) y dos productos planos en Shopify con el mismo SKU (113,80€ y 89,95€). La web del proveedor solo tiene Bruna sin/con brazos a 70,81€ / 84,19€. **No identificado** qué modelo es la variante 197,73€. Documentado en `PENDIENTES_PROVEEDOR.md`.

### Pendientes documentados

Archivo nuevo `docs/santavila/PENDIENTES_PROVEEDOR.md` (creado en esta sesión) acumula todo lo que hay que confirmar con Balliu:
- HPL Gran Densidad (10 modelos)
- Sofia, Ágata L, Olimpia Esquinera, Mesa Greta, Silla Greta, Atlanta 240×90, Werzalit Ø60, Capri Doble pie alto, Mesa alta Ø70
- Discrepancias precio: Olimpia aux tela, Altea 70×70 HPL, Taburete Etna
- SKU duplicado Bruna 197,73€

### Cómo se ejecutó

```bash
python3 consolidate_balliu_sillas.py            # dry-run
python3 consolidate_balliu_sillas.py --apply    # backup + apply + publish
```

Backup: `backups/sillas_<timestamp>.json`.

### Siguiente paso

- **Repaso final de precios y nombres** de todos los productos consolidados (47 + 10 = 57 productos · ~1.460 variantes).
- **Familia 6 · Pasarelas resina Balliu** (~2 modelos).
- **Hevea**: auditoría completa pendiente.

---

## 2026-05-17 · Sub-piloto 3a cerrado — Mesa comedor Balliu (9 consolidados / 240 variantes + 34 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3a (Mesa comedor — el más complejo y último)
**Estado:** ✅ Aplicado en producción · 9 consolidados publicados en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_comedor.py`

### Cierre de la Familia 3 (Mesas HPL)

Con 3a se completan las 4 fases del sub-piloto Familia 3. **Resumen Familia 3 completa**:

| Sub-piloto | Modelos | ACTIVE | Variantes | DRAFT |
|---|---|---|---|---|
| 3b · Mesa alta | Capri Alta | 1 | 2 | 5 |
| 3c · Mesa centro | Etna Central | 1 | 15 | 1 |
| 3d · Mesa auxiliar | Eva Pro Mini/BCN, Olimpia, Noa, Etna, Mini Prestige | 7 | 98 | 10 |
| 3a · Mesa comedor | Selva, Brunei, Atlanta, Java, Capri, Capri Doble, Altea, Ágata, Nora | 9 | 240 | 34 |
| **Total Familia 3** | | **18** | **355** | **50** |

### Decisiones del dueño en 3a (confirmadas con capturas web)

1. **HPL Gran Densidad** → siempre DRAFT separado (regla aplicada a Brunei, Java, Capri, Altea, Capri Doble extras, Ágata extras).
2. **Brunei**: 4 tamaños × 3 chasis × 5 colores HPL = 60 variantes ACTIVE. HPL_GD a DRAFT.
3. **Altea como la web**: solo 70×70 y 80×80, 2 chasis (Blanco/Tórtola), 5 HPL = 20 variantes. Resto (Ø80, 120×80, HPL_GD) a DRAFT. Precio 70×70 HPL = 421,43 € (precio mínimo del rango web).
4. **Capri Doble**: producto APARTE, no variante del Capri principal.
5. **Nora**: dimensión 72×72 cm (web), no Ø70 (Excel).
6. **Sofia, Ágata L, Atlanta 240×90**: NO están en web → todos DRAFT.

### Resultado 3a · 9 productos ACTIVE consolidados

| # | Consolidado ACTIVE | Variantes | Estructura | Precio base (€ IVA) |
|---|---|---|---|---|
| 1 | Mesa exterior resina · Werzalit · **Selva** | 6 | Tamaño 6 | 181,58 – 315,80 |
| 2 | Mesa exterior aluminio · HPL · **Brunei** | **60** | Tamaño 4 × Chasis 3 × HPL 5 | 478,77 – 943,15 según tamaño |
| 3 | Mesa extensible exterior aluminio · HPL · **Atlanta** | 30 | Tamaño 2 × Chasis 3 × HPL 5 | 1.274,08 / 1.669,81 |
| 4 | Mesa extensible exterior aluminio · HPL · **Java** | 30 | Tamaño 2 × Chasis 3 × HPL 5 | 1.573,34 / 2.016,97 |
| 5 | Mesa exterior aluminio · HPL · **Capri** | **75** | Tamaño 5 × Chasis 3 × HPL 5 | 349,19 – 406,34 según tamaño |
| 6 | Mesa exterior aluminio · HPL 120×80 cm · **Capri Doble** | 15 | Chasis 3 × HPL 5 | 531,53 |
| 7 | Mesa exterior aluminio · HPL · **Altea** | 20 | Tamaño 2 × Chasis 2 × HPL 5 | 421,43 / 422,17 |
| 8 | Mesa exterior aluminio · 75×75 cm · **Ágata** | 2 | Color 2 | 347,39 |
| 9 | Mesa exterior aluminio · 72×72 cm · **Nora** | 2 | Color 2 | 224,10 |

### DRAFT (34 productos)

**28 productos planos legacy pasados a DRAFT**:
- 5 Selva (legacy del consolidado)
- 3 Atlanta (240×90 HPL + HPL_GD + 200/260×100 secundario)
- 3 Java (140/180 HPL_GD + 200/260 secundario + HPL_GD)
- 5 Capri (Capri Ø90 + 4 DIAM HPL/HPL_GD)
- 5 Altea (80×80 HPL/HPL_GD, Ø80 HPL/HPL_GD, 120×80 HPL)
- 2 Ágata (120×80 HPL GD, 180×90 encimera = Ágata L)
- 5 Sofia (no en web actual del proveedor)

**6 productos DRAFT nuevos** con tag `pendiente-confirmar-proveedor`:
- Brunei HPL Gran Densidad (4 variantes tamaño)
- Java HPL Gran Densidad (2 variantes)
- Capri HPL Gran Densidad (5 variantes)
- Capri Doble · HPL GD / pie alto (3 variantes)
- Altea · variantes extras (5 variantes: HPL_GD, Ø80, 120×80)
- Ágata · variantes extras (2 variantes: 120×80 HPL_GD, 180×90 encimera)

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_comedor.py            # dry-run
python3 consolidate_balliu_mesas_comedor.py --apply    # backup 36 productos + apply + publish
```

Backup: `backups/mesas_comedor_20260517-105449.json` (36 productos).

### Siguientes pasos

1. **Repaso final de precios** de todos los productos consolidados (1+2+1+7+9 = 20 productos consolidados activos en total tras Familias 1, 2 y 3).
2. **Familia 5: Sillas Balliu** (Etna, Bruna, Selva, Vera, Mila…).
3. **Familia 6: Pasarelas resina Balliu**.
4. **Hevea**: auditoría completa pendiente.
5. **Imágenes por variante** (todas las familias).
6. **Confirmar con proveedor Balliu**: HPL Gran Densidad, Sofia, Olimpia Esquinera, Mesa Greta, Ágata L, Atlanta 240×90 — todos en DRAFT con tag `pendiente-confirmar-proveedor`.

---

## 2026-05-17 · Sub-piloto 3d cerrado — Mesa auxiliar Balliu (7 consolidados / 98 variantes + 10 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3d (Mesa auxiliar)
**Estado:** ✅ Aplicado en producción · 7 consolidados publicados en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_auxiliares.py`

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu de 14 productos planos + 1 ya consolidado (Etna aux) en la categoría "mesa auxiliar".

### Decisiones del dueño aplicadas

1. **Patrón Blanco/Prestige** en Eva Pro Mini, Eva Pro BCN, Noa aux y Mini Prestige: Blanco más barato; el resto de colores comparten precio Prestige.
2. **Olimpia aux tela**: precio Excel (157,63 €) — discrepa de la web (149,34 €) pero el Excel es la fuente de verdad.
3. **Naming refinado** (regla nueva, memorizada): Opción C + sufijo " · <Modelo>" para identificar entre productos similares. Ejemplo: "Mesa auxiliar exterior resina · 48×48 cm · Eva Pro Mini".
4. **HPL Gran Densidad** y **Werzalit**: no figuran en web → productos DRAFT separados (pendiente confirmar con proveedor).
5. **Olimpia Esquinera** y **Mesa Greta**: no figuran en web → DRAFT (pendiente confirmar).

### Resultado (29 productos en total: 7 ACTIVE consolidados + 10 DRAFT)

| # | Consolidado ACTIVE | Variantes | Precio (€ IVA) |
|---|---|---|---|
| 1 | Mesa auxiliar exterior resina · 48×48 cm · **Eva Pro Mini** | 5 (Color) | 33,43 / 34,41 (Prestige) |
| 2 | Mesa auxiliar exterior resina · 48×48 cm · **Eva Pro BCN** | 5 (Color) | 35,99 / 37,79 |
| 3 | Mesa auxiliar exterior aluminio · 48×48 cm tejido · **Olimpia** | **48** (Chasis 3 × Color tejido 16) | 157,63 |
| 4 | Mesa de centro exterior · aluminio HPL 74×54 cm · **Olimpia Central** | 15 (Chasis 3 × Color tablero 5) | 227,18 |
| 5 | Mesa auxiliar exterior aluminio · Ø42 cm · **Noa** | 5 (Color) | 130,24 / 136,98 |
| 6 | Mesa auxiliar exterior · aluminio HPL 45×45 cm · **Etna** | 15 (Chasis 3 × Color tablero 5) | 167,00 |
| 7 | Mesa auxiliar exterior resina decorativa · 48×48 cm · **Mini Prestige** | 5 (Color) | 27,66 / 29,17 |

**DRAFT existentes pasados (8)**: duplicados Prestige de Eva Pro Mini/BCN/Noa/MiniMesa, Olimpia Central HPL_GD, Olimpia Esquinera HPL/HPL_GD, Mesa Greta. Todos con tag `legacy-balliu-consolidado-2026-05`.

**DRAFT nuevos creados (2)**:
- `mesa-auxiliar-exterior-aluminio-hpl-gd-45x45-etna` → Etna HPL Gran Densidad (175,06 €).
- `mesa-auxiliar-exterior-aluminio-werzalit-60-etna` → Etna Werzalit Ø60 (157,84 €).
Tags: `pendiente-confirmar-proveedor`, `legacy-balliu-consolidado-2026-05`.

### Hallazgo Etna aux

El producto plano Shopify mostraba dimensiones "60 cm" pero la web actual del proveedor dice **45×45×39 cm**. El SKU Werzalit Ø60 sí es de 60 cm — probablemente discontinuado pero a confirmar. El consolidado ACTIVE se queda con la dimensión actual del proveedor (45×45 cm).

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_auxiliares.py            # dry-run
python3 consolidate_balliu_mesas_auxiliares.py --apply    # backup + apply + publish
```

Backup: `backups/mesas_auxiliares_20260517-090517.json` (15 productos).

### Siguiente paso

- **Sub-piloto 3a · Mesa comedor** (Selva, Brunei, Atlanta, Java, Sofia, Capri, Altea, Ágata, Nora — ~25 productos planos, el más complejo).

---

## 2026-05-17 · Sub-piloto 3c cerrado — Mesa de centro exterior HPL (1 consolidado / 15 variantes + 1 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3c (Mesa centro)
**Estado:** ✅ Aplicado en producción · consolidado publicado en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_centro.py`

### Origen y estado previo

- **Proveedor:** Etna Mesa Central (110×60×44,5 cm, aluminio mate).
- **Shopify previo:** 1 producto ya consolidado `balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e` ACTIVE con 2 variantes "Tablero Hpl" / "Tablero Hpl Gd" (349,90 € / 421,95 €). SKUs BALLIU_ETNA_MESA_CENTRAL_*.

### Decisiones del dueño aplicadas

1. **HPL Gran Densidad no aparece en web actual del proveedor** → producto DRAFT separado nuevo, pendiente confirmación con proveedor.
2. **Chasis (3 colores: Blanco / Tórtola / Aluminio)** → opción visible al cliente.
3. **Color tablero HPL (5: Gris / Blanco / Moonwalk / Skyline / Prado)** → opción visible.
4. **Naming Opción C**: `Mesa de centro exterior · aluminio HPL 110×60 cm`.

### Regla UX descubierta (memorizada)

> Si una característica tiene un único valor, no se añade como opción seleccionable — ir a descripción del producto. Caso 3b mesa alta (chasis único = descripción) vs 3c mesa centro (3 chasis = opción).

### Resultado

| | Antes | Después |
|---|---|---|
| Productos ACTIVE | 1 con 2 variantes Hpl/Hpl Gd | **1 consolidado** con **15 variantes** (Chasis × Color tablero) |
| Productos DRAFT | 0 | **1 nuevo** (HPL Gran Densidad), 1 variante a 421,95 € |
| Opciones | 1 (Tablero) | 2 (Chasis × Color tablero) |
| Naming | "Mesa de centro exterior aluminio \| 60 cm" | "Mesa de centro exterior · aluminio HPL 110×60 cm" |
| Tags duplicados | `match-verde` | Limpiados |
| SKU pattern | BALLIU_ETNA_MESA_CENTRAL_* | `SV-MESACENTRO-<chasis>-<color>` |
| Precio HPL | 349,90 € (desactualizado) | **362,44 €** (Excel × 1.21) en las 15 variantes |
| Precio HPL GD | 421,95 € | **421,95 €** (en DRAFT) |

### Productos resultantes

- **ACTIVE** `balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e`
  - 15 variantes Chasis(3) × Color tablero(5), todas a 362,44 €.
- **DRAFT** `mesa-de-centro-exterior-aluminio-hpl-gd-110x60` (handle nuevo)
  - 1 variante "HPL Gran Densidad" a 421,95 €.
  - Tags: `pendiente-confirmar-proveedor`, `legacy-balliu-consolidado-2026-05`.

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_centro.py            # dry-run
python3 consolidate_balliu_mesas_centro.py --apply    # backup + apply + publish
```

Backup: `backups/mesas_centro_20260517-084523.json`.

### Siguiente paso

- **Sub-piloto 3d · Mesa auxiliar** (Eva Pro Mini/BCN, Olimpia, Noa aux, Etna aux, Greta — ~14 productos planos).

---

## 2026-05-17 · Sub-piloto 3b cerrado — Mesa alta exterior HPL (1 producto / 2 variantes + 5 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3b (Mesa alta)
**Estado:** ✅ Aplicado en producción · consolidado publicado en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_altas.py`

### Decisión de partida: trocear la Familia 3 en sub-pilotos

Familia 3 (Mesas HPL) tiene ~50 productos planos en Shopify. Se decide trocear en 4 sub-pilotos por complejidad creciente y reducir el blast radius:

- **3b · Mesa alta** ← este sub-piloto
- **3c · Mesa centro**
- **3d · Mesa auxiliar**
- **3a · Mesa comedor** (el más complejo, último)

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu (Capri Alta). 6 productos planos en Shopify, todos ACTIVE con 1 variante "Default Title". Web del proveedor confirma que solo siguen vigentes 2 tamaños (60×60, 70×70) en HPL standard.

### Decisiones del dueño aplicadas

1. **Ø70 cm (mesa redonda)**: no figura en web actual del proveedor → **DRAFT**, no se elimina.
2. **HPL Gran Densidad**: no figura en web actual del proveedor → **DRAFT** las 4 SKUs HPL_GD.
3. **Precios desde Excel pestaña `20260508 -Todos `** (la única con IVA bien calculado en columna F y sin IVA en columna I). Se descarta usar otras pestañas (`Balliu`, `Todos`) — tienen columnas F = I (no separadas), no fiables.
4. **Chasis Aluminio**: como descripción de producto, **no como opción** visible.
5. **Naming Opción C**: sin nombre del modelo proveedor (Capri Alta) visible al cliente.

### Resultado

| | Antes (Shopify plano) | Después (consolidado) |
|---|---|---|
| Productos ACTIVE | 6 (con 1 variante c/u) | **1** consolidado con 2 variantes |
| Productos DRAFT | 0 | **5** (Ø70 HPL, Ø70 HPL GD, 60×60 HPL GD, 70×70 HPL GD, duplicado 60×60) |
| Naming | `Mesa alta exterior HPL` × 6 | `Mesa alta exterior · aluminio HPL 110 cm` |
| Tags duplicados | `match-rojo`, `envio:l` | Limpiados; legacy con `legacy-balliu-consolidado-2026-05` |
| Precio 60×60 HPL | €449,90 / €502,93 (caos) | **€456,69** (Excel × 1.21) |
| Precio 70×70 HPL | €529,00 (desactualizado) | **€528,46** (Excel × 1.21) |
| Winner Shopify | — | `balliu-mesa-alta-exterior-hpl-94512eab` |

Variantes ACTIVE finales:
- 60×60 cm — SKU `SV-MESAALTA-60-HPL` — €456,69
- 70×70 cm — SKU `SV-MESAALTA-70-HPL` — €528,46

### Hallazgo importante sobre pestañas del Excel

Solo **`20260508 -Todos `** (con espacio al final) tiene precios correctos:
- Columna F = "Precio Venta (con IVA 21%)" — IVA incluido ✓
- Columna I = "PVP Recomendado" — sin IVA; F = I × 1.21 ✓

Las pestañas `Balliu` y `Todos` tienen F = I (no separadas) → **no usar para precios**. Se memoriza.

### Anomalía detectada en Excel

Filas 222 y 223 del Excel comparten el mismo SKU `BALLIU_60X60_MESA_ALTA_TABLERO_HPL_GD_A3352658` pero con costes distintos (245,33€ vs 263,01€). Por diferencial de precio (HPL → HPL GD ≈ +7-12% en otros tamaños) se deduce que la fila 222 es **HPL standard mal etiquetado como GD**. Se trata como HPL standard para la variante 60×60 activa.

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_altas.py            # dry-run
python3 consolidate_balliu_mesas_altas.py --apply    # backup + apply + publish
```

Backup: `backups/mesas_altas_20260517-082726.json` (6 productos).

### Pendientes que arrastra al repaso final

- Confirmar con proveedor si Ø70 y HPL GD son legacy definitivos o pueden volver a venta.
- Decidir si el handle del winner se renombra a algo más limpio (`mesa-alta-exterior-aluminio-hpl`) en el repaso final con redirect 301.

### Siguiente paso

- **Sub-piloto 3c · Mesa centro** (Etna central, Olimpia central — ~2 modelos).

---

## 2026-05-17 · Familia 2 cerrada — Tumbonas Balliu (19 productos / 787 variantes)

**Paso del flujo:** Sprint adicional — calidad de catálogo (continuación del plan de consolidación)
**Estado:** ✅ Aplicado en producción · todos los productos publicados
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_tumbonas.py`

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu de la familia "tumbona". 20 productos planos → **19 productos con variantes ricas** + 1 a DRAFT (Alba).

**Documentos:**
- [`Agents-IA/consolidacion-catalogo.md`](../../Agents-IA/consolidacion-catalogo.md) — actualizado con la Familia 2 completada.
- [`consolidate_balliu_tumbonas.py`](../../consolidate_balliu_tumbonas.py) — nuevo script siguiendo el patrón de parasoles.
- `backups/tumbonas_<timestamp>.json` — snapshots previos (gitignored).

### Decisiones del dueño aplicadas

1. **Chasis con valores reales** (Opción A): cada modelo define sus 1-5 colores reales del proveedor.
2. **Precio Blanco vs "Prestige"** (= cualquier color no-Blanco, más caro).
3. **16 colores tejido como option visible** al cliente.
4. **Tablillas → producto separado** (Carmen T, Lola T, Eva Pro T) en lugar de variante. Carmen T y Lola T se crearon desde cero.
5. **Alba a DRAFT** (no existe en la web Balliu — pendiente verificar).
6. **Naming Opción C**: sin marca proveedor visible.

### Resultado

| Producto | Variantes |
|---|---|
| Eva Pro (tela / tablillas) | 80 + 5 |
| Eva RG / Eva RTG | 32 + 1 |
| Carmen (tela / tablillas) | 80 + 5 |
| Lola (tela / tablillas) | 80 + 5 |
| Noa | 80 |
| Olimpia / Etna / Etna Alta (con ruedas Sí/No) | 96 × 3 = 288 |
| Iris / Marina | 16 + 16 |
| Mini Cannes / Bristol / Marina | 48 + 16 + 32 |
| Colchoneta (3 tejidos) | 3 |
| Alba | DRAFT |
| **Total** | **787 variantes en 19 productos** |

Todos los productos vivos publicados a Online Store + Shop.

### Bugs resueltos

- **Productos con options legacy** (`Color chasis`, `Configuración`): 7 productos tenían options con nombres viejos. `productOptionsCreate` falla en silencio y luego `productVariantsBulkCreate` da `NEED_TO_ADD_OPTION_VALUES`. **Fix**: borrar variantes con `productVariantsBulkDelete`, luego borrar options con `productOptionsDelete strategy:POSITION`, luego re-aplicar consolidación normal.
- **SSL EOF intermitente**: añadidos retries con backoff exponencial.
- **`strategy: DEFAULT` no borra options con múltiples valores** — usar `strategy: POSITION` después de borrar variantes.

### Pendientes

- ⏳ Verificar Alba con el proveedor (descatalogado o nombre antiguo).
- ⏳ Imágenes por variante (todas las familias) — diferido.
- ⏳ Olimpia/Etna/Etna Alta con 96 variantes están al filo del límite Shopify (100/producto).

### Siguiente paso recomendado

**Familia 3 — Mesas HPL Balliu** (~6 productos planos → 2-3 modelos: SOFIA, ATLANTA, JAVA, DIAM, ALTEA). Patrón idéntico al usado en tumbonas.

---

## 2026-05-16 (tarde) · Cierre Familia 1 con Ágora + rename del documento maestro

**Paso del flujo:** completar Familia 1 (Parasoles) + reorganizar la documentación de consolidación
**Estado:** ✅ Familia 1 cerrada · 153 variantes totales

### Qué se ejecutó

#### Ágora creado desde cero
- Implementada la rama `create_new=True` en `consolidate_balliu_parasoles.py` (mutación `productCreate`).
- Bug menor resuelto en el camino: campo `code` no existe en `UserError` para `productCreate` (sí en otros tipos).
- Producto nuevo creado: `parasol-cuadrado-200x200` con 9 variantes y publicado al Online Store + Shop.
- Precios por serie de color del Excel: 6 colores serie 96 a 426,22 € + 3 colores serie 00 a 404,20 €.
- Colisión de "Blanco" resuelta con nombres diferenciados: **"Blanco acrílico"** (96/07) y **"Blanco tela"** (07/00).

#### Documento maestro renombrado
- `Agents-IA/auditoria-balliu-parasoles.md` → `Agents-IA/consolidacion-catalogo.md` (con `git mv`, historial preservado).
- Contenido reestructurado como **índice maestro** del catálogo: una sección por familia, plantilla para escalar.
- Referencias actualizadas en `JOURNAL.md` y `consolidate_balliu_parasoles.py` (docstring).
- `INDEX.md` actualizado.

### Estado final Familia 1

10 productos · **153 variantes** (24 + 64 + 24 + 19 + **9 Ágora** + 3 + 3 + 3 + 2 + 2).

### Siguiente paso recomendado

- **Familia 2: Tumbonas Balliu** — 16 productos planos → ~5 modelos. WebFetch a cada modelo (EVA PRO, CARMEN, LOLA, NOA, OLIMPIA, IRIS, ETNA, MARINA, ALBA).
- O **imágenes por variante** de Familia 1 — el dueño dijo "luego revisamos colores".

El usuario priorizó **continuar con la consolidación** antes de los colores, así que la próxima sesión empezará con tumbonas.

---

## 2026-05-16 · Consolidación piloto Balliu — familia parasoles (9 productos / 144 variantes)

**Paso del flujo:** Sprint adicional — calidad de catálogo (Nivel 2 de la auditoría de duplicados)
**Estado:** ✅ Aplicado en producción · piloto exitoso del patrón de consolidación
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_parasoles.py`

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu de la familia "parasol" y consolidación: **15 productos planos → 9 productos con variantes ricas**.

**Documentos generados:**
- [`Agents-IA/consolidacion-catalogo.md`](../../Agents-IA/consolidacion-catalogo.md) — mapeo Excel↔Modelo + 6 decisiones cerradas del dueño.
- [`consolidate_balliu_parasoles.py`](../../consolidate_balliu_parasoles.py) — script de consolidación (dry-run por defecto, `--only`, `--skip-delete`, `--skip-publish`).
- `backups/parasoles_<timestamp>.json` — snapshot completo previo a tocar nada.

### Decisiones del dueño aplicadas

1. **Naming Opción C** — sin nombre del proveedor visible, por característica técnica:
   - `Parasol cuadrado · aluminio 300×300 cm` (Brisa)
   - `Parasol exterior acrílico · mástil regulable Ø200 cm` (Pamela acrílico)
   - `Parasol redondo · aluminio Ø300 cm` (Garbí)
   - `Parasol lateral · aluminio 300×300 cm` (Roma)
   - etc.
2. **SKU derivado por variante** (`SV-BRISA-CAQUI`, `SV-PAMELA-ACR-ANTRACITA-CON-F`...) en lugar del SKU autogenerado del Excel, que NO es del proveedor.
3. **Metafields del producto**:
   - `santavila.proveedor_modelo` (Brisa / Pamela / Ocean / Garbí / Roma / Pie / Base)
   - `santavila.proveedor_grupo` (G1)
   - `santavila.proveedor_sku_original` (preservado para auditoría)
   - `santavila.espacio_principal` (lista)
4. **Metafield de variante** `santavila.color_codigo_proveedor` (96/42, 07/00, etc.) — permite reconstruir el código exacto al pasar pedido a Balliu.
5. **Colores con nombres simples** ("Blanco" en vez de "Blanco (tela Balliu)") — la serie del color queda en el metafield del producto. Excepción: Ágora (cuando se cree en v2) usará "Blanco acrílico" / "Blanco tela" por colisión.
6. **Bases de hormigón con precios invertidos** según decisión: 25 kg = 51,23 € · 30 kg = 102,16 € (antes estaban al revés).

### Resultado en producción

| Producto Shopify | Variantes | Precio | Canales |
|---|---|---|---|
| Parasol cuadrado · aluminio 300×300 cm (Brisa) | 3 | 1.045,32 € | Online Store + Shop |
| Parasol exterior acrílico · mástil regulable Ø200 cm (Pamela acr.) | 24 | 413,19 € | OS+Shop |
| Parasol exterior · mástil regulable 16 colores Ø200 cm (Pamela tela) | 64 | 384,37 € | OS+Shop |
| Parasol exterior acrílico · Ø200 / Ø250 cm (Ocean acr.) | 24 | 398,10 / 414,67 € | OS+Shop |
| Parasol exterior · 16 colores Ø200 / Ø250 cm (Ocean tela) | 19 | 304,13 / 381,54 € | OS+Shop |
| Parasol redondo · aluminio Ø300 cm (Garbí) | 3 | 1.045,32 € | OS+Shop |
| Parasol lateral · aluminio 300×300 cm (Roma) | 3 | 1.897,36 € | OS+Shop |
| Pie de parasol · 40 kg | 2 | 164,14 / 126,88 € | OS+Shop |
| Base de hormigón para parasol | 2 | 51,23 / 102,16 € | OS+Shop |
| **Total** | **144** | | |

**Productos eliminados (6):**
- 4 duplicados puros (Pamela acrílico `-2/-3`, Pamela tela `-2/-3`).
- 2 absorbidos como variante (pie RE, base 30 kg).

**Pendiente v2 (Ágora):** producto que existe en el Excel pero no en Shopify. Requiere `productCreate` desde cero. Documentado en el script como `create_new=True`.

### Bugs resueltos en el camino

- **`gql()` doblando `data["data"]`** en mi función helper. Corregido con `sed s|r\["data"\]\["|r\["|`.
- **Query `tag:envio:xs` devolvía 0** (no por bug previo): aplicado a productos via API.
- **Option value rename**: el piloto de Brisa quedó con "Blanco (tela Balliu)". Fix vía `productOptionUpdate` con `optionValuesToUpdate`.
- **`COLOR_CODES` global ambiguo** (Arena y Azul existen en serie 96 y serie 00): refactorizado a `color_code(color, serie)` con la serie definida por producto.

### Lo que NO se ha hecho (queda para próximas sesiones)

- **Ágora** — crear desde cero (9 variantes con precio por serie de color).
- **Imágenes por variante** — actualmente cada producto mantiene su galería original. Próxima iteración: extraer del JSON scrapeado y mapear color → imagen.
- **Consolidar otras familias Balliu** — tumbonas (16 productos → ~5 modelos), mesas HPL (varios), mesas auxiliares, sillas Etna/Bruna/Selva. Patrón ya validado.
- **Limpiar tags antiguos visibles** (`Balliu`, `match-verde`): tarea F0-02/F0-03 del backlog, no parte de la consolidación.
- **Confirmar peso real de las bases de hormigón con el proveedor** antes del primer pedido (etiquetas físicamente podrían estar invertidas también).

### Patrón validado para escalar

El piloto demuestra que el flujo siguiente funciona end-to-end y se puede aplicar a las otras familias del catálogo:

```
1. WebFetch a la web del proveedor para extraer matriz de variantes real.
2. Cruzar SKUs Excel ↔ modelo proveedor por precio + descripción.
3. Decisiones del dueño sobre naming, ambigüedades y precios.
4. Script declarativo con productos como `dict` (PRODUCTS).
5. Dry-run → apply piloto (--only) → apply resto → delete + publish.
6. Backup previo, reporte CSV, metafields para preservar info original.
```

### Siguiente paso recomendado

Aplicar el mismo patrón a la próxima familia con duplicación (tumbonas Balliu, 16 productos planos). O bien resolver Ágora (rápido, ~30 min) antes de pasar a la siguiente familia.

---

## 2026-05-14 · Auditoría de duplicados + 120 productos invisibles + activación parcial

**Paso del flujo:** validación previa al test de checkout
**Estado:** ⚠️ Hallazgos críticos documentados, decisiones diferidas

### Qué se ejecutó

Mientras se preparaba el test de los 5 escenarios de envío, salieron dos hallazgos importantes que no estaban en la auditoría original (faltaba scope `read_publications`):

#### 1. 120 de 235 productos ACTIVE están publicados a 0 canales (invisibles en la web)

Distribución: **115 productos visibles** (≈ todos los Hevea) y **120 invisibles** (≈ todo el catálogo Balliu). Cuando se importó Balliu se quedaron sin publicar al canal Online Store. La auditoría inicial no lo detectó porque el scope `read_publications` no estaba en el token viejo.

**Acción tomada:** se han publicado **8 productos** al canal Online Store + Shop para desbloquear el test inmediato:
- 4 fundas protectoras (necesarias para el Escenario 1 XS)
- 2 parasoles acrílicos (sacados de DRAFT a ACTIVE hoy)
- 1 cojín exterior (sacado de DRAFT, sin imagen — para test)
- 1 limpiador para mobiliario (sacado de DRAFT — para test)

**Pendiente:** decidir si publicar los **~106 productos Balliu restantes invisibles**. La tienda está bajo password page → publicar no expone nada al público. Es bug operativo histórico, no decisión deliberada.

#### 2. Duplicados en el catálogo (especialmente parasoles)

Detonante: el dueño vio "el parasol 4 veces" en la búsqueda del Admin. Auditoría completa con tres niveles:

- **Nivel 1 — Duplicados puros (~9 productos eliminables)**: mismo SKU + handle con sufijo `-2/-3` (parasol `236bd5f0`×3, parasol `82e48b2d`×3, mesa alta HPL `a3352658`×2, silla Bruna `94b6e5b5`×2, etc.).
- **Nivel 2 — Variantes mal modeladas (~70-80 productos en 7-8 familias)**: productos físicamente distintos del proveedor con título genérico repetido (Tumbona resina × 16, Mesa alta HPL × 6, etc.). NO son duplicados — se deben consolidar como variantes en Sprint posterior.
- **Nivel 3 — SKUs reusados a propósito por Hevea** (`557-010147`, `557-010884`): documentado ya en PROYECTO.md, no se tocan.

**Acción tomada:** documentación completa en [`Agents-IA/auditoria-productos.md`](../../Agents-IA/auditoria-productos.md). Diferido por decisión del dueño — no se aborda en este sprint.

### Activación temporal de DRAFTs para test

Se activaron 4 productos que estaban en DRAFT, **con `inventoryItem.tracked = false`** (stock infinito virtual) para testing. Snapshot del estado previo en `drafts_activation_state.json`. Para revertir cuando termine el test, reaplicar:

```
status: DRAFT (los 4)
inventoryItem.tracked: true (los 4)
```

### Decisiones pendientes que quedan abiertas

1. **¿Publicar los ~106 productos Balliu invisibles ahora?** Recomendado SÍ (bug operativo, tienda bajo password page). Trivial técnicamente.
2. **¿Eliminar los ~9 duplicados puros (Nivel 1) antes del test de checkout?** Recomendado SÍ, pero el dueño lo difiere.
3. **¿Cuándo abordar consolidación de variantes (Nivel 2)?** Recomendado antes del Sprint 4 (rediseño home) — sin consolidar la home muestra catálogo redundante.

### Cosas que actualizar en docs cuando se aborden las tareas

- `PROYECTO.md §3 Balliu`: añadir nota sobre el bug "no publicados al Online Store al importar" como aprendizaje operativo.
- `BACKLOG_SANTAVILA.md`: añadir tarea **F0-08b — Publicar los productos Balliu invisibles al Online Store** + **F0-08c — Eliminar duplicados puros del Nivel 1** + ampliar F0-04 con referencia a `auditoria-productos.md`.
- `AUDITORIA_SANTAVILA.md`: actualizar §1.5 "Apps instaladas / Channels" para reflejar que `resourcePublicationsCount` ahora sí se audita (scope `read_publications` disponible).

### Siguiente paso recomendado

El test de los 5 escenarios de envío puede continuar tal como estaba previsto. Los productos necesarios están publicados. Los hallazgos no bloquean.

Después del test, decisión por parte del dueño sobre las 3 tareas pendientes arriba.

### Validación del sistema de envío ✅ (final del día)

Tests de los 5 escenarios de envío ejecutados por el dueño vía Draft Orders en Admin. **Resultado: todos OK.** Los 3 shipping profiles (XS / M / L) aplican correctamente, el umbral de envío gratuito > 500€ funciona como esperado, y las 271 variantes asignadas vía API responden con su tarifa correspondiente en checkout preview.

**Estado final del sistema de envío al cierre del día:**
- 3 shipping profiles vivos en producción.
- 271 variantes asignadas correctamente por categoría volumétrica.
- 110 productos Balliu siguen invisibles (0 canales) — diferido.
- ~9 duplicados puros del Nivel 1 siguen en catálogo — diferido.
- 4 productos previamente DRAFT siguen ACTIVE con `inventoryItem.tracked=false` (snapshot en `drafts_activation_state.json` para revertir cuando se decida).

### Estado de tareas para la próxima sesión

| Tarea | Estado | Documento |
|---|---|---|
| Publicar los ~106 Balliu invisibles | Pendiente decisión | Este journal |
| Eliminar duplicados puros Nivel 1 | Pendiente decisión | `Agents-IA/auditoria-productos.md` |
| Consolidar variantes Nivel 2 | Diferido a Sprint posterior | `Agents-IA/auditoria-productos.md` |
| Decidir status final de los 4 DRAFTs activados (mantener o revertir) | Pendiente | Snapshot en `drafts_activation_state.json` |
| F0-09 `shopify theme pull` (ya tenemos `read_themes`) | Pendiente | `docs/santavila/BACKLOG_SANTAVILA.md` |
| F1-01 — 31 metafield definitions restantes | Pendiente | `docs/santavila/DATA_MODEL_SANTAVILA.md` |

---

## 2026-05-14 · Setup completo de Shipping Profiles + nueva app OAuth con scopes amplios

**Paso del flujo:** ejecución de la política de envío + ampliación de capacidad técnica
**Estado:** ✅ Aplicado en producción
**Quién:** sesión interactiva, app `Santavila Admin` creada desde cero en Partner Dashboard.

### Qué se ejecutó

**A. Creación de app nueva con scopes amplios.** Tras perder acceso al Partner Dashboard de la cuenta dueña de `API-Products`, se ha creado app nueva `Santavila Admin` (Client ID `1b30f2bd…36126`) con 18 scopes que cubren Sprint 1-2 completo:

```
read_products, write_products, read_files, write_files,
read_content, write_content, read_shipping, write_shipping,
read_themes, write_themes, read_locales,
read_translations, write_translations,
read_orders, write_orders, read_inventory, write_inventory,
read_publications, write_publications
```

Token capturado vía OAuth flow (`get_shopify_token.mjs` adaptado para leer credentials desde `.env`/`.env.local`). Token formato `shpat_…` (38 chars) guardado en `.env.local` como `SHOPIFY_ACCESS_TOKEN`. El token viejo (`shpca_…`) sigue en `.env` como fallback pero ya no se usa (mi script Python lee primero `.env.local`).

**B. Shipping Profiles creados manualmente en Admin.** 3 custom profiles, cada uno con 1 shipping option flat + checkbox "Offer free shipping" min 500€:

| Profile | Tarifa | Min gratis |
|---|---|---|
| `Envío XS - Accesorios` | 9,95€ | 500€ |
| `Envio M - Mediano` | 29,95€ | 500€ |
| `Envio L - Voluminoso` | 57,95€ | 500€ |

Zone: `Pen+Baleares · Spain (48 of 52 provinces)`. Canarias, Ceuta y Melilla excluidas (decisión de política).

**C. Asignación masiva de productos vía API.** Script nuevo [`assign_products_to_shipping_profiles.py`](../../assign_products_to_shipping_profiles.py): lee tags `envio:xs|m|l` aplicados ayer, obtiene variant IDs y los asocia al profile correspondiente vía `deliveryProfileUpdate`. Resultado:

| Profile | Variantes asignadas |
|---|---|
| Envío XS - Accesorios | 10 |
| Envio M - Mediano | 116 |
| Envio L - Voluminoso | 145 |
| **Total** | **271 variantes** · 0 errores |

### Bugs resueltos en el camino

- **Query Shopify por tag con `:`**: la sintaxis `tag:envio:xs` devolvía 0 resultados porque el parser corta en el primer `:`. Corregido a `tag:'envio:xs'` (comillas simples obligatorias). Documentado en el script.
- **CLIENT_SECRET literal del placeholder**: por darle un comando con `"el-secreto-que-has-copiado"` como ejemplo, el dueño lo pegó literal en `.env.local`. Reemplazado por el real (`shpss_…`, 38 chars).
- **App automation token ≠ Admin API token**: el botón "Create token" de Partner Dashboard genera un token de prefix `atkn_` para CI/CD de la app, NO sirve para Admin API. Hay que pasar por OAuth flow → token `shpat_…`. Anotado para no repetir.
- **Nombre de variable**: el token nuevo se pegó suelto en `.env.local` sin la clave `SHOPIFY_ACCESS_TOKEN=` delante. Renombrado y arreglado.
- **Error handling de `get_shopify_token.mjs`**: antes crasheaba con `JSON.parse` cuando Shopify devolvía HTML de error. Reescrito para leer el body como texto, detectar content-type no-JSON y reportar un mensaje claro con la primera parte de la respuesta.
- **Lectura de `.env`/`.env.local`**: scripts y `get_shopify_token.mjs` adaptados para probar 3 nombres por orden de prioridad: `.env.local` (gana) > `.envlocal` > `.env`.

### Decisiones operativas confirmadas

- **Coexistencia de apps**: la app vieja `API-Products` (token `shpca_…`) sigue funcional pero con scopes limitados. La nueva `Santavila Admin` (token `shpat_…`) es la nueva fuente de verdad. El `.env` antiguo se mantiene como red de seguridad mientras dura la transición.
- **Zone Pen+Baleares**: incluye Baleares al mismo coste que península. **Pendiente**: confirmar con proveedores si el coste real Baleares justifica un recargo (probablemente sí, +20-40€ por ferry). Por ahora se asume internamente.
- **5 escenarios de validación** del [SHIPPING_PROFILES_SETUP.md](SHIPPING_PROFILES_SETUP.md) pendientes de probar en checkout preview.

### Estado de bloqueadores

| # | Bloqueador | Estado |
|---|---|---|
| 1 | Política `compareAtPrice` | ✅ |
| 2 | PVP Balliu | ✅ |
| 3 | WhatsApp comercial | ⏸ Esperando SIM |
| 4 | Política envío Balliu | ✅ Implementada en producción |
| 5 | Garantía Balliu | ✅ |
| 6 | Theme versionado dónde | 📝 Se decide al ejecutar F0-09 |
| 7 | **Scopes OAuth ampliados** | ✅ Resuelto con app nueva |

### Siguiente paso recomendado

Sprint 1 sigue avanzando. Tres tareas siguientes en orden:

1. **Validar 5 escenarios en checkout preview** (Paso 4 del SHIPPING_PROFILES_SETUP.md). Especialmente Escenario 3 (multi-categoría sin llegar a 500€ → confirmar que se suman tarifas) y Escenario 5 (multi-categoría + ≥500€ → gratis).
2. **F0-09 — `shopify theme pull`** (~20 min). Ya tenemos `read_themes` activo. Desbloquea toda la Fase 0 visible.
3. **F1-01 — crear los 31 metafield definitions restantes** del namespace `santavila` (`santavila.envio_categoria` ya cuenta como el 1º de 32).

### Reclasificaciones de envío pendientes (anotadas en entrada anterior)

- `balliu-colchoneta-para-tumbona-0e9a3256` (asignada a L, probablemente M)
- `balliu-base-de-parasol-*` y `balliu-pie-de-parasol-*` (asignadas a L, probablemente M)

Cuando se revisen, basta con relanzar `apply_shipping_categories.py --apply --only-handles ...` y luego `assign_products_to_shipping_profiles.py --by-name --apply` (mueve las variantes al profile correcto).

---

## 2026-05-14 · Decisiones estratégicas cerradas (envío, garantía, WhatsApp)

**Paso del flujo:** desbloqueo de pre-Sprint 1
**Estado:** ✅ 3 decisiones cerradas · 1 en espera de hardware
**Quién:** sesión interactiva con dueño del negocio.

### Decisiones cerradas

#### 1. Garantía Balliu = 3 años ✅
Misma cobertura que Hevea. **F0-12 (página Garantía) desbloqueada.** El texto base puede usar "Garantía 3 años en todo el catálogo, ofrecida por nuestros proveedores españoles" sin diferenciar por marca.

#### 2. Política de envío — tarifas volumétricas

Decidida estructura por **3 tiers + umbral de gratuidad**, basada en clasificación de los 281 SKUs del catálogo (script de análisis ad-hoc sobre hoja `20260508 -Todos `):

| Tier | Tarifa cliente | Cubre | # SKUs | % catálogo |
|---|---|---|---|---|
| **XS** | 9,95€ (1 ud) / 14,95€ (2 ud) / 19,95€ (3-4) / 24,95€ (5-8) / 29,95€ (9+) | Cojines, fundas, limpiador, accesorios pequeños | 10 | 4 % |
| **M** | 29,95€ plano | Mesa auxiliar/centro/lateral, mesa ≤ 80 cm, silla individual, taburete, reposapiés, parasol < 250 cm Ø, accesorios resina | 134 | 48 % |
| **L** | 57,95€ plano | Mesa comedor, sofá, conjunto, tumbona, banco, balancín, cama balinesa, parasol ≥ 250 cm Ø, pérgola | 137 | 49 % |
| **Gratis** | 0 € | Pedidos con **subtotal del carrito > 500 €** | — | — |

**Umbral gratuito = 500€** (descartado 400€ para alinear con el AOV objetivo del modelo financiero `00_SUPUESTOS`). Con 500€, **131/281 SKUs (47%)** activan gratis por sí solos, vs 162/281 (58%) con 400€ — diferencia de 31 SKUs en la franja 400-500€ que ahora sí pagan envío. Ese tramo es importante porque es donde está el AOV de campañas Meta/Google y conviene que el cliente lo asuma para que el modelo no pierda margen ahí.

**Validación financiera** (sobre simulación 1 producto/pedido):
- 53% de los pedidos cobran envío al cliente.
- 47% activan gratis → coste interno asumido ≈ 49€ medio por pedido.
- Ratio envío/PVP en el tramo cobrado: 16-30% (coherente con dato real Hevea: mediana 11% a 50€ planos).

**Pendiente operativo:** confirmar tarifa real de Balliu para península. Mientras no llegue, asumimos coste interno ≈ 50€ por pedido Balliu sin gratuidad (mismo orden de magnitud que Hevea). Cuando llegue la tarifa, se rellena la columna `Coste Envío` (J) en `20260508 -Todos ` y el modelo financiero (`02_UNIT_ECONOMICS_SKU`) recalcula automáticamente.

**F0-11 (página Entrega) desbloqueada** con texto definitivo.

#### 3. WhatsApp comercial — en espera ⏸

Pendiente de tarjeta SIM. Cuando llegue, se constata en el proyecto.

**Implicación operativa para Sprint 1:**
- F0-14 (página Contacto): se crea **con email `hola@santavila.com` + formulario nativo Shopify**, sin botón WhatsApp.
- F2-10 (CTA flotante WhatsApp): queda diferida hasta que la SIM esté operativa. Sin entrada en el Sprint actual.

Nota recordatoria: cuando llegue el número, hay tres puntos del theme/sitio donde añadirlo — barra de confianza, footer, página Contacto, CTA secundario en PDPs. Anotado para no olvidar.

#### 4. Theme — dónde versionarlo (pendiente)

Sigue sin decidirse. Recomendación de la auditoría: versionar en `theme/` dentro de este mismo repo. Se decide al ejecutar F0-09 (`shopify theme pull`).

### Resumen del estado de los 6 bloqueadores originales

| # | Bloqueador | Estado |
|---|---|---|
| 1 | Política `compareAtPrice` | ✅ Resuelto (entrada 2026-05-13) |
| 2 | PVP Balliu | ✅ Resuelto (entrada 2026-05-13) |
| 3 | WhatsApp comercial | ⏸ En espera de SIM |
| 4 | Política envío Balliu | ✅ Resuelto (3 tiers + umbral 500€) |
| 5 | Garantía Balliu | ✅ Resuelto (3 años, misma que Hevea) |
| 6 | Theme versionado dónde | 📝 Se decide al ejecutar F0-09 |

### Aplicación técnica de la clasificación de envío (2026-05-14, mismo día)

Tras cerrar la política, se ha ejecutado la parte automatizable:

- **Entregables nuevos:**
  - [`apply_shipping_categories.py`](../../apply_shipping_categories.py) — script Python, mismo patrón que `sync_prices_to_shopify.py` (dry-run por defecto, `--apply`, `--limit`, `--only-handles`).
  - [`SHIPPING_PROFILES_SETUP.md`](SHIPPING_PROFILES_SETUP.md) — guía paso a paso para configurar los 4-5 shipping rates en Admin.

- **Metafield definition creada manualmente:** `santavila.envio_categoria` (single_line_text_field, valores controlados `xs|m|l`).

- **Apply ejecutado contra producción:**
  - 225 productos procesados (los 281 SKUs de la hoja maestra incluyen variantes que comparten handle).
  - **222 ACTUALIZADO · 3 SIN_CAMBIOS · 0 errores.**
  - Distribución final: **XS=6, M=93, L=126.**
  - Cada producto ahora tiene tag `envio:xs|m|l` y el metafield `santavila.envio_categoria`.

- **Reclasificaciones a revisar manualmente (heurística automática es conservadora):**
  - `balliu-colchoneta-para-tumbona-0e9a3256` → marcado **L**. Por nombre no contiene "cojin"/"funda" así que cae en default. Probablemente debería ser **XS** o **M** según peso real. Validar.
  - `balliu-base-de-parasol-*` y `balliu-pie-de-parasol-*` → marcado **L**. Una base/pie de parasol típicamente pesa 15-30 kg. Si la mayoría son <20 kg conviene bajar a **M** (29,95€) — más justo para el cliente. Validar.

- **Bug menor encontrado en docs:** PROYECTO.md menciona `.envlocal` pero el archivo real es `.env.local`. El script ahora prueba 3 nombres por compatibilidad. **Pendiente:** actualizar PROYECTO.md para reflejar la realidad y unificar `sync_prices_to_shopify.py` con el mismo patrón.

- **Estado del usuario:** ejecutando Paso 3 del SETUP (crear las 5 rates en Admin Shopify) en paralelo a este apply. Validación de checkout queda como tarea siguiente.

### Siguiente paso recomendado

Con 5 de 6 bloqueadores cerrados y la clasificación de envío ya en producción:

1. **Validar 5 escenarios en checkout preview** (Paso 4 del [SHIPPING_PROFILES_SETUP.md](SHIPPING_PROFILES_SETUP.md)). Confirmar especialmente Escenario 5 (multi-categoría + umbral 500€ → gratis) que es el más sensible.
2. **Revisar las reclasificaciones marcadas arriba** (colchoneta, bases/pies de parasol). Si hay que mover de L→M, basta `python3 apply_shipping_categories.py --apply --only-handles handle1,handle2` después de editar la heurística.
3. **F0-09 — `shopify theme pull` (20 min).** Desbloquea Fase 0 visible (footer, barra de confianza, badges).
4. **F1-01 — crear los 32 metafield definitions vacíos en Admin (45-60 min).** Lista en [`DATA_MODEL_SANTAVILA.md`](DATA_MODEL_SANTAVILA.md). No rompe nada y desbloquea fases 2-7.

> Nota: la metafield definition `santavila.envio_categoria` creada hoy **ya es 1 de los 32** del modelo de datos. Quedan 31.

---

## 2026-05-13 · Sincronización masiva de precios a Shopify con redondeo psicológico

**Paso del flujo:** F0-01 redefinido — `sync_prices_to_shopify.py`
**Estado:** ✅ Aplicado en producción (`mueblesexterior.myshopify.com`)
**Quién:** sesión interactiva, script existente extendido con `compareAtPrice` + redondeo por segmento.

### Qué se ejecutó

- Extensión de `sync_prices_to_shopify.py`: añadidas funciones `psy_price`, `psy_compare` y `_round_compare_high`; nueva flag `--skip-compare`; query y mutación GraphQL incluyen ahora `compareAtPrice`; reporte CSV con 2 columnas nuevas (`compare_antes` / `compare_despues`).
- Mapeo confirmado contra hoja `20260508 -Todos`:
  - Col E "Coste neto (sin IVA)" → `inventoryItem.cost` (sin redondear).
  - Col F "Precio Venta (con IVA 21%)" → `variant.price` (con redondeo psicológico).
  - `variant.compareAtPrice` = `price_bruto × 1.10` (≥ 50 €) o `× 1.30` (< 50 €), redondeado limpio.
- Reglas de redondeo acordadas **segmentando por PRICE bruto** (no por coste literal del enunciado del usuario — 63/281 productos caían en segmento distinto y los precios resultantes eran más naturales así):
  - **< 50 €**: price termina en .95 — compareAt = bruto × 1.30, entero .00.
  - **50–500 €**: price .95; si cae en `[umbral, umbral×1.05]` baja a `umbral-0.10` (ej. 104→99.90). CompareAt = bruto × 1.10 con mismo truco (`umbral-0.05`).
  - **> 500 €**: price sin decimales, sube al siguiente entero terminado en 0/5/9. CompareAt = bruto × 1.10, busca número "limpio" (100>50>25>10) dentro de `[price_psy×1.05, price_psy×1.12]`.
- Prueba en 1 handle (`balliu-parasol-para-terraza-aluminio-300-cm-3b7e77d1`) → resultado verificado vía Admin GraphQL: price 1.049 €, compareAt 1.150 €, cost 561,54 €.
- Apply masivo a los 224 handles restantes.

### Entregables

- `sync_prices_to_shopify.py` — script extendido con redondeo psicológico y `compareAtPrice`.
- `sync_prices_report.csv` — gitignored, contiene los 281 cambios variant-a-variant.

### Resultado del apply masivo

| Métrica | Valor |
|---|---|
| Handles procesados | 225 / 225 |
| Variantes actualizadas | 270 |
| Sin cambios | 1 (parasol de la prueba previa) |
| Errores | **0** |

**Impacto económico agregado** (dry-run previo, sobre 271 variantes):

- Suma total de prices: **200.710,59 € → 249.326,65 €** (`+48.616 €  / +24,2 %`).
- 115 variantes suben (mediana +46,5 %). Productos NO-Balliu (sofás, sillones, mesas HPL) estaban en Shopify muy por debajo del PVP del Excel.
- 156 variantes bajan (mediana -9,0 %). Productos Balliu estaban en Shopify por encima del PVP del Excel — bajadas ~-21 % consistentes.
- Caso anómalo conocido y aceptado: `balliu-silla-exterior-con-brazos-resina-estilo-funcional…` baja de 251,25 € a 89,95 € (-64 %); revisión del Excel confirmaba coste/PVP correctos.

### Hallazgos clave

- **F0-01 cambió de naturaleza.** El backlog original planteaba VACIAR `compareAtPrice` en bulk para que la tienda dejara de parecer "siempre rebajada". Decisión tomada hoy: en vez de vaciar, **reestructurar** con `compareAtPrice ≈ price × 1.10` (o × 1.30 en productos < 50 €) usando números psicológicos limpios. Resultado: tachado discreto que comunica "buen precio" sin gritar saldo. La tienda ya no tiene compareAt errático (el `980 € → 809,92 €` de BRANDON-1 que disparó el hallazgo original ya no existe — el sillón ahora tiene `price 1189 €` / `compareAt 1300 €` = -8,5 %).
- **Decisión Balliu cerrada** (era §3.5 del journal del Paso 1): SÍ se aplica el PVP recomendado Balliu del Excel. La estrategia diferida queda obsoleta.
- **El precio actual en Shopify difería significativamente del PVP del Excel.** ~47 % más bajo en muchos productos NO-Balliu — sugiere que el catálogo Hevea original se subió con un margen propio inferior al de la tarifa del proveedor. Importante recordarlo si se compara métrica histórica de conversión: el AOV va a cambiar a partir de hoy.

### Decisiones tomadas que cierran bloqueadores del journal anterior

| Bloqueador previo | Estado tras hoy |
|---|---|
| ¿`compareAtPrice` se vacía en masa o producto a producto? | **Resuelto.** Ni una cosa ni otra: se reestructura con regla psicológica `+10%` (o `+30%` en < 50 €). |
| ¿Aplicar PVP recomendado Balliu (156 SKUs bajan ~22 %) o markup propio? | **Resuelto.** Aplicado el PVP recomendado del Excel (con IVA, redondeado psicológicamente). |

### Prioridades vivas (sin cambios respecto al journal anterior)

F0-02 (vendor → Santavila), F0-03 (limpiar tags B2B), F0-07 (2 productos sin imagen), F0-09 (theme pull), F1-01/F1-02 (metafield y metaobject definitions). Todas siguen pendientes.

### Siguiente paso recomendado

- **Validación visual ligera:** abrir 4-5 PDPs en la admin de Shopify y confirmar que el tachado se renderiza con descuento entre 5-12 % y que no hay precios con decimales inesperados en gama alta.
- Cuando el pricing esté validado por el dueño, retomar **F0-02 → F0-03 → F0-09** como bloque siguiente de la Fase 0.

---

## 2026-05-13 · Cierre administrativo del Paso 1 (auditoría)

**Paso del flujo:** 1 — `00_PROMPT_ARRANQUE_AUDITORIA.md`
**Estado:** ✅ Entregables ya existentes. Sin reejecución.
**Quién:** snapshot original generado el **2026-05-06** contra `mueblesexterior.myshopify.com` vía Admin GraphQL API 2026-01 (autenticado como `hola@santavila.com`).

### Qué se ejecutó hoy

- Revisión de los 4 documentos ya presentes en `docs/santavila/`.
- Creación de este `JOURNAL.md` como registro vivo del plan.
- Decisión deliberada de **no regenerar** los documentos para no sobrescribir trabajo válido (la auditoría es de hace 7 días, sigue siendo representativa).

### Entregables vigentes

| Documento | Líneas | Estado |
|---|---|---|
| [`AUDITORIA_SANTAVILA.md`](AUDITORIA_SANTAVILA.md) | 324 | ✅ Completo, con datos reales del catálogo |
| [`BACKLOG_SANTAVILA.md`](BACKLOG_SANTAVILA.md) | 717 | ✅ Tareas con IDs estables `F0-01`, `F1-02`, … |
| [`DATA_MODEL_SANTAVILA.md`](DATA_MODEL_SANTAVILA.md) | 450 | ✅ 32 metafields `santavila.*` + 8 metaobjects `sv_*` definidos |
| [`THEME_PLAN_SANTAVILA.md`](THEME_PLAN_SANTAVILA.md) | 366 | ✅ 19 secciones `sv-*` planificadas. Asume `shopify theme pull` previo (F0-09) |

### Hallazgos clave (lo más cargado de información)

#### Estado real del catálogo (snapshot 2026-05-06)
- **235 productos**: 231 ACTIVE, 4 DRAFT (cifras de la API; difieren de los 252 anotados en `PROYECTO.md` del 24/04 — la tienda ha movido catálogo entre fechas).
- **Distribución por vendor real:** Balliu 120, Hevea 115.
- **7 colecciones**, todas por tipo de mueble. Cero con descripción ni SEO.
- **0 metafields del namespace `santavila`**. **0 metaobjects.** Greenfield total.
- **0 productos con `santavila.producto_hero`** marcado.

#### Bloqueadores de percepción premium (P0)
1. **Descuento permanente en toda la tienda.** BRANDON-1: `compareAtPrice=980€` / `price=809,92€`. Confirmado: la tienda hoy parece "siempre rebajada".
2. **Vendor real expuesto.** `vendor = "Hevea"` o `"Balliu"` en los 235 productos. Algunos handles llevan prefijo `balliu-…` que se ve en URL.
3. **Tags B2B expuestos al cliente final.** `match-verde / match-rojo / match-amarillo` en los 120 productos Balliu (probablemente vienen de la app "Wholesale Pricing Discount B2B"). Tag `hostelería` visible en PDPs residenciales.
4. **Typo público en H1**: colección `sillones-de-exterior` con título `"Sofas de exterior"` (sin tilde, y handle desalineado del título). Es H1 + URL al mismo tiempo.

#### Bloqueador estructural (P0)
5. **Modelo de datos = 0.** Plazo, garantía, montaje, material estructurado, espacio, mantenimiento, peso, bultos: nada existe como metafield. La información vive dispersa en HTML libre y en `Santavila.xlsx`. **Sin esta capa, las fases 2-7 del plan son cosmética**.

#### Otros hallazgos relevantes
- **71 productos sin ALT** en imagen principal. **2 productos sin imagen principal.**
- **21 productTypes para 235 productos** con duplicidades por capitalización/acentos (`Sofá`/`Sofa`, `Accesorios`/`Accesorio`).
- **Peso del producto = 0 kg** detectado en BRANDON-1. Probablemente generalizado. Dato logístico crítico.
- **Idioma en producto:** 100 % español (no hay títulos en inglés). Bien.
- **Idioma en theme/footer/correos:** no auditable hoy — scope OAuth actual NO incluye `read_themes` ni `read_content`. Marcado como pendiente de inspección visual.
- **Imágenes de proveedor expuestas en URL** vía prefijo `balliu-` en handles. Conviene migrar nombre en futuras altas pero **NO cambiar handles vivos sin redirect 301** (F0-05 contempla esto solo para la colección con typo).

### Prioridades vivas (P0 — Fase 0 + arranque Fase 1)

| ID | Tarea | Por qué es P0 |
|---|---|---|
| **F0-01** | Eliminar `compareAtPrice` permanente | Toda la tienda parece rebajada |
| **F0-02** | `vendor = "Santavila"` + crear `santavila.proveedor` interno | Marca coherente |
| **F0-03** | Limpiar tags `Hevea`, `Balliu`, `match-*`, `hostelería` visibles | Datos internos en storefront |
| **F0-07** | Resolver los 2 productos sin imagen principal | No se pueden vender así |
| **F0-09** | `shopify theme pull` del theme actual | Bloquea toda la Fase 0 visible (F0-10, F0-15, F0-16) |
| **F1-01** | Crear los 32 metafield definitions `santavila.*` | Palanca de todo lo demás |
| **F1-02** | Crear los 8 metaobject definitions `sv_*` | Palanca |
| **F1-03** | Poblar `sv_supplier` con Hevea y Balliu | Base para F0-02 |

Fase 0 completa (idioma, footer, claims, páginas Entrega/Garantía/Mantenimiento, barra de confianza, badges de valor) se ataca en paralelo a Fase 1 — son tareas independientes.

### Decisiones pendientes que bloquean el siguiente paso

Antes de pasar al **prompt 02 (sprints)** y empezar a ejecutar Sprint 1 sobre Shopify, hay decisiones de negocio que cerrar. Ya están listadas en `plan_santavila.md §24` y se reflejan aquí filtradas por las que bloquean acciones concretas:

1. **¿Hay WhatsApp comercial?** Bloquea F0-14 (página Contacto) y F2-10 (CTA flotante).
2. **¿`compareAtPrice` se vacía en masa o se decide producto a producto?** Bloquea F0-01.
3. **¿Política Balliu de envío gratuito a península?** Bloquea texto de F0-11 (página Entrega). Hevea ya está confirmado (>900€).
4. **¿Garantía Balliu confirmada?** Hevea = 3 años validados. Balliu = pendiente. Bloquea F0-12 y los datos de `garantia_resumen`.
5. **¿Aplicar PVP recomendado Balliu (156 SKUs bajan ~22%) o mantener markup propio?** Decisión comercial diferida según `PROYECTO.md §3.c`. No bloquea el Sprint 1 pero condiciona la home y los productos héroe.
6. **¿Theme actual versionar en este repo o en uno aparte?** F0-09 sugiere versionar en `theme/` dentro del repo.

### Riesgos no resueltos del entorno

- **Scopes OAuth insuficientes para auditar todo.** El token actual lleva `read_products,write_products,read_files,write_files`. **Faltan:** `read_content` (páginas, navegación, policies), `read_locales`, `read_themes`. Antes del Sprint 1, ampliar scopes en la app del Partner Dashboard, generar nuevo token y guardar en `.envlocal`.
- **Referencia rota detectada:** `BACKLOG_SANTAVILA.md` y `DATA_MODEL_SANTAVILA.md` apuntan a `../../plan_santavila_shopify/plan_santavila.md`, pero el plan vive en `Agents-IA/plan_santavila.md`. Conviene corregir los enlaces. **No es bloqueante** — el contenido es correcto.
- **Score B2B `match-*`** de origen sin documentar. Antes de eliminar (F0-03), confirmar si los consume alguna app activa.

### Siguiente paso recomendado

**Opción A — Cerrar decisiones de negocio primero (recomendado).**
Responder a las 6 preguntas anteriores. Sin eso, el Sprint 1 se ejecuta con placeholders y se corrige luego. Tiempo estimado: 1-2 horas con el dueño del negocio.

**Opción B — Empezar Sprint 1 ya con lo que no depende de decisiones pendientes.**
Tareas que no requieren decisión humana:
- `F0-06` — añadir ALT a 71 productos.
- `F0-07` — resolver 2 productos sin imagen.
- `F0-08` — auditar 4 productos en DRAFT.
- `F0-04` — normalizar 21 `productType` a 8-10 valores.
- `F0-05` — fix typo "Sofas" → "Sofás" + redirect 301.
- `F1-01` — crear 32 metafield definitions vacíos en Admin (no rompen nada, no necesitan datos).
- `F1-02` — crear 8 metaobject definitions vacíos.

**Opción C — Saltar al prompt 02 (sprints).**
Pegar `02_PROMPT_IMPLEMENTACION_SPRINTS.md` en Antigravity para que un agente arranque Sprint 1 con los entregables actuales como base. **Solo si las decisiones pendientes están cerradas** o se acepta usar placeholders.

> **Recomendación de este journal:** Opción A → luego Opción C. Sin las 6 decisiones cerradas, Sprint 1 genera trabajo que hay que rehacer.

### Limitaciones honestas de la auditoría del 2026-05-06

Estas limitaciones están reconocidas en el propio `AUDITORIA_SANTAVILA.md` y conviene tenerlas presentes:

- **Footer, menú, mobile, carrito, páginas legales: no auditados** (sin acceso al theme ni a `pages`).
- **Apps instaladas: hipótesis basada en metafields auto-creados**, no confirmadas.
- **Schema, sitemap, indexabilidad: no auditados** por API.
- **Configuración de Markets, checkout y locales: no auditadas** por scope.

Estas zonas oscuras se resuelven en F0-09 (theme pull) + ampliación de scopes OAuth.

---

## Plantilla para próximas entradas

```markdown
## YYYY-MM-DD · [Título del hito]

**Paso del flujo:** X — `nombre_del_prompt_o_sprint.md`
**Estado:** ✅ / 🔄 / ⏸
**Quién/qué:** [agente, modelo, persona]

### Qué se ejecutó
- …

### Entregables
- `ruta/al/archivo.md` — [una línea]

### Hallazgos clave
- …

### Prioridades vivas tras este hito
- …

### Decisiones pendientes
- …

### Siguiente paso recomendado
- …
```
