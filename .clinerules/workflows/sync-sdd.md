# Workflow — Sincronización spec ↔ código

## Disparador

Cambios en una spec, en su target o en ambos.

## Protocolo

1. Actualizar la baseline cuando cambie el código de un target:

```bash
python .ai-harness/skills/sync-sdd/runner.py --baseline
```

2. Verificar la sincronización:

```bash
python .ai-harness/skills/sync-sdd/runner.py
```

3. Corregir cualquier `MISSING` o `DIVERGED` antes de cerrar la tarea.

## Reglas

- No cambiar la baseline para ocultar una divergencia real.
- Toda spec debe tener target existente y estado coherente.
