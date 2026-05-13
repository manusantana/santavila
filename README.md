# Muebles Exterior — Tienda Shopify

Tienda Shopify multi-proveedor de mobiliario de exterior (terrazas, jardines, hostelería).

- **Dominio:** mueblesexterior.myshopify.com
- **Modelo:** B2B + B2C (app "Wholesale Pricing Discount B2B", customer tag `wholesale`)
- **Estado:** En construcción (protegida con contraseña de Shopify)

---

## Proveedores

Estado verificado contra Shopify Admin API el 24 de abril de 2026.

| Proveedor | Estado | En Shopify (`vendor`) |
|-----------|--------|-----------------------|
| Hevea     | ✅ Importado | 115 productos |
| Balliu    | 🔄 Galerías y consolidación de variantes en curso | 137 productos |

Total catálogo: **252 productos** (248 `ACTIVE`, 4 `DRAFT`).

> Los nombres de colección del proveedor **no se exponen** en títulos ni descripciones de cara al cliente. El campo `vendor` interno de Shopify sí mantiene el nombre real (`Balliu` / `Hevea`) para poder filtrar y reportar por origen.

---

## Convenciones de producto

- **Títulos SEO descriptivos** sin nombres de colección del proveedor.
  Ejemplo: `Sillón exterior aluminio · estilo envolvente | 98×90 cm`
- **Precios con IVA 21% incluido** — Shopify configurado con "incluir impuesto en precio".
- Productos publicados como `active` (la contraseña de Shopify protege la tienda durante construcción).
- Variantes de color: cuando un mismo diseño tiene SKUs separados por color, agruparlos como variantes Shopify en vez de productos independientes (ej: LOIRA rinconera blanco/beige y gris).

---

## Estructura de archivos

```
Muebles-Exterior/
│
├── docs/
│   ├── shopify-api-setup.md                    # Guía para conectar Shopify Admin API
│   ├── santavila/                              # Auditoría, backlog, modelo de datos y plan de tema
│   ├── Santavila como líder de mobiliario...   # Posicionamiento de marca
│   └── The Perfect Product Page Builder.pdf    # Guía de fichas de producto
│
├── plan_santavila_shopify/          # Prompts maestros y plan operativo del proyecto Santavila
│
├── proveedores_raw/                 # Catálogos originales de los proveedores
│   ├── hevea/      *.csv (con prefijo YYYYMMDD) + _archived/
│   └── balliu/     *.pdf (con prefijo YYYYMMDD) + _archived/
│
├── images_optimized/                # 49 imágenes Hevea comprimidas (~0.3 MB c/u)
├── images_balliu/                   # Imágenes originales de Balliu
├── images_cutout/                   # Imágenes con fondo eliminado (cutout)
├── images_lifestyle/                # Imágenes de ambiente generadas con IA
│
├── shopify_products.csv             # CSV principal Hevea (importado en Shopify)
├── shopify_products_optimized.csv   # CSV Hevea con rutas de imágenes optimizadas
├── balliu_shopify_products.csv      # CSV Balliu preparado para importar
├── balliu_catalog.json              # Catálogo Balliu extraído (97 productos)
├── balliu_catalog_full.json         # Catálogo Balliu con galería completa (498 imágenes)
├── balliu_extraction_report.json    # Reporte de extracción Balliu
├── balliu_image_mapping.json        # Mapeo SKU → imagen Balliu
├── balliu_smart_mapping.json        # Mapeo handle Shopify → SKU → variante
├── cutout_status.json               # Estado del proceso de cutout de imágenes
├── shopify_sync_report.csv          # Reporte de sincronización con Shopify
├── Santavila.xlsx                   # Hoja maestra de tarifas consolidadas
│
├── convert_to_shopify.py            # Convierte CSV de proveedor al formato Shopify
├── optimize_images.py               # Comprime imágenes (hasta 20 MB → ~0.3 MB)
├── extract_balliu_catalogs.py       # Extrae catálogo de Balliu desde la web del proveedor
├── balliu_full_images.py            # Descarga la galería completa del carrusel Balliu
├── sync_shopify_catalog.py          # Sincroniza catálogo con Shopify via API
├── upload_images.py / .mjs          # Sube imágenes a Shopify Files (GraphQL)
├── upload_balliu_images.py          # Sube imágenes de Balliu
├── consolidate_variants.py          # Consolida productos duplicados como variantes (genérico)
├── consolidate_remaining.py         # Consolida grupos pendientes Balliu (vera, brunei, capri)
├── generate_lifestyle_images.py     # Genera imágenes de ambiente con IA (FLUX.1-schnell)
├── export_tarifas.py                # Genera XLSX con tarifas Hevea+Balliu (requiere openpyxl)
├── update_hevea_seguimiento.py      # Regenera hojas "Hevea Seguimiento" y "Hevea Histórico" desde CSVs fechados
├── update_balliu_seguimiento.py     # Regenera hojas "Balliu Seguimiento" y "Balliu Histórico" desde PDFs fechados
├── update_todos_principal.py        # Actualiza la hoja maestra "20260508 -Todos " con costes y PVPs actuales
├── sync_prices_to_shopify.py        # Sincroniza price + compareAtPrice + cost a Shopify con redondeo psicológico (dry-run por defecto)
├── setup_pnl_unit_economics.py      # Crea hojas P&L, Unit Economics, Escenarios marketing y Dashboard
├── upload_blogs.py                  # Sube artículos al blog "News" de la tienda
│
├── get_shopify_token.mjs            # Servidor OAuth para obtener token de acceso
├── shopify.app.toml                 # Configuración de la app de Shopify Partner
└── package.json                     # Incluye @shopify/cli como devDependency
```

---

## API de Shopify

Ver guía completa en [docs/shopify-api-setup.md](docs/shopify-api-setup.md).

Hay **dos rieles de acceso** que conviven en el repo:

1. **Scripts Python** (`sync_shopify_catalog.py`, `consolidate_remaining.py`, `export_tarifas.py`, `upload_blogs.py`, etc.) — usan el token Admin (`shpca_...` / `shpat_...`) leído de `.envlocal` (variable `SHOPIFY_ACCESS_TOKEN`) contra `/admin/api/2026-01/graphql.json` directamente con `urllib`.
2. **Shopify CLI + plugin oficial `shopify-ai-toolkit`** — autenticación OAuth gestionada por el CLI (sesión separada del token de `.envlocal`). Pensado para gestión interactiva desde el editor / chat.

Operaciones más frecuentes vía Admin GraphQL:
- Subir imágenes con `stagedUploadsCreate` + `productCreateMedia`
- Crear/actualizar productos y variantes (`productUpdate`, `productVariantsBulkCreate`, `productOptionUpdate`)
- Sincronizar catálogos y consolidar duplicados como variantes

### Shopify CLI

```bash
# Instalar (ya en devDependencies del proyecto)
npm i

# Autenticar contra la tienda (abre navegador)
shopify store auth --store mueblesexterior.myshopify.com \
  --scopes read_files,read_products,write_files,write_products

# Ejecutar GraphQL desde la línea de comandos
shopify store execute --store mueblesexterior.myshopify.com \
  --query 'query { shop { name id } }'
```

### Dependencias Python externas

La mayoría de scripts usan solo la librería estándar (`json`, `urllib`, `csv`, `pathlib`, `re`). Excepciones:

- `export_tarifas.py` requiere **`openpyxl`** (`pip install openpyxl`)
- `update_hevea_seguimiento.py` requiere **`openpyxl`**
- `update_balliu_seguimiento.py` requiere **`openpyxl`** + **`pdfplumber`** (`pip install pdfplumber`)

### Seguimiento de tarifas (Hevea + Balliu)

Cada tarifa nueva se guarda en `proveedores_raw/<proveedor>/` con prefijo de fecha `YYYYMMDD …` (Hevea CSV, Balliu PDF). Snapshots descartados se mueven a `proveedores_raw/<proveedor>/_archived/` — el script no los recoge pero quedan recuperables.

**Premisa de IVA**: ambos proveedores envían precios **sin IVA**. El IVA (×1,21) lo aplica el script para mostrar el PVP de cara al cliente.

```bash
# 1. Regenerar Hevea Seguimiento + Hevea Histórico
python3 update_hevea_seguimiento.py

# 2. Regenerar Balliu Seguimiento + Balliu Histórico
python3 update_balliu_seguimiento.py

# 3. Actualizar la hoja maestra 20260508 -Todos con costes y PVPs actuales
python3 update_todos_principal.py

# 4. (Opcional) Regenerar el modelo financiero (P&L, Unit Economics, Dashboard, etc.)
python3 setup_pnl_unit_economics.py

# 5. (Opcional) Sincronizar a Shopify — modo dry-run primero
python3 sync_prices_to_shopify.py
python3 sync_prices_to_shopify.py --apply --skip-price --skip-compare  # solo costes
python3 sync_prices_to_shopify.py --apply                              # price + compareAtPrice + cost
```

Los dos primeros scripts crean/regeneran dos hojas por proveedor en `Santavila.xlsx`:

- **`<Proveedor> Seguimiento`** — vista de control wide. Una fila por producto con identificación, fechas, estado, **Coste sin IVA**, **PVP rec. sin IVA**, **PVP con IVA** (= PVP × 1,21), **Margen €** (sin IVA, = PVP − Coste), **Margen %** (margen bruto sobre PVP), **Markup %** (sobre coste), deltas y mini-tendencia (`▁▂▃▄▅▆▇█`).
- **`<Proveedor> Histórico`** — formato long. Una fila por (producto, fecha [, tipo]) con todos los valores y deltas vs fecha anterior.

El tercer script actualiza la **hoja maestra `20260508 -Todos `** (sólo columnas E..I, las fórmulas K..N de Margen Real / Max CPA / ROAS / Anunciar se preservan).

Diferencias clave entre proveedores:

| | Hevea | Balliu |
|---|---|---|
| Fuente | CSV con SKU + Producto + Coste + PVP recomendado | PDF (dos tipos): Tarifa CLIENT (coste) y Tarifa PVP (recomendado) |
| Estructura del histórico | 1 serie temporal por SKU | 2 series por producto: tipo `COSTE` y tipo `PVP_RECOMENDADO` |
| Margen € | PVP del CSV − Coste del CSV (sin IVA) | PVP del PDF tipo "pvp" − Coste del PDF tipo "client" |
| Identificación | (SKU, primera palabra del Producto) | (Producto, Variante, Grupo, Ord) |
| Parser | `csv.DictReader` con detección flexible de cabeceras | `pdfplumber` con coordenadas X + agrupación por bloques |
| Cruce con SKU Shopify | directo por SKU | mapping persistido en `proveedores_raw/balliu/_sku_mapping.json` (cruce por coste de fila) |

Todos los scripts son **idempotentes** y **reversibles** (retira un snapshot del directorio y vuelve a ejecutar — desaparece). Las hojas `Todos`, `Hevea`, `Balliu` antiguas no se tocan. Detalle completo en [PROYECTO.md](PROYECTO.md#hevea).

### Modelo financiero (P&L, Unit Economics, Escenarios)

`setup_pnl_unit_economics.py` añade 6 hojas a `Santavila.xlsx` con un modelo de control financiero completo, sin tocar las hojas operativas:

- **`00_SUPUESTOS`** — variables editables (amarillo). Una fuente de verdad. Plan Shopify, comisiones, AOV, ROAS objetivos, tasas de devolución/incidencias, márgenes. Al cambiar un valor, todo el modelo recalcula.
- **`01_PNL_SANTAVILA`** — P&L mensual Conservador/Base/Optimista con break-even y CPA medio.
- **`02_UNIT_ECONOMICS_SKU`** — los 281 productos con margen contributivo €/%, CAC máximo, ROAS mínimo y categoría comercial (PUSH / NEUTRAL / WATCH / NO ANUNCIAR).
- **`03_ESCENARIOS_MARKETING`** — calculadora bidireccional: presupuesto ↔ ROAS objetivo.
- **`04_PRODUCTOS_PRIORIDAD`** — top 30 SKUs por margen contributivo €.
- **`05_DASHBOARD`** — vista resumen 1 página.

Detalle completo en [PROYECTO.md § 3.b](PROYECTO.md). Backup automático en `.backups/` antes de cada ejecución (gitignored).

### Sincronización con Shopify

`sync_prices_to_shopify.py` actualiza `price`, `compareAtPrice` y `cost_per_item` de las variantes Shopify desde la hoja maestra `20260508 -Todos `, vía Admin GraphQL API, aplicando redondeo psicológico por segmento de precio.

```bash
# Dry-run completo (genera sync_prices_report.csv, NO toca Shopify)
python3 sync_prices_to_shopify.py

# Aplicar sólo costes (no cambia precios visibles)
python3 sync_prices_to_shopify.py --apply --skip-price --skip-compare

# Aplicar a un solo producto (test)
python3 sync_prices_to_shopify.py --apply --only-handles balliu-parasol-...

# Aplicar todo (price + compareAtPrice + cost)
python3 sync_prices_to_shopify.py --apply
```

**Mapeo y reglas de redondeo** (segmentado por **price bruto**, no por coste):

| Segmento (price bruto) | `price` | `compareAtPrice` |
|---|---|---|
| < 50 €   | termina en .95 | bruto × 1.30, entero limpio (.00) |
| 50–500 € | termina en .95 — si cae en `[umbral, umbral×1.05]` baja a `umbral-0.10` (ej. 104→99.90) | bruto × 1.10 con mismo truco (`umbral-0.05`) |
| > 500 €  | sube al siguiente entero terminado en 0/5/9 | bruto × 1.10, número limpio (múltiplo de 100 > 50 > 25 > 10) dentro de `[price_psy×1.05, price_psy×1.12]` |

`inventoryItem.cost` se sincroniza sin redondear (es lo que se paga al proveedor).

- Cruce por (Handle, SKU). Bulk update con `productVariantsBulkUpdate`.
- Resolución automática de SKUs reusados por proveedor (Hevea: `557-010884`, `557-010147`, `557-1563` y similar para Balliu): elige la fila cuyo coste es más cercano al actual de Shopify.
- Throttle-aware (pausa preventiva si bucket < 200 puntos), reintentos con backoff y respeto de `Retry-After`.
- Reporte CSV con `price/compare/cost` antes-después por SKU (gitignored — contiene precios sensibles).

Estado **mayo 2026**: ✅ 270 variantes con `price`, `compareAtPrice` y `cost_per_item` sincronizados en Shopify aplicando la regla psicológica. PVP recomendado del Excel adoptado como fuente única de precio (incluido el PVP Balliu del proveedor). Suma agregada de prices: 200.711 € → 249.327 € (+24,2 %). Cierra la tarea `F0-01` del backlog. Detalle en [`docs/santavila/JOURNAL.md`](docs/santavila/JOURNAL.md).

---

## Flujo de trabajo por proveedor

```
1. Recibir catálogo del proveedor (PDF / XLS / CSV)
       ↓
2. Extraer datos → JSON/CSV normalizado
   (extract_balliu_catalogs.py / convert_to_shopify.py)
       ↓
3. Optimizar imágenes
   (optimize_images.py) → images_optimized/
       ↓
4. [Opcional] Eliminar fondo (cutout) → images_cutout/
       ↓
5. [Opcional] Generar imágenes de ambiente con IA → images_lifestyle/
       ↓
6. Subir imágenes a Shopify Files → obtener URLs CDN
   (upload_images.py / upload_balliu_images.py)
       ↓
7. Importar/sincronizar productos en Shopify
   (sync_shopify_catalog.py o importación CSV manual)
       ↓
8. Consolidar duplicados como variantes (cuando aplica)
   (consolidate_variants.py / consolidate_remaining.py)
       ↓
9. Reporting de tarifas y márgenes
   (export_tarifas.py → tarifas_consolidadas.xlsx)
```

El blog editorial de la tienda (`/blogs/news`) se gestiona aparte con `upload_blogs.py`.

---

## Pendientes

- [ ] Completar galería Balliu (fase 7): 99 productos con 1 sola imagen — galerías completas mapeadas en `balliu_catalog_full.json` (498 imágenes)
- [ ] Resolver 4 productos Balliu en `DRAFT` (parasol acrílico ×2, cojín exterior, limpiador) — los dos parasoles parecen duplicados
- [ ] Ejecutar `consolidate_remaining.py` para los grupos pendientes (vera-silla, brunei-mesa, capri-mesa redondas+cuadradas)
- [ ] Revisar productos candidatos a variantes de color (misma línea, diferentes SKUs por color)
- [ ] Generar imágenes lifestyle para productos sin contexto de ambiente
- [ ] Configurar dominio propio, retirar contraseña y lanzar tienda
