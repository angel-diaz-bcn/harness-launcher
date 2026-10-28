"""
Check SDD: Software Driven Design (SDD) Specification Alignment.
"""

import re
import time
from pathlib import Path

try:
    from harness_config import harness_dir_of, load_config
    from models import SubCheckResult, ValidationStatus, ValidationViolation
except ImportError:
    from .models import (  # type: ignore[no-redef]
        SubCheckResult,
        ValidationStatus,
        ValidationViolation,
    )


VALID_SDD_STATES = {
    "DRAFT",
    "APPROVED",
    "SUPERSEDED",
}


def _spec_filename_re(component_prefix: str, process_prefix: str) -> re.Pattern[str]:
    """Construye el patrón de nombre de spec a partir de los prefijos configurados."""
    prefixes = "|".join(
        re.escape(prefix) for prefix in (component_prefix, process_prefix) if prefix
    )
    return re.compile(rf"^({prefixes})-\d{{2}}-[a-z0-9]+(?:-[a-z0-9]+)*\.spec\.md$")



def _frontmatter_value(content: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def run(harness_root: Path, strict: bool = False, fix: bool = False) -> SubCheckResult:
    start_time = time.perf_counter()
    violations: list[ValidationViolation] = []

    config = load_config(harness_root)
    component_prefix = str(config["sdd"].get("component_prefix", "CMP"))
    process_prefix = str(config["sdd"].get("process_prefix", "PRC"))
    required_blocks = [str(name) for name in config["sdd"].get("blocks", [])]
    required_frontmatter = [str(key) for key in config["sdd"].get("frontmatter", [])]
    component_layers = {str(x) for x in config["sdd"].get("component_layers", [])}
    map_heading = str(
        config["sdd"].get("implementation_map_heading", "Mapa de implementación")
    )
    spec_filename_re = _spec_filename_re(component_prefix, process_prefix)

    harness_dir = harness_dir_of(harness_root)
    sdd_dir = harness_dir / "sdd"
    workspace_root = harness_dir.parent


    if not sdd_dir.exists():
        violations.append(
            ValidationViolation(
                component="sdd",
                file_path=sdd_dir,
                rule_id="SDD-MISSING-ROOT",
                message="SDD directory '.ai-harness/sdd' does not exist.",
                severity="ERROR",
            )
        )
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return SubCheckResult(
            check_name="check_sdd",
            status=ValidationStatus.FAILED,
            violations=violations,
            execution_time_ms=elapsed_ms,
        )

    # 1. Verify 6 Block Directories
    for block_dir_name in required_blocks:
        block_path = sdd_dir / block_dir_name
        if not block_path.exists() or not block_path.is_dir():
            violations.append(
                ValidationViolation(
                    component="sdd",
                    file_path=block_path,
                    rule_id="SDD-MISSING-BLOCK-DIR",
                    message=f"Mandatory SDD block directory '{block_dir_name}' is missing.",
                    severity="ERROR",
                )
            )

    # 2. Inspect all SDD spec and user story files
    sdd_files = list(sdd_dir.rglob("*.md"))

    for sdd_file in sdd_files:
        norm_path = sdd_file.as_posix()
        if "/." in norm_path:
            continue

        try:
            content = sdd_file.read_text(encoding="utf-8", errors="ignore")

            # Handle empty files
            if len(content.strip()) == 0:
                if fix:
                    # Apply automatic template fix for empty SDD files
                    block_name = sdd_file.parent.parent.name
                    template_content = (
                        f"# SDD Specification: {sdd_file.parent.name}\n\n"
                        f"**Target:** {sdd_file.parent.name}\n"
                        f"**Bloque del Pipeline:** {block_name}\n"
                        f"**Estado:** DRAFT\n\n"
                        f"## Overview\nInitial SDD document created automatically by harness-validator fix.\n"
                    )
                    sdd_file.write_text(template_content, encoding="utf-8")
                    content = template_content
                else:
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=sdd_file,
                            rule_id="SDD-EMPTY-FILE",
                            message="SDD markdown file is empty (0 bytes).",
                            severity="ERROR",
                        )
                    )
                    continue

            relative_path = sdd_file.relative_to(sdd_dir)
            if relative_path.parts and relative_path.parts[0] == "templates":
                continue
            if sdd_file.name in {"user_story.md", "README.md", "INDEX.md"}:
                continue
            if not spec_filename_re.match(sdd_file.name):
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-INVALID-SPEC-FILENAME",
                        message=(
                            "Spec filename must match "
                            f"'<{component_prefix}|{process_prefix}>-<NN>-<slug>.spec.md'."
                        ),
                        severity="ERROR",
                    )
                )
                continue

            missing_frontmatter = [
                key for key in required_frontmatter if _frontmatter_value(content, key) is None
            ]
            if missing_frontmatter:
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-MISSING-FRONTMATTER",
                        message=(
                            "Spec front matter missing required keys: "
                            f"{', '.join(missing_frontmatter)}."
                        ),
                        severity="ERROR",
                    )
                )

            spec_id = _frontmatter_value(content, "spec_id")
            spec_type = _frontmatter_value(content, "spec_type")
            status = _frontmatter_value(content, "status")

            if spec_id and not sdd_file.name.startswith(f"{spec_id}-"):
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-SPEC-ID-MISMATCH",
                        message=(
                            f"Front matter spec_id '{spec_id}' does not match filename "
                            f"'{sdd_file.name}'."
                        ),
                        severity="ERROR",
                    )
                )

            if status and status not in VALID_SDD_STATES:
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-INVALID-STATUS",
                        message=(
                            f"Status '{status}' is invalid. Allowed: "
                            f"{', '.join(sorted(VALID_SDD_STATES))}."
                        ),
                        severity="ERROR",
                    )
                )

            if status == "APPROVED":
                approved_at = _frontmatter_value(content, "approved_at")
                approved_by = _frontmatter_value(content, "approved_by")
                if not approved_at or approved_at.lower() == "null":
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=sdd_file,
                            rule_id="SDD-MISSING-APPROVAL-DATE",
                            message="APPROVED spec requires 'approved_at'.",
                            severity="ERROR",
                        )
                    )
                if not approved_by or approved_by.lower() == "null":
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=sdd_file,
                            rule_id="SDD-MISSING-APPROVAL-OWNER",
                            message="APPROVED spec requires 'approved_by'.",
                            severity="ERROR",
                        )
                    )
            if status == "SUPERSEDED":
                superseded_by = _frontmatter_value(content, "superseded_by")
                if not superseded_by or superseded_by in {"[]", "null"}:
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=sdd_file,
                            rule_id="SDD-MISSING-SUPERSEDED-BY",
                            message="SUPERSEDED spec requires a non-empty 'superseded_by'.",
                            severity="ERROR",
                        )
                    )

            expected_type = (
                component_prefix
                if sdd_file.name.startswith(f"{component_prefix}-")
                else process_prefix
            )
            if spec_type and spec_type != expected_type:
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-SPEC-TYPE-MISMATCH",
                        message=(
                            f"Front matter spec_type '{spec_type}' does not match the "
                            f"filename prefix (expected '{expected_type}')."
                        ),
                        severity="ERROR",
                    )
                )

            layer = _frontmatter_value(content, "layer")
            if expected_type == component_prefix:
                valid_layers = component_layers
                if layer is None:
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=sdd_file,
                            rule_id="SDD-MISSING-LAYER",
                            message="Component spec front matter is missing required 'layer'.",
                            severity="ERROR",
                        )
                    )
                elif layer not in valid_layers:
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=sdd_file,
                            rule_id="SDD-INVALID-LAYER",
                            message=(
                                f"Layer '{layer}' is invalid. Allowed: "
                                f"{', '.join(sorted(valid_layers))}."
                            ),
                            severity="ERROR",
                        )
                    )
                else:
                    relative_parts = sdd_file.relative_to(sdd_dir).parts
                    if "1_COMPONENTS" in relative_parts:
                        layer_index = relative_parts.index("1_COMPONENTS") + 1
                        if layer_index < len(relative_parts):
                            folder_layer = relative_parts[layer_index]
                            if folder_layer in valid_layers and folder_layer != layer:
                                violations.append(
                                    ValidationViolation(
                                        component="sdd",
                                        file_path=sdd_file,
                                        rule_id="SDD-LAYER-PATH-MISMATCH",
                                        message=(
                                            f"Layer '{layer}' does not match folder "
                                            f"'1_COMPONENTS/{folder_layer}/'."
                                        ),
                                        severity="ERROR",
                                    )
                                )

            target = _frontmatter_value(content, "target")
            user_story_ref = _frontmatter_value(content, "user_story")
            story_path = sdd_file.parent / "user_story.md"
            if user_story_ref and user_story_ref != "user_story.md":
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-INVALID-USER-STORY-REF",
                        message="Front matter user_story must reference 'user_story.md'.",
                        severity="ERROR",
                    )
                )
            if not story_path.exists():
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=story_path,
                        rule_id="SDD-MISSING-USER-STORY",
                        message="Every spec must have user_story.md in the same folder.",
                        severity="ERROR",
                    )
                )

            if target:
                clean_target = target.strip().strip("`").split("::", 1)[0].strip()
                target_path = workspace_root / clean_target
                approved = status == "APPROVED"
                if approved and not target_path.exists():
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=target_path,
                            rule_id="SDD-TARGET-MISSING",
                            message=f"Approved spec target does not exist: {clean_target}.",
                            severity="ERROR",
                        )
                    )

            map_section = content.split(map_heading, 1)[-1]
            if not re.search(r"\b(FR|ST)-\d{2}\b", map_section):
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-MAP-MISSING-REQUIREMENT",
                        message="Implementation map must reference FR-* or ST-* rows.",
                        severity="ERROR",
                    )
                )
            if not re.search(r"\bTC-\d{2}\b", map_section):
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-MAP-MISSING-TEST",
                        message="Implementation map must reference TC-* tests.",
                        severity="ERROR",
                    )
                )

            required_traceability = r"\bST-\d{2}\b" if expected_type == "PRC" else r"\bFR-\d{2}\b"
            for pattern, label in (
                (required_traceability, "ST-NN" if expected_type == "PRC" else "FR-NN"),
                (r"\bCT-\d{2}\b", "CT-NN"),
                (r"\bTC-\d{2}\b", "TC-NN"),
            ):
                if not re.search(pattern, content):
                    violations.append(
                        ValidationViolation(
                            component="sdd",
                            file_path=sdd_file,
                            rule_id="SDD-MISSING-TRACEABILITY",
                            message=f"Spec is missing traceability identifiers ({label}).",
                            severity="ERROR",
                        )
                    )

            if map_heading not in content:
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-MISSING-IMPLEMENTATION-MAP",
                        message="Spec is missing the implementation/traceability map.",
                        severity="ERROR",
                    )
                )

            # Check metadata fields: Target, Bloque del Pipeline, Estado / Status
            has_target = bool(re.search(r"(Target|Objetivo|Scope)\s*:", content, re.IGNORECASE))
            has_block = bool(
                re.search(r"(Bloque|Block|Pipeline\s*Block)\s*:", content, re.IGNORECASE)
            )
            has_state = bool(re.search(r"(Estado|Status|State)\s*:", content, re.IGNORECASE))

            missing_meta = []
            if not has_target:
                missing_meta.append("Target")
            if not has_block:
                missing_meta.append("Bloque del Pipeline")
            if not has_state:
                missing_meta.append("Estado")

            if missing_meta:
                sev = "ERROR" if strict else "WARNING"
                violations.append(
                    ValidationViolation(
                        component="sdd",
                        file_path=sdd_file,
                        rule_id="SDD-MISSING-METADATA",
                        message=f"SDD file missing metadata headers: {', '.join(missing_meta)}.",
                        severity=sev,
                    )
                )

        except (OSError, ValueError) as e:
            violations.append(
                ValidationViolation(
                    component="sdd",
                    file_path=sdd_file,
                    rule_id="SDD-READ-ERROR",
                    message=f"Failed to read SDD file: {e!s}",
                    severity="ERROR",
                )
            )

    has_error = any(v.severity == "ERROR" for v in violations)
    has_warning = any(v.severity == "WARNING" for v in violations)

    if has_error or (strict and has_warning):
        status = ValidationStatus.FAILED
    elif has_warning:
        status = ValidationStatus.WARNING
    else:
        status = ValidationStatus.PASSED

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return SubCheckResult(
        check_name="check_sdd",
        status=status,
        violations=violations,
        execution_time_ms=elapsed_ms,
    )
