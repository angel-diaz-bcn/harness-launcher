---
name: bootstrap-harness
description: Inicializa y personaliza todo el arnés de desarrollo asistido por IA para un nuevo proyecto a partir de documentación previa depositada en .ai-harness/input/ o mediante una entrevista guiada por fases.
---

# Bootstrap Harness

Inicializa y personaliza todo el arnés de desarrollo asistido por IA para un nuevo proyecto a partir de documentación previa depositada en `.ai-harness/input/` o mediante una entrevista guiada por fases.

## Propósito

Transforma la "carcasa" base del arnés en un entorno gobernado a medida del proyecto, generando de forma atómica:
- Configuración estructural (`harness.config.yaml`).
- Orquestador de agentes estricto sin reglas de negocio (`AGENTS.md`).
- Presentación y setup del producto real (`README.md`).
- Exclusiones específicas del stack tecnológico (`.gitignore` y `.aiignore`).
- Los 12 documentos normativos de contexto en `.ai-harness/context/`.
- Scopes funcionales de escritura en `.ai-harness/scopes/`.
- Semilla de memoria preventiva (mínimo 5 modos de fallo) en `.ai-harness/memory/failure_modes.md` y `ADR-0001` a `ADR-0003`.
- Sistema de diseño completo (6 documentos + `tokens.json`).
- Semilla de especificaciones SDD (`CMP-00` a `CMP-03` y `PRC-01`).
- Skills documentadas en `.agents/skills/` y workflows en `.clinerules/workflows/`.

## Comandos

1. **Modo interactivo asistido:**
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --interactive
   ```

2. **Modo simulación (sin escribir archivos):**
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --interactive --dry-run
   ```

3. **Modo manifiesto (ejecución desatendida a partir de un YAML preparado):**
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --manifest ruta/al/manifiesto.yaml
   ```

## Protocolo

1. Si existe documentación previa, colocarla en `.ai-harness/input/`.
2. Ejecutar el runner o invocar `/bootstrap-harness.md`.
3. Responder las preguntas guiadas. En cada una es posible elegir una opción recomendada, solicitar *"🤖 Decidir por mí"* para que la IA aplique las mejores prácticas según el contexto, o escribir en *"✏️ Campo abierto"*.
4. Al concluir, el runner compila los archivos y ejecuta de inmediato las puertas de enlace (`harness-validator`, `preflight` y `sync-sdd`) para verificar la integridad del arnés.

## Reglas de Gobernanza

- No deja textos genéricos con etiquetas `<PROYECTO>` huérfanas.
- `AGENTS.md` se mantiene únicamente como router y orquestador JIT; nunca incluye reglas de implementación ni visuales.
- Al terminar la generación, el arnés debe quedar en estado `PASSED` en todas las comprobaciones.
