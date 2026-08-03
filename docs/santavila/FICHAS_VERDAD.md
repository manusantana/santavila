# Fichas de verdad del producto — paso 0 obligatorio antes de generar

> **Por qué existe este documento.** El 2026-07-29 se publicaron imágenes que cambiaban el material del
> tablero de una mesa (HPL gris cemento → piedra caliza; y en el segundo intento → gris claro brillante).
> La causa no fue el modelo: fue **empezar a generar sin haber leído el producto**. Este documento es el
> paso 0 del pipeline: **antes de tocar nada, se abre la foto real a resolución nativa, se recorta cada
> componente y se escribe aquí lo que hay**. Si un material no se puede determinar con certeza,
> **se escribe "NO DETERMINADO" y esa toma no se genera.**

## Regla
1. **Nada se genera sin ficha.** Sin fila en esta tabla, no se lanza ni un job.
2. **La ficha se escribe mirando el píxel**, no la descripción ni el título ni la memoria.
3. **Lo que no se ve con certeza, no existe.** No se deduce, no se completa, no se "interpreta".
   Si el tablero está tapado por un cojín en la única foto disponible → NO DETERMINADO → **no se hace
   ninguna toma en la que ese tablero aparezca**.
4. **La ficha se copia literalmente al prompt**, incluyendo la negación de lo que el modelo tiende a
   inventar (`not stone, not wood, no grain`).
5. **El QA se hace contra la ficha**, no contra el packshot propio (el packshot también puede estar mal).

## Cómo se lee un tablero (los 4 datos que hay que anotar SIEMPRE)
| Dato | Valores posibles | Por qué importa |
|---|---|---|
| **Material** | HPL/compacto · cerámico · cristal · lamas de aluminio · resina | Es lo que el modelo reescribe primero |
| **Tono** | claro / medio / oscuro + color | Un HPL gris cemento oscuro convertido en gris claro **ya es otro producto** |
| **Acabado** | liso mate · liso brillante · lamas (y ANCHO de lama) · veteado sutil | "Liso" y "de lamas" se confunden a tamaño miniatura |
| **Canto** | fino enrasado · grueso · con junta oscura · de cristal | Define si la mesa se lee como **una pieza** o como bandeja sobre base |

## Registro

| Producto | Chasis | Tejido | **Tablero: material · tono · acabado · canto** | Otros |
|---|---|---|---|---|
| **Acapulco 2 pl.** `set-jardin-2-plazas-moderno-...-mesa-4` | aluminio antracita mate | gris claro liso | **HPL/cerámico · GRIS CEMENTO MEDIO-OSCURO · mate con veta muy sutil · canto FINO enrasado en el marco antracita** → la mesa se lee como **una sola pieza** | reposapiés en la foto **NO** incluido |
| **Acapulco 3 pl.** `...-mesa-5` | aluminio blanco | gris claro | **CRISTAL translúcido gris · canto de cristal visible sobre marco blanco** | — |
| **Bellagio 2 pl.** `set-jardin-2-plazas-elegante-...-mesa-3` | aluminio blanco | gris medio | **LAMAS de aluminio BLANCAS · juntas visibles** (⚠️ NO es tablero liso) | reposapiés **NO** incluido |
| **Diva 3 pl.** `set-jardin-bicolor-3-plazas-...` | blanco + paneles de lamas antracita | crudo | **tablero BLANCO liso sobre faldón de LAMAS antracita · patas blancas** | — |
| **Diva 2 pl.** `set-jardin-bicolor-2-plazas-...` | tórtola + paneles de lamas | crudo con ribete | **tablero LISO efecto madera MARRÓN sobre faldón de lamas antracita** (⚠️ no es tablero de lamas) | reposapiés **NO** incluido |
| **Damasco 2 pl.** `set-jardin-2-plazas-elegante-...-mesa` | tórtola + cuerda beige | crudo | **LAMAS de aluminio tórtola · lamas anchas** | — |
| **Rinconera HPL** `set-rinconera-...-sofisticado` | aluminio blanco | arena | **HPL blanco liso · canto OSCURO grueso** | — |
| **Bolonia XL 3 pl.** `set-jardin-3-plazas-contemporaneo-...-mesa-2` | aluminio azul marino | azul claro grisáceo | **LAMAS de aluminio azul marino · marco perimetral más ancho** | reposapiés **NO** incluido |
| **CUPRA 3 pl.** `set-jardin-3-plazas-sofisticado-...-mesa-2` | aluminio tórtola mate | verde salvia | **LAMAS de aluminio tórtola · lamas ESTRECHAS y numerosas, dentro de marco más ancho** | 2 reposapiés **NO** incluidos |
| **Albania 3 pl.** `...-mesa-3` | tórtola | verde salvia | **NO DETERMINADO** — el export de imágenes apunta a otro producto; falta la foto real de esta ficha | — |
| **Brandon 3 pl.** `set-jardin-aluminio-3-plazas-...` | aluminio antracita, perfil fino | **chenille gris con JACQUARD tono sobre tono** (motivo irregular tipo pinceladas/grafismos en gris claro) — NO liso | **2 mesas redondas nido · LISO gris cemento · mate · canto fino · patas cilíndricas finas** | ⚠️ ver ficha ampliada abajo |
| **Brandon 2 pl.** `set-jardin-aluminio-2-plazas-...` | ídem | ídem (jacquard) | ídem | — |
| **Sofá 220×90** `sofa-terraza-aluminio-3-plazas-...` | ídem | ídem (jacquard) | — (pieza suelta, sin mesa) | — |
| Balinesa 198 · Balinesa 160 · Parasol Roma · LEISA · Tumbona | — | — | **PENDIENTE** — originales localizadas en `images_optimized/` e `images_balliu/` del repo, falta auditarlas | — |
| **Mesa Java + sillas Etna** `balliu-mesa-exterior-hpl-140-180100-cm-8e073aab` (1.575 €) | mesa y sillas en **aluminio GRIS TÓRTOLA mate**, patas de sección cuadrada gruesa a plomo | sillas Etna: **textileno BLANCO ROTO/CRUDO**, trama fina visible, tensado; respaldo curvo con **remate superior de aluminio** y **remaches visibles** en la unión brazo-respaldo; con brazos planos, apilables | **HPL · GRIS TOPO MEDIO · MATE y LISO · junta transversal central visible (es extensible) · canto FINO enrasado en el marco tórtola** → se lee como una pieza | Leída sobre `Balliu_Mesa-Java2` (1200×921) y `java-mesa-aluminio-ambiente` (800×614), **no** sobre la pos-0. **NO DETERMINADO:** el mecanismo interno de extensión (solo visible en otra variante de color) → no se genera toma de ese detalle |

> ⚠️ **Fallo de identidad detectado el 2026-07-30 (clase A0, fuera del alcance de la auditoría de las 25).**
> La **foto principal (pos-0) de la mesa Java** es, byte a byte, la foto de la **mesa Atlanta**
> (`balliu_mesa-extensible-de-aluminio-atlanta.jpg`, distancia perceptual **0** entre ambas pos-0).
> No son la misma mesa: la **Atlanta tiene tablero de LAMAS** y la **Java tiene tablero HPL LISO** — lo dicen
> su descripción y sus otras cuatro fotos. Es decir, la Java se vende con la foto de otro modelo como imagen
> principal. **Pendiente de corregir en la ficha.** Por eso la ficha de verdad de arriba se ha escrito
> deliberadamente sobre las fotos de ambiente, ignorando la pos-0.
>
> Alcance sin comprobar: la colección **Mesas (73 productos)** nunca se ha auditado por identidad. Este fallo
> apareció al mirar la primera mesa; conviene revisar las demás con el mismo método (comparación de huella
> perceptual entre pos-0 de productos distintos).

---

## FICHA AMPLIADA · Brandon 3 plazas — SKU 557-010885 (5.249 €, el de mayor ticket)
*Leída el 2026-08-01 sobre `brandon 8 (3).png` (1536×1024) a resolución nativa, recorte por componente.*

| Componente | Lo que hay **de verdad** |
|---|---|
| **Chasis** | Aluminio **antracita mate**, perfil **fino**. Marco perimetral en U de esquinas redondeadas que envuelve el lateral; **tornillos vistos** en el perfil. Patas **cilíndricas finas** antracita, ligeramente separadas de la esquina |
| **Tejido** | Chenille **gris medio** con **JACQUARD tono sobre tono**: trazos irregulares tipo grafismo en gris más claro. **Está en TODAS las piezas** — asiento, respaldo, brazos y panel lateral. **NO es liso** |
| **Brazos** | **Tapizados y gruesos**, con vuelta hacia fuera en la coronación (rulo). No son de aluminio desnudo |
| **Cojines** | Sofá: 3 de asiento + 3 de respaldo. Sillón: 1 + 1. Todos del mismo tejido; **no hay cojín decorativo distinto** |
| **Mesas** | **2 redondas nido** de distinto diámetro. Tablero **gris cemento medio, LISO y MATE**, veteado muy sutil, **canto fino redondeado**. Pie de 4 tubos finos antracita |
| **Cotas** | **NO DETERMINADO** — el proveedor no da medidas de este SKU → **esta ficha no lleva imagen de medidas** |
| **Piezas del lote** | ⚠️ **NO DETERMINADO — pendiente de Sergio.** La foto muestra **2 mesas**; la descripción dice *"Incluye: … y mesa"* (singular); el SKU hermano 557-010884 (Brandon-7, 2 pl.) **sí** lista `LUNA-44 SET MESAS CENTRO 80 + 60` como segunda fila, y el 557-010885 **no**. Hasta resolverlo no se fija el conteo de mesas del packshot |
| **A quitar de la escena** | La **mujer sentada** y el atrezzo del proveedor (copa de vino, cuenco de uvas). El fondo original —techo de madera oscura, carpintería negra y **vegetación tropical (estrelitzia)**— hay que **negarlo por nombre** en el prompt |

**Riesgo específico de esta ficha:** es el producto donde ya se publicó el **jacquard eliminado** en 3 fichas.
El QA del tejido es el bloqueante nº1 aquí, y se hace contra este recorte, no contra el packshot generado.

---

## Estado de auditoría de lo ya publicado
Ver [`AUDITORIA_FIDELIDAD_2026-07-29.md`](AUDITORIA_FIDELIDAD_2026-07-29.md) y
[`LECCIONES_FIDELIDAD.md`](LECCIONES_FIDELIDAD.md).

## Galerías rehechas con el método nuevo (ficha → generar → QA contra ficha → identidad → publicar)
| Ficha | € | Fecha | Notas |
|---|---|---|---|
| **Brandon 3 pl.** | 5.249 | 2026-07-30 | 5/5 aprobadas a la primera. Jacquard correcto en las 5 |
| **Brandon 2 pl.** | 4.679 | 2026-07-30 | El QA rechazó el ASMR (jacquard demasiado tenue, leído como rayas) y se regeneró antes de publicar |
