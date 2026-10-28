# Scope — Reproductor (`block_media_player`)

> Solo define límites. Contratos, matriz de códecs y estados se especifican en la SDD.
> Diseño visual fuera de ámbito: `ui-design-system.md`.

## Identidad

| Campo | Valor |
|---|---|
| Bloque | Capa de reproducción |
| Dominio | Decodificación y control del flujo local |
| Ruta autorizada | `lib/features/player/` |
| Motor | `media_kit` con MPV nativo |
| Consumidor | `lib/features/tv_experience/` |
| Entrada | URL local de `lib/features/p2p_engine/` |
| Estado | Límites cerrados |

## Propósito

Transforma el flujo local en una sesión de reproducción controlable. Termina en la reproducción y su estado; no descarga, no cataloga y no dibuja controles.

## Posee

- Apertura y cierre de la sesión de reproducción.
- Decodificación con preferencia hardware y fallback software.
- Pistas de audio y subtítulos, incluidas externas permitidas.
- Play, pause, seek, posición y duración.
- Estado de reproducción, errores y finalización.
- Superficie de vídeo como recurso opaco.

## No posee

- Sesión P2P, descarga o servidor local.
- Selección de contenido, variante o magnet.
- Catálogo, validación de fuentes o persistencia.
- Navegación, foco, entrada o estado de pantallas.
- Decisión de reanudar o persistir progreso.
- Controles OSD, estilos o tokens visuales.
- Transcodificación, DRM o reproducción en segundo plano.

## Rutas

```
lib/features/player/
├── domain/
├── data/
│   └── media_kit/
├── presentation/
└── test/
```

`media_kit` y MPV solo pueden importarse dentro de `data/media_kit/`.

Prohibido escribir en `lib/features/p2p_engine/`, `catalog/`, `tv_experience/`, `lib/app/` o `lib/core/`.

## Dependencias

Permitidas: `media_kit`, superficie de vídeo, SDK de Flutter y el contrato de flujo del P2P.

Prohibidas: motor BitTorrent, catálogo, bases de datos, navegación, estado de aplicación, analítica o librerías de diseño.

## Comprobaciones

- [ ] No gestiona sesiones P2P.
- [ ] No importa catálogo, navegación ni bases de datos.
- [ ] No expone tipos de `media_kit`/MPV fuera de su feature.
- [ ] No persiste progreso ni decide reanudación.
- [ ] No contiene estilos, OSD ni tokens visuales.
