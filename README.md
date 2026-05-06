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
│   ├── Santavila como líder de mobiliario...   # Posicionamiento de marca
│   └── The Perfect Product Page Builder.pdf    # Guía de fichas de producto
│
├── proveedores_raw/                 # Catálogos originales de los proveedores
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
