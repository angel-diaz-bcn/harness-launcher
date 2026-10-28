# Arnés de desarrollo asistido por IA

Plantilla de arnés para trabajar con agentes de IA en un repositorio real:
reglas normativas, especificaciones, memoria de errores y validadores
ejecutables. Todo el contenido es genérico: se copia a un proyecto y se adapta.

---

## 1. Qué hay aquí

El repositorio tiene **dos zonas** con propósitos distintos:

| Zona | Contenido | ¿Se copia? |
|---|---|---|
| **Núcleo** | `AGENTS.md`, `harness.config.yaml`, `requirements.txt`, `.aiignore`, `.gitignore`, `.clinerules/`, `.agents/`, `.ai-harness/` | Sí |
| **Documentación** | `docs/`, este `README.md`, `MANIFEST.md` | No |

La documentación explica **qué es cada pieza, por qué existe y qué valida**.
El núcleo es lo que se lleva al proyecto. `MANIFEST.md` detalla la lista exacta.

---

## 2. Arranque rápido

```bash
python -m pip install -r requirements.txt
python .ai-harness/skills/harness-validator/runner.py
python .ai-harness/skills/preflight/runner.py
python .ai-harness/skills/sync-sdd/runner.py
```

Las tres puertas deben devolver código 0. Sin proyecto de producto, `preflight`
devuelve `WARNING` por ausencia de manifiesto: es el comportamiento esperado.

Requisitos: Python 3.11 o superior (los modelos usan `enum.StrEnum`).

---

## 3. Cómo funciona

```
AGENTS.md ── enruta ──▶ .ai-harness/context/*  (reglas normativas)
    │                        │
    │                        ├──▶ scopes/*      (dónde se puede escribir)
    │                        ├──▶ sdd/*         (qué se va a construir)
    │                        └──▶ memory/*      (qué no debe repetirse)
    │
    └── valida con ──▶ skills/*/runner.py ──▶ harness.config.yaml
```

- `harness.config.yaml` declara la estructura: contextos, scopes, prefijos de
  spec, front matter, prefijo de modos de fallo y perfiles de invariantes.
- Ningún validador hardcodea esos valores: todos leen la configuración.
- Los workflows de `.clinerules/workflows/` se invocan como `/nombre.md`.

---

## 4. Primero, segundo y tercero

1. Lee `docs/00-indice.md` para elegir una ruta de lectura.
2. Adapta `harness.config.yaml` a tu proyecto (nombre, stack, scopes).
3. Reescribe `context/project_overview.md`: es el único documento que debe
   describir tu producto y no una plantilla.

---

## 5. Estructura

```
.
├── AGENTS.md                 # Enrutador operativo
├── harness.config.yaml       # Configuración estructural
├── requirements.txt          # Dependencias del tooling
├── MANIFEST.md               # Qué copiar y qué no
├── .aiignore                 # Qué no debe leer el agente
├── .gitignore                # Qué no debe versionarse
├── .clinerules/              # Reglas de workspace y workflows
├── .agents/skills/           # Documentación de uso de cada skill
├── .ai-harness/
│   ├── context/              # 12 documentos normativos
│   ├── design-system/        # tokens.json + 6 documentos de diseño
│   ├── scopes/               # 3 límites de escritura
│   ├── sdd/                  # taxonomía, plantillas y specs
│   ├── memory/               # modos de fallo, ADRs, feedback
│   ├── fixtures/             # datos deterministas
│   └── skills/               # validadores y runners
└── docs/                     # Explicación del arnés (no se copia)
```

---

## 6. Reglas que no se negocian

- Nada de código de producción sin spec aprobada.
- Una regla, un archivo. Prohibido duplicar normas entre documentos.
- Un fallo de validación se corrige en la causa raíz, nunca desactivando el check.
- Sin telemetría de usuario ni dependencias de analítica.
- `git push` solo con instrucción explícita.
