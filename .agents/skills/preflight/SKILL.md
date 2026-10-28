---
name: preflight
description: Valida código Flutter/Dart, fronteras de features, contratos, invariantes P2P, tokens y dependencias.
---

# Preflight

```bash
python .ai-harness/skills/preflight/runner.py
python .ai-harness/skills/preflight/runner.py --strict
python .ai-harness/skills/preflight/runner.py --json
```

Checks:

- `dart format`, `flutter analyze`, `flutter test`.
- imports entre features y capas.
- dominio/modelos inmutables.
- endpoint `127.0.0.1:8888/stream`, ausencia de backend/proxy.
- colores solo desde tokens.
- dependencias prohibidas.

No usa herramientas del proyecto anterior.
