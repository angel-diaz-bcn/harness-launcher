# Catálogo de modos de fallo

Memoria persistente de errores que no deben repetirse. Cada entrada tiene
síntoma, riesgo, regla de prevención y verificación. El prefijo y el número
mínimo de entradas se declaran en `harness.config.yaml` (`memory.failure_prefix`,
`memory.min_failure_modes`).

---

## FM-001 — Deriva entre spec y código

- **Síntoma:** el código añade campos, estados, reglas o estilos que no están en la spec.
- **Riesgo:** la documentación miente y el comportamiento deja de ser predecible.
- **Prevención:** mapa de implementación, comentarios `/// Spec: <ID> / <FR|ST>` y baseline de `sync-sdd`.
- **Verificación:** `sync-sdd` en estado `PRESENT` tras cada cambio de comportamiento.

## FM-002 — Regla duplicada en dos fuentes de verdad

- **Síntoma:** la misma norma aparece en `AGENTS.md`, en un contexto y en un scope, con matices distintos.
- **Riesgo:** el agente elige la versión que le conviene; las reglas se contradicen sin que nadie lo note.
- **Prevención:** `AGENTS.md` solo enruta; cada regla vive en un único archivo de `context/` o de `scopes/`.
- **Verificación:** auditoría de §11 de `harness_governance.md` (búsqueda de reglas repetidas).

## FM-003 — Scope que apunta a rutas inexistentes

- **Síntoma:** el scope autoriza `lib/features/x/` pero esa carpeta no existe o ya se renombró.
- **Riesgo:** el agente escribe en el sitio equivocado o se bloquea sin motivo.
- **Prevención:** todo scope declara rutas reales y se revisa al mover código.
- **Verificación:** `check_context` (`SCOPE-MISSING-AUTHORIZED-PATH`, `SCOPE-FORBIDDEN-PATH`).

## FM-004 — Skill fantasma o no registrada

- **Síntoma:** un workflow menciona un comando que no tiene runner, o existe un runner que el registro desconoce.
- **Riesgo:** la documentación ofrece herramientas que no existen y el agente las invoca igualmente.
- **Prevención:** toda skill tiene `skill.yaml`, runner, `SKILL.md` y entrada en `registry.yaml`.
- **Verificación:** `check_skills` (`SKILL-UNREGISTERED`, `SKILL-MISSING-FILE`, `SKILL-REGISTRY-ORPHAN`).

## FM-005 — Validación desactivada para "hacer pasar" el cambio

- **Síntoma:** se comenta un check, se relaja una lista o se usa `--no-verify`.
- **Riesgo:** el arnés deja de proteger y la deuda se acumula en silencio.
- **Prevención:** un fallo se corrige en la causa raíz; los checks solo cambian con justificación y versión.
- **Verificación:** revisión de `git diff` sobre `.ai-harness/skills/` en cada publicación.
