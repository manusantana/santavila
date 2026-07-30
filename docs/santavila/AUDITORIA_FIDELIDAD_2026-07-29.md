# Auditoría de fidelidad — todo lo que está mal en las imágenes publicadas

**Fecha:** 2026-07-29 · **Alcance:** las 25 galerías generadas con Higgsfield (125 imágenes publicadas).
**Método:** foto original del proveedor abierta a **resolución nativa**, recorte por componente
(chasis · tejido · tablero · elementos) y comparación contra cada imagen publicada.

> **Aviso de honestidad sobre este documento.** Antes ya di por buena una auditoría que estaba incompleta:
> comparé miniaturas y solo miré si el tablero era "de lamas o liso". Este informe distingue de forma
> explícita **lo verificado a resolución nativa** de **lo que aún no lo está**. Lo no verificado se lista
> como no verificado, no como correcto.

---

## A · FALLOS CONFIRMADOS

### A0 · ⛔⛔ FALLO DE IDENTIDAD — galería de OTRO producto en la ficha
`set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-3` (Bellagio 3 pl., **3.449 €**)

| | |
|---|---|
| **Producto real de la ficha** | Sofá de **brazos rectos cerrados**, chasis **antracita**, cojines gris claro + **cojines decorativos azul marino**, mesa de tablero liso |
| **Publicado** | Un mueble **distinto**: sillones de **estructura en A con aspa diagonal**, chasis **tórtola claro**, cojines **verde salvia** |

**No es una desviación de material: son dos muebles diferentes.** La carpeta de trabajo se llamaba `albania`
y su galería es la del **Albania**; el handle al que se publicó es el del **Bellagio 3 pl.** Durante días esa
ficha ha mostrado 5 fotos de un producto que no es el que se vende ahí.

**Causa:** el mapeo `carpeta → handle` del script de publicación se escribió a mano y nunca se validó contra
la foto real del handle destino. El nombre de la carpeta se dio por bueno como identificación del producto.

**Estado:** las 5 imágenes retiradas; la ficha está con su foto real del proveedor.

**Regla nueva (PASO 0.bis):** antes de publicar, **comparar el packshot generado con la foto real del handle
destino**. Si no es el mismo mueble, no se publica. La comprobación es de 10 segundos y esto no habría pasado.


### A1 · Acapulco 2 pl. — material de la mesa inventado (DOS veces)
`set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa-4` · imagen `05_asmr_sandia`

| | |
|---|---|
| **Producto real** | HPL/cerámico **gris cemento medio-oscuro, mate**, veta muy sutil, **canto fino enrasado** en el marco antracita → la mesa se lee como **una sola pieza** |
| **Publicado (1º)** | **Piedra caliza rugosa y beige** |
| **Publicado (2º, "corrección")** | **Gris claro brillante**, leyéndose como **bandeja apoyada sobre una base oscura** |
| **Estado** | **Retirada.** La ficha está con 4 imágenes, todas correctas |

**Por qué falló también la corrección:** se corrigió contra el packshot propio, no contra la foto real. El
packshot ya tenía el tono mal, así que el error se heredó. → De ahí el PASO 0 del skill.

### A2 · Familia Brandon — trama del tejido eliminada (3 fichas)
`set-jardin-aluminio-3-plazas-...` · `set-jardin-aluminio-2-plazas-...` · `sofa-terraza-aluminio-3-plazas-...-22090-cm`

| | |
|---|---|
| **Producto real** | Chenille gris con **jacquard estampado tono sobre tono** (motivo tipo grafismo visible en todo el tapizado) |
| **Publicado** | Chenille **liso**, sin motivo, solo textura de trama |
| **Alcance** | Las 3 fichas; el tejido aparece en las 5 imágenes de cada una |

Es el fallo inverso al A1 —aquí se **quitó** una trama que existe en lugar de inventar una— pero incumple
igual: la imagen no representa el producto.

### A3 · Bellagio 2 pl. — tablero de lamas mostrado como liso
`set-jardin-2-plazas-elegante-...-mesa-3` · imagen `05_asmr` (tomate)

| | |
|---|---|
| **Producto real** | **Lamas de aluminio blancas**, juntas visibles |
| **Publicado** | Tablero **blanco liso** |

### A4 · Diva 2 pl. — tablero liso mostrado como lamas
`set-jardin-bicolor-2-plazas-...` · imagen `05_asmr` (naranjas)

| | |
|---|---|
| **Producto real** | Tablero **liso efecto madera marrón** sobre faldón de lamas antracita |
| **Publicado** | Tablero **de lamas** |

### A5 · Odin 3 pl. — veta de madera inventada sobre el aluminio
`set-jardin-3-plazas-elegante-...-mesa` · imagen `04_asmr`

| | |
|---|---|
| **Producto real** | Aluminio antracita **liso mate**, sin veta |
| **Publicado** | Superficie oscura con **veteado longitudinal tipo MADERA** |

Es el caso de manual de la §15 y aun así se publicó.

### ~~A6 · Manhattan 3 pl.~~ — **FALSA ALARMA, corregida**
Di por ausentes los cojines decorativos estampados porque miré el ASMR de chasis, que no tiene por qué
mostrarlos. Comparado el **packshot** con la foto real: los **3 cojines decorativos estampados SÍ están**, y
el estampado coincide. **No hay fallo.**

Consecuencia de mi error: retiré 5 imágenes correctas de esa ficha. **Ya restauradas** (5 media, READY).
Lección: un ASMR de detalle no es la toma donde se audita el conteo de piezas — eso se hace en el packshot.

### A7 · Desviación de color cálida en los ASMR (6 fichas)
Acapulco 2 pl. · Acapulco 3 pl. · Dounvil 2 pl. · **Yina 3 pl.** · **Yina 2 pl.** · **Pérgola**

El material real es **gris frío** (tejido o cuerda) y en el ASMR se lee **beige dorado** por la luz de
atardecer. Supera el ΔE≤3 del QA-A. En el Sofá 220×69 este mismo fallo **sí** se detectó y corrigió en su
momento (regenerado a 5400 K); en estas seis no.

### A8 · Balancín Sidney — HERRAJE DE SUSPENSIÓN INVENTADO ⛔
`balancin-jardin-exterior-148194-cm` · imagen `04_asmr_suspension`

| | |
|---|---|
| **Producto real** | En la única foto disponible **el punto de suspensión NO se ve**: el asiento cuelga del travesaño, pero el herraje queda oculto |
| **Publicado** | **Grilletes cromados en U con bulón**, detallados y en primer plano, presentados como el herraje del producto |

**Este es el fallo más grave de la lista en términos de principio.** No es una desviación de tono ni una
trama mal leída: es **una pieza entera inventada y puesta como protagonista de la imagen**. Y encima el
razonamiento con el que la generé fue *"es lo que un cliente quiere ver para juzgar la calidad"* — es decir,
inventé precisamente el detalle en el que el cliente se va a apoyar para decidir.

Regla que se incumplió: **si no se ve, no existe, y la toma NO se hace.**

---

## B · NO VERIFICABLES — falta la foto original (6 fichas)
No se puede afirmar que estén bien **ni** que estén mal. Pendiente de localizar la foto real en Shopify.

| Ficha | Motivo |
|---|---|
| Albania 3 pl. `...-mesa-3` | el export de imágenes apunta a **otro producto** (antracita + azul marino, no tórtola + salvia) |
| Cama balinesa 198 · Cama balinesa 160 | sin URL de origen en el export |
| Parasol Roma | sin URL de origen en el export |
| LEISA · Tumbona Brescia | fichas de la primera tanda, sin mapeo a la foto original |

---

## C · VERIFICADO A RESOLUCIÓN NATIVA — **solo el tablero**
En estas fichas el **tablero** coincide con el producto real. **El tejido y el resto de componentes de estas
fichas NO están verificados todavía** (el fallo A2 demuestra que el tejido es un vector real de error).

Acapulco 3 pl. (cristal) · Damasco 2 pl. (lamas tórtola) · Diva 3 pl. (blanco liso sobre faldón de lamas) ·
Rinconera HPL (blanco liso, canto oscuro) · Albania 2 pl. · Dounvil 2 pl. · Dounvil 3 pl. ·
Manhattan 2 pl. · Odin 3 pl. (todas lamas, confirmado — **pero Odin falla en A5 y Manhattan 3 pl. en A6**) · Yina 3 pl. · Yina 2 pl.
(cuerda + tablero cerámico) · Brandon y Sofá 3 pl. (mesas redondas lisas — el fallo de estas fichas es el
tejido, no la mesa) · Pérgola · Balancín Sidney · Sofá 220×69.

---

## D · PENDIENTE DE AUDITAR
1. ~~Tejido~~ **COMPLETADO en las 19 fichas con foto original.** Verificadas OK: Albania 2 pl.,
   Bellagio 2 pl., Damasco 2 pl., Diva 2 pl., Diva 3 pl., Dounvil 3 pl., Manhattan 2 pl., Rinconera,
   Sofá 220×69, Acapulco 3 pl. (tablero). Falladas: A2 · A5 · A6 · A7 · A8.
2. ~~Elementos singulares~~ **COMPLETADO** — de aquí salió A8 (herraje inventado en el Sidney).
3. **Conteo de piezas** en las 5 imágenes de cada ficha (ya se revisó al generar, pero sin este rigor).
4. Las 6 fichas del bloque B, cuando aparezca su foto original.

---

## E · COSTE DE CORRECCIÓN
4 créditos por imagen rehecha (2 generar + 2 upscale). Saldo actual ≈ 300.

| Escenario | Imágenes | Créditos |
|---|---|---|
| A0 · Bellagio 3 pl. — galería entera de otro producto | 5 | 20 |
| A1–A5, A7, A8 (incluidos los 5×3 del Brandon) | ~23 | ~92 |
| Si el tejido falla en más fichas | +5 a +25 | +20 a +100 |

---

## F · LO QUE CAMBIA PARA QUE NO SE REPITA
1. **PASO 0 · Ficha de verdad** ([`FICHAS_VERDAD.md`](FICHAS_VERDAD.md)) — sin ficha escrita mirando el
   píxel a resolución nativa, **no se lanza ni un job**.
2. **Lo que no se ve con certeza se marca `NO DETERMINADO` y esa toma NO se genera.**
3. **El QA se hace contra la ficha, nunca contra el packshot propio.**
4. **La superficie que sostiene el atrezzo es producto** — material, tono, acabado y canto, los cuatro.
5. **El tejido se audita con la misma vara que el tablero**: si el real lleva jacquard, la imagen lleva
   jacquard; si es liso, es liso. Ni inventar ni quitar.
6. **PASO 0.bis · IDENTIDAD** — antes de publicar, comparar el packshot con la foto real **del handle
   destino**. El nombre de la carpeta NO identifica el producto. De aquí salió A0.
7. **No retirar por sospecha sin ampliar primero**: A6 fue falsa alarma y costó retirar 5 imágenes buenas.
   La duda se resuelve mirando el packshot a resolución nativa, no borrando.
