# Channels Screen — Historia de Usuario

## Problema

La aplicación no tenía pantalla de entrada. `CMP-12` abría directamente la Home de un catálogo implícito, sin forma de elegir entre varias bibliotecas ni de entender qué se está abriendo.

## Actores

- **Usuario de TV:** navega con D-Pad y confirma con Select.
- **Usuario de escritorio/móvil:** usa flechas, ratón o toque.
- **Composición de la app (`lib/app/`):** decide la navegación.

## Historia

> **Como** usuario,
> **quiero** una pantalla de entrada que me muestre mis canales,
> **para** elegir con qué biblioteca quiero entrar.

## Criterios de negocio

- `US-01`: es la primera pantalla al abrir la aplicación.
- `US-02`: muestra los cinco canales por defecto sin conexión.
- `US-03`: la selección se mueve en horizontal y actualiza la información del canal.
- `US-04`: activar la tarjeta abre el Home del canal.
- `US-05`: un canal sin contenido muestra su estado y la acción de conectar una lista.
- `US-06`: la pantalla se recorre completa con D-Pad y `Back` cierra la aplicación.
- `US-07`: el contador refleja cero títulos cuando no hay fuente conectada.
- `US-08`: la creación de canales está visible pero deshabilitada, con explicación.

## Fuera de alcance

- Crear canales y conectar listas (`PRC-07`).
- Buscar, favoritos y perfiles.
- Editar o borrar canales.
- Reproducción directa desde esta pantalla.
