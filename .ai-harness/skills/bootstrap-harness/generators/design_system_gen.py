"""
Template-Driven Design System Generator: Genera .ai-harness/design-system/ y tokens.json
utilizando los archivos Markdown y tokens.json existentes como base viva, inyectando
los tokens y decisiones reales recuperadas del brief/PRD por el modelo de IA.
"""

from __future__ import annotations

import json
from pathlib import Path
from models import BootstrapManifest, ProductArchetype


class DesignSystemGenerator:
    """Genera la suite de diseño a partir de las plantillas existentes."""

    def __init__(self, manifest: BootstrapManifest, harness_dir: Path | None = None) -> None:
        self.manifest = manifest
        self.harness_dir = Path(harness_dir).resolve() if harness_dir else Path(__file__).resolve().parents[3]
        self.ds_template_dir = self.harness_dir / "design-system"

    def generate_all(self) -> dict[str, str]:
        m = self.manifest
        if not m.ui.has_ui:
            return {
                "README.md": f"# Sistema de Diseño y Contratos — {m.identity.name}\n\nEste producto es un `{m.identity.archetype.value}` sin interfaz gráfica. No aplica tokens.json visual.\n",
                "01-foundations.md": f"# Fundaciones de API — {m.identity.name}\n\nDiseño centrado en contratos tipados, idempotencia y respuestas HTTP/CLI predecibles.\n",
                "02-tokens.md": f"# Diccionario de Formatos — {m.identity.name}\n\nConvención de serialización JSON, timestamps UTC en ISO-8601 y errores RFC 7807.\n",
                "03-layout.md": "# No aplica (sin UI)\n",
                "04-components.md": "# Controladores y Adaptadores (sin UI)\n",
                "05-pages.md": "# Endpoints y Comandos (sin UI)\n",
                "06-code-mapping.md": "# Mapeo de Contratos a Código\n",
                "tokens.json": json.dumps({"version": "1.0.0", "has_ui": False, "note": "Backend / CLI API - No visual tokens required"}, indent=2),
            }

        docs = [
            "01-foundations.md",
            "02-tokens.md",
            "03-layout.md",
            "04-components.md",
            "05-pages.md",
            "06-code-mapping.md",
            "README.md",
        ]

        result: dict[str, str] = {}
        for doc in docs:
            template_path = self.ds_template_dir / doc
            if template_path.exists():
                raw = template_path.read_text(encoding="utf-8", errors="ignore")
                content = raw.replace("<PROYECTO>", m.identity.name)
                if not m.ui.focus_navigation_required:
                    content = content.replace("D-Pad", "Teclado / Ratón / Táctil")
                result[doc] = content
            else:
                result[doc] = f"# {doc}\n\nEspecificación de diseño para {m.identity.name}.\n"

        result["tokens.json"] = self._resolve_tokens_json()
        return result

    def _resolve_tokens_json(self) -> str:
        m = self.manifest

        # 1. Si el manifiesto trae tokens personalizados recuperados del PRD/usuario, usarlos
        if m.ui.custom_tokens:
            return json.dumps(m.ui.custom_tokens, indent=2)

        # 2. Si existe un tokens.json en la plantilla, adaptarlo sin inventar valores mágicos
        template_tokens = self.ds_template_dir / "tokens.json"
        if template_tokens.exists():
            try:
                data = json.loads(template_tokens.read_text(encoding="utf-8", errors="ignore"))
                if "meta" in data:
                    data["meta"]["name"] = f"{m.identity.name} Design Tokens"
                return json.dumps(data, indent=2)
            except Exception:
                pass

        # 3. Fallback neutro
        neutral = {
            "version": "1.0.0",
            "theme": m.ui.theme_preference,
            "has_ui": True,
            "colors": {},
            "spacing": {},
            "typography": {}
        }
        return json.dumps(neutral, indent=2)
