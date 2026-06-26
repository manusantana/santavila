# GEO Schema Report - Santavila

Fecha: 2026-06-24

## Estado aplicado

Sprint 3 aplicado en theme DEV `189114876228` y LIVE `189222715716`.

Assets modificados:

- `theme/snippets/santavila-schema.liquid`
- `theme/layout/theme.liquid`
- `theme/sections/header.liquid`

## Antes

- Home: `Organization` basico.
- Coleccion: `Organization` basico + `FAQPage`.
- PDP: `Organization` basico + `Product` de Shopify.
- Pagina: `Organization` basico.

Problema principal: el `Organization.url` se generaba con la URL de la pagina actual, no con la home canonica. Faltaban `BreadcrumbList` y `ItemList`.

## Despues

### Global

Se emite una entidad unica:

- `@type`: `Organization` + `OnlineStore`
- `@id`: `https://santavila.com#organization`
- `url`: `https://santavila.com`
- `email`: `hola@santavila.com`
- `areaServed`: España
- `contactPoint`: customer support en ES
- `hasPart`: paginas de confianza:
  - `/pages/sobre-santavila`
  - `/pages/envio`
  - `/pages/garantia`
  - `/pages/mantenimiento`
  - `/pages/contacto`

### BreadcrumbList

Se emite en todas las paginas salvo home:

- Coleccion: Inicio -> Coleccion
- PDP: Inicio -> primera coleccion del producto -> Producto
- Pagina: Inicio -> Pagina
- Blog/articulo: Inicio -> Blog -> Articulo

### ItemList

Se emite en colecciones:

- `@type`: `ItemList`
- `@id`: `canonical_url#itemlist`
- `numberOfItems`: total de productos de la coleccion
- `itemListElement`: hasta 24 productos visibles

### FAQPage

Se mantiene la emision existente en colecciones desde `santavila-collection-faq.liquid`. No se duplico.

### Product

Se mantiene el `Product` nativo emitido por Shopify en `santavila-product.liquid`.

## Verificacion publica

URLs verificadas con `curl` y parseo JSON-LD:

- `https://santavila.com/`
  - `Organization` + `OnlineStore`
- `https://santavila.com/collections/sillones-de-exterior`
  - `Organization` + `OnlineStore`
  - `BreadcrumbList`
  - `ItemList`
  - `FAQPage`
- `https://santavila.com/products/base-de-parasol-25-kg`
  - `Organization` + `OnlineStore`
  - `BreadcrumbList`
  - `Product`
- `https://santavila.com/pages/sobre-santavila`
  - `Organization` + `OnlineStore`
  - `BreadcrumbList`

## Notas

- El `Product.@id` de Shopify sigue siendo relativo (`/products/...#product`). No se ha tocado para evitar sobreescribir schema nativo en este sprint.
- Para `AggregateRating` esperaremos a tener reviews reales.
- Para `sameAs` conviene añadir perfiles sociales oficiales cuando esten creados o confirmados.

## Siguiente paso recomendado

Sprint 4: guias citables con `Article` + `FAQPage`, empezando por materiales, lluvia/sol y mantenimiento.
