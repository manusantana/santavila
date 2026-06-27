# GSC Opportunities Santavila — 2026-06-23

Ventana analizada: `2026-03-25` -> `2026-06-22`.

Fuente: `.venv/bin/python scripts/gsc_opportunities.py`.

## Lectura rapida

Santavila todavia tiene poco volumen, pero ya aparecen senales accionables:

- Home capta branded (`santavila`, `santa vila`) y algunas consultas genericas muy tempranas (`muebles exteriores`, `muebles vigo`).
- Hay traccion clara en productos de tumbonas Balliu/resina, aunque muy lejos del top 10.
- Hay oportunidades cercanas en sofa por medidas (`sofa terraza 120 cm`, `sofa exterior 130 cm`).
- La mejor oportunidad no branded inmediata es `pérgola 250x300` en posicion media 13,9.
- El producto `banco jardin con mesa integrada 220 cm` ya aparece muy arriba para `banco con mesa incorporada`.

## Striking Distance

Queries en posicion 4-20 con impresiones:

| Query | Impresiones | Posicion | URL |
|---|---:|---:|---|
| `pérgola 250x300` | 7 | 13,9 | `/products/pergola-aluminio-para-jardin-300300250-cm` |
| `sofa terraza 120 cm` | 4 | 11,2 | `/products/sofa-terraza-2-plazas-es...` |
| `sofa exterior 130 cm` | 4 | 14,0 | `/products/sofa-terraza-2-plazas-es...` |
| `sofa bicolor` | 2 | 15,5 | `/products/sofa-terraza-bicolor-2-p...` |
| `acrylic patio umbrella` | 2 | 17,5 | `/products/balliu-parasol-para-terr...` |
| `pergola 250x300` | 2 | 19,5 | `/products/pergola-aluminio-para-jardin-300300250-cm` |
| `banco con mesa` | 1 | 5,0 | `/products/banco-jardin-con-mesa-in...` |
| `tumbona balliu` | 1 | 9,0 | `/products/balliu-tumbona-de-exteri...` |
| `terraza sofa` | 1 | 9,0 | `/products/sofa-terraza-2-plazas-es...` |
| `find the look` | 1 | 10,0 | `/products/sofa-terraza-3-plazas-es...` |
| `pergola 300 x 250` | 1 | 19,0 | `/products/pergola-aluminio-para-jardin-300300250-cm` |

Nota: se omiten aqui las multiples filas branded `santavila`, porque ayudan a confirmar indexacion pero no orientan tanto el Sprint GEO.

## Paginas con mas senal

| Pagina | Impresiones | Lectura |
|---|---:|---|
| `/` | 59 | Branded fuerte y primeras senales genericas. Home necesita meta description. |
| `/products/balliu-tumbona-de-exterior-resina-28ff014d` | 35 | Cluster tumbonas/resina profesional. Reforzar contenido y enlazar desde coleccion. |
| `/products/balliu-tumbona-de-exterior-resina-75-cm-009e68e4` | 17 | Cluster Balliu/tumbonas. |
| `/products/set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro` | 17 | Cluster rinconeras jardin/terraza, aun lejos. |
| `/products/balliu-tumbona-de-exterior-aluminio-d08586c1` | 16 | Cluster Balliu/tumbonas aluminio. |
| `/products/pergola-aluminio-para-jardin-300300250-cm` | 10 | Oportunidad clara por medida. |
| `/products/banco-jardin-con-mesa-integrada-220-cm` | 8 | Muy buena posicion para "banco con mesa incorporada". |
| `/products/base-de-parasol-25-kg` | 7 | Traccion en base/parasol/sombrilla, aunque posiciones muy bajas. |

## Acciones derivadas

### Prioridad 1

- Optimizar la ficha de pergola para variantes de query:
  - `pérgola 250x300`
  - `pergola 250x300`
  - `pergola 300 x 250`
- Reforzar PDP de sofa por medida:
  - `sofa terraza 120 cm`
  - `sofa exterior 120 cm`
  - `sofa exterior 130 cm`
- Convertir `banco con mesa incorporada` en mini landing o bloque FAQ dentro del PDP, porque ya rankea alto.

### Prioridad 2

- Agrupar y enlazar mejor el cluster `tumbonas Balliu`, `tumbonas resina`, `tumbonas jardin resina`.
- Crear/reforzar contenido de coleccion `tumbonas` con secciones por material:
  - resina;
  - aluminio;
  - piscina;
  - profesional/hosteleria.
- Revisar si conviene capturar `hamacas balliu` con copy aclaratorio, aunque semanticamente el producto sea tumbona.

### Prioridad 3

- Crear/reforzar contenido para `rinconera terraza`, `rinconera jardin`, `sofa rinconera terraza`.
- Revisar oportunidades en `base parasol`, `base para sombrilla`, `losas para sombrilla`.
- Home: mejorar snippet para aumentar CTR branded y generico temprano.

## Integracion con backlog GEO

- `GEO-01`: meta description home.
- `GEO-07`: coleccion/landing de conjuntos puede incluir sets y rinconeras.
- `GEO-08`: PDP top debe incluir pergola, sofa por medida, banco con mesa y cluster tumbonas.
- `GEO-09`: resolver fichas finas, especialmente si ya tienen impresiones.

## Sprint 1 aplicado - 2026-06-24

Fuente de ejecucion: `.venv/bin/python scripts/apply_gsc_opportunity_descriptions.py --apply`.

Estado: aplicado en Shopify Admin API sin errores tras reintento por corte SSL puntual.

Fichas actualizadas:

- `/products/pergola-aluminio-para-jardin-300300250-cm` - descriptionHtml y meta description orientadas a `pérgola 250x300`, `pergola 250x300` y `pergola 300 x 250`.
- `/products/sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm` - bloque de descripcion y meta para `sofa terraza 120 cm`.
- `/products/sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm` - bloque de descripcion y meta para `sofa exterior 130 cm`.
- `/products/banco-jardin-con-mesa-integrada-220-cm` - refuerzo de `banco con mesa incorporada` y `banco con mesa`.
- `/products/balliu-tumbona-de-exterior-resina-28ff014d` - refuerzo cluster tumbona exterior/resina/Balliu.
- `/products/balliu-tumbona-de-exterior-resina-75-cm-009e68e4` - refuerzo cluster tumbona exterior/resina/75 cm/Balliu.
- `/products/balliu-tumbona-de-exterior-aluminio-d08586c1` - refuerzo cluster tumbona exterior/aluminio/Balliu.
- `/products/base-de-parasol-25-kg` - refuerzo `base parasol`, `base para sombrilla` y `base de parasol 25 kg`.

Backups generados antes de escribir:

- `content/descriptions/backup_gsc_opportunities_20260624-063513.json` - snapshot dry-run.
- `content/descriptions/backup_gsc_opportunities_20260624-063613.json` - snapshot previo a la aplicacion final.

Nota tecnica: `santavila.es` resolvio a una pagina aparcada de Hostinger durante una comprobacion inicial, pero el dominio de GSC es `santavila.com` y este si apunta a Shopify (`23.227.38.x`). Verificacion publica confirmada en `santavila.com` para pergola y base de parasol: los textos aparecen en meta/OG y JSON-LD de producto.

## Sprint 1.2 aplicado - 2026-06-24

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_collections.py --apply`
- `.venv/bin/python scripts/push_theme_assets.py --theme 189114876228 sections/santavila-collection-grid.liquid`
- `.venv/bin/python scripts/push_theme_assets.py --theme 189222715716 sections/santavila-collection-grid.liquid`

Estado: aplicado en Shopify Admin API y theme live/dev sin errores.

Cambios:

- Reforzado `scripts/apply_collections.py` con reintentos ante cortes SSL puntuales.
- Reaplicadas intros, meta descriptions y FAQ de las 6 colecciones principales.
- Añadidos anchors internos en el contenido de coleccion hacia PDPs con oportunidad GSC.
- Añadido bloque visible `También se busca` en la rejilla de coleccion, solo en la primera pagina, con enlaces internos contextuales.

Colecciones verificadas en HTML publico:

- `/collections/sillones-de-exterior` enlaza a `sofa terraza 120 cm`, `sofa exterior 130 cm` y rinconera.
- `/collections/tumbonas` enlaza a tumbona Balliu resina, tumbona resina 75 cm y tumbona aluminio.
- `/collections/parasoles` enlaza a base de parasol 25 kg, bases para sombrilla y pergola 250x300.
- `/collections/accesorios` enlaza a base para sombrilla 25 kg, parasoles y colchonetas para tumbona.

Backups generados:

- `content/descriptions/backup_collections_20260624-073004.json` - dry-run inicial con corte SSL.
- `content/descriptions/backup_collections_20260624-073205.json` - dry-run limpio.
- `content/descriptions/backup_collections_20260624-073212.json` - snapshot previo a la aplicacion final.

## Sprint 1.3 aplicado - 2026-06-24

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_desduplicated_descriptions.py --apply`

Estado: aplicado en Shopify Admin API sin errores.

Motivo:

- Balliu fue contrastado con `curl` contra la ficha publica de proveedor `parasol-ocean-tejido-acrilico`; no se detecto duplicado literal relevante en descripcion, solo solapes de navegacion/legal.
- Hevea se priorizo por riesgo real de duplicado externo: algunas PDPs conservaban angulos y frases procedentes del CSV de proveedor.
- Los sets bicolor ademas tenian descripciones muy finas, con peor potencial de snippet y peor respuesta a intencion comercial.

Fichas actualizadas:

- `/products/set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro` - refuerzo `rinconera de terraza`, `rinconera de jardin`, `sofa de esquina exterior`.
- `/products/set-rinconera-exterior-hpl-moderno-sofa-de-esquina-mesa-de-centro` - refuerzo `set rinconera exterior HPL`, `terraza amplia`, `atico`.
- `/products/set-rinconera-exterior-hpl-elegante-sofa-de-esquina-mesa-de-centro` - refuerzo `rinconera terraza`, `set rinconera exterior`.
- `/products/set-rinconera-exterior-hpl-sofisticado-sofa-de-esquina-mesa-de-centro` - refuerzo blanco-beige + `sofa de esquina exterior`.
- `/products/set-jardin-bicolor-3-plazas-bicolor-sofa-3-plazas-2-sillones-mesa` - refuerzo `set jardin bicolor`, `sofa bicolor`, `sofa exterior bicolor`.
- `/products/set-jardin-bicolor-2-plazas-bicolor-sofa-2-plazas-2-sillones-mesa` - refuerzo `conjunto jardin bicolor`, `sofa bicolor exterior`.

Backups generados:

- `content/descriptions/backup_desduplicated_20260624-083526.json` - dry-run inicial.
- `content/descriptions/backup_desduplicated_20260624-083550.json` - snapshot previo a la aplicacion.
- `content/descriptions/backup_desduplicated_20260624-083632.json` - comprobacion posterior desde Admin.

Verificacion:

- Admin API confirma 6/6 fichas con nuevo `descriptionHtml`.
- HTML publico verificado en rinconera contemporanea y rinconera HPL sofisticada.
- HTML publico verificado en bicolor 2/3 plazas con cache-buster por cache de storefront.

## Sprint 2 aplicado - 2026-06-24

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_trust_pages.py --apply`
- `.venv/bin/python scripts/push_theme_assets.py --theme 189222715716 sections/santavila-product.liquid`
- `.venv/bin/python scripts/push_theme_assets.py --theme 189222715716 sections/santavila-collection-grid.liquid`
- `.venv/bin/python scripts/push_theme_assets.py --theme 189222715716 sections/santavila-footer.liquid`

Estado: aplicado en Shopify Admin API y theme live/dev.

Paginas creadas:

- `/pages/sobre-santavila` - entidad, seleccion, proveedores, mercado Espana y contacto real.
- `/pages/envio` - plazo orientativo, recepcion, bultos, montaje y dudas de entrega.
- `/pages/garantia` - cobertura, exclusiones y gestion de incidencias.
- `/pages/mantenimiento` - aluminio, resina, HPL, textiles, parasoles y guardado.

Enlazado aplicado:

- PDP: enlaces desde panel de confianza hacia entrega, mantenimiento y garantia.
- Colecciones: bloque `Compra con tranquilidad` con enlaces a entrega, garantia, mantenimiento y sobre Santavila.
- Footer: enlaces persistentes a las 4 paginas nuevas.

Backups:

- `content/descriptions/backup_trust_pages_20260624-092434.json` - dry-run previo.
- `content/descriptions/backup_trust_pages_20260624-092444.json` - snapshot previo a creacion final.

Verificacion:

- Las 4 paginas devuelven 200 en `santavila.com`.
- HTML SSR verificado en PDP, coleccion y footer con enlaces a las paginas nuevas.
- `/pages/sobre-santavila` expone meta description autogenerada desde el contenido y body visible.

## Sprint 3 aplicado - 2026-06-24

Fuente de ejecucion:

- `.venv/bin/python scripts/push_theme_assets.py --theme 189222715716 layout/theme.liquid`
- `.venv/bin/python scripts/push_theme_assets.py --theme 189222715716 sections/header.liquid`
- `.venv/bin/python scripts/push_theme_assets.py --theme 189222715716 snippets/santavila-schema.liquid`

Estado: aplicado en theme live/dev.

Cambios:

- `Organization` basico sustituido por `Organization` + `OnlineStore` con `@id` estable `https://santavila.com#organization`.
- `Organization.url` corregido a `https://santavila.com`, no la URL de cada pagina.
- `BreadcrumbList` añadido a colecciones, PDPs, paginas, blogs y articulos.
- `ItemList` añadido a colecciones con hasta 24 productos visibles.
- `FAQPage` de colecciones se mantiene sin duplicar.
- `Product` nativo de Shopify se mantiene sin sobreescritura.

Verificacion:

- Home: `Organization` + `OnlineStore`.
- `/collections/sillones-de-exterior`: `Organization`, `BreadcrumbList`, `ItemList`, `FAQPage`.
- `/products/base-de-parasol-25-kg`: `Organization`, `BreadcrumbList`, `Product`.
- `/pages/sobre-santavila`: `Organization`, `BreadcrumbList`.

Informe:

- `docs/santavila/GEO-SCHEMA-REPORT.md`

## Sprint 4.1 aplicado - 2026-06-24

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_geo_guides.py --apply`
- `.venv/bin/python scripts/apply_trust_pages.py --apply`

Estado: guia publicada y pagina de mantenimiento reenlazada.

URL publicada:

- `/blogs/news/que-muebles-de-exterior-aguantan-mejor-lluvia-y-sol`

Contenido:

- Respuesta directa inicial.
- Tabla comparativa de materiales.
- Secciones para aluminio, resina, HPL, madera, textiles, costa y piscina.
- Checklist de mantenimiento.
- FAQ final con 5 preguntas.

Enlazado:

- La guia enlaza a colecciones de sillas, tumbonas, mesas y parasoles.
- La guia enlaza a la guia de materiales existente y a `/pages/mantenimiento`.
- `/pages/mantenimiento` enlaza de vuelta a la guia.

Verificacion:

- URL devuelve 200.
- HTML contiene meta, contenido y enlaces internos.
- JSON-LD expone `Article`, `FAQPage` y `BreadcrumbList`.

Informe:

- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md`

## Sprint 4.6 aplicado - 2026-06-27

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_geo_guides.py --apply`

Estado: nueva guia citable de tumbonas por material publicada.

URL publicada:

- `/blogs/news/tumbona-de-aluminio-resina-o-madera-cual-elegir-para-exterior`

Contenido:

- Comparativa de aluminio + textilene, resina/polipropileno, madera/teca, acero tratado y ratán sintetico PE.
- Secciones para piscina, costa, comodidad, respaldo, ruedas y colchoneta.
- Checklist antes de comprar.
- Recomendaciones por caso.
- FAQ final con 5 preguntas.

Enlazado:

- El articulo enlaza a `/collections/tumbonas`.
- El articulo refuerza el cluster de materiales, mantenimiento, piscina y costa.

Verificacion:

- URL devuelve 200.
- Canonical apunta a la misma URL.
- H1 y meta description actualizados.
- HTML contiene tabla, bloque de fuentes y FAQ.
- JSON-LD expone `Article`, `FAQPage` y `BreadcrumbList`.

Informe:

- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md`

## Sprint 4.5 aplicado - 2026-06-27

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_geo_guides.py --apply`

Estado: nueva guia citable de mesas de exterior publicada.

URL publicada:

- `/blogs/news/como-elegir-mesa-de-exterior-medidas-comensales-y-espacio-necesario`

Contenido:

- Tabla por comensales: 2, 4, 6, 8 y uso variable/extensible.
- Recomendaciones de espacio para sacar sillas y circular.
- Comparativa de mesa redonda, rectangular, cuadrada y extensible.
- Secciones para sillas, materiales de tablero, altura, checklist y errores habituales.
- FAQ final con 5 preguntas.

Enlazado:

- El articulo enlaza a `/collections/mesas`.
- El articulo enlaza a guias de terraza pequena, lluvia/sol, materiales y mantenimiento.

Verificacion:

- URL devuelve 200.
- Canonical apunta a la misma URL.
- H1 y meta description actualizados.
- HTML contiene tabla, bloque de fuentes y FAQ.
- JSON-LD expone `Article`, `FAQPage` y `BreadcrumbList`.

Informe:

- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md`

## Sprint 4.4 aplicado - 2026-06-26

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_geo_guides.py --apply`

Estado: guia de terraza pequena/balcon existente reforzada.

URL actualizada:

- `/blogs/news/como-aprovechar-al-maximo-una-terraza-pequena-muebles-distribucion-y-trucos-visuales`

Contenido:

- Checklist de medicion previa: espacio util, apertura de puerta y acceso.
- Tabla por tipo de espacio: balcon estrecho, balcon 120-160 cm, terraza 4-6 m2 y terraza 6-10 m2.
- Recomendaciones para mesas, sillas, bancos, almacenaje, verticalidad, sombra y materiales.
- Checklist rapido antes de comprar.
- Errores habituales.
- FAQ final con 5 preguntas.

Enlazado:

- El articulo enlaza a colecciones de mesas, sillas, sillones y parasoles.
- El articulo enlaza a la guia lluvia/sol y a la guia de materiales.

Verificacion:

- URL devuelve 200.
- Canonical apunta a la misma URL.
- H1 y meta description actualizados.
- HTML contiene tabla, bloque de fuentes y FAQ.
- JSON-LD expone `Article`, `FAQPage` y `BreadcrumbList`.

Informe:

- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md`

## Sprint 4.3 aplicado - 2026-06-25

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_geo_guides.py --apply`
- `.venv/bin/python scripts/apply_trust_pages.py --apply`

Estado: guia de mantenimiento existente reforzada y enlazada desde `/pages/mantenimiento`.

URL actualizada:

- `/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada`

Contenido:

- Tabla de mantenimiento por material: aluminio, resina, HPL, ratán sintetico PE, teca/madera, cojines/textiles y parasoles.
- Secciones especificas por material.
- Calendario primavera, verano, otoño e invierno.
- Errores a evitar: abrasivos, textiles humedos, fundas sobre suciedad, presion alta y parasoles abiertos con viento.
- FAQ final con 5 preguntas.

Enlazado:

- El articulo enlaza a colecciones de sillas, tumbonas y mesas.
- El articulo enlaza a la guia de materiales.
- `/pages/mantenimiento` enlaza al articulo largo de mantenimiento y a la guia lluvia/sol.

Verificacion:

- URL devuelve 200.
- Canonical apunta a la misma URL.
- H1 y meta description actualizados.
- HTML contiene tabla, bloque de fuentes y FAQ.
- JSON-LD expone `Article`, `FAQPage` y `BreadcrumbList`.

Informe:

- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md`

## Sprint 5 iniciado - 2026-06-27

Fuente de ejecucion:

- Revision documental y theme audit local.
- Contraste de Google Business Profile contra guia oficial de Google.

Estado: autoridad de marca iniciada.

Entregable:

- `docs/santavila/GEO-BRAND-MENTIONS.md`
- `docs/santavila/GEO-SOCIAL-CONTENT-PACK.md`

Acciones definidas:

- Confirmar elegibilidad de Google Business Profile.
- Reservar/crear perfiles de Pinterest, Instagram, LinkedIn y YouTube.
- Elegir plataforma principal de reviews.
- Preparar 3-5 menciones externas realistas en blogs/directorios sectoriales.
- Aplicar `sameAs` solo cuando existan URLs publicas reales.

## Sprint 4.2 aplicado - 2026-06-25

Fuente de ejecucion:

- `.venv/bin/python scripts/apply_geo_guides.py --apply`

Estado: guia de materiales existente reforzada con contenido contrastado.

URL actualizada:

- `/blogs/news/como-elegir-muebles-de-exterior-que-duren-aluminio-teca-o-ratan-sintetico`

Contenido:

- Comparativa de aluminio lacado, resina/polipropileno, HPL, ratán sintetico PE, teca, acacia, acero y textiles.
- Secciones por caso: pleno sol, piscina, costa, porche cubierto, uso intensivo y calidez visual.
- Bloque de criterio tecnico y fuentes contrastadas.
- FAQ final con 5 preguntas.

Verificacion:

- URL devuelve 200.
- Canonical apunta a la misma URL.
- H1 y meta description actualizados.
- HTML contiene tabla comparativa, contenido de fuentes y FAQ.
- JSON-LD expone `Article`, `FAQPage` y `BreadcrumbList`.

Informe:

- `docs/santavila/GEO-CITABLE-CONTENT-REPORT.md`
