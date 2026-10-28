# create-component-sdd

Crea el esqueleto de una spec de componente (`CMP-NN`) a partir de la plantilla
canónica.

## Comando

```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-01 \
  --name "Nombre del componente" \
  --target lib/<ruta>/<archivo> \
  --dir .ai-harness/sdd/1_COMPONENTS/<capa>/CMP-01-<slug>
```

## Parámetros

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `component_id` | Sí | `CMP-NN`; el prefijo viene de la configuración |
| `--name` | Sí | Nombre legible del componente |
| `--target` | Sí | Ruta de implementación bajo una ruta autorizada |
| `--dir` | Sí | Carpeta donde se crean spec e historia |
| `--layer` | No | `bootstrap`, `domain` o `ui`; se infiere de `--dir` |
| `--force` | No | Sobrescribe un esqueleto existente |

## Qué genera

- `<ID>-<slug>.spec.md` con el front matter de la plantilla sustituido.
- `user_story.md` con la estructura de historia de usuario.

## Después de ejecutarla

1. Completar front matter y todas las secciones obligatorias.
2. Definir `FR-*`, `CT-*` y `TC-*`.
3. Rellenar el mapa de implementación con rutas y símbolos reales.
4. Cambiar a `APPROVED` solo con el checklist completo.

## Reglas

- No inventa identificadores ni capas: los lee de `harness.config.yaml`.
- No sobrescribe sin `--force`.
