---
name: launch-app
description: Arranca la aplicación en el entorno, dispositivo o plataforma configurada según el stack del proyecto.
---

# Launch App

Arranca la aplicación en el dispositivo o plataforma indicada según el stack del proyecto.

## Comando

```bash
python .ai-harness/skills/launch-app/runner.py
```

Comando subyacente configurado en `harness.config.yaml` (`project.launch_command`).

## Opciones avanzadas (para stacks móviles/desktop)

```bash
python .ai-harness/skills/launch-app/runner.py --list
python .ai-harness/skills/launch-app/runner.py --device windows
python .ai-harness/skills/launch-app/runner.py --device android --emulator <ID>
```

## Parámetros

| Parámetro | Descripción |
|---|---|
| `--device` | Identificador de dispositivo (`windows`, `macos`, `linux`, `android` o un ID de la herramienta) |
| `--emulator` | ID del emulador que se debe iniciar antes de arrancar la app |
| `--list` | Lista los dispositivos disponibles y termina |

## Qué hace

1. Localiza la raíz del proyecto por su manifiesto o configuración.
2. Ejecuta el comando oficial del proyecto (`launch_command`) o interactúa con el SDK del stack.
3. Reporta el resultado del arranque.

## Reglas

- No levanta servicios auxiliares ni backends no autorizados.
- No abre puertos externos innecesarios.
