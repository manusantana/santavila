# JOURNAL — Santavila / Transformación ecommerce

> Bitácora de ejecución del plan documentado en [`../../Agents-IA/plan_santavila.md`](../../Agents-IA/plan_santavila.md).
> Una entrada por hito. Cada entrada deja claro: **qué se hizo, qué hay que tener en cuenta y qué bloquea lo siguiente.**

---

## Cómo se usa este journal

- Entradas **en orden cronológico inverso** (lo más reciente arriba).
- Cada entrada lleva: fecha, paso del flujo (ver [`../../Agents-IA/INDEX.md`](../../Agents-IA/INDEX.md)), qué se ejecutó, entregables, hallazgos clave, prioridades vivas, decisiones pendientes y siguiente paso recomendado.
- Cuando el paso siguiente se ejecuta, se añade una entrada nueva arriba — **no se reescribe la anterior**.

---

## 2026-05-17 · Familia 2 cerrada — Tumbonas Balliu (19 productos / 787 variantes)

**Paso del flujo:** Sprint adicional — calidad de catálogo (continuación del plan de consolidación)
**Estado:** ✅ Aplicado en producción · todos los productos publicados
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_tumbonas.py`

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu de la familia "tumbona". 20 productos planos → **19 productos con variantes ricas** + 1 a DRAFT (Alba).

**Documentos:**
- [`Agents-IA/consolidacion-catalogo.md`](../../Agents-IA/consolidacion-catalogo.md) — actualizado con la Familia 2 completada.
- [`consolidate_balliu_tumbonas.py`](../../consolidate_balliu_tumbonas.py) — nuevo script siguiendo el patrón de parasoles.
- `backups/tumbonas_<timestamp>.json` — snapshots previos (gitignored).

### Decisiones del dueño aplicadas

1. **Chasis con valores reales** (Opción A): cada modelo define sus 1-5 colores reales del proveedor.
2. **Precio Blanco vs "Prestige"** (= cualquier color no-Blanco, más caro).
3. **16 colores tejido como option visible** al cliente.
4. **Tablillas → producto separado** (Carmen T, Lola T, Eva Pro T) en lugar de variante. Carmen T y Lola T se crearon desde cero.
5. **Alba a DRAFT** (no existe en la web Balliu — pendiente verificar).
6. **Naming Opción C**: sin marca proveedor visible.

### Resultado

| Producto | Variantes |
|---|---|
| Eva Pro (tela / tablillas) | 80 + 5 |
| Eva RG / Eva RTG | 32 + 1 |
| Carmen (tela / tablillas) | 80 + 5 |
| Lola (tela / tablillas) | 80 + 5 |
| Noa | 80 |
| Olimpia / Etna / Etna Alta (con ruedas Sí/No) | 96 × 3 = 288 |
| Iris / Marina | 16 + 16 |
| Mini Cannes / Bristol / Marina | 48 + 16 + 32 |
| Colchoneta (3 tejidos) | 3 |
| Alba | DRAFT |
| **Total** | **787 variantes en 19 productos** |

Todos los productos vivos publicados a Online Store + Shop.

### Bugs resueltos

- **Productos con options legacy** (`Color chasis`, `Configuración`): 7 productos tenían options con nombres viejos. `productOptionsCreate` falla en silencio y luego `productVariantsBulkCreate` da `NEED_TO_ADD_OPTION_VALUES`. **Fix**: borrar variantes con `productVariantsBulkDelete`, luego borrar options con `productOptionsDelete strategy:POSITION`, luego re-aplicar consolidación normal.
- **SSL EOF intermitente**: añadidos retries con backoff exponencial.
- **`strategy: DEFAULT` no borra options con múltiples valores** — usar `strategy: POSITION` después de borrar variantes.

### Pendientes

- ⏳ Verificar Alba con el proveedor (descatalogado o nombre antiguo).
- ⏳ Imágenes por variante (todas las familias) — diferido.
- ⏳ Olimpia/Etna/Etna Alta con 96 variantes están al filo del límite Shopify (100/producto).

### Siguiente paso recomendado

**Familia 3 — Mesas HPL Balliu** (~6 productos planos → 2-3 modelos: SOFIA, ATLANTA, JAVA, DIAM, ALTEA). Patrón idéntico al usado en tumbonas.

---

## 2026-05-16 (tarde) · Cierre Familia 1 con Ágora + rename del documento maestro

**Paso del flujo:** completar Familia 1 (Parasoles) + reorganizar la documentación de consolidación
**Estado:** ✅ Familia 1 cerrada · 153 variantes totales

### Qué se ejecutó

#### Ágora creado desde cero
- Implementada la rama `create_new=True` en `consolidate_balliu_parasoles.py` (mutación `productCreate`).
- Bug menor resuelto en el camino: campo `code` no existe en `UserError` para `productCreate` (sí en otros tipos).
- Producto nuevo creado: `parasol-cuadrado-200x200` con 9 variantes y publicado al Online Store + Shop.
- Precios por serie de color del Excel: 6 colores serie 96 a 426,22 € + 3 colores serie 00 a 404,20 €.
- Colisión de "Blanco" resuelta con nombres diferenciados: **"Blanco acrílico"** (96/07) y **"Blanco tela"** (07/00).

#### Documento maestro renombrado
- `Agents-IA/auditoria-balliu-parasoles.md` → `Agents-IA/consolidacion-catalogo.md` (con `git mv`, historial preservado).
- Contenido reestructurado como **índice maestro** del catálogo: una sección por familia, plantilla para escalar.
- Referencias actualizadas en `JOURNAL.md` y `consolidate_balliu_parasoles.py` (docstring).
- `INDEX.md` actualizado.

### Estado final Familia 1

10 productos · **153 variantes** (24 + 64 + 24 + 19 + **9 Ágora** + 3 + 3 + 3 + 2 + 2).

### Siguiente paso recomendado

- **Familia 2: Tumbonas Balliu** — 16 productos planos → ~5 modelos. WebFetch a cada modelo (EVA PRO, CARMEN, LOLA, NOA, OLIMPIA, IRIS, ETNA, MARINA, ALBA).
- O **imágenes por variante** de Familia 1 — el dueño dijo "luego revisamos colores".

El usuario priorizó **continuar con la consolidación** antes de los colores, así que la próxima sesión empezará con tumbonas.

---

## 2026-05-16 · Consolidación piloto Balliu — familia parasoles (9 productos / 144 variantes)

**Paso del flujo:** Sprint adicional — calidad de catálogo (Nivel 2 de la auditoría de duplicados)
**Estado:** ✅ Aplicado en producción · piloto exitoso del patrón de consolidación
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_parasoles.py`

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu de la familia "parasol" y consolidación: **15 productos planos → 9 productos con variantes ricas**.

**Documentos generados:**
- [`Agents-IA/consolidacion-catalogo.md`](../../Agents-IA/consolidacion-catalogo.md) — mapeo Excel↔Modelo + 6 decisiones cerradas del dueño.
- [`consolidate_balliu_parasoles.py`](../../consolidate_balliu_parasoles.py) — script de consolidación (dry-run por defecto, `--only`, `--skip-delete`, `--skip-publish`).
- `backups/parasoles_<timestamp>.json` — snapshot completo previo a tocar nada.

### Decisiones del dueño aplicadas

1. **Naming Opción C** — sin nombre del proveedor visible, por característica técnica:
   - `Parasol cuadrado · aluminio 300×300 cm` (Brisa)
   - `Parasol exterior acrílico · mástil regulable Ø200 cm` (Pamela acrílico)
   - `Parasol redondo · aluminio Ø300 cm` (Garbí)
   - `Parasol lateral · aluminio 300×300 cm` (Roma)
   - etc.
2. **SKU derivado por variante** (`SV-BRISA-CAQUI`, `SV-PAMELA-ACR-ANTRACITA-CON-F`...) en lugar del SKU autogenerado del Excel, que NO es del proveedor.
3. **Metafields del producto**:
   - `santavila.proveedor_modelo` (Brisa / Pamela / Ocean / Garbí / Roma / Pie / Base)
   - `santavila.proveedor_grupo` (G1)
   - `santavila.proveedor_sku_original` (preservado para auditoría)
   - `santavila.espacio_principal` (lista)
4. **Metafield de variante** `santavila.color_codigo_proveedor` (96/42, 07/00, etc.) — permite reconstruir el código exacto al pasar pedido a Balliu.
5. **Colores con nombres simples** ("Blanco" en vez de "Blanco (tela Balliu)") — la serie del color queda en el metafield del producto. Excepción: Ágora (cuando se cree en v2) usará "Blanco acrílico" / "Blanco tela" por colisión.
6. **Bases de hormigón con precios invertidos** según decisión: 25 kg = 51,23 € · 30 kg = 102,16 € (antes estaban al revés).

### Resultado en producción

| Producto Shopify | Variantes | Precio | Canales |
|---|---|---|---|
| Parasol cuadrado · aluminio 300×300 cm (Brisa) | 3 | 1.045,32 € | Online Store + Shop |
| Parasol exterior acrílico · mástil regulable Ø200 cm (Pamela acr.) | 24 | 413,19 € | OS+Shop |
| Parasol exterior · mástil regulable 16 colores Ø200 cm (Pamela tela) | 64 | 384,37 € | OS+Shop |
| Parasol exterior acrílico · Ø200 / Ø250 cm (Ocean acr.) | 24 | 398,10 / 414,67 € | OS+Shop |
| Parasol exterior · 16 colores Ø200 / Ø250 cm (Ocean tela) | 19 | 304,13 / 381,54 € | OS+Shop |
| Parasol redondo · aluminio Ø300 cm (Garbí) | 3 | 1.045,32 € | OS+Shop |
| Parasol lateral · aluminio 300×300 cm (Roma) | 3 | 1.897,36 € | OS+Shop |
| Pie de parasol · 40 kg | 2 | 164,14 / 126,88 € | OS+Shop |
| Base de hormigón para parasol | 2 | 51,23 / 102,16 € | OS+Shop |
| **Total** | **144** | | |

**Productos eliminados (6):**
- 4 duplicados puros (Pamela acrílico `-2/-3`, Pamela tela `-2/-3`).
- 2 absorbidos como variante (pie RE, base 30 kg).

**Pendiente v2 (Ágora):** producto que existe en el Excel pero no en Shopify. Requiere `productCreate` desde cero. Documentado en el script como `create_new=True`.

### Bugs resueltos en el camino

- **`gql()` doblando `data["data"]`** en mi función helper. Corregido con `sed s|r\["data"\]\["|r\["|`.
- **Query `tag:envio:xs` devolvía 0** (no por bug previo): aplicado a productos via API.
- **Option value rename**: el piloto de Brisa quedó con "Blanco (tela Balliu)". Fix vía `productOptionUpdate` con `optionValuesToUpdate`.
- **`COLOR_CODES` global ambiguo** (Arena y Azul existen en serie 96 y serie 00): refactorizado a `color_code(color, serie)` con la serie definida por producto.

### Lo que NO se ha hecho (queda para próximas sesiones)

- **Ágora** — crear desde cero (9 variantes con precio por serie de color).
- **Imágenes por variante** — actualmente cada producto mantiene su galería original. Próxima iteración: extraer del JSON scrapeado y mapear color → imagen.
- **Consolidar otras familias Balliu** — tumbonas (16 productos → ~5 modelos), mesas HPL (varios), mesas auxiliares, sillas Etna/Bruna/Selva. Patrón ya validado.
- **Limpiar tags antiguos visibles** (`Balliu`, `match-verde`): tarea F0-02/F0-03 del backlog, no parte de la consolidación.
- **Confirmar peso real de las bases de hormigón con el proveedor** antes del primer pedido (etiquetas físicamente podrían estar invertidas también).

### Patrón validado para escalar

El piloto demuestra que el flujo siguiente funciona end-to-end y se puede aplicar a las otras familias del catálogo:

```
1. WebFetch a la web del proveedor para extraer matriz de variantes real.
2. Cruzar SKUs Excel ↔ modelo proveedor por precio + descripción.
3. Decisiones del dueño sobre naming, ambigüedades y precios.
4. Script declarativo con productos como `dict` (PRODUCTS).
5. Dry-run → apply piloto (--only) → apply resto → delete + publish.
6. Backup previo, reporte CSV, metafields para preservar info original.
```

### Siguiente paso recomendado

Aplicar el mismo patrón a la próxima familia con duplicación (tumbonas Balliu, 16 productos planos). O bien resolver Ágora (rápido, ~30 min) antes de pasar a la siguiente familia.

---

## 2026-05-14 · Auditoría de duplicados + 120 productos invisibles + activación parcial

**Paso del flujo:** validación previa al test de checkout
**Estado:** ⚠️ Hallazgos críticos documentados, decisiones diferidas

### Qué se ejecutó

Mientras se preparaba el test de los 5 escenarios de envío, salieron dos hallazgos importantes que no estaban en la auditoría original (faltaba scope `read_publications`):

#### 1. 120 de 235 productos ACTIVE están publicados a 0 canales (invisibles en la web)

Distribución: **115 productos visibles** (≈ todos los Hevea) y **120 invisibles** (≈ todo el catálogo Balliu). Cuando se importó Balliu se quedaron sin publicar al canal Online Store. La auditoría inicial no lo detectó porque el scope `read_publications` no estaba en el token viejo.

**Acción tomada:** se han publicado **8 productos** al canal Online Store + Shop para desbloquear el test inmediato:
- 4 fundas protectoras (necesarias para el Escenario 1 XS)
- 2 parasoles acrílicos (sacados de DRAFT a ACTIVE hoy)
- 1 cojín exterior (sacado de DRAFT, sin imagen — para test)
- 1 limpiador para mobiliario (sacado de DRAFT — para test)

**Pendiente:** decidir si publicar los **~106 productos Balliu restantes invisibles**. La tienda está bajo password page → publicar no expone nada al público. Es bug operativo histórico, no decisión deliberada.

#### 2. Duplicados en el catálogo (especialmente parasoles)

Detonante: el dueño vio "el parasol 4 veces" en la búsqueda del Admin. Auditoría completa con tres niveles:

- **Nivel 1 — Duplicados puros (~9 productos eliminables)**: mismo SKU + handle con sufijo `-2/-3` (parasol `236bd5f0`×3, parasol `82e48b2d`×3, mesa alta HPL `a3352658`×2, silla Bruna `94b6e5b5`×2, etc.).
- **Nivel 2 — Variantes mal modeladas (~70-80 productos en 7-8 familias)**: productos físicamente distintos del proveedor con título genérico repetido (Tumbona resina × 16, Mesa alta HPL × 6, etc.). NO son duplicados — se deben consolidar como variantes en Sprint posterior.
- **Nivel 3 — SKUs reusados a propósito por Hevea** (`557-010147`, `557-010884`): documentado ya en PROYECTO.md, no se tocan.

**Acción tomada:** documentación completa en [`Agents-IA/auditoria-productos.md`](../../Agents-IA/auditoria-productos.md). Diferido por decisión del dueño — no se aborda en este sprint.

### Activación temporal de DRAFTs para test

Se activaron 4 productos que estaban en DRAFT, **con `inventoryItem.tracked = false`** (stock infinito virtual) para testing. Snapshot del estado previo en `drafts_activation_state.json`. Para revertir cuando termine el test, reaplicar:

```
status: DRAFT (los 4)
inventoryItem.tracked: true (los 4)
```

### Decisiones pendientes que quedan abiertas

1. **¿Publicar los ~106 productos Balliu invisibles ahora?** Recomendado SÍ (bug operativo, tienda bajo password page). Trivial técnicamente.
2. **¿Eliminar los ~9 duplicados puros (Nivel 1) antes del test de checkout?** Recomendado SÍ, pero el dueño lo difiere.
3. **¿Cuándo abordar consolidación de variantes (Nivel 2)?** Recomendado antes del Sprint 4 (rediseño home) — sin consolidar la home muestra catálogo redundante.

### Cosas que actualizar en docs cuando se aborden las tareas

- `PROYECTO.md §3 Balliu`: añadir nota sobre el bug "no publicados al Online Store al importar" como aprendizaje operativo.
- `BACKLOG_SANTAVILA.md`: añadir tarea **F0-08b — Publicar los productos Balliu invisibles al Online Store** + **F0-08c — Eliminar duplicados puros del Nivel 1** + ampliar F0-04 con referencia a `auditoria-productos.md`.
- `AUDITORIA_SANTAVILA.md`: actualizar §1.5 "Apps instaladas / Channels" para reflejar que `resourcePublicationsCount` ahora sí se audita (scope `read_publications` disponible).

### Siguiente paso recomendado

El test de los 5 escenarios de envío puede continuar tal como estaba previsto. Los productos necesarios están publicados. Los hallazgos no bloquean.

Después del test, decisión por parte del dueño sobre las 3 tareas pendientes arriba.

### Validación del sistema de envío ✅ (final del día)

Tests de los 5 escenarios de envío ejecutados por el dueño vía Draft Orders en Admin. **Resultado: todos OK.** Los 3 shipping profiles (XS / M / L) aplican correctamente, el umbral de envío gratuito > 500€ funciona como esperado, y las 271 variantes asignadas vía API responden con su tarifa correspondiente en checkout preview.

**Estado final del sistema de envío al cierre del día:**
- 3 shipping profiles vivos en producción.
- 271 variantes asignadas correctamente por categoría volumétrica.
- 110 productos Balliu siguen invisibles (0 canales) — diferido.
- ~9 duplicados puros del Nivel 1 siguen en catálogo — diferido.
- 4 productos previamente DRAFT siguen ACTIVE con `inventoryItem.tracked=false` (snapshot en `drafts_activation_state.json` para revertir cuando se decida).

### Estado de tareas para la próxima sesión

| Tarea | Estado | Documento |
|---|---|---|
| Publicar los ~106 Balliu invisibles | Pendiente decisión | Este journal |
| Eliminar duplicados puros Nivel 1 | Pendiente decisión | `Agents-IA/auditoria-productos.md` |
| Consolidar variantes Nivel 2 | Diferido a Sprint posterior | `Agents-IA/auditoria-productos.md` |
| Decidir status final de los 4 DRAFTs activados (mantener o revertir) | Pendiente | Snapshot en `drafts_activation_state.json` |
| F0-09 `shopify theme pull` (ya tenemos `read_themes`) | Pendiente | `docs/santavila/BACKLOG_SANTAVILA.md` |
| F1-01 — 31 metafield definitions restantes | Pendiente | `docs/santavila/DATA_MODEL_SANTAVILA.md` |

---

## 2026-05-14 · Setup completo de Shipping Profiles + nueva app OAuth con scopes amplios

**Paso del flujo:** ejecución de la política de envío + ampliación de capacidad técnica
**Estado:** ✅ Aplicado en producción
**Quién:** sesión interactiva, app `Santavila Admin` creada desde cero en Partner Dashboard.

### Qué se ejecutó

**A. Creación de app nueva con scopes amplios.** Tras perder acceso al Partner Dashboard de la cuenta dueña de `API-Products`, se ha creado app nueva `Santavila Admin` (Client ID `1b30f2bd…36126`) con 18 scopes que cubren Sprint 1-2 completo:

```
read_products, write_products, read_files, write_files,
read_content, write_content, read_shipping, write_shipping,
read_themes, write_themes, read_locales,
read_translations, write_translations,
read_orders, write_orders, read_inventory, write_inventory,
read_publications, write_publications
```

Token capturado vía OAuth flow (`get_shopify_token.mjs` adaptado para leer credentials desde `.env`/`.env.local`). Token formato `shpat_…` (38 chars) guardado en `.env.local` como `SHOPIFY_ACCESS_TOKEN`. El token viejo (`shpca_…`) sigue en `.env` como fallback pero ya no se usa (mi script Python lee primero `.env.local`).

**B. Shipping Profiles creados manualmente en Admin.** 3 custom profiles, cada uno con 1 shipping option flat + checkbox "Offer free shipping" min 500€:

| Profile | Tarifa | Min gratis |
|---|---|---|
| `Envío XS - Accesorios` | 9,95€ | 500€ |
| `Envio M - Mediano` | 29,95€ | 500€ |
| `Envio L - Voluminoso` | 57,95€ | 500€ |

Zone: `Pen+Baleares · Spain (48 of 52 provinces)`. Canarias, Ceuta y Melilla excluidas (decisión de política).

**C. Asignación masiva de productos vía API.** Script nuevo [`assign_products_to_shipping_profiles.py`](../../assign_products_to_shipping_profiles.py): lee tags `envio:xs|m|l` aplicados ayer, obtiene variant IDs y los asocia al profile correspondiente vía `deliveryProfileUpdate`. Resultado:

| Profile | Variantes asignadas |
|---|---|
| Envío XS - Accesorios | 10 |
| Envio M - Mediano | 116 |
| Envio L - Voluminoso | 145 |
| **Total** | **271 variantes** · 0 errores |

### Bugs resueltos en el camino

- **Query Shopify por tag con `:`**: la sintaxis `tag:envio:xs` devolvía 0 resultados porque el parser corta en el primer `:`. Corregido a `tag:'envio:xs'` (comillas simples obligatorias). Documentado en el script.
- **CLIENT_SECRET literal del placeholder**: por darle un comando con `"el-secreto-que-has-copiado"` como ejemplo, el dueño lo pegó literal en `.env.local`. Reemplazado por el real (`shpss_…`, 38 chars).
- **App automation token ≠ Admin API token**: el botón "Create token" de Partner Dashboard genera un token de prefix `atkn_` para CI/CD de la app, NO sirve para Admin API. Hay que pasar por OAuth flow → token `shpat_…`. Anotado para no repetir.
- **Nombre de variable**: el token nuevo se pegó suelto en `.env.local` sin la clave `SHOPIFY_ACCESS_TOKEN=` delante. Renombrado y arreglado.
- **Error handling de `get_shopify_token.mjs`**: antes crasheaba con `JSON.parse` cuando Shopify devolvía HTML de error. Reescrito para leer el body como texto, detectar content-type no-JSON y reportar un mensaje claro con la primera parte de la respuesta.
- **Lectura de `.env`/`.env.local`**: scripts y `get_shopify_token.mjs` adaptados para probar 3 nombres por orden de prioridad: `.env.local` (gana) > `.envlocal` > `.env`.

### Decisiones operativas confirmadas

- **Coexistencia de apps**: la app vieja `API-Products` (token `shpca_…`) sigue funcional pero con scopes limitados. La nueva `Santavila Admin` (token `shpat_…`) es la nueva fuente de verdad. El `.env` antiguo se mantiene como red de seguridad mientras dura la transición.
- **Zone Pen+Baleares**: incluye Baleares al mismo coste que península. **Pendiente**: confirmar con proveedores si el coste real Baleares justifica un recargo (probablemente sí, +20-40€ por ferry). Por ahora se asume internamente.
- **5 escenarios de validación** del [SHIPPING_PROFILES_SETUP.md](SHIPPING_PROFILES_SETUP.md) pendientes de probar en checkout preview.

### Estado de bloqueadores

| # | Bloqueador | Estado |
|---|---|---|
| 1 | Política `compareAtPrice` | ✅ |
| 2 | PVP Balliu | ✅ |
| 3 | WhatsApp comercial | ⏸ Esperando SIM |
| 4 | Política envío Balliu | ✅ Implementada en producción |
| 5 | Garantía Balliu | ✅ |
| 6 | Theme versionado dónde | 📝 Se decide al ejecutar F0-09 |
| 7 | **Scopes OAuth ampliados** | ✅ Resuelto con app nueva |

### Siguiente paso recomendado

Sprint 1 sigue avanzando. Tres tareas siguientes en orden:

1. **Validar 5 escenarios en checkout preview** (Paso 4 del SHIPPING_PROFILES_SETUP.md). Especialmente Escenario 3 (multi-categoría sin llegar a 500€ → confirmar que se suman tarifas) y Escenario 5 (multi-categoría + ≥500€ → gratis).
2. **F0-09 — `shopify theme pull`** (~20 min). Ya tenemos `read_themes` activo. Desbloquea toda la Fase 0 visible.
3. **F1-01 — crear los 31 metafield definitions restantes** del namespace `santavila` (`santavila.envio_categoria` ya cuenta como el 1º de 32).

### Reclasificaciones de envío pendientes (anotadas en entrada anterior)

- `balliu-colchoneta-para-tumbona-0e9a3256` (asignada a L, probablemente M)
- `balliu-base-de-parasol-*` y `balliu-pie-de-parasol-*` (asignadas a L, probablemente M)

Cuando se revisen, basta con relanzar `apply_shipping_categories.py --apply --only-handles ...` y luego `assign_products_to_shipping_profiles.py --by-name --apply` (mueve las variantes al profile correcto).

---

## 2026-05-14 · Decisiones estratégicas cerradas (envío, garantía, WhatsApp)

**Paso del flujo:** desbloqueo de pre-Sprint 1
**Estado:** ✅ 3 decisiones cerradas · 1 en espera de hardware
**Quién:** sesión interactiva con dueño del negocio.

### Decisiones cerradas

#### 1. Garantía Balliu = 3 años ✅
Misma cobertura que Hevea. **F0-12 (página Garantía) desbloqueada.** El texto base puede usar "Garantía 3 años en todo el catálogo, ofrecida por nuestros proveedores españoles" sin diferenciar por marca.

#### 2. Política de envío — tarifas volumétricas

Decidida estructura por **3 tiers + umbral de gratuidad**, basada en clasificación de los 281 SKUs del catálogo (script de análisis ad-hoc sobre hoja `20260508 -Todos `):

| Tier | Tarifa cliente | Cubre | # SKUs | % catálogo |
|---|---|---|---|---|
| **XS** | 9,95€ (1 ud) / 14,95€ (2 ud) / 19,95€ (3-4) / 24,95€ (5-8) / 29,95€ (9+) | Cojines, fundas, limpiador, accesorios pequeños | 10 | 4 % |
| **M** | 29,95€ plano | Mesa auxiliar/centro/lateral, mesa ≤ 80 cm, silla individual, taburete, reposapiés, parasol < 250 cm Ø, accesorios resina | 134 | 48 % |
| **L** | 57,95€ plano | Mesa comedor, sofá, conjunto, tumbona, banco, balancín, cama balinesa, parasol ≥ 250 cm Ø, pérgola | 137 | 49 % |
| **Gratis** | 0 € | Pedidos con **subtotal del carrito > 500 €** | — | — |

**Umbral gratuito = 500€** (descartado 400€ para alinear con el AOV objetivo del modelo financiero `00_SUPUESTOS`). Con 500€, **131/281 SKUs (47%)** activan gratis por sí solos, vs 162/281 (58%) con 400€ — diferencia de 31 SKUs en la franja 400-500€ que ahora sí pagan envío. Ese tramo es importante porque es donde está el AOV de campañas Meta/Google y conviene que el cliente lo asuma para que el modelo no pierda margen ahí.

**Validación financiera** (sobre simulación 1 producto/pedido):
- 53% de los pedidos cobran envío al cliente.
- 47% activan gratis → coste interno asumido ≈ 49€ medio por pedido.
- Ratio envío/PVP en el tramo cobrado: 16-30% (coherente con dato real Hevea: mediana 11% a 50€ planos).

**Pendiente operativo:** confirmar tarifa real de Balliu para península. Mientras no llegue, asumimos coste interno ≈ 50€ por pedido Balliu sin gratuidad (mismo orden de magnitud que Hevea). Cuando llegue la tarifa, se rellena la columna `Coste Envío` (J) en `20260508 -Todos ` y el modelo financiero (`02_UNIT_ECONOMICS_SKU`) recalcula automáticamente.

**F0-11 (página Entrega) desbloqueada** con texto definitivo.

#### 3. WhatsApp comercial — en espera ⏸

Pendiente de tarjeta SIM. Cuando llegue, se constata en el proyecto.

**Implicación operativa para Sprint 1:**
- F0-14 (página Contacto): se crea **con email `hola@santavila.com` + formulario nativo Shopify**, sin botón WhatsApp.
- F2-10 (CTA flotante WhatsApp): queda diferida hasta que la SIM esté operativa. Sin entrada en el Sprint actual.

Nota recordatoria: cuando llegue el número, hay tres puntos del theme/sitio donde añadirlo — barra de confianza, footer, página Contacto, CTA secundario en PDPs. Anotado para no olvidar.

#### 4. Theme — dónde versionarlo (pendiente)

Sigue sin decidirse. Recomendación de la auditoría: versionar en `theme/` dentro de este mismo repo. Se decide al ejecutar F0-09 (`shopify theme pull`).

### Resumen del estado de los 6 bloqueadores originales

| # | Bloqueador | Estado |
|---|---|---|
| 1 | Política `compareAtPrice` | ✅ Resuelto (entrada 2026-05-13) |
| 2 | PVP Balliu | ✅ Resuelto (entrada 2026-05-13) |
| 3 | WhatsApp comercial | ⏸ En espera de SIM |
| 4 | Política envío Balliu | ✅ Resuelto (3 tiers + umbral 500€) |
| 5 | Garantía Balliu | ✅ Resuelto (3 años, misma que Hevea) |
| 6 | Theme versionado dónde | 📝 Se decide al ejecutar F0-09 |

### Aplicación técnica de la clasificación de envío (2026-05-14, mismo día)

Tras cerrar la política, se ha ejecutado la parte automatizable:

- **Entregables nuevos:**
  - [`apply_shipping_categories.py`](../../apply_shipping_categories.py) — script Python, mismo patrón que `sync_prices_to_shopify.py` (dry-run por defecto, `--apply`, `--limit`, `--only-handles`).
  - [`SHIPPING_PROFILES_SETUP.md`](SHIPPING_PROFILES_SETUP.md) — guía paso a paso para configurar los 4-5 shipping rates en Admin.

- **Metafield definition creada manualmente:** `santavila.envio_categoria` (single_line_text_field, valores controlados `xs|m|l`).

- **Apply ejecutado contra producción:**
  - 225 productos procesados (los 281 SKUs de la hoja maestra incluyen variantes que comparten handle).
  - **222 ACTUALIZADO · 3 SIN_CAMBIOS · 0 errores.**
  - Distribución final: **XS=6, M=93, L=126.**
  - Cada producto ahora tiene tag `envio:xs|m|l` y el metafield `santavila.envio_categoria`.

- **Reclasificaciones a revisar manualmente (heurística automática es conservadora):**
  - `balliu-colchoneta-para-tumbona-0e9a3256` → marcado **L**. Por nombre no contiene "cojin"/"funda" así que cae en default. Probablemente debería ser **XS** o **M** según peso real. Validar.
  - `balliu-base-de-parasol-*` y `balliu-pie-de-parasol-*` → marcado **L**. Una base/pie de parasol típicamente pesa 15-30 kg. Si la mayoría son <20 kg conviene bajar a **M** (29,95€) — más justo para el cliente. Validar.

- **Bug menor encontrado en docs:** PROYECTO.md menciona `.envlocal` pero el archivo real es `.env.local`. El script ahora prueba 3 nombres por compatibilidad. **Pendiente:** actualizar PROYECTO.md para reflejar la realidad y unificar `sync_prices_to_shopify.py` con el mismo patrón.

- **Estado del usuario:** ejecutando Paso 3 del SETUP (crear las 5 rates en Admin Shopify) en paralelo a este apply. Validación de checkout queda como tarea siguiente.

### Siguiente paso recomendado

Con 5 de 6 bloqueadores cerrados y la clasificación de envío ya en producción:

1. **Validar 5 escenarios en checkout preview** (Paso 4 del [SHIPPING_PROFILES_SETUP.md](SHIPPING_PROFILES_SETUP.md)). Confirmar especialmente Escenario 5 (multi-categoría + umbral 500€ → gratis) que es el más sensible.
2. **Revisar las reclasificaciones marcadas arriba** (colchoneta, bases/pies de parasol). Si hay que mover de L→M, basta `python3 apply_shipping_categories.py --apply --only-handles handle1,handle2` después de editar la heurística.
3. **F0-09 — `shopify theme pull` (20 min).** Desbloquea Fase 0 visible (footer, barra de confianza, badges).
4. **F1-01 — crear los 32 metafield definitions vacíos en Admin (45-60 min).** Lista en [`DATA_MODEL_SANTAVILA.md`](DATA_MODEL_SANTAVILA.md). No rompe nada y desbloquea fases 2-7.

> Nota: la metafield definition `santavila.envio_categoria` creada hoy **ya es 1 de los 32** del modelo de datos. Quedan 31.

---

## 2026-05-13 · Sincronización masiva de precios a Shopify con redondeo psicológico

**Paso del flujo:** F0-01 redefinido — `sync_prices_to_shopify.py`
**Estado:** ✅ Aplicado en producción (`mueblesexterior.myshopify.com`)
**Quién:** sesión interactiva, script existente extendido con `compareAtPrice` + redondeo por segmento.

### Qué se ejecutó

- Extensión de `sync_prices_to_shopify.py`: añadidas funciones `psy_price`, `psy_compare` y `_round_compare_high`; nueva flag `--skip-compare`; query y mutación GraphQL incluyen ahora `compareAtPrice`; reporte CSV con 2 columnas nuevas (`compare_antes` / `compare_despues`).
- Mapeo confirmado contra hoja `20260508 -Todos`:
  - Col E "Coste neto (sin IVA)" → `inventoryItem.cost` (sin redondear).
  - Col F "Precio Venta (con IVA 21%)" → `variant.price` (con redondeo psicológico).
  - `variant.compareAtPrice` = `price_bruto × 1.10` (≥ 50 €) o `× 1.30` (< 50 €), redondeado limpio.
- Reglas de redondeo acordadas **segmentando por PRICE bruto** (no por coste literal del enunciado del usuario — 63/281 productos caían en segmento distinto y los precios resultantes eran más naturales así):
  - **< 50 €**: price termina en .95 — compareAt = bruto × 1.30, entero .00.
  - **50–500 €**: price .95; si cae en `[umbral, umbral×1.05]` baja a `umbral-0.10` (ej. 104→99.90). CompareAt = bruto × 1.10 con mismo truco (`umbral-0.05`).
  - **> 500 €**: price sin decimales, sube al siguiente entero terminado en 0/5/9. CompareAt = bruto × 1.10, busca número "limpio" (100>50>25>10) dentro de `[price_psy×1.05, price_psy×1.12]`.
- Prueba en 1 handle (`balliu-parasol-para-terraza-aluminio-300-cm-3b7e77d1`) → resultado verificado vía Admin GraphQL: price 1.049 €, compareAt 1.150 €, cost 561,54 €.
- Apply masivo a los 224 handles restantes.

### Entregables

- `sync_prices_to_shopify.py` — script extendido con redondeo psicológico y `compareAtPrice`.
- `sync_prices_report.csv` — gitignored, contiene los 281 cambios variant-a-variant.

### Resultado del apply masivo

| Métrica | Valor |
|---|---|
| Handles procesados | 225 / 225 |
| Variantes actualizadas | 270 |
| Sin cambios | 1 (parasol de la prueba previa) |
| Errores | **0** |

**Impacto económico agregado** (dry-run previo, sobre 271 variantes):

- Suma total de prices: **200.710,59 € → 249.326,65 €** (`+48.616 €  / +24,2 %`).
- 115 variantes suben (mediana +46,5 %). Productos NO-Balliu (sofás, sillones, mesas HPL) estaban en Shopify muy por debajo del PVP del Excel.
- 156 variantes bajan (mediana -9,0 %). Productos Balliu estaban en Shopify por encima del PVP del Excel — bajadas ~-21 % consistentes.
- Caso anómalo conocido y aceptado: `balliu-silla-exterior-con-brazos-resina-estilo-funcional…` baja de 251,25 € a 89,95 € (-64 %); revisión del Excel confirmaba coste/PVP correctos.

### Hallazgos clave

- **F0-01 cambió de naturaleza.** El backlog original planteaba VACIAR `compareAtPrice` en bulk para que la tienda dejara de parecer "siempre rebajada". Decisión tomada hoy: en vez de vaciar, **reestructurar** con `compareAtPrice ≈ price × 1.10` (o × 1.30 en productos < 50 €) usando números psicológicos limpios. Resultado: tachado discreto que comunica "buen precio" sin gritar saldo. La tienda ya no tiene compareAt errático (el `980 € → 809,92 €` de BRANDON-1 que disparó el hallazgo original ya no existe — el sillón ahora tiene `price 1189 €` / `compareAt 1300 €` = -8,5 %).
- **Decisión Balliu cerrada** (era §3.5 del journal del Paso 1): SÍ se aplica el PVP recomendado Balliu del Excel. La estrategia diferida queda obsoleta.
- **El precio actual en Shopify difería significativamente del PVP del Excel.** ~47 % más bajo en muchos productos NO-Balliu — sugiere que el catálogo Hevea original se subió con un margen propio inferior al de la tarifa del proveedor. Importante recordarlo si se compara métrica histórica de conversión: el AOV va a cambiar a partir de hoy.

### Decisiones tomadas que cierran bloqueadores del journal anterior

| Bloqueador previo | Estado tras hoy |
|---|---|
| ¿`compareAtPrice` se vacía en masa o producto a producto? | **Resuelto.** Ni una cosa ni otra: se reestructura con regla psicológica `+10%` (o `+30%` en < 50 €). |
| ¿Aplicar PVP recomendado Balliu (156 SKUs bajan ~22 %) o markup propio? | **Resuelto.** Aplicado el PVP recomendado del Excel (con IVA, redondeado psicológicamente). |

### Prioridades vivas (sin cambios respecto al journal anterior)

F0-02 (vendor → Santavila), F0-03 (limpiar tags B2B), F0-07 (2 productos sin imagen), F0-09 (theme pull), F1-01/F1-02 (metafield y metaobject definitions). Todas siguen pendientes.

### Siguiente paso recomendado

- **Validación visual ligera:** abrir 4-5 PDPs en la admin de Shopify y confirmar que el tachado se renderiza con descuento entre 5-12 % y que no hay precios con decimales inesperados en gama alta.
- Cuando el pricing esté validado por el dueño, retomar **F0-02 → F0-03 → F0-09** como bloque siguiente de la Fase 0.

---

## 2026-05-13 · Cierre administrativo del Paso 1 (auditoría)

**Paso del flujo:** 1 — `00_PROMPT_ARRANQUE_AUDITORIA.md`
**Estado:** ✅ Entregables ya existentes. Sin reejecución.
**Quién:** snapshot original generado el **2026-05-06** contra `mueblesexterior.myshopify.com` vía Admin GraphQL API 2026-01 (autenticado como `hola@santavila.com`).

### Qué se ejecutó hoy

- Revisión de los 4 documentos ya presentes en `docs/santavila/`.
- Creación de este `JOURNAL.md` como registro vivo del plan.
- Decisión deliberada de **no regenerar** los documentos para no sobrescribir trabajo válido (la auditoría es de hace 7 días, sigue siendo representativa).

### Entregables vigentes

| Documento | Líneas | Estado |
|---|---|---|
| [`AUDITORIA_SANTAVILA.md`](AUDITORIA_SANTAVILA.md) | 324 | ✅ Completo, con datos reales del catálogo |
| [`BACKLOG_SANTAVILA.md`](BACKLOG_SANTAVILA.md) | 717 | ✅ Tareas con IDs estables `F0-01`, `F1-02`, … |
| [`DATA_MODEL_SANTAVILA.md`](DATA_MODEL_SANTAVILA.md) | 450 | ✅ 32 metafields `santavila.*` + 8 metaobjects `sv_*` definidos |
| [`THEME_PLAN_SANTAVILA.md`](THEME_PLAN_SANTAVILA.md) | 366 | ✅ 19 secciones `sv-*` planificadas. Asume `shopify theme pull` previo (F0-09) |

### Hallazgos clave (lo más cargado de información)

#### Estado real del catálogo (snapshot 2026-05-06)
- **235 productos**: 231 ACTIVE, 4 DRAFT (cifras de la API; difieren de los 252 anotados en `PROYECTO.md` del 24/04 — la tienda ha movido catálogo entre fechas).
- **Distribución por vendor real:** Balliu 120, Hevea 115.
- **7 colecciones**, todas por tipo de mueble. Cero con descripción ni SEO.
- **0 metafields del namespace `santavila`**. **0 metaobjects.** Greenfield total.
- **0 productos con `santavila.producto_hero`** marcado.

#### Bloqueadores de percepción premium (P0)
1. **Descuento permanente en toda la tienda.** BRANDON-1: `compareAtPrice=980€` / `price=809,92€`. Confirmado: la tienda hoy parece "siempre rebajada".
2. **Vendor real expuesto.** `vendor = "Hevea"` o `"Balliu"` en los 235 productos. Algunos handles llevan prefijo `balliu-…` que se ve en URL.
3. **Tags B2B expuestos al cliente final.** `match-verde / match-rojo / match-amarillo` en los 120 productos Balliu (probablemente vienen de la app "Wholesale Pricing Discount B2B"). Tag `hostelería` visible en PDPs residenciales.
4. **Typo público en H1**: colección `sillones-de-exterior` con título `"Sofas de exterior"` (sin tilde, y handle desalineado del título). Es H1 + URL al mismo tiempo.

#### Bloqueador estructural (P0)
5. **Modelo de datos = 0.** Plazo, garantía, montaje, material estructurado, espacio, mantenimiento, peso, bultos: nada existe como metafield. La información vive dispersa en HTML libre y en `Santavila.xlsx`. **Sin esta capa, las fases 2-7 del plan son cosmética**.

#### Otros hallazgos relevantes
- **71 productos sin ALT** en imagen principal. **2 productos sin imagen principal.**
- **21 productTypes para 235 productos** con duplicidades por capitalización/acentos (`Sofá`/`Sofa`, `Accesorios`/`Accesorio`).
- **Peso del producto = 0 kg** detectado en BRANDON-1. Probablemente generalizado. Dato logístico crítico.
- **Idioma en producto:** 100 % español (no hay títulos en inglés). Bien.
- **Idioma en theme/footer/correos:** no auditable hoy — scope OAuth actual NO incluye `read_themes` ni `read_content`. Marcado como pendiente de inspección visual.
- **Imágenes de proveedor expuestas en URL** vía prefijo `balliu-` en handles. Conviene migrar nombre en futuras altas pero **NO cambiar handles vivos sin redirect 301** (F0-05 contempla esto solo para la colección con typo).

### Prioridades vivas (P0 — Fase 0 + arranque Fase 1)

| ID | Tarea | Por qué es P0 |
|---|---|---|
| **F0-01** | Eliminar `compareAtPrice` permanente | Toda la tienda parece rebajada |
| **F0-02** | `vendor = "Santavila"` + crear `santavila.proveedor` interno | Marca coherente |
| **F0-03** | Limpiar tags `Hevea`, `Balliu`, `match-*`, `hostelería` visibles | Datos internos en storefront |
| **F0-07** | Resolver los 2 productos sin imagen principal | No se pueden vender así |
| **F0-09** | `shopify theme pull` del theme actual | Bloquea toda la Fase 0 visible (F0-10, F0-15, F0-16) |
| **F1-01** | Crear los 32 metafield definitions `santavila.*` | Palanca de todo lo demás |
| **F1-02** | Crear los 8 metaobject definitions `sv_*` | Palanca |
| **F1-03** | Poblar `sv_supplier` con Hevea y Balliu | Base para F0-02 |

Fase 0 completa (idioma, footer, claims, páginas Entrega/Garantía/Mantenimiento, barra de confianza, badges de valor) se ataca en paralelo a Fase 1 — son tareas independientes.

### Decisiones pendientes que bloquean el siguiente paso

Antes de pasar al **prompt 02 (sprints)** y empezar a ejecutar Sprint 1 sobre Shopify, hay decisiones de negocio que cerrar. Ya están listadas en `plan_santavila.md §24` y se reflejan aquí filtradas por las que bloquean acciones concretas:

1. **¿Hay WhatsApp comercial?** Bloquea F0-14 (página Contacto) y F2-10 (CTA flotante).
2. **¿`compareAtPrice` se vacía en masa o se decide producto a producto?** Bloquea F0-01.
3. **¿Política Balliu de envío gratuito a península?** Bloquea texto de F0-11 (página Entrega). Hevea ya está confirmado (>900€).
4. **¿Garantía Balliu confirmada?** Hevea = 3 años validados. Balliu = pendiente. Bloquea F0-12 y los datos de `garantia_resumen`.
5. **¿Aplicar PVP recomendado Balliu (156 SKUs bajan ~22%) o mantener markup propio?** Decisión comercial diferida según `PROYECTO.md §3.c`. No bloquea el Sprint 1 pero condiciona la home y los productos héroe.
6. **¿Theme actual versionar en este repo o en uno aparte?** F0-09 sugiere versionar en `theme/` dentro del repo.

### Riesgos no resueltos del entorno

- **Scopes OAuth insuficientes para auditar todo.** El token actual lleva `read_products,write_products,read_files,write_files`. **Faltan:** `read_content` (páginas, navegación, policies), `read_locales`, `read_themes`. Antes del Sprint 1, ampliar scopes en la app del Partner Dashboard, generar nuevo token y guardar en `.envlocal`.
- **Referencia rota detectada:** `BACKLOG_SANTAVILA.md` y `DATA_MODEL_SANTAVILA.md` apuntan a `../../plan_santavila_shopify/plan_santavila.md`, pero el plan vive en `Agents-IA/plan_santavila.md`. Conviene corregir los enlaces. **No es bloqueante** — el contenido es correcto.
- **Score B2B `match-*`** de origen sin documentar. Antes de eliminar (F0-03), confirmar si los consume alguna app activa.

### Siguiente paso recomendado

**Opción A — Cerrar decisiones de negocio primero (recomendado).**
Responder a las 6 preguntas anteriores. Sin eso, el Sprint 1 se ejecuta con placeholders y se corrige luego. Tiempo estimado: 1-2 horas con el dueño del negocio.

**Opción B — Empezar Sprint 1 ya con lo que no depende de decisiones pendientes.**
Tareas que no requieren decisión humana:
- `F0-06` — añadir ALT a 71 productos.
- `F0-07` — resolver 2 productos sin imagen.
- `F0-08` — auditar 4 productos en DRAFT.
- `F0-04` — normalizar 21 `productType` a 8-10 valores.
- `F0-05` — fix typo "Sofas" → "Sofás" + redirect 301.
- `F1-01` — crear 32 metafield definitions vacíos en Admin (no rompen nada, no necesitan datos).
- `F1-02` — crear 8 metaobject definitions vacíos.

**Opción C — Saltar al prompt 02 (sprints).**
Pegar `02_PROMPT_IMPLEMENTACION_SPRINTS.md` en Antigravity para que un agente arranque Sprint 1 con los entregables actuales como base. **Solo si las decisiones pendientes están cerradas** o se acepta usar placeholders.

> **Recomendación de este journal:** Opción A → luego Opción C. Sin las 6 decisiones cerradas, Sprint 1 genera trabajo que hay que rehacer.

### Limitaciones honestas de la auditoría del 2026-05-06

Estas limitaciones están reconocidas en el propio `AUDITORIA_SANTAVILA.md` y conviene tenerlas presentes:

- **Footer, menú, mobile, carrito, páginas legales: no auditados** (sin acceso al theme ni a `pages`).
- **Apps instaladas: hipótesis basada en metafields auto-creados**, no confirmadas.
- **Schema, sitemap, indexabilidad: no auditados** por API.
- **Configuración de Markets, checkout y locales: no auditadas** por scope.

Estas zonas oscuras se resuelven en F0-09 (theme pull) + ampliación de scopes OAuth.

---

## Plantilla para próximas entradas

```markdown
## YYYY-MM-DD · [Título del hito]

**Paso del flujo:** X — `nombre_del_prompt_o_sprint.md`
**Estado:** ✅ / 🔄 / ⏸
**Quién/qué:** [agente, modelo, persona]

### Qué se ejecutó
- …

### Entregables
- `ruta/al/archivo.md` — [una línea]

### Hallazgos clave
- …

### Prioridades vivas tras este hito
- …

### Decisiones pendientes
- …

### Siguiente paso recomendado
- …
```
