# Configuración de envío Santavila — Paso a paso

Guía para aplicar las decisiones de envío del [JOURNAL.md (entrada 2026-05-14)](JOURNAL.md) en Shopify Admin.

**Resumen del sistema:**
- 3 tarifas planas por volumen del producto (XS / M / L)
- Envío gratis si subtotal del carrito > 500€
- Clasificación de productos asignada via metafield `santavila.envio_categoria` y tag `envio:xs|m|l`

---

## Resumen de tarifas

| Categoría | Tarifa | Productos | # SKUs únicos |
|---|---|---|---|
| **XS** | 9,95€ (1ud) → 14,95€ (2) → 19,95€ (3-4) → 24,95€ (5-8) → 29,95€ (9+) | Cojines, fundas, limpiador | 6 |
| **M** | 29,95€ plano | Mesa auxiliar, silla individual, taburete, parasol pequeño | 93 |
| **L** | 57,95€ plano | Mesa comedor, sofá, conjunto, tumbona, parasol grande, default | 126 |
| **Gratis** | 0 € | Cualquier carrito con subtotal > 500€ | — |

Totales: 225 productos clasificados (los 281 SKUs de la hoja maestra incluyen variantes que comparten handle).

---

## Paso 1 — Crear el metafield definition (5 min)

Solo se hace una vez.

1. Abrir Admin Shopify → **Settings → Custom data → Products**.
2. Click **"Add definition"**.
3. Rellenar:
   - **Name:** `Envío - Categoría volumétrica`
   - **Namespace and key:** `santavila.envio_categoria`
   - **Description:** `XS, M o L según volumen del producto. Determina la tarifa de envío.`
   - **Type:** **Single line text**
   - **Validations:**
     - **One of:** marca esta opción y añade los valores `xs`, `m`, `l` (uno por línea).
4. **Save**.

> Si saltas este paso, el script `apply_shipping_categories.py --apply` fallará con `userError` "metafield definition not found".

---

## Paso 2 — Aplicar la clasificación a los 225 productos (10 min)

Desde el directorio raíz del proyecto:

```bash
# 1. Dry-run: revisar la clasificación propuesta
python3 apply_shipping_categories.py
# Lee Santavila.xlsx, escribe shipping_categories_report.csv
# NO toca Shopify. Inspeccionar el CSV antes de seguir.

# 2. Apply real
python3 apply_shipping_categories.py --apply
# Lee tags y metafield actuales producto a producto,
# añade tag `envio:xs|m|l` y metafield santavila.envio_categoria.
# Dura ~1-2 min para los 225 productos.
```

**Lo que verás en consola:**
```
  ✓ [  1/225] tumbona-de-aluminio-etna-individual                  → l   (ACTUALIZADO)
  ✓ [  2/225] sillon-exterior-aluminio-estilo-envolvente-9890-cm   → m   (ACTUALIZADO)
  · [  3/225] cojin-exterior-50x50                                 → xs  (SIN_CAMBIOS)
  ...

── Resumen ──
  ACTUALIZADO: 224
  SIN_CAMBIOS: 1
```

Si algún producto sale `ERROR` o `NO_ENCONTRADO_EN_SHOPIFY`, el reporte CSV detalla la causa. Casos típicos:
- handle de la hoja maestra que ya no existe en Shopify (renombrado / borrado)
- metafield definition no creada (volver al Paso 1)

**Reversibilidad:** el script no borra tags previos no relacionados — solo gestiona `envio:xs|m|l`. Si quisieras revertir, basta con eliminar esos 3 tags y el metafield.

---

## Paso 3 — Crear los Shipping Rates en Admin (10 min)

1. Admin Shopify → **Settings → Shipping and delivery**.
2. En la sección **Shipping**, el shipping profile **"General shipping rates"** (el que se aplica por defecto) → click **"Manage rates"**.
3. En la zona **"Domestic" (España)** click **"Add rate"** y crear las 4 rates siguientes, una por una:

### Rate 1 — Envío estándar XS

- **Rate name:** `Envío accesorios (1 ud)`
- **Rate type:** Custom flat rate
- **Price:** `9,95 €`
- **Conditions:** **"Add conditions" → Based on item quantity**
  - Min quantity: `1`
  - Max quantity: `1`
- **Bonus** *(opcional, si Shopify lo permite en tu plan)*: añadir filtro de producto **"Only apply to products with tag"** → tag `envio:xs`.

### Rate 2 — Envío accesorios pack

Repetir el patrón anterior para los tramos restantes de XS:

| Rate name | Price | Min qty | Max qty | Tag filtro |
|---|---|---|---|---|
| `Envío accesorios (2 ud)` | 14,95 € | 2 | 2 | `envio:xs` |
| `Envío accesorios (3-4 ud)` | 19,95 € | 3 | 4 | `envio:xs` |
| `Envío accesorios (5-8 ud)` | 24,95 € | 5 | 8 | `envio:xs` |
| `Envío accesorios (9+ ud)` | 29,95 € | 9 | *(sin tope)* | `envio:xs` |

### Rate 3 — Envío M

- **Rate name:** `Envío mediano`
- **Price:** `29,95 €`
- **Conditions:** Tag del producto = `envio:m`

### Rate 4 — Envío L

- **Rate name:** `Envío voluminoso`
- **Price:** `57,95 €`
- **Conditions:** Tag del producto = `envio:l`

### Rate 5 — Envío gratis > 500€

- **Rate name:** `Envío gratuito a península`
- **Price:** `0,00 €`
- **Conditions:** **"Based on order price"** → Min order price: `500 €`
- Esta rate **no necesita filtro de tag**: se aplica a cualquier producto cuando el subtotal supera el umbral.

---

## Paso 4 — Validación (15 min)

Antes de dar el sistema por bueno, validar 4 escenarios en el checkout (modo "Preview as customer"):

| Escenario | Carrito | Envío esperado |
|---|---|---|
| 1. Cojín suelto | 1× cojín 30€ | **9,95€** |
| 2. Pack accesorios | 3× fundas (3×60€ = 180€) | **19,95€** |
| 3. Mesa pequeña + silla | 1× mesa auxiliar 120€ + 1× silla 150€ = 270€ | **29,95€ + 29,95€ = 59,90€** *(ver caveat abajo)* |
| 4. Conjunto premium | 1× sofá 1.500€ | **GRATIS** (>500€) |
| 5. Multi-categoría con umbral | 1× silla 150€ + 1× mesa grande 380€ = 530€ | **GRATIS** (>500€) |

### Caveat conocido — Escenario 3

Si el carrito tiene productos de varias categorías y NO supera 500€, **Shopify cobra la suma de tarifas aplicables**. Esto puede parecer injusto:
- 1 mesa auxiliar (M, 29,95€) + 1 silla (M, 29,95€) → cobra 59,90€

**Mitigación corta:** la mayoría de pedidos multi-producto pasan los 500€ y caen en envío gratis.
**Mitigación larga (Sprint 5):** usar Shopify Function que calcule la tarifa como `max(tarifa_por_categoría_presente_en_carrito)` en vez de sumar. Diferida hasta que sea problema real.

---

## Paso 5 — Comunicación en la web (Fase 0)

Cuando se ejecuten F0-11 (página Entrega) y F0-16 (barra de confianza), incluir:

**Texto base sugerido para `/pages/entrega`:**

> **Envío en España península**
>
> Entregamos en toda la península mediante transporte. **Envío gratuito a partir de 500 €.**
>
> Para pedidos por debajo del umbral, el coste depende del volumen del producto:
> - Accesorios (cojines, fundas, limpiador): desde 9,95 €
> - Sillas, mesas auxiliares y parasoles pequeños: 29,95 €
> - Mesas grandes, sofás, tumbonas y conjuntos: 57,95 €
>
> El servicio estándar no incluye montaje ni subida especial a vivienda salvo indicación expresa. El plazo estimado es de hasta 30 días según disponibilidad del proveedor.

**Para la barra de confianza global (`sv-trust-bar`):**

> Envío gratuito en España península desde 500 €

---

## Resumen del orden de ejecución

```
1. Crear metafield definition  santavila.envio_categoria    ~5 min   (Admin UI)
2. python3 apply_shipping_categories.py                    ~1 min   (dry-run)
3. Revisar shipping_categories_report.csv                  ~5 min   (manual)
4. python3 apply_shipping_categories.py --apply            ~2 min   (script)
5. Crear los 4-5 rates en "General shipping rates"         ~10 min  (Admin UI)
6. Validar los 5 escenarios en checkout preview            ~15 min  (manual)
7. Actualizar JOURNAL.md con la fecha de aplicación        ~2 min
```

Total estimado: **~40 minutos.**
