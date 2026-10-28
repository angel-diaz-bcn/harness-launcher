---
name: harness-validator
description: Valida contexto, scopes, memoria, SDD y skills del arnés de FLIK.
---

# Harness Validator

```bash
python .ai-harness/skills/harness-validator/runner.py
python .ai-harness/skills/harness-validator/runner.py --strict
python .ai-harness/skills/harness-validator/runner.py --json
```

Valida:

- contexto completo y sin términos del proyecto anterior;
- scopes existentes y apuntando a `lib/`;
- `failure_modes.md` con modos FLIK y decisiones;
- specs `.spec.md`, front matter, historia, target y mapa;
- skills registradas, manifiestos, runners y documentación.
