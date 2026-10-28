# Capa `ui` — Presentación y composición visual

Componentes visibles: pantallas, widgets, componentes del sistema de diseño y
todo lo relacionado con foco, entrada y navegación.

## Qué pertenece aquí

- Pantallas y sus componentes.
- Widgets reutilizables y variantes de estado.
- Navegación por foco y orden de tabulación.
- Estados vacíos, de carga y de error.

## Qué no pertenece aquí

- Acceso a red, almacenamiento o servicios.
- Reglas de negocio o validaciones.
- Valores de color o tamaño: se referencian por token.

## Convención

```
ui/
└── CMP-NN-<slug>/            # o una pantalla con components/
    ├── user_story.md
    ├── CMP-NN-<slug>.spec.md
    └── components/
        └── CMP-NN-<slug>/
```

Reglas adicionales:

- Toda spec de esta capa declara `design_ref: .ai-harness/context/ui-design-system.md`.
- La spec de pantalla declara `components: [CMP-NN, ...]` y compone; los
  componentes no dependen de la pantalla.
- El `README.md` de una carpeta de pantalla es el mapa visual y de estados; no
  lleva front matter ni se valida como spec.
