"""Check 00: Dart formatting, Flutter analyze and Flutter tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

preflight_dir = Path(__file__).resolve().parent.parent
if str(preflight_dir) not in sys.path:
    sys.path.insert(0, str(preflight_dir))
checks_dir = Path(__file__).resolve().parent
if str(checks_dir) not in sys.path:
    sys.path.insert(0, str(checks_dir))

from common import find_project_root
from models import CheckResult, CheckStatus, CheckViolation


def _run(command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=timeout,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return None


def run(scope_path: Path, strict: bool = False) -> CheckResult:
    start = time.perf_counter()
    violations: list[CheckViolation] = []
    root = find_project_root(scope_path)

    if root is None:
        violations.append(
            CheckViolation(
                file_path=scope_path,
                rule_id="FLUTTER-PROJECT-MISSING",
                message="No pubspec.yaml found. Flutter quality checks were skipped.",
            )
        )
        return CheckResult(
            check_name="00_code_quality",
            status=CheckStatus.WARNING,
            violations=violations,
            execution_time_ms=(time.perf_counter() - start) * 1000.0,
        )

    if shutil.which("dart") is None:
        violations.append(
            CheckViolation(
                file_path=root / "pubspec.yaml",
                rule_id="DART-MISSING",
                message="Dart SDK not found in PATH.",
            )
        )
    else:
        targets = [name for name in ("lib", "test", "integration_test") if (root / name).exists()]
        if targets:
            result = _run(
                ["dart", "format", "--output=none", "--set-exit-if-changed", *targets],
                root,
                90,
            )
            if result and result.returncode != 0:
                for line in (result.stdout + result.stderr).splitlines():
                    if line.strip() and ("Changed" in line or "would change" in line.lower()):
                        violations.append(
                            CheckViolation(
                                file_path=root,
                                rule_id="DART-FORMAT",
                                message=line.strip(),
                            )
                        )
                if not any(v.rule_id == "DART-FORMAT" for v in violations):
                    violations.append(
                        CheckViolation(
                            file_path=root,
                            rule_id="DART-FORMAT",
                            message="dart format reported unformatted files.",
                        )
                    )

    if shutil.which("flutter") is None:
        violations.append(
            CheckViolation(
                file_path=root / "pubspec.yaml",
                rule_id="FLUTTER-MISSING",
                message="Flutter SDK not found in PATH.",
            )
        )
    else:
        analyze = _run(["flutter", "analyze", "--no-pub"], root, 180)
        if analyze and analyze.returncode != 0:
            for line in (analyze.stdout + analyze.stderr).splitlines():
                if "error •" in line or "error:" in line or "warning •" in line:
                    violations.append(
                        CheckViolation(
                            file_path=root,
                            rule_id="FLUTTER-ANALYZE",
                            message=line.strip(),
                        )
                    )
            if not violations:
                violations.append(
                    CheckViolation(
                        file_path=root,
                        rule_id="FLUTTER-ANALYZE",
                        message="flutter analyze failed.",
                    )
                )

        if (root / "test").exists():
            tests = _run(["flutter", "test", "--no-pub"], root, 300)
            if tests and tests.returncode != 0:
                violations.append(
                    CheckViolation(
                        file_path=root / "test",
                        rule_id="FLUTTER-TEST",
                        message="flutter test failed. Run it directly for the full trace.",
                    )
                )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    if violations and all(v.rule_id in {"FLUTTER-PROJECT-MISSING", "DART-MISSING", "FLUTTER-MISSING"} for v in violations):
        status = CheckStatus.WARNING if not strict else CheckStatus.FAILED

    return CheckResult(
        check_name="00_code_quality",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
