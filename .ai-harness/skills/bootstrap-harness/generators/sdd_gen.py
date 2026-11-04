"""
SDD Generator: Genera la semilla inicial de especificaciones SDD (CMP y PRC)
con frontmatter completo, contratos, historias de usuario y mapas de implementación,
siguiendo estrictamente las plantillas canónicas TEMPLATE_COMPONENT_SDD y TEMPLATE_PROCESS_SDD.
"""

from __future__ import annotations

from models import BootstrapManifest, StackType


class SDDGenerator:
    """Genera especificaciones iniciales completas y canónicas en .ai-harness/sdd/."""

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
            f"1_COMPONENTS/bootstrap/CMP-00-app-bootstrap/user_story.md": self._story_cmp_00(),
            f"1_COMPONENTS/domain/CMP-01-{first_scope}-contract/CMP-01-{first_scope}-contract.spec.md": self._cmp_01(folder, ext, first_scope),
            f"1_COMPONENTS/domain/CMP-01-{first_scope}-contract/user_story.md": self._story_cmp_01(first_scope),
            f"1_COMPONENTS/domain/CMP-02-{first_scope}-repository/CMP-02-{first_scope}-repository.spec.md": self._cmp_02(folder, ext, first_scope),
            f"1_COMPONENTS/domain/CMP-02-{first_scope}-repository/user_story.md": self._story_cmp_02(first_scope),
            f"1_COMPONENTS/ui/CMP-03-home-screen/CMP-03-home-screen.spec.md": self._cmp_03(folder, ext),
            f"1_COMPONENTS/ui/CMP-03-home-screen/user_story.md": self._story_cmp_03(),
            f"2_PROCESSES/app/PRC-01-app-startup/PRC-01-app-startup.spec.md": self._prc_01(),
            f"2_PROCESSES/app/PRC-01-app-startup/user_story.md": self._story_prc_01(),
        }
        return specs

    def _story_cmp_00(self) -> str:
        m = self.manifest
        return f"""# Inicialización y Bootstrap del Sistema — Historia de Usuario

## Resumen Ejecutivo

Garantiza que la aplicación arranque de forma determinista, resiliente y ordenada antes de transferir el control a la interfaz gráfica de usuario.

---

## 1. Problema

El inicio del sistema requiere coordinar la lectura de variables de entorno, la inicialización del motor de persistencia ({m.architecture.persistence}), y el registro del árbol de dependencias transversal. Si alguno de estos pasos falla de manera incontrolada, la app puede quedar en un estado zombi, pantalla negra o sufrir un crash abrupto sin diagnóstico.

---

## 2. Actores

- **Actor primario:** Usuario final (experimenta un inicio ágil y una transición fluida hacia la vista inicial).
- **Actor secundario:** Desarrollador / Sistema (obtiene inyección de dependencias transversal desacoplada y trazabilidad en logs).

---

## 3. Historia de Usuario

> **Como** usuario de {m.identity.name},  
> **quiero** iniciar la aplicación de forma inmediata y confiable,  
> **para** disponer de todas las funcionalidades del sistema listas sin retrasos perceptibles ni inconsistencias.

---

## 4. Criterios de Aceptación (BDD)

### Escenario 1: Arranque normal y exitoso
- **Dado** un entorno configurado con parámetros válidos en `harness.config.yaml`,
- **Cuando** se ejecuta la inicialización del bootstrap,
- **Entonces** el motor de persistencia queda abierto, las dependencias transversales quedan registradas y la configuración inmutable queda disponible en menos de 300 ms.

### Escenario 2: Falla de inicialización de persistencia
- **Dado** un entorno donde el archivo de datos local o almacenamiento está bloqueado o inaccesible,
- **Cuando** se ejecuta la inicialización del bootstrap,
- **Entonces** el sistema captura el error en un `BootstrapFailure`, emite un log estructurado y expone un estado degradado seguro sin crashear.

---

## 5. Fuera de Alcance

- Renderizado de componentes visuales finales o animaciones de navegación (responsabilidad de `CMP-03`).
- Lógica de autenticación o llamadas de sincronización remota inicial.
"""

    def _story_cmp_01(self, scope: str) -> str:
        m = self.manifest
        return f"""# Contratos de Dominio para {scope.capitalize()} — Historia de Usuario

## Resumen Ejecutivo

Proporciona las definiciones inmutables de tipos, entidades y fronteras del módulo `{scope}`, garantizando la regla de oro: la lógica de negocio no depende de infraestructura ni de frameworks de UI.

---

## 1. Problema

El código de negocio a menudo se contamina con librerías externas de base de datos, serializadores de terceros o widgets visuales, haciendo que los tests unitarios sean lentos o requieran mocks complejos de frameworks.

---

## 2. Actores

- **Actor primario:** Desarrollador del módulo `{scope}` (dispone de modelos limpios, autocontenidos y fuertemente tipados).
- **Actor secundario:** Arquitectura del sistema (verifica que se cumplan las fronteras de aislamiento funcional).

---

## 3. Historia de Usuario

> **Como** desarrollador de {m.identity.name},  
> **quiero** definir entidades y contratos puros para `{scope}`,  
> **para** garantizar la integridad de las reglas de negocio, desacoplar la persistencia y permitir pruebas unitarias sin dependencias externas.

---

## 4. Criterios de Aceptación (BDD)

### Escenario 1: Validación e inmutabilidad de la entidad
- **Dado** un conjunto de datos válido para instanciar una entidad de `{scope}`,
- **Cuando** se construye la entidad,
- **Entonces** todos los atributos son inmutables y accesibles mediante getters tipados.

### Escenario 2: Rechazo de datos inconsistentes
- **Dado** un conjunto de datos con identificador vacío o valores de negocio fuera de rango,
- **Cuando** se intenta instanciar la entidad o llamar a su validación,
- **Entonces** se produce un `ValidationFailure` tipado sin generar efectos secundarios.

---

## 5. Fuera de Alcance

- Acceso a base de datos, archivos locales o APIs de red (responsabilidad de `CMP-02`).
- Transformaciones visuales o binding a widgets de interfaz.
"""

    def _story_cmp_02(self, scope: str) -> str:
        m = self.manifest
        return f"""# Repositorio de Datos de {scope.capitalize()} — Historia de Usuario

## Resumen Ejecutivo

Implementa el acceso a datos local y remoto para `{scope}`, abstrayendo el motor de persistencia ({m.architecture.persistence}) y proveyendo un mapeo determinista hacia las entidades de dominio.

---

## 1. Problema

El almacenamiento persistente ({m.architecture.persistence}) puede fallar, estar corrupto o sufrir latencia de E/S. Si la capa de dominio o presentación interactúa directamente con el almacenamiento, los fallos de I/O se propagan por toda la arquitectura.

---

## 2. Actores

- **Actor primario:** Desarrollador de casos de uso (consume el contrato de repositorio sin conocer la base de datos subyacente).
- **Actor secundario:** Usuario final (obtiene persistencia fiable de sus datos sin pérdida de información).

---

## 3. Historia de Usuario

> **Como** desarrollador de casos de uso en {m.identity.name},  
> **quiero** interactuar con la abstracción del repositorio de `{scope}`,  
> **para** guardar, recuperar y consultar datos de forma asíncrona y segura sin acoplarme al motor de persistencia real.

---

## 4. Criterios de Aceptación (BDD)

### Escenario 1: Lectura y deserialización exitosa
- **Dado** un registro existente en el almacenamiento local para `{scope}`,
- **Cuando** se invoca el método de búsqueda por identificador del repositorio,
- **Entonces** el repositorio lee el DTO subyacente, lo convierte a la entidad pura de dominio y la retorna en tiempo < 50 ms.

### Escenario 2: Manejo de entidad no encontrada o fallo de persistencia
- **Dado** un identificador inexistente o un fallo de lectura en el medio de almacenamiento,
- **Cuando** se ejecuta la consulta,
- **Entonces** el repositorio retorna un resultado explícito tipado (`Failure` / `None`), evitando lanzar excepciones descontroladas.

---

## 5. Fuera de Alcance

- Reglas de validación intrínsecas de las entidades (responsabilidad de `CMP-01`).
- Componentes de presentación visual.
"""

    def _story_cmp_03(self) -> str:
        m = self.manifest
        return f"""# Pantalla Principal e Interfaz de Inicio — Historia de Usuario

## Resumen Ejecutivo

Presenta la interfaz principal de {m.identity.name}, asegurando navegación accesible por teclado / D-Pad y estricta adherencia a los tokens del sistema de diseño.

---

## 1. Problema

Las interfaces gráficas frecuentemente sufren de falta de accesibilidad por teclado, saltos visuales o inconsistencias de estilo si los desarrolladores usan colores o tipografías literales en lugar de un sistema unificado de tokens.

---

## 2. Actores

- **Actor primario:** Usuario final (interactúa con la pantalla mediante ratón, teclado, pantalla táctil o mando D-Pad).
- **Actor secundario:** Diseñador del sistema (garantiza consistencia visual y coherencia con la identidad de marca).

---

## 3. Historia de Usuario

> **Como** usuario final de {m.identity.name},  
> **quiero** una pantalla principal clara, fluida y totalmente navegable por teclado / D-Pad,  
> **para** acceder a las funcionalidades del sistema con una experiencia visual consistente y accesible.

---

## 4. Criterios de Aceptación (BDD)

### Escenario 1: Foco inicial y navegación por teclado
- **Dado** que la pantalla principal ha completado su carga,
- **Cuando** se renderiza la interfaz,
- **Entonces** el foco inicial se ubica en el primer elemento interactivo, permitiendo avanzar mediante tecla `Tab` o `Flecha Abajo` con resaltado visible según tokens.

### Escenario 2: Estados visuales diferenciados (Loading, Error, Content)
- **Dado** que la vista solicita los datos iniciales al módulo correspondiente,
- **Cuando** la operación está en curso, falla o tiene éxito,
- **Entonces** la pantalla muestra el indicador correspondiente usando exclusivamente los tokens de diseño sin parpadeos.

---

## 5. Fuera de Alcance

- Persistencia de datos directa (delegada en `CMP-02`).
- Acceso a APIs de red no mediadas por la arquitectura.
"""

    def _story_prc_01(self) -> str:
        m = self.manifest
        return f"""# Proceso de Arranque y Coordinación Inicial — Historia de Usuario

## Resumen Ejecutivo

Define el pipeline temporal y de coordinación que orquesta la secuencia de inicio de {m.identity.name}: configuración → persistencia → dependencias → interfaz.

---

## 1. Problema

El inicio del software requiere una coreografía precisa. Si los módulos se inician en orden incorrecto (por ejemplo, cargar la UI antes de haber abierto la persistencia o antes de leer las variables de entorno), se generan condiciones de carrera difíciles de diagnosticar.

---

## 2. Actores

- **Actor primario:** Usuario final (percibe un inicio continuo y coherente).
- **Actor secundario:** Sistema / SO (garantiza liberación de recursos y manejo de señales de interrupción).

---

## 3. Historia de Usuario

> **Como** usuario de {m.identity.name},  
> **quiero** que el sistema coordine todas sus capas de forma determinista al arrancar,  
> **para** que la aplicación esté completamente operativa antes de recibir mi primera interacción.

---

## 4. Criterios de Aceptación (BDD)

### Escenario 1: Secuencia de orquestación completa
- **Dado** el lanzamiento del proceso de la aplicación,
- **Cuando** se inicia el pipeline `PRC-01`,
- **Entonces** se ejecuta primero la validación de configuración, luego la persistencia, luego la inyección y finalmente la vista sin saltos.

### Escenario 2: Recuperación ante fallo de un paso crítico
- **Dado** un fallo irrecuperable en la etapa de base de datos durante el inicio,
- **Cuando** el pipeline detecta la excepción,
- **Entonces** interrumpe la transición hacia la UI principal, invoca la rutina de cleanup y presenta una pantalla de diagnóstico controlada.

---

## 5. Fuera de Alcance

- Implementación detallada de los métodos internos de cada componente participante.
"""

    def _cmp_00(self, folder: str, ext: str) -> str:
        m = self.manifest
        first_scope = m.scopes[0].name if m.scopes else "core"
        return f"""# CMP-00 — Inicialización y Bootstrap del Sistema

---
spec_id: CMP-00
spec_type: CMP
layer: bootstrap
name: app-bootstrap
target: {folder}/app/bootstrap.{ext}
block: 1_COMPONENTS
status: APPROVED
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-11-04
approved_at: 2026-11-04
approved_by: arquitecto
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-01]
design_ref: .ai-harness/context/ui-design-system.md
depends_on: []
consumed_by: [CMP-01, CMP-03]
---

`CMP-00` · `v1.0.0` · `1_COMPONENTS` · `{m.stack.language}` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature / Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `1_COMPONENTS` | `{folder}/app/bootstrap.{ext}` |

> [!IMPORTANT]
> **Contrato de lectura rápida.** Esta spec es la fuente de verdad del comportamiento de arranque. El código no puede añadir dependencias ni estados fuera de este documento.

---

## 0. Protocolo de lectura y no invención

Antes de escribir código:
1. Leer completa esta spec y `context/architecture_rules.md`.
2. Implementar únicamente los requisitos `FR-*` y contratos `CT-*`.
3. No inventar campos ni omitir el mapa de implementación §10.
4. Cualquier error en el proceso se canaliza a través de un resultado tipado sin provocar crashes.

---

## 1. Contexto y objetivo

### 1.1 Problema
El sistema necesita inicializar la persistencia ({m.architecture.persistence}), registrar los servicios del núcleo y preparar el entorno de ejecución antes de conceder el foco a la UI.

### 1.2 Objetivo medible
Secuencia de bootstrap completada en menos de 300 ms en entornos locales, entregando un contenedor de dependencias inmutable.

### 1.3 No objetivos
- No gestiona renderizado de vistas finales ni navegación profunda.
- No realiza peticiones de autenticación síncronas de red durante el arranque crítico.

---

## 2. Alcance y límites

**Incluye:**
- Lectura y validación de variables de configuración.
- Inicialización del driver de persistencia ({m.architecture.persistence}).
- Ensamblado del árbol de inyección de dependencias.

**Excluye:**
- Pantallas o componentes de interfaz de usuario de dominio.
- Servicios en segundo plano no requeridos para el primer frame.

**Invariantes aplicables:**
- `INV-BOOTSTRAP-01`: La persistencia debe estar abierta antes de instanciar cualquier repositorio.
- `INV-BOOTSTRAP-02`: Fallos en servicios opcionales no deben abortar el bootstrap.

---

## 3. Actores e historia de usuario

> **Como** usuario de {m.identity.name},  
> **quiero** iniciar la aplicación de forma inmediata y confiable,  
> **para** disponer de todas las funcionalidades del sistema listas sin retrasos.

**Actores secundarios:** Desarrollador, Sistema Operativo.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Carga y validación de la configuración base del sistema | Must | `AC-01` | `BR-01` |
| `FR-02` | Inicialización del motor de persistencia ({m.architecture.persistence}) | Must | `AC-02` | `BR-02` |
| `FR-03` | Registro y ensamblado del contenedor de inyección de dependencias | Must | `AC-03` | `BR-03` |
| `FR-04` | Emisión de diagnóstico estructurado ante fallos tempranos | Should | `AC-04` | `BR-04` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla / invariante | Fuente canónica | Verificación |
|---|---|---|---|
| `BR-01` | Si falta un parámetro obligatorio en la configuración, se aborta con error tipado. | `context/architecture_rules.md` | `TC-01` |
| `BR-02` | La persistencia debe cerrarse ordenadamente si el bootstrap se cancela. | `context/architecture_rules.md` | `TC-02` |
| `BR-03` | El contenedor de dependencias expone solo instancias inmutables o factorías singleton. | `context/coding_standards.md` | `TC-03` |
| `INV-01` | Cero llamadas de red bloqueantes durante el arranque inicial. | `context/architecture_rules.md` | `TC-01` |

---

## 6. Estados, comportamiento y errores

### 6.1 Máquina de estados

```mermaid
stateDiagram-v2
    [*] --> Uninitialized
    Uninitialized --> Configuring: init()
    Configuring --> InitializingPersistence: configValid
    Configuring --> Failed: configInvalid
    InitializingPersistence --> RegisteringServices: dbReady
    InitializingPersistence --> Failed: dbError
    RegisteringServices --> Ready: servicesRegistered
    Failed --> [*]
    Ready --> [*]
```

### 6.2 Tabla de estados

| Estado | Entrada | Salida | UI / efecto observable |
|---|---|---|---|
| `Uninitialized` | Entrada al proceso | Invocación `init()` | Pantalla de splash del SO activa |
| `Configuring` | Lectura de config | Validación | Log de arranque emitido |
| `InitializingPersistence` | Configuración válida | Apertura de almacenamiento | Conexión a {m.architecture.persistence} establecida |
| `RegisteringServices` | Almacenamiento listo | Registro de dependencias | Contenedor transversal ensamblado |
| `Ready` | Dependencias listas | Traspaso a UI | Control transferido a `CMP-03` |
| `Failed` | Excepción no recuperable | Notificación | Pantalla técnica de diagnóstico amigable |

### 6.3 Errores y casos borde

| Código | Condición | Resultado | Recuperable |
|---|---|---|---|
| `ERR_CONFIG_INVALID` | Falta configuración o clave requerida | Retorna `BootstrapFailure.invalidConfig` | No |
| `ERR_STORAGE_LOCKED` | Almacenamiento bloqueado o sin permisos | Retorna `BootstrapFailure.storageLocked` | Sí (reintento) |
| `ERR_CONTAINER_DUPLICATE` | Doble registro en el contenedor | Retorna `BootstrapFailure.serviceDuplicated` | No |

---

## 7. UX/UI y foco

> No aplica (`layer: bootstrap`). La UI es delegada en `CMP-03`.

---

## 8. Contratos de datos (`CT-*`)

### 8.1 Modelos e interfaces

```python
# Símbolo canónico: {folder}/app/bootstrap.{ext}
# Spec: CMP-00
# FR cubiertos: FR-01, FR-02, FR-03

from dataclasses import dataclass
from typing import Protocol, Any

@dataclass(frozen=True)
class AppConfig:
    app_name: str
    environment: str
    debug_mode: bool

@dataclass(frozen=True)
class BootstrapResult:
    is_success: bool
    config: AppConfig | None
    error_message: str | None = None

class BootstrapOrchestrator(Protocol):
    def initialize(self) -> BootstrapResult:
        ...
```

### 8.2 Tabla de campos

| Campo | Tipo | Obligatorio | Restricción | Origen / destino |
|---|---|---|---|---|
| `app_name` | `str` | Sí | No vacío | `harness.config.yaml` |
| `environment` | `str` | Sí | `production` / `staging` / `development` | Variable de entorno |
| `debug_mode` | `bool` | Sí | Booleano determinista | Configuración |

### 8.3 Contratos expuestos

| ID | Símbolo público | Entrada | Salida | Errores |
|---|---|---|---|---|
| `CT-01` | `BootstrapOrchestrator.initialize()` | Ninguna | `BootstrapResult` | `ERR_CONFIG_INVALID`, `ERR_STORAGE_LOCKED` |

---

## 9. Interfaces y dependencias

### 9.1 Dependencias permitidas
- Módulos internos del núcleo (`core/`).
- Driver o adaptador de persistencia configurado ({m.architecture.persistence}).

### 9.2 Dependencias prohibidas
- Widgets o capas visuales de presentación (`features/ui/`).
- SDKs de analítica externa no gobernados.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `{folder}/app/bootstrap.{ext}::BootstrapOrchestrator.initialize` | `TC-01` | Pending |
| `FR-02` | `CT-01` | `{folder}/app/bootstrap.{ext}::init_persistence` | `TC-02` | Pending |
| `FR-03` | `CT-01` | `{folder}/app/bootstrap.{ext}::register_services` | `TC-03` | Pending |
| `FR-04` | `CT-01` | `{folder}/app/bootstrap.{ext}::handle_bootstrap_error` | `TC-04` | Pending |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | Carga de config válida e inválida | Archivo de config mock | Config válida devuelve `is_success=True` |
| `TC-02` | Integration | Conexión con persistencia ({m.architecture.persistence}) | Driver en memoria | Driver inicializado sin excepciones |
| `TC-03` | Unit | Registro íntegro de dependencias | Contenedor mock | Servicios resueltos sin ambigüedad |
| `TC-04` | Unit | Emisión de diagnóstico ante fallo | Config corrupta | Genera `BootstrapResult` con `error_message` |

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-01 @FR-02
Scenario: Inicialización exitosa del sistema
  Given una configuración válida para el entorno
  When se invoca el método initialize de BootstrapOrchestrator
  Then el resultado reporta is_success igual a verdadero
  And el contenedor de dependencias tiene registrados los servicios base

@FR-04
Scenario: Captura de fallo de almacenamiento
  Given un motor de persistencia inaccesible
  When se intenta inicializar el sistema
  Then se produce un BootstrapResult con is_success falso
  And el error contiene un código identificable sin abortar el proceso abruptamente
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` tienen `AC-*`, `TC-*` y entrada en §10.
- [ ] Todos los `CT-*` están tipados y referenciados.
- [ ] Sin tokens visuales hardcodeados.
- [ ] No hay secciones vacías ni placeholders `<...>`.
- [ ] Tests unitarios en verde.
- [ ] Spec en estado `APPROVED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-11-04 | Arquitectura de arranque modular | Resiliencia y desacoplamiento de dependencias | Base transversal | arquitecto |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Se requiere splash nativo extendido? | No | arquitecto | Resuelto por plataforma. |
"""

    def _cmp_01(self, folder: str, ext: str, scope: str) -> str:
        m = self.manifest
        return f"""# CMP-01 — Contratos de Dominio y Entidades de {scope.capitalize()}

---
spec_id: CMP-01
spec_type: CMP
layer: domain
name: {scope}-contracts
target: {folder}/features/{scope}/domain/contracts.{ext}
block: 1_COMPONENTS
status: APPROVED
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-11-04
approved_at: 2026-11-04
approved_by: arquitecto
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-01]
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-00]
consumed_by: [CMP-02, CMP-03]
---

`CMP-01` · `v1.0.0` · `1_COMPONENTS` · `{m.stack.language}` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature / Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `1_COMPONENTS` | `{folder}/features/{scope}/domain/contracts.{ext}` |

> [!IMPORTANT]
> **Contrato inmutable de dominio.** No contiene llamadas a infraestructura, red ni bibliotecas de persistencia o UI.

---

## 0. Protocolo de lectura y no invención

1. Leer esta spec y las reglas de arquitectura en `context/architecture_rules.md`.
2. Implementar los modelos inmutables y la interfaz abstracta del repositorio.
3. No inventar campos fuera de la tabla §8.2.

---

## 1. Contexto y objetivo

### 1.1 Problema
La lógica central de `{scope}` requiere operar con tipos puros, inmutables y verificables, inmunes a cambios de proveedores de datos o de UI.

### 1.2 Objetivo medible
Modelos serializables con 100% de cobertura en pruebas de validación de invariantes.

### 1.3 No objetivos
- No interactúa directamente con APIs ni con la base de datos.
- No contiene elementos de presentación visual.

---

## 2. Alcance y límites

**Incluye:**
- Definición de entidades de `{scope}` inmutables.
- Definición del contrato de interfaz abstracta del repositorio.
- Reglas de validación y fallos tipados de dominio.

**Excluye:**
- Implementación de almacenamiento (responsabilidad de `CMP-02`).

---

## 3. Actores e historia de usuario

> **Como** desarrollador de {m.identity.name},  
> **quiero** definir entidades y contratos puros para `{scope}`,  
> **para** garantizar la integridad de las reglas de negocio y desacoplar la persistencia.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Estructura inmutable de la entidad principal de `{scope}` | Must | `AC-01` | `BR-01` |
| `FR-02` | Definición de interfaz de repositorio para `{scope}` | Must | `AC-02` | `BR-02` |
| `FR-03` | Catálogo de fallos de dominio tipados | Must | `AC-03` | `BR-03` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla / invariante | Fuente canónica | Verificación |
|---|---|---|---|
| `BR-01` | Las entidades no pueden tener identificador nulo o vacío. | `context/architecture_rules.md` | `TC-01` |
| `BR-02` | Los contratos de dominio no admiten tipos de librerías de UI o BD. | `context/architecture_rules.md` | `TC-02` |
| `INV-01` | Todo modelo de dominio es inmutable una vez instanciado. | `context/coding_standards.md` | `TC-01` |

---

## 6. Estados, comportamiento y errores

### 6.1 Máquina de estados

```mermaid
stateDiagram-v2
    [*] --> Validating
    Validating --> Valid: datosCorrectos
    Validating --> Invalid: falloInvariante
    Valid --> [*]
    Invalid --> [*]
```

### 6.2 Tabla de estados

| Estado | Entrada | Salida | UI / efecto observable |
|---|---|---|---|
| `Validating` | Datos de entrada | Ejecución de validadores | Verificación en memoria |
| `Valid` | Parámetros conformes | Creación de entidad | Objeto inmutable retornado |
| `Invalid` | Datos no conformes | Retorno de error tipado | Excepción de dominio controlada |

### 6.3 Errores y casos borde

| Código | Condición | Resultado | Recuperable |
|---|---|---|---|
| `ERR_EMPTY_ID` | Identificador vacío | `DomainFailure.emptyId` | No |
| `ERR_INVALID_DATA` | Campos fuera de especificación | `DomainFailure.invalidData` | No |

---

## 7. UX/UI y foco

> No aplica (`layer: domain`).

---

## 8. Contratos de datos (`CT-*`)

### 8.1 Modelos e interfaces

```python
# Símbolo canónico: {folder}/features/{scope}/domain/contracts.{ext}
# Spec: CMP-01
# FR cubiertos: FR-01, FR-02, FR-03

from dataclasses import dataclass
from typing import Protocol, Optional, Sequence

@dataclass(frozen=True)
class {scope.capitalize()}Entity:
    id: str
    name: str
    is_active: bool

class {scope.capitalize()}RepositoryContract(Protocol):
    def get_by_id(self, item_id: str) -> Optional[{scope.capitalize()}Entity]:
        ...
    def list_all(self) -> Sequence[{scope.capitalize()}Entity]:
        ...
```

### 8.2 Tabla de campos

| Campo | Tipo | Obligatorio | Restricción | Origen / destino |
|---|---|---|---|---|
| `id` | `str` | Sí | No vacío, formato alfanumérico | Almacenamiento |
| `name` | `str` | Sí | Longitud 1..100 caracteres | Entrada de usuario / BD |
| `is_active` | `bool` | Sí | Booleano | Estado del sistema |

### 8.3 Contratos expuestos

| ID | Símbolo público | Entrada | Salida | Errores |
|---|---|---|---|---|
| `CT-01` | `{scope.capitalize()}RepositoryContract.get_by_id` | `item_id: str` | `Optional[{scope.capitalize()}Entity]` | `ERR_EMPTY_ID` |
| `CT-02` | `{scope.capitalize()}RepositoryContract.list_all` | Ninguna | `Sequence[{scope.capitalize()}Entity]` | Ninguno |

---

## 9. Interfaces y dependencias

- **Permitidas:** Librería estándar del lenguaje (`dataclasses`, `typing`, `enum`).
- **Prohibidas:** Cualquier import de base de datos o paquetes de presentación.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `{folder}/features/{scope}/domain/entities.{ext}::{scope.capitalize()}Entity` | `TC-01` | Pending |
| `FR-02` | `CT-01` | `{folder}/features/{scope}/domain/contracts.{ext}::{scope.capitalize()}RepositoryContract` | `TC-02` | Pending |
| `FR-03` | `CT-02` | `{folder}/features/{scope}/domain/failures.{ext}::DomainFailure` | `TC-03` | Pending |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | Inmutabilidad e integridad de `{scope.capitalize()}Entity` | Parámetros válidos | La entidad es inmutable |
| `TC-02` | Unit | Cumplimiento del protocolo de repositorio | Mock del contrato | Tipos verificados estáticamente |
| `TC-03` | Unit | Validación de campos y rechazo de ID vacío | ID = "" | Retorna fallo de validación tipado |

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-01
Scenario: Construcción de entidad válida
  Given un identificador válido y un nombre conforme
  When se crea la instancia de la entidad
  Then la entidad conserva todos sus valores y no permite mutación directa

@FR-03
Scenario: Rechazo de entidad inválida
  Given un identificador vacío
  When se valida la creación de la entidad
  Then se emite un fallo tipado ERR_EMPTY_ID
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` tienen `AC-*`, `TC-*` y entrada en §10.
- [ ] Todos los `CT-*` están tipados.
- [ ] No existen dependencias impuras en la capa de dominio.
- [ ] Spec en estado `APPROVED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-11-04 | Modelos de dominio inmutables | Clean Architecture estricta | Core de `{scope}` | arquitecto |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Requiere soft-delete a nivel de contrato? | No | arquitecto | Se gestiona mediante campo `is_active`. |
"""

    def _cmp_02(self, folder: str, ext: str, scope: str) -> str:
        m = self.manifest
        return f"""# CMP-02 — Implementación de Repositorio de {scope.capitalize()}

---
spec_id: CMP-02
spec_type: CMP
layer: domain
name: {scope}-repository
target: {folder}/features/{scope}/data/{scope}_repository.{ext}
block: 1_COMPONENTS
status: APPROVED
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-11-04
approved_at: 2026-11-04
approved_by: arquitecto
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-01]
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-00, CMP-01]
consumed_by: [CMP-03]
---

`CMP-02` · `v1.0.0` · `1_COMPONENTS` · `{m.stack.language}` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature / Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `1_COMPONENTS` | `{folder}/features/{scope}/data/{scope}_repository.{ext}` |

> [!IMPORTANT]
> **Adaptador de infraestructura.** Conecta el motor de persistencia ({m.architecture.persistence}) con los contratos definidos en `CMP-01`.

---

## 0. Protocolo de lectura y no invención

1. Leer `CMP-01` y respetar fielmente las firmas de `CT-01` y `CT-02`.
2. Encapsular las excepciones del almacenamiento en fallos tipados de repositorio.
3. No invocar APIs visuales ni de presentación.

---

## 1. Contexto y objetivo

### 1.1 Problema
El acceso a datos debe ser fiable, manejar fallos de I/O y mapear estructuras físicas a entidades puras de dominio.

### 1.2 Objetivo medible
Tiempo de recuperación por clave < 50 ms en operaciones locales sin fuga de recursos.

### 1.3 No objetivos
- No define reglas de negocio (responsabilidad de `CMP-01`).
- No interactúa con elementos visuales de la interfaz.

---

## 2. Alcance y límites

**Incluye:**
- Implementación de `{scope.capitalize()}RepositoryContract`.
- Mapeo bidireccional entre DTOs y entidades de dominio.
- Captura y traducción de excepciones de persistencia.

**Excluye:**
- Reglas de validación intrínsecas de las entidades.

---

## 3. Actores e historia de usuario

> **Como** desarrollador de casos de uso en {m.identity.name},  
> **quiero** interactuar con la abstracción del repositorio de `{scope}`,  
> **para** guardar y recuperar datos de forma asíncrona y segura sin acoplarme al motor de base de datos.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Recuperación por identificador según contrato `CMP-01` | Must | `AC-01` | `BR-01` |
| `FR-02` | Listado completo de registros disponibles | Must | `AC-02` | `BR-02` |
| `FR-03` | Manejo y contención de fallos del motor de almacenamiento | Must | `AC-03` | `BR-03` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla / invariante | Fuente canónica | Verificación |
|---|---|---|---|
| `BR-01` | Si el registro no existe, devuelve `None` sin lanzar excepción no capturada. | `CMP-01` | `TC-01` |
| `BR-02` | Las operaciones de almacenamiento no deben bloquear el hilo principal. | `context/architecture_rules.md` | `TC-02` |
| `INV-01` | Todo dato persistido debe pasar por validación de contrato antes de almacenarse. | `CMP-01` | `TC-01` |

---

## 6. Estados, comportamiento y errores

### 6.1 Máquina de estados

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Querying: get_by_id()
    Querying --> DataReady: recordFound
    Querying --> NotFound: noRecord
    Querying --> Failure: storageError
    DataReady --> Idle
    NotFound --> Idle
    Failure --> Idle
```

### 6.2 Tabla de estados

| Estado | Entrada | Salida | UI / efecto observable |
|---|---|---|---|
| `Idle` | Espera de solicitud | Ninguna | En reposo |
| `Querying` | Identificador provisto | Lectura de storage | Operación I/O asíncrona |
| `DataReady` | Registro obtenido | Retorno de entidad | Datos mapeados a dominio |
| `NotFound` | Clave inexistente | Retorno de `None` | Operación completada vacía |
| `Failure` | Fallo de persistencia | Error capturado | Emisión de log estructurado |

### 6.3 Errores y casos borde

| Código | Condición | Resultado | Recuperable |
|---|---|---|---|
| `ERR_STORAGE_READ` | Fallo físico de lectura | Retorna error tipado de almacenamiento | Sí (reintento) |
| `ERR_DESERIALIZATION` | Datos corruptos en almacenamiento | Retorna fallo de datos corruptos | No |

---

## 7. UX/UI y foco

> No aplica (`layer: domain`).

---

## 8. Contratos de datos (`CT-*`)

### 8.1 Modelos e interfaces

```python
# Símbolo canónico: {folder}/features/{scope}/data/{scope}_repository.{ext}
# Spec: CMP-02
# FR cubiertos: FR-01, FR-02, FR-03

from typing import Optional, Sequence, Any
from {folder}.features.{scope}.domain.contracts import {scope.capitalize()}Entity, {scope.capitalize()}RepositoryContract

class {scope.capitalize()}Repository({scope.capitalize()}RepositoryContract):
    def __init__(self, persistence_adapter: Any) -> None:
        self._adapter = persistence_adapter

    def get_by_id(self, item_id: str) -> Optional[{scope.capitalize()}Entity]:
        ...

    def list_all(self) -> Sequence[{scope.capitalize()}Entity]:
        ...
```

### 8.2 Tabla de campos

Mapea directamente contra los campos definidos en `CMP-01` §8.2.

### 8.3 Contratos expuestos

| ID | Símbolo público | Entrada | Salida | Errores |
|---|---|---|---|---|
| `CT-01` | `{scope.capitalize()}Repository.get_by_id` | `item_id: str` | `Optional[{scope.capitalize()}Entity]` | `ERR_STORAGE_READ` |
| `CT-02` | `{scope.capitalize()}Repository.list_all` | Ninguna | `Sequence[{scope.capitalize()}Entity]` | `ERR_STORAGE_READ` |

---

## 9. Interfaces y dependencias

- **Permitidas:** Contratos de dominio de `CMP-01`, motor de persistencia ({m.architecture.persistence}).
- **Prohibidas:** Componentes de presentación visual.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `{folder}/features/{scope}/data/{scope}_repository.{ext}::{scope.capitalize()}Repository.get_by_id` | `TC-01` | Pending |
| `FR-02` | `CT-02` | `{folder}/features/{scope}/data/{scope}_repository.{ext}::{scope.capitalize()}Repository.list_all` | `TC-02` | Pending |
| `FR-03` | `CT-01` | `{folder}/features/{scope}/data/{scope}_repository.{ext}::_handle_storage_error` | `TC-03` | Pending |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | Recuperación exitosa y mapeo a entidad | Base de datos mock con 1 item | Retorna entidad idéntica a los datos de mock |
| `TC-02` | Unit | Búsqueda de elemento no existente | Clave "non-existent" | Retorna `None` |
| `TC-03` | Unit | Resiliencia ante excepción de base de datos | Mock que lanza IOError | Captura y retorna error controlado sin crash |

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-01
Scenario: Consulta de registro existente
  Given un registro con id "ITEM-01" en la persistencia
  When se solicita get_by_id con id "ITEM-01"
  Then el repositorio retorna la entidad correspondiente

@FR-03
Scenario: Manejo de falla de I/O en consulta
  Given una desconexión en el almacenamiento
  When se ejecuta list_all
  Then el repositorio captura la excepción y retorna un fallo controlado
```

---

## 13. Definition of Done

- [ ] Implementación conforme al contrato de `CMP-01`.
- [ ] Pruebas unitarias de repositorio pasando.
- [ ] Sin referencias a UI ni a dependencias no autorizadas.
- [ ] Spec en estado `APPROVED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-11-04 | Uso de persistencia desacoplada ({m.architecture.persistence}) | Facilidad de pruebas unitarias | Capa de datos | arquitecto |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Se requiere caché en memoria de primer nivel? | No | arquitecto | Postergado a optimización futura. |
"""

    def _cmp_03(self, folder: str, ext: str) -> str:
        m = self.manifest
        first_scope = m.scopes[0].name if m.scopes else "core"
        return f"""# CMP-03 — Pantalla Principal e Interfaz de Inicio

---
spec_id: CMP-03
spec_type: CMP
layer: ui
name: home-screen
target: {folder}/features/ui/presentation/home_screen.{ext}
block: 1_COMPONENTS
status: APPROVED
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-11-04
approved_at: 2026-11-04
approved_by: arquitecto
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-01]
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-00, CMP-01, CMP-02]
consumed_by: []
---

`CMP-03` · `v1.0.0` · `1_COMPONENTS` · `{m.stack.language}` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature / Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `1_COMPONENTS` | `{folder}/features/ui/presentation/home_screen.{ext}` |

> [!IMPORTANT]
> **Disciplina visual estricta.** Uso exclusivo de tokens definidos en `design-system/tokens.json`. Prohibido código con colores HEX o márgenes literales.

---

## 0. Protocolo de lectura y no invención

1. Leer `context/ui-design-system.md` y `design-system/tokens.json`.
2. Implementar los requisitos de foco y navegación por teclado / D-Pad.
3. No utilizar valores visuales directos en el código.

---

## 1. Contexto y objetivo

### 1.1 Problema
La pantalla principal debe renderizar el contenido inicial de {m.identity.name} con soporte universal para ratón, teclado y D-Pad, manteniendo coherencia con el sistema de diseño.

### 1.2 Objetivo medible
Navegación 100% operable por teclado con contraste visual de foco conforme a WCAG AA.

### 1.3 No objetivos
- No accede directamente al motor de base de datos (consume `CMP-02`).

---

## 2. Alcance y límites

**Incluye:**
- Estructura visual de la pantalla principal (layout y contenedores).
- Gestión del foco inicial y ciclo de navegación accesible.
- Manejo de estados visuales: cargando, contenido disponible y error.

**Excluye:**
- Lógica de persistencia o llamadas de bajo nivel.

---

## 3. Actores e historia de usuario

> **Como** usuario final de {m.identity.name},  
> **quiero** una pantalla principal clara, fluida y totalmente navegable por teclado / D-Pad,  
> **para** acceder a las funcionalidades del sistema con una experiencia visual consistente y accesible.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Renderizado del layout principal según tokens del sistema de diseño | Must | `AC-01` | `BR-01` |
| `FR-02` | Gestión de foco interactivo accesible por teclado y D-Pad | Must | `AC-02` | `BR-02` |
| `FR-03` | Representación visual diferenciada de estados (Loading, Content, Error) | Must | `AC-03` | `BR-03` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla / invariante | Fuente canónica | Verificación |
|---|---|---|---|
| `BR-01` | Los colores y dimensiones deben consumirse de `tokens.json`. | `design-system/tokens.json` | `TC-01` |
| `BR-02` | El foco inicial se posiciona en el primer elemento interactivo al cargar. | `context/ui-design-system.md` | `TC-02` |
| `INV-01` | Prohibidos los códigos de color hexadecimales literales en el código fuente de UI. | `context/architecture_rules.md` | `TC-01` |

---

## 6. Estados, comportamiento y errores

### 6.1 Máquina de estados

```mermaid
stateDiagram-v2
    [*] --> Loading
    Loading --> Content: dataReceived
    Loading --> ErrorState: fetchError
    Content --> Loading: refresh
    ErrorState --> Loading: retry
```

### 6.2 Tabla de estados

| Estado | Entrada | Salida | UI / efecto observable |
|---|---|---|---|
| `Loading` | Inicio de vista | Petición a dominio en curso | Spinner centrado consumiendo `tokens.colors.brand.primary` |
| `Content` | Datos listos | Visualización | Lista / cuadrícula de elementos interactivos |
| `ErrorState` | Fallo de carga | Visualización de alerta | Mensaje legible y botón con foco en reintentar |

### 6.3 Errores y casos borde

| Código | Condición | Resultado | Recuperable |
|---|---|---|---|
| `UI_NO_DATA` | Lista de datos vacía | Muestra ilustración / mensaje de estado vacío | Sí |
| `UI_FETCH_FAIL` | Fallo en la capa de datos | Presenta mensaje de error con botón de reintento | Sí |

---

## 7. UX/UI y foco (`layer: ui`)

- **Tokens aplicados:**
  - Fondo: `colors.surface.background`
  - Paneles: `colors.surface.panel`
  - Tipografía principal: `colors.text.primary`
  - Indicador de foco: `colors.accent.focus`
- **Jerarquía:** Encabezado con título principal, contenedor de catálogo/items, barra de estado inferior.
- **Foco inicial:** Primer botón o tarjeta de contenido visible.
- **Orden D-Pad / Teclado:**
  - `Flecha Abajo` / `Tab`: Avanzar al siguiente control.
  - `Flecha Arriba` / `Shift+Tab`: Retroceder al control anterior.
  - `Enter` / `Espacio`: Ejecutar acción del control enfocado.
- **Accesibilidad:** Contraste mínimo 4.5:1, etiquetas semánticas en cada control interactivo.

---

## 8. Contratos de datos (`CT-*`)

### 8.1 Modelos e interfaces

```python
# Símbolo canónico: {folder}/features/ui/presentation/home_screen.{ext}
# Spec: CMP-03
# FR cubiertos: FR-01, FR-02, FR-03

from typing import Protocol, Any, Sequence

class HomeScreenPresenter(Protocol):
    def load_initial_data(self) -> None:
        ...
    def on_retry_clicked(self) -> None:
        ...
```

### 8.2 Tabla de campos

| Campo | Tipo | Obligatorio | Restricción | Origen / destino |
|---|---|---|---|---|
| `view_state` | `str` | Sí | `loading`, `content`, `error` | Estado interno del presenter |

### 8.3 Contratos expuestos

| ID | Símbolo público | Entrada | Salida | Errores |
|---|---|---|---|---|
| `CT-01` | `HomeScreenPresenter.load_initial_data` | Ninguna | `None` | Capturados internamente |
| `CT-02` | `HomeScreenPresenter.on_retry_clicked` | Ninguna | `None` | Capturados internamente |

---

## 9. Interfaces y dependencias

- **Permitidas:** Framework de interfaz ({m.stack.framework}), tokens del sistema de diseño, contratos de `CMP-01`.
- **Prohibidas:** Conexiones directas a persistencia o llamadas de red nativas no abstraídas.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `{folder}/features/ui/presentation/home_screen.{ext}::HomeScreenView.build` | `TC-01` | Pending |
| `FR-02` | `CT-01` | `{folder}/features/ui/presentation/home_screen.{ext}::HomeScreenView.setup_focus` | `TC-02` | Pending |
| `FR-03` | `CT-02` | `{folder}/features/ui/presentation/home_screen.{ext}::HomeScreenPresenter.load_initial_data` | `TC-03` | Pending |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | UI / Snapshot | Aplicación estricta de tokens de diseño | Vista renderizada | Sin colores HEX literales en código |
| `TC-02` | UI / Interaction | Comportamiento del foco de teclado | Simulación de teclas Tab y Enter | El foco responde en el orden configurado |
| `TC-03` | Unit | Transiciones de estado del presenter | Simulación de datos / error | Cambia adecuadamente entre Loading, Content y Error |

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-01 @FR-02
Scenario: Renderizado y foco de la vista principal
  Given la aplicación se inicia correctamente
  When se carga la pantalla principal
  Then el primer elemento interactivo tiene el foco asignado
  And los estilos visuales provienen de design-system/tokens.json

@FR-03
Scenario: Transición a pantalla de error y reintento
  Given la capa de datos retorna un fallo en la carga inicial
  When la pantalla procesa la respuesta
  Then se muestra la vista de error
  And el botón reintentar recibe el foco de teclado
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` cuentan con `AC-*`, `TC-*` y entrada en §10.
- [ ] No existen valores literales de color o margen.
- [ ] Foco y navegación accesible verificados.
- [ ] Spec en estado `APPROVED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-11-04 | Disciplina estricta de tokens | Consistencia multiplataforma | UI y presentación | diseñador / arquitecto |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Soporte para modo de alto contraste? | No | diseñador | Se cubre con los tokens semánticos actuales. |
"""

    def _prc_01(self) -> str:
        m = self.manifest
        return f"""# PRC-01 — Proceso de Arranque y Coordinación Inicial

---
spec_id: PRC-01
spec_type: PRC
name: app-startup-flow
target: docs/flows/startup_flow.md
block: 2_PROCESSES
status: APPROVED
version: 1.0.0
owner: arquitecto
last_reviewed: 2026-11-04
approved_at: 2026-11-04
approved_by: arquitecto
supersedes: []
superseded_by: []
user_story: user_story.md
trigger: Lanzamiento del ejecutable de la aplicación
participants: [CMP-00, CMP-01, CMP-02, CMP-03]
depends_on: []
---

`PRC-01` · `v1.0.0` · `2_PROCESSES` · `APPROVED`

| 🔄 Tipo | 🚦 Estado | 🧭 Bloque | 🎬 Disparador |
|---|---|---|---|
| `PRC` | `APPROVED` | `2_PROCESSES` | Lanzamiento del ejecutable de la aplicación |

> [!IMPORTANT]
> **El proceso orquesta, no reimplementa.** Cada paso delega en los componentes participantes (`CMP-00`, `CMP-01`, `CMP-02`, `CMP-03`).

---

## 0. Protocolo de lectura y no invención

1. Leer esta spec y las de los componentes participantes.
2. Implementar los pasos `ST-*` exactamente en el orden de la secuencia declarada.
3. No inventar pasos intermedios ni relajar el control de errores.

---

## 1. Resultado esperado

### 1.1 Objetivo del proceso
Coordinar la inicialización secuencial y controlada de {m.identity.name}, pasando de un proceso recién lanzado por el sistema operativo a una aplicación completamente configurada y con la pantalla principal activa.

### 1.2 Resultado observable
Usuario visualiza la pantalla principal (`CMP-03`) con el foco interactivo inicial asignado y las dependencias preparadas en menos de 500 ms en entorno de desarrollo.

### 1.3 No objetivos
- No implementa la lógica interna de base de datos (delegada en `CMP-02`).
- No contiene código visual (delegado en `CMP-03`).

---

## 2. Disparador y condiciones

| Elemento | Definición |
|---|---|
| Disparador | Ejecución del binario / entrada al método main. |
| Precondiciones | Acceso a sistema de archivos local y permisos de ejecución concedidos. |
| Postcondiciones | `CMP-00` finalizado, persistencia abierta y `CMP-03` renderizado con foco. |
| Cancelación | Si se recibe señal de término temprana (`SIGINT`), se cierran conexiones abiertas. |
| Reintento | Fallos en persistencia se reintentan una vez antes de reportar fallo crítico. |

---

## 3. Alcance y límites

**Incluye:**
- Secuencia de llamadas de orquestación entre `CMP-00`, `CMP-01`, `CMP-02` y `CMP-03`.
- Manejo de excepciones y degradación ante fallo de servicios.

**Excluye:**
- Flujos de autenticación o de negocio posteriores al arranque.

---

## 4. Actores y participantes

| Actor / componente | Rol en el proceso |
|---|---|
| Usuario / Sistema Operativo | Lanza el proceso y provee el contexto de ejecución. |
| `CMP-00` | Ejecuta la inicialización de configuración y registro de servicios. |
| `CMP-01` | Provee contratos y entidades puras de dominio. |
| `CMP-02` | Abre la conexión de datos y prepara el almacenamiento ({m.architecture.persistence}). |
| `CMP-03` | Renderiza la interfaz inicial y captura el foco de teclado. |

---

## 5. Flujo de control

```mermaid
sequenceDiagram
    autonumber
    actor SO as Usuario / SO
    participant B as Bootstrap (CMP-00)
    participant D as Persistencia (CMP-02)
    participant U as UI Home (CMP-03)

    SO->>B: 1. Iniciar ejecutable
    activate B
    B->>B: 2. Cargar configuración base
    B->>D: 3. Inicializar almacenamiento ({m.architecture.persistence})
    activate D
    D-->>B: 4. Almacenamiento listo
    deactivate D
    B->>U: 5. Inyectar dependencias y renderizar Home
    deactivate B
    activate U
    U->>U: 6. Asignar foco interactivo inicial
    U-->>SO: 7. Interfaz operativa
    deactivate U
```

---

## 6. Pasos del proceso (`ST-*`)

| ID | Paso | Responsable | Entrada | Salida | Errores manejados |
|---|---|---|---|---|---|
| `ST-01` | Carga de variables de entorno y configuración | `CMP-00` | Archivos de config | Objeto `AppConfig` inmutable | Configuración ausente o inválida |
| `ST-02` | Inicialización del adaptador de almacenamiento | `CMP-02` | Parámetros de conexión | Almacenamiento abierto | Fallo de permisos o fichero bloqueado |
| `ST-03` | Registro e inyección de servicios | `CMP-00` | Servicios del núcleo | Contenedor transversal | Dependencia duplicada |
| `ST-04` | Presentación del primer frame visual y foco | `CMP-03` | Contenedor listo | Vista con foco | Excepción de renderizado |

---

## 7. Estados, comportamiento y errores

### 7.1 Máquina de estados

```mermaid
stateDiagram-v2
    [*] --> Starting
    Starting --> Configuring: main()
    Configuring --> InitializingData: configOk
    InitializingData --> MountingUI: dbReady
    MountingUI --> Completed: uiFocused
    InitializingData --> Aborted: dbFatalError
    Configuring --> Aborted: configFatalError
    Completed --> [*]
    Aborted --> [*]
```

### 7.2 Errores y recuperación

| Paso | Código de error | Causa | Estrategia de recuperación |
|---|---|---|---|
| `ST-01` | `ERR_STARTUP_CONFIG` | Parámetro obligatorio faltante | Emitir log y mostrar alerta de configuración. |
| `ST-02` | `ERR_STARTUP_STORAGE` | Persistencia inaccesible | Reintentar una vez en modo solo lectura o memoria. |
| `ST-04` | `ERR_STARTUP_UI` | Fallo al montar vista inicial | Fallback a vista mínima de diagnóstico. |

---

## 8. Datos y contratos

- Entrada del proceso: Argumentos de línea de comandos y variables de entorno del sistema.
- Salida del proceso: Estado de la aplicación en ejecución normal con código de salida `0`.

---

## 9. Contratos expuestos (`CT-*`)

| ID | Símbolo público | Entrada | Salida | Errores |
|---|---|---|---|---|
| `CT-01` | `startup_pipeline.execute_startup()` | Ninguna | `bool` | `ERR_STARTUP_CONFIG`, `ERR_STARTUP_STORAGE` |

---

## 10. Invariantes del proceso

- `INV-PRC-01`: Bajo ninguna circunstancia se debe intentar montar la interfaz `CMP-03` si `CMP-00` no completó exitosamente su inicialización.
- `INV-PRC-02`: Toda señal de aborto antes del frame final debe liberar los descriptores de persistencia abiertos.

---

## 11. Mapa de implementación y trazabilidad

| Paso | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `ST-01` | `CT-01` | `docs/flows/startup_flow.md::execute_startup` | `TC-01` | Pending |
| `ST-02` | `CT-01` | `docs/flows/startup_flow.md::init_storage_step` | `TC-02` | Pending |
| `ST-03` | `CT-01` | `docs/flows/startup_flow.md::register_services_step` | `TC-03` | Pending |
| `ST-04` | `CT-01` | `docs/flows/startup_flow.md::render_home_step` | `TC-04` | Pending |

---

## 12. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Integration | Ejecución completa del pipeline en condiciones normales | Entorno mock preparado | `execute_startup()` retorna `True` |
| `TC-02` | Integration | Manejo de fallo en paso `ST-02` (persistencia) | Storage mock con fallo provocado | Pipeline aborta limpiamente sin crash |
| `TC-03` | E2E | Foco asignado tras completar el pipeline | Entorno de prueba UI | Primer elemento de `CMP-03` enfocado |

---

## 13. Criterios de aceptación BDD

```gherkin
@ST-01 @ST-02 @ST-03 @ST-04
Scenario: Arranque exitoso coordinado
  Given un entorno configurado correctamente
  When se ejecuta el proceso de inicio de la aplicación
  Then todos los pasos se ejecutan en orden estricto
  And el sistema culmina con la vista principal activa y enfocada

@ST-02
Scenario: Manejo de falla crítica en paso de almacenamiento
  Given un error irrecuperable en la base de datos
  When se ejecuta el pipeline de inicio
  Then el proceso no monta la interfaz principal de datos
  And se liberan los recursos y se notifica el fallo
```

---

## 14. Definition of Done

- [ ] Todos los pasos `ST-*` cuentan con asignación de componente participante y test `TC-*`.
- [ ] Diagrama de secuencia Mermaid actualizado.
- [ ] Invariantes verificables.
- [ ] Spec en estado `APPROVED`.

---

## 15. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-11-04 | Secuencia síncrona en fase de inicio crítico | Prevenir estados de carrera en UI | Ciclo de vida | arquitecto |

---

## 16. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Requiere pantalla de splash con progreso porcentual? | No | arquitecto | El tiempo es menor a 300 ms, no es necesario. |
"""
