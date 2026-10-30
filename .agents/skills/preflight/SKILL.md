---
name: preflight
description: Valida el código, arquitectura, contratos inmutables, disciplina de tokens y dependencias antes de cerrar un cambio de producto.
---

# Preflight

Valida el código y la arquitectura antes de cerrar un cambio de producto.

## Comando

```bash
python .ai-harness/skills/preflight/runner.py [target]
python .ai-harness/skills/preflight/runner.py --strict
python .ai-harness/skills/preflight/runner.py --json
```

## Qué comprueba

- Formato, análisis estático y tests del stack declarado (`00_code_quality`).
- Fronteras entre features, barrels e imports prohibidos (`01_architecture`).
- Contratos inmutables, sin tipos genéricos descontrolados (`any`/`dynamic`), sin logs (`console.log`/`print`) y sin bloques vacíos (`02_contracts`).
- Disciplina de tokens: sin colores HEX hardcodeados ni tamaños fuera de tokens (`04_ui_tokens`).
- Dependencias prohibidas declaradas en `harness.config.yaml` (`05_dependencies`).

Cada check que no puede ejecutarse (por ejemplo, sin código de producción todavía) devuelve `WARNING`, no `FAILED`.

## Cuándo usarla

Antes de cerrar cambios de código, configuración, assets o dependencias.

## Salida

Código 0 si no hay fallos. Los fallos se escriben además en
`memory/ephemeral_feedback/last_failure.md` para el ciclo de corrección.

## Reglas

- Un fallo se corrige en el código, no en el check.
- No se declara terminado un cambio con fallos abiertos.
