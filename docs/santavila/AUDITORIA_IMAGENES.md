# Auditoría de imágenes — Santavila (producto ↔ imagen)

> Fecha: 2026-06-18 · Solo lectura, no se modificó Shopify ni archivos locales.
> Método en 3 capas: (1) estado **live** de imágenes por producto vía Admin API; (2) **cruce determinista** archivo↔producto; (3) **inspección visual** de 161 imágenes por agentes que las vieron de verdad.
> Datos reproducibles: `auditoria_imagenes.py` → `_estado_imagenes.json`, `auditoria_imagenes_report.csv`, `auditoria_imagenes_orphans.csv`. Inspección visual → `_visual_imagenes.json`.

---

## 1. Resumen ejecutivo

- **La asociación imagen↔producto está prácticamente resuelta.** De 409 imágenes locales de producto, **352 ya están subidas** (se identifican por el nombre de archivo en el CDN de Shopify → certeza de a qué producto pertenecen), **45** recortes mapean exacto por *handle*, **6** Balliu por catálogo; solo **6 huérfanas** reales.
- **El problema no es "asignar imágenes", son tres carencias de calidad:**
  1. **Cantidad en Hevea** — **87 de 115** productos Hevea tienen **una sola foto**. (Balliu ya va sobrado: media 8 img/producto.)
  2. **Resolución** — **45% del material es ≤800px**; los recortes (`images_cutout`) están **todos** por debajo del umbral premium (≈500px).
  3. **Coherencia e integridad** — fondos mezclados (estudio gris / blanco / lifestyle), ~25% de imágenes que no encajan limpio con su ficha (sobre todo fotos de *detalle* usadas mal y solapamiento de sets 2↔3 plazas), y 4 imágenes con logo de tercero.
- **Ningún producto ACTIVO está vacío**: los 12 sin foto son DRAFT (10 son de marca propia "santavila", aún sin terminar). La tienda pública está cubierta de mínimos.
- **Buena noticia inesperada:** la *calidad fotográfica* de Hevea es alta (76% de su muestra es apta para catálogo premium). El cuello de botella de Hevea es **cuántas** fotos hay, no cómo son.

---

## 2. Inventario (qué tenemos)

**243 productos vivos** → Hevea 115 · Balliu 114 · santavila (marca propia) 14.

**409 imágenes locales de producto** en 5 carpetas:

| Carpeta | Nº | Qué es | Esquema de nombre |
|---|---|---|---|
| `images_balliu/` (+`nuevas`) | 306 (+4) | Catálogo Balliu (proveedor) | `CÓDIGO-NOMBRE` (`260-COLCHONETA`) o composición |
| `images_optimized/` | 49 | Hevea, optimizadas | `TIMESTAMP_NOMBRE-N` (`1739541476_BRANDON-7`) |
| `images_cutout/` | 45 | Recortes PNG (fondo quitado) | por *handle* (`sillon-exterior-…`) |
| `images_lifestyle/` | 5 | Experimentos de recorte/ambiente IA | `damasco_rmbg`, `brandon_set_cutout` |

**No-producto (fuera de alcance):** `imagen-corporativa` 6 (logos), `design_handoff_shopify_theme/assets` 9 (tema), `imgs-downloader-extension` 12 (extensión).

**Activos de mapeo que ya existían:** `balliu_smart_mapping.json` (137: handle↔slug↔galería), `balliu_catalog.json` (97 slugs con URLs), `balliu_image_mapping.json` (67), `auditoria_fichas_report.csv`.

---

## 3. Asociación imagen ↔ producto (el objetivo)

| Método | Imágenes | Fiabilidad |
|---|---|---|
| **CDN live** (nombre de archivo presente en la galería viva del producto) | 352 | Certeza |
| **Handle exacto** (recortes nombrados por handle) | 45 | Certeza |
| **Catálogo/slug Balliu** | 6 | Alta |
| **Sin asociar (huérfanas)** | 6 | — |

Las 6 huérfanas: 1 Balliu (`Silla-Etna-Tortola-…-sin-fondo2.jpg`) + 5 experimentos `lifestyle` de "damasco" (R&D de quitar fondo, no aptas tal cual).
→ **Entregable:** `auditoria_imagenes_report.csv` (una fila por producto: vendor, tipo, nº imágenes live, nº imágenes locales asociadas, rutas).

---

## 4. Cobertura de galería (el hueco real)

Distribución del nº de imágenes por producto (estado **live** hoy):

| nº imágenes | productos |
|---|---|
| 0 | 12 (todos DRAFT) |
| **1** | **102** |
| 2 | 26 |
| 3–11 | 87 |
| 12+ (incl. 2 outliers de 64 y 85) | 16 |

**Por proveedor:**

| Proveedor | Productos | Media img/prod | Con 1 sola img | Con 0 |
|---|---|---|---|---|
| **Hevea** | 115 | **1,3** | **87** | 0 |
| Balliu | 114 | 8,0 | 11 | 2 (DRAFT) |
| santavila | 14 | 0,3 | 4 | 10 (DRAFT) |

**Lectura:** todo el déficit de galería es **Hevea** (87 fichas a una foto) + los productos de marca propia sin terminar. Balliu está cubierto e incluso con exceso/redundancia en 2 fichas.

---

## 5. Calidad visual (161 imágenes inspeccionadas de verdad)

Muestra: **100% de Hevea (49) y de cutout (45→40 válidas) y lifestyle (5)** + **muestra de Balliu (67 de ~310)**, incluidas las 2 galerías-outlier.

| Categoría | Insp. | Premium | Aceptable | Pobre | **Apta catálogo** | No encaja bien | Baja res |
|---|---|---|---|---|---|---|---|
| **Hevea** | 49 | 34 | 13 | 2 | **37 (76%)** | 3 | 3 |
| **Balliu** (muestra) | 67 | 36 | 25 | 6 | **31 (46%)** | 19 | 27 |
| **Cutout** | 40 | 0 | 21 | 19 | **0** | 14 | **40 (100%)** |
| **Lifestyle** | 5 | 2 | 1 | 2 | 2 | 5 | 2 |
| **TOTAL** | 161 | 72 | 60 | 29 | **70 (43%)** | 41 | 72 (45%) |

**Por categoría:**

- **Hevea — sólido.** Dos estilos: bodegón de estudio gris premium (ALBANIA, LEISA, CUPRA-7, yina, haston, dounvil) + lifestyle editorial de exterior (BRANDON-7, CUPRA-8). Calidad alta, nitidez y atrezzo profesional. Único pero: algún lifestyle "amateur" (samson fachada rosa, CARACAS jardín rústico) que sirve solo como secundaria, y panorámicas (ALBANIA_09 2000×903, DIVA_N24 banner) que dejan aire muerto como principal.
- **Balliu — a dos velocidades.** Lo bueno: lifestyle de estudio original (haston, dounvil, acapulco, manhatan, bellagio, odin) + packshots limpios sobre blanco = material premium. Lo bloqueado: **resolución baja sistemática** (800×614 de proveedor y recortes a 500px), **recortes sucios** (bordes dentados, halos, fragmentos de otros muebles) y **fallos de matching** (fotos de detalle de pata/base como principal, conjunto completo en ficha de "mesa de centro aislada", set 2 plazas en ficha de 3).
- **Cutout — archivos de trabajo, no entregables.** 0 aptos: **todos ≤~800px** (la mayoría 500×500). El recorte es decente pero la resolución los descalifica como imagen principal. Sirven de base, hay que re-exportarlos a ≥2000px desde el original.
- **Lifestyle — R&D.** 5 experimentos de quitar fondo a "damasco"/"brandon"; 100% sin producto asociado; 2 son duplicados del mismo sillón. Solo 1 activo limpio único.

**Defectos más frecuentes (sobre 161):** baja resolución 65 · recorte sucio 24 · render IA defectuoso 8 · **logo de tercero 4** (grabado "Balliu" en canto + camiseta "GUESS" en una modelo) · duplicada 2.

---

## 6. Integridad: las "41 que no encajan"

Matización importante — **no son 41 imágenes catastróficamente erróneas:**
- **~29 "dudoso"** = en su mayoría **fotos de detalle** (pie/pata de mesa Capri/Brunei, esquina de tablero) válidas como **secundaria** pero no como hero, y **solapamiento de sets 2↔3 plazas** que comparten foto.
- **6 `no_coincide`** = errores reales a corregir (p. ej. tumbona de madera en ficha de resina; pie de parasol que es una tumbona).
- **6 `sin_producto`** = los experimentos lifestyle.

→ Acción: revisar manualmente los `no_coincide` y reordenar las de detalle a posición secundaria.

---

## 7. Coherencia de marca

Fondos en la muestra: Hevea = estudio_gris 16 / lifestyle 27 / blanco 5 · Balliu = lifestyle 47 / blanco 19.
→ Conviven **tres sistemas visuales** (estudio gris, blanco puro, lifestyle de exterior). Para "la mejor tienda de decoración exterior del mundo" falta **un estándar único** (fondo, encuadre, ratio) que haga que Hevea y Balliu parezcan la misma tienda. Esto enlaza con el HOME, que aún espera **fotos de ambiente reales** (ver `IMAGENES_HOME_PENDIENTES.md`) — el ambiente/lifestyle es el activo de conversión que más falta.

---

## 8. Conclusiones → de qué va el proyecto

1. **Enriquecer Hevea** (87 fichas de 1 foto) — su pool de 49 imágenes ya es premium pero no alcanza para todos; habrá que generar/ampliar (variantes, ambiente, detalle).
2. **Subir resolución** — re-exportar Balliu y recortes a ≥2000px desde el origen (pedir alta al proveedor / re-render).
3. **Estandarizar** un sistema visual único (fondo + ratio + orden de galería) y aplicarlo.
4. **Limpiar integridad** — corregir los 6 `no_coincide`, reordenar las de detalle, quitar logos de tercero, deduplicar.
5. **Ambiente de marca** — producir lifestyle coherente (sirve a PDP y al HOME).

> Siguiente paso: priorizar estos 5 frentes y definir alcance/medios (proveedor vs. generación IA vs. foto real) → **planificación**.

---

## 9. Limpieza de base ejecutada (2026-06-19)

Antes del proyecto Higgsfield se cerró la integridad con lo que había:

- **Fotos de playa equivocadas eliminadas** (no mostraban el producto): `Lola_Mesita-Mini_playa2` (aérea) y `Mesa-auxiliar-Mini_Lola_Carmen_playa2` (hamacas) en `balliu-mesa-exterior-5d0fb586` (ACTIVE) y sus duplicadas en `balliu-mesa-exterior-1cf4d3d5` (DRAFT).
- **2 tumbonas reordenadas**: `balliu-tumbona-…-923110d9` y `…-b19af1ea` mostraban la **tela de repuesto** de portada → reordenadas para que la **tumbona real** (`eva-pro-blanco`) sea la principal.
- **"IA horribles": no existían.** Inspección directa de todos los candidatos IA marcados → de aceptables a premium. No se borró nada bueno (varias eran única foto).
- **Barrido completo** de las 255 imágenes principales de los 176 productos activos (listón estricto de "horrible") → solo **4 graves**; 2 arregladas, 2 sin fuente limpia.

### Cola de reemplazo Higgsfield (prioridad)
1. `silla-exterior-estilo-estilizado` — cutout reventado, **única foto** (no borrable). Sin original limpio.
2. `banco-de-exterior-150-cm` (gullivert) — cutout reventado, **única foto**. Sin original limpio.
3. `DIVA_N24` (set bicolor 3 plazas) — banner deforme + muestra 2 plazas, **única foto**.
4. `Capri-Quadrada2` — baja resolución (secundaria).
5. **Bucket grande:** 87 fichas Hevea con 1 sola imagen + subida de resolución del material ≤800px.
