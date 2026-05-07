# Cómo usar estos prompts — Santavila

No copies todo el contenido directamente sin orden. Usa estos archivos en fases.

## Orden recomendado

### 1. Primero usa `00_PROMPT_ARRANQUE_AUDITORIA.md`

Este es el prompt que debes pegar primero en Claude Code / Antigravity.

Objetivo:
- que lea `plan_santavila.md`,
- que audite la tienda/theme,
- que no toque código todavía,
- que genere documentos de diagnóstico y planificación.

Resultado esperado:
- `AUDITORIA_SANTAVILA.md`
- `BACKLOG_SANTAVILA.md`
- `DATA_MODEL_SANTAVILA.md`
- `THEME_PLAN_SANTAVILA.md`

No dejes que el agente empiece rediseñando la home sin haber hecho esto.

---

### 2. Después usa `01_PROMPT_MAESTRO_SANTAVILA.md`

Este es el prompt completo.

Úsalo cuando:
- el agente ya haya leído `plan_santavila.md`,
- tengas la auditoría inicial,
- quieras que trabaje por sprints,
- quieras implementar theme, metafields, metaobjects, PDP, home, PLP, SEO, Flow y visuales IA.

---

### 3. Usa `02_PROMPT_IMPLEMENTACION_SPRINTS.md` cuando ya quieras ejecutar

Este prompt es más operativo.

Sirve para decirle:
- empieza por Sprint 1,
- no hagas todos los cambios a la vez,
- valida antes de avanzar,
- documenta cada cambio.

---

## Archivos que debes tener en el proyecto

En la raíz del proyecto o carpeta de trabajo de Antigravity/Claude Code deberías tener:

```txt
plan_santavila.md
00_PROMPT_ARRANQUE_AUDITORIA.md
01_PROMPT_MAESTRO_SANTAVILA.md
02_PROMPT_IMPLEMENTACION_SPRINTS.md
```

Si puedes, añade también una carpeta:

```txt
/docs/santavila/
```

Y pide al agente que guarde ahí todos los documentos que genere.

---

## Flujo recomendado real

1. Abre Antigravity o Claude Code.
2. Carga o coloca `plan_santavila.md` en el proyecto.
3. Pega el contenido de `00_PROMPT_ARRANQUE_AUDITORIA.md`.
4. Revisa los documentos que genere.
5. Valida tú las decisiones principales.
6. Después pega `01_PROMPT_MAESTRO_SANTAVILA.md`.
7. Cuando toque ejecutar, usa `02_PROMPT_IMPLEMENTACION_SPRINTS.md`.

---

## Regla importante

No permitas que el agente haga cambios directamente en producción.

Primero:
- auditoría,
- backlog,
- modelo de datos,
- plan de theme,
- sprint pequeño,
- validación,
- publicación controlada.

Santavila debe dejar de ser “Shopify con productos cargados” y convertirse en una marca ecommerce premium, pero eso hay que hacerlo con estructura, no solo con diseño bonito.
