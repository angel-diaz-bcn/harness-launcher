"""Check 04: disciplina de tokens visuales y navegación por foco.

La feature que concentra la navegación por foco se lee de `ui.token_feature`
en `harness.config.yaml`. Los colores literales se bloquean en todo `lib/`
salvo en la implementación del tema, que es donde viven los tokens.
"""

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
from harness_config import load_config
from models import CheckResult, CheckStatus, CheckViolation

COLOR_PATTERNS = (
    re.compile(r"Color\s*\(\s*0x[0-9A-Fa-f]{6,8}"),
    re.compile(r"Color\.fromARGB\s*\("),
    re.compile(r"\bColors\.[A-Za-z]+\b"),
)
THEME_PATH = "lib/app/theme/"
FOCUS_MARKERS = ("FocusNode", "FocusScope", "Focus(")


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
                    rule_id="PROJECT-MISSING",
                    message="No manifest file found. UI token checks were skipped.",
                )
            ],
            execution_time_ms=(time.perf_counter() - start) * 1000.0,
        )

    config = load_config(root)
    focus_feature = str(config["ui"].get("token_feature", "") or "").strip()
    focus_dir = root / "lib" / "features" / focus_feature if focus_feature else None
    focus_uses_focus = False
    files = dart_files(root, "lib")
    focus_has_code = bool(focus_feature) and any(
        path.relative_to(root).as_posix().startswith(f"lib/features/{focus_feature}/")
        for path in files
    )

    for path in files:
        relative = path.relative_to(root).as_posix()
        content = read_text(path)

        if not relative.startswith(THEME_PATH):
            for pattern in COLOR_PATTERNS:
                for match in pattern.finditer(content):
                    line = content[: match.start()].count("\n") + 1
                    violations.append(
                        CheckViolation(
                            file_path=path,
                            line_number=line,
                            rule_id="UI-HARDCODED-COLOR",
                            message=(
                                "Use tokens from ui-design-system.md; "
                                "hardcoded colors are forbidden."
                            ),
                        )
                    )

        if (
            focus_feature
            and relative.startswith(f"lib/features/{focus_feature}/")
            and any(marker in content for marker in FOCUS_MARKERS)
        ):
            focus_uses_focus = True

    if focus_dir is not None and focus_dir.exists() and focus_has_code and not focus_uses_focus:
        violations.append(
            CheckViolation(
                file_path=focus_dir,
                rule_id="UI-FOCUS-MISSING",
                message=(
                    f"'{focus_feature}' must implement FocusNode/FocusScope navigation."
                ),
            )
        )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    return CheckResult(
        check_name="04_ui_tokens",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
