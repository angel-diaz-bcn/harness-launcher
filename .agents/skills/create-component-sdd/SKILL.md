---
name: create-component-sdd
description: Crea el esqueleto de una spec de componente (CMP-NN) a partir de la plantilla canónica .spec.md.
---

# Create Component SDD

Crea el esqueleto de una spec de componente (`CMP-NN`) a partir de la plantilla
canónica.

## Comando

```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-01 \
  --name "Nombre del componente" \
  --target lib/<ruta>/<archivo> \
  --dir .ai-harness/sdd/1_COMPONENTS/<capa>/CMP-01-<slug>
```

## Parámetros

| Parámetro | Obligatorio | Descripción |
|---|---|---|
| `component_id` | Sí | `CMP-NN`; el prefijo viene de la configuración |
| `--name` | Sí | Nombre legible del componente |
| `--target` | Sí | Ruta de implementación bajo una ruta autorizada |
| `--dir` | Sí | Carpeta donde se crean spec e historia |
| `--layer` | No | `bootstrap`, `domain` o `ui`; se infiere de `--dir` |
| `--force` | No | Sobrescribe un esqueleto existente |

## Qué genera

- `<ID>-<slug>.spec.md` con la plantilla canónica exhaustiva de 15 secciones (Protocolo, Problema, Requisitos `FR-*`, Reglas `BR-*`, Estados y Errores, Contratos `CT-*`, Trazabilidad §10, Pruebas `TC-*` y BDD).
- `user_story.md` con la historia de usuario estructurada: Resumen Ejecutivo, Problema, Actores primarios y secundarios, Historia formal, Criterios BDD (Escenario de éxito y de contingencia) y Fuera de alcance.

## Flujo de trabajo para redactar la especificación

Para evitar specs incompletas o superficiales, sigue este protocolo estricto:

1. **Definir la Historia de Usuario (`user_story.md`):** Explicar el valor de negocio real y al menos 2 criterios de aceptación en formato BDD (`Dado / Cuando / Entonces`).
2. **Requisitos Funcionales (§4):** Listar requisitos atómicos `FR-01`, `FR-02`, etc., con prioridad MoSCoW (`Must`, `Should`).
3. **Reglas de Negocio (§5):** Declarar invariantes `BR-*` e `INV-*` con su fuente canónica.
4. **Estados y Errores (§6):** Diagramar la máquina de estados en Mermaid y catalogar los errores con códigos tipados.
5. **UI y Foco (§7, si es capa `ui`):** Referenciar tokens de `tokens.json` y orden de foco por teclado/D-Pad. En otras capas indicar "No aplica".
6. **Contratos de Datos (§8):** Escribir los tipos, clases inmutables e interfaces `CT-*` exactas.
7. **Mapa de Implementación (§10):** Mapear cada fila `FR` → `CT` → `archivo::símbolo` → `TC` con estado `Pending`.
8. **Pruebas (§11 y §12):** Detallar los casos de prueba unitarios/integración `TC-*` y escenarios Gherkin.
9. **Aprobación:** Solo cuando todo esté completo y sin placeholders `<...>`, cambiar `status: DRAFT` a `status: APPROVED` asignando `approved_at` y `approved_by`.

## Reglas

- SDD-First: Prohibido escribir código en `lib/` o `src/` sin que la spec esté en estado `APPROVED`.
- No inventa identificadores ni capas: los lee de `harness.config.yaml`.
- No sobrescribe sin `--force`.
