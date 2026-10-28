# Workflow — Inventario de Skills

## Objetivo

Mostrar las skills realmente disponibles, sin listas hardcodeadas.

## Protocolo

1. Leer `.ai-harness/skills/registry.yaml`.
2. Para cada entrada, verificar que existe su `skill.yaml` y su runner.
3. Contrastar con `.agents/skills/<name>/SKILL.md`.
4. Presentar una tabla:

| Skill | Estado | Descripción | Comando | Inputs |
|---|---|---|---|---|

## Reglas

- Si una skill aparece en el registro pero no tiene runner, marcarla como `BROKEN`.
- Si existe un directorio de skill sin entrada en el registro, marcarlo como `UNREGISTERED`.
- No inventar skills ni versiones.
- No ejecutar ninguna skill durante el inventario.
