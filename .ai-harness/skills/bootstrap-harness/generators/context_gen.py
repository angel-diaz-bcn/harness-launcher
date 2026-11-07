"""
Template-Driven Context Generator: Genera los 12 documentos de .ai-harness/context/
utilizando los archivos Markdown existentes en el arnés como plantillas maestras y sustituyendo
únicamente los datos recuperados del proyecto real (o fusionando inteligentemente overrides de IA).
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
            template_path = self.context_template_dir / doc
            base_template = ""
            if template_path.exists():
                base_template = template_path.read_text(encoding="utf-8", errors="ignore")

            # 1. Si la IA preparó un override específico en el manifiesto
            if doc in self.manifest.custom_context_overrides:
                override_text = self.manifest.custom_context_overrides[doc].strip()

                # Si el override es exhaustivo (> 40 líneas), usarlo directamente
                if len(override_text.splitlines()) >= 40:
                    result[doc] = self._resolve_common_vars(override_text)
                    continue

                # Si es un snippet corto (< 40 líneas), fusionarlo con la plantilla maestra
                result[doc] = self._merge_override_with_template(doc, override_text, base_template)
                continue

            # 2. De lo contrario, procesar la plantilla Markdown canónica existente
            if base_template:
                result[doc] = self._interpolate_template(doc, base_template)
            else:
                result[doc] = f"# {doc}\n\nDocumento normativo del proyecto {self.manifest.identity.name}.\n"

        return result

    def _resolve_common_vars(self, content: str) -> str:
        m = self.manifest
        content = content.replace("<PROYECTO>", m.identity.name)
        content = content.replace("<proyecto>", m.identity.slug)
        content = content.replace("<plataformas>", ", ".join(m.platform.platforms))
        content = content.replace("<stack>", f"{m.stack.language} {f'({m.stack.framework})' if m.stack.framework else ''}")
        return content

    def _merge_override_with_template(self, doc_name: str, override_text: str, base_template: str) -> str:
        """Fusiona snippets de contexto aportados por el usuario con las reglas maestras inmutables."""
        m = self.manifest
        interpolated_base = self._interpolate_template(doc_name, base_template)

        if doc_name == "coding_standards.md":
            return f"""{override_text}

---

## 3. Estándares Transversales y Disciplina de Calidad

- **Trazabilidad de Símbolos:** Todo símbolo público relevante lleva comentario de trazabilidad hacia su contrato en OpenSpec:
  `/// Spec: MOD-<modulo> / CT-<id>`
- **Cero Excepciones Huérfanas:** Las funciones públicas de servicio capturan errores de bajo nivel y devuelven tipos cerrados o excepciones tipadas de dominio.
- **Tipado Estricto:** Prohibido el uso de tipos genéricos dinámicos (`Any`, `dynamic`, `unknown`) en contratos públicos.
- **Formateo y Linters:** El código debe superar sin advertencias la ejecución de las herramientas estáticas del lenguaje (`ruff/mypy` en Python, `eslint` en TypeScript/Node, `dart analyze` en Dart).
- **Pruebas de Regresión:** Todo fallo o bug detectado requiere al menos un test unitario que lo reproduzca antes de aplicar la corrección.
"""

        if doc_name == "security_privacy.md":
            return f"""{override_text}

---

## 3. Gestión y Rotación de Secretos

- **Variables de Entorno:** Las credenciales nunca se compilan en imágenes ni se versionan en Git; viven en `.env` local (ignorado en `.gitignore`).
- **Rotación Inmediata:** Si un secreto se expone accidentalmente, se invalida de inmediato en el proveedor, se rota y se documenta un ADR de remediación.
- **Principio de Mínimo Privilegio:** Los tokens de APIs externas (Cloudflare, Stripe, DeepSeek, etc.) se generan con permisos acotados exclusivamente a los recursos necesarios.
- **Auditoría de Dependencias:** No se admiten paquetes con vulnerabilidades conocidas (CVE) ni paquetes de telemetría invasiva.
"""

        # Fallback genérico: cabecera del override + cuerpo de la base
        return f"{override_text}\n\n---\n\n{interpolated_base}"

    def _interpolate_template(self, doc_name: str, template: str) -> str:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"

        content = self._resolve_common_vars(template)

        # Adaptaciones especializadas según el documento
        if doc_name == "project_overview.md":
            content = content.replace("<una frase que describa el producto y su usuario principal>", m.identity.description)
            content = content.replace("<qué problema resuelve y por qué esta solución es mejor que la alternativa actual>", m.identity.description)
            module_rows = "\n".join([f"| `{s.name}` | {s.description} | `{s.path_roots[0] if s.path_roots else folder + '/' + s.name}` |" for s in m.scopes])
            content = re.sub(
                r"\|\s*<módulo A>[\s\S]*?\|\s*<módulo C>.*?\n",
                module_rows + "\n",
                content,
            )

        elif doc_name == "ui-design-system.md":
            if not m.ui.has_ui:
                return f"""# Directriz de Diseño y Contratos — {m.identity.name}

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
                content = content.replace("- Todo elemento interactivo es alcanzable con flechas o D-Pad.", "- Todo elemento interactivo es alcanzable con teclado (Tab/Shift+Tab) o interacción táctil/ratón según WCAG AA.")
                content = content.replace("D-Pad", "Teclado y Táctil")

        elif doc_name == "platform_matrix.md":
            rows = "\n".join([f"| **{p}** | Versión estable moderna | Compilación nativa optimizada | Hardware estándar |" for p in m.platform.platforms])
            content = re.sub(r"\|\s*<Plataforma A>[\s\S]*?\|\s*<Plataforma C>.*?\n", rows + "\n", content)

        elif doc_name == "architecture_rules.md":
            if m.architecture.forbidden_packages:
                content += f"\n\n## 7. Paquetes Prohibidos por Diseño\n\nQueda formalmente prohibida la inclusión de las siguientes dependencias:\n"
                for pkg in m.architecture.forbidden_packages:
                    content += f"- `{pkg}`\n"

        return content
