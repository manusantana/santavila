# foto-producto-ia · skill portable

Galería de producto con IA —packshot, ambiente, detalle, el dato que decide la compra— con
fidelidad al producto real. **Cualquier producto físico, cualquier proveedor, cualquier tienda.**

## Instalar en otra máquina o proyecto

```bash
# 1 · skill personal — disponible en TODOS tus proyectos
cp -r foto-producto-ia ~/.claude/skills/

# 2 · o solo para un proyecto
cp -r foto-producto-ia <proyecto>/.claude/skills/
```

Se activa solo cuando el encargo lo pide (generar/rehacer fotos de producto, fichas con una sola
foto, reemplazar fotos de proveedor en baja resolución). También se puede invocar por nombre.

## Cómo se usa en un proyecto nuevo

1. **Responde el cuestionario** (`cuestionario.md`) — 12 preguntas, 4 bloques. Los bloques 1 y 4
   son obligatorios: son los que impiden inventar el producto y prometer de más.
2. **Guarda las respuestas** en `docs/<proyecto>/BRIEF_IMAGEN.md`. Es la fuente de verdad de todas
   las tandas y lo que necesita quien te releve.
3. **Genera una ficha piloto** y mide en ella tu coste unitario real. Presupuesta con ese número,
   no con el teórico.
4. **A partir de ahí, en tandas**, con el QA del Paso 5 delante.

## Qué NO trae

Deliberadamente fuera, porque cambia en cada proyecto:

- **El publicador.** Subir a Shopify, WooCommerce, PrestaShop o un PIM es específico de cada
  tienda. El skill acaba en "imagen aprobada"; publicarla es tu integración.
- **El overlay de la toma 5.** El script de cotas depende de tu tipografía y tu paleta. El skill
  dice **qué reglas** cumple (contorno automático, etiqueta explícita, de extremo a extremo,
  detector verificado); el código lo pones tú.
- **El motor de imagen.** Escrito y medido sobre modelos tipo *Nano Banana / Seedream / Flux* vía
  Higgsfield. Las tres reglas de mecánica (prompt corto en edición, generar a 1k y upscalar
  después, describir física y no calidad) se repiten en todos los motores probados, pero comprueba
  los límites del tuyo.

## Origen

Destilado de una producción real de ~120 fichas de ecommerce. Cada regla nació de un fallo que
llegó a publicarse o estuvo a punto — no de teoría.

Su origen es un skill de proyecto mucho más largo y específico (mobiliario de exterior, un
proveedor concreto, una marca concreta). **Este es el poso genérico**: si en tu proyecto acumulas
reglas propias, van en un skill de proyecto que se apoya en este, no dentro de este.
