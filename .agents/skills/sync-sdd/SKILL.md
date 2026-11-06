---
name: sync-sdd
description: Audita que cada módulo vivo en modules/ y cada propuesta en changes/ estén alineados con el código en disco.
---

# Sync SDD (OpenSpec)

Audita el estado de sincronización entre la verdad consolidada de `modules/`, las tareas en curso en `changes/` y el código fuente.

## Comandos

```bash
python .ai-harness/skills/sync-sdd/runner.py            # auditoría completa
python .ai-harness/skills/sync-sdd/runner.py --baseline  # registra los hashes actuales de los módulos
python .ai-harness/skills/sync-sdd/runner.py --tier fast # auditoría para modo fast-path
python .ai-harness/skills/sync-sdd/runner.py --json
```

## Estados de alineación

| Estado | Significado |
|---|---|
| `PRESENT` | El módulo existe, su target en disco existe y coincide con la línea base |
| `PENDING_TASKS` | La propuesta en `changes/` tiene tareas pendientes (`[ ]`) |
| `READY_TO_CONSOLIDATE` | Todas las tareas de `tasks.md` están completadas (`[x]`); listo para `/consolidate-change` |
| `MISSING` | El `target_path` declarado en el módulo no existe en el repositorio |
| `DIVERGED` | El módulo o su target han cambiado respecto a la última línea base |
| `N/A` | Módulo sin target declarado o sin tareas ejecutables |

## Cuándo usarla

- Tras completar la implementación de un cambio.
- Antes de publicar en Git o solicitar revisión de PR.
- Para verificar que no quedan tareas huérfanas en `changes/`.
