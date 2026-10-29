"""
Generator Engine: Generación atómica 360° del arnés personalizado.
Produce harness.config.yaml, AGENTS.md, README.md, .gitignore, .aiignore,
los 12 contextos, scopes, memoria y contratos SDD.
"""

from __future__ import annotations

import json
from pathlib import Path
from models import BootstrapManifest, StackType


class HarnessGenerator:
    """Compila y escribe todos los artefactos del arnés a partir de un manifiesto."""

    def __init__(self, manifest: BootstrapManifest, workspace_root: Path, dry_run: bool = False) -> None:
        self.manifest = manifest
        self.workspace_root = Path(workspace_root).resolve()
        self.harness_dir = self.workspace_root / ".ai-harness"
        self.dry_run = dry_run
        self.generated_files: list[str] = []

    def _write(self, target_path: Path, content: str) -> None:
        rel = target_path.relative_to(self.workspace_root)
        self.generated_files.append(str(rel))
        if self.dry_run:
            return
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content.strip() + "\n", encoding="utf-8")

    def execute(self) -> list[str]:
        """Genera el árbol completo del arnés."""
        self._generate_harness_config()
        self._generate_agents_md()
        self._generate_readme_md()
        self._generate_gitignore()
        self._generate_aiignore()
        self._generate_context_files()
        self._generate_scope_files()
        self._generate_memory_and_adrs()
        self._generate_design_system()
        self._generate_bootstrap_spec()
        return self.generated_files

    # -------------------------------------------------------------------------
    # 1. harness.config.yaml
    # -------------------------------------------------------------------------
    def _generate_harness_config(self) -> None:
        m = self.manifest
        scope_files = [f"block_{s.name}.md" for s in m.scopes]
        all_path_roots = [p for s in m.scopes for p in s.path_roots]
        all_forbidden_paths = [p for s in m.scopes for p in s.forbidden_paths]

        content = f"""version: 1

project:
  name: "{m.identity.name}"
  slug: "{m.identity.slug}"
  stack: {m.stack.stack_type.value}

context:
  required:
    - system_identity.md
    - harness_governance.md
    - project_overview.md
    - architecture_rules.md
    - project_structure.md
    - coding_standards.md
    - testing_guidelines.md
    - security_privacy.md
    - platform_matrix.md
    - glossary.md
    - sdd_framework.md
    - ui-design-system.md
  agents_must_reference:
    - system_identity.md
    - harness_governance.md

scopes:
  required:
{self._to_yaml_list(scope_files, indent=4)}
  path_roots:
{self._to_yaml_list(all_path_roots or ['lib/'], indent=4)}
  forbidden_paths:
{self._to_yaml_list(all_forbidden_paths, indent=4)}

sdd:
  component_prefix: CMP
  process_prefix: PRC
  component_layers:
    - bootstrap
    - domain
    - ui
  blocks:
    - 1_COMPONENTS
    - 2_PROCESSES
    - templates
  implementation_map_heading: "Mapa de implementación"
  frontmatter:
    - spec_id
    - spec_type
    - name
    - target
    - block
    - status
    - version
    - owner
    - last_reviewed
    - approved_at
    - approved_by
    - supersedes
    - superseded_by
    - user_story

memory:
  failure_prefix: "FM"
  min_failure_modes: 5

legacy_terms: []

skills:
  docs_root: ".agents/skills"

architecture:
  features:
{self._to_yaml_list([s.name for s in m.scopes], indent=4)}
  forbidden_by_feature: {{}}
  exclusive_import_paths: {{}}
  framework_import_prefix: "package:{m.identity.slug}/"
  framework_free_features: ["domain"]
  persistence_feature: "{'database' if m.architecture.persistence != 'none' else ''}"
  persistence_imports: []
  forbidden_packages:
{self._to_yaml_list(m.architecture.forbidden_packages, indent=4)}

ui:
  token_feature: "{'tokens' if m.ui.has_ui else ''}"

invariants:
  profile: none
"""
        self._write(self.workspace_root / "harness.config.yaml", content)

    # -------------------------------------------------------------------------
    # 2. AGENTS.md (Orquestador Estricto)
    # -------------------------------------------------------------------------
    def _generate_agents_md(self) -> None:
        m = self.manifest
        content = f"""# AGENTS.md — Orquestador del arnés para {m.identity.name}

Punto de entrada obligatorio para cualquier agente de IA en este repositorio.
Este archivo solo enruta: no duplica reglas de producto, arquitectura ni
implementación.

---

## 1. Carga inicial obligatoria (JIT)

Antes de leer código, proponer cambios o escribir archivos, cargar en este orden:

1. `.ai-harness/context/system_identity.md` — rol y postura del agente.
2. `.ai-harness/context/harness_governance.md` — reglas del propio arnés.
3. `.ai-harness/context/project_overview.md` — visión y módulos del producto.
4. `.ai-harness/context/architecture_rules.md` — fronteras e invariantes.
5. `.ai-harness/context/ui-design-system.md` y `.ai-harness/design-system/README.md`.
6. `.ai-harness/scopes/block_*.md` — scope del área que se va a tocar.
7. `.ai-harness/context/sdd_framework.md` — gobernanza SDD y convención `.spec.md`.
8. La spec `.spec.md` activa, si existe.
9. `.ai-harness/memory/failure_modes.md` — fallos que no deben repetirse.

Si falta el scope o la spec de la tarea, detenerse y pedir la definición antes
de implementar.

---

## 2. Enrutamiento por tarea

| Tarea | Fuente de verdad | Herramienta |
|---|---|---|
| Inicialización del arnés | `.ai-harness/skills/bootstrap-harness/` | `/bootstrap-harness.md` |
| Configuración estructural | `harness.config.yaml` | — |
| Descubrimiento de skills | `.ai-harness/skills/registry.yaml` | `/list-skills.md` |
| Visión de producto | `context/project_overview.md` | — |
| Arquitectura y fronteras | `context/architecture_rules.md` | — |
| Estructura de código | `context/project_structure.md` | — |
| Estándares de código | `context/coding_standards.md` | — |
| Diseño y tokens | `context/ui-design-system.md` y `design-system/` | — |
| Seguridad y privacidad | `context/security_privacy.md` | — |
| Glosario | `context/glossary.md` | — |
| Plataformas | `context/platform_matrix.md` | — |
| Testing | `context/testing_guidelines.md` | — |
| Límites de escritura | `scopes/block_*.md` | — |
| Especificaciones | `sdd/` y `sdd/templates/README.md` | `/create-component-sdd.md`, `/create-process-sdd.md` |
| Validación de producto | `context/architecture_rules.md` §6 | `/preflight.md` |
| Validación del arnés | `context/harness_governance.md` §8 | `/harness-validator.md` |
| Sincronización spec↔código | `sdd/templates/README.md` | `/sync-sdd.md` |
| Arranque de la app | `context/platform_matrix.md` | `/launch-app.md` |
| Publicación Git | `.clinerules/workflows/git-publish.md` | `/git-publish.md` solo bajo demanda |

Los workflows se descubren en `.clinerules/workflows/`; el nombre del comando
incluye la extensión `.md`. Si no aparecen en el menú `/`, recargar la ventana.

---

## 3. Reglas de trabajo

- **SDD-First:** no se escribe código de producción sin spec aprobada en `.ai-harness/sdd/`.
- **Sin invención:** si falta un dato, se registra como pregunta abierta y se detiene la implementación.
- **Configuración primero:** un cambio de estructura del arnés empieza en `harness.config.yaml`, no en el código de un validador.
- **Privacidad:** {m.platform.privacy_policy}.
- **Foco universal:** todo control debe ser navegable con teclado o D-Pad.
- **Diseño:** solo tokens de `design-system/tokens.json`; prohibido HEX literal.
- **Git:** `git push` solo con instrucción explícita del usuario.
- **Sin residuos:** no introducir referencias ni tecnologías de otro proyecto.

---

## 4. Cierre de tarea

Antes de declarar una tarea terminada:

1. Ejecutar `python .ai-harness/skills/harness-validator/runner.py`.
2. Ejecutar `python .ai-harness/skills/preflight/runner.py`.
3. Ejecutar `python .ai-harness/skills/sync-sdd/runner.py`.
4. Corregir la causa raíz de cualquier fallo; no reejecutar a ciegas.
5. Actualizar la spec y el mapa de implementación si cambió el comportamiento.
"""
        self._write(self.workspace_root / "AGENTS.md", content)

    # -------------------------------------------------------------------------
    # 3. README.md
    # -------------------------------------------------------------------------
    def _generate_readme_md(self) -> None:
        m = self.manifest
        content = f"""# {m.identity.name}

> {m.identity.description}

Proyecto construido con **{m.stack.language}** ({m.stack.framework}) bajo **Clean Architecture** y desarrollo guiado por especificaciones (**SDD**).

---

## 1. Visión y Módulos

- **Audiencia:** {m.identity.target_audience}
- **Stack:** {m.stack.language} | {m.stack.framework} | Gestor: {m.stack.package_manager}
- **Plataformas objetivo:** {', '.join(m.platform.platforms)}
- **Privacidad:** {m.platform.privacy_policy}

### Módulos Principales
{chr(10).join([f"- **{s.title}:** {s.description}" for s in m.scopes])}

---

## 2. Requisitos de Desarrollo

- Python 3.11+ (para tooling del arnés de IA).
- Runtime de {m.stack.language} instalado localmente.
- Dependencias del arnés:
  ```bash
  python -m pip install -r requirements.txt
  ```

---

## 3. Puertas de Verificación (Quality Gates)

Antes de realizar commits o publicar cambios, el sistema valida la arquitectura e integridad:

```bash
python .ai-harness/skills/harness-validator/runner.py
python .ai-harness/skills/preflight/runner.py
python .ai-harness/skills/sync-sdd/runner.py
```

---

## 4. Flujo de Trabajo para Agentes de IA

Los agentes de IA que colaboren en este repositorio deben comenzar leyendo obligatoriamente [`AGENTS.md`](file:///./AGENTS.md) y cargar los contextos normativos en el orden JIT indicado.
"""
        self._write(self.workspace_root / "README.md", content)

    # -------------------------------------------------------------------------
    # 4. .gitignore y .aiignore
    # -------------------------------------------------------------------------
    def _generate_gitignore(self) -> None:
        m = self.manifest
        extra_ignores = ""
        if m.stack.stack_type == StackType.FLUTTER:
            extra_ignores = """
# Flutter / Dart
.dart_tool/
.packages
build/
.flutter-plugins
.flutter-plugins-dependencies
"""
        elif m.stack.stack_type == StackType.PYTHON:
            extra_ignores = """
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.pytest_cache/
.mypy_cache/
"""
        elif m.stack.stack_type == StackType.NODE:
            extra_ignores = """
# Node / Web
node_modules/
dist/
.next/
out/
.npm/
"""

        content = f"""# Archivos de entorno y credenciales
.env
.env.*
*.pem
*.key
*.keystore

# Caché del sistema y arnés
.spectra/
__pycache__/
*.log
replay_pid*
{extra_ignores}
"""
        self._write(self.workspace_root / ".gitignore", content)

    def _generate_aiignore(self) -> None:
        content = """# Exclusiones de contexto para agentes de IA
.git/
.spectra/
build/
dist/
node_modules/
.venv/
__pycache__/
*.log
*.sqlite
*.db
"""
        self._write(self.workspace_root / ".aiignore", content)

    # -------------------------------------------------------------------------
    # 5. Contextos Normativos (.ai-harness/context/)
    # -------------------------------------------------------------------------
    def _generate_context_files(self) -> None:
        m = self.manifest
        c_dir = self.harness_dir / "context"

        self._write(c_dir / "system_identity.md", f"""# Identidad del sistema — {m.identity.name}

- **Identidad:** Arquitecto de software de {m.identity.name}.
- **Dominio técnico:** {m.stack.language} con {m.stack.framework} ({m.architecture.style}).
- **Propósito:** {m.identity.description}.

## Límites no negociables
1. SDD-First: sin código de producción sin spec aprobada.
2. Privacidad: {m.platform.privacy_policy}.
3. Calidad: todas las puertas preflight deben pasar en verde.
""")

        self._write(c_dir / "project_overview.md", f"""# Visión General del Proyecto — {m.identity.name}

## 1. Misión
{m.identity.description}

## 2. Audiencia Objetivo
{m.identity.target_audience}

## 3. Módulos
{chr(10).join([f"- **{s.title} ({s.name}):** {s.description}" for s in m.scopes])}
""")

        self._write(c_dir / "architecture_rules.md", f"""# Reglas de Arquitectura — {m.identity.name}

- **Estilo:** {m.architecture.style}.
- **Persistencia:** {m.architecture.persistence}.

## Invariantes Estructurales
1. Las capas superiores consumen las inferiores a través de interfaces (abstracciones).
2. La capa de dominio es pura y agnóstica a librerías de UI o frameworks externos.
3. Paquetes vetados: {', '.join(m.architecture.forbidden_packages)}.
""")

        self._write(c_dir / "project_structure.md", f"""# Estructura del Código — {m.identity.name}

```
lib/ o src/
├── core/             # Infraestructura común y utilidades
├── domain/           # Entidades y contratos puros de negocio
├── infrastructure/   # Implementación de repositorios y adaptadores
└── presentation/     # Vistas y componentes visuales
```
""")

        self._write(c_dir / "coding_standards.md", f"""# Estándares de Código — {m.identity.name}

- **Lenguaje:** {m.stack.language}.
- **Tipado:** Tipado estático estricto, sin tipos implícitos ni variables no verificadas.
- **Asincronía:** Manejo obligatorio de errores en llamadas I/O.
""")

        self._write(c_dir / "platform_matrix.md", f"""# Matriz de Plataformas — {m.identity.name}

Plataformas soportadas oficialmente:
{chr(10).join([f"- {p}" for p in m.platform.platforms])}
""")

        self._write(c_dir / "security_privacy.md", f"""# Seguridad y Privacidad — {m.identity.name}

- **Política de telemetría:** {m.platform.privacy_policy}.
- **Gestión de secretos:** {m.platform.secrets_management}. Prohibido hardcodear credenciales en git.
""")

        self._write(c_dir / "glossary.md", f"""# Glosario de Términos — {m.identity.name}

Términos canónicos del dominio:
- **{m.identity.name}:** El sistema principal.
- **Scope:** Límite modular de responsabilidad y escritura.
- **Spec:** Especificación formal técnica antes de la codificación.
""")

        self._write(c_dir / "ui-design-system.md", f"""# Sistema de Diseño y Tokens — {m.identity.name}

- **UI activa:** {'Sí' if m.ui.has_ui else 'No'}.
- **Tema preferente:** {m.ui.theme_preference}.
- **Foco universal:** {'Obligatorio para teclado / D-Pad' if m.ui.focus_navigation_required else 'No requerido'}.
- **Valores visuales:** Prohibidos colores HEX literales en código de presentación; usar design-system/tokens.json.
""")

    # -------------------------------------------------------------------------
    # 6. Scopes (.ai-harness/scopes/)
    # -------------------------------------------------------------------------
    def _generate_scope_files(self) -> None:
        s_dir = self.harness_dir / "scopes"
        for scope in self.manifest.scopes:
            content = f"""# Scope: {scope.title}

- **Nombre:** `{scope.name}`
- **Descripción:** {scope.description}

## Rutas Autorizadas (path_roots)
{chr(10).join([f"- `{p}`" for p in scope.path_roots]) or "- `lib/`"}

## Rutas Prohibidas (forbidden_paths)
{chr(10).join([f"- `{p}`" for p in scope.forbidden_paths]) or "- Ninguna"}
"""
            self._write(s_dir / f"block_{scope.name}.md", content)

    # -------------------------------------------------------------------------
    # 7. Memoria y Decisiones (.ai-harness/memory/)
    # -------------------------------------------------------------------------
    def _generate_memory_and_adrs(self) -> None:
        m_dir = self.harness_dir / "memory"
        fm_content = f"""# Catálogo de Modos de Fallo — {self.manifest.identity.name}

{chr(10).join([f'''## {fm.id} — {fm.title}

- **Síntoma:** {fm.symptom}
- **Causa raíz:** {fm.root_cause}
- **Mitigación obligatoria:** {fm.mitigation}
''' for fm in self.manifest.failure_modes])}
"""
        self._write(m_dir / "failure_modes.md", fm_content)

        adr = self.manifest.adr_0001
        adr_content = f"""# {adr.id}: {adr.title}

- **Estado:** {adr.status}
- **Fecha:** Inicialización del proyecto

## Contexto
{adr.context}

## Decisión
{adr.decision}

## Consecuencias
{adr.consequences}
"""
        self._write(m_dir / "decisions" / f"{adr.id}-stack-base.md", adr_content)

    # -------------------------------------------------------------------------
    # 8. Sistema de Diseño
    # -------------------------------------------------------------------------
    def _generate_design_system(self) -> None:
        tokens = {
            "version": "1.0.0",
            "theme": self.manifest.ui.theme_preference,
            "colors": {
                "background": "#121212" if self.manifest.ui.theme_preference == "dark" else "#FFFFFF",
                "surface": "#1E1E1E" if self.manifest.ui.theme_preference == "dark" else "#F5F5F5",
                "primary": "#3B82F6",
                "text": "#E5E7EB" if self.manifest.ui.theme_preference == "dark" else "#1F2937",
                "error": "#EF4444",
                "success": "#10B981"
            },
            "spacing": {
                "xs": 4,
                "sm": 8,
                "md": 16,
                "lg": 24,
                "xl": 32
            }
        }
        self._write(
            self.harness_dir / "design-system" / "tokens.json",
            json.dumps(tokens, indent=2, ensure_ascii=False),
        )

    # -------------------------------------------------------------------------
    # 9. SDD Inicial (CMP-00-app-bootstrap)
    # -------------------------------------------------------------------------
    def _generate_bootstrap_spec(self) -> None:
        m = self.manifest
        spec_content = f"""---
spec_id: CMP-00
spec_type: component
name: app-bootstrap
target: lib/core/bootstrap.dart
block: 1_COMPONENTS
status: approved
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-10-29
approved_at: 2026-10-29
approved_by: arquitecto
supersedes: null
superseded_by: null
user_story: Como usuario, quiero arrancar {m.identity.name} de forma rápida e íntegra.
---

# CMP-00 — Inicialización y Arranque de {m.identity.name}

Inicializa los servicios esenciales, dependencias del núcleo y la configuración antes de presentar la pantalla principal.

## 1. Contrato de Arranque
- Carga de variables de entorno seguras.
- Inicialización de persistencia ({m.architecture.persistence}).
- Verificación de integridad inicial.

## Mapa de implementación
- [ ] `lib/core/bootstrap` — inicialización de dependencias principales.
"""
        spec_dir = self.harness_dir / "sdd" / "1_COMPONENTS" / "bootstrap"
        self._write(spec_dir / "CMP-00-app-bootstrap.spec.md", spec_content)

    @staticmethod
    def _to_yaml_list(items: list[str], indent: int = 4) -> str:
        prefix = " " * indent
        if not items:
            return f"{prefix}[]"
        return "\n".join([f"{prefix}- {item}" for item in items])

