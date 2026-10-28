# Capa `bootstrap` — Proyecto y arranque

Componentes que existen antes que cualquier feature: identidad del proyecto,
configuración, composición de dependencias y punto de entrada.

## Qué pertenece aquí

- `CMP-00`: bootstrap, identidad, estructura inicial y arranque.
- Configuración transversal que no es lógica de negocio (tema, router raíz,
  observadores de ciclo de vida).
- Contratos de composición de dependencias.

## Qué no pertenece aquí

- Reglas de negocio de una feature concreta.
- Widgets de pantalla que pertenecen a una feature de `ui/`.
- Infraestructura reutilizable: eso vive en `lib/core/` y se especifica en
  `domain/`.

## Convención

```
bootstrap/
└── CMP-00-<slug>/
    ├── user_story.md
    └── CMP-00-<slug>.spec.md
```

`CMP-00` es una excepción de infraestructura: no compite con la numeración de
los componentes funcionales.
