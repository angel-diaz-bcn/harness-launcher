# Índice de la documentación

Explicación del arnés: qué es cada pieza, por qué existe, qué valida y qué rompe
si falta. No contiene reglas nuevas: las reglas están en `.ai-harness/context/`.

---

## 1. Cómo leer esta documentación

### Ruta corta (30 minutos)

1. `01-que-es-un-harness.md`
2. `02-agents-md.md`
3. `cheatsheet.md`

Sirve para entender la idea y poder explicarla.

### Ruta operativa (2 horas)

1. `01` → `02` → `03` → `04` → `05`
2. `08-skills-y-validadores.md`
3. `cheatsheet.md`

Sirve para usar el arnés en un proyecto real sin romperlo.

### Ruta completa (4 horas)

Todas las páginas en orden. Sirve para diseñar y mantener un arnés propio.

---

## 2. Mapa de documentos

| Doc | Tema | Archivos que explica |
|---|---|---|
| `01-que-es-un-harness.md` | Problema y modelo mental | — |
| `02-agents-md.md` | El contrato con el agente | `AGENTS.md`, `.clinerules/rules.md` |
| `03-contexto.md` | Verdad normativa y orden de carga | `.ai-harness/context/*` |
| `04-scopes.md` | Límites de escritura | `.ai-harness/scopes/*` |
| `05-sdd.md` | Especificaciones y trazabilidad | `.ai-harness/sdd/*` |
| `06-design-system.md` | Tokens y disciplina visual | `.ai-harness/design-system/*` |
| `07-memoria.md` | Fallos, decisiones y feedback | `.ai-harness/memory/*` |
| `08-skills-y-validadores.md` | Automatización y puertas | `.ai-harness/skills/*` |
| `09-workflows.md` | Comandos y automatización de entrada | `.clinerules/workflows/*` |
| `10-ignorar.md` | `.gitignore` vs `.aiignore` | Ambos archivos |
| `11-cierre-y-auditoria.md` | Definition of Done y mantenimiento | `harness_governance.md` |
| `12-bootstrap-harness.md` | Inicializador interactivo y asistido del arnés | `.ai-harness/skills/bootstrap-harness/*`, `.ai-harness/input/*` |
| `cheatsheet.md` | Resumen de una página | — |

---

## 3. Anatomía de cada página

Todas siguen la misma estructura:

| Sección | Responde a |
|---|---|
| Qué es | Definición en dos frases |
| Por qué existe | El problema que evita |
| Archivos implicados | Tabla ruta → responsabilidad |
| Mecánica interna | Cómo encaja con el resto |
| Qué valida el arnés | Comprobaciones automáticas asociadas |
| Qué rompe si falta | Síntoma observable |
| Anti-patrón | Error frecuente |
| Referencias | Dónde seguir leyendo |

---

## 4. Qué no encontrarás aquí

- Reglas de producto: viven en `context/`.
- Contratos de datos: viven en las specs.
- Valores visuales: viven en `design-system/tokens.json`.
- Ejemplos de proyectos concretos: este arnés es genérico por diseño.

---

## 5. Convención de marcadores

En la plantilla, `<algo entre ángulos>` significa "sustitúyelo por el valor real
de tu proyecto". Un archivo con marcadores sin sustituir es documentación
incompleta, no un ejemplo.
