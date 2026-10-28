# Workflow — Publicación Git

## Regla de gobernanza

Este workflow solo se ejecuta si el usuario pide explícitamente publicar, subir o sincronizar cambios. Prohibida la ejecución autónoma.

## Protocolo

1. Confirmar la instrucción explícita del usuario.
2. Ejecutar:

```bash
python .ai-harness/skills/git-publish/runner.py status
python .ai-harness/skills/git-publish/runner.py push -m "<mensaje>"
```

3. El runner ejecuta `harness-validator` y `preflight` antes de publicar.
4. Si cualquiera falla, no forzar la subida: corregir primero.

## Reglas

- No usar `--no-verify` salvo emergencia autorizada.
- No publicar secretos, fixtures pesados ni artefactos de build.
- No cambiar de rama ni de remoto sin instrucción del usuario.
