# Muebles Exterior — Documento de Proyecto

> Registro completo del proyecto: contexto, decisiones, historial de trabajo y estado actual.
> Útil como briefing para agentes de IA o nuevas sesiones de trabajo.

---

## 1. Resumen Ejecutivo

Tienda Shopify multi-proveedor de mobiliario de exterior (terrazas, jardines, hostelería).
Actualmente en construcción y protegida con contraseña de Shopify.

| Campo | Valor |
|-------|-------|
| Tienda | mueblesexterior.myshopify.com |
| Modelo de negocio | B2B + B2C |
| Proveedores activos | Hevea, Balliu |
| Estado | En construcción |
| Región / Mercado | España |

---

## 2. Stack Técnico

### Shopify
- **API:** Admin GraphQL API 2026-01 (`/admin/api/2026-01/graphql.json`)
- **Autenticación:** OAuth 2.0 vía Partner Dashboard (las Custom/Private Apps quedaron obsoletas a partir de 2026)
- **App:** `API-Products`, client_id `b29216aed8d9ba73423c54a8828cf65d`, configurada en `shopify.app.toml`
- **Distribución:** Distribución personalizada (no pública), enlace de instalación generado desde Partner Dashboard → Distribución
- **Token:** `[REDACTED_VER_ENV_LOCAL]` (guardado en `.env.local`)
- **Scopes usados:** `read_products`, `write_products`, `read_files`, `write_files`

### Scripts Python
- **Intérprete:** `/usr/bin/python3` (Python 3.9.6 del sistema). **NO usar el virtualenv** (Python 3.13 de pyenv tiene módulo `_lzma` roto).
- **Dependencias:** solo librería estándar (`json`, `urllib`, `csv`, `time`, `pathlib`, `re`)

### Herramientas externas
- **remove.bg** API key `[REDACTED_VER_ENV_LOCAL]` — eliminación de fondo. Límite: 50 créditos/mes (plan gratuito). Rate limit: ~12 req seguidas → `sleep(3)` entre peticiones.
- **Hugging Face** token `[REDACTED_VER_ENV_LOCAL]` — generación de imágenes con FLUX.1-schnell (endpoint: `https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell`)

---

## 3. Proveedores

### Hevea
- **Origen del catálogo:** CSV con 116 productos recibido del proveedor
- **Estado:** ✅ 116 productos importados en Shopify con imágenes
- **Imágenes:** 49 imágenes optimizadas en `images_optimized/` (~0.3 MB c/u)
- **Cutouts (fondos eliminados):** 48 PNGs con fondo transparente en `images_cutout/`
  - 31 calificados como `completo` (producto bien recortado)
  - 14 calificados como `recortado` (producto toca el borde de la imagen original)
  - Estado detallado en `cutout_status.json`

### Balliu
- **Origen del catálogo:** Web `balliuexport.com` (no había CSV ni PDF con imágenes)
- **Estado:** ✅ 165 productos en Shopify | 🔄 Galerías de imágenes en curso
- **Catálogo v1:** `balliu_catalog.json` — 97 productos, ~5 imgs/producto (original)
- **Catálogo v2:** `balliu_catalog_full.json` — 97 productos, **498 imágenes** totales (todas las del carrusel WooCommerce, extraídas con `data-large_image`)
- **Imágenes en Shopify (estado actual):**
  - 66 productos: 1 imagen subida (upload_balliu_images.py, fase 6)
  - 99 productos: imágenes del CSV original (1 imagen cada uno)
  - Todos tienen solo 1 imagen — galería completa pendiente (fase 7)
- **Mapeo inteligente:** `balliu_smart_mapping.json`
  - Hash en handle Shopify → SKU en CSV → variante (Individual/Doble/Triple)
  - Variante → imagen específica por tamaño (ej. etna-1p, etna-2p, etna-3p)
  - Estado: 66/165 con galería mapeada. Pendiente actualizar para cubrir los 165

---

## 4. Convenciones de Producto

- **Títulos SEO descriptivos** sin nombres de colección del proveedor ni nombres propios de la marca.
  Ejemplo: `Sillón exterior aluminio · estilo envolvente | 98×90 cm`
- **Proveedor (`vendor`):** Siempre `"Muebles Exterior"` — nunca Hevea, Balliu, etc.
- **Precios con IVA 21% incluido** — Shopify configurado con "incluir impuesto en precio".
- **Variantes de color/tamaño:** Cuando un mismo diseño tiene SKUs separados por color o tamaño significativo, agruparlos como variantes Shopify (no como productos independientes).
  - **Excepción revisada:** Mesa Córcega sí se consolidó (dos tamaños del mismo diseño). Mesa Mundra NO (una es redonda, la otra rectangular).

---

## 5. Historial de Trabajo

### Fase 1 — Importación del catálogo Hevea
- Recepción del CSV de Hevea con 116 productos
- Conversión al formato Shopify con `convert_to_shopify.py`
- Importación manual vía CSV en el Admin de Shopify
- Subida de 49 imágenes optimizadas con `upload_images.py` (staged upload → S3 multipart → `productCreateMedia`)

### Fase 2 — Acceso a la API de Shopify (resolución del problema de 2026)
**Problema:** A partir de 2026, Shopify eliminó las "Custom Apps" desde el Admin y las "Private Apps". Intentar instalar una app sin método de distribución configurado devolvía el error *"Esta app no se puede instalar todavía"*.

**Solución:**
1. Crear app en Partner Dashboard → Apps → Crear app manualmente
2. Configurar URL `http://localhost:3000`, callback, scopes
3. Ir a **Partner Dashboard → Distribución → Distribución personalizada** → introducir el dominio de la tienda → generar enlace de instalación
4. Abrir el enlace de instalación en el navegador → autorizar → el servidor OAuth local (`get_shopify_token.mjs`) captura el token
5. Guardar el token en `.env.local`

Ver guía completa en `docs/shopify-api-setup.md`.

### Fase 3 — Eliminación de fondos (remove.bg)
- Procesadas 48 imágenes Hevea con la API de remove.bg
- Guardadas en `images_cutout/` como PNGs con transparencia
- Estado registrado en `cutout_status.json` (completo / recortado / error)
- Coste: ~48 créditos del plan gratuito (50/mes). Quedan ~2 créditos.

### Fase 4 — Imágenes lifestyle con IA (investigación, no implementado en producción)
Se investigaron tres enfoques para generar imágenes de ambiente:

| Enfoque | Resultado | Problema |
|---------|-----------|----------|
| Text-to-image (FLUX.1-schnell) | Genera ambiente pero sillón genérico | El producto generado no corresponde al real |
| Composite (cutout + fondo IA) | Producto correcto pero flotante | Sin sombras ni perspectiva integrada |
| **Inpainting (FLUX.1-Fill)** | **Correcto (mantiene producto, rellena fondo)** | **No disponible en tier gratuito de HF** |

**Estado actual:** 31 cutout PNGs listos para inpainting cuando se disponga del crédito (Replicate ~€1 por 31 imágenes, Stability AI, etc.).

**Lección técnica:** rembg con modelos BiRefNet/isnet crashea con OOM (exit code 144) en Mac con CPU. Solo u2net (176 MB) funciona, pero se usa remove.bg API para mejor calidad.

### Fase 5 — Revisión y consolidación de variantes
Revisión manual producto a producto de si había que consolidar variantes de color/tamaño:
- **Mesa Córcega:** Consolidada (dos tamaños del mismo diseño rectangular) ✅
- **Mesa Mundra:** Mantenida separada (redonda vs. rectangular) ✅
- **LOIRA rinconera:** Revisada — blanco/beige y gris como variantes de color (pendiente)
- **Resto:** Mantenidos como productos independientes

### Fase 6 — Catálogo Balliu (imágenes iniciales)
**Problema:** Balliu no tenía CSV con imágenes. Solo PDF de catálogo y web.

**Solución:** Scraping de `balliuexport.com`:
1. `extract_balliu_catalogs.py` → navegó 9 categorías → 97 URLs de producto únicas → extrajo primeras 5 imágenes por página → `balliu_catalog.json`
2. Script de matching cruzó los 68 productos Shopify sin imagen contra el catálogo Balliu → `balliu_image_mapping.json`
3. Mejora manual de matches de baja confianza (score=1):
   - Parasoles: de "base de parasol" → a imágenes de parasoles reales (Ágora, Ocean)
   - Mesas extensibles: → Mesa Atlanta
   - Mesas rectangulares grandes: → Mesa Altea
   - Mesas altas: → Mesa Capri alta
   - Tumbona → Weguard (caja de seguridad): descartado sin match
4. `upload_balliu_images.py` → descargó 18 imágenes únicas → staged upload a CDN Shopify → adjuntadas a 66 productos ✅

**Resultado:** 1 imagen por producto. El catálogo se veía pobre — cada producto tenía una sola foto genérica.

### Fase 7 — Galería completa Balliu + mapeo inteligente (en curso)
**Problema:** La fase 6 subió solo 1 imagen por producto. La web de Balliu tiene múltiples imágenes por producto (variantes de color y tamaño, fotos de detalle, lifestyle).

**Descubrimiento clave:** El scraper original usaba un regex genérico que en páginas con productos relacionados capturaba hasta 100 imágenes incorrectas. La forma correcta es usar el atributo `data-large_image` del HTML — son exactamente los items del carrusel de galería de WooCommerce.

**Trabajo realizado:**
1. **Re-scraping correcto** (`balliu_full_images.py --scrape-only --rescrape`):
   - Usa `data-large_image` para extraer solo las imágenes del producto, no relacionados
   - 97 productos scrapeados → 498 imágenes únicas → `balliu_catalog_full.json`
   - Ejemplo `sofa-etna`: ahora tiene 11 imágenes (individual/doble/triple × blanco-gris/aluminio-gris + lifestyle)

2. **Mapeo inteligente parcial** (`balliu_full_images.py --remap`):
   - El hash al final del handle Shopify (`...674ab9a1`) coincide con el hash del SKU en el CSV
   - Ejemplo: `BALLIU_ETNA_SOFA_INDIVIDUAL_ACRIL_674AB9A1` → hash `674ab9a1` → "Individual Acrílico"
   - Con ese dato, busca en `balliu_catalog_full.json` la imagen cuyo filename contiene "1p" o "individual"
   - Resultado actual: 66/165 productos mapeados (solo los que ya estaban en `balliu_image_mapping.json`)
   - **Pendiente:** actualizar `build_smart_mapping` para usar `CSV_HANDLE_TO_SLUG` (ya definido en el script) y cubrir los 165 productos totales

3. **Tabla `CSV_HANDLE_TO_SLUG`** (69 entradas), ejemplos:
   - `etna-sofa` → `sofa-etna`
   - `etna-tumbona` → `tumbona-de-aluminio-etna`
   - `capri-mesa` → `mesa-de-aluminio-capri`
   - 7 handles sin match en catálogo: `aura-cama-balinesa`, `alma-cama-balinesa`, `greta-silla`, `greta-mesa`, `sofia-mesa`, `cojin-40x40`, `alba-tumbona`

**Archivos generados:**
- `balliu_catalog_full.json` — 97 productos, 498 imágenes (reemplaza `balliu_catalog.json`)
- `balliu_smart_mapping.json` — 165 productos, 66 con galería (parcial, hay que regenerar)
- `balliu_full_images.py` — script completo: rescrape + mapeo + descarga + subida

**Siguiente paso inmediato:**
```python
# En build_smart_mapping(), sustituir la línea:
balliu_slug = slug_lookup.get(pid)
# Por:
csv_handle, variant_opt = hash_to_variant.get(hash_val, ("", ""))
balliu_slug = CSV_HANDLE_TO_SLUG.get(csv_handle)
# Y eliminar la dependencia de slug_lookup (balliu_image_mapping.json)
```
Tras ese cambio, ejecutar: `python3 balliu_full_images.py --remap` y luego sin flags para descargar y subir.

---

## 6. Errores Conocidos y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| "Esta app no se puede instalar todavía" | Sin método de distribución en Partner Dashboard | Configurar Distribución personalizada → generar enlace |
| `options` field not in `ProductInput` | API 2026-01 eliminó `options` de `productUpdate` | Usar mutación `productOptionsCreate` separada |
| `sku` not in `ProductVariantsBulkInput` | Campo eliminado | Usar `inventoryItem: {sku: "..."}` |
| `variantStrategy: "LEAVE_EXISTING_VARIANTS_AS_IS"` invalid | Valor incorrecto | Usar `"LEAVE_AS_IS"` |
| rembg exit code 144 (OOM) | Modelos BiRefNet/isnet demasiado grandes (973 MB / 179 MB) | Usar remove.bg API en su lugar |
| Python `_lzma` not found | pyenv Python 3.13 con lzma roto en el virtualenv | Usar `/usr/bin/python3` (system 3.9.6) |
| remove.bg 429 rate limit | ~12 requests seguidas | Añadir `time.sleep(3)` entre peticiones |
| FLUX.1-schnell 410 Gone | Endpoint antiguo deprecado | Nuevo endpoint: `router.huggingface.co/hf-inference/models/...` |
| CSV parser JS rompe en campos HTML multilínea | Campos con saltos de línea dentro de comillas | Usar módulo `csv` de Python en lugar de JS |

---

## 7. Estructura de Archivos

```
Muebles-Exterior/
│
├── .env.local                          # Tokens API (Shopify, HF, remove.bg)
├── shopify.app.toml                    # Config app Shopify Partner
├── package.json
│
├── docs/
│   └── shopify-api-setup.md            # Guía completa conexión API Shopify 2026
│
├── proveedores_raw/                    # Catálogos originales de los proveedores
│
├── images_optimized/                   # 49 imágenes Hevea comprimidas (~0.3 MB c/u)
├── images_balliu/                      # Imágenes Balliu descargadas (18 iniciales + más)
├── images_cutout/                      # 48 PNGs Hevea con fondo eliminado (remove.bg)
├── images_lifestyle/                   # Imágenes de ambiente (generación IA — futuro)
├── imgs-downloader-extension/          # Imágenes descargadas manualmente con extensión
│
├── shopify_products.csv                # CSV Hevea original (importado en Shopify)
├── shopify_products_optimized.csv      # CSV Hevea con rutas de imágenes optimizadas
├── balliu_shopify_products.csv         # CSV Balliu preparado para importar
├── balliu_catalog.json                 # Catálogo Balliu v1 (5 imgs/producto, original)
├── balliu_catalog_full.json            # Catálogo Balliu v2 (todas las imgs, data-large_image)
├── balliu_extraction_report.json       # Reporte del scraping inicial
├── balliu_image_mapping.json           # Mapeo 1ª imagen Shopify → img Balliu (67/68)
├── balliu_smart_mapping.json           # Mapeo inteligente: galería completa + var. (parcial)
├── cutout_status.json                  # Estado cutouts: completo/recortado/error
├── shopify_sync_report.csv             # Reporte de sincronización con Shopify
│
├── convert_to_shopify.py               # Convierte CSV proveedor → formato Shopify
├── optimize_images.py                  # Comprime imágenes (hasta 20 MB → ~0.3 MB)
├── extract_balliu_catalogs.py          # Scraping web Balliu → balliu_catalog.json
├── sync_shopify_catalog.py             # Sincroniza catálogo con Shopify via API
├── upload_images.py                    # Sube imágenes Hevea a Shopify (GraphQL staged upload)
├── upload_balliu_images.py             # Subida inicial: 1 imagen por producto Balliu
├── balliu_full_images.py               # Subida completa: galería + mapeo inteligente
├── generate_lifestyle_images.py        # Genera imágenes ambiente con IA (investigación)
│
└── get_shopify_token.mjs               # Servidor OAuth local para obtener token
```

---

## 8. API de Shopify — Referencia Rápida

```
Endpoint: https://mueblesexterior.myshopify.com/admin/api/2026-01/graphql.json
Header:   X-Shopify-Access-Token: [REDACTED_VER_ENV_LOCAL]
```

### Flujo de subida de imágenes
1. `stagedUploadsCreate` → obtiene URL de S3 + parámetros
2. POST multipart a S3 → devuelve `resourceUrl` (CDN Shopify)
3. `productCreateMedia(productId, media: [{originalSource: cdn_url}])` → adjunta al producto

### Mutaciones frecuentes
- `productUpdate` — actualizar campos (título, descripción, precio, etc.)
- `productOptionsCreate(productId, options, variantStrategy: "LEAVE_AS_IS")` — añadir opciones/variantes
- `productVariantsBulkCreate(productId, variants: [{inventoryItem: {sku: "..."}}])` — crear variantes

---

## 9. Flujo de Trabajo por Proveedor

```
1. Recibir catálogo (PDF / XLS / CSV / Web)
       ↓
2. Extraer datos → JSON/CSV normalizado
   (extract_balliu_catalogs.py / convert_to_shopify.py)
       ↓
3. Importar productos en Shopify
   (sync_shopify_catalog.py o importación CSV manual)
       ↓
4. Optimizar imágenes del proveedor
   (optimize_images.py) → images_optimized/
       ↓
5. [Opcional] Eliminar fondo (cutout)
   (remove.bg API, 50/mes gratis) → images_cutout/
       ↓
6. [Opcional] Generar imágenes de ambiente con IA
   (inpainting FLUX.1-Fill o similar) → images_lifestyle/
       ↓
7. Subir imágenes a CDN Shopify y adjuntarlas a productos
   (upload_images.py / upload_balliu_images.py)
```

---

## 10. Tareas Pendientes

### Inmediato (Fase 7 — Galería Balliu)
- [ ] **Completar `build_smart_mapping()`** en `balliu_full_images.py`:
  - Cambiar `balliu_slug = slug_lookup.get(pid)` por `csv_handle, _ = hash_to_variant.get(hash_val, ("",""))` + `balliu_slug = CSV_HANDLE_TO_SLUG.get(csv_handle)`
  - Tras el cambio: 165 productos cubiertos (vs. 66 actuales)
- [ ] **Ejecutar `python3 balliu_full_images.py --remap`** para regenerar `balliu_smart_mapping.json`
- [ ] **Ejecutar `python3 balliu_full_images.py`** para descargar (~84 imágenes únicas) y subir galerías

### Alta prioridad
- [ ] **Consolidar variantes Balliu:** Productos con mismo diseño y distinto tamaño/color están como productos separados. Ejemplo: "Sofá exterior 3 plazas · estilo contemporáneo | 77 cm" aparece 3 veces (Individual / Doble / Triple Acrílico) — deberían ser variantes de 1 producto
- [ ] **Colecciones / navegación:** Ninguna colección configurada (por tipo: tumbonas, sillas, mesas, sofás, parasoles, accesorios)
- [ ] **B2B pricing:** App "Wholesale Pricing Discount B2B" + customer tag `wholesale` — no configurada

### Media prioridad
- [ ] **Lifestyle images (inpainting):** 31 cutout PNGs listos en `images_cutout/`. Necesita FLUX.1-Fill (Replicate ~€1 para 31 imgs) o Stability AI
- [ ] **Remove.bg mes siguiente:** 67 productos Hevea restantes sin cutout. Se pueden procesar en lotes de 50 cada mes
- [ ] **7 handles Balliu sin catálogo:** `aura-cama-balinesa`, `alma-cama-balinesa`, `greta-silla`, `greta-mesa`, `sofia-mesa`, `cojin-40x40`, `alba-tumbona` — no encontrados en la web scrapeada

### Baja prioridad
- [ ] **Dominio propio:** Configurar dominio personalizado y lanzar tienda
- [ ] **Variantes de color pendientes:** Revisar línea LOIRA (rinconera blanco/beige vs. gris)
- [ ] **Rotar CLIENT_SECRET:** El secreto fue expuesto y eliminado, rotarlo en Partner Dashboard

---

## 11. Contexto para Otros Agentes de IA

### Lo que ya está hecho
- 116 productos Hevea importados con imágenes
- 165 productos Balliu en Shopify, todos con al menos 1 imagen
- Catálogo Balliu completo scrapeado: 97 productos, 498 imágenes → `balliu_catalog_full.json`
- Sistema de subida de imágenes via GraphQL completamente funcional
- Mapeo hash SKU → variante (individual/doble/triple) → imagen específica por tamaño implementado
- `balliu_full_images.py` listo para ejecutar (solo falta 1 línea de cambio en `build_smart_mapping`)

### Restricciones importantes
- **No exponer nombres de proveedor** en títulos, descripciones ni metadatos de producto
- **Usar `/usr/bin/python3`** (no python3 del virtualenv, que tiene lzma roto)
- **API Shopify 2026-01:** No usar campos deprecated (`options` en `productUpdate`, `sku` directo en variante)

### Cómo añadir un nuevo proveedor
1. Conseguir catálogo (CSV, PDF o web)
2. Normalizar a formato Shopify (ver `convert_to_shopify.py` como referencia)
3. Importar via `sync_shopify_catalog.py` o CSV manual
4. Obtener imágenes y subirlas con `upload_images.py`
5. Revisar candidatos a consolidación de variantes

### Cómo reutilizar la app de Shopify con otra tienda
Ver `docs/shopify-api-setup.md`. Pasos clave:
1. Crear nueva app en Partner Dashboard (o usar la misma y añadir distribución personalizada a la nueva tienda)
2. Generar nuevo enlace de instalación desde Distribución personalizada
3. Correr `get_shopify_token.mjs` localmente para capturar el nuevo token OAuth
4. Guardar el nuevo token en `.env.local`
