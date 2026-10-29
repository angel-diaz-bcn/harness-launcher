"""
Bootstrap Harness Data Models (Pydantic V2).
"""

from __future__ import annotations

from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field


class StackType(StrEnum):
    GENERIC = "generic"
    FLUTTER = "flutter"
    DART = "dart"
    PYTHON = "python"
    NODE = "node"
    GO = "go"
    RUST = "rust"


class ProjectIdentity(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Nombre comercial del producto")
    slug: str = Field(..., description="Identificador corto en minúsculas y guiones")
    description: str = Field(..., description="Propuesta de valor en una o dos frases")
    target_audience: str = Field(
        default="Usuarios finales y desarrolladores",
        description="Público objetivo o tipo de usuario principal",
    )


class TechStack(BaseModel):
    model_config = ConfigDict(frozen=True)

    stack_type: StackType = Field(default=StackType.GENERIC, description="Tipo de stack base")
    language: str = Field(..., description="Lenguaje de programación principal")
    framework: str = Field(default="", description="Framework de desarrollo (ej. Flutter, FastAPI, Express)")
    package_manager: str = Field(default="", description="Gestor de paquetes (pub, poetry, pip, pnpm)")
    min_runtime_version: str = Field(default="", description="Versión mínima del runtime")


class ArchitectureConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    style: str = Field(default="Clean Architecture", description="Estilo arquitectónico")
    layers: list[str] = Field(
        default_factory=lambda: ["domain", "application", "infrastructure", "presentation"],
        description="Capas ordenadas del sistema",
    )
    persistence: str = Field(default="none", description="Motor de persistencia (ej. sqlite, postgres, none)")
    forbidden_packages: list[str] = Field(
        default_factory=lambda: [
            "firebase_analytics",
            "sentry_flutter",
            "amplitude_flutter",
            "google_analytics",
        ],
        description="Paquetes cuya importación está vetada",
    )
    forbidden_imports: list[str] = Field(
        default_factory=list,
        description="Reglas de importación prohibidas entre capas",
    )


class ScopeDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Nombre del módulo (ej. auth, catalog, core)")
    title: str = Field(..., description="Título legible del scope")
    description: str = Field(..., description="Responsabilidad del bloque funcional")
    path_roots: list[str] = Field(default_factory=list, description="Directorios autorizados")
    forbidden_paths: list[str] = Field(default_factory=list, description="Directorios prohibidos")


class PlatformConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    platforms: list[str] = Field(
        default_factory=lambda: ["Android", "iOS", "Windows", "Web"],
        description="Plataformas objetivo",
    )
    privacy_policy: str = Field(
        default="zero_telemetry",
        description="Política de telemetría (zero_telemetry, anonymous_crash_only)",
    )
    secrets_management: str = Field(
        default="env_vars",
        description="Estrategia de gestión de secretos",
    )


class UIConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    has_ui: bool = Field(default=True, description="Indica si el sistema incluye interfaz gráfica")
    theme_preference: str = Field(default="dark", description="Preferencia de tema (dark, light, adaptive)")
    focus_navigation_required: bool = Field(
        default=True,
        description="Exigir navegación por foco universal (teclado / D-Pad)",
    )


class FailureModeItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(..., description="Identificador FM-NN")
    title: str = Field(..., description="Título del modo de fallo")
    symptom: str = Field(..., description="Cómo se manifiesta el fallo")
    root_cause: str = Field(..., description="Causa raíz técnica o asunción incorrecta de la IA")
    mitigation: str = Field(..., description="Regla preventiva y verificación")


class ADRItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(default="ADR-0001", description="Identificador de la decisión")
    title: str = Field(..., description="Título de la decisión arquitectónica")
    status: str = Field(default="Aceptada", description="Estado de la decisión")
    context: str = Field(..., description="Contexto técnico y fuerzas en juego")
    decision: str = Field(..., description="Decisión adoptada")
    consequences: str = Field(..., description="Consecuencias positivas y negativas")


class BootstrapManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    identity: ProjectIdentity
    stack: TechStack
    architecture: ArchitectureConfig
    scopes: list[ScopeDefinition]
    platform: PlatformConfig
    ui: UIConfig
    failure_modes: list[FailureModeItem]
    adr_0001: ADRItem
    referenced_documents: list[str] = Field(
        default_factory=list,
        description="Documentos de .ai-harness/input analizados para alimentar el arnés",
    )

