# Flujo de imagen por producto — runbook Santavila (rol fotógrafo + Higgsfield MCP)

> Procedimiento **robusto, repetible y escalable** para producir la galería de cada SKU.
> Combina: el **oficio** ([`ROL_FOTOGRAFO_SENIOR.md`](ROL_FOTOGRAFO_SENIOR.md)) + la **mecánica** (Higgsfield vía MCP) + **QA** + **subida a Shopify**.
> Spec de origen: [`specs/2026-06-19-procedimiento-imagenes-higgsfield-design.md`](specs/2026-06-19-procedimiento-imagenes-higgsfield-design.md). Estado live de partida: `_estado_imagenes.json`; cruce SKU↔imagen: `auditoria_imagenes_report.csv`.
> **Ley rectora:** el producto NO se transforma. Lo premium lo aporta el oficio, anclado a la foto real.

---

## 1. Modelos y parámetros Higgsfield (decididos)

Todo vía MCP. Reference media = la foto real del producto (el ancla de fidelidad).

| Uso | Modelo MCP | Por qué |
|---|---|---|
| **Principal, ambientes, detalle (fidelidad)** | **`nano_banana_pro`** | image-to-image, fotorrealista, **4K**, conserva el sujeto de la referencia y reconstruye la escena. Es nuestra ley de fidelidad. |
| Iteración rápida / barata | `nano_banana_2` | misma familia, más rápido para tantear escena/luz antes de la final |
| Alternativa packshot comercial | `marketing_studio_image` | orientado a producto/ads (1 ref `role:"image"`) |
| Alternativa con brand-kit | `ms_image` (DTC) | folds logo/colores/fuentes Santavila; requiere `style_id` (vía `show_marketing_studio`) — fase posterior |

**Parámetros `generate_image`:** `model`, `prompt` (receta de 7 bloques del rol §7.2), `medias:[{value:<media_id>, role:"image"}]`, `aspect_ratio` (`1:1` principal/detalle/medidas · `1:1`+`4:5` ambiente), `resolution` (`4k`), `count` (1–4 para elegir la mejor), `get_cost:true` (preflight de créditos).

---

## 2. El flujo de UN producto (8 pasos)

### Paso 0 · Inputs del SKU
- **Foto real de origen**: la de mayor resolución/limpieza del SKU (de su carpeta; ver `auditoria_imagenes_report.csv`). Si hay **variante** (chasis/tejido), la foto de ESA variante.
- **Cotas reales** (del título/variante/metafield) para la Toma 5.
- **Escena(s) asignada(s)** de la librería de 6 (rol §4.bis), según tipología (rol §5).
- **Receta de prompt** por tipología (rol §5 + §7).

### Paso 1 · Importar el ancla
`media_import_url(url = <URL CDN Shopify de la foto real>)` → devuelve `media_id`.
(Si la foto es local, subirla antes a un host/CDN accesible o usar el widget de carga.)

### Paso 2 · Generar las tomas 1–4 (fidelidad anclada)
Por cada toma, construir el prompt con la **estructura de 7 bloques** (rol §7.2), con la spec técnica de esa toma (rol §4) y los ajustes de la tipología (rol §5). Luego:
1. `generate_image({model:"nano_banana_pro", prompt, medias:[{value:media_id, role:"image"}], aspect_ratio, resolution:"4k", count:2, get_cost:true})` → **preflight de coste** primero.
2. Si el coste es aceptable, repetir sin `get_cost` para lanzar el job (devuelve `job_id`).
- **Tomas:** (1) Principal 1:1 · (2) Ambiente A 1:1 · (3) Ambiente B 4:5 · (4) Detalle macro 1:1.
- `count:2` para tener dos candidatas y quedarnos con la mejor.

### Paso 3 · Recoger resultados
`job_status(jobId, sync:true)` (imagen ~10–20 s) → URL(es) de salida.

### Paso 4 · Resolución
Generar ya a `resolution:"4k"`. Si alguna toma queda <2400 px o se importó una fuente pequeña, `upscale_image({image_id, width, height, resolution:"4k"})`.

### Paso 5 · Toma 5 (medidas) — NO IA
Overlay determinista por plantilla (script) sobre la **Toma 1**: cotas reales en **JetBrains Mono**, líneas ink `#23251D` 70–80%, máx. 3 magnitudes (rol §4 Toma 5). Fuente del dato = verificada, nunca inventada.

### Paso 6 · Puerta de calidad (QA) — bloqueante
Pasar cada imagen por el **Checklist §6 del rol** (A Fidelidad · B Artefactos IA · C On-brand · D Técnico). Automatizable con un agente-visión que compara la salida contra la **foto real de referencia** y el checklist, y devuelve aceptar/rechazar + motivo.
- **Falla un bloqueante → regenerar** (bajar `strength`/ajustar prompt; A2 solo si A1 no integra), **no subir**.
- Vigilar las confusiones de SKU auditadas (set 2 vs 3 plazas, detalle de pata como hero, etc.).

### Paso 7 · Subir a Shopify
`stagedUploadsCreate` → PUT bytes → `productCreateMedia(productId, [{originalSource, alt}])` → `productReorderMedia` para el **orden de la receta** (principal → ambientes → detalle → medidas). Verificar `mediaCount` y que la principal (pos 0) es la correcta. (Reutilizar infra: `upload_images.py/.mjs`.)

### Paso 8 · Registrar
Anotar por SKU: prompts finales por toma, **créditos gastados**, nº de regeneraciones, veredicto QA. Esto **afina la receta por tipología** y permite presupuestar el escalado.

---

## 2.bis ⚠️ Lección crítica (Fase 0, LEISA) — PROMPT CORTO EN MODO EDICIÓN
**Los modelos Nano Banana de Higgsfield colapsan a un gradiente en blanco con prompts muy largos** (la receta de 7 bloques + todas las restricciones en un solo prompt → imagen vacía o `failed`). **El servicio y la referencia funcionan**; el enemigo es la **longitud/saturación** del prompt.
- **Regla:** enviar un prompt **CORTO, natural, en modo edición** (≈3–6 frases): *"Usando la imagen de referencia, conserva el mueble EXACTAMENTE como está (no lo cambies) y sustituye solo el fondo/escena por [escena mediterránea], luz [X], fotorrealista."* En **inglés** funciona muy bien.
- Los **7 bloques del rol §7.2 son el CHECKLIST mental**, NO el texto literal: se **comprimen** a ese párrafo corto (mantener: conservar producto + escena + luz/mood; soltar el dump exhaustivo de restricciones).
- **Modelos:** `nano_banana_2`/`nano_banana_pro` se **coercen a `nano_banana_flash`** (rápido, buena fidelidad de edición). `marketing_studio_image` también vale pero igualmente colapsa con prompt largo.
- **Resolución (¡crítico!):** **`1k` es la resolución FIABLE.** `2k` y `4k` **colapsan a un gradiente en blanco** con nano_banana (verificado: las 1k salen con std ~60; las 2k/4k con std ~15 = vacías). → **Generar SIEMPRE a `1k` y subir calidad con `upscale_image` a 2k/4k** (paso 4 del flujo). No pedir 2k/4k directo en `generate_image`.
- **Coste real:** ~2 créditos por imagen a 1k; el upscale aparte.
- **Emparejamiento (rol §8):** elegir la escena cuya paleta CONVERSE con el textil/chasis (gris/antracita→atlántico/piedra/urbano frío; arena/teca→sur cálido/barro/madera). Variedad real de España, no solo mediterráneo. Hiperrealismo: describir la FÍSICA (luz/hora/material), no adjetivos de calidad.
- **Validado:** ancla `media_import_url`(URL CDN Shopify) → `media_id` → `generate_image(medias:[{role:"image"}])` con prompt corto → resultado premium fiel (terraza menorquina con barro/cal/olivo).

## 3. Optimización (sacarle el 2000%)
- **Preflight siempre** con `get_cost:true` antes de gastar.
- **Iterar barato:** tantear escena/luz con `nano_banana_2` a baja resolución; solo la final a `nano_banana_pro` 4K.
- **`count:2`** por toma para elegir, no regenerar a ciegas.
- **Reutilizar prompts por tipología:** una vez afinada la receta de "sofá 3 plazas", se clona para todos los sofás cambiando solo la variante/escena.
- **Reutilizar escenas:** las 6 escenas fijas → coherencia + menos prompt-engineering por SKU.
- **Lote:** modelos DTC (`ms_image`) permiten `batch_size` para tandas.

---

## 4. Bucle de escalado (tras validar la Fase 0)
1. **Fase 0** — 1 SKU end-to-end (este runbook completo) → medir créditos/ficha, afinar prompts. *(siguiente paso: elegir el SKU)*
2. **Plantilla por tipología** — 1 SKU de cada tipo (sofá/conjunto, mesa, silla, tumbona, parasol…) → receta-prompt fija por tipo.
3. **Catálogo** — priorizar **87 Hevea de 1 foto** + cola de reemplazo (`silla-exterior-estilo-estilizado`, `banco-de-exterior-150-cm`, `DIVA_N24`, `Capri-Quadrada2`).
4. **Variantes** — repetir con la foto de cada variante (fidelidad imagen↔variante).
5. **Shop the Look** — las 6 escenas con hotspots (infra Dwell ya existe).
6. **Home premium** — hero + escenarios + materiales con la librería.

---

## 5. Métricas de la Fase 0 (criterios para escalar)
- **Créditos por ficha completa** (4 generaciones + upscale) → presupuesto del escalado.
- **Tasa de aprobación QA** a la 1ª (cuántas regeneraciones por toma).
- **Fidelidad** (cero desviaciones de conteo/color en las aceptadas).
- **Tiempo** por ficha → ritmo de escalado (todo de golpe vs por tandas).

> Si la Fase 0 confirma fidelidad + escena premium + coste razonable, el procedimiento queda **sólido y replicable**: clonar receta por tipología y escalar.
