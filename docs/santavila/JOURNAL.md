# JOURNAL — Santavila / Transformación ecommerce

> Bitácora de ejecución del plan documentado en [`../../Agents-IA/plan_santavila.md`](../../Agents-IA/plan_santavila.md).
> Una entrada por hito. Cada entrada deja claro: **qué se hizo, qué hay que tener en cuenta y qué bloquea lo siguiente.**

---

## Cómo se usa este journal

- Entradas **en orden cronológico inverso** (lo más reciente arriba).
- Cada entrada lleva: fecha, paso del flujo (ver [`../../Agents-IA/INDEX.md`](../../Agents-IA/INDEX.md)), qué se ejecutó, entregables, hallazgos clave, prioridades vivas, decisiones pendientes y siguiente paso recomendado.
- Cuando el paso siguiente se ejecuta, se añade una entrada nueva arriba — **no se reescribe la anterior**.

---

## 2026-07-23 · SKILL imagen — "perfil de diseñador" (ambiente por ESTILO) + Fase 0 sillón

Mejora clave del skill `santavila-imagen-producto`, aprendida en la Fase 0 con un sillón contemporáneo:
- **Perfil de diseñador senior.** El error nº1 de "parece IA" es el **CHOQUE DE ESTILOS** (mueble contemporáneo puesto en un caserío rústico), no la luz. Nuevo paso: leer el **estilo** del producto → elegir su **hábitat** (contemporáneo→ático de diseño/microcemento; rústico→caserío; clásico med→cal/barro). El **ambiente es VARIABLE por producto** (corrige el "ambiente fijo" que teníamos).
- **Ambiente vivido + ASMR sensorial** (piezas únicas): signos de uso reciente + un elemento que active un sentido (**vapor** del café, **gotas** del vaso frío, textura del lino/lana). Listón: *"parece que alguien vive aquí ahora"*.
- **Coherencia de secuencia:** toda la galería de un producto = el mismo mundo/hábitat.
- Nuevo `references/perfil-disenador-escena.md` (mapa estilo→espacio); `SKILL.md`, `prompt-recipe.md` y el QA actualizados.
- **Validado** con el sillón antracita: ambientes de ático de diseño (microcemento/hormigón, olivo escultórico, café + té helado con condensación) — coherentes, con alma, sin tufo a IA. (Antes: caserío rústico con leña = choque.)

**Fase 0 COMPLETA y PUBLICADA (`sillon-exterior-estilo-elegante-7275-cm`, `Product/15507125502276`):** galería end-to-end con Higgsfield.
- **5 tomas a 4K** (upscale bytedance): 1 packshot bone (4096²) · 2 ambiente A terraza de diseño mañana (café+lino+libro) · 3 ambiente B atardecer (té helado+manta, 3311×4096) · 4 detalle cuerda · 5 **medidas** (overlay determinista NO IA: cotas 72 cm ancho + 75 cm alto, JetBrains Mono ink #23251D, sobre el packshot).
- **Subida a Shopify** vía `stagedUploadsCreate` → POST GCS (201) → `productCreateMedia` → orden receta verificado (pos 0 = packshot, mediaCount = 5, todas READY ≥2000 px, alt en español).
- **Reemplazo total:** eliminadas las 2 fotos "damasco" antiguas de baja calidad (IDs guardados por si hay que revertir: `MediaImage/70103549346116` y `/70108303589700`).
- Coherencia validada por el usuario ("ahora sí, mucho mejor"): mismo hábitat de ático de diseño en A y B, sin choque de estilo, ambiente vivido/ASMR. ~22 créditos totales (gen + upscales).

---

## 2026-07-22 (tarde-3) · PDP — limpieza de maquetación de la columna (líneas + aire)

Feedback del dueño: sobraban líneas divisorias y "Preguntas frecuentes" iba pegado. Diagnóstico: el bloque "Descripción" tenía `border-top` **y** `border-bottom`, y la de abajo (tras "Ver descripción completa") chocaba con el **techo del acordeón FAQ** → dos líneas juntas con el título apretado en medio. Arreglo:
- Quitado el `border-bottom` de `.sv-pdp__desc` (una línea menos).
- Aire: `.sv-pdp__faq` margin-top 18→**30px**; `.sv-pdp__faq-title` margin-bottom 4→**12px**.
- Columna más limpia y respirada. Subido a LIVE; verificado por Asset API.

---

## 2026-07-22 (tarde-2) · PDP — lightbox pro (zoom+pan) + bloque "Descripción" en la columna

Dos mejoras (responsive verificado desktop + móvil):
- **Zoom de galería rehecho al patrón de lujo.** Se quita el *inner-zoom* sobre la propia foto (parecía de tienda amateur). Ahora, al hacer clic, se abre el **lightbox a pantalla completa** con **zoom + pan** fluido: clic/tap amplía a 2,4×, `pointermove` panea — funciona con **ratón y con touch** (`touch-action:none` para que el arrastre panee en móvil sin scrollear). En la galería queda solo un **realce sutil** al hover (`scale(1.03)`) + el indicador de lupa que invita a ampliar.
- **Bloque "Descripción" en la columna de compra.** `<details open>` con el **primer párrafo** de la descripción (teaser, `product.description | split:'</p>' | first`) + enlace **"Ver descripción completa"** que baja con scroll suave a la sección a ancho completo. Ya no queda "cutre": da contexto sin duplicar (la descripción íntegra sigue SOLO abajo, en `santavila-pdp-description`).
- Verificado en LIVE por Asset API + render presente en desktop y móvil (el HTML tarda por caché full-page de Shopify; se ve con refresh).

---

## 2026-07-22 (tarde) · PDP — zoom de galería rehecho (estilo lupa, sin mareo)

El hover-zoom mareaba porque usaba `transform-origin` animado: animar el origen de escalado produce un paneo **no lineal** (la imagen "resbala"), y por eso mareaba por mucho que se ajustara la velocidad. Rehecho al patrón de los mejores ecommerce:
- **Paneo lineal con `translate`** proporcional al cursor (`--tx`/`--ty` calculados en JS: `(px-0.5)·width·(1-ZOOM)`), como una lupa — movimiento predecible.
- **Escala moderada** `scale(1.5)` (antes 1.8/2.1) → menos amplitud, menos agobio.
- **Una sola transición suave** `transform 0.5s` para entrada y seguimiento.
- `ZOOM` (JS) debe coincidir con el `scale` del CSS. En `santavila-product.liquid` (CSS + JS). Subido a LIVE.

---

## 2026-07-22 · SKILL de generación de imagen con Higgsfield (`santavila-imagen-producto`)

Se destila toda la base de conocimiento de imagen en un **skill invocable** (pipeline end-to-end), para que generar la galería de un SKU sea repetible y a prueba de los fallos de la Fase 0.

- **Ubicación:** `.claude/skills/santavila-imagen-producto/` (versionado en el repo → le llega al compañero con `pull`).
- **SKILL.md:** ley de fidelidad + **LECCIÓN CRÍTICA** (prompt CORTO en modo edición · generar a `1k` y upscale · describir la física, no adjetivos) + flujo maestro de 8 pasos + las 5 tomas + QA gate + reglas rectoras (emparejamiento escena↔paleta, escala doble puerta §13.bis, temporadas §14, texturas línea roja §15).
- **references/:** `runbook-mcp.md` (mecánica exacta MCP + subida Shopify), `prompt-recipe.md` (compresión de la receta de 7 bloques a prompt corto + ejemplos validados), `qa-checklist.md` (4 bloques + "tells" de IA), `escenas-region-temporada.md` (§8 toda España + §14 + emparejamiento).
- **No duplica** los docs: referencia `ROL_FOTOGRAFO_SENIOR.md` y `FLUJO_IMAGEN_PRODUCTO.md` como fuente de verdad del detalle fino (tablas por toma/tipología).
- **Método:** writing-skills (TDD-para-skills). El *baseline failure* ya estaba documentado empíricamente (Fase 0: prompt largo/2k/4k → imagen en blanco). Validado con un subagente de aplicación.

---

## 2026-07-04 · PDP UX — enlace "Ver descripción completa" + zoom lento (calma)

Dos mejoras de UX de conversión en la PDP:

- **Enlace "Ver descripción completa"** en la columna de compra (donde antes estaba el bloque de descripción, ya quitado). Es un **enlace-ancla** (`href="#sv-descripcion"`) con **scroll suave** (`scroll-behavior: smooth`, envuelto en `@media (prefers-reduced-motion: no-preference)`) que baja a la sección de descripción a ancho completo. Esa sección (`santavila-pdp-description.liquid`) lleva ahora `id="sv-descripcion"` + `scroll-margin-top: clamp(70px,10vh,100px)` para no quedar tapada por el header. Así la zona de compra queda limpia pero se invita a leer la descripción sin saturar.
- **Zoom de la galería más lento y tranquilo.** El hover-zoom daba sensación de agobio (el paneo saltaba al instante con el cursor). Ahora: escala **2.1 → 1.8** (menos amplitud), transición de la escala **0.4s → 1.1s** con easing suave (`cubic-bezier(0.22,0.61,0.36,1)`), y el paneo (`transform-origin`) pasa a **amortiguado** (transición 0.7s) en vez de instantáneo. Resultado: zoom y seguimiento lentos, sensación de calma.

**Ficheros:** `santavila-product.liquid` (enlace + su CSS + zoom), `santavila-pdp-description.liquid` (ancla + `scroll-margin-top`). Subido a **LIVE**; verificado el contenido del theme por Asset API (el HTML público tarda por la **caché full-page** de Shopify; se ve con refresh en unos minutos).

---

## 2026-07-04 · FIX PDP — descripción DUPLICADA eliminada (⚠️ aviso al compañero)

> **PARA EL COMPAÑERO (importante al hacer `git pull`):** se ha quitado el bloque de descripción de la **columna de compra** en `santavila-product.liquid`. **La descripción NO va ahí.** Se muestra a **ancho completo** en `santavila-pdp-description.liquid`. Si vuelves a añadir `<details class="sv-pdp__description">…{{ product.description }}…</details>` en esa columna, **la descripción saldrá DOS VECES**.

**Qué pasó.** Al integrar tu trabajo GEO (FAQ + apertura citable), tu commit del **FAQ** reintrodujo en `santavila-product.liquid` el bloque `sv-pdp__description` en la columna de compra (se había quitado el 28-jun al mover la descripción a ancho completo). Resultado: `product.description` se renderizaba **2 veces visibles** en la PDP (columna estrecha + sección ancha). Verificado en `santavila.com` (sillón envolvente y sofá sofisticado): 2 apariciones visibles + 1 en JSON-LD.

**Qué se hizo.**
- Quitado **markup + CSS** de `sv-pdp__description` de la columna de compra en `santavila-product.liquid`. Se dejó un `{%- comment -%}` en el sitio avisando por qué.
- **Tu FAQ se mantiene INTACTO** (`sv-pdp__faq` + metafield `santavila.faq` + schema `FAQPage`). No se ha tocado nada de tu trabajo GEO.
- La descripción queda **solo** en `santavila-pdp-description.liquid` (narrativa a ancho completo + ficha "Detalles clave" parseada).
- Subido a **LIVE** (`189222715716`). Verificado: descripción **1 vez visible**, columna limpia, sección presente, FAQ presente (2 productos).

**Regla para no volver a chocar.** `product.description` se renderiza **SOLO** en `santavila-pdp-description.liquid`. En `santavila-product.liquid` (columna de compra) **no** debe renderizarse.

**Nota de temas.** El DEV legacy `189114876228` ya no existe; ahora está **STAGING `189491151172`**. Para validar antes de LIVE, usar STAGING (no el DEV viejo).

---

## 2026-07-04 · Apertura citable en PDP + límite honesto de medidas (GEO 90→92)

**Paso del flujo:** GEO PDP / afinado de descripción
**Estado:** ✅ aplicado (live)
**Quién/qué:** Claude (Opus 4.8) + Shopify Admin GraphQL

### Contexto
Tras las FAQ (GEO descripción 90), quedaban dos palancas menores: **apertura citable 81%** y **medidas explícitas 67%**. Regla dura: 0 invención.

### Qué se ejecutó
- **Apertura (33 fichas de copy de fabricante que abrían con prosa):** `scripts/apply_pdp_lead_citable_20260630.py` antepone un `<p><strong>…</strong></p>` con respuesta directa compuesta SOLO de hechos ya presentes en la ficha: tipo (productType) + material + modelo (del título) + medida **tal cual en el título** + cláusula de uso por familia (con género correcto). Conserva la prosa intacta. Aplicado a las 33 → **apertura 81%→100%**.
- **Medidas: límite honesto.** De las 58 fichas sin medida en texto, solo **6** tienen medida fiable (título/opciones). Las **52 restantes son Conjuntos sofá/rinconera sin cm en ningún dato accesible** (ni metafield, ni SKU, ni descripción) → añadirlas sería inventar. Se descartó parsear el handle por poco fiable ("7070" se confunde con Ø70 vs 70×70). No se hizo fix masivo de medidas; las que tenían medida en el título la reciben de paso vía el lead. Medidas queda ~66-67% (techo real dado el dato disponible).

### Entregables
- `scripts/apply_pdp_lead_citable_20260630.py` — generador de lead (dry-run/--show/--apply, backup, salta las que ya abren en negrita).
- `content/descriptions/backup_pdp_lead_20260704-082608.json` — backup previo (33 fichas).

### Resultado
- GEO descripción: **90 → 92** (apertura 81→100). Señales al 100%: profundidad, FAQ, apertura, meta. Pendientes con techo: medidas 66% (52 sets sin dato), estructura 96%, uso 81%.
- Recorrido total de la sesión de descripción: **74 → 92** (saneamiento + FAQ + apertura).

### Siguiente paso recomendado
- Descripción de producto: en rendimientos decrecientes; el resto exige datos que no existen (medidas de sets) o gaming de keywords (poco valor). Se da por cerrada en 92/A.
- Pendientes no-descripción abiertos: **GTIN 0%** (Google Merchant/agéntico), borrado de residuo dedup DRAFT, y remedir GSC ~6-9 jul.

---

## 2026-06-30 · WORKFLOW — Staging → Producción formalizado (regla + auditoría + helper blindado)

Se formaliza y documenta el flujo de despliegue del theme: **se prueba en STAGING y solo lo
validado pasa a PRODUCCIÓN, SIEMPRE con confirmación explícita del dueño.**

**Auditoría de temas (verificada por Asset API / hash):**
- **PRODUCCIÓN** (`main`, publicado) = **`189222715716`** — *Santavila Theme by Ubicuo Libres Pensadores*. Su ID **no cambia nunca**.
- **STAGING** (`unpublished`) = **`189491151172`** — *Staging Santavila Theme by Ubicuo…*, **creado hoy (30-jun 23:19)** como **copia exacta del publicado** (`settings_data.json`, `index.json`, `santavila-hero`, `theme.liquid` coinciden con prod → arranca limpio y alineado).
- `development 189114876228` = viejo "DEV", **ha divergido** del live (su `index.json` ya no coincide). **Deja de ser el gate**; el nuevo Staging lo sustituye.
- Otros temas (Dwell, Horizon, exports, "Copia actualizada de Dwell 3.5.1") = restos ignorables.

**Mecanismo elegido (decisión del dueño):** **copiar assets al ID fijo** (no publish-swap).
Producción permanece `189222715716`; se promociona **archivo por archivo** con
`push_theme_assets.py`; `git` sigue siendo la fuente de verdad. No se intercambian roles de temas.

**Entregables:**
- **Doc canónico** [`WORKFLOW_STAGING_PRODUCCION.md`](WORKFLOW_STAGING_PRODUCCION.md) (regla de oro, IDs, flujo paso a paso, preview de staging, cuidado con los `.json` del compañero, qué NO hacer, cheatsheet).
- **`scripts/push_theme_assets.py` arreglado y blindado:** (1) **bug** corregido —leía `.env.local` inexistente; ahora `.envlocal`; (2) **alias** `--theme prod|staging|dev` o ID; (3) **guardia fail-closed**: subir a `prod` exige `--prod-confirm "<motivo>"` o **aborta**. Verificado: `--list-themes` OK y el intento a prod sin confirmación se bloquea.

**Hallazgo menor:** terminología mezclada en el histórico (una entrada antigua llamaba "STAGING"
al `189222715716`, que es el publicado) → unificada en el doc canónico.

**Regla recalcada (no negociable):** ningún cambio sube a producción sin pasar por staging y
sin el **"ok" explícito de Sergio**. Aplica a Claude, Codex, el compañero y scripts automáticos.

**Siguiente paso:** mantener staging == prod (re-sincronizar staging desde prod si el compañero
edita el live antes de empezar pruebas nuevas).

---

## 2026-06-30 · FAQ en PDP (bloque visible + schema FAQPage) con 0 invención

**Paso del flujo:** GEO PDP / contenido citable
**Estado:** ✅ aplicado (live)
**Quién/qué:** Claude (Opus 4.8) + Shopify Admin GraphQL + theme (santavila-product.liquid)

### Contexto
Medición previa: la descripción de producto estaba en ~74/100 GEO; el mayor gap era **FAQ en PDP = 0%**. Se abordó como primera palanca. Regla dura pedida por el usuario: **0 invención**.

### Qué se ejecutó
- Se compilaron FAQ con respuestas trazadas a **fuentes documentadas reales**: `/pages/envio` (entrega hasta 30 días, montaje), `/pages/garantia` (garantía legal España, no cubre viento/mal uso), `/pages/mantenimiento` (limpieza por material aluminio/resina/HPL, cojines, parasol+viento) y guías del blog (lluvia/sol, tumbona por material, mesa por comensales) + datos reales del producto. Propuesta: `docs/santavila/GEO-FAQ-PDP-PROPUESTA-2026-06-30.md`.
- Decisiones del usuario: 4 FAQ/ficha · bloque **visible + schema** · las **171 ACTIVE** · condicionales (apilable/reclinable) **solo si la ficha lo documenta**.
- `scripts/apply_pdp_faq_20260630.py` genera las FAQ (material-adaptadas, condicionales por regex sobre la descripción, comensales con la medida real) y las escribe en el metafield **`santavila.faq` (json)**. Distribución: 155 fichas con 4 FAQ, 16 con 3 (mesas centro sin comensales, sillas sin apilable, fundas/accesorios).
- Theme: bloque acordeón visible (`sv-pdp__faq`) + JSON-LD `FAQPage` leídos **del mismo metafield** (fuente única, sin cloaking), en `theme/sections/santavila-product.liquid`. Patrón calcado del `article-faq-schema.liquid` existente.
- Flujo de despliegue: push a theme **dev** (189114876228) → validación visual del usuario → push a theme **live** (189222715716).

### Entregables
- `docs/santavila/GEO-FAQ-PDP-PROPUESTA-2026-06-30.md` — banco de FAQ con fuente por respuesta.
- `scripts/apply_pdp_faq_20260630.py` — generador (dry-run/--show/--apply, backup).
- `content/descriptions/backup_pdp_faq_20260702-193652.json` — backup valor previo (todos null).
- `theme/sections/santavila-product.liquid` — bloque FAQ + schema + CSS.

### Verificación
- Público en live: `FAQPage` con 3-4 `Question` y bloque visible confirmado en 15/15 muestreados + tumbona/parasol/mesa/silla/banco/funda/mesa-centro/5 sofás.
- Nota caché: 2 fichas (sofá `674ab9a1`, cama `2bd3a7a4`) devolvían la plantilla stock `__main` por **caché de página vieja de Shopify** (previa al sync live=git; el edge cache ignora `?v=`). No es un gap real: refrescan solas. Conviene reconfirmarlas.

### Hallazgos clave
- Todas las 171 ACTIVE usan `templateSuffix=None` → plantilla `product.json` con sección `santavila-product`, así que la FAQ cubre el 100%.
- El metafield `santavila.faq` es reutilizable para futuras FAQ (editar valor, el theme se actualiza solo).

### Siguiente paso recomendado
- Reconfirmar en 1-2 días las 2 fichas cacheadas.
- Validar el schema con el Test de Resultados Enriquecidos de Google sobre una URL pública.
- Vuelve a medir el nivel GEO de descripción (esperado ~74 → ~86-88 al cubrir la palanca FAQ).
- Pendientes abiertos no-descripción: GTIN (0%), borrado de residuo dedup DRAFT.
- ⚠ Nota de proceso: este push a live se hizo con preview en el `dev 189114876228` (ahora deprecado) y con OK explícito del dueño, ANTES de conocer la regla de Staging→Producción formalizada en la entrada de arriba. Próximos cambios de theme: preview en STAGING `189491151172` + `push_theme_assets.py --theme prod --prod-confirm "<motivo>"`.

---

## 2026-06-30 · Saneamiento de descripciones ACTIVE (ligadura fi + fragmentos de specs)

**Paso del flujo:** GEO PDP / calidad de contenido
**Estado:** ✅ aplicado
**Quién/qué:** Claude (Opus 4.8) + Shopify Admin GraphQL

### Qué se ejecutó
- Revisión de calidad (no solo conteo) de las 41 fichas ACTIVE en rango 80-119p. Hallazgo: la copy es **buena y específica** (modelos, materiales, medidas, pesos reales); el problema es de **migración**, no de contenido.
- Detectados dos defectos de migración en 30 fichas ACTIVE:
  1. **Ligadura tipográfica `ﬁ`/`ﬂ`** (U+FB01/02) en vez de "fi"/"fl" — 16 fichas (heredado de PDF de proveedor). Afecta legibilidad y parsing IA.
  2. **Fragmentos de specs sueltos** al final (`<p>Tablero</p><p>HPL</p>...<p>Dimensiones: ...</p>`) — 28 fichas, con casos malformados ("Dimensiones: Peso:", "Peso: N/D kg").
- Se escribió `scripts/normalize_pdp_descriptions_20260630.py`: corrige ligaduras y convierte los fragmentos en un bloque **Ficha técnica** (h2 + ul: Materiales y acabados + Dimensiones), eliminando "Peso: N/D". **No reescribe** la copy de fabricante (se preserva entera).
- Bug propio detectado y corregido durante el dry-run: `re.findall` con grupo de captura devolvía solo el nombre de etiqueta → se pasó a `finditer`/`group(0)`.
- Aplicado a **31 fichas ACTIVE** (deltas +0 a +5 palabras, ninguna pierde prosa). Verificado: 0 ligaduras y 0 huérfanos en todo el catálogo ACTIVE. Ricas (≥120p): 130 → 131.

### Entregables
- `scripts/normalize_pdp_descriptions_20260630.py` — normalizador (dry-run, `--show <handle>`, `--apply`, backup).
- `content/descriptions/backup_normalize_descriptions_20260630-223339.json` — backup previo a aplicar (31 fichas).

### Hallazgos clave
- Las 171 ACTIVE ya están limpias en descripción/meta/imagen; las 40 que siguen en 80-119p son copy buena algo corta, **sin defecto** → no requieren reescritura artificial.
- El bug de ligadura `ﬁ` es típico de copy migrada desde PDF: conviene revisarlo en futuras importaciones de catálogo (reutilizable para otras tiendas).

### Siguiente paso recomendado
- Descripciones ACTIVE quedan en estado OK. Pendientes abiertos (no de descripción): borrado del residuo dedup (9 mesas DRAFT duplicadas, requiere OK) y carga de GTIN/barcode (100% ACTIVE sin código).
- Mantener el plan: esperar recrawl y repetir GSC delta ~6-9 jul.

---

## 2026-06-30 · Auditoría de descripciones de TODO el catálogo + fichas de parasoles DRAFT

**Paso del flujo:** GEO PDP / saneamiento de catálogo
**Estado:** ✅ aplicado
**Quién/qué:** Claude (Opus 4.8) + Shopify Admin GraphQL + verificación en vivo

### Qué se ejecutó
- Se sincronizó git (commit del trabajo GEO pendiente + rebase de un commit remoto de cierre `sync live=git` + push).
- Se ejecutó `scripts/audit_products.py` sobre **todo** el catálogo para verificar el estado real de las descripciones (no fiarse de la nota del batch 7).
- Resultado ACTIVE (171): **0 vacías, 0 pobres, 0 finas**; 130 ricas (≥120p) + 41 aceptables (80-119p); meta SEO, marca e imagen al 100%. → En lo publicado no hay nada sin describir.
- Resultado DRAFT (70): 10 vacías, 28 pobres, 12 finas, 18 aceptables, 2 ricas.
- Se clasificaron los 70 DRAFT: **modelos reales** (handle limpio) vs **artefactos** (handle con hash / `pendiente`).
- Auditoría cruzada: las **9 mesas `hpl-gd`/`extras`** (Capri, Brunei, Java, Etna, Altea, Ágata, mesa centro 110×60, Capri Doble) son **duplicados legacy** — cada una tiene su gemela ya ACTIVE publicada; llevan tags `legacy-balliu-consolidado-2026-05` + `pendiente-confirmar-proveedor` y **sin imagen**. → NO se describen (es residuo de deduplicación).
- Modelos reales pendientes de verdad = **4 parasoles** sin equivalente activo: `parasol-cuadrado-200x200` (Ágora), `parasol-para-terraza-300-cm` (Viena), `parasol-para-terraza-300-cm-2` (Caracas, económico) y `parasol-para-terraza-350-cm` (Samson).
- Se escribieron fichas ricas para esos 4 parasoles (47-55p → 188-211p) ancladas en datos reales (medida, estructura acero inox/fibra de vidrio del Ágora, resistencia UV/lluvia, montaje sin herramientas), con meta description. **Status DRAFT intacto** (no se publica nada; el merchant decide activar).

### Entregables
- `scripts/apply_pdp_rich_descriptions_batch9_parasoles.py` — script (dry-run por defecto, `--apply`, guard `productType==Parasol`).
- `content/descriptions/backup_pdp_rich_batch9_parasoles_20260630-081833.json` — backup previo a aplicar.
- `auditoria_fichas_report.csv` — auditoría completa actualizada.

### Hallazgos clave
- El sitio vivo (ACTIVE) está 100% cubierto en descripción/meta/imagen → el "esperar recrawl" sí está justificado para lo publicado.
- Los 70 DRAFT son mayoritariamente **residuo de la consolidación Balliu**: 53 con hash/pendiente (incluidas todas las mesas-gd) son duplicados de productos ya activos.
- 100% de los productos ACTIVE siguen **sin GTIN/barcode** en variantes → gap real para Google Merchant y comercio agéntico (no abordado aún).

### Decisiones pendientes
- **Borrado del residuo dedup:** las ~9 mesas `hpl-gd`/`extras` + `werzalit-60-etna` son duplicados; lo sano es borrarlas, pero es destructivo → requiere OK explícito.
- **GTIN:** decidir si cargar EANs (desde datos de proveedor/migración) en los 171 activos.
- Activar (o no) los 4 parasoles ahora que tienen ficha — decisión del merchant.

### Siguiente paso recomendado
- Mantener el plan: esperar recrawl 7-10 días y repetir GSC delta (~6-9 jul) para medir impacto de PDP 2.0 + enlazado interno.
- En paralelo, sin depender del recrawl: valorar el bloque GTIN o el hub de tumbonas Balliu/resina.

---

## 2026-06-28 · CIERRE DE SESIÓN — PDP (descripción/ficha) + Hero (velo, carrusel) + sync

Resumen de la sesión (detalle en las entradas siguientes):

- **PDP:** la descripción SEO sale de la columna de compra a una sección a ancho completo (`santavila-pdp-description.liquid`) con **ficha técnica** extraída de la propia descripción (adaptativa por tipo de producto). Ajustes posteriores: ficha `dt/dd` con negritas consistentes, narrativa justificada, compostura de columnas, botón "Añadir al carrito" sólido (verde marca), "Guía de medidas" retirada.
- **Hero:** (1) **velo configurable** (color/opacidad/refuerzo) para legibilidad sobre la imagen; (2) **altura** fija escritorio/móvil, **color de texto** y **caja/fondo** opcional; (3) **carrusel v1** (slides como bloques + snippet `santavila-hero-slide`, navegación, auto-rotación, swipe, accesible) con fallback legacy que **no rompe la home**; (4) **3 diapositivas de ejemplo ocultas** (`disabled`) dejadas en el live para activar con un clic.
- **Sincronización:** cerrada la divergencia `index.json` / `footer-group.json` / `cart.json` / `settings_data.json` (trabajo del home del compañero, que vivía solo en el live) → **git == live** para todo el theme.

**Estado:** todo en producción y documentado. `main` = `origin/main`. ~14 commits en la sesión. Solo el theme tocado; el `index.json` se sincronizó con salvaguardas (sin cambiar estructura del home).

**Pendiente (opcional):** remates visuales a criterio del dueño (verde del botón PDP, justify en móvil, contraste del velo); activar el carrusel y afinar; **split screen** del hero (v1.1); **F5-07** (ficha desde metafields). **Coordinación:** avisar al compañero de hacer `git pull` antes de seguir con la home (su trabajo ya está en git).

---

## 2026-06-28 (tarde-5) · SINCRONIZACIÓN live→git completa (home del compañero)

Se bajaron a git los 4 ficheros que vivían solo en el live (trabajo del compañero en el editor + diapositivas ocultas del hero): `templates/index.json`, `sections/footer-group.json`, `templates/cart.json`, `config/settings_data.json`.
- Verificado: los 4 son **idénticos semánticamente** git==live (la diferencia de MD5 era la re-serialización JSON de Shopify, no contenido). Sin cambios de estructura en el home (mismas 12 secciones, mismo orden).
- **git == live restaurado** para todo el theme; la divergencia que arrastrábamos queda cerrada. Commit atribuido al trabajo del compañero. En `main` `b41bb16`.
- Notas menores: `config/markets.json` sigue solo-en-git (no lo exporta el Asset API); `.DS_Store` es basura local (conviene gitignorar).

---

## 2026-06-28 (tarde-4) · HERO — 3 diapositivas de ejemplo OCULTAS en el live

A petición del dueño, se dejaron **3 bloques `slide` con `disabled: true`** en `santavila_hero`, dentro del `templates/index.json` del **LIVE** (no en git: el `index.json` es territorio del compañero y ya estaba diverged).
- Los bloques `disabled` **no cuentan** en `section.blocks` → la home pública sigue en modo legacy (1 slide). Verificado en `santavila.com`: `is-carousel=0`, sin puntos ni navegación.
- En el editor aparecen como diapositivas **ocultas**; el dueño las muestra (clic en el ojo) para activar el carrusel. Usan la imagen actual (`tumbona_consumible`) de placeholder + textos de ejemplo distintos.
- El script de inserción llevó **salvaguardas** (aborta si cambiaría cualquier otra sección o el orden). Ninguna otra sección de la home fue tocada.
- **Aumenta la divergencia `index.json` live≠git** (ya existente por el trabajo del compañero). Pendiente de sincronizar de forma coordinada.

---

## 2026-06-28 (tarde-3) · HERO Fase 2 — carrusel/slideshow (v1)

El hero pasa de una imagen a **carrusel** de varias diapositivas, **sin romper la home**.
- **Slides = bloques** (imagen + eyebrow + título + subtítulo + 2 CTAs). Snippet nuevo `santavila-hero-slide.liquid` reutilizable (carrusel y legacy).
- **Compatibilidad:** sin bloques → slide **legacy** desde los settings de sección (idéntico a hoy). Con 2+ bloques se activan navegación y auto-rotación. **No toca `index.json`** del compañero; el live (sin bloques) se ve como hoy — verificado.
- **Funciones:** fundido o deslizar+fundir, puntos/flechas (posición configurable), auto-rotación (pausa en hover/foco y con `prefers-reduced-motion`), teclado ←/→ y **swipe** móvil. Accesible (`aria-live`, `aria-current`). JS vanilla, sin librerías.
- Velo, caja, altura, color, sello y "Descubre" siguen **globales**. 1ª imagen `eager`, resto `lazy`.
- **Sin split screen** (queda para v1.1).

**Verificación:** schema válido, PUT 200 (compila snippet + sección), subido a DEV y LIVE; **legacy verificado intacto** en `santavila.com` (1 slide, sin carrusel ni nav). Spec: `docs/superpowers/specs/2026-06-28-hero-carrusel-design.md`. En `main` `48ff4e7`.

**Para activarlo:** el dueño añade 2+ bloques "Diapositiva" desde el editor (Hero → Añadir bloque). El carrusel real se valida ahí (no se puede sin tocar `index.json`).

---

## 2026-06-28 (tarde-2) · HERO Fase 1 — altura, color de texto y caja de fondo

Sobre las funciones que pidió el dueño (referencias del tema Atlantica). **Fase 1** (additive, defaults neutros = no cambian el aspecto actual; solo añaden controles en el editor):
- **Altura** configurable: automática (del tema) o fija en px, independiente escritorio/móvil.
- **Color del texto** del hero configurable (default blanco; el eyebrow y subtítulo heredan).
- **Caja/fondo** opcional tras el texto: panel semitransparente (color, opacidad, esquinas, borde), **off por defecto** — alternativa al velo global. Usa `color_modify`.

Subido a DEV y LIVE (solo `santavila-hero.liquid`); verificado que el hero sigue intacto (caja off, texto blanco, foto presente). En `main` `28827bf`.

**Pendiente — Fase 2:** hero en **carrusel/slideshow** (varias diapositivas, navegación flechas/puntos, auto-rotación, split screen). Es un **rediseño estructural grande** (blocks de slide + JS + schema): tarea dedicada con su propio diseño y validación.

---

## 2026-06-28 (tarde) · HERO — velo configurable para legibilidad

El velo del hero de la home pasa de **gradiente fijo** (casi transparente en el centro → el texto sobre la foto no se leía) a **configurable** desde el editor: color, opacidad uniforme y refuerzo arriba/abajo.

- **Por qué:** el compañero había puesto una imagen al hero **solo en live** (`tumbona_consumible.jpg`, vía `index.json` que sigue live≠git). Con foto, el velo viejo (0.05 en el centro) no daba contraste y el texto no se leía.
- **Qué se hizo:** en `santavila-hero.liquid` (git==live para ese fichero) el `::after` ahora deriva de variables CSS calculadas con `color_modify` nativo. Settings nuevos (sección "Velo / legibilidad"): `overlay_color`, `overlay_opacity` (0-90 %), `overlay_gradient` (0-100 %). Defaults `#141610` / 40 % / 60 % → contraste suficiente **sin tocar `index.json`** (territorio del compañero, NO tocado).
- **Velo** = capa uniforme (`--sv-ov-base`) + refuerzo arriba (menú) y abajo (título/CTAs) (`--sv-ov-grad`).
- **Verificación:** schema JSON válido, PUT 200 (compila), subido a DEV y LIVE (solo el hero); render confirmado en `santavila.com` (variables del velo presentes sobre la imagen). En `main` `8eea6e8`.

---

## 2026-06-28 · PDP — descripción a ancho completo + ficha técnica

La descripción SEO deja de estar metida en la columna de compra (sitio equívoco) y baja a **ancho completo** con **ficha técnica** al lado. Patrón PDP premium: arriba compacto = comprar; debajo = contenido.

**Qué se hizo (rama `pdp-descripcion` → `main`):**
- **Nueva sección `santavila-pdp-description.liquid`** (ancho completo) entre la zona de compra y "Por qué Santavila". Parte `product.description` por `<h2>Detalles clave</h2>`: narrativa a la izquierda + **ficha** (`<dl>` Detalles clave) a la derecha. Fallback a texto completo si no hay marcador. **Sin datos inventados** (línea roja): la ficha = lo que ya dice la descripción. Adaptativa por tipo: sofá→Medidas/Estilo, mesa→Altura/Material, conjunto→Incluye/Consejo.
- Quitada la descripción de la columna de compra (`santavila-product.liquid`).
- Quitado el botón **"Guía de medidas"** (redundante: las medidas están en la ficha).
- **Botón "Añadir al carrito"**: fondo sólido `--sage-deep` + texto `--paper` en standby (ya no se pierde con el fondo); hover vira a `--sage` + sombra.
- Narrativa **justificada** (izquierda en móvil ≤749 para evitar ríos). **Compostura**: las dos columnas a la misma altura (`align-items: stretch` + ficha centrada).

**Sincronización previa (importante):** el bloque de descripción vivía **solo en el live** (no en git, +75 líneas; lo había añadido el compañero/editor). Se bajó a git (`beccd32`) antes de rediseñar, para restaurar `git==live` en la PDP. Quedan **4 ficheros del compañero por delante en live** (`templates/index.json`, `sections/footer-group.json`, `templates/cart.json`, `config/settings_data.json`) — **NO tocados**; pendiente de sincronizar con él.

**Verificación:** parseo validado en 3 tipos de producto; Shopify compila la sección (PUT 200, un 422 inicial por un filtro dentro de un `if` ya corregido); subido a DEV y a LIVE **solo los 3 assets de la PDP** (sin pisar el theme del compañero); render confirmado en producción (`santavila.com`).

**Entregables:** `theme/sections/santavila-pdp-description.liquid` (nueva), `theme/sections/santavila-product.liquid`, `theme/templates/product.json`, spec `docs/superpowers/specs/2026-06-28-pdp-descripcion-ficha-design.md`.

**Pendiente (handoff):** poblar metafields de medidas/material para migrar a ficha-tabla 100% estructurada → BACKLOG **F5-07**.

---

## 2026-06-24 · CIERRE DE FASE: todo a `main`, temas sincronizados, documentado

Cierre limpio para arrancar la siguiente fase (SEO) sin dudas:

- **Git:** todo el trabajo de la sesión está en **`main`** y **`redesign`** (ambas en el mismo commit `a121b88`) y **subido a GitHub** — `origin/main = origin/redesign = a121b88`. Remoto: `github.com/manusantana/santavila`.
- **Temas Shopify SINCRONIZADOS:** **DEV (`189114876228`) = LIVE (`189222715716`)**, **454/454 assets idénticos** (verificado por checksum MD5 del Asset API). El único que divergía (`templates/index.json`, por re-serialización) se igualó escribiendo el mismo contenido en ambos.
- **Seguridad (importante):** `.claude/settings.json` contenía **tokens de Shopify**; GitHub Push Protection bloqueó el primer push. **NO hubo fuga**: el commit que ya estaba en GitHub (`80abcb1`) no contenía el token, y el rango completo subido ahora (`80abcb1..a121b88`) escanea **0 tokens**. Se sacó del *tracking* y se **gitignoró** (`.claude/settings.json` + `.claude/settings.local.json`). **No hace falta rotar el token.** Regla operativa: nunca commitear `.claude/settings.json` ni `.envlocal`.
- **Repo limpio:** scratch (`/_*`, `*.log`, caches, dumps) gitignorado; masters 4K de imagen, `precios_santavila.py`, backups (`compare_at_backup.csv`) y listas de publicación commiteados.

**Estado para la siguiente fase (SEO):** todo al día y verificado. Pendiente con dueño claro: **F5-06** (honestidad de descripciones de catálogo, la absorbe la tarea SEO completa) — ver [`BACKLOG_SANTAVILA.md`](BACKLOG_SANTAVILA.md).

---

## 2026-06-23 · PDP INTEGRAL VERIFICADA (galería, imagen-ambiente, honestidad)

Pasada **integral y verificada al 100%** de la PDP (con auditoría adversarial independiente), tras feedback del dueño sobre errores cíclicos. Todo a live + verificado:

- **Galería:** rejilla `1.2fr 1fr`→`1fr 1fr` (imagen más pequeña) + miniaturas `flex:1 1 0` que **llenan el rail** (alineadas con la foto); en móvil quedan cuadradas fijas.
- **"Por qué Santavila":** la caja estaba **vacía** (era la imagen del highlights, no la Destacada). Ahora muestra **el AMBIENTE del propio producto** (`closest.product.images[1]`), con imagen de marca de lujo (`santavila_pdp_brand.jpg`, File verificado que SÍ sirve) como **fallback** para productos de 1 foto.
- **Honestidad (líneas rojas) — falsas eliminadas:**
  - Highlights: fuera "Asiento profundo, fundas lavables", "Cuerda náutica PE", "Modular", "Aluminio termolacado" (LEISA-específicas aplicadas a todos) → copy genérico honesto.
  - Confianza (`santavila-pdp-social`): default "cojines desenfundables" → "todo lo necesario para el montaje". Titular default "Razones reales para confiar" (prohibido por GUÍA) → "Compra con tranquilidad".
  - **Descripción de la tumbona** reescrita: material real (aluminio + textileno), reclinable, dimensiones; **fuera** "Resistente a rayos UV" y "no requiere almacenamiento en invierno" (absolutos no verificables).
- **Mejoras premium:** material declarado; "**Envío gratis a partir de 500 €**" en iconos de confianza; modal "Guía de medidas" deja de ser placeholder; sticky a un solo precio.
- **Honestidad global:** 0 frases prohibidas; métodos de pago dinámicos (`shop.enabled_payment_types`) = reales.

**⚠️ PENDIENTE GRANDE (línea roja, catálogo):** la **descripción tipo** de MUCHOS productos (importadas) repite "Resistente a rayos UV, lluvia y humedad" y "no requiere almacenamiento en invierno" — **afirmaciones no verificables**. Corregida solo la tumbona; **falta una pasada honesta a todas las descripciones del catálogo.**

> **HANDOFF (decisión del dueño, 2026-06-23):** viene una **herramienta/tarea SEO** que reescribirá **descripciones + URLs** de producto. **NO tocar descripciones por separado** (evitar trabajo doble); esa pasada SEO debe **limpiar también la honestidad**. Documentado como tarea [`BACKLOG_SANTAVILA.md` → **F5-06**](BACKLOG_SANTAVILA.md) + memoria `santavila_catalog_descriptions_honesty`.

---

## 2026-06-22 (noche) · PDP TOP: cross-sell relacionados + fix sticky

Revisión del dueño en móvil → dos arreglos en la PDP (todo a live):
- **Sticky cart duplicaba el precio:** el JS clonaba el bloque de precio de Dwell que, **sin compare-at**, escribe el importe dos veces. Fix en `santavila-product.liquid`: el clon ahora extrae **solo el primer importe** (regex `\d[\d.,]*\s*€`).
- **Quitada la "Destacada" (imagen genérica en blanco) de la PDP** y sustituida por un módulo premium de **cross-sell / relacionados** ([`sections/santavila-related.liquid`](../../theme/sections/santavila-related.liquid)): reutiliza el motor de Dwell (`product-recommendations.js` + objeto `recommendations`, `morphSection` async) pero con la **tarjeta Santavila** (`santavila-product-card`). Fallback robusto: si no hay recomendaciones → productos de la misma colección → catálogo (nunca sale vacía). Colocada **al final** de la ficha (producto → por qué → confianza → relacionados).
- Verificado en vivo (tumbona): muestra "Colchoneta exterior para tumbona" (complementario) + mini-tumbonas. La `santavila-featured` sigue en el home; solo se quitó de la PDP.

---

## 2026-06-22 (tarde-6) · NO-REBAJA + TRANSPORTE VALIDADO + DESTACADA GENERAL

Tres cosas a raíz de la revisión del dueño en móvil:

- **Rebajas (compare-at) eliminadas de TODO el catálogo:** 1.515 variantes en **130 productos** tenían `compareAtPrice` (lo ponía el sync `psy_compare` = price×1,10) → borradas (directiva "precios definitivos, sin rebaja"). **Ningún `price` ni `cost` tocado.** Backup reversible en `compare_at_backup.csv`. ⚠️ Si se re-ejecuta `sync_prices_to_shopify.py`, vuelven; para cerrarlo del todo habría que desactivar `psy_compare` (el dueño lo deja para más adelante).
- **Pricing re-auditado (en vivo, `precios_santavila.py --audit`):** **0 bajo coste · 0 infra/sobre vs Col G · 100% terminaciones ,95/,90/,00 · 0 ACTIVE sin coste.** Márgenes ACTIVE: mediana 35,1%, mín 19,4% (mesa centro 120). Verificado además que los 1.515 precios afectados por el borrado **no cambiaron** (0/1.515).
- **Regla del transporte VALIDADA (no rota):** vive en el Excel (Col K "Coste Envío" 50€ en 26 voluminosos) y en los **perfiles de envío de Shopify**: **gratis ≥500 €**, y por debajo el cliente paga por tamaño (XS 9,95 · M 29,95 · L 57,95 · Hevea 50). Como el cliente cubre el transporte por debajo de 500€ y por encima el pedido lo absorbe, **la ganancia final está protegida**. El borrado de compare-at no toca nada de esto.
- **Destacada GENERAL para todos los productos:** generada imagen de marca (terraza costera española al atardecer, olivo + mar, fotorreal, sin muebles/personas) → `santavila_destacada_general.jpg` (File). Puesta como **imagen por defecto** del `santavila_featured` en `product.json` (live + dev + local) + copy de marca ("Hecho en España" / "Pensado para vivirse fuera"). Verificado: sale en la tumbona y en todos; **LEISA mantiene su imagen propia** por metafield. Master: `images_generated/brand/`.
- Bug del sticky cart (3 precios) era el compare-at → resuelto al borrarlo (queda 1 precio).

---

## 2026-06-22 (tarde-5) · TODO A LIVE (Destacada + tumbona publicada)

Subido todo a la tienda pública (autorizado por el dueño):
- **Destacada al tema LIVE** (`189222715716`) de forma **quirúrgica** (no se pisó el live): sección `santavila-featured.liquid` (versión metafield-aware + guard) wholesale; `product.json` → insertada la Destacada tras `santavila_product` sobre la versión del live; `index.json` → solo cambiada la imagen del featured del home a la costera (dev/live divergían en otras cosas, no se tocaron). Verificado en público: PDP de LEISA y home muestran la Destacada costera; **el guard funciona en producción** (no aparece en productos sin metafield, p. ej. la tumbona).
- **Tumbona PUBLICADA** (DRAFT→ACTIVE): cumple la regla [[santavila_publish_requires_cost_and_photo]] — coste 101 € + precio 193,95 € (margen ~48%) + 5 fotos. URL pública `santavila.com/products/tumbona-de-exterior`. Reversible a DRAFT si se quiere.
- LEISA ya era ACTIVE → su galería costera ya era pública.

**Pendiente futuro:** reconciliar divergencia dev↔live de `index.json` (escapado/`min_height`) en algún momento; decidir producción en lote.

---

## 2026-06-22 (tarde-4) · TUMBONA (2º producto) + LÍNEA ROJA de texturas (§15)

Validado el sistema en una **tipología nueva**: Tumbona Hevea "Brescia" (DRAFT, era 1-foto), en **Verano Costero**.

- **Galería (5) aplicada a la ficha** (sigue DRAFT, falta coste para publicar): packshot estudio → ambiente piscina costera (mujer reclinada, **§13.bis pasado** con un solo cuerpo: hombros ≈0,85 del ancho de 53 cm, manos correctas) → **detalle de estructura/mecanismo reclinable** → ASMR agua+sombrero → ASMR toalla+gafas+libro. Eliminada la foto real antigua.
- **Dim. reales:** 53 ancho · 136 fondo · 105 alto cm (ancla §13.bis adaptada a tumbona).
- **NUEVA LÍNEA ROJA (rol §15):** en ASMR/detalle **prohibido inventar material/textura**. El primer macro de "tejido" **fabricó un tweed grueso** que no es el sling fino real → rechazado y regenerado como **detalle fiel** (estructura+mecanismo), anclado a la **foto real** y a escala moderada. QA = recorte lado a lado contra la foto real. Memoria [[higgsfield_image_flow]] actualizada.
- **Flujo Python a prueba de erratas** para subir media (staged+POST+create+delete+reorder sin copiar firmas a mano).

**Estado:** parar y revisar (decisión del dueño) antes de producir en lote.

---

## 2026-06-22 (tarde-3) · SISTEMA VISUAL POR TEMPORADAS (marco de marca)

Decidido con el dueño el **modelo visual de toda la tienda** (rol §14):
- **Dos capas:** *backbone de producto* (packshot + ASMR) **estable** todo el año; *capa de temporada* (1 ambiente por producto + home + heroes + Destacada + social) que **rota**.
- **Eje = temporada**; el **lugar es el tema rotativo** de cada temporada, no una etiqueta fija del producto; el **tipo de producto define la escena** (craft). Cohesión por temporada + diferenciación por tipo.
- **Guardarraíl PM:** pos-1 packshot NO cambia (Google/og:image); el cambio vive en pos-2 + editorial + acento estacional ligero en un ASMR. Cadencia: 2 temporadas/año.
- **Foso:** con el flujo IA (swap de fondo) podemos refrescar todo el catálogo cada temporada; RH/Kettal (foto real) no.
- **TEMPORADA ACTIVA = "Verano Costero" (Cantábrico/Levante):** todos los productos se producen ahora en ella → tienda cohesiva. Brief en §14.5. Memorias: [[santavila_visual_season_system]], [[santavila_scale_standard]].

**Siguiente:** escalar al 2º producto con este marco + el flujo validado.

---

## 2026-06-22 (tarde-2) · GALERÍA LEISA ASMR-FIRST RECONSTRUIDA Y EN VIVO

Aplicada la receta nueva (**1 producto + 1 ambiente + 3 ASMR**) a LEISA, generando con Higgsfield bajo §13.bis.

- **Ambiente costero (recompuesto):** generado con swap de fondo desde Madrid (hereda la composición que SÍ pasa) → costa cantábrica. 4K, QA-limpio (escala + composición + anatomía + lógica de bebida). Reemplaza a la Cantabria mal compuesta.
- **ASMR (3):** café (la 05 que gustó) + **macro de material** (tejido + estructura, mar en bokeh) + **té helado** con menta/almendras (sin alcohol). Sin personas/manos → inmunes a escala. Consumible rotado.
- **Galería EN VIVO (pública):** Hero → ambiente costero → ASMR café → ASMR material → ASMR té helado (todas READY, reordenadas). Eliminadas Cantabria vieja, Madrid y Toledo de la ficha.
- **Destacada (dev):** PDP de LEISA y home actualizadas al **ambiente costero** (File `leisa_destacada_costero.jpg`; metafield + image_picker).
- **Masters locales 4K:** `images_generated/leisa/` → `02_ambiente_costero_v2.jpg`, `06_asmr_material.jpg`, `07_asmr_te_helado.jpg`.

**Flujo validado (replicable):** swap de fondo desde una toma de composición correcta = camino seguro para el ÚNICO plano con cuerpo entero; ASMR sin personas para el resto. Créditos Higgsfield: ~saldo 89→~70.

---

## 2026-06-22 (tarde) · AUDITORÍA DE ESCALA + GIRO DE RECETA A "ASMR-FIRST"

El dueño detecta que en la galería LEISA las personas leen **más grandes en Cantabria que en Madrid** respecto al asiento (línea roja §13). Se **frena** todo (nada de 2º producto, nada a vivo) y se audita.

**Auditoría rigurosa (workflow `audit-escala-leisa`, 7 agentes):** medición por imagen + comparación **lado a lado** + verificación. Resultado contraintuitivo y **honesto**:
- **Escala MÉTRICA del cuerpo = correcta en ambas** (hombros 0,75–0,80 de cojín, factor ~1,0, estatura implícita ~173 cm en las dos). El cuerpo **no** es más grande en Cantabria.
- **La diferencia real es COMPOSICIÓN/OCUPACIÓN:** Cantabria mete **2 personas juntas** que **llenan el sofá** (0 cojines libres) + postura inclinada a cámara + plano abierto → leen "enormes". Madrid: 1 persona + **1 cojín vacío** + reclinada + plano cerrado → "holgado". Viola la regla **ya existente** §13.7-B ("deja sitio para otras dos"); el fallo fue de **enforcement**, no de la herramienta. El mueble y los cuerpos son **dimensionalmente fieles** (refuerza el "100% real").
- **Fix correcto:** no encoger personas → **separar figuras (cojín visible), enderezar espalda, plano más cerrado.**

**Estándar grabado:** [`ROL_FOTOGRAFO_SENIOR.md`](ROL_FOTOGRAFO_SENIOR.md) **§13.bis** — la **doble puerta** (escala métrica + composición/ocupación), anclas verificables (cojín 60 · sillón 76 · asiento 44 · respaldo 85 · taza 8 · libro 30 · copa 22 · mano 18), protocolo, umbrales y reglas de ocupación.

**Giro de estrategia (dueño):** menos ambientes, **mucho más ASMR/detalle** (como la 05 sensorial: "hay vida", escala anclada por objetos cotidianos → inmune al problema de cuerpo entero). **Nueva receta por producto:** 1 foto de producto + 1 ambiente/escena (con check de escala obligatorio) + **2–3 ASMR**. Cantabria revertida ya del home; pendiente reconstruir galería LEISA (drop Cantabria + 2 ASMR nuevos), a confirmar receta.

---

## 2026-06-22 · DESTACADA POR PRODUCTO + BARRIDO RESPONSIVE (tema)

Cerrados dos pendientes del hito anterior, sobre el **tema dev** (`189114876228`).

**Sección "Destacada" por producto** ([`sections/santavila-featured.liquid`](../../theme/sections/santavila-featured.liquid)): ahora es **metafield-aware** vía `closest.product`. Lee `santavila.featured_image` (file_reference) + `featured_tag/eyebrow/heading/body`, con `section.settings` como _fallback_. Detalles:
- **Resolución robusta de imagen:** `feat_src = feat_img.image | default: feat_img` → sirve para `MediaImage` (metafield) **y** para `image_picker` (home), sin romper ninguno.
- **Guard `if feat_src != blank`:** la sección solo renderiza si hay imagen → aparece **solo donde hay metafield**; en productos sin foto (y en el home sin imagen) queda **oculta** en vez de mostrar una caja vacía.
- **Colocación:** insertada en [`templates/product.json`](../../theme/templates/product.json) entre `santavila_product` y `santavila_pdp_highlights` ("Por qué Santavila"), imagen a la derecha, métricas/CTAs ocultas por ahora (hasta tener colecciones).
- **LEISA:** imagen **Madrid noble** subida como _File_ (`gid://shopify/MediaImage/70834392596804`, 4096²) + copy honesto (sin inventar materiales) fijado por `metafieldsSet`. **Verificado en preview dev**: render + `srcset` + orden + eyebrow/tag/body correctos.
- ⚠️ **Decisión pendiente del dueño:** el `santavila_featured` del **home** no tiene imagen → ahora queda oculto por el guard. Decidir si darle una imagen (p. ej. Cantabria) o dejarlo oculto.

**Barrido responsive (auditoría CSS estática, sin bugs nuevos):**
- Clase del bug "Hecho en España" (`position:absolute` que pierde su ancla en móvil): **no se repite**. Los 6 `position:static` en media queries son el fix intencionado o `sticky→static` seguros (sin hijos absolutos).
- `min-width:240px` del panel de filtros ya se anula en móvil; títulos `nowrap` se truncan con `ellipsis` (no desbordan); sin anchos fijos grandes.
- Todos los grids colapsan bien en teléfono (1 col o 2 col en tarjetas/escenarios/upsell); ninguno se queda en 3–4 columnas.

**Commit:** `bbe924f` (rama `redesign`). **Siguiente:** decidir Destacada del home + **escalar imágenes a un 2º producto** con escenarios rotados (confirmar SKU; consume créditos Higgsfield).

## 2026-06-23 · GEO Sprint 0 + quick wins en theme live

Se ejecuta el arranque GEO de Santavila y se aplican los quick wins previos al Sprint 1.

**GSC / baseline:** OAuth reautorizado con `.venv/bin/python scripts/google_auth.py`; `sc-domain:santavila.com` confirmado como `siteOwner`. `SEO-BASELINE.md` actualizado: 9 clics, 630 impresiones, CTR 1,43%, posición media 15,9 (ventana 2026-05-26 → 2026-06-22). Oportunidades resumidas en `GSC-OPPORTUNITIES-2026-06-23.md`.

**Theme:** subidos por Asset API a DEV `189114876228` y LIVE `189222715716`:
- `snippets/meta-tags.liquid` — fallback de meta description para home cuando Shopify no trae `page_description`.
- `sections/santavila-collection-hero.liquid` — H1/crumb/alt visual `Sofás de exterior` para la colección `sillones-de-exterior`.

**Admin Shopify:** colección `sillones-de-exterior` actualizada de `Sofas de exterior` a `Sofás de exterior` sin cambiar handle.

**Verificación pública:** home emite meta description nueva; colección de sofás emite H1 `Sofás de exterior`. Quedan 2 labels `Sofas de exterior` en navegación (menu drawer / menu list), que vienen del menú de Shopify Admin y no del theme local; pendiente corregir en navegación si se quiere limpieza total.

**Agentic endpoints:** `llms.txt`/`agents.md` confirmados como endpoints generados por Shopify (`LlmsTxtController` / `AgentsMdController`), no editables desde theme. Informe: `GEO-AGENTIC-ENDPOINTS-REPORT.md`.

**Siguiente paso recomendado:** Sprint 1 sobre URLs con señales GSC: pérgola 250x300, sofás por medida, banco con mesa incorporada, tumbonas resina/Balliu.

---

## 2026-06-19/21 · ROL FOTÓGRAFO + GALERÍA LEISA EN VIVO (Fase 0 de imagen)

Se valida el **proyecto de imagen de producto con Higgsfield**. Piloto: **LEISA** (conjunto 3 plazas antracita).

**Rol del fotógrafo (documento maestro §0–§13):** [`ROL_FOTOGRAFO_SENIOR.md`](ROL_FOTOGRAFO_SENIOR.md) — leyes (fidelidad absoluta), pilares con specs medibles, 5 tomas, QA, prompt-recipe; §8 hiperrealismo "foto no render" + escenas de toda España + emparejamiento por paleta; §9 ASMR (consumible+aperitivo rotados, no siempre alcohol); §10 avatares regionales VIVOS (no de espaldas) + anti-fallo anatómico (multi-candidato + QA 4K); tells de IA (lógica de props/placement, peso, escena vacía sin vapor); §11 roster ~20 localizaciones de España + rotación; §12 Master QA; **§13 Proporcionalidad (línea roja)** con anclas antropométricas. Runbook: [`FLUJO_IMAGEN_PRODUCTO.md`](FLUJO_IMAGEN_PRODUCTO.md) + [`SET_GALERIA_PREMIUM.md`](SET_GALERIA_PREMIUM.md).

**Mecánica Higgsfield (validada):** `media_import_url`(foto real) → `generate_image` (nano_banana, **prompt CORTO en modo edición**) **a 1k** (2k/4k directos salen en blanco) → `upscale_image` 4K → personas en 2 pasos. A Shopify: **JPG por staged upload** (PNG 4K >20MB los rechaza la ingesta).

**Galería LEISA EN VIVO** (5×4K, escenarios ROTADOS): hero estudio · Cantabria (pareja, café) · Madrid noble (vermut) · Toledo (en reposo) · sensorial. Archivo maestro local en `images_generated/leisa/`.

**Tema:** arreglado el label **"Hecho en España"** descolocado en móvil (PDP: `position: relative` en el media query) → dev + LIVE (Asset API, verificado). IDs: DEV `189114876228` / LIVE `189222715716` [[santavila_theme_ids]].

**Pendiente:** "Destacada" por producto (metafield + Madrid) · barrido responsive · escalar a 2º producto.

---

## 2026-06-18 · AUDITORÍA DE IMÁGENES (producto ↔ imagen) — fase de revisión

Arranca el proyecto de imágenes con una auditoría en profundidad en 3 capas: estado **live** vía Admin API + **cruce determinista** archivo↔producto + **inspección visual** de 161 imágenes por agentes que las vieron. Informe completo: [`AUDITORIA_IMAGENES.md`](AUDITORIA_IMAGENES.md).

**Hallazgos clave:**
- **Asociación resuelta:** de 409 imágenes locales, 352 ya subidas (match por nombre en CDN), 45 cutouts por handle, 6 Balliu por slug; solo **6 huérfanas**.
- **El hueco es Hevea:** **87 de 115** productos con **1 sola foto** (media 1,3). Balliu sobra-cubierto (media 8). Ningún producto ACTIVO vacío (los 12 sin foto son DRAFT).
- **Calidad (161 inspeccionadas):** 43% apta para catálogo; Hevea sólida (76% apta — su problema es cantidad, no calidad); Balliu a dos velocidades; **cutouts 100% baja-res** (≈500px, archivos de trabajo); lifestyle = R&D.
- **Problemas:** 45% del material ≤800px; ~25% no encaja limpio (sobre todo fotos de detalle mal colocadas y solapamiento sets 2↔3 plazas); 4 con logo de tercero (Balliu/GUESS); fondos mezclados (sin sistema visual único).

**Entregables (solo lectura):** `auditoria_imagenes.py`, `_estado_imagenes.json`, `auditoria_imagenes_report.csv` (fila/producto), `auditoria_imagenes_orphans.csv`, `_visual_imagenes.json`.

**Pendiente / siguiente paso:** planificar 5 frentes — (1) enriquecer Hevea, (2) subir resolución, (3) estandarizar sistema visual, (4) limpiar integridad/matching, (5) ambiente de marca (enlaza con HOME pendiente). Decisión de medios por definir: alta del proveedor vs. generación IA vs. foto real.

---

## 2026-06-18 · AUDITORÍA INTEGRAL DE PRECIOS + herramienta blindada (`precios_santavila.py`)

Revisión total de precios tras la consolidación de Balliu (flat→variantes), que rompió el mapeo precio/coste. Objetivo del dueño: 100% seguro de NO vender por debajo de coste, y dejarlo preparado para cualquier cambio futuro (subida/bajada).

**Diagnóstico (verificado por 4 vías independientes + workflow adversarial):**
- **0 variantes por debajo de coste. CERO pérdidas.** La "pérdida" inicial de base-parasol-25kg (51,95€) fue **falso positivo de mi propio matcher** (le pegó el coste de la base de 25kg=54,88 cuando en realidad es la base barata: Excel `...890a4cd4` 30kg coste 27,52 / psy_G 51,95 → margen 36%). La verificación lo cazó **antes** de aplicar un fix erróneo.
- **Trampa evitada:** aplicar Col G por handle a lo bruto habría regalado cientos de € (p.ej. tirar mesas ATLANTA/JAVA 200-260×100 de 1.670/2.019€ a 1.275/1.575€, porque el Excel solo tiene la talla pequeña de ese producto). **Solo se corrige donde la talla/SKU coincide EXACTO.**
- **Único infravalorado genuino:** ALTEA 70×70 (handle `balliu-mesa-exterior-aluminio-7070-cm-1b61e6b6`) a 421,95€ cuando Col G = 480,95€ (×10 variantes tela). Decisión pendiente: subir crea incoherencia con la 80×80 (422,95€, sin fila Excel).
- **5 SKU duplicados en >1 producto** (incl. set contemporáneo 349,9€ que comparte SKU 557-010884 con el set de 2 plazas 4.679€; y 557-010147 compartido entre un set y un sofá). Decisión pendiente (borrar/recolocar SKU = irreversible, no se toca sin OK).
- El "escalonado por color" (chasis blanco más barato que prestige) es **intencionado** — son precios reales del Excel, no errores.

**Hecho:**
- `precios_santavila.py` — herramienta autoritativa: `--audit` (informe + CSV `precios_auditoria.csv`), `--set-price`/`--set-cost`/`--backfill-costs`. **Guardia anti-pérdida fail-closed** (no escribe un precio cuyo neto quede < coste; si no conoce el coste, bloquea salvo `--allow-no-cost`), **aborta con SKU duplicado**, suelo de coste conservador (MAX), matcher de coste por SKU/talla/precio-en-handle/precio-en-familia. A correr **antes de cada publicación**.
- **Backfill de costes aplicado a Shopify:** de 278 → **1.334/1.678 variantes con coste real**. Permite ver margen en Admin y blinda la guardia en vivo.
- `dump_estado_precios.py` (volcado live → `_estado_tienda.json`) + `_excel_precios.json`.

**Aplicado (con OK del dueño):**
- **ALTEA 70×70 + 80×80 → 480,95€** (×20 variantes; coherente, margen ~35%). Verificado en vivo.
- **Dedup SKU:** set contemporáneo 349,90€ (SKU 557-010884) → **DRAFT** (despublicado; era riesgo de pérdida); set 3 plazas → SKU `557-010147-SET` (separado del sofá ACAPULCO-3); mesa centro A → SKU `557-1563-B` (separado de la `-2` canónica); **borradas** las 2 copias `-2` (BRUNA silla y mesa alta 60×60), corregidos los que se quedan a Excel (89,95€/coste 55,51 y 449,90€/coste 245,33).
- Auditoría de cierre (estado vivo): **0 bajo coste, 0 infra, 0 sobre, 1 SKU dup restante** (solo 557-010884, ya DRAFT).

**Política "sin coste → no se publica" + "sin foto → no se publica" (decisión del dueño 2026-06-18):**
- **Productos enteros sin coste → DRAFT.** Despublicados los que no tienen coste en ningún sitio (1 Balliu + santavila marca propia). 2 que sí tenían coste (varía por chasis blanco/prestige: tumbona NOA, silla BIMBA) se re-activaron con su coste.
- **Variantes/tallas añadidas sin coste:** de 126, **92 recuperables** (su precio casa con un coste único de Balliu en el Excel bajo otro handle — mesas 200-260×100 a 1.670/2.019€, resina, CAPRI Ø70/Ø90, parasol acrílico…) → costeadas y mantenidas. **34 sin coste en ningún sitio → borradas** (CAPRI Ø80, parasol Ocean 200cm, etc.). Salvaguarda: nunca borrar la última variante.
- **Premisa de FOTO (dueño, no negociable):** ningún producto/variante PUBLICADO sin foto. Auditado: **0 productos ACTIVE sin foto** (los 12 sin imagen están todos en DRAFT).

**VERIFICACIÓN DURA FINAL (contra coste VIVO de Shopify, no inferido) — 1.462 variantes ACTIVE:**
`sin coste vivo: 0 ✅ · precio neto < coste: 0 ✅ · productos ACTIVE sin foto: 0 ✅` → **todo lo PUBLICADO tiene coste, foto y margen positivo** (mínimo 19,4%, mediana 35%).
- ⚠️ Esta verificación destapó un hueco que las auditorías "resoluble" ocultaban: las **10 variantes ALTEA 80×80** estaban ACTIVE a 480,95€ **sin coste** (las subí con `--allow-no-cost`). Cero riesgo de pérdida (HPL 80×80 ≈ 258€; comparable balliu 0a3ee957 a 481,95€ cuesta 258,75€). Fijado **coste provisional 258,75€** (= la 80×80 comparable, margen 35%). **PENDIENTE: confirmar el coste real de la ALTEA 80×80 con Balliu.**

**Estado de cierre: 1.642 variantes totales · 1 SKU dup (set 349,90€ en DRAFT).**

**Pendiente (dueño):** `productos_pendientes_publicar.csv` = **17 productos en BORRADOR** (3 Balliu + 14 santavila marca propia) que necesitan **coste** (15) y/o **foto** (12) para poder publicarse. + aclarar el set 349,90€ (DRAFT). Ver memoria [[pricing_audit_santavila_2026_06]].

---

## 2026-06-16 · IMÁGENES → COVER en toda la tienda (revierte product-fit)

El dueño comparó con el tema publicado y rechazó el `contain`: las bandas blancas "quedan rarísimas". **Decisión: todas las imágenes RELLENAN su cuadro (`object-fit: cover`)**, como el live. Revierte la regla "product-fit/contain" del 2026-06-12. Memoria [[santavila_images_cover]] + `GUIA §4` actualizadas.

**Cambiado `contain`→`cover` (revisión integral):**
- `santavila-components.css`: tarjetas `.sv-pcard__media` (home/colección/upsell) + `.card-gallery` (búsqueda/404). Fondo de respaldo `--bone`.
- `santavila-cart.css`: `.cart-items__media` (quitado también el `padding:5px` que dejaba borde).
- `santavila-hotspots.css`: `.sv-stl__media` (lista shop-the-look).
- `santavila-product.liquid`: galería principal `.sv-gal__slide` + miniaturas `.sv-gal__thumb`.
- **Excepción mantenida en `contain`:** lightbox/zoom de la PDP (`.sv-lightbox__img`) → al ampliar se ve el producto entero.
- Subido a STAGING #189222715716 **y** dev #189114876228 (200 en ambos). Ambiente/editorial ya estaban en cover.

---

## 2026-06-16 · BÚSQUEDA + 404 vestidos + QA de lanzamiento

Cierra los puntos "Búsqueda + 404" de los siguientes pasos. Tema renombrado a **"Santavila Theme by Ubicuo Libres Pensadores"** (dev #189114876228, rol `development`).

### Búsqueda + 404
- **404 traducido a español + tono Santavila** (`404.json`): "No encontramos esta página" · "El enlace puede estar mal… tu próximo rincón de exterior te sigue esperando" · botón "Volver a la tienda" · lista "Quizá esto te inspire".
- **Tarjetas nativas de Dwell** (`.card-gallery`, usadas SOLO en búsqueda/404/predictive — no chocan con `.sv-pcard`) vestidas **product-fit** (producto sobre blanco, sin recortar) + título serif, en `santavila-components.css`. Coherencia sin tocar la fontanería de búsqueda.

### QA de lanzamiento (verificado por API)
- ✅ Tienda EUR · santavila.com · **idioma español** (principal/publicado).
- ✅ **Email de contacto = hola@santavila.com** (destino del formulario).
- ✅ 243 productos · 6 políticas legales con contenido · todos los assets del tema presentes.
- ⚠️ **Manual (no verificable por API):** pasarela de pago activa (Ajustes→Pagos), pedido de prueba completo, que el checkbox legal no bloquee compra legítima, mensaje de prueba del formulario de contacto, pasada visual en móvil real.
- ⏳ **Antes de publicar:** imágenes reales (home/colección) + decisión naming (#4) + duplicar el tema `development` a uno permanente para publicar.

---

## 2026-06-16 · ESTADO + SIGUIENTES PASOS (snapshot de cierre)

> Punto de control. Todo lo de abajo está en la rama `redesign` y subido a `origin`. Tema dev #189114876228 (NUNCA tocar el live #188231123268).

### ✅ Hecho y verificado
- **Páginas vestidas Santavila:** Home, Colección (hero/grid/FAQ), PDP (galería 1+miniaturas, swatches color, precio por variante, barra sticky), Carrito (rediseño integral: tipografía única, alineación, resumen sticky, aceptación legal, upsell, franja confianza), **Contacto a medida** (canales + form + proyectos), Header/announcement (slider, ñ), Footer (legal).
- **Auditoría móvil completa** (5 auditores) + fixes reales + pulido. Menú hamburguesa (tipografía + pie de marca). Hotspots móvil → navegan a la ficha.
- **Redondez global** restaurada: botones pill + inputs 10px (contacto y todo).
- **Moneda España/UE**: símbolo € a la derecha (ajuste global del dueño) + sin "EUR" duplicado.
- **Confianza visible (estrategia):** franja de 4 pilares tras el hero + CTA de asesoramiento en la PDP. Datos 100% honestos.
- **Memoria** actualizada: [[santavila_strategy_docs]] (PDF de estrategia/competencia — no buscar en web), [[pricing_currency_format_eu]], [[announcement_n_tilde_font]], etc.

### ⏭️ SIGUIENTES PASOS
1. **SIGUIENTE FASE (decisión del dueño) — Dato de producto:**
   - Renombrar ~243 productos con **sistema de marca** (quitar "estilo X"/adjetivos de proveedor, "Set"→"Conjunto", "de exterior" sistemático, medidas limpias). 2 estilos propuestos (descriptivo con medida / limpio). **Plan seguro:** preview completo de los 243 + backup de títulos originales + aplicar por lotes; handle/URL y `global.title_tag` (SEO) intactos.
   - Reescribir **descripciones** hacia consultivo/concreto (hoy son de proveedor, vendor=**Hevea**).
   - **Ocultar el vendor "Hevea"** si se muestra en algún sitio (una sola voz).
2. **Búsqueda + 404** (investigado, pendiente): la búsqueda usa la tarjeta de **Dwell**, no `santavila-product-card` → incoherente. Vestir resultados + estado "sin resultados" + 404 con estilo Santavila.
3. **Menú "compra por espacio" + Proyectos/Profesionales** (estrategia: vender por escenario + canal B2B).
4. **Contacto a fondo** (iteración futura) · **Revisión global QA** antes de producción.

### 🙋 Pendiente del DUEÑO (datos, no código)
- **Nº de WhatsApp** → activa el canal en Contacto y permite enlazarlo desde el CTA de asesoría de la PDP.
- **Plazos y garantía REALES por familia** (el PDF aspira a 3-5 años / 7-10 días; hoy solo mostramos garantía legal y "según disponibilidad").
- **Imágenes reales** (home + cabeceras de colección) — escenas españolas creíbles (ático/patio/balcón), no resort.
- Configurar **Productos complementarios** en Search & Discovery (para el "Completa el conjunto" real del carrito).

---

## 2026-06-15 · CONFIANZA visible (estrategia) — franja home + CTA de asesoría en PDP

Aplicando el PDF de estrategia ([[santavila_strategy_docs]]): "la confianza es ventaja visible, no pie de página" + "CTA principal + CTA secundario para asesoramiento". Datos 100% HONESTOS (sin teléfono, garantía legal, envío deslocalizado). Aditivo, no rompe nada.

### Franja de confianza en el HOME (nueva `santavila-trust.liquid`)
- 4 pilares de la estrategia, visibles JUSTO tras el hero (posición 1 del orden): **Envío a toda España · Fabricado en España · Garantía legal · Atención personalizada**. Iconos sage, título sans + sublínea honesta. Texto FIJO (evita que se cuele un claim falso). Responsive 4→2→1 col.
- Insertado en `index.json` order: hero → **trust** → manifesto.

### CTA secundario de asesoramiento en la PDP (`santavila-product.liquid`)
- Tras el botón de compra: bloque "¿Dudas sobre medidas, materiales o tu espacio? Te asesoramos personalmente, sin compromiso." → mailto con el producto en el asunto. Activa el pilar diferencial (asesoría humana) justo donde se decide la compra.
- La PDP YA tenía el bloque de confianza (entrega/montaje/atención/garantía) — se respeta, solo se añade el CTA.

### Pendiente del dueño (para completar la estrategia, son datos, no código)
- Plazos y **garantía reales por familia** (el PDF sugiere 3-5 años como ideal; hoy solo mostramos garantía legal).
- Nº de **WhatsApp** (para activar el canal en contacto y poder enlazarlo desde el CTA de asesoría).

---

## 2026-06-15 · CONTACTO a medida (nivel top, según estrategia) + memoria del PDF

El dueño recordó que YA tenemos el PDF de estrategia/competencia (`docs/Santavila como líder…pdf`). Guardado en memoria [[santavila_strategy_docs]] para no volver a buscar en web. Clave aplicada: tono **consultivo y cálido**, **asesoría humana = pilar de marca**.

### Nueva sección `santavila-contact.liquid` (reemplaza main-page + form genérico)
- **Mantiene el texto del dueño** intacto (`{{ page.content }}`) como intro centrada (serif + lead).
- **Canales**: Email (hola@santavila.com), WhatsApp (setting `whatsapp`; oculto si vacío), Chat en directo (Shopify Inbox). Tarjetas con icono, hover, honestas. SIN teléfono (no lo tenemos).
- **Canal de Proyectos/Profesionales** (el 20% B2B que la estrategia subraya): callout "¿Un proyecto o varias piezas?" → mailto con asunto.
- **Formulario real** `{% raw %}{% form 'contact' %}{% endraw %}` (Nombre, Email, Teléfono opcional, Mensaje) con inputs redondeados (radio 10), botón pill, feedback ok/err, enlace a privacidad.
- **Atajos de ayuda**: Envíos, Devoluciones, Condiciones, Privacidad.
- Móvil: canales primero (1 toque), luego formulario. `page.contact.json` → solo `santavila_contact`.
- Settings editables: eyebrow, email, whatsapp, chat on/off. **Pendiente dueño: rellenar nº WhatsApp.**

### Nota: 422 de Shopify por `default:""` en setting de texto → se quita el default (text settings no admiten default en blanco).

---

## 2026-06-15 · HOTSPOTS móvil — el quick-add se renderizaba roto → navegar a la ficha

El dueño confirmó que en móvil, al tocar un punto, abría "una cajita modal rota abajo".

**Causa:** en móvil `product-hotspot.js` llama a `#openQuickAddModal()` (quick-add nativo de Dwell). Ese modal en `≤749px` es `position:fixed; margin:auto 0 0 0` **sin `width`** → un `<dialog>` con ancho `fit-content` que queda como una cajita abajo-izquierda.

**Fix (fiable, no a ciegas):** en `product-hotspot.js`, `handleHotspotClick` en móvil/táctil ahora **navega a la ficha del producto** (`data-product-url` del bloque, con fallback a `productLink`) en vez de abrir el modal. Es determinista y la lista "Comprar el conjunto" de abajo cubre la compra del look completo. Desktop sigue con el popover.

---

## 2026-06-15 · MÓVIL 2ª ronda — menú hamburguesa, redondez global, hotspots

Tras probar en móvil el dueño reportó: menú hamburguesa con letras gigantes y "falta info"; campos/botón de contacto sin redondez; Shop the look no se ve.

### Menú hamburguesa (drawer)
- **Letras gigantes:** Dwell ponía el 1er nivel a `var(--menu-font-2xl--size)`. Override en `santavila-header.css`: sans, 18px/500 (parent 15px, child 14px), `text-transform:none`, alto de ítem ≈52px.
- **"Falta info":** añadido **pie de marca** en `header-drawer.liquid` (`.sv-drawer-foot`): Mi cuenta · Buscar · Contacto y ayuda + 3 valores (Fabricado en España · Fácil de montar · Atención personalizada). El menú es `main-menu` (mismas 7 categorías que escritorio); con la letra corregida se ven todas.

### Redondez de marca GLOBAL (ajustes de Dwell estaban a 0)
- `button_border_radius_primary` y `_secondary`: **0 → 100** (pill). Era el default de Dwell; alguien lo había puesto a 0. Ahora **todos** los botones del tema son pill nativamente (incluido el de contacto, 404, etc.), no solo los forzados por CSS.
- `inputs_border_radius`: **0 → 10** → todos los campos de texto (contacto, newsletter, búsqueda, descuento) con la redondez de marca.
- Resuelve el feedback del contacto ("campos y botón con la redondez de siempre") y da coherencia en toda la tienda.

### Shop the look (hotspots) en móvil
- El home SÍ tiene imagen (`bolonia-xl-1.jpg`) + 3 hotspots, pero en horizontal quedaba una franja fina con los puntos amontonados (y: 20/40/52). Fix en `santavila-hotspots.css`: en ≤749px la imagen pasa a **4/5 (vertical)**. La lista de productos de abajo (1 col + "Comprar el conjunto") es la vía de compra robusta en móvil.
- **PENDIENTE de verificar en móvil real:** que al tocar un punto se abra el **quick-add** (es JS nativo de Dwell, no comprobable por CSS). Si no abre, ajustar `product-hotspot.js`.

### Confirmado bien por el dueño en móvil
Home, contacto (salvo redondez, ya corregida), colecciones y producto se ven bien. Tráfico ~95% móvil → foco máximo aquí.

---

## 2026-06-15 · AUDITORÍA MÓVIL COMPLETA (≤749px) — 5 auditores en paralelo + fixes

**Estado:** ✅ Fixes reales + pulido aplicados (10 archivos, subidos 200 + verificados idénticos). Base sólida confirmada: sin desbordamientos masivos, heroes en `svh`, rejillas que colapsan.

**Método:** 5 subagentes auditaron en paralelo el código responsive (no visual; el preview anónimo sirve el live) de: Header/announcement · Home A (hero, manifesto, scenarios, featured, product-row) · Home B (materials, spain, editorial, services, newsletter, hotspots) · PDP · Colección+Footer+Upsell.

### Fallos REALES corregidos
- **Tarjeta de producto compartida** (`santavila-components.css`): `.sv-pcard__name` 23px fijo → 19px en ≤749px (descuadraba rejillas en home/colección/upsell). `.sv-pcard__foot` → `flex-wrap:wrap` y `.sv-pcard__ship` deja de ser `nowrap` (precio + envío se solapaban en 2-col a 375px). **Un fix arregla 3 zonas.**
- **Panel de filtros de colección** (`santavila-collection-grid.liquid`): `min-width:240px` + `position:absolute left:0` anclado al chip → **scroll horizontal** cuando el chip estaba a la derecha. Fix: en ≤749px el panel se ancla a la fila completa (`.sv-facets{position:relative}`, `.sv-facet{position:static}`, panel `left:0;right:0;min-width:0`).
- **Hero home** (`santavila-hero.liquid`): breakpoint 680→749px; padding-top y mínimo del título (54→40px) reducidos para no exceder `100svh`; flecha "Descubre" oculta en móvil (solapaba los CTAs).
- **Barra sticky PDP** (`santavila-product.liquid`): `padding-bottom: env(safe-area-inset-bottom)` (home-indicator iPhone); CTA más compacto a ≤560px; **swatches 32→40px** y pills de variante ~44px de área táctil en móvil.

### Pulido aplicado
- Footer: enlaces con `padding-block` (área táctil) + 1 columna en ≤480px.
- Editorial: colapso a 1 col 620→749px. · Services: 1 col en ≤480px. · `.sv-prow__head` (scenarios + product-row): `flex-wrap:wrap`. · Hero colección: padding-top mínimo 120→92px.

### Pendiente de verificar EN TU MÓVIL (no por código)
- **Hotspots / Shop the Look:** en ≤749px el popover se oculta y el toque debe abrir el **quick-add nativo** de Dwell. Si al tocar un punto no pasa nada en móvil real, hay que ajustar el JS. Único punto potencialmente bloqueante no verificable por CSS.
- Deuda menor (no rompe): token `--ann-h` huérfano; `santavila-product.css` apunta al PDP nativo (no a `.sv-pdp`, código muerto); announcement 10.5px y truncado por elipsis (ok para los 3 textos actuales).

---

## 2026-06-15 · CARRITO — afinado (alineación de fila, hueco del resumen, raya única) + MONEDA UE

**Estado:** ✅ Implementado lo del tema. ⏳ El símbolo € a la derecha depende de un ajuste **global** que cambia el dueño a mano.

### Afinado del carrito (2ª pasada sobre feedback con captura)
- **Fila desalineada (texto arriba, no centrado con la imagen):** la imagen ocupaba 2 filas del grid y el sobrante caía en la fila del error. → **Fix:** fila a **una sola línea** (`grid-template-areas: 'media details quantity price'`), miniatura **cuadrada 96px** product-fit, `align-items: center` → todo centrado vertical con la imagen.
- **Hueco enorme sobre el panel "SANTAVILA" (derecha):** `.cart-summary__inner` tenía `grid-row: 2 / -1` (empezaba en la fila 2 del subgrid → fila del título vacía). → **Fix:** se **aplana** toda la cadena `subgrid`/`--extend` de Dwell (`.cart-summary`, `--extend`, `__inner` a `display:block`/`flex`, `grid-row:auto`), resumen pegado arriba y sticky en `.cart-page__summary`.
- **Doble raya ("raya, espacio, raya") bajo el panel:** el panel tenía borde inferior y `.cart-actions` borde superior. → **Fix:** divisor **único** = borde inferior del panel; se quita `border-top` de `.cart-actions`.

### MONEDA — formato España/UE (afecta a TODA la tienda)
- **Problema:** mostraba `€9.418,00 EUR` (símbolo a la izquierda + "EUR"). Convención correcta: **`9.418,00 €`** (símbolo a la derecha; o palabra EUR sin símbolo, nunca ambos).
- **`money_format` es global y NO editable por API** (PUT /shop.json → **406**; sin mutación GraphQL). → El dueño lo cambia en **Ajustes → Datos de la tienda → Moneda → Editar formato**:
  - HTML sin divisa: `{{amount_with_comma_separator}}&nbsp;€`
  - HTML con divisa: `{{amount_with_comma_separator}}&nbsp;EUR`
- **Lado tema (hecho):** desactivado `currency_code_enabled_cart_items` y `cart_total` en `settings_data.json` (ya estaban los de product). Así el carrito no duplica "EUR"; en cuanto se ajuste el formato global mostrará `9.418,00 €`.
- Regla guardada en memoria [[pricing_currency_format_eu]] + `GUIA_DISENO §3b`.

---

## 2026-06-15 · CARRITO — rediseño integral del sistema (tipografía + alineación + resumen)

**Estado:** ✅ Implementado. El dueño señaló (con captura) "un desastre de tipografías, tamaños y alineaciones" en `/cart`. Se rehace el sistema, no más parches.

### Causas raíz diagnosticadas (en el markup de Dwell)
- **Precios con dos tipografías:** el precio **unitario** (bajo el título) hereda `cart-primary-typography` y el de **línea** (derecha) usa `cart-secondary-typography` → dos familias del tema. → **Fix:** TODOS los importes forzados a `var(--sans)` + `tabular-nums`.
- **Texto "flotando arriba" / imagen desalineada:** la fila (`.cart-items__table-row`) usa `align-items: start` con imagen de 7.5rem. → **Fix:** en la página, `align-items: center` + columnas `92px | 1fr | auto | auto` + divisores `1px var(--line)` y ritmo `24px`.
- **Hueco enorme sobre "Descuento" (derecha):** `.cart-page__summary` usaba `subgrid` + `align-self: stretch` (se estiraba). → **Fix:** `display:block` + `align-self:start` + `position:sticky; top:20px`. Resumen pegado arriba y que sigue al hacer scroll (escala con 1 o 200 líneas).
- **Tamaños sin criterio:** jerarquía fijada → título serif 18px · variantes sans 13px muted · precio línea 16px/600 · total 27px/700 tabular.

### Añadido
- **Panel de marca** al inicio del resumen (llena el hueco que pedía el dueño): eyebrow "Santavila" + lead serif + 3 valores **honestos** (Fabricado en España · Fácil de montar en casa, sin instaladores · Atención personalizada: email, WhatsApp y chat). Oculto en el drawer.
- Resumen como **tarjeta** (`--paper-2` + borde + `--radius-media`).

### Archivos
- `assets/santavila-cart.css` — reescrito entero (sistema unificado, 8 bloques).
- `snippets/cart-summary.liquid` — panel `.sv-cart-brand` antes de `.cart-totals`.
- Subidos vía Asset API (200) + verificado local↔remoto idéntico (md5).

---

## 2026-06-15 · CARRITO — franja de confianza + upsell "Completa el conjunto"

**Estado:** ✅ Implementado. Arranca con `related`; el "completa el conjunto" real necesita config del dueño.

### Franja de confianza (cart-summary)
Bajo los botones de pago: entrega "hasta 30 días según disponibilidad", "pago 100% seguro · garantía legal", "devolución por desistimiento legal". Honesto, reduce ansiedad antes de pagar.

### Upsell (nueva sección `santavila-cart-upsell`, en /cart)
- Reemplaza el `product-list` genérico (colección "all") por productos relacionados con el producto del carrito, con la **tarjeta santavila-product-card** (product-fit).
- **Iteración 1 (fetch dinámico, descartada 2026-06-15):** usaba el componente `product-recommendations` de Dwell (fetch a `/recommendations/products` + `morphSection`). **No mostraba nada para sets/bundles**: `related` venía vacío para el "Set jardín" y el fetch JS añadía fragilidad.
- **Iteración 2 (ACTUAL, server-side robusto):** la sección recorre `cart.items.first.product.collections`, toma la primera colección no-`frontpage` con >1 producto y renderiza hasta N tarjetas (excluyendo el propio). **Sin JS, sin API → siempre se ve.** Verificado: el "Set jardín" está en `sillones-de-exterior` (88 productos) → muestra 4 sofás.
- **Para el "Completa el conjunto" REAL** (cojines/mesa/parasol para un sofá, en vez de "más de lo mismo"): configurar **Productos complementarios** en la app **Search & Discovery** (gratis de Shopify). Convierte 3–5× en carrito (investigación). Pendiente del dueño.

---

## 2026-06-15 · LEGAL — aceptación de políticas + enlaces legales

**Estado:** ✅ Implementado. Pendiente confirmación visual del dueño.

### Contexto
Por RGPD + comercio electrónico (España): el cliente debe **aceptar** privacidad + condiciones de venta antes de comprar, y las políticas deben ser **accesibles**.

### Hecho
- **Las políticas YA existen con contenido** en Shopify (Aviso legal, Privacidad, Condiciones de venta, Devoluciones, Envío, Contacto) — no se redacta nada legal aquí.
- **Checkbox obligatorio en el carrito** (`cart-summary.liquid`, página /cart + drawer): "He leído y acepto la [política de privacidad] y las [condiciones de venta]" con enlaces reales. JS (`santavila-cart.js`) **deshabilita "Finalizar compra" y el pago acelerado hasta marcarlo**. Robusto al re-render AJAX (cart:update + MutationObserver, sin IDs duplicados).
- **Enlaces legales fijos en el footer** (`sv-ft__legal`): Aviso legal · Privacidad · Condiciones · Devoluciones · Envío → URLs `/policies/...` reales.

### Límite honesto (técnico/legal)
El checkbox del TEMA cubre el flujo normal (carrito → pagar). NO es infalible al 100%: un cliente que vaya directo a `/checkout` por URL podría saltárselo, porque el **checkout de Shopify no es editable sin Shopify Plus**. Para 100% blindado: Shopify Plus (checkout UI extensions) o app de consentimiento. Recomendable validar con asesoría legal.

---

## 2026-06-14 · CARRITO — revestido con estilo Santavila

**Estado:** ✅ Capa de estilo aplicada. Falta confirmación VISUAL del dueño + (opcional) mensajes de envío/confianza y upsell.

### Hallazgo
El **carrito y el cart drawer usaban el estilo de Dwell** (no había sección ni capa Santavila). Heredaban las fuentes/colores de marca (vía tokens globales) pero el **layout/botones específicos** eran de Dwell → incoherencia con el resto.

### Hecho
- Nueva capa **`assets/santavila-cart.css`** (cargada en theme.liquid) sobre las clases de Dwell:
  - **"Finalizar compra"** → pill de marca (fondo ink, hover sage-deep), `.shopify-payment-button` pill.
  - **Totales**: titular serif, importes sans **tabular**; nota de IVA en mono.
  - **Líneas**: títulos de producto serif, precios tabular, variantes en `--ink-3`.
  - **Imágenes del carrito** → **product-fit** (contain sobre blanco), coherente con PDP/tarjetas.
  - Descuentos y botones secundarios con redondeo/tipografía de marca.
- Solo estilo; la fontanería de Dwell (cantidades, AJAX, descuentos, checkout) intacta.

### Pendiente
- Confirmación visual del dueño (página /cart + abrir el drawer).
- Opcional (mejora): mensaje de **entrega honesto** ("hasta 30 días…") + **pago seguro** en el carrito, y **upsell "completa el conjunto"** (cross-sell, convierte 3–5× en carrito).

---

## 2026-06-14 · Revisión de la COLECCIÓN

**Estado:** ✅ Auditada. Estaba casi perfecta; solo se ajustó la banda de ayuda.

### Hallazgos
- **Grid** (`santavila-collection-grid`): EXCELENTE — filtros faceted (chips + contador + price range), "Limpiar", contador de productos, **Ordenar** (sort), grid product-fit (tarjeta compartida), **"Cargar más"** (paginación), estado vacío honesto ("No hay productos… Quitar filtros"). No tocar.
- **Hero** (`santavila-collection-hero`): MUY BIEN — imagen (s.image o `collection.image`), **migas de pan** (Inicio/Colecciones/Título, bueno SEO), título, e **intro de la descripción SEO** de la colección (corta antes del FAQ). No tocar.
- **FAQ** (`santavila-collection-faq`): bien diseñada — **extrae las preguntas de `collection.description`** (`<h3>P</h3><p>R</p>`) y **NO se muestra si la colección no tiene FAQ** (degradación elegante, cero claims inventados). No tocar.

### Corregido
- **Banda de ayuda** (`.sv-cband`): CTA **"Hablar con un experto"** (sobre-promete + caía a `#`) → **"Escríbenos"** con destino real **`mailto:hola@santavila.com`**; el CTA solo se muestra si tiene enlace. Texto ya honesto ("atención personalizada, sin compromiso").

### Pendiente del dueño (datos, no técnico)
- Imagen de cada **colección** (Shopify admin → la usa el hero). · Imagen opcional de la banda. · FAQ por colección (añadir `<h3>/<p>` en la descripción) si se quiere.

---

## 2026-06-14 · Auditoría y saneamiento del HOME

**Estado:** ✅ Estructura y honestidad saneadas (2 subagentes auditaron las 11 secciones). Pendiente: imágenes del dueño ([`IMAGENES_HOME_PENDIENTES.md`](IMAGENES_HOME_PENDIENTES.md)).

### Honestidad (corregido)
- **Materiales**: fuera "Teca **FSC**", "**Anticorrosión** real", "**Cero plástico**" (greenwashing sin respaldo); intro reescrito.
- **Profesionales (B2B)**: claims no confirmados (doc técnica, packs, volumen) + CTA a `#` → **sección quitada del home** (reactivable como /profesionales si hay oferta real).
- **Destacada**: placeholder "Colección Cala" + "muestras de tejido" (no confirmado) → reconfigurada a **Sofás de exterior** (88 productos, la categoría más fuerte) con copy honesto y CTA real.

### Bugs / CTAs
- **Newsletter**: el mensaje éxito/error estaba FUERA del `{% form %}` → nunca se mostraba. Movido dentro.
- **CTAs rotos a `#`**: hero CTA2, manifiesto, "ver toda la tienda" → `/collections/all`; **4 escenarios** enlazados a su colección (Áticos→Sofás, Balcón→Sillas, Jardín→Tumbonas, Comedores→Mesas).
- **Editorial**: mantenida (habrá blog); cabecera solo si hay destino + tarjetas no-clicables hasta que existan los artículos.

### Pendiente del dueño
Imágenes de ambiente (hero, 4 escenarios, destacada, materiales, editorial) — documentado. + nº WhatsApp + envío gratis (Excel).

---

## 2026-06-14 · Shop the Look — mejoras de conversión (investigación aplicada)

**Estado:** ✅ Implementadas las 2 de mayor impacto (tras investigar competidores — ver [`INVESTIGACION_SHOP_THE_LOOK.md`](INVESTIGACION_SHOP_THE_LOOK.md)).

### Qué se construyó (en `sections/product-hotspots.liquid` + `santavila-hotspots.css`)
1. **Lista de productos del look** bajo la imagen (numerada, reutiliza los mismos productos de los puntos): foto product-fit + nombre serif + precio real. Garantiza que el 100% vea/compre las piezas aunque no descubra los puntos (clave en móvil). Grid responsive (1 col en móvil).
2. **Botón "Comprar el conjunto completo"**: JS recoge los `selected_or_first_available_variant.id` de todos los productos disponibles del look y hace `POST /cart/add.js` con todos → redirige a /cart. Palanca de AOV (benchmarks +15–39%).

### Técnico
- Itera `section.blocks | where: 'type', '_hotspot-product'` para la lista y los IDs del bundle. Solo estilo/markup Santavila; la fontanería de hotspots de Dwell intacta.
- Validado (Liquid+JS+CSS+schema), Asset API 200, dev == disco.

### Pendiente (Tier 1/2 restante, si se quiere)
- Variantes en botones dentro del quick-add · precio tachado en popover · puntos numerados vinculados a la lista · página dedicada "Ambientes" por escenario · lazy-load/WebP.

---

## 2026-06-14 · Shop the Look (hotspots) — revestido + activado

**Estado:** ✅ Disponible en cualquier página + demo clonada en el home del dev.

### Qué se hizo (petición dueño)
- Revisada la función nativa de Dwell ya presente en el tema: `sections/product-hotspots.liquid`, `blocks/_hotspot-product.liquid`, `assets/product-hotspot.js`. Atributos documentados en [`GUIA_DISENO.md`](GUIA_DISENO.md) §8.
  - Sección: imagen de ambiente, ancho/alto, overlay, `hotspot_color`/`bullseye_color`, color_scheme, tipografía popover.
  - Bloque por punto: `product` + `x-position`/`y-position` (0–100 %). Popover con foto + precio real + quick-add. Desktop popover / móvil quick-add modal.
- **Revestimiento Santavila** `assets/santavila-hotspots.css` (cargado en theme.liquid): popover tarjeta papel + redondeo + sombra, título serif, precio sans tabular, punto con pulso sage. Solo estilo; fontanería intacta.
- **Clonado el del live** (`bolonia-xl-1.jpg` + 3 productos: sofá 3 plazas, set jardín, mesa de centro) al **home del dev** tras "Escenarios" (id `santavila_shop_the_look`).

### Cómo reutilizarlo
Añadir la sección "Shop the Look" en cualquier página desde el editor → elegir imagen de ambiente → añadir bloques de producto y colocar cada punto (x/y) sobre su producto.

### Verificación
Asset API 200 (css/theme.liquid/index.json); re-pull confirma sección + css en remoto.

---

## 2026-06-14 · Auditoría de coherencia (todas las páginas) + GUÍA DE DISEÑO

**Estado:** ✅ Auditoría hecha, claims corregidos y guía documentada ([`GUIA_DISENO.md`](GUIA_DISENO.md)).

### Qué se revisó (home, colección, contacto, PDP)
- **Honestidad:** NO hay reseñas/prensa/testimonios falsos en home ni colección (limpio). Corregido:
  - Home `santavila_services` s4: "**Teléfono** y WhatsApp" → "**Email, WhatsApp y chat**".
  - `santavila-spain` default: "en cada pieza indicamos la provincia de fabricación / proveedores verificados" → "Diseño y fabricación en España, con proveedores nacionales…". ⚠️ La **lista de 5 provincias** del home sigue: PENDIENTE confirmar con el dueño cuáles son reales.
  - `santavila-services` schema: etiqueta de icono "Asesoría" → "Atención".
- **Anchos:** coherentes — todas las secciones usan `.sv-container`; los `max-width` que hay son en `ch` (legibilidad de texto), no estrechan rejillas. (El de los sellos ya se quitó.)
- **Imágenes:** ambiente = `cover` (OK); **tarjetas de producto = `cover`** (recortan) → incoherente con el product-fit de la PDP. PENDIENTE de decisión del dueño aplicar `contain` a las tarjetas.

### Entregable
- **`GUIA_DISENO.md`**: estándares vivos (honestidad, tono, anchos, imágenes producto/ambiente, PDP, swatches, precio, tokens, animaciones, operativa). Referencia para no desviarse.

### Pendiente (dueño)
- Provincias reales de fabricación · aplicar contain a tarjetas de producto (sí/no) · nº WhatsApp · envío gratis (Excel).

---

## 2026-06-14 · PDP — alineación DEFINITIVA: contain + stretch

**Estado:** ✅ Aplicado y sincronizado.

### Clave que faltaba (feedback dueño)
La imagen debe ser **PRODUCT-FIT (no recortar por los lados)** Y estar alineada con la columna. El intento previo usó `object-fit: cover` (recorta/amplía → mesa gigante). La combinación correcta es **`contain` + `stretch`**:
- `align-items: stretch` + `.sv-pdp__gallery` flex + `.sv-gal` `flex:1` + stage/slide `height:100%` → el contenedor se iguala a la altura de la columna (alineación total).
- **`object-fit: contain`** → la foto se ve **completa, nunca recortada**.
- Fondo del visor `#fff` (las fotos de producto son sobre blanco → se funden).
- Quitado el hover-zoom (recortaba, contradecía el product-fit). Móvil: proporción natural.

### Efecto secundario conocido
Con columna muy alta + foto muy horizontal (ambiente), puede quedar banda blanca arriba/abajo. Aceptable (prioridad: no recortar). Si molesta, opciones: limitar altura o fondo por tipo de foto.

---

## 2026-06-14 · PDP — alineación foto↔columna + nota precio "lento al inicio"

**Estado:** ✅ Alineación aplicada y sincronizada. Precio lento = hidratación/preview (no es bug).

### Alineación (feedback dueño: la foto queda más corta que la columna de compra)
- `.sv-pdp__grid` → `align-items: stretch` + `1.3fr 1fr`; `.sv-pdp__gallery` flex column; `.sv-gal` `flex:1`; `.sv-gal__stage` y `.sv-gal__slide.is-active` a `height:100%` (object-fit cover) → la foto principal **se estira a la altura exacta de la columna de compra**. En móvil se resetea a aspect-ratio natural.
- Nota: en productos con columna muy corta la foto podría quedar baja; revisar si aparece algún caso.

### Precio "cacheado/lento las primeras veces" (diagnóstico)
- NO es un bug ni hay caché que limpiar. Causas: (1) **hidratación** de los web components (variant-picker / product-price cargan como módulos con prioridad baja; hasta que hidratan, los primeros clics solo marcan el radio); (2) el **preview** `?preview_theme_id` va al origen sin caché de CDN → cada Section Rendering tarda más que en producción.
- En el tema publicado será notablemente más fluido. Mejora opcional posible: actualización de precio client-side instantánea (sin esperar al fetch) — pendiente de decisión (añade complejidad).

---

## 2026-06-13 · PDP — VALIDACIÓN de precio por variante (crítico)

**Estado:** ✅ Validado (datos + mecanismo + E2E). Bug de la sticky bar corregido. Falta confirmación visual del dueño.

### Por qué (petición dueño)
"Asegúrate de que la variante tiene el precio correcto; no vender a precio incorrecto."

### Hallazgos
- **43 de 243 productos tienen precio VARIABLE por variante** (rangos grandes: una mesa 478,95 €→945 €; otra 1.575 €→2.019 €). El riesgo es real, no teórico.
- **Mecanismo Dwell (confirmado por código):** el variant-picker dispara `variant:update` (bubbles) → el bloque `product-price` lo escucha en su `.shopify-section` y reemplaza `[ref="priceContainer"]` buscando `product-price[data-block-id=…]` en el HTML re-fetcheado. En la PDP custom, price y variant-picker están en la **misma** `.shopify-section` con id de bloque consistente → **se actualiza correctamente**.
- **E2E (datos reales):** pedir `?variant=ID` devuelve el precio EXACTO de esa variante (478,95 / 945 / 181,95 / 315,95 — todos OK).

### Bug encontrado y corregido
- La **barra sticky** tenía el precio en Liquid (estático = primera variante) → en productos de precio variable habría mostrado un precio engañoso al cambiar de variante. **Fix:** JS escucha `variant:update` en la sección y clona el precio real del bloque principal a la sticky (también al cargar). 

### Verificación
Liquid + JSON + balance JS/CSS OK; Asset API 200; dev == disco.

### Pendiente
- Confirmación VISUAL del dueño en un producto de precio variable (cambiar tamaño y ver precio + sticky).

---

## 2026-06-12 · PDP — swatches de color LIMPIOS + ocultar "retiro"

**Estado:** ✅ Aplicado y sincronizado (dev == disco).

### Feedback dueño (captura): "muchos círculos queda feo / horrible" + "¿qué es el retiro?"
- **Color**: los círculos dentro de botones de texto quedaban recargados. **HALLAZGO técnico:** la Admin API NO permite asignar `swatch.color` por mutation (no existe el campo en `OptionValueUpdateInput` en 2024-10/2025-01/04/07; solo `linkedMetafieldValue`). Los swatches nativos se gestionan en **Configuración → Swatches** (global, admite **foto real de tela**) o vía metaobjects+linkedMetafield (complejo, por producto).
- **Solución entregada (tema):** swatches **LIMPIOS** = el botón ES el círculo de color (oculto texto y pill), nombre del color elegido junto al título (JS `.sv-sw-name`, event-delegation robusto a re-render) + tooltip `title`. Mapa de color por nombre (orientativo). Visualmente como la nativa.
- **"El retiro no está disponible"** = aviso de recogida en tienda (pickup) de Dwell. Oculto vía CSS (`pickup-availability-component`, `[class*="pickup-availability"]`) — Santavila es envío, no recogida.

### Límite / nota
- Mapa de color cubre los nombres de Balliu; un valor sin color cae a círculo `--bone` (productos solo-color OK; si hubiera tallas, revisar).
- **Fidelidad real de color** = Configuración → Swatches con las fotos/hex reales de las telas Balliu (global, 1 vez). Pendiente de las telas reales del dueño.

### Verificación
Liquid + JSON + balance JS/CSS OK; Asset API 200; re-pull diff = dev == disco.

---

## 2026-06-12 · PDP — feedback (captura): galería alineada + sellos humanos + color

**Estado:** ✅ Aplicado y sincronizado (dev == disco). Color = solución de tema (orientativa); fidelidad real pendiente.

### Feedback del dueño (con capturas) y solución
1. **Galería desalineada** (la foto principal más corta que la columna; las miniaturas sobresalían) → **rail de miniaturas en `position:absolute` con `top/bottom:0`**, igualado a la altura exacta de la foto principal; scroll interno si hay muchas (nunca sobresale). Móvil: rail horizontal debajo.
2. **Sellos "parecen muy IA"** → reducidos de **6 a 3** (Hecho en España · Garantía legal · Detrás hay personas) con **copy humano**, título "Compra con tranquilidad" sin eyebrow. Rejilla centrada (max-width 1040).
3. **Color en botones de texto** (no convertía; el dueño quiere swatches como Sklum) → Dwell solo pinta swatch si el valor tiene `swatch.color` (dato de Shopify, ausente). Solución inmediata: **mapa de color en el tema** (`:has(input[value="…"])` → círculo de color antes del nombre) + `variant_style: buttons`. Seguro: valor sin mapa → círculo 0px (no se ve).

### Honestidad / límites
- Los colores del mapa son **ORIENTATIVOS** (aproximados por nombre). Fidelidad 100% = imágenes/hex reales de las telas Balliu cargadas como **swatches nativos de Shopify** (Settings → Swatches) — pendiente, idealmente con las fichas reales de tela.
- El mapa cubre los nombres vistos (Balliu); otros productos con otros nombres degradan a texto sin romper.

### Verificación
Liquid + JSON válidos; subida Asset API (200×3); re-pull diff = dev idéntico a disco.

### Pendiente
- **Colores fieles** (telas reales) · importe envío gratis (Excel) · nº WhatsApp.

---

## 2026-06-12 · PDP — feedback dueño: galería 1-foto + recorte + pago informativo

**Estado:** ✅ Aplicado y sincronizado (dev == disco). Pendiente SOLO de colores (esperando captura del dueño).

### Feedback del dueño y decisiones
- **Galería interminable** (apilaba las 10 fotos en grid) → **visor de 1 foto principal grande + miniaturas que la cambian** (clic) + lightbox para ampliar + carga diferida. Se elimina el modelo grid/mosaico y el setting `gallery_columns`.
- **PDP demasiado larga/"interminable y fea"** → recortada a lo esencial: **producto → Por qué Santavila (highlights) → Confianza (sellos)**. Quitadas del template (siguen disponibles como presets reactivables): promise, emocional, servicios/usps (duplicaba sellos), acordeones, recomendaciones.
- **"Más opciones de pago" llevaba directo a comprar** → eliminado el bloque `accelerated-checkout` (dynamic checkout). En su lugar, **collapse informativo** "Métodos de pago aceptados" con los iconos reales (`payment_type_svg_tag`) + texto "pago 100% seguro". NOTA: esto también quita los botones tipo Shop Pay (suben conversión) — reactivar si el dueño los quiere.
- Producto de 1 foto: validado por el dueño (bien).

### Técnico
- Shopify exige que toda sección de `sections` esté en `order` (422 si no) → las secciones recortadas se ELIMINAN del template (no basta sacarlas del order).
- JS galería: miniatura → `setActive` (toggle `.is-active` en slide+thumb); se retira el IntersectionObserver de scroll. Lightbox intacto.
- Validado (Liquid+JSON), subido Asset API (200), re-pull diff = dev idéntico a disco.

### Pendiente
- **Colores** (esperando captura del dueño) · importe envío gratis · nº WhatsApp.

---

## 2026-06-12 · PDP nivel-10 — CIERRE (reveals + variant-picker + tipografía)

**Estado:** ✅ Terminado, validado y sincronizado (re-pull + diff = dev idéntico a disco). PDP nivel-10 cerrada.

### Qué se añadió (todo seguro y degradable)
- **Reveals al scroll (CSS PURO)** en `santavila-components.css`: `@keyframes sv-rise-in` + `animation-timeline: view()`, envuelto en `@supports (animation-timeline: view())` y `prefers-reduced-motion: no-preference`. Aplica a bloques de contenido (promise, highlights items/feats, emocional, sellos, acordeones, servicios). **Sin soporte o con reduced-motion → contenido visible normal; nunca depende de JS.**
- **Variant-picker**: dropdowns con tipografía de marca (`--sans`), radio 12px y altura 48px. Selectores defensivos (no rompen si la estructura difiere).
- **Tipografía fina**: `text-wrap: balance` en el H1 del producto.

### Verificación
Balance Liquid + schema JSON OK; llaves CSS balanceadas (44=44); subida Asset API (200×2); `diff -rq` dev vs disco = idéntico salvo triviales (markets.json, orden de claves index.json).

### Enlace de revisión (dueño, logueado en admin)
- Editor: `https://mueblesexterior.myshopify.com/admin/themes/189114876228/editor`
- PDP directa (10 fotos): `https://santavila.com/products/balliu-silla-exterior-con-brazos-aluminio-estilo-elegante-56-cm-eaf4a34a?preview_theme_id=189114876228`

### Pendiente (datos del negocio, no técnico)
- Importe envío gratis (Excel de costes) · nº de WhatsApp.

---

## 2026-06-12 · Auditoría nivel-10 PDP (2/2): estética + conversión

**Estado:** ✅ Aplicado, validado y sincronizado en dev (re-pull + diff = idéntico a disco). Revisión íntegra OK.

### Mejoras aplicadas (todas seguras: hover/spacing/jerarquía; sin JS frágil ni animaciones que oculten contenido)
- **Galería:**
  - Zoom suave al hover sobre la foto (scale 1.045, solo `hover:hover`).
  - Indicador "ampliar" (lupa) en la esquina de cada imagen ampliable (`:has()` + data-uri SVG; degrada sin romper si el navegador no soporta `:has`).
  - **Mosaico editorial**: la última foto impar ocupa el ancho completo en el stage 2-up (clase `sv-gal--grid`, solo desktop). `gallery_columns` ahora se castea a int (`| plus: 0`).
- **Columna de compra:**
  - Precio con `tabular-nums` (cifras alineadas).
  - CTA add-to-cart: sombra al hover + micro-scale en `:active`.
  - Barra sticky: sombra superior para despegarla del contenido.
- **Confianza (sellos):** elevación sutil al hover (borde sage + translateY).
- **Highlights:** hover-zoom en la imagen, coherente con galería y cards de home.

### Decisión consciente (no romper)
NO se añadieron animaciones de entrada por scroll que pongan el contenido en `opacity:0` dependiendo de JS (violaría "contenido visible sin JS" y es lo más propenso a romperse). Si se quiere ese nivel de "wow", la vía segura es scroll-driven CSS puro (`animation-timeline: view()`), que degrada a contenido visible — pendiente de decisión del dueño.

### Verificación
Balance Liquid + schema JSON OK en los 3 archivos; subida por Asset API (200); re-pull + `diff -rq` confirma dev == disco salvo trivialidades (markets.json, orden de claves en index.json).

### Pendiente
- Importe envío gratis (del Excel de costes) y nº de WhatsApp.
- Si el dueño lo quiere: reveals scroll-driven CSS-puras; pulido del variant-picker de Dwell.

---

## 2026-06-12 · Auditoría nivel-10 PDP (1/2): saneamiento de claims falsos

**Estado:** ✅ Aplicado y subido a dev (Asset API, 200). Pendiente: 2 datos del dueño (importe envío gratis, contactos) y mejoras estéticas (parte 2).

### Por qué (la prioridad real del nivel-10)
La PDP estaba llena de **afirmaciones inventadas** que chocan con la regla de no falsear nada y con riesgo legal (reseñas/prensa falsas = publicidad engañosa). Antes de pulir estética, había que sanear. Ver [[santavila_facts]].

### Decisiones del dueño (2026-06-12)
- **Atención:** email, **WhatsApp** y **chat (Shopify Inbox, se activará)**. NO teléfono.
- **Envío:** gratis **desde un importe** (umbral pendiente de confirmar). Mientras tanto, solo se afirma el plazo.
- **Reseñas:** sin reales aún → fuera nombres ficticios, estrellas y "Verificada". Prueba social genérica/honesta.
- **Prensa:** sustituir medios inventados por **sellos reales**.

### Qué se saneó
- **Cabecera PDP:** eliminado el rating de estrellas inventado (bloque `review` fuera de la cabecera y del `product.json`). Trust row: envío sin "lo gestionamos nosotros" (es deslocalizado), atención por "email, WhatsApp y chat".
- **Emocional:** eliminada la reseña ficticia (Marta G.); reconvertida a statement de marca a pantalla completa + texto de apoyo. 100% honesto.
- **Social → reescrita como "Confianza":** fuera prensa inventada (El País/AD/Elle Decor…), testimonios ficticios y UGC vacío. Ahora 6 **sellos reales** (Hecho en España, Pago seguro, Garantía legal, Devolución legal, Atención personalizada, Fácil de montar) + bloque "Qué incluye" sin nº de bultos inventado.
- **Servicios + Acordeones (`.liquid` y `product.json`):** envío "deslocalizado (proveedor logístico externo)", quitado "Envío gratis a península", "asesoría"→"atención personalizada", teléfono→email/WhatsApp/chat.

### Vía técnica
Subida **archivo por archivo vía Asset API** (no `--only`), con validación previa de balance Liquid + schema JSON. Lección [[shopify_push_path_trap]].

### Pendiente (para cerrar honestidad)
- **Importe del envío gratis** (umbral €) → para añadir el claim "envío gratis desde X".
- **Email de contacto + número/enlace de WhatsApp** → para enlazar la atención.
- Parte 2: mejoras estéticas/conversión nivel-10 (jerarquía, galería, microinteracciones).

---

## 2026-06-12 · 🚨 INCIDENCIA: PDP "sin producto" — 5 archivos nunca llegaron al tema dev

**Estado:** ✅ Resuelto. Causa raíz encontrada y archivos re-subidos vía Asset API (todos 200).

### Síntoma (dueño)
"Te has cargado el announcement y cuando entras en una página de producto no se ve el producto."

### Causa raíz (la importante)
El tema vive en **`theme/`**, no en la raíz del repo. Hice los `shopify theme push --only ...` **desde la raíz, sin `--path theme`**. El CLI avisó "doesn't seem like you're running this command in a theme directory", resolvió `sections/...` contra la raíz (no existen ahí), **subió 0 archivos y aun así imprimió "pushed successfully"**.
Consecuencia: el tema dev #189114876228 quedó **sin 5 archivos** (404 confirmado vía Asset API):
`sections/santavila-product.liquid`, `sections/header-announcements.liquid`, `sections/header-group.json`, `assets/santavila-header.css`, `assets/santavila-product.css`.
Como `templates/product.json` apunta a `santavila-product` y **el archivo de la sección no existía → la PDP se renderizaba vacía** ("no se ve el producto"). El announcement, igual.

### Diagnóstico ejecutado
- `shopify theme pull --path /tmp/devtheme` + `diff -rq` → reveló los archivos disk-only.
- Asset API `GET assets.json?asset[key]=...` → 404 en los 5; 200 en santavila-tokens.css (ese sí estaba).
- Confirmado que el preview anónimo (`?preview_theme_id=`) **siempre sirve el tema live**, no el dev → no sirve para verificar; hay que mirar vía Asset API / editor.

### Solución
- Subidos los 5 archivos vía **Asset API (PUT)**, leyendo de `theme/…` (determinista). Verificado 200 en los 5.
- Re-pull + `diff -rq`: remoto == disco salvo trivialidades (`config/markets.json` y orden de claves en `index.json` — sin efecto en render).
- Validado: Liquid de la PDP balanceado (if 14/14, for 3/3, case 1/1, unless 1/1) y schema JSON válido.

### Lección (memoria [[shopify_push_path_trap]])
`push`/`pull`/`dev` SIEMPRE con `--path theme`. Nunca fiarse del "success": verificar existencia real vía Asset API.

---

## 2026-06-12 · Fix galería 1-imagen + announcement SLIDER (ñ resuelta)

**Estado:** ✅ Aplicado y subido a dev theme #189114876228 (push token, theme dev parado).

### Qué se ejecutó (feedback dueño con captura)
- **Galería adaptativa por nº de fotos** (`product.media.size`): si el producto tiene **1 sola imagen** → `.sv-gal--single` (sin rail de miniaturas, 1 columna, slide cuadrado a ancho completo). Arregla la foto "partida en dos / a media anchura con hueco" que se veía en productos de 1 imagen. Con ≥2 fotos sigue el rail + columnas (`gallery_columns`).
- **Announcement convertido en SLIDER** de 3 mensajes que rotan (auto-play nativo de Dwell, `blocks.size > 1`, speed 4s):
  1. `FABRICADO EN ESPAÑA` → 2. `FÁCIL DE MONTAR EN CASA` → 3. `ATENCIÓN PERSONALIZADA` → vuelve a empezar.
- **Flechas chevron de Dwell ocultas** (`slideshow-arrows`/`.slideshow-control { display:none }`): rota solo, sin controles; slides a ancho completo y centrados.

### Cómo se resolvió la "ñ" (España sin ñ → "ESPANA")
- Causa raíz: el `text-transform: uppercase` sobre la fuente mono se comía la Ñ.
- Fix: el texto se escribe **ya en mayúsculas con Ñ explícita** (U+00D1) y el bloque va con **`case: none`** → no hay `text-transform`, el carácter Ñ se pasa tal cual a la fuente y se renderiza. Mantiene el look uppercase del README sin el bug.
- Bonus: cada mensaje es corto → entra en **una sola línea** (con `nowrap` + elipsis de respaldo). Resuelve el salto a 2 líneas.

### Decisión de copy
- Se simplificó "Atención personalizada para tu terraza" → **"ATENCIÓN PERSONALIZADA"** (el dueño dijo "con atención personalizada sobra"). Sin claims inventados — ver [[santavila_facts]].

### Pendiente
- Confirmación visual del dueño del slider + galería 1-imagen.

---

## 2026-06-12 · PDP nivel-10 — galería bespoke + sticky qty

**Estado:** ✅ Construida, schema-válida y en dev theme (push token + verificación API). Falta confirmación VISUAL del dueño (theme dev se atascó).

### Qué se ejecutó (feedback dueño: Zara Home/Sklum/Westwing)
- **Galería bespoke** (`product.media`): rail vertical de miniaturas (clic→scroll+activo), **stage 2 fotos por fila** (setting `gallery_columns`), vídeo soportado. Reemplaza la galería de Dwell (perdemos su auto-sync por variante; aceptado).
- **Lightbox full-screen** (prev/next, contador, teclado, clic-fuera) → arregla el zoom "fuera de contexto".
- **Sticky add-to-cart con stepper de cantidad**: setea la cantidad real del form de Dwell antes de proxy-clicar el add. Carrito intacto.

### Hallazgos / incidencias
- `range` de Shopify exige **≥3 valores** (min/max/step) → para 1–2 usar `select`.
- **theme dev se atasca con su fichero `.tmp` al guardar rápido** ("contains illegal characters" / 500). Solución: parar theme dev + `theme push` por token (estable). Confirmado en memoria [[shopify_two_auth_rails]].

### Pendiente
- Confirmación visual del dueño (re-activar theme dev OAuth o revisar shareable link).
- Specs metafields + reseñas (app) con su OK.

---

## 2026-06-12 · PDP nivel-10 — pulido UI (tags, guía medidas, sticky bar)

**Estado:** ✅ Pulido UI aplicado y verificado en render local.

### Qué se ejecutó
- **Tags de galería** honestos (Hecho en España, badge metafield, "Pocas unidades" si inventory<=6).
- **Guía de medidas (modal `<dialog>`)** con setting richtext `size_guide`; enlace bajo variantes; cierre botón/fuera/Esc.
- **Sticky add-to-cart bar** propio (thumb+nombre+precio+CTA) que **proxy-clica el add-to-cart real de Dwell** (al perder de vista la buy-box vía IntersectionObserver). Carrito intacto.

### Pendiente (con tu OK / apps)
- Specs estructuradas → metafields `santavila.*` (toca productos).
- Reseñas reales → app (Judge.me).
- Galería rail+stage 100% fiel (miniatura vídeo, contador) — opcional.

---

## 2026-06-12 · PDP nivel-10 — sección de producto bespoke (validada)

**Estado:** 🔄 Foundation validada (carrito vivo). Sigue el pulido de conversión.
**Decisión dueño:** buy-box bespoke máximo techo. Referencias: Sklum, Zara Home, Westwing (Westwing analizado vía WebFetch; los otros 403 bot).

### Hallazgo clave (desbloquea todo)
- Una **sección propia** puede reusar los bloques reales de Dwell con `{%- content_for 'block', type: 'X', id: 'Y', closest.product: closest.product -%}` (galería, review, price, variant-picker, buy-buttons). → maquetado 100% propio + carrito/variantes/Shop Pay intactos. Los ids del content_for deben existir como bloques en product.json. Verificado: HTTP 200, carrito vivo.

### Qué se ejecutó
- `sections/santavila-product.liquid`: columna de compra bespoke (rating, H1 serif, USP metafield, precio grande+IVA, escasez real por inventory, trust row honesto, iconos de pago reales) + bloques Dwell por content_for. product.json: `main` → `santavila_product`.

### Síntesis de conversión (referencias)
- Above-the-fold que vende: precio prominente, swatches visibles, escasez real, plazo claro, add-to-cart enorme, trust + iconos de pago, atención personalizada. Specs estructuradas (metafields, pendiente). Prueba social (reseñas/app, pendiente).

### Siguiente (pulido nivel-10)
- Galería rail+stage fiel (tags, zoom, contador) · specs estructuradas (metafields `santavila.*`) · reseñas reales (app) · micro-UX · guía de medidas modal · sticky bar afinado.

---

## 2026-06-12 · Limpieza de claims falsos + espaciado (feedback dueño)

**Estado:** ✅ Corregido y verificado en render local.

### Qué se ejecutó
- **CRÍTICO — claims inventados eliminados de TODO el tema** (announcement, home services, PDP buy column + USPs + acordeones, featured, collection band): "enviado en 24h", "7–10 días", "30 días de prueba en casa", "SeQura / a plazos", "garantía 3/5 años", "asesoría humana".
- **Hechos reales (dueño 2026-06-12):** envío **deslocalizado** (un tercero lo gestiona), recepción **3–5 días** laborables península. Sin prueba 30 días. Sin financiación confirmada. Garantía → "garantía legal" (sin años inventados). "Asesoría humana" → **"Atención personalizada"**. Guardado en memoria `santavila_facts` como regla DURA.
- **Espaciado apretado:** `.sv-section` padding-block `clamp(64,10vw,150)` → `clamp(40,5vw,76)` (el dueño veía demasiado hueco en blanco entre secciones).

### Decisiones pendientes / a confirmar
- **Conflicto de plazo de envío:** el dueño dice 3–5 días; `Agents-IA/plan_santavila.md` decía "hasta 30 días según proveedor". Confirmar cuál es canónico.
- **Casing** (mayúsculas/minúsculas): el dueño nota mezcla; revisar con ejemplos concretos.

### Siguiente
- Pase nivel-10 de la PDP (referencia Sklum del dueño): conversión, cercanía a la venta, columna de compra bespoke.

---

## 2026-06-12 · Fase 8 — PDP completa (estructura + contenido)

**Estado:** ✅ Estructura completa y verificada en render local (HTTP 200, carrito intacto). Falta pase de calidad "nivel-10" (lo hará el dueño con referencias tipo Sklum).

### Qué se ejecutó
- Buy column: reordenada al README (rating→H1→precio→IVA/BNPL→variantes→add-to-cart→risk-remover) reusando bloques de Dwell + text blocks de valor.
- Secciones bespoke: `santavila-pdp-promise`, `-highlights` (3 beneficios + 3 características), `-emotional` (sage-900 + review), `-accordions` (medidas/envío/devoluciones/FAQ), `-social` (prensa + 3 testimonios + UGC + qué incluye). Company USPs reusando `santavila-services`. Related = product-recommendations de Dwell.

### Hallazgos clave
- **El `text` block de Dwell es richtext sanitizado**: elimina `class`, `<div>`, `<span>` y Liquid al inicio. → No sirve para chips/USP con clases. Pendiente nivel-10: columna de compra bespoke propia.
- **NO mezclar `theme dev` (OAuth) con `theme push` (token)** sobre el mismo dev theme: chocan y theme dev muestra "Failed to Upload" (500). Con theme dev activo, sincronizar SOLO guardando archivos (hot-reload).

### Siguiente
- **Pase nivel-10 de la PDP** (cercanía a la venta, conversión, referencias del dueño): columna de compra bespoke (USP, BNPL real, chips, guía de medidas modal, sticky bar afinado), galería rail+stage fiel, micro-UX.

---

## 2026-06-12 · Fase 8a (pase 1) — PDP restyle sobre Dwell

**Estado:** 🔄 En curso (primer pase aplicado y verificado en render local).
**Arquitectura (confirmada por el dueño):** reestilizar `product-information` de Dwell (galería + columna de compra con su carrito/variantes/Shop Pay/sticky-bar nativos) + bloques bespoke + galería/contenido a medida. NO hand-roll del form.

### Qué se ejecutó
- Reconocimiento: Dwell trae todo el core funcionando (gallery carousel+thumbnails, `product-details` sticky, `product-form-component`, add-to-cart, y **sticky-add-to-cart bar nativo**). Clases reales mapeadas.
- `assets/santavila-product.css`: H1 serif, precio prominente, add-to-cart pill ≥56px, swatches 44px, media redondeada (--radius-media), sticky bar en papel+blur.
- `product.json`: galería rail vertical + media_radius 14; título serif.

### Siguiente
- 8a (sig): bloques bespoke en la columna (USP 1 línea, línea BNPL SeQura, "IVA incluido · envío gratis", risk-remover "30 días", chips USP).
- 8b: promise + beneficios + características + emocional + review. 8c: acordeones (medidas/specs, envío, devoluciones, FAQ) + guía de medidas. 8d: social proof + related + sticky bar afinado.
- Recordatorio: sin montaje a domicilio.

---

## 2026-06-12 · Patrón de altura de hero (token --hero-h)

**Estado:** ✅ Aplicado y verificado en render local.

### Qué se ejecutó (feedback del dueño)
- Heroes con altura inconsistente (home 100svh, colección 56vh). Definido patrón común por **token**: `--hero-h: 100svh` (pantalla completa) y `--hero-h-secondary: 80svh` (casi completa, deja asomar el grid). `svh` = estable en móvil.
- Home usa `--hero-h`; colección usa `--hero-h-secondary`. Selector "Pantalla completa / Casi completa" por instancia. Decisión del dueño: home entera + colección casi entera.

### Siguiente
- Más revisión visual de la tienda con el dueño; luego Fase 8 (PDP).

---

## 2026-06-12 · Colección — fix hero + FAQ bespoke (full-width + JSON-LD)

**Estado:** ✅ Aplicado y verificado en render local (theme dev OAuth activo).

### Qué se ejecutó (feedback del dueño)
- **Hero volcaba toda la `collection.description`** (intro + `<h2>Preguntas frecuentes</h2>` + FAQ) → salía un "título pequeño" (h2) y la FAQ dentro del hero. Fix: el hero corta antes del primer `<h2>`, limpia HTML y trunca → solo la intro.
- **FAQ recuperada como sección bespoke** (`santavila-collection-faq.liquid`): parsea pares pregunta/respuesta de la descripción, acordeones on-brand a ancho completo (heading sticky izq + acordeones dcha), y emite **JSON-LD FAQPage** (SEO/GEO). Se oculta si no hay FAQ. collection.json: hero + grid + FAQ.

### Hallazgos / método
- **QA visual ahora vía inspección del render local** (`curl http://127.0.0.1:9292/...`) con theme dev (OAuth). Permite verificar estructura real (encabezados en hero, acordeones, JSON-LD) aunque no pixeles.
- Las capturas headless con Chrome NO funcionaron aquí; además un `pkill` amplio cerró el Chrome del dueño (error, registrado en memoria `no_broad_process_kill`).

### Siguiente
- Más revisión de colección con el dueño (vía su ojo + inspección local). Luego Fase 8 (PDP).

---

## 2026-06-12 · Revisión colección — UX de filtros + radio global + sin FAQ

**Estado:** ✅ Aplicado (`37a0324`). Pendiente verificación visual del dueño.
**Quién/qué:** revisión del dueño sobre la colección + Claude (Opus 4.8).

### Qué se ejecutó (feedback del dueño)
- **Filtros apelotonados → desplegables por faceta**: cada filtro (`Material ▾`, `Precio ▾`, `Disponibilidad ▾`…) abre un panel con checkboxes, contador por opción, contador de activos en el chip, "Limpiar" y caret animado. JS: cierra al abrir otro / clic fuera / Esc. Mucho mejor UX que los chips planos.
- **Radio de imagen global**: nuevo token `--radius-media: 14px` aplicado a TODAS las cards/media (pcard, escenarios, destacada, materiales, editorial, banda). Patrón de diseño consistente. Heroes full-bleed sin radio (a propósito). Footer payicon conserva 4px.
- **FAQ fuera de sitio** (estrecha, en Accesorios) → eliminada de `collection.json`. La colección queda hero + grid limpio.

### Hallazgos clave / honestidad
- **No puedo verificar visualmente el dev theme por curl** (el `preview_theme_id` exige sesión de admin; el muro de contraseña bloquea el render anónimo). Solo valido sintaxis/schema en `theme push`. Por eso se colaron detalles de UX (filtros apelotonados, FAQ) que el dueño sí vio. **Para QA visual: el dueño revisa o reactivamos `theme dev` (OAuth) en ciclos de iteración.**

### Prioridades vivas
- Verificación visual del dueño de la colección revisada.
- Metafields `santavila.*` + Search & Discovery → activan los filtros de marca (material, quick ship).

### Siguiente paso recomendado
- Cerrar la revisión de colección con el dueño; luego **Fase 8 — PDP**.

---

## 2026-06-12 · Rediseño tema — Fase 7 (plantilla de Colección)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Completada (`35975df`). Pendiente verificación visual del dueño.
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8). Decisión: bespoke + filtros nativos de Shopify.

### Qué se ejecutó
- **Card compartida (DRY):** `snippets/santavila-product-card.liquid` (home + colección). El CSS `.sv-pcard*` se movió a `santavila-components.css` (global, disponible en ambas plantillas). `santavila-product-row.liquid` ahora hace `render` del snippet.
- **`santavila-collection-hero.liquid`:** hero 56vh — breadcrumb mono (Inicio / Colecciones / título), H1 serif = `collection.title`, descripción (`collection.description` o override); imagen de colección o degradado sage; bajo el header transparente.
- **`santavila-collection-grid.liquid`:** filter bar **sticky** (top = `--header-height`) con chips desde `collection.filters` (faceted, Search & Discovery), popover de **precio** (min/max), **orden** nativo (`sort_by` preservando filtros) + contador; grid 3 col con la card Santavila; **banda editorial** intercalada (`grid-column:1/-1`, solo en página 1); **"Cargar más"** con mejora progresiva AJAX (append sin recarga; fallback a navegación si falla JS).
- **`collection.json`:** hero + grid Santavila + `collection-faq` (se conserva por su JSON-LD/SEO).

### Hallazgos clave
- Filtrado server-side Shopify-native vía `collection.filters` (URLs `url_to_add`/`url_to_remove`) + `paginate`. Robusto y SEO-friendly; el AJAX de "Cargar más" es solo mejora progresiva.
- Los chips de **marca** (material, Quick ship) sólo aparecerán cuando existan los **metafields `santavila.*` + configuración de Search & Discovery**. El grid los renderiza automáticamente en cuanto existan (ahora muestra los filtros nativos: disponibilidad, precio, opciones).

### Prioridades vivas
- Configurar Search & Discovery + metafields para los filtros de marca.
- Imágenes (hero de colección, banda editorial) — cliente.
- Verificación visual del dueño en una colección real.

### Siguiente paso recomendado
- **Fase 8**: Ficha de producto (PDP) — la "Perfect Product Page" del README (la más rica: galería, columna de compra sticky, acordeones, social proof, sticky add-to-cart). Recordar: **sin montaje a domicilio** ([[santavila_no_assembly]]).

---

## 2026-06-12 · Revisión home — modelo self-assembly + pulido

**Estado:** ✅ Correcciones aplicadas y pusheadas al dev theme.
**Quién/qué:** revisión del dueño sobre la home + Claude (Opus 4.8).

### Qué se ejecutó
- **CRÍTICO — modelo de negocio:** Santavila **NO ofrece montaje a domicilio** (self-assembly: el cliente lo monta en casa). Eliminado de todo el proyecto:
  - **Tema:** announcement ("Fabricado en España · **Fácil de montar en casa** · Asesoría humana…") y sección Servicios (col. montaje → "Fácil de montar en casa / llega en pocos bultos con instrucciones ilustradas; lo montas tú").
  - **Handoff:** `README.md` (nota de modelo destacada + línea Servicios + ejemplo metafield `assembly`) y los 3 prototipos (`Santavila Tienda/Coleccion/Producto.html`, este último con 2 referencias de envío).
  - `Agents-IA/*` ya estaba correcto ("no incluye montaje") — el error venía solo del handoff de diseño. Regla en memoria `santavila_no_assembly`.
- **Announcement a una sola línea**: eliminado el límite de 680px de Dwell; `nowrap` + elipsis en `santavila-header.css` (antes saltaba a 2 líneas).
- **Pulido de composición**: `text-wrap: pretty` en párrafos y `balance` en titulares de todas las secciones (`santavila-components.css`) → rag limpio, sin huérfanas ni "saltitos".

### Hallazgos clave
- El handoff de diseño **contradecía** el modelo de negocio ya documentado en el plan. Lección: validar copy del handoff contra `Agents-IA/plan_santavila.md`.

### Siguiente paso recomendado
- Verificación visual del dueño (announcement en una línea, alineación). Luego **Fase 7** (plantilla de Colección).

---

## 2026-06-12 · Rediseño tema — Fase 6 (cierre de la HOME)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Home 100% Santavila (`6a0aaec` + `381e53a`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8). Premisa: la mejor tienda de decoración exterior del mundo (Shopify-native, responsive, cero errores de maquetado).

### Qué se ejecutó
**6a — cuerpo de la home** (`6a0aaec`)
- `santavila-editorial.liquid`: revista 1 card grande + 2 pequeñas (bloques de artículo).
- `santavila-pro.liquid`: Profesionales, reutiliza el componente global `.sv-feat` (espejado) + botón sage.
- `santavila-services.liquid`: 4 columnas (icono por `select` + título + texto).
- `santavila-newsletter.liquid`: sage-900 + `{% form 'customer' %}` real con estados éxito/error.
- `index.json`: insertadas en orden README y **eliminadas las 7 secciones demo de Dwell** → la home renderiza solo las 11 secciones Santavila.

**6b — footer** (`381e53a`)
- `santavila-footer.liquid`: marca (logo del tema + eslogan + social en pills) · 3 columnas por `link_list` (menús reales colecciones/información/condiciones) · copyright + **iconos de pago reales** (`shop.enabled_payment_types | payment_type_svg_tag`).
- `footer-group.json`: reemplazado el footer de Dwell + email-signup redundante por la sección Santavila.

### Hallazgos clave
- `tag: null` no es válido en el schema de una sección (debe ser string u omitirse). En bloques sí se permite.
- Reutilizar clases CSS entre secciones funciona porque Dwell agrega todos los `{% stylesheet %}` en un único CSS global (Profesionales reusa `.sv-feat` del destacado).
- El footer de Dwell ya traía menús reales (colecciones, footer, información) → el footer bespoke los reaprovecha vía `link_list`.

### Prioridades vivas
- **Imágenes**: hero, escenarios, destacada, materiales, editorial — pendientes de foto del cliente (empty-states con fondo bone/sage cuidados).
- **Contenido**: nav del header y columnas del footer dependen de menús + colecciones por escenario; data model de metafields `santavila.*` para cards/PDP/filtros.

### Siguiente paso recomendado
- **Fase 7**: plantilla de **Colección** (`collection.json`): hero de colección, filter bar sticky (Search & Discovery), grid 3 col con banda editorial intercalada. Luego **Ficha de producto (PDP)** — la más compleja (Perfect Product Page).

---

## 2026-06-12 · Rediseño tema — Fase 5 (Materiales + Fabricado en España)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Completada (`fd6c452`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8). Premisa: "la mejor tienda online de home del mundo".

### Qué se ejecutó
- `sections/santavila-materials.liquid`: bloque oscuro sage-900 (scheme-5), media + lista de 4 materiales en bloques repetibles (swatch de color, nombre, descripción, tag mono) con hover de sangrado. Copy: cuerda náutica / aluminio termolacado / teca FSC / piedra y hormigón.
- `sections/santavila-spain.liquid`: banda bone centrada (scheme-4) con el arco SVG de marca (un único gesto), H2 serif, texto y provincias en chips mono pill (textarea, una por línea).
- `templates/index.json`: insertadas tras "Lo más deseado". Sincronizado con `theme push` (token).

### Hallazgos clave
- Las secciones con esquema no-default (dark/bone) deben fijar `background-color: var(--color-background)` y `color: var(--color-foreground)` en su wrapper: la clase `.color-scheme-N` define las CSS vars pero no pinta el fondo del elemento por sí sola.

### Prioridades vivas
- Imágenes reales (hero, escenarios, destacada, materiales) — foto del cliente.
- Data model de metafields `santavila.*` (alimenta cards, badges, plazos, filtros).

### Siguiente paso recomendado
- **Fase 6**: Editorial "El exterior bien vivido" (1 card grande + 2 pequeñas) + Profesionales (CTA sage) + Servicios (4 columnas) + Newsletter + Footer, cerrando la home. Después: plantillas de Colección y Ficha de producto (PDP).

---

## 2026-06-12 · Rediseño tema — Fase 4 ("Lo más deseado")

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Completada (`dbc2a22`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8).

### Qué se ejecutó
- `sections/santavila-product-row.liquid`: grid de product cards con **datos reales** (loop sobre colección). Card de marca: media 4/5 + hover zoom, badge opcional (`metafield santavila.badge`), categoría mono (`product.type`), nombre serif, precio `money_without_trailing_zeros` + compare_at tachado, plazo desde `santavila.lead_time_type/label` (Quick ship / Bajo pedido en arcilla), swatches desde `value.swatch.color`. Corazón de favoritos opcional (off; requiere app wishlist).
- `templates/index.json`: insertada tras la destacada, colección `frontpage` (8 productos), 4 columnas.
- Sincronizado al dev theme con `theme push` (token) — flujo de preview elegido por el dueño.

### Hallazgos clave
- La colección `frontpage` ("Home page") tiene 8 productos → el grid renderiza 4 reales.
- Catálogo sin metafields `santavila.*` todavía → badge/plazo/swatches degradan a vacío. Cuando se cree el data model (README) las cards se completan solas.

### Prioridades vivas
- Data model de producto (metafields `santavila.*`: material, lead_time, origin, warranty, scenario, product_usp, badge) — alimenta cards, PDP y filtros.
- Imágenes reales del hero/escenarios/destacada (foto cliente).

### Siguiente paso recomendado
- **Fase 5**: Materiales (bloque oscuro sage-900: media + 4 materiales con swatch) y/o "Fabricado en España" (banda bone con arco + provincias).

---

## 2026-06-12 · Rediseño tema — Fase 3 (banda editorial home)

**Paso del flujo:** Theme rebuild — rama `redesign`, dev theme #189114876228.
**Estado:** ✅ Fase 3 completada (`a0a8d16`).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8) · Shopify CLI 3.94.3.

### Qué se ejecutó
- `assets/santavila-components.css`: primitivas compartidas del design system (botones pill `sv-btn` + variantes, `sv-ulink`, `sv-eyebrow`, `sv-container`, `sv-section`). El hero se refactorizó para consumirlas.
- `sections/santavila-manifesto.liquid`: statement serif a 2 columnas (parte destacada + continuación atenuada) + párrafo + ulink.
- `sections/santavila-scenarios.liquid`: header + 4 cards de escenario (bloques repetibles: imagen, número mono, nombre serif con flecha en hover, enlace). Áticos y terrazas / Balcón / Jardín y porche / Comedores.
- `sections/santavila-featured.liquid`: Colección Cala (media 4/4.6 con tag, eyebrow, H2, 3 métricas: desde 779€ / 7-10 días / 5 años, CTAs).
- `templates/index.json`: las 3 secciones insertadas tras el hero.

### Entregables
- 3 secciones nuevas + `santavila-components.css` (todas bajo `theme/`).

### Hallazgos clave
- **Límite de 25 caracteres** en el `name` de un `{% schema %}` (y de presets/bloques). "Santavila Colección destacada" (29) rompía el build → renombrado a "Santavila Destacada".
- **La sesión OAuth de `shopify theme dev` caduca entre fases** ("CLI credentials are invalid") y corta la sincronización. Workaround robusto sin re-login: `shopify theme push --theme 189114876228 --nodelete` con `SHOPIFY_CLI_THEME_TOKEN` (el token `shpat_` SÍ vale para push/validación de schema). El push valida el schema antes de subir. Preview por navegador con el shareable link `?preview_theme_id=189114876228`.

### Prioridades vivas
- Imágenes reales (image_picker) de hero / escenarios / destacada: pendientes de foto del cliente (mientras, degradado/bone de marca).
- Enlaces de los 4 escenarios → dependen de crear las colecciones por escenario.

### Decisiones pendientes
- ¿Mantener `theme dev` (OAuth, hot-reload pero re-login cada sesión) o flujo `theme push` por token + shareable link (estable, sin hot-reload)?

### Siguiente paso recomendado
- **Fase 4**: "Lo más deseado" (grid de 4 product cards) o Materiales (bloque oscuro), siguiendo el orden del README.

---

## 2026-06-11 · Rediseño del tema (Dwell) — Fases 0–2

**Paso del flujo:** Theme rebuild — rama `redesign`, tema base **Dwell 3.5.1**.
**Estado:** 🔄 En curso (Fases 0, 1, 2 ✅; siguen 3+).
**Quién/qué:** sesión interactiva con dueño · Claude (Opus 4.8) · Shopify CLI 3.94.3.

### Qué se ejecutó

**Setup**
- `git pull` (merge limpio de 7 commits de origin, sin conflictos → `474da1d`).
- `shopify theme pull --live` del tema publicado a `theme/` (423 archivos). Baseline commiteado (`619c772`).
- Token de `.envlocal` regenerado a `shpat_…` (app nueva, client_id `1b30f2bd…`) con `read_themes`/`write_themes`. Sigue con read/write de products+files (scripts Python intactos). Desapareció `HF_TOKEN` del `.envlocal`.
- Dev theme de trabajo **#189114876228** (`shopify theme dev`). El live es **#188231123268** — NUNCA se le hace push.

**Fase 0 — Cimientos de tokens** (`6e9247e`)
- `assets/santavila-tokens.css`: paleta exacta de `store.css :root` + reasigna las 4 familias base de Dwell → Hanken (body) / Cormorant (heading+subheading) / JetBrains Mono (accent). Se propaga a presets, botones, carrito y búsqueda.
- `layout/theme.liquid`: Google Fonts (preconnect + display=swap) y carga de los CSS de marca tras `color-schemes`.
- `config/settings_data.json`: 7 color schemes remapeados a la paleta de marca (paper, sage, sage-900, bone, arcilla).

**Fase 1 — Announcement + Header** (`1266528`, `f061556`)
- Announcement: 3 mensajes `·` en un bloque (scheme-5 sage-900, JetBrains Mono uppercase, 11.5px / 0.14em).
- Header: layout logo-izq / nav-centro / iconos-dcha, sticky always, papel translúcido + blur 16px en sólido, nav en Hanken con subrayado en hover. Conserva cart/search/drawer de Dwell.

**Fase 2 — Hero + header transparente** (`0188013`)
- `sections/santavila-hero.liquid`: sección bespoke OS 2.0 (100svh, eyebrow + H1 "El exterior, bien vivido." con em, sello rotatorio textPath, 2 CTAs pill, indicador "Descubre"). Degradado sage si no hay foto.
- Header transparente encendido en home (logo blanco/nav sobre hero → sólido papel al scroll).

### Entregables
- `theme/assets/santavila-tokens.css`, `theme/assets/santavila-header.css`, `theme/sections/santavila-hero.liquid`.
- `theme/layout/theme.liquid`, `theme/config/settings_data.json`, `theme/sections/header-group.json`, `theme/templates/index.json` (modificados).

### Hallazgos clave
- Colores → por **settings de Dwell** (color schemes); fuentes → por **CSS** (no garantizadas en la librería de Shopify). Sobrescribir 4 vars de fuente viste toda la fontanería.
- `theme dev` local (127.0.0.1) **no** funciona con token Admin API por la contraseña de escaparate → se usa **login OAuth del CLI** + `--store-password`. Preview por navegador (preview_theme_id / editor) funciona siempre con sesión admin.
- La conmutación de logo blanco↔verde y el header transparente son **nativos** de Dwell (settings), no requieren JS propio.

### Prioridades vivas
- Verificación visual fina del hero bajo el header transparente (posición/offset) en navegador.
- Nav del header: los 7 labels del README (Colecciones, Áticos y terrazas, Balcón…) son **contenido** del menú `main-menu` en Admin → Navegación; dependen de que existan las colecciones por escenario.

### Decisiones pendientes
- Reponer `HF_TOKEN` en `.envlocal` si se usan los scripts de imágenes.
- Crear colecciones por escenario + reescribir menú `main-menu`.

### Siguiente paso recomendado
- **Fase 3**: Manifesto + Escenarios (4 cards) + Colección destacada, siguiendo el orden del README (`design_handoff_shopify_theme/README.md`).

---

## 2026-05-18 · Costes Shopify + sync Hevea completo

**Paso del flujo:** Pricing — costes unitarios y datos de proveedor sincronizados.
**Estado:** ✅ Completado.
**Quién:** sesión interactiva con dueño · scripts `set_unit_costs.py` + `sync_hevea_full.py`.

### Qué se hizo

**1. Costes BRUNEI + Capri fijados en Shopify** (`set_unit_costs.py --apply`):
- 89 variantes actualizadas con coste real por variante (fin de los falsos CRÍTICO del auditor).
- BRUNEI: 80×80=257.19€ · 130×80=342.68€ · 160×90=412.95€ · 190×90=506.65€
- Capri cuadrada: 70×70=203.29€ · 80×80=218.28€
- Técnica: `productVariantsBulkUpdate` con `inventoryItem.cost` (scope `write_products`, no necesita `write_inventory`).

**2. Sync completo Hevea CSV → Excel + Shopify** (`sync_hevea_full.py --apply`):
- Fuente de verdad: `proveedores_raw/hevea/20260507 ▶️CSV hevea 07_05_25.csv` (110 SKUs únicos).
- **Excel** (hoja `20260508 -Todos `): 47 filas actualizadas — carrier_cost corregido (regla: <500€ IVA → 50€, ≥500€ → 0€).
- **Shopify**: 106 productos actualizados — price (PSY), compareAtPrice, unitCost, descriptionHtml (descripción + tabla dimensiones).
- 3 SKUs duplicados en CSV omitidos para revisión manual: `557-010147`, `557-010884`, `557-1563`.
- Bug corregido en compareAtPrice: solo se activa cuando `pvp_iva > psy` (precio rebajado real). Segunda pasada eliminó ~100 compareAtPrice que eran menores que el price.

**3. ACAPULCO-3 corregido manualmente** (SKU `557-010147`, handle `sofa-terraza-3-plazas-estilo-moderno-18570-cm`):
- El sofá había sido subido a 819€ durante la auditoría basándose en un coste incorrecto (523€).
- Datos correctos del CSV: exworks=599€, pvp=950 sin IVA → pvp_iva=1149.50€ → PSY=1150€.
- Shopify: **819€ → 1150€**, coste **523€ → 599€**, compareAtPrice eliminado.
- Excel fila 86: handle corregido a `sofa-terraza-3-plazas-estilo-moderno-18570-cm`.
- Excel fila 90 (ACAPULCO-8 set, mismo SKU): datos restaurados (coste=1440€, pvp=2764.85€, psy=2765€).

### Pendiente · SKUs duplicados en CSV

| SKU | Producto A | Producto B |
|---|---|---|
| `557-010147` | ACAPULCO-3 sofá 3P (exworks=599) | ACAPULCO-8 set 3P (exworks=1440) |
| `557-010884` | LUNA-44 (handle desconocido) | BRANDON-7 set (handle a verificar) |
| `557-1563` | Mesa centro 120cm (×2 versiones) | — |

Hevea debe asignar SKUs únicos a estos productos. Mientras tanto los handles en Shopify/Excel son correctos pero el CSV no se puede usar como fuente de verdad para ellos.

### Entregables

- `set_unit_costs.py` — setea unitCost para cualquier handle/psy del Excel
- `sync_hevea_full.py` — sync completo CSV→Excel→Shopify para Hevea; reutilizable

---

## 2026-05-18 · Auditoría financiera completa + corrección precio sofá

**Paso del flujo:** Pricing — revisión de márgenes post-shipping.
**Estado:** ✅ Auditoría ejecutada. ✅ Corrección aplicada. ⏳ Costes pendientes de completar en Shopify.
**Quién:** sesión interactiva con dueño · script `audit_financiero.py`.

### Qué se hizo

Auditoría de 1.596 variantes / 177 productos ACTIVOS: márgenes netos con coste real de producto + comisión Shopify Payments (2.1%+0.30€) + coste de envío real según categoría XS/M/L.

**Resultado:**
- **CRÍTICO real: 0** — los 16 flags CRÍTICO eran falsos positivos (coste estimado por promedio de handle en Excel vs coste real por variante).
- **AVISO real: 1** → sofá 789€ con margen 17.2% (coste verificado en Shopify: 523€).
- **SIN_COSTE: 202 variantes** (7 handles) sin coste en Shopify ni en Excel — no auditables hasta completar datos.

**Corrección ejecutada:**
- `sofa-terraza-3-plazas-estilo-moderno-18570-cm`: precio **789€ → 819€** (compareAtPrice 850€ mantenido). Margen neto resultante: ~20.1%.

### Falsos positivos detectados — causa raíz

| Handle | Variantes | Coste estimado (avg) | Coste real (Excel) | Margen real |
|---|---|---|---|---|
| BRUNEI 80×80 (ef580ae2) | 15 var · 478.95€ | 411€ | 257€ | ~40% ✅ |
| BRUNEI 130×80 (ef580ae2) | 15 var · 639€ | 411€ | 343€ | ~32% ✅ |
| Capri Ø70 (724b0db0) | 15 var · 349.95€ | 273€ | ~203€ | ~37% ✅ |
| Capri 70×70 (724b0db0) | 15 var · 378.95€ | 273€ | ~203€ | ~33% ✅ |
| Base parasol 25kg (3ee8b72d) | 1 var · 51.95€ | 54.88€ (cruzado) | ~27€ | ~36% ✅ |

El auditor usa la media de costes del handle Excel cuando Shopify no tiene el coste individual. Para eliminar estos falsos positivos: **meter costes reales por variante en Shopify Admin → Productos → Variante → Coste por artículo**.

### SIN_COSTE — pendiente

| Handle | Variantes | Rango precio |
|---|---|---|
| Tumbona resina (b19af1ea) | 80 | 228–242€ |
| Parasol acrílico (236bd5f0) | 24 | 399€ |
| Parasol (82e48b2d) | 64 | 384€ |
| Parasol cuadrado 200×200 | 9 | 399–426€ |
| Tumbona Carmen tablillas | 5 | 199–219€ |
| Tumbona Lola tablillas | 5 | 199–212€ |
| Mesa Capri Doble 120×80 | 15 | 535€ |

### Entregables

- `audit_financiero.py` — script reutilizable para futuras auditorías
- `audit_financiero.csv` — 1.596 filas con margen neto por variante

---

## 2026-05-18 · Categorías de envío aplicadas + metafield definition creada

**Paso del flujo:** Shipping — categorización volumétrica XS/M/L.
**Estado:** ✅ Metafield + tags aplicados. ⏳ Tarifas en Admin pendientes (manual).
**Quién:** sesión interactiva con dueño · script `apply_shipping_categories.py`.

### Qué se hizo

1. **Metafield definition creada via API**: `santavila.envio_categoria` (single_line_text_field, choices: xs/m/l). Id: `gid://shopify/MetafieldDefinition/319933219140`.

2. **`apply_shipping_categories.py --apply`** — Clasifica los 225 handles únicos del Excel en XS/M/L y aplica metafield + tag `envio:xs|m|l`:
   - **72 actualizados · 149 sin cambios · 4 no encontrados** (DRAFTs eliminados).
   - Distribución final: XS=6 · M=87 · L=132.

3. **Bug corregido** en `categorize()`: sets de sofás y rinconeras con "mesa de centro" en el nombre se clasificaban como M → añadida regla prioritaria para "sofa"/"rinconera" → L. 6 sets corregidos.

### Reglas de clasificación aplicadas

| Categoría | Criterio |
|---|---|
| XS | cojín, funda, limpiador |
| M | silla/sillón individual, taburete, reposapiés, mesa auxiliar/centro/baja/lateral, mesa ≤80cm, accesorio resina, parasol <250cm |
| L | sofá, rinconera, tumbona, mesa grande, conjunto, parasol ≥250cm, default |

### Estado final — Tarifas configuradas en Shopify Admin

Perfiles creados y tarifas verificadas:

| Perfil | Productos | Tarifa España |
|---|---|---|
| Envío XS - Accesorios | 10 | 9,95€ plano + gratis >500€ |
| Envío M - Mediano | 70 | 29,95€ plano + gratis >500€ |
| Envío L - Voluminoso | 105 | 57,95€ plano + gratis >500€ |
| Perfil general (fallback) | todos los demás | 57,95€ (€0–€499) + gratis ≥€500 |

"Gestionar envío dividido" activado.

3 productos ACTIVE no estaban en el Excel (fuera del alcance del script) → etiquetados manualmente y pendientes de mover a perfil L/M:
- `set-jardin-contemporaneo-sofa-2-plazas-2-sillones-mesa` → L
- `sofa-terraza-3-plazas-estilo-moderno-18570-cm` → L
- `mesa-de-centro-exterior-120-cm-altura-40-cm` → M

---

## 2026-05-18 · Precios psicológicos aplicados a TODO el catálogo activo

**Paso del flujo:** Pricing — redondeo psicológico.
**Estado:** ✅ Aplicado en producción.
**Quién:** sesión interactiva con dueño · scripts `fill_psy_column.py` + `sync_all_psy_prices.py`.

### Qué se hizo

1. **`fill_psy_column.py --apply`** — Rellena col G "Precio Venta Psicológico (con IVA 21%)" en la hoja `20260508 -Todos ` de `Santavila.xlsx`. 281 filas procesadas con las reglas segmentadas por price bruto.

2. **`sync_all_psy_prices.py --apply`** — Aplica precios psicológicos a todos los productos con `status:active` de Shopify:
   - **177 productos · 1.479 variantes actualizadas · 0 errores.**
   - Fuente `excel_col_G` para los 263 SKUs con correspondencia única en el Excel (productos originales Balliu).
   - Fuente `psy(shopify)` para los ~1.216 SKUs `SV-*` (consolidados) y Hevea sin correspondencia única.
   - Delta agregado en catálogo: **−0,60%** (normal — umbral-trick baja precios justo por encima de 150/200/300/450 €).

### Reglas de redondeo aplicadas

| Segmento (price bruto) | Precio | CompareAt |
|---|---|---|
| < 50 € | termina en .95 | × 1.30, entero |
| 50–500 € | termina en .95; si en [umbral, umbral×1.05] → umbral − 0.10 | × 1.10, misma lógica |
| > 500 € | entero con terminación 0/5/9 (ceil) | × 1.10, múltiplo más limpio en [psy×1.05, psy×1.12] |

### Decisiones tomadas

- **Solo productos `status:active`**: los DRAFTs y pendientes-proveedor se excluyen automáticamente.
- **SKUs duplicados en Excel** (mismo handle+sku en múltiples filas): excluidos del mapping → se aplica `psy(shopify)` sobre el precio actual de Shopify. Afecta a 8 SKUs (principalmente conjuntos Hevea y un caso EVA PRO con dato incorrecto en fila 130).
- **Reporte**: `psy_prices_report.csv` con columnas `fuente/price_antes/price_despues/compare_antes/compare_despues/status`.

---

## 2026-05-17 · Repaso final — precios, nombres y limpieza legacy

**Paso del flujo:** Cierre y QA tras consolidar Familias 1, 2, 3 y 5.
**Estado:** ✅ Aplicado en producción.
**Quién:** sesión interactiva con dueño · scripts ad-hoc.

### Repaso de precios — 0 discrepancias

Cruce automático Excel pestaña `20260508 -Todos ` col F (PVP IVA) ↔ Shopify para los **1.444 variantes con SKU `SV-*`** (productos consolidados). Resultado:

- ✅ **512 variantes-base** matchean exactamente con Excel (±0,05 €).
- ✅ **931 variantes derivadas** (Chasis × Color, Tamaño × Color, etc.) comparten precio con la variante base.
- ✅ **0 discrepancias**. Catalogación totalmente sincronizada con el Excel maestro.

### Productos legacy adicionales pasados a DRAFT

Detectados durante el repaso (productos ACTIVE Balliu sin consolidar todavía):

- **Pasarelas resina B2B** (2 productos): no encaja con el perfil residencial. Tags: `producto-b2b`, `pendiente-confirmar-proveedor`, `legacy-balliu-consolidado-2026-05`.
- **Eva Pro tumbonas legacy** (3 productos): duplicados de la consolidación Familia 2 (`ddeeef3f`, `b19af1ea con 73-cm`, `32a6c0ea con 73-cm`).
- **Parasoles legacy sin modelo** (3 productos): `parasol-para-terraza-300-cm`, `-300-cm-2`, `-350-cm`.
- **Tumbona legacy sin modelo** (1 producto): `tumbona-de-exterior`.

**Total**: 9 productos legacy pasados a DRAFT.

### Refactor de nombres — Familias 1 y 2

Aplicada regla **"Opción C + sufijo Modelo"** (introducida en sub-piloto 3d) retroactivamente a Familias 1 Parasoles y 2 Tumbonas. Script: [`refactor_nombres_balliu_familias_1_2.py`](../../refactor_nombres_balliu_familias_1_2.py).

**26 productos renombrados.** Ejemplos:

| Antes | Después |
|---|---|
| Parasol cuadrado · aluminio 300×300 cm | **Parasol cuadrado exterior · aluminio 300×300 cm · Brisa** |
| Parasol exterior · 16 colores Ø200 cm | **Parasol exterior tela · Ø200 cm · Pamela tela** |
| Parasol exterior acrílico · mástil regulable Ø200 cm | **Parasol exterior acrílico · Ø200 cm · Pamela acrílico** |
| Tumbona resina · respaldo regulable Ø73 cm tablillas (Mario Eskenazi) | **Tumbona exterior resina · Ø73 cm tablillas · Eva Pro T** |
| Tumbona resina premium · respaldo regulable | **Tumbona exterior resina · Noa** |
| Mini tumbona aluminio plegable · 62 cm | **Mini tumbona exterior aluminio plegable · 62 cm · Cannes** |

**Limpiezas aplicadas:**
- Quitado `(Mario Eskenazi)` del título Eva Pro T (queda para descripción).
- Quitado `premium` de Noa.
- Quitado `16 colores` (no es atributo de producto) — cambiado a `tela` cuando aplica.
- Añadido `exterior` consistentemente.
- Pamela y Ocean diferenciados con sufijo `tela`/`acrílico` ya que el mismo modelo se vende en dos materiales.

### Ágora — verificada y completada

`parasol-cuadrado-200x200` (Ágora, 9 variantes ACTIVE) **no tenía tag `Balliu`** y por eso no aparecía en mis listados anteriores. Corregido: tags `Balliu`, `envio:l` añadidos.

### Backup

`backups/refactor_nombres_<timestamp>.json` con snapshot previo de todos los productos renombrados.

### Siguientes pasos

- **Hevea**: auditoría completa (115 SKUs en pestaña `Hevea`).
- **Familia 7 estimada**: Camas balinesas, Sofás Olimpia/Etna, Fundas protectoras, Cojines, Weguard (productos ACTIVE legacy sin consolidar que el dueño decidirá si consolidar).
- **Imágenes por variante** (todas las familias).

---

## 2026-05-17 · Familia 5 cerrada — Sillas Balliu (10 consolidados / 168 variantes + 5 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 5 (Sillas)
**Estado:** ✅ Aplicado en producción · 10 consolidados publicados en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_sillas.py`

### Qué se ejecutó

Inspección Excel + Shopify + web Balliu de 21 SKUs sillas/taburetes/sillones repartidos en 11 modelos. WebFetch a 12 modelos para confirmar matriz.

### Decisiones del dueño aplicadas

1. **Patrón Blanco/Prestige** para Bimba, Duna (3 colores: Blanco/Negro/Tórtola).
2. **Selva** solo 2 colores (Blanco/Arena), sin la nota "para más colores consultar".
3. **Venus** sin opción Color (solo Tórtola en web → regla UX N=1).
4. **Vera** consolidado con opciones [Configuración(3) × Color(2)] = 6 variantes.
5. **Bruna** consolidado con [Brazos(2) × Color(2)] = 4 variantes.
6. **Silla/Etna Alta/Taburete Etna**: Chasis(3) × Tejido Balliu(16) = 48 variantes c/u, precio único.
7. **Mila** con Chasis(2) × Tejido(2) = 4 variantes.
8. **Taburete Etna**: precio Excel (186,62€), no web (188,63€).
9. **Silla Greta** y **Bruna 197,73€ misteriosa** → DRAFT con tag `pendiente-confirmar-proveedor`.

### Resultado (10 ACTIVE + 5 DRAFT)

| # | ACTIVE | Variantes | Precio (€) |
|---|---|---|---|
| 1 | Silla exterior resina · estilo clásico · **Bimba** | 3 (Color B/N/T) | 102,03 / 103,56 |
| 2 | Silla exterior resina · estilo minimalista · **Duna** | 3 (Color B/N/T) | 77,39 / 81,76 |
| 3 | Silla exterior resina apilable · **Selva** | 2 (Color B/A) | 33,50 / 40,52 |
| 4 | Silla exterior resina · **Bruna** | 4 (Brazos × Color) | 70,81 / 84,19 |
| 5 | Silla exterior resina · **Vera** | 6 (Configuración × Color) | 77,97 / 79,76 / 115,08 |
| 6 | Silla exterior resina · **Venus** | 2 (Brazos) | 65,42 / 70,71 |
| 7 | Silla exterior aluminio · tejido Balliu · **Etna** | **48** (Chasis × Tejido 16) | 181,89 |
| 8 | Silla exterior aluminio alta · tejido Balliu · **Etna Alta** | **48** | 190,20 |
| 9 | Taburete exterior aluminio · tejido Balliu · **Etna** | **48** | 186,62 |
| 10 | Silla exterior aluminio · tejido Balliu · **Mila** | 4 (Chasis 2 × Tejido 2) | 97,88 |

**Total ACTIVE: 10 productos · 168 variantes.**

**DRAFT (5):**
- 4 existentes: Venus con brazos (consolidado), Silla Greta (no en web), 2 duplicados Bruna misteriosos.
- 1 nuevo: `silla-exterior-resina-bruna-precio-alto-pendiente` (197,73€) — `pendiente-confirmar-proveedor`.

### Hallazgo Bruna misteriosa

El SKU `BALLIU_BRUNA_SILLA_CON_BRAZ_94B6E5B5` aparece dos veces en Excel con precios muy distintos (89,55€ y 197,73€) y dos productos planos en Shopify con el mismo SKU (113,80€ y 89,95€). La web del proveedor solo tiene Bruna sin/con brazos a 70,81€ / 84,19€. **No identificado** qué modelo es la variante 197,73€. Documentado en `PENDIENTES_PROVEEDOR.md`.

### Pendientes documentados

Archivo nuevo `docs/santavila/PENDIENTES_PROVEEDOR.md` (creado en esta sesión) acumula todo lo que hay que confirmar con Balliu:
- HPL Gran Densidad (10 modelos)
- Sofia, Ágata L, Olimpia Esquinera, Mesa Greta, Silla Greta, Atlanta 240×90, Werzalit Ø60, Capri Doble pie alto, Mesa alta Ø70
- Discrepancias precio: Olimpia aux tela, Altea 70×70 HPL, Taburete Etna
- SKU duplicado Bruna 197,73€

### Cómo se ejecutó

```bash
python3 consolidate_balliu_sillas.py            # dry-run
python3 consolidate_balliu_sillas.py --apply    # backup + apply + publish
```

Backup: `backups/sillas_<timestamp>.json`.

### Siguiente paso

- **Repaso final de precios y nombres** de todos los productos consolidados (47 + 10 = 57 productos · ~1.460 variantes).
- **Familia 6 · Pasarelas resina Balliu** (~2 modelos).
- **Hevea**: auditoría completa pendiente.

---

## 2026-05-17 · Sub-piloto 3a cerrado — Mesa comedor Balliu (9 consolidados / 240 variantes + 34 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3a (Mesa comedor — el más complejo y último)
**Estado:** ✅ Aplicado en producción · 9 consolidados publicados en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_comedor.py`

### Cierre de la Familia 3 (Mesas HPL)

Con 3a se completan las 4 fases del sub-piloto Familia 3. **Resumen Familia 3 completa**:

| Sub-piloto | Modelos | ACTIVE | Variantes | DRAFT |
|---|---|---|---|---|
| 3b · Mesa alta | Capri Alta | 1 | 2 | 5 |
| 3c · Mesa centro | Etna Central | 1 | 15 | 1 |
| 3d · Mesa auxiliar | Eva Pro Mini/BCN, Olimpia, Noa, Etna, Mini Prestige | 7 | 98 | 10 |
| 3a · Mesa comedor | Selva, Brunei, Atlanta, Java, Capri, Capri Doble, Altea, Ágata, Nora | 9 | 240 | 34 |
| **Total Familia 3** | | **18** | **355** | **50** |

### Decisiones del dueño en 3a (confirmadas con capturas web)

1. **HPL Gran Densidad** → siempre DRAFT separado (regla aplicada a Brunei, Java, Capri, Altea, Capri Doble extras, Ágata extras).
2. **Brunei**: 4 tamaños × 3 chasis × 5 colores HPL = 60 variantes ACTIVE. HPL_GD a DRAFT.
3. **Altea como la web**: solo 70×70 y 80×80, 2 chasis (Blanco/Tórtola), 5 HPL = 20 variantes. Resto (Ø80, 120×80, HPL_GD) a DRAFT. Precio 70×70 HPL = 421,43 € (precio mínimo del rango web).
4. **Capri Doble**: producto APARTE, no variante del Capri principal.
5. **Nora**: dimensión 72×72 cm (web), no Ø70 (Excel).
6. **Sofia, Ágata L, Atlanta 240×90**: NO están en web → todos DRAFT.

### Resultado 3a · 9 productos ACTIVE consolidados

| # | Consolidado ACTIVE | Variantes | Estructura | Precio base (€ IVA) |
|---|---|---|---|---|
| 1 | Mesa exterior resina · Werzalit · **Selva** | 6 | Tamaño 6 | 181,58 – 315,80 |
| 2 | Mesa exterior aluminio · HPL · **Brunei** | **60** | Tamaño 4 × Chasis 3 × HPL 5 | 478,77 – 943,15 según tamaño |
| 3 | Mesa extensible exterior aluminio · HPL · **Atlanta** | 30 | Tamaño 2 × Chasis 3 × HPL 5 | 1.274,08 / 1.669,81 |
| 4 | Mesa extensible exterior aluminio · HPL · **Java** | 30 | Tamaño 2 × Chasis 3 × HPL 5 | 1.573,34 / 2.016,97 |
| 5 | Mesa exterior aluminio · HPL · **Capri** | **75** | Tamaño 5 × Chasis 3 × HPL 5 | 349,19 – 406,34 según tamaño |
| 6 | Mesa exterior aluminio · HPL 120×80 cm · **Capri Doble** | 15 | Chasis 3 × HPL 5 | 531,53 |
| 7 | Mesa exterior aluminio · HPL · **Altea** | 20 | Tamaño 2 × Chasis 2 × HPL 5 | 421,43 / 422,17 |
| 8 | Mesa exterior aluminio · 75×75 cm · **Ágata** | 2 | Color 2 | 347,39 |
| 9 | Mesa exterior aluminio · 72×72 cm · **Nora** | 2 | Color 2 | 224,10 |

### DRAFT (34 productos)

**28 productos planos legacy pasados a DRAFT**:
- 5 Selva (legacy del consolidado)
- 3 Atlanta (240×90 HPL + HPL_GD + 200/260×100 secundario)
- 3 Java (140/180 HPL_GD + 200/260 secundario + HPL_GD)
- 5 Capri (Capri Ø90 + 4 DIAM HPL/HPL_GD)
- 5 Altea (80×80 HPL/HPL_GD, Ø80 HPL/HPL_GD, 120×80 HPL)
- 2 Ágata (120×80 HPL GD, 180×90 encimera = Ágata L)
- 5 Sofia (no en web actual del proveedor)

**6 productos DRAFT nuevos** con tag `pendiente-confirmar-proveedor`:
- Brunei HPL Gran Densidad (4 variantes tamaño)
- Java HPL Gran Densidad (2 variantes)
- Capri HPL Gran Densidad (5 variantes)
- Capri Doble · HPL GD / pie alto (3 variantes)
- Altea · variantes extras (5 variantes: HPL_GD, Ø80, 120×80)
- Ágata · variantes extras (2 variantes: 120×80 HPL_GD, 180×90 encimera)

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_comedor.py            # dry-run
python3 consolidate_balliu_mesas_comedor.py --apply    # backup 36 productos + apply + publish
```

Backup: `backups/mesas_comedor_20260517-105449.json` (36 productos).

### Siguientes pasos

1. **Repaso final de precios** de todos los productos consolidados (1+2+1+7+9 = 20 productos consolidados activos en total tras Familias 1, 2 y 3).
2. **Familia 5: Sillas Balliu** (Etna, Bruna, Selva, Vera, Mila…).
3. **Familia 6: Pasarelas resina Balliu**.
4. **Hevea**: auditoría completa pendiente.
5. **Imágenes por variante** (todas las familias).
6. **Confirmar con proveedor Balliu**: HPL Gran Densidad, Sofia, Olimpia Esquinera, Mesa Greta, Ágata L, Atlanta 240×90 — todos en DRAFT con tag `pendiente-confirmar-proveedor`.

---

## 2026-05-17 · Sub-piloto 3d cerrado — Mesa auxiliar Balliu (7 consolidados / 98 variantes + 10 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3d (Mesa auxiliar)
**Estado:** ✅ Aplicado en producción · 7 consolidados publicados en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_auxiliares.py`

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu de 14 productos planos + 1 ya consolidado (Etna aux) en la categoría "mesa auxiliar".

### Decisiones del dueño aplicadas

1. **Patrón Blanco/Prestige** en Eva Pro Mini, Eva Pro BCN, Noa aux y Mini Prestige: Blanco más barato; el resto de colores comparten precio Prestige.
2. **Olimpia aux tela**: precio Excel (157,63 €) — discrepa de la web (149,34 €) pero el Excel es la fuente de verdad.
3. **Naming refinado** (regla nueva, memorizada): Opción C + sufijo " · <Modelo>" para identificar entre productos similares. Ejemplo: "Mesa auxiliar exterior resina · 48×48 cm · Eva Pro Mini".
4. **HPL Gran Densidad** y **Werzalit**: no figuran en web → productos DRAFT separados (pendiente confirmar con proveedor).
5. **Olimpia Esquinera** y **Mesa Greta**: no figuran en web → DRAFT (pendiente confirmar).

### Resultado (29 productos en total: 7 ACTIVE consolidados + 10 DRAFT)

| # | Consolidado ACTIVE | Variantes | Precio (€ IVA) |
|---|---|---|---|
| 1 | Mesa auxiliar exterior resina · 48×48 cm · **Eva Pro Mini** | 5 (Color) | 33,43 / 34,41 (Prestige) |
| 2 | Mesa auxiliar exterior resina · 48×48 cm · **Eva Pro BCN** | 5 (Color) | 35,99 / 37,79 |
| 3 | Mesa auxiliar exterior aluminio · 48×48 cm tejido · **Olimpia** | **48** (Chasis 3 × Color tejido 16) | 157,63 |
| 4 | Mesa de centro exterior · aluminio HPL 74×54 cm · **Olimpia Central** | 15 (Chasis 3 × Color tablero 5) | 227,18 |
| 5 | Mesa auxiliar exterior aluminio · Ø42 cm · **Noa** | 5 (Color) | 130,24 / 136,98 |
| 6 | Mesa auxiliar exterior · aluminio HPL 45×45 cm · **Etna** | 15 (Chasis 3 × Color tablero 5) | 167,00 |
| 7 | Mesa auxiliar exterior resina decorativa · 48×48 cm · **Mini Prestige** | 5 (Color) | 27,66 / 29,17 |

**DRAFT existentes pasados (8)**: duplicados Prestige de Eva Pro Mini/BCN/Noa/MiniMesa, Olimpia Central HPL_GD, Olimpia Esquinera HPL/HPL_GD, Mesa Greta. Todos con tag `legacy-balliu-consolidado-2026-05`.

**DRAFT nuevos creados (2)**:
- `mesa-auxiliar-exterior-aluminio-hpl-gd-45x45-etna` → Etna HPL Gran Densidad (175,06 €).
- `mesa-auxiliar-exterior-aluminio-werzalit-60-etna` → Etna Werzalit Ø60 (157,84 €).
Tags: `pendiente-confirmar-proveedor`, `legacy-balliu-consolidado-2026-05`.

### Hallazgo Etna aux

El producto plano Shopify mostraba dimensiones "60 cm" pero la web actual del proveedor dice **45×45×39 cm**. El SKU Werzalit Ø60 sí es de 60 cm — probablemente discontinuado pero a confirmar. El consolidado ACTIVE se queda con la dimensión actual del proveedor (45×45 cm).

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_auxiliares.py            # dry-run
python3 consolidate_balliu_mesas_auxiliares.py --apply    # backup + apply + publish
```

Backup: `backups/mesas_auxiliares_20260517-090517.json` (15 productos).

### Siguiente paso

- **Sub-piloto 3a · Mesa comedor** (Selva, Brunei, Atlanta, Java, Sofia, Capri, Altea, Ágata, Nora — ~25 productos planos, el más complejo).

---

## 2026-05-17 · Sub-piloto 3c cerrado — Mesa de centro exterior HPL (1 consolidado / 15 variantes + 1 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3c (Mesa centro)
**Estado:** ✅ Aplicado en producción · consolidado publicado en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_centro.py`

### Origen y estado previo

- **Proveedor:** Etna Mesa Central (110×60×44,5 cm, aluminio mate).
- **Shopify previo:** 1 producto ya consolidado `balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e` ACTIVE con 2 variantes "Tablero Hpl" / "Tablero Hpl Gd" (349,90 € / 421,95 €). SKUs BALLIU_ETNA_MESA_CENTRAL_*.

### Decisiones del dueño aplicadas

1. **HPL Gran Densidad no aparece en web actual del proveedor** → producto DRAFT separado nuevo, pendiente confirmación con proveedor.
2. **Chasis (3 colores: Blanco / Tórtola / Aluminio)** → opción visible al cliente.
3. **Color tablero HPL (5: Gris / Blanco / Moonwalk / Skyline / Prado)** → opción visible.
4. **Naming Opción C**: `Mesa de centro exterior · aluminio HPL 110×60 cm`.

### Regla UX descubierta (memorizada)

> Si una característica tiene un único valor, no se añade como opción seleccionable — ir a descripción del producto. Caso 3b mesa alta (chasis único = descripción) vs 3c mesa centro (3 chasis = opción).

### Resultado

| | Antes | Después |
|---|---|---|
| Productos ACTIVE | 1 con 2 variantes Hpl/Hpl Gd | **1 consolidado** con **15 variantes** (Chasis × Color tablero) |
| Productos DRAFT | 0 | **1 nuevo** (HPL Gran Densidad), 1 variante a 421,95 € |
| Opciones | 1 (Tablero) | 2 (Chasis × Color tablero) |
| Naming | "Mesa de centro exterior aluminio \| 60 cm" | "Mesa de centro exterior · aluminio HPL 110×60 cm" |
| Tags duplicados | `match-verde` | Limpiados |
| SKU pattern | BALLIU_ETNA_MESA_CENTRAL_* | `SV-MESACENTRO-<chasis>-<color>` |
| Precio HPL | 349,90 € (desactualizado) | **362,44 €** (Excel × 1.21) en las 15 variantes |
| Precio HPL GD | 421,95 € | **421,95 €** (en DRAFT) |

### Productos resultantes

- **ACTIVE** `balliu-mesa-de-centro-exterior-aluminio-60-cm-510b363e`
  - 15 variantes Chasis(3) × Color tablero(5), todas a 362,44 €.
- **DRAFT** `mesa-de-centro-exterior-aluminio-hpl-gd-110x60` (handle nuevo)
  - 1 variante "HPL Gran Densidad" a 421,95 €.
  - Tags: `pendiente-confirmar-proveedor`, `legacy-balliu-consolidado-2026-05`.

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_centro.py            # dry-run
python3 consolidate_balliu_mesas_centro.py --apply    # backup + apply + publish
```

Backup: `backups/mesas_centro_20260517-084523.json`.

### Siguiente paso

- **Sub-piloto 3d · Mesa auxiliar** (Eva Pro Mini/BCN, Olimpia, Noa aux, Etna aux, Greta — ~14 productos planos).

---

## 2026-05-17 · Sub-piloto 3b cerrado — Mesa alta exterior HPL (1 producto / 2 variantes + 5 DRAFT)

**Paso del flujo:** Sprint catálogo — Familia 3 (Mesas HPL), sub-piloto 3b (Mesa alta)
**Estado:** ✅ Aplicado en producción · consolidado publicado en Online Store + Shop
**Quién:** sesión interactiva con dueño · script `consolidate_balliu_mesas_altas.py`

### Decisión de partida: trocear la Familia 3 en sub-pilotos

Familia 3 (Mesas HPL) tiene ~50 productos planos en Shopify. Se decide trocear en 4 sub-pilotos por complejidad creciente y reducir el blast radius:

- **3b · Mesa alta** ← este sub-piloto
- **3c · Mesa centro**
- **3d · Mesa auxiliar**
- **3a · Mesa comedor** (el más complejo, último)

### Qué se ejecutó

Auditoría cruzada Shopify ↔ Excel ↔ web Balliu (Capri Alta). 6 productos planos en Shopify, todos ACTIVE con 1 variante "Default Title". Web del proveedor confirma que solo siguen vigentes 2 tamaños (60×60, 70×70) en HPL standard.

### Decisiones del dueño aplicadas

1. **Ø70 cm (mesa redonda)**: no figura en web actual del proveedor → **DRAFT**, no se elimina.
2. **HPL Gran Densidad**: no figura en web actual del proveedor → **DRAFT** las 4 SKUs HPL_GD.
3. **Precios desde Excel pestaña `20260508 -Todos `** (la única con IVA bien calculado en columna F y sin IVA en columna I). Se descarta usar otras pestañas (`Balliu`, `Todos`) — tienen columnas F = I (no separadas), no fiables.
4. **Chasis Aluminio**: como descripción de producto, **no como opción** visible.
5. **Naming Opción C**: sin nombre del modelo proveedor (Capri Alta) visible al cliente.

### Resultado

| | Antes (Shopify plano) | Después (consolidado) |
|---|---|---|
| Productos ACTIVE | 6 (con 1 variante c/u) | **1** consolidado con 2 variantes |
| Productos DRAFT | 0 | **5** (Ø70 HPL, Ø70 HPL GD, 60×60 HPL GD, 70×70 HPL GD, duplicado 60×60) |
| Naming | `Mesa alta exterior HPL` × 6 | `Mesa alta exterior · aluminio HPL 110 cm` |
| Tags duplicados | `match-rojo`, `envio:l` | Limpiados; legacy con `legacy-balliu-consolidado-2026-05` |
| Precio 60×60 HPL | €449,90 / €502,93 (caos) | **€456,69** (Excel × 1.21) |
| Precio 70×70 HPL | €529,00 (desactualizado) | **€528,46** (Excel × 1.21) |
| Winner Shopify | — | `balliu-mesa-alta-exterior-hpl-94512eab` |

Variantes ACTIVE finales:
- 60×60 cm — SKU `SV-MESAALTA-60-HPL` — €456,69
- 70×70 cm — SKU `SV-MESAALTA-70-HPL` — €528,46

### Hallazgo importante sobre pestañas del Excel

Solo **`20260508 -Todos `** (con espacio al final) tiene precios correctos:
- Columna F = "Precio Venta (con IVA 21%)" — IVA incluido ✓
- Columna I = "PVP Recomendado" — sin IVA; F = I × 1.21 ✓

Las pestañas `Balliu` y `Todos` tienen F = I (no separadas) → **no usar para precios**. Se memoriza.

### Anomalía detectada en Excel

Filas 222 y 223 del Excel comparten el mismo SKU `BALLIU_60X60_MESA_ALTA_TABLERO_HPL_GD_A3352658` pero con costes distintos (245,33€ vs 263,01€). Por diferencial de precio (HPL → HPL GD ≈ +7-12% en otros tamaños) se deduce que la fila 222 es **HPL standard mal etiquetado como GD**. Se trata como HPL standard para la variante 60×60 activa.

### Cómo se ejecutó

```bash
python3 consolidate_balliu_mesas_altas.py            # dry-run
python3 consolidate_balliu_mesas_altas.py --apply    # backup + apply + publish
```

Backup: `backups/mesas_altas_20260517-082726.json` (6 productos).

### Pendientes que arrastra al repaso final

- Confirmar con proveedor si Ø70 y HPL GD son legacy definitivos o pueden volver a venta.
- Decidir si el handle del winner se renombra a algo más limpio (`mesa-alta-exterior-aluminio-hpl`) en el repaso final con redirect 301.

### Siguiente paso

- **Sub-piloto 3c · Mesa centro** (Etna central, Olimpia central — ~2 modelos).

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

## 2026-06-24 · GEO Sprint 1 - PDPs con oportunidad GSC

**Paso del flujo:** GEO Sprint 1
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API

### Qué se ejecutó
- Se creó `scripts/apply_gsc_opportunity_descriptions.py` con dry-run, backup, reintentos y aplicación controlada.
- Se ejecutó dry-run contra Shopify Admin API para validar 8 productos con señal en GSC.
- Se aplicaron `descriptionHtml` y `seo.description` en las 8 fichas objetivo.
- El primer `--apply` sufrió un corte SSL puntual tras aplicar la pérgola; se endureció el script con reintentos y backup previo a mutaciones, y el segundo pase terminó con 8/8 OK.

### Entregables
- `scripts/apply_gsc_opportunity_descriptions.py` — script estrecho para el lote GEO Sprint 1.
- `docs/santavila/GSC-OPPORTUNITIES-2026-06-23.md` — sección "Sprint 1 aplicado".
- `content/descriptions/backup_gsc_opportunities_20260624-063513.json` — snapshot del dry-run.
- `content/descriptions/backup_gsc_opportunities_20260624-063613.json` — snapshot previo a la aplicación final.

### Hallazgos clave
- `santavila.es` resolvió a una página aparcada de Hostinger durante una comprobación inicial, pero el dominio trabajado en GSC es `santavila.com`, que sí apunta a Shopify (`23.227.38.x`).
- Verificación pública confirmada en `santavila.com` para pérgola y base de parasol: los textos aparecen en meta/OG y JSON-LD de producto.
- Las fichas ya existían y se actualizaron sin errores de GraphQL.
- Se reforzaron consultas por medida/intención: `pérgola 250x300`, `sofa terraza 120 cm`, `sofa exterior 130 cm`, `banco con mesa incorporada`, `base para sombrilla` y cluster de tumbonas.

### Siguiente paso recomendado
- Revisar si `santavila.es` debe redirigir a `santavila.com` o quedar fuera de la estrategia.
- Pasar a Sprint 1.2: enlazado interno desde colecciones hacia estas PDPs y pequeños bloques de ayuda en colecciones `tumbonas`, `sofás de exterior`, `pérgolas` y `parasoles`.

---

## 2026-06-24 · GEO Sprint 1.2 - enlazado interno desde colecciones

**Paso del flujo:** GEO Sprint 1.2
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + Asset API

### Qué se ejecutó
- Se reforzó `scripts/apply_collections.py` con reintentos ante cortes SSL puntuales de Shopify.
- Se actualizaron intros/meta/FAQ de las 6 colecciones principales, añadiendo anchors hacia PDPs con oportunidad GSC.
- Se añadió en `theme/sections/santavila-collection-grid.liquid` un bloque visible `También se busca` con enlaces internos contextuales por colección.
- Se subió el asset a DEV `189114876228` y LIVE `189222715716`, verificado remoto == local.

### Entregables
- `scripts/apply_collections.py` — reintentos y copy de colección reforzado.
- `theme/sections/santavila-collection-grid.liquid` — bloque `sv-csuggest` con enlaces internos.
- `docs/santavila/GSC-OPPORTUNITIES-2026-06-23.md` — sección "Sprint 1.2 aplicado".
- `content/descriptions/backup_collections_20260624-073205.json` y `backup_collections_20260624-073212.json` — snapshots antes de aplicar.

### Hallazgos clave
- Verificación pública en `santavila.com`: el bloque aparece en sofás, tumbonas, parasoles y accesorios.
- El enlazado empuja señales hacia `sofa terraza 120 cm`, `sofa exterior 130 cm`, tumbonas Balliu/resina, `base de parasol 25 kg` y `pérgola 250x300`.
- La primera consulta pública devolvió mucho HTML por scripts de Shopify, pero los anchors aparecen en HTML SSR y no dependen de JavaScript.

### Siguiente paso recomendado
- Completar Sprint 1 con 7-12 PDP adicionales por señal comercial: rinconeras, sofá bicolor, parasoles acrílicos y conjuntos.
- Después, pasar a Sprint 2: páginas de confianza y E-E-A-T enlazadas desde footer/PDP/colecciones.

---

## 2026-06-24 · GEO Sprint 1.3 - desduplicación PDP Hevea top

**Paso del flujo:** GEO Sprint 1.3
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + contraste público con `curl`

### Qué se ejecutó
- Se contrastó una ficha Balliu pública (`parasol-ocean-tejido-acrilico`) contra Santavila y no se detectó duplicado literal relevante: los solapes eran navegación/legal.
- Se priorizó Hevea porque varias PDPs heredaban frases del CSV de proveedor y los bicolor tenían descripciones públicas muy finas.
- Se creó `scripts/apply_desduplicated_descriptions.py` con dry-run, backup, reintentos y aplicación controlada.
- Se aplicaron `descriptionHtml` y `seo.description` a 6 PDPs de alto valor: 4 rinconeras y 2 sets bicolor.

### Entregables
- `scripts/apply_desduplicated_descriptions.py` — script de Sprint 1.3 para reescritura anti-duplicado.
- `content/descriptions/backup_desduplicated_20260624-083550.json` — snapshot previo a la aplicación.
- `docs/santavila/GSC-OPPORTUNITIES-2026-06-23.md` — sección "Sprint 1.3 aplicado".

### Hallazgos clave
- En Shopify Admin las 6 fichas quedaron actualizadas sin errores.
- Verificación pública confirmada con cache-buster para bicolor 2/3 plazas y sin cache-buster para rinconera contemporánea/sofisticada.
- Los sets bicolor pasaron de 31-35 palabras a 87-101 palabras, con intención `sofá bicolor`, `set jardín bicolor` y `sofá exterior bicolor`.
- Las rinconeras refuerzan `rinconera terraza`, `rinconera jardín`, `sofá de esquina exterior` y `set rinconera exterior`, evitando las frases más calcadas del CSV Hevea.

### Siguiente paso recomendado
- Pasar a Sprint 2: confianza/E-E-A-T y páginas auxiliares enlazadas desde footer, PDP y colecciones.
- Mantener un lote posterior para sofás individuales bicolor y sofás 3 plazas si GSC confirma impresiones crecientes.

---

## 2026-06-24 · GEO Sprint 2 - páginas de confianza y E-E-A-T

**Paso del flujo:** GEO Sprint 2
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + Asset API

### Qué se ejecutó
- Se creó `scripts/apply_trust_pages.py` con dry-run, backup y aplicación controlada.
- Se crearon 4 páginas publicadas en Shopify: `/pages/sobre-santavila`, `/pages/envio`, `/pages/garantia` y `/pages/mantenimiento`.
- Se enlazaron las páginas desde PDP, colecciones y footer para que queden accesibles en HTML SSR.
- Se reforzó `scripts/push_theme_assets.py` con reintentos por cortes SSL puntuales de Shopify.

### Entregables
- `scripts/apply_trust_pages.py` — creación/refuerzo de páginas de confianza.
- `theme/sections/santavila-product.liquid` — enlaces de entrega, mantenimiento y garantía en el panel de confianza PDP.
- `theme/sections/santavila-collection-grid.liquid` — bloque `Compra con tranquilidad` en colecciones.
- `theme/sections/santavila-footer.liquid` — enlaces persistentes a páginas de confianza.
- `content/descriptions/backup_trust_pages_20260624-092444.json` — snapshot previo a la creación final.

### Hallazgos clave
- Las 4 páginas nuevas responden 200 en producción.
- Verificación pública confirmada en HTML SSR para PDP, colección, footer y `/pages/sobre-santavila`.
- La página de devoluciones se mantiene como policy canónica de Shopify (`/policies/refund-policy`) para no duplicar condiciones legales.
- Shopify devolvió alguna verificación prematura en DEV, pero los assets quedaron remoto == local tras comprobación directa; LIVE quedó subido y verificado por script.

### Siguiente paso recomendado
- Sprint 3: schema GEO, empezando por `BreadcrumbList`, `FAQPage` en colecciones y `Organization` con enlaces a páginas de confianza.
- Después Sprint 4: guías citables sobre materiales, lluvia/sol y mantenimiento enlazadas desde estas páginas.

---

## 2026-06-24 · GEO Sprint 3 - schema GEO

**Paso del flujo:** GEO Sprint 3
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Asset API + verificación pública con `curl`

### Qué se ejecutó
- Se auditó JSON-LD actual en home, colección, PDP y página de confianza.
- Se creó `theme/snippets/santavila-schema.liquid` para emitir schema global controlado.
- Se conectó el snippet desde `theme/layout/theme.liquid`.
- Se retiró el `Organization` básico de `theme/sections/header.liquid` porque generaba `url` con la página actual.
- Se subió el cambio a DEV y LIVE.

### Entregables
- `theme/snippets/santavila-schema.liquid` — `Organization`/`OnlineStore`, `BreadcrumbList` e `ItemList`.
- `theme/layout/theme.liquid` — render global del snippet.
- `theme/sections/header.liquid` — retirada del schema antiguo.
- `docs/santavila/GEO-SCHEMA-REPORT.md` — informe del sprint.

### Hallazgos clave
- Home ahora emite `Organization` + `OnlineStore` con `@id` estable `https://santavila.com#organization`.
- Colecciones emiten `BreadcrumbList`, `ItemList` y mantienen `FAQPage`.
- PDPs emiten `BreadcrumbList` y mantienen `Product` nativo de Shopify.
- Páginas de confianza emiten `BreadcrumbList`.
- No se añadió `AggregateRating` porque todavía no hay reviews reales.

### Siguiente paso recomendado
- Sprint 4: guías citables con `Article` + `FAQPage`, empezando por materiales, lluvia/sol y mantenimiento.

---

## 2026-06-24 · GEO Sprint 4.1 - primera guía citable

**Paso del flujo:** GEO Sprint 4
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificación pública con `curl`

### Qué se ejecutó
- Se creó `scripts/apply_geo_guides.py` con dry-run, backup y aplicación controlada.
- Se publicó la guía `/blogs/news/que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol`.
- Se añadió un enlace desde `/pages/mantenimiento` hacia la guía.
- Se verificó HTML público, meta y schema.

### Entregables
- `scripts/apply_geo_guides.py` — creación/refuerzo de guías GEO.
- `scripts/apply_trust_pages.py` — página de mantenimiento enlazada a la guía.
- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md` — informe de contenido citable.

### Hallazgos clave
- La guía publica ~1.099 palabras, tabla comparativa, secciones por material/caso y FAQ con 5 preguntas.
- Schema verificado: `Organization` + `OnlineStore`, `BreadcrumbList`, `Article` y `FAQPage`.
- Enlazado interno saliente hacia sillas, tumbonas, mesas, parasoles, guía de materiales y mantenimiento.
- Enlazado entrante desde `/pages/mantenimiento`.

### Siguiente paso recomendado
- Sprint 4.2: reforzar o rehacer la guía de materiales existente, o publicar una nueva guía específica `Aluminio, resina, HPL o madera: qué material elegir`.

---

## 2026-06-25 · GEO Sprint 4.2 - guía de materiales contrastada

**Paso del flujo:** GEO Sprint 4
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificación pública con `curl`

### Qué se ejecutó
- Se reforzó la guía existente `/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico`.
- Se evitó crear una URL nueva para no canibalizar el artículo de materiales ya existente.
- Se contrastó el contenido con referencias externas sobre HPL/EN 438, ratán sintético PE, textiles de exterior y teca.
- Se verificó HTML público, canonical, meta, H1 y schema.

### Entregables
- `scripts/apply_geo_guides.py` — ahora gestiona la guía de materiales y la guía lluvia/sol.
- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md` — informe actualizado con Sprint 4.2.

### Hallazgos clave
- La guía pasa de ~731 a ~1.467 palabras.
- Schema verificado: `BreadcrumbList`, `Article` y `FAQPage` con 5 preguntas.
- El copy evita afirmaciones absolutas y aterriza la decisión por uso real: sol, piscina, costa, porche, uso intensivo y mantenimiento.
- La URL pública devuelve 200 con canonical correcto.

### Siguiente paso recomendado
- Sprint 4.3: guía de limpieza/mantenimiento citable, cuidando no duplicar la página `/pages/mantenimiento`.

---

## 2026-06-25 · GEO Sprint 4.3 - guía de mantenimiento contrastada

**Paso del flujo:** GEO Sprint 4
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificación pública con `curl`

### Qué se ejecutó
- Se reforzó la guía existente `/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada`.
- Se mantuvo `/pages/mantenimiento` como hub/resumen y se enlazó hacia la guía larga.
- Se contrastó el contenido con fuentes externas sobre textiles técnicos, HDPE/polietileno, teca y limpieza por material.
- Se verificó HTML público, canonical, meta, H1, tabla y schema.

### Entregables
- `scripts/apply_geo_guides.py` — ahora gestiona materiales, lluvia/sol y mantenimiento.
- `scripts/apply_trust_pages.py` — página de mantenimiento enlazada a la guía larga.
- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md` — informe actualizado con Sprint 4.3.

### Hallazgos clave
- La guía pasa de ~761 a ~1.306 palabras.
- Schema verificado: `BreadcrumbList`, `Article` y `FAQPage` con 5 preguntas.
- El copy evita recomendaciones agresivas: hidrolimpiadora a presión alta, lejía generalizada o abrasivos como primera opción.
- La URL pública devuelve 200 con canonical correcto.

### Siguiente paso recomendado
- Sprint 4.4: guía de muebles para terraza pequeña y balcón.

---

## 2026-06-26 · GEO Sprint 4.4 - guía terraza pequeña y balcón

**Paso del flujo:** GEO Sprint 4
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificación pública con `curl`

### Qué se ejecutó
- Se reforzó la guía existente `/blogs/news/como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales`.
- Se mantuvo la URL previa para no canibalizar contenido ya indexable.
- Se contrastó el contenido con fuentes externas sobre distribución, medidas de paso/comedor y soluciones de balcón compacto.
- Se verificó HTML público, canonical, meta, H1, tabla y schema.

### Entregables
- `scripts/apply_geo_guides.py` — ahora gestiona materiales, lluvia/sol, mantenimiento y terraza pequeña.
- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md` — informe actualizado con Sprint 4.4.

### Hallazgos clave
- La guía pasa de ~566 a ~1.319 palabras.
- Schema verificado: `BreadcrumbList`, `Article` y `FAQPage` con 5 preguntas.
- La guía evita reglas rígidas y propone bajar escala cuando el balcón no permite un comedor completo.
- La URL pública devuelve 200 con canonical correcto.

### Siguiente paso recomendado
- Sprint 4.5: guía de mesas de exterior por medidas, comensales y espacio necesario.

---

## 2026-06-27 · GEO Sprint 4.5 - guía mesas por medidas y comensales

**Paso del flujo:** GEO Sprint 4
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificación pública con `curl`

### Qué se ejecutó
- Se creó la guía `/blogs/news/como-elegir-mesa-de-exterior-medidas-comensales-y-espacio-necesario`.
- Se contrastó el contenido con fuentes externas sobre medidas de mesa, espacio para sillas, ancho por comensal y mesas para espacios pequeños.
- Se verificó HTML público, canonical, meta, H1, tabla y schema.

### Entregables
- `scripts/apply_geo_guides.py` — ahora gestiona materiales, lluvia/sol, mantenimiento, terraza pequeña y mesas.
- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md` — informe actualizado con Sprint 4.5.

### Hallazgos clave
- La guía publica ~1.231 palabras.
- Schema verificado: `BreadcrumbList`, `Article` y `FAQPage` con 5 preguntas.
- La guía aterriza medidas por 2, 4, 6 y 8 comensales, con advertencias por sillas, brazos, extensibles y paso real.
- La URL pública devuelve 200 con canonical correcto.

### Siguiente paso recomendado
- Sprint 4.6: comparativa de tumbona de aluminio vs madera/resina.

---

## 2026-06-27 · GEO Sprint 4.6 - guía tumbonas por material

**Paso del flujo:** GEO Sprint 4
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificación pública con `curl`

### Qué se ejecutó
- Se creó la guía `/blogs/news/tumbona-de-aluminio-resina-o-madera-cual-elegir-para-exterior`.
- Se contrastó el contenido con fuentes externas sobre aluminio, resina/PE, teca, textiles técnicos, piscina, costa y mantenimiento.
- Se verificó HTML público, canonical, meta, H1, tabla y schema.

### Entregables
- `scripts/apply_geo_guides.py` — ahora gestiona 6 guías citables del cluster GEO inicial.
- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md` — informe actualizado con Sprint 4.6.

### Hallazgos clave
- La guía publica ~1.120 palabras.
- Schema verificado: `BreadcrumbList`, `Article` y `FAQPage` con 5 preguntas.
- La guía diferencia material principal, acabado, tornillería, salitre, cloro, ruedas, respaldo y colchoneta.
- La URL pública devuelve 200 con canonical correcto.

### Siguiente paso recomendado
- Cerrar Sprint 4 como cluster inicial y pasar a Sprint 5: autoridad de marca y señales externas.

---

## 2026-06-27 · GEO Sprint 5 - autoridad de marca y menciones externas

**Paso del flujo:** GEO Sprint 5
**Estado:** 🔄 iniciado
**Quién/qué:** Codex + revision theme + contraste guia oficial Google Business Profile

### Qué se ejecutó
- Se creo el documento operativo de autoridad externa para Santavila.
- Se reviso el theme para confirmar soporte de enlaces sociales en footer.
- Se dejo pendiente `sameAs` hasta tener perfiles publicos reales y verificables.
- Se contrasto el criterio de Google Business Profile con la guia oficial de Google.

### Entregables
- `docs/santavila/GEO-BRAND-MENTIONS.md` — roadmap de perfiles, reviews, menciones, Pinterest, piezas visuales y `sameAs`.
- `docs/santavila/GEO-SOCIAL-CONTENT-PACK.md` — copys y guiones base para Pinterest, Instagram y YouTube Shorts.

### Hallazgos clave
- El footer ya soporta Instagram y Pinterest desde ajustes del theme.
- El schema de organizacion no debe incluir `sameAs` hasta tener URLs reales.
- Google Business Profile solo conviene si Santavila tiene ubicacion visitable o servicio presencial elegible.
- El cluster de 6 guias ya puede reutilizarse como contenido social sin tocar producto ni precios.

### Decisiones pendientes
- Confirmar si Santavila es elegible para Google Business Profile.
- Crear o facilitar URLs reales de Instagram, Pinterest, LinkedIn y YouTube.
- Elegir plataforma principal de reviews.

### Siguiente paso recomendado
- Con URLs reales, aplicar `sameAs` en schema y enlazado social en theme.

---

## 2026-06-27 · GEO Sprint 6 - reaudit endpoints agenticos Shopify

**Paso del flujo:** GEO Sprint 6
**Estado:** ✅ validado
**Quién/qué:** Codex + `curl` publico

### Qué se ejecutó
- Se validaron `llms.txt`, `agents.md`, `/.well-known/ucp`, `robots.txt` y `sitemap.xml`.
- Se comprobo redireccion 301 de `santavila.es` y `www.santavila.es` hacia `santavila.com` en endpoints agenticos.
- Se actualizo el informe de endpoints agenticos.

### Entregables
- `docs/santavila/GEO-AGENTIC-ENDPOINTS-REPORT.md` — informe actualizado con reaudit 2026-06-27.

### Hallazgos clave
- `llms.txt` y `agents.md` responden `200` y siguen generados por Shopify.
- `robots.txt` declara `agents.md`, UCP discovery, UCP/MCP endpoint y sitemap.
- `santavila.es` redirige `301` al dominio primario en los endpoints probados.
- UCP sigue devolviendo endpoints con `mueblesexterior.myshopify.com`, aunque `merchant_origin` aparece como `santavila.com`.

### Siguiente paso recomendado
- No tocar `llms.txt` desde theme; seguir con contenido, schema, reviews, menciones y enlazado interno.

---

## 2026-06-27 · GEO Reauditoria - delta GSC y siguiente lote PDP

**Paso del flujo:** Reauditoria y delta
**Estado:** ✅ ejecutado
**Quién/qué:** Codex + Google Search Console

### Qué se ejecutó
- Se actualizo `SEO-BASELINE.md` con ventana 2026-05-30 -> 2026-06-26.
- Se ejecuto el informe de oportunidades GSC de 90 dias.
- Se creo un informe delta con prioridades por URL/query.

### Entregables
- `SEO-BASELINE.md` — baseline GSC actualizado.
- `docs/santavila/GEO-DELTA-2026-06-27.md` — lectura de delta y siguiente lote de PDPs.

### Hallazgos clave
- 28 dias: 9 clics, 636 impresiones, CTR 1,42%, posicion media 16,7.
- El delta frente al 2026-06-23 aun es pequeno: las guias nuevas necesitan crawl y maduracion.
- Hay oportunidades claras en `banco con mesa incorporada`, `pérgola 250x300`, sofas 120/130 cm, tumbonas Balliu/resina y rinconeras.

### Siguiente paso recomendado
- Refuerzo quirurgico de PDPs con senales GSC: title/meta/descripcion y enlazado interno desde guias.

---

## 2026-06-27 · GEO PDP audit - descripciones pobres

**Paso del flujo:** PDP quality audit
**Estado:** ✅ ejecutado
**Quién/qué:** Codex + Shopify Admin API

### Qué se ejecutó
- Se ejecuto auditoria viva de productos activos.
- Se ajusto `scripts/audit_products.py` para medir descripciones con umbrales utiles para GEO, no solo vacias.
- Se creo un informe especifico de calidad PDP.

### Entregables
- `auditoria_fichas_report.csv` — export actualizado.
- `docs/santavila/GEO-PDP-DESCRIPTION-AUDIT-2026-06-27.md` — diagnostico y sprint propuesto.
- `scripts/audit_products.py` — umbrales ajustados: pobre, fina, aceptable y rica.

### Hallazgos clave
- 171 productos activos.
- 118 productos activos tienen menos de 80 palabras.
- 79 productos activos tienen menos de 50 palabras.
- Solo 1 producto activo supera 120 palabras.

### Siguiente paso recomendado
- Ejecutar Sprint PDP 2.0 por familias, empezando por productos con senales GSC y familias con muchas fichas pobres.

---

## 2026-06-27 · GEO PDP 2.0 - batch 1 con señales GSC

**Paso del flujo:** PDP 2.0
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se creo `scripts/apply_pdp_rich_descriptions.py`.
- Se ejecuto dry-run y aplicacion sobre 6 PDP con señales GSC.
- Se actualizaron descripcion HTML y meta description SEO.
- Se verifico que el HTML publico y JSON-LD incluyen los nuevos textos.

### Entregables
- `scripts/apply_pdp_rich_descriptions.py` — lote 1 reutilizable.
- `content/descriptions/backup_pdp_rich_batch1_20260627-093828.json` — backup dry-run.
- `content/descriptions/backup_pdp_rich_batch1_20260627-093834.json` — backup previo a aplicar.
- `auditoria_fichas_report.csv` — auditoria recalculada tras aplicar.

### Productos aplicados
- `/products/banco-jardin-con-mesa-integrada-220-cm` — 81 -> 190 palabras.
- `/products/pergola-aluminio-para-jardin-300300250-cm` — 94 -> 192 palabras.
- `/products/sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm` — 90 -> 185 palabras.
- `/products/sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm` — 78 -> 196 palabras.
- `/products/balliu-tumbona-de-exterior-resina-28ff014d` — 73 -> 190 palabras.
- `/products/set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro` — 100 -> 196 palabras.

### Hallazgos clave
- Productos activos con descripcion rica 120+ palabras: 1 -> 7.
- Productos activos bajo 80 palabras: 118 -> 116.
- La prioridad sigue estando en sofas, conjuntos sofa, sillones y mesas centro.

### Siguiente paso recomendado
- Batch 2: sofas/conjuntos con menos de 50 palabras y potencial long-tail por medida/plazas.

---

## 2026-06-28 · GEO PDP 2.0 - batch 2 sofas y conjuntos

**Paso del flujo:** PDP 2.0
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se creo `scripts/apply_pdp_rich_descriptions_batch2.py`.
- Se ejecuto dry-run y aplicacion sobre 10 PDP de sofas/conjuntos.
- Se actualizaron descripcion HTML y meta description SEO.
- Se verifico que el bloque visible `Descripción y detalles` aparece en PDPs publicas.

### Entregables
- `scripts/apply_pdp_rich_descriptions_batch2.py` — lote 2 reutilizable.
- `content/descriptions/backup_pdp_rich_batch2_20260628-105748.json` — backup dry-run.
- `content/descriptions/backup_pdp_rich_batch2_20260628-105759.json` — backup previo a aplicar.
- `auditoria_fichas_report.csv` — auditoria recalculada tras aplicar.

### Productos aplicados
- 6 sofas por plazas/medidas: 33-37 -> 177-188 palabras.
- 4 conjuntos sofa: 30-31 -> 174-180 palabras.

### Hallazgos clave
- Productos activos con descripcion rica 120+ palabras: 7 -> 17.
- Productos activos bajo 80 palabras: 116 -> 106.
- Productos activos con menos de 50 palabras: 79 -> 69.

### Siguiente paso recomendado
- Batch 3: sofas/conjuntos restantes con menos de 50 palabras, sillones y mesas centro.

---

## 2026-06-28 · GEO PDP 2.0 - batch 3 sofas, conjuntos y bancos

**Paso del flujo:** PDP 2.0
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se creo `scripts/apply_pdp_rich_descriptions_batch3.py`.
- Se ejecuto dry-run y aplicacion sobre 12 PDP: sofas, conjuntos sofa y bancos.
- Se actualizaron descripcion HTML y meta description SEO.
- Se verifico en publico que el HTML, JSON-LD y bloque visible `Descripción y detalles` ya sirven los nuevos textos.

### Entregables
- `scripts/apply_pdp_rich_descriptions_batch3.py` — lote 3 reutilizable.
- `content/descriptions/backup_pdp_rich_batch3_20260628-111220.json` — backup dry-run.
- `content/descriptions/backup_pdp_rich_batch3_20260628-111226.json` — backup previo a aplicar.
- `auditoria_fichas_report.csv` — auditoria recalculada tras aplicar.

### Productos aplicados
- 5 sofas por plazas/medidas: 38 -> 159-166 palabras.
- 5 conjuntos sofa: 30-32 -> 157-165 palabras.
- 2 bancos de exterior: 33-35 -> 165-172 palabras.

### Hallazgos clave
- Productos activos con descripcion rica 120+ palabras: 17 -> 29.
- Productos activos bajo 80 palabras: 106 -> 94.
- Productos activos con menos de 50 palabras: 69 -> 57.

### Siguiente paso recomendado
- Batch 4: sillones con menos de 80 palabras, mesas de centro HPL, tumbonas y reposapies.

---

## 2026-06-28 · GEO PDP 2.0 - batch 4 sillones

**Paso del flujo:** PDP 2.0
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se creo `scripts/apply_pdp_rich_descriptions_batch4.py`.
- Se ejecuto dry-run y aplicacion sobre 16 PDP de sillones de exterior.
- Se actualizaron descripcion HTML y meta description SEO.
- Se verifico en publico que el HTML, JSON-LD y bloque visible `Descripción y detalles` ya sirven los nuevos textos.

### Entregables
- `scripts/apply_pdp_rich_descriptions_batch4.py` — lote 4 reutilizable.
- `content/descriptions/backup_pdp_rich_batch4_20260628-114046.json` — backup dry-run.
- `content/descriptions/backup_pdp_rich_batch4_20260628-114053.json` — backup previo a aplicar.
- `auditoria_fichas_report.csv` — auditoria recalculada tras aplicar.

### Productos aplicados
- 16 sillones de exterior: 33-67 -> 154-165 palabras.

### Hallazgos clave
- Productos activos con descripcion rica 120+ palabras: 29 -> 45.
- Productos activos bajo 80 palabras: 94 -> 78.
- Productos activos con menos de 50 palabras: 57 -> 44.
- La familia `Sillón` ya no aparece como pendiente bajo 80 palabras.

### Siguiente paso recomendado
- Batch 5: mesas de centro HPL, tumbonas y reposapies.

---

## 2026-06-28 · GEO PDP 2.0 - batch 5 mesas centro, tumbonas y reposapies

**Paso del flujo:** PDP 2.0
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se creo `scripts/apply_pdp_rich_descriptions_batch5.py`.
- Se ejecuto dry-run y aplicacion sobre 25 PDP: mesas de centro, reposapies y tumbonas.
- Se actualizaron descripcion HTML y meta description SEO.
- Se verifico en publico que el HTML, JSON-LD y bloque visible `Descripción y detalles` ya sirven los nuevos textos.

### Entregables
- `scripts/apply_pdp_rich_descriptions_batch5.py` — lote 5 reutilizable.
- `content/descriptions/backup_pdp_rich_batch5_20260628-122122.json` — backup dry-run.
- `content/descriptions/backup_pdp_rich_batch5_20260628-122131.json` — backup previo a aplicar.
- `auditoria_fichas_report.csv` — auditoria recalculada tras aplicar.

### Productos aplicados
- 12 mesas de centro: 34-70 -> 129-142 palabras.
- 6 reposapies: 36-41 -> 136-145 palabras.
- 7 tumbonas: 72-77 -> 156-165 palabras.

### Hallazgos clave
- Productos activos con descripcion rica 120+ palabras: 45 -> 70.
- Productos activos bajo 80 palabras: 78 -> 53.
- Productos activos con menos de 50 palabras: 44 -> 27.
- `Mesa centro`, `Tumbona` y `Reposapiés` ya no aparecen como familias pendientes bajo 80 palabras.

### Siguiente paso recomendado
- Batch 6: terminar sofas/conjuntos restantes o cerrar familias menores: sillas, mesas comedor, parasoles, fundas y accesorios.

---

## 2026-06-28 · GEO PDP 2.0 - batch 6 sofas y conjuntos restantes

**Paso del flujo:** PDP 2.0
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se creo `scripts/apply_pdp_rich_descriptions_batch6.py`.
- Se ejecuto dry-run, se corrigio el parser de estilos para sets y se aplico sobre 31 PDP.
- Se actualizaron descripcion HTML y meta description SEO.
- Se verifico en publico que el HTML, JSON-LD y bloque visible `Descripción y detalles` ya sirven los nuevos textos.

### Entregables
- `scripts/apply_pdp_rich_descriptions_batch6.py` — lote 6 reutilizable.
- `content/descriptions/backup_pdp_rich_batch6_20260628-123505.json` — backup dry-run inicial.
- `content/descriptions/backup_pdp_rich_batch6_20260628-123524.json` — backup dry-run corregido.
- `content/descriptions/backup_pdp_rich_batch6_20260628-123534.json` — backup previo a aplicar.
- `auditoria_fichas_report.csv` — auditoria recalculada tras aplicar.

### Productos aplicados
- 16 sofas: 39-71 -> 157-174 palabras.
- 15 conjuntos sofa: 33-77 -> 174-186 palabras.

### Hallazgos clave
- Productos activos con descripcion rica 120+ palabras: 70 -> 101.
- Productos activos bajo 80 palabras: 53 -> 22.
- Productos activos con menos de 50 palabras: 27 -> 7.
- `Sofá` y `Conjunto sofá` ya no aparecen como familias pendientes bajo 80 palabras.

### Siguiente paso recomendado
- Batch 7 opcional: cerrar familias menores restantes o pausar y medir impacto en GSC tras recrawl.

---

## 2026-06-28 · GEO PDP 2.0 - batch 7 cierre de familias menores

**Paso del flujo:** PDP 2.0
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se creo `scripts/apply_pdp_rich_descriptions_batch7.py`.
- Se ejecuto dry-run, se aplico sobre 22 PDP de familias menores y se reaplico una correccion de lenguaje para productos sin material explicito.
- Se actualizaron descripcion HTML y meta description SEO.
- Se verifico en publico que el HTML, JSON-LD y bloque visible `Descripción y detalles` sirven los nuevos textos.

### Entregables
- `scripts/apply_pdp_rich_descriptions_batch7.py` — lote 7 reutilizable.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124709.json` — backup dry-run inicial.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124726.json` — backup dry-run corregido.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124735.json` — backup previo a aplicar.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124931.json` — backup dry-run de correccion de lenguaje.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124940.json` — backup previo a reaplicar correccion.
- `auditoria_fichas_report.csv` — auditoria recalculada tras aplicar.

### Productos aplicados
- 22 productos: sillas, mesas comedor, mesas auxiliares, fundas, parasoles, accesorios, balancin, rinconera, mini tumbona y mobiliario exterior.

### Hallazgos clave
- Productos activos con descripcion rica 120+ palabras: 101 -> 123.
- Productos activos bajo 80 palabras: 22 -> 0.
- Productos activos con menos de 50 palabras: 7 -> 0.
- Productos activos entre 50 y 79 palabras: 15 -> 0.
- Quedan 48 fichas aceptables de 80-119 palabras para optimizacion selectiva, no como deuda critica.

### Siguiente paso recomendado
- Pausar reescritura masiva, dejar recrawlear y volver a GSC para priorizar las 48 fichas aceptables por señales reales.

---

## 2026-06-29 · GEO delta y enlaces internos por señales GSC

**Paso del flujo:** Reauditoria GEO + enlazado interno
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Google Search Console + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se ejecuto baseline GSC de 28 dias y oportunidades de 90 dias.
- Se identificaron clusters con señales reales: tumbonas Balliu/resina, pergola 250x300, bases/parasol, sofas compactos y banco con mesa.
- Se creo y aplico `scripts/apply_geo_cluster_links_20260629.py`.
- Se insertaron bloques pequeños de enlaces contextuales en 5 guias editoriales.

### Entregables
- `SEO-BASELINE.md` — baseline GSC actualizado a 2026-06-29.
- `docs/santavila/GEO-DELTA-2026-06-29.md` — informe del delta y decision de sprint.
- `scripts/apply_geo_cluster_links_20260629.py` — script reutilizable/idempotente para los bloques de enlaces.
- `content/descriptions/backup_geo_cluster_links_20260629-145138.json` — backup dry-run.
- `content/descriptions/backup_geo_cluster_links_20260629-145143.json` — backup previo a aplicar.

### Hallazgos clave
- 28 dias GSC: 10 clics, 675 impresiones, CTR 1,48%, posicion media 17,7.
- Sitemap HTTPS limpio: 0 errores, 0 warnings.
- El cluster mas claro sigue siendo tumbonas Balliu/resina.
- Tambien hay señales accionables en pergola 250x300, bases de parasol, sofas 120/130 cm y banco con mesa.

### Siguiente paso recomendado
- Esperar 7-10 dias para recrawl.
- Si tumbonas mantiene crecimiento, crear/reforzar un hub especifico de tumbonas Balliu/resina.

---

## 2026-06-29 · Imagen destacada en guias GEO

**Paso del flujo:** GEO editorial
**Estado:** ✅ aplicado
**Quién/qué:** Codex + Shopify Admin API + verificacion publica con `curl`

### Qué se ejecutó
- Se revisaron 5 guias editoriales recientes.
- Se subieron imagenes destacadas reales a las 4 guias que no tenian imagen.
- Se añadió alt descriptivo a la guia de terraza pequena, que ya tenia imagen.
- Se verifico que Shopify expone `og:image`, `og:image:secure_url`, `summary_large_image` e imagen visible con alt.

### Entregables
- `scripts/apply_blog_featured_images_20260629.py` — script de subida de imagenes destacadas para articulos.
- `content/descriptions/backup_blog_featured_images_20260629-150354.json` — backup dry-run.
- `content/descriptions/backup_blog_featured_images_20260629-150359.json` — backup previo a aplicar.

### Guias actualizadas
- Guia de tumbonas por material.
- Guia de muebles resistentes a lluvia y sol.
- Guia de mesa exterior por medidas y comensales.
- Guia de mantenimiento de muebles de exterior.
- Guia de terraza pequena.

### Ajuste posterior
- La imagen inicial de mantenimiento era poco contextual y de baja definicion.
- La primera version generada (`content/images/blog/mantenimiento-muebles-exterior-hero-20260629.png`) se descarto como imagen final porque no mostraba claramente el uso de la funda.
- Se reaprovecho la referencia de una tumbona junto a piscina y se genero una version final con la tumbona protegida con funda: `content/images/blog/mantenimiento-tumbona-piscina-cubierta-20260629.png`.
- Se reaplico solo esa guia con `--only guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada`.
- Verificado en publico: `og:image`, `Article.image`, imagen visible y alt descriptivo.

### Siguiente paso recomendado
- Mantener estas guias sin mas cambios unos dias para que Google recrawlee contenido, enlaces e imagenes.

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
