# QA gate (antes de subir) — bloqueante

> Del rol §6 + capa de coherencia lógica. Comparar SIEMPRE lado a lado contra la **foto real** de referencia. Falla un solo bloqueante → regenerar, no subir. Registrar el veredicto.

## A · Fidelidad (tolerancia cero) — BLOQUEANTE
- [ ] Geometría, silueta y proporciones idénticas al original.
- [ ] **Conteo 1:1**: listones/lamas/cuerdas, cojines, plazas/módulos, patas, varillas, costuras. Desviación ≠ 0 = rechazo.
- [ ] Material y trama reales (no genéricos); acabado mate/satinado correcto.
- [ ] **Color de chasis y tejido = variante real** (ΔE≤3). Tórtola no vira a beige/rosa; antracita no se aplasta a negro; blanco no amarillea/azulea.
- [ ] Herrajes, juntas y remates respetados. Ninguna cara inventada.

## B · Sin artefactos IA — BLOQUEANTE
- [ ] Verticales a plomo (patas/respaldos/mástiles rectos).
- [ ] Sin fusiones/derretidos/listones fundidos/manos defectuosas/cuerda que se funde.
- [ ] **Sombra de contacto** nace bajo cada apoyo (no flota).
- [ ] **Una sola dirección de luz/sombra**, coherente con las otras fotos de la ficha (no dos soles).
- [ ] Sin HDR falso (halos, claridad global, cielo quemado), sin sobre-sharpen.

## C · On-brand
- [ ] Luz/paleta española creíble; **NO resort, NO chalet**.
- [ ] Fondo cálido (paper/bone), **nunca blanco puro `#FFFFFF`**.
- [ ] Más sombra y textura que color; saturación contenida; máx. 1 acento clay.
- [ ] 0 logos de tercero, 0 watermark, 0 texto generado por IA.
- [ ] Atrezzo ≤5 props; no ocluye el producto; no sugiere montaje nuestro (self-assembly).

## D · Técnico y composición
- [ ] ≥2000 px (objetivo 2400), nítida, sin upscaling que invente trama.
- [ ] Ratio correcto (1:1 packshot/detalle/medidas; 4:5 ambiente B); **cover** en producto.
- [ ] Compone en 1:1 sin aire muerto ni patas/brazos amputados; 8–12 % de aire.
- [ ] Textura del material legible. Escala legible (referente real cuando aplica).

## E · Toma 5 · medidas — BLOQUEANTE (lo más delicado de la galería)
- [ ] Cota = **dato verificado** de ficha/título/metafield. Si no hay dato, la cota NO se dibuja.
- [ ] Se sabe **cuál es ancho y cuál alto**. Si la ficha da "72×75" sin desglosar → **preguntar**; jamás deducirlo de la foto (en 3/4 unos centímetros son indistinguibles).
- [ ] Etiqueta **explícita**: `Ancho · N cm` / `Alto · N cm`. Nunca solo "N cm".
- [ ] Cada línea abarca el producto **de extremo a extremo** en su eje, con topes en los extremos REALES (contorno automático, no medido a ojo).
- [ ] La cota vertical va en el lado **limpio** (la sombra suele caer a la derecha).
- [ ] Overlay determinista con `scripts/overlay_medidas_producto.py` — **nunca** cotas generadas por IA.

## "Tells" de IA en la lógica de la escena — BLOQUEANTE (ambientes con vida)
- **Consumibles = personas, con DUEÑO:** el nº de copas/tazas es coherente con el nº de personas; cada bebida junto a quien la toma (nunca en el lado opuesto de la mesa ni amontonada). Una persona con la copa en la mano no puede tener otra idéntica delante.
- **Deformación por peso:** cojín donde se sienta alguien → hundimiento y arruga; respaldo cede; ropa pliega. Persona sobre cojín intacto = "flotando" = tell.
- **Coherencia física:** sombras/reflejos/dirección de luz de personas y props concuerdan con el sol único; cada objeto con su sombra de contacto; recuento sillas/personas/sombras cuadra.
- **Escala doble puerta:** si "lee personas grandes", **mídelo lado a lado** antes de concluir — suele ser composición (dos personas llenando el sofá), no tamaño. Fix: separar figuras (≥1 cojín libre), enderezar espalda, plano más cerrado. No encoger personas.

## Confusiones de SKU auditadas (vigilar)
Set 2 plazas en ficha de 3 · foto de detalle de pata como hero · tela de repuesto como portada de tumbona · pie de parasol como producto · conjunto completo en ficha de mesa aislada · cutout reventado a <800 px como única foto.
