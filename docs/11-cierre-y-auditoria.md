# 11 — Cierre, auditoría y mantenimiento

## Qué es

El conjunto de criterios y rutinas que impiden que el arnés se degrade con el
tiempo. Un arnés no se rompe de golpe: se ablanda por acumulación de excepciones.

## Por qué existe

Los arneses mueren por cuatro causas conocidas:

1. **Reglas duplicadas** que se contradicen y nadie borra.
2. **Checks desactivados** para cerrar un cambio con prisa.
3. **Documentación desactualizada** que el agente usa como verdad.
4. **Referencias muertas** a archivos, skills o rutas que ya no existen.

Este documento define cómo detectarlas antes de que el arnés deje de servir.

## Archivos implicados

| Archivo | Contenido |
|---|---|
| `context/harness_governance.md` | Constitución del arnés |
| `harness.config.yaml` | Estructura declarada |
| `skills/registry.yaml` | Inventario de skills |
| `memory/failure_modes.md` | Errores conocidos |
| `sdd/**` | Specs y su estado |

## Mecánica interna

### Definition of Done

Un cambio está terminado cuando:

- [ ] `harness-validator` devuelve 0.
- [ ] `preflight` devuelve 0 o un warning justificado.
- [ ] `sync-sdd` no reporta `DIVERGED`.
- [ ] Cada skill tocada mantiene manifiesto, runner, doc y registro.
- [ ] Cada scope apunta a rutas existentes.
- [ ] Cada spec tiene historia, target y mapa de implementación.
- [ ] No hay términos del proyecto anterior.
- [ ] No hay dos fuentes de verdad para la misma regla.

### Auditoría periódica

Antes de cada release:

| # | Comprobación | Cómo |
|---|---|---|
| 1 | Términos heredados | `legacy_terms` en la configuración + búsqueda manual |
| 2 | Scopes vs estructura | Comparar `scopes/*` con `project_structure.md` |
| 3 | Registro vs realidad | Comparar `registry.yaml` con los `skill.yaml` reales |
| 4 | Specs con target y pruebas | Revisar `status: APPROVED` |
| 5 | `AGENTS.md` sin reglas duplicadas | Lectura crítica de una página |
| 6 | Enlaces y rutas | Comprobar que todo path citado existe |

### Cambio y deprecación

- Una regla nueva se añade a `context/` o a un scope, nunca a `AGENTS.md`.
- Una skill obsoleta se marca `deprecated` y se retira tras migrar referencias.
- Una spec reemplazada se marca `SUPERSEDED` con `superseded_by`.
- Un cambio normativo devuelve la spec a `DRAFT`.
- Un check solo cambia con justificación y actualización de su documentación.
- Una decisión se reemplaza con otro ADR, nunca reescribiendo el anterior.

## Qué valida el arnés

| Regla | Check |
|---|---|
| Estructura y contenido del contexto | `check_context` |
| Memoria mínima y decisiones | `check_memory` |
| Specs, estados y trazabilidad | `check_sdd` |
| Skills registradas y documentadas | `check_skills` |
| Código, arquitectura, tokens | `preflight` |
| Deriva spec ↔ implementación | `sync-sdd` |

Lo que **no** valida ningún check automático: duplicación semántica de reglas,
calidad de la prosa normativa y coherencia de la jerarquía de verdad. Eso exige
lectura humana y es el motivo de la auditoría.

## Qué rompe si falta

- El arnés se convierte en ruido que se ignora.
- Los checks pasan pero el repositorio está mal documentado.
- Se pierde la trazabilidad y vuelve la deriva.
- Cada nuevo miembro del equipo aprende el arnés por ósmosis.

## Anti-patrón

Cerrar un cambio con `--no-verify` "solo esta vez".

Un check desactivado una vez no se reactiva. La única salida legítima es
corregir la causa, y si la regla es incorrecta, cambiarla explícitamente con su
justificación y su versión.

## Rutina mínima por cambio

```
1. harness-validator
2. preflight
3. sync-sdd
4. ¿Cambió el comportamiento? → actualizar spec y mapa
5. ¿Error recurrente?        → añadir a failure_modes.md
6. ¿Decisión estructural?    → añadir ADR
```

## Referencias

- `07-memoria.md` — cómo se registra lo aprendido.
- `08-skills-y-validadores.md` — qué comprueba cada puerta.
