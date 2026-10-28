# Workflow — Validación del arnés

## Disparador

Cambios en specs, contexto, scopes, memoria, skills o configuración del arnés.

## Protocolo

1. Ejecutar:

```bash
python .ai-harness/skills/harness-validator/runner.py
```

2. Si falla, leer el check señalado y corregir la causa raíz.
3. Volver a ejecutar hasta que pase.

## Reglas

- No desactivar checks para “hacer pasar” la validación.
- No declarar la tarea terminada con fallos abiertos.
- La fuente de verdad de las skills es `.ai-harness/skills/registry.yaml`.
