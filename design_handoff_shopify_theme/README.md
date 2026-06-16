# Handoff: Tema Shopify Santavila — Home · Colección · Ficha de producto

## Overview

Santavila es una marca española de mobiliario de exterior **premium accesible** ("Diseño español para vivir fuera"). Este paquete contiene las **referencias de diseño de alta fidelidad** para construir su tema Shopify (Online Store 2.0): página de inicio, página de colección/listado y ficha de producto construida sobre la anatomía del *Perfect Product Page Builder™* (alta conversión).

La tienda live actual es `santavila.com` — se va a reemplazar por completo. **Trabajar siempre en un tema en desarrollo (no publicado), nunca sobre el tema live.**

> **⚠️ Modelo de entrega y montaje — IMPORTANTE.** Santavila **NO ofrece montaje a domicilio ni instalación**. El cliente recibe el producto en casa y **lo monta él mismo** (modelo self-assembly, estilo IKEA), con instrucciones ilustradas y kit de montaje incluidos. **Ningún texto, sección, metafield ni copy puede sugerir que Santavila realiza el montaje/instalación.** Sí se comunican plazo y nº de bultos; el montaje se describe siempre como sencillo y a cargo del cliente. (Este README contenía referencias erróneas a "montaje a domicilio" que se han corregido.)

## About the Design Files

Los archivos de este paquete son **referencias de diseño creadas en HTML** — prototipos que muestran el aspecto y comportamiento final, NO código de producción para copiar tal cual. La tarea es **recrear estos diseños como tema Shopify** (Liquid + JSON templates + secciones OS 2.0), siguiendo los patrones del ecosistema Shopify.

**Base recomendada:** partir de **Dawn** (fontanería: carrito, búsqueda, accesibilidad, performance) y reemplazar íntegramente la capa visual con este diseño. Alternativa válida: tema desde cero con arquitectura OS 2.0.

Los HTML se pueden abrir directamente en un navegador para inspeccionar medidas, estados y comportamiento (las imágenes son zonas de arrastre vacías a propósito — la fotografía real está pendiente).

## Fidelity

**Alta fidelidad (hifi).** Colores, tipografía, espaciados, radios, sombras y microcopy son finales y deben recrearse con exactitud. Reproducir píxel-perfect usando Liquid/CSS del tema.

## Files

| Archivo | Qué es |
|---|---|
| `Santavila Tienda.html` | Home completa (referencia principal) |
| `Santavila Coleccion.html` | Colección / listado con filtros |
| `Santavila Producto.html` | Ficha de producto (Perfect Product Page) |
| `store.css` | **Design system de la tienda: tokens + todos los componentes** |
| `pdp.css` | Componentes específicos de la ficha |
| `store.js` / `pdp.js` | Comportamiento (header, menú, sticky bar, acordeones, opciones) |
| `image-slot.js` | Soporte de las zonas de imagen de los prototipos (solo para visualizarlos; NO portar) |
| `Santavila Fundamentos.html` | Módulos de marca: overview, iconografía completa, elementos gráficos (el arco), layout |
| `Santavila Sistema Maestro.html` | Gobernanza, control de calidad y matriz del sistema |
| `styles.css`, `components.css`, `extra.css` | CSS de los documentos de marca (solo referencia) |
| `assets/` | Logos (principal, blanco, crema, wordmark, imagotipo) + favicons |

## Design Tokens → `settings_schema.json` + CSS global

Volcar estos tokens como settings del tema y/o custom properties globales. Fuente exacta: `store.css` (`:root`).

### Colores
| Token | Hex | Uso |
|---|---|---|
| `--paper` | `#F7F4EC` | Fondo base (blanco roto cálido) |
| `--paper-2` | `#FCFAF3` | Superficie elevada |
| `--bone` | `#EEE8DA` | Fondos de imagen / media vacía |
| `--sand` | `#E4DCCB` | Neutro cálido |
| `--stone` | `#D6D2C6` | Piedra fría |
| `--ink` | `#23251D` | Texto principal |
| `--ink-2` | `#4B4E41` | Texto secundario |
| `--ink-3` | `#767869` | Texto terciario / metadatos |
| `--sage` | `#687060` | **Color de marca** (medido del logo) |
| `--sage-deep` | `#474B3D` | Marca oscura / hover |
| `--sage-900` | `#2C2F26` | Fondos oscuros (header announcement, secciones ink) |
| `--sage-soft` | `#DCDFD4` | Tinte de marca claro |
| `--sage-50` | `#EEF0E9` | Fondo de badge |
| `--clay` | `#B27A5B` | Acento arcilla (uso <5% de superficie) |
| `--clay-deep` | `#8E5E42` | Acento oscuro (texto "Bajo pedido") |

Estados semánticos: éxito `#5E7350` / fondo `#e8eedf` · aviso `#B98A3E` / fondo `#f4ead3` · error `#A85440`.

### Tipografía (Google Fonts)
| Familia | Rol | Pesos |
|---|---|---|
| **Cormorant Garamond** | Display/serif: titulares, nombres de producto, citas | 400–600 + itálicas |
| **Hanken Grotesk** | Sans: cuerpo, UI, botones, navegación | 400–700 |
| **JetBrains Mono** | Mono: eyebrows, precios meta, etiquetas técnicas, breadcrumbs | 400–500 |

Patrones tipográficos clave (ver CSS para exactitud):
- `.eyebrow`: mono 11.5px, letter-spacing 0.28em, uppercase, color sage.
- Hero H1: serif, `clamp(54px, 9vw, 148px)`, line-height 0.92, em itálica.
- H2 de sección: serif `clamp(34px,4.6vw,64px)`.
- Cuerpo: Hanken 17px / 1.65.

### Espaciado, radios, sombras, easing
- Contenedor: max-width `1480px`, gutter `clamp(20px, 5vw, 76px)`. Secciones: padding-block `clamp(64px, 10vw, 150px)`.
- Botones/badges: **pill** (`border-radius:999px`). Cards/media: radios 4–18px.
- Easing: `cubic-bezier(.22,1,.36,1)`; transiciones 250–450ms; hover zoom de imagen `scale(1.04–1.05)` a 1.1s.
- Announcement bar fija (39px) + header fijo debajo.

## Screens / Views

### 1 · Home (`Santavila Tienda.html`) → `templates/index.json`
Secciones en orden (cada una = una sección Liquid):
1. **Announcement bar** (fija, sage-900, mono uppercase, 3 mensajes separados por ·).
2. **Header** (fijo): transparente con logo blanco sobre el hero → al hacer scroll pasa a crema sólido con blur y logo verde. Nav: Colecciones, Áticos y terrazas, Balcón, Jardín y porche, Materiales, Inspiración, Profesionales. Iconos: buscar, favoritos, cesta. Menú burger en <1080px (overlay sage-900 a pantalla completa, enlaces serif 34px; cerrado = `visibility:hidden`).
3. **Hero** 100svh full-bleed: imagen + gradiente oscuro, eyebrow + H1 "El exterior, *bien vivido.*" abajo-izquierda; derecha: **sello circular** (texto "FABRICADO EN ESPAÑA · DISEÑO PARA VIVIR FUERA ·" orbitando el arco, rotación lenta 30s) sobre los CTA "Explorar colecciones" (light) y "Amueblar por espacio" (ghost). Indicador "Descubre" inferior centro.
4. **Manifesto**: statement serif grande 2 columnas + párrafo y ulink.
5. **Escenarios**: 4 cards 3/4.3 con imagen, overlay, número mono y nombre serif con flecha en hover. → colecciones por escenario.
6. **Colección destacada** (Cala): media 4/4.6 + contenido (eyebrow, H2 serif, párrafo, 3 metas: precio desde / plazo / garantía, CTAs).
7. **Lo más deseado**: grid 4 product cards (ver componente abajo).
8. **Materiales** (fondo sage-900): media + lista de 4 materiales con swatch circular, nombre, descripción y tag mono.
9. **Fabricado en España** (fondo bone, centrado): arco SVG, H2 serif, párrafo, chips de provincias (mono, pill).
10. **Editorial "El exterior bien vivido"**: 1 card grande + 2 pequeñas (revista).
11. **Profesionales**: bloque espejado con CTA sage "Pedir propuesta".
12. **Servicios**: 4 columnas con icono + título + texto (entrega, **montaje fácil en casa** —self-assembly, no servicio—, garantía, asesoría).
13. **Newsletter** (sage-900): "Recibe ideas, no spam" + input pill + botón light.
14. **Footer**: marca + 3 columnas de enlaces + social + legal + placeholder pagos.

### 2 · Colección (`Santavila Coleccion.html`) → `templates/collection.json`
- Hero de colección 56vh con breadcrumb mono, H1 serif, descripción.
- **Filter bar sticky** (debajo del header fijo): chips pill (Todo, materiales, Quick ship, precio) + contador + ordenar. → mapear a Shopify **Search & Discovery filters** (metafields).
- Grid 3 columnas de product cards con **banda editorial** a ancho completo intercalada (asesoramiento CTA).
- "Cargar más" (botón line).

### 3 · Ficha de producto (`Santavila Producto.html`) → `templates/product.json`
Anatomía completa del Perfect Product Page (orden estricto):
1. **Galería**: rail de 6 miniaturas (1 vídeo con icono play) + stage 4/4.7 con **tags** ("Best seller" tinta, "Hecho en España" crema, "Pocas unidades" ámbar — pills mono, 1 línea), contador y zoom.
2. **Columna de compra (sticky)**: rating + nº reseñas (ancla) → H1 serif → **USP de producto en 1 línea** → precio + "IVA incluido · envío gratis" → línea BNPL (SeQura) → swatches color (44px, actualiza etiqueta) → configuración (botones con precio, actualiza precio del CTA) + **"Guía de medidas"** (abre modal con tabla) → QTY stepper + **"Añadir a la cesta · 779 €"** (≥56px, contraste) → botón express Shop Pay → risk remover ("30 días de prueba en casa") + mensaje de envío ("Enviado en 24h") → 2 chips USP de producto.
3. **Product promise** (statement serif centrado).
4. **3 Beneficios** (media + lista con iconos circulares) y **3 Características** (numeradas, border-top).
5. **Bloque emocional** (sage-900) + **review destacada** (blockquote serif itálica + estrellas).
6. **4 Company USPs** (asesoría, diseñado en España, entrega clara, garantía).
7. **Acordeones**: Medidas y materiales (abierto, con tabla specs) · Envío y entrega · Devoluciones y garantía · FAQ (3 preguntas + enlace).
8. **Social proof**: "Hablan de nosotros" (logos prensa serif itálica) · 3 testimonios card con "Verificada" · grid UGC #SantavilaEnCasa (5) · "Qué incluye / llega en 2 bultos".
9. **Completa la colección** (4 relacionados).
10. **Sticky add-to-cart bar** (aparece al perder de vista el bloque de compra): thumb + nombre + precio + QTY + CTA.

## Interactions & Behavior

- **Header**: páginas con hero → transparente (`hdr--over`, logo blanco) y sólido tras el hero (`hdr--solid`, blur + logo verde). Páginas sin hero → siempre sólido. Ver `store.js`.
- **Sticky add-to-cart**: IntersectionObserver sobre el bloque de compra (en producción funciona; ver nota abajo).
- **Opciones de producto**: swatch → actualiza etiqueta de acabado; configuración → actualiza precio en CTA y sticky bar. En Shopify: variantes nativas + `variant change` events.
- **Acordeones**: max-height animado; primero abierto por defecto.
- **Modal guía de medidas**: overlay blur, cierre con Escape/click fuera.
- **Hovers**: imagen `scale(1.04)`, botones flecha `translateX(4px)`, cards elevación suave.
- ⚠️ **Regla de oro de visibilidad**: los prototipos NO usan reveal-on-scroll porque el contenido nunca debe depender de JS/animación para ser visible. En el tema real se pueden añadir entradas sutiles **solo como mejora progresiva** (base siempre visible, respetar `prefers-reduced-motion`).

## Data model (hacer ANTES que las plantillas)

Metafields de producto (namespace sugerido `santavila`):
| Key | Tipo | Ejemplo | Alimenta |
|---|---|---|---|
| `material` | list.single_line_text | Cuerda náutica PE | Filtros, specs, card |
| `lead_time_type` | single_line_text | `quick_ship` \| `made_to_order` | Badge verde/ámbar, PDP, card |
| `lead_time_label` | single_line_text | "7–10 días" | PDP + card |
| `origin_province` | single_line_text | C. Valenciana | Bloque confianza + sello |
| `warranty_years` | number_integer | 3 | Chips, acordeón |
| `assembly` | single_line_text | "2 bultos · montaje sencillo en casa (2 personas)" | Acordeón |
| `scenario` | list.single_line_text | Ático, Balcón | Colecciones por escenario |
| `product_usp` | single_line_text | (1 línea bajo el título) | PDP |

Colecciones: por categoría (Salones, Comedores, Relax…) **y por escenario** (Áticos y terrazas, Balcón, Jardín y porche). Catálogo: títulos/SEO pendientes — reescribir con la voz de marca (consultiva, precisa, sin superlativos; CTAs: "Añadir a la cesta", "Hablar con un experto", "Pedir propuesta").

## Apps / integraciones
Reseñas (Judge.me o similar, con "compra verificada") · SeQura (BNPL) + Shop Pay · WhatsApp (asesoría) · Shopify Search & Discovery (filtros por metafield) · Markets ES/PT.

## Assets
`assets/`: `logo-santavila.png` (verde, sobre claro) · `logo-santavila-blanco.png` (sobre oscuro) · `logo-santavila-crema.png` · `santavila-wordmark.png` · `icono-santavila.png` / `ico-santavila.png` (imagotipo arco) · `favicon-32/64/180.png`. El **sello circular** y el **arco** están como SVG inline en los HTML (copiables tal cual). Fotografía: pendiente del cliente — usar `image_picker` en settings de sección.

## QA antes de publicar (resumen de gobernanza)
Tokens exactos (nunca aproximar colores) · contraste AA mínimo · sage ancla / arcilla <5% · sin urgencia falsa ni descuentos permanentes · datos honestos (material, plazo, origen, garantía) · un solo gesto de arco por composición · Core Web Vitals verdes.
