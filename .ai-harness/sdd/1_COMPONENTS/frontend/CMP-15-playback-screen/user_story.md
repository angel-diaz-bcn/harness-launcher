# Pantalla de reproducción — Historia de Usuario

## Problema

El usuario quiere ver el contenido P2P con controles completos desde el sofá. Hoy solo existe una pantalla mínima que muestra la superficie y una línea de estado; no hay play/pausa visible, no se puede buscar con precisión ni elegir audio o subtítulos.

## Actores

- Usuario de TV con D-Pad.
- Usuario de móvil o escritorio con teclado y puntero.
- Reproductor local (`CMP-06`) y motor P2P (`CMP-05`), coordinados por `PRC-01`.

## Necesidad

Como usuario,
quiero ver la película a pantalla completa y controlarla sin salir de la reproducción,
para disfrutar del contenido con la misma comodidad que en un servicio de streaming prémium.

## Resultado esperado

- El vídeo empieza solo cuando el flujo está listo.
- Play, pausa, −10 s y +10 s funcionan con el mando y el teclado.
- El OSD aparece al pulsar y se oculta al reproducir.
- Puedo elegir audio y subtítulos sin reiniciar la película.
- Si algo falla, entiendo qué pasó y puedo reintentar o salir.
- Al salir se cierra la sesión y se guarda el progreso disponible.

## Criterios de negocio

| ID | Criterio |
|---|---|
| `US-01` | Nunca se muestra un error técnico crudo al usuario. |
| `US-02` | Todo control es alcanzable con D-Pad. |
| `US-03` | El OSD no tapa el contenido de forma permanente. |
| `US-04` | Cambiar de pista no pierde la posición. |
| `US-05` | Salir libera P2P y reproductor. |

## Fuera de alcance

- Siguiente episodio y cambio de calidad.
- Gestos móviles y velocidad de reproducción.
- «Omitir intro».
