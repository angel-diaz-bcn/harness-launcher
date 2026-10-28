# Decisiones de arquitectura (ADR)

Cada decisión estructural relevante se registra aquí como un documento corto,
inmutable y numerado.

## Convención

```
decisions/
├── README.md
├── ADR-0001-<slug>.md
└── ADR-0002-<slug>.md
```

## Reglas

- Un ADR describe **contexto, decisión, alternativas y consecuencias**.
- Un ADR no se reescribe: si la decisión cambia, se crea otro ADR que la
  reemplaza y se enlazan entre sí.
- Un ADR no sustituye a una spec: la spec describe comportamiento; el ADR
  describe por qué se eligió una tecnología o una estructura.
- Numeración correlativa desde `ADR-0001`. La plantilla es
  `ADR-0000-plantilla.md` y no se numera como decisión real.

## Cuándo crear un ADR

- Se elige una dependencia con impacto en licencia, tamaño o rendimiento.
- Se fija una frontera entre módulos.
- Se decide una estrategia de persistencia, sincronización o caché.
- Se acepta una limitación conocida de la plataforma.
