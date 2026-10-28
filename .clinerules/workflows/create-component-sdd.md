# Workflow — Crear spec de componente (CMP-NN)

## Disparador

Solicitud de crear o actualizar una spec de componente.

## Protocolo

1. Leer `.agents/skills/create-component-sdd/SKILL.md` y `skill.yaml`.
2. Ejecutar el runner con los datos reales de la tarea:

```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-NN \
  --name "<nombre>" \
  --target lib/<ruta>/<archivo>.dart \
  --layer <frontend|backend> \
  --dir .ai-harness/sdd/1_COMPONENTS/<layer>/CMP-NN-<slug>
```

3. Completar la plantilla y validar:

```bash
python .ai-harness/skills/harness-validator/runner.py
```

## Reglas

- No inventar contratos, campos, estados ni dependencias.
- No marcar `APPROVED` sin aprobación explícita del Product Owner.
- Una spec vive en una única carpeta.
