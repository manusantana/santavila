# Auditoría de productos duplicados — Santavila

> **Estado:** documentado, sin abordar todavía.
> **Snapshot:** 2026-05-14
> **Fuente:** query GraphQL completa contra `mueblesexterior.myshopify.com` (235 productos ACTIVE) con app `Santavila Admin` (scopes ampliados).
> **Detonante:** el dueño vio "el parasol 4 veces" en la búsqueda del Admin.

---

## Resumen ejecutivo

Sobre los **235 productos ACTIVE** del catálogo se han detectado tres tipos distintos de "duplicación":

| Tipo | Qué es | Cuántos afectados | Acción |
|---|---|---|---|
| **1. Duplicados puros** | Mismo SKU exacto en >1 producto Shopify, con handle terminando en `-2`, `-3`, `-N`. Creados por re-importaciones que colisionaron con el handle existente. | **~15 productos eliminables** | Eliminar (Fase A) |
| **2. Variantes mal modeladas** | Productos con mismo título genérico pero **SKUs distintos** (modelos / tamaños / colores diferentes del proveedor). Cada uno es un producto real, pero deberían vivir como variantes del mismo producto Shopify, no como productos independientes. | ~30-40 productos en 7-8 familias | Consolidar (Fase B, ver F0-04 del backlog) |
| **3. SKUs reusados intencionalmente** | El proveedor (Hevea sobre todo) ha reutilizado SKUs (`557-010147`, `557-010884`, `557-1563`) para productos físicamente distintos. Ya documentado en `PROYECTO.md §3 Hevea`. | 3 SKUs reusados conocidos | No tocar |

**Por qué se ven precios distintos en lo que parece el mismo producto:**
- En el Tipo 1, los precios distintos son resultado de varias importaciones en momentos distintos del histórico de tarifas (el último coste de Balliu vs uno anterior). Solo uno es el "vivo".
- En el Tipo 2, los precios distintos son **legítimos** porque son productos físicamente distintos (un Bruna 80 cm cuesta distinto de un Bruna 100 cm). El error está en cómo se modelaron en Shopify.

---

## Lo que vio el dueño — caso "parasol × 4"

Búsqueda en Admin: `balliu-parasol-para-terraza-acrilico-236bd5f0` devolvió **4 productos** con título "Parasol para terraza acrílico":

```
[ACTIVE pub:2] balliu-parasol-para-terraza-acrilico-236bd5f0       455,02€  SKU: …236BD5F0
[ACTIVE pub:2] balliu-parasol-para-terraza-acrilico-c8dd492d       399,90€  SKU: …25_C8DD492D     ← producto distinto (modelo "25")
[ACTIVE pub:0] balliu-parasol-para-terraza-acrilico-236bd5f0-2     438,41€  SKU: …236BD5F0       ← DUPLICADO PURO
[ACTIVE pub:0] balliu-parasol-para-terraza-acrilico-236bd5f0-3     399,90€  SKU: …236BD5F0       ← DUPLICADO PURO
```

Interpretación: hay **2 parasoles acrílicos legítimos** (`236bd5f0` y `c8dd492d`, con SKUs distintos) y **2 duplicados puros** del primero (`-2` y `-3`) creados por re-importación.

---

## Nivel 1 — Duplicados puros eliminables (Fase A)

Criterio combinado: **mismo SKU exacto** + **handle base con sufijo `-2/-3/-N`** + **mismo título**.

### Lista exacta (mantener el de PVP más alto o más recientemente publicado, eliminar el resto)

| Familia / SKU | Producto a mantener | Producto(s) a eliminar |
|---|---|---|
| Parasol acrílico `236BD5F0` | `balliu-parasol-para-terraza-acrilico-236bd5f0` (455,02€, publicado) | `…-236bd5f0-2` (438,41€) · `…-236bd5f0-3` (399,90€) |
| Parasol tela Balliu `82E48B2D` | `balliu-parasol-para-terraza-82e48b2d` (423,28€) | `…-82e48b2d-2` (334,93€) · `…-82e48b2d-3` (384,95€) |
| Mesa alta HPL `60X60_GD_A3352658` | `balliu-mesa-alta-exterior-hpl-a3352658` (502,93€) | `…-a3352658-2` (449,90€) |
| Silla Bruna brazos resina `94B6E5B5` | `balliu-silla-exterior-con-brazos-resina-estilo-funcional-94b6e5b5` (113,80€) | `…-94b6e5b5-2` (89,95€) |
| Tumbona EVA PRO blanco TE `B19AF1EA` | uno de los dos (revisar manualmente cuál) | `balliu-tumbona-de-exterior-resina-b19af1ea` (239,95€) ↔ `…-resina-73-cm-b19af1ea` (228,95€) |
| Mesa centro HPL 120/40 `557-1563` | `mesa-de-centro-exterior-120-cm-altura-40-cm` (322,31€) | `…-2` (441,95€, mismo SKU) |
| Reposapiés 85×50×43 — handles `557-0185` y `557-010482` | revisar, los SKUs son distintos → NO es duplicado puro, va a Nivel 2 | — |

**Subtotal duplicados puros a eliminar: ~9 productos** (estimación conservadora; revisar al ejecutar).

### Casos límite que requieren decisión humana

- **`balliu-tumbona-de-exterior-resina-b19af1ea`** y **`balliu-tumbona-de-exterior-resina-73-cm-b19af1ea`**: dos handles distintos pero mismo SKU `B19AF1EA`. El segundo tiene la medida (73 cm) en el handle. Probablemente el segundo es el correcto y el primero es la versión genérica antes de añadir medida. Decisión: mantener el que lleva medida en el handle (mejor SEO).
- **Sets de jardín con sufijos `-2`, `-3`, `-4`, `-5`** (`set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa`, etc.): aquí los **SKUs son distintos** (`557-010938`, `557-010816`, `557-1094`, `557-010729`, `557-0793`). NO son duplicados puros — son sets realmente distintos del proveedor con composiciones similares. Van a Nivel 2.

---

## Nivel 2 — Variantes mal modeladas (Fase B, diferida)

Productos físicamente distintos del proveedor con título genérico repetido. **NO son duplicados** — se deben consolidar como variantes del mismo producto Shopify (color, tamaño, modelo).

### Familias detectadas

| Título genérico | # productos hoy | Modelos / variantes reales | SKUs ejemplo |
|---|---|---|---|
| **Tumbona de exterior resina** | 16 | EVA PRO, EVA RG, EVA RTG, CARMEN, LOLA, MARINA, NOA, ALBA, OLIMPIA, IRIS, ETNA, ETNA ALTA | `…EVA_PRO_…`, `…NOA_…`, `…ETNA_…` |
| **Mesa alta exterior HPL** | 6 | DIAM 70, DIAM 70 GD, 60×60 GD, 70×70, 70×70 GD | `…DIAM_70_…`, `…60X60_…`, `…70X70_…` |
| **Mesa auxiliar exterior aluminio 54 cm** | 5 | OLIMPIA tela, OLIMPIA central, OLIMPIA esquinera | `…OLIMPIA_MESA_AUXILIA_…` |
| **Mesa auxiliar exterior resina 48 cm** | 4 | EVA PRO MINI blanco/natural, EVA PRO BCN blanco/natural | `…EVA_PRO_MINI_…`, `…EVA_PRO_BCN_…` |
| **Mesa exterior HPL** (varios tamaños) | 4 + 3 + 2 + 2 + 2 | DIAM 70/80, SOFIA 70×70/80×80, ATLANTA 240×90, JAVA 140-180/200-260 | varios |
| **Mesa exterior aluminio Ø80 cm / 80×80 cm** | 2 + 2 | ALTEA HPL / HPL GD | `…ALTEA_…` |
| **Parasol para terraza aluminio 300 cm** | 2 | BRISA, ROMA | `…BRISA_PARASOL_…`, `…ROMA_PARASOL_…` |
| **Silla exterior con brazos aluminio 56 cm** | 2 | ETNA, ETNA ALTA | `…ETNA_SILLA_…`, `…ETNA_SILLA_ALTA_…` |
| **Mesa exterior** (mini) | 2 | MINI blanco / natural | `…MINI_MESA_COLOR_BLANCO_…`, `…NATURAL_…` |
| **Mesa auxiliar exterior aluminio** | 2 | NOA blanco / natural | `…NOA_MESA_AUXILIAR_COLOR_…` |
| **Accesorio exterior resina** | 2 | Pasarela B / Pasarela 1 | `…PASARELA_RESINA_…` |
| **Pie de parasol** | 2 | 40 kg / 40 kg RE | `…PIE_PARASOL_40_KG_…` |
| **Base de parasol** | 2 | hormigón 25 kg / 30 kg | `…BASE_HORMIGON_…` |
| **Sets de jardín** (varias composiciones) | 2 + 3 + 4 + 4 + 5 + 2 + 4 | Hevea — combinaciones de sofá + sillones + mesa por estilo | múltiples `557-…` |

### Total productos involucrados en consolidación
~70-80 productos hoy "independientes" que podrían ser ~15-20 productos Shopify con variantes. Trabajo significativo, pero el impacto en percepción premium y SEO es alto.

### Conexión con el backlog
- **F0-04** del [`docs/santavila/BACKLOG_SANTAVILA.md`](../docs/santavila/BACKLOG_SANTAVILA.md): "Normalizar productType a 8-10 valores limpios" — primer paso.
- **Consolidar variantes Balliu**: tarea explícita listada en `PROYECTO.md §10 Tareas Pendientes` ("Productos con mismo diseño y distinto tamaño/color están como productos separados").

---

## Nivel 3 — SKUs reusados a propósito (NO duplicados)

Documentado en `PROYECTO.md §3`:

| SKU | Productos donde aparece | Razón |
|---|---|---|
| `557-010147` | `sofa-terraza-3-plazas-estilo-moderno-18570-cm` + `set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-5` | Hevea reusó SKU para sofá individual y set que lo incluye |
| `557-010884` | `set-jardin-contemporaneo-…` × 2 variantes | Reuso documentado |
| `557-1563` | `mesa-de-centro-exterior-120-cm-altura-40-cm` × 2 | **OJO**: este SÍ es duplicado puro (mismo título). Va a Nivel 1, no Nivel 3 |

> **Matiz**: PROYECTO.md lista `557-1563` como SKU reusado, pero el segundo handle en Shopify es `…-2` (sufijo de colisión). Aquí sí parece duplicado de importación, no reuso intencional del proveedor. Revisar manualmente al abordar Fase A.

---

## Fase A — Plan de ejecución cuando se aborde

Cuando se decida ejecutar:

1. **Script propuesto**: `delete_duplicate_products.py` (mismo patrón que `sync_prices_to_shopify.py`):
   - `--dry-run` por defecto: lista qué se eliminaría.
   - `--apply` ejecuta la mutación `productDelete`.
   - Lee la lista desde un CSV de input (no hardcodea handles).
2. **Mutación**: `productDelete(input: {id: $id})` — requiere scope `write_products` que ya tenemos.
3. **Reversibilidad**: Shopify **no** permite restaurar un producto eliminado vía API. Hay 7 días de papelera en Admin, después se borra permanentemente. **Antes de borrar, hacer dump JSON de cada producto** (script de backup) por si hay que recrear alguno.
4. **Verificar antes de borrar**:
   - Que el producto a eliminar NO tiene pedidos asociados (con el `read_orders` que ya tenemos: `orders(query: "line_item_product:<id>")`).
   - Que el producto a eliminar NO está referenciado en alguna colección manual destacada.
   - Que el SKU "ganador" sigue accesible en la otra instancia (la que se mantiene).
5. **Antes/después**: snapshot del contador total de productos ACTIVE.

## Fase B — Plan de consolidación cuando se aborde

1. Trabajar **una familia a la vez**, no en bulk.
2. Por cada familia (ej. "Tumbona de exterior resina"):
   - Decidir cuál es el producto Shopify "ganador" que recibirá las variantes.
   - Crear las options (ej. "Modelo": [EVA PRO, EVA RG, NOA, …]).
   - Migrar los SKUs como variantes del producto ganador.
   - Eliminar los productos independientes una vez migrados.
3. Cuidado con:
   - Imágenes asociadas (cada modelo tiene su foto; las variantes pueden tener imagen propia).
   - Precios distintos por variante (Shopify lo permite nativo).
   - Metafields que se aplican a producto vs variante.
   - Tags `envio:xs|m|l` ya aplicados: si la nueva variante consolidada cambia de categoría de envío, hay que reaplicar.

---

## Decisiones pendientes para retomar

1. ¿Se aborda Fase A antes o después de levantar el password page? Recomendado: **antes** (el cliente final no debe ver duplicados al lanzar).
2. ¿Fase B se hace antes del Sprint 4 (rediseño home)? Recomendado: **sí**, porque sin consolidar variantes la home muestra catálogo redundante.
3. Cuando se aborde, decidir nombres y opciones de variantes preferidos:
   - "Modelo" + "Color" para resina/tela
   - "Tamaño" para mesas
   - "Tablero" (HPL / GD) para mesas exteriores
4. ¿Productos "GD" (HPL Gran Diam) se modelan como variante de tablero o como producto separado? PROYECTO sugiere variante.

---

## Histórico

- 2026-05-14 — auditoría inicial detectada al ver el caso "parasol × 4" durante prep de test de envío. Documentado aquí. Sin acción inmediata, prioridad media-alta.
