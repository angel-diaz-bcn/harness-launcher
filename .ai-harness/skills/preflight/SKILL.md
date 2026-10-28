---
name: preflight
description: Valida código Flutter/Dart, arquitectura, contratos, invariantes P2P, tokens y dependencias.
---

# Preflight

```bash
python .ai-harness/skills/preflight/runner.py
python .ai-harness/skills/preflight/runner.py --strict
python .ai-harness/skills/preflight/runner.py --json
```

Checks: formato, análisis estático, tests, imports entre features, inmutabilidad, tokens de diseño, dependencias prohibidas y, si hay perfil activo, invariantes de dominio.

No usa herramientas del proyecto anterior.
