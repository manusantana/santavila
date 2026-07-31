---
name: santavila-imagen-producto
description: Úsalo al generar, crear, regenerar o mejorar imágenes o la galería de un producto de Santavila con Higgsfield — packshot, ambiente/lifestyle, ASMR/detalle, medidas; reemplazar fotos de baja resolución o productos con una sola foto; producir imágenes de catálogo, PDP o home de Santavila.
---

# Santavila · Imagen de producto — v4 (2026-07-31)

**Un producto cada vez. Cada imagen validada por el dueño. Cero invención.**

> **Qué cambia respecto a la v3.** La v3 se escribió sin haber leído entero el
> [`ROL_FOTOGRAFO_SENIOR.md`](../../docs/santavila/ROL_FOTOGRAFO_SENIOR.md) — 1.362 líneas que son la fuente
> real del oficio. Esta versión lo integra (escala, carriles de paleta, rotación de localizaciones, Master QA)
> y cierra las cuatro contradicciones que había entre ambos documentos con la decisión de Sergio del 31-07:
> **receta del 26-07 · solo manos, nunca cuerpo · macro de tejido prohibido · medidas solo con cota verificada.**

---

## LEY 0

> ### Si no existe, no lo hago. Si no sé hacerlo, no lo hago. Si no lo puedo verificar, no lo publico.

Una imagen de producto es **una afirmación sobre un objeto que alguien va a pagar**. Una textura inventada,
un tono desviado o una pieza que no existe son **datos falsos** sobre lo que el cliente recibirá en su casa.

**Ley 1 (del ROL §2), inviolable:** nunca se transforman geometría, silueta, proporciones, nº de
listones/lamas/cuerdas/cojines/plazas/módulos/patas, material y trama, acabado, color de variante, herrajes ni
remates. **Solo cambian** escena, suelo, fondo, atrezzo, luz, sombra, encuadre y resolución.

---

## PASO 0 · EL PRIMER COMANDO, SIEMPRE

```bash
python3 scripts/fuente_verdad_producto.py <handle>
```

Devuelve el **dato duro** del proveedor, no una interpretación:

| Campo | Para qué sirve |
|---|---|
| **SKU** | identifica el producto de verdad. El título de la ficha y el nombre de la carpeta **no identifican nada** |
| **producto** | nombre real del proveedor (BRANDON-3, CLOE, EVA PRO…) |
| **VARIANTE** | Balliu: "Chasis Blanco/Tablillas" vs "Chasis Blanco/Tela" — resuelve productos que parecen iguales |
| **foto real** | URL oficial del proveedor. **Es la referencia de todo el QA** |
| **galería** | el resto de fotos del proveedor: sirven para ver caras que la principal no muestra |
| **cotas** | ancho · fondo · alto REALES. Nunca se deducen de la foto |
| **descripción** | texto del proveedor: nombra materiales que la foto no aclara |
| **catálogo** | ficha técnica de Balliu 2025 |
| **cutout** | recorte de la pieza suelta. **CONOCIMIENTO, no se publica** (todos <800 px) |

**Si sale `*** NO HAY ***` en foto real → NO SE GENERA NADA para esa ficha.** Se anota y se pide el dato.
Hoy son 9 fichas ACTIVE. `--cobertura` las lista en cualquier momento.
**Si sale `*** NO HAY ***` en cotas → esa ficha no lleva imagen de medidas.** Hoy son 103.

> **Esto no es burocracia: es el paso que faltaba.** Sin él se publicó la galería del Albania en la ficha del
> Bellagio, y las balinesas y el parasol Roma se generaron sin ninguna referencia contra la que auditarlos.

---

## PASO 1 · FICHA DE VERDAD

Con el SKU, **abre la foto oficial a resolución nativa** (y las de la galería), recorta cada componente y
escribe en [`FICHAS_VERDAD.md`](../../docs/santavila/FICHAS_VERDAD.md):

| Componente | Qué anotar |
|---|---|
| **Chasis** | material · color exacto · acabado (mate/satinado/brillo) |
| **Tejido** | color · **¿liso o con motivo?** · ribete · costuras |
| **Tablero** | **material · tono · acabado · canto** — los cuatro, siempre |
| **Elementos** | cuerda, lamas, herrajes, toldo — **y si NO se ven, se escribe que no se ven** |
| **Piezas del lote** | qué entra y qué no (leer "Incluye:" + **todas** las filas del SKU en el Excel) |

**Lo que no se ve con certeza → `NO DETERMINADO` → esa toma NO se hace.** Nunca se deduce ni se interpreta.
La ficha queda con menos fotos y ninguna miente.

> **Ojo con las piezas del lote.** Un mismo SKU puede tener varias filas en el Excel (el 557-010884 lleva
> `BRANDON-7 SET SOFA 2 PLAZAS` **y** `LUNA-44 SET MESAS CENTRO`: las mesas entran en el lote). Y al revés:
> los reposapiés que salen en muchas fotos del proveedor **no** están incluidos. Quitar es seguro; añadir, nunca.

---

## PASO 2 · HÁBITAT Y ESCENA (antes de escribir un solo prompt)

Cuatro filtros, en este orden. Saltarse el orden es lo que produce el "parece IA".

**1 · Estilo → hábitat.** El error nº1 de "parece IA" no es la luz: es el **choque de estilos**. Lee el
carácter del mueble (líneas, material, lenguaje) y elige su tipo de espacio — contemporáneo → ático de
microcemento; rústico → caserío de piedra; clásico mediterráneo → cal y barro; industrial → loft.
Mapa: [`perfil-disenador-escena.md`](references/perfil-disenador-escena.md).

**2 · Eje térmico → CARRIL de paleta.** *(ROL §8 — la regla que más abarata una foto si se rompe)*

| Eje del producto | Carril | Entornos |
|---|---|---|
| Antracita · gris · azul apagado | **FRÍO / piedra** | atlántico-cantábrico, ático de hormigón, granito, caliza gris |
| Arena · beige · crudo · teca | **CÁLIDO / barro** | patio andaluz, tarima miel, gres arena, balear, jardín mediterráneo |
| Tórtola · greige · blanco roto · salvia | **camaleónico** | puente entre ambos, con luz y suelo desaturados |

**Prohibido el choque gratuito: un antracita JAMÁS va sobre barro naranja.** Se rota **dentro** del carril,
nunca cruzándolo. El entorno nunca gana al producto en saturación ni en temperatura.

**3 · Rotación de localización.** Consulta **siempre**
[`REGISTRO_LOCALIZACIONES.md`](../../docs/santavila/REGISTRO_LOCALIZACIONES.md) y elige del roster (ROL §11.1)
las **menos usadas** del carril. Dos productos no comparten set; coincidencia de 1 localización como mucho.
Rota también el **consumible**: dos fotos de la misma ficha nunca llevan la misma bebida+aperitivo, y no
siempre alcohol. Al terminar, **anota la fila nueva en el registro.**

**4 · Temporada activa.** *(ROL §14)* Hoy: **"Verano Costero"** (Cantábrico/Levante). Aporta luz, paleta y
consumible — no el hábitat. El packshot y los ASMR son **backbone estable**: no cambian por temporada.

---

## PASO 3 · LAS 5 IMÁGENES *(receta decidida por Sergio el 26-07, confirmada el 31-07)*

| # | Toma | Aspecto | Qué tiene que conseguir |
|---|---|---|---|
| 1 | **Packshot** limpio, fondo `bone #EEE8DA` | 1:1 | Fidelidad y conteo. **Nunca blanco puro.** 8–12% de aire por lado |
| 2 | **Ambiente EXTERIOR** | 1:1 | "cómo se ve en mi terraza". Producto ≥45% del cuadro |
| 3 | **Ambiente INTERIOR** — mismo hábitat, otro momento | 4:5 | "cómo se ve en mi porche/galería". Misma casa, distinta hora |
| 4 | **ASMR de material / FEATURE verificable** | 1:1 | Prueba de calidad. Costura, unión, herraje, canto — **nunca la trama** |
| 5 | **ASMR de consumible** — plano ABIERTO | 1:1 | Vida. La superficie que sostiene el atrezzo **es producto** |

**+ Medidas (overlay determinista, NO IA) solo si el Paso 0 dio cotas.** Sin cota verificada, no hay imagen.
Si la ficha da "72×75" sin desglosar → **se pregunta a Sergio**; en 3/4 tres centímetros son indistinguibles.

**Coherencia de secuencia:** las tomas 2 y 3 son el **mismo mundo**, un solo sol, un solo grade. La 1 y las
ASMR son neutras. Toda la ficha comparte dirección de luz y temperatura.

---

## PASO 4 · MECÁNICA HIGGSFIELD

1. `media_import_url(<URL oficial del SKU>)` → `media_id`
2. `generate_image({model:"nano_banana_pro", prompt:<CORTO>, medias:[{value:media_id, role:"image"}], aspect_ratio, resolution:"1k", count:2, get_cost:true})`
3. preflight → lanzar sin `get_cost` → `job_status(jobId, sync:true)`
4. QA (Paso 5) → validación de Sergio (Paso 6) → `upscale_image` a `4k`

- **Prompt CORTO en modo edición** (3–6 frases, inglés). Los largos **colapsan a blanco**.
- **Generar a `1k` SIEMPRE.** Pedir 2k/4k en generación da imagen vacía (std de píxeles ~15 = vacía, ~60 = real).
  *(El ROL §7.4 dice `4k`: está desactualizado, se verificó empíricamente en la Fase 0.)*
- **Describe la FÍSICA** (hora, dirección y dureza del sol, material, distancia de cámara). Nunca "8k, ultrarrealista".
- **Nombra material Y FORMA, y niega lo que el modelo inventa:**
  *"ROUND nesting tables, round never rectangular"* · *"FLAT SMOOTH GREY HPL — not stone, not travertine, no grain"*.
- **Óptica que no miente:** 70–105 mm en packshot y detalle, 35–50 mm en ambiente desde >2 m. **Cero gran
  angular** — es la causa nº1 del "mueble de juguete en paisaje enorme".
- **8 jobs concurrentes** máximo. Los créditos se descuentan **al encolar**: si la cola se para, **NO reencolar**.
  Coste real: **~34 créditos por galería** con regeneraciones incluidas.

Detalle: [`runbook-mcp.md`](references/runbook-mcp.md) · [`prompt-recipe.md`](references/prompt-recipe.md)

---

## PASO 5 · QA — falla un bloqueante, se regenera

Todo **contra la foto oficial del proveedor**, nunca contra el packshot propio. Lista larga:
[`qa-checklist.md`](references/qa-checklist.md) y ROL §12.

**A · Fidelidad (tolerancia cero)** — conteo 1:1 de listones/cojines/plazas/patas · material y trama reales ·
color de variante ΔE≤3 (antracita no se aplasta a negro, tórtola no vira a rosa, blanco no amarillea) ·
herrajes respetados · verticales a plomo · **SKU correcto**.

**B · Física de luz** — un solo sol · sombra de contacto bajo **cada** apoyo (si flota, rechazo) · sombra
proyectada al lado opuesto, nunca hacia cámara · sombra coloreada, negros al ink `#23251D` nunca `#000` ·
sin HDR falso · microtextura sin denoise plástico.

**C · Escala — línea roja del dueño** *(ROL §13.bis)*. Sin cuerpo entero, la escala se ancla en objetos:

| Ancla | Cota real |
|---|---|
| Mano humana | **18 cm** — obligatoria en ASMR con manos |
| Taza de cerámica | 8 cm Ø |
| Copa de vino | 22 cm alto |
| Libro abierto | 30 cm |
| Cojín de asiento | 45–60 cm |

Producto **≥78% del ancho** en packshot, **≥45%** en ambiente (nunca <30%). Plano de cierre sólido a 2–5 m
detrás; sin fuga al infinito. Cielo ≤25%. **Mano gigante o taza desproporcionada invalida el ASMR aunque la
textura sea perfecta.**

**D · Lógica de la escena (tells de IA)** — cada bebida con dueño y **junto a él**, nunca en el lado opuesto ·
nada de props duplicados sin dueño · **escena sin personas = escena EN REPOSO**: cojines mullidos y lisos, sin
vapor, sin huella de cuerpo (el vapor implica que alguien está ahí ahora).

**E · On-brand** — NO resort tropical, NO chalet imposible · fondo bone nunca blanco puro · ≤5 props ·
0 logos, 0 watermark, 0 texto de IA · no sugerir montaje nuestro (self-assembly).

**F · Técnico** — ≥2000 px (objetivo 2400) · cover en producto · sin amputar patas ni brazos en el 1:1.

---

## PASO 6 · VALIDACIÓN IMAGEN A IMAGEN (el paso que no se salta)

Por **cada** imagen, antes de subir nada:

1. **Montar el comparador**: recorte de la foto oficial a resolución nativa **junto a** la generada.
2. **Presentarla a Sergio** afirmando explícitamente qué se ha verificado:
   > *"Packshot. Tablero HPL gris cemento mate, canto fino enrasado — igual que el real. Jacquard presente.
   > Conteo 1 sofá + 2 sillones + 2 mesas. Sin reposapiés."*
3. **Esperar su "ok" por imagen.** No hay aprobación implícita ni por lote.
4. Si algo no se puede afirmar mirando el píxel → **no se afirma y no se aprueba**.

**El pipeline termina en "listo para revisar", nunca en "publicado". Una ficha cada vez. Sin tandas.**

---

## PASO 7 · PUBLICAR Y VERIFICAR

Solo con el "ok" de todas. `scripts/publicar_galeria_producto.py` (dry-run por defecto, `--apply`).
Verificar: `ACTIVE · READY · ≥2000 px · pos 0 = packshot · 0 alt vacíos`.
**Orden correcto: borrar la foto antigua primero, reponer después** — al revés se borró lo que se acababa de subir.

---

## LO PROHIBIDO — cada línea es un fallo que ya se publicó

| Prohibido | Qué pasó |
|---|---|
| **Macro de tejido** | A escala macro el modelo **fabrica** la trama. 3 ASMR con jacquard inventado. El detalle de tela solo como **feature**: costura, ribete, unión tela-estructura, herraje, nudo |
| **Inventar lo que no se ve** | Los grilletes del balancín no aparecen en la foto real. Se inventó **el detalle donde el cliente juzga la calidad** |
| **Quitar una trama que existe** | El jacquard del Brandon publicado **liso** en 3 fichas. La línea roja va en **los dos sentidos** |
| **Cambiar material, tono, acabado o canto** | HPL gris cemento → piedra caliza → gris claro brillante. **El tablero es producto, no bodegón** |
| **Mezclar variantes en la ficha** | La Java con principal blanca y secuencia gris: son **dos productos** |
| **Cruzar de carril de paleta** | Gris frío al atardecer vira a beige y el aluminio a bronce |
| **Cuerpo entero de una persona** | Solo manos y consumibles. El cuerpo entero abre la doble puerta de escala donde ya fallamos (Cantabria) |
| **Piezas fantasma** | Reposapiés o mesas que salen en la foto pero **no entran en el lote** |
| **QA contra el packshot propio** | Si el packshot está mal, arrastra el error a las 5. **Siempre contra la foto oficial** |
| **Cota deducida de la imagen** | El bbox medido a ojo dejó la cota 663 px corta. Contorno automático o no se dibuja |

---

## Herramientas

| Script | Para qué |
|---|---|
| `scripts/fuente_verdad_producto.py <handle>` | **PASO 0.** SKU, variante, foto oficial, galería, cotas, descripción, catálogo |
| `scripts/fuente_verdad_producto.py --cobertura` | qué fichas se pueden trabajar y cuáles no |
| `scripts/auditar_fotos_duplicadas.py` | fichas que comparten foto principal (huella perceptual) |
| `scripts/publicar_galeria_producto.py` | publicar (dry-run por defecto; `--apply`) |
| `scripts/overlay_medidas_producto.py` | cotas deterministas, **NO IA**, solo con medidas del PASO 0 |

## Contexto obligatorio antes de empezar
[`ROL_FOTOGRAFO_SENIOR.md`](../../docs/santavila/ROL_FOTOGRAFO_SENIOR.md) (el oficio: §8 paleta · §11 roster ·
§12 Master QA · §13 escala) · [`LECCIONES_FIDELIDAD.md`](../../docs/santavila/LECCIONES_FIDELIDAD.md) ·
[`REFLEXION_2026-07-30.md`](../../docs/santavila/REFLEXION_2026-07-30.md) ·
[`REGISTRO_LOCALIZACIONES.md`](../../docs/santavila/REGISTRO_LOCALIZACIONES.md)

## Regla final
Si dudas entre **más espectacular** y **más fiel** → gana **fiel**.
Si dudas entre **publicar** y **preguntar** → gana **preguntar**.
