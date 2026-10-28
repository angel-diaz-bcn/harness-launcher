# Workflow — Preflight de FLIK

## Disparador

Cambios en código Dart/Flutter, configuración, assets o dependencias.

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

- `dart format` y `flutter analyze`.
- `flutter test`.
- fronteras de imports entre features.
- contratos inmutables en dominio/modelos.
- endpoint local y ausencia de backend/proxy.
- tokens de diseño, sin HEX hardcodeados.
- dependencias prohibidas en `pubspec.yaml`.

## Reglas

- No usar herramientas del proyecto anterior: no pertenecen a FLIK.
- No declarar la tarea terminada con exit code distinto de 0.
- No desactivar checks para “hacer pasar” el pipeline.
