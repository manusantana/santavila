# WORKFLOW — Staging → Producción (temas Shopify)

> **Documento canónico.** Esta es la única fuente de verdad sobre cómo se prueba y se
> publica el theme de Santavila. Si algo en otro sitio contradice esto, manda esto.
>
> Tienda: `mueblesexterior.myshopify.com` · Dominio público: `santavila.com`
> Última revisión: **2026-06-30**

---

## 🔴 Regla de oro (NO negociable)

1. **Todo se prueba primero en STAGING.** Cualquier cambio del theme (desarrollo,
   experimento, ajuste visual) se sube y se valida **antes** en el tema de staging.
2. **A producción solo lo validado.** Únicamente cuando el cambio está revisado y
   aprobado en staging se promociona al tema **publicado**.
3. **La promoción a PRODUCCIÓN exige SIEMPRE confirmación explícita del dueño (Sergio).**
   Nadie sube a producción sin esa confirmación: ni Claude, ni Codex, ni el compañero,
   ni ningún script automático. **Sin "ok" explícito → no se toca producción.**

> Si tienes dudas de si algo está validado: **no subas a producción.** El coste de
> esperar es cero; el de romper la tienda en vivo, no.

---

## Los entornos (IDs reales — verificados 2026-06-30)

| Rol | ID | Nombre | Para qué |
|---|---|---|---|
| **PRODUCCIÓN** (`main`, publicado) | **`189222715716`** | *Santavila Theme by Ubicuo Libres Pensadores* | Lo que ve el público en santavila.com. **Este ID no cambia nunca.** |
| **STAGING** (`unpublished`) | **`189491151172`** | *Staging Santavila Theme by Ubicuo Libres Pensadores* | Banco de pruebas estable. Se valida aquí antes de promocionar. |
| ~~development~~ (legacy) | `189114876228` | *Santavila Theme…* | Viejo "DEV". **Ha divergido del live, ya NO es la referencia.** No usar como gate. |

> Histórico: el ID `188231123268` ("Dwell 3.5.1") es un tema **antiguo que NO debe usarse**.
> El resto de temas de la tienda (Dwell, Horizon, exports) son restos ignorables.

---

## Mecanismo elegido: **copia de assets al ID fijo**

Decisión tomada (2026-06-30). Entre "copiar assets" y "publicar/intercambiar el tema",
se usa **copiar assets**:

- **Producción es SIEMPRE `189222715716`.** No se intercambian roles, no se "publica" el
  staging. El tema publicado permanece estable.
- Se promociona **archivo por archivo** con `scripts/push_theme_assets.py`.
- **`git` es la fuente de verdad** del código del theme (`theme/`).
- Encaja con toda la infraestructura existente (IDs fijos en memoria, scripts, helper de push).

**No se hace publish-swap** (no se cambia el rol de los temas). Eso rompería los IDs fijos
y se perderían las ediciones en vivo del compañero.

---

## Flujo paso a paso

```
   theme/  (git, fuente de verdad)
     │  1) desarrollas / editas aquí
     ▼
  STAGING 189491151172   ◀── 2) push:  python3 scripts/push_theme_assets.py --theme staging <archivos>
     │
     │  3) VALIDAS en staging (preview, responsive móvil/tablet/desktop, enlaces, etc.)
     │  4) pides confirmación al dueño  ──►  ⛔ sin "ok" explícito, PARA AQUÍ
     ▼
  PRODUCCIÓN 189222715716 ◀── 5) push CON confirmación:
                                   python3 scripts/push_theme_assets.py --theme prod \
                                     --prod-confirm "validado en staging + ok de Sergio" <archivos>
     │
     ▼  6) verificas en santavila.com   7) documentas el hito en JOURNAL.md
```

1. **Desarrolla** en `theme/` (commit en git).
2. **Sube a STAGING:** `python3 scripts/push_theme_assets.py --theme staging <keys…>`
   (el helper sube **y verifica** que el remoto == local).
3. **Valida en STAGING** (ver "Cómo previsualizar staging" más abajo). Incluye el
   **responsive** (móvil/tablet/desktop), no solo escritorio.
4. **Pide confirmación al dueño.** Enséñale qué cambió y dónde verlo. Espera el "ok".
5. **Con el "ok" → sube a PRODUCCIÓN** con el flag de confirmación obligatorio:
   `python3 scripts/push_theme_assets.py --theme prod --prod-confirm "<motivo>" <keys…>`
   Sin `--prod-confirm`, el helper **aborta** (guardia fail-closed).
6. **Verifica en `santavila.com`** que el cambio salió bien.
7. **Documenta** el hito en `docs/santavila/JOURNAL.md` (entrada nueva arriba).

---

## Cómo previsualizar STAGING

El tema staging es `unpublished`, así que se ve con su enlace de previsualización del admin:

```
https://mueblesexterior.myshopify.com/admin/themes/189491151172/editor   (editor)
https://santavila.com/?preview_theme_id=189491151172                     (preview en el dominio)
```

⚠️ **Ojo (memoria `shopify_theme_preview_needs_staff`):** un `fetch` anónimo con
`preview_theme_id` puede caer al LIVE. Para validar de verdad: míralo con sesión de staff
en el navegador, o verifica por Asset API (hash del asset) que lo subido a staging es lo
esperado. No te fíes de un fetch anónimo.

---

## Cuidado con los `.json` del editor (trabajo del compañero)

El compañero trabaja la **home y la configuración** directamente en el **editor del LIVE**
(memoria `santavila_team_git_source_of_truth`). Esos cambios viven en archivos JSON:
`templates/index.json`, `config/settings_data.json`, `sections/footer-group.json`,
`templates/cart.json`, etc.

- Al promocionar **código** (`.liquid`, `assets/…`, `snippets/…`, `sections/*.liquid`),
  **NO arrastres esos `.json`** salvo que sepas que deben ir. Pisarlos borraría el
  merchandising en vivo del compañero.
- Si un cambio **sí** toca un `.json` de plantilla, **coordínalo** con el compañero y
  re-sincroniza staging desde producción antes de empezar.
- Regla práctica: **sube solo los archivos que tocaste**, nunca el theme entero.

---

## Mantener STAGING alineado con PRODUCCIÓN

Hoy (2026-06-30) **staging == producción** (verificado por hash). Para que siga siendo un
banco de pruebas fiable:

- Antes de empezar un trabajo nuevo, si el compañero ha tocado el live, **re-sincroniza
  staging desde producción** (copia los `.json`/assets cambiados de prod → staging) para
  partir de un estado igual al público.
- Así lo que validas en staging refleja lo que de verdad hay en producción.

---

## Qué NO hacer (errores a evitar)

- ❌ **Subir a producción sin validar en staging.**
- ❌ **Subir a producción sin el "ok" explícito del dueño.**
- ❌ Usar `--theme prod` sin `--prod-confirm` (el helper lo bloquea a propósito).
- ❌ Hacer *publish-swap* / cambiar el rol de los temas.
- ❌ Tratar el viejo `development 189114876228` como entorno de pruebas (ha divergido).
- ❌ Subir el theme completo "por si acaso": sube solo los archivos tocados.
- ❌ Confiar en un `preview` anónimo para dar algo por validado.

---

## Cheatsheet

```bash
# Listar temas y sus roles (id / role / name)
python3 scripts/push_theme_assets.py --list-themes

# Subir a STAGING (sin fricción)
python3 scripts/push_theme_assets.py --theme staging \
  sections/santavila-hero.liquid snippets/santavila-hero-slide.liquid

# Subir a PRODUCCIÓN (requiere confirmación explícita — guardia fail-closed)
python3 scripts/push_theme_assets.py --theme prod \
  --prod-confirm "validado en staging + ok de Sergio 2026-06-30" \
  sections/santavila-hero.liquid

# (también admite el ID numérico crudo en --theme)
```

Aliases admitidos en `--theme`: `prod` / `production` / `live` → `189222715716`;
`staging` / `stage` → `189491151172`; `dev` / `development` → `189114876228`; o el ID numérico.

---

## Resumen en una frase

> **Se prueba en staging (`189491151172`); a producción (`189222715716`) solo lo validado
> y SOLO con el "ok" explícito de Sergio.**
