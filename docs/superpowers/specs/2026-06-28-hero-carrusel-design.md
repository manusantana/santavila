# Hero — Carrusel / slideshow (v1, sin split screen)

**Fecha:** 2026-06-28 · **Rama:** `hero-carrusel` · **Base:** `main` @ `507a0bd`

## Objetivo
Convertir el hero de la home (1 imagen) en un **carrusel** de varias diapositivas, **sin romper la home** en ningún momento y conservando todo lo ya hecho (velo, caja, altura, color de texto, sello, "Descubre").

## Arquitectura
- **Slides = bloques** (`type: "slide"`): cada uno con imagen, eyebrow, título (2 líneas), subtítulo y 2 CTAs.
- **Compatibilidad (no-break):** si la sección **no tiene bloques**, se renderiza **un slide "legacy"** con los settings de sección actuales (lo de hoy). Con ≥1 bloque, se usan los bloques. Con ≥2 bloques se activan navegación y auto-rotación. → El `index.json` del live (sin bloques, del compañero) sigue mostrando el hero actual; **no se toca**.
- **Globales (sección):** velo (`overlay_*`), caja (`text_panel`…), altura, color de texto, `seal_text`, `show_scroll`, y navegación (`nav_dots`, `nav_arrows`, `nav_position`, `autorotate`, `interval`, `transition`).
- **Snippet `santavila-hero-slide.liquid`:** renderiza el contenido de un slide (media + velo + inner) para no duplicar markup entre legacy y bloques.

## Estructura de capas (por slide)
`.sv-hero` (position: relative, min-height, overflow hidden) → N× `.sv-hero__slide` (absolute, inset:0, flex flex-end):
- `.sv-hero__media` (z0, imagen `cover`)
- `.sv-hero__slide::after` velo (z1, usa `--sv-ov-base/grad`)
- `.sv-hero__inner` → `.sv-hero__box` (z2, texto/CTAs/sello)

Nav y "Descubre" sobre todo (z3).

## Transición
Slides apilados en absolute; activo = `opacity:1; transform:none`, inactivos = `opacity:0` (+ `translateX` si `transition: slide-fade`). Cambia con clase `.is-active`. Sin "track" (más robusto para full-bleed).

## Navegación (JS vanilla, sin librerías)
- Puntos y/o flechas (configurable) + posición.
- Teclado ←/→, **swipe** en móvil (touchstart/end), foco accesible, `aria-live="polite"` en el viewport, dots con `aria-label` y `aria-current`.
- **Auto-rotación:** activable + intervalo; **se pausa** en hover/focus y con `prefers-reduced-motion: reduce` (no auto-rota).
- Sin dependencias. Primera imagen `eager` (LCP), resto `lazy`.

## Fuera de v1
- **Split screen** (2 slides a la vez). Se añade en v1.1 si se quiere.

## Validación
1. Compila (PUT 200) en DEV.
2. **Legacy intacto:** sin bloques, el hero se ve igual que hoy (verificado en live).
3. El dueño añade 2-3 slides desde el editor para activar el carrusel (no toco `index.json`).
4. Responsive: 1 slide visible siempre; swipe + dots en móvil.

## Líneas rojas
- No tocar `index.json` (home del compañero) ni los otros 3 ficheros pendientes.
- No romper el hero actual: el camino legacy debe ser idéntico al de hoy.
