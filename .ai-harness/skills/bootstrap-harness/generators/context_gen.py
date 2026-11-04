"""
Template-Driven Context Generator: Genera los 12 documentos de .ai-harness/context/
utilizando los archivos Markdown existentes en el arnés como plantillas maestras y sustituyendo
únicamente los datos recuperados del proyecto real (o inyectando overrides generados por IA).
"""

from __future__ import annotations

import re
from pathlib import Path
from models import BootstrapManifest, ProductArchetype, StackType


class ContextGenerator:
    """Genera los 12 documentos normativos a partir de las plantillas existentes."""

    def __init__(self, manifest: BootstrapManifest, harness_dir: Path | None = None) -> None:
        self.manifest = manifest
        self.harness_dir = Path(harness_dir).resolve() if harness_dir else Path(__file__).resolve().parents[3]
        self.context_template_dir = self.harness_dir / "context"

    def generate_all(self) -> dict[str, str]:
        docs = [
            "system_identity.md",
            "harness_governance.md",
            "project_overview.md",
            "architecture_rules.md",
            "project_structure.md",
            "coding_standards.md",
            "testing_guidelines.md",
            "security_privacy.md",
            "platform_matrix.md",
            "glossary.md",
            "sdd_framework.md",
            "ui-design-system.md",
        ]

        result: dict[str, str] = {}
        for doc in docs:
            # 1. Si la IA ya preparó un override específico de contexto en el manifiesto, usarlo directamente
            if doc in self.manifest.custom_context_overrides:
                result[doc] = self.manifest.custom_context_overrides[doc]
                continue

            # 2. De lo contrario, procesar la plantilla Markdown canónica existente
            template_path = self.context_template_dir / doc
            if template_path.exists():
                raw = template_path.read_text(encoding="utf-8", errors="ignore")
                result[doc] = self._interpolate_template(doc, raw)
            else:
                result[doc] = f"# {doc}\n\nDocumento normativo del proyecto {self.manifest.identity.name}.\n"

        return result

    def _interpolate_template(self, doc_name: str, template: str) -> str:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"

        # Sustitución de variables canónicas
        content = template
        content = content.replace("<PROYECTO>", m.identity.name)
        content = content.replace("<proyecto>", m.identity.slug)
        content = content.replace("<plataformas>", ", ".join(m.platform.platforms))
        content = content.replace("<stack>", f"{m.stack.language} {f'({m.stack.framework})' if m.stack.framework else ''}")

        # Adaptaciones especializadas según el documento
        if doc_name == "project_overview.md":
            content = content.replace("<una frase que describa el producto y su usuario principal>", m.identity.description)
            content = content.replace("<qué problema resuelve y por qué esta solución es mejor que la alternativa actual>", m.identity.description)
            # Reemplazar tabla de módulos con los scopes reales detectados
            module_rows = "\n".join([f"| `{s.name}` | {s.description} | `{s.path_roots[0] if s.path_roots else folder}` |" for s in m.scopes])
            content = re.sub(
                r"\|\s*<módulo A>[\s\S]*?\|\s*<módulo C>.*?\n",
                module_rows + "\n",
                content,
            )

        elif doc_name == "ui-design-system.md":
            if not m.ui.has_ui:
                return f"""# Directriz de Diseño — {m.identity.name}

> **Nota:** Este producto es un `{m.identity.archetype.value}` sin interfaz gráfica de usuario.

---

## 1. Alcance
No aplica sistema de diseño visual ni tokens de color o tipografía. La disciplina de diseño en este proyecto se rige por:
- Consistencia en contratos de API (REST, gRPC, CLI).
- Nomenclatura unificada de campos JSON y respuestas tipadas.
- Mensajes de error legibles y estructurados según RFC 7807 o estándar equivalente.
"""
            if not m.ui.focus_navigation_required:
                content = content.replace("D-Pad / Mando a distancia (si aplica a TV o consolas)", "Navegación táctil y por teclado estándar según WCAG")

        elif doc_name == "platform_matrix.md":
            rows = "\n".join([f"| **{p}** | Versión estable moderna | Compilación nativa optimizada | Hardware estándar |" for p in m.platform.platforms])
            content = re.sub(r"\|\s*<Plataforma A>[\s\S]*?\|\s*<Plataforma C>.*?\n", rows + "\n", content)

        return content
