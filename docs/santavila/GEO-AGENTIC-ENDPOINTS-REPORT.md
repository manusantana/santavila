# GEO Agentic Endpoints Report — Santavila

**Fecha:** 2026-06-23
**Reauditoria:** 2026-06-27

## Resumen

Santavila ya expone endpoints agenticos nativos de Shopify:

- `https://santavila.com/llms.txt`
- `https://santavila.com/agents.md`
- `https://santavila.com/.well-known/ucp`
- `https://santavila.com/api/ucp/mcp`

La conclusion operativa es clara: **no debemos tratar `llms.txt` como un fichero editable del theme**. En Santavila responde como endpoint generado por Shopify (`pageType=llms_txt`, `LlmsTxtController`) y no aparece en el theme local como template, asset o snippet.

Reauditoria 2026-06-27:

- `https://santavila.com/llms.txt` responde `200`.
- `https://santavila.com/agents.md` responde `200`.
- `https://santavila.com/.well-known/ucp` responde `200`.
- `https://santavila.com/sitemap.xml` responde `200`.
- `https://santavila.es/llms.txt` redirige `301` a `https://santavila.com/llms.txt`.
- `https://www.santavila.es/llms.txt` redirige `301` a `https://santavila.com/llms.txt`.
- `https://santavila.es/.well-known/ucp` redirige `301` a `https://santavila.com/.well-known/ucp`.

## Evidencias

### `llms.txt`

Cabeceras observadas:

- Status: `200`.
- Content-Type: `text/markdown; charset=utf-8`.
- `server-timing` incluye `pageType;desc="llms_txt"`.
- `etag` incluye `LlmsTxtController`.

Contenido actual:

- Replica instrucciones para agentes.
- Recomienda Shop skill.
- Explica UCP/MCP.
- Lista endpoints de browsing y politicas.
- Describe la tienda en `https://santavila.com`.
- Indica que `/agents.md` es la descripcion canonica para agentes.

Lectura GEO:

- Correcto para comercio agentico y compra asistida.
- No esta pensado como indice editorial de colecciones/guias.
- No conviene intentar sobreescribirlo desde Liquid salvo que Shopify publique una via soportada.

### `agents.md`

Cabeceras observadas:

- Status: `200`.
- Content-Type: `text/markdown; charset=utf-8`.
- `server-timing` incluye `pageType;desc="agents_md"`.
- `etag` incluye `AgentsMdController`.

Lectura:

- Endpoint nativo de instrucciones para agentes.
- Consistente con `llms.txt`.
- Se presenta como descripcion canonica agent-facing de la tienda.

### `/.well-known/ucp`

Status: `200`.

Expone:

- version `2026-04-08`;
- capacidades UCP shopping/catalog/cart/checkout/order;
- MCP endpoint;
- payment handlers.

Observacion:

- El discovery devuelve varios endpoints con dominio `mueblesexterior.myshopify.com` en lugar de `santavila.com`.
- Puede ser comportamiento normal de Shopify, pero conviene revisarlo si buscamos consistencia completa de marca/dominio para agentes.
- El `merchant_origin` de Google Pay aparece como `santavila.com`, lo que compensa parcialmente la observacion anterior desde el punto de vista de marca.

### `robots.txt`

Status: `200`.

Lectura:

- Declara `Agent instructions: https://santavila.com/agents.md`.
- Declara `UCP discovery: https://santavila.com/.well-known/ucp`.
- Declara `UCP/MCP endpoint: https://santavila.com/api/ucp/mcp`.
- Mantiene `Sitemap: https://santavila.com/sitemap.xml`.
- Permite rastreo publico general y bloquea superficies privadas/transaccionales.

### Dominio canonico

Reauditoria 2026-06-27:

- `santavila.es` redirige con `301` por `primary_domain_redirection`.
- `www.santavila.es` redirige con `301` por `primary_domain_redirection`.
- Los endpoints agenticos probados terminan en `santavila.com`.

Lectura:

- Correcto para evitar duplicidad entre `.es` y `.com`.
- Correcto para señales agenticas: los documentos publicos se concentran en el dominio primario.

## Documentacion Shopify revisada

Shopify documenta su capa de agentic commerce y Storefront Catalog MCP:

- https://shopify.dev/docs/agents
- https://shopify.dev/docs/agents/catalog/storefront-catalog

La documentacion confirma que Shopify expone herramientas UCP/MCP para descubrimiento de catalogo, carrito, checkout y pedidos. No se ha encontrado en la documentacion oficial una via para editar manualmente `llms.txt` desde el theme.

## Decision para GEO-04

`GEO-04` queda redefinido:

Antes:

- Editar/ampliar `llms.txt` con colecciones, guias y paginas clave.

Ahora:

- Auditar `llms.txt`, `agents.md` y UCP generados por Shopify.
- No sobrescribir endpoints nativos.
- Complementar discoverability mediante elementos que si controlamos:
  - meta description de home;
  - paginas de confianza indexables;
  - colecciones con contenido citable;
  - guias editoriales;
  - schema;
  - sitemap limpio;
  - enlazado interno.

## Acciones recomendadas

1. Mantener `llms.txt` y `agents.md` como endpoints Shopify.
2. Validar periodicamente que responden `200`.
3. Revisar si el uso de `mueblesexterior.myshopify.com` en UCP discovery afecta a marca o agentes.
4. Priorizar contenido/sitemap/schema por encima de tocar endpoints nativos.
5. Documentar cualquier cambio futuro de Shopify si publica soporte explicito para personalizar `llms.txt`.

## Estado Sprint 6

Estado: validado el 2026-06-27.

Resultado:

- La capa agentica nativa de Shopify esta activa.
- El dominio canonico se comporta bien.
- No hay cambios de theme recomendados para `llms.txt`/`agents.md`.
- Las mejoras GEO deben seguir por contenido, schema, reviews, menciones y enlazado interno.
