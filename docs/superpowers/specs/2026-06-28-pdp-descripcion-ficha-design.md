# PDP — Descripción a ancho completo + Ficha técnica

**Fecha:** 2026-06-28
**Rama:** `pdp-descripcion`
**Base:** `main` @ `beccd32` (ya con la descripción del live sincronizada en git)

---

## Problema

La descripción SEO del producto (potente, reescrita por el sprint GEO) está embebida en la
**columna de compra** de la PDP (`santavila-product.liquid`), como `<details class="sv-pdp__description" open>`
entre el CTA de asesoría y la lista de envío. Es el peor sitio:

- Compite visualmente con el botón de comprar (ensucia la zona de conversión).
- Va en una columna estrecha (~40% del ancho), ilegible para un texto largo.
- Desbalancea la página: la columna derecha queda larguísima frente a la galería.

## Objetivo

PDP de mobiliario de exterior premium (ticket 1.000–5.000 €) que convierta: **arriba compacto = comprar;
debajo a ancho completo = descripción rica + ficha técnica**. 100 % responsiva (móvil/tablet/desktop).

## Decisiones de diseño

1. **Sacar la descripción de la columna de compra.** Se elimina el bloque `sv-pdp__description`
   (markup + CSS) de `santavila-product.liquid`. La columna de compra queda: título · precio · variantes ·
   carrito · asesoría · lista de confianza · métodos de pago.

2. **Nueva sección a ancho completo `santavila-pdp-description.liquid`**, ubicada **entre** `santavila_product`
   y `santavila_pdp_highlights`. Vive como sección propia (no engorda la PDP; reordenable desde el editor).

3. **Ficha técnica desde la propia descripción** (sin metafields nuevos, sin inventar datos — línea roja).
   La descripción tiene estructura fija escrita por el sprint GEO:
   ```
   <p><strong>…resumen+medidas…</strong>…</p>
   <p>…consejo de medir…</p>
   <h2>Detalles clave</h2>
   <ul><li><strong>Formato:</strong>…</li> … (Formato, Medidas, Estilo, Uso recomendado, Mantenimiento) …</ul>
   <p>…cierre…</p>
   ```
   **Parseo (Liquid, robusto):**
   - `assign parts = product.description | split: '<h2>Detalles clave</h2>'`
   - Si `parts.size > 1`: `parts[0]` = narrativa intro; `parts[1] | split: '</ul>'` → `[0]+'</ul>'` = la ficha (`<ul>`),
     `[1]` = `<p>` de cierre (se añade al final de la narrativa).
   - **Fallback** (si no existe el marcador `<h2>Detalles clave</h2>`, p. ej. descripciones aún no reescritas):
     se muestra `product.description` completa como narrativa a ancho completo, **sin** columna de ficha.
   - La ficha **solo** renderiza el `<ul>` tal cual (estilado). No reescribe ni añade campos.

4. **Chips de contexto** sobre la ficha: `product.type` (Sofá/Sillón/Mesa…) y "Hecho en España".
   Datos reales y universales (el `productType` está poblado en todo el catálogo).

## Layout

```
┌─ santavila_product · ZONA DE COMPRA (compacta, SIN descripción) ─┐
│  [ galería ]        Título · Precio · IVA                        │
│  [  foto   ]        [ Añadir al carrito ]                        │
│  [ thumbs  ]        asesoría · ✓envío ✓montaje ✓garantía · pago  │
└──────────────────────────────────────────────────────────────────┘

┌─ santavila_pdp_description · NUEVA (ancho completo) ─────────────┐
│  eyebrow + H2 "Descripción"      ┌─ Detalles clave ───────────┐ │
│  [chips: Sofá · Hecho en España] │ Formato    sofá 3 plazas   │ │
│  Sofá de terraza de 3 plazas…    │ Medidas    194×75 cm       │ │
│  Antes de comprar, mide…         │ Estilo     sofisticado     │ │
│  Elige este sofá si…             │ Uso        terraza, jardín…│ │
│                                  │ Mantenim.  …               │ │
│                                  └────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘

[ Por qué Santavila ]   [ Compra con tranquilidad ]   [ Relacionados ]
```

## Responsive (requisito duro — verificar de verdad)

- **Desktop ≥990px:** 2 columnas → narrativa `~1.6fr` | ficha `~1fr`. Ficha con `position: sticky` suave.
- **Tablet 750–989px:** 1 columna; la ficha pasa a tarjeta full-width **debajo** de la narrativa; padding contenido.
- **Móvil ≤749px:** apilado vertical — narrativa, luego ficha full-width como tarjeta debajo. Tipografía y `gap`
  reducidos; las filas de la ficha (`label / valor`) no se cortan ni se solapan.
- **Verificación:** preview en DEV con UA desktop **y** UA móvil (iPhone) antes de aprobar. No vale "se ve bien en desktop".

## SEO

- Sigue siendo un **único** `{{ product.description }}` (no se duplica) → sin contenido duplicado.
  Solo cambia de ubicación y gana jerarquía (H2 visible a ancho completo, mejor legibilidad).
- `<script type="application/ld+json">{{ product | structured_data }}</script>` y `santavila-schema.liquid`
  **intactos** (trabajo GEO del compañero). No se tocan.
- El `<h2>Detalles clave</h2>` se conserva (señal semántica).

## Líneas rojas / no-tocar

- **Honestidad:** la ficha refleja exactamente lo que dice la descripción. Cero datos inventados.
- **Trabajo del compañero:** no tocar `index.json`, `footer-group.json`, `cart.json`, `settings_data.json`
  (los 4 ficheros live≠git pendientes), ni el schema, ni las páginas de confianza.
- **Montaje:** Santavila no monta a domicilio (self-assembly). No añadir claims de instalación nuestra.
- Al subir a LIVE: subir **solo** `santavila-product.liquid`, `santavila-pdp-description.liquid` y `product.json`.
  No re-subir el theme entero (evita pisar los 4 ficheros del compañero).

## Validación

1. Implementar en rama `pdp-descripcion`.
2. Subir los 3 assets a **DEV** `189114876228` por Asset API (token `.envlocal`).
3. Preview real: desktop + UA móvil. Comprobar: descripción legible a ancho completo, ficha bien alineada,
   fallback OK en un producto sin "Detalles clave", nada roto en la zona de compra.
4. Ajustar hasta que esté impecable en los 3 tamaños.
5. Subir a **LIVE** `189222715716` (solo los 3 assets) + merge a `main` + documentar (journal/backlog).

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Descripciones sin estructura "Detalles clave" | Fallback: descripción completa como narrativa, sin ficha. |
| `<p>` de cierre tras `</ul>` se cuela en la ficha | Split por `</ul>`; el cierre va a la narrativa. |
| Compañero edita `santavila-product.liquid` en paralelo | Trabajo en rama; al subir a live, solo los 3 assets; verificar md5 antes/después. |
| Romper responsive | Verificación obligatoria con UA móvil en DEV antes de live. |

## Fuera de alcance (handoff)

- **Poblar metafields estructurados** (`santavila.material`, medidas ancho/fondo/alto) en ~200 productos para
  una ficha-tabla 100 % estructurada. Es un proyecto de datos que encaja en la tarea SEO/datos del compañero.
  Se documenta en BACKLOG. Cuando existan, la sección puede migrar de "ficha desde descripción" a "ficha desde metafields"
  sin cambiar el layout.
