"""
Context Generator Engine: Genera los 12 documentos normativos de .ai-harness/context/
garantizando personalización profunda, cero placeholders (<...>), total soberanía
cuando se proporcionan overrides e idempotencia absoluta en cualquier tecnología.
"""

from __future__ import annotations

import re
from pathlib import Path
from models import BootstrapManifest, ProductArchetype, StackType


class ContextGenerator:
    """Genera los 12 documentos normativos a partir del manifiesto y plantillas canónicas."""

    def __init__(self, manifest: BootstrapManifest, harness_dir: Path | None = None) -> None:
        self.manifest = manifest
        launcher_root = Path(__file__).resolve().parents[3]
        self.canonical_template_dir = launcher_root / "context"
        self.harness_dir = Path(harness_dir).resolve() if harness_dir else launcher_root

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
            # 1. Leer siempre la plantilla canónica limpia como referencia
            template_path = self.canonical_template_dir / doc
            base_template = ""
            if template_path.exists():
                base_template = template_path.read_text(encoding="utf-8", errors="ignore")

            # 2. Si existe un override específico en el manifiesto (soporta tanto _ como - en el nombre)
            override_key = None
            for candidate in (doc, doc.replace("_", "-"), doc.replace("-", "_")):
                if candidate in self.manifest.custom_context_overrides and self.manifest.custom_context_overrides[candidate].strip():
                    override_key = candidate
                    break

            if override_key:
                override_text = self.manifest.custom_context_overrides[override_key].strip()
                result[doc] = self._handle_custom_override(doc, override_text, base_template)
                continue

            # 3. De lo contrario, generar el documento contextualizado sin ningún placeholder (<...>)
            result[doc] = self._generate_rich_context_doc(doc, base_template)

        return result

    def _resolve_common_vars(self, content: str) -> str:
        m = self.manifest
        content = content.replace("<PROYECTO>", m.identity.name)
        content = content.replace("<proyecto>", m.identity.slug)
        content = content.replace("<plataformas>", ", ".join(m.platform.platforms))
        content = content.replace("<stack>", f"{m.stack.language} {f'({m.stack.framework})' if m.stack.framework else ''}")
        return content

    def _handle_custom_override(self, doc_name: str, override_text: str, base_template: str) -> str:
        """Procesa un override aportado en el manifiesto garantizando soberanía sin duplicaciones."""
        m = self.manifest
        resolved = self._resolve_common_vars(override_text)

        # Caso especial 1: Glosario (Fusión limpia de términos de dominio con términos del arnés)
        if doc_name == "glossary.md":
            domain_lines = []
            for line in resolved.splitlines():
                stripped = line.strip()
                if stripped.startswith(("#", "---")):
                    continue
                if stripped.startswith(("-", "*")) or (":" in stripped and len(stripped) > 5):
                    domain_lines.append(line)

            domain_section = "\n".join(domain_lines).strip()
            interpolated_base = self._generate_rich_context_doc(doc_name, base_template)

            if domain_section:
                placeholder_regex = r"## 5\. Términos de (?:Dominio y )?Producto[\s\S]*?(?=## 6|\Z)"
                replacement = f"## 5. Términos de Dominio y Producto ({m.identity.name})\n\n{domain_section}\n\n"
                if re.search(placeholder_regex, interpolated_base):
                    return re.sub(placeholder_regex, replacement, interpolated_base)
                return f"{interpolated_base}\n\n## 5. Términos de Dominio ({m.identity.name})\n\n{domain_section}\n"
            return interpolated_base

        # Caso especial 2: Coding Standards (Preserva estándares y añade disciplina transversal si falta)
        if doc_name == "coding_standards.md":
            if "Estándares Transversales y Disciplina de Calidad" not in resolved:
                resolved += f"""

---

## 3. Estándares Transversales y Disciplina de Calidad

- **Trazabilidad de Símbolos:** Todo símbolo público relevante lleva comentario de trazabilidad hacia su contrato en OpenSpec:
  `/// Spec: MOD-<modulo> / CT-<id>`
- **Cero Excepciones Huérfanas:** Las funciones públicas de servicio capturan errores de bajo nivel y devuelven tipos cerrados o excepciones tipadas de dominio.
- **Tipado Estricto:** Prohibido el uso de tipos genéricos dinámicos (`Any`, `dynamic`, `unknown`) en contratos públicos.
- **Formateo y Linters:** El código debe superar sin advertencias la ejecución de las herramientas estáticas del lenguaje (`ruff/mypy` en Python, `eslint` en TypeScript/Node, `dart analyze` en Dart).
- **Pruebas de Regresión:** Todo fallo o bug detectado requiere al menos un test unitario que lo reproduzca antes de aplicar la corrección.
"""
            return resolved

        # Caso especial 3: Security & Privacy (Preserva reglas y asegura gestión de secretos si falta)
        if doc_name == "security_privacy.md":
            if "Gestión y Rotación de Secretos" not in resolved:
                resolved += f"""

---

## 3. Gestión y Rotación de Secretos

- **Variables de Entorno:** Las credenciales nunca se compilan en imágenes ni se versionan en Git; viven en `.env` local (ignorado en `.gitignore`).
- **Rotación Inmediata:** Si un secreto se expone accidentalmente, se invalida de inmediato en el proveedor, se rota y se documenta un ADR de remediación.
- **Principio de Mínimo Privilegio:** Los tokens de APIs externas se generan con permisos acotados exclusivamente a los recursos necesarios.
- **Auditoría de Dependencias:** No se admiten paquetes con vulnerabilidades conocidas (CVE) ni librerías de telemetría invasiva.
"""
            return resolved

        # Caso especial 4: Architecture Rules (Soberano; añade paquetes prohibidos si no estaban en el texto)
        if doc_name == "architecture_rules.md":
            if m.architecture.forbidden_packages and "Paquetes Prohibidos" not in resolved:
                resolved += "\n\n## 4. Paquetes Prohibidos por Diseño\n\nQueda formalmente prohibida la inclusión de las siguientes dependencias:\n"
                for pkg in m.architecture.forbidden_packages:
                    resolved += f"- `{pkg}`\n"
            return resolved

        return resolved

    def _generate_rich_context_doc(self, doc_name: str, base_template: str) -> str:
        """Genera un documento de contexto rico, contextualizado y sin ningún placeholder (<...>)."""
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"

        if doc_name == "system_identity.md":
            return self._build_system_identity(m)
        if doc_name == "project_overview.md":
            return self._build_project_overview(m, folder)
        if doc_name == "architecture_rules.md":
            return self._build_architecture_rules(m, folder)
        if doc_name == "project_structure.md":
            return self._build_project_structure(m, folder)
        if doc_name == "platform_matrix.md":
            return self._build_platform_matrix(m)
        if doc_name == "ui-design-system.md":
            return self._build_ui_design_system(m)
        if doc_name == "coding_standards.md":
            return self._build_coding_standards(m)
        if doc_name == "testing_guidelines.md":
            return self._build_testing_guidelines(m)
        if doc_name == "security_privacy.md":
            return self._build_security_privacy(m)

        # Para harness_governance.md, sdd_framework.md y glossary.md: interpolar variables limpiamente
        content = self._resolve_common_vars(base_template)
        content = content.replace("<PROYECTO>", m.identity.name)
        return content

    def _build_system_identity(self, m: BootstrapManifest) -> str:
        forbidden_clause = ""
        if m.architecture.forbidden_packages:
            forbidden_clause = f"\n- Prohibida la inclusión de paquetes o dependencias vetadas: {', '.join([f'`{p}`' for p in m.architecture.forbidden_packages])}."

        return f"""# Identidad del Sistema y Marco de Decisión — {m.identity.name}

Define el rol del agente de IA, su postura técnica y los principios deterministas con los que decide y construye.
Es el primer documento de la carga obligatoria: sin él, el agente no comprende su marco de actuación ni los límites del producto.

---

## 1. Rol y Posicionamiento

- **Producto:** {m.identity.name} — {m.identity.description}
- **Arquetipo:** `{m.identity.archetype.value}` dirigido a {m.identity.target_audience}.
- **Identidad del Agente:** Arquitecto de software e ingeniero principal responsable del desarrollo, gobernanza y calidad de {m.identity.name}.
- **Dominio Técnico:** {m.stack.language} {f'({m.stack.framework})' if m.stack.framework else ''} ejecutándose en {', '.join(m.platform.platforms)}.
- **Propósito:** Diseñar, especificar mediante OpenSpec y auditar el código con reglas explícitas, contratos inmutables y calidad verificable, eliminando alucinaciones y código huérfano.

---

## 2. Principios de Decisión

1. **Contratos antes que implementación:** Ningún comportamiento se codifica sin estar descrito en una propuesta aprobada (`changes/`) o módulo consolidado (`modules/`), salvo parches bajo el protocolo Fast-Path (<3 archivos).
2. **Una sola fuente de verdad:** Cada regla vive en un único archivo normativo; el resto la referencia.
3. **Evidencia sobre suposición:** Las decisiones se justifican con requerimientos verificables, no con suposiciones o atajos hipotéticos.
4. **Reversibilidad y modularidad:** Se prefieren cambios pequeños, atómicos y desacoplados.
5. **Dependencias mínimas y gobernadas:** Toda dependencia nueva se somete a evaluación y se registra en la arquitectura.
6. **Privacidad por defecto ({m.platform.privacy_policy}):** Cero recolección de datos de usuario no consentida ni telemetría invasiva.

---

## 3. Jerarquía de Autoridad

1. `.ai-harness/context/` y `.ai-harness/scopes/` (Directrices maestras y fronteras de escritura).
2. Módulos vivos consolidados en `.ai-harness/sdd/modules/` y propuestas activas en `changes/`.
3. Contratos de interfaz (`CT-*`) y código fuente.
4. Documentación auxiliar y logs efímeros.

Si una instrucción contradice una regla de contexto o arquitectura, prevalece la regla y se detiene el cambio.

---

## 4. Límites No Negociables

- Sin código de producción huérfano sin propuesta consolidada o protocolo Fast-Path.
- Sin reglas duplicadas entre archivos.
- Sin valores visuales literales fuera del sistema de tokens (si aplica a UI).
- Sin secretos ni credenciales en el repositorio.{forbidden_clause}
- Sin publicar en Git sin instrucción explícita del usuario (`git-publish`).
- Sin desactivar validadores para forzar el paso de un cambio.

---

## 5. Comunicación y Postura

- **Rigor y franqueza:** Se señalan riesgos de rendimiento, memoria, seguridad o acoplamiento sin adornos.
- **Respuestas estructuradas:** Orientadas a decisiones y acciones concretas.
- **Fidelidad al arnés:** Ante ambigüedad, se consulta la especificación o se detiene la tarea; nunca se inventa un contrato.
"""

    def _build_project_overview(self, m: BootstrapManifest, folder: str) -> str:
        module_rows = "\n".join([
            f"| `{s.name}` | {s.description} | `{s.path_roots[0] if s.path_roots else folder + '/' + s.name}` |"
            for s in m.scopes
        ])

        return f"""# Overview del Producto — {m.identity.name}

Describe qué es el sistema, qué pilares lo sostienen y qué queda fuera de alcance. Es la referencia para decidir si una idea pertenece al producto o no.

---

## 1. Resumen Ejecutivo

**{m.identity.name}** es {m.identity.description}

- **Propuesta de valor:** Solución concebida para {m.identity.target_audience}, maximizando la autonomía, consistencia y calidad mediante ingeniería guiada por especificaciones (OpenSpec SDD).
- **Entorno operativo:** El sistema opera en **{', '.join(m.platform.platforms)}** con un stack rector basado en **{m.stack.language} {f'({m.stack.framework})' if m.stack.framework else ''}**.

---

## 2. Pilares del Sistema

1. **Propósito Claro:** Cada funcionalidad responde a un objetivo de producto verificable dirigido a {m.identity.target_audience}.
2. **Contratos Explícitos:** La comunicación entre componentes se rige por contratos tipados e inmutables, nunca improvisados.
3. **Aislamiento Modular:** Cada capacidad está delimitada por su propio scope con límites de escritura infranqueables.
4. **Privacidad por Defecto ({m.platform.privacy_policy}):** Cumplimiento estricto de la política de cero telemetría no consentida.
5. **Calidad Determinista:** Todo cambio requiere verificación automática mediante las puertas de calidad del arnés.

---

## 3. Módulos del Sistema

| Módulo | Responsabilidad | Ruta Autorizada |
|---|---|---|
{module_rows}

Los módulos se comunican exclusivamente mediante interfaces y contratos públicos definidos en sus respectivas especificaciones de OpenSpec (`.ai-harness/sdd/modules/`).

---

## 4. Flujo Principal del Sistema

1. **Inicialización:** El sistema arranca y verifica la integridad de dependencias y contratos transversales.
2. **Coordinación:** El módulo orquestador coordina el flujo de datos invocando las interfaces públicas de cada módulo.
3. **Procesamiento:** Cada capacidad ejecuta su lógica de dominio aislada sin acoplarse a detalles de infraestructura.
4. **Persistencia:** La información de estado se gestiona mediante `{m.architecture.persistence}` de forma segura e idempotente.
5. **Salida y Notificación:** Las respuestas, eventos o artefactos generados se emiten hacia las plataformas objetivo ({', '.join(m.platform.platforms)}).

---

## 5. Fuera de Alcance

- Funcionalidades no especificadas previamente en una propuesta aprobada de OpenSpec (`changes/`).
- Integración de servicios con costes fijos no planificados o contrarios al presupuesto del producto.
- Inclusión de librerías de rastreo comercial invasivo o recolección de datos personales de usuarios.
- Acoplamiento directo entre carpetas privadas de distintos módulos sin pasar por contratos públicos.

---

## 6. Criterios de Éxito

- Validación del 100% de los quality gates deterministas (`harness-validator`, `preflight`, `sync-sdd`).
- Arquitectura desacoplada y verificable con suite de tests automatizada (`{m.stack.test_command}`).
- Cero divergencias entre el código implementado y las especificaciones consolidadas.
"""

    def _build_architecture_rules(self, m: BootstrapManifest, folder: str) -> str:
        layer_items = "\n".join([f"├── {l}/" + (" " * max(1, 14 - len(l))) + f"# Capa de {l.capitalize()}" for l in m.architecture.layers[:-1]])
        last_l = m.architecture.layers[-1] if m.architecture.layers else "presentation"
        layer_items += f"\n└── {last_l}/" + (" " * max(1, 14 - len(last_l))) + f"# Capa de {last_l.capitalize()}"

        forbidden_section = ""
        if m.architecture.forbidden_packages:
            forbidden_section = f"""

---

## 4. Paquetes Prohibidos por Diseño

Queda formalmente prohibida la inclusión de las siguientes dependencias:
""" + "\n".join([f"- `{p}`" for p in m.architecture.forbidden_packages])

        return f"""# Arquitectura y Guardarraíles — {m.identity.name}

Enfoque arquitectónico, dirección de dependencias e invariantes del sistema.

---

## 1. Enfoque Arquitectónico

El sistema está estructurado bajo **{m.architecture.style}**, garantizando separación estricta entre reglas de negocio puras y detalles de infraestructura:

```
{folder}/<modulo>/
{layer_items}
```

Reglas de organización:
- `{folder}/core/` concentra la infraestructura transversal, contratos abstractos y utilidades compartidas.
- Cada módulo es autónomo y encapsula su modelo de datos y servicios.
- La comunicación inter-módulo se realiza exclusivamente a través de interfaces públicas (`__init__.py`, `index.ts` o barrels públicos).
- El dominio no importa frameworks de presentación, librerías de I/O de bajo nivel ni bases de datos concretas.

---

## 2. Dirección de Dependencias

```
Adaptadores / Entrada (CLI, Endpoints, UI)
        │
        ├──▶ Casos de Uso / Servicios
        │         │
        │         └──▶ Dominio (Entidades y Reglas Puras)
        │
Infraestructura (APIs, BD: {m.architecture.persistence}) ──▶ Implementa interfaces del Dominio
```

Reglas de dependencia:
- Las dependencias fluyen siempre hacia el dominio y hacia las interfaces abstractas.
- Prohibidas las dependencias circulares entre módulos o capas.
- Ningún módulo accede directamente a las tablas o almacenamiento privado de otro.

---

## 3. Invariantes del Sistema

- **Invariante 1 (Aislamiento de Módulo):** Cada módulo opera dentro de sus rutas autorizadas especificadas en su archivo de scope (`block_<modulo>.md`).
- **Invariante 2 (Persistencia Desacoplada):** El almacenamiento ({m.architecture.persistence}) se accede únicamente a través de contratos y repositorios tipados.
- **Invariante 3 (Privacidad Garantizada):** Cero telemetría de usuario final en todo el proyecto ({m.platform.privacy_policy}).{forbidden_section}
"""

    def _build_project_structure(self, m: BootstrapManifest, folder: str) -> str:
        scope_tree_lines = []
        scope_desc_lines = []
        for s in m.scopes:
            clean_p = (s.path_roots[0] if s.path_roots else f"{folder}/{s.name}").rstrip("/")
            scope_tree_lines.append(f"│   ├── {s.name}/" + (" " * max(1, 14 - len(s.name))) + f"# {s.title}")
            scope_desc_lines.append(f"- **`{clean_p}/`**: {s.description}")

        scope_tree = "\n".join(scope_tree_lines)
        scope_descs = "\n".join(scope_desc_lines)

        return f"""# Estructura del Proyecto — {m.identity.name}

Topología física del repositorio y responsabilidad de cada directorio.

---

## 1. Árbol de Directorios

```
{m.identity.slug}/
├── .ai-harness/              # Gobernanza: contexto, scopes, SDD, memoria, skills
│   ├── context/              # Documentos normativos del producto
│   ├── scopes/               # Límites contractuales de escritura
│   ├── sdd/                  # Especificaciones OpenSpec (modules, changes, archive)
│   ├── memory/               # Modos de fallo y registro de ADRs
│   └── skills/               # Herramientas ejecutables de auditoría
├── .agents/skills/           # Catálogo de skills en formato canónico para agentes
├── .clinerules/              # Reglas de orquestación y workflows de ejecución
├── {folder}/
{scope_tree}
├── tests/
│   ├── unit/                 # Pruebas unitarias de contratos y lógica
│   ├── integration/          # Pruebas de integración entre módulos
│   └── fixtures/             # Payloads deterministas para pruebas locales sin red
├── AGENTS.md                 # Orquestador maestro del arnés
├── harness.config.yaml       # Configuración estructural del arnés
├── requirements.txt          # Dependencias Python del tooling de gobernanza
└── README.md                 # Presentación y arranque de {m.identity.name}
```

---

## 2. Responsabilidades por Directorio

{scope_descs}
- **`tests/`**: Garantía determinista de cobertura y verificación de contratos sin llamadas a servicios externos de producción.
"""

    def _build_platform_matrix(self, m: BootstrapManifest) -> str:
        rows = "\n".join([
            f"| **{p}** | {'Puntero, táctil y teclado' if m.ui.has_ui else 'Línea de comandos / Daemon'} | Compilación nativa optimizada | Hardware estándar |"
            for p in m.platform.platforms
        ])

        return f"""# Plataformas y Matriz de Soporte — {m.identity.name}

Plataformas soportadas, modos de interacción y restricciones del entorno operativo.

---

## 1. Matriz de Plataformas

| Plataforma | Entrada Principal | Modo de Ejecución | Entorno |
|---|---|---|---|
{rows}

---

## 2. Reglas Transversales

- Toda funcionalidad debe estar validada para ejecutarse en las plataformas declaradas ({', '.join(m.platform.platforms)}).
- Degradación elegante: Si una capacidad no está disponible en un entorno específico, el sistema informa con un error tipado sin interrumpir el proceso principal.
- Prohibido asumir recursos infinitos: Los consumos de memoria y almacenamiento se acotan a los límites de la plataforma más restrictiva.

---

## 3. Accesibilidad y Navegación

- Todo control o acción relevante es accesible mediante teclado estándar según WCAG AA.
- Las respuestas interactivas proporcionan feedback inmediato y estructurado.
- El foco y la navegación se gestionan de forma predecible sin atrapar al usuario en bucles de navegación.
"""

    def _build_ui_design_system(self, m: BootstrapManifest) -> str:
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

        css_info = f"acoplado a **{m.ui.css_framework}**" if m.ui.css_framework else "mediante variables CSS y tokens canónicos"

        return f"""# Sistema de Diseño y Tokens — {m.identity.name}

Principios visuales, consumo de tokens semánticos y reglas de interfaz de usuario.

---

## 1. Fuente de Verdad de Diseño

La única autoridad para colores, espacios, tipografías y bordes es `.ai-harness/design-system/tokens.json`.

- **Framework visual:** Implementación {css_info}.
- **Prohibición absoluta:** Cero valores literales (códigos HEX `#1E40AF`, píxeles hardcodeados) en componentes de interfaz.
- **Tema:** Soporte nativo para modo `{m.ui.theme_preference}`.

---

## 2. Componentes Clave Declarados

{chr(10).join([f"- **`{c}`**: Componente semántico desacoplado que consume tokens semánticos." for c in m.ui.key_components]) if m.ui.key_components else "- Componentes estándar modulares basados en tokens."}

---

## 3. Accesibilidad y Foco

- Contraste cromático mínimo según WCAG AA (mínimo 4.5:1 en texto principal).
- Navegación accesible por teclado y puntero táctil con indicadores de foco visibles.
- Todo estado interactivo (hover, focus, disabled, active) se deriva de los tokens semánticos de estado.
"""

    def _build_coding_standards(self, m: BootstrapManifest) -> str:
        lang = m.stack.language.lower()
        if "python" in lang:
            tooling = "Ruff (linter y formateador) y Mypy (chequeo estricto de tipos)"
            style_rule = "- Respeto estricto a PEP 8 y anotaciones de tipo completas en contratos públicos."
        elif "node" in lang or "type" in lang or "java" in lang:
            tooling = "ESLint y Prettier con configuración estricta"
            style_rule = "- Prohibido el uso de `any` en interfaces públicas y contratos exportados."
        elif "dart" in lang or "flutter" in lang:
            tooling = "dart analyze con flutter_lints estricto"
            style_rule = "- Constructor const en todos los widgets inmutables y tipado fuerte."
        else:
            tooling = "Linters y formateadores oficiales del lenguaje"
            style_rule = "- Convenciones idiomáticas canónicas y tipado estricto."

        return f"""# Estándares de Código — {m.identity.name}

Convenciones técnicas, linters obligatorios y disciplina de calidad para {m.stack.language}.

---

## 1. Tooling y Linters Obligatorios

- **Herramientas:** {tooling}.
- {style_rule}
- El código no debe presentar advertencias ni errores en la inspección estática.

---

## 2. Nomenclatura y Organización

- Clases, contratos y tipos en `PascalCase`.
- Funciones, métodos y variables en snake_case (o camelCase según estándar del lenguaje).
- Constantes inmutables en `SCREAMING_SNAKE_CASE`.
- Archivos y carpetas en minúsculas separadas por guiones o guiones bajos consistentes.

---

## 3. Estándares Transversales y Disciplina de Calidad

- **Trazabilidad de Símbolos:** Todo símbolo público relevante lleva comentario de trazabilidad hacia su contrato en OpenSpec:
  `/// Spec: MOD-<modulo> / CT-<id>`
- **Cero Excepciones Huérfanas:** Las funciones públicas capturan errores de bajo nivel y devuelven tipos cerrados o excepciones tipadas de dominio.
- **Tipado Estricto:** Prohibido el uso de tipos dinámicos o comodines en contratos públicos.
- **Pruebas de Regresión:** Todo fallo o bug detectado requiere al menos un test unitario que lo reproduzca antes de aplicar la corrección.
"""

    def _build_testing_guidelines(self, m: BootstrapManifest) -> str:
        return f"""# Directrices de Testing — {m.identity.name}

Estrategia de verificación, pirámide de pruebas y ejecución determinista.

---

## 1. Comando de Ejecución

La suite de pruebas automatizadas se ejecuta mediante:

```bash
{m.stack.test_command}
```

---

## 2. Niveles de Prueba

1. **Unitarias (`tests/unit/`):**
   - Validan lógica de negocio pura, algoritmos y reglas de invariantes.
   - Ejecución ultrarrápida en memoria; cero I/O a servicios externos reales.
2. **Integración (`tests/integration/`):**
   - Validan la comunicación entre módulos y el flujo de orquestación.
   - Uso de bases de datos embebidas o mocks deterministas.
3. **Fixtures Deterministas (`tests/fixtures/`):**
   - Payloads estáticos reproducibles para pruebas sin dependencia de red.

---

## 3. Criterios de Aceptación de Tests

- **Determinismo:** Ningún test depende de reloj no mockeado, llamadas a internet o estados aleatorios.
- **Aislamiento:** Cada prueba es independiente y puede ejecutarse en cualquier orden.
- **Paridad con OpenSpec:** Cada contrato `CT-NN` debe contar con su correspondiente test `TC-NN`.
"""

    def _build_security_privacy(self, m: BootstrapManifest) -> str:
        return f"""# Seguridad y Privacidad — {m.identity.name}

Política de privacidad, protección de datos y gestión segura de secretos.

---

## 1. Política de Privacidad ({m.platform.privacy_policy})

- **Cero Telemetría Invasiva:** Queda formalmente prohibida la inyección de bibliotecas de analítica comercial, mapas de calor o rastreadores de usuario en el código.
- **Tratamiento de Datos:** Únicamente se procesan los datos estrictamente imprescindibles para la funcionalidad declarada en el producto.
- **Métricas Agregadas:** Toda analítica operativa se recopila a nivel de infraestructura agregada y anonimizada.

---

## 2. Gestión y Rotación de Secretos

- **Variables de Entorno:** Ninguna credencial, clave de API o secreto se compila en código fuente ni se versiona en Git. Residen exclusivamente en `.env` local.
- **Ignorado en Git:** El archivo `.env` está estrictamente registrado en `.gitignore` y protegido por `.aiignore`.
- **Principio de Mínimo Privilegio:** Los tokens de servicios externos se configuran con los permisos mínimos requeridos para su función.
- **Rotación Inmediata:** Si un secreto se expone accidentalmente, se revoca en el proveedor de inmediato y se documenta un ADR de remediación.
"""
