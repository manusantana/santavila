# Punto de inflexión — 20 de agosto de 2026

> Este documento cierra una semana en la que se publicaron tres galerías, se retiró un método
> entero y se descubrió que el Paso 0 podía devolver el producto equivocado. Recoge **lo que
> cambia a partir de hoy** y **el estado real del catálogo**. Si algo aquí choca con un documento
> anterior, manda este.

---

## 1. La regla que impide volver atrás

**El problema, con las palabras de Sergio:** *"esto hemos pasado mil veces y no puede ser que
tengamos aún errores así y tengamos que volver atrás."*

Tenía razón, y la causa no era el descuido: era que **una imagen publicada no dejaba rastro de qué
se le había verificado**. Cada criterio nuevo obligaba a abrir las fichas ya publicadas y mirarlas a
ojo, una a una. Eso no escala y siempre acaba en "déjame comprobar una cosa antes de seguir".

**Lo que cambia:**

| Antes | Ahora |
|---|---|
| Publicar y olvidar | `publicar_galeria_producto.py` escribe cada publicación en `docs/santavila/_verificaciones.json` (fichero, píxeles, megapíxeles, longitud del alt, fecha) |
| Comprobar una ficha a mano cuando surge una duda | `scripts/auditar_galerias.py` recorre **las 171 fichas activas** y aplica todos los criterios objetivos de una pasada |
| Un criterio nuevo vive solo en mi cabeza | Un criterio nuevo **se añade al auditor**, y el auditor se pasa sobre todo lo publicado |

**La regla, en una línea:**
> **Un criterio que no está en el auditor no existe.** Si descubro uno nuevo, primero lo
> programo y lo paso sobre todo el catálogo; solo después sigo con la ficha que estaba haciendo.

Y su corolario: **nunca más "voy a comprobar una cosa antes de seguir"**. Se ejecuta el auditor.

---

## 2. Lo que se ha retirado y lo que se ha añadido

### Retirado

**El método A1** (recortar el producto de la foto del proveedor y componerlo sobre la escena).
Producía collages: el recorte arrastra la luz del estudio del proveedor y no admite sombra de
contacto, oclusión ambiental ni rebote de color. Cinco imágenes así llegaron a producción en la
ficha de 5.249 € y hubo que retirarlas.

**Aprobar por métrica.** Aquellas cinco cumplían todos los números. Un número **rechaza** una
imagen; ninguno la **acepta**.

### Añadido

| Regla | De dónde sale |
|---|---|
| **Test de collage** — sombra de contacto, sombra proyectada, oclusión ambiental, rebote de color, grano coherente, borde al 200 %, y la prueba de los dos tapados | Los cinco collages del Brandon-8 |
| **Las tres promesas** — vida, lujo, deseo; se responden por escrito antes de presentar cada imagen | Sergio, 20-08 |
| **Lo no incluido se declara** — o no se dibuja, o va en el texto al estilo Zara Home, con enlace si se vende | El reposapiés del Bolonia XL-8 |
| **Atrezzo medido** — todo prop se mide en cm reales usando una cota del mueble como regla; 0 texto en props | El libro de 28 cm |
| **Reparar sin regenerar** — reencuadrar → reparar fondo liso sin IA → regenerar. Si tapar el defecto exige repintar producto, no se repara | El canto de la mesa que el libro ocultaba |
| **Swap de fondo puro** — pedirle al modelo que recoloque le hace redibujar, y al redibujar inventa | Cinco descartes con respaldos de lamas |
| **Encuadre que no muestre caras no fotografiadas** | La trasera del sillón Bolonia |
| **Un motivo se mide en banda media**, no con la métrica de los hilos; y el parche va en la misma zona anatómica de la pieza | Casi tumbo una imagen buena del Brandon-7 |

Todo el detalle operativo está en el
[`SKILL.md`](../../.claude/skills/santavila-imagen-producto/SKILL.md) v5.

---

## 3. El Paso 0 podía devolver otro producto

La referencia `557-010884` figura en los CSV de Hevea como **dos productos distintos**:
"LUNA-44 SET MESAS CENTRO 80+60" (435 €) y "BRANDON-7 SET SOFA 2 PLAZAS" (3.865 €). El Paso 0 se
quedaba con el primero: devolvía la foto de **unas mesas** para una ficha de 4.679 €.

Ya desempata por el **coste real de la variante** contra el exworks de cada candidato, y dice por
qué lo hace. La columna del coste se busca por contenido, porque cada CSV del proveedor la nombra
distinto (`Precio exworks (sin iva)`, `Precio neto exworks`, …).

**Cómo se detecta una pieza fantasma:** cruzar la foto con la fórmula de composición de la tarifa
y con la suma de PVP. Funcionó dos veces esta semana, al euro:
- `2XA+C+D` Bolonia XL-8 → 1.740 + 840×2 + 470 = **3.890 €**
- `2xA+B+D` Brandon-7 → 1.470 + 980×2 + 435 = **3.865 €**

---

## 4. Estado real del catálogo (auditoría del 20-08)

`python3 scripts/auditar_galerias.py`

| | |
|---|---|
| Fichas activas | **171** |
| Con galería completa (≥5 imágenes) | **55** |
| Con **una sola imagen** | **79** — 88.099 € de catálogo |
| Con alguna imagen **por debajo de 2000 px** | **143** — 138.930 € |
| Con algún **texto alternativo vacío** | **80** — 73.569 € |
| Sin ninguna imagen | **0** ✓ |
| Con imágenes duplicadas dentro de la ficha | **0** ✓ |
| Con media que Shopify rechazó (no READY) | **0** ✓ |
| Con foto compartida con otra ficha | **0** ✓ |

Los cuatro ceros son deuda que ya estaba saldada. Lo que queda es **volumen**, no errores.

---

## 5. Cuánto cuesta terminar el catálogo

**Medido esta semana**, créditos de Higgsfield por galería completa de 5 imágenes, descartes incluidos:

| Ficha | Créditos | Por qué |
|---|---|---|
| Bolonia XL-8 | **22** | Tapicería lisa: el modelo la reproduce a la primera |
| Brandon 7 | **64** | Jacquard con motivo: dos packshots y dos detalles descartados |

El coste lo manda **el material**, no el precio del mueble. Con una mezcla de 60 % telas lisas y
40 % con motivo sale una media de **~40 créditos por ficha**.

| | |
|---|---|
| Galerías ya hechas | 29 |
| Fichas activas pendientes | **~142** |
| Coste estimado | **142 × 40 ≈ 5.700 créditos** (rango 3.100–9.100 según la mezcla de materiales) |
| Saldo actual | 921 → alcanza para **~23 fichas** |

### Tres palancas para bajarlo

1. **Trabajar por familia, no por ticket.** Brandon tiene 5 fichas en el catálogo; Bolonia XL, 5;
   Yina, 7. La primera de cada familia paga el aprendizaje (hábitat, prompt del material,
   encuadres que evitan las caras no fotografiadas); las hermanas reutilizan todo. Estimación:
   **−40 % en la segunda y siguientes**. Con esta palanca el total baja a **~3.900 créditos**.
2. **Receta corta para ticket bajo.** Packshot + un ambiente + medidas cuesta la mitad que las
   cinco tomas, y para una ficha de 300 € es suficiente.
3. **No pelearse con un material que el modelo no sabe hacer.** A la segunda, se cambia el
   encuadre para que ese material deje de mandar en el cuadro. Los 42 créditos de diferencia entre
   el Bolonia y el Brandon son exactamente eso.

---

## 6. Lo que sigue pendiente

- **Los títulos de las piezas Bolonia** dicen 215 y 80 cm (dato del CSV); el catálogo dice 200 y 78.
  Corregirlos toca SEO — trabajo del compañero.
- **El texto de composición y el enlace al reposapiés** en la ficha del Bolonia XL-8: redactado,
  sin aplicar, porque toca la descripción.
- **80 fichas con alt vacío** y **143 con imágenes por debajo de 2000 px**: se resuelven solas
  según avancen las galerías.
