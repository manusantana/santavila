# Notas importantes — cosas a tener en cuenta

> Documento de "no perder esto". Pensado sobre todo para cuando **cambiemos de tema** en Shopify.
> Última actualización: 2026-05-31.

---

## 0. Principio clave: qué se pierde y qué NO al cambiar de tema

| Tipo | ¿Sobrevive a un cambio de tema? | Dónde vive |
|---|---|---|
| Descripciones de producto, meta descriptions, SEO titles | ✅ **Sí** | Datos de Shopify (producto/colección) |
| Descripciones de colección + FAQ (texto) | ✅ **Sí** | Dato `description` de cada colección |
| Imágenes de producto, metafields, precios | ✅ **Sí** | Datos de Shopify |
| **Renderizado** de intro/FAQ de colección | ❌ **NO** — se pierde | Archivos del **tema** (ver §1) |
| Cualquier schema JSON-LD, breadcrumbs, etc. que añadamos al tema | ❌ **NO** | Archivos del tema |
| Ajustes del editor (bloques añadidos a mano en Personalizar) | ❌ **NO** | Configuración del tema |

**Conclusión:** el contenido está a salvo. Lo que hay que **re-aplicar tras cambiar de tema** son las personalizaciones de código del §1 (y las futuras de schema).

---

## 1. Personalizaciones de tema aplicadas (RE-APLICAR tras cambiar de theme)

**Tema actual:** `Dwell 3.5.1` (id `188231123268`).
**Problema que resuelven:** el tema por defecto **no renderiza `collection.description`** en la página de colección (solo el `<h1>` del título). Sin esto, la intro + FAQ que escribimos para las 6 colecciones **no se ven** (aunque estén guardadas).

### Convención de contenido de la que depende todo
La descripción de cada colección guarda **intro + FAQ en un solo campo**, separados por exactamente este encabezado:

```
<h2>Preguntas frecuentes</h2>
```

El renderizado **parte** la descripción por esa cadena: lo de antes = intro, lo de después = FAQ. **Si alguien cambia ese `<h2>` no coincidirá el split.** (Mantener el texto literal "Preguntas frecuentes" en `<h2>`.)

### Archivos creados en el tema

**`sections/collection-intro.liquid`** (intro, debajo del título):
```liquid
{%- assign _intro = collection.description | split: '<h2>Preguntas frecuentes</h2>' | first -%}
{%- if _intro != blank -%}
  <div class="page-width" style="max-width:760px;margin-inline:auto;text-align:center;padding-block:0 16px;">
    {{ _intro }}
  </div>
{%- endif -%}
{% schema %}
{"name":"Collection intro","settings":[]}
{% endschema %}
```

**`sections/collection-faq.liquid`** (FAQ, al final del listado):
```liquid
{%- assign _parts = collection.description | split: '<h2>Preguntas frecuentes</h2>' -%}
{%- if _parts.size > 1 -%}
  <div class="page-width" style="max-width:820px;margin-inline:auto;padding-block:40px;">
    <h2>Preguntas frecuentes</h2>{{ _parts | last }}
  </div>
{%- endif -%}
{% schema %}
{"name":"Collection FAQ","settings":[]}
{% endschema %}
```

### Cambios en `templates/collection.json`
- Se **eliminó** el bloque de texto manual de la cabecera (mostraba la descripción entera).
- Se **añadieron** las dos secciones nuevas al `order`, quedando:
  `["section", "collection-intro", "main", "collection-faq"]`
  (título → intro → grid de productos → FAQ).

> ⚠️ **Por qué NO se hizo en un bloque de texto del editor:** los ajustes de bloque en plantillas JSON solo permiten **1 filtro** en una fuente dinámica; `split | first` usa 2 → error 422. Por eso va en archivos `.liquid` (sin ese límite).

### Cómo re-aplicarlo en un tema nuevo
1. Confirmar si el tema nuevo ya muestra la descripción de colección (muchos tienen toggle "Mostrar descripción de la colección" en Personalizar). Si lo muestra entero, solo faltaría separar la FAQ abajo.
2. Si no, recrear las dos secciones de arriba (copiar el liquid) y añadirlas a la plantilla de colección en el orden indicado.
3. Backups del `templates/collection.json` original en `content/theme_backups/`.
4. El script que lo montó: `scripts/collection_faq_sections.py` (usa el token de `.env.local`).

---

## 2. Acceso al tema (cómo editarlo por código)

- Se edita por **Admin API** (no por CLI — el CLI usa una sesión de otra tienda sin acceso). Ver `PROYECTO.md §2`.
- Token con permisos de tema (`read_themes`/`write_themes`): **`.env.local`** (`shpat_…`). El de catálogo (`.env`, `shpca_…`) **no** sirve para temas.
- REST: `/admin/api/2026-01/themes/188231123268/assets.json` (GET con `?asset[key]=...`, PUT con `{"asset":{"key":...,"value":...}}`).

---

## 3. Gotchas (cosas que despistan)

- **Los `<meta>` del tema van en varias líneas** (`<meta\n name=...\n content=...>`). Un `grep '<meta name="description"'` de una sola línea da falso negativo. Usar regex multilínea para verificar. La meta description **sí funciona** (sale de `page_description` = SEO description de la página).
- **GTIN en Merchant NO es un problema** para mobiliario: Google lo acepta sin código de barras si hay marca. No inventar GTINs.
- **Cuenta Merchant correcta = `5781655181`** (santavila.com). Ignorar la `515612993` (agencia).
- **Aviso `language_mismatch` en Merchant** = Mercados de Shopify internacionales publicando el catálogo español en inglés. Se arregla en **Shopify → Mercados** (no es código).
- **Nombre de empresa visible en Merchant** debe ser **Santavila** (Información empresarial); la razón social `Ubicuo Libres Pensadores S.L.` es solo dato legal.

---

## 4. Pendiente que también tocará el tema (para no olvidar)

- **FAQPage schema (JSON-LD)** de las FAQ de colección/producto → se añadirá en el tema; **se perderá** al cambiar de theme, re-aplicar.
- Breadcrumbs, ItemList y otros schema que se decidan → igual, son del tema.
- `llms.txt` ampliado → vive en Shopify (template/redirect), confirmar si depende del tema al migrar.
