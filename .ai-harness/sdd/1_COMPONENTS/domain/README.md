# Capa `domain` — Dominio, datos y motores

Componentes sin interfaz: entidades, contratos, casos de uso, repositorios,
parsers, servicios y cualquier motor que produzca o transforme datos.

## Qué pertenece aquí

- Entidades, objetos de valor y contratos de repositorio.
- Casos de uso y controladores de aplicación.
- Fuentes de datos, DTOs y mapeadores.
- Motores locales sin dependencia de UI.

## Qué no pertenece aquí

- Widgets, temas o navegación.
- Lógica que solo existe para pintar una pantalla.
- Detalles de una plataforma concreta mezclados con reglas de negocio.

## Convención

```
domain/
└── CMP-NN-<slug>/
    ├── user_story.md
    └── CMP-NN-<slug>.spec.md
```

El `target` de la spec debe apuntar a una ruta real bajo `lib/features/` o
`lib/core/`, nunca a una carpeta inexistente.
