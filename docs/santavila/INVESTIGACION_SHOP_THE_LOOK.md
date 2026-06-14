# Investigación — Shop the Look / Hotspots (competidores + best practices)

> Objetivo: tener el MEJOR "Shop the Look" de decoración de exterior. Fecha: 2026-06-14.
> Fuentes: Baymard, NN/g, Publitas, Stylitics, guías CRO/Shopify + webs de competidores.

## Qué hacen los competidores

| Marca | Cómo lo hace | Para llevarnos |
|---|---|---|
| **Westwing** | Galería de "looks" por estancia con **página dedicada por look** (incl. "Balcony & Garden"). Curado por estilistas. | Página/colección de **Ambientes por escenario de exterior** con URL propia (SEO + Pinterest). |
| **Kave Home** | **Páginas "Shop the Look" por tema, una específica `/shop-the-look-outdoor`**. Conjunto curado comprable (foto + lista de piezas). | Lo más cercano y mejor montado: **set comprable con lista de productos**. |
| **SKLUM** | NO usa hotspots: vende **conjuntos de jardín** (set coordinado) + configurador **3D/AR (HomeByMe)**. | "Comprar el conjunto" como bundle; AR = fase posterior. |
| **IKEA** | **Shoppable lookbooks** (revista interactiva): clic en la imagen → producto. Room sets dan contexto, descubren "piezas ocultas". | Fotos de ambiente REALES + descubrimiento de piezas. |
| **Zara / Zara Home / H&M Home** | Conjuntos curados + slider de imágenes clicables → PDP. (El "shoppable video con hotspots de Zara" es un concept de agencia, NO feature real.) | Curación estética + imagen→producto directo. |

## Principios que CONVIERTEN (consenso de las 3 investigaciones)
1. **Las mejores combinan las dos escuelas:** hotspots sobre la imagen (inspiración/descubrimiento) **+ lista de productos visible** debajo/junto a la imagen. La lista garantiza que el 100% vea y compre aunque no descubra los puntos (crítico en móvil, donde los puntos son difíciles de tocar).
2. **"Comprar el look completo" = palanca nº1 de AOV.** Añadir todas las piezas al carrito de una vez. Benchmarks: **+15–39% AOV**, +13% conversión (Stylitics, fashion; direccional). Para un set de terraza (sofá+mesa+cojines+sombrilla) encaja perfecto.
3. **3–6 hotspots por imagen**, colocados sobre el producto, sin tapar la escena; con **pulse** y **microcopy** ("Toca para comprar el look").
4. **Popover corto = soporte de decisión:** foto + nombre + **precio (+ tachado si descuento)** + variante (**botones, no dropdown**) + **2 CTAs: "Añadir" y "Ver producto"**. Sin descripciones largas.
5. **Móvil (la mayoría del tráfico):** puntos **numerados** + **lista numerada vinculada** debajo + tap → quick-add modal. Targets grandes (~44px).
6. **Fidelidad imagen↔variante** (Baymard): el punto lleva al producto EXACTO y la imagen muestra la variante real (color de cojín/acabado). El **79%** interactúa primero con la imagen en home/furniture → la foto de ambiente es el mayor activo.
7. **Rendimiento** (lazy-load, WebP/AVIF, evitar CLS) y **accesibilidad** (puntos como botones focusables, teclado, `aria-expanded`, alt, fallback sin JS = la lista de productos).
8. **NO priorizar AR / "ver en tu habitación"**: el 87% lo ignora (Baymard).

## Lo que YA tenemos vs lo que falta
**Tenemos:** hotspot → popover con foto + precio + añadir al carrito; móvil quick-add modal; estilo Santavila. Buena base.

**Falta para ser "el mejor" (priorizado):**

### Tier 1 — alto impacto, esfuerzo bajo-medio
1. **Lista de productos del look** debajo/junto a la imagen (siempre visible; fallback y móvil-friendly). Reutiliza la tarjeta de producto.
2. **Botón "Comprar el look completo / Añadir todo el ambiente"** (AJAX, añade todas las piezas). Palanca de AOV.
3. **Variantes como botones** en el quick-add (verificar el de Dwell).
4. **Precio tachado** en el popover si hay descuento.
5. **Doble CTA** en el popover: Añadir + Ver producto.
6. **Pulse + microcopy** "Toca los puntos para comprar el look" (pulse ya aplicado).

### Tier 2 — alto impacto, esfuerzo medio
7. **Móvil**: puntos numerados + lista numerada vinculada.
8. **Rendimiento**: lazy-load + WebP en la imagen de ambiente.
9. **Página dedicada "Ambientes / Compra el ambiente"** por escenario de exterior (terraza pequeña / balcón / jardín / porche / chill-out / comedor) → SEO + landing + Pinterest.

### Tier 3 — pulido y experimentación
10. Accesibilidad completa (teclado/foco/aria). 11. Cross-sell "completa tu conjunto" en PDP y carrito (convierte 3–5×). 12. Medir taps/AOV con control 2–4 semanas (GA4).

## Honestidad sobre los datos
- Benchmarks de AOV son de fashion (Stylitics) y agregados CRO → direccionales, no garantía para exterior.
- No hay dato A/B publicado del nº ideal exacto de hotspots ni del lift del pulse; "3–6" es consenso de guías.
- Fotos de ambiente REALES de exterior son el activo que más mueve la aguja → producir/seleccionar lifestyle real.

## Fuentes
Baymard (furniture/home UX, mobile, size buttons), NN/g (tooltips), Publitas (lookbooks), Stylitics (shop-the-look benchmarks), Monetate (shop vs complete the look), Cylindo (AOV furniture), Westwing /looks/, Kave Home /shop-the-look-outdoor, SKLUM conjuntos+HomeByMe, IKEA shoppable lookbooks, WebAIM (teclado).
