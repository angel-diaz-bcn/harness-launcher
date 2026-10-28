# 07 — Memoria: fallos, decisiones y feedback

## Qué es

`memory/` es la parte del arnés que aprende. Guarda tres cosas distintas:

1. **Modos de fallo** — errores que no deben repetirse.
2. **Decisiones (ADR)** — por qué se eligió una tecnología o una estructura.
3. **Feedback efímero** — la última ejecución fallida, para corregir en caliente.

## Por qué existe

Un agente sin memoria comete el mismo error con nombres nuevos cada semana.
La memoria convierte cada fallo en una regla concreta y cada decisión en un
documento que evita reabrir el debate.

## Archivos implicados

| Ruta | Contenido | ¿Versionado? |
|---|---|---|
| `memory/failure_modes.md` | Catálogo `FM-NNN` con síntoma, riesgo, prevención y verificación | Sí |
| `memory/decisions/README.md` | Convención de ADRs | Sí |
| `memory/decisions/ADR-NNNN-<slug>.md` | Decisiones inmutables | Sí |
| `memory/decisions/ADR-0000-plantilla.md` | Plantilla de ADR | Sí |
| `memory/ephemeral_feedback/*` | Salida de la última validación fallida | No |
| `memory/sync-state.json` | Baseline de `sync-sdd` | No |
| `memory/README.md` | Índice y ciclo de corrección | Sí |

## Mecánica interna

### Ciclo de auto-corrección

```
1. Un validador falla
2. El fallo se escribe en ephemeral_feedback/last_failure.md
3. El agente lee el fallo, corrige la causa raíz
4. Vuelve a validar
5. Si el fallo era recurrente, se añade a failure_modes.md
6. Si el cambio altera una decisión, se registra un ADR
```

### Anatomía de un modo de fallo

```markdown
## FM-004 — Skill fantasma o no registrada

- **Síntoma:** un workflow menciona un comando sin runner.
- **Riesgo:** se invocan herramientas que no existen.
- **Prevención:** toda skill tiene manifiesto, runner, doc y registro.
- **Verificación:** check_skills (SKILL-UNREGISTERED).
```

Las cuatro secciones son obligatorias: sin verificación, la prevención es
una intención.

### Inmutabilidad de los ADR

Un ADR no se reescribe. Si la decisión cambia, se crea otro que la reemplaza y
ambos se enlazan. Reescribir el pasado destruye la única prueba de por qué el
sistema es como es.

## Qué valida el arnés

`check_memory` aplica:

| Regla | Qué detecta |
|---|---|
| `MEM-MISSING-FAILURE-MODES` | No existe el catálogo de fallos |
| `MEM-INSUFFICIENT-CONTENT` | El catálogo es demasiado corto para ser útil |
| `MEM-INSUFFICIENT-FAILURE-MODES` | Menos entradas que `memory.min_failure_modes` |
| `MEM-LEGACY-TERMS` | Términos del proyecto anterior |
| `MEM-MISSING-DECISIONS` | Falta el índice de decisiones |
| `MEM-MISSING-EPHEMERAL` | Falta el directorio de feedback |

El prefijo (`FM` por defecto) y el mínimo de entradas se configuran en
`harness.config.yaml`.

## Qué rompe si falta

- Los mismos errores se repiten y se depuran desde cero.
- Las decisiones se reabren en cada sesión sin contexto histórico.
- El agente corrige el síntoma, no la causa, y el fallo reaparece.
- Nadie sabe si un fallo ya estaba catalogado.

## Anti-patrón

Convertir `failure_modes.md` en un diario:

```markdown
## 2025-03-14
Hoy el test falló y lo arreglé cambiando el mock.
```

Eso no es un modo de fallo: es una anécdota. Un modo de fallo es reutilizable,
abstracto y verificable.

## Cómo mantenerlo

1. Un fallo entra en memoria solo si puede repetirse.
2. Cada entrada tiene verificación automática o manual explícita.
3. Los ADRs se numeran de forma correlativa y nunca se reescriben.
4. `ephemeral_feedback/` se vacía en cada ciclo correcto.
5. `sync-state.json` no se edita a mano: lo genera `sync-sdd`.

## Referencias

- `08-skills-y-validadores.md` — quién escribe el feedback.
- `11-cierre-y-auditoria.md` — auditoría de memoria.
