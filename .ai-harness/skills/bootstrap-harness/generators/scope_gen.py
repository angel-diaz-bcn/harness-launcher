"""
Scope Generator: Genera documentos de scope de alta fidelidad con la anatomía de FLIK.
Incluye tabla de identidad, propósito, posee, no posee, árbol de carpetas e invariantes.
"""

from __future__ import annotations

from typing import Any
from models import BootstrapManifest, ScopeDefinition, StackType


class ScopeGenerator:
    """Genera archivos de scope (.ai-harness/scopes/block_*.md) exhaustivos."""

    def __init__(self, manifest: BootstrapManifest) -> None:
        self.manifest = manifest

    def generate_scope(self, scope: ScopeDefinition) -> str:
        m = self.manifest
        path_root = scope.path_roots[0] if scope.path_roots else f"lib/features/{scope.name}"
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder_prefix = "lib" if is_flutter else "src"

        # Deducir responsabilidades según el tipo de bloque
        owns, does_not_own = self._deduce_responsibilities(scope)

        return f"""# Scope — {scope.title} (`block_{scope.name}`)

> Solo define límites y fronteras de responsabilidad. Contratos, esquemas e implementación se especifican en la SDD.
> Diseño visual fuera de ámbito: consultar `design-system/`.

---

## 1. Identidad

| Campo | Valor |
|---|---|
| Bloque | {scope.title} |
| Dominio | {scope.description} |
| Ruta autorizada | `{path_root}/` |
| Rutas prohibidas | {', '.join([f'`{p}`' for p in scope.forbidden_paths]) or '`Ninguna de otros bloques`'} |
| Formatos | JSON / Tipos nativos inmutables |
| Persistencia | {m.architecture.persistence if 'core' in scope.name or 'domain' in scope.name else 'A través del repositorio del dominio'} |
| Estado | Límites estrictos y cerrados |

---

## 2. Propósito

Es la autoridad responsable de **{scope.description}** dentro de {m.identity.name}.
Garantiza el aislamiento funcional del módulo, encapsulando sus estructuras internas y exponiendo únicamente interfaces públicas hacia el resto del sistema.

---

## 3. Posee (Responsabilidades exclusivas)

{chr(10).join([f"- {item}" for item in owns])}

---

## 4. No posee (Límites y exclusiones estrictas)

{chr(10).join([f"- {item}" for item in does_not_own])}

---

## 5. Estructura interna de rutas

```
{path_root}/
├── domain/          # Entidades puras, contratos de repositorio y casos de uso
├── data/            # Implementación de fuentes de datos, DTOs y serialización
└── presentation/    # Controladores de estado, vistas y componentes propios
```

---

## 6. Dependencias

- **Dependencias entrantes:** Solo componentes autorizados mediante la API pública de `{scope.name}`. Prohibido que otros módulos importen submódulos internos.
- **Dependencias salientes:** Únicamente infraestructura compartida en `{folder_prefix}/core` y contratos de dominio aprobados.
- **Prohibido:** Dependencias circulares con otros bloques funcionales.

---

## 7. Invariantes no negociables

1. **Aislamiento de capa:** La lógica de negocio pura no depende de frameworks de presentación ni de clientes de red directos.
2. **Inmutabilidad:** Todas las entidades expuestas son inmutables; no se exponen colecciones mutables directamente.
3. **Manejo tipado de errores:** Ningún error sale del bloque sin estar tipado en el catálogo de fallos del dominio.
4. **Foco y accesibilidad:** Cualquier control visual de este bloque debe integrarse con el modelo de navegación por teclado/foco.
5. **Cero valores visuales literales:** Prohibido el uso de colores HEX o márgenes directos en código de interfaz; obligatorio consultar `design-system/tokens.json`.
"""

    def _deduce_responsibilities(self, scope: ScopeDefinition) -> tuple[list[str], list[str]]:
        sname = scope.name.lower()
        if "core" in sname or "app" in sname:
            owns = [
                "Inicialización de dependencias base y configuración transversal del sistema.",
                "Clientes de red, logging, manejo de errores genéricos y utilidades de bajo nivel.",
                "Mapeo de variables de entorno seguras y ciclo de vida de la aplicación.",
                "Definición de tipos base (Result, Either, Failure) para el resto de módulos.",
                "Constantes globales del sistema sin lógica de negocio.",
            ]
            does_not_own = [
                "Lógica de negocio específica de features particulares.",
                "Pantallas complejas de usuario o flujos de presentación finales.",
                "Decisiones de compra, visualización o gestión de datos de dominio.",
                "Contratos específicos de APIs externas ajenas a la infraestructura genérica.",
                "Valores de diseño visual específicos fuera de los tokens compartidos.",
            ]
        elif "domain" in sname:
            owns = [
                "Entidades de negocio y reglas de validación puras e invariantes.",
                "Casos de uso y orquestación de la lógica del sistema.",
                "Definición de interfaces (puertos) para repositorios y servicios externos.",
                "Cálculos y transformaciones de datos del negocio libres de efectos secundarios.",
            ]
            does_not_own = [
                "Implementación concreta de bases de datos, SQLite, APIs o disco.",
                "Widgets, componentes visuales, layouts o frameworks de UI.",
                "Llamadas directas a librerías de terceros (Firebase, HTTP crudo).",
                "Gestión de ciclo de vida de vistas o eventos de entrada de usuario.",
            ]
        elif "ui" in sname or "presentation" in sname:
            owns = [
                "Composición visual de pantallas y componentes conforme a design-system/.",
                "Controladores de estado de presentación y gestión del ciclo de vida de la vista.",
                "Gestión del árbol de foco, navegación por teclado o D-Pad y eventos de usuario.",
                "Traducción de estados del dominio a representaciones visuales comprensibles.",
            ]
            does_not_own = [
                "Llamadas directas a APIs de red o manipulación de sockets.",
                "Acceso directo a almacenamiento o bases de datos sin pasar por repositorios.",
                "Modificación directa de reglas de negocio en widgets o vistas.",
                "Hardcodeo de estilos, fuentes o colores fuera de tokens.json.",
            ]
        else:
            owns = [
                f"Gestión integral de los casos de uso correspondientes a {scope.title}.",
                f"Definición de modelos de datos, validación y persistencia de {scope.title}.",
                f"Exposición de API pública del módulo hacia el resto de la aplicación.",
                "Caché local y sincronización de datos de su responsabilidad.",
            ]
            does_not_own = [
                "Acceso directo e ilegítimo a la estructura interna de otros módulos.",
                "Manejo global de temas visuales o enrutamiento principal de la aplicación.",
                "Infraestructura común perteneciente al núcleo (Core).",
                "Persistencia de datos que pertenezcan a otros dominios funcionales.",
            ]
        return owns, does_not_own

