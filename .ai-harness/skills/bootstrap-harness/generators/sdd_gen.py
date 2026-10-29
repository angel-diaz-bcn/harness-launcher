"""
SDD Generator: Genera la semilla inicial de especificaciones SDD (CMP y PRC)
con frontmatter completo, contratos, historias de usuario y mapas de implementación.
"""

from __future__ import annotations

from models import BootstrapManifest, StackType


class SDDGenerator:
    """Genera especificaciones iniciales en .ai-harness/sdd/."""

    def __init__(self, manifest: BootstrapManifest) -> None:
        self.manifest = manifest

    def generate_all(self) -> dict[str, str]:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"
        ext = "dart" if is_flutter else "ts" if m.stack.stack_type == StackType.NODE else "py"

        first_scope = m.scopes[0].name if m.scopes else "core"

        specs: dict[str, str] = {
            f"1_COMPONENTS/bootstrap/CMP-00-app-bootstrap/CMP-00-app-bootstrap.spec.md": self._cmp_00(folder, ext),
            f"1_COMPONENTS/domain/CMP-01-{first_scope}-contract/CMP-01-{first_scope}-contract.spec.md": self._cmp_01(folder, ext, first_scope),
            f"1_COMPONENTS/domain/CMP-02-{first_scope}-repository/CMP-02-{first_scope}-repository.spec.md": self._cmp_02(folder, ext, first_scope),
            f"1_COMPONENTS/ui/CMP-03-home-screen/CMP-03-home-screen.spec.md": self._cmp_03(folder, ext),
            f"2_PROCESSES/app/PRC-01-app-startup/PRC-01-app-startup.spec.md": self._prc_01(),
        }
        return specs

    def _cmp_00(self, folder: str, ext: str) -> str:
        m = self.manifest
        return f"""---
spec_id: CMP-00
spec_type: component
name: app-bootstrap
target: {folder}/app/bootstrap.{ext}
block: 1_COMPONENTS
status: approved
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-10-29
approved_at: 2026-10-29
approved_by: arquitecto
supersedes: null
superseded_by: null
user_story: Como usuario, quiero que {m.identity.name} arranque de forma rápida, segura y resiliente.
---

# CMP-00 — Inicialización y Bootstrap del Sistema

Define la secuencia de arranque, inyección de dependencias transversal y verificación de integridad previa a la UI.

---

## 1. Contrato de Arranque

- Carga de variables de entorno y configuración desde `harness.config.yaml`.
- Inicialización del servicio de logging y telemetría local.
- Apertura del motor de persistencia ({m.architecture.persistence}).
- Manejo de fallos tempranos de inicio con pantalla de error controlada.

---

## 2. Criterios de Aceptación

1. Si la configuración es válida, el proceso de bootstrap no debe tardar más de 300 ms en entornos locales.
2. Si falla la persistencia, se muestra una alerta técnica y se registra en log estructurado sin crash abrupto.
3. El resultado del bootstrap produce una instancia inmutable de configuración lista para inyectar en la raíz de la app.

---

## Mapa de implementación

- [ ] `{folder}/app/bootstrap.{ext}` — Orquestador de dependencias y arranque.
- [ ] `{folder}/core/config/app_config.{ext}` — Modelo inmutable de configuración del sistema.
"""

    def _cmp_01(self, folder: str, ext: str, scope: str) -> str:
        m = self.manifest
        return f"""---
spec_id: CMP-01
spec_type: component
name: {scope}-contracts
target: {folder}/features/{scope}/domain/contracts.{ext}
block: 1_COMPONENTS
status: approved
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-10-29
approved_at: 2026-10-29
approved_by: arquitecto
supersedes: null
superseded_by: null
user_story: Como desarrollador, quiero contratos de dominio tipados e inmutables para desacoplar la lógica de {scope}.
---

# CMP-01 — Contratos de Dominio y Entidades de {scope.capitalize()}

Define las entidades inmutables y las interfaces del dominio para el módulo `{scope}`.

---

## 1. Entidades del Dominio

- Las entidades no contienen llamadas de red ni dependencias de base de datos.
- Todos los atributos son obligatorios y tipados.
- Se definen métodos puros para cálculos y transformaciones de negocio.

---

## 2. Criterios de Aceptación

1. Las entidades deben ser serializables y deserializables sin pérdida de precisión.
2. Cualquier intento de crear una entidad con datos inválidos genera un error de validación tipado.

---

## Mapa de implementación

- [ ] `{folder}/features/{scope}/domain/entities.{ext}` — Definición de entidades inmutables.
- [ ] `{folder}/features/{scope}/domain/contracts.{ext}` — Interfaces de repositorio y casos de uso.
"""

    def _cmp_02(self, folder: str, ext: str, scope: str) -> str:
        m = self.manifest
        return f"""---
spec_id: CMP-02
spec_type: component
name: {scope}-repository
target: {folder}/features/{scope}/data/{scope}_repository.{ext}
block: 1_COMPONENTS
status: approved
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-10-29
approved_at: 2026-10-29
approved_by: arquitecto
supersedes: null
superseded_by: null
user_story: Como caso de uso, quiero acceder a datos de {scope} de forma abstracta e independientemente del almacenamiento.
---

# CMP-02 — Implementación de Repositorio de {scope.capitalize()}

Implementa el contrato de acceso a datos y persistencia ({m.architecture.persistence}) para `{scope}`.

---

## 1. Responsabilidades

- Traducir DTOs de persistencia a entidades de dominio inmutables.
- Gestionar caché en memoria o disco según el modelo offline-first.
- Manejar excepciones de almacenamiento y convertirlas en `Failure` tipados.

---

## 2. Criterios de Aceptación

1. El repositorio implementa fielmente la interfaz definida en `CMP-01`.
2. Las operaciones asíncronas se ejecutan sin bloquear el hilo principal.

---

## Mapa de implementación

- [ ] `{folder}/features/{scope}/data/{scope}_repository.{ext}` — Implementación del repositorio.
"""

    def _cmp_03(self, folder: str, ext: str) -> str:
        m = self.manifest
        return f"""---
spec_id: CMP-03
spec_type: component
name: home-screen
target: {folder}/features/ui/presentation/home_screen.{ext}
block: 1_COMPONENTS
status: approved
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-10-29
approved_at: 2026-10-29
approved_by: arquitecto
supersedes: null
superseded_by: null
user_story: Como usuario, quiero acceder a la pantalla principal para navegar fluidamente por {m.identity.name}.
---

# CMP-03 — Pantalla Principal e Interfaz de Inicio

Especificación de la vista principal conforme a `design-system/05-pages.md`.

---

## 1. Requisitos de UI y Foco

- Consume estrictamente los tokens de color y espaciado de `design-system/tokens.json`.
- Foco inicial en el primer elemento interactivo de la vista.
- Navegación completa por teclado (Tab / Flechas / Enter) y D-Pad.

---

## 2. Criterios de Aceptación

1. Sin valores visuales literales en el código.
2. Soporte para estados `Loading`, `Success` y `Error`.

---

## Mapa de implementación

- [ ] `{folder}/features/ui/presentation/home_screen.{ext}` — Vista principal.
"""

    def _prc_01(self) -> str:
        m = self.manifest
        return f"""---
spec_id: PRC-01
spec_type: process
name: app-startup-flow
target: docs/flows/startup_flow.md
block: 2_PROCESSES
status: approved
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-10-29
approved_at: 2026-10-29
approved_by: arquitecto
supersedes: null
superseded_by: null
user_story: Como sistema, quiero coordinar el flujo de arranque desde el inicio del proceso hasta la primera interacción del usuario.
---

# PRC-01 — Proceso de Arranque y Coordinación Inicial

Define la secuencia temporal y el flujo de control durante el inicio de {m.identity.name}.

---

## 1. Secuencia de Arranque

```
Usuario / SO          Bootstrap (CMP-00)       Persistencia        UI (CMP-03)
     │                        │                     │                  │
     ├── Iniciar proceso ────▶│                     │                  │
     │                        ├── Validar config ──▶│                  │
     │                        ├── Abrir DB ────────▶│                  │
     │                        │◀── DB lista ────────┤                  │
     │                        │                                        │
     │                        ├── Inyectar dependencias y renderizar ─▶│
     │                        │                                        │◀── Renderizar Home
     │◀───────────────────────┴────────────────────────────────────────┤
```

---

## 2. Criterios de Aceptación del Proceso

1. Si no hay conexión de red, la app arranca en modo offline utilizando la caché local.
2. Si el proceso de inicialización se interrumpe, se liberan los recursos abiertos.

---

## Mapa de implementación

- [ ] `docs/flows/startup_flow.md` — Diagrama de estados y secuencia documentado.
"""

