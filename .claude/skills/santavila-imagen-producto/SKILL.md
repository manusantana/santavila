---
name: santavila-imagen-producto
description: Úsalo al generar, crear, regenerar o mejorar imágenes o la galería de un producto de Santavila con Higgsfield — packshot, ambiente/lifestyle, ASMR/detalle, medidas; reemplazar fotos de baja resolución o productos con una sola foto; producir imágenes de catálogo, PDP o home de Santavila.
---

# Santavila · Imagen de producto (v2 · reescrito 2026-07-30)

> **Por qué existe la v2.** La v1 produjo imágenes que **cambiaban el producto**: un tablero HPL convertido
> en piedra, un jacquard inventado en tres fichas, un herraje que no existe, la galería de un producto en la
> ficha de otro. El dueño tuvo que detectar cuatro de esos fallos. La v1 no fallaba por falta de reglas —
> tenía muchas — sino porque **las reglas no eran puertas: eran consejos que yo mismo me saltaba al acelerar**.
> La v2 convierte cada regla en una puerta, y **termina en "listo para revisar", nunca en "publicado"**.
> (La v1 se conserva en `SKILL_v1_archivo.md` solo como registro histórico.)

---

## LEY 0 · La frase que manda sobre todo lo demás

> ### Si no existe, no lo hago. Si no sé hacerlo, no lo hago. Si no lo puedo verificar, no lo publico.

Una imagen de producto es **una afirmación sobre un objeto que alguien va a pagar**. Una textura inventada,
un tono desviado o una pieza que no existe no son licencia creativa: son **datos falsos** sobre lo que el
cliente recibirá en su casa.

**Lectura obligatoria antes de empezar:**
[`LECCIONES_FIDELIDAD.md`](../../docs/santavila/LECCIONES_FIDELIDAD.md) ·
[`REFLEXION_2026-07-30.md`](../../docs/santavila/REFLEXION_2026-07-30.md)

---

## Las 6 imágenes de una ficha

| # | Toma | Aspecto | Fuente |
|---|---|---|---|
| 1 | **Packshot** limpio, fondo `bone` | 1:1 | generada |
| 2 | **Ambiente exterior** | 1:1 | generada |
| 3 | **Ambiente interior** (mismo hábitat, otro momento) | 4:5 | generada |
| 4 | **Detalle de FEATURE verificable** | 1:1 | generada |
| 5 | **ASMR de consumible** — plano ABIERTO | 1:1 | generada |
| 6 | **FOTO REAL DEL PROVEEDOR** — cierra la galería | original | **nunca se borra** |

**La foto 6 es innegociable.** Es la red de seguridad: si algo generado se desvía, el cliente tiene la
referencia verdadera en la misma ficha. **El script de publicación NO borra la original: la reordena al final.**

---

## Las 5 PUERTAS (no se salta ninguna)

### PUERTA 1 · FICHA DE VERDAD — sin ficha no se genera nada
Abre la foto real a **resolución nativa**, recorta cada componente y escribe lo que ves en
[`FICHAS_VERDAD.md`](../../docs/santavila/FICHAS_VERDAD.md):

| Componente | Qué anotar |
|---|---|
| **Chasis** | material · color exacto · acabado (mate/brillo) |
| **Tejido** | color · ¿liso o con motivo? · ribete |
| **Tablero** | material · **tono** · **acabado** · **canto** (los cuatro) |
| **Elementos** | cuerda, lamas, herrajes, toldo — y **si NO se ven, se anota que no se ven** |
| **Piezas NO incluidas** | reposapiés o mesas que salen en la foto pero no en el lote (leer "Incluye:") |

- **Sin fila en esa tabla, no se lanza ni un job.**
- **Lo que no se ve con certeza se marca `NO DETERMINADO`** y **la toma donde ese elemento sería protagonista
  NO se hace**. La ficha queda con menos fotos y ninguna miente. Nunca se deduce ni se interpreta.

### PUERTA 2 · IDENTIDAD — ¿es este el producto de esta ficha?
Compara tu packshot con **la foto real DEL HANDLE DESTINO**. Si no es el mismo mueble (tipo de brazo,
estructura, color de chasis y tejido), **no se publica**.
El nombre de la carpeta **no identifica nada**: se publicó la galería del Albania en la ficha del Bellagio
3 pl. (3.449 €) por dar por bueno un nombre de carpeta.

### PUERTA 3 · QA CONTRA LA FICHA, nunca contra el packshot propio
El packshot también puede estar mal, y si lo está **arrastra el error a las 6 imágenes**. La corrección de la
mesa falló dos veces por comparar contra mi propio packshot.
Se compara **siempre contra la foto del proveedor a resolución nativa**.

### PUERTA 4 · VALIDACIÓN HUMANA — imagen a imagen
**Se presenta cada imagen con el recorte de la foto real al lado. El dueño aprueba una a una.**
Nada se sube sin su "ok" explícito **por imagen**. **Una ficha cada vez. Sin tandas.**

### PUERTA 5 · VERIFICACIÓN TÉCNICA tras publicar
ACTIVE · 6 media · READY · ≥2000 px · pos 0 = packshot · última = foto real · 0 alt vacíos.

---

## LO PROHIBIDO (cada línea es un fallo que ya se publicó)

| Prohibido | Qué pasó |
|---|---|
| **Macro de tejido** | A escala macro el modelo **fabrica** la trama, no la copia. 3 ASMR con jacquard inventado. El detalle de tela solo como **feature**: costura, ribete, unión tela-estructura, herraje, nudo |
| **Inventar una pieza que no se ve** | Los grilletes del balancín: en la foto real el punto de suspensión no se ve. Se inventó **el detalle en el que el cliente juzga la calidad** |
| **Quitar una trama que existe** | El jacquard del Brandon publicado **liso** en 3 fichas. La línea roja va en **los dos sentidos** |
| **Cambiar material, tono, acabado o canto de una superficie** | HPL gris cemento → piedra caliza → gris claro brillante. **El tablero es producto, no bodegón** |
| **Mezclar variantes en la ficha** | La Java con principal **blanca** y secuencia **gris**: son dos productos |
| **Gris frío bajo luz de atardecer** | Vira a beige dorado y el aluminio a bronce. Es **incompatibilidad de paleta**: gris frío → luz neutra o del norte, 5400 K |
| **Personas** | Nunca. La escena vive por los signos de uso, no por gente |
| **Piezas fantasma** | Reposapiés y mesas que salen en la foto del proveedor pero **no entran en el lote** |

---

## Cómo se compone cada toma

**Referencia visual: Kave Home exteriores** — español, mediterráneo contemporáneo, luz natural franca,
espacios reales habitados. Ni resort tropical ni chalet de lujo.

- **Hábitat: uno propio por ficha**, nunca repetido. Consultar
  [`REGISTRO_LOCALIZACIONES.md`](../../docs/santavila/REGISTRO_LOCALIZACIONES.md) antes de elegir.
- **El ambiente lo dicta el ESTILO del mueble**, no solo el color: contemporáneo → ático de diseño,
  microcemento; rústico → caserío, madera; clásico mediterráneo → cal y barro. Un choque de estilo lee
  "IA" y se rechaza.
- **Escena vivida**: manta con caída natural, libro abierto, vaso servido, vapor. Nunca la pieza sola en un
  espacio vacío y perfecto.
- **Adecuación por tipología**: una silla de comedor va a una mesa puesta; una tumbona junto al agua; un
  parasol dando sombra sobre algo; un balancín en un porche. El sitio donde ese mueble **existiría de verdad**.
- **Toma 5 · ASMR de consumible con PLANO ABIERTO**: la mesa entera en cuadro, con su canto y sus patas, para
  que el material sea comparable con la foto real. El macro cerrado del tablero produjo la piedra caliza.

---

## Mecánica Higgsfield

1. `media_import_url(<URL CDN de la foto real>)` -> `media_id`
2. `generate_image({model:"nano_banana_pro", prompt:<CORTO>, medias:[{value:media_id, role:"image"}], aspect_ratio, resolution:"1k"})`
3. `job_status(jobId, sync:true)` -> 4. QA -> 5. `upscale_image` a `4k`

- **Prompt CORTO en modo edición** (3-6 frases, inglés). Los prompts largos colapsan a blanco.
- **Generar SIEMPRE a `1k`** y subir con `upscale_image`. Pedir 2k/4k en generación da imagen vacía.
- **Describe la FÍSICA** (hora, dirección y dureza del sol, material, distancia de cámara), nunca adjetivos
  de calidad ("8k, ultrarrealista").
- **Nombra el material Y niega el que el modelo inventa**:
  *"the table top is FLAT SMOOTH GREY HPL — not stone, not travertine, not wood, no grain"*.
- Límite del plan: **8 jobs concurrentes**. Los créditos se descuentan **al encolar**: si la cola se para,
  **NO reencolar** — esperar y recoger.
- Coste: 2 créditos/imagen + 2/upscale.

---

## Detalle operativo
- Runbook MCP y subida a Shopify: [`references/runbook-mcp.md`](references/runbook-mcp.md)
- Prompt corto y ejemplos validados: [`references/prompt-recipe.md`](references/prompt-recipe.md)
- Estilo -> espacio: [`references/perfil-disenador-escena.md`](references/perfil-disenador-escena.md)
- Escenas por región y temporada: [`references/escenas-region-temporada.md`](references/escenas-region-temporada.md)
- QA detallado y "tells" de IA: [`references/qa-checklist.md`](references/qa-checklist.md)
- Auditoría de fotos duplicadas del catálogo: `scripts/auditar_fotos_duplicadas.py`

## Regla final
Si dudas entre **más espectacular** y **más fiel** -> gana **fiel**.
Si dudas entre **publicar** y **preguntar** -> gana **preguntar**.
