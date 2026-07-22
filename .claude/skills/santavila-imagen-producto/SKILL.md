---
name: santavila-imagen-producto
description: Úsalo al generar, crear, regenerar o mejorar imágenes o la galería de un producto de Santavila con Higgsfield — packshot, ambiente/lifestyle, ASMR/detalle, medidas; reemplazar fotos de baja resolución o productos con una sola foto; producir imágenes de catálogo, PDP o home de Santavila.
---

# Santavila · Imagen de producto con Higgsfield (pipeline end-to-end)

Produce la galería de un SKU (packshot → ambientes → detalle → medidas) con **fidelidad absoluta** al producto real, en una sola voz visual premium, y la sube a Shopify. Lo premium lo aporta el **oficio** (luz, sombra, escena), nunca cambiar el mueble.

**Fuente de verdad (leer para el detalle fino):** [`docs/santavila/ROL_FOTOGRAFO_SENIOR.md`](../../docs/santavila/ROL_FOTOGRAFO_SENIOR.md) (oficio: leyes, pilares, 5 tomas, tipologías, QA) · [`docs/santavila/FLUJO_IMAGEN_PRODUCTO.md`](../../docs/santavila/FLUJO_IMAGEN_PRODUCTO.md) (runbook). Este skill es la **capa de acción**.

## Ley suprema — FIDELIDAD (línea roja, no negociable)
Toda generación se **ancla a la foto real** del SKU (image-to-image / referencia). **NUNCA** se transforma: geometría, proporciones, nº de listones/cuerdas/cojines/módulos/plazas/patas, material y trama, acabado, color de chasis y tejido, herrajes. **Solo cambian:** escena, suelo, fondo, atrezzo, luz, sombra, encuadre, resolución. Si un ángulo obligaría a inventar una cara no fotografiada → se descarta el ángulo, no se inventa el mueble. Variante = su propia foto (si no hay foto de esa variante, no se genera).

## ⚠️ LECCIÓN CRÍTICA (así NO falla — verificado en la Fase 0)
Los modelos Nano Banana de Higgsfield **colapsan a un gradiente en blanco** con:
1. **Prompts largos** → envía un **prompt CORTO en modo edición** (3–6 frases, inglés): *"Using the reference image, keep the furniture EXACTLY as shown (do not change it) and replace only the background/scene with [escena], light [X]. Photorealistic."* La receta de 7 bloques del rol es el **checklist MENTAL, no el texto**.
2. **Resolución `2k`/`4k` directa** → genera **SIEMPRE a `1k`** y sube calidad después con `upscale_image`.
3. **Adjetivos de calidad** ("8k, ultrarrealista, fotorrealista extremo") → describe **la FÍSICA** (hora, dirección y dureza del sol, material, distancia de cámara), nunca calificativos.

Diagnóstico de imagen vacía: desviación estándar de píxeles ~15 = blanca; ~60 = contenido real. Coste ≈ 2 créditos/imagen a 1k.

## Flujo maestro (8 pasos)
1. **Inputs del SKU + lectura de diseñador:** foto real de mayor resolución; cotas reales (título/metafield) para la Toma 5; tipología (rol §5). **Lee el ESTILO del producto y fija su HÁBITAT** (perfil de diseñador — ver reglas rectoras): un tipo de espacio coherente con el estilo (contemporáneo→ático de diseño; rústico→caserío…) que se mantiene en TODA la galería. La temporada (§14) aporta luz/paleta/consumible.
2. **Anclar:** `media_import_url(<URL CDN Shopify de la foto real>)` → `media_id`.
3. **Generar tomas 1–4:** por toma, `generate_image({model:"nano_banana_pro", prompt:<CORTO>, medias:[{value:media_id, role:"image"}], aspect_ratio, resolution:"1k", count:2, get_cost:true})` → preflight de coste → lanzar sin `get_cost`. (nano_banana se coerce a `nano_banana_flash`.)
4. **Recoger:** `job_status(jobId, sync:true)` → URLs.
5. **Upscale:** `upscale_image` a 2k/4k lo aceptado (nunca pedir 2k/4k en generación).
6. **Toma 5 · medidas — NO IA:** overlay determinista (script) sobre la Toma 1; JetBrains Mono, líneas ink `#23251D` 70–80 %, máx. 3 cotas, dato verificado (nunca inventado).
7. **QA gate (bloqueante):** ver abajo. Falla un bloqueante → regenerar, **no subir**.
8. **Subir a Shopify:** `stagedUploadsCreate` → PUT bytes → `productCreateMedia` → `productReorderMedia` en el orden de la receta (packshot → ambientes → detalle → medidas). Verificar `mediaCount` y que la pos 0 es el packshot.

## Las 5 tomas
| # | Toma | Aspecto | Fuente |
|---|---|---|---|
| 1 | Packshot limpio (cover, fondo `bone`) | 1:1 | Higgsfield anclado |
| 2 | Ambiente A (escena/temporada) | 1:1 | Higgsfield anclado |
| 3 | Ambiente B (ángulo/escena opuesta) | 4:5 | Higgsfield anclado |
| 4 | Detalle / ASMR de material | 1:1 | Higgsfield anclado |
| 5 | Medidas (cotas) | 1:1 | **Overlay, NO IA** |

## QA gate — 4 bloques bloqueantes (contra la foto real)
- **A · Fidelidad:** conteo 1:1 exacto (listones/cojines/plazas/patas); geometría, material, color de variante (ΔE≤3). Cualquier desviación = rechazo.
- **B · Sin artefactos IA:** verticales a plomo; sin fusiones/derretidos; sombra de contacto bajo cada apoyo (no flota); una sola dirección de sol; sin HDR falso.
- **C · On-brand + estilo:** el ambiente **PEGA con el estilo del mueble** (lo pondría un interiorista — sin choque contemporáneo↔rústico); escena **vivida** (signos de uso + ASMR sensorial), no la pieza sola en un espacio vacío; **coherencia de secuencia** (mismo mundo en toda la galería); luz/paleta española creíble; NO resort/chalet; fondo cálido (nunca `#FFFFFF`); ≤5 props on-brand; 0 logos/texto IA; no sugiere montaje nuestro.
- **D · Técnico:** ≥2000 px, nítida; ratio correcto (cover en producto); compone en 1:1 sin amputar; textura legible.

Detalle completo y "tells" de IA: [`references/qa-checklist.md`](references/qa-checklist.md).

## Reglas rectoras (el oficio)
- **Perfil de diseñador — el ambiente lo dicta el ESTILO (no solo el color):** lee el estilo del mueble (contemporáneo / rústico / clásico mediterráneo / industrial / boho) y ponlo en SU hábitat (contemporáneo→ático de diseño, microcemento/hormigón; rústico→caserío/madera; clásico med→cal/barro). El ambiente es **variable por producto**; la paleta y la temporada afinan la luz/consumible. Un choque de estilo (mueble moderno en caserío rústico) = "parece IA" → rechazo. Mapa completo: [`references/perfil-disenador-escena.md`](references/perfil-disenador-escena.md).
- **Ambiente vivido + ASMR sensorial (piezas únicas):** la escena debe sentirse **habitada** (signos de uso reciente: libro abierto, manta con caída natural, cojín con huella) y activar un sentido — **vapor** del café/té, textura del lino/lana, gotas de un vaso frío, calidez de la luz. Listón: *"parece que alguien vive aquí ahora"*. **Nunca** la pieza sola en un espacio vacío y perfecto.
- **Coherencia de la secuencia:** toda la galería de UN producto = el **mismo mundo/hábitat**; los ambientes A y B son variaciones (ángulo, momento, atrezzo) del mismo espacio, no mundos distintos. Decide el hábitat una vez y mantenlo.
- Vender a **toda España**; **nunca** resort tropical ni chalet de lujo.
- **Escala doble puerta (§13.bis):** métrica (factor 0,92–1,10; hombros ≤0,80 de un cojín; estatura 160–188 cm) **y** composición (máx 2 personas en sofá 3 plazas + ≥1 cojín libre). Si "lee personas grandes" → suele ser composición; mídelo lado a lado antes de concluir. Los ASMR sin personas esquivan el problema.
- **Temporadas (§14):** backbone ESTABLE todo el año (packshot + ASMR — son la `og:image`/Google) + capa de temporada ROTATIVA (el ambiente). Temporada activa: **Verano Costero** (Cantábrico/Levante). La pos-1 NO cambia entre temporadas.
- **Texturas — línea roja (§15):** en ASMR/detalle, **prohibido inventar tramas**. El macro extremo empuja al modelo a fabricar textura (sling fino → tweed inventado = rechazo). Anclar a la foto real, **escala moderada**, y preferir features reales (mecanismo, unión estructura↔tela, costura, nudo) a un macro de tejido.

## Detalle operativo (references)
- Mecánica MCP exacta + subida Shopify: [`references/runbook-mcp.md`](references/runbook-mcp.md)
- Prompt corto: compresión de la receta + ejemplos validados: [`references/prompt-recipe.md`](references/prompt-recipe.md)
- **Perfil de diseñador (estilo→espacio, ambiente vivido/ASMR, coherencia de secuencia): [`references/perfil-disenador-escena.md`](references/perfil-disenador-escena.md)**
- Escenas por región y temporada + emparejamiento de paleta: [`references/escenas-region-temporada.md`](references/escenas-region-temporada.md)
- Parámetros por toma y tipología (ángulos/focales/kelvin): rol §3–§5.

## Regla rectora final
Si dudas entre *más espectacular* y *más fiel* → gana **fiel**. El lujo de Santavila nace de la sombra y la textura bien resueltas, no de inventar el mueble.
