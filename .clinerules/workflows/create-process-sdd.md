# Workflow — Crear spec de proceso (PRC-XX)

## Disparador

Solicitud de crear o actualizar una spec de proceso.

## Protocolo

1. Leer `.agents/skills/create-process-sdd/SKILL.md` y `skill.yaml`.
2. Ejecutar el runner con los datos reales de la tarea:

```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-XX \
  --name "<nombre>" \
  --target lib/<ruta>/<archivo>.dart \
  --dir .ai-harness/sdd/2_PROCESSES/<área>/PRC-XX-<slug>
```

3. Completar la plantilla y validar:

```bash
python .ai-harness/skills/harness-validator/runner.py
```

## Reglas

- No inventar contratos, estados ni dependencias.
- No marcar `APPROVED` sin aprobación explícita del Product Owner.
- Una spec vive en una única carpeta.
