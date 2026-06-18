# Spec — Procedimiento de imagen de producto con Higgsfield (Santavila)

> Fecha: 2026-06-19 · Estado: aprobado en brainstorming, pendiente de plan de implementación.
> Origen: auditoría de imágenes ([`../AUDITORIA_IMAGENES.md`](../AUDITORIA_IMAGENES.md)) + investigación de posicionamiento ([`../../Santavila como líder de mobiliario exterior premium accesible en España.pdf`](../../Santavila%20como%20líder%20de%20mobiliario%20exterior%20premium%20accesible%20en%20España.pdf)) + guía de diseño ([`../GUIA_DISENO.md`](../GUIA_DISENO.md)) + Shop the Look ([`../INVESTIGACION_SHOP_THE_LOOK.md`](../INVESTIGACION_SHOP_THE_LOOK.md)).

## 1. Objetivo

Definir un **procedimiento repetible** para producir, con el MCP de **Higgsfield**, la galería de imagen de cada producto de Santavila, de forma que la tienda parezca **una marca premium española de exterior** (no un catálogo de proveedor). Se valida primero en **1 producto end-to-end** (Fase 0), se afina, y luego se escala a todos los productos, sus variantes, las categorías, el Shop the Look y el home — **paso a paso**.

No es "poner imágenes": la asociación imagen↔producto ya está resuelta y la base está limpia (auditoría). El proyecto resuelve las 3 carencias reales: **galerías pobres (87 Hevea con 1 foto)**, **baja resolución (≤800px)** y **falta de coherencia/ambiente de marca**.

## 2. Principios (no negociables)

1. **Fidelidad ante todo.** Siempre se ancla en la **foto real del producto** (image-to-image / referencia). Higgsfield cambia escena, luz y calidad; **nunca** inventa el mueble (ni nº de tablillas, proporciones, acabado ni color). En ecommerce real no se puede mostrar algo distinto a lo que se envía.
2. **Mediterráneo contemporáneo creíble.** Escenas españolas reales: terrazas de ático, patios con sombra, porches, balcones urbanos, jardines medianos, pequeños hoteles con gusto. **Evitar los 2 errores del PDF: el tropical-resort genérico y el chalet de lujo imposible.** Más Menorca/Valencia/costa andaluza que Bali. Más sombra y textura que exceso de color. Más casa real que escapismo.
3. **No parecer catálogo ajeno.** Sin logos de proveedor, sin marcas de terceros, una sola voz visual.
4. **Honestidad (regla viva de la tienda).** La imagen no puede sugerir lo prohibido (montaje a domicilio, claims no confirmados). Self-assembly.
5. **Puerta de calidad antes de subir.** Ninguna imagen generada va a la tienda sin pasar QA (sección 7).

## 3. Galería objetivo por producto (receta del PDF)

Cada ficha termina con **4-5 imágenes**:

| # | Imagen | Fuente | Fondo |
|---|---|---|---|
| 1 | **Principal limpia** del producto, alta res | Packshot del real (recorte + limpieza) | Neutro Santavila (`--bone`) |
| 2 | **Ambiente A** — escena mediterránea de uso | Higgsfield (producto anclado en escena) | Escena de la librería |
| 3 | **Ambiente B** — segundo escenario | Higgsfield (producto anclado) | Otra escena de la librería |
| 4 | **Detalle** — macro de material/acabado/tejido | Zoom del real o gen anclado | Neutro |
| 5 | **Medidas** — toma técnica con cotas visibles | **Overlay determinista** (no IA) | Sobre el packshot (#1) |

Aspectos: PDP principal **1:1 cover**; las imágenes se preparan a ≥2000px lado mayor.

## 4. Método de generación

**A1 (elegido) — Recorte fiel + recomposición en escena.** El producto real se usa como **referencia** y Higgsfield genera el ambiente mediterráneo alrededor (`lifestyle_scene` / Nano Banana reference). Mueble 100% fiel, escena premium.

**A2 (fallback) — Restyle img2img directo** sobre la foto del proveedor. Solo si A1 no integra bien una pieza concreta (mayor realismo de escena a cambio de riesgo de fidelidad → exige QA más estricto).

## 5. Pipeline por producto (6 pasos repetibles)

1. **Origen** — seleccionar la mejor foto real del producto (mayor resolución/limpieza de su carpeta; usar el cruce de la auditoría `auditoria_imagenes_report.csv`).
2. **Packshot limpio** (#1) — recorte + fondo neutro Santavila, alta res.
3. **Ambientes** (#2-3) — colocar el producto en 1-2 escenas de la **librería** (sección 6), anclado.
4. **Detalle** (#4) — macro de material/acabado.
5. **Medidas** (#5) — overlay de marca con las cotas (del título/variante/metafield), tipografía JetBrains Mono; generado por plantilla, **no** por IA.
6. **QA + subida** — puerta de calidad (sección 7); si pasa → subir a Shopify (sección 8) en el orden de la receta.

## 6. Librería de escenas Santavila (6, reutilizables)

Mediterráneo contemporáneo creíble, luz y paleta constantes (coherentes con tokens: paper `#F7F4EC`, sage `#687060`, ink `#23251D`):

1. **Ático/terraza Menorca** — cal blanca, mar al fondo, sombra suave.
2. **Patio andaluz con sombra** — piedra, cal, vegetación contenida.
3. **Porche de casa real** — madera/aluminio, luz de tarde.
4. **Balcón urbano bien resuelto** — espacio pequeño, ciudad mediterránea.
5. **Jardín mediano mediterráneo** — césped/grava, plantas locales.
6. **Pequeño hotel / comedor exterior** — mesa puesta con gusto, sin teatralidad.

**Un sistema, tres usos:** estas 6 escenas alimentan también las páginas de **Shop the Look** y los **"Escenarios" del home** (mapea a la arquitectura del PDF: Salones, Comedores, Tumbonas y relax, Balcón y pequeño espacio, Áticos y terrazas, Jardín y porche). Cada producto se coloca en el/los escenario(s) coherentes con su tipología.

## 7. Puerta de calidad (QA) — antes de subir

Cada imagen generada pasa 4 chequeos (método de agentes-visión ya validado en la auditoría):
1. **Fidelidad** al producto real (geometría, proporciones, nº de elementos, color/acabado).
2. **Sin artefactos IA** (patas torcidas, fusiones, derretidos, manos/personas defectuosas).
3. **On-brand** (luz/paleta mediterránea creíble; NO resort/chalet; sin logos de tercero).
4. **Resolución** ≥2000px lado mayor y nitidez.

Si falla cualquiera → **re-prompt / regenerar**, no se sube. El resultado del QA queda registrado.

## 8. Herramientas y subida

- **Generación:** MCP/skills de Higgsfield (`higgsfield-product-photoshoot` modos `product_shot`/`lifestyle_scene`/`restyle`; `higgsfield-generate` con Nano Banana para trabajo de referencia/fidelidad). El backend de Higgsfield arma el prompt final; nosotros aportamos imagen de referencia + intención de escena.
- **Medidas (#5):** plantilla determinista (script) con tokens/fuentes de marca; cotas desde título/variante/metafield.
- **Subida a Shopify:** `stagedUploadsCreate` → PUT bytes → `productCreateMedia` → orden de la receta (reutilizar la infraestructura existente: `upload_images.py/.mjs`, `upload_balliu_images.py`; verificar 200). Estado live de partida en `_estado_imagenes.json`.
- **Coste:** Higgsfield consume créditos; la Fase 0 mide el coste real por ficha completa antes de escalar.

## 9. Fase 0 — piloto (1 producto end-to-end)

- **Producto:** 1 sofá/conjunto **Hevea de 1 sola foto** (para que el salto sea visible), con buen packshot de origen. Se elige juntos en el primer paso del plan.
- **Salida:** las 4-5 imágenes de la receta + QA + subida a su ficha.
- **Criterios de éxito (qué validamos):**
  1. Fidelidad: el mueble generado = el real (QA pasa).
  2. Escena: ambiente mediterráneo creíble y premium (no resort).
  3. Coherencia: encaja con el sistema visual de la tienda (PDP 1:1 cover, `--bone`).
  4. **Coste:** nº de créditos Higgsfield por ficha completa (para presupuestar el escalado).
  5. Procedimiento: prompts/recetas afinados y documentados para reutilizar.

## 10. Escalado (después de la Fase 0, paso a paso)

1. **1 por tipología** (sofá/conjunto, mesa, silla, tumbona, parasol) → plantilla de prompts por tipo.
2. **Todos los productos** (priorizando las 87 Hevea de 1 foto + cola de reemplazo de la auditoría: `silla-exterior-estilo-estilizado`, `banco-de-exterior-150-cm`, `DIVA_N24`, `Capri-Quadrada2`).
3. **Variantes** de color/acabado (fidelidad imagen↔variante).
4. **Categorías** (heros de colección con la librería de escenas).
5. **Shop the Look** (las mismas escenas con hotspots; la infraestructura Dwell ya existe).
6. **Home premium** (hero + escenarios + materiales, con la librería).

Cada fase entra cuando la anterior está validada. Cada salto grande puede tener su propio plan.

## 11. Fuera de alcance (YAGNI por ahora)

- Reescritura de fichas (copy), precios, envío: fuera; este spec es solo imagen.
- AR / "ver en tu habitación" (el 87% lo ignora — Shop the Look research).
- Vídeo de producto (posible fase futura, no ahora).
- Fotografía real con estudio/modelo (Higgsfield es el medio elegido para el arranque).

## 12. Riesgos / decisiones abiertas

- **Fidelidad de variantes sutiles** (chasis blanco vs tórtola): validar en QA que el color generado = el de la variante.
- **Medidas fiables:** confirmar que el título/metafield tiene las cotas correctas por producto antes del overlay.
- **Coste a escala:** el dato de créditos de la Fase 0 decide el ritmo (todo de golpe vs por tandas).
- **Integración de sombra/perspectiva** en A1: si una pieza no integra, usar A2 con QA reforzado.
