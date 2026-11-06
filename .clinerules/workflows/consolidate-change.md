# Workflow — Consolidar cambio OpenSpec (consolidate-change)

## Disparador

Aprobación por parte del desarrollador de una propuesta activa en `.ai-harness/sdd/changes/`.

## Protocolo

1. Aplicar las modificaciones aprobadas sobre el módulo maestro en `.ai-harness/sdd/modules/<modulo>.md`.
2. Archivar la propuesta:

```bash
python .ai-harness/skills/consolidate-change/runner.py [change_id]
```

3. Realizar commit documental de la spec consolidada.
4. Proceder a la implementación del código siguiendo `tasks.md`.

## Reglas

- No consolidar si el desarrollador no ha aprobado explícitamente el delta.
- Tras consolidar, el cambio pasa a `archive/` y queda como registro inmutable.

