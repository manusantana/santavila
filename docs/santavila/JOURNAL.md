# JOURNAL — Santavila / Transformación ecommerce

> Bitácora de ejecución del plan documentado en [`../../Agents-IA/plan_santavila.md`](../../Agents-IA/plan_santavila.md).
> Una entrada por hito. Cada entrada deja claro: **qué se hizo, qué hay que tener en cuenta y qué bloquea lo siguiente.**

---

## Cómo se usa este journal

- Entradas **en orden cronológico inverso** (lo más reciente arriba).
- Cada entrada lleva: fecha, paso del flujo (ver [`../../Agents-IA/INDEX.md`](../../Agents-IA/INDEX.md)), qué se ejecutó, entregables, hallazgos clave, prioridades vivas, decisiones pendientes y siguiente paso recomendado.
- Cuando el paso siguiente se ejecuta, se añade una entrada nueva arriba — **no se reescribe la anterior**.

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
