# 🗄️ backend — Lógica local no visual

> [!NOTE]
> `backend/` agrupa componentes de dominio, datos y motores locales de FLIK. **No es un servidor remoto:** FLIK sigue siendo 100 % client-side.
>
> Aquí viven los contratos y servicios que no dependen de Flutter UI: catálogo, almacenamiento, P2P y reproducción.

## Catálogo

> **Prerrequisito:** [`CMP-00 — App Bootstrap`](../bootstrap/CMP-00-app-bootstrap/CMP-00-app-bootstrap.spec.md) crea el proyecto Flutter y la estructura donde aterriza este bloque.

1. [`CMP-01-catalog-json-contract/`](CMP-01-catalog-json-contract/CMP-01-catalog-json-contract.spec.md) — contrato JSON cerrado.
2. `CMP-02-catalog-parser/` — parser estricto y errores.
3. `CMP-03-catalog-repository/` — caché local y fuentes.
4. `PRC-02-catalog-sync` — sincronización offline-first, en `2_PROCESSES/`.

## P2P y reproducción

1. [`CMP-05-p2p-engine/`](CMP-05-p2p-engine/CMP-05-p2p-engine.spec.md) — magnet → flujo local `127.0.0.1:8888/stream` con `206`.
2. [`CMP-06-media-player/`](CMP-06-media-player/CMP-06-media-player.spec.md) — `media_kit` sobre la URL local.
3. `PRC-01-magnet-playback` — orquestación de la sesión (pendiente).

## Límites

- Solo JSON; YAML queda fuera del MVP.
- Sin UI, P2P, player ni progreso de visualización en el contrato.
- La persistencia y la red pertenecen a las specs 03 y PRC-02.

