# DATA_MODEL_SANTAVILA.md

**Snapshot:** 2026-05-06
**Estado actual en Shopify:**
- Namespace `santavila`: **0 metafield definitions** (todo por crear).
- Metaobjects: **0 definiciones** (todo por crear).
- Existen metafields auto-creados por Shopify (`shopify--discovery--*`) y Google Shopping (`mm-google-shopping`). Esos no se tocan; el modelo Santavila convive con ellos.

## Convenciones

- **Namespace de producto:** `santavila` para todo lo propio.
- **Namespace de metaobjects:** prefijo `sv_` (no admite punto en `type`).
- **Boolean → siempre `true | false`.** Para campos opcionales con tres estados (sí / no / desconocido), usar `single_line_text_field` con valores controlados.
- **Listas vs referencias:**
  - Listas cerradas, fijas y simples → `list.single_line_text_field` con valores documentados.
  - Listas con info reusable (texto largo, imagen, atributos) → `metaobject_reference` o `list.metaobject_reference`.
- **Visibilidad:**
  - `Pública` = el campo se renderea en el storefront (PDP, PLP, filtros). Storefront API access habilitado.
  - `Interna` = solo visible en Admin/Flow/exports. Storefront API access deshabilitado.

---

## 1. Metafield definitions de PRODUCTO (32)

> Todos en `ownerType: PRODUCT`, namespace `santavila`. La columna **F** indica si está pensado para **filtrar en PLP** (Search & Discovery).

### Bloque A — Origen y proveedor (4)

| # | Key | Tipo Shopify | Visibilidad | F | Uso en PDP | Uso en PLP | Uso en automatizaciones | Ejemplo | Prioridad |
|---|-----|--------------|-------------|---|------------|------------|--------------------------|---------|-----------|
| 1 | `proveedor` | `metaobject_reference` → `sv_supplier` | Interna | — | — | — | Flow: tag pedido por proveedor; segmentar reporting | `gid://…/Metaobject/123` (Hevea) | P0 |
| 2 | `fabricado_espana` | `boolean` | Pública | ✓ | Badge "Fabricado en España" si true | Filtro "Fabricado en España" | Feed Google Shopping (`origin_country`) | `true` | P0 |
| 3 | `proveedor_espanol` | `boolean` | Pública | — | Texto "Proveedor español" | — | — | `true` | P1 |
| 4 | `provincia_origen` | `single_line_text_field` | Pública (opcional) | — | Línea opcional en bloque "Por qué esta pieza" | — | — | `Valencia` | P2 |

> **Nota crítica:** `fabricado_espana` y `proveedor_espanol` son **distintos**. El plan exige no decir "fabricado en España" salvo validación SKU. Solo activar `fabricado_espana=true` cuando el proveedor lo confirme por escrito.

### Bloque B — Logística (8)

| # | Key | Tipo Shopify | Visibilidad | F | Uso en PDP | Uso en PLP | Automatizaciones | Ejemplo | Prio |
|---|-----|--------------|-------------|---|------------|------------|------------------|---------|------|
| 5 | `plazo_min_dias` | `number_integer` | Pública | ✓ | "Entrega en X-Y días" | Filtro "Plazo" | Flow: alerta si pedido contiene producto plazo>21 | `7` | P0 |
| 6 | `plazo_max_dias` | `number_integer` | Pública | ✓ | (igual) | (igual) | (igual) | `15` | P0 |
| 7 | `tipo_entrega` | `list.single_line_text_field` (valores: `transporte`, `transporte_especial`, `bajo_consulta`) | Pública | ✓ | "Entrega: transporte" | Filtro | — | `["transporte"]` | P1 |
| 8 | `montaje_incluido` | `boolean` | Pública | — | "Sin montaje" si false | — | — | `false` | P0 |
| 9 | `subida_incluida` | `boolean` | Pública | — | "Sin subida especial" si false | — | — | `false` | P0 |
| 10 | `peso_kg` | `number_decimal` | Interna (logística) | — | — | — | Cálculo de transporte; etiquetas | `42.5` | P1 |
| 11 | `numero_bultos` | `number_integer` | Interna | — | — | — | Cálculo de transporte | `2` | P1 |
| 12 | `dimensiones_bultos` | `single_line_text_field` | Interna | — | — | — | Logística | `120×50×30 / 80×30×30` | P2 |

### Bloque C — Garantía (2)

| # | Key | Tipo | Visibilidad | F | PDP | PLP | Automatizaciones | Ejemplo | Prio |
|---|-----|------|-------------|---|-----|-----|------------------|---------|------|
| 13 | `garantia_resumen` | `single_line_text_field` | Pública | — | "Garantía: 3 años" | — | — | `3 años` | P0 |
| 14 | `garantia_detalle` | `metaobject_reference` → `sv_warranty_policy` | Pública | — | Bloque garantía PDP enlaza al detalle | — | — | `gid://…/Metaobject/901` | P1 |

### Bloque D — Materiales (3)

| # | Key | Tipo | Visibilidad | F | PDP | PLP | Automatizaciones | Ejemplo | Prio |
|---|-----|------|-------------|---|-----|-----|------------------|---------|------|
| 15 | `material_estructura` | `list.single_line_text_field` (valores: `aluminio`, `acero`, `madera_teca`, `madera_eucalipto`, `resina`, `mimbre_sintetico`) | Pública | ✓ | Bloque materiales | Filtro principal | — | `["aluminio"]` | P0 |
| 16 | `material_superficie` | `list.single_line_text_field` (`hpl`, `ceramica`, `madera`, `cristal`, `aluminio`, `marmol`) | Pública | ✓ | (igual) | Filtro | — | `["hpl"]` | P1 |
| 17 | `material_textil` | `list.single_line_text_field` (`olefin`, `acrilico`, `textilene`, `cuerda`, `pe_ratan`, `sin_textil`) | Pública | ✓ | (igual) | Filtro | — | `["olefin"]` | P1 |

> Las listas controladas se documentan abajo en §5. Diferenciamos *estructura* (lo que aguanta el peso) de *superficie* (tablero/cojín visible) de *textil* (acabado tela).

### Bloque E — Uso y espacio (4)

| # | Key | Tipo | Visibilidad | F | PDP | PLP | Automatizaciones | Ejemplo | Prio |
|---|-----|------|-------------|---|-----|-----|------------------|---------|------|
| 18 | `uso_recomendado` | `list.single_line_text_field` (`residencial`, `hosteleria`, `contract_hotel`, `contract_restaurante`, `casa_rural`) | Pública | — | "Recomendado para hostelería" | — | Segmentar productos profesionales | `["residencial", "hosteleria"]` | P1 |
| 19 | `uso_cubierto` | `list.single_line_text_field` (`cubierto`, `descubierto`, `ambos`) | Pública | ✓ | "Apto cubierto y descubierto" | Filtro | — | `["ambos"]` | P1 |
| 20 | `nivel_mantenimiento` | `list.single_line_text_field` (`bajo`, `medio`, `alto`) | Pública | ✓ | "Mantenimiento bajo" | Filtro | — | `["bajo"]` | P1 |
| 21 | `espacio_principal` | `list.single_line_text_field` (`terraza`, `atico`, `jardin`, `porche`, `balcon`, `patio`, `piscina`) | Pública | ✓ | — | **Smart collection** por espacio + filtro | — | `["terraza","atico"]` | P0 |

### Bloque F — Medidas (3)

| # | Key | Tipo | Visibilidad | F | PDP | PLP | Automatizaciones | Ejemplo | Prio |
|---|-----|------|-------------|---|-----|-----|------------------|---------|------|
| 22 | `ancho_cm` | `number_integer` | Pública | ✓ | Bloque medidas | Filtro rango | — | `196` | P0 |
| 23 | `fondo_cm` | `number_integer` | Pública | ✓ | (igual) | Filtro rango | — | `90` | P0 |
| 24 | `alto_cm` | `number_integer` | Pública | ✓ | (igual) | Filtro rango | — | `90` | P0 |
| 25 | `medidas_resumen` | `single_line_text_field` | Pública | — | Línea visible junto al título "196 × 90 × 90 cm" | — | — | `196 × 90 × 90 cm` | P1 |

> Mantener `medidas_resumen` aunque sea redundante con `ancho/fondo/alto`: la cadena humana es para cards y meta description; los enteros son para filtrar.

### Bloque G — Catálogo Santavila (4)

| # | Key | Tipo | Visibilidad | F | PDP | PLP | Automatizaciones | Ejemplo | Prio |
|---|-----|------|-------------|---|-----|-----|------------------|---------|------|
| 26 | `estilo` | `list.single_line_text_field` (`mediterraneo`, `contemporaneo`, `natural`, `clasico`, `minimalista`) | Pública | ✓ | — | Filtro estilo | — | `["mediterraneo","contemporaneo"]` | P2 |
| 27 | `coleccion_santavila` | `metaobject_reference` → `sv_collection_story` | Pública | — | Bloque "Pertenece a la colección X" | Smart collection por colección Santavila | — | `gid://…/Metaobject/501` | P2 |
| 28 | `producto_hero` | `boolean` | Interna | — | — | Smart collection "Productos héroe" para home | Mostrar en home + boost en search | `true` | P0 |
| 29 | `exclude_feed` | `boolean` | Interna | — | — | — | Excluir de Google Shopping / feeds externos | `false` | P2 |

### Bloque H — Comercial e interno (4)

| # | Key | Tipo | Visibilidad | F | PDP | PLP | Automatizaciones | Ejemplo | Prio |
|---|-----|------|-------------|---|-----|-----|------------------|---------|------|
| 30 | `margen_porcentaje` | `number_decimal` | Interna | — | — | — | Reporting; alerta si margen < umbral | `33.5` | P1 |
| 31 | `margen_euros` | `number_decimal` | Interna | — | — | — | (igual) | `271.92` | P1 |
| 32 | `prioridad_comercial` | `list.single_line_text_field` (`alta`, `media`, `baja`) | Interna | — | — | Boost en search | — | `["alta"]` | P1 |
| **+1** | `estado_enriquecimiento` | `list.single_line_text_field` (`pendiente`, `en_progreso`, `revisado`, `completo`) | Interna | — | — | — | Filtro Admin para curación; Flow alerta si nuevo producto sin completar | `["pendiente"]` | P0 |

> **Nota:** `estado_enriquecimiento` se añade aunque suma 33. Es operativamente crítico — sin él no se sabe qué SKUs están listos para destacar.

### Sin metafield — pero se usa el campo nativo Shopify

| Concepto | Dónde vive |
|----------|------------|
| Vendor real | `santavila.proveedor` (metafield) — el campo nativo `vendor` se unifica en `"Santavila"` |
| Tipo de producto | `productType` nativo (Sofá, Sillón, Mesa, Mesa centro, Mesa comedor, Silla, Tumbona, Parasol, Conjunto, Reposapiés, Banco, Funda, Accesorio, Pérgola, Cama balinesa, Balancín) |
| Tags | reservado para campañas/etiquetas operativas (`heroe`, `bajo_pedido`, `pendiente_enriquecimiento`); ya no se usa para proveedor ni material |

---

## 2. Metaobject definitions (8)

### 2.1 `sv_supplier` (proveedor)

| Campo | Tipo | Obligatorio | Notas |
|-------|------|-------------|-------|
| `nombre_interno` | single_line_text | ✓ | "Hevea", "Balliu" |
| `nombre_publico` | single_line_text | — | Si se quiere mostrar (normalmente no) |
| `origen_pais` | single_line_text | ✓ | "España" |
| `provincia` | single_line_text | — | "Castellón" / "Valencia" |
| `plazo_estandar_dias` | number_integer | ✓ | 10 |
| `condiciones_envio` | rich_text | — | Texto: "Envío gratuito península pedidos > 900 €" |
| `garantia_estandar` | single_line_text | — | "3 años" |
| `contacto_operativo` | single_line_text | — | Email/teléfono interno |
| `score_proveedor` | number_integer | — | 1-5, actualizado mensualmente |
| `notas_internas` | rich_text | — | Internas |
| `logo` | file_reference | — | Para uso interno o página "Quiénes somos" |

**Visibilidad:** Interna (Storefront API: solo `nombre_publico`, `origen_pais`, `garantia_estandar` si se decide mostrar).
**Uso en PDP:** ninguno por defecto. Si se decide mostrar, vía componente "Sobre el productor".
**Uso en automatizaciones:** Flow lee `lineItems[].product.metafield.santavila.proveedor → metaobject.nombre_interno` para tag de pedido.
**Prioridad:** P0.
**Inicializar con:** Hevea, Balliu (datos en `PROYECTO.md §3` y email a Hevea pendiente de respuesta).

### 2.2 `sv_material_guide` (guía de material)

| Campo | Tipo | Obligatorio |
|-------|------|-------------|
| `material_clave` | single_line_text | ✓ ("aluminio", "hpl"…) |
| `nombre_visible` | single_line_text | ✓ ("Aluminio termo-lacado") |
| `descripcion` | rich_text | ✓ |
| `ventajas` | list.single_line_text | — |
| `cuidados` | rich_text | ✓ |
| `recomendado_para` | rich_text | — |
| `no_recomendado_para` | rich_text | — |
| `imagen_principal` | file_reference | — |
| `icono` | file_reference (svg) | — |

**Visibilidad:** Pública.
**Uso en PDP:** sección `sv-product-materials` enlaza productos con sus guías. Cuando un producto tiene `material_estructura=["aluminio","acero"]`, la sección lee las dos guías.
**Uso en PLP:** página dedicada `/pages/aluminio` (ver F5-03).
**Prioridad:** P1.
**Inicializar con:** aluminio, acero, madera_teca, madera_eucalipto, resina, mimbre_sintetico, hpl, ceramica, cristal, marmol, olefin, acrilico, textilene, cuerda, pe_ratan = **15 entradas**.

### 2.3 `sv_delivery_type` (tipo de entrega)

| Campo | Tipo |
|-------|------|
| `clave` | single_line_text (`transporte`, `transporte_especial`, `bajo_consulta`) |
| `nombre` | single_line_text |
| `descripcion_corta` | single_line_text |
| `incluye` | rich_text |
| `no_incluye` | rich_text |
| `plazo_estimado` | single_line_text |
| `condiciones` | rich_text |

**Visibilidad:** Pública.
**Uso en PDP:** sección `sv-product-delivery` lee `tipo_entrega` y muestra el detalle.
**Prioridad:** P1.
**Inicializar:** 3 entradas (transporte estándar, transporte especial, bajo consulta).

### 2.4 `sv_warranty_policy` (política de garantía)

| Campo | Tipo |
|-------|------|
| `proveedor` | metaobject_reference → sv_supplier |
| `familia` | single_line_text (opcional, p.ej. "Tumbonas Balliu") |
| `duracion_meses` | number_integer |
| `cobertura` | rich_text |
| `exclusiones` | rich_text |
| `procedimiento` | rich_text |

**Visibilidad:** Pública.
**Uso en PDP:** referenciado por `santavila.garantia_detalle`. Si vacío → fallback al texto literal de `santavila.garantia_resumen`.
**Prioridad:** P1.
**Inicializar:** mínimo 2 (Hevea genérico, Balliu genérico). Más específicos según familias.

### 2.5 `sv_collection_story` (colección Santavila propia)

| Campo | Tipo |
|-------|------|
| `nombre` | single_line_text |
| `claim` | single_line_text |
| `descripcion` | rich_text |
| `estilo` | list.single_line_text |
| `espacios_recomendados` | list.single_line_text |
| `productos` | list.product_reference |
| `imagen_hero` | file_reference |

**Visibilidad:** Pública.
**Uso en PDP:** "Pertenece a la colección X" → link.
**Uso en PLP:** página propia con narrativa.
**Prioridad:** P2.
**Inicializar:** 3-5 colecciones piloto (ej. "Mediterráneo", "Lounge", "Comedor terraza").

### 2.6 `sv_space_solution` (espacio)

| Campo | Tipo |
|-------|------|
| `espacio` | single_line_text (`terraza`, `atico`…) |
| `nombre_visible` | single_line_text ("Terrazas") |
| `problema_que_resuelve` | rich_text |
| `recomendaciones` | rich_text |
| `medidas_orientativas` | rich_text |
| `productos_recomendados` | list.product_reference |
| `imagen_hero` | file_reference |

**Visibilidad:** Pública.
**Uso:** alimenta páginas `/pages/muebles-para-terraza`, `/pages/muebles-para-atico`, etc.
**Prioridad:** P2.
**Inicializar:** 7 entradas (Terraza, Ático, Jardín, Porche, Balcón, Patio, Piscina).

### 2.7 `sv_faq` (FAQ reutilizable)

| Campo | Tipo |
|-------|------|
| `pregunta` | single_line_text |
| `respuesta` | rich_text |
| `familia` | single_line_text (opcional) |
| `producto` | product_reference (opcional) |
| `visibilidad` | single_line_text (`pdp`, `home`, `coleccion`, `pagina_ayuda`) |
| `orden` | number_integer |

**Visibilidad:** Pública.
**Uso en PDP:** sección `sv-product-faq` lee FAQs ligadas al producto/familia.
**Uso adicional:** schema.org FAQPage cuando proceda.
**Prioridad:** P2.
**Inicializar:** 30-50 FAQs comunes (entrega, garantía, materiales, mantenimiento, devoluciones).

### 2.8 `sv_care_guide` (guía de cuidado)

| Campo | Tipo |
|-------|------|
| `material_clave` | single_line_text (igual que `sv_material_guide.material_clave` para join) |
| `frecuencia` | single_line_text |
| `limpieza_recomendada` | rich_text |
| `productos_evitar` | rich_text |
| `recomendaciones_temporada` | rich_text |

**Visibilidad:** Pública.
**Uso en PDP:** sección `sv-product-care`.
**Uso adicional:** /pages/mantenimiento.
**Prioridad:** P2.
**Inicializar:** una por material (ver §2.2 lista).

---

## 3. Resumen visual de tipos por bloque

```
santavila (32 metafields)
├── A · Origen y proveedor (4)
├── B · Logística (8)
├── C · Garantía (2)
├── D · Materiales (3)
├── E · Uso y espacio (4)
├── F · Medidas (3)
├── G · Catálogo Santavila (4)
└── H · Comercial e interno (4)

sv_* (8 metaobjects)
├── sv_supplier ← referenciado por santavila.proveedor
├── sv_material_guide ← join por material_clave
├── sv_delivery_type ← referenciado por tipo_entrega (versión enriquecida)
├── sv_warranty_policy ← referenciado por santavila.garantia_detalle
├── sv_collection_story ← referenciado por santavila.coleccion_santavila
├── sv_space_solution ← join por espacio_principal
├── sv_faq
└── sv_care_guide ← join por material_clave con sv_material_guide
```

## 4. Orden de creación recomendado

1. **`sv_supplier`** primero (lo necesita `santavila.proveedor`).
2. Crear los 32 **metafields santavila.\*** (orden libre, pero respetando que `proveedor` referencia a `sv_supplier` y `coleccion_santavila` referencia a `sv_collection_story`, así que esos dos metaobjects deben existir antes que sus metafields).
3. **`sv_material_guide`**, **`sv_delivery_type`**, **`sv_warranty_policy`**, **`sv_care_guide`**, **`sv_space_solution`**, **`sv_collection_story`**, **`sv_faq`** después.
4. Poblar `sv_supplier` con Hevea + Balliu (F1-03).
5. Migrar datos desde `Santavila.xlsx` y CSVs proveedor a metafields (F1-05). Empezar por los 20 héroe.

## 5. Listas controladas (vocabulario cerrado)

Documentar en este archivo evita drift de valores. Cada uno se sincroniza con el campo `definition.choices` del metafield correspondiente.

```yaml
material_estructura:
  - aluminio
  - acero
  - madera_teca
  - madera_eucalipto
  - resina
  - mimbre_sintetico

material_superficie:
  - hpl
  - ceramica
  - madera
  - cristal
  - aluminio
  - marmol

material_textil:
  - olefin
  - acrilico
  - textilene
  - cuerda
  - pe_ratan
  - sin_textil

uso_recomendado:
  - residencial
  - hosteleria
  - contract_hotel
  - contract_restaurante
  - casa_rural

uso_cubierto:
  - cubierto
  - descubierto
  - ambos

nivel_mantenimiento:
  - bajo
  - medio
  - alto

espacio_principal:
  - terraza
  - atico
  - jardin
  - porche
  - balcon
  - patio
  - piscina

estilo:
  - mediterraneo
  - contemporaneo
  - natural
  - clasico
  - minimalista

tipo_entrega:
  - transporte
  - transporte_especial
  - bajo_consulta

prioridad_comercial:
  - alta
  - media
  - baja

estado_enriquecimiento:
  - pendiente
  - en_progreso
  - revisado
  - completo
```

> Si se necesita añadir un valor nuevo (ej. nuevo material), se actualiza primero esta lista, luego el metafield definition en Admin, luego se documenta el cambio en `BACKLOG_SANTAVILA.md`.

## 6. Decisiones pendientes que afectan al modelo

| Decisión | Por qué importa | Bloquea |
|----------|------------------|---------|
| ¿`fabricado_espana` se valida producto a producto con el proveedor? | Determina el badge en PDP y el copy de marca | Activación de F0-15 (badges de valor) |
| ¿Se añade WhatsApp comercial? | Decide si hay metafield `santavila.whatsapp_disponible` o se usa global | F2-10 |
| ¿Hay productos bajo pedido específico? | Necesita valor `bajo_consulta` activo en `tipo_entrega` y un mensaje propio | F2-04 |
| ¿`prioridad_comercial` la asigna sistema (score) o humano? | Define si F1-07 lo automatiza o queda manual | F1-07 |
| ¿Se preparará Markets para Portugal? | Si sí, hay que multiidioma y multimoneda; afecta a `medidas_resumen` y otros | Fase futura |

---

## 7. Cómo se renderea cada metafield (resumen)

### Productos (PDP)

```
[título · medidas_resumen]
[precio]
[sv-product-trust-panel]   ← lee plazo_min/max, tipo_entrega, montaje_incluido, garantia_resumen
"Sin montaje"               ← si montaje_incluido = false
"Sin subida especial"       ← si subida_incluida = false

[badge fabricado_espana]    ← si true
[badge envio_gratis]        ← si superior a umbral

[descripcion HTML actual]

[sv-product-materials]      ← lee material_estructura/superficie/textil + sv_material_guide
[sv-product-delivery]       ← lee tipo_entrega + sv_delivery_type
[sv-product-warranty]       ← lee garantia_resumen + garantia_detalle (sv_warranty_policy)
[sv-product-care]           ← lee material_estructura → sv_care_guide
[sv-product-faq]            ← lee sv_faq filtradas por producto/familia
[sv-compatible-products]    ← lee coleccion_santavila → sv_collection_story.productos
```

### Productos (PLP)

- Smart collections automáticas por:
  - `espacio_principal` (7 colecciones)
  - `material_estructura` (5 colecciones)
  - `producto_hero=true` (1 colección "Lo destacado")
  - `coleccion_santavila` (N colecciones)

- Filtros activos:
  - precio (nativo)
  - `material_estructura`, `material_superficie`, `material_textil`
  - `plazo_max_dias` (rango)
  - `ancho_cm`, `fondo_cm`, `alto_cm` (rangos)
  - `uso_cubierto`, `nivel_mantenimiento`, `espacio_principal`, `estilo`
  - `fabricado_espana` (boolean)

### Productos (operaciones internas)

- Reporting: `margen_porcentaje`, `margen_euros`, `prioridad_comercial`, `estado_enriquecimiento`.
- Logística: `peso_kg`, `numero_bultos`, `dimensiones_bultos`.
- Flow: `proveedor` (→ tag pedido), `plazo_max_dias>21` (→ alerta), `producto_hero=true` (→ feed home).

---

## 8. Migración desde el estado actual

| Origen actual | Destino | Cómo |
|---------------|---------|------|
| `vendor` = "Hevea" / "Balliu" | `santavila.proveedor` (referencia) | F0-02 |
| Tags `aluminio`, `HPL`, `bicolor` | `santavila.material_estructura` / `material_superficie` | F1-05 script |
| Tags `terraza`, `jardín`, `hostelería` | `santavila.uso_recomendado` + `santavila.espacio_principal` | F1-05 script |
| Tags `2 plazas`, `3 plazas` | nuevo `productType="Conjunto"` o columna `numero_plazas` (no en este modelo aún — añadir si demanda) | Eval F1 |
| `compareAtPrice` permanente | nada (eliminar) — `santavila.fabricado_espana=true` reemplaza la lógica de "valor extra" | F0-01 + F0-15 |
| `Santavila.xlsx` hoja Hevea/Balliu cols Margen €/% | `santavila.margen_euros` y `santavila.margen_porcentaje` | F1-05 script |
| `Santavila.xlsx` Estado columna | `santavila.estado_enriquecimiento` | F1-05 script |
| Medidas en título y handle | parseo regex → `santavila.ancho_cm/fondo_cm/alto_cm` | F1-05 script |
| Texto descripción HTML | bloques: extraer plazo, garantía, materiales y poblar metafields → texto descripción se simplifica | F1-05 manual + F2-09 |
