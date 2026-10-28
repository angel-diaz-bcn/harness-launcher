# create-process-sdd

Crea el esqueleto de una spec de proceso (`PRC-NN`) a partir de la plantilla
canónica.

## Comando

```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-01 \
  --name "Nombre del proceso" \
  --target lib/<ruta>/<archivo> \
  --dir .ai-harness/sdd/2_PROCESSES/PRC-01-<slug> \
  --block <bloque>
```

## Parámetros

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `process_id` | Sí | `PRC-NN`; el prefijo viene de la configuración |
| `--name` | Sí | Nombre legible del proceso |
| `--target` | Sí | Ruta de implementación bajo una ruta autorizada |
| `--dir` | Sí | Carpeta donde se crean spec e historia |
| `--block` | No | Bloque propietario del proceso |
| `--force` | No | Sobrescribe un esqueleto existente |

## Qué genera

- `<ID>-<slug>.spec.md` con el front matter de la plantilla sustituido.
- `user_story.md` con la estructura de historia de usuario.

## Después de ejecutarla

1. Definir pasos `ST-*`, contratos `CT-*` y pruebas `TC-*`.
2. Documentar el caso de error y el de cancelación.
3. Rellenar el mapa de implementación.
4. Cambiar a `APPROVED` solo con el checklist completo.

## Reglas

- Un proceso cruza dos o más componentes; si no, es un componente.
- No inventa identificadores: los lee de `harness.config.yaml`.
