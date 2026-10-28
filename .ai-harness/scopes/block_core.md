# Scope — Núcleo compartido (`block_core`)

> Este documento solo define límites de escritura. Los contratos se especifican
> en la SDD; el diseño visual, en `ui-design-system.md`.

## Identidad

| Campo | Valor |
|---|---|
| Bloque | Infraestructura transversal |
| Dominio | Utilidades sin lógica de negocio |
| Rutas autorizadas | `lib/core/` |
| Consumidores | Todas las features y `lib/app/` |
| Estado | Límites cerrados |

## Propósito

Concentra lo que cualquier feature necesita y ninguna debe reimplementar:
cliente HTTP, contratos de almacenamiento, logger, errores tipados, constantes
y utilidades puras.

## Posee

- Cliente HTTP base y política de reintentos.
- Contratos de almacenamiento y caché compartidos.
- Logger, errores tipados y utilidades puras.
- Constantes transversales sin significado de negocio.

## No posee

- Reglas de negocio, entidades de dominio ni casos de uso.
- Widgets, pantallas, temas o tokens visuales.
- Persistencia concreta de ninguna feature.
- Acceso a red con semántica de producto.

## Rutas

```
lib/core/
├── http/
├── storage/
├── logging/
├── errors/
├── constants/
└── utils/
```

Prohibido escribir en `lib/features/*` o `lib/app/`.

## Comprobaciones

- [ ] `lib/core/` no importa `lib/features/`.
- [ ] No contiene lógica de negocio ni nombres de features.
- [ ] Toda caché declara su límite y su política de evicción.
