# Skills para agentes

Índice de las skills disponibles. La implementación canónica vive en
`.ai-harness/skills/`; aquí solo se documenta su uso.

| Skill | Documentación | Función |
|---|---|---|
| `harness-validator` | `harness-validator/SKILL.md` | Valida la estructura del arnés |
| `preflight` | `preflight/SKILL.md` | Valida código, arquitectura, tokens y dependencias |
| `sync-sdd` | `sync-sdd/SKILL.md` | Deriva el estado spec ↔ implementación |
| `create-component-sdd` | `create-component-sdd/SKILL.md` | Crea el esqueleto de un componente |
| `create-process-sdd` | `create-process-sdd/SKILL.md` | Crea el esqueleto de un proceso |
| `launch-app` | `launch-app/SKILL.md` | Arranca la app (stack Flutter) |
| `git-publish` | `git-publish/SKILL.md` | Publica en Git bajo petición explícita |

Reglas:

- No hay runners en este directorio; solo documentación de uso.
- El inventario canónico está en `.ai-harness/skills/registry.yaml`.
- Si una skill no aparece en el registro, no se invoca.
- Toda skill nueva necesita manifiesto, runner, documentación y registro.
