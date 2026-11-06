---
name: consolidate-change
description: Aplica una propuesta aprobada sobre el módulo maestro correspondiente y archiva la propuesta en .ai-harness/sdd/archive/.
---

# consolidate-change

Esta skill consolida un cambio aprobado según el ciclo OpenSpec.

## Cuándo usarla

- Una vez que la propuesta en `changes/<id>/proposal.md` ha sido revisada y aprobada por el desarrollador.
- Tras actualizar la verdad viva en `modules/<modulo>.md`.
- Deja el cambio archivado en `archive/` para trazabilidad y memoria histórica.

## Uso

```bash
python .ai-harness/skills/consolidate-change/runner.py [change_id]
```

Ejemplo:
```bash
python .ai-harness/skills/consolidate-change/runner.py 2026-11-add-google-oauth
```

