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
Manhattan 2 pl. · Manhattan 3 pl. · Odin 3 pl. (todas lamas, confirmado) · Yina 3 pl. · Yina 2 pl.
(cuerda + tablero cerámico) · Brandon y Sofá 3 pl. (mesas redondas lisas — el fallo de estas fichas es el
tejido, no la mesa) · Pérgola · Balancín Sidney · Sofá 220×69.

---

## D · PENDIENTE DE AUDITAR
1. **Tejido de las 22 fichas restantes** contra el recorte nativo (el A2 salió de aquí).
2. **Elementos singulares**: cuerda, lamas de respaldo, herrajes, toldos.
3. **Conteo de piezas** en las 5 imágenes de cada ficha (ya se revisó al generar, pero sin este rigor).
4. Las 6 fichas del bloque B, cuando aparezca su foto original.

---

## E · COSTE DE CORRECCIÓN
4 créditos por imagen rehecha (2 generar + 2 upscale). Saldo actual ≈ 300.

| Escenario | Imágenes | Créditos |
|---|---|---|
| Lo confirmado hoy (A1 + A3 + A4 + los 5×3 del Brandon) | ~18 | ~72 |
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
