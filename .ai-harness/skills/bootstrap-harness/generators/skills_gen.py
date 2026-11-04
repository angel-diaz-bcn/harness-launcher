"""Skills & Workflows Generator: Generador completo del ecosistema de skills.

Produce:
1. Replicación del motor ejecutor de skills (.ai-harness/skills/) en el proyecto destino
2. .ai-harness/skills/registry.yaml y README.md
3. .agents/skills/ (README.md y SKILL.md de alta fidelidad para cada una de las 7 skills)
4. .clinerules/ (rules.md y workflows/*.md para invocación con /)
"""

from __future__ import annotations

import shutil
from pathlib import Path
from models import BootstrapManifest, GitProvider, StackType


class SkillsGenerator:
    """Genera artefactos de documentación y orquestación de skills para agentes."""

    def __init__(self, manifest: BootstrapManifest) -> None:
        self.m = manifest

    def generate_agents_skills(self) -> dict[str, str]:
        """Devuelve diccionario relativo a .agents/skills/ con contenido."""
        m = self.m
        out: dict[str, str] = {}
        root_path = m.scopes[0].path_roots[0] if m.scopes and m.scopes[0].path_roots else "lib/"

        # 1. README general de .agents/skills/
        out["README.md"] = f"""# Inventario de Skills para Agentes — {m.identity.name}

Este directorio documenta el catálogo de capacidades y herramientas operativas para agentes de IA en `{m.identity.name}`.
Cada skill cuenta con su especificación canónica en `SKILL.md` y su runner ejecutable en `.ai-harness/skills/`:

| Skill | Finalidad | Comando principal |
|---|---|---|
| `harness-validator` | Valida integridad estructural, frontmatter, contexto y scopes | `python .ai-harness/skills/harness-validator/runner.py` |
| `preflight` | Valida código ({m.stack.language}), arquitectura, inmutabilidad y tokens | `python .ai-harness/skills/preflight/runner.py` |
| `sync-sdd` | Comprueba paridad entre specs aprobadas y código real en disco | `python .ai-harness/skills/sync-sdd/runner.py` |
| `create-component-sdd` | Crea el esqueleto canónico de componente CMP-NN | `python .ai-harness/skills/create-component-sdd/runner.py` |
| `create-process-sdd` | Crea el esqueleto canónico de proceso PRC-NN | `python .ai-harness/skills/create-process-sdd/runner.py` |
| `launch-app` | Arranca la aplicación en el entorno configurado | `python .ai-harness/skills/launch-app/runner.py` |
| `git-publish` | Publicación gobernada en Git bajo demanda explícita | `python .ai-harness/skills/git-publish/runner.py` |
"""

        # 2. harness-validator/SKILL.md
        out["harness-validator/SKILL.md"] = f"""---
name: harness-validator
description: Valida contexto, scopes, memoria, SDD y skills del arnés de {m.identity.name}.
---

# Harness Validator

Puerta de enlace normativa del arnés. Previene derivas en la configuración, ausencia de documentos obligatorios o inconsistencias de especificaciones.

## Comandos

```bash
# Ejecución estándar (reporte legible)
python .ai-harness/skills/harness-validator/runner.py

# Modo estricto (advertencias tratadas como errores)
python .ai-harness/skills/harness-validator/runner.py --strict

# Salida estructurada para pipelines o agentes
python .ai-harness/skills/harness-validator/runner.py --json
```

## Checks y Verificaciones

1. **Contexto Normativo (`check_context.py`):** Verifica que los 12 documentos canónicos existan y contengan contenido sustantivo sin marcadores pendientes (`<PROYECTO>`).
2. **Scopes Modulares (`check_context.py`):** Asegura que cada `block_*.md` tenga rutas autorizadas y ninguna prohibida.
3. **Memoria Preventiva (`check_memory.py`):** Comprueba el número mínimo de modos de fallo y la presencia de ADRs requeridos.
4. **Especificaciones SDD (`check_sdd.py`):** Audita frontmatter obligatorio, presencia de `user_story.md`, trazabilidad `FR-*`/`ST-*` y mapa de implementación.
5. **Registro de Skills (`check_skills.py`):** Valida que toda skill listada en `registry.yaml` cuente con su runner y su archivo `SKILL.md`.

## Protocolo de resolución de fallos

- Si falla `SDD-MISSING-FRONTMATTER`: Completar los campos requeridos en la cabecera YAML de la spec.
- Si falla `SDD-MAP-MISSING-REQUIREMENT`: Incluir filas con `FR-NN` o `ST-NN` en la tabla del mapa de implementación §10.
- Si un check falla, **investigar la causa raíz** antes de reejecutar. Prohibido omitir validaciones.
"""

        # 3. preflight/SKILL.md
        forbidden_str = ", ".join(m.architecture.forbidden_packages) if m.architecture.forbidden_packages else "ninguno"
        out["preflight/SKILL.md"] = f"""---
name: preflight
description: Valida código {m.stack.language}/{m.stack.framework}, fronteras de features, contratos, tokens y dependencias para {m.identity.name}.
---

# Preflight

Puerta de calidad del código de producción. Debe ejecutarse antes de declarar cualquier tarea terminada o realizar un commit.

## Comandos

```bash
# Verificación completa del repositorio
python .ai-harness/skills/preflight/runner.py

# Verificación acotada a un archivo o carpeta target
python .ai-harness/skills/preflight/runner.py [ruta/al/target]

# Modo estricto
python .ai-harness/skills/preflight/runner.py --strict
```

## Checks ejecutados

1. **00_code_quality:** Ejecución de linters y pruebas del stack (`{m.stack.test_command}`).
2. **01_architecture:** Aislamiento de features; prohibido importar archivos privados de otra feature.
3. **02_contracts:** Inmutabilidad de modelos de dominio, prohibición de tipos `any`/`dynamic`, ausencia de logs de depuración (`console.log`/`print`) y prohibición de bloques `catch` vacíos.
4. **04_ui_tokens:** Cumplimiento del sistema de diseño; detección de colores HEX literales fuera de `design-system/tokens.json`.
5. **05_dependencies:** Detección de paquetes prohibidos ({forbidden_str}).
"""

        # 4. sync-sdd/SKILL.md
        out["sync-sdd/SKILL.md"] = f"""---
name: sync-sdd
description: Comprueba la sincronización entre especificaciones SDD (.spec.md) y código fuente real en disco para {m.identity.name}.
---

# Sync SDD

Verifica que cada spec aprobada tiene su archivo de código destino (`target`) correspondiente y detecta divergencias mediante hashes criptográficos.

## Comandos

```bash
# Comprobación de estado general
python .ai-harness/skills/sync-sdd/runner.py

# Actualizar la línea base tras implementar cambios en una spec aprobada
python .ai-harness/skills/sync-sdd/runner.py --baseline
```

## Estados de alineación

- **PRESENT:** La spec y su implementación están alineadas con la línea base.
- **MISSING:** La spec está aprobada pero el archivo de destino en disco no existe.
- **DIVERGED:** El archivo de código ha cambiado respecto a la última baseline registrada.
- **N/A:** Specs en borrador (`DRAFT`) que aún no exigen código de producción.
"""

        # 5. create-component-sdd/SKILL.md
        out["create-component-sdd/SKILL.md"] = f"""---
name: create-component-sdd
description: Genera el andamiaje canónico de una spec de componente (CMP-NN) para {m.identity.name}.
---

# Create Component SDD

Genera una nueva especificación técnica de componente en `.ai-harness/sdd/1_COMPONENTS/`.

## Comandos

```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-NN \\
  --name "<Nombre legible>" \\
  --target {root_path}<ruta>/<archivo> \\
  --layer <bootstrap|domain|ui> \\
  --dir .ai-harness/sdd/1_COMPONENTS/<layer>/CMP-NN-<slug>
```

## Flujo de trabajo para redactar la especificación

1. **Definir la Historia de Usuario (`user_story.md`):** Explicar el valor de negocio real y al menos 2 criterios de aceptación en formato BDD (`Dado / Cuando / Entonces`).
2. **Requisitos Funcionales (§4):** Listar requisitos atómicos `FR-01`, `FR-02`, etc., con prioridad MoSCoW (`Must`, `Should`).
3. **Reglas de Negocio (§5):** Declarar invariantes `BR-*` e `INV-*` con su fuente canónica.
4. **Estados y Errores (§6):** Diagramar la máquina de estados en Mermaid y catalogar los errores con códigos tipados.
5. **UI y Foco (§7, si es capa `ui`):** Referenciar tokens de `tokens.json` y orden de foco por teclado/D-Pad.
6. **Contratos de Datos (§8):** Escribir los tipos, clases inmutables e interfaces `CT-*` exactas.
7. **Mapa de Implementación (§10):** Mapear cada fila `FR` → `CT` → `archivo::símbolo` → `TC` con estado `Pending`.
8. **Pruebas (§11 y §12):** Detallar los casos de prueba unitarios/integración `TC-*` y escenarios Gherkin.
9. **Aprobación:** Solo cuando todo esté completo y sin placeholders `<...>`, cambiar `status: DRAFT` a `status: APPROVED`.
"""

        # 6. create-process-sdd/SKILL.md
        out["create-process-sdd/SKILL.md"] = f"""---
name: create-process-sdd
description: Genera el andamiaje canónico de una spec de proceso (PRC-NN) para {m.identity.name}.
---

# Create Process SDD

Genera una nueva especificación técnica de flujo o proceso en `.ai-harness/sdd/2_PROCESSES/`.

## Comandos

```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-NN \\
  --name "<Nombre del flujo>" \\
  --target docs/flows/<nombre_flujo>.md \\
  --dir .ai-harness/sdd/2_PROCESSES/<modulo>/PRC-NN-<slug> \\
  --block 2_PROCESSES
```

## Flujo de trabajo para redactar la especificación

1. **Historia de Usuario (`user_story.md`):** Identificar qué flujo orquesta, los componentes involucrados y los escenarios BDD de éxito y contingencia.
2. **Disparador y Condiciones (§2):** Fijar claramente el trigger, precondiciones, postcondiciones y política de reintento.
3. **Flujo y Secuencia (§5):** Diseñar el diagrama de secuencia Mermaid numerado con todos los actores y participantes (`CMP-*`).
4. **Pasos Atómicos (§6):** Desglosar la secuencia en pasos `ST-01`, `ST-02`, etc., asignando el componente responsable de cada paso.
5. **Errores y Recuperación (§7):** Documentar la estrategia de contingencia y liberación de recursos ante fallos.
6. **Mapa de Implementación (§11):** Mapear cada paso `ST` → `CT` → `archivo::símbolo` → `TC`.
7. **Aprobación:** Pasar a `status: APPROVED` cuando no queden placeholders pendientes.
"""

        # 7. launch-app/SKILL.md
        out["launch-app/SKILL.md"] = f"""---
name: launch-app
description: Arranca el entorno y la aplicación {m.identity.name} localmente.
---

# Launch App

Ejecuta el entorno de la aplicación según el stack configurado (`{m.stack.language}` / `{m.stack.framework}`).

## Comandos

```bash
python .ai-harness/skills/launch-app/runner.py
```

Comando subyacente ejecutado: `{m.stack.launch_command}`.
"""

        # 8. git-publish/SKILL.md
        out["git-publish/SKILL.md"] = f"""---
name: git-publish
description: Publica en Git ({m.git_remote.provider.value.upper()}) de forma segura y gobernada bajo demanda explícita.
---

# Git Publish

Publica los cambios en el repositorio remoto únicamente tras verificar que todas las puertas de enlace pasan limpias.

## Comandos

```bash
# Inspección de estado de repositorio
python .ai-harness/skills/git-publish/runner.py status

# Publicación formal protegida por puertas de calidad
python .ai-harness/skills/git-publish/runner.py push -m "<tipo>: <descripcion del cambio>"
```

## Reglas no negociables

1. **Bajo demanda:** Requiere instrucción expresa del usuario.
2. **Puertas previas:** Ejecuta internamente `harness-validator` y `preflight`. Si alguna falla, la publicación se aborta automáticamente sin modificar el repositorio remoto.
"""
        return out

    def generate_clinerules_rules(self) -> str:
        m = self.m
        return f"""# Reglas de Integración del Agente con el Arnés — {m.identity.name}

## 1. Autoridad y Jerarquía
`AGENTS.md` es el enrutador maestro del repositorio. El agente no puede contradecir, relajar ni ignorar las reglas de `context/` ni de los scopes activos.

## 2. Modus Operandi
1. **Carga JIT:** Antes de inspeccionar código o proponer cambios, cargar en orden los documentos de `AGENTS.md` §1.
2. **Límites de Escritura:** Localizar el scope correspondiente en `.ai-harness/scopes/` y escribir exclusivamente en sus rutas autorizadas.
3. **SDD-First:** Prohibido escribir código de producción sin spec `.spec.md` aprobada (`status: APPROVED`).
4. **Cero Invención:** Si falta un dato o requerimiento, registrarlo como pregunta abierta en §15/§16 y detenerse.

## 3. Despacho de Workflows
Los comandos disponibles se invocan con barra inclinada (`/`) a través de `.clinerules/workflows/`:
- `/list-skills.md`: Inventario de herramientas y skills operativas.
- `/create-component-sdd.md`: Andamiaje para nuevos componentes.
- `/create-process-sdd.md`: Andamiaje para flujos y procesos.
- `/harness-validator.md`: Verificación de integridad normativa.
- `/preflight.md`: Puerta de calidad de código y arquitectura.
- `/sync-sdd.md`: Sincronización spec ↔ código.
- `/launch-app.md`: Arranque de la aplicación.
- `/git-publish.md`: Publicación segura en Git (solo bajo demanda).

## 4. Resolución Autónoma de Problemas
- Si un test o validador falla, leer la traza de error antes de editar a ciegas.
- Prohibido silenciar excepciones o usar `--no-verify`.
- Corregir la causa raíz del fallo y revalidar las puertas de enlace.
"""

    def generate_clinerules_workflows(self) -> dict[str, str]:
        m = self.m
        out: dict[str, str] = {}

        out["workflows/harness-validator.md"] = f"""# Workflow — Validación del Arnés ({m.identity.name})

## Objetivo
Verificar la integridad estructural y coherencia normativa del arnés.

## Protocolo
1. Ejecutar el validador:
```bash
python .ai-harness/skills/harness-validator/runner.py
```
2. Si existen fallos (`ERROR`), corregir la spec o archivo señalado antes de continuar.
"""

        out["workflows/preflight.md"] = f"""# Workflow — Preflight de Calidad ({m.identity.name})

## Objetivo
Validar código, arquitectura, inmutabilidad y respeto a tokens antes de un commit.

## Protocolo
1. Ejecutar preflight:
```bash
python .ai-harness/skills/preflight/runner.py
```
2. Resolver cualquier infracción de linters, tests o violación de tokens.
"""

        out["workflows/sync-sdd.md"] = f"""# Workflow — Sincronización SDD ({m.identity.name})

## Objetivo
Comprobar paridad entre specs aprobadas y el código en disco.

## Protocolo
1. Ejecutar:
```bash
python .ai-harness/skills/sync-sdd/runner.py
```
2. Tras completar una implementación aprobada, fijar la línea base:
```bash
python .ai-harness/skills/sync-sdd/runner.py --baseline
```
"""

        out["workflows/create-component-sdd.md"] = f"""# Workflow — Crear Spec de Componente ({m.identity.name})

## Objetivo
Crear una nueva spec de componente CMP-NN conforme a las plantillas canónicas.

## Protocolo
1. Ejecutar:
```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-NN --name "<Nombre>" --target "<ruta>" --layer "<layer>" --dir ".ai-harness/sdd/1_COMPONENTS/<layer>/CMP-NN-<slug>"
```
2. Completar las 15 secciones técnicas sin placeholders pendientes.
3. Cambiar a `status: APPROVED`.
"""

        out["workflows/create-process-sdd.md"] = f"""# Workflow — Crear Spec de Proceso ({m.identity.name})

## Objetivo
Crear una nueva spec de proceso PRC-NN conforme a las plantillas canónicas.

## Protocolo
1. Ejecutar:
```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-NN --name "<Nombre>" --target "docs/flows/<flujo>.md" --dir ".ai-harness/sdd/2_PROCESSES/<modulo>/PRC-NN-<slug>"
```
2. Diseñar el diagrama Mermaid y completar los pasos `ST-*`.
3. Cambiar a `status: APPROVED`.
"""

        out["workflows/launch-app.md"] = f"""# Workflow — Arranque de la Aplicación ({m.identity.name})

## Protocolo
Ejecutar el comando de arranque local:
```bash
python .ai-harness/skills/launch-app/runner.py
```
"""

        out["workflows/git-publish.md"] = f"""# Workflow — Publicación en Git ({m.identity.name})

## Disparador
SOLICITUD EXPRESA DEL USUARIO para hacer push o publicar en {m.git_remote.provider.value.upper()}.

## Protocolo
1. Inspeccionar:
```bash
python .ai-harness/skills/git-publish/runner.py status
```
2. Publicar tras pasar puertas de enlace:
```bash
python .ai-harness/skills/git-publish/runner.py push -m "<tipo>: <descripcion del cambio>"
```
"""

        out["workflows/list-skills.md"] = f"""# Workflow — Inventario de Skills ({m.identity.name})

## Protocolo
1. Leer `.ai-harness/skills/registry.yaml`.
2. Presentar la lista de herramientas operativas del repositorio.
"""
        return out

    def generate_registry_yaml(self) -> str:
        m = self.m
        return f"""version: 1
skills:
  - name: harness-validator
    status: active
    command: python .ai-harness/skills/harness-validator/runner.py
    doc: .agents/skills/harness-validator/SKILL.md
    description: Valida la estructura y coherencia del arnés normativo.

  - name: preflight
    status: active
    command: python .ai-harness/skills/preflight/runner.py
    doc: .agents/skills/preflight/SKILL.md
    description: Valida código ({m.stack.language}), arquitectura, contratos y tokens.

  - name: sync-sdd
    status: active
    command: python .ai-harness/skills/sync-sdd/runner.py
    doc: .agents/skills/sync-sdd/SKILL.md
    description: Comprueba la sincronización entre specs .spec.md y código en disco.

  - name: create-component-sdd
    status: active
    command: python .ai-harness/skills/create-component-sdd/runner.py
    doc: .agents/skills/create-component-sdd/SKILL.md
    description: Crea el esqueleto de una spec de componente CMP-NN.

  - name: create-process-sdd
    status: active
    command: python .ai-harness/skills/create-process-sdd/runner.py
    doc: .agents/skills/create-process-sdd/SKILL.md
    description: Crea el esqueleto de una spec de proceso PRC-NN.

  - name: launch-app
    status: active
    command: python .ai-harness/skills/launch-app/runner.py
    doc: .agents/skills/launch-app/SKILL.md
    description: Arranca la aplicación ({m.stack.launch_command}).

  - name: git-publish
    status: active
    command: python .ai-harness/skills/git-publish/runner.py
    doc: .agents/skills/git-publish/SKILL.md
    description: Publica en Git ({m.git_remote.provider.value.upper()}) bajo demanda explícita.
"""
