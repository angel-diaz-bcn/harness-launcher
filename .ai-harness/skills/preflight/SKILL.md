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

Checks: `dart format`, `flutter analyze`, `flutter test`, imports entre features, inmutabilidad, endpoint `127.0.0.1:8888/stream`, ausencia de backend/proxy, tokens de diseño y dependencias prohibidas.

No usa herramientas del proyecto anterior.
