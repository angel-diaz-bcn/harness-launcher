# FLIK — Gobernanza del Harness

Este documento define las reglas del propio arnés `.ai-harness/`. No describe el producto; para eso están `project_overview.md`, `architecture_rules.md` y el resto del contexto.

---

## 1. Propósito y autoridad

El arnés existe para que cualquier agente o desarrollador pueda:

- saber qué reglas son inmutables;
- saber dónde escribir y dónde no;
- encontrar la spec de lo que va a implementar;
- validar que código y especificación no divergen;
- repetir errores conocidos.

`AGENTS.md` es el enrutador. Este documento es la constitución del arnés.

---

## 2. Mapa de directorios y propietario

| Directorio | Contenido | Propietario |
|---|---|---|
| `context/` | Verdad de producto, arquitectura, diseño, seguridad y gobernanza | Arquitectura |
| `design-system/` | Sistema de diseño: foundations, tokens, layout, componentes, páginas y code-mapping | Arquitectura + Diseño |
| `scopes/` | Límites de escritura por bloque | Arquitectura |
| `sdd/` | Especificaciones e historias de usuario | Producto + Arquitectura |
| `memory/` | Modos de fallo y decisiones | Arquitectura |
| `skills/` | Skills ejecutables y manifiestos | Plataforma |
| `fixtures/` | Datos deterministas para pruebas | QA |
| `.clinerules/` | Reglas de workspace (`rules.md`) | Plataforma |
| `.clinerules/workflows/` | Workflows invocables con `/` | Plataforma |

Regla: un archivo vive en un único lugar. Prohibido duplicar reglas, skills o manifiestos en dos árboles.

---

## 3. Orden de carga

1. `system_identity.md`
2. `harness_governance.md`
3. `project_overview.md`
4. `architecture_rules.md`
5. `ui-design-system.md` y `design-system/README.md`
6. `scopes/block_<área>.md`
7. `sdd_framework.md`
8. Spec `.spec.md` activa
9. `memory/failure_modes.md`

Si falta cualquier pieza para la tarea, el agente debe detenerse.

---

## 4. Jerarquía de verdad

1. `context/` y `scopes/`.
2. Spec `.spec.md` aprobada.
3. Contratos y código.
4. Documentación auxiliar.

Si el código contradice la spec, el código está mal. Si la spec contradice el contexto, la spec está mal. Nunca se resuelve la contradicción inventando una tercera regla.

---

## 5. Convenciones de nombre

- Specs: `<ID>-<slug>.spec.md`.
- Componentes: `CMP-NN`.
- Procesos: `PRC-XX`.
- Scopes: `block_<área>.md`.
- Skills: `<nombre>/skill.yaml`, `<nombre>/runner.py`, `.agents/skills/<nombre>/SKILL.md`.

La taxonomía física de specs por pantalla está aprobada: una spec de pantalla puede contener una carpeta `components/` con las specs de sus componentes, cada una en su carpeta `<ID>-<slug>` con su `user_story.md`. Ver `sdd/templates/README.md` §2.1.

---

## 6. Reglas de skills

Cada skill debe tener:

1. `skill.yaml` con `name`, `version`, `description`, `command`, `inputs` y `outputs`.
2. Un runner ejecutable y determinista.
3. Documentación en `.agents/skills/<nombre>/SKILL.md`.
4. Entrada en `skills/registry.yaml`.
5. Un comando de verificación o test cuando aplique.

Prohibido:

- skills fantasma en documentación sin runner;
- dos runners para la misma skill;
- runners que impriman éxito sin ejecutar la acción;
- skills que dependan de servicios externos no declarados.

---

## 7. Puertas de validación

| Puerta | Valida | Cuándo |
|---|---|---|
| `harness-validator` | Estructura del arnés: contexto, scopes, memoria, SDD, skills | Antes de cerrar cualquier cambio |
| `preflight` | Código Flutter/Dart, arquitectura, tokens, invariantes P2P | Antes de cerrar cambios de producto |
| `sync-sdd` | Spec ↔ target ↔ implementación | Antes de publicar o cerrar una spec |
| `git-publish` | Ambas puertas antes de publicar | Solo bajo petición explícita |

Un fallo de validación no se ignora ni se desactiva. Se corrige la causa raíz.

---

## 8. Herramientas y lenguajes

- **Producto:** Dart y Flutter.
- **Tooling del arnés:** Python y PowerShell están permitidos exclusivamente para validadores, runners y automatización.
- **Prohibido** introducir tecnologías de backend, analítica o UI web en el producto.

Esta separación evita confundir “el proyecto no usa Python” con “el arnés no puede usar Python”.

---

## 9. Cambio, deprecación y limpieza

- Toda regla nueva se añade a `context/` o a un scope, no a `AGENTS.md`.
- Toda skill nueva se registra en `skills/registry.yaml`.
- Toda spec conserva su historial; no se borra al implementarse.
- Una spec reemplazada se marca `SUPERSEDED` y apunta a su reemplazo con `superseded_by`.
- Los cambios normativos vuelven la spec a `DRAFT` hasta su reaprobación.
- Toda skill obsoleta se marca `deprecated` y se retira tras migrar sus referencias.
- Prohibido dejar directorios vacíos, archivos huérfanos o documentación de otro proyecto.
- Los logs de fallo van a `memory/ephemeral_feedback/`, nunca a `fixtures/`.
- Los fixtures son datos deterministas de prueba; no son logs ni caché.

---

## 10. Definition of Done del harness

- [ ] `harness-validator` devuelve exit code 0.
- [ ] `preflight` devuelve exit code 0 o un warning justificado.
- [ ] `sync-sdd` reporta explícitamente `N/A`, `MISSING`, `PRESENT` o `DIVERGED`.
- [ ] Cada skill tiene manifiesto, runner, documentación y registro.
- [ ] Cada scope apunta a una ruta existente de `lib/`.
- [ ] Cada spec tiene `user_story.md`, `.spec.md`, `target` y mapa de implementación.
- [ ] No hay referencias al proyecto anterior ni a las tecnologías que utilizaba.
- [ ] No hay dos fuentes de verdad para la misma regla.

---

## 11. Auditoría periódica

Ejecutar como mínimo antes de cada release:

1. Buscar términos prohibidos en `context/`, `scopes/`, `AGENTS.md` y `skills/`.
2. Comparar scopes con `project_structure.md`.
3. Comparar `skills/registry.yaml` con los `skill.yaml` reales.
4. Verificar que cada spec tiene target y pruebas.
5. Verificar que `AGENTS.md` solo enruta y no duplica reglas.
