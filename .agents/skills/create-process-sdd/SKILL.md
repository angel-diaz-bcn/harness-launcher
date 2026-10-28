---
name: create-process-sdd
description: Genera o actualiza la especificación técnica de un flujo de FLIK (PRC-XX) bajo la plantilla canónica `.spec.md`.
---

# Create Process SDD Skill

Genera o actualiza especificaciones de **Procesos** en `.ai-harness/sdd/2_PROCESSES/`.

## Convención obligatoria

- Carpeta: `<ID>-<slug>/`.
- Archivo: `<ID>-<slug>.spec.md`.
- Historia: `user_story.md`.
- Plantilla: `.ai-harness/sdd/templates/TEMPLATE_PROCESS_SDD.md`.
- Reglas completas: `.ai-harness/sdd/templates/README.md`.

## Directrices anti-deriva

- **Cero placeholders:** prohibido dejar secciones vacías o resúmenes informales.
- **Diagrama real:** el diagrama Mermaid debe coincidir con los pasos `ST-*`.
- **Mapeo campo a campo:** toda transformación de datos se declara explícitamente.
- **Recursos:** cada paso define éxito, error, cancelación y liberación de recursos.
- **Trazabilidad:** cada `ST-*` se mapea a `CT-*`, archivo::símbolo y `TC-*`.
- **BDD:** al menos dos escenarios Gherkin, uno de éxito y otro de fallo/recuperación.
- **Sin invención:** si falta información, se registra en `Q-*` y se detiene la implementación.

## Instrucciones de ejecución

```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-01 \
  --name "Reproducción magnet" \
  --target lib/features/tv_experience/application/playback_coordinator.dart \
  --dir .ai-harness/sdd/2_PROCESSES/playback/PRC-01-magnet-playback
```

El runner crea `user_story.md` y `<ID>-<slug>.spec.md` desde la plantilla. Completar todos los placeholders y validar el checklist de `.ai-harness/sdd/templates/README.md` antes de cambiar el estado a `APPROVED` y registrar la aprobación.
