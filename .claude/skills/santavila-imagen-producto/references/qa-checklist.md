# QA gate (antes de subir) — bloqueante

> ## ⛔ NADA DE COMIDA NI BEBIDA (Sergio, 03-08-2026)
> Vendemos **decoración de exterior**, no una comida. Donde este documento diga taza, copa, vino, café, té,
> vermut, cerveza, aperitivo o "consumible", **está derogado**.
> **Atrezzo vigente:** libro · maceta de barro o gres con olivo/romero/lavanda · manta o plaid de lino ·
> cesta · sombrero de paja · farol apagado · cerámica artesana **vacía**.
> En escena de carril FRÍO la maceta va en **gres gris o piedra**, nunca terracota naranja.


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

## D.bis · Escala — BLOQUEANTE (línea roja del dueño, ROL §13.bis)
Sin cuerpo entero en la galería, la escala se ancla **exclusivamente en objetos cotidianos**:
- [ ] **Mano humana 18 cm** (obligatoria en toda toma con manos) · libro cerrado 22–25 cm · maceta 25–40 cm Ø · romero/olivo en maceta 60–120 cm · cojín de asiento 45–60 cm.
- [ ] **Las COTAS REALES del Paso 0 mandan sobre el encuadre:** si el sofá mide 220 cm y la mesa 80, la mesa es 0,36 de su ancho **y lo sigue siendo al acercarse**. Un mueble que encoge al acercar la cámara = rechazo.
- [ ] Producto **≥78 % del ancho** en packshot y **≥45 %** en ambiente (nunca <30 %). Cielo ≤25 %.
- [ ] **Plano de cierre** sólido a 2–5 m detrás (seto, muro, pérgola). Prohibida la fuga al infinito tras el mueble.
- [ ] Perspectiva única: una línea de horizonte, una escala física para todo el cuadro. Patas apoyadas con su sombra.
- [ ] **Mano gigante o prop desproporcionado invalida la toma** aunque la textura sea perfecta.

## D.ter · Presencia humana — solo MANOS (decisión 31-07)
- [ ] **Nunca cuerpo entero ni cara.** Solo manos. El §10 del ROL está archivado.
- [ ] Manos: 5 dedos, sin fusiones, muñeca natural. **Verificar tras el upscale a 4K**, no en la previa.
- [ ] Mano que TOCA el producto = máximo escrutinio: si falla, rechazo aunque el resto sea perfecto.
- [ ] **Escena sin persona = escena EN REPOSO:** cojines mullidos y lisos, **sin vapor**, sin huella de cuerpo.
      El vapor y el cojín hundido implican que alguien está ahí ahora → tell de IA en una foto vacía.

## E · Medidas — BLOQUEANTE **cuando aplica** (solo si el Paso 0 dio cota)
> Hoy **103 de 176 fichas no tienen cotas reales**. Sin cota verificada, la ficha simplemente no lleva esta imagen.
- [ ] Cota = **dato verificado** del proveedor/ficha/metafield. Si no hay dato, la cota NO se dibuja.
- [ ] Se sabe **cuál es ancho y cuál alto**. Si la ficha da "72×75" sin desglosar → **preguntar**; jamás deducirlo de la foto (en 3/4 unos centímetros son indistinguibles).
- [ ] Etiqueta **explícita**: `Ancho · N cm` / `Alto · N cm`. Nunca solo "N cm".
- [ ] Cada línea abarca el producto **de extremo a extremo** en su eje, con topes en los extremos REALES (contorno automático, no medido a ojo).
- [ ] La cota vertical va en el lado **limpio** (la sombra suele caer a la derecha).
- [ ] Overlay determinista con `scripts/overlay_medidas_producto.py` — **nunca** cotas generadas por IA.

## "Tells" de IA en la lógica de la escena — BLOQUEANTE (ambientes con vida)
- **Props con dueño y con lógica:** cada objeto está donde alguien lo habría dejado, no repartido de adorno. Nada duplicado sin motivo. *(La antigua regla de consumibles queda sin objeto: ya no hay comida ni bebida en escena.)*
- **Deformación por peso:** cojín donde se sienta alguien → hundimiento y arruga; respaldo cede; ropa pliega. Persona sobre cojín intacto = "flotando" = tell.
- **Coherencia física:** sombras/reflejos/dirección de luz de personas y props concuerdan con el sol único; cada objeto con su sombra de contacto; recuento sillas/personas/sombras cuadra.
- **Escala doble puerta:** si "lee personas grandes", **mídelo lado a lado** antes de concluir — suele ser composición (dos personas llenando el sofá), no tamaño. Fix: separar figuras (≥1 cojín libre), enderezar espalda, plano más cerrado. No encoger personas.

## Confusiones de SKU auditadas (vigilar)
Set 2 plazas en ficha de 3 · foto de detalle de pata como hero · tela de repuesto como portada de tumbona · pie de parasol como producto · conjunto completo en ficha de mesa aislada · cutout reventado a <800 px como única foto.
