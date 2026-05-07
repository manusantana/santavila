# PROMPT DE IMPLEMENTACIÓN POR SPRINTS — SANTAVILA

Ya existe el documento `plan_santavila.md` y deben existir, o debes crear antes de avanzar, estos documentos:

```txt
AUDITORIA_SANTAVILA.md
BACKLOG_SANTAVILA.md
DATA_MODEL_SANTAVILA.md
THEME_PLAN_SANTAVILA.md
```

Tu misión ahora es implementar por sprints, con máximo control y sin romper Shopify.

No hagas todos los cambios a la vez.

No publiques en producción sin validación.

No cambies checkout.

No instales apps salvo justificación clara y aprobación.

No inventes datos de producto.

---

## Modo de trabajo

Para cada sprint debes entregar:

1. Objetivo del sprint.
2. Cambios propuestos.
3. Archivos afectados.
4. Recursos Shopify afectados.
5. Riesgos.
6. Cómo validar.
7. Qué queda fuera del sprint.
8. Cambios realizados.
9. Checklist final.

---

# Sprint 1 — Limpieza urgente

Objetivo:

Dejar de parecer una tienda Shopify sin pulir y empezar a parecer una marca seria.

Tareas:

- unificar idioma español,
- eliminar textos en inglés,
- revisar footer,
- revisar menú,
- revisar claims,
- revisar etiquetas “Oferta”,
- revisar nombres visibles de categorías,
- crear barra de confianza,
- crear o mejorar páginas de entrega, garantía y mantenimiento,
- añadir CTA de asesoramiento si procede.

Copy base:

```txt
Diseño español para vivir fuera.
```

Subclaim:

```txt
Mobiliario exterior seleccionado de proveedores españoles para terrazas, jardines, áticos y porches. Diseño sereno, materiales preparados para exterior y entrega en España península.
```

Trust bar:

```txt
Proveedores españoles
Entrega en España península
Plazo estimado hasta 30 días
Garantía según proveedor
Asesoramiento humano
```

Validación:

- home sin mezcla de idiomas,
- footer coherente,
- menú claro,
- no hay promesas falsas,
- mobile correcto,
- carrito y checkout intactos.

---

# Sprint 2 — Modelo de datos Shopify

Objetivo:

Preparar metafields y metaobjects para que la tienda no dependa de textos sueltos.

Tareas:

- crear/proponer metafields,
- crear/proponer metaobjects,
- documentar namespaces,
- separar datos públicos e internos,
- crear plantilla maestra de producto,
- definir estado de enriquecimiento.

Namespace:

```txt
santavila
```

Metafields clave:

```txt
santavila.proveedor
santavila.fabricado_espana
santavila.proveedor_espanol
santavila.plazo_min_dias
santavila.plazo_max_dias
santavila.tipo_entrega
santavila.montaje_incluido
santavila.subida_incluida
santavila.garantia_resumen
santavila.material_estructura
santavila.uso_recomendado
santavila.nivel_mantenimiento
santavila.espacio_principal
santavila.coleccion_santavila
santavila.producto_hero
santavila.prioridad_comercial
santavila.estado_enriquecimiento
```

Validación:

- metafields creados sin errores,
- no se exponen datos internos sensibles,
- los productos pueden enriquecerse de forma ordenada,
- queda documentado cómo usarlos en PDP/PLP.

---

# Sprint 3 — PDP premium piloto

Objetivo:

Crear una ficha de producto superior para validar el modelo antes de aplicarlo a todo el catálogo.

Tareas:

- crear template PDP premium,
- aplicar a 3-5 productos piloto,
- crear bloques de entrega,
- garantía,
- materiales,
- medidas,
- mantenimiento,
- asesoramiento,
- FAQs,
- productos compatibles.

Texto entrega:

```txt
Entrega en España península mediante transporte. El servicio estándar no incluye montaje ni subida especial a vivienda salvo indicación expresa. El plazo estimado de este producto es de hasta 30 días según disponibilidad del proveedor.
```

Texto garantía:

```txt
Garantía ofrecida por el proveedor. La cobertura concreta puede variar según familia de producto, material y fabricante. Santavila centraliza la gestión para ayudarte ante cualquier incidencia.
```

Validación:

- no se inventan datos,
- las fichas reducen dudas,
- CTA principal claro,
- CTA asesoramiento visible,
- mobile perfecto,
- no se rompe añadir al carrito.

---

# Sprint 4 — Home premium

Objetivo:

Rediseñar la home para comunicar marca, producto, confianza y compra por espacio.

Estructura:

1. Hero.
2. Trust bar.
3. Compra por espacio.
4. Colecciones principales.
5. Por qué Santavila.
6. Productos héroe.
7. Materiales.
8. Asesoramiento.
9. Profesionales.
10. Inspiración.

Validación:

- en 10 segundos se entiende qué vende Santavila,
- se entiende la diferencia,
- se entiende dónde entrega,
- se entiende cómo pedir ayuda,
- no hay ruido promocional excesivo.

---

# Sprint 5 — PLP y SEO base

Objetivo:

Convertir colecciones en páginas que ayudan a decidir y captan tráfico SEO.

Tareas:

- mejorar colección de sofás,
- mejorar colección de mesas,
- mejorar colección de sillas,
- mejorar colección de tumbonas,
- crear contenido superior e inferior,
- mejorar filtros,
- crear FAQs,
- enlaces internos.

Validación:

- H1 correcto,
- title/meta description,
- texto útil,
- filtros relevantes,
- enlaces internos,
- mobile correcto.

---

# Sprint 6 — Profesionales y operativa

Objetivo:

Crear canal B2B ligero y automatizaciones internas.

Tareas:

- página profesionales,
- formulario,
- flujo de contacto,
- Shopify Flow pedidos premium,
- Shopify Flow productos pendientes,
- Shopify Flow pedidos con plazo largo,
- score proveedor/producto.

Validación:

- formulario funciona,
- mensaje claro,
- no promete condiciones no aprobadas,
- automatizaciones documentadas.

---

## Cierre de cada sprint

Al terminar cada sprint, devuelve:

```txt
SPRINT_X_RESUMEN.md
```

Con:

- qué se hizo,
- qué no se hizo,
- qué falta,
- riesgos,
- pruebas realizadas,
- capturas o rutas si aplica,
- siguiente sprint recomendado.

Empieza por Sprint 1 solo si ya existen auditoría, backlog, modelo de datos y plan de theme.
