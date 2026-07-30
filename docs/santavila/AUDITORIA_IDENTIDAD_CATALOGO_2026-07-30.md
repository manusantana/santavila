# Auditoría de identidad del catálogo — productos que comparten foto principal

**Fecha:** 2026-07-30 · **Alcance:** los **170 productos ACTIVE** con imagen, no solo las 25 galerías de IA.
**Método:** huella perceptual (average-hash 16×16) de la **pos-0** de cada producto, agrupando por distancia
de Hamming ≤ 6, y revisión visual de cada grupo contra el título de cada ficha.

> **Por qué existe.** La [`AUDITORIA_FIDELIDAD_2026-07-29.md`](AUDITORIA_FIDELIDAD_2026-07-29.md) cubrió las
> **25 galerías generadas con Higgsfield**. Este documento cubre lo que aquella no miraba: **las fotos de
> proveedor del resto del catálogo**. El fallo A0 (galería del Albania en la ficha del Bellagio) no era un
> caso aislado del pipeline de imagen: el mismo tipo de error existe en las fichas de proveedor.

## Resultado

**15 grupos · 34 productos comparten su foto principal con otro producto.**

### ⛔ Errores de identidad confirmados (la foto NO es el producto de la ficha)

| # | Ficha afectada | Qué muestra la foto | Prueba |
|---|---|---|---|
| **G12** | **Mesa extensible Java · HPL** `balliu-mesa-exterior-hpl-140-180100-cm-8e073aab` · **1.575 €** | La mesa **Atlanta**: **tablero de LAMAS**. La Java lleva **tablero HPL LISO** — lo dicen su descripción ("tablero HPL") y sus otras 4 fotos | Fichero `balliu_mesa-extensible-de-aluminio-atlanta_<uuid>.jpg`, **distancia perceptual 0** contra la pos-0 de la Atlanta |
| **G9** | **Taburete exterior aluminio · Etna** `balliu-taburete-exterior-aluminio-estilo-elegante-56...` | Una **silla CON respaldo y brazos**. Un taburete no tiene respaldo | Fichero `silla-etna-800x614-2_<uuid>.jpg`, compartido con las dos sillas Etna |
| **G15** | **Funda protectora para sofá exterior** `balliu-funda-protectora-exterior-6f6d4953` (+2 fundas más) | Una **funda de TUMBONA** (larga y baja) | Fichero `balliu_funda-protectora-para-2-tumbonas_<uuid>.jpg` en 4 fichas distintas |
| **G6** | **Tumbona resina Ø73 · tablillas · Eva Pro T** (+3 fichas Eva) | Una tumbona de **TELA azul**. La ficha vende la versión de **tablillas** — es otro asiento | Fichero `eva-pro-blanco-01-00-800x614-1<uuid>.jpg` en 4 fichas |
| **G11** | **Mesa auxiliar exterior · aluminio HPL 45×45 cm · Etna** | Una mesa **rectangular alargada**, no un cuadrado de 45×45 | Compartida con `Mesa de centro · HPL 110×60 cm` |
| **G8** | **Tumbona exterior aluminio · Etna** | La **Etna ALTA** (modelo de acceso fácil, más alta) | Fichero `balliu_tumbona-de-aluminio-etna-alta.jpg` |

### ⚠️ Mala práctica (la foto contiene el producto, pero no lo protagoniza)

En estos casos el producto **sí aparece** en la imagen, pero es un elemento secundario: la ficha de un
reposapiés o de una mesa de centro se ilustra con una foto dominada por el sillón o el sofá. No es falso,
pero incumple el criterio del rol §6 ("foto de detalle o pieza acompañante como portada").

| # | Ficha | Foto dominada por |
|---|---|---|
| G1 | Reposapiés exterior 85×50×43 | el sillón Albania |
| G3 | Reposapiés bicolor 70×45×44 | el sillón bicolor Diva |
| G4 | Mesa de centro exterior 90 cm | el sofá Dounvil 2 pl. |
| G5 | Mesa de centro exterior 120 cm | el sofá Dounvil 3 pl. |
| G10 | Mesa auxiliar Olimpia 48×48 | comparte foto con la mesa de centro Olimpia 74×54 |

### ❔ A verificar (parecido alto, no concluyente sin la referencia del proveedor)

| # | Fichas | Duda |
|---|---|---|
| G2 | Set 2 plazas elegante · Set 3 plazas contemporáneo | Ficheros distintos (`bolonia_xl_20_20_1/2.png`) de la misma sesión. Hay que contar las plazas de cada uno contra su título — es exactamente la "confusión 2 vs 3 plazas" que el rol §6 marca como error auditado |
| G7 | Tumbona Carmen · Tumbona Lola | Ficheros propios y productos muy parecidos; puede ser legítimo |
| G13 | Parasol Pamela Ø200 · Parasol Ocean | El fichero se llama `parasol-ocean` y está en la ficha de la **Pamela** |
| G14 | Pie de parasol 40 kg · Base de hormigón para parasol | Podrían ser el mismo producto duplicado |

## Impacto

- **La colección Mesas (73 productos) nunca se había auditado por identidad** y el primer producto mirado
  ya falla. Conviene pasar este mismo método a las 73.
- Afecta a la **home**: cualquier sección que enlace a estas fichas manda al cliente a una foto que no es
  el producto. Es el mismo riesgo comercial que el A0 del Bellagio, pero repartido por el catálogo.

## Reproducir

El script está en el scratchpad de la sesión (`dup_pos0.py`): descarga la pos-0 de cada producto ACTIVE a
320 px, calcula el average-hash y agrupa por distancia ≤ 6. Coste: 0 €, ~2 minutos.

## Pendiente

1. Corregir las 6 fichas del bloque ⛔ (sustituir la pos-0 por la foto real del producto).
2. Decidir sobre las 5 del bloque ⚠️.
3. Resolver las 4 del bloque ❔ contra el catálogo del proveedor.
4. Extender la comprobación a **todas** las posiciones de media, no solo la pos-0.
