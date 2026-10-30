---
name: harness-validator
description: Valida la estructura y la coherencia del arnés normativo (contexto, scopes, memoria, SDD y skills).
---

# Harness Validator

Valida la estructura y la coherencia del arnés: contexto, scopes, memoria, SDD
y skills.

## Comando

```bash
python .ai-harness/skills/harness-validator/runner.py
python .ai-harness/skills/harness-validator/runner.py --strict
python .ai-harness/skills/harness-validator/runner.py --json
```

## Qué comprueba

- Existen los contextos declarados en `harness.config.yaml` y tienen contenido.
- No hay marcadores pendientes en documentos normativos.
- Existen los scopes declarados y apuntan a una ruta autorizada.
- `AGENTS.md` referencia los documentos de gobernanza exigidos.
- `failure_modes.md` tiene el mínimo de entradas con el prefijo configurado.
- Cada spec cumple nombre, front matter, estado y trazabilidad.
- Cada skill tiene manifiesto, runner, documentación con frontmatter válido y entrada en el registro.

## Cuándo usarla

Antes de cerrar cualquier cambio que toque contexto, scopes, specs, memoria,
skills o configuración.

## Salida

Código 0 si todo pasa; 1 si hay fallos (o warnings en modo `--strict`).
Con `--json` emite el informe completo.

## Reglas

- No desactivar checks para hacer pasar la validación.
- Un fallo se corrige en la causa raíz, no en el check.
