---
name: bootstrap-harness
description: Inicializa y personaliza todo el arnés de desarrollo asistido por IA para un nuevo proyecto a partir de documentación previa depositada en .ai-harness/input/, análisis del codebase o mediante asistencia del modelo de IA.
---

# Bootstrap Harness Skill

Inicializa y personaliza todo el arnés de desarrollo asistido por IA para un nuevo proyecto a partir de documentación previa depositada en `.ai-harness/input/` o mediante asistencia directa del modelo de IA.

## Comandos

```bash
# Modo manifiesto (Recomendado para Agentes de IA)
python .ai-harness/skills/bootstrap-harness/runner.py --manifest .ai-harness/input/manifest.yaml

# Modo interactivo por consola (Para humanos)
python .ai-harness/skills/bootstrap-harness/runner.py --interactive

# Modo simulación
python .ai-harness/skills/bootstrap-harness/runner.py --interactive --dry-run
```

## Protocolo Obligatorio para Agentes de IA

1. **Ingesta:** Analizar los documentos depositados en `.ai-harness/input/` (PRD, brief, arquitectura).
2. **Scaffolding:** Generar el manifiesto y ejecutar el runner para crear la estructura base del arnés.
3. **Adaptación Semántica Profunda (OBLIGATORIO):**
   Las plantillas generadas por el runner sirven **únicamente como referencia estructural** para no dejar archivos incompletos o mal formateados. **El agente de IA DEBE modificar y adaptar totalmente los ficheros generados para volcar toda la riqueza del proyecto real**:
   - `context/project_overview.md` y `architecture_rules.md`: Incorporar reglas reales del PRD (invariantes, FSMs, topes presupuestarios, kill switches, fronteras de capas y servicios).
   - `context/security_privacy.md` y `platform_matrix.md`: Políticas de seguridad, gestión de tokens, plataformas y entornos reales.
   - `context/glossary.md`: Glosario de términos del dominio extraídos del PRD.
   - `design-system/` (si el producto tiene UI): Reescribir `03-layout.md` (filosofía de layout real, alta densidad por píxel), `04-components.md` (componentes visuales reales) y `05-pages.md` (blueprint real de las páginas/pantallas del producto).
   - `memory/failure_modes.md` y `decisions/`: Modos de fallo específicos del stack y ADRs técnicos.
   - `sdd/modules/*.md`: Requerimientos (`FR-*`), APIs y contratos funcionales según la especificación del negocio.
4. **Verificación:** Ejecutar `harness-validator`, `preflight` y `sync-sdd` para asegurar que el arnés queda 100% verificado.
