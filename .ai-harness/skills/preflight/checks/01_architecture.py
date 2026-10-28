"""Check 01: Feature boundaries and forbidden imports."""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

preflight_dir = Path(__file__).resolve().parent.parent
if str(preflight_dir) not in sys.path:
    sys.path.insert(0, str(preflight_dir))
checks_dir = Path(__file__).resolve().parent
if str(checks_dir) not in sys.path:
    sys.path.insert(0, str(checks_dir))

from common import dart_files, feature_of, find_project_root, import_paths, pubspec_name, read_text
from models import CheckResult, CheckStatus, CheckViolation

FEATURES = {"catalog", "player", "p2p_engine", "tv_experience"}
FORBIDDEN_BY_FEATURE = {
    "catalog": {"media_kit", "player", "p2p_engine", "tv_experience"},
    "player": {"catalog", "p2p_engine", "tv_experience"},
    "p2p_engine": {"catalog", "player", "tv_experience"},
}


def run(scope_path: Path, strict: bool = False) -> CheckResult:
    start = time.perf_counter()
    violations: list[CheckViolation] = []
    root = find_project_root(scope_path)

    if root is None:
        return CheckResult(
            check_name="01_architecture",
            status=CheckStatus.WARNING,
            violations=[
                CheckViolation(
                    file_path=scope_path,
                    rule_id="FLUTTER-PROJECT-MISSING",
                    message="No pubspec.yaml found. Architecture checks were skipped.",
                )
            ],
            execution_time_ms=(time.perf_counter() - start) * 1000.0,
        )

    package = pubspec_name(root)
    files = dart_files(root, "lib")

    for path in files:
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

            if feature == "p2p_engine" and imported.startswith("package:flutter/"):
                violations.append(
                    CheckViolation(
                        file_path=path,
                        line_number=line,
                        rule_id="ARCH-P2P-FLUTTER",
                        message="p2p_engine cannot depend on Flutter widgets/services.",
                    )
                )

            if imported.startswith("package:media_kit") and "/data/media_kit/" not in relative:
                violations.append(
                    CheckViolation(
                        file_path=path,
                        line_number=line,
                        rule_id="ARCH-MEDIA-KIT-LEAK",
                        message="media_kit may only be imported inside lib/features/player/data/media_kit/.",
                    )
                )

            if feature in FORBIDDEN_BY_FEATURE:
                for forbidden in FORBIDDEN_BY_FEATURE[feature]:
                    token = forbidden if forbidden != "media_kit" else "media_kit"
                    if token in imported and not (feature == "player" and token == "media_kit"):
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

        if feature not in FEATURES and feature is not None:
            violations.append(
                CheckViolation(
                    file_path=path,
                    rule_id="ARCH-UNKNOWN-FEATURE",
                    message=f"Feature '{feature}' is not declared in project_structure.md.",
                )
            )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    return CheckResult(
        check_name="01_architecture",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
