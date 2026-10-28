"""FLIK sync-sdd: derives implementation state from specs and targets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

current_dir = Path(__file__).resolve().parent
harness_dir = current_dir.parent.parent
workspace_root = harness_dir.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from models import SddSyncItem, SddSyncReport

APPROVED = "APPROVED"
STATE_PATH = harness_dir / "memory" / "sync-state.json"


def _value(content: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def _target_path(value: str) -> Path:
    clean = value.strip().strip("`").split("::", 1)[0].strip()
    return workspace_root / clean


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {"version": 1, "items": {}}
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "items": {}}
    if not isinstance(state, dict) or not isinstance(state.get("items"), dict):
        return {"version": 1, "items": {}}
    return state


def _save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="FLIK SDD sync")
    parser.add_argument("spec", nargs="?", default="all", help="Spec id, path, or 'all'")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Record current spec/target hashes as the implementation baseline",
    )
    args = parser.parse_args()

    sdd_dir = harness_dir / "sdd"
    specs = sorted(sdd_dir.rglob("*.spec.md"))
    previous_state = _load_state()
    next_state = {"version": 1, "items": dict(previous_state.get("items", {}))}

    items: list[SddSyncItem] = []
    for spec in specs:
        content = spec.read_text(encoding="utf-8", errors="ignore")
        spec_id = _value(content, "spec_id") or spec.stem
        target = _value(content, "target") or ""
        status = _value(content, "status") or "DRAFT"
        version = _value(content, "version") or ""

        if args.spec != "all":
            requested = Path(args.spec)
            matches = args.spec == spec_id or requested.resolve() == spec.resolve()
            if not matches:
                continue

        story = spec.parent / "user_story.md"
        target_path = _target_path(target) if target else workspace_root / "__missing__"
        has_target = bool(target) and target_path.exists()
        spec_hash = _hash_file(spec)
        target_hash = _hash_file(target_path) if has_target else ""
        previous = previous_state.get("items", {}).get(spec_id)

        if not story.exists():
            state = "DIVERGED"
            details = "missing user_story.md"
            next_state["items"].pop(spec_id, None)
        elif status != APPROVED:
            state = "N/A"
            details = f"status {status}; implementation not expected"
            next_state["items"].pop(spec_id, None)
        elif not target:
            state = "MISSING"
            details = "missing target in front matter"
            next_state["items"].pop(spec_id, None)
        elif not has_target:
            state = "MISSING"
            details = f"target does not exist: {target}"
            next_state["items"].pop(spec_id, None)
        else:
            if args.baseline or previous is None:
                state = "PRESENT"
                details = (
                    "target exists; baseline recorded"
                    if args.baseline
                    else "target exists; no baseline yet"
                )
            elif previous.get("spec_hash") != spec_hash:
                state = "DIVERGED"
                details = "spec changed since last baseline"
            elif previous.get("target_hash") != target_hash:
                state = "DIVERGED"
                details = "target changed since last baseline"
            else:
                state = "PRESENT"
                details = "target exists and matches baseline"

            if state == "PRESENT" or args.baseline:
                next_state["items"][spec_id] = {
                    "spec_hash": spec_hash,
                    "target_hash": target_hash,
                    "status": status,
                    "version": version,
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                }

        items.append(
            SddSyncItem(
                spec_id=spec_id,
                spec_path=str(spec.relative_to(workspace_root)),
                target=target,
                status=status,
                version=version,
                has_user_story=story.exists(),
                has_target=has_target,
                sync_state=state,
                details=details,
            )
        )

    not_applicable = sum(1 for item in items if item.sync_state == "N/A")
    missing = sum(1 for item in items if item.sync_state == "MISSING")
    present = sum(1 for item in items if item.sync_state == "PRESENT")
    diverged = sum(1 for item in items if item.sync_state == "DIVERGED")
    report = SddSyncReport(
        total=len(items),
        not_applicable=not_applicable,
        missing=missing,
        present=present,
        diverged=diverged,
        items=items,
        is_successful=diverged == 0,
    )

    _save_state(next_state)

    if args.json:
        print(report.model_dump_json(indent=2))
    else:
        print("FLIK SDD SYNC")
        print("=" * 72)
        for item in items:
            print(f"[{item.sync_state}] {item.spec_id} -> {item.target or '(sin target)'}")
            if item.details:
                print(f"  {item.details}")
        print("=" * 72)
        print(
            f"Total: {report.total} | N/A: {not_applicable} | MISSING: {missing} | "
            f"PRESENT: {present} | DIVERGED: {diverged}"
        )

    sys.exit(0 if report.is_successful else 1)


if __name__ == "__main__":
    main()
