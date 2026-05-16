# Auditoría Balliu — Familia Parasoles (piloto de consolidación)

> **Snapshot:** 2026-05-16
> **Fuentes:** scrapeo de [balliuexport.com](https://www.balliuexport.com/) (8 URLs de parasoles), `Santavila.xlsx` hojas `20260508 -Todos ` y `Balliu`, query GraphQL al Admin Shopify.
> **Estado:** auditoría completa. Plan de consolidación documentado. **Sin ejecutar en producción.**
> **Objetivo del piloto:** validar el patrón de consolidación antes de aplicarlo al resto del catálogo (tumbonas, mesas, sillas).

---

## Resumen ejecutivo

| Dato | Valor |
|---|---|
| Modelos reales de parasol en la web de Balliu | **8** (Pamela acrílico, Pamela Balliu, Ocean acrílico, Ocean Balliu, Ágora, Brisa, Garbí, Roma) |
| Productos planos hoy en Shopify (parasoles) | **15** (sin contar pies/bases) |
| Productos esperados tras consolidación | **8** (uno por modelo) |
| Variantes esperadas tras consolidación | **~140-160** (suma de matrices color × tamaño × punta × faldón) |
| Productos a eliminar (duplicados puros) | **4** (sufijos `-2` `-3` con mismo SKU) |
| Productos a crear de cero | **1** (Ágora, no existe en Shopify) |

**Conclusión**: el catálogo actual presenta **15 productos planos para algo que en realidad son 8 productos con variantes**. Lo equivalente a vender una camiseta con 6 tallas como 6 productos distintos. Tras la consolidación, el cliente verá UN parasol Pamela que puede configurar.

---

## 1. Inventario actual de Shopify (parasoles)

| # | Handle Shopify | SKU proveedor | PVP € | Pub | Modelo Balliu inferido |
|---|---|---|---|---|---|
| 1 | `balliu-parasol-para-terraza-acrilico-236bd5f0` | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` | 455,02 | ✓ | Pamela acrílico |
| 2 | `balliu-parasol-para-terraza-acrilico-236bd5f0-2` | (mismo SKU) | 438,41 | ✗ | Pamela acrílico (**duplicado**) |
| 3 | `balliu-parasol-para-terraza-acrilico-236bd5f0-3` | (mismo SKU) | 399,90 | ✗ | Pamela acrílico (**duplicado**) |
| 4 | `balliu-parasol-para-terraza-acrilico-c8dd492d` | `BALLIU_PARASOL_TELA_ACRILICA_25_C8DD492D` | 399,90 | ✓ | Ocean acrílico Ø250 |
| 5 | `balliu-parasol-para-terraza-82e48b2d` | `BALLIU_PARASOL_TELA_BALLIU_82E48B2D` | 423,28 | ✗ | Pamela tela Balliu |
| 6 | `balliu-parasol-para-terraza-82e48b2d-2` | (mismo SKU) | 334,93 | ✗ | Pamela tela Balliu (**duplicado**) |
| 7 | `balliu-parasol-para-terraza-82e48b2d-3` | (mismo SKU) | 384,95 | ✗ | Pamela tela Balliu (**duplicado**) |
| 8 | `balliu-parasol-para-terraza-f1ed8b8b` | `BALLIU_PARASOL_TELA_BALLIU_250__F1ED8B8B` | 381,95 | ✗ | Ocean tela Balliu Ø250 |
| 9 | `balliu-parasol-para-terraza-aluminio-300-cm-3b7e77d1` | `BALLIU_GARBI_PARASOL_DIAM_300_CM_TELA_3B7E77D1` | 1.049,00 | ✗ | Garbí (Ø300 redondo) |
| 10 | `balliu-parasol-para-terraza-aluminio-300-cm-0ceba8e7` | `BALLIU_BRISA_PARASOL_PARASOL_TELA_BAL_0CEBA8E7` | 1.049,00 | ✗ | Brisa (300×300 cuadrado) |
| 11 | `balliu-parasol-para-terraza-aluminio-300-cm-6c1e1224` | `BALLIU_ROMA_PARASOL_300X300_CM_6C1E1224` | 1.899,00 | ✗ | Roma (300×300 lateral) |
| 12 | `balliu-pie-de-parasol-c2147052` | `BALLIU_PIE_PARASOL_40_KG_C2147052` | 164,95 | ✗ | Pie 40 kg |
| 13 | `balliu-pie-de-parasol-fab3cac6` | `BALLIU_PIE_PARASOL_40_KG_RE_FAB3CAC6` | 126,95 | ✗ | Pie 40 kg "RE" |
| 14 | `balliu-base-de-parasol-3ee8b72d` | `BALLIU_BASE_HORMIGON_25_KG_3EE8B72D` | 99,90 | ✗ | Base hormigón 25 kg |
| 15 | `balliu-base-de-parasol-890a4cd4` | `BALLIU_BASE_HORMIGON_30_KG_890A4CD4` | 51,95 | ✗ | Base hormigón 30 kg |

**Observaciones:**
- Solo **2 productos están publicados al Online Store** (los que activamos manualmente para el test del 14-may).
- 4 duplicados puros (filas 2, 3, 6, 7) — eliminables.
- Ágora **no existe** en Shopify aunque sí en la web de Balliu.

---

## 2. Matriz real Balliu (web del proveedor)

### A · Parasol Pamela acrílico — 24 variantes a precio único

| Dimensión | Opciones |
|---|---|
| Color (Acrílico, serie 96) | Antracita 96/42 · Arena 96/30 · Azul 96/01 · Blanco 96/07 · Crudo 96/08 · Mineral 96/28 |
| Punta de mástil | Cónica (base Balliu) · Plana (uso playa) |
| Faldón | Sí · No |
| **Precio único** | **413,19 €** (Balliu PVP) — IVA incluido |

### B · Parasol Pamela tela Balliu — 64 variantes a precio único

| Dimensión | Opciones |
|---|---|
| Color (Balliu, serie 00) | 16 colores: Azul 01/00 · Amarillo 02/00 · Naranja 03/00 · Verde claro 04/00 · Blanco 07/00 · Natural 10/00 · Capuchino 12/00 · Caqui 16/00 · Marrón oscuro 21/00 · Arena 30/00 · Verde oscuro 32/00 · Azul celeste 36/00 · Ceniza 38/00 · Azul marino 40/00 · Gris oscuro 50/00 · Azul acero 61/00 |
| Punta de mástil | Cónica · Plana |
| Faldón | Sí · No |
| **Precio único** | **384,37 €** |

### C · Parasol Ocean acrílico — 24 variantes (precio por diámetro)

| Dimensión | Opciones |
|---|---|
| Diámetro | 200 cm · 250 cm |
| Color (Acrílico, serie 96) | 6 colores (mismos que Pamela acrílico) |
| Faldón | Sí · No |
| **Precio** | **398,10 € – 414,67 €** según diámetro y faldón |

### D · Parasol Ocean tela Balliu — ~32 variantes

| Dimensión | Opciones |
|---|---|
| Diámetro | 200 cm (todos los colores) · 250 cm (limitado a 3 colores) |
| Color (Balliu, serie 00) | 16 colores en 200 cm · subset (Blanco, Caqui, Gris oscuro) en 250 cm |
| **Precio** | **304,13 € – 381,54 €** |

### E · Parasol Ágora — 9 variantes (cuadrado 200×200)

| Dimensión | Opciones |
|---|---|
| Tamaño | 200×200 cm (único) |
| Color | 9 colores (mezcla serie 96 y serie 00) |
| Tejido | Acrílico (Tejido Balliu) |
| **Precio** | **404,20 € – 426,22 €** |
| ⚠️ | **No existe en Shopify** — proponer crear o ignorar |

### F · Parasol Brisa — 3 variantes (cuadrado 300×300, aluminio)

| Dimensión | Opciones |
|---|---|
| Tamaño | 300×300 cm (único) |
| Color tejido (Balliu) | Blanco 07/00 · Caqui 16/00 · Gris oscuro 50/00 |
| Estructura | Aluminio mate blanco |
| **Precio único** | **1.045,32 €** |

### G · Parasol Garbí — 3 variantes (redondo Ø300, aluminio)

| Dimensión | Opciones |
|---|---|
| Diámetro | 300 cm (único) |
| Color tejido (Balliu) | Blanco 07/00 · Caqui 16/00 · Gris oscuro 50/00 |
| Estructura | Aluminio mate blanco |
| **Precio único** | **1.045,32 €** |

### H · Parasol Roma — 3 variantes (lateral 300×300, aluminio)

| Dimensión | Opciones |
|---|---|
| Tamaño | 300×300 cm (lateral) |
| Color tejido (Acrílico) | Antracita 96/42 · Blanco 96/07 · Mineral 96/28 |
| Estructura | Aluminio lateral |
| **Precio único** | **1.897,36 €** |

---

## 3. Plan de consolidación (modelo a modelo)

Convención: **1 producto Shopify por modelo Balliu**. Options separadas (no concatenadas) tal como definió el dueño:
- Opción "Color"
- Opción "Diámetro" (cuando aplique)
- Opción "Faldón" (cuando aplique)
- Opción "Punta" (cuando aplique)

Shopify permite hasta **3 options por producto** y hasta **100 variantes por producto**. Todos los parasoles caben.

### Consolidación 1 — Pamela acrílico

| Acción | Detalle |
|---|---|
| Producto Shopify ganador | `balliu-parasol-para-terraza-acrilico-236bd5f0` (el único publicado) |
| Productos a eliminar | `…-236bd5f0-2`, `…-236bd5f0-3` (duplicados puros, mismo SKU) |
| Title nuevo | `Parasol Pamela · acrílico` |
| Options | Color (6) · Punta de mástil (2) · Faldón (2) = **24 variantes** |
| Precio variantes | 413,19 € uniforme (PVP Balliu, ya en Excel) |
| SKU pattern | `BAL_PAMELA_ACR_{COLOR}_{PUNTA}_{FALDON}` derivado |
| Imágenes | Las 11 de `balliu_catalog_full.json` → mapear por color (swatches) |

### Consolidación 2 — Pamela tela Balliu

| Acción | Detalle |
|---|---|
| Ganador | `balliu-parasol-para-terraza-82e48b2d` |
| Eliminar | `…-82e48b2d-2`, `…-82e48b2d-3` |
| Title | `Parasol Pamela · tela Balliu` |
| Options | Color (16) · Punta (2) · Faldón (2) = **64 variantes** |
| Precio | 384,37 € uniforme |
| Imágenes | 10 disponibles |

### Consolidación 3 — Ocean acrílico

| Acción | Detalle |
|---|---|
| Ganador | `balliu-parasol-para-terraza-acrilico-c8dd492d` (representa Ø250) |
| Eliminar | ninguno (los duplicados de 236bd5f0 son del modelo Pamela, no Ocean) |
| Title | `Parasol Ocean · acrílico` |
| Options | Diámetro (200/250) · Color (6) · Faldón (2) = **24 variantes** |
| Precio | 398,10 € - 414,67 € según diámetro |
| ⚠ Decisión | **Falta el Ø200 en Shopify hoy.** Hay que crear esa variante (el dueño tendrá que validar precio exacto contra Excel) |

### Consolidación 4 — Ocean tela Balliu

| Acción | Detalle |
|---|---|
| Ganador | `balliu-parasol-para-terraza-f1ed8b8b` (representa Ø250) |
| Eliminar | ninguno |
| Title | `Parasol Ocean · tela Balliu` |
| Options | Diámetro (200/250) · Color (16 en 200, subset 3 en 250) = **~32 variantes** |
| Precio | 304,13 € - 381,54 € según diámetro |
| ⚠ Decisión | **Falta el Ø200 en Shopify.** Crear |
| ⚠ Variantes "no existe" | El proveedor limita 250 cm a 3 colores. Hay que marcar las otras 13 combinaciones 250×color como `out_of_stock` o no crearlas. Decisión |

### Consolidación 5 — Ágora (NUEVO)

| Acción | Detalle |
|---|---|
| Acción | **Crear producto desde cero** |
| Title | `Parasol Ágora · acrílico 200×200` |
| Options | Color (9) = **9 variantes** |
| Precio | 404,20 € - 426,22 € (validar exacto con dueño) |
| ⚠ Decisión | ¿Crearlo? Solo añade variedad de oferta. Bajo esfuerzo |

### Consolidación 6 — Brisa

| Ganador | `balliu-parasol-para-terraza-aluminio-300-cm-0ceba8e7` |
|---|---|
| Title | `Parasol Brisa · aluminio 300×300` |
| Options | Color (3) = **3 variantes** |
| Precio | 1.045,32 € uniforme |

### Consolidación 7 — Garbí

| Ganador | `balliu-parasol-para-terraza-aluminio-300-cm-3b7e77d1` |
|---|---|
| Title | `Parasol Garbí · aluminio Ø300` |
| Options | Color (3) = **3 variantes** |
| Precio | 1.045,32 € uniforme |

### Consolidación 8 — Roma

| Ganador | `balliu-parasol-para-terraza-aluminio-300-cm-6c1e1224` |
|---|---|
| Title | `Parasol Roma · aluminio lateral 300×300` |
| Options | Color (3) = **3 variantes** |
| Precio | 1.897,36 € uniforme |

### Consolidación 9 — Pies de parasol

| Ganador | `balliu-pie-de-parasol-c2147052` (40 kg, 164,95 €) |
|---|---|
| Title | `Pie de parasol 40 kg` |
| Options | Acabado (Estándar / "RE") = **2 variantes** |
| ⚠ | El "RE" probablemente es "Redondo" o "Reforzado" — confirmar con proveedor antes de etiquetar |

### Consolidación 10 — Bases de parasol

| Ganador | `balliu-base-de-parasol-3ee8b72d` (25 kg, 99,90 €) |
|---|---|
| Title | `Base de hormigón para parasol` |
| Options | Peso (25 kg / 30 kg) = **2 variantes** |
| ⚠ | Precios actuales **incoherentes** en Shopify: 25 kg cuesta más (99,90 €) que 30 kg (51,95 €). Verificar con Excel y proveedor — probable error de tarifa antigua |

---

## 4. Decisiones que necesitamos antes de ejecutar

1. **Ocean Ø200 (acrílico y tela Balliu)**: en Shopify hoy solo tenemos Ø250. ¿Creamos la variante Ø200 leyendo precio del Excel o esperamos a confirmar con proveedor?
2. **Ágora**: ¿se crea? Es trabajo extra pero amplía oferta.
3. **Base de parasol 25 kg vs 30 kg**: precios incoherentes (99,90 € vs 51,95 €). ¿Revisar tarifa antes o aplicar y corregir después?
4. **Política de SKU para variantes**: ¿generamos SKUs derivados (`BAL_PAMELA_ACR_BLANCO_CONICA_FALDON_NO`) o todas las variantes comparten el SKU base del proveedor? Recomendado: **derivado**, así cada variante es trazable individualmente y se puede gestionar stock por variante en el futuro.
5. **Imágenes por variante**: cada parasol tiene una imagen por color. ¿Asignamos imagen por variante en Shopify (ideal UX) o dejamos galería única?
6. **Naming de variantes en español**: ¿usamos los nombres exactos del proveedor (`Antracita 96/42`) o simplificados para cliente final (`Antracita`)? Recomendado: simplificados, código solo internamente.

---

## 5. Plan técnico de implementación

Cuando el dueño valide las decisiones de arriba, ejecución en 4 fases:

### Fase A — Backup
Antes de tocar nada, snapshot JSON de los 15 productos actuales (script tipo `backup_products.py --handles balliu-parasol-*,balliu-pie-*,balliu-base-*`).

### Fase B — Crear variantes en los productos ganadores
Mutación `productOptionsCreate` para añadir options al producto, después `productVariantsBulkCreate` para crear cada variante con su SKU, precio, color, etc. Hay que aplicar el script en este orden:

1. Para cada producto ganador (8 productos), `productOptionsCreate` con sus options.
2. `productVariantsBulkCreate` con la matriz de combinaciones.
3. `productUpdate` para actualizar el title del producto a la versión canónica.

### Fase C — Eliminar duplicados puros
Una vez los productos ganadores tengan las variantes pobladas, eliminar los duplicados:
- 4 productos (`-2`, `-3` de Pamela acrílico y Balliu).
- Mutación `productDelete`.
- Crear redirects 301 si los handles eliminados tenían tráfico.

### Fase D — Crear Ágora (si se decide hacerlo)
- `productCreate` con title, descripción, options.
- `productVariantsBulkCreate` con las 9 variantes de color.

### Fase E — Publicar al Online Store + Shop
- `publishablePublish` para los 8 productos ganadores en los canales Online Store y Shop.
- Anota: hoy solo 2 de los 8 están publicados (de los productos planos actuales).

### Fase F — Verificar y reportar
- Validar que el contador de productos del Admin pasa de "X parasoles planos" a "8 parasoles con variantes".
- Snapshot final + reporte CSV con los antes/después.

**Tiempo estimado de ejecución total**: 1-2 horas + tiempo de validación visual del dueño.

---

## 6. Patrón generalizable para el resto del catálogo

Si el piloto de parasoles funciona bien, este es el patrón a replicar:

1. **Identificar la familia** (tumbonas, mesas, sillas).
2. **Inventario plano Shopify** + cruce con `Santavila.xlsx`.
3. **WebFetch a cada URL del proveedor** para extraer matriz real.
4. **Mapeo** SKU Shopify ↔ modelo proveedor.
5. **Documento de consolidación** (este formato).
6. **Decisiones de negocio** (creación de variantes faltantes, naming, etc.).
7. **Plan técnico de mutaciones**.
8. **Backup + ejecución + validación**.

Familias candidatas (ordenadas por urgencia):
- **Tumbonas Balliu** — 16 productos planos → ~5 modelos con variantes.
- **Mesas HPL Balliu** — 6 productos planos → 2-3 modelos.
- **Mesas auxiliares aluminio Balliu** — 5 productos → 1 modelo (Olimpia) con variantes de tipo.
- **Sillas Balliu** (Etna, Bruna, Selva, Vera) — 5+ productos planos.
- **Pasarelas resina** — 2 productos → 1 con variante.

---

## 7. Decisiones del dueño aplicadas (2026-05-16)

| # | Decisión | Aplicación |
|---|---|---|
| 1 | **Ceñirse al Excel** como fuente de verdad sobre qué productos vender | Ágora SÍ está en Excel (filas 259 y 260) → crear · Ocean Ø200 SÍ está → crear |
| 2 | **Ágora** ¿crear? | SÍ (está en Excel) |
| 3 | **Bases parasol** invertir precios | 25 kg → 51,23 € · 30 kg → 102,16 € (intercambio respecto al estado actual) |
| 4 | **SKU**: respetar el del Excel | Productos distintos pueden compartir SKU base. Se anota internamente la combinación elegida por el cliente al procesar pedido |
| 5 | **Imágenes por color** | SÍ |
| 6 | **Naming simplificado** (sin código de proveedor visible) | OK. Código serie 96/00 va a metafield interno `santavila.color_codigo_proveedor` |

## 8. Mapeo definitivo Excel → Modelo Shopify

Tras el cruce de PVP IVA del Excel con precios oficiales de la web Balliu, **el SKU del proveedor no identifica el modelo**: identifica el TIPO DE TEJIDO. El modelo (Pamela / Ocean / Ágora) lo determina el precio + diámetro implícito en el SKU:

```
SKU _ACRILICA_236BD5F0  → 3 modelos distintos según precio (413/398/426 €)
                          = Pamela acrílico / Ocean acrílico Ø200 / Ágora
SKU _BALLIU_82E48B2D    → 3 modelos según precio (384/304/404 €)
                          = Pamela tela Balliu / Ocean tela Balliu Ø200 / Ágora
SKU _ACRILICA_25_C8DD492D → 1 modelo (Ocean acrílico Ø250, 414,67 €)
SKU _BALLIU_250__F1ED8B8B → 1 modelo (Ocean tela Balliu Ø250, 381,54 €)
SKU _GARBI_DIAM_300_CM  → 1 modelo (Garbí Ø300, 1.045,32 €)
SKU _BRISA_PARASOL_BAL  → 1 modelo (Brisa 300×300, 1.045,32 €)
SKU _ROMA_300X300       → 1 modelo (Roma lateral, 1.897,36 €)
```

### Tabla maestra de los 8 productos Shopify resultantes

| # | Producto Shopify | Options (web Balliu) | # Variantes | Precio IVA | SKU del proveedor (compartido) | Fuente Excel |
|---|---|---|---|---|---|---|
| 1 | **Parasol Pamela · acrílico** | Color (6) × Punta (2) × Faldón (2) | 24 | 413,19 € | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` | fila 253 |
| 2 | **Parasol Pamela · tela Balliu** | Color (16) × Punta (2) × Faldón (2) | 64 | 384,37 € | `BALLIU_PARASOL_TELA_BALLIU_82E48B2D` | fila 254 |
| 3 | **Parasol Ocean · acrílico** | Diámetro (2) × Color (6) × Faldón (2) | 24 | 398,10 € (Ø200) · 414,67 € (Ø250) | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` (Ø200) + `..._25_C8DD492D` (Ø250) | filas 255 + 258 |
| 4 | **Parasol Ocean · tela Balliu** | Diámetro (2) × Color (16 en 200; 3 en 250) | ~22 | 304,13 € (Ø200) · 381,54 € (Ø250) | `BALLIU_PARASOL_TELA_BALLIU_82E48B2D` (Ø200) + `..._250__F1ED8B8B` (Ø250) | filas 256 + 257 |
| 5 | **Parasol Ágora · 200×200** | Color (9) | 9 | 404,20 € o 426,22 € según serie | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` (serie 96, 6 colores) + `..._BALLIU_82E48B2D` (serie 00, 3 colores) | filas 259 + 260 |
| 6 | **Parasol Brisa · 300×300** | Color (3) | 3 | 1.045,32 € | `BALLIU_BRISA_PARASOL_PARASOL_TELA_BAL_0CEBA8E7` | fila 262 |
| 7 | **Parasol Garbí · Ø300** | Color (3) | 3 | 1.045,32 € | `BALLIU_GARBI_PARASOL_DIAM_300_CM_TELA_3B7E77D1` | fila 261 |
| 8 | **Parasol Roma · lateral 300×300** | Color (3) | 3 | 1.897,36 € | `BALLIU_ROMA_PARASOL_300X300_CM_6C1E1224` | fila 263 |
| 9 | **Pie de parasol 40 kg** | Acabado (Estándar / "RE") | 2 | 164,14 € (estándar) · 126,88 € (RE) | 2 SKUs distintos | filas 270 + 271 |
| 10 | **Base de hormigón** | Peso (25 kg / 30 kg) | 2 | 51,23 € (25 kg) · 102,16 € (30 kg) ← **PRECIOS INVERTIDOS RESPECTO A SHOPIFY ACTUAL** | 2 SKUs distintos | filas 272 + 273 |

**Total**: 10 productos Shopify con ~157 variantes (vs 15 productos planos hoy).

## 9. Ágora — 2 niveles de precio por serie de color (DECIDIDO)

Decisión del dueño 2026-05-16: **Opción A confirmada**. Precio según código del color:

- **Si el código empieza por `96/`** → 426,22 € (acrílico, 6 colores)
- **Si el código termina en `/00`** → 404,20 € (tela Balliu, 3 colores)

### Tabla de variantes de Ágora con precio por variante

| Color (cliente) | Código proveedor | Precio | SKU base |
|---|---|---|---|
| Antracita | 96/42 | 426,22 € | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` |
| Arena | 96/30 | 426,22 € | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` |
| Azul | 96/01 | 426,22 € | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` |
| Blanco | 96/07 | 426,22 € | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` |
| Crudo | 96/08 | 426,22 € | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` |
| Mineral | 96/28 | 426,22 € | `BALLIU_PARASOL_TELA_ACRILICA_236BD5F0` |
| Blanco | 07/00 | 404,20 € | `BALLIU_PARASOL_TELA_BALLIU_82E48B2D` |
| Caqui | 16/00 | 404,20 € | `BALLIU_PARASOL_TELA_BALLIU_82E48B2D` |
| Gris oscuro | 50/00 | 404,20 € | `BALLIU_PARASOL_TELA_BALLIU_82E48B2D` |

> **Implicación de naming**: hay 2 colores llamados "Blanco" — uno serie 96 (a 426,22€) y otro serie 00 (a 404,20€). Para evitar confusión al cliente, propongo nombrarlos diferenciados: **"Blanco" (acrílico)** y **"Blanco" (tela Balliu)** — o mostrar el código completo solo en este caso. Decisión pendiente al ejecutar.

## 10. Resolución de la incoherencia de bases (decisión 3)

Hoy en Shopify:
- `balliu-base-de-parasol-3ee8b72d` (etiquetada **25 kg**) → 99,90 €
- `balliu-base-de-parasol-890a4cd4` (etiquetada **30 kg**) → 51,95 €

Tras la corrección decidida (intercambiar precios) y leyendo Excel:

| Variante consolidada | Precio Excel | Precio Shopify nuevo |
|---|---|---|
| Base hormigón **25 kg** | 51,23 € (fila 273, hoy mal asignada a 30 kg) | **51,23 €** |
| Base hormigón **30 kg** | 102,16 € (fila 272, hoy mal asignada a 25 kg) | **102,16 €** |

**Implicación operativa importante**: las etiquetas físicas del proveedor podrían estar invertidas también. Conviene avisar al proveedor antes del primer pedido real para evitar enviar al cliente la base equivocada.

---

## Histórico

- 2026-05-16 09:00 — auditoría piloto completada. Pendiente validación del dueño + decisión sobre los 6 puntos del §4.
- 2026-05-16 12:00 — decisiones del dueño aplicadas (§7). Mapeo Excel↔Modelo cerrado (§8). Queda decisión §9 (Ágora con 1 o 2 precios) antes de ejecutar.
