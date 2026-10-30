---
name: git-publish
description: Publica los cambios en Git solo bajo petición explícita del usuario y tras pasar las puertas de validación.
---

# Git Publish

Publica los cambios en Git **solo** bajo petición explícita del usuario y tras
pasar las puertas de validación.

## Comando

```bash
python .ai-harness/skills/git-publish/runner.py status
python .ai-harness/skills/git-publish/runner.py push -m "<mensaje>"
```

## Protocolo

1. El usuario pide explícitamente publicar, subir o sincronizar.
2. El runner ejecuta `harness-validator` y `preflight`.
3. Si cualquiera falla, no se publica: se corrige primero.
4. Se muestra el resultado del `push` y el enlace al MR/PR.

## Reglas

- Prohibida la ejecución autónoma sin instrucción del usuario.
- No usar `--no-verify` salvo emergencia autorizada.
- No publicar secretos, fixtures pesados ni artefactos de build.
- No cambiar de rama ni de remoto sin instrucción explícita.
- Si el repositorio no está inicializado, el runner lo informa y no improvisa.
