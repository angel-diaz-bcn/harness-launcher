---
name: launch-app
description: Arranca la aplicación Flutter de FLIK en el dispositivo o plataforma indicada.
---

# Launch App

```bash
# Ver emuladores disponibles (ej. FLIK_TV, FLIK_PHONE_30)
python .ai-harness/skills/launch-app/runner.py --list-emulators

# Lanzar el emulador de TV y ejecutar FLIK directamente:
python .ai-harness/skills/launch-app/runner.py --emulator FLIK_TV

# O ver dispositivos conectados y ejecutar en uno específico:
python .ai-harness/skills/launch-app/runner.py --list
python .ai-harness/skills/launch-app/runner.py --device windows
```

Requiere `pubspec.yaml` en la raíz. No existe backend ni frontend web. El endpoint local lo crea la app al iniciar una sesión P2P.
