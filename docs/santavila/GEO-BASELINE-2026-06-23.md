# GEO Baseline Santavila — 2026-06-23

## Estado del Sprint 0

Sprint 0 ejecutado sobre:

- Sitio publico: `https://santavila.com`
- Repo local: `Santavila`
- Fecha: 2026-06-23
- Referencias previas: `GEO-AUDIT-REPORT.md`, `SEO-BASELINE.md`, `KEYWORD-RESEARCH.md`

Resultado corto: Santavila ha mejorado desde la auditoria del 2026-05-30. Ya hay contenido en colecciones, FAQPage en colecciones, blog editorial con Article + FAQPage y PDP con descripciones mas completas. El bloqueo inicial de Search Console quedo resuelto durante el Sprint 0 reautorizando OAuth con `.venv/bin/python scripts/google_auth.py`.

## Search Console

OAuth reautorizado correctamente:

```bash
.venv/bin/python scripts/google_auth.py
.venv/bin/python scripts/gsc_baseline.py
```

Resultado de verificacion:

- `sc-domain:santavila.com` aparece como `siteOwner`.
- `SEO-BASELINE.md` actualizado el 2026-06-23.
- GA4 no se pudo verificar porque `analyticsadmin.googleapis.com` esta deshabilitada en el proyecto GCP `998987187130`. Esto no bloquea Search Console.

Rendimiento GSC de los ultimos 28 dias (`2026-05-26` -> `2026-06-22`):

- Clics: 9.
- Impresiones: 630.
- CTR: 1,43%.
- Posicion media: 15,9.

Sitemaps:

- `https://santavila.com/sitemap.xml`: registrado, errores 0, warnings 0.
- `http://santavila.com/sitemap.xml`: aun registrado, errores 0, warnings 8. Conviene retirar o ignorar si no afecta, pero la version canonica correcta ya es HTTPS.

Comandos ejecutados:

```bash
.venv/bin/python scripts/gsc_baseline.py
.venv/bin/python scripts/gsc_opportunities.py
```

## Rastreo publico

### HTTP / tecnico

- Home responde `200`.
- `content-language: es-ES`.
- Shopify sirve SSR publico.
- HTTPS, HSTS, `x-content-type-options: nosniff`, `x-frame-options: DENY`.
- Sitemap declarado en robots: `https://santavila.com/sitemap.xml`.

### Robots

`https://santavila.com/robots.txt` permite rastreo publico general:

- `User-agent: *`
- `Allow: /`
- Bloquea zonas transaccionales privadas: `/admin`, `/cart/`, `/checkout`, `/account`, `/orders`, etc.
- Declara endpoints agenticos: `/agents.md`, `/.well-known/ucp`, `/api/ucp/mcp`.

Lectura GEO: correcto. No hay bloqueo a GPTBot/ClaudeBot/PerplexityBot por user-agent especifico.

### llms.txt / agents

`https://santavila.com/llms.txt` existe y replica instrucciones para agentes de compra. Esta bien para comercio agentico, pero sigue siendo debil como guia de contenido:

- lista UCP, MCP, Shop skill y politicas;
- no lista colecciones principales;
- no lista guias editoriales;
- no prioriza paginas que queremos que una IA lea/cite.

### UCP

`https://santavila.com/.well-known/ucp` responde `200` y expone version `2026-04-08`.

Detalle a revisar: el discovery devuelve endpoints sobre `https://mueblesexterior.myshopify.com/...` en vez de `https://santavila.com/...`. Puede ser normal en Shopify, pero conviene validar si queremos consistencia total de marca/dominio para agentes.

## Sitemap actual

Sitemap raiz:

- `sitemap_agentic_discovery.xml`
- `sitemap_products_1.xml`
- `sitemap_pages_1.xml`
- `sitemap_collections_1.xml`
- `sitemap_blogs_1.xml`

Colecciones indexadas:

| Coleccion | URL |
|---|---|
| Frontpage | `/collections/frontpage` |
| Accesorios | `/collections/accesorios` |
| Tumbonas | `/collections/tumbonas` |
| Mesas | `/collections/mesas` |
| Sofas / sillones | `/collections/sillones-de-exterior` |
| Sillas | `/collections/sillas-de-exterior` |
| Parasoles | `/collections/parasoles` |

Paginas indexadas:

| Pagina | URL |
|---|---|
| Contacto | `/pages/contacto` |

Blogs indexados:

- `/blogs/news`
- guia materiales: aluminio, teca, ratan sintetico;
- guia mantenimiento;
- ideas decoracion terraza;
- hosteleria;
- tendencias 2026;
- terraza pequena.

Lectura: el contenido editorial que Sprint 4 proponia ya esta parcialmente arrancado. Falta conectarlo mejor con colecciones/PDP y ampliar paginas de confianza.

## Muestra HTML analizada

URLs muestreadas:

- `/`
- `/collections/sillas-de-exterior`
- `/collections/sillones-de-exterior`
- `/collections/tumbonas`
- `/collections/mesas`
- `/collections/parasoles`
- `/pages/contacto`
- `/products/sillon-exterior-aluminio-estilo-envolvente-9890-cm`
- `/products/set-jardin-aluminio-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa`
- `/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico`

| URL tipo | Words aprox. | Title/meta | H1 | Schema |
|---|---:|---|---|---|
| Home | 824 | Title `santavila`; sin meta description | `santavila` + hero H1 | Organization |
| Sillas | 678 | Title + meta OK | `Sillas de exterior` | Organization, FAQPage |
| Sofas | 727 | Title + meta OK | `Sofas de exterior` | Organization, FAQPage |
| Tumbonas | 650 | Title + meta OK | `Tumbonas` | Organization, FAQPage |
| Mesas | 719 | Title + meta OK | `Mesas de exterior` | Organization, FAQPage |
| Parasoles | 636 | Title + meta OK | `Parasoles` | Organization, FAQPage |
| Contacto | 458 | Title + meta larga | sin H1 detectado | Organization |
| PDP sillon | 664 | Title + meta OK | producto | Organization, Product |
| PDP set | 695 | Title + meta OK | producto | Organization, Product |
| Blog materiales | 1039 | Title + meta OK | articulo | Organization, Article, FAQPage |

## Cambios positivos desde la auditoria previa

- Colecciones ya no estan vacias: tienen texto introductorio y FAQ.
- Colecciones principales tienen meta description.
- Blog ya contiene articulos citables con schema `Article` y `FAQPage`.
- PDP top ya tienen descripciones mas robustas que las 25 palabras detectadas en mayo.
- El theme Santavila actual ya incorpora bloques de confianza en home y PDP.
- Sitemap de blog contiene 6 URLs editoriales.

## Brechas actuales

### Criticas / altas

- GSC no actualizado por token OAuth invalido.
- Home sin meta description.
- Solo hay una pagina de contenido indexada en `sitemap_pages_1.xml`: contacto. Faltan paginas propias de confianza tipo sobre Santavila, entrega, garantia, mantenimiento.
- `llms.txt` no lista contenido citable ni colecciones clave, pero parece generado por Shopify (`LlmsTxtController`), no por el theme.
- Colecciones no muestran `BreadcrumbList` ni `ItemList` en la muestra HTML.
- PDP muestran `Product`, pero sin `AggregateRating`, `Review`, `shippingDetails` o `hasMerchantReturnPolicy`.
- Muchas fichas siguen finas en datos locales: 190 de 243 con menos de 80 palabras; 13 con 0 palabras.

### Medias

- H1 de la coleccion de sofas sale como `Sofas de exterior`, sin tilde.
- Handle de sofas sigue siendo `/collections/sillones-de-exterior`; decidir si se mantiene por compatibilidad o se migra a `/collections/sofas-de-exterior` con 301.
- `/.well-known/ucp` devuelve endpoints sobre `mueblesexterior.myshopify.com`; revisar consistencia de marca.
- Contacto no tiene H1 detectado en HTML.
- Producto schema usa `brand` del proveedor (`Hevea`/`Balliu`). Esto puede ser correcto como fabricante, pero Santavila necesita reforzar su entidad como seller/merchant.

## Productos prioritarios por margen local

Fuente: `audit_financiero.csv`, ordenado por `net_eur`.

| Prioridad | Handle | Precio | Margen neto aprox. |
|---:|---|---:|---:|
| 1 | `set-jardin-aluminio-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa` | 5249 | 1495 |
| 2 | `set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-2` | 4709 | 1342 |
| 3 | `set-jardin-aluminio-2-plazas-contemporaneo-sofa-2-plazas-2-sillones-mesa` | 4679 | 1283 |
| 4 | `set-jardin-bicolor-3-plazas-bicolor-sofa-3-plazas-2-sillones-mesa` | 4405 | 1254 |
| 5 | `set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-2` | 4345 | 1237 |
| 6 | `set-rinconera-exterior-hpl-moderno-sofa-de-esquina-mesa-de-centro` | 4225 | 1204 |
| 7 | `set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa` | 4195 | 1196 |
| 8 | `set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-5` | 4175 | 1188 |
| 9 | `set-jardin-bicolor-2-plazas-bicolor-sofa-2-plazas-2-sillones-mesa` | 3965 | 1129 |
| 10 | `set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-2` | 3825 | 1090 |

Lectura: para Sprint 1 conviene priorizar conjuntos/sets y rinconeras, porque concentran margen y encajan con la coleccion nueva sugerida `conjuntos`.

## Fichas finas detectadas localmente

Fuente: `auditoria_fichas_report.csv`.

- Total auditadas: 243.
- Sin descripcion: 13.
- Menos de 80 palabras: 190.
- Sin SEO description: 14.
- Sin imagen principal en reporte local: 16.

Primeras fichas sin descripcion:

- `tumbona-carmen-tablillas`
- `tumbona-lola-tablillas`
- `mesa-exterior-aluminio-hpl-120x80-capri-doble`
- `mesa-de-centro-exterior-aluminio-hpl-gd-110x60`
- `mesa-auxiliar-exterior-aluminio-hpl-gd-45x45-etna`
- `mesa-auxiliar-exterior-aluminio-werzalit-60-etna`
- `mesa-exterior-aluminio-hpl-gd-brunei`
- `mesa-extensible-exterior-aluminio-hpl-gd-java`
- `mesa-exterior-aluminio-hpl-gd-capri`
- `mesa-exterior-aluminio-hpl-gd-120x80-capri-doble`
- `mesa-exterior-aluminio-altea-extras`
- `mesa-exterior-aluminio-agata-extras`
- `silla-exterior-resina-bruna-precio-alto-pendiente`

## Backlog GEO estable

| ID | Prioridad | Tarea | Entrega |
|---|---|---|---|
| GEO-00 | P0 | Reautorizar Google OAuth y regenerar GSC baseline | `SEO-BASELINE.md` actualizado + output de `gsc_opportunities.py` |
| GEO-01 | P0 | Anadir meta description de home | Hecho en theme local |
| GEO-02 | P1 | Corregir H1 `Sofas` -> `Sofás` en coleccion | Hecho en theme local; handle pendiente de decision |
| GEO-03 | P1 | Crear/reforzar paginas Sobre, Entrega, Garantia, Mantenimiento | URLs indexables y enlazadas |
| GEO-04 | P1 | Auditar `llms.txt`/`agents.md`/UCP generados por Shopify y complementar discoverability con contenido, sitemap y enlazado | Hecho: `GEO-AGENTIC-ENDPOINTS-REPORT.md` |
| GEO-05 | P1 | Implementar schema `BreadcrumbList` + `ItemList` en colecciones | Validacion schema |
| GEO-06 | P1 | Enriquecer schema Product con seller/shipping/returns cuando sea viable | PDP top con schema ampliado |
| GEO-07 | P1 | Crear coleccion `conjuntos` o landing equivalente | URL para sets de alto margen |
| GEO-08 | P1 | Reescribir 15 PDP top por margen/intencion | Fichas citables >150 palabras |
| GEO-09 | P2 | Resolver 13 fichas con 0 palabras | 0 productos sin descripcion |
| GEO-10 | P2 | Revisar consistencia UCP dominio Santavila vs myshopify | Decision documentada |

## Siguiente bloque recomendado

1. Preparar Sprint 1 real sobre:
   - coleccion/landing `conjuntos`;
   - 10 productos top por margen;
   - paginas de confianza indexables.
2. Priorizar las oportunidades GSC detectadas:
   - pergola 250x300;
   - sofas por medida;
   - banco con mesa incorporada;
   - tumbonas resina/Balliu.
