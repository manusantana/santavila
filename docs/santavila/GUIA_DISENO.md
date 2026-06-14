# GUÍA DE DISEÑO — Santavila (estándares de la tienda)

> Reglas vivas para mantener TODA la tienda coherente. Antes de tocar cualquier sección, revisa esto.
> Objetivo: la mejor tienda de decoración exterior — coherente, honesta y que convierte.

---

## 1. Honestidad (NO negociable, riesgo legal)
Prohibido inventar afirmaciones. Solo lo confirmado por el dueño. En concreto **NO usar nunca**:
- ❌ Reseñas/testimonios con nombre o "Verificada" (no hay reseñas reales aún).
- ❌ Prensa ("Hablan de nosotros: El País / AD / Elle Decor…").
- ❌ "Envío gratis" (pospuesto: depende del proveedor; el umbral está en el Excel de costes).
- ❌ "Teléfono" como canal (NO hay). ❌ "Asesoría" → decir **"Atención personalizada"**.
- ❌ Plazos inventados (24 h, etc.), "30 días de prueba", garantía de "X años", financiación/SeQura.
- ❌ Montaje a domicilio / instalación nuestra (es **self-assembly**: lo monta el cliente).
- ❌ "Indicamos la provincia de fabricación en cada pieza" (no es real). ⚠️ Provincias del home `santavila-spain`: PENDIENTE de confirmar cuáles son reales.

**Hechos confirmados que SÍ se pueden decir:**
- Diseño y fabricación **en España** ("Hecho en España").
- Entrega estimada **hasta 30 días según disponibilidad del proveedor** (envío deslocalizado / proveedor logístico externo; NO "lo gestionamos nosotros").
- **Garantía legal** y **devolución por derecho de desistimiento** (las legales).
- **Fácil de montar en casa**, pocos bultos, instrucciones ilustradas (lo monta el cliente).
- Atención por **email `hola@santavila.com`**, **WhatsApp** (nº pendiente) y **chat** (Shopify Inbox).
- **Pago seguro** (pasarela de Shopify cifrada).

## 2. Tono "humano al 100%" (nada que parezca IA)
- Pocos elementos, copy cercano y real. Evitar rejillas de 6 cards iguales con copy de marketing vacío.
- Máx 3 sellos de confianza. Titulares simples y honestos ("Compra con tranquilidad", no "Razones reales para confiar").

## 3a. Botones (regla fija)
**TODOS los botones son pill (redondeo `999px`)** — primitiva `.sv-btn` y derivados. Esto incluye:
- Botón "Finalizar compra"/"Pagar" (`.cart__checkout-button`), add-to-cart, CTAs.
- **Botones de pago acelerado** (Shop Pay, Google Pay, Apple Pay, PayPal): Shopify ataba su radio al botón del tema (no pill) → se fuerza con `--shopify-accelerated-checkout-button-border-radius: 999px` (en `santavila-cart.css`).
- `.shopify-payment-button__button` también pill.
Nunca dejar un botón con esquinas rectas.

## 3. Anchos / layout
- TODA sección usa **`.sv-container`** (maxw 1480, gutter `clamp(20px,5vw,76px)`) → mismo ancho de página.
- Las rejillas de contenido ocupan **el ancho completo** del container (NO meter `max-width` que las estreche y rompa la alineación con las vecinas). El `max-width` solo se usa en **ch** para que los textos no sean líneas eternas (legibilidad), nunca para encoger una rejilla.

## 4. Imágenes (regla clave: PRODUCTO vs AMBIENTE)
- **Imagen de PRODUCTO** (ficha + tarjetas de producto): **`object-fit: contain`** sobre **fondo blanco** = product-fit, el producto se ve **completo, nunca recortado por los lados**. PDP: aspecto **1:1**; tarjetas (`.sv-pcard__media`): **4:5**. Sin hover-zoom (recortaría). ✅ Aplicado en PDP y en todas las tarjetas (`santavila-product-card` → home + colección).
- **Imagen de AMBIENTE / editorial** (hero, escenarios, materiales, editorial, featured, collection-hero, bandas `.sv-cband`): **`object-fit: cover`** = llena el espacio (recorte aceptable, son fotos de estilo de vida).

## 5. PDP (santavila-product) — patrón de referencia
- **Galería:** 1 foto principal **cuadrada (1:1) contain** sobre blanco + **miniaturas a la izquierda** (rail absoluto, scroll interno) que cambian la principal + **lightbox** para ampliar. Galería **sticky**. En móvil: apilado, miniaturas en fila abajo.
- **Variantes de color = swatches** (círculo de color) SOLO en la opción cuyo título contiene "color" (detección por JS → clase `.sv-sw-color`); **el resto de atributos (Chasis, etc.) = botones de texto**. Nombre del color elegido junto al título + tooltip. Robusto al re-render de Dwell (MutationObserver). Colores = mapa orientativo (la fidelidad real = Configuración → Swatches con foto de tela).
- **Precio:** se actualiza por variante (mecanismo nativo de Dwell, validado E2E). La **barra sticky** clona el precio real (no estático). 43/243 productos tienen precio variable → crítico que funcione.
- **Pago:** sin atajos; collapse informativo "Métodos de pago aceptados" con iconos reales. Oculto el aviso de "recogida en tienda" (es envío).
- **Secciones de la PDP:** producto → Por qué Santavila (highlights) → Confianza (3 sellos). Corta, no interminable.

## 6. Tokens y fuentes
- Tokens exactos en `santavila-tokens.css` (paper #F7F4EC, sage #687060, ink #23251D…). NUNCA aproximar colores.
- serif Cormorant (titulares), sans Hanken (cuerpo/UI), mono JetBrains (eyebrows/etiquetas/precios meta).

## 7. Animaciones
- El contenido SIEMPRE visible sin JS. Reveals al scroll solo como mejora CSS pura (`animation-timeline: view()` bajo `@supports` + `prefers-reduced-motion`). Nada que oculte contenido esperando JS.

## 8. Shop the Look (hotspots) — disponible en CUALQUIER página
Función nativa de Dwell, ya en el tema. Revestida con estilo Santavila (`santavila-hotspots.css`).
- **Sección:** `product-hotspots` (preset, categoría "Productos"). Se añade desde el editor en cualquier template (home, página, colección…).
  - Settings: **imagen** de ambiente, ancho (página/completo), altura (auto/21:9/16:9/4:3), overlay opcional, **`hotspot_color`** + **`bullseye_color`** (marca: sage `#737666` + crema `#ede6de`), color_scheme, tipografía del popover, padding.
  - Bloque **título** estático ("Shop the look").
- **Bloque `_hotspot-product`** (un punto = un producto): `product` (selector), `x-position` y `y-position` (0–100 % sobre la imagen).
- **Comportamiento (nativo, no tocar):** desktop = popover con foto + título + **precio real** + **añadir al carrito** (quick-add), posicionamiento automático sin salirse de pantalla; móvil = abre el quick-add modal. Punto con pulso sutil (CSS Santavila).
- **Revestimiento Santavila** (`santavila-hotspots.css`, solo estilo): popover = tarjeta papel + redondeo + sombra; título serif; precio sans tabular. La fontanería (posición, quick-add) es de Dwell.
- **Demo activa:** clonado el del live en el HOME del dev (tras "Escenarios"): imagen `bolonia-xl-1.jpg` + 3 productos. Para reutilizar: añadir la sección "Shop the Look" en la página que sea, elegir imagen y colocar los puntos sobre los productos.

## 9. Operativa (técnico)
- Tema vive en `theme/`. `push`/`pull`/`dev` SIEMPRE con `--path theme`. Subir archivos concretos por **Asset API** (no `--only`) y verificar 200. Tras subir, `pull` a /tmp + `diff -rq` (dev == disco).
- Dev theme: **#189114876228**. Live (NO tocar): #188231123268.
- Documentar cada hito en `JOURNAL.md`.
