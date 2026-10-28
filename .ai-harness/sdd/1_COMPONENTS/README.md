# 1_COMPONENTS — Artefactos estáticos

Cada componente del sistema se especifica aquí con un identificador `CMP-NN`
y una carpeta propia. Un componente es una unidad que existe por sí misma:
un motor, un repositorio, un widget, una pantalla o el arranque del proyecto.

## Capas

| Carpeta | Ámbito | Ejemplos |
|---|---|---|
| `bootstrap/` | Proyecto, identidad y arranque | configuración inicial, composición de dependencias |
| `domain/` | Dominio, datos y motores sin interfaz | repositorios, parsers, servicios, controladores |
| `ui/` | Widgets, pantallas, foco y composición visual | tarjetas, listas, pantallas, tema |

## Estructura obligatoria

```
1_COMPONENTS/<capa>/
└── CMP-NN-<slug>/
    ├── user_story.md
    └── CMP-NN-<slug>.spec.md
```

Reglas:

- La carpeta y el archivo comparten el mismo `<ID>-<slug>`.
- Una spec de pantalla puede agrupar componentes en `components/`.
- Prohibido dejar specs sueltas en la raíz de la capa.
- El `README.md` de cada capa describe el ámbito; no es una spec.

## Cómo crear una spec

```bash
python .ai-harness/skills/create-component-sdd/runner.py CMP-01 \
  --name "Nombre del componente" \
  --target lib/features/<feature>/... \
  --dir .ai-harness/sdd/1_COMPONENTS/<capa>/CMP-01-<slug>
```

El runner copia la plantilla, sustituye los marcadores y crea `user_story.md`.
Después: completar el front matter, definir `FR-*`, `CT-*` y `TC-*`, rellenar el
mapa de implementación y pasar el estado a `APPROVED` solo cuando el checklist
esté completo. Ver `templates/README.md`.
