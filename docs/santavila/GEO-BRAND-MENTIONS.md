# GEO Brand Mentions - Santavila

Fecha: 2026-06-27

## Objetivo

Construir senales externas verificables para que Santavila deje de depender solo de santavila.com:

- perfiles sociales basicos;
- perfiles de reviews;
- menciones editoriales realistas;
- piezas visuales reutilizables;
- `sameAs` en schema cuando existan URLs reales.

## Estado actual

Revision rapida realizada el 2026-06-27:

- No hay URLs publicas verificadas de Instagram, Pinterest, YouTube o LinkedIn en el theme.
- El footer `theme/sections/santavila-footer.liquid` ya soporta Instagram y Pinterest si se configuran en el editor.
- El schema `theme/snippets/santavila-schema.liquid` no incluye `sameAs`, decision correcta hasta tener perfiles reales.
- Busquedas web por perfiles publicos de Santavila no devolvieron resultados fiables.

## Google Business Profile

Estado: pendiente de decision.

Google indica que un Business Profile aplica a negocios con una ubicacion fisica visitable por clientes o que se desplazan al cliente. Tambien pide representar el negocio de forma precisa, usar nombre real, direccion/area de servicio precisa y evitar perfiles duplicados.

Decision recomendada:

- Crear Google Business Profile solo si Santavila tiene una ubicacion atendida, showroom, oficina visitable, almacen/oficina con senalizacion y horario, o servicio real de desplazamiento al cliente.
- Si Santavila es ecommerce puro sin atencion presencial ni servicio local, no forzar GBP.
- Si existe direccion operativa pero no se atiende al publico, evaluar perfil de area de servicio solo si se presta servicio presencial real.

Fuente:

- Google Business Profile Guidelines: https://support.google.com/business/answer/3038177

## Perfiles sociales minimos

Prioridad 1:

| Canal | Handle recomendado | Estado | Uso GEO |
|---|---|---|---|
| Pinterest | `santavila` o `santavila_es` | Pendiente | Descubrimiento visual, guias, tableros por espacio/material |
| Instagram | `santavila` o `santavila.es` | Pendiente | Prueba de marca, reels cortos, carruseles de guias |
| LinkedIn | `Santavila` | Pendiente | Credibilidad corporativa y B2B/hosteleria |
| YouTube | `@santavila` o `@santavila_es` | Pendiente | Shorts de guias y mantenimiento |

Prioridad 2:

| Canal | Estado | Uso |
|---|---|---|
| TikTok | Opcional | Clips cortos si hay capacidad creativa |
| Houzz | A evaluar | Autoridad en decoracion/reformas si encaja mercado ES |
| Facebook | Opcional | Solo si se usara para GBP/Meta/ads o atencion |

## Configuracion recomendada de cada perfil

Nombre:

- `Santavila`

Bio corta:

- `Muebles de exterior para terrazas, jardines y porches en España. Guías claras sobre materiales, medidas, mantenimiento y compra segura.`

URL:

- `https://santavila.com`

Email publico:

- `hola@santavila.com`

Categorias/keywords:

- muebles de exterior;
- mobiliario de terraza;
- jardin y piscina;
- sofas de exterior;
- tumbonas;
- mesas de exterior;
- mantenimiento de muebles de exterior.

## Tableros de Pinterest recomendados

Crear 8 tableros iniciales:

1. `Muebles de exterior para terraza`
2. `Terrazas pequenas y balcones`
3. `Tumbonas para piscina y jardin`
4. `Mesas de exterior: medidas e ideas`
5. `Materiales de exterior: aluminio, resina, HPL y madera`
6. `Mantenimiento de muebles de exterior`
7. `Parasoles y sombra para jardin`
8. `Porches y comedores exteriores`

Primeras piezas a pinear:

- portada de cada una de las 6 guias GEO;
- 3 productos por coleccion principal;
- 2 comparativas visuales por material;
- 2 checklists: mantenimiento y medidas de mesa.

Pack operativo:

- `docs/santavila/GEO-SOCIAL-CONTENT-PACK.md`

## Calendario de contenido reutilizable

Partir de las 6 guias citables publicadas:

| Guia | Pinterest | Instagram | YouTube Shorts |
|---|---|---|---|
| Lluvia y sol | checklist de materiales | carrusel 5 errores | short `que material aguanta mejor` |
| Materiales | tabla aluminio/resina/HPL/madera | carrusel comparativo | short `aluminio vs resina` |
| Mantenimiento | checklist temporada | carrusel limpieza por material | short `3 cosas que no hacer` |
| Terraza pequena | layout por m2 | carrusel antes/despues | short `balcon estrecho` |
| Mesas | tabla comensales | carrusel medidas 2/4/6/8 | short `mesa para 6 personas` |
| Tumbonas | comparativa aluminio/resina/madera | carrusel piscina/costa | short `mejor tumbona piscina` |

## Reviews

Estado: pendiente de elegir plataforma.

Opciones:

- Shopify Product Reviews / app de reviews integrada: mejor para PDP y conversion.
- Trustpilot: mejor para senal externa si se va a pedir review de forma sistematica.
- Google reviews: solo si GBP es elegible.

Recomendacion:

1. Elegir una plataforma principal.
2. Configurar flujo post-compra.
3. No simular testimonios ni estrellas.
4. Cuando existan reviews reales, evaluar `AggregateRating` solo en PDPs con datos verificables.

## Menciones externas realistas

Objetivo inicial: 3-5 menciones en 60-90 dias.

Targets por tipo:

| Tipo | Ejemplos de pitch | Activo a ofrecer |
|---|---|---|
| Blogs de decoracion | `como preparar una terraza pequena` | guia + imagenes propias |
| Reformas/interiorismo | `materiales que aguantan exterior` | tabla de materiales |
| Jardineria/paisajismo | `muebles para piscina y porche` | guia lluvia/sol |
| Hosteleria local | `mobiliario exterior facil de mantener` | checklist mantenimiento |
| Medios regionales | `marca espanola de mobiliario exterior online` | historia de marca |

Pitch base:

```text
Hola, soy [nombre] de Santavila.

Estamos construyendo una guia practica sobre mobiliario exterior para terrazas reales en Espana: materiales, medidas, mantenimiento y errores habituales antes de comprar.

Creo que podria encajar con vuestro contenido sobre [tema concreto]. Podemos aportar una tabla breve, consejos contrastados y ejemplos visuales sin coste, citando a Santavila como fuente.

Te dejo una guia de referencia:
[URL guia relevante]

Gracias,
[firma]
```

## Directorios y marketplaces sectoriales

No publicar en directorios de baja calidad. Priorizar sitios donde el perfil aporte contexto real y enlace limpio.

Lista a evaluar:

- Houzz España;
- Habitissimo, si encaja como proveedor/decoracion y no fuerza servicios que no se prestan;
- directorios de decoracion/interiorismo con ficha editorial;
- asociaciones o blogs sectoriales de jardin/terraza;
- marketplaces solo si no diluyen marca ni duplican catalogo de forma conflictiva.

## Schema `sameAs`

Estado: pendiente.

Cuando existan perfiles reales y publicados, actualizar `theme/snippets/santavila-schema.liquid`:

```json
"sameAs": [
  "https://www.instagram.com/...",
  "https://www.pinterest.es/...",
  "https://www.linkedin.com/company/...",
  "https://www.youtube.com/@..."
]
```

Validacion:

- El perfil debe estar publico.
- El perfil debe enlazar a `https://santavila.com` o mostrar marca clara.
- No incluir perfiles vacios o reservados sin contenido.
- Revalidar JSON-LD en home tras publicar.

## Acciones inmediatas

1. Confirmar si Santavila tiene ubicacion/servicio elegible para Google Business Profile.
2. Reservar handles sociales.
3. Crear bio y visuales base.
4. Publicar 6-12 piezas iniciales en Pinterest e Instagram.
5. Elegir plataforma de reviews.
6. Preparar 10 contactos de menciones externas.
7. Cuando haya URLs reales, actualizar `sameAs` y footer.

## Estado de Sprint 5

Estado: iniciado.

Bloque completado:

- Documento operativo de menciones y perfiles creado.
- Pack de piezas sociales iniciales creado.
- Criterio GBP revisado contra guia oficial.
- Theme auditado: soporte footer para Instagram/Pinterest existe; `sameAs` pendiente hasta tener URLs verificadas.

Siguiente paso:

- Usuario debe confirmar/crear perfiles externos o facilitar URLs.
- Con URLs reales, se puede aplicar `sameAs` y enlazado footer en el theme.
