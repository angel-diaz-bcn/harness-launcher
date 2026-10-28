# Workflow — Arranque de la aplicación

## Objetivo

Arrancar la aplicación en el dispositivo o plataforma solicitada. Requiere que
el proyecto sea Flutter; en otro stack, este workflow no aplica.

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
- El endpoint local que necesite la app lo crea la propia app al iniciar; nunca
  se expone fuera de loopback.
- No levantar servicios web ni backends intermedios.
