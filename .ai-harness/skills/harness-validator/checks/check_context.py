"""Check Context: FLIK context and scope integrity."""

from __future__ import annotations

import re
import time
from pathlib import Path

try:
    from models import SubCheckResult, ValidationStatus, ValidationViolation
except ImportError:
    from .models import SubCheckResult, ValidationStatus, ValidationViolation

REQUIRED_CONTEXT_FILES = [
    "architecture_rules.md",
    "coding_standards.md",
    "glossary.md",
    "harness_governance.md",
    "platform_matrix.md",
    "project_overview.md",
    "project_structure.md",
    "sdd_framework.md",
    "security_privacy.md",
    "system_identity.md",
    "testing_guidelines.md",
    "ui-design-system.md",
]

REQUIRED_SCOPE_FILES = [
    "block_app_core.md",
    "block_catalog_service.md",
    "block_media_player.md",
    "block_p2p_engine.md",
    "block_ui_navigation_engine.md",
]

LEGACY_TERMS = [
    "Kronos",
    "Polars",
    "Parquet",
    "CCXT",
    "TradingView",
    "FastAPI",
    "Vite",
    "apps/web_console",
    "apps/server_api",
    "packages/shared",
    "CMP-BE",
]

PENDING_MARKERS = re.compile(r"\b(TODO|TBD|FIXME)\b")


def _check_file(
    path: Path,
    component: str,
    violations: list[ValidationViolation],
    *,
    require_no_legacy: bool = True,
) -> None:
    if not path.exists():
        violations.append(
            ValidationViolation(
                component=component,
                file_path=path,
                rule_id=f"{component.upper()}-MISSING-FILE",
                message=f"Mandatory file '{path.name}' does not exist.",
                severity="ERROR",
            )
        )
        return

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, ValueError) as exc:
        violations.append(
            ValidationViolation(
                component=component,
                file_path=path,
                rule_id=f"{component.upper()}-READ-ERROR",
                message=f"Failed to read file: {exc}",
                severity="ERROR",
            )
        )
        return

    if len(content.strip()) < 200:
        violations.append(
            ValidationViolation(
                component=component,
                file_path=path,
                rule_id=f"{component.upper()}-INSUFFICIENT-CONTENT",
                message="File is under the minimum content threshold (200 chars).",
                severity="ERROR",
            )
        )

    markers = sorted({m.group(0) for m in PENDING_MARKERS.finditer(content)})
    if markers:
        violations.append(
            ValidationViolation(
                component=component,
                file_path=path,
                rule_id=f"{component.upper()}-PENDING-MARKERS",
                message=f"Pending markers found: {', '.join(markers)}.",
                severity="ERROR",
            )
        )

    if require_no_legacy:
        found = [term for term in LEGACY_TERMS if term.lower() in content.lower()]
        if found:
            violations.append(
                ValidationViolation(
                    component=component,
                    file_path=path,
                    rule_id=f"{component.upper()}-LEGACY-TERMS",
                    message=f"Legacy project terms found: {', '.join(found)}.",
                    severity="ERROR",
                )
            )


def run(harness_root: Path, strict: bool = False, fix: bool = False) -> SubCheckResult:
    start = time.perf_counter()
    violations: list[ValidationViolation] = []

    harness_dir = harness_root / ".ai-harness" if harness_root.name != ".ai-harness" else harness_root
    workspace = harness_dir.parent
    context_dir = harness_dir / "context"
    scopes_dir = harness_dir / "scopes"

    for filename in REQUIRED_CONTEXT_FILES:
        _check_file(context_dir / filename, "context", violations)

    for filename in REQUIRED_SCOPE_FILES:
        path = scopes_dir / filename
        _check_file(path, "scope", violations, require_no_legacy=True)
        if path.exists():
            content = path.read_text(encoding="utf-8", errors="ignore")
            if "packages/" in content or "apps/flik_app" in content:
                violations.append(
                    ValidationViolation(
                        component="scope",
                        file_path=path,
                        rule_id="SCOPE-LEGACY-PATH",
                        message="Scope must point to lib/features, not packages/ or apps/flik_app.",
                        severity="ERROR",
                    )
                )
            if "lib/" not in content:
                violations.append(
                    ValidationViolation(
                        component="scope",
                        file_path=path,
                        rule_id="SCOPE-MISSING-LIB-PATH",
                        message="Scope must declare an authorized path under lib/.",
                        severity="ERROR",
                    )
                )

    agents = workspace / "AGENTS.md"
    _check_file(agents, "agents", violations)
    if agents.exists():
        content = agents.read_text(encoding="utf-8", errors="ignore")
        for required in ("harness_governance.md", "system_identity.md"):
            if required not in content:
                violations.append(
                    ValidationViolation(
                        component="agents",
                        file_path=agents,
                        rule_id="AGENTS-MISSING-REFERENCE",
                        message=f"AGENTS.md must reference {required}.",
                        severity="ERROR",
                    )
                )

    has_error = any(v.severity == "ERROR" for v in violations)
    has_warning = any(v.severity == "WARNING" for v in violations)
    status = (
        ValidationStatus.FAILED
        if has_error or (strict and has_warning)
        else (ValidationStatus.WARNING if has_warning else ValidationStatus.PASSED)
    )

    return SubCheckResult(
        check_name="check_context",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
