# 12 — bootstrap-harness: Inicializador del arnés

## Qué es

`bootstrap-harness` es la skill que transforma la plantilla neutra ("carcasa")
en un arnés completamente adaptado a un proyecto nuevo. Funciona mediante un
asistente conversacional guiado por la doctrina de `docs/` o mediante la ingesta
semántica de documentación previa depositada en `.ai-harness/input/`.

## Por qué existe

Adaptar manualmente un arnés a un proyecto nuevo exige editar más de 20 archivos:
`harness.config.yaml`, los 12 documentos de contexto, los scopes de escritura,
los ignorados de Git/IA, las decisiones iniciales y la primera spec. Hacerlo a mano:

1. **Provoca omisiones:** quedan textos residuales como `<PROYECTO>` o reglas
   inconsistentes entre archivos.
2. **Exige conocimiento previo:** una persona sin experiencia en la gobernanza
   del arnés no sabe qué valores espera cada validador.
3. **Desaprovecha documentación existente:** si el equipo ya dispone de un PRD
   o especificación técnica, redactar el arnés desde cero es duplicar esfuerzo.
4. **Desconecta las skills del stack real:** si el proyecto es Python o Node,
   skills como `launch-app` o `git-publish` deben adaptarse al lenguaje y a la
   plataforma (GitLab vs GitHub).

`bootstrap-harness` automatiza todo el proceso garantizando que, al concluir, el
repositorio queda 100% configurado, vinculado a su repositorio remoto y con todas
las puertas de validación en verde.

## Archivos implicados

```
.ai-harness/input/                 # Carpeta para depositar PRDs, briefs o especificaciones
.ai-harness/skills/bootstrap-harness/
├── skill.yaml                     # Manifiesto canónico de la skill
├── runner.py                      # Punto de entrada CLI con validación final
├── models.py                      # Modelos tipados con Pydantic v2
├── input_scanner.py               # Motor de escaneo e ingesta de documentos
├── prompter.py                    # Entrevistador interactivo con referencias a docs/
├── generator.py                   # Compilador y generador atómico 360°
└── SKILL.md                       # Especificación técnica de la skill

.agents/skills/bootstrap-harness/SKILL.md  # Documentación operativa para agentes y usuarios
.clinerules/workflows/bootstrap-harness.md # Workflow invocable (/bootstrap-harness.md)
```

## Mecánica interna

### 1. Ingesta de contexto previo (Document-Aware)

Antes de iniciar las preguntas, el motor `InputScanner` revisa `.ai-harness/input/`.
Si encuentra archivos `.md`, `.txt`, `.json` o `.yaml`, extrae heurísticamente:

- Nombre comercial y descripción del producto.
- Stack tecnológico sugerido (Flutter, Python, Node, Go, Rust, etc.).
- Módulos funcionales y candidatos a scopes.
- Requisitos de privacidad y persistencia.

### 2. Entrevista accesible guiada por docs/

El módulo `Prompter` guía al usuario mediante un formato universal diseñado tanto
para desarrolladores como para perfiles no técnicos:

```mermaid
flowchart TD
    IN[Documentación en .ai-harness/input/] --> SCAN[Escaneo semántico]
    SCAN --> F1[1. Identidad del Producto docs/01]
    F1 --> F2[2. Stack & Plataformas docs/08]
    F2 --> F3[3. Módulos & Scopes docs/04]
    F3 --> F4[4. UI, Tokens & Privacidad docs/06]
    F4 --> F5[5. Modos de Fallo & ADR docs/07]
    F5 --> F6[6. Repositorio Git: GitLab vs GitHub]
    F6 --> GEN[Generación atómica 360°]
    GEN --> VAL[Puerta de enlace: harness-validator]
```

Cada pregunta incluye:
- **Explicación llana:** *"¿Por qué importa?"* sin jerga innecesaria.
- **Fundamento canónico:** cita explícitamente el documento de `docs/` que rige la norma.
- **Opciones numeradas:** con la opción técnica más recomendada señalada.
- **🤖 Decidir por mí:** la IA deduce la mejor decisión técnica basándose en la
  documentación previa o en el estándar de la industria.
- **✏️ Campo abierto:** permite especificar respuestas personalizadas.

### 3. Detección Git (GitLab vs GitHub) y Autenticación Segura

Por cumplimiento estricto de `security_privacy.md`, **nunca se solicitan ni
almacenan contraseñas en el repositorio**.

1. **Detección automática del proveedor:** Analiza la URL y distingue entre
   GitLab (`gitlab.com`), GitHub (`github.com`) o Bitbucket.
2. **Autenticación SSH o HTTPS:**
   - Si es **SSH** (`git@...`): ejecuta una verificación en vivo (`ssh -T`)
     para confirmar la autorización del usuario.
   - Si es **HTTPS** (`https://...`): delega la gestión en el Git Credential Manager
     del sistema operativo mediante Personal Access Tokens (PAT).
3. **Pipeline CI/CD automático:** Genera `.gitlab-ci.yml` o `.github/workflows/harness-ci.yml`
   para correr `harness-validator` y `preflight` en cada push o Merge/Pull Request.

### 4. Adaptación Polimórfica de Skills

`bootstrap-harness` parametriza las skills existentes para que funcionen con el
stack y proveedor elegido:

- **`git-publish`:** tras publicar cambios, emite el enlace directo para crear el
  **Merge Request** en GitLab o el **Pull Request** en GitHub.
- **`launch-app`:** ejecuta el comando real del stack configurado en `harness.config.yaml`
  (`uvicorn` en Python, `pnpm dev` en Node, `go run` en Go, `flutter run` en Flutter).
- **`preflight`:** ajusta la validación de linters y tests según el lenguaje.

### 5. Generación atómica 360°

`HarnessGenerator` escribe o reescribe en una única pasada coherente:

| Artefacto | Contenido generado |
|---|---|
| `harness.config.yaml` | Nombre, slug, stack, comandos de launch/test, proveedor Git, scopes y paquetes prohibidos. |
| `AGENTS.md` | Orquestador puro: mantiene la carga JIT estricta y tabla de tareas sin reglas de negocio. |
| `README.md` | Presentación del producto real, URL de repo, comandos de arranque y guía para agentes. |
| `.gitignore` / `.aiignore` | Exclusiones específicas del stack elegido (builds, cachés, virtualenvs) y secretos. |
| `.ai-harness/context/*.md` | Los 12 documentos normativos redactados según las decisiones de la entrevista. |
| `.ai-harness/scopes/block_*.md` | Un archivo de scope por módulo con `path_roots` y `forbidden_paths` explícitos. |
| `.ai-harness/memory/failure_modes.md` | 5 modos de fallo iniciales (`FM-01` a `FM-05`) adaptados al stack. |
| `.ai-harness/memory/decisions/` | `ADR-0001` documentando la elección del stack y arquitectura. |
| `.ai-harness/design-system/tokens.json` | Tokens de color, tipografía y espaciado (o perfil de API si es backend). |
| `.ai-harness/sdd/.../CMP-00-*.spec.md` | Especificación inicial de arranque del sistema (`app-bootstrap`). |
| `.gitlab-ci.yml` / GitHub Actions | Canalización remota de calidad en GitLab o GitHub. |

### 6. Modos de ejecución del runner

```bash
# 1. Modo interactivo estándar (recomendado para nuevos proyectos):
python .ai-harness/skills/bootstrap-harness/runner.py --interactive

# 2. Modo simulación (inspecciona qué generaría sin tocar el disco):
python .ai-harness/skills/bootstrap-harness/runner.py --interactive --dry-run

# 3. Modo desatendido mediante manifiesto YAML:
python .ai-harness/skills/bootstrap-harness/runner.py --manifest mi-producto.yaml
```

## Qué valida el arnés

`harness-validator` (`check_skills`) comprueba sobre esta skill:

1. Existencia obligatoria de `skill.yaml` y `runner.py`.
2. Presencia de la documentación canónica en `.agents/skills/bootstrap-harness/SKILL.md`.
3. Registro activo en `.ai-harness/skills/registry.yaml`.
4. Sintaxis válida del runner y correspondencia del comando de ejecución.

## Referencias

- `08-skills-y-validadores.md` — arquitectura de las skills del arnés.
- `09-workflows.md` — workflow `/bootstrap-harness.md`.
- `MANIFEST.md` — lista canónica de elementos del arnés.
