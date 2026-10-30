"""
Memory Generator: Genera la memoria preventiva, modos de fallo y ADRs de arquitectura
con el estándar de calidad y justificación técnica de FLIK.
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

Cada decisión estructural relevante se registra aquí como un documento corto,
inmutable y numerado.

## Convención

```
decisions/
├── README.md
├── ADR-0001-<slug>.md
└── ADR-0002-<slug>.md
```

## Reglas

- Un ADR describe context, decision, consecuencias y alternativas.
- Un ADR no se reescribe: si la decisión cambia, se crea otro ADR que la reemplaza.
"""

    def _ephemeral_readme(self) -> str:
        return """# Ephemeral Feedback

Directorio para almacenar logs temporales de ejecución y fallos de validación.
Estos archivos no forman parte de la arquitectura del producto ni se commitean.
"""

    def _failure_modes(self) -> str:
        m = self.manifest
        items = []
        
        # Garantizar al menos 5 modos de fallo canónicos y formato FM-NNN
        fms = list(m.failure_modes)
        if len(fms) < 5:
            default_extras = [
                ("Violación de Tokens de Diseño", "Colores HEX o dimensiones hardcodeadas en componentes UI.", "La IA genera estilos rápidos sin consultar design-system/tokens.json.", "El validador preflight bloquea cualquier HEX literal. Usar exclusivamente tokens semánticos."),
                ("Código de Producción sin Spec Aprobada", "Creación de archivos en lib/ o src/ sin .spec.md en status: APPROVED.", "Asumir requerimientos informales sin contrato BDD ni trazabilidad.", "Principio SDD-First estricto: toda implementación requiere spec aprobada previa."),
                ("Fugas de Tipado Dinámico o Genérico", "Uso de 'any' o 'dynamic' en modelos y contratos de dominio.", "La IA relaja tipos para evitar errores de compilador inmediatos.", "Prohibición estricta de any/dynamic; modelos inmutables y tipado exhaustivo en contratos."),
                ("Captura Vacía de Errores y Silencio de Excepciones", "Bloques try/catch vacíos que ocultan fallos de runtime.", "Intentar que una operación no rompa la ejecución sin registrar ni manejar el error.", "Manejo explícito de excepciones, logging centralizado y degradación controlada."),
            ]
            for title, symptom, root_cause, mitigation in default_extras:
                if len(fms) >= 5:
                    break
                fms.append(type("FM", (), {
                    "title": title,
                    "symptom": symptom,
                    "root_cause": root_cause,
                    "mitigation": mitigation
                })())

        for idx, fm in enumerate(fms, start=1):
            fmid = f"FM-{idx:03d}"
            items.append(f"""## {fmid}: {fm.title}

- **Síntoma observable:** {fm.symptom}
- **Causa raíz técnica (trampa típica de IA):** {fm.root_cause}
- **Mitigación obligatoria y verificación:** {fm.mitigation}
""")

        return f"""# Catálogo de Modos de Fallo — {m.identity.name}

Memoria preventiva de errores y asunciones incorrectas que los agentes de IA o desarrolladores no deben repetir.
Cada modo de fallo documenta la causa raíz y la regla de mitigación verificable.

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
Para construir {m.identity.name} ({m.identity.description}), orientada a {m.identity.target_audience}, se requiere un stack que ofrezca alto rendimiento, tipado estricto y soporte para las plataformas objetivo ({', '.join(m.platform.platforms)}).

## Decisión
Adoptar **{m.stack.language}** con el framework **{m.stack.framework}** y gestor de dependencias `{m.stack.package_manager}`.

## Consecuencias
- **Positivas:** Compilación optimizada, tooling moderno, fuerte ecosistema y soporte para desarrollo guiado por contratos SDD.
- **Negativas:** Se exige cumplimiento estricto del linter y verificación en preflight para evitar malas prácticas del lenguaje.
"""

    def _adr_0002(self) -> str:
        m = self.manifest
        return f"""# ADR-0002: Adopción de {m.architecture.style} y Aislamiento por Módulos

- **Estado:** Aceptada
- **Fecha:** Inicialización del proyecto

## Contexto
El sistema crecerá modularmente con múltiples bloques funcionales ({', '.join([s.name for s in m.scopes])}). Permitir que la presentación acceda directamente a bases de datos o que las entidades dependan de librerías visuales genera deuda técnica y acoplamiento severo.

## Decisión
Implementar **{m.architecture.style}** estricta:
1. El dominio es puro y no depende de frameworks externos.
2. La infraestructura implementa interfaces del dominio.
3. Las features no importan código interno de otras features.

## Consecuencias
- **Positivas:** Testabilidad del 100 % del dominio sin mocks complejos, aislamiento ante cambios de librerías y menor propensión a errores de agentes de IA.
- **Negativas:** Mayor número inicial de archivos y necesidad de mapear DTOs a entidades inmutables.
"""

    def _adr_0003(self) -> str:
        m = self.manifest
        return f"""# ADR-0003: Estrategia de Persistencia y Caché ({m.architecture.persistence})

- **Estado:** Aceptada
- **Fecha:** Inicialización del proyecto

## Contexto
{m.identity.name} requiere una estrategia de almacenamiento de datos conforme a su modelo de persistencia: `{m.architecture.persistence}`.

## Decisión
Adoptar almacenamiento desacoplado mediante el patrón Repository:
- Las entidades de negocio se persisten a través de contratos de repositorio tipados.
- Si es local ({m.architecture.persistence}), se prioriza la consistencia y la velocidad de consulta en disco.
- Se aísla el motor de persistencia dentro de la capa `data/` del módulo correspondiente.

## Consecuencias
- **Positivas:** Capacidad de sustituir o actualizar el motor de base de datos sin tocar la lógica de negocio.
- **Negativas:** Se deben mantener migraciones de esquema versionadas.
"""

