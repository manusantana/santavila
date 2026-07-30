# Auditoría de fotos del catálogo — fichas que muestran otro producto

**Fecha:** 2026-07-30 · **Método:** dHash perceptual de 256 bits sobre la **foto principal** de las
**171 fichas ACTIVE**, agrupando por distancia de Hamming ≤ 12. Detecta imágenes iguales aunque el fichero
tenga otro nombre o sufijo.

**Resultado: 11 grupos · 25 fichas comparten foto principal con otra.**

> **Este problema NO viene de las galerías generadas con IA.** Ninguna de las 25 galerías generadas aparece
> en los grupos: sus packshots son todos distintos entre sí. Es un problema de **asignación de fotos del
> proveedor** en el catálogo original.

---

## A · CRÍTICO — la foto muestra un producto de OTRA CATEGORÍA
El cliente ve algo que no es lo que compra. Riesgo directo de devolución.

| Ficha | € | La foto muestra | Grupo con |
|---|---|---|---|
| **Mesa de centro exterior 120 cm** | 441,95 | el **sofá Dounvil 3 plazas entero** | sofá de 1.175 € |
| **Mesa de centro exterior 90 cm** | 332,95 | el **sofá Dounvil 2 plazas entero** | sofá de 909 € |
| **Reposapiés exterior bicolor 70×45×44** | 509 | el **sillón Diva completo** | sillón de 945 € |
| **Reposapiés exterior 85×50×43** | 349,90 | el **sillón Albania completo** | sillón de 599 € |
| **Funda protectora para tumbona** | 329,95 | la misma foto que otras 2 fundas distintas | ↓ |
| **Funda protectora exterior acrílico** | 36,95 | ídem | ↓ |
| **Funda protectora exterior** | 84,95 | ídem | 3 fundas ≠ con 1 foto |
| **Pie de parasol 40 kg** | 164,95 | la misma que la base de hormigón | base de 99,90 € |
| **Base de hormigón para parasol** | 99,90 | ídem | pie de 164,95 € |

## B · VARIANTES de la misma familia con foto compartida
No es otra categoría, pero la ficha no muestra **su** variante: el cliente no puede ver la diferencia
por la que paga.

| Grupo | Fichas | Diferencia que no se ve |
|---|---|---|
| Tumbonas **Eva** | 4 fichas (242,95 · 242,95 · 192,95 · 190,95) | tablillas vs tela · Pro vs RG |
| Tumbona **Etna** / **Etna Alta** | 449,90 / 496,95 | altura de acceso |
| Silla **Etna** / **Etna Alta** | 181,95 / 190,95 | altura |
| Mesa auxiliar **Olimpia 48×48** / Mesa centro **Olimpia 74×54** | 157,95 / 227,95 | tamaño y forma |
| Parasol **Pamela** Ø200 / **Ocean** Ø200-250 | 399,90 / 399,90 | modelo |

---

## C · YA CORREGIDO (2026-07-30)
Sustituido con **foto real del proveedor** localizada en `images_balliu/`. Sin coste de generación.

| Ficha | € | Antes | Ahora |
|---|---|---|---|
| **Mesa extensible Java** | 2.019 | la **Atlanta** (tablero de lamas) en pos 0 | la Java real · 8 fotos correctas ya existían |
| **Taburete Etna** | 186,95 | **10 fotos, todas de SILLAS** con respaldo y brazos | el taburete real (1 foto) |
| **Funda para sofá** | 227,95 | una funda de **tumbona** | funda de sofá |
| **Mesa auxiliar Etna 45×45** | 167,95 | la **mesa central 110×60** en pos 0 | la auxiliar real |

**Hallazgo del taburete:** sus diez fotos eran de sillas. Se dejó con **una sola foto correcta** —
mejor una verdadera que diez que mienten.

---

## D · NO DETERMINADO — no se toca
Siguiendo la regla del skill (*lo que no se puede verificar, no se publica*):

- **Tumbona Etna vs Etna Alta**: las candidatas de `images_balliu/` son tumbonas del mismo modelo y **no se
  puede distinguir con certeza cuál es la "alta"** sin la ficha técnica del proveedor.
- **Tumbonas Eva tablillas vs tela**: la diferencia de superficie no se confirma visualmente en las fotos
  disponibles.

Para cerrarlas hace falta el catálogo técnico de Balliu o una consulta al proveedor.

---

## E · CÓMO SE REPRODUCE ESTA AUDITORÍA
dHash 16×16 (256 bits) de la foto en posición 0 de cada ficha ACTIVE, agrupando por Hamming ≤ 12.
Detecta el mismo contenido aunque cambie el nombre del fichero, el sufijo UUID de Shopify o la compresión.
**Debe ejecutarse cada vez que se cargue un lote de productos nuevo.**
