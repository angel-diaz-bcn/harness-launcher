"""
Memory Generator: Genera la memoria preventiva, catálogo exhaustivo de modos de fallo con anti-patrones
(Código incorrecto de IA vs Código canónico esperado) y ADRs técnicos con trade-offs completos.
"""

from __future__ import annotations

from models import BootstrapManifest


class MemoryGenerator:
    """Genera .ai-harness/memory/ con catálogo de fallos y ADRs exhaustivos."""

    def __init__(self, manifest: BootstrapManifest) -> None:
        self.manifest = manifest

    def generate_all(self) -> dict[str, str]:
        files: dict[str, str] = {
            "failure_modes.md": self._failure_modes(),
            "decisions/README.md": self._decisions_readme(),
            "decisions/ADR-0001-stack-base.md": self._adr_0001(),
            "decisions/ADR-0002-clean-architecture.md": self._adr_0002(),
            "decisions/ADR-0003-persistence-strategy.md": self._adr_0003(),
            "ephemeral_feedback/README.md": self._ephemeral_readme(),
        }
        return files

    def _decisions_readme(self) -> str:
        return """# Decisiones de arquitectura (ADR)

Cada decisión estructural relevante se registra aquí como un documento corto, inmutable y numerado.

## Convención

```
decisions/
├── README.md
├── ADR-0001-<slug>.md
├── ADR-0002-<slug>.md
└── ADR-0003-<slug>.md
```

## Reglas

- Un ADR describe Contexto, Decisión, Consecuencias positivas y negativas, y Alternativas descartadas.
- Un ADR no se reescribe: si la decisión cambia, se crea otro ADR que la reemplaza formalmente.
"""

    def _ephemeral_readme(self) -> str:
        return """# Ephemeral Feedback

Directorio para almacenar logs temporales de ejecución y fallos de validación.
Estos archivos no forman parte de la arquitectura del producto ni se commitean.
"""

    def _failure_modes(self) -> str:
        m = self.manifest
        items = []

        # Catálogo canónico de fallos de alta densidad con anti-patrones de código
        detailed_modes = [
            (
                "FM-001",
                "Violación de Tokens de Diseño con Estilos Literales",
                "Colores HEX, constantes o dimensiones numéricas directas en componentes de UI.",
                "La IA tiende a generar código rápido inventando `#2563EB`, `Colors.blue` o márgenes mágicos `padding: 14` sin consultar `design-system/tokens.json`.",
                """// ❌ INCORRECTO (Antipatrón típico de IA):
Container(
  color: Color(0xFF1E40AF), // HEX literal prohibido
  padding: EdgeInsets.all(12), // Dimensión mágica
)

// ✅ CORRECTO (Canónico):
Container(
  color: theme.colors.brand.primary, // Consumo semántico de token
  padding: EdgeInsets.all(theme.spacing.md),
)""",
                "El check 04_ui_tokens de `preflight` rastrea expresiones regulares de color y bloquea el commit con código de error."
            ),
            (
                "FM-002",
                "Código de Producción sin Spec Aprobada (Bypass de SDD)",
                "Creación o edición de archivos en `lib/` o `src/` sin una spec `.spec.md` en estado `APPROVED`.",
                "La IA asume requerimientos o intenta programar directamente sin pasar por el ciclo SDD-First.",
                """// ❌ INCORRECTO:
// Escribir src/feature/service.py sin spec previa en .ai-harness/sdd/

// ✅ CORRECTO:
// 1. Ejecutar /create-component-sdd.md
// 2. Redactar FR-*, CT-*, TC-* y mapa de implementación
// 3. Pasar a status: APPROVED
// 4. Implementar en src/feature/service.py""",
                "El validador `sync-sdd` y `harness-validator` reportan error fatal ante código no referenciado en una spec aprobada."
            ),
            (
                "FM-003",
                "Fugas de Tipado Dinámico o Genérico en Contratos",
                "Uso de `dynamic`, `any` o tipos comodín en entidades y contratos de dominio.",
                "La IA relaja los tipos para evitar errores inmediatos de compilación o para no definir clases inmutables.",
                """// ❌ INCORRECTO:
Map<String, dynamic> fetchUserData();
def process_data(data: Any) -> Any:

// ✅ CORRECTO:
UserEntity fetchUserData();
def process_data(data: ImmutableRequestModel) -> DomainResult:""",
                "El check 02_contracts de `preflight` analiza el AST del código y rechaza tipos no seguros."
            ),
            (
                "FM-004",
                "Captura Silenciosa de Errores y Excepciones Huérfanas",
                "Bloques `try/catch` vacíos o con logging informal (`print` / `console.log`) que ocultan fallos de runtime.",
                "La IA intenta que una función no arroje error a toda costa, dejando la aplicación en un estado zombi inconsistente.",
                """// ❌ INCORRECTO:
try:
    repository.save(item)
except Exception:
    pass # Silenciar fallo

// ✅ CORRECTO:
try:
    repository.save(item)
except StorageAccessException as err:
    logger.error("Error guardando item %s: %s", item.id, err)
    return Failure.storageFailure(err)""",
                "El linter de `preflight` detecta bloques catch sin manejo y prohíbe llamadas a `print()`."
            ),
            (
                "FM-005",
                "Invasión de Fronteras e Importación Interna entre Módulos",
                "Una feature importa submódulos privados de otra feature (ej. `import features/auth/data/auth_datasource.dart`).",
                "La IA busca reutilizar una función o clase existente sin respetar el desacoplamiento vertical.",
                """// ❌ INCORRECTO:
import 'features/billing/data/billing_dao.dart'; // Acoplamiento a capa privada

// ✅ CORRECTO:
import 'features/billing/public/billing_contracts.dart'; // API pública autorizada""",
                "El check 01_architecture de `preflight` verifica la matriz de imports entre carpetas de features."
            ),
        ]

        for fmid, title, symptom, root_cause, code_sample, mitigation in detailed_modes:
            items.append(f"""## {fmid}: {title}

- **Síntoma observable:** {symptom}
- **Causa raíz técnica (trampa típica de IA):** {root_cause}

### Ejemplo de Anti-patrón vs Patrón Canónico
```
{code_sample}
```

- **Mitigación obligatoria y verificación:** {mitigation}
""")

        return f"""# Catálogo de Modos de Fallo — {m.identity.name}

Memoria preventiva de errores, sesgos y asunciones incorrectas que los agentes de IA no deben repetir.
Cada modo de fallo documenta la causa raíz técnica, el contraste de código y el guardarraíl de verificación.

---

{chr(10).join(items)}
"""

    def _adr_0001(self) -> str:
        m = self.manifest
        return f"""# ADR-0001: Elección de Stack Base ({m.stack.language} / {m.stack.framework})

- **Estado:** Aceptada
- **Fecha:** Inicialización del proyecto
- **Decisores:** Equipo de arquitectura

## Contexto
Para construir {m.identity.name} ({m.identity.description}), orientada a {m.identity.target_audience}, se requiere un stack tecnológico que ofrezca alto rendimiento, tipado estricto en tiempo de compilación y soporte determinista para las plataformas objetivo ({', '.join(m.platform.platforms)}).

## Decisión
Adoptar **{m.stack.language}** con el framework **{m.stack.framework}** y gestor de dependencias `{m.stack.package_manager}`.

## Alternativas consideradas
1. **Solución basada en scripts dinámicos:** Descartada por carecer de verificación de tipos robusta para arquitecturas guiadas por contratos.
2. **Frameworks multiplataforma pesados:** Descartados por sobrecarga de runtime o telemetría embebida.

## Consecuencias
- **Positivas:** Compilación optimizada, tooling moderno, fuerte ecosistema y soporte para desarrollo guiado por contratos SDD.
- **Negativas:** Se exige cumplimiento estricto del linter y verificación en `preflight` para evitar malas prácticas del lenguaje.
"""

    def _adr_0002(self) -> str:
        m = self.manifest
        return f"""# ADR-0002: Adopción de {m.architecture.style} y Aislamiento Modular

- **Estado:** Aceptada
- **Fecha:** Inicialización del proyecto
- **Decisores:** Equipo de arquitectura

## Contexto
El sistema crecerá modularmente con múltiples bloques funcionales ({', '.join([s.name for s in m.scopes])}). Permitir que la presentación acceda directamente a bases de datos o que las entidades dependan de librerías visuales genera deuda técnica insostenible y acoplamiento severo ante modificaciones de agentes de IA.

## Decisión
Implementar **{m.architecture.style}** estricta:
1. El dominio es puro, inmutable y no depende de frameworks externos ni de almacenamiento físico.
2. La infraestructura implementa interfaces definidas en el dominio.
3. Las features no importan código interno de otras features; toda comunicación es por contratos de API pública.

## Consecuencias
- **Positivas:** Testabilidad del 100 % del dominio sin mocks complejos, aislamiento ante cambios de librerías y menor propensión a errores de agentes de IA.
- **Negativas:** Mayor número inicial de archivos y necesidad de mapear DTOs a entidades inmutables.
"""

    def _adr_0003(self) -> str:
        m = self.manifest
        return f"""# ADR-0003: Estrategia de Persistencia y Caché ({m.architecture.persistence})

- **Estado:** Aceptada
- **Fecha:** Inicialización del proyecto
- **Decisores:** Equipo de arquitectura

## Contexto
{m.identity.name} requiere una estrategia de almacenamiento de datos conforme a su modelo de persistencia: `{m.architecture.persistence}`. Debe garantizarse atomicidad, velocidad de lectura en frío (< 50 ms) y cero fugas de descriptores.

## Decisión
Adoptar almacenamiento desacoplado mediante el patrón Repository:
- Las entidades de negocio se persisten a través de contratos de repositorio tipados.
- Si es almacenamiento local ({m.architecture.persistence}), se prioriza la consistencia y la velocidad de consulta en disco.
- Se aísla el motor de persistencia dentro de la capa `data/` del módulo correspondiente.

## Consecuencias
- **Positivas:** Capacidad de sustituir o actualizar el motor de base de datos sin tocar la lógica de negocio.
- **Negativas:** Se deben mantener migraciones de esquema versionadas y tests de integración con bases de datos en memoria.
"""
