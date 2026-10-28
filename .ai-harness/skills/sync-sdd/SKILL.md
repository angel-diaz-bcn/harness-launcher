---
name: sync-sdd
description: Comprueba la sincronización entre specs .spec.md y su target de código.
---

# Sync SDD

Deriva el estado de implementación de cada `*.spec.md`:

- `N/A`: spec en `DRAFT` o `SUPERSEDED`; no se espera implementación.
- `MISSING`: spec `APPROVED` y target inexistente.
- `PRESENT`: target existente y alineado con la línea base.
- `DIVERGED`: la spec o el target cambiaron después de la línea base.

## Uso

```bash
python .ai-harness/skills/sync-sdd/runner.py
python .ai-harness/skills/sync-sdd/runner.py CMP-01
python .ai-harness/skills/sync-sdd/runner.py --json
python .ai-harness/skills/sync-sdd/runner.py --baseline
```

`--baseline` registra el estado actual como nueva línea base cuando el cambio es intencional.
