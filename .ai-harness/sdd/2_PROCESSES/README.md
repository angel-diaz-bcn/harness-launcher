# 2_PROCESSES — Flujos dinámicos

Un proceso (`PRC-NN`) describe un recorrido completo que cruza varios
componentes: entrada, transformación, efectos y salida. No es un componente ni
un widget: es la historia de cómo las piezas colaboran.

## Cuándo un proceso merece spec

- Cruza dos o más componentes con contratos entre ellos.
- Tiene estados intermedios observables (cargando, reintentando, cancelado).
- Necesita orden, idempotencia o gestión de errores explícita.
- Su fallo deja el sistema en un estado inconsistente.

## Estructura obligatoria

```
2_PROCESSES/
└── PRC-NN-<slug>/
    ├── user_story.md
    └── PRC-NN-<slug>.spec.md
```

Reglas:

- La carpeta y el archivo comparten el mismo `<ID>-<slug>`.
- La trazabilidad usa `ST-*` (pasos) en lugar de `FR-*`.
- Los pasos son observables; los detalles internos no se especifican.
- Todo proceso documenta su caso de cancelación y su caso de error.

## Cómo crear una spec

```bash
python .ai-harness/skills/create-process-sdd/runner.py PRC-01 \
  --name "Nombre del proceso" \
  --target lib/features/<feature>/application/<orquestador>.dart \
  --dir .ai-harness/sdd/2_PROCESSES/PRC-01-<slug> \
  --block <bloque>
```

Ver `templates/README.md` para el front matter y el checklist de aprobación.
