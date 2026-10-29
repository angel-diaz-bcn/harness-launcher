"""
Context Generator: Genera los 12 documentos normativos de .ai-harness/context/
con la profundidad, diagramas y densidad técnica del proyecto FLIK.
"""

from __future__ import annotations

from models import BootstrapManifest, StackType


class ContextGenerator:
    """Genera los 12 documentos de contexto normativo exhaustivos."""

    def __init__(self, manifest: BootstrapManifest) -> None:
        self.manifest = manifest

    def generate_all(self) -> dict[str, str]:
        return {
            "system_identity.md": self._system_identity(),
            "harness_governance.md": self._harness_governance(),
            "project_overview.md": self._project_overview(),
            "architecture_rules.md": self._architecture_rules(),
            "project_structure.md": self._project_structure(),
            "coding_standards.md": self._coding_standards(),
            "testing_guidelines.md": self._testing_guidelines(),
            "security_privacy.md": self._security_privacy(),
            "platform_matrix.md": self._platform_matrix(),
            "glossary.md": self._glossary(),
            "sdd_framework.md": self._sdd_framework(),
            "ui-design-system.md": self._ui_design_system(),
        }

    def _system_identity(self) -> str:
        m = self.manifest
        return f"""# Identidad del sistema y marco de decisión — {m.identity.name}

Define el rol del agente de IA, su postura técnica y los principios no negociables con los que decide.
Es el primer documento de la carga obligatoria: sin él, el agente no sabe qué sombrero lleva.

---

## 1. Rol y posicionamiento

- **Identidad:** Arquitecto de software y desarrollador principal responsable de {m.identity.name}.
- **Dominio técnico:** El declarado en `platform_matrix.md` y en `architecture_rules.md` ({m.stack.language} con {m.stack.framework}). No se asume ninguno más.
- **Propósito:** Diseñar, especificar y construir el sistema con reglas explícitas, verificables y sin ambigüedad.

---

## 2. Principios de decisión

1. **Contratos antes que implementación:** Ningún comportamiento se codifica sin estar descrito en una spec aprobada en `.ai-harness/sdd/`.
2. **Una sola fuente de verdad:** Cada regla vive en un único archivo; el resto la referencia.
3. **Evidencia sobre suposición:** Las decisiones se justifican con el comportamiento real de la plataforma, no con optimizaciones hipotéticas.
4. **Reversibilidad:** Se prefieren cambios pequeños, verificables y fáciles de deshacer.
5. **Dependencias mínimas:** Cada dependencia nueva se justifica formalmente en un ADR en `.ai-harness/memory/decisions/`.
6. **Privacidad por defecto:** Política estricta de {m.platform.privacy_policy}; no se recogen datos de usuario sin justificación ética y explícita.

---

## 3. Jerarquía de autoridad

1. `context/` y `scopes/`.
2. La spec `.spec.md` aprobada.
3. Los contratos e interfaces de código.
4. La documentación auxiliar.

Si una instrucción contradice una regla de contexto, prevalece la regla y se detiene el cambio.

---

## 4. Límites no negociables

- Sin código de producción sin spec aprobada.
- Sin reglas duplicadas entre archivos.
- Sin valores visuales literales fuera de `design-system/tokens.json`.
- Sin secretos ni credenciales en el repositorio.
- Sin publicar en Git sin instrucción explícita del usuario.
- Sin desactivar validadores (`--no-verify`) para forzar un cambio.
"""

    def _harness_governance(self) -> str:
        return """# Gobernanza del arnés y ciclo de vida de especificaciones

Define las reglas de funcionamiento del arnés, las puertas de validación deterministas y los criterios de cierre de tareas.

---

## 1. Naturaleza del arnés

El arnés no es documentación pasiva; es un entorno gobernado ejecutable:
- Las reglas se verifican mediante código en `.ai-harness/skills/`.
- La configuración estructural vive en `harness.config.yaml`.
- Todo cambio de comportamiento exige una actualización sincronizada de spec y código.

---

## 2. Puertas de calidad obligatorias (Quality Gates)

Antes de dar por concluida cualquier tarea o realizar un commit en Git, deben pasar limpias tres puertas:

```
harness-validator  ──▶  preflight  ──▶  sync-sdd
```

1. **`harness-validator`:** Integridad estructural del arnés, validez de frontmatter, coherencia de scopes y registro de skills.
2. **`preflight`:** Calidad de código, linter, pruebas de arquitectura, respeto a las invariantes negativas y uso de tokens.
3. **`sync-sdd`:** Comprobación estricta de que el mapa de implementación de cada spec aprobada coincide con los archivos en disco.

---

## 3. Criterios de cierre (Definition of Done)

Una tarea solo se considera terminada si:
1. Las 3 puertas de enlace devuelven código de salida `0` (`PASSED`).
2. Se corrigió la causa raíz de cualquier violación detectada.
3. Se actualizó la spec SDD asociada y su mapa de implementación.
4. No quedan archivos temporales, stubs huérfanos ni logs residuales.
"""

    def _project_overview(self) -> str:
        m = self.manifest
        module_rows = []
        for s in m.scopes:
            module_rows.append(f"| **{s.title}** | {s.description} | `{s.path_roots[0] if s.path_roots else 'lib/'}` |")

        module_details = []
        for s in m.scopes:
            module_details.append(f"""### Módulo {s.title} (`block_{s.name}`)
- **Responsabilidad:** {s.description}.
- **Fronteras:** Opera de forma desacoplada dentro de sus rutas autorizadas.
- **Interacción:** Consume infraestructura común y se comunica mediante contratos tipados con otros módulos.""")

        return f"""# {m.identity.name} — Overview Global del Producto

## 1. Resumen ejecutivo

**{m.identity.name}** (slug `{m.identity.slug}`) es una solución de software orientada a {m.identity.description.lower()}.

- **Propuesta de valor:** {m.identity.description}
- **Público objetivo:** {m.identity.target_audience}
- **Stack tecnológico:** {m.stack.language} ({m.stack.framework}) con gestor `{m.stack.package_manager}`.
- **Plataformas objetivo:** {', '.join(m.platform.platforms)}.
- **Arquitectura base:** {m.architecture.style}.
- **Persistencia:** {m.architecture.persistence}.
- **Política de privacidad:** {m.platform.privacy_policy}.

---

## 2. Pilares del producto

1. **Arquitectura Contrato-Primero:** Ningún flujo de datos se implementa sin especificación previa en SDD.
2. **Desacoplamiento Estricto:** Cada feature es un bloque vertical autónomo que no invade la estructura interna de otros módulos.
3. **Rendimiento y Recursos Acotados:** Operaciones asíncronas controladas, liberación de memoria obligatoria y arranque inmediato.
4. **Privacidad por Diseño:** Sin telemetría oculta ni dependencias invasivas de analítica.
5. **Experiencia de Usuario Consistente:** Diseño basado en tokens semánticos y navegación por foco universal (teclado / D-Pad).

---

## 3. Arquitectura de los Módulos Core

| Módulo | Responsabilidad | Ruta Autorizada |
|---|---|---|
{chr(10).join(module_rows)}

{chr(10).join(module_details)}
"""

    def _architecture_rules(self) -> str:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"

        return f"""# {m.identity.name} — Arquitectura y Guardarraíles del Sistema

## 1. Enfoque arquitectónico

{m.identity.name} aplica **{m.architecture.style}** con organización modular por features o capas en {m.stack.language}.

```
{folder}/
├── app/              # Configuración global, temas, rutas y composición raíz
├── core/             # Infraestructura transversal: cliente HTTP, almacenamiento, errores, utilidades
└── features/         # Slices verticales de negocio
    └── <feature>/
        ├── domain/          # Entidades, contratos de repositorio y casos de uso
        ├── data/            # Fuentes de datos, DTOs y persistencia
        └── presentation/    # Controladores de estado, vistas y componentes visuales
```

Reglas de organización:
- `{folder}/app/` contiene inicialización, routing, tema global y composición de dependencias.
- `{folder}/core/` contiene infraestructura transversal sin lógica de negocio.
- `{folder}/features/` contiene exclusivamente slices funcionales aislados.
- Una feature no importa archivos internos de otra; solo consume su API pública (`<feature>.dart` o `public/`).
- El dominio no importa frameworks de UI, clientes HTTP crudos ni librerías de infraestructura.
- La presentación no accede a red, base de datos ni almacenamiento sin pasar por repositorios.

---

## 2. Desacoplamiento de módulos

```
app / composition root
        │
        ├── features/ui  ────────┐
        ├── features/domain ────┼───▶ core (infraestructura transversal)
        └── features/data ──────┘

core no depende de ninguna feature.
Las features se comunican únicamente mediante interfaces de dominio.
```

1. **Presentación delgada:** Los widgets o vistas solo renderizan y emiten intenciones del usuario. La lógica de negocio y de sesión vive en controladores y casos de uso.
2. **Dominio puro e inmutable:** Todas las entidades son inmutables y encapsulan invariantes de validación.
3. **Persistencia desacoplada ({m.architecture.persistence}):** La capa de datos implementa las interfaces definidas en el dominio. Cambiar el motor de persistencia nunca altera la lógica de negocio.

---

## 3. Modelo de concurrencia y asincronía

- Todas las operaciones de I/O (red, disco, base de datos) son estrictamente asíncronas y cancelables.
- Prohibido bloquear el hilo principal de ejecución con cálculos intensivos o serializaciones masivas.
- Cada suscripción o listener abierto debe registrar su desuscripción obligatoria en el ciclo de limpieza (`dispose`/`cleanup`).

---

## 4. Invariantes negativas (Paquetes y patrones prohibidos)

Paquetes cuya inclusión en el proyecto está formalmente vetada por `preflight`:
{chr(10).join([f"- `{pkg}`: Prohibido por directriz de privacidad o rendimiento." for pkg in m.architecture.forbidden_packages])}

Reglas negativas:
- Prohibido hardcodear cadenas de conexión o tokens en el código fuente.
- Prohibido el uso de tipos genéricos no seguros (`dynamic` o `any`) fuera de la capa de serialización.
- Prohibido silenciar excepciones con bloques `try/catch` vacíos.
"""

    def _project_structure(self) -> str:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"

        return f"""# Estructura del Proyecto — {m.identity.name}

Árbol canónico de directorios y responsabilidades de cada carpeta.

```
{m.identity.slug}/
├── .ai-harness/           # Gobernanza del arnés de IA, contexto, scopes, SDD y validadores
│   ├── context/          # 12 documentos normativos obligatorios
│   ├── design-system/    # Especificaciones visuales y tokens.json
│   ├── memory/           # Modos de fallo y decisiones de arquitectura (ADRs)
│   ├── scopes/           # Límites de escritura modular (block_*.md)
│   ├── sdd/              # Especificaciones formales (CMP-NN y PRC-NN)
│   └── skills/           # Runners y validadores deterministas
├── .agents/              # Documentación de skills para agentes
├── .clinerules/          # Workflows invocables con barra inclinada
├── {folder}/                  # Código fuente de producción
│   ├── app/              # Composición raíz y routing
│   ├── core/             # Servicios transversales y utilidades
│   └── features/         # Bloques funcionales aislados
├── test/                 # Pruebas unitarias, de integración y de arquitectura
├── AGENTS.md             # Orquestador y punto de entrada para agentes
├── harness.config.yaml   # Única fuente de verdad de la configuración
└── README.md             # Presentación del producto
```

### Reglas de importación entre directorios
1. `{folder}/core/` no puede importar nada de `{folder}/features/` ni de `{folder}/app/`.
2. `{folder}/features/<f1>/` no puede importar nada interno de `{folder}/features/<f2>/`.
3. `{folder}/app/` orquesta la inyección de dependencias pero no implementa lógica de dominio.
"""

    def _coding_standards(self) -> str:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        is_python = m.stack.stack_type == StackType.PYTHON
        is_node = m.stack.stack_type == StackType.NODE

        stack_rules = ""
        if is_flutter:
            stack_rules = """### Reglas específicas de Flutter y Dart
- **Tipado estricto:** `analysis_options.yaml` con linter riguroso y sin warnings nuevos.
- **Prohibido `dynamic`:** Salvo fronteras de serialización justificadas y confinadas a `data/`.
- **Prohibido `print`:** Usar el logger de `core/`.
- **Prohibido `catch` vacío o silencioso:** Todo error se tipa y se propaga o registra con contexto.
- **Inmutabilidad:** Usar clases inmutables para entidades y estados.
- **Paridad de ciclo de vida:** Todo `StreamSubscription`, `TextEditingController` o `FocusNode` creado en `initState` debe cancelarse en `dispose`."""
        elif is_python:
            stack_rules = """### Reglas específicas de Python
- **Tipado estricto:** Uso de type hints en todas las funciones y clases. Verificado con `mypy` o `pyright`.
- **Modelos:** Usar Pydantic v2 para validación de datos en fronteras de I/O.
- **Prohibido `print`:** Usar el módulo `logging` estructurado de `core/`.
- **Prohibido `except Exception: pass`:** Captura explícita de tipos de excepción conocidos.
- **Formato:** `ruff format` y `ruff check` antes de cada commit."""
        elif is_node:
            stack_rules = """### Reglas específicas de TypeScript / Node
- **Tipado estricto:** `tsconfig.json` con `strict: true`, `noImplicitAny: true`.
- **Prohibido `any`:** Usar `unknown` con type guards o esquemas Zod en fronteras de serialización.
- **Prohibido `console.log`:** Usar logger centralizado estructurado.
- **Asincronía:** Siempre `async/await`; prohibido mezclar promesas crudas con callbacks."""

        return f"""# Estándares de Código y Directrices de Implementación — {m.identity.name}

Estándares obligatorios para el desarrollo, revisión y mantenimiento del código de {m.identity.name}.

---

## 1. Principios de calidad del código

1. **Legibilidad sobre ingenio:** Código directo, autoexplicativo y fácil de auditar.
2. **Inmutabilidad por defecto:** Los objetos de dominio y los estados de UI son inmutables.
3. **Manejo tipado de errores:** Prohibido propagar errores crudos no estructurados; usar tipos de fallo explícitos (`Failure` / `Result`).
4. **Nomenclatura uniforme:** Nombres descriptivos y consistentes con el glosario oficial.

---

## 2. Directrices técnicas por lenguaje

{stack_rules}

---

## 3. Manejo de estado y asincronía

- El estado de la aplicación es determinista y fluye en una sola dirección (Unidirectional Data Flow).
- Las vistas son funciones puras del estado; no mutan variables globales.
- Toda operación de red o disco debe manejar los 4 estados canónicos: `Initial`, `Loading`, `Success` y `Failure`.
"""

    def _testing_guidelines(self) -> str:
        m = self.manifest
        return f"""# Directrices de Testing y Verificación — {m.identity.name}

Estrategia de pruebas automatizadas para garantizar la estabilidad y regresión cero.

---

## 1. Pirámide de testing

```
        /\\
       /  \\      Integration Tests (Flujos punta a punta de features críticas)
      /────\\
     /      \\    Component / UI Tests (Renderizado, interacción y foco)
    /────────\\
   /          \\  Unit Tests (Dominio, casos de uso, parsing y repositorios)
  /────────────\\
```

- **Unit Tests (70 %):** Verifican la lógica pura del dominio, cálculos y contratos de datos sin dependencias de red ni disco.
- **Component / UI Tests (20 %):** Verifican el renderizado de componentes, navegación por foco y emisión de eventos.
- **Integration Tests (10 %):** Verifican flujos completos entre múltiples capas.

---

## 2. Política de Mocks y Fakes

- Se prefieren **Fakes en memoria** (ej. `FakeCatalogRepository`) sobre mocks dinámicos para pruebas de casos de uso.
- Las llamadas a APIs externas de red siempre se aíslan mediante adaptadores mockeables.
- Prohibido ejecutar tests unitarios que requieran conexión activa a internet.

---

## 3. Invariantes de prueba

1. Ningún commit se aprueba si rompe tests existentes.
2. Cada bug corregido debe ir acompañado de un test unitario que reproduzca el fallo para evitar regresiones.
3. El comando de test configurado (`{m.stack.test_command}`) debe finalizar con código de salida `0`.
"""

    def _security_privacy(self) -> str:
        m = self.manifest
        return f"""# Seguridad, Privacidad y Telemetría — {m.identity.name}

Límites no negociables de seguridad de datos y protección del usuario.

---

## 1. Política de telemetría: {m.platform.privacy_policy}

- **Cero telemetría no consentida:** Ningún dato personal, identificador de dispositivo o hábito de uso se envía a servidores de analítica.
- **Librerías de tracking vetadas:** Preflight audita y bloquea SDKs de tracking comercial ({', '.join(m.architecture.forbidden_packages[:3])}...).
- **Logs limpios:** Los logs de depuración nunca imprimen tokens, contraseñas ni datos sensibles del usuario.

---

## 2. Gestión de secretos y credenciales

- **Prohibido commitear credenciales:** Ningún archivo `.env`, certificado `.pem`, clave privada ni keystore puede subirse a Git.
- **Variables de entorno:** Los secretos se inyectan en tiempo de ejecución o compilación mediante `{m.platform.secrets_management}`.
- Todo archivo de configuración con credenciales está registrado en `.gitignore`.

---

## 3. Seguridad en comunicaciones y almacenamiento

- Todas las conexiones externas utilizan obligatoriamente TLS/HTTPS con verificación estricta de certificados.
- Si existe almacenamiento local de credenciales o sesión, se utiliza el llavero seguro nativo de la plataforma (Keystore / Keychain / SecretService).
"""

    def _platform_matrix(self) -> str:
        m = self.manifest
        rows = []
        for p in m.platform.platforms:
            rows.append(f"| **{p}** | Versión moderna estable | Compilación nativa optimizada | Hardware estándar |")

        return f"""# Matriz de Plataformas y Requisitos del Sistema — {m.identity.name}

Plataformas soportadas oficialmente y requisitos de hardware y runtime.

---

## 1. Plataformas objetivo

| Plataforma | Versión mínima | Target | Requisitos especiales |
|---|---|---|---|
{chr(10).join(rows)}

---

## 2. Dependencias de entorno para desarrollo

- Runtime: {m.stack.language} ({m.stack.min_runtime_version or 'versión estable recomendada'}).
- Gestor de dependencias: `{m.stack.package_manager}`.
- Python 3.11+ para la ejecución del tooling del arnés de IA (`.ai-harness/skills/`).
"""

    def _glossary(self) -> str:
        m = self.manifest
        return f"""# Glosario Ubicuo de Términos — {m.identity.name}

Vocabulario canónico del dominio para evitar ambigüedades entre desarrolladores y agentes de IA.

---

| Término | Definición unívoca | Qué NO significa | Dónde se usa |
|---|---|---|---|
| **{m.identity.name}** | El sistema principal y producto objeto de este repositorio. | No es una librería genérica. | Todo el sistema |
| **Scope** | Límite modular estricto de responsabilidad y escritura de código. | No es un archivo de código ni una carpeta arbitraria. | `.ai-harness/scopes/` |
| **Spec** | Especificación técnica formal (SDD) previa a la codificación. | No es documentación post-hoc ni un comentario. | `.ai-harness/sdd/` |
| **Preflight** | Puerta de enlace determinista que valida arquitectura y calidad. | No es un simple linter de sintaxis. | `.ai-harness/skills/preflight/` |
| **Tokens** | Variables semánticas de diseño (colores, espaciados, fuentes). | No son valores HEX ni píxeles directos. | `design-system/tokens.json` |
| **ADR** | Architectural Decision Record; registro inmutable de decisión técnica. | No es un plan temporal de tareas. | `.ai-harness/memory/decisions/` |
"""

    def _sdd_framework(self) -> str:
        return """# Marco de Desarrollo Guiado por Especificaciones (SDD Framework)

Gobierna el ciclo de vida de los componentes y procesos antes de escribir código de producción.

---

## 1. Principio fundamental: SDD-First

En este repositorio **está prohibido escribir código de producción sin una especificación formal aprobada**.
La spec es el contrato entre el arquitecto y el desarrollador (humano o IA).

---

## 2. Taxonomía de especificaciones

1. **Componentes (`CMP-NN`):** Unidades técnicas autónomas (modelos, servicios, repositorios, widgets o pantallas).
2. **Procesos (`PRC-NN`):** Flujos transversales de negocio que orquestan múltiples componentes mediante diagramas de secuencia y máquinas de estados.

---

## 3. Ciclo de vida de una Spec

```
draft  ──▶  proposed  ──▶  approved  ──▶  implemented  ──▶  deprecated
```

1. **`draft`:** En redacción inicial.
2. **`proposed`:** Lista para revisión técnica.
3. **`approved`:** Aprobada formalmente. Es la única fase que autoriza comenzar a codificar.
4. **`implemented`:** Implementación completada y verificada al 100 % por `sync-sdd`.
5. **`deprecated`:** Sustituida por una nueva spec declarada en `superseded_by`.
"""

    def _ui_design_system(self) -> str:
        m = self.manifest
        return f"""# Directriz Normativa de Diseño y Experiencia de Usuario — {m.identity.name}

Reglas obligatorias para la capa de presentación. Las especificaciones detalladas viven en `design-system/`.

---

## 1. Prohibición de valores visuales literales

- **Prohibido colores HEX o constantes directas:** Queda prohibido escribir `#FFFFFF`, `Colors.blue` o valores mágicos en componentes.
- Todo valor visual debe consumirse desde `design-system/tokens.json` o mediante la clase de tema semántico generada.

---

## 2. Navegación por foco universal

Cualquier pantalla o componente interactivo debe ser navegable mediante:
1. Teclado (flechas, Tab, Enter, Escape).
2. D-Pad / Mando a distancia (si aplica a TV o consolas).
3. Pantalla táctil o ratón.

El foco activo debe tener una señal visual inequívoca (anillo de foco, cambio de escala o borde semántico).
"""
