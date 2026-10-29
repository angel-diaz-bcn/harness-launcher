# Cheatsheet

Una página. Comandos, rutas, reglas y a dónde va cada cosa.

---

## 1. Comandos

```bash
# Instalación del tooling (una vez)
python -m pip install -r requirements.txt

# Inicialización asistida del arnés (nuevo proyecto o tras fork)
python .ai-harness/skills/bootstrap-harness/runner.py --interactive

# Las tres puertas
python .ai-harness/skills/harness-validator/runner.py
python .ai-harness/skills/preflight/runner.py
python .ai-harness/skills/sync-sdd/runner.py

# Modo estricto y salida JSON
python .ai-harness/skills/harness-validator/runner.py --strict --json

# Sincronización de una spec y baseline
python .ai-harness/skills/sync-sdd/runner.py CMP-01
python .ai-harness/skills/sync-sdd/runner.py --baseline

# Nuevas specs
python .ai-harness/skills/create-component-sdd/runner.py CMP-01 --name "..." --target lib/... --dir ...
python .ai-harness/skills/create-process-sdd/runner.py PRC-01 --name "..." --target lib/... --dir ...

# Arranque (stack Flutter)
python .ai-harness/skills/launch-app/runner.py --list

# Publicación (solo bajo petición explícita)
python .ai-harness/skills/git-publish/runner.py status
```

| Exit | Significado |
|---|---|
| 0 | Sin fallos |
| 1 | Hay fallos de validación |
| 2 | Faltan dependencias del tooling |

---

## 2. Rutas

| Quiero... | Voy a |
|---|---|
| Saber qué leer primero | `AGENTS.md` |
| Cambiar la estructura del arnés | `harness.config.yaml` |
| Escribir una regla nueva | `.ai-harness/context/` o un scope |
| Saber dónde puedo escribir | `.ai-harness/scopes/` |
| Especificar un componente | `.ai-harness/sdd/1_COMPONENTS/` |
| Especificar un proceso | `.ai-harness/sdd/2_PROCESSES/` |
| Añadir un valor visual | `.ai-harness/design-system/tokens.json` |
| Registrar un error recurrente | `.ai-harness/memory/failure_modes.md` |
| Documentar una decisión | `.ai-harness/memory/decisions/` |
| Añadir un validador | `.ai-harness/skills/<skill>/` + `registry.yaml` |
| Explicar el arnés | `docs/` |

---

## 3. Claves de configuración

| Clave | Para qué |
|---|---|
| `project.name` / `.slug` / `.stack` | Identidad del proyecto |
| `context.required` | Documentos normativos obligatorios |
| `context.agents_must_reference` | Referencias obligatorias en `AGENTS.md` |
| `scopes.required` | Scopes obligatorios |
| `scopes.path_roots` | Rutas autorizadas |
| `scopes.forbidden_paths` | Rutas prohibidas de otro proyecto |
| `sdd.component_prefix` / `.process_prefix` | Identificadores |
| `sdd.component_layers` | Capas válidas |
| `sdd.frontmatter` | Campos obligatorios de una spec |
| `memory.failure_prefix` / `.min_failure_modes` | Memoria |
| `legacy_terms` | Términos heredados prohibidos |
| `architecture.features` | Features declaradas |
| `architecture.forbidden_by_feature` | Fronteras entre features |
| `architecture.forbidden_packages` | Dependencias prohibidas |
| `ui.token_feature` | Feature con navegación por foco |
| `invariants.profile` | Perfil de checks (`none` / `streaming`) |

---

## 4. Reglas que no se negocian

1. Sin spec aprobada no hay código de producción.
2. Una regla, un archivo. Si aparece dos veces, una copia está mal.
3. Un fallo se corrige en la causa raíz, nunca desactivando el check.
4. Prohibidos los valores visuales literales fuera del tema.
5. Prohibida la telemetría de usuario y las dependencias de analítica.
6. `git push` solo con instrucción explícita.
7. Si falta información, se detiene el trabajo y se pregunta.

---

## 5. Decisiones rápidas

**¿Dónde escribo esta regla?**
→ Si es del sistema: `context/`. Si es un límite de escritura: `scopes/`. Si es
de una unidad concreta: la spec. Nunca en `AGENTS.md`.

**¿Necesito un ADR?**
→ Si la decisión afecta a dependencias, licencias, persistencia, rendimiento o
fronteras entre módulos: sí.

**¿Necesito un modo de fallo?**
→ Si el error puede repetirse y tiene una verificación concreta: sí.

**¿Necesito una skill nueva?**
→ Si la comprobación es repetible y determinista: sí. Si es juicio humano: no,
documenta el criterio en `context/`.

**¿Componente o proceso?**
→ Componente si existe por sí mismo. Proceso si describe cómo colaboran dos o
más componentes.

---

## 6. Antes de decir "terminado"

```
harness-validator  0
preflight          0
sync-sdd           0
spec actualizada si cambió el comportamiento
failure_modes actualizado si el error era recurrente
```
