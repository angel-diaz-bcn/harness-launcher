# Poster Card — Historia de Usuario

## Problema

Cada título necesita una tarjeta enfocable que muestre su arte y sus metadatos mínimos y que inicie la reproducción.

## Actores

- Usuario que recorre una fila.
- `CMP-31` (Home Row), que la contiene.

## Historia

> **Como** usuario,
> **quiero** una tarjeta clara por título con foco visible,
> **para** identificar el contenido y abrirlo con `Select`.

## Criterios de negocio

- `US-01`: muestra arte 2:3 o placeholder del sistema si no hay carátula.
- `US-02`: muestra título y un metadato (año o temporadas).
- `US-03`: el foco combina anillo, halo y escala, sin reflow.
- `US-04`: `Select` emite la intención de reproducción.
- `US-05`: no descarga imágenes ni conoce el reproductor.

## Fuera de alcance

- Progreso, badges de calidad y sinopsis en la tarjeta.
- Acciones secundarias o menús contextuales.
