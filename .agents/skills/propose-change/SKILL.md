---
name: propose-change
description: Crea una propuesta de cambio aislada (delta OpenSpec) en .ai-harness/sdd/changes/ para su revisión rápida en 2 minutos antes de codificar.
---

# propose-change

Esta skill inicia una nueva propuesta de cambio según la metodología OpenSpec.

## Cuándo usarla

- Cada vez que el usuario solicite una nueva funcionalidad, un cambio de lógica de negocio o una modificación de contrato.
- **Antes** de tocar cualquier archivo de código fuente en `src/` o `lib/`.
- Permite que el desarrollador revise en 2 minutos el delta exacto antes de autorizar la implementación.

## Uso

```bash
python .ai-harness/skills/propose-change/runner.py <slug> --module <MOD-id> --title "<Título del cambio>"
```

Ejemplo:
```bash
python .ai-harness/skills/propose-change/runner.py add-google-oauth --module MOD-auth --title "Inicio de sesión con Google OAuth"
```

## Artefactos generados

1. `.ai-harness/sdd/changes/[YYYY-MM]-[slug]/proposal.md`: Contiene la motivación, los contratos/reglas que se añaden (`+`), modifican (`~`) o deprecian (`-`).
2. `.ai-harness/sdd/changes/[YYYY-MM]-[slug]/tasks.md`: Lista de tareas técnicas para guiar la implementación.

