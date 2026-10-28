"""FLIK launch-app: starts the Flutter app on a selected device."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _find_project_root(start: Path) -> Path | None:
    for candidate in (start, *start.parents):
        if (candidate / "pubspec.yaml").exists():
            return candidate
    return None


def _default_device() -> str:
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch FLIK with Flutter")
    parser.add_argument("--device", default=None, help="Flutter device id (windows, macos, linux, android, ...)")
    parser.add_argument("--emulator", default=None, help="Emulator ID to launch (e.g. FLIK_TV, FLIK_PHONE_30)")
    parser.add_argument("--list", action="store_true", help="List available Flutter devices and exit")
    parser.add_argument("--list-emulators", action="store_true", help="List available Flutter emulators and exit")
    args = parser.parse_args()

    if shutil.which("flutter") is None:
        print("[launch-app] Flutter SDK not found in PATH.", file=sys.stderr)
        sys.exit(1)

    root = _find_project_root(Path.cwd())
    if root is None:
        print("[launch-app] pubspec.yaml not found. Run from the Flutter project root.", file=sys.stderr)
        sys.exit(1)

    is_win = sys.platform == "win32"
    if args.list_emulators:
        result = subprocess.run(["flutter", "emulators"], cwd=str(root), shell=is_win, check=False)
        sys.exit(result.returncode)

    if args.list:
        result = subprocess.run(["flutter", "devices"], cwd=str(root), shell=is_win, check=False)
        sys.exit(result.returncode)

    if args.emulator:
        print(f"[launch-app] Launching emulator '{args.emulator}'...")
        subprocess.run(["flutter", "emulators", "--launch", args.emulator], cwd=str(root), shell=is_win, check=False)
        print("[launch-app] Waiting for emulator to be ready...")
        import time
        for _ in range(30):
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True, shell=is_win, check=False)
            lines = [l for l in res.stdout.splitlines() if "device" in l and not l.startswith("List")]
            if lines:
                break
            time.sleep(2)

    device = args.device or _default_device()
    print(f"[launch-app] Starting FLIK on device '{device}'...")
    result = subprocess.run(["flutter", "run", "-d", device], cwd=str(root), shell=is_win, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
