# Registro de localizaciones por producto (rol §11.2.d)

> Sirve para **no repetir escenarios** entre productos ni dentro de una misma ficha, manteniendo el
> emparejamiento por paleta (§8): se rota **dentro del carril**, nunca cruzándolo.
> Se actualiza al validar cada galería. Referencia: [`ROL_FOTOGRAFO_SENIOR.md`](ROL_FOTOGRAFO_SENIOR.md) §11.

## Cómo se usa
1. Lee el producto → **eje térmico** (frío/neutro/cálido) → **carril**.
2. Filtra el roster §11.1 por ese carril y **ordena por nº de usos ascendente**.
3. Asigna 2 localizaciones (ambiente exterior + ambiente interior del **mismo hábitat**, distinto momento).
4. Bandera: si un producto comparte **≥2** localizaciones con otro del mismo carril → sustituir.

## Registro

| Producto (handle) | Variante / eje | Carril | Ambiente exterior | Ambiente interior (mismo hábitat) | Consumible |
|---|---|---|---|---|---|
| `set-jardin-3-plazas-contemporaneo-sofa-3-plazas-2-sillones-mesa-3` (LEISA) | antracita + gris / **frío** | Frío/piedra | A4 Ático Eixample · A1 Galería Rías Baixas · A6 Patio Salamanca *(receta antigua, 3 ambientes)* | — | café · té helado |
| `tumbona-de-exterior` (Brescia) | sling gris / **frío** | Frío/piedra | Piscina costera (B8-like) | — | agua · toalla |
| `sillon-exterior-estilo-elegante-7275-cm` | antracita + cuerda / **frío** | Frío/piedra | Ático de diseño, mañana | Ático de diseño, atardecer | café · té helado |
| **`set-jardin-aluminio-3-plazas-contemporaneo-...`** (Brandon set) | gris chenille + antracita / **frío** | Frío/piedra | **A3 Villa cántabra** — terraza de granito, mampostería, hortensias | **A3 interior** — galería acristalada con lluvia en el cristal | café + galletas |
| **`set-jardin-3-plazas-sofisticado-...-mesa-3`** (Albania) | verde salvia + gris claro / **neutro-vegetal** | Cálido-neutro | **B4 Huerta de Murcia/Levante** — pérgola de cañizo, gres arena, limonero | **B4 interior** — porche cubierto encalado con vigas | aceitunas + almendras · té helado |
| **`set-jardin-3-plazas-contemporaneo-...-mesa`** (Yina) | cuerda greige + crudo / **cálido-luminoso** | Cálido/cal | **B5 Porxada de marés, Menorca** — piedra clara, sabina, mar desaturado | **B5 interior** — sala payesa con cortina de lino al olivar | higos + vino blanco |
| **`set-rinconera-exterior-hpl-sofisticado-...`** | blanco + arena HPL / **cálido** | Cálido/barro | **B3 Villa Costa Blanca** — tarima miel, pérgola de lamas, piscina residencial | **B3 interior** — porche-salón de microcemento tórtola | limonada + sandía |
| **`pergola-aluminio-para-jardin-300300250-cm`** | blanco roto / **camaleónico** | Puente | **B7 Jardín de grava, Pozuelo** — tarima, seto de boj, olivo en barro | **Bajo la pérgola** (el espacio cubierto que crea) | — (estructura) |
| **`sofa-terraza-aluminio-3-plazas-...-22090-cm`** | gris chenille + antracita / **frío** | Frío/piedra | **A5 Azotea de Chamberí (Madrid noble)** — microcemento, parapeto de piedra, cornisas | **A5 interior** — galería/mirador de la finca, terrazo | vermut + almendras marcona |
| **`set-jardin-aluminio-2-plazas-contemporaneo-...`** (Brandon 2 pl.) | gris chenille + antracita / **frío** | Frío/urbano | **A2 Loft junto a la ría, Bilbao** — hormigón encofrado, acero corten, gramíneas | **A2 interior** — loft con ventanal de acero negro y pared de ladrillo | cerveza fría + aceitunas |
| **`set-jardin-bicolor-3-plazas-...`** (Diva) | blanco + lamas antracita / **blanco roto** | Blanco/cal | **B6 Casa payesa moderna, Ibiza** — cal blanca de aristas redondeadas, sabina, grava | **B6 interior** — salón con techo de troncos de sabina y arco al patio | granada + agua con hielo |
| **`set-jardin-2-plazas-moderno-...`** (Yina 2 pl.) | azul celeste + cuerda gris / **frío claro** | Frío/cal atlántica | **A9 Azotea de casa-torre, Cádiz** — cal blanca, suelo de ladrillo, catedral y Atlántico | **A9 interior** — salón de baldosa hidráulica con balcón al mar | tinto de verano + almendras |
| **`set-jardin-2-plazas-elegante-...-mesa`** (Damasco) | tórtola + crudo + cuerda beige / **cálido-neutro** | Cálido-neutro | **B2 Cortijo contemporáneo, campiña sevillana** — caliza clara, olivo, campos dorados | **B2 interior** — galería de arcos encalados abierta al olivar | queso curado + pan + aceite |
| **`set-jardin-2-plazas-elegante-...-mesa-3`** (Bellagio) | blanco + gris claro / **blanco** | Blanco/cal | **B10 Casa cúbica, Cabo de Gata (Almería)** — cal, agave y chumbera, mar árido | **B10 interior** — sala encalada con hornacinas de piedra, microcemento | tomate raf + aceite + pan |
| **`balliu-cama-balinesa-...-198-cm`** (Alma) | blanco / **blanco** | Blanco/piedra | **B11 Piscina entre pinos, Mallorca** — caliza, muro de piedra seca, pinar | **B11 interior** — porche abovedado abierto a la piscina | toalla + sombrero (sin bebida) |
| **`set-jardin-bicolor-2-plazas-...`** (Diva 2 pl.) | tórtola + lamas antracita + crudo / **cálido-neutro** | Cálido/cal | **B1 Patio cordobés contemporáneo** — cal, macetas de geranios en la pared, celosía de forja, limonero en tinaja | **B1 interior** — zaguán abovedado con suelo de barro y reja al patio | naranjas partidas + zumo |
| **`set-jardin-2-plazas-elegante-...-mesa-4`** (Albania 2 pl.) | antracita + crudo / **frío** | Frío/atlántico | **A10 Terraza sobre el puerto pesquero, Asturias** — piedra, barandilla de hierro, casas de colores y barcas | **A10 interior** — porche de columnas de piedra con vigas, abierto al prado y al mar | sidra escanciada + queso azul |
| **`set-jardin-3-plazas-elegante-...-mesa-2`** (Dounvil) | antracita + azul grisáceo / **frío** | Frío/granito | **A11 Costa da Morte, Galicia** — granito rugoso, tojo en flor y brezo, Atlántico rompiendo | **A11 interior** — galería acristalada gallega de carpintería blanca | albariño + berberechos |
| **`set-jardin-3-plazas-contemporaneo-...-mesa-5`** (Acapulco) | blanco + gris claro, mesa de CRISTAL / **blanco** | Blanco/barro | **B12 Terraza valenciana** — suelo de barro, persianas de esparto, romero y naranjo en tinaja | **B12 interior** — porche encalado con persiana de esparto, abierto al jardín | horchata + fartons |

## Cobertura regional (acumulado)
Cantabria · Levante (Murcia) · Baleares (Menorca, **Ibiza**, **Mallorca**) · C. Valenciana (Costa Blanca) · Madrid residencial (Pozuelo) · Madrid noble (Chamberí) · **País Vasco (Bilbao)** · **Cádiz** · **campiña sevillana** · **Almería (Cabo de Gata)** · *(previas: Barcelona, Galicia, Salamanca, Toledo)*.

**Infrautilizadas — empujar en las próximas tandas:** Galicia (A1, 1 uso), Salamanca (A6, 1 uso), Córdoba (B1), HORECA (A8/B9), Segovia (C2), Asturias, Extremadura, Aragón/Pirineo, Canarias (con cuidado: nunca resort).

## Anti-repetición de consumible
Usados: café+galletas · aceitunas+almendras · té helado · vino blanco+higos · limonada+sandía · vermut+almendras marcona · **cerveza+aceitunas** · **granada+agua con hielo** · **tinto de verano+almendras** · **queso+pan+aceite** · **tomate raf+aceite**.
**Libres para las próximas:** caldo/té humeante del norte, horchata, naranjas abiertas, cesta de hortalizas, sidra, chocolate con churros (otoño), sandía, uvas.
