"""Check 01: límites entre features, imports exclusivos y persistencia.

Las features, sus fronteras, los imports exclusivos y la propiedad de la
persistencia local se leen de `harness.config.yaml`. El check no conoce ningún
producto concreto: aplica el contrato de arquitectura declarado.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

preflight_dir = Path(__file__).resolve().parent.parent
if str(preflight_dir) not in sys.path:
    sys.path.insert(0, str(preflight_dir))
checks_dir = Path(__file__).resolve().parent
if str(checks_dir) not in sys.path:
    sys.path.insert(0, str(checks_dir))

from common import (
    dart_files,
    feature_of,
    find_project_root,
    import_paths,
    pubspec_name,
    read_text,
)
from harness_config import load_config
from models import CheckResult, CheckStatus, CheckViolation


def _warn(scope_path: Path, start: float, message: str) -> CheckResult:
    return CheckResult(
        check_name="01_architecture",
        status=CheckStatus.WARNING,
        violations=[
            CheckViolation(
                file_path=scope_path,
                rule_id="PROJECT-MISSING",
                message=message,
            )
        ],
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )


def run(scope_path: Path, strict: bool = False) -> CheckResult:
    start = time.perf_counter()
    violations: list[CheckViolation] = []

    root = find_project_root(scope_path)
    if root is None:
        return _warn(
            scope_path,
            start,
            "No manifest file found. Architecture checks were skipped.",
        )

    rules = load_config(root)["architecture"]
    features = {str(f) for f in rules.get("features", []) or []}
    forbidden_by_feature = {
        str(key): {str(x) for x in (value or [])}
        for key, value in (rules.get("forbidden_by_feature") or {}).items()
    }
    exclusive = {
        str(key): str(value)
        for key, value in (rules.get("exclusive_import_paths") or {}).items()
    }
    framework_prefix = str(rules.get("framework_import_prefix", "") or "")
    framework_free = {str(f) for f in rules.get("framework_free_features", []) or []}
    persistence_feature = str(rules.get("persistence_feature", "") or "")
    persistence_imports = [str(x) for x in rules.get("persistence_imports", []) or []]

    package = pubspec_name(root)

    for path in dart_files(root, "lib"):
        relative = path.relative_to(root).as_posix()
        feature = feature_of(path, root)
        content = read_text(path)

        for line, imported in import_paths(content):
            if imported.startswith(f"package:{package}/features/"):
                remainder = imported.split(f"package:{package}/features/", 1)[1]
                other = remainder.split("/", 1)[0]
                if feature and other != feature:
                    public_barrel = f"package:{package}/features/{other}/{other}.dart"
                    if imported != public_barrel:
                        violations.append(
                            CheckViolation(
                                file_path=path,
                                line_number=line,
                                rule_id="ARCH-CROSS-FEATURE-IMPORT",
                                message=(
                                    f"Feature '{feature}' imports internals of '{other}'. "
                                    f"Use the public barrel '{public_barrel}'."
                                ),
                            )
                        )

            if (
                framework_prefix
                and feature in framework_free
                and imported.startswith(framework_prefix)
            ):
                violations.append(
                    CheckViolation(
                        file_path=path,
                        line_number=line,
                        rule_id="ARCH-FRAMEWORK-LEAK",
                        message=(
                            f"Feature '{feature}' is framework-free and cannot import "
                            f"'{framework_prefix}'."
                        ),
                    )
                )

            for module, allowed_path in exclusive.items():
                if imported.startswith(f"package:{module}") and (
                    not allowed_path or allowed_path not in relative
                ):
                    violations.append(
                        CheckViolation(
                            file_path=path,
                            line_number=line,
                            rule_id="ARCH-EXCLUSIVE-IMPORT",
                            message=(
                                f"'{module}' may only be imported inside "
                                f"'{allowed_path or '(sin ruta declarada)'}'."
                            ),
                        )
                    )

            for forbidden in sorted(forbidden_by_feature.get(feature or "", set())):
                if forbidden and forbidden in imported:
                    violations.append(
                        CheckViolation(
                            file_path=path,
                            line_number=line,
                            rule_id="ARCH-FEATURE-BOUNDARY",
                            message=f"Feature '{feature}' cannot import '{forbidden}'.",
                        )
                    )

        if relative.startswith("lib/core/"):
            for line, imported in import_paths(content):
                if "/features/" in imported:
                    violations.append(
                        CheckViolation(
                            file_path=path,
                            line_number=line,
                            rule_id="ARCH-CORE-IMPORTS-FEATURE",
                            message="lib/core cannot import lib/features.",
                        )
                    )

        if persistence_imports and feature != persistence_feature:
            for module in persistence_imports:
                if module in content:
                    violations.append(
                        CheckViolation(
                            file_path=path,
                            rule_id="ARCH-PERSISTENCE-LEAK",
                            message=(
                                "Local persistence belongs to "
                                f"lib/features/{persistence_feature or '<owner>'}."
                            ),
                        )
                    )

        if feature is not None and features and feature not in features:
            violations.append(
                CheckViolation(
                    file_path=path,
                    rule_id="ARCH-UNKNOWN-FEATURE",
                    message=(
                        f"Feature '{feature}' is not declared in "
                        "architecture.features (harness.config.yaml)."
                    ),
                )
            )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    return CheckResult(
        check_name="01_architecture",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )

