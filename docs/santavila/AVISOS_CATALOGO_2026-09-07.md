# Avisos de catálogo — lo que encontró la fase 3

> Salidos de fotografiar 50 fichas de Balliu una a una el **07-09-2026**. Ninguno es un problema
> de imagen: son datos del catálogo que no cuadran. Se anotan aquí porque **no me corresponde
> tocarlos** —los títulos y las descripciones los lleva el compañero de SEO— y porque varios
> necesitan una respuesta del proveedor.

## 1 · Hay que preguntar al proveedor

### Parasol «Ocean tela» · 382 € · [`balliu-parasol-para-terraza-f1ed8b8b`]
El título dice **Ø200/Ø250 cm** —o sea, redondo— y sus **dos únicas fotos son de un parasol
cuadrado**. O el título está mal o las fotos son de otro producto.

**Es la única ficha de las 50 que se ha quedado sin imagen nueva.** No se inventa la forma de un
producto: en cuanto Balliu diga cuál de las dos cosas es, se hace en diez minutos.

### Mesa comedor Córcega 135×90 · 720 € · [`mesa-comedor-exterior-hpl-13590-cm`] · Hevea
El CSV da **alto = 90 cm**. Una mesa de comedor de 90 cm de alto no existe (eso es altura de
mesa alta), y en la propia foto del proveedor **los respaldos de las sillas sobresalen por
encima del tablero**, lo que sería imposible con 90 cm.

El catálogo Hevea (pág. 74) da **76 H** para toda la familia HPL —Naloa, Córcega, Palma,
Camelia— pero **no lista la Córcega 135×90**, solo la cuadrada de 90×90.

**Actualización 08-09-2026 — se publicó con 76 H, y conviene saber de dónde sale.** La ficha de
medidas declara `135 × 90 × 76 cm` y `160 × 90 × 76 cm`. El 76 **no** viene de la línea de esa
referencia —el catálogo no la lista— sino de que **toda la familia HPL de Hevea mide 76 H**
(Naloa, Córcega 90×90, Palma, Camelia). Es una inferencia por familia, sólida pero inferencia.

Se prefirió eso a dejar una mesa de comedor sin altura: el 90 del CSV es imposible y el cliente
necesita el dato para saber si le encajan sus sillas.

**Sigue pendiente que Hevea confirme la altura de la 135×90 y la 160×90.** Si dijera otra cosa,
hay que corregir `images_generated/mesa_corcega/03_medidas.jpg` y republicar esa toma.

### ⛔ Funda acrílico · 37 € · [`balliu-funda-protectora-exterior-acrilico-a1c16324`] — URGENTE

**La foto es de otro producto, y no tenemos ninguna del bueno.**

| Fuente | Qué dice |
|---|---|
| SKU de la ficha | `BALLIU_FUNDA_**PARASOL**_1_UNIDADES_ACRIL_A1C16324` |
| CSV del proveedor, campo Descripción | **«Funda Parasol»** |
| Tarifa 2026 (las dos versiones) | **«Funda Parasol 1 Unidades acrilico»** |
| Nuestra imagen publicada | una **funda de tumbona** cubriendo una tumbona |

El producto es una **funda de parasol**; lo que se ve es una **funda de tumbona**. Un cliente
puede comprar lo que no es.

**Por qué no se ha arreglado generando otra imagen:** el catálogo general **no ilustra la funda
de parasol** — su pág. 160 solo documenta la *«Funda para tumbona»*, y la de parasol aparece
únicamente en la tarifa, sin foto ni descripción. La única imagen original que tenía la ficha se
borró al publicar la galería nueva. **Sin foto real no se genera: sería inventar el producto.**

Por eso esta ficha se ha dejado **en 2 imágenes a propósito** —es la única del catálogo—, en vez
de añadirle una tercera toma que reforzaría un producto equivocado.

**Qué hace falta:** pedir a Balliu la foto de la funda de parasol. Mientras no llegue, decidir si
la ficha pasa a DRAFT.

## 2 · Fotos que no son del producto

### «Tumbona resina Ø73 tablillas · Eva Pro T» · 220 € · [`balliu-tumbona-de-exterior-resina-923110d9`]
Su packshot y casi toda su galería son de la versión de **TELA**, que es **otra ficha distinta**
([`...resina-b19af1ea`], 229 €). La única foto real de la versión de tablillas era un ambiente
con dos unidades; de ahí se aisló una para el packshot nuevo.

Merece la pena revisar qué fotos de proveedor quedan en esa ficha: varias son del producto que
no es.

## 3 · Títulos que no describen el producto

| Ficha | Dice el título | Es en realidad |
|---|---|---|
| [`balliu-mobiliario-exterior-resina-28-cm-6264905d`] · 68 € | «Mobiliario exterior resina \| 28 cm» | Una **caja de seguridad** con cerradura de combinación. Lo dice su propio SKU: `WEGUARD_CAJA_DE_SEGU` |
| [`balliu-mesa-exterior-aluminio-72-cm-72514f40`] · 225 € | «Mesa exterior aluminio · **72×72 cm** · Nora» | Una mesa **redonda**, en sus cuatro fotos |
| [`balliu-mesa-alta-exterior-hpl-94512eab`] · 529 € | «Mesa alta exterior · aluminio HPL **110 cm**» | El 110 es la **altura**; la opción de tamaño dice 70×70. Se entiende mal |

En los tres casos la imagen nueva retrata **lo que el producto es**, no lo que dice el título.

## 4 · ~~Dos vídeos en primera posición~~ — ✅ RESUELTO (07-09-2026)

[`set-jardin-3-plazas-contemporaneo-...`] (2.899 €) y [`tumbona-de-exterior`] (193,95 €) tenían un
**VÍDEO** en la posición 0, que desplazaba al packshot de la miniatura del listado y de la
`og:image`. **Reordenadas: la posición 0 vuelve a ser el packshot en las dos.**

Verificado el 08-09: en las 241 fichas de la tienda, **ninguna tiene un medio que no sea imagen en
la posición 0**, y hay **0 alt vacíos** en las 890 imágenes de fichas ACTIVE.

Lo que sí salió de aquí y **sigue vivo**: al pedir solo `... on MediaImage`, el auditor **nunca
había leído el alt de un vídeo**. Los dos decían justo lo que la marca prohíbe («bebida fría»,
«junto a la piscina») y el informe daba cero. Ya está corregido en
`scripts/auditar_reglas_galeria.py`, y la decisión de Sergio sobre el vídeo del Leisa quedó
registrada como excepción explícita — ver
[`ESTADO_Y_TRASPASO_2026-09-08.md` §5.2](ESTADO_Y_TRASPASO_2026-09-08.md).

## 5 · El acabado de la foto y el de la variante por defecto no siempre coinciden

Pasa en unas cuantas fichas de Balliu: el SKU por defecto dice, por ejemplo, `BLANCO-AZUL` y el
único packshot limpio que existe es en tórtola. **No es un error que haya que corregir**, y la
regla que se ha seguido es la única defendible:

> Se fotografía **el acabado que existe fotografiado**, y el alt lo declara. Las demás variantes
> las siguen cubriendo las fotos del proveedor, que se conservan.

Inventar el color de una variante sería exactamente lo que la ley de fidelidad prohíbe.
