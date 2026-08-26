---
name: foto-producto-ia
description: Use when generating, regenerating or improving product photos with AI image models for an ecommerce, catalogue or PDP — packshot, lifestyle/ambient shot, material detail, dimension card; replacing low-resolution supplier photos; or a product listing that has only one photo. Covers any physical product, any supplier, any store.
---

# Fotografía de producto con IA

Producir la galería de un producto físico —packshot, ambiente, detalle, medidas— con **fidelidad
absoluta al producto real**, partiendo del material que haya (aunque sea poco y malo), y sin
prometer nada que el cliente no vaya a recibir.

**Lo premium lo aporta el oficio** —luz, sombra, escena, encuadre—, nunca cambiar el producto.

> **Origen:** destilado de una producción real de ~120 fichas de ecommerce. Las reglas de aquí no
> son teóricas: cada una nació de un fallo que llegó a publicarse o estuvo a punto.

---

## LAS CINCO LEYES

**1 · FIDELIDAD.** Toda generación se **ancla a la foto real** del producto (image-to-image).
**NUNCA** se transforma: geometría, proporciones, número de elementos (piezas, cojines, botones,
costuras, ruedas, patas), material, acabado, color, herrajes, logotipos.
**Solo cambian:** escena, fondo, suelo, atrezzo, luz, sombra, encuadre, resolución.
Variante = su propia foto. Si no hay foto de esa variante, **no se genera esa variante**.

**2 · LEY 0.** *Si no existe, no lo hago. Si no sé hacerlo, no lo hago. Si no soy capaz de
creerlo, no lo creo.* Un dato que no puedas defender no se publica: ni una cota, ni un material,
ni una cara del producto que nadie fotografió.

**3 · LO QUE NO SE VENDE, NO SE DIBUJA.** Los proveedores fotografían el **ambiente**, no el lote.
Ver §Pieza fantasma.

**4 · UNA MÉTRICA RECHAZA, NUNCA ACEPTA.** Un número puede tumbar una imagen. Ninguno la aprueba:
eso lo hace mirarla al lado de la original.

**5 · LO QUE NO SE HA MIRADO NO HA MEDIDO NADA.** Antes de creerte tu propia métrica, comprueba
**dónde ha mirado**. Ver §Las cuatro trampas.

---

## PASO 0 · EL CUESTIONARIO (antes de generar nada)

**Obligatorio en un proyecto nuevo.** Doce preguntas en cuatro bloques que fijan qué es fiel, qué
está prohibido y qué se publica: **[cuestionario.md](cuestionario.md)**.

Sin respuesta a los bloques 1 y 4 **no se genera**: son los que evitan inventar el producto y
prometer de más. Los bloques 2 y 3 admiten valores por defecto si el cliente no tiene criterio
formado, pero se le enseñan y se confirman.

**Guarda las respuestas en el repo** (`docs/<proyecto>/BRIEF_IMAGEN.md` o similar). Son la fuente
de verdad de todas las tandas siguientes, y quien te releve las necesita.

---

## PASO 1 · LA FUENTE DE VERDAD

Antes de la primera imagen, ten localizado y **abierto**:

| Qué | Para qué | Si no existe |
|---|---|---|
| **Foto oficial del producto**, la de mayor resolución | anclaje y referencia de fidelidad | no se genera esa ficha |
| **Catálogo / ficha técnica del proveedor** (PDF) | cotas, composición del lote, acabados | se trabaja solo con la foto |
| **Cotas verificadas** | la toma de medidas | **no se dibuja ficha de medidas** |
| **Qué incluye exactamente el lote** | evitar la pieza fantasma | se aplica el criterio conservador |

**Dos fuentes que discrepan.** Fija la jerarquía **por escrito** en el brief (típicamente el
catálogo publicado gana al volcado CSV). Y antes de aplicarla, comprueba que **miden lo mismo**:
si el ancho y el fondo coinciden en ambas fuentes y solo baila el alto, probablemente no es
contradicción sino **dos magnitudes distintas** (alto total vs. alto de asiento, con/sin embalaje).
Discrepa el ancho → ahí sí es discrepancia.

**El catálogo suele tener más de lo que parece.** Cuando la foto del SKU no sirve, mira, en este
orden: (1) el PDF general, (2) los catálogos secundarios (profesional, contract, temporada),
(3) la foto oficial del **lote o set** al que pertenece la pieza. Las imágenes embebidas de un PDF
se extraen con `pypdf` (`page.images`) y a veces están en mejor resolución que la web.

---

## PASO 2 · EL HÁBITAT

**Decide una vez por producto y mantenlo en toda su galería.** Lee el **estilo** del producto y
ponlo en el espacio donde ese estilo vive de verdad. Un choque de estilo (producto minimalista en
un decorado recargado) se lee como "esto es IA" aunque todo lo demás sea perfecto.

**Reglas que se transfieren a cualquier producto:**
- **Coherencia de secuencia:** todas las tomas de un producto, el mismo mundo. Los ambientes son
  variaciones (ángulo, momento, atrezzo) del mismo espacio.
- **El hábitat lo hereda el ACABADO, no la familia.** El mismo producto en otro color vive en otro
  sitio; dos productos del mismo color y familia, en el mismo. Esto es lo que hace que un catálogo
  se lea como una sola tienda.
- **Escena vivida, no escaparate vacío.** Signos de uso reciente y un detalle sensorial. Listón:
  *"parece que alguien vive aquí ahora"*.
- **Lleva un registro de localizaciones** (`REGISTRO_LOCALIZACIONES.md`): producto → mundo →
  atrezzo. Sin él, a la vigésima ficha repites escena sin darte cuenta.

---

## PASO 3 · LAS TOMAS

Receta por defecto. **Ajústala en el bloque 3 del cuestionario**, no por capricho.

| # | Toma | Aspecto | Origen |
|---|---|---|---|
| 1 | **Packshot** limpio, fondo neutro cálido | 1:1 | IA anclada |
| 2 | **Ambiente A** — el producto en su mundo | 1:1 | IA anclada |
| 3 | **Ambiente B** — otro ángulo/momento del mismo mundo | 4:5 | IA anclada |
| 4 | **Detalle / material** — una unión, una costura, un mecanismo | 1:1 | IA anclada |
| 5 | **El dato que decide la compra** | 1:1 | **overlay determinista, NO IA** |

**Pieza suelta y barata:** packshot + 1 ambiente + toma 5 (3 tomas) es una galería digna.
**Fondo:** cálido neutro, nunca `#FFFFFF` puro — el blanco absoluto delata el recorte.

### La toma 5 no siempre son centímetros

Es **el dato por el que se devuelve el producto si falla**. Cámbialo según la categoría — lo fija
la pregunta 1.4 del cuestionario:

| Categoría | El dato que decide | Cómo se resuelve |
|---|---|---|
| Mobiliario, electrodoméstico, decoración | cotas en cm (¿me cabe?) | cotas sobre el packshot, de extremo a extremo |
| Calzado y ropa | talla y **horma/ajuste** | tabla de tallas + referencia de ajuste; NO cotas |
| Cosmética, alimentación, droguería | formato (ml/g) e **ingredientes** | el envase a escala junto a una referencia conocida |
| Joyería, relojería, accesorio pequeño | **escala real** | la pieza sobre una mano o junto a un objeto cotidiano |
| Electrónica | compatibilidad y puertos | detalle de conectores, no una cota total |

**Nunca se genera con IA:** es un overlay determinista sobre el packshot, con **dato verificado**.
Si no hay dato, **no hay toma 5** — y no se deduce de la foto.

**Regla de la cota, cuando la haya:**
1. **Contorno automático, nunca "a ojo"** — medir el bbox a ojo deja la cota corta.
2. **Etiqueta explícita:** `Ancho · 72 cm`, nunca un `72×75` suelto: es ambiguo y se lee al revés.
3. **De extremo a extremo**, y en el lado limpio (la sombra suele caer a un lado).
4. **Verifica el detector**: dibuja el bbox sobre una hoja de contacto y **míralo**. Un detector
   que no se ha mirado no ha detectado nada.

---

## PASO 4 · MECÁNICA DEL GENERADOR

Verificado en modelos tipo *Nano Banana / Seedream / Flux* vía Higgsfield. Comprueba los límites
de tu motor, pero **estas tres se repiten en todos**:

**1 · Prompt CORTO en modo edición (3–6 frases, inglés).** Los prompts largos colapsan a un
gradiente en blanco. La receta completa es tu checklist **mental**, no el texto.
> *"Using the reference image, keep the product EXACTLY as shown (do not change it) and replace
> only the background with [escena], light [X]. Photorealistic."*

**2 · Generar a `1k` y subir después con upscale.** Pedir 2k/4k en la generación devuelve basura.

**3 · Describe FÍSICA, no calidad.** Hora del día, dirección y dureza de la luz, material,
distancia de cámara. Nunca "8k, ultrarrealista, calidad premium".

**Diagnóstico rápido:** desviación estándar de píxeles ≈15 → imagen colapsada en blanco.
**Pero `std` no juzga la calidad:** un packshot de producto **blanco sobre fondo claro** da
`std ≈ 26` y es perfecto. El `std` solo detecta el colapso.

**Dos frases que rompen la fidelidad, medidas:**

| Frase | Qué provoca | Antídoto |
|---|---|---|
| `warm raking light` | el metal oscuro se vuelve **latón** (R−B pasó de −7 a **+67**) | *"must stay dark neutral grey — never golden or brass. Neutral white balance"* |
| aislar sobre fondo neutro | el packshot **se inventa el acabado** que la escena le daba (gris pizarra → beige madera) | **nombrar el material** en el prompt del packshot |

**Quitar personas u objetos sí se puede pedir. Recolocar el producto, no:** si le pides
recomponer, lo redibuja, y al redibujar inventa. Si la composición no sirve, **cambia el encuadre,
no la escena**.

**Persona sentada sobre el producto** — el caso que más fichas bloquea. Al borrarla, el modelo
rehace el asiento como una superficie continua. Se resuelve **diciendo qué debe quedar**:
> *"Remove the seated person completely and **restore the empty cushions underneath as separate
> individual cushions, never one continuous pad**."*

Funcionó a la primera en 8 fichas, cuatro **partiendo de fotos de 1.080 px**. La orden no basta:
hay que **CONTAR** después. **1.080 px bastan** si el anclaje y el conteo se hacen bien — la baja
resolución del original no es excusa para dejar una ficha sin galería.

---

## PASO 5 · QA — falla un bloqueante, se regenera

**A · FIDELIDAD.** **Cuenta 1:1** los elementos contra la foto oficial (piezas, cojines, listones,
botones, ruedas, costuras). Geometría, material y color de la variante. Cualquier desviación:
rechazo.
**B · SIN ARTEFACTOS.** Verticales a plomo; sin fusiones ni derretidos; sombra de contacto bajo
cada apoyo (que no flote); una sola dirección de luz; nada de HDR falso.
**C · MARCA.** El ambiente pega con el estilo; escena vivida; coherencia con el resto de la
galería; cumple las prohibiciones del bloque 4 del cuestionario.
**D · TÉCNICO.** Resolución mínima acordada; nítida; ratio correcto; compone sin amputar el
producto.

**El conteo se hace en GRANDE.** Ver §Las cuatro trampas.

---

## PIEZA FANTASMA — lo que sale en la foto y no se vende

El fallo más caro de una ficha: el cliente ve algo que no le va a llegar.

**Cómo se detecta.** Muchos catálogos traen la **fórmula de composición** del lote:
```
A=sillón  B=sofá 2pl  C=sofá 3pl  D/E=mesa  F=reposapiés
LOTE-7 = 2xA + B + D          LOTE-8 = 2xA + C + E
```
La `F` no entra en ninguna fórmula → **ese reposapiés no se vende**, aunque salga en la foto
oficial. Verifícalo también con la **suma de PVP de las piezas**: si cuadra sin el elemento
dudoso, ese elemento no entra.

**Si el catálogo no trae fórmula**, aplica el criterio **que no promete de más**: se quita la
pieza dudosa. **Mostrar de menos no engaña; mostrar de más, sí.**

**Dos salidas, en este orden:**
1. **No dibujarla** — siempre que la imagen sea tuya.
2. **Declararla en texto** cuando aparezca igualmente. Primero lo que **sí** entra
   (*"El conjunto incluye: …"*), después una línea sobria (*"El reposapiés de las imágenes se
   vende por separado"*), y **enlace** si está en el catálogo: la nota deja de ser un descargo y
   pasa a ser una venta.
   **Prohibido:** mayúsculas, negritas de alarma, "OJO", "IMPORTANTE", letra pequeña al pie.

---

## LAS CUATRO TRAMPAS

Cuatro disfraces de la misma ley (nº 5). Los cuatro estuvieron a punto de provocar un rechazo —o
un borrado— equivocado **en un solo día**:

| Trampa | Qué pasó | Antídoto |
|---|---|---|
| **Caja de muestreo fuera del producto** | "el material ha cambiado de color": la caja había caído en el fondo y en el suelo | **recorte lado a lado**, no una media de píxeles |
| **Filtro por subcadena** | `villa` marcó buga**nvilla**, se**villa**na, **Villa**mayor: **25 falsos de 29** | `\bvilla\b`, siempre |
| **Miniatura** | "tiene dos mesas"; en grande eran dos sillones y una mesa | contar **en grande** |
| **Tu propio auditor** | marcó como comida una *"jarra de gres con romero"* | todo filtro lleva su lista de **excepciones** |

---

## AUDITAR HACIA ATRÁS

**Una regla nueva no se aplica sola a lo ya publicado.** Una prohibición de atrezzo dejó **8
imágenes vivas** en fichas activas por valor de 17.000 €, descubiertas **tres semanas después**.

Monta un auditor que barra **los textos alternativos** de todo lo publicado contra las reglas del
bloque 4, y **pásalo después de cada cambio de regla**. El alt es el único texto que delata lo que
hay dentro de una imagen sin abrirla.

**Al quitar una toma prohibida, no hace falta reponerla:** si tu receta canónica son 4 tomas +
medidas, esa quinta era un extra. **Borrar cuesta 0; regenerar, el precio de una ficha entera.**
Descarga la imagen **antes** de borrarla: así es reversible.

---

## COSTE Y RITMO

Mide **tu** coste unitario real en la primera tanda y presupuesta con él, no con el teórico.

Referencia medida (Higgsfield, Nano Banana Pro): 2 créditos por generación + 2 por upscale = 4 por
imagen publicada; el real sale **~4,1** contando rechazos, ya netos de los reembolsos automáticos.
**Una ficha de 3 tomas = 2 imágenes IA + overlay = ~8 créditos.**

- **Lotes según la concurrencia de tu plan** (típico: 8 simultáneos). Con saldo bajo, **de 4 en 4**.
- **Upscala lo aprobado antes de generar más:** una generación sin upscale no vale nada.
- Antes de abrir un frente nuevo, mira **cuántas fichas están a medias**: solo necesitan las tomas
  que faltan, la mitad de coste, y heredan el mundo ya fijado.

---

## RED FLAGS — para y vuelve al Paso 0

- Vas a generar sin tener delante la foto oficial
- Vas a dibujar una cota que no has verificado en una fuente
- Vas a publicar sin contar los elementos contra la original
- Le estás pidiendo al modelo que **recoloque** el producto
- Estás juzgando por la miniatura o por un número, sin abrir la imagen
- Una pieza de la foto no la has confirmado en el lote
- Cambias una regla y no barres lo ya publicado

---

## Regla final
Si dudas entre **más espectacular** y **más fiel** → gana **fiel**.
Si dudas entre **publicar** y **preguntar** → gana **preguntar**.
