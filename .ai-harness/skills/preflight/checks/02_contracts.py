"""Check 02: Dart immutability and error-handling hygiene."""

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

from common import dart_files, find_project_root, read_text
from models import CheckResult, CheckStatus, CheckViolation

VAR_FIELD = re.compile(r"^\s*var\s+[A-Za-z_]\w*\s*;", re.MULTILINE)
DYNAMIC = re.compile(r"\bdynamic\b")
EMPTY_CATCH = re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}", re.DOTALL)
PRINT = re.compile(r"(?<![\w.])print\s*\(")


def run(scope_path: Path, strict: bool = False) -> CheckResult:
    start = time.perf_counter()
    violations: list[CheckViolation] = []
    root = find_project_root(scope_path)

    if root is None:
        return CheckResult(
            check_name="02_contracts",
            status=CheckStatus.WARNING,
            violations=[
                CheckViolation(
                    file_path=scope_path,
                    rule_id="FLUTTER-PROJECT-MISSING",
                    message="No pubspec.yaml found. Contract checks were skipped.",
                )
            ],
            execution_time_ms=(time.perf_counter() - start) * 1000.0,
        )

    for path in dart_files(root, "lib"):
        content = read_text(path)
        relative = path.relative_to(root).as_posix()

        if "/domain/" in relative or "/data/" in relative:
            for match in VAR_FIELD.finditer(content):
                line = content[: match.start()].count("\n") + 1
                violations.append(
                    CheckViolation(
                        file_path=path,
                        line_number=line,
                        rule_id="DART-MUTABLE-FIELD",
                        message="Domain/model fields must be final or immutable.",
                    )
                )

        if "/domain/" in relative:
            for match in DYNAMIC.finditer(content):
                line = content[: match.start()].count("\n") + 1
                violations.append(
                    CheckViolation(
                        file_path=path,
                        line_number=line,
                        rule_id="DART-DYNAMIC-DOMAIN",
                        message="dynamic is forbidden in the domain layer.",
                    )
                )

        if EMPTY_CATCH.search(content):
            violations.append(
                CheckViolation(
                    file_path=path,
                    rule_id="DART-EMPTY-CATCH",
                    message="Empty catch detected; handle or log the error.",
                )
            )

        if PRINT.search(content):
            violations.append(
                CheckViolation(
                    file_path=path,
                    rule_id="DART-PRINT",
                    message="print() is forbidden; use the core logger.",
                )
            )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    return CheckResult(
        check_name="02_contracts",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
