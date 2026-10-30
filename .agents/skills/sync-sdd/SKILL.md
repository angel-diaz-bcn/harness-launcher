---
name: sync-sdd
description: Comprueba que cada spec aprobada (.spec.md), su target y la implementación en disco no divergen.
---

# Sync SDD

Comprueba que cada spec aprobada, su `target` y la implementación no divergen.

## Comando

```bash
python .ai-harness/skills/sync-sdd/runner.py            # todas las specs
python .ai-harness/skills/sync-sdd/runner.py CMP-01     # una spec concreta
python .ai-harness/skills/sync-sdd/runner.py --baseline  # registra el estado actual
python .ai-harness/skills/sync-sdd/runner.py --json
```

## Estados

| Estado | Significado |
|---|---|
| `N/A` | La spec no está aprobada; no se espera implementación |
| `MISSING` | El `target` no existe |
| `PRESENT` | Target existe y coincide con el baseline |
| `DIVERGED` | Cambió la spec o el target desde el baseline |

## Cuándo usarla

- Al cerrar una spec (`--baseline` para fijar el punto de partida).
- Antes de publicar en Git.
- Tras cualquier cambio de comportamiento.

## Salida

Código 0 si no hay `DIVERGED`; 1 si hay divergencias. El baseline se guarda en
`memory/sync-state.json` (no se edita a mano).

## Reglas

- Una divergencia se resuelve actualizando spec o código, no falseando el baseline.
- Toda spec aprobada debe tener target existente.
