"""Check 05: Forbidden Flutter dependencies."""

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

from common import find_project_root, read_text
from harness_config import load_config
from models import CheckResult, CheckStatus, CheckViolation

SECTIONS = ("dependencies:", "dev_dependencies:")


def _declared_packages(content: str) -> set[str]:
    packages: set[str] = set()
    in_section = False
    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        if any(line.startswith(section) for section in SECTIONS):
            in_section = True
            continue
        if in_section and line and not line.startswith((" ", "\t")):
            in_section = False
        if not in_section or ":" not in line:
            continue
        key = line.split(":", 1)[0].strip()
        if re.fullmatch(r"[a-z0-9_]+", key):
            packages.add(key)
    return packages


def run(scope_path: Path, strict: bool = False) -> CheckResult:
    start = time.perf_counter()
    violations: list[CheckViolation] = []
    root = find_project_root(scope_path)

    if root is None:
        return CheckResult(
            check_name="05_dependencies",
            status=CheckStatus.WARNING,
            violations=[
                CheckViolation(
                    file_path=scope_path,
                    rule_id="FLUTTER-PROJECT-MISSING",
                    message="No pubspec.yaml found. Dependency checks were skipped.",
                )
            ],
            execution_time_ms=(time.perf_counter() - start) * 1000.0,
        )

    pubspec = root / "pubspec.yaml"
    packages = _declared_packages(read_text(pubspec))
    configured = load_config(root)["architecture"].get("forbidden_packages", []) or []
    forbidden_packages = {str(name) for name in configured}
    for package in sorted(packages & forbidden_packages):
        violations.append(
            CheckViolation(
                file_path=pubspec,
                rule_id="DEP-FORBIDDEN",
                message=(
                    f"Forbidden dependency '{package}': declared in "
                    "architecture.forbidden_packages (harness.config.yaml)."
                ),
            )
        )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    return CheckResult(
        check_name="05_dependencies",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
