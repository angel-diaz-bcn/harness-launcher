"""Check 03: FLIK P2P/streaming invariants."""

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

from common import dart_files, feature_of, find_project_root, read_text
from models import CheckResult, CheckStatus, CheckViolation

FORBIDDEN = {
    "0.0.0.0": "SEC-NON-LOOPBACK-BIND",
    "apps/server_api": "ARCH-BACKEND-LEAK",
    "fastapi": "ARCH-BACKEND-LEAK",
    "uvicorn": "ARCH-BACKEND-LEAK",
    "transcod": "P2P-TRANSCODING",
    "sentry_flutter": "PRIVACY-REMOTE-TELEMETRY",
    "firebase": "PRIVACY-REMOTE-TELEMETRY",
    "google_analytics": "PRIVACY-REMOTE-TELEMETRY",
    "mixpanel": "PRIVACY-REMOTE-TELEMETRY",
    "amplitude": "PRIVACY-REMOTE-TELEMETRY",
}
DB_IMPORTS = ("package:hive", "package:sqflite", "package:drift", "package:sqlite3")
BIND_PATTERN = re.compile(r"HttpServer\.bind\s*\(([^)]*)\)", re.DOTALL)


def run(scope_path: Path, strict: bool = False) -> CheckResult:
    start = time.perf_counter()
    violations: list[CheckViolation] = []
    root = find_project_root(scope_path)

    if root is None:
        return CheckResult(
            check_name="03_p2p_invariants",
            status=CheckStatus.WARNING,
            violations=[
                CheckViolation(
                    file_path=scope_path,
                    rule_id="FLUTTER-PROJECT-MISSING",
                    message="No pubspec.yaml found. P2P invariants were skipped.",
                )
            ],
            execution_time_ms=(time.perf_counter() - start) * 1000.0,
        )

    files = dart_files(root, "lib")
    p2p_has_endpoint = False

    for path in files:
        content = read_text(path)
        feature = feature_of(path, root)
        relative = path.relative_to(root).as_posix()

        for token, rule in FORBIDDEN.items():
            if token in content.lower():
                violations.append(
                    CheckViolation(
                        file_path=path,
                        rule_id=rule,
                        message=f"Forbidden P2P/architecture token detected: '{token}'.",
                    )
                )

        if feature == "p2p_engine":
            if "127.0.0.1" in content and "8888" in content and "stream" in content:
                p2p_has_endpoint = True
            for match in BIND_PATTERN.finditer(content):
                bind_args = match.group(1)
                if "loopbackIPv4" not in bind_args and "127.0.0.1" not in bind_args:
                    line = content[: match.start()].count("\n") + 1
                    violations.append(
                        CheckViolation(
                            file_path=path,
                            line_number=line,
                            rule_id="SEC-NON-LOOPBACK-BIND",
                            message="HttpServer must bind to 127.0.0.1 or InternetAddress.loopbackIPv4.",
                        )
                    )

        if feature != "catalog" and any(db in content for db in DB_IMPORTS):
            violations.append(
                CheckViolation(
                    file_path=path,
                    rule_id="ARCH-DB-OUTSIDE-CATALOG",
                    message="Local database access belongs to lib/features/catalog.",
                )
            )

        if feature == "player" and ("http://" in content or "https://" in content):
            for match in re.finditer(r"https?://[^\s'\"\)]+", content):
                url = match.group(0)
                if "127.0.0.1" not in url and "localhost" not in url:
                    line = content[: match.start()].count("\n") + 1
                    violations.append(
                        CheckViolation(
                            file_path=path,
                            line_number=line,
                            rule_id="PLAYER-REMOTE-STREAM",
                            message="The player must consume only the local P2P stream.",
                        )
                    )

        if relative.startswith("lib/features/p2p_engine/") and "media_kit" in content:
            violations.append(
                CheckViolation(
                    file_path=path,
                    rule_id="ARCH-P2P-MEDIA-KIT",
                    message="p2p_engine cannot depend on media_kit.",
                )
            )

    p2p_dir = root / "lib" / "features" / "p2p_engine"
    p2p_has_code = any(
        path.relative_to(root).as_posix().startswith("lib/features/p2p_engine/")
        for path in files
    )
    if p2p_dir.exists() and p2p_has_code and not p2p_has_endpoint:
        violations.append(
            CheckViolation(
                file_path=p2p_dir,
                rule_id="P2P-ENDPOINT-MISSING",
                message="P2P engine must expose the 127.0.0.1:8888/stream endpoint.",
            )
        )

    status = CheckStatus.PASSED if not violations else CheckStatus.FAILED
    return CheckResult(
        check_name="03_p2p_invariants",
        status=status,
        violations=violations,
        execution_time_ms=(time.perf_counter() - start) * 1000.0,
    )
