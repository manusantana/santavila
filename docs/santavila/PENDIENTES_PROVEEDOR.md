# Pendientes de confirmar con el proveedor (Balliu)

> Documento vivo. Acumula todos los productos / variantes / precios que durante la consolidación del catálogo no han podido confirmarse contra la web del proveedor o el Excel y necesitan validación manual con Balliu antes de pasar a venta.
>
> **Cómo usar:** llamar/escribir a Balliu con esta lista. Cuando se confirme un punto, marcar con `✅` y pasar el producto correspondiente de DRAFT a ACTIVE (o eliminarlo definitivamente si está descontinuado).

---

## Convención de DRAFT en Shopify

Productos en estado DRAFT con tag `pendiente-confirmar-proveedor` son los que aparecen aquí. Filtro en Shopify Admin:

```
status:draft tag:pendiente-confirmar-proveedor
```

---

## 1. HPL Gran Densidad — ¿existe / se sigue fabricando?

La web del proveedor en 2026-05 **no muestra** "HPL Gran Densidad" (HPL GD) como tablero seleccionable en ningún modelo. Sin embargo el Excel `Santavila.xlsx` tiene SKUs HPL GD para muchos modelos a precios coherentes. Hay que confirmar si HPL GD:

- (a) sigue disponible bajo demanda (no se muestra en web pero se puede pedir),
- (b) está descontinuado,
- (c) ha sido renombrado.

**Modelos afectados (todos en DRAFT con tag `pendiente-confirmar-proveedor`)**:

| Modelo | Producto DRAFT en Shopify | Variantes/precios |
|---|---|---|
| Mesa alta Capri Alta | `balliu-mesa-alta-exterior-hpl-f99491ce` y otros legacy | Ø70 HPL_GD 521,21€ · 60×60 HPL_GD 489,60€ · 70×70 HPL_GD 590,63€ |
| Mesa centro Etna | `mesa-de-centro-exterior-aluminio-hpl-gd-110x60` | 421,95€ |
| Mesa auxiliar Etna | `mesa-auxiliar-exterior-aluminio-hpl-gd-45x45-etna` | 175,06€ |
| Mesa auxiliar Olimpia Central | `balliu-mesa-auxiliar-exterior-aluminio-54-cm-9e2a2ecb` | 242,65€ |
| Mesa Brunei | `mesa-exterior-aluminio-hpl-gd-brunei` | 4 tamaños: 540,25 / 737,34 / 892,79 / 1.123,45 € |
| Mesa Java | `mesa-extensible-exterior-aluminio-hpl-gd-java` | 140/180×100: 1.593,26€ · 200/260×100: 2.296,36€ |
| Mesa Capri | `mesa-exterior-aluminio-hpl-gd-capri` | 5 tamaños: 387,59 – 442,82€ |
| Mesa Capri Doble | `mesa-exterior-aluminio-hpl-gd-120x80-capri-doble` | HPL GD 622,93€ + pie alto |
| Mesa Altea | `mesa-exterior-aluminio-altea-extras` | 70×70 HPL_GD 480,94€ · 80×80 HPL_GD 481,68€ · Ø80 HPL_GD 392,86€ |
| Mesa Ágata | `mesa-exterior-aluminio-agata-extras` | 120×80 HPL_GD 686,15€ |

---

## 2. Modelos no encontrados en la web del proveedor

### 2.1 Mesa Sofia (familia 3a)

Excel tiene **5 SKUs Sofia** (70×70 y 80×80, HPL y HPL_GD) pero la búsqueda en `balliuexport.com` devuelve "Nothing Found".

- ¿Sofia está descontinuado o ha sido renombrado?
- Si sigue activo, confirmar matriz: ¿tamaños 70×70 y 80×80? ¿chasis? ¿tableros HPL std + HPL_GD?

Productos DRAFT: `balliu-mesa-exterior-hpl-7070-cm-9d14e31f`, `-146f72ca`, `-f6074154`, `balliu-mesa-exterior-hpl-8080-cm-1a2fe7b5`, `-96593887`.

### 2.2 Mesa Ágata L (180×90 encimera aluminio)

Excel tiene Ágata 180×90 a 504,03€ pero la web solo muestra Ágata 75×75. La URL `/producto/mesa-de-aluminio-agata-l/` devuelve 404.

- ¿Ágata L 180×90 sigue disponible?
- ¿Hay otros tamaños grandes de Ágata?

DRAFT: `balliu-mesa-exterior-aluminio-75-cm-c0092e17` y variante en `mesa-exterior-aluminio-agata-extras`.

### 2.3 Olimpia Esquinera (familia 3d)

Excel tiene 2 SKUs Olimpia Mesa Auxiliar **ESQUINERA** (HPL y HPL_GD, 229,56€ / 254,64€) pero la web solo muestra **Central**.

- ¿La versión Esquinera sigue activa?
- ¿Precio actualizado?

DRAFT: `balliu-mesa-auxiliar-exterior-aluminio-54-cm-5ad43bf2` y `-2ad5a2df`.

### 2.4 Mesa Greta (familia 3d)

Excel tiene Mesa Greta (108,63€) pero no aparece en la web del proveedor.

- ¿Modelo descontinuado o renombrado?

DRAFT: `balliu-mesa-exterior-aluminio-9e30ca7f`.

### 2.4-bis Silla Greta (familia 5)

Excel tiene Silla Greta (r170, 155,06€) pero no aparece en la web del proveedor. Igual que la Mesa Greta — todo el modelo Greta parece descontinuado.

- ¿Toda la línea Greta está discontinuada?

DRAFT: `balliu-silla-exterior-aluminio-estilo-contemporaneo-afd89221`.

### 2.5 Mesa Atlanta 240×90 fija

Excel tiene Atlanta 240×90 fija HPL y HPL_GD (1.282,60 / 1.291,98€) pero la web solo muestra los modelos extensibles (140/180×90 y 200/260×100).

- ¿La versión 240×90 fija sigue activa?

DRAFT: `balliu-mesa-exterior-hpl-24090-cm-78358691` y `-d4e471c5`.

### 2.6 Etna Mesa Auxiliar — Werzalit Ø60

El Excel tiene una variante Etna Mesa Auxiliar con tablero Werzalit Ø60 (157,84€). La web actual solo muestra HPL standard (no Werzalit).

- ¿Werzalit Ø60 sigue disponible?

DRAFT: `mesa-auxiliar-exterior-aluminio-werzalit-60-etna`.

### 2.7 Capri Doble · pie alto

Excel tiene Capri Doble 120×80 con variante "pie alto" (HPL 605,18€ / HPL_GD 666,49€). La web menciona "single support base and double support base" pero no diferencia altura del pie.

- ¿La opción "pie alto" sigue ofreciéndose?

DRAFT: `mesa-exterior-aluminio-hpl-gd-120x80-capri-doble`.

### 2.8 Mesa alta Capri Alta — Ø70 (redonda)

Excel tiene 2 SKUs Mesa alta Ø70 HPL y HPL_GD (510,05 / 521,21€) pero la web actual solo muestra 60×60 y 70×70 cuadradas (sin redonda Ø70).

- ¿La mesa alta Ø70 sigue disponible?

DRAFT: `balliu-mesa-alta-exterior-hpl-45c511e9` y `-f99491ce`.

---

## 3. Precios — discrepancias Excel ↔ web

### 3.1 Olimpia mesa auxiliar tela

- **Excel**: 157,63 € (col F IVA, pestaña `20260508 -Todos `)
- **Web**: 149,34 €

Aplicamos el Excel en producción (decisión dueño 2026-05-17). Confirmar con proveedor cuál es el precio vigente.

### 3.1-bis Silla Bruna — SKU duplicado con 3 precios distintos

El SKU `BALLIU_BRUNA_SILLA_CON_BRAZ_94B6E5B5` aparece en Excel **dos veces** con precios muy distintos:

- fila 167: coste 55,51€ · PVP IVA 89,55€ (silla Bruna con brazos normal)
- fila 169: coste 122,56€ · PVP IVA **197,73€** (¡mucho más caro, no identificado!)

Y en Shopify hay 2 productos con ese SKU:

- `balliu-silla-exterior-con-brazos-resina-estilo-funcional-94b6e5b5` (€113,80 sin coste)
- `balliu-silla-exterior-con-brazos-resina-estilo-funcional-94b6e5b5-2` (€89,95 cost=55,51)

La web del proveedor solo muestra **Silla Bruna** a 70,81€ (sin brazos) y **Bruna con reposabrazos** a 84,19€. No hay variante a ~197€.

**Hipótesis**: ¿es una "Bruna L" o "Bruna XL" no documentada en web? ¿O el SKU está duplicado por error?

- Confirmar con proveedor si existe una variante "Bruna" a 197,73€ y qué es exactamente.

DRAFT: `silla-exterior-resina-bruna-precio-alto-pendiente` (nuevo) + los 2 duplicados Shopify (`94b6e5b5` y `-2`).

### 3.2 Mesa Altea 70×70 HPL standard

El Excel **no tiene** precio explícito para Altea 70×70 HPL standard (solo HPL_GD a 480,94€). La web muestra rango 421,43–481,68€.

Se ha aplicado 421,43€ a la variante 70×70 HPL standard (precio mínimo del rango web), pero es una asunción.

- Confirmar precio exacto.

### 3.3 Taburete Etna — Excel 186,62€ vs web 188,63€

Pequeña discrepancia. Se aplica Excel (186,62€) según decisión 2026-05-17, pero conviene confirmar precio vigente.

---

## 4. Otros puntos a verificar

### 4.1 SKU autogenerado `BALLIU_*_xxxxxxx`

El SKU `BALLIU_<MODELO>_<TIPO>_<HASH>` que aparece en `Santavila.xlsx` columna C es autogenerado por el importador Shopify, **no es el SKU real del proveedor**. Balliu identifica por (Producto + Variante + Grupo) según tarifas en PDF.

Importante recordar: **no enviar SKUs Shopify a Balliu en los pedidos**. Usar la descripción humana del modelo + variante.

### 4.2 Anomalía mesa alta — fila 222 Excel

La fila 222 del Excel (60×60 mesa alta) está marcada como `HPL_GD` en el SKU, pero su precio (456,69€ con IVA) corresponde a HPL standard (no HPL GD). Se trata como HPL standard en la consolidación.

- Confirmar si fila 222 efectivamente es HPL standard mal etiquetado.

---

## 5. Estado actualizado

| Fecha | Estado |
|---|---|
| 2026-05-17 | Documento creado tras cerrar Familia 3 completa (mesas) |
| 2026-05-17 | Añadidos: Silla Greta, Bruna 197,73€ misterio, Taburete Etna precio (tras cerrar Familia 5 sillas) |

---

> Última actualización: 2026-05-17
