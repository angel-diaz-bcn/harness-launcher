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

        # 1. README general de .agents/skills/
        out["README.md"] = f"""# Inventario de Skills para Agentes — {m.identity.name}

Este directorio documenta el uso operativo de las skills registradas en `.ai-harness/skills/registry.yaml`:

- `harness-validator/` — Valida la estructura e integridad normativa del arnés.
- `preflight/` — Valida la calidad del código, arquitectura y tokens.
- `sync-sdd/` — Comprueba la paridad entre especificaciones aprobadas y código en disco.
- `create-component-sdd/` — Genera el esqueleto de una spec de componente CMP-NN.
- `create-process-sdd/` — Genera el esqueleto de una spec de proceso PRC-NN.
- `launch-app/` — Arranca la aplicación con el comando `{m.stack.launch_command}`.
- `git-publish/` — Publicación gobernada en Git ({m.git_remote.provider.value.upper()}) bajo demanda explícita.
"""

        # 2. harness-validator/SKILL.md
        out["harness-validator/SKILL.md"] = f"""---
name: harness-validator
description: Valida contexto, scopes, memoria, SDD y skills del arnés de {m.identity.name}.
---

# Harness Validator

Valida la integridad del arnés y previene derivas normativas o desincronización de configuraciones.

## Comandos

```bash
python .ai-harness/skills/harness-validator/runner.py
python .ai-harness/skills/harness-validator/runner.py --strict
python .ai-harness/skills/harness-validator/runner.py --json
```

## Qué valida

- Contexto normativo completo (12 documentos) y sin marcadores sin rellenar.
- Scopes existentes, contractuales y alineados con las rutas autorizadas del proyecto.
- `failure_modes.md` con modos de fallo preventivos y ADRs técnicos.
- Specs `.spec.md`, frontmatter canónico, historias de usuario y mapa de implementación.
- Skills registradas en `registry.yaml`, manifiestos `skill.yaml`, runners y documentación operativa.

## Reglas

- Si un check falla, investigar la causa raíz en la spec o configuración antes de continuar.
- No relajar ni desactivar validadores para falsear resultados.
"""

        # 3. preflight/SKILL.md
        forbidden_str = ", ".join(m.architecture.forbidden_packages) if m.architecture.forbidden_packages else "ninguno"
        out["preflight/SKILL.md"] = f"""---
name: preflight
description: Valida código {m.stack.language}/{m.stack.framework}, fronteras de features, contratos, tokens y dependencias para {m.identity.name}.
---

# Preflight

Puerta de calidad previa a commit o cierre de tarea. Garantiza que el código cumple los contratos de arquitectura y calidad.

## Comandos

```bash
python .ai-harness/skills/preflight/runner.py
python .ai-harness/skills/preflight/runner.py [target]
python .ai-harness/skills/preflight/runner.py --strict
python .ai-harness/skills/preflight/runner.py --json
```

## Checks ejecutados

1. **00_code_quality:** Formato, linter y tests del stack (`{m.stack.test_command}`).
2. **01_architecture:** Fronteras entre features, prohibición de imports cruzados no expuestos en barrels/index y propiedad de la persistencia.
3. **02_contracts:** Inmutabilidad de modelos de dominio, prohibición de tipos genéricos/dinámicos (`any`/`dynamic`), ausencia de logs de depuración (`console.log`/`print`) y bloques `catch` vacíos.
4. **04_ui_tokens:** Cumplimiento del sistema de diseño; detección de colores HEX hardcodeados fuera de `tokens.json`.
5. **05_dependencies:** Detección de paquetes prohibidos o no autorizados ({forbidden_str}).

## Reglas

- No declarar la tarea terminada con exit code distinto de 0.
- El arnés no bloquea por ausencia de herramientas, pero alerta con `WARNING`.
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
python .ai-harness/skills/sync-sdd/runner.py
python .ai-harness/skills/sync-sdd/runner.py [ID_SPEC]
python .ai-harness/skills/sync-sdd/runner.py --baseline
python .ai-harness/skills/sync-sdd/runner.py --json
```

## Estados derivados

- **PRESENT:** La spec y su implementación están alineadas con la línea base.
- **MISSING:** La spec está aprobada pero el archivo de destino en disco no existe.
- **DIVERGED:** El archivo de código ha cambiado respecto a la última baseline registrada.
- **N/A:** Specs en borrador (DRAFT) que aún no requieren código.

## Reglas

- Tras implementar o actualizar un componente aprobado, actualizar la baseline con `--baseline`.
- Prohibido falsear la baseline sin haber completado los requisitos de la spec.
"""

        # 5. create-component-sdd/SKILL.md
        root_path = m.scopes[0].path_roots[0] if m.scopes and m.scopes[0].path_roots else "src/"
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

## Estructura creada

- `user_story.md`: Historia de usuario en formato estándar (Como... Quiero... Para...).
- `CMP-NN-<slug>.spec.md`: Plantilla técnica completa basada en `TEMPLATE_COMPONENT_SDD.md`.

## Reglas

- No escribir código sin que la spec esté aprobada (`status: APPROVED`).
- Completar todos los marcadores y definir al menos dos escenarios Gherkin.
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
  --target {root_path}<coordinador> \\
  --dir .ai-harness/sdd/2_PROCESSES/<modulo>/PRC-NN-<slug>
```

## Requisitos

- Diagrama Mermaid de secuencia o estados coherente con los pasos `ST-*`.
- Definición de tratamiento de errores y liberación de recursos en cada paso.
- Casos BDD de éxito y de contingencia/rollback.
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

Publica ramas o commits hacia el repositorio remoto configurado (`{m.git_remote.url or 'origin'}`).

## Comandos

```bash
python .ai-harness/skills/git-publish/runner.py status
python .ai-harness/skills/git-publish/runner.py push -m "feat: descripcion del cambio"
```

## Protocolo de seguridad

1. Verifica que no haya credenciales ni secretos en los archivos staged.
2. Ejecuta `harness-validator` y `preflight`. Si alguno falla, el push se aborta.
3. Realiza el commit y push.
4. Genera el enlace directo para abrir el Merge Request / Pull Request en {m.git_remote.provider.value.upper()}.

## Reglas

- NUNCA se invoca automáticamente: requiere solicitud explícita del usuario.
"""

        return out

    def generate_clinerules(self) -> dict[str, str]:
        """Devuelve diccionario relativo a .clinerules/ con contenido."""
        m = self.m
        out: dict[str, str] = {}

        # 1. rules.md
        out["rules.md"] = f"""# Reglas de Integración de Cline / Antigravity — {m.identity.name}

## 1. Autoridad

`AGENTS.md` es el enrutador operativo obligatorio. Cline no puede contradecir, relajar ni omitir las reglas de `AGENTS.md`, del contexto normativo ni de los scopes activos.

## 2. Modus operandi

- Antes de leer código o proponer cambios, ejecutar la carga JIT de `AGENTS.md` §1.
- Identificar el scope del módulo a modificar y no escribir fuera de sus rutas autorizadas.
- Prohibido implementar código de producción sin spec `.spec.md` aprobada en `.ai-harness/sdd/`.
- Ante cualquier ambigüedad, detenerse y preguntar; prohibido inventar contratos o dependencias.

## 3. Despacho de workflows

Los workflows se descubren en `.clinerules/workflows/`. El comando se invoca como `/nombre.md`:

- Validación del arnés: `/harness-validator.md`
- Validación de calidad y arquitectura: `/preflight.md`
- Sincronización spec ↔ código: `/sync-sdd.md`
- Creación de spec de componente: `/create-component-sdd.md`
- Creación de spec de proceso: `/create-process-sdd.md`
- Arranque de la aplicación: `/launch-app.md`
- Publicación en Git: `/git-publish.md` (únicamente bajo petición explícita)
- Descubrimiento de skills: `/list-skills.md`

## 4. Pruebas y verificación

- Ejecutar los tests con el comando oficial del stack: `{m.stack.test_command}`.
- Si un comando falla, diagnosticar la causa raíz antes de proponer soluciones superficiales.

## 5. Prohibiciones infranqueables

- Telemetría de usuario o librerías de analítica no autorizadas ({m.platform.privacy_policy}).
- `git push` sin instrucción explícita del usuario.
- Colores o márgenes fuera de `design-system/tokens.json`.
- Código sin spec aprobada.
"""

        # 2. workflows/harness-validator.md
        out["workflows/harness-validator.md"] = f"""# Workflow — Validación del arnés ({m.identity.name})

## Disparador
Cambios en specs, contexto, scopes, memoria, skills o configuración del arnés.

## Protocolo
1. Ejecutar:
```bash
python .ai-harness/skills/harness-validator/runner.py
```
2. Si falla, leer el check señalado y corregir la causa raíz.
3. Volver a ejecutar hasta que pase.

## Reglas
- No desactivar checks para "hacer pasar" la validación.
- No declarar la tarea terminada con fallos abiertos.
- La fuente de verdad de las skills es `.ai-harness/skills/registry.yaml`.
"""

        # 3. workflows/preflight.md
        out["workflows/preflight.md"] = f"""# Workflow — Preflight de Calidad y Arquitectura ({m.identity.name})

## Disparador
Cambios en código fuente ({m.stack.language}), configuración, dependencias o interfaz gráfica.

## Protocolo
1. Ejecutar:
```bash
python .ai-harness/skills/preflight/runner.py [target]
```
2. Interpretar el resultado:
   - `PASSED`: no hay violaciones.
   - `WARNING`: avisos informativos; revisar y decidir.
   - `FAILED`: corregir antes de continuar.
3. Si falla:
   - Leer archivo y línea indicados.
   - Diagnosticar causa raíz.
   - Corregir el código.
   - Reejecutar el preflight.

## Checks
- Formato, linter y tests del stack (`{m.stack.test_command}`).
- Fronteras de imports entre features y barrels autorizados.
- Contratos de dominio inmutables sin `any`/`dynamic`.
- Disciplina estricta de tokens de diseño (cero HEX literal).
- Dependencias prohibidas o no homologadas.
"""

        # 4. workflows/sync-sdd.md
        out["workflows/sync-sdd.md"] = f"""# Workflow — Sincronización spec ↔ código ({m.identity.name})

## Disparador
Cambios en una spec, en su target de código o en ambos.

## Protocolo
1. Actualizar la baseline tras implementar o modificar intencionalmente un componente:
```bash
python .ai-harness/skills/sync-sdd/runner.py --baseline
```
2. Verificar la sincronización:
```bash
python .ai-harness/skills/sync-sdd/runner.py
```
3. Corregir cualquier `MISSING` o `DIVERGED` antes de cerrar la tarea.

## Reglas
- No actualizar la baseline para ocultar una divergencia involuntaria.
- Toda spec aprobada debe tener target existente.
"""

        # 5. workflows/create-component-sdd.md
        root_path = m.scopes[0].path_roots[0] if m.scopes and m.scopes[0].path_roots else "src/"
        out["workflows/create-component-sdd.md"] = f"""# Workflow — Crear spec de componente (CMP-NN)

## Disparador
Solicitud de crear o actualizar una spec técnica de componente.

## Protocolo
1. Ejecutar el runner:
```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-NN \\
  --name "<nombre>" \\
  --target {root_path}<ruta>/<archivo> \\
  --layer <bootstrap|domain|ui> \\
  --dir .ai-harness/sdd/1_COMPONENTS/<layer>/CMP-NN-<slug>
```
2. Completar todos los marcadores en `CMP-NN-<slug>.spec.md` y `user_story.md`.
3. Validar:
```bash
python .ai-harness/skills/harness-validator/runner.py
```
"""

        # 6. workflows/create-process-sdd.md
        out["workflows/create-process-sdd.md"] = f"""# Workflow — Crear spec de proceso (PRC-NN)

## Disparador
Solicitud de crear o actualizar una spec técnica de proceso o flujo.

## Protocolo
1. Ejecutar el runner:
```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-NN \\
  --name "<nombre>" \\
  --target {root_path}<coordinador> \\
  --dir .ai-harness/sdd/2_PROCESSES/<modulo>/PRC-NN-<slug>
```
2. Completar el diagrama Mermaid y los pasos técnicos `ST-*`.
3. Validar:
```bash
python .ai-harness/skills/harness-validator/runner.py
```
"""

        # 7. workflows/launch-app.md
        out["workflows/launch-app.md"] = f"""# Workflow — Arranque de la App ({m.identity.name})

## Disparador
Cuando el usuario solicite arrancar, ejecutar o probar la aplicación localmente.

## Protocolo
1. Ejecutar:
```bash
python .ai-harness/skills/launch-app/runner.py
```
2. El comando arrancará el entorno mediante `{m.stack.launch_command}`.
"""

        # 8. workflows/git-publish.md
        out["workflows/git-publish.md"] = f"""# Workflow — Publicación en Git ({m.identity.name})

## Disparador
Solicitud EXPLÍCITA del usuario para publicar, hacer push o crear PR/MR en {m.git_remote.provider.value.upper()}.

## Protocolo
1. Comprobar estado previo:
```bash
python .ai-harness/skills/git-publish/runner.py status
```
2. Publicar tras confirmación de calidad:
```bash
python .ai-harness/skills/git-publish/runner.py push -m "<tipo>: <descripcion del cambio>"
```

## Reglas
- PROHIBIDO ejecutar push sin solicitud explícita del usuario.
- Si `harness-validator` o `preflight` fallan, la publicación se aborta automáticamente.
"""

        # 9. workflows/list-skills.md
        out["workflows/list-skills.md"] = f"""# Workflow — Inventario de Skills ({m.identity.name})

## Objetivo
Mostrar las skills realmente disponibles en el arnés.

## Protocolo
1. Leer `.ai-harness/skills/registry.yaml`.
2. Para cada entrada, verificar su `skill.yaml` y su runner.
3. Contrastar con `.agents/skills/<name>/SKILL.md`.
4. Presentar la tabla de capacidades disponibles.
"""

        return out

    def generate_registry_yaml(self) -> str:
        """Genera el contenido de .ai-harness/skills/registry.yaml."""
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
    description: Publica en {m.git_remote.provider.value.upper()} solo bajo petición explícita y tras pasar quality gates.
"""

