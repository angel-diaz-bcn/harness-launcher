# FLIK — Skills del Arnés

Este directorio contiene las skills ejecutables. La fuente de verdad del inventario es `registry.yaml`.

## Inventario

| Skill | Función |
|---|---|
| `harness-validator` | Valida contexto, scopes, memoria, SDD y skills |
| `preflight` | Valida Flutter/Dart, arquitectura, tokens e invariantes P2P |
| `sync-sdd` | Comprueba spec `.spec.md` ↔ target ↔ implementación |
| `create-component-sdd` | Crea el esqueleto de un componente |
| `create-process-sdd` | Crea el esqueleto de un proceso |
| `launch-app` | Arranca la app Flutter |
| `git-publish` | Publica en Git bajo demanda explícita |

## Reglas

- Cada skill tiene `skill.yaml`, runner, documentación en `.agents/skills/<name>/SKILL.md` y entrada en `registry.yaml`.
- No se duplican runners ni manifiestos en dos árboles.
- Una skill que no esté en el registro no se considera disponible.
- Los comandos se ejecutan desde la raíz del repositorio.
- No se añaden skills que dependan de servicios externos no declarados.

## Documentación

La documentación de uso de cada skill está en `.agents/skills/`. Este README solo indexa; no duplica manuales.
