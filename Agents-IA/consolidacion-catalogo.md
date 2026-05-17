# Consolidación del catálogo Santavila

> **Estado vivo:** este documento es el **índice maestro** de la consolidación de variantes del catálogo.
> Una sección por familia. Cada familia se aborda como un "piloto" siguiendo el patrón validado en la primera (parasoles).

---

## Patrón validado

El piloto de **parasoles Balliu** ya cerrado (2026-05-16) demostró el flujo:

```
1. WebFetch a la web del proveedor → matriz real de variantes.
2. Cruzar SKUs del Excel ↔ modelo del proveedor por precio + descripción.
3. Decisiones del dueño (naming, ambigüedades, precios incoherentes).
4. Script declarativo con productos como dict (PRODUCTS).
5. Dry-run → apply piloto (--only) → apply resto → delete + publish.
6. Backup previo, reporte CSV, metafields para preservar info original.
```

**Convenciones globales acordadas con el dueño:**

| Decisión | Aplicación |
|---|---|
| Ceñirse al Excel `Santavila.xlsx` como fuente de verdad sobre qué productos vender. La web del proveedor da matriz de variantes; si el Excel no tiene un modelo, no se crea | Si está en Excel → crear · Si no → no crear |
| Naming **Opción C**: sin nombre del proveedor visible al cliente | "Parasol cuadrado · aluminio 300×300 cm" en vez de "Parasol Brisa" |
| SKU **derivado por variante** (`SV-<MODELO>-<COLOR>-…`) | Único por variante, trazable, no comparte SKU entre variantes |
| Metafields para preservar info del proveedor | `santavila.proveedor_modelo`, `santavila.proveedor_grupo`, `santavila.proveedor_sku_original`, `santavila.espacio_principal`, `santavila.color_codigo_proveedor` (variante) |
| Naming de colores **simplificado** (sin "(tela Balliu)" etc.) | Excepción: productos donde colisionan dos series usan "Blanco acrílico" / "Blanco tela" |
| Imágenes por variante (color) | Sí — pendiente de implementar en siguiente iteración |

---

## Estado por familia

| Familia | Productos planos hoy | Modelos consolidados | Estado |
|---|---|---|---|
| **Parasoles Balliu** | 15 (parasoles + pies + bases) | **10** (con 153 variantes) | ✅ Completado 2026-05-16 |
| **Tumbonas Balliu** | 20 (tumbonas + mini + colchonetas) | **19** (con 787 variantes) · 1 a DRAFT (Alba) | ✅ Completado 2026-05-17 |
| **Mesas HPL Balliu** | ~50 (real) | ~25 estimado (troceado en 4 sub-pilotos) | 🟡 En curso — 3b ✅ |
| **Mesas auxiliares aluminio Balliu** | ~5 | 1 (Olimpia con variantes) | ⏳ Pendiente |
| **Sillas Balliu** (Etna, Bruna, Selva, Vera) | 5+ | 4 estimado | ⏳ Pendiente |
| **Pasarelas resina Balliu** | 2 | 1 con variante | ⏳ Pendiente |
| **Imágenes por variante (todas las familias)** | — | — | ⏳ Pendiente — atacar tras completar consolidaciones |
| **Hevea** | 115 | TBD — la mayoría sets/conjuntos sin variantes | 🟦 Auditoría pendiente |

---

## Familia 1 — Parasoles Balliu ✅ COMPLETADO (2026-05-16)

**Resultado:** 15 productos planos → 10 productos con 153 variantes ricas (24+64+24+19+9+3+3+3+2+2).
**Script:** [`consolidate_balliu_parasoles.py`](../consolidate_balliu_parasoles.py).
**Backup:** `backups/parasoles_<timestamp>.json` (gitignored).

### Hallazgo clave del proveedor

El **SKU autogenerado del Excel NO es del proveedor** — Balliu trabaja con (Producto + Variante + Grupo), no con códigos únicos. Por eso un mismo SKU aparece en filas distintas con costes distintos: corresponden a modelos físicamente diferentes que comparten el SKU base por tejido.

Mapeo final tras cruzar PVP IVA del Excel con la web Balliu:

```
SKU _ACRILICA_236BD5F0      → 3 modelos según precio: Pamela acr. (413 €) / Ocean acr. Ø200 (398 €) / Ágora serie 96 (426 €)
SKU _BALLIU_82E48B2D        → 3 modelos: Pamela tela (384 €) / Ocean tela Ø200 (304 €) / Ágora serie 00 (404 €)
SKU _ACRILICA_25_C8DD492D   → Ocean acrílico Ø250 (414,67 €)
SKU _BALLIU_250__F1ED8B8B   → Ocean tela Balliu Ø250 (381,54 €)
SKU _GARBI_DIAM_300_CM      → Garbí Ø300 (1.045,32 €)
SKU _BRISA_PARASOL_BAL      → Brisa 300×300 (1.045,32 €)
SKU _ROMA_300X300           → Roma lateral (1.897,36 €)
```

### Resultado final (10 productos Shopify)

| # | Producto Shopify | Variantes | Precio IVA | Origen Excel |
|---|---|---|---|---|
| 1 | Parasol exterior acrílico · mástil regulable Ø200 cm (Pamela acr.) | 24 (Color × Punta × Faldón) | 413,19 € | fila 253 |
| 2 | Parasol exterior · mástil regulable 16 colores Ø200 cm (Pamela tela) | 64 (Color × Punta × Faldón) | 384,37 € | fila 254 |
| 3 | Parasol exterior acrílico · Ø200 / Ø250 cm (Ocean acr.) | 24 (Diámetro × Color × Faldón) | 398,10 / 414,67 € | filas 255+258 |
| 4 | Parasol exterior · 16 colores Ø200 / Ø250 cm (Ocean tela) | 19 (Diámetro × Color, limitado) | 304,13 / 381,54 € | filas 256+257 |
| 5 | Parasol cuadrado · 200×200 cm (Ágora) | 9 (Color) | 404,20 / 426,22 € según serie | filas 259+260 — CREADO 2026-05-16 |
| 6 | Parasol cuadrado · aluminio 300×300 cm (Brisa) | 3 (Color) | 1.045,32 € | fila 262 |
| 7 | Parasol redondo · aluminio Ø300 cm (Garbí) | 3 (Color) | 1.045,32 € | fila 261 |
| 8 | Parasol lateral · aluminio 300×300 cm (Roma) | 3 (Color) | 1.897,36 € | fila 263 |
| 9 | Pie de parasol · 40 kg | 2 (Acabado: Estándar / RE) | 164,14 / 126,88 € | filas 270+271 |
| 10 | Base de hormigón para parasol | 2 (Peso: 25 / 30 kg) | **51,23 / 102,16 € (invertidos respecto al estado anterior)** | filas 272+273 |
| **Total** | | **153** | | |

**Productos eliminados (6):**
- 4 duplicados puros (Pamela acrílico `-2/-3`, Pamela tela `-2/-3`)
- 2 absorbidos como variante (pie RE, base 30 kg)

**Pendientes operativos:**
- ⚠ Bases de hormigón: **etiquetas físicas del proveedor probablemente invertidas también**. Avisar a Balliu antes del primer pedido real.
- ⏳ Imágenes por variante (mapear color → imagen del JSON scrapeado en `balliu_catalog_full.json`).
- ⏳ Limpiar tags antiguos visibles (`Balliu`, `match-verde`) — tarea F0-02/F0-03 del backlog.

---

## Familia 2 — Tumbonas Balliu ✅ COMPLETADO (2026-05-17)

**Resultado:** 20 productos planos → 19 productos con **787 variantes** + Alba a DRAFT.
**Script:** [`consolidate_balliu_tumbonas.py`](../consolidate_balliu_tumbonas.py).
**Backup:** `backups/tumbonas_<timestamp>.json` (gitignored).

### Decisiones del dueño aplicadas (2026-05-17)

1. **Chasis con valores reales** (Opción A): cada modelo define sus 1-5 colores reales (Blanco / Arena / Bronce / Gris Oscuro / Madera / Tórtola / Antracita / Aluminio).
2. **Precio Blanco vs "Prestige"**: Blanco = precio base · cualquier otro color = +precio Prestige (más caro).
3. **16 colores de tejido como option visible al cliente** (mismo precio, todas las combinaciones).
4. **Tablillas → producto separado** (Carmen T, Lola T, Eva Pro T) en lugar de variante.
5. **Alba a DRAFT** (no existe en la web actual de Balliu — pendiente verificar con proveedor).
6. **Mini tumbonas** verificadas en la web: Cannes (3 chasis), Bristol (madera teca), Marina mini (2 chasis), todos con 16 colores tejido.

### Resultado final (19 productos Shopify)

| # | Producto Shopify | Variantes | Precio IVA |
|---|---|---|---|
| 1 | Tumbona resina · respaldo regulable Ø73 cm tela (Eva Pro) | 80 (5 chasis × 16 tejido) | 228,44 / 242,13 € |
| 2 | Tumbona resina · respaldo regulable Ø73 cm tablillas (Eva Pro T, Mario Eskenazi) | 5 (5 chasis) | 219,66 / 242,13 € |
| 3 | Tumbona resina playa · 73 cm tela (Eva RG) | 32 (2 chasis × 16 tejido) | 184,83 / 192,27 € |
| 4 | Tumbona resina jardín · 73 cm tablillas (Eva RTG) | 1 | 190,14 € |
| 5 | Tumbona resina · respaldo regulable 75 cm tela (Carmen) | 80 | 183,23 / 188,28 € |
| 6 | Tumbona resina · respaldo regulable 75 cm tablillas (Carmen T) ⭐ creado nuevo | 5 | 209,03 / 219,66 € |
| 7 | Tumbona resina · respaldo regulable playa 75 cm tela (Lola) | 80 | 182,17 / 187,74 € |
| 8 | Tumbona resina · respaldo regulable playa 75 cm tablillas (Lola T) ⭐ creado nuevo | 5 | 208,76 / 212,34 € |
| 9 | Tumbona resina premium · respaldo regulable (Noa) | 80 | 400,68 / 419,31 € |
| 10 | Tumbona aluminio · respaldo regulable con/sin ruedas (Olimpia) | 96 (Ruedas × Chasis × Tejido) | 535,45 / 587,56 € |
| 11 | Tumbona aluminio · respaldo regulable (Etna) | 96 | 426,44 / 470,48 € |
| 12 | Tumbona aluminio alta · respaldo regulable acceso fácil (Etna Alta) | 96 | 463,07 / 496,21 € |
| 13 | Tumbona aluminio · con ruedas integradas 58 cm (Iris) | 16 (color tejido) | 628,76 € |
| 14 | Tumbona aluminio apilable · 68 cm (Marina) | 16 | 323,76 € |
| 15 | Mini tumbona aluminio plegable · 62 cm (Cannes) | 48 (3 chasis × 16 tejido) | 262,28 € |
| 16 | Mini tumbona madera teca plegable · 59 cm (Bristol) | 16 | 304,51 € |
| 17 | Mini tumbona aluminio apilable · 57 cm (Mini Marina) | 32 (2 chasis × 16 tejido) | 213,34 € |
| 18 | Colchoneta para tumbona | 3 (Tela Balliu / Acrílico / Dry Feel) | 115,55 / 131,37 / 190,88 € |
| 19 | Tumbona Alba ⏸ **DRAFT** (pendiente verificar con proveedor) | — | — |
| **Total** | | **787 variantes** | |

### Bugs resueltos en el camino

- **Productos con options legacy** (`Color chasis`, `Configuración`): 7 productos (eva_rg, carmen_tela, lola_tela, noa, olimpia, etna, etna_alta) tenían options con nombres viejos del estado original. La mutación `productOptionsCreate` falla en silencio al detectar duplicado, pero luego `productVariantsBulkCreate` falla con `NEED_TO_ADD_OPTION_VALUES`.
  - **Fix**: borrar variantes (`productVariantsBulkDelete` dejando 1 Default Title) → borrar options (`productOptionsDelete` con `strategy: POSITION`) → re-crear options + variantes con el script normal.
- **SSL EOF intermitente** en mitad del fix masivo: añadir retries con backoff exponencial al wrapper `gql()`.
- **Productos creados desde cero** (Carmen T, Lola T): el script ya soportaba `create_new=True` del piloto de Ágora, funcionó al primer intento.

### Pendientes operativos

- ⏳ **Verificar Alba con el proveedor**: no aparece en balliuexport.com. ¿Está descatalogado? ¿Es nombre antiguo de otro modelo? Mientras tanto en DRAFT.
- ⏳ **Imágenes por variante** (mapear color del tejido → swatch del proveedor).
- ⏳ **Olimpia/Etna/Etna Alta tienen 96 variantes**, al filo del límite Shopify (100/producto). Si en futuro hay que añadir alguna option más, considerar separar en 2 productos.

---

## Familia 2 — Tumbonas Balliu — ESPECIFICACIÓN ORIGINAL (referencia)

> Histórico de cómo se planificó. La sección de arriba refleja el resultado final.

---

## Familia 3 — Mesas HPL Balliu 🟡 EN CURSO

**Inventario real:** ~50 productos planos en Shopify (`handle:balliu-mesa*`), no 6 como se estimó inicialmente.

**Decisión:** trocear en **4 sub-pilotos por categoría funcional**, en orden de complejidad creciente.

| Sub-piloto | Categoría | Productos planos | Consolidados | Estado |
|---|---|---|---|---|
| **3b** | Mesa alta (Capri Alta) | 6 | 1 (+5 DRAFT) | ✅ 2026-05-17 |
| **3c** | Mesa centro (Etna, Olimpia) | ~2 | ~2 | ⏳ Siguiente |
| **3d** | Mesa auxiliar (Eva Pro Mini/BCN, Olimpia, Noa, Etna, Greta) | ~14 | ~7 estimado | ⏳ |
| **3a** | Mesa comedor (Selva, Brunei, Atlanta, Java, Sofia, Capri, Altea, Ágata, Nora) | ~25 | ~12 estimado | ⏳ |

### Sub-piloto 3b — Mesa alta exterior HPL ✅ COMPLETADO (2026-05-17)

**Origen proveedor:** Mesa Capri Alta (`mesa-de-aluminio-capri-alta`, altura 110 cm, chasis aluminio).

**Script:** [`consolidate_balliu_mesas_altas.py`](../consolidate_balliu_mesas_altas.py).
**Backup:** `backups/mesas_altas_20260517-082726.json` (gitignored).

**Decisiones del dueño:**
1. Ø70 cm (mesa redonda) → DRAFT (no figura en web actual del proveedor, no se elimina).
2. HPL Gran Densidad → DRAFT (no figura en web actual).
3. Precios desde Excel pestaña `20260508 -Todos ` (única fiable).
4. Chasis Aluminio como descripción de producto, no como opción.

**Resultado:**

| | Antes | Después |
|---|---|---|
| ACTIVE | 6 productos planos · 1 variante c/u | **1 consolidado** · 2 variantes |
| DRAFT | 0 | **5** (Ø70 HPL, Ø70 HPL GD, 60×60 HPL GD, 70×70 HPL GD, duplicado 60×60) |
| Naming | `Mesa alta exterior HPL` × 6 | `Mesa alta exterior · aluminio HPL 110 cm` |
| Precios 60×60 | €449,90 / €502,93 | **€456,69** (Excel) |
| Precios 70×70 | €529,00 | **€528,46** (Excel) |
| Winner Shopify | — | `balliu-mesa-alta-exterior-hpl-94512eab` |
| Tag legacy | — | `legacy-balliu-consolidado-2026-05` para los 5 DRAFT |

**Variantes ACTIVE finales:**
- 60×60 cm — SKU `SV-MESAALTA-60-HPL` — €456,69
- 70×70 cm — SKU `SV-MESAALTA-70-HPL` — €528,46

### Hallazgo crítico sobre precios del Excel

Solo la pestaña **`20260508 -Todos `** (con espacio al final) tiene precios consistentes:
- Columna F = "Precio Venta (con IVA 21%)" — IVA incluido
- Columna I = "PVP Recomendado" — sin IVA
- F = I × 1,21 ✓ en todas las filas

Las pestañas `Balliu` y `Todos` tienen F = I (no separadas IVA/sin IVA), por lo que **no son fiables como fuente de precios**. Memorizado en la memoria persistente del proyecto.

### Anomalía en Excel (filas 222-223)

Mismo SKU `BALLIU_60X60_MESA_ALTA_TABLERO_HPL_GD_A3352658` aparece en dos filas con costes distintos (245,33€ / 263,01€). Por el patrón HPL → HPL GD de otros tamaños, se deduce que la fila 222 es **HPL standard mal etiquetado**. Se aplica como tal a la variante 60×60 activa.

---

## Familia 4 — Mesas auxiliares aluminio Balliu ⏳ PENDIENTE

Inventario inicial estimado:
- ~5 productos planos "Mesa auxiliar exterior aluminio | 54 cm".
- Modelo único: OLIMPIA con variantes (tela / central / esquinera).

---

## Familia 5 — Sillas Balliu ⏳ PENDIENTE

Modelos detectados: ETNA, ETNA ALTA, BRUNA, SELVA, VERA. ~5 productos planos.

---

## Familia 6 — Pasarelas resina Balliu ⏳ PENDIENTE

2 productos "Accesorio exterior resina" → 1 modelo (Pasarela) con variante de longitud.

---

## Hevea ⏳ AUDITORÍA PENDIENTE

Hevea trabaja con SKUs limpios (`557-…`, `928-…`) y la mayoría son **sets/conjuntos** específicos sin matriz de variantes. Auditoría más simple — la atacaremos cuando se cierre Balliu.

---

## Histórico

- **2026-05-16 (mañana)** — auditoría inicial de Familia 1 (Parasoles) creada con título `auditoria-balliu-parasoles.md`. 6 decisiones del dueño cerradas.
- **2026-05-16 (mediodía)** — Familia 1 ejecutada en producción: 10 productos / 144 variantes (sin Ágora todavía). Script `consolidate_balliu_parasoles.py` validado end-to-end.
- **2026-05-16 (tarde)** — Ágora creado desde cero (9 variantes, 2 precios por serie de color). Flag `create_new=True` del script implementada y validada. Total Familia 1: **153 variantes**.
- **2026-05-16 (tarde)** — Documento renombrado de `auditoria-balliu-parasoles.md` a `consolidacion-catalogo.md` para que sirva como índice maestro de todas las familias del catálogo.
