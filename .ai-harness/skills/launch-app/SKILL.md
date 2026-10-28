---
name: launch-app
description: Arranca la aplicación (stack Flutter) en el dispositivo o plataforma indicada.
---

# Launch App

Arranca la app Flutter desde la raíz del proyecto.

## Uso

```bash
python .ai-harness/skills/launch-app/runner.py --list
python .ai-harness/skills/launch-app/runner.py --device windows
python .ai-harness/skills/launch-app/runner.py --device android
```

Si no se indica dispositivo, usa `windows`, `macos` o `linux` según el sistema.

## Reglas

- Requiere `pubspec.yaml` en la raíz.
- No existe backend ni frontend web.
- El endpoint local lo crea la app al iniciar y nunca se expone fuera de loopback.
- No abrir puertos externos.
