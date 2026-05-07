# PROMPT DE ARRANQUE — AUDITORÍA SANTAVILA

Actúa como un equipo senior formado por:

- Senior Shopify Architect
- Ecommerce Manager especializado en mobiliario premium
- UX/UI Lead para ecommerce de alto ticket
- CRO Specialist
- SEO Technical Lead
- Shopify Theme Developer
- Data/Product Operations Manager
- Brand & Art Direction Lead

Tu misión inicial NO es tocar código.

Tu misión inicial es auditar, diagnosticar y planificar la transformación de Santavila.com, una tienda Shopify de mobiliario exterior premium accesible para España península.

Debes leer primero el documento:

```txt
plan_santavila.md
```

Y después revisar todo lo que tengas disponible del proyecto:

- theme,
- templates,
- sections,
- snippets,
- config,
- locales,
- navegación,
- colecciones,
- productos,
- páginas,
- metafields,
- metaobjects,
- apps instaladas si están disponibles,
- configuración Shopify si está disponible.

---

## Contexto de negocio

Santavila es una tienda Shopify de mobiliario exterior premium accesible.

Estado actual:

- Ya hay productos, categorías y precios.
- Hay más de 200 productos/SKUs activos.
- Hay 2 proveedores.
- Los proveedores son españoles.
- El margen está controlado por SKU.
- Mercado inicial: España península.
- Plazo máximo real de entrega: hasta 30 días.
- Entrega: solo transporte.
- No hay montaje incluido.
- No hay subida a vivienda incluida salvo acuerdo específico.
- Garantía: la garantía real del proveedor.
- Fotos base: proveedor.
- Se usarán herramientas IA como Higgsfield para generar visuales complementarios.
- No hay presupuesto de marketing de pago ahora mismo.
- El foco actual es UX, UI, CRO, SEO base, estructura ecommerce, confianza, diseño premium y datos de producto.

---

## Posicionamiento deseado

Santavila debe parecer:

- marca especialista en mobiliario exterior,
- ecommerce curado,
- marca premium accesible,
- marca serena, cálida y experta,
- alternativa más confiable que Sklum,
- más especializada en exterior que Kave Home,
- más aspiracional que Leroy Merlin/IKEA,
- mucho más accesible que Gandia Blasco, Kettal o Vondom.

Santavila NO debe parecer:

- dropshipping,
- catálogo genérico,
- marketplace,
- tienda low-cost,
- theme Shopify sin dirección,
- tienda traducida automáticamente,
- web llena de descuentos permanentes.

Claim principal:

```txt
Diseño español para vivir fuera.
```

Concepto creativo:

```txt
El exterior bien vivido.
```

Propuesta de valor:

```txt
Santavila selecciona mobiliario exterior de proveedores españoles, con diseño mediterráneo contemporáneo, materiales preparados para el uso exterior y una experiencia de compra clara en lo que más importa: medidas, entrega, garantía, mantenimiento y servicio.
```

Importante:

No digas “fabricado en España” de forma genérica salvo que esté validado por SKU. La promesa general segura es “proveedores españoles” o “seleccionado de proveedores españoles”.

---

## Restricciones

No hagas cambios todavía.

No modifiques código.

No publiques nada.

No crees ni borres recursos en Shopify.

No instales apps.

No cambies checkout.

No inventes datos de producto.

No prometas montaje.

No prometas subida.

No prometas garantías no verificadas.

No prometas fabricación española si no está validada.

---

## Entregables que debes crear

Genera estos documentos en `/docs/santavila/` o en la raíz si no existe esa carpeta:

```txt
AUDITORIA_SANTAVILA.md
BACKLOG_SANTAVILA.md
DATA_MODEL_SANTAVILA.md
THEME_PLAN_SANTAVILA.md
```

---

# 1. AUDITORIA_SANTAVILA.md

Debe incluir:

## 1.1 Diagnóstico ejecutivo

- situación actual,
- principales problemas,
- principales oportunidades,
- riesgos,
- prioridades.

## 1.2 Auditoría de marca

Revisa:

- claim,
- tono,
- idioma,
- consistencia,
- textos genéricos,
- premium percibido,
- confianza.

## 1.3 Auditoría UX/UI

Revisa:

- home,
- menú,
- navegación,
- footer,
- colecciones,
- fichas de producto,
- carrito,
- páginas de ayuda,
- mobile,
- jerarquía visual,
- CTAs.

## 1.4 Auditoría ecommerce

Revisa:

- categorías,
- colecciones,
- filtros,
- badges,
- promociones,
- cross-sell,
- información logística,
- garantía,
- devoluciones,
- asesoramiento,
- confianza.

## 1.5 Auditoría Shopify

Revisa:

- theme actual,
- templates,
- sections,
- snippets,
- settings,
- locales,
- metafields,
- metaobjects,
- navegación,
- productos,
- colecciones,
- policies,
- redirects,
- apps instaladas si están disponibles.

## 1.6 Auditoría SEO base

Revisa:

- titles,
- meta descriptions,
- H1,
- URLs,
- indexabilidad,
- categorías prioritarias,
- textos pobres,
- ALT de imágenes,
- schema,
- enlaces internos.

## 1.7 Auditoría de datos de producto

Detecta si faltan:

- proveedor,
- plazo mínimo,
- plazo máximo,
- tipo de entrega,
- garantía,
- material,
- medidas,
- peso,
- bultos,
- uso recomendado,
- espacio recomendado,
- mantenimiento,
- margen interno,
- prioridad comercial,
- estado de enriquecimiento.

---

# 2. BACKLOG_SANTAVILA.md

Organiza el backlog por fases:

## Fase 0 — Limpieza urgente

- unificar idioma español,
- eliminar textos en inglés,
- revisar footer,
- revisar menú,
- revisar claims,
- revisar etiquetas “Oferta”,
- revisar nombres de producto,
- crear barra de confianza,
- crear páginas de entrega, garantía y mantenimiento,
- añadir contacto/WhatsApp si procede.

## Fase 1 — Modelo de datos Shopify

- definir metafields,
- definir metaobjects,
- documentar namespaces,
- crear plantilla maestra de producto,
- decidir datos públicos/internos,
- sistema de priorización de SKUs.

## Fase 2 — PDP premium

- template PDP premium,
- entrega,
- garantía,
- materiales,
- mantenimiento,
- medidas,
- asesoramiento,
- FAQs,
- productos compatibles.

## Fase 3 — Home y PLP

- rediseño home,
- compra por espacio,
- colecciones destacadas,
- PLPs con contenido útil,
- filtros,
- bloques SEO,
- bloques de ayuda.

## Fase 4 — Dirección visual IA

- guía visual,
- prompts Higgsfield,
- escenas por espacio,
- imágenes para hero,
- imágenes para colecciones,
- reglas para no alterar producto real.

## Fase 5 — SEO y contenido

- categorías SEO,
- guías,
- páginas por espacio,
- páginas por material,
- FAQs,
- enlaces internos.

## Fase 6 — Profesionales

- página profesionales,
- formulario,
- condiciones,
- proceso interno.

## Fase 7 — Operativa y automatizaciones

- Shopify Flow,
- etiquetado por proveedor,
- alerta pedido premium,
- alerta plazo largo,
- seguimiento incidencias,
- score proveedor,
- score producto.

Cada tarea debe tener:

- prioridad,
- impacto,
- dificultad,
- riesgo,
- dependencia,
- archivos afectados si aplica,
- si requiere Shopify Admin,
- si requiere theme,
- si requiere contenido,
- validación manual.

---

# 3. DATA_MODEL_SANTAVILA.md

Propón metafields y metaobjects.

Namespace recomendado:

```txt
santavila
```

Metafields mínimos:

```txt
santavila.proveedor
santavila.fabricado_espana
santavila.proveedor_espanol
santavila.provincia_origen
santavila.plazo_min_dias
santavila.plazo_max_dias
santavila.tipo_entrega
santavila.montaje_incluido
santavila.subida_incluida
santavila.garantia_resumen
santavila.garantia_detalle
santavila.material_estructura
santavila.material_superficie
santavila.material_textil
santavila.uso_recomendado
santavila.uso_cubierto
santavila.nivel_mantenimiento
santavila.medidas_resumen
santavila.ancho_cm
santavila.fondo_cm
santavila.alto_cm
santavila.peso_kg
santavila.numero_bultos
santavila.dimensiones_bultos
santavila.estilo
santavila.espacio_principal
santavila.coleccion_santavila
santavila.producto_hero
santavila.exclude_feed
santavila.margen_porcentaje
santavila.margen_euros
santavila.prioridad_comercial
santavila.estado_enriquecimiento
```

Metaobjects recomendados:

```txt
sv_material_guide
sv_delivery_type
sv_warranty_policy
sv_supplier
sv_collection_story
sv_space_solution
sv_faq
sv_care_guide
```

Para cada uno indica:

- nombre,
- namespace,
- tipo Shopify recomendado,
- público/interno,
- uso en PDP,
- uso en PLP,
- uso en filtros,
- uso en automatizaciones,
- ejemplo,
- prioridad.

---

# 4. THEME_PLAN_SANTAVILA.md

Propón estructura de theme.

Secciones recomendadas:

```txt
sv-hero-premium
sv-trust-bar
sv-shop-by-space
sv-featured-collections
sv-material-grid
sv-why-santavila
sv-advice-block
sv-professionals-block
sv-editorial-guides
sv-product-trust-panel
sv-product-materials
sv-product-delivery
sv-product-warranty
sv-product-care
sv-product-faq
sv-compatible-products
sv-collection-hero
sv-collection-guide
sv-space-page
sv-material-page
```

Templates recomendados:

```txt
index.json
product.premium.json
product.sofa.json
product.table.json
product.chair.json
product.sunbed.json
collection.premium.json
collection.space.json
collection.material.json
page.delivery.json
page.warranty.json
page.care.json
page.professionals.json
page.inspiration.json
```

Snippets recomendados:

```txt
sv-badge-list
sv-delivery-summary
sv-warranty-summary
sv-material-summary
sv-product-score
sv-whatsapp-cta
sv-measurements
sv-care-icons
sv-trust-icons
```

Para cada sección/template/snippet indica:

- objetivo,
- dónde se usa,
- datos necesarios,
- metafields/metaobjects usados,
- dificultad,
- archivos a crear/modificar.

---

## Formato de respuesta

Primero responde con:

1. Qué has entendido.
2. Qué vas a auditar.
3. Riesgos principales.
4. Archivos que vas a generar.
5. Limitaciones de acceso si las hay.

Después genera los documentos.

No hagas cambios de código todavía.
