"""
Scanner and Ingestion Engine for Project Documentation.
Analiza .ai-harness/input/ o carpetas externas para alimentar el cuestionario guiado.
"""

from __future__ import annotations

import re
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field


class InputDigest(BaseModel):
    model_config = ConfigDict(frozen=True)

    files_found: list[str] = Field(default_factory=list)
    suggested_name: str | None = None
    suggested_description: str | None = None
    detected_stack: str | None = None
    detected_framework: str | None = None
    detected_modules: list[str] = Field(default_factory=list)
    raw_summary: str = ""


class InputScanner:
    """Escanea y procesa documentos de texto de entrada."""

    SUPPORTED_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}

    def __init__(self, input_dir: Path) -> None:
        self.input_dir = Path(input_dir).resolve()

    def scan(self) -> InputDigest:
        if not self.input_dir.exists() or not self.input_dir.is_dir():
            return InputDigest()

        valid_files: list[Path] = []
        for path in self.input_dir.iterdir():
            if path.is_file() and path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                if path.name.lower() != "readme.md" or len(list(self.input_dir.iterdir())) == 1:
                    valid_files.append(path)

        if not valid_files:
            return InputDigest()

        combined_text = ""
        found_names: list[str] = []

        for file_path in valid_files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                combined_text += f"\n--- {file_path.name} ---\n" + content
                found_names.append(file_path.name)
            except Exception:
                continue

        # Detección heurística
        suggested_name = self._extract_project_name(combined_text)
        suggested_description = self._extract_description(combined_text)
        detected_stack, detected_framework = self._detect_stack(combined_text)
        detected_modules = self._extract_modules(combined_text)

        summary = f"Analizados {len(valid_files)} documento(s): {', '.join(found_names)}."

        return InputDigest(
            files_found=found_names,
            suggested_name=suggested_name,
            suggested_description=suggested_description,
            detected_stack=detected_stack,
            detected_framework=detected_framework,
            detected_modules=detected_modules,
            raw_summary=summary,
        )

    def _extract_project_name(self, text: str) -> str | None:
        # Buscar encabezados markdown # Proyecto o Name:
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
        # Buscar párrafos descriptivos iniciales
        match_desc = re.search(
            r"(?:descripción|propósito|visión|overview):\s*([^\r\n]{15,200})", text, re.IGNORECASE
        )
        if match_desc:
            return match_desc.group(1).strip()
        return None

    def _detect_stack(self, text: str) -> tuple[str | None, str | None]:
        lower = text.lower()
        if "flutter" in lower or "dart" in lower or "widget" in lower or "bloc" in lower:
            return "flutter", "Flutter"
        if "fastapi" in lower or "django" in lower or "flask" in lower or "python" in lower or "pydantic" in lower:
            return "python", "FastAPI" if "fastapi" in lower else "Python"
        if "react" in lower or "next.js" in lower or "node" in lower or "typescript" in lower or "express" in lower:
            return "node", "TypeScript / Node"
        if "golang" in lower or "go " in lower or "gin" in lower:
            return "go", "Go"
        if "rust" in lower or "cargo" in lower:
            return "rust", "Rust"
        return "generic", "Generic"

    def _extract_modules(self, text: str) -> list[str]:
        modules: list[str] = []
        # Buscar secciones de módulos / features
        match = re.search(r"(?:##\s*(?:módulos|features|componentes|bloques))([\s\S]*?)(?:##|\Z)", text, re.IGNORECASE)
        if match:
            block = match.group(1)
            for line in block.splitlines():
                item = re.search(r"[-*]\s+\*\*?([A-Za-z0-9_\-\s]+)\*\*?", line)
                if item:
                    mod_name = item.group(1).strip().lower().replace(" ", "_")
                    if mod_name and mod_name not in modules:
                        modules.append(mod_name)
        return modules[:6]

