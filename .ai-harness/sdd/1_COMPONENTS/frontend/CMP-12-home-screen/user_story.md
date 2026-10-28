# Home Screen — Historia de Usuario

## Problema

El catálogo ya está persistido y validado, pero no existe ninguna pantalla que lo muestre. El usuario solo puede entrar directamente al reproductor de desarrollo.

## Actores

- Usuario de TV, móvil o escritorio que abre FLIK.
- `CMP-02` (Catalog Repository), que entrega las filas.
- `CMP-15` (Playback Screen), que recibe la petición de reproducción.

## Historia

> **Como** usuario de FLIK,
> **quiero** una Home con un título destacado y raíles de contenido,
> **para** elegir qué ver y empezar a reproducirlo con el mando.

## Criterios de negocio

- `US-01`: la Home muestra un hero y, debajo, raíles horizontales navegables con D-Pad.
- `US-02`: ninguna fila vacía se pinta.
- `US-03`: activar una tarjeta abre el reproductor con la mejor variante disponible.
- `US-04`: una serie reproduce su primer episodio.
- `US-05`: si el catálogo falla, se muestra un estado de error con reintento.
- `US-06`: todo el contenido sale de SQLite; no hay red.

## Fuera de alcance

- Detalle, Categoría, Perfiles y Espacios.
- Continuar viendo y progreso.
- Descarga de carátulas.
- Autoplay de tráilers o del hero.
