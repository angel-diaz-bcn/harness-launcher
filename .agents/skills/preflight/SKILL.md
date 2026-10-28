# preflight

Valida el código y la arquitectura antes de cerrar un cambio de producto.

## Comando

```bash
python .ai-harness/skills/preflight/runner.py [target]
python .ai-harness/skills/preflight/runner.py --strict
python .ai-harness/skills/preflight/runner.py --json
```

## Qué comprueba

- Formato, análisis estático y tests del stack declarado.
- Fronteras entre features e imports prohibidos.
- Contratos inmutables en dominio y modelos.
- Disciplina de tokens: sin colores ni tamaños literales fuera del tema.
- Dependencias prohibidas declaradas en `harness.config.yaml`.
- Checks de perfil, solo si `invariants.profile` está activo.

Cada check que no puede ejecutarse (por ejemplo, sin manifiesto de proyecto)
devuelve `WARNING`, no `FAILED`: el arnés no bloquea por ausencia de stack.

## Cuándo usarla

Antes de cerrar cambios de código, configuración, assets o dependencias.

## Salida

Código 0 si no hay fallos. Los fallos se escriben además en
`memory/ephemeral_feedback/last_failure.md` para el ciclo de corrección.

## Reglas

- Un fallo se corrige en el código, no en el check.
- No se declara terminado un cambio con fallos abiertos.
