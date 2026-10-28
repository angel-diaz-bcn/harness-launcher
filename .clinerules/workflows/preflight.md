# Workflow — Preflight del producto

## Disparador

Cambios en código, configuración, assets o dependencias.

## Protocolo

1. Ejecutar:

```bash
python .ai-harness/skills/preflight/runner.py [target]
```

2. Interpretar el resultado:
   - `PASSED`: no hay violaciones.
   - `WARNING`: hay avisos no bloqueantes; revisar y decidir.
   - `FAILED`: corregir antes de continuar.

3. Si falla:
   - leer el archivo y la línea indicados;
   - diagnosticar la causa raíz;
   - corregir;
   - volver a ejecutar el preflight.

## Checks esperados

- formato y análisis estático del stack declarado.
- suite de tests.
- fronteras de imports entre features (`architecture` en la configuración).
- contratos inmutables en dominio y modelos.
- tokens de diseño, sin valores literales.
- dependencias prohibidas declaradas en la configuración.
- checks de perfil, solo si `invariants.profile` está activo.

## Reglas

- No usar herramientas ni términos de otro proyecto: no pertenecen a este arnés.
- No declarar la tarea terminada con exit code distinto de 0.
- No desactivar checks para “hacer pasar” el pipeline.
