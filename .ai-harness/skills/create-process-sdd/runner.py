"""Scaffolds a process spec from the canonical template."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
harness_dir = current_dir.parent.parent
skills_dir = current_dir.parent
if str(skills_dir) not in sys.path:
    sys.path.insert(0, str(skills_dir))

from harness_config import load_config

template_path = harness_dir / "sdd" / "templates" / "TEMPLATE_PROCESS_SDD.md"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def main() -> None:
    config = load_config(harness_dir)
    process_prefix = str(config["sdd"].get("process_prefix", "PRC"))
    path_roots = tuple(
        str(x) for x in config["scopes"].get("path_roots", []) or ["lib/"]
    )
    id_pattern = re.compile(rf"^{re.escape(process_prefix)}-\d{{2}}$")

    parser = argparse.ArgumentParser(description="Create a process spec scaffold")
    parser.add_argument("process_id", help=f"{process_prefix}-01")
    parser.add_argument("--name", required=True, help="Human-readable process name")
    parser.add_argument(
        "--target", required=True, help=f"Implementation path under {path_roots[0]}"
    )
    parser.add_argument("--dir", required=True, help="Directory for story and spec")
    parser.add_argument("--block", default="", help="Block that owns the process")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing scaffold")
    args = parser.parse_args()

    if not id_pattern.match(args.process_id):
        print(f"Process id must match {process_prefix}-NN.", file=sys.stderr)
        sys.exit(1)
    if path_roots and not args.target.startswith(path_roots[0]):
        print(f"Target must be a path under {path_roots[0]}.", file=sys.stderr)
        sys.exit(1)
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    spec_dir = Path(args.dir)
    spec_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.name)
    spec_path = spec_dir / f"{args.process_id}-{slug}.spec.md"
    story_path = spec_dir / "user_story.md"

    if not args.force and (spec_path.exists() or story_path.exists()):
        print("Scaffold already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    content = template_path.read_text(encoding="utf-8")
    content = re.sub(r"[A-Z]{2,5}-<NN>", args.process_id, content)
    content = re.sub(r"<Nombre del proceso>", args.name, content)
    content = re.sub(r"<ruta/[^>]*>", args.target, content)
    if args.block:
        content = re.sub(r"block:\s*<[^>]*>", f"block: {args.block}", content)
    content = content.replace("<nombre>.spec.md", spec_path.name)

    story = (
        f"# {args.name} — Historia de Usuario\n\n"
        "## Problema\n\n<Qué problema resuelve.>\n\n"
        "## Actores\n\n<Quién lo usa.>\n\n"
        "## Historia\n\n"
        f"> **Como** <rol>, **quiero** <acción>, **para** <beneficio>.\n\n"
        "## Criterios de negocio\n\n"
        "- <Criterio verificable.>\n\n"
        "## Fuera de alcance\n\n"
        "- <Lo que no cubre.>\n"
    )

    spec_path.write_text(content, encoding="utf-8")
    story_path.write_text(story, encoding="utf-8")

    print(f"[create-process-sdd] Created {spec_path}")
    print(f"[create-process-sdd] Created {story_path}")
    print("[create-process-sdd] Complete all placeholders before APPROVED.")


if __name__ == "__main__":
    main()
