# Cuestionario de arranque

**Se responde UNA vez por proyecto**, antes de la primera imagen. Guarda las respuestas en el repo
(`docs/<proyecto>/BRIEF_IMAGEN.md`): son la fuente de verdad de todas las tandas siguientes.

**Bloques 1 y 4: obligatorios.** Sin ellos no se genera — son los que impiden inventar el producto
y prometer de más.
**Bloques 2 y 3: admiten los valores por defecto** de más abajo, pero se enseñan al cliente y se
confirman. Un defecto aceptado a sabiendas es una decisión; uno aplicado en silencio es una
suposición.

**Cómo preguntar:** de golpe, en bloque, no de una en una. La mayoría de clientes responden 12
preguntas en un mensaje si las ven juntas y con ejemplos.

---

## BLOQUE 1 · EL PRODUCTO *(obligatorio — evita inventar)*

**1.1 · ¿Qué se vende exactamente en esta ficha?**
Una pieza suelta, un lote, un pack. Si es un lote: **la lista literal de lo que entra en la caja**.

**1.2 · ¿Cuál es la fuente de verdad del producto?**
Dónde está la foto oficial de mayor resolución y quién la da por buena.
¿Hay catálogo o ficha técnica en PDF? *(suele tener cotas y composición que la web no tiene)*

**1.3 · ¿Qué sale en las fotos del proveedor y NO se vende?**
La pregunta que más dinero salva. Atrezzo, piezas de otro lote, complementos opcionales.
Si el cliente no lo sabe: ¿hay **fórmula de composición** en el catálogo? ¿cuadra la **suma de PVP
de las piezas** con el precio del lote?

**1.4 · ¿Cuál es el dato por el que se devuelve el producto si falla — y está verificado?**
No siempre son centímetros. Es **la magnitud que decide la compra** y que la toma 5 tiene que
resolver:

| Si vendes… | pregunta por |
|---|---|
| mobiliario, electrodoméstico, decoración | cotas en cm — *¿me cabe?* |
| calzado y ropa | talla y **horma/ajuste** — *¿me vale?* |
| cosmética, alimentación, droguería | formato (ml/g) e ingredientes |
| joyería, relojería, accesorio pequeño | **escala real** — *¿de qué tamaño es esto?* |
| electrónica | compatibilidad y puertos |

Anota **qué mide cada número** (con o sin embalaje; alto total o de asiento; talla ES o UK).
Si dos fuentes discrepan, **cuál manda** — por escrito.
→ *Sin dato verificado no se dibuja la toma 5. No se deduce de la foto.*

**1.5 · ¿Hay variantes (color, acabado, tamaño) y foto propia de cada una?**
Variante sin foto propia = variante que **no se genera**.

---

## BLOQUE 2 · MARCA Y ESCENA *(defecto disponible)*

**2.1 · ¿Quién compra esto y dónde lo va a poner?**
No el perfil de marketing: **el espacio físico**. Es lo que decide el hábitat.

**2.2 · ¿Qué mundo NO es el vuestro?**
Casi siempre es más rápido que describir el bueno. *(«nada de resort», «nada de oficina
corporativa», «no somos low cost»)*

**2.3 · ¿Hay paleta, tipografía o marca gráfica que respetar?**
Para el fondo del packshot y la toma de medidas.
**Defecto:** fondo cálido neutro (nunca blanco puro), tipografía mono para las cotas.

**2.4 · ¿Qué atrezzo está permitido, y cuál prohibido?**
Muy concreto. *(Un cliente prohibió comida y bebida en toda escena de exterior: sin esa respuesta
se habrían producido decenas de imágenes inservibles.)*

---

## BLOQUE 3 · DESTINO Y FORMATO *(defecto disponible)*

**3.1 · ¿Dónde se publica y cuántas imágenes admite la ficha?**
**3.2 · ¿Resolución mínima y máxima? ¿límite de peso?**
**Defecto:** ≥2.000 px de lado menor; exportar a ~2.600 px JPEG q92 *(un PNG 4096² pasa de los
límites de la mayoría de plataformas)*.
**3.3 · ¿Qué aspectos hacen falta?**
**Defecto:** 1:1 para packshot y detalle, 4:5 para un ambiente.
**3.4 · ¿Los textos alternativos los escribo yo o los lleva alguien más (SEO)?**
→ *Si los lleva otra persona, no toques títulos ni descripciones. Anota las discrepancias que
encuentres y pásaselas.*

---

## BLOQUE 4 · LO PROHIBIDO *(obligatorio — evita prometer de más)*

**4.1 · ¿Qué NO puede aparecer nunca en una imagen?**
Escenas, objetos, personas, servicios que no prestáis.
*(Ejemplo real: una tienda que no monta a domicilio no puede insinuar montaje propio.)*

**4.2 · ¿Qué afirmaciones no podéis sostener?**
Lo que la imagen no debe sugerir aunque no lo diga: garantías, resistencias, certificaciones.
**Ley 0: si no puedes defenderlo, no lo insinúas.**

**4.3 · ¿Quién aprueba antes de publicar, y qué es "aprobado"?**
¿Basta tu QA o hay validación humana? ¿Publicas en producción o en un entorno de pruebas?

---

## PLANTILLA DE RESPUESTA

Cópiala al repo y complétala.

```markdown
# BRIEF DE IMAGEN · <proyecto>
Fecha · Responde · Aprueba

## 1 · PRODUCTO
- Qué se vende:
- Fuente de verdad:            (URL / carpeta / PDF)
- Sale y NO se vende:
- Cotas verificadas:           (qué mide cada número y de dónde sale)
- Jerarquía si discrepan:      (X manda sobre Y)
- Variantes con foto propia:

## 2 · MARCA Y ESCENA
- Comprador y espacio real:
- Mundos prohibidos:
- Paleta / fondo / tipografía:
- Atrezzo permitido / prohibido:

## 3 · DESTINO
- Plataforma y nº de imágenes:
- Resolución y peso:
- Aspectos:
- Textos alternativos: los lleva ___

## 4 · PROHIBIDO
- Nunca aparece:
- No podemos sostener:
- Aprueba: ___   Publica en: ___

## RECETA ACORDADA
Tomas por ficha: ___    Coste medido por ficha: ___
```

---

## SI EL CLIENTE NO SABE RESPONDER

Pasa en la mitad de los proyectos. **No inventes la respuesta: redúcela a una comprobación.**

| No sabe… | Compruébalo tú |
|---|---|
| qué entra en el lote | fórmula de composición del catálogo; suma de PVP de las piezas |
| las cotas | ficha técnica del PDF; contrástala con el título del producto |
| qué mundo es el suyo | mira sus 3 competidores directos y enséñale dos referencias |
| qué está prohibido | enséñale una imagen de prueba: lo que no le guste, ahí está la regla |

Lo que salga de esas comprobaciones **se escribe en el brief y se le confirma**. Una regla
descubierta es tan válida como una regla dictada — pero solo si queda por escrito.
