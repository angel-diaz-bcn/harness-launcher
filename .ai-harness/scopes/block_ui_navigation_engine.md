# Scope — UI, Navegación y TV (`block_ui_navigation_engine`)

> Solo define límites. Rutas, foco, entrada y estados se especifican en la SDD.
> Diseño visual fuera de ámbito: `ui-design-system.md`.

## Identidad

| Campo | Valor |
|---|---|
| Bloque | Presentación, navegación y entrada |
| Dominio | Vistas, foco, D-Pad/táctil/teclado y sesión de reproducción |
| Rutas autorizadas | `lib/app/` y `lib/features/tv_experience/` |
| Entradas | D-Pad, teclado, táctil |
| Consumidores | Ninguno; es la capa superior |
| Estado | Límites cerrados |

## Propósito

Gobierna qué pantalla está activa, qué elemento tiene foco, cómo se traduce una entrada y cómo se orquesta la sesión de reproducción. No implementa catálogo, player ni P2P.

## Posee

- Pantallas de canales, home del canal, categoría, detalle, reproducción y configuración.
- Vistas de catálogo, detalle y reproductor.
- Pila de navegación y restauración de estado.
- Normalización de D-Pad, teclado y táctil.
- Árbol de foco y retención de selección.
- Contexto de entrada: modales y campos de texto.
- Apertura y cierre coordinados de P2P + player.
- Decisión de reanudar y guardado de progreso.
- Localización de interfaz con ARB (`es`, `en`) y microcopy.
- Telemetría local de navegación y sesión.

## No posee

- Valores de tokens, colores, tipografías o estilos: los consume desde `lib/app/theme/`.
- Lógica de catálogo, validación o persistencia.
- Decodificación, pistas o estado interno del player.
- Protocolo P2P, búfer o servidor local.
- Persistencia directa en base de datos.
- Descarga de carátulas.
- Traducción del contenido del catálogo; se muestra en su idioma de origen.
- Deep links, PiP o background playback.

## Rutas

```
lib/app/
├── bootstrap/
├── theme/          # implementa tokens, no los define
├── l10n/           # ARB y localizaciones generadas
├── routing/
└── lifecycle/

lib/features/tv_experience/
├── domain/
├── data/
├── presentation/   # shell, screens, widgets, controllers
└── test/
```

Prohibido escribir en `lib/features/p2p_engine/`, `player/`, `catalog/` o `lib/core/`.

## Dependencias

Permitidas: Flutter SDK, `flutter_localizations`, `intl`, `catalog`, `player`, `p2p_engine` (solo ciclo de sesión) y el adaptador de estado confinado a `lib/app/`.

Prohibidas: `media_kit`/MPV, bases de datos, parsers de catálogo, HTTP directo, protocolo P2P, librerías de diseño en la lógica y mutación directa de navegación desde widgets.

## Comprobaciones

- [ ] No importa `media_kit` ni bases de datos.
- [ ] Ningún widget contiene lógica de catálogo, P2P o decodificación.
- [ ] Todo control es alcanzable con D-Pad.
- [ ] El cierre de sesión libera P2P y player.
- [ ] No define colores, tipografías ni tokens.
- [ ] Todo texto de interfaz proviene de ARB; no hay literales en widgets.
- [ ] Las pantallas de canales, home del canal, categoría, detalle, reproducción y configuración existen y están enrutadas.
