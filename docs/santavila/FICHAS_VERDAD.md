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
| **Brandon 3 pl.** `set-jardin-aluminio-3-plazas-...` | aluminio antracita, perfil fino | **chenille gris con JACQUARD tono sobre tono** (motivo irregular tipo pinceladas/grafismos en gris claro) — NO liso | **2 mesas redondas nido · LISO gris cemento · mate · canto fino · patas cilíndricas finas** | — |
| **Brandon 2 pl.** `set-jardin-aluminio-2-plazas-...` | ídem | ídem (jacquard) | ídem | — |
| **Sofá 220×90** `sofa-terraza-aluminio-3-plazas-...` | ídem | ídem (jacquard) | — (pieza suelta, sin mesa) | — |
| Balinesa 198 · Balinesa 160 · Parasol Roma · LEISA · Tumbona | — | — | **PENDIENTE** — originales localizadas en `images_optimized/` e `images_balliu/` del repo, falta auditarlas | — |

## Estado de auditoría de lo ya publicado
Ver [`AUDITORIA_FIDELIDAD_2026-07-29.md`](AUDITORIA_FIDELIDAD_2026-07-29.md) y
[`LECCIONES_FIDELIDAD.md`](LECCIONES_FIDELIDAD.md).

## Galerías rehechas con el método nuevo (ficha → generar → QA contra ficha → identidad → publicar)
| Ficha | € | Fecha | Notas |
|---|---|---|---|
| **Brandon 3 pl.** | 5.249 | 2026-07-30 | 5/5 aprobadas a la primera. Jacquard correcto en las 5 |
| **Brandon 2 pl.** | 4.679 | 2026-07-30 | El QA rechazó el ASMR (jacquard demasiado tenue, leído como rayas) y se regeneró antes de publicar |
