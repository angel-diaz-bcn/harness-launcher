# Home Row — Historia de Usuario

## Problema

El catálogo necesita presentarse en raíles temáticos que se recorran horizontalmente sin ratón.

## Actores

- Usuario con D-Pad o teclado.
- `CMP-12`, que compone las filas.

## Historia

> **Como** usuario,
> **quiero** recorrer cada fila con las flechas y ver el foco siempre visible,
> **para** explorar el catálogo desde el sofá.

## Criterios de negocio

- `US-01`: cada fila tiene título y tarjetas alineadas horizontalmente.
- `US-02`: `Left`/`Right` mueven el foco entre tarjetas y desplazan la fila.
- `US-03`: `Down` baja a la siguiente fila; `Up` vuelve a la anterior o al hero.
- `US-04`: sin scrollbar ni desplazamiento por hover.
- `US-05`: una fila sin ítems no se pinta.

## Fuera de alcance

- «Ver todo» y navegación a Categoría.
- Paginación dentro de la fila.
