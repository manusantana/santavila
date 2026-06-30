# GEO PDP Description Audit - Santavila

Fecha: 2026-06-27

## Objetivo

Revisar la calidad real de las descripciones de producto activas. La auditoria anterior marcaba como "OK" fichas de 30 palabras, que tecnicamente no estan vacias pero siguen siendo pobres para SEO/GEO, comparacion de compra y citabilidad por IA.

Fuente:

- `.venv/bin/python scripts/audit_products.py`
- `auditoria_fichas_report.csv`

## Resultado

Productos totales en Shopify:

- 241 productos.
- 171 productos `ACTIVE`.
- 70 productos `DRAFT` u otros estados.

Estado de descripciones en productos `ACTIVE`:

| Tramo | Productos | Lectura |
|---|---:|---|
| 0 palabras | 0 | No hay fichas vacias activas. |
| Menos de 50 palabras | 79 | Muy pobres para producto indexable. |
| 50-79 palabras | 39 | Fichas finas: explican algo, pero no resuelven decision. |
| 80-119 palabras | 52 | Aceptables, pero mejorables en productos con demanda. |
| 120+ palabras | 1 | Solo una ficha alcanza un nivel realmente rico. |

Conclusion:

- 118 de 171 productos activos tienen menos de 80 palabras.
- El problema no es ausencia total de descripcion, sino falta de profundidad, diferenciacion y respuesta a dudas reales.
- La intuicion de que las PDP siguen pobres es correcta.

Estado tras Sprint PDP 2.0 completo, actualizado el 2026-06-28:

| Tramo | Productos | Lectura |
|---|---:|---|
| 0 palabras | 0 | No hay fichas vacias activas. |
| Menos de 50 palabras | 0 | Se ha cerrado el tramo critico. |
| 50-79 palabras | 0 | Ya no quedan fichas finas activas. |
| 80-119 palabras | 48 | Fichas aceptables pendientes de mejora selectiva. |
| 120+ palabras | 123 | 72% del catalogo activo queda en rango rico. |

Conclusion actualizada:

- 0 de 171 productos activos quedan por debajo de 80 palabras.
- El sprint paso de 1 a 123 PDP en rango rico.
- La siguiente mejora ya no es "rellenar fichas pobres", sino optimizar las 48 aceptables segun señales de GSC, margen o prioridad comercial.

## Tipos mas afectados bajo 80 palabras

| Tipo | Productos <80 palabras |
|---|---:|
| Sofá | 28 |
| Conjunto sofá | 24 |
| Sillón | 16 |
| Mesa centro | 12 |
| Tumbona | 8 |
| Reposapiés | 6 |
| Silla | 5 |
| Funda | 4 |
| Mesa | 3 |
| Mesa comedor | 3 |
| Banco | 2 |
| Parasol | 2 |
| Otros | 5 |

## Por que importa

Una ficha de 30-50 palabras puede servir para que Shopify no aparezca vacio, pero no basta para:

- resolver dudas de medidas, materiales, uso y mantenimiento;
- diferenciar productos parecidos;
- reducir contenido duplicado entre proveedor y tienda;
- ganar long-tail por medida o uso;
- ser citada por una IA como respuesta util;
- mejorar CTR cuando la URL ya aparece en GSC.

## Criterio nuevo de calidad

Para Santavila, una PDP citable deberia tener:

- 100-180 palabras como minimo operativo en productos simples;
- 180-260 palabras en productos principales o con señales GSC;
- primer parrafo directo explicando que es y para quien encaja;
- bullets de medidas, material, uso recomendado y mantenimiento;
- bloque breve de decision: cuando elegirlo y cuando no;
- meta description unica y orientada a query real;
- enlaces internos cuando encaje con guias o colecciones.

## Prioridad recomendada

No conviene reescribir las 171 fichas de golpe. La mejor secuencia es:

1. **PDPs con señales GSC**, porque ya tienen demanda real.
2. **Familias con muchas fichas pobres**, para mejorar cobertura semantica.
3. **Productos top por margen/inventario**, si el usuario confirma prioridad comercial.

Primer lote recomendado:

- banco de exterior 108/150 cm;
- sofas de 2 y 3 plazas con menos de 50 palabras;
- sillones con menos de 50 palabras;
- mesas de centro HPL;
- set jardin / conjunto sofa con 30-40 palabras;
- fichas ya detectadas en GSC: banco con mesa, pergola, sofas 120/130, tumbonas y rinconera.

## Sprint propuesto

Sprint PDP 2.0 - descripciones ricas por familias.

Formato:

- 15-20 productos por lote.
- Backup previo de Shopify.
- Dry-run con palabras actuales -> nuevas.
- Aplicacion via Shopify Admin API.
- Verificacion publica con `curl` en 3-5 URLs.
- Actualizacion de journal y GSC opportunities.

Primer lote sugerido:

1. Sofas 2 plazas con queries por medida.
2. Sofas 3 plazas y conjuntos sofa.
3. Bancos y mesas centro.
4. Sillones.
5. Tumbonas/resina/Balliu.

## Decision

Seguir por descripciones de producto tiene mas sentido que seguir creando guias ahora mismo. Las guias ya estan sembradas; las PDP son el punto debil vivo del catalogo.

## Sprint PDP 2.0 - batch 1 aplicado

Fecha: 2026-06-27

Estado: aplicado en Shopify.

Productos trabajados:

| Producto | Palabras antes | Palabras despues | Query/cluster |
|---|---:|---:|---|
| `/products/banco-jardin-con-mesa-integrada-220-cm` | 81 | 190 | `banco con mesa incorporada`, `banco 220` |
| `/products/pergola-aluminio-para-jardin-300300250-cm` | 94 | 192 | `pérgola 250x300`, `pergola 300 x 250` |
| `/products/sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm` | 90 | 185 | `sofa terraza 120 cm` |
| `/products/sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm` | 78 | 196 | `sofa exterior 130 cm` |
| `/products/balliu-tumbona-de-exterior-resina-28ff014d` | 73 | 190 | `tumbonas de resina`, `tumbona Balliu` |
| `/products/set-rinconera-exterior-contemporaneo-sofa-de-esquina-mesa-de-centro` | 100 | 196 | `rinconera terraza`, `rinconera jardin` |

Resultado tras recalcular auditoria:

| Tramo | Antes batch 1 | Despues batch 1 |
|---|---:|---:|
| Menos de 50 palabras | 79 | 79 |
| 50-79 palabras | 39 | 37 |
| 80-119 palabras | 52 | 48 |
| 120+ palabras | 1 | 7 |
| Total bajo 80 palabras | 118 | 116 |

Backups:

- `content/descriptions/backup_pdp_rich_batch1_20260627-093828.json` - dry-run.
- `content/descriptions/backup_pdp_rich_batch1_20260627-093834.json` - previo a aplicar.

Script:

- `scripts/apply_pdp_rich_descriptions.py`

Verificacion publica:

- Metas y JSON-LD verificados con `curl` en banco, pergola, sofa 130 y tumbona Balliu.

Siguiente lote recomendado:

- Sofas 2 plazas y 3 plazas con menos de 50 palabras, priorizando medidas con potencial long-tail.
- Conjuntos sofa con 30-40 palabras.
- Bancos 108/150 cm y mesas de centro HPL.

## Sprint PDP 2.0 - batch 2 aplicado

Fecha: 2026-06-28

Estado: aplicado en Shopify.

Productos trabajados:

| Producto | Palabras antes | Palabras despues |
|---|---:|---:|
| `/products/sofa-terraza-2-plazas-estilo-contemporaneo-13370-cm` | 33 | 188 |
| `/products/sofa-terraza-3-plazas-estilo-moderno-18770-cm` | 36 | 178 |
| `/products/sofa-terraza-3-plazas-estilo-contemporaneo-18583-cm` | 37 | 177 |
| `/products/sofa-terraza-2-plazas-estilo-contemporaneo-16269-cm` | 37 | 180 |
| `/products/sofa-terraza-3-plazas-estilo-contemporaneo-215104-cm` | 37 | 180 |
| `/products/sofa-terraza-2-plazas-estilo-elegante-13170-cm` | 37 | 179 |
| `/products/set-jardin-2-plazas-moderno-sofa-2-plazas-2-sillones-mesa` | 30 | 180 |
| `/products/set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa` | 30 | 174 |
| `/products/set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-4` | 30 | 177 |
| `/products/set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-3` | 31 | 174 |

Resultado tras recalcular auditoria:

| Tramo | Antes batch 1 | Tras batch 1 | Tras batch 2 |
|---|---:|---:|---:|
| Menos de 50 palabras | 79 | 79 | 69 |
| 50-79 palabras | 39 | 37 | 37 |
| 80-119 palabras | 52 | 48 | 48 |
| 120+ palabras | 1 | 7 | 17 |
| Total bajo 80 palabras | 118 | 116 | 106 |

Backups:

- `content/descriptions/backup_pdp_rich_batch2_20260628-105748.json` - dry-run.
- `content/descriptions/backup_pdp_rich_batch2_20260628-105759.json` - previo a aplicar.

Script:

- `scripts/apply_pdp_rich_descriptions_batch2.py`

Verificacion publica:

- Metas, JSON-LD y bloque visible `Descripción y detalles` verificados con `curl` en:
  - sofa 2 plazas 133×70 cm;
  - sofa 3 plazas 187×70 cm;
  - set jardin moderno con sofa 2 plazas.

Siguiente lote recomendado:

- Sofas/conjuntos restantes con menos de 50 palabras.
- Sillones con menos de 50 palabras.
- Mesas de centro HPL y bancos 108/150 cm.

## Sprint PDP 2.0 - batch 3 aplicado

Fecha: 2026-06-28

Estado: aplicado en Shopify.

Productos trabajados:

| Producto | Palabras antes | Palabras despues |
|---|---:|---:|
| `/products/sofa-terraza-2-plazas-estilo-estilizado-14383-cm` | 38 | 166 |
| `/products/sofa-terraza-2-plazas-estilo-contemporaneo-15082-cm` | 38 | 162 |
| `/products/sofa-terraza-2-plazas-estilo-contemporaneo-145100-cm` | 38 | 159 |
| `/products/sofa-terraza-3-plazas-estilo-sofisticado-212100-cm` | 38 | 159 |
| `/products/sofa-terraza-2-plazas-estilo-contemporaneo-164104-cm` | 38 | 159 |
| `/products/set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-2` | 30 | 165 |
| `/products/set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-3` | 30 | 162 |
| `/products/set-jardin-3-plazas-sofisticado-sofa-3-plazas-2-sillones-mesa-3` | 31 | 157 |
| `/products/set-jardin-2-plazas-elegante-sofa-2-plazas-2-sillones-mesa-5` | 31 | 164 |
| `/products/set-jardin-3-plazas-elegante-sofa-3-plazas-2-sillones-mesa-2` | 32 | 165 |
| `/products/banco-de-exterior-150-cm` | 33 | 172 |
| `/products/banco-de-exterior-108-cm` | 35 | 165 |

Resultado tras recalcular auditoria:

| Tramo | Antes batch 1 | Tras batch 1 | Tras batch 2 | Tras batch 3 |
|---|---:|---:|---:|---:|
| Menos de 50 palabras | 79 | 79 | 69 | 57 |
| 50-79 palabras | 39 | 37 | 37 | 37 |
| 80-119 palabras | 52 | 48 | 48 | 48 |
| 120+ palabras | 1 | 7 | 17 | 29 |
| Total bajo 80 palabras | 118 | 116 | 106 | 94 |

Backups:

- `content/descriptions/backup_pdp_rich_batch3_20260628-111220.json` - dry-run.
- `content/descriptions/backup_pdp_rich_batch3_20260628-111226.json` - previo a aplicar.

Script:

- `scripts/apply_pdp_rich_descriptions_batch3.py`

Verificacion publica:

- Metas, JSON-LD y bloque visible `Descripción y detalles` verificados con `curl` en:
  - sofa 2 plazas 143×83 cm;
  - set jardin contemporaneo con sofa 3 plazas;
  - banco exterior 150 cm.

Siguiente lote recomendado:

- Sillones con menos de 80 palabras.
- Mesas de centro HPL.
- Tumbonas y reposapies con descripciones finas.

## Sprint PDP 2.0 - batch 4 aplicado

Fecha: 2026-06-28

Estado: aplicado en Shopify.

Productos trabajados:

| Producto | Palabras antes | Palabras despues |
|---|---:|---:|
| `/products/sillon-exterior-estilo-urbano-6670-cm` | 33 | 165 |
| `/products/sillon-exterior-estilo-elegante-80104-cm` | 36 | 159 |
| `/products/sillon-exterior-estilo-moderno-7085-cm` | 36 | 159 |
| `/products/sillon-exterior-estilo-versatil-6470-cm` | 36 | 157 |
| `/products/sillon-exterior-estilo-versatil-76100-cm` | 39 | 164 |
| `/products/sillon-exterior-estilo-versatil-7783-cm` | 40 | 160 |
| `/products/sillon-exterior-estilo-envolvente-7582-cm` | 40 | 161 |
| `/products/sillon-exterior-estilo-estilizado-7069-cm` | 40 | 156 |
| `/products/sillon-exterior-estilo-contemporaneo-68115-cm` | 42 | 154 |
| `/products/sillon-exterior-estilo-versatil-58100-cm` | 43 | 154 |
| `/products/sillon-exterior-estilo-versatil-7685-cm` | 44 | 155 |
| `/products/sillon-exterior-estilo-elegante-6590-cm` | 47 | 158 |
| `/products/sillon-exterior-estilo-elegante-6578-cm` | 47 | 157 |
| `/products/sillon-exterior-bicolor-estilo-bicolor-7376-cm` | 51 | 161 |
| `/products/sillon-exterior-estilo-elegante-7275-cm` | 66 | 158 |
| `/products/sillon-exterior-aluminio-estilo-envolvente-9890-cm` | 67 | 162 |

Resultado tras recalcular auditoria:

| Tramo | Tras batch 3 | Tras batch 4 |
|---|---:|---:|
| Menos de 50 palabras | 57 | 44 |
| 50-79 palabras | 37 | 34 |
| 80-119 palabras | 48 | 48 |
| 120+ palabras | 29 | 45 |
| Total bajo 80 palabras | 94 | 78 |

Backups:

- `content/descriptions/backup_pdp_rich_batch4_20260628-114046.json` - dry-run.
- `content/descriptions/backup_pdp_rich_batch4_20260628-114053.json` - previo a aplicar.

Script:

- `scripts/apply_pdp_rich_descriptions_batch4.py`

Verificacion publica:

- Metas, JSON-LD y bloque visible `Descripción y detalles` verificados con `curl` en:
  - sillon exterior urbano 66×70 cm;
  - sillon exterior contemporaneo 68×115 cm;
  - sillon exterior aluminio envolvente 98×90 cm.

Siguiente lote recomendado:

- Mesas de centro HPL y mesas auxiliares.
- Tumbonas y reposapies.
- Sofas/conjuntos restantes solo si se quiere terminar esa familia antes de pasar a Balliu.

## Sprint PDP 2.0 - batch 5 aplicado

Fecha: 2026-06-28

Estado: aplicado en Shopify.

Productos trabajados:

- 12 mesas de centro.
- 6 reposapies.
- 7 tumbonas.

Resultado tras recalcular auditoria:

| Tramo | Tras batch 4 | Tras batch 5 |
|---|---:|---:|
| Menos de 50 palabras | 44 | 27 |
| 50-79 palabras | 34 | 26 |
| 80-119 palabras | 48 | 48 |
| 120+ palabras | 45 | 70 |
| Total bajo 80 palabras | 78 | 53 |

Backups:

- `content/descriptions/backup_pdp_rich_batch5_20260628-122122.json` - dry-run.
- `content/descriptions/backup_pdp_rich_batch5_20260628-122131.json` - previo a aplicar.

Script:

- `scripts/apply_pdp_rich_descriptions_batch5.py`

Verificacion publica:

- Metas, JSON-LD y bloque visible `Descripción y detalles` verificados con `curl` en:
  - mesa de centro exterior HPL 90 cm;
  - reposapies exterior 85×50×43 cm;
  - tumbona exterior resina Balliu Carmen 75 cm.

Siguiente lote recomendado:

- Sofas y conjuntos sofa restantes, o bien cierre de familias menores: sillas, mesas comedor, parasoles, fundas y accesorios.

## Sprint PDP 2.0 - batch 6 aplicado

Fecha: 2026-06-28

Estado: aplicado en Shopify.

Productos trabajados:

- 16 sofas.
- 15 conjuntos sofa.

Resultado tras recalcular auditoria:

| Tramo | Tras batch 5 | Tras batch 6 |
|---|---:|---:|
| Menos de 50 palabras | 27 | 7 |
| 50-79 palabras | 26 | 15 |
| 80-119 palabras | 48 | 48 |
| 120+ palabras | 70 | 101 |
| Total bajo 80 palabras | 53 | 22 |

Backups:

- `content/descriptions/backup_pdp_rich_batch6_20260628-123505.json` - dry-run inicial.
- `content/descriptions/backup_pdp_rich_batch6_20260628-123524.json` - dry-run corregido.
- `content/descriptions/backup_pdp_rich_batch6_20260628-123534.json` - previo a aplicar.

Script:

- `scripts/apply_pdp_rich_descriptions_batch6.py`

Verificacion publica:

- Metas, JSON-LD y bloque visible `Descripción y detalles` verificados con `curl` en:
  - sofa terraza 3 plazas elegante 220×69 cm;
  - sofa terraza aluminio 3 plazas contemporaneo 220×90 cm;
  - set jardin 3 plazas sofisticado.

Siguiente lote recomendado:

- Cierre de familias menores: sillas, fundas, mesas comedor, mesas, parasoles, accesorio, balancin, rinconera, mini tumbona y mobiliario exterior.

## Sprint PDP 2.0 - batch 7 aplicado

Fecha: 2026-06-28

Estado: aplicado en Shopify.

Productos trabajados:

- 22 productos de familias menores: sillas, mesas comedor, mesas auxiliares, fundas, parasoles, accesorios, balancin, rinconera, mini tumbona y mobiliario exterior.

Resultado tras recalcular auditoria:

| Tramo | Tras batch 6 | Tras batch 7 |
|---|---:|---:|
| Menos de 50 palabras | 7 | 0 |
| 50-79 palabras | 15 | 0 |
| 80-119 palabras | 48 | 48 |
| 120+ palabras | 101 | 123 |
| Total bajo 80 palabras | 22 | 0 |

Backups:

- `content/descriptions/backup_pdp_rich_batch7_20260628-124709.json` - dry-run inicial.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124726.json` - dry-run corregido.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124735.json` - previo a aplicar.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124931.json` - dry-run de correccion de lenguaje.
- `content/descriptions/backup_pdp_rich_batch7_20260628-124940.json` - previo a reaplicar correccion.

Script:

- `scripts/apply_pdp_rich_descriptions_batch7.py`

Verificacion publica:

- Metas, JSON-LD y bloque visible `Descripción y detalles` verificados con `curl` en:
  - silla exterior estilo contemporaneo;
  - mesa comedor exterior HPL 150×90 cm;
  - funda protectora para sofa exterior.
- Se corrigio el fallback de material para evitar frases artificiales como "en exterior"; ahora las fichas sin material explicito usan "diseño para uso exterior".

Estado final del sprint:

- Productos activos: 171.
- Productos activos bajo 80 palabras: 0.
- Productos activos con descripcion rica 120+ palabras: 123.
- Productos activos en tramo aceptable 80-119 palabras: 48.

Siguiente lote recomendado:

- Reauditar GSC tras recrawl y priorizar las 48 fichas aceptables por impresiones, clics, margen o familias estrategicas.
