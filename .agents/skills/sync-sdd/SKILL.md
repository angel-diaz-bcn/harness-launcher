---
name: sync-sdd
description: Deriva el estado de implementación de las specs .spec.md desde su target y una línea base de hashes.
---

# Sync SDD

```bash
python .ai-harness/skills/sync-sdd/runner.py
python .ai-harness/skills/sync-sdd/runner.py CMP-01
python .ai-harness/skills/sync-sdd/runner.py --json
```

Comprueba:

- `user_story.md` en la carpeta de la spec.
- `target` en el front matter.
- estado derivado `N/A`, `MISSING`, `PRESENT` o `DIVERGED`.
- línea base de hashes en `.ai-harness/memory/sync-state.json`.

`--baseline` registra cambios intencionales de spec o target.

No usa `spec.md` ni `packages/`.
