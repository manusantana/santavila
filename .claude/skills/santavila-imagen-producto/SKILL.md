---
name: santavila-imagen-producto
description: Úsalo al generar, crear, regenerar o mejorar imágenes o la galería de un producto de Santavila con Higgsfield — packshot, ambiente/lifestyle, ASMR/detalle, medidas; reemplazar fotos de baja resolución o productos con una sola foto; producir imágenes de catálogo, PDP o home de Santavila.
---

# Santavila · Imagen de producto — v5 (2026-08-20)

**Un producto cada vez. Cada imagen validada por el dueño. Cero invención.**

> **Qué cambia respecto a la v4 — la lección del 20-08.** Publiqué una galería que pasaba todas las métricas
> y que Sergio describió como *"horrible"*, sustituyendo unas fotos suyas que ya eran buenas. Habían dejado de
> ser fotografías: eran **collages**. De ahí salen los tres bloques nuevos de este documento —
> [las tres promesas](#paso-5bis--las-tres-promesas-lo-que-la-foto-tiene-que-cumplir),
> el [test de collage](#i--test-de-collage--la-foto-tiene-que-ser-una-foto-bloqueante) y la
> [prohibición del método A1](#método-a1--por-qué-ya-no-se-usa) — y la regla que gobierna todas:
> **una métrica puede rechazar una imagen; ninguna métrica puede aceptarla.**

> **Qué cambia respecto a la v3.** La v3 se escribió sin haber leído entero el
> [`ROL_FOTOGRAFO_SENIOR.md`](../../docs/santavila/ROL_FOTOGRAFO_SENIOR.md), que es la fuente
> real del oficio. Esta versión lo integra (escala, carriles de paleta, rotación de localizaciones, Master QA)
> y cierra las cuatro contradicciones que había entre ambos documentos con la decisión de Sergio del 31-07:
> **receta del 26-07 · solo manos, nunca cuerpo · macro de tejido prohibido · medidas solo con cota verificada.**

---

## LEY 0

> ### Si no existe, no lo hago. Si no sé hacerlo, no lo hago. Si no lo puedo verificar, no lo publico.

Una imagen de producto es **una afirmación sobre un objeto que alguien va a pagar**. Una textura inventada,
un tono desviado o una pieza que no existe son **datos falsos** sobre lo que el cliente recibirá en su casa.

> ### Una métrica RECHAZA. Nunca ACEPTA. *(20-08-2026)*
> Los números —ΔE, R−B, px/cm, conteo— existen para **tumbar** una imagen deprisa y sin discutir. En cuanto
> uno de ellos se convierte en el motivo por el que una imagen se aprueba, se ha dejado de mirar la fotografía.
> Así se publicaron cinco collages con el color del tejido exacto. **Ninguna imagen entra en la ficha porque
> haya pasado una medición: entra porque, mirada entera y a tamaño real, es una fotografía.**

**Ley 1 (del ROL §2), inviolable:** nunca se transforman geometría, silueta, proporciones, nº de
listones/lamas/cuerdas/cojines/plazas/módulos/patas, material y trama, acabado, color de variante, herrajes ni
remates. **Solo cambian** escena, suelo, fondo, atrezzo, luz, sombra, encuadre y resolución.

---

## LEY DEL AUDITOR — antes que el Paso 0

> **Sergio, 20-08-2026:** *"esto hemos pasado mil veces y no puede ser que tengamos aún errores así
> y tengamos que volver atrás."*

Tenía razón, y la causa no era el descuido. Era que **una imagen publicada no dejaba rastro de qué
se le verificó**, así que cada criterio nuevo obligaba a abrir las fichas ya publicadas y mirarlas a
ojo. De ahí el bucle de *"déjame comprobar una cosa antes de seguir"*.

> ### Un criterio que no está en el auditor no existe.
> Cuando descubras un criterio nuevo: **primero lo programas en `scripts/auditar_galerias.py` y lo
> pasas sobre las 171 fichas activas. Después** sigues con la ficha que tenías entre manos.

**Las dos herramientas:**
- `python3 scripts/auditar_galerias.py [--json]` — recorre lo publicado y aplica todos los criterios
  objetivos: sin imagen · una sola imagen · duplicadas dentro de la ficha · alt vacío · <2000 px ·
  media que no llegó a READY · foto compartida con otra ficha.
- `docs/santavila/_verificaciones.json` — lo escribe el publicador solo: qué fichero, cuántos
  píxeles, cuántos megapíxeles y qué largo tiene el alt, ficha por ficha y con fecha.

**Prohibido** volver a mirar una ficha publicada "por si acaso" sin haber pasado antes el auditor.
Si el auditor no lo detecta, es que le falta ese criterio: se le añade.

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

### Las tres puertas del Paso 0

**1 · Sin foto → no se genera nada.** Si sale `*** NO HAY ***` en foto real, esa ficha está bloqueada.
**Antes de darla por bloqueada, búscala de verdad**: `images_optimized/`, `images_balliu/`, el CDN de Shopify,
por SKU y por `balliu_slug`. *(Un export ya dio una foto equivocada por buena y se declaró "no verificable" algo
que estaba en el repo.)* Si tampoco aparece, se anota en `PENDIENTES_PROVEEDOR.md` y se pide.

**2 · ⚠️ Foto COMPARTIDA → no identifica la variante → se pregunta a Sergio.** Si el Paso 0 avisa de que la
foto la comparten varias fichas, **esa foto no prueba que sea este producto**. Se marca `NO DETERMINADO` y se
confirma antes de gastar un crédito.

> **El caso que lo demuestra:** la ficha `Mesa exterior HPL 70×70` (SKU **SOFIA**) trae como foto oficial
> `Balliu_MesaCentral-**Etna**_blanco.jpg`, compartida con **otras 9 mesas de medidas distintas**. Se puede
> generar una galería impecablemente fiel… a la mesa equivocada. Es el fallo A0 del Bellagio, pero en origen.

**3 · Sin cotas → esa ficha no lleva imagen de medidas.** Nunca se deduce una medida de la foto.

> **Las cifras vivas salen de `--cobertura`, no de este documento.** El comando avisa de la antigüedad del
> snapshot (`_estado_imagenes.json`); si tiene más de dos semanas, refréscalo antes de fiarte.
> Orden de magnitud a fecha del último snapshot: ~9 fichas sin foto, ~32 con foto compartida, ~103 sin cotas.

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
Rota también el **atrezzo**. Al terminar, **anota la fila nueva en el registro.**

> ### ⛔ VERACIDAD DEL LUGAR — un español tiene que reconocer SU tierra
> Decir "Cantabria" en el prompt no basta: el modelo tira al norte de Europa genérico, que es lo que más ha
> visto. **Una localización que un local no reconoce es peor que no localizar**, porque delata el montaje.
>
> **Nombra la ARQUITECTURA concreta, no solo la región.** Antes de generar, escribe qué elemento hace que ese
> sitio sea inconfundiblemente español, y ponlo en el prompt con nombre propio:
>
> | Región | Lo que la identifica de verdad | Lo que el modelo pone si no se lo dices |
> |---|---|---|
> | Cantabria / Asturias | **galería acristalada de fachada**: mirador vertical de carpintería blanca de madera, adosado al muro, **sin techo de cristal**; casona de sillería y mampostería | *conservatory* victoriano inglés con techo de cristal a dos aguas |
> | Galicia | granito, hórreo, mampostería de sillar | cottage irlandés de piedra redondeada |
> | Andalucía | patio encalado, olambrilla, celosía, reja de forja | riad marroquí |
> | Levante / Baleares | porxada de vigas de sabina, marés, cañizo | villa griega de Santorini |
>
> **Verificación:** mira la imagen y pregúntate *"¿esto está en España o podría estar en Cornualles?"*
> Si un muro de piedra con musgo, un prado verde y un mar gris valen igual para Irlanda, **no has localizado nada**.

**4 · Temporada activa.** *(ROL §14)* Hoy: **"Verano Costero"** (Cantábrico/Levante). Aporta luz, paleta y
atrezzo — no el hábitat. El packshot y los ASMR son **backbone estable**: no cambian por temporada.

> ### ⛔ LA ESCENA VA EN LA ESTACIÓN EN QUE SE VENDE (Sergio, 04-08)
> *"Ahora mismo estamos en verano, estamos ofreciendo verano. No me pongas algo que está lloviendo."*
> Una terraza mojada en agosto no vende una terraza: **vende el mes en que no se usa.**
>
> | En temporada de VERANO — prohibido | Lo que sí |
> |---|---|
> | Lluvia, gotas en el cristal, suelo mojado, charcos | Suelo **seco** |
> | **Hojas secas caídas** (leen a otoño) | Sombra moteada, alguna flor, polvo fino |
> | Cielo plomizo cerrado, luz de día gris | Cielo **claro** aunque velado; luz suave pero **de verano** |
> | Mantas de lana gruesa, ropa de abrigo | Lino, algodón fino, plaid ligero |
>
> **Norte ≠ lluvia.** El Cantábrico en agosto tiene **luz difusa y suave con cielo claro** — eso da el carril
> frío que pide un antracita **sin** convertir la foto en noviembre. Confundir "luz del norte" con "día de
> lluvia" es el error que se coló en el Brandon.
>
> **Comprobación antes de generar:** ¿en qué mes se va a vender esto? La escena tiene que ser de ese mes.

---

## PASO 3 · LAS 5 IMÁGENES *(receta decidida por Sergio el 26-07, confirmada el 31-07)*

| # | Toma | Aspecto | Qué tiene que conseguir |
|---|---|---|---|
| 1 | **Packshot** limpio, fondo `bone #EEE8DA` | 1:1 | Fidelidad y conteo. **Nunca blanco puro.** 8–12% de aire por lado |
| 2 | **Ambiente EXTERIOR** | 1:1 | "cómo se ve en mi terraza". Producto ≥45% del cuadro |
| 3 | **Ambiente INTERIOR** — mismo hábitat, otro momento | 4:5 | "cómo se ve en mi porche/galería". Misma casa, distinta hora |
| 4 | **ASMR de material / FEATURE verificable** | 1:1 | Prueba de calidad. Costura, unión, herraje, canto — **nunca la trama** |
| 5 | **ASMR de atrezzo de EXTERIOR** — plano ABIERTO | 1:1 | Vida. La superficie que sostiene el atrezzo **es producto** |

> ### ⛔ NADA DE COMIDA NI BEBIDA (decisión de Sergio, 03-08)
> Vendemos **decoración de exterior**, no una comida. Un caldo y un pan en una terraza no se sostienen: la
> lógica se rompe antes que la imagen. **Deroga la "ley del consumible + aperitivo" del ROL §9** y la columna
> "Consumible" del registro de localizaciones.
>
> **Atrezzo permitido:** libro · planta o maceta de barro (olivo, romero, lavanda) · manta o plaid de lino ·
> cesta · sombrero de paja · farol apagado · cerámica artesana vacía.
> **Prohibido:** platos, cuencos con comida, pan, fruta, tazas y jarras servidas, copas, botellas, vasos con
> bebida, cubertería, bandejas de aperitivo.

**La ficha SIEMPRE queda con 5 media** (es el precedente aprobado en las 25 galerías publicadas).
Si el Paso 0 dio cotas, **la imagen de medidas ocupa el hueco 5 y se queda un solo ASMR**; si no hay cota,
el hueco 5 es el segundo ASMR. *(Si algún día quieres 6, dilo y se cambia también el verificador del Paso 7.)*

**La cota se dibuja sobre una vista FRONTAL casi ortográfica generada aparte, nunca sobre el packshot en 3/4.**
En perspectiva 3/4 el ancho proyectado no son los centímetros reales y **la cota miente**. Prompt:
*"strictly FRONTAL elevation view, camera perfectly level and centred, 135 mm"*.
Si la ficha da "72×75" sin desglosar → **se pregunta a Sergio**; en 3/4 tres centímetros son indistinguibles.

**Coherencia de secuencia:** las tomas 2 y 3 son el **mismo mundo**, un solo sol, un solo grade. La 1 y las
ASMR son neutras. Toda la ficha comparte dirección de luz y temperatura.

> ### ⛔ Los ambientes se hacen por SWAP DE FONDO desde el packshot ya aprobado
> **Nunca desde la foto del proveedor.** En el ambiente el mueble ocupa menos cuadro y el modelo **simplifica
> el tejido**: un jacquard, una trama o una veta sutil desaparecen y salen lisos. Anclando al packshot que ya
> pasó el QA, el modelo parte de un tejido correcto y lo conserva.
> Se pasa el `job_id` del packshot aprobado en `medias[]` y el prompt dice *"change ONLY the background and
> the ground"*. El QA se sigue haciendo **contra la foto oficial del proveedor**, no contra el packshot.
> *(Verificado en el Brandon 3 pl.: generado desde la foto del proveedor, el jacquard se perdía; por swap, se
> mantuvo en las tres tomas.)*

**Dónde caben las manos:** en las tomas 2, 3, 4 y 5 (nunca en el packshot). **Con manos** en cuadro, la huella
de uso es obligatoria: vapor, cojín hundido, libro abierto. **Sin manos, la escena va EN REPOSO** — pero no
muerta: la vida la dan huellas *frías* que no implican a nadie ahora mismo (condensación en un vaso, sombra
moteada, hoja caída, manta plegada, libro cerrado). **Una toma de ambiente sin ninguna señal de vida se regenera.**

---

## PASO 4 · MECÁNICA HIGGSFIELD

1. `media_import_url(<URL oficial del SKU>)` → `media_id`
2. `generate_image({model:"nano_banana_pro", prompt:<CORTO>, medias:[{value:media_id, role:"image"}], aspect_ratio, resolution:"1k", count:2, get_cost:true})`
3. preflight → lanzar sin `get_cost` → `job_status(jobId, sync:true)`
4. **QA de fidelidad y escena sobre la 1k** (Paso 5) → `upscale_image` a `4k` → **re-QA anatómico de manos
   sobre el 4k, BLOQUEANTE** → validación de Sergio (Paso 6) sobre la imagen final

> **El orden importa.** A 1k una mano mide ~40 px y no se le pueden contar los dedos; a 4k mide ~160 px y sí.
> Si el upscale va después del "ok", **Sergio aprueba una imagen y se publica otra que nadie ha inspeccionado.**

- **Prompt CORTO en modo edición** (3–6 frases, inglés). Los largos **colapsan a blanco**.
- **Generar a `1k` SIEMPRE.** Pedir 2k/4k en generación da imagen vacía (std de píxeles ~15 = vacía, ~60 = real).
  *(El ROL §7.4 dice `4k`: está desactualizado, se verificó empíricamente en la Fase 0.)*
- **Describe la FÍSICA** (hora, dirección y dureza del sol, material, distancia de cámara). Nunca "8k, ultrarrealista".
- **Nombra material Y FORMA, y niega lo que el modelo inventa:**
  *"ROUND nesting tables, round never rectangular"* · *"FLAT SMOOTH GREY HPL — not stone, not travertine, no grain"*.
- **Niega el fondo HEREDADO desde el primer prompt.** El modelo arrastra lo que hay en la foto de origen: si el
  proveedor fotografió con palmeras o playa, aparecerán. Ya pasó dos veces (playa de Cádiz colada en un ASMR de
  Albania, cortinas inventadas en la pérgola). Escribe el fondo que quieres **y el que no**:
  *"whitewashed lime wall and dry-stone wall — NO palm trees, no tropical plants, no beach"*.
- **Óptica que no miente:** 70–105 mm en packshot y detalle, 35–50 mm en ambiente desde >2 m. **Cero gran
  angular** — es la causa nº1 del "mueble de juguete en paisaje enorme".
- **El upscale a `4k` falla en ratio 4:5** — usar `2k` (da ~2160×2672, por encima del mínimo de 2000 px).
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

> ### ⛔ CÓMO SE COMPARA UNA TRAMA — el método, no la buena voluntad
> **Mirar los dos recortes "ampliados" en pantalla NO es comparar.** Así aprobé el jacquard perdido en dos
> imágenes del Brandon: los puse uno al lado del otro a tamaños distintos y "parecía que estaba".
>
> **Protocolo obligatorio, en este orden:**
> 1. **Calcula los px/cm de cada imagen** con una cota conocida. *(Sofá de 220 cm que mide 1711 px → 7,8 px/cm.)*
> 2. **Recorta el MISMO número de centímetros reales** en las dos —30-40 cm de cojín— y llévalos al **mismo
>    tamaño final**. Solo entonces la trama es comparable.
> 3. **Recorta la pieza MÁS CERCANA a cámara**, no la más lejana. El sofá del fondo tiene menos píxeles por
>    centímetro que el sillón de delante: mirar el sofá es darse la razón a uno mismo.
> 4. **Si a igual escala el motivo no aparece, NO está.** No es "sutileza", no es "resolución": el modelo lo
>    ha borrado. Rechazo.
>
> **Prueba de fuego:** si la foto del proveedor tiene MENOS px/cm que tu imagen y en ella el motivo se ve y en
> la tuya no, la excusa de la resolución no existe.
>
> ### Y dos errores de medición que ya me han hecho fallar dos veces (20-08)
> **1 · Un motivo no se mide con la métrica de los hilos.** La diferencia entre píxeles vecinos mide la **trama**
> (frecuencia alta). El motivo de un jacquard son **manchas de 1–4 cm**: frecuencia media. Medirlo con la métrica
> equivocada dio 0,129 frente a 0,249 del real y me hizo tumbar una imagen que sí tenía el motivo.
> **La medida correcta:** `blur(4) − blur(26)` sobre el parche normalizado, y comparar su desviación típica.
> Con esa banda, el mismo par daba **88 % del real** — atenuado, no ausente.
>
> **2 · El parche va en la MISMA zona anatómica de la pieza.** Recortar por coordenadas fijas en dos imágenes con
> composiciones distintas compara el asiento de una con el respaldo de la otra. Asiento con asiento, brazo con brazo.
>
> **Y el veredicto se da MIRANDO los tres parches juntos** —real, candidata y, si existe, la ficha hermana ya
> publicada— a la misma escala. El número solo acompaña.

**B · Física de luz** — un solo sol · sombra de contacto bajo **cada** apoyo (si flota, rechazo) · sombra
proyectada al lado opuesto, nunca hacia cámara · sombra coloreada, negros al ink `#23251D` nunca `#000` ·
sin HDR falso · microtextura sin denoise plástico.

**C · Escala — línea roja del dueño** *(ROL §13.bis)*. Sin cuerpo entero, la escala se ancla en objetos:

| Ancla | Cota real |
|---|---|
| Mano humana | **18 cm** — obligatoria en toda toma con manos |
| Libro cerrado | 22–25 × 15 cm |
| Maceta de barro | 25–40 cm Ø · olivo/romero en maceta 60–120 cm de alto total |
| Cojín de asiento | 45–60 cm |
| Cesta / farol | 30–40 cm · 15–30 cm |

**Las COTAS REALES del producto mandan sobre el encuadre.** Antes de acercarte, apunta las medidas del Paso 0
y comprueba la razón en la imagen: si el sofá mide 220 cm y la mesa 80 cm Ø, **la mesa es 0,36 del ancho del
sofá — y sigue siéndolo en el primer plano.** Acercarse cambia el encuadre, nunca las proporciones.

Producto **≥78% del ancho** en packshot, **≥45%** en ambiente (nunca <30%). Plano de cierre sólido a 2–5 m
detrás; sin fuga al infinito. Cielo ≤25%.
**Un mueble que "encoge" al acercarse invalida la toma aunque la textura sea perfecta** — es el fallo que
Sergio señaló en el primer ASMR del Brandon: mesas enanas respecto al sofá.

**C.bis · Manos — el fallo IA nº1, sobre el 4k** — 5 dedos por mano, sin dedos fundidos ni de más, sin "tercera
mano", muñeca natural. **La mano que TOCA el producto es la de máximo escrutinio: si falla, rechazo aunque el
resto sea perfecto.** Se verifica **tras el upscale**, nunca en la previa a 1k.

**D · Lógica de la escena (tells de IA)** — cada bebida con dueño y **junto a él**, nunca en el lado opuesto ·
nada de props duplicados sin dueño · **escena sin manos = escena EN REPOSO**: cojines mullidos y lisos, sin
vapor, sin huella de cuerpo (el vapor implica que alguien está ahí ahora) — pero con huella *fría* que dé vida
(condensación, sombra moteada, hoja caída, manta plegada). **Con manos en cuadro, el vapor y la huella son
obligatorios.**

**E · On-brand** — NO resort tropical, NO chalet imposible · fondo bone nunca blanco puro · ≤5 props ·
0 logos, 0 watermark, 0 texto de IA · no sugerir montaje nuestro (self-assembly).

**F · Técnico** — ≥2000 px (objetivo 2400) · cover en producto · sin amputar patas ni brazos en el 1:1.

**G · ESTACIÓN — bloqueante, se mira EN LA IMAGEN** *(no basta con pensarlo antes de generar)*
Mira el suelo, el cielo y los textiles: ¿suelo **seco**, sin charcos ni reflejos de agua? ¿sin gotas en
cristales? ¿cielo claro aunque velado, no plomizo? ¿**sin hojas secas caídas**? ¿textiles ligeros, sin lana
gruesa? Si alguna falla en temporada de verano → **regenerar**.

**H · VERACIDAD DEL LUGAR — bloqueante, se mira EN LA IMAGEN**
1. **¿Hay arquitectura española en cuadro?** Al menos una esquina de la casa: mampostería, sillería, galería
   acristalada blanca, alero de teja. **Una terraza flotando en un prado no está en ningún sitio.**
2. **¿Hay 2 anclas de paisaje de la región?** En el norte: silueta de sierra al fondo *(la costa cantábrica
   siempre tiene monte detrás)*, eucaliptal o mancha de monte, parcelas con seto. Un horizonte recto y vacío
   sobre césped raso es Irlanda, no Cantabria.
3. **¿El muro es del país correcto?** Norte de España: **mampostería de caliza gris angular trabada con
   mortero**, esquinas de sillar. **NO** muro de piedra seca de cantos redondeados con líquenes naranjas —
   eso es *cornish hedge* irlandés/córnico, y es lo que el modelo pone si no se lo niegas.
4. **La pregunta final:** *"¿esto está en España o podría estar en Cornualles?"* Si vale igual para las dos,
   no has localizado nada → **regenerar**.

**I · TEST DE COLLAGE — la foto tiene que ser una foto (bloqueante, 20-08)**
Es el fallo que costó la galería del Brandon. Un producto **compuesto** sobre una escena no se integra jamás,
porque arrastra la luz del estudio donde lo fotografió el proveedor: plana, frontal y difusa. Seis
comprobaciones, todas **mirando la imagen**, no calculando:

| # | Qué se mira | Señal de collage |
|---|---|---|
| 1 | **Sombra de contacto** | La pata se apoya sobre losa limpia. Cada apoyo tiene que ennegrecer el suelo justo donde lo toca |
| 2 | **Sombra proyectada** | No existe, o cada pieza tira la suya hacia un lado distinto, o su largo no corresponde a la altura del sol |
| 3 | **Oclusión ambiental** | Bajo el asiento y entre las piezas el suelo está igual de claro que a tres metros. Un mueble sin penumbra debajo flota |
| 4 | **Rebote de color** | El bajo de las patas no recoge el verde de la hierba ni el cálido de la caliza. Misma temperatura en todas las caras = viene de otro sitio |
| 5 | **Grano y nitidez** | El mueble está más definido que los objetos a su misma distancia, o no comparte su grano |
| 6 | **El borde, al 200 %** | Halo, orla clara, o un contorno más limpio que cualquier borde real de la escena |

> **Prueba de los dos tapados** — vale más que las seis:
> **Tapa el mueble con la mano.** ¿La escena sigue teniendo sentido? Si el suelo queda impecable y vacío, sin
> marca de que ahí viva nada, la escena se generó sin él y el mueble se pegó encima.
> **Tapa el fondo.** ¿La luz sobre el mueble podría ser la de esa escena? Si es plana y frontal, es de estudio.

---

## PASO 5.bis · LAS TRES PROMESAS — lo que la foto tiene que cumplir

> *"Que exprese ASMR, una forma de vivir el producto, que el producto tenga vida. Que exprese el lujo, que
> exprese determinación para la calidad. Y que nada más ver la foto te entren ganas de comprarlo."*
> — Sergio, 20-08-2026

El QA de arriba dice **qué no puede fallar**. Estas tres dicen **qué tiene que conseguir**. Se juzgan mirando
la imagen a tamaño real, en menos de tres segundos, y se responden por escrito antes de enseñarla:

**1 · VIDA — ¿alguien vive aquí?**
Sin persona en cuadro, la vida la da el **rastro reciente**: la manta caída por el brazo del sillón como la
dejó alguien, no doblada de tienda · el cojín con la huella de una espalda · el libro abierto boca abajo ·
la maceta con tierra recién regada. Un conjunto perfectamente alineado y sin tocar es un catálogo de fábrica.
**Contra-regla:** el rastro es *frío* (nadie está ahí ahora). Nada de vapor ni de bebidas — [ver la prohibición](#-nada-de-comida-ni-bebida-decisión-de-sergio-03-08).

**2 · LUJO — ¿de dónde sale?**
De la **luz y la sombra**, nunca del precio de los props ni de la saturación. Lujo es: una sola luz suave y
direccional que modela el volumen del cojín · negros abiertos con detalle dentro (ink `#23251D`, jamás `#000`)
· materiales que se leen al tacto con los ojos · aire alrededor del producto · paleta corta. Si para que
parezca caro hay que meter una piscina, un resort o una copa de champán, la foto no es cara: es hortera.

**3 · DESEO — ¿me lo quiero comprar?**
La última pregunta y la más honesta: *¿esta foto me da ganas de sentarme ahí?* No *"¿es correcta?"*, no
*"¿pasa el QA?"*. Si la respuesta es tibia, la imagen no entra aunque no falle ni un bloqueante. El cliente
paga 5.249 € por lo que siente en los primeros dos segundos.

**Las tres se responden por escrito al presentar la imagen.** Una imagen que no puede defender las tres frases
no se presenta.

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

## PASO 7 · IDENTIDAD, y solo entonces publicar

### 7.a · PUERTA DE IDENTIDAD (bloqueante — es el fallo A0)

Con el "ok" de todas las imágenes y **antes de tocar Shopify**:

1. Volver a ejecutar `python3 scripts/fuente_verdad_producto.py <handle-DESTINO>`.
2. Abrir su **foto real** junto al **packshot generado**.
3. Afirmar por escrito: **"es el mismo mueble"** — chasis, forma de los brazos, nº de plazas, color, tablero.
4. Si no se puede afirmar mirando el píxel, **no se publica**.

> La galería del Albania estuvo días en la ficha del Bellagio (3.449 €) porque el nombre de la carpeta se dio
> por bueno como identificación. **La carpeta no identifica nada; el handle destino sí.** Son diez segundos.

### 7.b · Publicar

`scripts/publicar_galeria_producto.py` (dry-run por defecto, `--apply`).

**Orden seguro, el que hace el script:** capturar los IDs antiguos → subir las nuevas → **esperar READY** →
reordenar → **y solo entonces borrar las antiguas**. Si alguna no llega a READY, **no se borra nada**.
Nunca borrar primero: una ficha sin imagen, aunque sea un segundo, es una ficha rota.
*(El incidente real fue un filtro `*` demasiado amplio que borró lo recién subido — el remedio es excluir
explícitamente lo nuevo, no invertir el orden.)*

**Dos límites de Shopify que hacen fallar la subida en silencio** (la imagen queda en `FAILED`, la ficha se
queda sin foto y el script dice "subida HTTP 201"):

| Límite | Síntoma | Arreglo |
|---|---|---|
| **~20 megapíxeles** | `status: FAILED`, `image: null`. Las fotos de Hevea vienen a **35–39 MP** | redimensionar a ≤18 MP antes de subir |
| **20 MB** por fichero | error 400 al crear el media | recomprimir a 4000 px, quality 92 |

**Verificar SIEMPRE el `status` de cada media después de subir.** Un `productCreateMedia` que responde bien no
significa que la imagen exista: puede quedarse en `FAILED` minutos después.

Verificar al cierre: `ACTIVE · 5 media · READY · ≥2000 px · pos 0 = packshot · 0 alt vacíos`.
Y anotar la fila del producto en [`REGISTRO_LOCALIZACIONES.md`](../../docs/santavila/REGISTRO_LOCALIZACIONES.md).

---

## MÉTODO A1 · POR QUÉ YA NO SE USA

> **Se probó en el Brandon 3 pl. el 19-08-2026 y se retiró al día siguiente.** La idea era buena sobre el
> papel: si el modelo no sabe dibujar el jacquard, **el tejido no se genera — se recorta de la foto del
> proveedor y se compone sobre la escena**. La fidelidad del material deja de depender de la suerte.
>
> Funcionó exactamente como prometía: el color quedó a 0,1 del real, el motivo intacto, la geometría exacta.
> Y las cinco imágenes eran **inservibles**. Sergio: *"está fatal… es horrible… no tiene sentido ni coherencia"*.

**Por qué falla, y por qué no tiene arreglo.** El recorte trae consigo la **luz del estudio del proveedor**:
plana, frontal, sin dirección. La escena tiene otra luz, otra hora y otro cielo. Al pegar uno sobre otra no
hay —ni se pueden fabricar a mano— **sombra de contacto, oclusión ambiental, rebote de color del entorno ni
coherencia de grano**. El ojo lo detecta en menos de un segundo aunque no sepa nombrarlo: *el mueble flota*.
Una elipse difuminada bajo cada pata no es una sombra; es una mancha.

**⛔ Prohibido componer el producto sobre una escena.** Ni en ambiente, ni en detalle, ni en packshot.

### Qué se hace en su lugar

1. **Generar anclado a la foto real** — el camino de siempre, y el que dio las dos mejores imágenes del
   Brandon. El modelo pone el mueble *dentro* de la luz de la escena, con sus sombras, y por eso parece una foto.
2. **Si el material no sale a la segunda**, no se fuerza: se **cambia el encuadre** para que ese material deje
   de ser la superficie dominante (plano más abierto, o sujeto = estructura/canto/herraje). El jacquard
   tono sobre tono se lee perfectamente a distancia de ambiente; lo que el modelo no sabe es hacerlo en macro.
3. **Si aun así no hay imagen defendible**, la ficha se queda con la foto del proveedor. Es la LEY 0.

**Lo único que sobrevive del A1** —porque no toca la fotografía— es la **reparación local determinista**:
ver [Reparar sin regenerar](#reparar-sin-regenerar).

---

## DOS COSAS QUE EL MODELO INVENTA SIEMPRE *(Bolonia XL-8, 20-08-2026)*

**1 · Si le pides recolocar, redibuja — y al redibujar, inventa.**
Pedirle *"pon los sillones abiertos hacia la cámara"* o *"recompón el conjunto"* le obliga a construir el mueble
de nuevo, y entonces aparece lo que no existe: en el Bolonia, un **respaldo de lamas verticales** en un sillón
que lo tiene liso, y en otro intento el respaldo bajó 20 cm. Cinco descartes por esto.
> **Regla: swap de fondo puro.** *"Keep the furniture exactly as shown: same pieces, same arrangement, same
> camera angle, same proportions. Replace only the background with …"* Quitar un objeto (un reposapiés, un vaso)
> sí se puede pedir. Mover, girar o recomponer el mueble, no.
> **Si la composición del proveedor no sirve, se cambia el encuadre — no la escena.**

**2 · La cara que el proveedor no fotografió, se la inventa.**
El catálogo enseña los sillones de frente y de tres cuartos. Ninguna foto enseña la **trasera**. Cada vez que
un encuadre dejaba un sillón de espaldas, el modelo le puso lamas. No es que el modelo se equivoque: es que ahí
**no hay dato**, y por la LEY 0 tampoco lo hay para aprobarlo.
> **Regla: si un encuadre muestra una cara no fotografiada, se cambia el encuadre.** Y una toma no necesita
> enseñar todas las piezas: el ambiente interior del Bolonia se resolvió con **solo el sofá y la mesa**, porque
> el conjunto completo ya estaba en el packshot y en el ambiente exterior.

---

## LO QUE SALE EN LA FOTO Y NO SE VENDE

> **Sergio, 20-08-2026:** *"O no dibujarlo, o dejar una nota en los textos de qué elemento es y que no se incluye.
> Esto lo hacen muy bien en Zara Home y en Maisons du Monde: explicar con elegancia lo que no está incluido."*

Los proveedores fotografían el **ambiente**, no el lote. Hevea llega a anotarlo en su propio catálogo —*"Set BOLONIA
XL-8 (Sin reposapiés)"*— pero esa advertencia se queda en el PDF y **no viaja con la foto**. Si la copiamos tal cual,
el cliente ve un reposapiés de 340 € que no le va a llegar.

**Cómo se detecta.** En el PASO 0, comparar la foto con la **fórmula de composición** de la tarifa
(`2XA+C+D`) y con la suma de PVP de las piezas. Si la cuenta cuadra sin una pieza que sale en la foto, esa pieza
no entra. *(Bolonia XL-8: 1.740 + 840×2 + 470 = 3.890 € = PVP del set, al euro.)*

**Dos salidas, y en este orden:**

**1 · No dibujarla** — siempre que la imagen sea nuestra. Una foto que no la enseña no necesita explicarse. Es lo
que se hizo en el Bolonia: las cinco imágenes van sin el reposapiés.

**2 · Declararla en texto** — cuando la pieza aparece igualmente (foto del proveedor sin alternativa, o atrezzo que
da vida a la escena). Se escribe como un dato más de la ficha, **nunca como una advertencia**:
- Primero lo que **sí** entra: *"El conjunto incluye: sofá de 3 plazas, dos sillones y mesa de centro."*
- Después, en una línea sobria: *"El reposapiés que aparece en las imágenes se vende por separado."*
- Si esa pieza está en el catálogo, **se enlaza**: la nota deja de ser un descargo y pasa a ser una venta.
- Para el atrezzo: *"Los elementos decorativos no están incluidos."*

**Prohibido:** mayúsculas, negritas de alarma, "OJO", "IMPORTANTE", exclamaciones o letra pequeña al pie. Una
tienda de lujo no se disculpa por lo que no vende: lo dice, y ofrece dónde comprarlo.

---

## REPARAR SIN REGENERAR

> Una imagen aprobada con un defecto pequeño **no se regenera**: regenerar cambia todo lo demás. *(Al rehacer
> la 02 del Brandon para quitar un libro, el sillón izquierdo cambió de color: R−B de +19 a +29.)*

**Orden de intentos, del más barato al más caro:**

1. **Reencuadrar** — el defecto sale del cuadro. Gratis, sin riesgo, y a menudo mejora la composición.
   *La toma 05 del Brandon salió así: un recorte cerrado de la 02, ya con los libros a escala.*
2. **Reparación local sin IA** — solo sobre **fondo liso y continuo**: prolongar el gradiente de una pared,
   estirar un suelo en perspectiva, cerrar un letterbox. *Así se quitaron las dos bandas del packshot.*
   Técnica: difusión (Laplace) con el contorno como frontera, más el grano tomado de **una zona lisa del
   mismo material y la misma luz** — un grano tomado sobre un canto o una junta repite ese canto y se ve.
3. **Regenerar solo esa toma** — último recurso, y obliga a repasar el QA entero de la imagen nueva.

> ### ⛔ La línea roja de la reparación
> **Si tapar el defecto obliga a repintar geometría del producto, no se repara.** En el Brandon el libro
> ocultaba el canto trasero de la mesa: borrarlo exigía redibujar ese arco, y redibujar el canto de una mesa
> es **inventar mueble**. Se reencuadró en su lugar. Fondo, sí. Producto, jamás.

---

## SUSTITUIR UNA IMAGEN QUE YA ESTABA BIEN

El error más caro del 19-08 no fue técnico: **cambié cinco fotografías que ya eran buenas por otras peores**,
por mi cuenta, persiguiendo una métrica.

- Una imagen aprobada **solo se reemplaza si la nueva gana en la comparación directa**, las dos a tamaño real
  y una al lado de la otra — nunca porque la nueva puntúe mejor en un número.
- Esa comparación **se le enseña a Sergio antes de tocar nada**. No hay sustitución silenciosa.
- Un defecto acotado (un prop grande, una banda, un texto) **no invalida el resto de la fotografía**: se
  repara por el orden de arriba. Tirar una foto entera por un libro es tirar el trabajo bueno con el malo.

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
| **Componer el producto sobre la escena** | Cinco collages publicados en la ficha de 5.249 €. El recorte trae la luz del estudio y flota. [Ver el A1](#método-a1--por-qué-ya-no-se-usa) |
| **Aprobar por métrica** | Las cinco tenían el color del tejido exacto. Un número tumba una imagen; no la aprueba |
| **Sustituir en silencio una foto ya buena** | Cambié una galería aprobada por otra peor sin comparar ni preguntar |
| **Texto en un prop** | El libro del Brandon llevaba letras inventadas en la portada. O el prop no lleva texto, o el prop no va |
| **Prop sin medir** | Ese mismo libro medía 28 cm sobre una mesa de 80. Todo prop se mide en cm reales usando una cota del mueble como regla, **antes** de aceptar la imagen |
| **Repintar producto para tapar un defecto** | Quitar el libro obligaba a redibujar el canto de la mesa. Se reencuadra o se descarta |

---


## Si dos fuentes del proveedor discrepan, manda el CATÁLOGO (21-08-2026)

Pasa: el **CSV maestro** y el **catálogo PDF** de Hevea dan cotas distintas para la misma
referencia. Bolonia XL fue el caso: CSV 215/164/80, catálogo 200/141/78.

**Decisión de Sergio: siempre catálogo.** El PDF es el documento que el proveedor publica e
imprime; el CSV es un volcado que arrastra errores. Cuando las dos hablen, gana el catálogo.

- CSV **==** catálogo → cota confirmada por doble fuente, la mejor situación
- CSV **≠** catálogo → **catálogo**, sin dudarlo
- solo CSV (la serie no está en el PDF) → CSV, es fuente del proveedor
- ninguna de las dos → **esa ficha no lleva imagen de medidas**

Ojo: el **título de Shopify** puede llevar la cota vieja del CSV. Eso es SEO (trabajo del
compañero) y se anota, no se toca; pero la cota que se DIBUJA sale del catálogo.


## La cota se dibuja donde diga el detector, y el detector se verifica (21-08-2026)

El overlay lleva su propio detector de contorno *por neutralidad* (§ el producto es gris, el fondo bone es
cálido). Con los packshots nuevos **falla**, y falla en silencio: devuelve un bbox que llega al borde de la
imagen, así que la cota de alto arranca del cielo y la de ancho se pasa de largo. Nadie lo ve si no se mira.

Cuatro detectores se probaron antes de dar con el bueno, y cada uno enseñó algo:

| Detector | Por qué falla |
|---|---|
| neutralidad (R≈B) | el producto **blanco** también es neutro |
| fondo por mediana de los bordes | el bone lleva **viñeta** (198 en la esquina, 252 bajo el foco) |
| umbral global de luminancia | la viñeta cae bajo el umbral y arrastra el borde entero |
| solo oscuridad local | el cojín claro del sillón blanco no la supera → cortaba el respaldo |

**Lo que sí se cumple siempre:** el fondo es, en su vecindad, *lo más claro* **y** *lo más cálido*. Las dos
cosas se estiman con un máximo local (que salta por encima del producto) y es producto lo que queda por
debajo en cualquiera de las dos. Eso es `scripts/bbox_producto.py`, con margen del 1 % hacia fuera porque
**una cota corta engaña más que una larga**.

**Regla de trabajo:** ejecutar `bbox_producto.py --hoja /tmp/x.jpg`, **mirar la hoja** y solo entonces pasar
el bbox al overlay. Un detector que no se ha mirado no ha detectado nada.

## Herramientas

| Script | Para qué |
|---|---|
| `scripts/fuente_verdad_producto.py <handle>` | **PASO 0.** SKU, variante, foto oficial, galería, cotas, descripción, catálogo |
| `scripts/fuente_verdad_producto.py --cobertura` | qué fichas se pueden trabajar y cuáles no |
| `scripts/auditar_fotos_duplicadas.py` | fichas que comparten foto principal (huella perceptual) |
| `scripts/publicar_galeria_producto.py` | publicar (dry-run por defecto; `--apply`) |
| `scripts/overlay_medidas_producto.py` | cotas deterministas, **NO IA**, solo con medidas del PASO 0 |
| `scripts/bbox_producto.py <packshot>` | **el contorno para la cota.** Pásaselo al overlay con `--bbox` |
| `scripts/auditar_galerias.py` | qué fichas ACTIVE están sin galería, en baja resolución o sin alt |
| `scripts/auditar_identidad.py` | puerta de identidad: packshot contra la foto oficial del SKU |

## Contexto obligatorio antes de empezar
[`ROL_FOTOGRAFO_SENIOR.md`](../../docs/santavila/ROL_FOTOGRAFO_SENIOR.md) (el oficio: §8 paleta · §11 roster ·
§12 Master QA · §13 escala) · [`LECCIONES_FIDELIDAD.md`](../../docs/santavila/LECCIONES_FIDELIDAD.md) ·
[`REFLEXION_2026-07-30.md`](../../docs/santavila/REFLEXION_2026-07-30.md) ·
[`REGISTRO_LOCALIZACIONES.md`](../../docs/santavila/REGISTRO_LOCALIZACIONES.md)

## Regla final
Si dudas entre **más espectacular** y **más fiel** → gana **fiel**.
Si dudas entre **publicar** y **preguntar** → gana **preguntar**.
