# Muebles Exterior — Tienda Shopify

Tienda Shopify multi-proveedor de mobiliario de exterior (terrazas, jardines, hostelería).

- **Dominio:** mueblesexterior.myshopify.com
- **Modelo:** B2B + B2C (app "Wholesale Pricing Discount B2B", customer tag `wholesale`)
- **Estado:** En construcción (protegida con contraseña de Shopify)

---

## Proveedores

| Proveedor | Estado | Productos importados |
|-----------|--------|----------------------|
| Hevea     | ✅ Importado | 116 productos |
| Balliu    | 🔄 En proceso | Ver `balliu_shopify_products.csv` |

> Los nombres de proveedor y colección **nunca se exponen** en títulos ni descripciones. Todos los productos usan `vendor = "Muebles Exterior"`.

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
│   └── shopify-api-setup.md        # Guía completa para conectar Shopify Admin API
│
├── proveedores_raw/                 # Catálogos originales de los proveedores
│
├── images_optimized/               # 49 imágenes Hevea comprimidas (~0.3 MB c/u)
├── images_balliu/                  # Imágenes originales de Balliu
├── images_cutout/                  # Imágenes con fondo eliminado (cutout)
├── images_lifestyle/               # Imágenes de ambiente generadas con IA
│
├── shopify_products.csv            # CSV principal Hevea (importado en Shopify)
├── shopify_products_optimized.csv  # CSV Hevea con rutas de imágenes optimizadas
├── balliu_shopify_products.csv     # CSV Balliu preparado para importar
├── balliu_catalog.json             # Catálogo Balliu extraído
├── balliu_extraction_report.json   # Reporte de extracción Balliu
├── balliu_image_mapping.json       # Mapeo de imágenes Balliu
├── cutout_status.json              # Estado del proceso de cutout de imágenes
├── shopify_sync_report.csv         # Reporte de sincronización con Shopify
│
├── convert_to_shopify.py           # Convierte CSV de proveedor al formato Shopify
├── optimize_images.py              # Comprime imágenes (hasta 20 MB → ~0.3 MB)
├── extract_balliu_catalogs.py      # Extrae catálogo de Balliu
├── sync_shopify_catalog.py         # Sincroniza catálogo con Shopify via API
├── upload_images.py / .mjs         # Sube imágenes a Shopify Files (GraphQL)
├── upload_balliu_images.py         # Sube imágenes de Balliu
├── generate_lifestyle_images.py    # Genera imágenes de ambiente con IA (DALL-E / similar)
│
├── get_shopify_token.mjs           # Servidor OAuth para obtener token de acceso
├── shopify.app.toml                # Configuración de la app de Shopify Partner
└── package.json
```

---

## API de Shopify

Ver guía completa en [docs/shopify-api-setup.md](docs/shopify-api-setup.md).

El token de acceso (`shpat_...`) se obtiene via OAuth desde Partner Dashboard.
Se usa la **Admin API GraphQL** (`/admin/api/2026-01/graphql.json`) para:
- Subir imágenes via `stagedUploadsCreate`
- Actualizar productos con URLs CDN
- Sincronizar catálogos

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
```

---

## Pendientes

- [ ] Finalizar importación catálogo Balliu
- [ ] Revisar productos candidatos a variantes de color (misma línea, diferentes SKUs por color)
- [ ] Completar subida de imágenes Hevea vía API
- [ ] Generar imágenes lifestyle para productos sin contexto de ambiente
- [ ] Configurar dominio propio y lanzar tienda
