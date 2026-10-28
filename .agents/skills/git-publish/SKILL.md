---
name: git-publish
description: Publica en Git solo bajo petición explícita del usuario y tras validar el arnés y el código.
---

# Git Publish

```bash
python .ai-harness/skills/git-publish/runner.py status
python .ai-harness/skills/git-publish/runner.py push -m "feat: add catalog parser"
```

Reglas:

- Solo se ejecuta si el usuario pide publicar, subir o sincronizar.
- Ejecuta `harness-validator` y `preflight` antes de publicar.
- Si una puerta falla, no se fuerza la subida.
