# launch-app

Arranca la aplicación en el dispositivo o plataforma indicada. Requiere un
proyecto Flutter; en otro stack, este skill no aplica.

## Comando

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

1. Localiza la raíz del proyecto por su manifiesto.
2. Comprueba que el SDK del stack está disponible.
3. Arranca el emulador si se indicó y espera a que esté listo.
4. Ejecuta la app y reporta el resultado.

## Reglas

- No levanta servicios auxiliares ni backends intermedios.
- No abre puertos externos.
- Los endpoints locales que necesite la app los crea la propia app.
