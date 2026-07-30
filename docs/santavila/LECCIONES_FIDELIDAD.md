# Lecciones del incidente de fidelidad (2026-07-29/30)

> Este documento existe porque **el dueño tuvo que detectar tres veces seguidas fallos que yo había dado por
> buenos**. No es un post-mortem técnico: es la lista de creencias equivocadas que me llevaron a publicar
> imágenes que no representaban el producto. Se lee **antes** de generar, junto al skill.

---

## 1 · El fallo no fue del modelo. Fue de método.

El modelo hizo lo que hacen los modelos: rellenar huecos. **Yo era la única garantía de fidelidad y fallé
como garantía.** Cada vez que dije "ya está verificado", lo que había hecho era mirar miniaturas.

**Regla:** a tamaño tira no se distingue una lama de una veta, ni un gris cemento de un gris claro, ni un
jacquard de un liso. **Verificar significa ampliar a resolución nativa.** Si no has ampliado, no has
verificado — y entonces no puedes decir que está bien.

---

## 2 · Las cinco creencias equivocadas que causaron todo

| Creía | La realidad |
|---|---|
| "El tablero de la mesa es parte del bodegón" | **Es producto.** Y en el ASMR del consumible ocupa el 70 % del encuadre: es la mayor superficie de producto de toda la galería |
| "Mi packshot sirve de referencia para corregir" | **El packshot también puede estar mal.** Si lo está, arrastra el error a las 5 imágenes. La referencia es SIEMPRE la foto del proveedor |
| "El nombre de la carpeta identifica el producto" | **No identifica nada.** La carpeta `albania` se publicó en la ficha del Bellagio 3 pl. Cinco fotos de otro mueble, días en producción |
| "El riesgo está en inventar texturas" | **También en quitarlas.** El tapizado del Brandon lleva jacquard estampado y lo publiqué liso en 3 fichas |
| "Si el cliente quiere ver el herraje, hay que enseñarlo" | **Si no se ve en la foto real, no existe.** Inventé los grilletes del balancín — justo el detalle en el que el cliente se apoya para juzgar calidad |

---

## 3 · Lo que aprendí sobre auditar

**3.1 · Cada vez que miré con más rigor, apareció algo nuevo — y siempre en el componente que no estaba
mirando.** Primero el tablero. Luego la trama del tejido. Luego el color. Luego la identidad del producto.
Un "está todo bien" que sale de haber mirado un solo componente no vale nada.

**3.2 · Un informe honesto separa lo verificado de lo no verificado.** Dije "1 fallo, 20 correctas" cuando
lo cierto era "1 fallo, 20 con el tablero comprobado y todo lo demás sin mirar". La diferencia no es
matiz: es la diferencia entre información y falsa tranquilidad.

**3.3 · La duda se resuelve ampliando, no borrando.** Retiré 5 imágenes correctas del Manhattan 3 pl. por un
fallo que no existía (creí que faltaban los cojines estampados; estaban, y yo miraba el ASMR de chasis).
Precipitarse a retirar también hace daño.

**3.4 · El conteo de piezas se audita en el PACKSHOT, no en un detalle.** Un ASMR de reposabrazos no tiene
por qué mostrar los cojines decorativos. Confundir eso genera falsos positivos.

**3.5 · El fallo puede estar en toda la galería, no solo en el ASMR.** En Diva 2 pl. y Yina 3 pl. el material
estaba mal **ya en el packshot**. Al detectar un fallo hay que preguntarse siempre: *¿en cuántas de las 5?*

**3.6 · Un export de datos no es la fuente de verdad.** El CSV me dio la foto de otro producto para un
handle. Las originales estaban en `images_optimized/` y `images_balliu/` del propio repo, y en el CDN de
Shopify. **Antes de declarar algo "no verificable", hay que buscarlo de verdad.**

---

## 4 · Errores de ejecución que cometí durante la propia corrección

1. **Corregí contra mi packshot en vez de contra la foto real** → la corrección heredó el error de tono y
   hubo que retirarla otra vez. Segundo fallo en la misma imagen.
2. **Repuse la foto del proveedor y luego la borré** con un filtro `*` demasiado amplio: cuatro fichas se
   quedaron unos segundos sin ninguna imagen. Orden correcto: **borrar primero, reponer después**, o excluir
   explícitamente lo que acabas de subir.
3. **Publiqué sin comparar el packshot con la foto real del handle destino.** Diez segundos de comprobación
   habrían evitado el fallo más grave de todos.

---

## 5 · Las puertas que ahora existen en el skill

| Puerta | Qué obliga |
|---|---|
| **PASO 0 · Ficha de verdad** | Escribir material · tono · acabado · canto leyendo el píxel a resolución nativa **antes** del primer job. Sin ficha, no se genera |
| **PASO 0.bis · Identidad** | Comparar el packshot con la foto real **del handle destino** antes de publicar |
| **NO DETERMINADO** | Lo que no se ve con certeza no se deduce: se marca, y **la toma en la que aparecería no se hace** |
| **QA contra la ficha** | Nunca contra el packshot propio |
| **§15 en los dos sentidos** | Ni inventar tramas ni quitarlas |
| **Superficies horizontales** | El tablero es producto: material, tono, acabado y canto, los cuatro |

---

## 6 · La frase que resume el estándar

> **Si no existe, no lo hago. Si no sé hacerlo, no lo hago. Si no lo puedo verificar, no lo publico.**

No es una aspiración de calidad: es el mínimo. Una imagen de producto es una **afirmación sobre un objeto
que alguien va a pagar**. Una textura inventada, un tono desviado o un herraje que no existe no son
"licencias creativas": son datos falsos sobre lo que el cliente recibirá en su casa.
