---
name: bootstrap-harness
description: Inicialización interactiva del arnés a partir de documentación en .ai-harness/input/ o entrevista guiada por fases.
---

# Bootstrap Harness Skill

Inicializa y personaliza todo el arnés de desarrollo asistido por IA para un nuevo proyecto a partir de documentación previa depositada en `.ai-harness/input/` o mediante una entrevista guiada por fases.

## Instrucciones de Ejecución

1. Modo interactivo asistido:
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --interactive
   ```

2. Modo simulación (dry-run):
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --interactive --dry-run
   ```

3. Modo manifiesto:
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --manifest ruta/al/manifiesto.yaml
   ```

