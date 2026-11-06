# MANIFEST — qué copiar y qué no

Lista canónica de los elementos que forman el arnés. Al trasladarlo a un
proyecto nuevo, se copia **solo** la sección 1.

---

## 1. Núcleo copiable

| Ruta | Obligatorio | Función |
|---|---|---|
| `AGENTS.md` | Sí | Enrutador operativo |
| `harness.config.yaml` | Sí | Configuración estructural |
| `requirements.txt` | Sí | Dependencias del tooling |
| `LICENSE` | Sí | Licencia de código abierto MIT |
| `CONTRIBUTING.md` | Sí | Guía de contribución para humanos y agentes |
| `.gitattributes` | Sí | Normalización de saltos de línea LF para determinismo criptográfico |
| `.gitlab-ci.yml` | Opcional | Pipeline de CI/CD para GitLab |
| `.github/workflows/harness-ci.yml` | Opcional | Pipeline de CI/CD para GitHub Actions |
| `.github/*` y `.gitlab/*` | Opcional | Plantillas nativas de PR, MR e issues |
| `.aiignore` | Sí | Exclusión de contexto para el agente |
| `.gitignore` | Sí | Exclusión de control de versiones |
| `.clinerules/rules.md` | Sí | Reglas de integración del agente |
| `.clinerules/workflows/*.md` | Sí | Workflows invocables con `/` |
| `.agents/skills/<name>/SKILL.md` | Sí | Documentación de uso por skill |
| `.agents/skills/README.md` | Sí | Índice de skills |
| `.ai-harness/context/*` | Sí | 12 documentos normativos |
| `.ai-harness/scopes/*` | Sí | Límites de escritura |
| `.ai-harness/sdd/templates/*` | Sí | Plantillas y convención OpenSpec |
| `.ai-harness/sdd/modules/*` | Sí | Módulos vivos consolidados |
| `.ai-harness/sdd/changes/*` | Sí | Propuestas activas de cambio |
| `.ai-harness/sdd/archive/*` | Sí | Histórico de cambios completados |
| `.ai-harness/memory/*` | Sí | Modos de fallo, ADRs y feedback |
| `.ai-harness/design-system/*` | Sí | Tokens y documentos de diseño |
| `.ai-harness/fixtures/README.md` | Sí | Convención de datos de prueba |
| `.ai-harness/input/` | Sí | Carpeta para depositar PRDs y documentación previa |
| `.ai-harness/skills/**` | Sí | Validadores y runners |

---

## 2. No copiable

| Ruta | Motivo |
|---|---|
| `docs/` | Documentación explicativa de la formación |
| `README.md` | Presentación de esta plantilla (Español) |
| `README.en.md` | Presentación de esta plantilla (Inglés) |
| `MANIFEST.md` | Este archivo |
| `.ai-harness/memory/ephemeral_feedback/*` | Logs locales de ejecución |
| `.ai-harness/memory/sync-state.json` | Baseline generada por `sync-sdd` |
| `.git/` | Historia de la plantilla |

---

## 3. Checklist tras copiar

1. [ ] `harness.config.yaml`: `project.name`, `project.slug` y `project.stack`.
2. [ ] `context/project_overview.md`: sustituir todos los marcadores `<...>`.
3. [ ] `context/platform_matrix.md`: plataformas reales.
4. [ ] `scopes/*`: rutas autorizadas reales del proyecto.
5. [ ] `architecture.features`: features reales o lista vacía.
6. [ ] `architecture.forbidden_packages`: política de dependencias del proyecto.
7. [ ] `design-system/tokens.json`: valores de marca propios.
8. [ ] `legacy_terms`: términos del proyecto anterior, si existe migración.
9. [ ] Eliminar los apéndices de `.gitignore` y `.aiignore` que no apliquen.
10. [ ] `python .ai-harness/skills/harness-validator/runner.py` devuelve 0.
11. [ ] `python .ai-harness/skills/preflight/runner.py` devuelve 0.
12. [ ] `python .ai-harness/skills/sync-sdd/runner.py` devuelve 0.

---

## 4. Verificación de portabilidad

Prueba mínima: copiar la sección 1 a una carpeta vacía, instalar
`requirements.txt` y ejecutar `harness-validator`. Si devuelve 0, el arnés es
autónomo y no depende de la documentación ni del proyecto de origen.
