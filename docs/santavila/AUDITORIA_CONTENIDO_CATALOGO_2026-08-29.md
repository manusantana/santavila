# Auditoría de contenido del catálogo — 2026-08-29

> Alcance: los 171 productos ACTIVE de mueblesexterior.myshopify.com (70 DRAFT excluidos).
> Fuente: `scripts/audit_contenido_catalogo_20260829.py` (solo lectura) → `content/descriptions/auditoria_contenido_2026-08-29.csv`.
> Complementa (no sustituye) a `AUDITORIA_IMAGENES.md`, `AUDITORIA_FIDELIDAD_2026-07-29.md` y `_auditoria_galerias.json` del compañero,
> que cubren la CALIDAD visual de las galerías IA. Aquí se mide el CONTENIDO textual y de accesibilidad/SEO de las fichas.

## 1. Resumen ejecutivo

| Área | Estado | Veredicto |
|---|---|---|
| Descripciones | 100% ≥80 palabras; 87% en 120-199; 94% con H2; 100% con lista | ✅ Resuelto (PDP 2.0, jun-ago) |
| Meta descriptions | 98% → **100%** tras restaurar 4 borradas por error el 3-ago; 32 superan 160 chars | 🟡 Recorte pendiente (menor) |
| Títulos | 91% siguen la convención `modelo · medida · nombre`; **20 superan 70 chars** (sets y rinconeras con sufijos `2/3/4/5`); 1 duplicado exacto | 🟡 Lote concreto de 21 fichas |
| SEO title propio | 23% (40) — el resto usa el título de producto (válido si ≤60-70 chars) | 🟢 Solo donde el título es largo |
| **Alt de imágenes** | **372 de 826 imágenes SIN alt (45%)** — 364 son de Balliu (98%) · 57 productos afectados · 20 imágenes destacadas sin alt (19 Balliu) | 🔴 El hueco principal |
| Resolución de imágenes | 184 imágenes <1000 px (22%) — 182 de Balliu (fotos de proveedor, máx. 1.119 px según su catálogo) | 🔴 Ligado al plan de regeneración Balliu del compañero |
| GTIN / barcode | 0% en todo el catálogo | 🟡 No bloquea Merchant hoy; pedir EANs a proveedores |
| Taxonomía | 21 tipos, 0 sin tipo/vendor/tags; vendors Hevea 111 · Balliu 60 | ✅ |
| Handles | 60 con sufijo hash (`-aca076ae`) | ⚪ Cosmético; no tocar (redirecciones, señales GSC ya acumuladas) |

**Lectura:** el trabajo de texto (descripciones, metas, tipos) está hecho. Lo que queda es **casi todo Balliu y casi todo imagen**: alt vacíos y fotos de proveedor pequeñas. Hevea (111 fichas, galerías IA del compañero) está prácticamente impecable: alts descriptivos y ricos ("Sillón gris en una azotea del Madrid antiguo, con parapeto encalado…").

## 2. Hallazgos en detalle

### 2.1 Alt de imágenes (prioridad 1)
- 372 imágenes sin alt; por vendor: Balliu 364 · Hevea 8. Por tipo: Mesa 153 · Tumbona 75 · Silla 63 · Parasol 27 · Sofá 24 · Mini tumbona 15.
- Peores fichas: mesas aluminio 80×80 y 70×70 (24 de 25 imágenes sin alt cada una), sofás 3 plazas aluminio (13/14 y 11/12), sillas resina (11/12, 10/11), tumbona aluminio Etna (11/11).
- No hay alts "basura" (0 con <15 chars, 3 tipo nombre de fichero): el problema es ausencia, no calidad.
- Causa: son las fotos del proveedor Balliu subidas en la migración; nadie les puso alt. Las galerías IA sí lo llevan (el `publicar_galeria_producto.py` lo escribe).

### 2.2 Títulos (prioridad 2)
- 20 títulos >70 chars, todos del mismo patrón: `Set jardín 3 plazas · contemporáneo | sofá 3 plazas + 2 sillones + mesa 4`. Dos problemas: el **sufijo numérico `2/3/4/5` es visible** (es un desambiguador, no un nombre) y el pipe `|` con la enumeración duplica lo que ya dice el nombre. Google los trunca en SERP y en el feed de Merchant.
  - Propuesta de patrón: `Set jardín 3 plazas · contemporáneo · <Modelo>` (≤60 chars) — los modelos existen (Albania, Odín, Dounvil, Bolonia…: aparecen en los nombres de archivo de sus fotos) y el compañero ya los conoce por su trabajo de fidelidad.
- 1 duplicado exacto: `Reposapiés exterior · 85×50×43 cm` en `reposapies-exterior-855043-cm` y `…-cm-2` (3 y 2 imágenes, 145 y 142 palabras). O son el mismo producto (→ fusionar y redirigir) o difieren en color/tejido (→ diferenciar en el título).
- 5 títulos <25 chars: revisar si son descriptivos (p. ej. "Tumbona de exterior").

### 2.3 Metas (prioridad 3)
- 32 metas >160 chars → Google las corta. Recorte programático a ≤155 en límite de frase (backup previo). Trivial.
- Las 4 que faltaban (pérgola, base 25 kg, sofás 120/130) las borré yo el 3-ago al fijar `seo.title` sin `description` — **restauradas hoy** desde backup. Lección: `productUpdate.seo` sustituye el objeto entero; enviar siempre ambos campos.

### 2.4 Imágenes pequeñas (prioridad ligada al plan Balliu)
- 182 de 184 imágenes <1000 px son de Balliu. Coincide con el diagnóstico del compañero (25-ago): el catálogo Balliu no tiene fotos mejores; o se regeneran (plan C: 50 fichas, ~412 créditos) o se piden en alta al proveedor (lo primero que intentar, gratis).

## 3. Plan priorizado (quién / esfuerzo)

| # | Acción | Quién | Esfuerzo | Efecto |
|---|---|---|---|---|
| 1 | **Alt baseline programático para las 372 imágenes vacías**: `"<Título del producto> — <tipo de toma>"` inferido del nombre de archivo (ambiente/detalle/vista N) + color si aparece en el fichero. Backup + script idempotente. Se sobreescribe luego con alts artesanales cuando el compañero regenere cada galería. | Claude | 1 h | Cierra el 45% de alts vacíos hoy; accesibilidad + Google Imágenes + Merchant |
| 2 | Recortar las 32 metas >160 chars | Claude | 15 min | Snippets completos en SERP |
| 3 | Retitular los 21 sets/rinconeras con nombre de modelo (≤60 chars) + resolver el reposapiés duplicado | Compañero (conoce modelos) con script de Claude | 1-2 h | SERP, feed y coherencia de marca |
| 4 | Pedir a Balliu fotos en alta + lista de EAN (un solo email) | Dueño | 10 min | Desbloquea resolución sin gastar créditos y el GTIN |
| 5 | Regeneración de galerías Balliu (plan C del compañero, ~412 cr tras la renovación del 5-sep) | Compañero | semanas | Resolución + alts artesanales + fidelidad |
| 6 | Limpieza de los 70 DRAFT (9 mesas duplicadas, residuo de consolidación) | Claude tras OK del dueño | 15 min | Higiene del admin |

Regla de coordinación: el **auditor del compañero** (`auditar_galerias.py`) manda sobre calidad visual y alts de galerías IA; los alts baseline de esta auditoría solo rellenan huecos y deben marcarse como reemplazables (sufijo no visible no existe en alt → se registran en `content/descriptions/alt_baseline_<fecha>.json` para poder distinguirlos).
