# PLAN DE CIERRE · imagen de producto

> Redactado el 22-08-2026 con **1.007 créditos** disponibles y el catálogo medido ese día.
> Coste unitario usado: **4,12 créditos por imagen publicada** (medido, no estimado: 268 créditos
> / 65 imágenes en la jornada anterior).

## Punto de partida

| | Fichas | Valor |
|---|---|---|
| Con galería completa (≥3 img, todas ≥2.000 px) | **106** | — |
| **A** · pendientes (≤2 imágenes) | **14** | 2.764 € |
| **B** · con galería pero en baja resolución | **51** | 17.699 € |
| **Total ACTIVE** | **171** | |

---

## FASE 0 · Limpieza sin coste — **HECHA** (22-08-2026) · 0 créditos

**150 imágenes duplicadas borradas.** Balliu pasa de **523 a 373 imágenes**; ninguna ficha se
quedó sin fotos y la que más tiene ahora son 15 (antes 75).

| | Antes | Ahora |
|---|---|---|
| Mesa Brunei 80×80 | 75 imágenes | **15** |
| Mesa Capri 70×70 | 52 imágenes | **10** |
| Silla resina | 12 | 5 |

### La lección: el nombre no basta, hay que hashear
El primer criterio fue *"mismo nombre de fichero + mismas dimensiones"*. Parecía seguro y daba 57
duplicados. Al verificar por **MD5 del contenido real**, **7 de esos 57 eran imágenes DISTINTAS**
con el mismo nombre y el mismo tamaño (`397-CAPRI`, `180-CAPRI-scaled`, `DSC_0360-scaled`,
`jmf2012_jml1499-scaled`). Se salvaron por haber comprobado.

**Solo se borra con hash de fichero idéntico. Nunca por nombre.**
Herramienta: `scripts/borrar_duplicados_balliu.py` (dry-run por defecto).

---

## FASE 0 · planteamiento original

**57 imágenes duplicadas** en 22 fichas de Balliu: la misma foto subida varias veces con distinto
sufijo de Shopify. Una mesa llega a tener **18 duplicados de 25 imágenes**.

Verificado antes de tocar nada: **ninguna variante tiene imagen asignada** (0 de 20 en la ficha
peor), así que borrar duplicados no rompe ninguna variante.

**Se hace primero porque mejora fichas sin gastar un crédito** y porque reduce el ruido antes de
decidir nada sobre Balliu.

---

## FASE 1 · Grupo A — **CERRADA** (07-09-2026) · 14 fichas, ~120 créditos

**Las 14 publicadas.** El catálogo pasa de 106 a **120 fichas con todas sus imágenes ≥2.000 px**.
De Hevea solo queda la mesa Córcega (Fase 2). Coste real: ~120 créditos frente a los 82
presupuestados — la diferencia son tres regeneraciones por control de calidad y dos upscales
que hubo que relanzar.

### Dos piezas fantasma cazadas en el catálogo ANTES de generar
- **LOSAS DE CEMENTO (218 €).** Su foto sale con la base de ruedas **y** el mástil del parasol.
  El catálogo lo dice tres veces —*"(Las losas se venden por separado)"*, *"(No incluye losas)"*—
  y en la pág. 101 las lista como producto propio: **JUEGO 4 LOSAS, 25 kg cada una, COD LS210**.
  Se dibujan **solo las cuatro losas**, y la toma 5 lo declara por escrito.
  Aquí **el dato que decide la compra no son los centímetros: es el PESO** — justo el caso que
  el skill portable recoge.
- **TABURETE ETNA (187 €).** Su foto sale con una mesa alta que no se vende. Aislado.

### Una imagen rota, rescatada
La **silla Janeiro (200 €)** venía de un recorte con artefactos azules pegados. El producto sí era
legible, así que se reconstruyó el packshot. Su ambiente se **rechazó** por aclarar el textilene
(pixeles de estructura a L=59 frente a L=85 del packshot) y se regeneró nombrando el color:
**R−B +5,2 frente a +5,0**. Sin cota fiable en catálogo, **no lleva ficha de medidas**.

### Un fallo de tipografía, detectado y corregido
La primera ficha de medidas de las losas salió en **Menlo** en vez de JetBrains Mono:
`ficha_medidas_set.py` tenía `/tmp` **fijo** y en un entorno con sandbox no es escribible, así que
la conversión de la fuente fallaba **en silencio**. Corregido para usar `TMPDIR`.

### Planteamiento original

Al mirarlas de una en una, **8 de las 14 ya tienen packshot en alta**: no necesitan packshot, solo
ambiente y la toma 5.

| Sub | Fichas | Qué necesita | IA/ficha | Créditos |
|---|---|---|---|---|
| **A1** · ya tienen packshot ≥2.000 px | 8 (910 €) | ambiente + toma 5 | 1 | 33 |
| **A2** · material en baja (614–1.024 px) | 6 (1.855 €) | packshot + ambiente + toma 5 | 2 | 49 |

**A2** — las de más valor: mesa de centro 125 (569 €), reposapiés 85×50×43 (400 €), mesas de
centro 90 y 120 (339 y 323 €), taburete Etna (187 €), funda acrílica (37 €).

**Tres avisos ya detectados:**
- `set-losas-cemento` — el CSV le asigna **la foto de otro producto**. Verificar antes de generar.
- `silla-exterior-estilo-estilizado` (silla Janeiro) — la imagen del catálogo salió a **167×216 px**.
- Las **4 fundas**: un objeto textil amorfo es de lo más difícil de fotografiar. Presupuestar un
  reintento extra.

**Resultado:** cierra el frente Hevea por completo. Ninguna ficha con ≤2 imágenes.

---

## FASE 2 · La mesa Córcega — **CERRADA** (07-09-2026) · ~20 créditos

`mesa-comedor-exterior-hpl-13590-cm` (720 €), la **única Hevea** del grupo B. Con ella **el
frente Hevea queda cerrado del todo**.

Costó el doble de lo presupuestado por una razón que merece quedar escrita: el packshot aislado
sobre bone **convirtió el tablero HPL opaco en un cristal transparente** apoyado encima del
marco, y el ambiente heredó el mismo fallo. Se vio comparando el canto **a tamaño real** contra
la foto del proveedor —en la miniatura no se aprecia— y se corrigió nombrando material y
construcción en el prompt: *"opaque matte compact laminate, never glass"* + *"sits flush INSIDE
the aluminium frame"*.

También salieron **seis sillas fantasma** en las tres fotos del proveedor, y una altura que no
se pudo escribir: ver [`AVISOS_CATALOGO_2026-09-07.md`](AVISOS_CATALOGO_2026-09-07.md).

---

## FASE 3 · BALLIU — no es "más de lo mismo" · **decisión pendiente**

**50 fichas · 17.699 €.** Aquí la estrategia de Hevea **no se puede copiar**, y conviene verlo
antes de gastar:

### Por qué es un problema distinto

| | Hevea | Balliu |
|---|---|---|
| Variantes por ficha | 1 acabado | **hasta 96 combinaciones** |
| Fichas con eje de color/chasis/acabado | pocas | **43 de 51** |
| Qué enseñan sus fotos pequeñas | el producto | **los acabados reales** |
| Fórmula de composición en catálogo | sí | **no** (212 págs, cero) |
| ¿El catálogo tiene fotos mejores? | sí, a veces | **no**: máx. 1.119 px |

Ejemplos reales: tumbonas con **Ruedas(2) × Chasis(3) × Color tejido(16) = 96 combinaciones**;
mesas con **Tamaño(4) × Chasis(3) × Tablero(5) = 60**.

**El choque con nuestra propia ley.** *"Variante = su propia foto; si no hay foto de esa variante,
no se genera esa variante."* Las fotos de 800 px de Balliu **son** las fotos de variante. Si se
sustituyen por una galería generada, la ficha gana belleza y **pierde la información de acabado**
—que es justo lo que el cliente necesita para elegir—.

Generar un packshot por acabado serían 150–250 imágenes: **600–1.000 créditos** solo en packshots,
y aun así no cubriría los 16 colores de tejido de una tumbona.

### Las tres salidas

| | Qué se hace | Créditos | Qué gana | Qué pierde |
|---|---|---|---|---|
| **1 · Añadir** | 1–2 tomas de ambiente premium **al principio**, conservando las fotos de acabado | **210–420** | la primera imagen vende; se conservan las variantes | la ficha sigue teniendo fotos pequeñas dentro |
| **2 · Sustituir** | galería nueva de 3–4 tomas, se borra lo viejo | 420–630 | fichas homogéneas y en alta | **se pierde la información de acabado** |
| **3 · Pedir al proveedor** | correo a Balliu con las fotos en alta | **0** | material real de todas las variantes | depende de ellos; puede tardar o no llegar |

**DECIDIDO (Sergio, 22-08-2026): opción 1 — añadir ambiente y conservar los acabados.**
No se espera al proveedor. Por ficha se añaden **1–2 tomas nuevas al principio** (el ambiente que
vende en el listado, y packshot limpio donde haga falta) y **las fotos de acabado del proveedor se
quedan intactas**, aunque sean de 800 px: son la única información real de variante que existe.

Consecuencia asumida: estas fichas **no van a cumplir el criterio de "todas las imágenes ≥2.000
px"**, y no pasa nada — ese criterio se hizo para fichas de un solo acabado. Aquí el objetivo es
otro: **que la primera imagen venda, sin que el cliente pierda de vista los colores**.

*(Pedir el material en alta a Balliu sigue mereciendo la pena en paralelo: es gratis y, si llega,
convierte estas fichas en galerías completas de verdad.)*

---

## FASE 3 · **CERRADA** (07-09-2026) — 49 de 50 fichas · ~305 créditos

**La tienda pasa de 120 a 170 fichas (de 171) con la primera imagen en alta.** Se publicaron en
ocho tandas, con packshot + ambiente por ficha y conservando las fotos de acabado del proveedor.

Solo queda fuera **a propósito** el parasol «Ocean tela» (382 €): su título dice redondo y sus
fotos son de un parasol cuadrado. No se inventa la forma de un producto.

### Lo que Balliu enseñó y Hevea no

**1 · La resolución no elige el ancla; lo hace ver la pieza.** Tres veces la foto de más píxeles
no era del producto: en la mesa alta era **solo el pie** (2.480 px), en el pie de parasol eran
**tres adaptadores de mástil** (2.312 px), y en la Eva Pro T era **otro producto**. Vale más una
foto de 800 px que enseña la pieza entera.

**2 · El ambiente se ancla al packshot ya validado, no a la foto del proveedor.** Generando los
dos a la vez desde el original de 800 px, fallaba **uno de cada cuatro**: la tumbona Iris perdió
su bastidor arqueado, la mesa Altea aclaró su tablero topo a beige y perdió el canto negro. Con
el flujo en dos pasos —packshot, validar, y de ahí el ambiente— la tanda D salió con **cero
regeneraciones**.

**3 · El conteo 1:1 también vale para listones y para tramas.** El modelo ensanchó los listones
de la mesa Atlanta (12 en vez de 30 y pico) y le inventó a la colchoneta un **acolchado en
rombos** cuando el original tiene costuras rectas. Se arreglan nombrando el rasgo en el prompt.

**4 · La pieza de más también la inventa el modelo.** Dos ambientes duplicaron el producto —una
tumbona de teca, una silla— siendo fichas de una sola unidad. Y en un caso la segunda salía
**cortada por el borde**: cortada también cuenta.

**5 · Un producto que se usa sobre otro se fotografía sin el otro.** La colchoneta de tumbona va
sobre un poyete de obra, no sobre una tumbona que no se vende.

**6 · El auditor de reglas tiene un punto ciego.** Solo mira los ALT, y las fotos de Balliu
tienen alt genéricos («vista 3»). Una foto con comida y ese alt le pasa desapercibida: se
encontraron dos —un bodegón de fruta y unas manzanas sobre una mesa— **mirándolas**, no
auditándolas. Ambas retiradas.

### Coste real

~305 créditos para 49 fichas ≈ **6,2 créditos por ficha**, por debajo de los 8,4 que salían de
las dos tomas a 4,12. Saldo tras la fase: **487 créditos**.

---

## Presupuesto

| Fase | Presupuestado | **Real** |
|---|---|---|
| 0 · duplicados | 0 | **0** |
| 1 · grupo A (14 fichas) | 82 | **~120** |
| 2 · mesa Córcega | 8 | **~20** |
| 3 · Balliu (49 fichas) | 210–420 | **~305** |
| **Total** | 300–510 | **~445** |

**Saldo: 1.007 → 487 créditos.** Dentro de lo previsto: la fase 3 salió incluso barata (6,2
créditos por ficha frente a los 8,4 teóricos), y lo que se desvió fueron las fases 1 y 2, donde
las regeneraciones por control de calidad pesaron más que el volumen.

---

## Orden de ejecución

1. **Fase 0** — duplicados (0 créditos, mejora inmediata)
2. **Fase 1 A2** — las 6 de más valor del grupo A
3. **Fase 1 A1** — las 8 que solo necesitan ambiente
4. **Fase 2** — mesa Córcega → *aquí el frente Hevea queda cerrado con ~90 créditos*
5. **Fase 3** — Balliu, según la decisión

Tras cada fase: `auditar_reglas_galeria.py` y commit. Sin excepción.

---

## Lo que queda (07-09-2026)

1. **Parasol «Ocean tela»** (382 €) — en cuanto Balliu diga si es redondo o cuadrado.
2. **Altura de la mesa Córcega** — en cuanto Hevea la confirme, se añade a su ficha de medidas.
3. **Fotos en alta a Balliu** — sigue mereciendo la pena pedirlas: es gratis, y convertiría estas
   50 fichas en galerías completas de verdad en vez de "primera imagen premium + acabados
   pequeños detrás".
4. Los avisos de catálogo del compañero: [`AVISOS_CATALOGO_2026-09-07.md`](AVISOS_CATALOGO_2026-09-07.md).

Herramientas nuevas de esta fase:
- `scripts/inventario_balliu.py` — qué fichas tienen la primera imagen en baja (filtra vídeos).
- `scripts/anclas_balliu.py` — propone el packshot de proveedor de cada ficha por blancura del borde.
- `scripts/ver_ficha_balliu.py` — mosaico numerado de TODA la galería de una ficha.
- `publicar_galeria_producto.py --anadir` — publica conservando los media del proveedor.
