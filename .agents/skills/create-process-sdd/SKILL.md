---
name: create-process-sdd
description: Crea el esqueleto de una spec de proceso (PRC-NN) a partir de la plantilla canónica .spec.md.
---

# Create Process SDD

Crea el esqueleto de una spec de proceso (`PRC-NN`) a partir de la plantilla
canónica.

## Comando

```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-01 \
  --name "Nombre del proceso" \
  --target docs/flows/<nombre_flujo>.md \
  --dir .ai-harness/sdd/2_PROCESSES/<modulo>/PRC-01-<slug> \
  --block 2_PROCESSES
```

## Parámetros

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `process_id` | Sí | `PRC-NN`; el prefijo viene de la configuración |
| `--name` | Sí | Nombre legible del proceso |
| `--target` | Sí | Ruta de implementación bajo una ruta autorizada |
| `--dir` | Sí | Carpeta donde se crean spec e historia |
| `--block` | No | Bloque propietario del proceso |
| `--force` | No | Sobrescribe un esqueleto existente |

## Qué genera

- `<ID>-<slug>.spec.md` con la plantilla canónica exhaustiva de 16 secciones (Protocolo, Resultado esperado, Disparador y condiciones, Actores y participantes, Flujo Mermaid, Pasos `ST-*`, Estados y Errores, Contratos `CT-*`, Invariantes, Trazabilidad §11, Pruebas `TC-*` y BDD).
- `user_story.md` con la historia de usuario estructurada: Resumen Ejecutivo, Problema, Actores y Participantes, Historia formal, Criterios BDD y Fuera de alcance.

## Flujo de trabajo para redactar la especificación

Para evitar flujos indefinidos o frágiles, sigue este protocolo:

1. **Definir la Historia de Usuario (`user_story.md`):** Identificar qué flujo orquesta, los componentes involucrados y los escenarios BDD de éxito y de aborto/contingencia.
2. **Disparador y Condiciones (§2):** Fijar claramente el trigger, precondiciones, postcondiciones y política de reintento.
3. **Flujo y Secuencia (§5):** Diseñar el diagrama de secuencia Mermaid numerado con todos los actores y participantes (`CMP-*`).
4. **Pasos Atómicos (§6):** Desglosar la secuencia en pasos `ST-01`, `ST-02`, etc., asignando el componente responsable de cada paso.
5. **Errores y Recuperación (§7):** Para cada paso `ST-*`, documentar la estrategia de contingencia y liberación de recursos.
6. **Contratos Expuestos (§9):** Especificar la función o pipeline orquestador `CT-*`.
7. **Mapa de Implementación (§11):** Mapear cada paso `ST` → `CT` → `archivo::símbolo` → `TC`.
8. **Pruebas y BDD (§12 y §13):** Detallar los tests de integración `TC-*` y escenarios BDD.
9. **Aprobación:** Solo cuando no queden placeholders `<...>`, pasar a `status: APPROVED` con fecha y responsable.

## Reglas

- El proceso orquesta, no reimplementa: delega el trabajo en componentes `CMP-*`.
- No inventa identificadores: los lee de `harness.config.yaml`.
- No sobrescribe sin `--force`.
