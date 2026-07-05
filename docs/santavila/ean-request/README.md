# Petición de EAN a proveedores — Santavila · 2026-07-05

Los productos ACTIVE de Santavila **no tienen EAN/GTIN** (variant.barcode vacío al 100%).
El GTIN lo asigna el fabricante, así que hay que pedírselo a cada proveedor. Hay **dos**:

| Proveedor | Web | Productos ACTIVE | Variantes | Fichero |
|---|---|---:|---:|---|
| **Balliu** | balliuexport.com (WooCommerce) | 60 | 1351 | `peticion_ean_balliu.csv` |
| **Hevea** | (pendiente localizar) | 111 | 112 | `peticion_ean_hevea.csv` |

> La web de Balliu **no publica EAN** (solo SKU de modelo y códigos de artículo tipo
> `AUC/BL-96/07`). Por eso hay que pedir el listado comercial/tarifa con EAN a nivel variante.

## Cómo usar

1. Envía cada CSV a su proveedor pidiendo que rellenen la columna **`EAN_a_rellenar`**
   (EAN-13 por variante/color). Columnas de apoyo para que lo localicen:
   `modelo_fabricante`, `color_variante`, `ref_proveedor_guardada`, `sku_santavila`.
2. Cuando devuelvan el fichero, se cargan los EAN en `variant.barcode` con un script
   (mapeo por `sku_santavila` → barcode). Pendiente de crear al recibir los datos.

## Notas
- Los **conjuntos/sets** (34 productos: Conjunto sofá/rinconera, Banco con mesa) son bundles
  montados por Santavila → normalmente **no tienen EAN de fábrica**. Para esos, en Google
  Merchant se marca `identifier_exists: no` (no es un error).
- Balliu tiene explosión combinatoria (chasis × color) → 1351 variantes. Puede que Balliu solo
  asigne EAN a ciertas configuraciones; su listado lo aclarará.
- **Nunca** inventar ni scrapear EANs de bases de datos: un GTIN erróneo hace que Google
  desapruebe el producto. Solo dato del fabricante.
