"""Shared helpers for FLIK preflight checks."""

from __future__ import annotations

import re
from pathlib import Path


def find_project_root(scope: Path) -> Path | None:
    start = scope if scope.is_dir() else scope.parent
    for candidate in (start, *start.parents):
        if (candidate / "pubspec.yaml").exists():
            return candidate
    return None


def pubspec_name(root: Path) -> str:
    pubspec = root / "pubspec.yaml"
    if not pubspec.exists():
        return "flik"
    match = re.search(r"^name:\s*([A-Za-z0-9_]+)\s*$", pubspec.read_text(encoding="utf-8"), re.M)
    return match.group(1) if match else "flik"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def dart_files(root: Path, relative: str | None = None) -> list[Path]:
    base = root / relative if relative else root
    if not base.exists():
        return []
    files: list[Path] = []
    for path in base.rglob("*.dart"):
        normalized = path.as_posix()
        if any(part in normalized for part in ("/.dart_tool/", "/build/", "/.git/")):
            continue
        files.append(path)
    return sorted(files)


def feature_of(path: Path, root: Path) -> str | None:
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError:
        return None
    match = re.match(r"lib/features/([a-z0-9_]+)/", relative)
    return match.group(1) if match else None


def import_paths(content: str) -> list[tuple[int, str]]:
    imports: list[tuple[int, str]] = []
    pattern = re.compile(r"""^\s*import\s+['"]([^'"]+)['"]""", re.MULTILINE)
    for match in pattern.finditer(content):
        line = content[: match.start()].count("\n") + 1
        imports.append((line, match.group(1)))
    return imports
