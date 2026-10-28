# Channel Card — Historia de Usuario

## Problema

La pantalla de entrada necesita una tarjeta que represente un canal sin depender de imágenes que aún no existen, mantenga el contraste del texto sobre el arte y sea activable con el mando.

## Actores

- **Usuario de TV:** navega y activa con D-Pad.
- **Usuario de escritorio/móvil:** usa ratón, teclado o toque.
- **Carrusel (`CMP-33`):** orquesta la selección.

## Historia

> **Como** usuario,
> **quiero** una tarjeta de canal atractiva, legible y con foco evidente,
> **para** elegir un canal de un vistazo desde el sofá.

## Criterios de negocio

- `US-01`: cada canal muestra arte propio, nunca un hueco vacío.
- `US-02`: el arte por defecto es distinto por canal y no requiere red.
- `US-03`: el título se lee a tres metros y admite dos líneas.
- `US-04`: el contador de títulos siempre está visible, aunque valga cero.
- `US-05`: el estado de la fuente se comunica con texto, no solo con color.
- `US-06`: el foco combina anillo, halo y escala sin mover el layout.
- `US-07`: pulsar la tarjeta abre el canal; no hay botón adicional.

## Fuera de alcance

- Descargar portadas.
- Progreso de visualización.
- Acciones secundarias (editar, borrar, favoritos).
- Reproducción directa.
