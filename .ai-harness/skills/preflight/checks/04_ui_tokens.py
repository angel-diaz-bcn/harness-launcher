"""Check 04: Design-token discipline and TV focus presence."""

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

COLOR_PATTERNS = (
    re.compile(r"Color\s*\(\s*0x[0-9A-Fa-f]{6,8}"),
    re.compile(r"Color\.fromARGB\s*\("),
    re.compile(r"\bColors\.[A-Za-z]+\b"),
)


def run(scope_path: Path, strict: bool = False) -> CheckResult:
    start = time.perf_counter()
    violations: list[CheckViolation] = []
    root = find_project_root(scope_path)

    if root is None:
        return CheckResult(
            check_name="04_ui_tokens",
            status=CheckStatus.WARNING,
            violations=[
                CheckViolation(
                    file_path=scope_path,
                    rule_id="FLUTTER-PROJECT-MISSING",
                    message="No pubspec.yaml found. UI token checks were skipped.",
                )
            ],
            execution_time_ms=(time.perf_counter() - start) * 1000.0,
        )

    tv_dir = root / "lib" / "features" / "tv_experience"
    tv_uses_focus = False
    tv_has_code = any(
        path.relative_to(root).as_posix().startswith("lib/features/tv_experience/")
        for path in dart_files(root, "lib")
    )

    for path in dart_files(root, "lib"):
        relative = path.relative_to(root).as_posix()
        content = read_text(path)

        if relative.startswith("lib/app/theme/"):
            continue

        for pattern in COLOR_PATTERNS:
            for match in pattern.finditer(content):
                line = content[: match.start()].count("\n") + 1
                violations.append(
                    CheckViolation(
                        file_path=path,
                        line_number=line,
                        rule_id="UI-HARDCODED-COLOR",
                        message="Use tokens from ui-design-system.md; hardcoded colors are forbidden.",
                    )
                )

        if relative.startswith("lib/features/tv_experience/") and (
            "FocusNode" in content or "FocusScope" in content or "Focus(" in content
        ):
            tv_uses_focus = True

    if tv_dir.exists() and tv_has_code and not tv_uses_focus:
        violations.append(
            CheckViolation(
                file_path=tv_dir,
                rule_id="UI-FOCUS-MISSING",
                message="tv_experience must implement FocusNode/FocusScope navigation.",
            )
        )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    return CheckResult(
        check_name="04_ui_tokens",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
