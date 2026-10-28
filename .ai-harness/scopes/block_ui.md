# Scope — Presentación y composición (`block_ui`)

> Este documento solo define límites de escritura. Los contratos se especifican
> en la SDD; el diseño visual, en `ui-design-system.md`.

## Identidad

| Campo | Valor |
|---|---|
| Bloque | Presentación, navegación y composición |
| Dominio | Interfaz, foco, entrada y arranque |
| Rutas autorizadas | `lib/app/`, `lib/features/<feature>/presentation/`, `assets/` |
| Consumidores | Usuario final |
| Estado | Límites cerrados |

## Propósito

Pinta el estado y emite intenciones. Compone dependencias en el arranque y
materializa los tokens del sistema de diseño. No implementa reglas de negocio.

## Posee

- Widgets, pantallas y componentes visuales.
- Rutas, transiciones y árbol de foco.
- Tema global generado a partir de `design-system/tokens.json`.
- Composición de dependencias y ciclo de vida de la app.
- Textos localizados y microcopy.

## No posee

- Llamadas HTTP, acceso a almacenamiento ni sockets.
- Parseo de datos o validación de negocio.
- Valores de color, tamaño o tipografía literales fuera del tema.
- Lógica duplicada de una feature en otra.

## Rutas

```
lib/app/
├── bootstrap/
├── theme/
├── routing/
└── lifecycle/

lib/features/<feature>/presentation/
├── screens/
├── widgets/
└── controllers/

assets/
├── fonts/
└── images/
```

Prohibido escribir en `lib/features/*/domain/` y `lib/features/*/data/`.

## Comprobaciones

- [ ] Ningún widget contiene URLs, rutas de fichero ni credenciales.
- [ ] Todo control interactivo es alcanzable con teclado o D-Pad.
- [ ] Los colores provienen de tokens, nunca de literales.
