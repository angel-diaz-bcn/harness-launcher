"""
Generator Engine: Orquestador atómico 360° de generación de alta fidelidad.
Coordina la creación de todo el arnés de forma perfecta y en el orden exacto:
1. Configuración raíz (harness.config.yaml)
2. Los 12 contextos normativos profundos (context_gen.py)
3. Scopes contractuales con identidad, posee/no posee e invariantes (scope_gen.py)
4. Suite completa de diseño: 6 docs + tokens.json (design_system_gen.py)
5. Memoria preventiva: fallos + 3 ADRs técnicos (memory_gen.py)
6. Semilla SDD: 4 componentes + 1 proceso (sdd_gen.py)
7. Fixtures deterministas (.ai-harness/fixtures/README.md)
8. Motor de skills (.ai-harness/skills/) y carpeta .agents/ (SKILL.md por skill y README de índice)
9. Carpeta .clinerules/ (rules.md adaptado al stack y workflows invocables)
10. Ficheros .gitignore y .aiignore adaptados a la tecnología
11. Repositorio remoto Git y canalización CI/CD (GitLab vs GitHub)
12. Dependencias del arnés (requirements.txt)
13. Manifiesto del arnés (MANIFEST.md)
14. README.md de la raíz del producto
15. Y AL FINAL: AGENTS.md como orquestador estricto sin reglas de negocio
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from models import BootstrapManifest, GitProvider, StackType

from generators.context_gen import ContextGenerator
from generators.design_system_gen import DesignSystemGenerator
from generators.memory_gen import MemoryGenerator
from generators.scope_gen import ScopeGenerator
from generators.sdd_gen import SDDGenerator
from generators.skills_gen import SkillsGenerator


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
        """Genera el árbol completo del arnés en el orden de gobernanza estricto."""
        # 1. Configuración estructural primero
        self._generate_harness_config()

        # 2. Contexto normativo profundo (12 documentos)
        self._generate_context_files()

        # 3. Scopes contractuales
        self._generate_scope_files()

        # 4. Suite completa de Sistema de Diseño (6 documentos + tokens.json)
        self._generate_design_system()

        # 5. Memoria preventiva (Modos de fallo + 3 ADRs)
        self._generate_memory_and_adrs()

        # 6. Semilla SDD (CMP-00 a CMP-03 y PRC-01)
        self._generate_sdd()

        # 7. Fixtures deterministas
        self._generate_fixtures_readme()

        # 8. Skills de .ai-harness y carpeta .agents/
        self._generate_skills_and_agents()

        # 9. Carpeta .clinerules/ (rules.md y workflows)
        self._generate_clinerules()

        # 10. Ficheros .gitignore y .aiignore específicos del stack
        self._generate_gitignore()
        self._generate_aiignore()

        # 11. Configuración de repositorio remoto y canalización CI/CD
        self._setup_git_remote_and_ci()

        # 12. Dependencias del arnés (requirements.txt)
        self._generate_requirements_txt()

        # 13. Manifiesto del arnés (MANIFEST.md)
        self._generate_manifest_md()

        # 14. README.md de presentación del producto
        self._generate_readme_md()

        # 15. Y AL FINAL: AGENTS.md (orquestador maestro con todos los scopes y workflows)
        self._generate_agents_md()

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
  launch_command: "{m.stack.launch_command}"
  test_command: "{m.stack.test_command}"
  git_provider: "{m.git_remote.provider.value}"
  remote_url: "{m.git_remote.url}"

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
    # 2. Los 12 Contextos Normativos (.ai-harness/context/)
    # -------------------------------------------------------------------------
    def _generate_context_files(self) -> None:
        gen = ContextGenerator(self.manifest)
        for filename, content in gen.generate_all().items():
            self._write(self.harness_dir / "context" / filename, content)

    # -------------------------------------------------------------------------
    # 3. Scopes Contractuales (.ai-harness/scopes/)
    # -------------------------------------------------------------------------
    def _generate_scope_files(self) -> None:
        gen = ScopeGenerator(self.manifest)
        for scope in self.manifest.scopes:
            content = gen.generate_scope(scope)
            self._write(self.harness_dir / "scopes" / f"block_{scope.name}.md", content)

    # -------------------------------------------------------------------------
    # 4. Suite completa de Sistema de Diseño (.ai-harness/design-system/)
    # -------------------------------------------------------------------------
    def _generate_design_system(self) -> None:
        gen = DesignSystemGenerator(self.manifest)
        for filename, content in gen.generate_all().items():
            self._write(self.harness_dir / "design-system" / filename, content)

    # -------------------------------------------------------------------------
    # 5. Memoria y Decisiones (.ai-harness/memory/)
    # -------------------------------------------------------------------------
    def _generate_memory_and_adrs(self) -> None:
        gen = MemoryGenerator(self.manifest)
        for filename, content in gen.generate_all().items():
            self._write(self.harness_dir / "memory" / filename, content)

    # -------------------------------------------------------------------------
    # 6. Semilla SDD (.ai-harness/sdd/)
    # -------------------------------------------------------------------------
    def _generate_sdd(self) -> None:
        # Copiar plantillas canónicas de SDD
        launcher_templates = Path(__file__).resolve().parent.parent.parent / "sdd" / "templates"
        target_templates = self.harness_dir / "sdd" / "templates"
        if launcher_templates.exists():
            for tpl in launcher_templates.glob("*"):
                if tpl.is_file():
                    content = tpl.read_text(encoding="utf-8", errors="ignore")
                    self._write(target_templates / tpl.name, content)

        gen = SDDGenerator(self.manifest)
        for filepath, content in gen.generate_all().items():
            self._write(self.harness_dir / "sdd" / filepath, content)

    # -------------------------------------------------------------------------
    # 7. Fixtures Deterministas (.ai-harness/fixtures/)
    # -------------------------------------------------------------------------
    def _generate_fixtures_readme(self) -> None:
        content = """# Fixtures deterministas

Datos de prueba reproducibles, sin red y sin servicios externos. Un fixture es
entrada conocida con salida esperada: si cambia el fixture, cambia el test.

## Estructura sugerida

```
fixtures/
├── valid/       # Casos que deben procesarse sin error
├── invalid/     # Casos que deben rechazarse con un error concreto
└── edge/        # Límites: vacío, máximo, duplicado, formato inesperado
```

## Reglas

- Los fixtures no contienen datos personales ni contenido con derechos.
- Cada fixture declara en su nombre el caso que representa.
- Los tests no descargan fixtures de Internet.
- Los logs de fallo no se guardan aquí: van a `memory/ephemeral_feedback/`.
- Un fixture sin test que lo consuma es deuda: se elimina o se usa.
"""
        self._write(self.harness_dir / "fixtures" / "README.md", content)

    # -------------------------------------------------------------------------
    # 8. Skills de .ai-harness y carpeta .agents/
    # -------------------------------------------------------------------------
    def _generate_skills_and_agents(self) -> None:
        m = self.manifest
        skills_gen = SkillsGenerator(m)

        # 1. Si el workspace destino es diferente al lanzador, copiar herramientas ejecutables de .ai-harness/skills/
        launcher_skills_dir = Path(__file__).resolve().parent.parent
        target_skills_dir = self.harness_dir / "skills"

        if launcher_skills_dir.resolve() != target_skills_dir.resolve():
            for item in launcher_skills_dir.iterdir():
                if item.name.startswith((".", "__")) or item.name in ("bootstrap-harness", "registry.yaml"):
                    continue
                target_dest = target_skills_dir / item.name
                if item.is_dir():
                    for subfile in item.rglob("*"):
                        rel = subfile.relative_to(launcher_skills_dir)
                        if subfile.is_file() and not any(p.startswith((".", "__")) for p in rel.parts):
                            rel_target = target_skills_dir / rel
                            self.generated_files.append(str(rel_target.relative_to(self.workspace_root)))
                            if not self.dry_run:
                                rel_target.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(subfile, rel_target)
                elif item.is_file():
                    self.generated_files.append(str(target_dest.relative_to(self.workspace_root)))
                    if not self.dry_run:
                        target_dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target_dest)

        # 2. Generar .ai-harness/skills/registry.yaml adaptado al proyecto
        self._write(self.harness_dir / "skills" / "registry.yaml", skills_gen.generate_registry_yaml())

        # 3. Generar toda la suite de .agents/skills/
        agents_skills_dir = self.workspace_root / ".agents" / "skills"
        for rel_path, content in skills_gen.generate_agents_skills().items():
            self._write(agents_skills_dir / rel_path, content)

    # -------------------------------------------------------------------------
    # 9. Carpeta .clinerules/ (rules.md y workflows)
    # -------------------------------------------------------------------------
    def _generate_clinerules(self) -> None:
        m = self.manifest
        skills_gen = SkillsGenerator(m)
        clinerules_dir = self.workspace_root / ".clinerules"

        for rel_path, content in skills_gen.generate_clinerules().items():
            self._write(clinerules_dir / rel_path, content)

    # -------------------------------------------------------------------------
    # 10. .gitignore y .aiignore
    # -------------------------------------------------------------------------
    def _generate_gitignore(self) -> None:
        m = self.manifest
        extra_ignores = ""
        stype = m.stack.stack_type

        if stype in (StackType.FLUTTER, StackType.DART):
            extra_ignores = """# --- Flutter & Dart ---
.dart_tool/
.packages
build/
.flutter-plugins
.flutter-plugins-dependencies
ephemeral/
"""
        elif stype == StackType.PYTHON:
            extra_ignores = """# --- Python ---
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.ruff_cache/
"""
        elif stype == StackType.NODE:
            extra_ignores = """# --- Node & Web / React Native ---
node_modules/
dist/
build/
.next/
out/
.expo/
.npm/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
"""
        elif stype == StackType.GO:
            extra_ignores = """# --- Go ---
bin/
dist/
*.exe
*.test
vendor/
"""
        elif stype == StackType.RUST:
            extra_ignores = """# --- Rust ---
target/
**/*.rs.bk
"""

        content = f"""# =============================================================================
# .gitignore — {m.identity.name}
# =============================================================================

# --- Secretos, Entornos y Credenciales (PROHIBIDO EN GIT) ---
.env
.env.*
*.pem
*.key
*.keystore
*.p12

# --- Sistema Operativo e IDEs ---
.DS_Store
Thumbs.db
.idea/
.vscode/
*.swp
*.swo

# --- Caché del Arnés y Herramientas ---
.spectra/
*.log
replay_pid*
coverage/

{extra_ignores}
"""
        self._write(self.workspace_root / ".gitignore", content)

    def _generate_aiignore(self) -> None:
        content = """# =============================================================================
# .aiignore — Exclusiones de contexto para agentes de IA
# =============================================================================
.git/
.spectra/
node_modules/
.venv/
venv/
build/
dist/
.next/
.expo/
.dart_tool/
target/
__pycache__/
*.log
*.lock
*.sqlite
*.db
coverage/
*.map
"""
        self._write(self.workspace_root / ".aiignore", content)

    # -------------------------------------------------------------------------
    # 11. Configuración Git Remoto y Pipeline CI/CD (GitLab vs GitHub)
    # -------------------------------------------------------------------------
    def _setup_git_remote_and_ci(self) -> None:
        m = self.manifest
        if m.git_remote.url and not self.dry_run:
            try:
                res = subprocess.run(["git", "remote", "get-url", "origin"], cwd=self.workspace_root, capture_output=True, text=True)
                if res.returncode == 0:
                    subprocess.run(["git", "remote", "set-url", "origin", m.git_remote.url], cwd=self.workspace_root, check=False)
                else:
                    subprocess.run(["git", "remote", "add", "origin", m.git_remote.url], cwd=self.workspace_root, check=False)
            except Exception:
                pass

        if m.git_remote.setup_ci:
            if m.git_remote.provider == GitProvider.GITLAB:
                gitlab_ci = f"""stages:
  - test
  - preflight

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/

harness_validator:
  stage: test
  image: python:3.11-slim
  script:
    - pip install -r requirements.txt
    - python .ai-harness/skills/harness-validator/runner.py

preflight_gate:
  stage: preflight
  image: python:3.11-slim
  script:
    - pip install -r requirements.txt
    - python .ai-harness/skills/preflight/runner.py
    - python .ai-harness/skills/sync-sdd/runner.py
"""
                self._write(self.workspace_root / ".gitlab-ci.yml", gitlab_ci)

            elif m.git_remote.provider == GitProvider.GITHUB:
                github_ci = f"""name: Harness Quality Gate

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Harness dependencies
        run: pip install -r requirements.txt
      - name: Run Harness Validator
        run: python .ai-harness/skills/harness-validator/runner.py
      - name: Run Preflight Checks
        run: python .ai-harness/skills/preflight/runner.py
      - name: Run SDD Sync Check
        run: python .ai-harness/skills/sync-sdd/runner.py
"""
                self._write(self.workspace_root / ".github" / "workflows" / "harness-ci.yml", github_ci)

    # -------------------------------------------------------------------------
    # 12. Dependencias del arnés (requirements.txt)
    # -------------------------------------------------------------------------
    def _generate_requirements_txt(self) -> None:
        content = """pyyaml>=6.0.0
pydantic>=2.0.0
"""
        self._write(self.workspace_root / "requirements.txt", content)

    # -------------------------------------------------------------------------
    # 13. Manifiesto del arnés (MANIFEST.md)
    # -------------------------------------------------------------------------
    def _generate_manifest_md(self) -> None:
        m = self.manifest
        content = f"""# MANIFEST — qué copiar y qué no

Lista canónica de los elementos que forman el arnés de {m.identity.name}. Al trasladarlo a un
proyecto nuevo, se copia solo la sección 1.

---

## 1. Núcleo copiable

| Ruta | Obligatorio | Función |
|---|---|---|
| `AGENTS.md` | Sí | Enrutador operativo |
| `harness.config.yaml` | Sí | Configuración estructural |
| `requirements.txt` | Sí | Dependencias del tooling |
| `.aiignore` | Sí | Exclusión de contexto para el agente |
| `.gitignore` | Sí | Exclusión de control de versiones |
| `.clinerules/rules.md` | Sí | Reglas de integración del agente |
| `.clinerules/workflows/*.md` | Sí | Workflows invocables con `/` |
| `.agents/skills/<name>/SKILL.md` | Sí | Documentación de uso por skill |
| `.agents/skills/README.md` | Sí | Índice de skills |
| `.ai-harness/context/*` | Sí | 12 documentos normativos |
| `.ai-harness/scopes/*` | Sí | Límites de escritura |
| `.ai-harness/sdd/templates/*` | Sí | Plantillas y convención |
| `.ai-harness/sdd/1_COMPONENTS/*` | Sí | Taxonomía de componentes |
| `.ai-harness/sdd/2_PROCESSES/*` | Sí | Taxonomía de procesos |
| `.ai-harness/memory/*` | Sí | Modos de fallo, ADRs y feedback |
| `.ai-harness/design-system/*` | Sí | Tokens y documentos de diseño |
| `.ai-harness/fixtures/README.md` | Sí | Convención de datos de prueba |
| `.ai-harness/skills/**` | Sí | Validadores y runners |

---

## 2. No copiable

| Ruta | Motivo |
|---|---|
| `README.md` | Presentación de este producto específico |
| `MANIFEST.md` | Este archivo |
| `.ai-harness/memory/ephemeral_feedback/*` | Logs locales de ejecución |
| `.ai-harness/memory/sync-state.json` | Baseline generada por sync-sdd |
| `.git/` | Historia del repositorio |
"""
        self._write(self.workspace_root / "MANIFEST.md", content)

    # -------------------------------------------------------------------------
    # 14. README.md de la raíz del producto
    # -------------------------------------------------------------------------
    def _generate_readme_md(self) -> None:
        m = self.manifest
        repo_info = ""
        if m.git_remote.url:
            repo_info = f"- **Repositorio remoto ({m.git_remote.provider.value.upper()}):** `{m.git_remote.url}`"

        content = f"""# {m.identity.name}

> {m.identity.description}

Proyecto construido con **{m.stack.language}** ({m.stack.framework}) bajo **Clean Architecture** y desarrollo guiado por especificaciones (**SDD**).

---

## 1. Visión y Módulos del Producto

- **Audiencia objetivo:** {m.identity.target_audience}
- **Stack tecnológico:** {m.stack.language} | {m.stack.framework} | Gestor: `{m.stack.package_manager}`
- **Plataformas objetivo:** {', '.join(m.platform.platforms)}
- **Política de privacidad:** {m.platform.privacy_policy}
{repo_info}

### Módulos Principales (Scopes)
{chr(10).join([f"- **{s.title} (`block_{s.name}`):** {s.description}" for s in m.scopes])}

---

## 2. Requisitos y Comandos de Desarrollo

- Runtime de {m.stack.language} instalado en la máquina.
- Python 3.11+ para la ejecución del tooling de gobernanza (`requirements.txt`).

```bash
# Instalación de dependencias del arnés
python -m pip install -r requirements.txt

# Arranque de la aplicación
python .ai-harness/skills/launch-app/runner.py
# (Comando subyacente: {m.stack.launch_command})

# Ejecución de la suite de tests
{m.stack.test_command}
```

---

## 3. Puertas de Verificación de Calidad (Quality Gates)

Antes de realizar commits o publicar cambios, el sistema valida la arquitectura e integridad:

```bash
python .ai-harness/skills/harness-validator/runner.py
python .ai-harness/skills/preflight/runner.py
python .ai-harness/skills/sync-sdd/runner.py
```

---

## 4. Flujo de Trabajo para Agentes de IA

Cualquier agente de IA que colabore en este repositorio debe comenzar leyendo obligatoriamente [`AGENTS.md`](file:///./AGENTS.md) y ejecutar la carga JIT en el orden exacto indicado antes de inspeccionar o modificar código.
"""
        self._write(self.workspace_root / "README.md", content)

    # -------------------------------------------------------------------------
    # 15. Y AL FINAL: AGENTS.md (Orquestador Estricto sin reglas de negocio)
    # -------------------------------------------------------------------------
    def _generate_agents_md(self) -> None:
        m = self.manifest
        scopes_list = ", ".join([f"`block_{s.name}.md`" for s in m.scopes])

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
6. `.ai-harness/scopes/block_*.md` — scope del área que se va a tocar ({scopes_list}).
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

    @staticmethod
    def _to_yaml_list(items: list[str], indent: int = 4) -> str:
        prefix = " " * indent
        if not items:
            return f"{prefix}[]"
        return "\n".join([f"{prefix}- {item}" for item in items])
