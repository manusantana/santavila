---
name: ARCHIVO-santavila-imagen-producto-v1-NO-USAR
description: "ARCHIVO HISTORICO — NO SEGUIR. Version 1 del skill de imagen, superada. El skill vigente es SKILL.md (v4). Se conserva solo como registro de como se trabajaba antes de los incidentes de fidelidad del 29-07-2026."
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
6. **Toma 5 · medidas — NO IA:** `python3 scripts/overlay_medidas_producto.py --img <packshot> --ancho N --alto N`. Overlay determinista sobre la Toma 1; JetBrains Mono, líneas ink `#23251D` 70–80 %, máx. 3 cotas, dato **verificado** (nunca inventado). **Tres reglas que se saltan solas y arruinan la cota** (ver más abajo): contorno automático, etiqueta explícita, cota de extremo a extremo.
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

## ⛔⛔ PROHIBIDO EL MACRO DE TEJIDO (2026-07-30)
Se publicaron **tres** ASMR con el jacquard **inventado** — y la regla que lo prohibía (§15) la había
escrito yo mismo horas antes. A escala macro **el modelo SIEMPRE fabrica la trama**: no la copia, la
reconstruye. Y una foto de catálogo a 1.500 px **no permite auditarla**, así que el QA tampoco puede
cazarlo. Es una toma que no se puede hacer con garantías.

**El detalle de tela solo se fotografía como FEATURE VERIFICABLE:** costura, ribete, cremallera, unión
tela↔estructura, herraje, nudo de cuerda. Nunca la trama por sí misma.
**Si la trama no se distingue en la foto del proveedor, NO HAY TOMA DE TRAMA.**

## ⛔ COHERENCIA DE VARIANTE dentro de la ficha
Todas las fotos de una ficha deben ser **el mismo color y acabado**. Mezclar el packshot de la versión
blanca con ambientes de la gris es tan grave como cambiar un material: son **dos productos**.
Verificar la variante de TODAS las fotos, no solo de la principal.

## 🛑 NADA SE PUBLICA SIN VISTO BUENO
El pipeline termina en **"listo para revisar"**, no en "publicado". Una ficha cada vez: se genera, se enseña,
el dueño valida, y solo entonces se sube. **Nada de tandas.**

## 📕 LEE ESTO ANTES DE EMPEZAR
[`docs/santavila/LECCIONES_FIDELIDAD.md`](../../docs/santavila/LECCIONES_FIDELIDAD.md) — las creencias
equivocadas que llevaron a publicar imágenes con material inventado, trama eliminada, color desviado, un
herraje que no existe y **la galería de un producto en la ficha de otro**. No es historia: son los errores
que se repiten si no se leen.

> **Si no existe, no lo hago. Si no sé hacerlo, no lo hago. Si no lo puedo verificar, no lo publico.**

## 🚦 PASO 0 — FICHA DE VERDAD (sin ficha no se genera NADA)
**Antes de importar la foto, antes del primer prompt, antes de cualquier cosa:** abre la foto real a
**resolución nativa**, recorta cada componente y escribe lo que ves en
[`docs/santavila/FICHAS_VERDAD.md`](../../docs/santavila/FICHAS_VERDAD.md) — chasis, tejido, **tablero
(material · tono · acabado · canto)** y piezas que la ficha NO incluye.

- **Sin fila en esa tabla, no se lanza ni un job.** No es una recomendación: es la puerta de entrada.
- **Lo que no se ve con certeza no existe.** Se anota `NO DETERMINADO` y **la toma en la que ese elemento
  aparecería NO se genera**. Nunca se deduce, se completa ni se interpreta.
- **La ficha se copia literalmente al prompt**, con la negación de lo que el modelo tiende a inventar.
- **El QA se hace contra la FICHA**, no contra el packshot propio — el packshot también puede estar mal,
  y si lo está, arrastra el error a toda la galería.

Este paso existe porque se publicaron **dos** versiones seguidas de una misma imagen con el material de la
mesa inventado (piedra caliza, y luego gris claro brillante en vez de gris cemento oscuro mate). El fallo no
fue del modelo: fue **empezar a generar sin haber leído el producto**.

## 🚦 PASO 0.bis — IDENTIDAD: ¿es este el producto de esta ficha?
**Antes de publicar, compara tu packshot con la foto real DEL HANDLE DESTINO.** Si no es el mismo mueble
(mismo tipo de brazo, misma estructura, mismo color de chasis y tejido), **no se publica**.

Se publicó la galería del **Albania** (tórtola + salvia, sillones de aspa) en la ficha del **Bellagio 3 pl.**
(antracita + gris, brazos rectos, 3.449 €), y estuvo días en producción. El mapeo `carpeta → handle` del
script se escribió a mano y **el nombre de la carpeta se dio por bueno como identificación del producto**.
Un nombre de carpeta no identifica nada: la única identificación válida es **la foto real del handle**.

## ⛔ La SUPERFICIE que sostiene el atrezzo ES PRODUCTO (lección 2026-07-29)
En el ASMR de consumible (la copa, la fruta, el plato) el **tablero de la mesa ocupa la mayor parte del
encuadre** — y es exactamente ahí donde el modelo lo reescribe: un HPL gris liso se convirtió en **piedra
caliza rugosa** y se publicó. El fallo pasó el QA porque yo miraba el mueble (conteo, chasis, tejido) y leía
la mesa como "bodegón". **No lo es: es producto, y su material es tan innegociable como el nº de plazas.**

Antes de aprobar CUALQUIER toma en la que el producto sostenga algo:
1. **Recorta el tablero de la foto REAL a resolución nativa** y ponlo al lado del tuyo. A tamaño tira no se
   distingue una lama de una veta — hay que ampliar.
2. Verifica las tres cosas por separado: **material** (HPL / cristal / lamas de aluminio / piedra),
   **acabado** (liso vs. lamas, y el ancho de la lama) y **canto** (fino, con junta oscura, biselado).
3. En el prompt, **nombra el material y niega el que el modelo tiende a inventar**:
   *"the table top is FLAT SMOOTH GREY HPL — not stone, not travertine, not wood, no visible grain"*.
   Esto es lo mismo que ya hacemos con las lamas de aluminio → madera (§15): la línea roja de texturas
   **también aplica a las superficies horizontales**, no solo a los tejidos.

## 🌡️ El GRIS FRÍO no aguanta la luz de atardecer (lección 2026-07-30)
Cuando el producto es **gris frío** (tejido, cuerda o chasis antracita), una escena de atardecer cálido lo
vira a **beige dorado** y el aluminio antracita a **bronce**. Salió publicado así en 6 fichas (A7) y volvió a
salir al primer intento del Sofá 220×90 en tres de sus cinco tomas.

**No es un defecto del prompt de escena: es incompatibilidad de paleta.** Si la ficha de verdad dice
"gris frío", el hábitat se elige con **luz neutra o del norte**, y el prompt lo fija explícitamente:

> *"CRITICAL COLOUR: the fabric must read COOL NEUTRAL GREY and the frame MATT ANTHRACITE — never beige,
> never golden, never bronze. Neutral daylight, white balance 5400 K, no warm colour cast."*

Los ambientes de atardecer se reservan para las paletas cálidas (tórtola, crudo, arena, blanco cal).

## QA gate — 4 bloques bloqueantes (contra la foto real)
- **A · Fidelidad:** conteo 1:1 exacto (listones/cojines/plazas/patas); geometría, material, color de variante (ΔE≤3). Cualquier desviación = rechazo.
- **B · Sin artefactos IA:** verticales a plomo; sin fusiones/derretidos; sombra de contacto bajo cada apoyo (no flota); una sola dirección de sol; sin HDR falso.
- **C · On-brand + estilo:** el ambiente **PEGA con el estilo del mueble** (lo pondría un interiorista — sin choque contemporáneo↔rústico); escena **vivida** (signos de uso + ASMR sensorial), no la pieza sola en un espacio vacío; **coherencia de secuencia** (mismo mundo en toda la galería); luz/paleta española creíble; NO resort/chalet; fondo cálido (nunca `#FFFFFF`); ≤5 props on-brand; 0 logos/texto IA; no sugiere montaje nuestro.
- **D · Técnico:** ≥2000 px, nítida; ratio correcto (cover en producto); compone en 1:1 sin amputar; textura legible.

Detalle completo y "tells" de IA: [`references/qa-checklist.md`](references/qa-checklist.md).

## Toma 5 · medidas — las 3 reglas (lección 2026-07-23)
Las medidas son lo más **delicado** de la galería: un cliente decide la compra con ellas.
1. **Contorno AUTOMÁTICO, nunca "a ojo".** Medir el bbox a ojo dejó la cota de ancho corta (no llegaba al reposabrazos). En los packshots bone el producto es **neutro** (gris/antracita, R≈B) y el fondo **y la sombra** son **cálidos** (R−B alto): filtrar por neutralidad da el contorno real sin que la sombra lo contamine. Lo hace el script.
2. **Etiqueta EXPLÍCITA:** `Ancho · 72 cm` / `Alto · 75 cm`, nunca solo "72 cm". Un "72×75" suelto es ambiguo (hay categorías que usan largo×ancho×alto) y se lee al revés.
3. **De extremo a extremo:** cada cota debe abarcar **todo** el producto en ese eje (con sus topes en los extremos reales) y colocarse en el lado **limpio** (la sombra suele caer a la derecha → la cota vertical va a la izquierda).

Si la ficha no desglosa qué medida es cuál (p. ej. "72×75 cm"), **pregunta**; no lo deduzcas de la foto: en perspectiva 3/4 una diferencia de 3 cm es indistinguible.

**4. Acota sobre una vista FRONTAL, no sobre un 3/4** (lección 2026-07-26, pérgola). En 3/4 el bbox horizontal suma el fondo en escorzo: una pérgola de 300×300 proyecta bastante más de 300 cm y la cota mentiría. Genera una toma frontal casi ortográfica aparte (*"strictly FRONTAL elevation view, camera perfectly level and centred, long lens, 135mm"*) y acota sobre ella — es además lo que pide el rol §4 (Toma 5 = frontal o perfil puro).

**5. Verifica el bbox mirando la imagen.** La detección por neutralidad **falla si el fondo bone tiene viñeteado** (las esquinas se vuelven neutras y estiran el contorno al borde del cuadro). Fallback: `warm<8 & luma<215` exigiendo ≥30 px por fila/columna, y pasar `--bbox x0,y0,x1,y1`. Nunca subir una cota sin haberla visto.

## Packshot de SET (conjunto de varias piezas) — lección 2026-07-28
Un set (sofá + 2 sillones + mesa) es **ancho y bajo**: en 1:1 deja fondo por encima de los respaldos y es **normal**. No intentes eliminarlo pidiendo un encuadre cerrado: probado en 4 fichas, el modelo acerca la cámara y **corta los dos sillones laterales** (y en un caso metió un tercer sillón parcial). En un packshot de conjunto el cliente tiene que **contar las piezas**, así que:
- **Prioridad: todas las piezas completas dentro del cuadro** > llenar el cuadro.
- La disposición en **U** ("U-shaped conversation layout") es la que mejor reparte el set en 1:1; el fondo bone sobrante es respiración de estudio, no aire muerto.
- El recorte en post **no** lo arregla: si el set ya ocupa ~90 % del ancho, no hay margen para recentrar sin amputar. Mídelo antes de gastar créditos.

## Reglas rectoras (el oficio)
- **Perfil de diseñador — el ambiente lo dicta el ESTILO (no solo el color):** lee el estilo del mueble (contemporáneo / rústico / clásico mediterráneo / industrial / boho) y ponlo en SU hábitat (contemporáneo→ático de diseño, microcemento/hormigón; rústico→caserío/madera; clásico med→cal/barro). El ambiente es **variable por producto**; la paleta y la temporada afinan la luz/consumible. Un choque de estilo (mueble moderno en caserío rústico) = "parece IA" → rechazo. Mapa completo: [`references/perfil-disenador-escena.md`](references/perfil-disenador-escena.md).
- **Ambiente vivido + ASMR sensorial (piezas únicas):** la escena debe sentirse **habitada** (signos de uso reciente: libro abierto, manta con caída natural, cojín con huella) y activar un sentido — **vapor** del café/té, textura del lino/lana, gotas de un vaso frío, calidez de la luz. Listón: *"parece que alguien vive aquí ahora"*. **Nunca** la pieza sola en un espacio vacío y perfecto.
- **Coherencia de la secuencia:** toda la galería de UN producto = el **mismo mundo/hábitat**; los ambientes A y B son variaciones (ángulo, momento, atrezzo) del mismo espacio, no mundos distintos. Decide el hábitat una vez y mantenlo.
- Vender a **toda España**; **nunca** resort tropical ni chalet de lujo.
- **Escala doble puerta (§13.bis):** métrica (factor 0,92–1,10; hombros ≤0,80 de un cojín; estatura 160–188 cm) **y** composición (máx 2 personas en sofá 3 plazas + ≥1 cojín libre). Si "lee personas grandes" → suele ser composición; mídelo lado a lado antes de concluir. Los ASMR sin personas esquivan el problema.
- **Temporadas (§14):** backbone ESTABLE todo el año (packshot + ASMR — son la `og:image`/Google) + capa de temporada ROTATIVA (el ambiente). Temporada activa: **Verano Costero** (Cantábrico/Levante). La pos-1 NO cambia entre temporadas.
- **Texturas — línea roja (§15):** en ASMR/detalle, **prohibido inventar tramas — y prohibido QUITARLAS**.
  El tapizado del Brandon lleva un **jacquard estampado tono sobre tono** y se publicó liso en 3 fichas: el
  modelo alisa lo estampado con la misma facilidad con la que inventa trama donde no la hay. Si el real
  lleva motivo, el prompt lo nombra; si es liso, lo niega. El macro extremo empuja al modelo a fabricar textura (sling fino → tweed inventado = rechazo). Anclar a la foto real, **escala moderada**, y preferir features reales (mecanismo, unión estructura↔tela, costura, nudo) a un macro de tejido.

## Detalle operativo (references)
- Mecánica MCP exacta + subida Shopify: [`references/runbook-mcp.md`](references/runbook-mcp.md)
- Prompt corto: compresión de la receta + ejemplos validados: [`references/prompt-recipe.md`](references/prompt-recipe.md)
- **Perfil de diseñador (estilo→espacio, ambiente vivido/ASMR, coherencia de secuencia): [`references/perfil-disenador-escena.md`](references/perfil-disenador-escena.md)**
- Escenas por región y temporada + emparejamiento de paleta: [`references/escenas-region-temporada.md`](references/escenas-region-temporada.md)
- Parámetros por toma y tipología (ángulos/focales/kelvin): rol §3–§5.

## Regla rectora final
Si dudas entre *más espectacular* y *más fiel* → gana **fiel**. El lujo de Santavila nace de la sombra y la textura bien resueltas, no de inventar el mueble.
