"""
Scanner and Ingestion Engine for Project Documentation & Codebase.
Analiza tanto .ai-harness/input/ como la raíz del proyecto para inferir automáticamente
el stack real, archivos de configuración (pubspec, package.json, pyproject.toml, go.mod) y módulos de negocio.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from models import ProductArchetype, ScopeDefinition, StackType, TechStack


class InputDigest(BaseModel):
    model_config = ConfigDict(frozen=True)

    files_found: list[str] = Field(default_factory=list)
    suggested_name: str | None = None
    suggested_description: str | None = None
    suggested_archetype: ProductArchetype | None = None
    detected_stack: StackType | None = None
    detected_framework: str | None = None
    detected_package_manager: str | None = None
    detected_launch_cmd: str | None = None
    detected_test_cmd: str | None = None
    detected_modules: list[ScopeDefinition] = Field(default_factory=list)
    detected_context_overrides: dict[str, str] = Field(default_factory=dict)
    detected_design_overrides: dict[str, str] = Field(default_factory=dict)
    raw_summary: str = ""


class InputScanner:
    """Escanea documentos de entrada y el workspace existente."""

    SUPPORTED_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}

    def __init__(self, input_dir: Path, workspace_root: Path | None = None) -> None:
        self.input_dir = Path(input_dir).resolve()
        self.workspace_root = Path(workspace_root).resolve() if workspace_root else self.input_dir.parent.parent

    def scan(self) -> InputDigest:
        found_names: list[str] = []
        combined_text = ""

        # 1. Escanear .ai-harness/input/
        if self.input_dir.exists() and self.input_dir.is_dir():
            for path in self.input_dir.iterdir():
                if path.is_file() and path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    if path.name.lower() != "readme.md" or len(list(self.input_dir.iterdir())) == 1:
                        try:
                            content = path.read_text(encoding="utf-8", errors="ignore")
                            combined_text += f"\n--- {path.name} ---\n" + content
                            found_names.append(path.name)
                        except Exception:
                            continue

        # 2. Inspeccionar archivos de configuración del workspace real
        workspace_stack, ws_fw, ws_pkg, ws_launch, ws_test, ws_name = self._scan_workspace_config()

        # Detección heurística en base a docs o workspace
        suggested_name = ws_name or self._extract_project_name(combined_text)
        suggested_description = self._extract_description(combined_text)
        archetype = self._detect_archetype(combined_text, workspace_stack)
        detected_modules = self._extract_modules(combined_text, workspace_stack)

        summary_parts = []
        if found_names:
            summary_parts.append(f"Documentos analizados en input/: {', '.join(found_names)}")
        if workspace_stack:
            summary_parts.append(f"Workspace configurado con {workspace_stack.value}")

        ctx_ov, ds_ov = self.scan_overrides()

        return InputDigest(
            files_found=found_names,
            suggested_name=suggested_name,
            suggested_description=suggested_description,
            suggested_archetype=archetype,
            detected_stack=workspace_stack,
            detected_framework=ws_fw,
            detected_package_manager=ws_pkg,
            detected_launch_cmd=ws_launch,
            detected_test_cmd=ws_test,
            detected_modules=detected_modules,
            detected_context_overrides=ctx_ov,
            detected_design_overrides=ds_ov,
            raw_summary=" | ".join(summary_parts) or "Workspace limpio",
        )

    def scan_overrides(self) -> tuple[dict[str, str], dict[str, str]]:
        """Descubre documentos normativos pre-redactados en .ai-harness/input/."""
        context_docs = {
            "system_identity.md", "harness_governance.md", "project_overview.md",
            "architecture_rules.md", "project_structure.md", "coding_standards.md",
            "testing_guidelines.md", "security_privacy.md", "platform_matrix.md",
            "glossary.md", "sdd_framework.md", "ui-design-system.md",
            "system-identity.md", "ui_design_system.md"
        }
        design_docs = {
            "README.md", "01-foundations.md", "02-tokens.md", "03-layout.md",
            "04-components.md", "05-pages.md", "06-code-mapping.md"
        }
        ctx_overrides: dict[str, str] = {}
        ds_overrides: dict[str, str] = {}

        if not self.input_dir.exists():
            return ctx_overrides, ds_overrides

        # Subcarpetas explícitas: .ai-harness/input/context/ y .ai-harness/input/design-system/
        ctx_dir = self.input_dir / "context"
        if ctx_dir.exists() and ctx_dir.is_dir():
            for p in ctx_dir.glob("*.md"):
                ctx_overrides[p.name] = p.read_text(encoding="utf-8", errors="ignore")

        ds_dir = self.input_dir / "design-system"
        if ds_dir.exists() and ds_dir.is_dir():
            for p in ds_dir.glob("*.md"):
                ds_overrides[p.name] = p.read_text(encoding="utf-8", errors="ignore")

        # Ficheros en la raíz de .ai-harness/input/ que coincidan con nombres normativos
        for p in self.input_dir.glob("*.md"):
            clean_name = p.name.replace("-", "_")
            if p.name in context_docs or clean_name in context_docs:
                canonical = clean_name if clean_name in context_docs else p.name
                ctx_overrides[canonical] = p.read_text(encoding="utf-8", errors="ignore")
            elif p.name in design_docs:
                ds_overrides[p.name] = p.read_text(encoding="utf-8", errors="ignore")

        return ctx_overrides, ds_overrides

    def _scan_workspace_config(self) -> tuple[StackType | None, str | None, str | None, str | None, str | None, str | None]:
        ws = self.workspace_root

        # Flutter / Dart
        pubspec = ws / "pubspec.yaml"
        if pubspec.exists():
            content = pubspec.read_text(encoding="utf-8", errors="ignore")
            name_m = re.search(r"^name:\s*([a-zA-Z0-9_-]+)", content, re.MULTILINE)
            name = name_m.group(1) if name_m else None
            is_flutter = "flutter:" in content
            return (
                StackType.FLUTTER if is_flutter else StackType.DART,
                "Flutter" if is_flutter else "Dart",
                "pub",
                "flutter run" if is_flutter else "dart run",
                "flutter test" if is_flutter else "dart test",
                name,
            )

        # Node / TypeScript / JavaScript
        pkg_json = ws / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8", errors="ignore"))
                name = data.get("name")
                scripts = data.get("scripts", {})
                launch = "npm run dev" if "dev" in scripts else "npm start" if "start" in scripts else "node index.js"
                test = "npm test" if "test" in scripts else "npm test"
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                fw = "Next.js" if "next" in deps else "Express" if "express" in deps else "React" if "react" in deps else "Node.js"
                return StackType.NODE, fw, "npm", launch, test, name
            except Exception:
                pass

        # Python
        if (ws / "pyproject.toml").exists() or (ws / "requirements.txt").exists():
            return StackType.PYTHON, "FastAPI / Python", "pip", "uvicorn src.main:app --reload", "pytest", None

        # Go
        if (ws / "go.mod").exists():
            return StackType.GO, "Go", "go modules", "go run ./cmd/main.go", "go test ./...", None

        return None, None, None, None, None, None

    def _extract_project_name(self, text: str) -> str | None:
        match_h1 = re.search(r"^#\s+([A-Za-z0-9_\-\s]{3,30})$", text, re.MULTILINE)
        if match_h1:
            candidate = match_h1.group(1).strip()
            if candidate.lower() not in {"readme", "documentación", "input", "brief", "prd"}:
                return candidate
        match_name = re.search(r"(?:name|proyecto|producto):\s*([A-Za-z0-9_\-\s]{3,30})", text, re.IGNORECASE)
        if match_name:
            return match_name.group(1).strip()
        return None

    def _extract_description(self, text: str) -> str | None:
        match_desc = re.search(r"(?:descripción|propósito|visión|overview):\s*([^\r\n]{15,200})", text, re.IGNORECASE)
        if match_desc:
            return match_desc.group(1).strip()
        return None

    def _detect_archetype(self, text: str, stack: StackType | None) -> ProductArchetype:
        lower = text.lower()
        if "backend" in lower or "api rest" in lower or "microservicio" in lower or "endpoint" in lower:
            return ProductArchetype.BACKEND_API
        if "cli" in lower or "terminal" in lower or "línea de comando" in lower:
            return ProductArchetype.CLI_TOOL
        if "librería" in lower or "sdk" in lower or "paquete" in lower:
            return ProductArchetype.LIBRARY
        if stack in (StackType.FLUTTER, StackType.NODE):
            return ProductArchetype.GUI_APP
        return ProductArchetype.GUI_APP

    def _extract_modules(self, text: str, stack: StackType | None) -> list[ScopeDefinition]:
        prefix = "lib" if stack in (StackType.FLUTTER, StackType.DART) else "src"
        modules: list[ScopeDefinition] = []

        # Buscar listas de módulos o features en la documentación
        found = set()
        matches = re.findall(r"[-*]\s*(?:Módulo|Feature|Scope)\s*[:—]\s*([a-zA-Z0-9_-]+)", text, re.IGNORECASE)
        for m in matches:
            slug = m.lower().strip()
            if slug not in found and len(slug) >= 3:
                found.add(slug)
                modules.append(
                    ScopeDefinition(
                        name=slug,
                        title=f"Módulo {slug.capitalize()}",
                        description=f"Responsabilidad y lógica del módulo {slug}",
                        path_roots=[f"{prefix}/features/{slug}"],
                        forbidden_paths=[],
                    )
                )

        return modules
