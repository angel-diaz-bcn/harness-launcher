"""
SDD Generator: Genera la semilla inicial de especificaciones OpenSpec
(módulos vivos en modules/ y propuesta inicial archivada en archive/).
"""

from __future__ import annotations

from datetime import datetime
from models import BootstrapManifest, StackType


class SDDGenerator:
    """Genera módulos vivos y memoria de cambios inicial en .ai-harness/sdd/."""

    def __init__(self, manifest: BootstrapManifest) -> None:
        self.manifest = manifest

    def generate_all(self) -> dict[str, str]:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"
        ext = "dart" if is_flutter else "ts" if m.stack.stack_type == StackType.NODE else "py"

        first_scope = m.scopes[0].name if m.scopes else "domain"
        today = datetime.now().strftime("%Y-%m-%d")
        month_slug = datetime.now().strftime("%Y-%m")

        specs: dict[str, str] = {
            "modules/README.md": self._modules_readme(first_scope),
            "modules/core.md": self._module_core(folder, ext, today),
            f"modules/{first_scope}.md": self._module_domain(folder, ext, first_scope, today),
            f"archive/{month_slug}-initial-setup/proposal.md": self._initial_proposal(month_slug, today),
            f"archive/{month_slug}-initial-setup/tasks.md": self._initial_tasks(),
        }

        if m.stack.has_ui:
            specs["modules/ui.md"] = self._module_ui(folder, ext, today)

        return specs

    def _modules_readme(self, first_scope: str) -> str:
        m = self.manifest
        return f"""# Catálogo de Módulos Vivos — {m.project.name}

Este directorio contiene las especificaciones consolidadas del sistema.
Cada archivo representa la verdad viva y actual de una capacidad funcional o subsistema.

| Módulo ID | Nombre | Ruta de Código | Scope Asociado |
|---|---|---|---|
| `MOD-core` | Núcleo transversal y utilidades | `lib/core/` o `src/core/` | `block_core.md` |
| `MOD-{first_scope}` | {first_scope.capitalize()} y lógica de negocio | `lib/{first_scope}/` o `src/{first_scope}/` | `block_{first_scope}.md` |
{"| `MOD-ui` | Sistema de interfaz y componentes | `lib/ui/` o `src/ui/` | `block_ui.md` |" if m.stack.has_ui else ""}
"""

    def _module_core(self, folder: str, ext: str, today: str) -> str:
        m = self.manifest
        return f"""# Módulo: Núcleo Transversal (MOD-core)

```yaml
module_id: MOD-core
name: "Infraestructura Transversal y Utilidades"
target_path: "{folder}/core/"
scope: "block_core.md"
owner: "Architecture Team"
version: "1.0.0"
last_updated: "{today}"
```

---

## 1. Propósito y Responsabilidades

Concentra utilidades puras, abstracciones de red, contratos de almacenamiento y logging compartido que cualquier módulo puede consumir.

### Lo que hace
- Cliente HTTP y gestión de reintentos con fallos tipados.
- Contratos de persistencia local y caché.
- Logger estructurado y utilidades universales.

### Lo que NO hace
- No contiene lógica de negocio ni entidades de dominio.
- No contiene componentes gráficos, temas ni widgets.

---

## 2. Contratos y Tipos Públicos (CT-*)

### CT-01: Contrato de Cliente HTTP (`HttpClient`)
- **Símbolo / Archivo:** `{folder}/core/http/http_client.{ext}::HttpClient`
- **Firma:** Expone métodos `get`, `post`, `put`, `delete` devolviendo resultados envueltos en `Result<T, AppError>`.

### CT-02: Contrato de Almacenamiento Local (`StorageContract`)
- **Símbolo / Archivo:** `{folder}/core/storage/storage_contract.{ext}::StorageContract`

---

## 3. Reglas de Negocio e Invariantes (BR-*)

- **BR-01:** Cero excepciones no controladas escapan a capas superiores; todo error se tipa con `AppError`.
- **BR-02:** Los métodos de almacenamiento deben ser idempotentes y con timeouts finitos.

---

## 4. Flujos y Ciclos de Vida

### Flujo de Ejecución Segura con Reintentos
```mermaid
sequenceDiagram
    Caller->>Core: invokeRequest()
    Core->>HTTP: send()
    alt Éxito
        HTTP-->>Caller: Ok(data)
    else Error Transitorio
        Core->>HTTP: retry()
        HTTP-->>Caller: Ok(data)
    else Error Fatal
        HTTP-->>Caller: Err(NetworkError)
    end
```

---

## 5. Mapa de Implementación

| Contrato / Flujo | Símbolo de Código | Ruta en Disco | Pruebas Unitarias |
|---|---|---|---|
| CT-01 | `HttpClient` | `{folder}/core/http/http_client.{ext}` | `test/core/http_client_test.{ext}` |
| CT-02 | `StorageContract` | `{folder}/core/storage/storage_contract.{ext}` | `test/core/storage_test.{ext}` |
"""

    def _module_domain(self, folder: str, ext: str, scope: str, today: str) -> str:
        m = self.manifest
        return f"""# Módulo: {scope.capitalize()} (MOD-{scope})

```yaml
module_id: MOD-{scope}
name: "Dominio y Lógica de Negocio de {scope.capitalize()}"
target_path: "{folder}/{scope}/"
scope: "block_{scope}.md"
owner: "Product Engineering"
version: "1.0.0"
last_updated: "{today}"
```

---

## 1. Propósito y Responsabilidades

Alberga los modelos de dominio, las interfaces de repositorios y los casos de uso que gobiernan las reglas de negocio de `{m.project.name}`.

### Lo que hace
- Modela las entidades inmutables y reglas de validación.
- Define los casos de uso principales.
- Implementa la persistencia desacoplada.

### Lo que NO hace
- No depende de frameworks visuales.
- No almacena secretos ni credenciales en memoria plana.

---

## 2. Contratos y Tipos Públicos (CT-*)

### CT-01: Entidad de Dominio (`{scope.capitalize()}Entity`)
- **Símbolo / Archivo:** `{folder}/{scope}/domain/{scope}_entity.{ext}::{scope.capitalize()}Entity`
- **Invariantes:** Todos sus campos son inmutables (`final` o `readonly`).

### CT-02: Repositorio de Dominio (`{scope.capitalize()}Repository`)
- **Símbolo / Archivo:** `{folder}/{scope}/domain/{scope}_repository.{ext}::{scope.capitalize()}Repository`

---

## 3. Reglas de Negocio e Invariantes (BR-*)

- **BR-01:** La validación de estado debe realizarse en el constructor de la entidad.
- **BR-02:** Los métodos del repositorio deben garantizar transaccionalidad atómica.

---

## 4. Flujos y Ciclos de Vida

### Ciclo de Obtención y Procesamiento
```mermaid
sequenceDiagram
    Caller->>UseCase: execute(input)
    UseCase->>Repository: findById(id)
    Repository-->>UseCase: entity
    UseCase->>Entity: validate()
    UseCase-->>Caller: Result
```

---

## 5. Mapa de Implementación

| Contrato / Flujo | Símbolo de Código | Ruta en Disco | Pruebas Unitarias |
|---|---|---|---|
| CT-01 | `{scope.capitalize()}Entity` | `{folder}/{scope}/domain/{scope}_entity.{ext}` | `test/{scope}/domain_entity_test.{ext}` |
| CT-02 | `{scope.capitalize()}Repository` | `{folder}/{scope}/domain/{scope}_repository.{ext}` | `test/{scope}/repository_test.{ext}` |
"""

    def _module_ui(self, folder: str, ext: str, today: str) -> str:
        return f"""# Módulo: Sistema de Interfaz (MOD-ui)

```yaml
module_id: MOD-ui
name: "Presentación, Navegación y UI Core"
target_path: "{folder}/ui/"
scope: "block_ui.md"
owner: "Design System Team"
version: "1.0.0"
last_updated: "{today}"
```

---

## 1. Propósito y Responsabilidades

Concentra la experiencia gráfica, los componentes reutilizables, el tema y la navegación de la aplicación.

### Lo que hace
- Renderiza vistas respetando tokens de diseño de `tokens.json`.
- Garantiza accesibilidad y navegación por foco (teclado / D-Pad).

### Lo que NO hace
- No contiene lógica de persistencia ni llamadas directas de red.

---

## 2. Contratos y Tipos Públicos (CT-*)

### CT-01: Pantalla Principal (`HomeScreen`)
- **Símbolo / Archivo:** `{folder}/ui/screens/home_screen.{ext}::HomeScreen`

---

## 3. Reglas de Negocio e Invariantes (BR-*)

- **BR-01:** Ningún color o espaciado puede especificarse con literales mágicos; deben usarse tokens.
- **BR-02:** Todo elemento interactivo debe exponer su estado de foco.

---

## 4. Mapa de Implementación

| Contrato / Flujo | Símbolo de Código | Ruta en Disco | Pruebas Unitarias |
|---|---|---|---|
| CT-01 | `HomeScreen` | `{folder}/ui/screens/home_screen.{ext}` | `test/ui/home_screen_test.{ext}` |
"""

    def _initial_proposal(self, month_slug: str, today: str) -> str:
        m = self.manifest
        return f"""# Propuesta de Cambio: Inicialización del Sistema

```yaml
change_id: "{month_slug}-initial-setup"
title: "Configuración e Inicialización Base del Arnés"
module: "MOD-core"
status: CONSOLIDATED
created_at: "{today}"
consolidated_at: "{today}"
author: "bootstrap-harness"
tier: core
```

---

## 1. Motivación y Contexto

Inicialización fundacional del proyecto {m.project.name} con arquitectura OpenSpec y gobernanza determinista.

---

## 2. Delta de Especificación

- **[+] Añadido:** Módulos maestros en `modules/` (`core`, dominio y UI).
- **[+] Añadido:** Verificación determinista y límites de escritura en `scopes/`.
"""

    def _initial_tasks(self) -> str:
        return """# Tareas de Implementación: Inicialización Base

- [x] Generar configuración estructural `harness.config.yaml`.
- [x] Establecer módulos vivos iniciales en `.ai-harness/sdd/modules/`.
- [x] Configurar límites contractuales en `.ai-harness/scopes/`.
- [x] Verificar conformidad con `harness-validator`.
"""
