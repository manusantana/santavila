# JOURNAL — Santavila / Transformación ecommerce

> Bitácora de ejecución del plan documentado en [`../../Agents-IA/plan_santavila.md`](../../Agents-IA/plan_santavila.md).
> Una entrada por hito. Cada entrada deja claro: **qué se hizo, qué hay que tener en cuenta y qué bloquea lo siguiente.**

---

## Cómo se usa este journal

- Entradas **en orden cronológico inverso** (lo más reciente arriba).
- Cada entrada lleva: fecha, paso del flujo (ver [`../../Agents-IA/INDEX.md`](../../Agents-IA/INDEX.md)), qué se ejecutó, entregables, hallazgos clave, prioridades vivas, decisiones pendientes y siguiente paso recomendado.
- Cuando el paso siguiente se ejecuta, se añade una entrada nueva arriba — **no se reescribe la anterior**.

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
