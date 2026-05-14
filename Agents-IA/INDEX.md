# Índice — Agents-IA / Santavila

> Carpeta con la documentación estratégica y los prompts para agentes IA del proyecto Santavila (tienda Shopify de mobiliario exterior premium accesible).
>
> Esta guía explica qué contiene cada archivo, en qué orden usarlos y para qué sirven.

---

## Mapa rápido

```txt
Agents-IA/
├── INDEX.md                              ← este archivo (guía de la carpeta)
│
├── PROYECTO.md                           ← estado REAL del proyecto (técnico + operativo)
├── plan_santavila.md                     ← ESTRATEGIA de marca, UX, datos y roadmap
├── README_USO_PROMPTS_SANTAVILA.md       ← cómo y en qué orden usar los prompts
│
├── 00_PROMPT_ARRANQUE_AUDITORIA.md       ← prompt 1: auditar antes de tocar nada
├── 01_PROMPT_MAESTRO_SANTAVILA.md        ← prompt 2: plan completo de transformación
├── 02_PROMPT_IMPLEMENTACION_SPRINTS.md   ← prompt 3: ejecución por sprints
│
├── auditoria-productos.md                ← hallazgo de duplicados y variantes mal modeladas
└── shopify-api-setup.md                  ← guía técnica para conectar la Admin API
```

---

## Dos bloques de documentación

La carpeta mezcla dos cosas con propósitos distintos. Conviene tenerlas claras:

### Bloque A — Realidad operativa del proyecto

Lo que ya existe, lo que se ha hecho, los datos técnicos y financieros actuales.

- [PROYECTO.md](PROYECTO.md)
- [shopify-api-setup.md](shopify-api-setup.md)
- [auditoria-productos.md](auditoria-productos.md) — duplicados detectados + variantes mal modeladas, sin abordar todavía

### Bloque B — Estrategia y prompts para agentes IA

El plan deseado de transformación de la tienda, y los prompts que se pegan en Claude Code / Antigravity para que un agente lo ejecute por fases.

- [plan_santavila.md](plan_santavila.md)
- [README_USO_PROMPTS_SANTAVILA.md](README_USO_PROMPTS_SANTAVILA.md)
- [00_PROMPT_ARRANQUE_AUDITORIA.md](00_PROMPT_ARRANQUE_AUDITORIA.md)
- [01_PROMPT_MAESTRO_SANTAVILA.md](01_PROMPT_MAESTRO_SANTAVILA.md)
- [02_PROMPT_IMPLEMENTACION_SPRINTS.md](02_PROMPT_IMPLEMENTACION_SPRINTS.md)

---

## Detalle de cada archivo

### [PROYECTO.md](PROYECTO.md)
**Qué es:** documento de referencia del estado REAL del proyecto. Es el briefing técnico que usar como punto de partida para cualquier agente o sesión nueva.

**Contiene:**
- Resumen ejecutivo (tienda, proveedores, mercado, estado verificado)
- Stack técnico (Shopify Admin API 2026-01, scripts Python, remove.bg, Hugging Face)
- Proveedores Hevea y Balliu: condiciones comerciales, seguimiento de tarifas, scripts de actualización
- Modelo financiero (P&L, unit economics, escenarios) — 6 hojas en `Santavila.xlsx`
- Sincronización de precios y costes con Shopify (`sync_prices_to_shopify.py`)
- Historial de trabajo por fases (1-9)
- Errores conocidos y soluciones
- Estructura de archivos del repo
- Tareas pendientes priorizadas

**Cuándo leerlo:** SIEMPRE primero al abrir el proyecto. Es la fuente de verdad de "qué hay hoy".

---

### [plan_santavila.md](plan_santavila.md)
**Qué es:** plan estratégico completo de transformación de la tienda. Es la fuente de verdad para todo lo que tiene que ver con marca, posicionamiento, UX, datos y roadmap.

**Contiene:**
- Decisiones de partida y restricciones
- Posicionamiento de marca (claim "Diseño español para vivir fuera", tono, propuesta de valor)
- Principios estratégicos (menos catálogo, más criterio; logística como producto; PDP como página de venta)
- Auditoría UX/UI actual y problemas detectados
- Arquitectura ecommerce recomendada (menú, colecciones, espacios, materiales)
- Home, PLP y PDP ideales (estructura módulo a módulo)
- Sistema de datos Shopify (metafields `santavila.*` y metaobjects `sv_*`)
- Naming de productos
- Dirección visual y paleta
- Prompts base para Higgsfield AI
- Sistema de confianza (entrega, garantía, mantenimiento)
- Roadmap operativo y backlog priorizado por fases
- Automatizaciones Shopify Flow
- SEO base, CRO, área profesionales

**Cuándo leerlo:** antes de usar cualquiera de los prompts numerados. Es la base estratégica que todos los prompts referencian.

---

### [README_USO_PROMPTS_SANTAVILA.md](README_USO_PROMPTS_SANTAVILA.md)
**Qué es:** manual de uso de los 3 prompts numerados. Explica el orden, el flujo y las reglas para que el agente no se descontrole.

**Contiene:**
- Orden recomendado (00 → 01 → 02)
- Resultado esperado de cada prompt
- Estructura de carpetas sugerida (`/docs/santavila/`)
- Regla principal: no permitir cambios directos en producción sin auditoría previa

**Cuándo leerlo:** antes de pegar el primer prompt en Claude Code / Antigravity.

---

### [00_PROMPT_ARRANQUE_AUDITORIA.md](00_PROMPT_ARRANQUE_AUDITORIA.md)
**Qué es:** primer prompt a ejecutar. Pone al agente en modo auditoría — **no toca código**.

**Lo que hace el agente al pegar este prompt:**
- Lee `plan_santavila.md` y el theme actual
- Audita marca, UX/UI, ecommerce, Shopify, SEO y datos de producto
- Genera 4 documentos base:
  - `AUDITORIA_SANTAVILA.md`
  - `BACKLOG_SANTAVILA.md`
  - `DATA_MODEL_SANTAVILA.md`
  - `THEME_PLAN_SANTAVILA.md`

**Cuándo usarlo:** al inicio del proyecto, antes de cualquier cambio.

---

### [01_PROMPT_MAESTRO_SANTAVILA.md](01_PROMPT_MAESTRO_SANTAVILA.md)
**Qué es:** prompt completo y exhaustivo de transformación. Más amplio que el de auditoría — define toda la operación.

**Lo que cubre:**
- Contexto de negocio y restricciones no negociables
- Forma de trabajo obligatoria (auditoría → propuesta → cambios → validación)
- Entregables adicionales: `SEO_PLAN`, `ART_DIRECTION`, `SHOPIFY_FLOW`, `VALIDATION_CHECKLIST`
- Home premium, PDP premium, PLP, SEO base
- Dirección visual + prompts Higgsfield
- Shopify Flow, área profesionales, productos héroe
- Plan de implementación por sprints (alto nivel)
- Criterio final de éxito ("test de 10 segundos")

**Cuándo usarlo:** después de tener la auditoría inicial y querer planificar la ejecución completa.

---

### [02_PROMPT_IMPLEMENTACION_SPRINTS.md](02_PROMPT_IMPLEMENTACION_SPRINTS.md)
**Qué es:** prompt operativo para implementar por sprints con control. Empuja al agente a ejecutar de forma segura, sprint a sprint.

**Sprints definidos:**
1. Limpieza urgente (idioma, footer, menú, claims, páginas de confianza)
2. Modelo de datos Shopify (metafields, metaobjects)
3. PDP premium piloto (3-5 productos)
4. Home premium
5. PLP y SEO base
6. Profesionales y operativa (Shopify Flow, scoring)

**Cierre de cada sprint:** archivo `SPRINT_X_RESUMEN.md` con cambios, riesgos, pruebas y siguiente paso.

**Cuándo usarlo:** cuando ya existen los documentos del prompt 00 y se quiere empezar a ejecutar cambios reales.

---

### [shopify-api-setup.md](shopify-api-setup.md)
**Qué es:** guía técnica para conectar la Admin API de Shopify desde 2026. Independiente del bloque estratégico.

**Contiene:**
- Crear app en Partner Dashboard (las Custom/Private Apps quedaron obsoletas en 2026)
- Vincular con Shopify CLI
- Configurar distribución personalizada
- Obtener token de acceso vía servidor OAuth local (`get_shopify_token.mjs`)
- Guardar el token en `.env.local`
- Snippet Python para llamadas GraphQL
- Errores comunes y scopes más usados

**Cuándo leerlo:** cuando haya que reconectar la API, rotar tokens o vincular la app con otra tienda.

---

## Flujo recomendado de uso

```txt
1. Leer PROYECTO.md         → entender qué hay HOY
2. Leer plan_santavila.md   → entender la ESTRATEGIA
3. Leer README_USO_PROMPTS  → entender el ORDEN de los prompts
4. Pegar 00_PROMPT_ARRANQUE → generar auditoría + backlog + data model + theme plan
5. Validar manualmente
6. Pegar 01_PROMPT_MAESTRO  → planificar transformación completa
7. Pegar 02_PROMPT_SPRINTS  → ejecutar sprint a sprint con validación
```

`shopify-api-setup.md` se consulta solo cuando aparece un problema de conexión o autenticación con la Admin API.

---

## Regla de oro

Ningún agente debe hacer cambios directos en producción sin haber pasado antes por:

> auditoría → backlog → modelo de datos → plan de theme → sprint pequeño → validación → publicación controlada

Ningun cambio realizado en el catalogo actual debe realizarase sin antes hacer un backup del mismo en una carpeta llamada tmp/catalogo-[fecha]
