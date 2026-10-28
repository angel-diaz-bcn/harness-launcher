"""Scaffolds a FLIK process spec from the canonical template."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
harness_dir = current_dir.parent.parent
template_path = harness_dir / "sdd" / "templates" / "TEMPLATE_PROCESS_SDD.md"
ID_PATTERN = re.compile(r"^PRC-\d{2}$")


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a FLIK process spec scaffold")
    parser.add_argument("process_id", help="PRC-01")
    parser.add_argument("--name", required=True, help="Human-readable process name")
    parser.add_argument("--target", required=True, help="Implementation path under lib/")
    parser.add_argument("--dir", required=True, help="Directory for story and spec")
    parser.add_argument("--block", default="navigation", help="catalog, playback or navigation")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing scaffold")
    args = parser.parse_args()

    if not ID_PATTERN.match(args.process_id):
        print("Process id must match PRC-NN.", file=sys.stderr)
        sys.exit(1)
    if not args.target.startswith("lib/"):
        print("Target must be a path under lib/.", file=sys.stderr)
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
    content = content.replace("PRC-<NN>", args.process_id)
    content = content.replace("<Nombre del proceso>", args.name)
    content = content.replace("<ruta/exacta/al/orquestador.dart>", args.target)
    content = content.replace("block: <playback|catalog|navigation>", f"block: {args.block}")
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
