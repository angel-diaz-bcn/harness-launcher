"""
Template-Driven Scope Generator: Genera archivos de scope (.ai-harness/scopes/block_*.md)
utilizando las plantillas canónicas de scopes como estructura y abstrayendo responsabilidades
según las features reales detectadas del negocio.
"""

from __future__ import annotations

from pathlib import Path
from models import BootstrapManifest, ScopeDefinition, StackType


class ScopeGenerator:
    """Genera archivos de scope a partir de los bloques reales definidos en el manifiesto."""

    def __init__(self, manifest: BootstrapManifest, harness_dir: Path | None = None) -> None:
        self.manifest = manifest
        self.harness_dir = Path(harness_dir).resolve() if harness_dir else Path(__file__).resolve().parents[3]
        self.scopes_dir = self.harness_dir / "scopes"

    def generate_scope(self, scope: ScopeDefinition) -> str:
        m = self.manifest
        path_root = scope.path_roots[0] if scope.path_roots else f"src/features/{scope.name}"
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder_prefix = "lib" if is_flutter else "src"

        # 1. Si existe una plantilla canónica para este bloque (ej. block_core.md), reutilizar su estructura
        template_file = self.scopes_dir / f"block_{scope.name}.md"
        if template_file.exists():
            raw = template_file.read_text(encoding="utf-8", errors="ignore")
            content = raw.replace("<PROYECTO>", m.identity.name)
            content = content.replace("lib/", f"{folder_prefix}/")
            return content

        # 2. Si es una feature de negocio personalizada detectada por el modelo de IA
        return f"""# Scope — {scope.title} (`block_{scope.name}`)

> Solo define límites y fronteras de responsabilidad. Contratos, esquemas e implementación se especifican en la SDD.

---

## 1. Identidad

| Campo | Valor |
|---|---|
| Bloque | {scope.title} |
| Dominio | {scope.description} |
| Ruta autorizada | `{path_root}/` |
| Rutas prohibidas | {', '.join([f'`{p}`' for p in scope.forbidden_paths]) or '`Ninguna de otros bloques`'} |
| Formatos | Tipos nativos inmutables / JSON serializado |
| Estado | Límites estrictos y cerrados |

---

## 2. Propósito y Valor del Bloque

Es la autoridad responsable de **{scope.description}** dentro de {m.identity.name}.
Garantiza el aislamiento funcional del módulo, encapsulando sus estructuras internas y exponiendo únicamente interfaces públicas.

---

## 3. Posee (Responsabilidades exclusivas)

- Modelos de dominio, reglas de negocio e invariantes de {scope.title}.
- Implementación de adaptadores y repositorios asociados a {scope.name}.
- {'Controladores y componentes visuales propios de ' + scope.title if m.ui.has_ui else 'Controladores y endpoints de API para ' + scope.title}.

---

## 4. No posee (Límites y exclusiones estrictas)

- Infraestructura transversal compartida (vive en `{folder_prefix}/core/`).
- Entidades, contratos o datos pertenecientes a otras features.
- Configuración global o ciclo de vida transversal de la aplicación.

---

## 5. Estructura interna de rutas

```
{path_root}/
├── domain/          # Entidades puras, contratos de repositorio y casos de uso
├── data/            # Fuentes de datos, DTOs y persistencia
└── {'presentation/' if m.ui.has_ui else 'controllers/'}    # {'Vistas y componentes' if m.ui.has_ui else 'Controladores de API / handlers'}
```

---

## 6. API Pública y Matriz de Dependencias

- **API Pública autorizada:** `{path_root}/public/` o `{path_root}.{ 'dart' if is_flutter else 'ts' if m.stack.stack_type == StackType.NODE else 'py' }`.
- **Dependencias entrantes:** Solo módulos que consuman la interfaz pública documentada.
- **Prohibido:** Importar archivos de carpetas internas `data/` o submódulos privados de otro bloque.
"""
