# Skills exportables

> ⚠️ **`foto-producto-ia` ya no se mantiene aquí (25-09-2026).** Se ha integrado en la capa
> workspace del repo **Super-IA**, que es ahora la **copia canónica**, y desde allí está disponible
> en todos los e-commerce del workspace sin copiar nada:
>
> ```
> Super-IA/workspace/skills/foto-producto-ia/
> ```
>
> Lo que queda en esta carpeta es el **origen histórico**: no lo edites. Si aprendes algo genérico
> nuevo, tócalo en Super-IA y haz `git push` (así llega a las dos máquinas). Pendiente de hablarlo
> con Manu, por si prefiere otro reparto.

Skills **genéricos**, sin nada de este proyecto dentro, listos para llevar a otro cliente.

| Skill | Qué hace |
|---|---|
| [`foto-producto-ia/`](foto-producto-ia/) | galería de producto con IA para cualquier producto físico: packshot, ambiente, detalle y el dato que decide la compra |

## Por qué están aquí

Esta carpeta es la **copia canónica y versionada**: lo que hay en `~/.claude/skills/` es una
instalación de trabajo, vive solo en una máquina y no está respaldada. Si tocas el skill, tócalo
aquí y reinstala:

```bash
cp -r skills-exportables/foto-producto-ia ~/.claude/skills/
```

## Ojo: no confundir con el skill de proyecto

`.claude/skills/santavila-imagen-producto/` es **el skill de ESTE proyecto** y no se toca: lleva
las reglas propias de la marca, los proveedores y la tienda. El exportable es el **poso genérico**.

Cuando aprendas algo nuevo, pregúntate dónde va:
- ¿vale para cualquier producto? → **skill exportable**
- ¿es de esta marca, este proveedor o esta tienda? → **skill de proyecto**
