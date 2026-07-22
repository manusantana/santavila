# Prompt-recipe: de los 7 bloques al prompt CORTO

> Los 7 bloques del rol (§7.2) son el **checklist mental**. Al enviar a Higgsfield se **comprimen** a 3–6 frases en modo edición (inglés). Prompt largo = imagen en blanco.

## Los 7 bloques (checklist mental — NO se escriben literales)
1. **Sujeto fiel** — tipología anclada a la foto real; conservar geometría, nº de piezas, material, acabado, color de variante; NO transformar.
2. **Escena** — una escena española creíble emparejada por paleta (ver escenas-region-temporada.md).
3. **Luz** — una sola fuente (sol); hora/dirección/dureza; sombra de contacto bajo las patas + proyectada.
4. **Óptica** — focal, altura de cámara (= plano de uso), ángulo 3/4, verticales a plomo, apertura.
5. **Estilismo** — props del kit de marca (0–1 hero · 3–5 ambiente); restraint; ocupación del mueble.
6. **Mood/grade** — neutros cálidos (paper/bone/sage/ink), 1 acento clay, saturación baja, más sombra y textura que color.
7. **Restricciones** — sin logos/texto; sin resort/chalet; sin personas montando; fondo nunca blanco puro.

## Regla de compresión
Mantén SIEMPRE: **conservar el producto exacto + escena + luz/hora**. Suelta: el dump de restricciones y los adjetivos de calidad. Describe **física**, no calificativos.

## Plantilla de prompt corto (inglés, modo edición)
```
Using the reference image, keep the [furniture type] EXACTLY as shown — same shape,
same [nº de cojines/listones/módulos], same material and finish, same color. Do not change the furniture.
Replace only the background/scene with [escena española concreta: suelo, muro, vegetación].
Light: [hora] sun, single source from [dirección], soft contact shadow under the legs.
Photorealistic, shot on a real camera.
```

## Ejemplos por toma (base — adaptar el sujeto y la escena)

**Toma 1 · Packshot (1:1, fondo bone)**
> *Using the reference image, keep the 3-seater outdoor sofa EXACTLY as shown (same 3 seat cushions, same aluminium frame, same rope weave, same color). Do not change it. Place it on a clean warm-bone studio backdrop (never pure white), soft large key light from 40° left at ~40° elevation, neutral 5400 K, crisp contact shadow under the legs and a long soft shadow to the right. 3/4 view at 35°, verticals plumb. Photorealistic.*

**Toma 2 · Ambiente (golden hour, escena emparejada)**
> *Using the reference image, keep the sofa EXACTLY as shown (do not change it). Put it on a real Spanish porch: microcement floor, whitewashed wall, an olive tree in a terracotta pot slightly out of focus. Late-afternoon Mediterranean sun, single source, warm light with long soft shadows. One linen cushion as accent, nothing else. Photorealistic, shot on a real camera.*

**Toma 4 · Detalle / ASMR (escala moderada, textura REAL)**
> *Using the reference image, close but not extreme detail of the real rope weave over the aluminium armrest and the cushion seam. Keep the exact real texture — do not invent any weave or fabric. Grazing side light at low angle to reveal the relief. Photorealistic.*

## Validado (Fase 0, LEISA)
Ancla `media_import_url`(URL CDN Shopify) → `media_id` → `generate_image(medias:[{role:"image"}])` con prompt corto → resultado premium fiel (terraza menorquina con barro/cal/olivo). El fondo se cambió desde una composición YA correcta (camino seguro: swap de fondo, no recomponer de cero cuando hay personas — evita el fallo de escala).
