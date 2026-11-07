---
name: bootstrap-harness
description: Inicializa y personaliza todo el arnés de desarrollo asistido por IA para un nuevo proyecto a partir de documentación previa depositada en .ai-harness/input/, análisis del codebase o mediante asistencia del modelo de IA.
---

# Bootstrap Harness

Inicializa y personaliza todo el arnés de desarrollo asistido por IA para un nuevo proyecto a partir de documentación previa (`.ai-harness/input/`), análisis del codebase existente o asistencia directa del modelo de IA.

## Propósito

Transforma la plantilla neutra en un entorno gobernado de ingeniería adaptado al producto real, generando de forma atómica:
- Configuración estructural (`harness.config.yaml`).
- Orquestador de agentes estricto sin reglas de negocio (`AGENTS.md`).
- Presentación y setup del producto real (`README.md`).
- Exclusiones específicas del stack tecnológico (`.gitignore` y `.aiignore`).
- Los 12 documentos normativos de contexto en `.ai-harness/context/` (adaptados a GUI, Backend API o CLI).
- Scopes funcionales de escritura en `.ai-harness/scopes/` según los módulos del negocio real.
- Semilla de memoria preventiva en `.ai-harness/memory/failure_modes.md` y `ADR-0001` a `ADR-0003`.
- Sistema de diseño completo (6 documentos + `tokens.json`, solo si el producto incluye interfaz gráfica).
- Semilla canónica SDD (`CMP-00` a `CMP-03` y `PRC-01`).
- Skills documentadas en `.agents/skills/` y workflows en `.clinerules/workflows/`.

## Modos de Ejecución

### 1. Modo Asistido por IA (Recomendado para Agentes)
Cuando trabajas con un modelo de IA (Antigravity, Cline, Roo-Code):
1. **Ingesta:** Depositar el PRD, brief o arquitectura previa en `.ai-harness/input/` (o explicárselo a la IA en el chat).
2. **Análisis:** El agente analiza el dominio, deduce los módulos reales (`scopes`), el stack y las políticas de persistencia/privacidad.
3. **Manifiesto:** El agente redacta un manifiesto estructurado (`manifest.yaml`) en `.ai-harness/input/`.
4. **Scaffolding inicial:** El agente ejecuta:
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --manifest .ai-harness/input/manifest.yaml
   ```
5. **Adaptación Semántica Profunda (OBLIGATORIO):**
   Las plantillas generadas por el runner sirven **únicamente como referencia estructural** para no dejar archivos incompletos. **El agente de IA DEBE modificar y adaptar totalmente los ficheros generados para volcar toda la riqueza del proyecto real**:
   - `context/project_overview.md` y `architecture_rules.md`: Reglas reales del PRD (invariantes, FSMs, topes de coste, kill switches, fronteras de capas y servicios).
   - `context/security_privacy.md` y `platform_matrix.md`: Políticas de seguridad, tokens, plataformas y entornos reales.
   - `context/glossary.md`: Términos de negocio del PRD.
   - `design-system/` (si el producto tiene UI): Reescribir `03-layout.md` (alta densidad, layout real), `04-components.md` (componentes visuales reales) y `05-pages.md` (blueprint real de las páginas/pantallas del producto).
   - `memory/failure_modes.md` y `ADR-0001` a `ADR-0003`: Modos de fallo y decisiones técnicas reales.
   - `sdd/modules/*.md`: Requerimientos (`FR-*`), APIs y contratos funcionales según la especificación del negocio.
6. **Verificación:** Ejecutar `harness-validator`, `preflight` y `sync-sdd`.

### 2. Modo Interactivo por Consola
Para desarrolladores humanos respondiendo pregunta por pregunta en terminal:
```bash
python .ai-harness/skills/bootstrap-harness/runner.py --interactive
```

### 3. Modo Simulación (Dry-Run)
Prueba la generación sin escribir archivos en disco:
```bash
python .ai-harness/skills/bootstrap-harness/runner.py --interactive --dry-run
```

## Protocolo de Gobernanza

- **Cero Plantillas Vacías:** Las plantillas sirven de referencia estructural; el agente debe sustituir los esquemas genéricos por el contenido real del proyecto.
- **Sin Valores Inventados:** Toda regla, color o invariante proviene del PRD o de la confirmación del usuario.
- **Verificación Completa:** Al concluir, las puertas de enlace (`harness-validator`, `preflight`, `sync-sdd`) deben pasar 100% limpias.
