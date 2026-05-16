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
| **Tumbonas Balliu** | ~16 | ~5 estimado | ⏳ Pendiente |
| **Mesas HPL Balliu** | ~6 | 2-3 estimado | ⏳ Pendiente |
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

## Familia 2 — Tumbonas Balliu ⏳ PENDIENTE

> Próxima familia a auditar siguiendo el mismo patrón.

**Inventario inicial estimado** (de la auditoría anterior):
- 16 productos planos con título genérico "Tumbona de exterior resina" / "Tumbona de exterior" / "Tumbona de exterior aluminio".
- Modelos detectados: EVA PRO, EVA RG, EVA RTG, CARMEN, LOLA, NOA, ALBA, OLIMPIA, IRIS, ETNA, ETNA ALTA, MARINA.
- Probablemente ~5 modelos base con variantes de chasis/tablillas/tela.

**Pasos al abordar:**
1. WebFetch a cada URL de tumbona en balliuexport.com.
2. Cruce Excel ↔ modelo (por precio + nombre).
3. Decisiones del dueño sobre ambigüedades.
4. Añadir entries `PRODUCTS` a un nuevo script (o extender el actual con un módulo).
5. Dry-run → piloto → resto.

---

## Familia 3 — Mesas HPL Balliu ⏳ PENDIENTE

Inventario inicial estimado:
- ~6 productos planos: "Mesa exterior HPL", "Mesa alta exterior HPL", "Mesa exterior aluminio".
- Modelos detectados en el log: DIAM 70, 60×60, 70×70, SOFIA 80×80, ATLANTA 240×90, JAVA 140-180/200-260, ALTEA.

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
