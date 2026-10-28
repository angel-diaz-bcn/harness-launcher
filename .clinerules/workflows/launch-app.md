# Workflow — Arranque de FLIK

## Objetivo

Arrancar la aplicación Flutter en el dispositivo o plataforma solicitada.

## Protocolo

1. Verificar que existe `pubspec.yaml` en la raíz.
2. Ejecutar:

```bash
python .ai-harness/skills/launch-app/runner.py --device <device>
```

Ejemplos de `device`: `windows`, `macos`, `linux`, `android`, o el ID que devuelva `flutter devices`.

3. Si no se indica dispositivo, el runner lista los disponibles y usa el primero compatible.
4. Verificar que la app arranca sin errores de compilación ni de plataforma.

## Reglas

- No existe backend ni frontend web que levantar.
- No abrir puertos externos.
- El endpoint `127.0.0.1:8888/stream` lo crea la propia app cuando inicia una sesión P2P.
- No levantar servicios web ni backends intermedios.
