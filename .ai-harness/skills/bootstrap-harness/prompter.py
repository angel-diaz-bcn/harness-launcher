"""
Prompter Engine: Entrevistador interactivo accesible para perfiles técnicos y no técnicos.
Ofrece opciones cerradas con recomendación, '🤖 Decidir por mí' y '✏️ Campo abierto'.
"""

from __future__ import annotations

import sys
from typing import Any
from input_scanner import InputDigest
from models import (
    ADRItem,
    ArchitectureConfig,
    BootstrapManifest,
    FailureModeItem,
    PlatformConfig,
    ProjectIdentity,
    ScopeDefinition,
    StackType,
    TechStack,
    UIConfig,
)


class Prompter:
    """Gestiona el diálogo interactivo con el usuario."""

    def __init__(self, digest: InputDigest | None = None) -> None:
        self.digest = digest or InputDigest()

    def _ask_choice(
        self,
        title: str,
        why_it_matters: str,
        options: list[tuple[str, str]],
        ai_recommendation: str,
        default_index: int = 1,
    ) -> str:
        """Presenta una pregunta estructurada con opciones numeradas + AI + Campo abierto."""
        print(f"\n\033[1;34m[Pregunta]\033[0m \033[1m{title}\033[0m")
        print(f"\033[36m¿Por qué importa?\033[0m {why_it_matters}\n")

        for idx, (label, desc) in enumerate(options, start=1):
            rec_tag = " \033[1;32m(Recomendado)\033[0m" if idx == default_index else ""
            print(f"  \033[1m{idx}.\033[0m {label}{rec_tag}")
            if desc:
                print(f"     \033[90m└─ {desc}\033[0m")

        ai_opt_num = len(options) + 1
        custom_opt_num = len(options) + 2

        print(f"  \033[1m{ai_opt_num}.\033[0m 🤖 \033[1mDecidir por mí\033[0m: {ai_recommendation}")
        print(f"  \033[1m{custom_opt_num}.\033[0m ✏️  \033[1mCampo abierto\033[0m (escribir respuesta personalizada)")

        while True:
            try:
                raw = input(f"\nSelecciona una opción [1-{custom_opt_num}] (Enter para opción {default_index}): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nOperación cancelada.")
                sys.exit(1)

            if not raw:
                raw = str(default_index)

            if raw == str(ai_opt_num) or raw.lower() in ("ai", "ia", "robot"):
                print(f"\033[32m[IA]\033[0m Aplicando recomendación experta: \033[1m{ai_recommendation}\033[0m")
                return options[default_index - 1][0]

            if raw == str(custom_opt_num) or raw.lower() in ("custom", "otro", "personalizado"):
                try:
                    custom_text = input("Escribe tu especificación: ").strip()
                    if custom_text:
                        return custom_text
                except (EOFError, KeyboardInterrupt):
                    sys.exit(1)
                continue

            try:
                choice_idx = int(raw)
                if 1 <= choice_idx <= len(options):
                    return options[choice_idx - 1][0]
            except ValueError:
                # Si el usuario escribió directamente texto
                return raw

            print(f"\033[91mOpción inválida. Introduce un número entre 1 y {custom_opt_num}.\033[0m")

    def _ask_text(self, title: str, why_it_matters: str, default: str | None = None) -> str:
        """Pide texto libre pero con valor por defecto visible."""
        print(f"\n\033[1;34m[Pregunta]\033[0m \033[1m{title}\033[0m")
        print(f"\033[36m¿Por qué importa?\033[0m {why_it_matters}")
        prompt_label = f" (Enter para '{default}')" if default else ""
        while True:
            try:
                val = input(f"Respuesta{prompt_label}: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nOperación cancelada.")
                sys.exit(1)
            if val:
                return val
            if default:
                return default

    def collect(self) -> BootstrapManifest:
        """Ejecuta el protocolo de entrevista guiada de 5 fases."""
        print("\n" + "=" * 76)
        print("  \033[1;32mHARNESS LAUNCHER — ASISTENTE INTERACTIVO DE ARQUITECTURA (BOOTSTRAP)\033[0m")
        print("=" * 76)
        if self.digest.files_found:
            print(f"\033[1m[Documentación previa detectada]\033[0m {self.digest.raw_summary}")
        else:
            print("\033[90mNo se detectó documentación previa en .ai-harness/input. Procediendo en modo paso a paso.\033[0m")

        # ---------------------------------------------------------------------
        # FASE 1: Identidad del Producto
        # ---------------------------------------------------------------------
        def_name = self.digest.suggested_name or "MiProducto"
        name = self._ask_text(
            "Nombre oficial del proyecto",
            "Identifica el repositorio, logs y la spec raíz del sistema.",
            default=def_name,
        )

        slug = name.lower().replace(" ", "-").replace("_", "-")
        def_desc = self.digest.suggested_description or "Aplicación construida bajo arquitectura y contratos SDD."
        desc = self._ask_text(
            "Propuesta de valor / Descripción en una frase",
            "Define la misión principal del sistema en project_overview.md y README.md.",
            default=def_desc,
        )

        audience = self._ask_choice(
            "Público objetivo principal",
            "Determina el tono de la documentación y los criterios de experiencia de usuario.",
            [
                ("Usuarios finales (B2C / App de consumo)", "Enfoque en usabilidad, rapidez visual y tolerancia a fallos."),
                ("Empresas y equipos internos (B2B / SaaS)", "Enfoque en integridad de datos, seguridad y trazabilidad."),
                ("Desarrolladores y sistemas (Herramienta / API / CLI)", "Enfoque en contratos estrictos, documentación de API y stdout."),
            ],
            ai_recommendation="Usuarios finales (B2C / App de consumo) con foco en privacidad y autonomía.",
            default_index=1,
        )

        identity = ProjectIdentity(name=name, slug=slug, description=desc, target_audience=audience)

        # ---------------------------------------------------------------------
        # FASE 2: Stack Tecnológico y Plataformas
        # ---------------------------------------------------------------------
        stack_def_idx = 1
        if self.digest.detected_stack == "flutter":
            stack_def_idx = 1
        elif self.digest.detected_stack == "python":
            stack_def_idx = 2
        elif self.digest.detected_stack == "node":
            stack_def_idx = 3

        stack_choice = self._ask_choice(
            "Stack tecnológico principal",
            "Condiciona los linters, el validador preflight y las exclusiones de .gitignore.",
            [
                ("Flutter / Dart", "Multiplataforma para móvil, escritorio y web con alto rendimiento nativo."),
                ("Python (FastAPI / Poetry)", "Excelente para microservicios, APIs reactivas, IA o tooling backend."),
                ("Node / TypeScript (Next.js / Express)", "Estándar para aplicaciones web modernas y APIs ligeras."),
                ("Go (Golang)", "Servicios de alta concurrencia, bajo consumo de memoria y binarios únicos."),
                ("Genérico / A definir", "Arnés neutro agnóstico a cualquier tecnología."),
            ],
            ai_recommendation=f"Elegir '{self.digest.detected_framework or 'Flutter / Dart'}' por madurez multiplataforma y robustez tipada.",
            default_index=stack_def_idx,
        )

        if "Flutter" in stack_choice:
            stype = StackType.FLUTTER
            lang, fw, pkg_mgr = "Dart", "Flutter", "pub"
        elif "Python" in stack_choice:
            stype = StackType.PYTHON
            lang, fw, pkg_mgr = "Python", "FastAPI", "pip/poetry"
        elif "TypeScript" in stack_choice or "Node" in stack_choice:
            stype = StackType.NODE
            lang, fw, pkg_mgr = "TypeScript", "Node/Express", "pnpm"
        elif "Go" in stack_choice:
            stype = StackType.GO
            lang, fw, pkg_mgr = "Go", "Gin", "go modules"
        else:
            stype = StackType.GENERIC
            lang, fw, pkg_mgr = "Agnóstico", "Generic", "system"

        stack = TechStack(stack_type=stype, language=lang, framework=fw, package_manager=pkg_mgr)

        platforms_choice = self._ask_choice(
            "Plataformas objetivo donde correrá el producto",
            "Configura la platform_matrix.md y los requisitos de despliegue/arranque.",
            [
                ("Multiplataforma cliente (Android, iOS, Windows, Web)", "Cubre móvil, escritorio y navegadores."),
                ("Móvil nativo exclusivo (Android e iOS)", "Optimizado para teléfonos y tablets."),
                ("Servidor / Cloud Backend (Linux Container / Docker)", "Servicio sin pantalla corriendo en contenedores."),
                ("Escritorio exclusivo (Windows, macOS, Linux)", "Herramienta o estación de trabajo local."),
            ],
            ai_recommendation="Multiplataforma cliente (Android, iOS, Windows, Web) para máxima portabilidad.",
            default_index=1,
        )

        platform_list = ["Android", "iOS", "Windows", "Web"]
        if "Móvil nativo" in platforms_choice:
            platform_list = ["Android", "iOS"]
        elif "Servidor" in platforms_choice:
            platform_list = ["Linux", "Docker"]
        elif "Escritorio" in platforms_choice:
            platform_list = ["Windows", "macOS", "Linux"]

        # ---------------------------------------------------------------------
        # FASE 3: Arquitectura y Módulos (Scopes)
        # ---------------------------------------------------------------------
        arch_choice = self._ask_choice(
            "Estilo arquitectónico y organización de capas",
            "Establece las reglas de importación en architecture_rules.md y los checks de preflight.",
            [
                ("Clean Architecture (Domain, Application, Infrastructure, Presentation)", "Desacopla lógica de negocio pura de frameworks y bases de datos."),
                ("Modular Feature-First (Módulos autónomos por funcionalidad)", "Agrupa cada caso de uso con su UI y datos en carpetas independientes."),
                ("Hexagonal / Ports & Adapters", "Aislamiento estricto de adaptadores de entrada y salida."),
            ],
            ai_recommendation="Clean Architecture por su capacidad de probar el dominio sin depender de UI ni bases de datos.",
            default_index=1,
        )

        persistence_choice = self._ask_choice(
            "Mecanismo de persistencia y almacenamiento",
            "Registra la tecnología de datos en el arnés y bloquea librerías no deseadas.",
            [
                ("Base de datos local embebida (SQLite / Drift / Floor)", "Datos estructurados, offline-first y consultas SQL locales."),
                ("Persistencia remota en API / Backend externo", "La app no almacena grandes bases de datos locales, solo caché de sesión."),
                ("Almacenamiento Clave-Valor simple (Preferences / Hive)", "Configuraciones, tokens y datos no relacionales ligeros."),
                ("Sin persistencia (In-Memory o Stateless)", "Toda la información se destruye al cerrar el proceso."),
            ],
            ai_recommendation="Base de datos local embebida (SQLite) para garantizar experiencia offline.",
            default_index=1,
        )

        persistence = "sqlite" if "SQLite" in persistence_choice else "api" if "remota" in persistence_choice else "none"

        # Detección o selección de scopes
        default_scopes = [
            ScopeDefinition(
                name="core",
                title="Núcleo del Sistema (Core)",
                description="Infraestructura base, inyección de dependencias y utilidades compartidas.",
                path_roots=["lib/core", "src/core"],
                forbidden_paths=["lib/features", "lib/ui"],
            ),
            ScopeDefinition(
                name="domain",
                title="Capa de Dominio y Reglas de Negocio",
                description="Entidades, value objects, repositorios e invariantes puras.",
                path_roots=["lib/domain", "src/domain"],
                forbidden_paths=["lib/infrastructure", "lib/presentation", "lib/ui"],
            ),
            ScopeDefinition(
                name="ui",
                title="Capa de Presentación y Experiencia de Usuario",
                description="Pantallas, componentes visuales, consumo de estado y navegación.",
                path_roots=["lib/presentation", "lib/ui", "src/ui"],
                forbidden_paths=["lib/data", "lib/infrastructure"],
            ),
        ]

        # ---------------------------------------------------------------------
        # FASE 4: UI, Privacidad y Seguridad
        # ---------------------------------------------------------------------
        has_ui = stype in (StackType.FLUTTER, StackType.GENERIC, StackType.NODE)
        privacy_choice = self._ask_choice(
            "Política de telemetría y privacidad",
            "Queda grabada como límite infranqueable en security_privacy.md.",
            [
                ("Cero Telemetría Absoluta (Zero-telemetry)", "Ningún dato de usuario ni evento de analítica sale del dispositivo."),
                ("Reporte anónimo mínimo de crashes (Opt-in)", "Solo trazas técnicas anónimas de error previa autorización del usuario."),
            ],
            ai_recommendation="Cero Telemetría Absoluta para cumplir las directrices éticas del arnés.",
            default_index=1,
        )

        privacy = "zero_telemetry" if "Cero" in privacy_choice else "anonymous_crash_only"

        # ---------------------------------------------------------------------
        # FASE 5: Modos de Fallo Preventivos y Primer ADR
        # ---------------------------------------------------------------------
        failure_modes = [
            FailureModeItem(
                id="FM-01",
                title="Pérdida de foco y accesibilidad en navegación",
                symptom="El usuario con teclado o mando no puede seleccionar botones o queda atrapado en un bucle.",
                root_cause="La IA no declara FocusNodes explícitos ni gestiona la tecla Tab.",
                mitigation="Toda vista debe incorporar pruebas de recorrido de foco y controles navegables.",
            ),
            FailureModeItem(
                id="FM-02",
                title="Valores visuales literales fuera del sistema de tokens",
                symptom="Colores HEX, márgenes o fuentes hardcodeados directamente en widgets o componentes.",
                root_cause="La IA usa colores directos (ej. Colors.blue) en lugar de consultar tokens.json.",
                mitigation="Preflight rechaza cualquier commit con valores literales en capas de presentación.",
            ),
            FailureModeItem(
                id="FM-03",
                title="Fugas de memoria en suscripciones asíncronas no canceladas",
                symptom="Consumo progresivo de RAM al cambiar repetidamente de pantalla.",
                root_cause="La IA inicializa Streams, Listeners o Controladores sin destruirlos en el dispose().",
                mitigation="Regla obligatoria de paridad: cada suscripción en initState/setup tiene su desuscripción en dispose/cleanup.",
            ),
            FailureModeItem(
                id="FM-04",
                title="Acoplamiento indebido de infraestructura en la capa de dominio",
                symptom="Las entidades o casos de uso importan librerías de bases de datos o frameworks visuales.",
                root_cause="La IA intenta resolver rápido un problema llamando a la BD directamente desde la lógica.",
                mitigation="El dominio solo conoce interfaces (puertos) y nunca implementaciones de infraestructura.",
            ),
            FailureModeItem(
                id="FM-05",
                title="Inconsistencia de estado por falta de manejo de errores en llamadas I/O",
                symptom="La pantalla se congela o queda en estado de carga infinito si la red o disco fallan.",
                root_cause="La IA asume operaciones síncronas o no captura excepciones en bloques try/catch/Result.",
                mitigation="Toda operación asíncrona debe retornar un tipo Result/Either o capturar y propagar el fallo.",
            ),
        ]

        adr_0001 = ADRItem(
            id="ADR-0001",
            title=f"Elección de stack base ({stack.language} / {stack.framework}) y arquitectura {arch_choice.split('(')[0].strip()}",
            status="Aceptada",
            context=f"Inicio del desarrollo de {name}. Se requiere una base robusta para {identity.description} dirigida a {identity.target_audience}.",
            decision=f"Adoptar {stack.language} con framework {stack.framework} siguiendo {arch_choice.split('(')[0].strip()}.",
            consequences=f"Desarrollo desacoplado y verificable mediante Spec-Driven Development; preflight validará las invariantes.",
        )

        return BootstrapManifest(
            identity=identity,
            stack=stack,
            architecture=ArchitectureConfig(
                style=arch_choice.split("(")[0].strip(),
                persistence=persistence,
            ),
            scopes=default_scopes,
            platform=PlatformConfig(platforms=platform_list, privacy_policy=privacy),
            ui=UIConfig(has_ui=has_ui),
            failure_modes=failure_modes,
            adr_0001=adr_0001,
            referenced_documents=self.digest.files_found,
        )

