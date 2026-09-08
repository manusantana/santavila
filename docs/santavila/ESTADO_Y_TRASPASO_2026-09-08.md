# ESTADO Y TRASPASO · 8 de septiembre de 2026

> **Este es el documento que hay que leer primero.** Cierra la sesión de producción de imagen y
> deja por escrito el estado verificado, lo que queda y de quién es cada cosa.
>
> Todas las cifras de aquí están **verificadas contra la Admin API el 08-09-2026**, no estimadas.
> Donde una cifra contradice a otro documento del repo, manda esta y se dice cuál corregir.

---

## 1 · Lo primero: tres cosas que necesitan a Sergio

### 1.1 ⛔ Cinco fichas ACTIVE que el cliente NO puede ver — 6.091,95 €

Están en `ACTIVE`, tienen galería terminada y **no están publicadas en ningún canal de venta**:
`publishedAt = null`, `resourcePublicationsCount = 0`, sin `onlineStoreUrl`. En la web dan 404.

| Precio | Ficha | Imágenes |
|---|---|---|
| 2.815,00 € | `balliu-cama-balinesa-exterior-aluminio-estilo-minimalista-198-cm-dcaf71d8` | 5 |
| 1.999,00 € | `balliu-cama-balinesa-exterior-aluminio-estilo-sofisticado-160-cm-2bd3a7a4` | 5 |
| 685,00 € | `balliu-sofa-exterior-3-plazas-aluminio-estilo-contemporaneo-77-cm-674ab9a1` | 13 |
| 525,00 € | `balliu-sofa-exterior-3-plazas-aluminio-estilo-elegante-62-cm-5e2ef268` | 16 |
| 67,95 € | `balliu-mobiliario-exterior-resina-28-cm-6264905d` | 8 |

**No se han tocado**: publicar un producto es una decisión de negocio, no de producción de imagen.
No hay ni una línea en el JOURNAL que explique por qué están así, así que **no se sabe si fue
deliberado**. Dos de ellas se retocaron el 07-09 sin que nadie notara que apuntaban a ninguna parte.

**Qué hace falta:** que Sergio diga si se publican o se quedan así — y que la respuesta se anote
aquí, aunque sea «déjalas».

### 1.2 ⛔ La funda que enseña otro producto — 37 €

`balliu-funda-protectora-exterior-acrilico-a1c16324`. El SKU, el CSV y las dos tarifas dicen
**funda de PARASOL**; la imagen publicada muestra una **funda de TUMBONA**.

No se ha corregido porque **no existe ninguna foto real de ese producto**: el catálogo solo
ilustra la funda de tumbona (pág. 160) y la única imagen original de la ficha se borró al publicar
la galería nueva. Generarla sería inventar el producto, y eso lo prohíbe la Ley 0.

Es la **única ficha del catálogo con 2 imágenes**, dejada así a propósito para no reforzar el
error con una tercera toma. Detalle en
[`PENDIENTES_PROVEEDOR.md` §4.3](PENDIENTES_PROVEEDOR.md).

**Qué hace falta:** pedir la foto a Balliu, y decidir si mientras tanto pasa a DRAFT.

### 1.3 Los 17 commits siguen sin subir

`main` está **17 commits por delante de `origin/main`**. El push no se pudo hacer desde la sesión:
primero por falta de credenciales en el entorno y después porque la acción quedó bloqueada por
permisos. **Hay que hacerlo a mano desde una terminal normal:**

```bash
cd "/Users/sergio/Personal/19 - IA/00-Google Antigravity/12 - ULP Santavila"
git push origin main
```

Mientras no se haga, dos jornadas de trabajo viven solo en este portátil, en contra de la regla
del proyecto de que **git es la fuente de verdad**.

---

## 2 · Estado verificado del catálogo

| | |
|---|---|
| Productos totales | **241** — 171 ACTIVE, 70 DRAFT, 0 archivados |
| ACTIVE por proveedor | Hevea **111** · Balliu **60** |
| ACTIVE sin coste | **0** — la regla «publicar exige coste» se cumple al 100 % |
| ACTIVE sin imagen | **0** |
| ACTIVE con menos de 3 imágenes | **1** (la funda de parasol del §1.2, a propósito) |
| Alt vacíos en ACTIVE | **0** de 890 media |
| Posición 0 que no sea imagen | **0** |
| Violaciones de reglas de marca | **0** + 1 excepción aceptada (§5.2) |
| Variantes ACTIVE | 1.463 · **0 sin coste, 0 por debajo de coste, 0 con margen < 15 %** |

### Resolución de imagen — el frente que queda abierto

| | Fichas con TODAS sus imágenes ≥ 2.000 px |
|---|---|
| **Hevea** | **111 de 111** — cerrado |
| **Balliu** | **10 de 60** |

**50 fichas de Balliu** tienen alguna imagen por debajo de 2.000 px (337 imágenes, 294 de ellas
por debajo de 1.000 px; las peores a 401 y 410 px). **Esto es esperado, no un fallo**: es la
consecuencia aceptada de la decisión del 22-08 (ver §4).

> **Cuidado con el importe.** Circulan tres cifras para ese lote: 20.130 €, 17.699 € y 16.979 €.
> La de 20.130 € es la suma del **precio máximo de variante**; por **precio de entrada son
> 16.933,60 €**. Lo único sólido y en lo que todas las fuentes coinciden es **el recuento: 50 fichas**.

### Contexto que cambia la lectura de todo lo demás

**La tienda tiene 0 pedidos.** Nadie ha comprado la funda con la foto equivocada: no hay daño
consumado ni cliente al que avisar. Todo lo marcado como urgente es **riesgo prospectivo**. Pero
también significa que ni el trabajo de imagen ni el de GEO tienen todavía ninguna señal de
conversión que los valide.

---

## 3 · Qué se hizo en esta sesión

1. **Mesa Córcega** (720 €) — cierra el frente Hevea. Se rechazó el primer par: el aislado sobre
   bone había convertido el **tablero HPL opaco en un cristal transparente**.
2. **Auditoría profunda** — el informe decía 0 violaciones y **había 2**: comida en la ficha más
   cara del catálogo (4.405 €) y un vídeo con bebida, ambos invisibles para el auditor.
3. **Las 9 fichas cortas suben a 3 tomas** — 8 publicadas; la novena es la funda del §1.2.
4. **Auditor reforzado** — ahora pide vídeos, tiene lista ampliada, cruza por nombre de fichero y
   usa `curl` en lugar de `urllib`.
5. **Dos claims retirados** — «impermeable» en dos alt nuestros: el catálogo dice *«tejido acrílico
   resinado»* y *«protección eficaz contra la lluvia»*, que no es lo mismo.
6. **El publicador, desarmado** — `ACTIVA = {}` (ver §5.1).

---

## 4 · Balliu: por qué sus fichas tienen fotos pequeñas

**No es trabajo sin terminar, es una decisión tomada** (Sergio, 22-08-2026).

Una ficha de Balliu puede tener hasta **96 combinaciones** de color, chasis y tejido, y sus fotos
pequeñas **son** las fotos de variante: la única información real de acabado que existe. Si se
sustituyen por una galería generada, la ficha gana belleza y **pierde justo lo que el cliente
necesita para elegir**.

Por eso se eligió **añadir** en vez de sustituir: 1–2 tomas nuevas al principio (las que venden en
el listado) y **las fotos de acabado del proveedor intactas**. Las 49 fichas de la Fase 3 están
hechas así.

**Consecuencia asumida:** esas fichas no cumplen «todas las imágenes ≥ 2.000 px», y no pasa nada —
ese criterio se hizo para fichas de un solo acabado.

---

## 5 · Cómo continuar sin romper nada

### 5.1 El publicador está desarmado a propósito

`scripts/publicar_galeria_producto.py` tiene **`ACTIVA = {}`**. Dejarlo apuntando a la última
tanda era una mina: un `--apply` **sin** `--anadir` borra todos los media previos, y las 8 fichas
de `GALERIAS_TERCERA_TOMA` declaran **un solo fichero** cada una → se quedarían con una única
imagen, que además es una hoja de medidas. **El dry-run no avisa de eso.**

Para publicar: crea un dict **nuevo** y apunta `ACTIVA` ahí. Nunca reactives uno antiguo.

```bash
python3 scripts/publicar_galeria_producto.py                 # dry-run (por defecto)
python3 scripts/publicar_galeria_producto.py --anadir         # dry-run del modo aditivo
python3 scripts/publicar_galeria_producto.py --anadir --apply # publica conservando lo existente
python3 scripts/publicar_galeria_producto.py --verificar      # integridad de todos los dicts
python3 scripts/auditar_reglas_galeria.py --reglas            # reglas de marca (pásalo SIEMPRE)
```

### 5.2 La excepción aceptada

El vídeo del set Leisa (2.899 €) **muestra una bebida fría**, lo que incumple la regla de atrezzo
del 03-08-2026. Sergio decidió el 07-09 **conservarlo y reescribir solo el alt**.

Como al cambiar el alt el auditor deja de verlo, **la excepción está registrada en el código**
(`scripts/auditar_reglas_galeria.py`, dict `EXCEPCIONES`) y el informe la imprime cada vez. No es
un descuido: es una decisión, con su fecha.

### 5.3 Los puntos ciegos que le quedan al auditor

Conviene saberlos antes de fiarse de un «0 violaciones»:

- `media(first:16)` — una ficha con 17 media nunca se audita entera.
- La detección de fotos compartidas **no normaliza el UUID de Shopify**: comparando URLs exactas
  da 0, pero normalizando salen **45 ficheros repartidos en 28 fichas ACTIVE**.
- El auditor filtra por `status:active`, así que **los 387 media de los DRAFT nunca han pasado por
  las reglas de marca** (358 de ellos con el alt vacío).

---

## 6 · Pendientes, por dueño

### 6.1 De Sergio

| Urgencia | Qué |
|---|---|
| **Alta** | Decidir las **5 fichas invisibles** (§1.1) y **la funda de parasol** (§1.2) |
| **Alta** | **Hacer el push** de los 17 commits (§1.3) |
| Media | Decidir si se cierra el frente Balliu (50 fichas, ~350–420 créditos; quedan **453**) |
| Media | Decidir la regla de tomas por ficha: el SKILL exige **5**, la producción real usa **3** (§6.4) |
| Media | Qué se hace con los **46 DRAFT de Balliu** con coste y ≥3 fotos pero sin resolución ni alt |
| Media | Pedir a los proveedores los **EAN/GTIN** ya preparados en `docs/santavila/ean-request/` (1.351 + 112 variantes; hoy **0 variantes tienen barcode**) |
| Media | Conseguir el **coste de 15 DRAFT** que no lo tienen (14 de vendor santavila + 1 parasol Balliu con 64 variantes) |
| Baja | Higiene del repo: `.git` pesa 959 MB en objetos sueltos (`git gc`), y decidir si `images_generated/` (563 MB) pasa a Git LFS |

### 6.2 Del compañero de GEO/SEO

> Recordatorio de la frontera: **los títulos y las descripciones son suyos**; nosotros llevamos las
> imágenes y sus textos alternativos. Nada de esto se ha tocado.

| Urgencia | Qué |
|---|---|
| **Alta** | **14 `seo.title` obsoletos que contradicen al H1**: dicen una medida distinta a la que el cliente lee en la ficha (45×45 vs «60 cm», 48×48 vs «54 cm», «HPL · Brunei» vs «80×80 cm»…). En dos sofás el título perdió «3 plazas» y solo el `seo.title` lo conserva |
| Media | Terminar el retitulado del 29-08: **13 títulos** conservan la enumeración vieja y **11 acaban en un dígito suelto** (un desambiguador interno que sale tal cual en el SERP y en el feed de Merchant). Sobrevivieron porque el filtro fue «> 70 caracteres» y miden 64-69 |
| Media | **101 descripciones no nombran ningún material.** Es lo que busca el cliente («sofá exterior aluminio», «tumbona resina») y afecta a piezas de 4.000 €. El dato está en nuestros alt y en el catálogo: no hay que inventar nada |
| Media | Quitar el bloque de **UV / almacenamiento en invierno** de las **3** fichas que aún lo llevan |
| Media | La **FAQ de `mesa-comedor-exterior-hpl-13590-cm`** responde «esta mesa mide 160 cm… 160-180 para 6», pero la ficha tiene **dos tamaños**: a quien compre la de 135 se le está recomendando para 6 comensales |
| Media | Decidir qué hacer con los **45 ficheros de proveedor compartidos entre 28 fichas ACTIVE** (parasoles Ágora en 3 fichas, sillas Etna que además comparten `seo.title` exacto). Se canibalizan en Google Imágenes. Nota buena: **0 packshots compartidos en posición 0** |
| Media | Rellenar los **358 alt vacíos de los DRAFT** antes de publicar ninguno |
| Baja | Retomar su ciclo GEO: delta GSC (previsto ~13-sep), Wikidata, Bing Webmaster + IndexNow, LinkedIn de empresa |

**Corrección importante para él:** en el JOURNAL se dijo que había **~200 descripciones** con
claims no sostenibles. Verificado con regex sobre las 171 descripciones: son **3**. Lo que sí
existe, y es mayor, son las **101 sin material declarado**.

### 6.3 Del proveedor

- **Balliu:** foto de la funda de parasol acrílica, y **las medidas de las cinco fundas** — no
  existen en el CSV, ni en las dos tarifas, ni en el catálogo (§4.4 de `PENDIENTES_PROVEEDOR.md`).
- **Hevea:** el parasol «Ocean tela» (382 €) sigue siendo la única ficha con la primera imagen en
  baja (800 px), pendiente de material en alta.

### 6.4 Del siguiente chat

| Qué | Por qué |
|---|---|
| Llevar al SKILL de proyecto y al portable las dos lecciones del 08-09: **«para el acabado manda la foto, no el texto de la ficha técnica»** y **«un grep devuelve líneas, no relaciones»** | El SKILL dice hoy «si dos fuentes discrepan manda el catálogo» justo donde la lección dice lo contrario. Falta el matiz: **cotas → manda el catálogo; material y acabado → manda la foto** |
| Añadir al SKILL el criterio de la tercera toma: **peso** cuando el dato que decide no son los cm, **detalle de feature real** cuando no hay cota | Es el criterio que se acaba de usar en 8 fichas y no está escrito |
| Arreglar los tres puntos ciegos del auditor (§5.3) | Producen la misma falsa seguridad que ya costó cara con los vídeos |
| Actualizar los documentos con datos caducos: `PUNTO_DE_INFLEXION_2026-08-20.md` (sus 4 cifras ya no valen), la cabecera de versión del SKILL, y los contadores de dicts/ficheros | Se usan para estimar créditos: quien planifique con ellos pedirá el triple |
| Eliminar el `GALERIAS_FASE2` muerto (hay **dos dicts con el mismo nombre**; el segundo pisa al primero) | Quien lea el primero y escriba `ACTIVA = GALERIAS_FASE2` publicará el segundo sin saberlo |
| Unificar el criterio escrito de los 2.000 px: `ROL_FOTOGRAFO_SENIOR.md` dice **lado mayor**, el JOURNAL dice **lado menor** | Hoy dan el mismo resultado; en cuanto entre una imagen apaisada, darán dos números |

---

## 7 · Mapa de documentos

| Documento | Para qué |
|---|---|
| **este fichero** | estado y traspaso — el punto de entrada |
| [`JOURNAL.md`](JOURNAL.md) | bitácora cronológica inversa; una entrada por hito |
| [`PLAN_CIERRE_IMAGEN.md`](PLAN_CIERRE_IMAGEN.md) | las fases 0–3 de producción de imagen y su presupuesto medido |
| [`AVISOS_CATALOGO_2026-09-07.md`](AVISOS_CATALOGO_2026-09-07.md) | lo que hay que preguntar al proveedor o al compañero |
| [`PENDIENTES_PROVEEDOR.md`](PENDIENTES_PROVEEDOR.md) | lista viva para llamar a Balliu |
| [`ROL_FOTOGRAFO_SENIOR.md`](ROL_FOTOGRAFO_SENIOR.md) | el oficio: leyes, pilares, las 5 tomas, QA |
| `.claude/skills/santavila-imagen-producto/` | el skill de proyecto — la capa de acción |
| `skills-exportables/foto-producto-ia/` | el mismo oficio, genérico y sin marca, para otros proyectos |

**Coste medido:** 4,12 créditos por imagen publicada. Una ficha de 3 tomas ≈ 8–12 créditos.
**Saldo al cerrar: 453 créditos.**
