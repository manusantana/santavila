# Informe de Auditoría GEO: Santavila

**Fecha de auditoría:** 2026-05-30
**URL:** https://santavila.com
**Tipo de negocio:** E-commerce (mobiliario de exterior premium) — Shopify
**Páginas analizadas:** 7 (home, 2 colecciones, 2 productos, contacto, robots/llms/sitemap)
**Idiomas:** ES (es-ES) + EN, con hreflang

---

## Resumen ejecutivo

**GEO Score global: 37/100 (Crítico–Pobre)**

Santavila tiene una **base técnica excelente y poco común** para una tienda nueva: SSR de Shopify, robots.txt que no bloquea crawlers de IA, sitemap multilingüe, `llms.txt`, endpoint UCP/MCP y sitemap agéntico (preparado para compra asistida por IA vía Shop skill). El problema no es la infraestructura, es el **contenido y la autoridad**: las fichas de producto tienen ~25 palabras, las colecciones tienen 0 texto descriptivo, no hay reseñas, no hay contenido tipo FAQ/guía de compra, y la marca es **invisible fuera del dominio** (sin menciones en Trustpilot, Wikipedia, Reddit ni resultados indexados). Hoy, un motor de IA puede *rastrear* Santavila perfectamente, pero **no tiene casi nada que citar ni señales para confiar en la marca**. Esa es exactamente la palanca de mejora: el techo técnico ya está puesto, falta llenarlo de contenido citable y construir presencia.

### Desglose de puntuación

| Categoría | Score | Peso | Ponderado |
|---|---|---|---|
| AI Citability | 30/100 | 25% | 7,5 |
| Brand Authority | 12/100 | 20% | 2,4 |
| Content E-E-A-T | 28/100 | 20% | 5,6 |
| Technical GEO | 78/100 | 15% | 11,7 |
| Schema & Structured Data | 55/100 | 10% | 5,5 |
| Platform Optimization | 40/100 | 10% | 4,0 |
| **GEO Score global** | | | **≈37/100** |

---

## Problemas críticos (corregir de inmediato)

1. **La marca no existe como entidad para la IA.** Búsquedas de "Santavila muebles de exterior" devuelven competidores (muebles-exterior.com), no a Santavila. Sin presencia off-site, ningún modelo recomendará la marca aunque rastree el sitio. → Construir señales de entidad (ver Plan, Semanas 2-4).
2. **Contenido de producto no citable.** Ficha de ejemplo (`banco-de-exterior-108-cm`): ~25 palabras de descripción. Sin materiales, sin uso recomendado, sin cuidado/mantenimiento, sin garantía. Un modelo no puede extraer un párrafo útil. → Reescritura de fichas con estructura citable.
3. **Colecciones con 0 palabras de contenido.** `/collections/sillas-de-exterior` va directa del H1 al grid de productos. No hay introducción, ni guía de compra, ni FAQ. Es la página que mejor podría posicionar para consultas tipo "mejores sillas de exterior" y está vacía. → Añadir texto + FAQ por colección.

## Problemas de prioridad alta (≤ 1 semana)

4. **Sin `meta description`** detectada en home, colecciones, contacto ni producto. Shopify la genera vacía si no se rellena. Impacta CTR en Google y el snippet que la IA resume.
5. **Sin reseñas / `AggregateRating`.** No hay prueba social ni en la página ni en el schema. Las reseñas son una de las señales más citadas por la IA en e-commerce.
6. **E-E-A-T débil.** Solo hay página de contacto (~280 palabras de mensaje de marca). No hay dirección física, teléfono, "Sobre nosotros" con historia/equipo, ni señales de confianza (devoluciones, envíos, garantía visibles).
7. **`llms.txt` orientado a agentes de compra, no a contenido.** Excelente que exista, pero hoy describe protocolo UCP; no lista las páginas/colecciones clave que quieres que la IA conozca y cite.

## Problemas de prioridad media (≤ 1 mes)

8. **Falta `BreadcrumbList` schema** en producto/colección (ayuda a la IA a entender jerarquía).
9. **Falta `FAQPage` schema** (no hay FAQ que marcar todavía — crear primero el contenido, luego el schema).
10. **Colecciones sin `ItemList` schema.**
11. **Alt text de imágenes mínimo** — solo la imagen principal del producto lo tiene; faltan en galería.
12. **Sin presencia en plataformas que la IA cita** (Reddit, YouTube, Wikipedia, foros de jardín/decoración).

## Problemas de prioridad baja (optimizar cuando se pueda)

13. Verificar `canonical` explícito por página (Shopify normalmente lo emite; confirmar en el tema).
14. Open Graph presente pero ampliable (descripciones más ricas).
15. Revisar jerarquía de encabezados H2/H3 dentro de fichas una vez ampliadas.

---

## Profundización por categoría

### AI Citability (30/100)
El sitio es rastreable pero ofrece muy poco texto extraíble. La ficha de producto tipo es una sola frase de marketing ("El banco SEVILLA combina líneas clásicas y resistencia estructural...") más una tabla de 3 dimensiones. Las colecciones no tienen ni una frase. Para que ChatGPT/Perplexity citen a Santavila ("¿qué banco de exterior comprar?"), necesitan párrafos autónomos que respondan: qué es, de qué material, para qué espacio, cómo se mantiene, cuánto dura, cuánto cuesta. **Mayor oportunidad de todo el informe.**

### Brand Authority (12/100)
Cero menciones de terceros encontradas. No hay perfil de Trustpilot, ni Wikipedia, ni hilos de Reddit, ni canal de YouTube, ni reseñas en Google visibles en búsqueda. Los modelos infieren confianza a partir de menciones cruzadas; sin ellas, Santavila no es una "entidad" reconocible. Es normal en una tienda nueva, pero es el segundo mayor freno por peso (20%).

### Content E-E-A-T (28/100)
Mensaje de marca correcto pero sin sustancia verificable. Falta: "Sobre nosotros" real (quién hay detrás, dónde, desde cuándo), NAP (nombre-dirección-teléfono) consistente, políticas de envío/devolución/garantía visibles y enlazadas, y cualquier señal de experiencia real con los productos (fotos propias, montaje, durabilidad).

### Technical GEO (78/100) — punto fuerte
- ✅ SSR (HTML completo servido por Shopify) — la IA lee el contenido sin ejecutar JS.
- ✅ `robots.txt` no bloquea GPTBot/ClaudeBot/PerplexityBot (regla `User-agent: *` permisiva en contenido público).
- ✅ HTTPS + HSTS (`max-age` ~91 días), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`.
- ✅ Sitemap multilingüe en tiempo real + `hreflang` ES/EN.
- ✅ `llms.txt` presente y `/.well-known/ucp` responde 200 (preparación agéntica adelantada).
- ⚠️ `meta description` ausente; rendimiento real no verificable de forma fiable en esta auditoría (Cloudflare devolvió challenge en re-test).

### Schema & Structured Data (55/100)
- ✅ `Organization` en todo el sitio.
- ✅ `Product` + `Offer` + `Brand` en fichas de producto.
- ❌ Sin `AggregateRating`/`Review` (no hay reseñas).
- ❌ Sin `BreadcrumbList`, sin `ItemList` en colecciones, sin `FAQPage`.

### Platform Optimization (40/100)
Mejor preparado para **comercio agéntico** (ChatGPT con Shop skill, UCP) que la media del mercado — eso es real y valioso. Pero para **AI Overviews de Google, Perplexity y Gemini**, que dependen de contenido citable y señales de autoridad, está poco preparado por las carencias de las otras categorías. Resultado mixto.

---

## Quick wins (esta semana)

1. **Rellenar `meta description`** en home + las 6 colecciones principales (Shopify > cada página > SEO). Impacto: CTR y snippet.
2. **Escribir 80-120 palabras de introducción + 3-4 FAQ** en las 6 colecciones (sillas, sofás, tumbonas, mesas, parasoles, accesorios). Impacto alto en citabilidad.
3. **Reescribir las 10-15 fichas de producto más importantes** con estructura citable (plantilla abajo). Impacto: el mayor del informe.
4. **Activar app de reseñas** (Judge.me / Shopify Product Reviews) y pedir reseñas a primeros clientes. Genera `AggregateRating` automáticamente.
5. **Crear "Sobre Santavila"** con historia, ubicación, NAP y por qué confiar (materiales, garantía, envíos).

## Plan de acción a 30 días

### Semana 1 — Fundamentos on-page (lo que controlas al 100%)
- [ ] Rellenar `meta description` en home + 6 colecciones + 15 productos top.
- [ ] Redactar intro (80-120 palabras) para las 6 colecciones principales.
- [ ] Crear página "Sobre nosotros" con NAP, historia y propuesta de valor.
- [ ] Hacer visibles políticas de envío, devolución y garantía (enlazadas en footer y fichas).

### Semana 2 — Contenido citable de producto
- [ ] Reescribir 15-20 fichas con la plantilla citable (qué es / material / uso / mantenimiento / medidas / garantía).
- [ ] Añadir bloque FAQ (3-4 preguntas) a cada colección.
- [ ] Completar `alt text` descriptivo en todas las imágenes de esas fichas.
- [ ] Instalar app de reseñas y configurar solicitud automática post-compra.

### Semana 3 — Schema y autoridad de marca (inicio)
- [ ] Añadir `BreadcrumbList` (producto y colección) e `ItemList` (colecciones) vía tema/metafields.
- [ ] Añadir `FAQPage` schema a las FAQ creadas en Semana 2.
- [ ] Crear/optimizar perfil de Google Business + ficha en directorios sectoriales.
- [ ] Abrir perfil en plataformas que la IA cita: Pinterest, YouTube (montaje/ambientes), Instagram con enlace al dominio.

### Semana 4 — Difusión y `llms.txt` de contenido
- [ ] Ampliar `llms.txt` para listar colecciones y páginas clave (no solo protocolo UCP).
- [ ] Publicar 2 guías de blog citables ("Cómo elegir muebles de exterior según tu espacio", "Materiales: aluminio vs. resina vs. madera").
- [ ] Conseguir primeras reseñas en Trustpilot/Google y primeras menciones (foros de decoración/jardín, colaboraciones).
- [ ] Reauditar con `/geo-audit` para medir delta (objetivo: 37 → 55+).

---

## Plantilla de ficha de producto citable

```
[Nombre simple] — [1 frase: qué es y para quién].

Material y construcción: [material principal, acabado, por qué aguanta el exterior].
Uso recomendado: [terraza/jardín/balcón; nº de personas; interior cubierto].
Medidas: Ancho X cm · Fondo Y cm · Alto Z cm · Peso/soporta N kg.
Mantenimiento: [cómo limpiar, si se puede dejar a la intemperie, funda recomendada].
Garantía y envío: [años de garantía, plazo de entrega, devoluciones].

Preguntas frecuentes:
- ¿Resiste la lluvia y el sol? ...
- ¿Necesita montaje? ...
- ¿Qué cojín/funda es compatible? ...
```

Objetivo: cada ficha responde de forma autónoma a las preguntas que un usuario haría a ChatGPT, en párrafos de 40-60 palabras fáciles de extraer y citar.

---

## Apéndice: páginas analizadas

| URL | Hallazgo principal |
|---|---|
| `/` (home) | Solo `Organization` schema; sin meta description; SSR ok |
| `/collections/sillas-de-exterior` | 0 palabras de contenido; sin FAQ; sin meta description |
| `/products/banco-de-exterior-108-cm` | Schema Product+Offer+Brand ok; descripción ~25 palabras; sin reseñas |
| `/pages/contact` | ~280 palabras de marca; sin NAP, equipo ni prueba social |
| `/robots.txt` | Permisivo con IA; sitemap declarado; nota anti-checkout automático |
| `/llms.txt` | Existe; orientado a protocolo UCP/agentes, no a listar contenido |
| `/sitemap.xml` | 10 sub-sitemaps ES/EN + sitemap agéntico |
