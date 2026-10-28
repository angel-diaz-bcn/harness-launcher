---
name: create-component-sdd
description: Genera o actualiza la especificación técnica de un componente Flutter de FLIK (CMP-NN) bajo la plantilla canónica `.spec.md`.
---

# Create Component SDD Skill

Genera o actualiza especificaciones técnicas de **Componentes** en:

- `.ai-harness/sdd/1_COMPONENTS/bootstrap/` para `CMP-00` (infraestructura de arranque).
- `.ai-harness/sdd/1_COMPONENTS/frontend/` para `CMP-NN`.
- `.ai-harness/sdd/1_COMPONENTS/backend/` para el resto de `CMP-NN` (lógica local, no servidor).

## Convención obligatoria

- Carpeta: `<ID>-<slug>/`.
- Archivo: `<ID>-<slug>.spec.md`.
- Historia: `user_story.md`.
- Plantilla: `.ai-harness/sdd/templates/TEMPLATE_COMPONENT_SDD.md`.
- Reglas completas: `.ai-harness/sdd/templates/README.md`.

## Directrices anti-deriva

- **Cero placeholders:** prohibido dejar secciones vacías o textos genéricos en una spec aprobada.
- **Contratos reales:** modelos Dart inmutables, interfaces y errores tipados; sin `dynamic` injustificado.
- **Trazabilidad:** cada `FR-*` se mapea a `CT-*`, archivo::símbolo y `TC-*`.
- **UI:** solo tokens de `ui-design-system.md`; prohibido HEX literales.
- **BDD:** al menos dos escenarios Gherkin, uno de éxito y otro de error o caso borde.
- **Sin invención:** si falta información, se registra en `Q-*` y se detiene la implementación.

## Instrucciones de ejecución

```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-10 \
  --name "Billboard Hero" \
  --target lib/features/tv_experience/presentation/widgets/billboard_hero.dart \
  --layer frontend \
  --dir .ai-harness/sdd/1_COMPONENTS/frontend/CMP-10-billboard-hero
```

El runner crea `user_story.md` y `<ID>-<slug>.spec.md` desde la plantilla. Completar todos los placeholders y validar el checklist de `.ai-harness/sdd/templates/README.md` antes de cambiar el estado a `APPROVED` y registrar la aprobación.
