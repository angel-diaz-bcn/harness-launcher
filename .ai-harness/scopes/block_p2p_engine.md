# Scope — Motor P2P (`block_p2p_engine`)

> Solo define límites. Contratos, telemetría y algoritmos se especifican en la SDD.
> Diseño visual fuera de ámbito: `ui-design-system.md`.

## Identidad

| Campo | Valor |
|---|---|
| Bloque | Motor P2P local |
| Dominio | Obtención de contenido y exposición del flujo local |
| Ruta autorizada | `lib/features/p2p_engine/` |
| Consumidor | `lib/features/player/` mediante URL local |
| Estado | Límites cerrados |

## Propósito

Convierte un magnet en un flujo local reproducible y seekable. Termina cuando entrega el flujo y su estado; no reproduce, no pinta y no cataloga.

## Posee

- Ciclo de vida de la sesión P2P.
- Descubrimiento de peers, trackers y DHT.
- Descarga secuencial con prioridad de cabeceras.
- Búfer acotado con evicción de piezas vistas.
- Servidor HTTP local en `127.0.0.1:8888/stream` con `206`.
- Estado operativo: velocidad, peers, progreso y disponibilidad.
- Liberación de sockets, puerto y memoria nativa.

## No posee

- Decodificación, reproducción, seeking o pistas.
- Catálogo, metadatos, carátulas o progreso de usuario.
- Navegación, foco, entrada o UI.
- Transcodificación, DRM o descarga permanente.
- Exposición del endpoint fuera de loopback.
- Proceso daemon separado.

## Rutas

Autorizado:

```
lib/features/p2p_engine/
├── domain/
├── data/
├── application/
└── test/
```

Código nativo de plataforma, solo dentro de la carpeta del motor:

```
android/app/src/main/*/p2p_engine/
windows/*/p2p_engine/
macos/*/p2p_engine/
linux/*/p2p_engine/
```

Prohibido escribir en `lib/features/player/`, `catalog/`, `tv_experience/`, `lib/app/` o `lib/core/`.

## Dependencias

Permitidas: runtime BitTorrent embebido, utilidades de red local, almacenamiento temporal y criptografía.

Prohibidas: `media_kit`, MPV, catálogo, bases de datos de catálogo, UI, analítica o servicios remotos.

## Comprobaciones

- [ ] No importa `media_kit`, `catalog`, `tv_experience` ni `flutter/widgets`.
- [ ] No escribe fuera de su feature.
- [ ] El endpoint es loopback y responde `206`.
- [ ] El cierre libera puerto, sockets y temporales.
