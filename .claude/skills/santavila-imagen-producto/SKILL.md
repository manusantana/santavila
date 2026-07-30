---
name: santavila-imagen-producto
description: Úsalo al generar, crear, regenerar o mejorar imágenes o la galería de un producto de Santavila con Higgsfield — packshot, ambiente/lifestyle, ASMR/detalle, medidas; reemplazar fotos de baja resolución o productos con una sola foto; producir imágenes de catálogo, PDP o home de Santavila.
---

# Santavila · Imagen de producto — v3 DEFINITIVO (2026-07-30)

**Un producto cada vez. Cada imagen validada por el dueño. Cero invención.**

---

## LEY 0

> ### Si no existe, no lo hago. Si no sé hacerlo, no lo hago. Si no lo puedo verificar, no lo publico.

Una imagen de producto es **una afirmación sobre un objeto que alguien va a pagar**. Una textura inventada,
un tono desviado o una pieza que no existe son **datos falsos** sobre lo que el cliente recibirá en su casa.

---

## PASO 0 · EL PRIMER COMANDO, SIEMPRE

```bash
python3 scripts/fuente_verdad_producto.py <handle>
```

Devuelve el **dato duro** del proveedor, no una interpretación:

| Campo | Para qué sirve |
|---|---|
| **SKU** | identifica el producto de verdad. El título de la ficha y el nombre de la carpeta **no identifican nada** |
| **producto** | nombre real del proveedor (BRANDON-3, CLOE, LUNA-44…) |
| **variante** | Balliu: "Chasis Blanco/Tablillas" vs "Chasis Blanco/Tela" — resuelve productos que parecen iguales |
| **foto real** | URL oficial del proveedor. **Es la referencia de todo el QA** |
| **cotas** | ancho · fondo · alto REALES. Nunca se deducen de la foto |

**Si el handle no aparece → no se genera nada.** Se anota y se pide el dato.

> **Esto no es burocracia: es el paso que faltaba.** Sin él se publicó la galería del Albania en la ficha del
> Bellagio, y se dejaron de dibujar cotas que estaban en el repo desde el principio (el "220×69" era
> ancho 220 · fondo 64 · **alto 69**).

Fuentes que consolida: `Santavila.xlsx` (hojas Hevea/Balliu) · `proveedores_raw/hevea/*.csv` ·
`proveedores_raw/balliu/_sku_mapping.json`.

---

## PASO 1 · FICHA DE VERDAD

Con el SKU en la mano, **abre la foto oficial a resolución nativa**, recorta cada componente y escribe en
[`FICHAS_VERDAD.md`](../../docs/santavila/FICHAS_VERDAD.md):

| Componente | Qué anotar |
|---|---|
| **Chasis** | material · color exacto · acabado (mate/brillo) |
| **Tejido** | color · **¿liso o con motivo?** · ribete |
| **Tablero** | **material · tono · acabado · canto** — los cuatro, siempre |
| **Elementos** | cuerda, lamas, herrajes, toldo — **y si NO se ven, se escribe que no se ven** |
| **Piezas del lote** | qué entra y qué no (leer "Incluye:" + las filas del SKU en el Excel) |

**Lo que no se ve con certeza → `NO DETERMINADO` → esa toma NO se hace.** Nunca se deduce ni se interpreta.
La ficha queda con menos fotos y ninguna miente.

---

## PASO 2 · LAS 6 IMÁGENES

| # | Toma | Aspecto | Fuente |
|---|---|---|---|
| 1 | **Packshot** limpio, fondo `bone` | 1:1 | generada |
| 2 | **Ambiente exterior** | 1:1 | generada |
| 3 | **Ambiente interior** — mismo hábitat, otro momento | 4:5 | generada |
| 4 | **Detalle de FEATURE verificable** | 1:1 | generada |
| 5 | **ASMR de consumible** — plano ABIERTO, la mesa entera en cuadro | 1:1 | generada |
| 6 | **FOTO OFICIAL DEL PROVEEDOR** — cierra la galería | del SKU | **nunca se borra** |

**La 6 es innegociable**: si algo generado se desvía, el cliente tiene la referencia verdadera en la ficha.

---

## PASO 3 · VALIDACIÓN IMAGEN A IMAGEN (el paso que no se salta)

Por **cada** imagen generada, y antes de subir nada:

1. **Montar el comparador**: recorte de la foto oficial a resolución nativa **junto a** la imagen generada.
2. **Presentarla al dueño** con la afirmación explícita de qué se ha verificado:
   > *"Packshot. Tablero HPL gris cemento mate, canto fino enrasado — igual que el real. Jacquard presente.
   > Conteo 1 sofá + 2 sillones + 2 mesas. Sin reposapiés."*
3. **Esperar su "ok" por imagen.** No hay aprobación implícita ni por lote.
4. Si algo no se puede afirmar mirando el píxel → **no se afirma y no se aprueba**.

**El pipeline termina en "listo para revisar", nunca en "publicado".
Una ficha cada vez. Sin tandas.**

---

## PASO 4 · PUBLICAR Y VERIFICAR

Solo con el "ok" de todas las imágenes. Después:
`ACTIVE · 6 media · READY · ≥2000 px · pos 0 = packshot · última = foto oficial · 0 alt vacíos`

---

## LO PROHIBIDO — cada línea es un fallo que ya se publicó

| Prohibido | Qué pasó |
|---|---|
| **Macro de tejido** | A escala macro el modelo **fabrica** la trama. 3 ASMR con jacquard inventado. El detalle de tela solo como **feature**: costura, ribete, unión tela-estructura, herraje, nudo |
| **Inventar lo que no se ve** | Los grilletes del balancín no aparecen en la foto real. Se inventó **el detalle donde el cliente juzga la calidad** |
| **Quitar una trama que existe** | El jacquard del Brandon publicado **liso** en 3 fichas. La línea roja va en **los dos sentidos** |
| **Cambiar material, tono, acabado o canto** | HPL gris cemento → piedra caliza → gris claro brillante. **El tablero es producto, no bodegón** |
| **Mezclar variantes en la ficha** | La Java con principal blanca y secuencia gris: son **dos productos** |
| **Gris frío al atardecer** | Vira a beige y el aluminio a bronce. **Incompatibilidad de paleta**: gris frío → luz neutra/norte, 5400 K |
| **Personas** | Nunca. La escena vive por los signos de uso |
| **Piezas fantasma** | Reposapiés o mesas que salen en la foto pero **no entran en el lote** (comprobar en el Excel) |
| **QA contra el packshot propio** | Si el packshot está mal, arrastra el error a las 6. **Siempre contra la foto oficial** |

---

## Cómo se compone cada toma

**Referencia: Kave Home exteriores** — español, mediterráneo contemporáneo, luz natural franca, espacios
reales habitados. Ni resort tropical ni chalet de lujo.

- **Un hábitat propio por ficha**, nunca repetido → [`REGISTRO_LOCALIZACIONES.md`](../../docs/santavila/REGISTRO_LOCALIZACIONES.md)
- **El ambiente lo dicta el ESTILO**: contemporáneo → ático de microcemento; rústico → caserío;
  clásico mediterráneo → cal y barro. Un choque de estilo lee "IA" y se rechaza.
- **Adecuación por tipología**: la silla de comedor a una mesa puesta; la tumbona junto al agua; el parasol
  dando sombra sobre algo; el balancín en un porche. **Donde ese mueble existiría de verdad.**
- **Escena vivida**: manta con caída natural, libro abierto, vaso servido, vapor. Nunca la pieza sola en un
  espacio vacío y perfecto.
- **Luz según paleta**: gris frío → neutra/norte 5400 K · tórtola, crudo, arena, cal → cálida, atardecer OK.

---

## Mecánica Higgsfield

1. `media_import_url(<URL oficial del SKU>)` → `media_id`
2. `generate_image({model:"nano_banana_pro", prompt:<CORTO>, medias:[{value:media_id, role:"image"}], aspect_ratio, resolution:"1k"})`
3. `job_status(jobId, sync:true)` → 4. comparador + validación → 5. `upscale_image` a `4k`

- **Prompt CORTO en modo edición** (3-6 frases, inglés). Los largos colapsan a blanco.
- **Generar a `1k` SIEMPRE** y subir con `upscale_image`. Pedir 2k/4k en generación da imagen vacía.
- **Describe la FÍSICA** (hora, dirección y dureza del sol, material, distancia de cámara). Nunca "8k,
  ultrarrealista".
- **Nombra el material Y niega lo que el modelo inventa**:
  *"the table top is FLAT SMOOTH GREY HPL — not stone, not travertine, not wood, no grain"*.
- **8 jobs concurrentes** máximo. Los créditos se descuentan **al encolar**: si la cola se para,
  **NO reencolar** — esperar y recoger. Coste: 2 créditos/imagen + 2/upscale.

---

## Herramientas del proyecto

| Script | Para qué |
|---|---|
| `scripts/fuente_verdad_producto.py <handle>` | **PASO 0.** SKU, producto, variante, foto oficial, cotas |
| `scripts/auditar_fotos_duplicadas.py` | fichas que comparten foto principal (huella perceptual) |
| `scripts/publicar_galeria_producto.py` | publicar (dry-run por defecto; `--apply` para subir) |
| `scripts/overlay_medidas_producto.py` | cotas deterministas, **NO IA**, solo con medidas del PASO 0 |

## Contexto obligatorio antes de empezar
[`LECCIONES_FIDELIDAD.md`](../../docs/santavila/LECCIONES_FIDELIDAD.md) ·
[`REFLEXION_2026-07-30.md`](../../docs/santavila/REFLEXION_2026-07-30.md) ·
[`AUDITORIA_CATALOGO_FOTOS.md`](../../docs/santavila/AUDITORIA_CATALOGO_FOTOS.md)

## Regla final
Si dudas entre **más espectacular** y **más fiel** → gana **fiel**.
Si dudas entre **publicar** y **preguntar** → gana **preguntar**.
