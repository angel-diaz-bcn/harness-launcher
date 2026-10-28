---
name: git-publish
description: Publicación gobernada en Git (git status, pull, push, sync) previa aprobación de las puertas de validación preflight. Ejecutable ÚNICAMENTE bajo demanda explícita del usuario.
---

# Git Publish Skill

Publicación gobernada en Git previa superación determinista de las puertas de enlace (Harness Validator + Preflight).

> [!IMPORTANT]
> Esta herramienta **SOLO** debe ejecutarse cuando el usuario lo solicite explícitamente (ej. "haz push", "publica los cambios", "sincroniza con el repositorio").

## Instrucciones de Ejecución

1. Estado del repositorio:
   ```bash
   python .ai-harness/skills/git-publish/runner.py status
   ```

2. Publicar cambios (requiere mensaje de commit):
   ```bash
   python .ai-harness/skills/git-publish/runner.py push -m "feat: add catalog parser"
   ```

3. Sincronizar (Pull con rebase + Preflight + Push):
   ```bash
   python .ai-harness/skills/git-publish/runner.py sync -m "docs: update SDD specifications"
   ```
