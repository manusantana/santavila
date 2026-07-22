# Runbook Higgsfield MCP + subida Shopify (mecánica exacta)

> Fuente: `docs/santavila/FLUJO_IMAGEN_PRODUCTO.md` + memoria de la Fase 0. Todo vía MCP de Higgsfield.

## Modelos
| Uso | Modelo | Notas |
|---|---|---|
| Fidelidad (packshot/ambiente/detalle) | `nano_banana_pro` | image-to-image; se **coerce a `nano_banana_flash`** (rápido, buena fidelidad de edición) |
| Iterar barato (tantear escena/luz) | `nano_banana_2` | misma familia |
| Alternativa producto/ads | `marketing_studio_image` | 1 ref `role:"image"`; también colapsa con prompt largo |
| Brand-kit DTC (fase posterior) | `ms_image` | requiere `style_id` vía `show_marketing_studio`; permite `batch_size` |

## Paso a paso

**1) Anclar la foto real**
`media_import_url({ url: "<URL CDN Shopify de la foto real del SKU>" })` → `media_id`.
Si la foto es local: subirla antes a un host/CDN accesible, o `media_upload_widget` (cliente con UI). Nunca pasar una URL cruda en `medias[].value` — siempre el `media_id`.

**2) Preflight de coste + generar (por toma)**
```
generate_image({
  model: "nano_banana_pro",
  prompt: <PROMPT CORTO en modo edición — ver prompt-recipe.md>,
  medias: [{ value: <media_id>, role: "image" }],
  aspect_ratio: "1:1",   // 1:1 packshot/detalle/medidas · 4:5 ambiente B
  resolution: "1k",       // ⚠️ SIEMPRE 1k. 2k/4k colapsan a blanco.
  count: 2,               // 2 candidatas para elegir
  get_cost: true          // PREFLIGHT primero
})
```
Si el coste es aceptable, repetir la misma llamada **sin** `get_cost` para lanzar el job → devuelve `job_id`.

**3) Recoger**
`job_status({ jobId: <job_id>, sync: true })` (imagen ~10–20 s) → URL(s) de salida.
Diagnóstico de blanco: descargar y medir desviación estándar de píxeles — **~15 = vacía** (regenerar/bajar longitud de prompt), **~60 = contenido real**.

**4) Upscale (subir calidad DESPUÉS)**
`upscale_image({ image_id, width, height, resolution: "4k" })` sobre las aceptadas. Objetivo ≥2400 px lado mayor.

**5) Toma 5 (medidas): NO pasa por Higgsfield** — overlay determinista por script sobre la Toma 1.

## Gotchas (Fase 0)
- **Prompt largo = imagen en blanco.** Comprimir a 3–6 frases (prompt-recipe.md).
- **2k/4k en `generate_image` = blanco.** Generar a 1k, upscale aparte.
- **Adjetivos de calidad = colapso.** Describir física (hora/sol/material/distancia).
- **Preflight siempre** con `get_cost:true` antes de gastar. ~2 créditos/imagen a 1k.
- **`count:2`** por toma para elegir, no regenerar a ciegas.
- **Reutilizar** prompt por tipología y escenas fijas → coherencia + menos prompt-engineering.

## Subida a Shopify (orden de la receta)
Reutilizar la infra existente (`upload_images.py/.mjs`, `upload_balliu_images.py`; verificar 200).
1. `stagedUploadsCreate` → obtener target + parámetros.
2. PUT de los bytes de cada imagen al target.
3. `productCreateMedia(productId, [{ originalSource, alt }])` por imagen.
4. `productReorderMedia(productId, moves)` → orden: **packshot(0) → ambiente A → ambiente B → detalle → medidas**.
5. Verificar `mediaCount` y que la posición 0 es el packshot correcto (no un detalle ni un ambiente).

**Registrar por SKU:** prompts finales por toma, créditos gastados, nº de regeneraciones, veredicto QA → afina la receta por tipología y presupuesta el escalado.
