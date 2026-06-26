# GEO Agentic Endpoints Report — Santavila

**Fecha:** 2026-06-23

## Resumen

Santavila ya expone endpoints agenticos nativos de Shopify:

- `https://santavila.com/llms.txt`
- `https://santavila.com/agents.md`
- `https://santavila.com/.well-known/ucp`
- `https://santavila.com/api/ucp/mcp`

La conclusion operativa es clara: **no debemos tratar `llms.txt` como un fichero editable del theme**. En Santavila responde como endpoint generado por Shopify (`pageType=llms_txt`, `LlmsTxtController`) y no aparece en el theme local como template, asset o snippet.

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
