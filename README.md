# 🚀 AI Harness Launcher

> **Entorno de desarrollo asistido por IA gobernado, determinista y auditable.**  
> Este repositorio cumple una **doble función**: es una **guía didáctica y de referencia canónica** sobre cómo diseñar y gobernar un arnés de IA profesional, y al mismo tiempo es una **herramienta generadora (launcher)** capaz de montar un arnés a medida para cualquier stack y producto real mediante la skill `bootstrap-harness`.

---

## 🧭 Tabla de contenidos

1. [¿Qué es este proyecto?](#-qué-es-este-proyecto)
2. [Los dos propósitos del repositorio](#-los-dos-propósitos-del-repositorio)
3. [Arquitectura conceptual: cómo funciona el arnés](#-arquitectura-conceptual-cómo-funciona-el-arnés)
4. [Estructura del proyecto y zonas](#-estructura-del-proyecto-y-zonas)
5. [Guía de uso: dos formas de utilizarlo](#-guía-de-uso-dos-formas-de-utilizarlo)
   - [Modo A: didáctico / estudio y referencia](#modo-a-didáctico--estudio-y-referencia)
   - [Modo B: lanzador de un proyecto real (`bootstrap-harness`)](#modo-b-lanzador-de-un-proyecto-real-bootstrap-harness)
6. [Las puertas de calidad (*quality gates*)](#-las-puertas-de-calidad-quality-gates)
7. [Catálogo de *skills* y flujos de trabajo (*workflows*)](#-catálogo-de-skills-y-flujos-de-trabajo-workflows)
8. [Reglas de oro no negociables](#-reglas-de-oro-no-negociables)

---

## 💡 ¿Qué es este proyecto?

Cuando se trabaja con modelos de IA (Antigravity, Claude, Cline, Roo-Code, Cursor, etc.) en bases de código reales, los modelos tienden a **alucinar requerimientos**, inventar contratos de datos, degradar la arquitectura, omitir pruebas o introducir dependencias incompatibles.

El **arnés de IA** es el sistema de contención, contexto y validación que rodea al agente:
- **No es un prompt:** es un conjunto de archivos normativos, contratos de límites de escritura y scripts ejecutables que auditan el código en cada paso.
- **SDD-first (*spec-driven development*):** se prohíbe escribir una sola línea de código en producción sin una especificación previa aprobada (`.spec.md`).
- **Verificación determinista:** el código no se aprueba por "opinión", sino porque supera puertas de validación automatizadas en Python.

---

## 🎯 Los dos propósitos del repositorio

```
┌────────────────────────────────────────────────────────────────────────┐
│                        HARNESS-LAUNCHER                                │
├──────────────────────────────────┬─────────────────────────────────────┤
│      1. PROPÓSITO DIDÁCTICO      │       2. PROPÓSITO LAUNCHER         │
│         (docs/ + context/)       │         (bootstrap-harness)         │
│                                  │                                     │
│  📖 Explica el "por qué":        │  ⚡ Transforma la base canónica:    │
│  - Teoría completa del arnés.    │  - Lee tu PRD o idea de negocio.    │
│  - Cómo gobernar un agente.      │  - Genera tu arnés a medida.        │
│  - 14 capítulos estructurados.   │  - Configura scopes y validadores.  │
│  - Rutas de lectura rápida.      │  - Deja todo verificado y listo.    │
└──────────────────────────────────┴─────────────────────────────────────┘
```

1. **Propósito didáctico:** si estás aprendiendo a estructurar proyectos para agentes de IA, `docs/` contiene la explicación paso a paso de cada pieza (qué es, qué problema evita, qué rompe si falta).
2. **Propósito como lanzador (*launcher*):** si vas a iniciar un nuevo proyecto (o gobernar uno existente), la skill `bootstrap-harness` analiza tu documentación o interactúa contigo y genera un arnés a medida (Flutter, Python, Node/TS, Go, API, CLI o app con interfaz de usuario) sin valores prefijados ni sesgos.

---

## 🧠 Arquitectura conceptual: cómo funciona el arnés

El flujo de control de un agente en el repositorio sigue un orden estricto unidireccional:

```mermaid
flowchart TD
    Agent["🤖 Agente de IA / Dev"] --> Router["AGENTS.md (router operativo JIT)"]
    
    subgraph Normativa["1. Verdad normativa"]
        Router --> Context[".ai-harness/context/ (12 documentos)"]
        Router --> Scopes[".ai-harness/scopes/ (límites de escritura)"]
        Router --> Memory[".ai-harness/memory/ (modos de fallo + ADRs)"]
    end
    
    subgraph SDD["2. Especificación (SDD-first)"]
        Context --> Spec[".ai-harness/sdd/ (CMP-NN / PRC-NN)"]
        Spec --> Story["user_story.md (criterios BDD)"]
        Spec --> Contract["Contratos CT-* e invariantes BR-*"]
    end
    
    subgraph Code["3. Producción y pruebas"]
        Contract --> Prod["Código en lib/ o src/"]
        Contract --> Tests["Pruebas unitarias y de arquitectura"]
    end
    
    subgraph Gates["4. Puertas de calidad (quality gates)"]
        Prod --> Gate1["harness-validator"]
        Prod --> Gate2["preflight"]
        Prod --> Gate3["sync-sdd"]
    end
    
    style Router fill:#2563EB,color:#fff
    style Normativa fill:#1E293B,color:#fff
    style SDD fill:#1E40AF,color:#fff
    style Gates fill:#047857,color:#fff
```

- **`AGENTS.md`:** es el semáforo y router JIT. No duplica reglas de negocio; solo indica el orden de carga obligatorio.
- **`harness.config.yaml`:** es la **única fuente de verdad estructural**. Ningún script asume nombres de carpetas ni prefijos: todo se lee de este archivo.
- **`.ai-harness/context/`:** 12 documentos normativos que definen identidad, arquitectura, estándares de código, pruebas, privacidad y framework SDD.
- **`.ai-harness/scopes/`:** fronteras modulares (`block_*.md`). Cada módulo define qué rutas posee, cuáles le están prohibidas y qué API pública expone.
- **`.ai-harness/sdd/`:** especificaciones canónicas de componentes (`CMP-NN`) y procesos (`PRC-NN`) con trazabilidad completa:  
  `FR-* (Requisito) → CT-* (Contrato) → archivo::símbolo → TC-* (Prueba)`.

---

## 📁 Estructura del proyecto y zonas

El repositorio distingue claramente dos zonas:

```
.
├── AGENTS.md                          # Router de entrada obligatorio para agentes
├── harness.config.yaml                # Fuente de verdad de configuración del arnés
├── requirements.txt                   # Dependencias Python del tooling (Pydantic, PyYAML)
├── MANIFEST.md                        # Lista canónica de qué se traslada y qué no
├── .aiignore                          # Archivos excluidos del contexto del agente
├── .gitignore                         # Archivos excluidos de control de versiones
│
├── .clinerules/                       # Reglas de workspace y workflows invocables
│   ├── rules.md                       # Protocolo de actuación del agente
│   └── workflows/                     # Comandos '/' (list-skills, preflight, etc.)
│
├── .agents/skills/                    # Documentación operativa para el agente
│   └── <skill>/SKILL.md               # Cómo invocar y diagnosticar cada herramienta
│
├── .ai-harness/                       # NÚCLEO OPERATIVO DEL ARNÉS
│   ├── context/                       # 12 documentos normativos maestros
│   ├── design-system/                 # tokens.json + 6 especificaciones de diseño
│   ├── scopes/                        # Límites de escritura (block_*.md)
│   ├── sdd/                           # Taxonomía SDD, plantillas y specs activas
│   │   ├── 1_COMPONENTS/              # Componentes (bootstrap, domain, ui)
│   │   ├── 2_PROCESSES/               # Procesos y flujos orquestados
│   │   └── templates/                 # Plantillas canónicas de CMP y PRC
│   ├── memory/                        # failure_modes.md (antipatrones) + ADRs
│   ├── fixtures/                      # Datos deterministas para pruebas
│   ├── input/                         # Buzón para depositar PRDs o briefs de entrada
│   └── skills/                        # Runners ejecutables de los validadores
│
└── docs/                              # ZONA DIDÁCTICA (Explicación del arnés; no se copia)
    ├── 00-indice.md a 12-bootstrap    # Guía conceptual capítulo a capítulo
    └── cheatsheet.md                  # Resumen rápido de una página
```

---

## 🛠️ Guía de uso: dos formas de utilizarlo

### Modo A: didáctico / estudio y referencia

Si deseas comprender la ingeniería detrás de un arnés de IA gobernado:

1. Abre [`docs/00-indice.md`](file:///docs/00-indice.md) y elige tu itinerario:
   - **Ruta corta (30 min):** `01-que-es-un-harness.md` → `02-agents-md.md` → `cheatsheet.md`.
   - **Ruta operativa (2 horas):** `01` a `05` → `08-skills-y-validadores.md` → `cheatsheet.md`.
   - **Ruta completa (4 horas):** Los 13 capítulos en orden para dominar la arquitectura SDD y gobernanza.
2. Examina las plantillas canónicas en `.ai-harness/sdd/templates/` para entender la anatomía de una especificación sin vacíos ni asunciones.

---

### Modo B: lanzador de un proyecto real (`bootstrap-harness`)

Para inicializar y personalizar este arnés para un nuevo producto o repositorio:

#### 1. Preparación de dependencias
```bash
python -m pip install -r requirements.txt
```
*(Requiere Python 3.11 o superior).*

#### 2. Vía recomendada: asistido por modelo de IA (*agent-driven*)
Si estás en una sesión de chat con Antigravity, Cline o Roo-Code:
1. Deposita tu PRD, brief o notas técnicas en `.ai-harness/input/` (o explícale tu producto en el chat).
2. Pídele al agente:
   > *"Por favor, analiza la documentación en input/ e inicializa el arnés adaptándolo a mi proyecto usando bootstrap-harness."*
3. El agente analizará el dominio real, deducirá los módulos (`scopes`), el stack y las políticas de persistencia/privacidad, redactará un manifiesto estructurado (`manifest.yaml`) y compilará el arnés ejecutando:
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --manifest .ai-harness/input/manifest.yaml
   ```

#### 3. Vía manual: entrevista interactiva en terminal
Si prefieres responder tú mismo por consola paso a paso:
```bash
python .ai-harness/skills/bootstrap-harness/runner.py --interactive
```
*(También puedes simular sin escribir en disco añadiendo `--dry-run`).*

---

## 🚦 Las puertas de calidad (*quality gates*)

Antes de dar cualquier tarea por concluida o realizar un commit en Git, deben pasar limpias tres puertas deterministas:

```bash
# 1. Valida integridad estructural, frontmatter, contexto normativo y scopes
python .ai-harness/skills/harness-validator/runner.py

# 2. Valida linters, arquitectura, inmutabilidad, tokens y dependencias prohibidas
python .ai-harness/skills/preflight/runner.py

# 3. Valida sincronización criptográfica entre specs aprobadas y código real
python .ai-harness/skills/sync-sdd/runner.py
```

| Puerta | Qué audita | Criterio de fallo |
|---|---|---|
| **`harness-validator`** | Integridad del arnés | Documentos ausentes, tags `<PROYECTO>` sin rellenar, specs sin historia BDD o frontmatter inválido. |
| **`preflight`** | Calidad del código fuente | Fallo de pruebas, imports cruzados entre features privadas, uso de `any`/`dynamic`, estilos literales o paquetes vetados. |
| **`sync-sdd`** | Alineación spec ↔ código | Specs aprobadas cuyo target no existe en disco (`MISSING`) o cuyo código ha variado sin actualizar la baseline (`DIVERGED`). |

---

## 🧰 Catálogo de *skills* y flujos de trabajo (*workflows*)

Todas las capacidades del arnés están empaquetadas como ***skills* ejecutables** y pueden invocarse como flujos de trabajo `/comando.md` en entornos compatibles:

| Skill / Flujo de trabajo | Función | Comando directo |
|---|---|---|
| `/bootstrap-harness.md` | Inicializa y adapta el arnés al producto real | `python .ai-harness/skills/bootstrap-harness/runner.py` |
| `/harness-validator.md` | Audita la coherencia y normativa del arnés | `python .ai-harness/skills/harness-validator/runner.py` |
| `/preflight.md` | Control de calidad de código y arquitectura | `python .ai-harness/skills/preflight/runner.py` |
| `/sync-sdd.md` | Comprueba paridad entre spec y disco | `python .ai-harness/skills/sync-sdd/runner.py` |
| `/create-component-sdd.md` | Crea esqueleto canónico de componente (`CMP-NN`) | `python .ai-harness/skills/create-component-sdd/runner.py` |
| `/create-process-sdd.md` | Crea esqueleto canónico de proceso (`PRC-NN`) | `python .ai-harness/skills/create-process-sdd/runner.py` |
| `/launch-app.md` | Arranca la aplicación según su stack | `python .ai-harness/skills/launch-app/runner.py` |
| `/git-publish.md` | Publicación protegida en Git bajo demanda | `python .ai-harness/skills/git-publish/runner.py push` |
| `/list-skills.md` | Inventario de capacidades registradas | Lee `.ai-harness/skills/registry.yaml` |

---

## ⚖️ Reglas de oro no negociables

1. **SDD-first obligatorio:** ninguna línea de código de producción se escribe sin una spec previa en estado `APPROVED`.
2. **Cero invención (*zero-assumption*):** si falta un dato de producto o requerimiento, se registra como pregunta abierta en §15/§16 de la spec y se detiene la implementación.
3. **Una sola fuente de verdad:** cada regla vive en un único archivo; el resto la referencia. Prohibido duplicar normativas.
4. **Configuración estructural primero:** cualquier cambio de capas, scopes o prefijos empieza en `harness.config.yaml`.
5. **Calidad inquebrantable:** prohibido usar `--no-verify` o silenciar tests para forzar un commit. Los fallos se resuelven en su causa raíz.
6. **Privacidad por defecto:** cero telemetría no consentida ni librerías de rastreo comercial.
7. **Publicación bajo demanda:** `git push` solo se ejecuta ante una instrucción explícita del usuario.
