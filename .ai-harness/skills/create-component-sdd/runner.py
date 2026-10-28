"""Scaffolds a component spec from the canonical template."""

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

template_path = harness_dir / "sdd" / "templates" / "TEMPLATE_COMPONENT_SDD.md"


def infer_layer(path_value: str, layers: tuple[str, ...] = ()) -> str | None:
    if not layers:
        layers = tuple(
            str(x)
            for x in load_config(harness_dir)["sdd"].get("component_layers", []) or []
        )
    normalized = "/" + path_value.replace("\\", "/").strip("/")
    for layer in layers:
        if f"/1_COMPONENTS/{layer}/" in normalized:
            return layer
    return None


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def main() -> None:
    config = load_config(harness_dir)
    sdd = config["sdd"]
    component_prefix = str(sdd.get("component_prefix", "CMP"))
    layers = tuple(str(x) for x in sdd.get("component_layers", []) or [])
    path_roots = tuple(
        str(x) for x in config["scopes"].get("path_roots", []) or ["lib/"]
    )
    id_pattern = re.compile(rf"^{re.escape(component_prefix)}-\d{{2}}$")

    parser = argparse.ArgumentParser(description="Create a component spec scaffold")
    parser.add_argument("component_id", help=f"{component_prefix}-01")
    parser.add_argument("--name", required=True, help="Human-readable component name")
    parser.add_argument(
        "--target", required=True, help=f"Implementation path under {path_roots[0]}"
    )
    parser.add_argument("--dir", required=True, help="Directory for story and spec")
    parser.add_argument(
        "--layer",
        choices=layers or None,
        help="Component layer; inferred from --dir when omitted",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing scaffold")
    args = parser.parse_args()

    if not id_pattern.match(args.component_id):
        print(
            f"Component id must match {component_prefix}-NN.",
            file=sys.stderr,
        )
        sys.exit(1)
    if path_roots and not args.target.startswith(path_roots[0]):
        print(f"Target must be a path under {path_roots[0]}.", file=sys.stderr)
        sys.exit(1)
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    layer = args.layer or infer_layer(args.dir, layers)
    if layer is None:
        print(
            "Indicate --layer "
            + "|".join(layers)
            + " or use a 1_COMPONENTS/<layer>/ directory.",
            file=sys.stderr,
        )
        sys.exit(1)
    folder_layer = infer_layer(args.dir, layers)
    if folder_layer is not None and folder_layer != layer:
        print(
            f"Layer '{layer}' does not match --dir layer '{folder_layer}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    feature_match = re.match(r"lib/features/([a-z0-9_]+)/", args.target)
    feature = feature_match.group(1) if feature_match else "app"

    spec_dir = Path(args.dir)
    spec_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.name)
    spec_path = spec_dir / f"{args.component_id}-{slug}.spec.md"
    story_path = spec_dir / "user_story.md"

    if not args.force and (spec_path.exists() or story_path.exists()):
        print("Scaffold already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    content = template_path.read_text(encoding="utf-8")
    content = re.sub(r"[A-Z]{2,5}-<NN>", args.component_id, content)
    content = re.sub(r"layer:\s*<[^>]*>", f"layer: {layer}", content)
    content = re.sub(r"<Nombre del componente>", args.name, content)
    content = re.sub(r"<ruta/[^>]*>", args.target, content)
    content = re.sub(r"block:\s*<[^>]*>", f"block: {feature}", content)
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

    print(f"[create-component-sdd] Created {spec_path}")
    print(f"[create-component-sdd] Created {story_path}")
    print("[create-component-sdd] Complete all placeholders before APPROVED.")


if __name__ == "__main__":
    main()
