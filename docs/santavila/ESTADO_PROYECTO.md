# Santavila — Estado del proyecto (compactado)

> **Documento vivo**: foto completa del proyecto en una página. Actualizar al cierre de cada
> bloque grande; el detalle histórico sigue en `JOURNAL.md` (cronológico) y los informes fechados.
> Última actualización: **2026-09-15**.

## La tienda en una línea
Shopify `mueblesexterior.myshopify.com` → **santavila.com** · mobiliario de exterior (Hevea 111 + Balliu 60 productos ACTIVE) · idioma `es` · sin ventas aún: fase de visibilidad.

## Infraestructura y flujos (cómo se trabaja)
| Cosa | Estado / cómo |
|---|---|
| Tema | Git = fuente de verdad (`theme/`, repo `github.com/manusantana/santavila`). STAGING `189491151172` → validar → PROD `189222715716` solo con OK, vía `scripts/push_theme_assets.py` (token en `.env.local`). ⚠️ Sin integración GitHub↔Shopify (flujo por Asset API; los `.json` del editor son del compañero: parchear siempre sobre el live fresco) |
| Tokens API | Shopify: `.env` (productos/GraphQL) + `.env.local` (temas). Google (GSC+GA4+Merchant): `token.json` **permanente** desde 30-ago (consent screen en producción, proyecto GCP `santavila-muebles-exteriores`) |
| Metricool | blogId `6606564`, MCP vía mcp-remote (OAuth caduca ~1h, refresh automático en scripts; reconexión = `claude mcp add` + URL en texto plano SIN abrir navegador) |
| Higgsfield | Plan Plus 1.000 cr/mes (renovación ~día 5); presupuesto del compañero manda (~550 cr fichas Balliu) |
| Merchant Center | id `5781655181` · feed sano (imágenes de variante arregladas 3-ago; desaprobados restantes = envío BG/HR/MT, ignorados por decisión) · GTIN 0% (no bloquea) |

## Catálogo (texto ✅ · imagen Balliu ⏳)
- **171 ACTIVE al 100% en texto**: descripciones (todas ≥80p, 87% 120-199), metas (100%, ≤160), títulos (≤70 chars, con modelo Hevea en sets/rinconeras), alts (0 vacíos; 382 son *baseline* registrados en `content/descriptions/alt_baseline_20260829-080424.json`, reemplazables por los artesanales del compañero).
- **Pendiente = imagen Balliu**: 48 fichas con 184 fotos <1000px → lista y orden por señales GSC en `IMAGENES_BAJA_RESOLUCION_2026-08-29.md` (Lola → Eva RG → Noa → Atlanta → sofás 3p → reposapiés Standard XL con galería basura). Plan C del compañero (~412 cr).
- 70 DRAFT residuales (9 mesas duplicadas candidatas a borrar, falta OK del dueño).

## GEO / visibilidad
- **Hecho**: 10 guías citables (Article+FAQPage) · hub `/collections/tumbonas-de-resina` · landings de marca `/collections/balliu` y `/hevea` · llms.txt propio (con marcas y guías) · sameAs (4 perfiles) · schema Org/Breadcrumb/ItemList/FAQ · sitemap limpio · home dinámica (editorial = últimos 3 posts sola).
- **Métrica**: impresiones 28d: 692 (3-ago) → 866 → **1.040 (30-ago, +50% en el mes)**; clics 12→14; marca pos ~3-6; `muebles vigo` pos 4-6.
- **Clusters**: sombra ✅ (pérgola 13,1 y bajando) · sofás 120/130 ~12,8 · resina = mucha demanda (339 impr) pero pos 40-47 → cuello de botella de AUTORIDAD, no de contenido.
- **⏰ Delta GSC VENCIDO** (tocaba ~13-sep) → correr al retomar.
- **Siguiente guía decidida**: "Tumbonas de resina para piscinas comunitarias y hostelería" (query `…profesionales`, 76 impr).

## RRSS (Metricool)
- Agosto: 22 piezas publicadas (1 fallo el 4-ago, republicado). Sept cubierto **hasta el 19-sep** (guías pérgola/parasol, carruseles Sofás-por-España y Puertas-adentro, serie "El detalle", pins de colección). IG ~4/sem · Pinterest ~3/sem · IG tiene ~6K seguidores (el activo); Pinterest = siembra a meses.
- **Sin programar del 20-sep en adelante** → lote 4 pendiente (carrusel/pin landing Balliu + piezas de la próxima guía + reels ASMR si se aprueban créditos).

## Pendientes por persona
**Dueño (Manu):** renombrar filtros "Availability/Price" en app Search & Discovery → Disponibilidad/Precio · email Balliu/Hevea (listado como distribuidor + EAN; borrador en chat 30-ago) · GBP (falta móvil) · Pinterest: meta-tag dominio + 3 tableros · Bing Webmaster (importar de GSC) → avisar para IndexNow · cuentas Wikidata/LinkedIn · OK borrado 9 mesas DRAFT.
**Compañero (Sergio):** regeneración galerías Balliu según orden del traspaso (JOURNAL 29-ago) · reposapiés Standard XL prioritario · sobreescribir alts baseline al regenerar.
**Claude:** delta GSC (vencido) · escribir/programar guía resina profesional · lote 4 RRSS · vídeos ASMR PDP tras OK de créditos (5 candidatas elegidas) · IndexNow cuando haya Bing.

## Dónde está cada cosa
`JOURNAL.md` (historia) · `GEO-DELTA-*.md` (métricas) · `AUDITORIA_CONTENIDO_CATALOGO_2026-08-29.md` (catálogo) · `WORKFLOW_STAGING_PRODUCCION.md` (tema) · `GEO-SOCIAL-CONTENT-PACK.md` + `content/social/` (RRSS, URLs CDN en `cdn_urls.json`) · scripts idempotentes con backup en `scripts/` (backups en `content/descriptions/`).
