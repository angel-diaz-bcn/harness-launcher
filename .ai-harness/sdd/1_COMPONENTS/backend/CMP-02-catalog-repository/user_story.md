# Catalog Repository — Historia de Usuario

## Problema

La Home necesita leer el catálogo local sin conocer SQLite, sin bloquear el isolate de UI y sin acoplarse a `drift`. Hoy no existe ninguna API que entregue ítems, géneros o tags desde la base de datos.

## Actores

- Usuario de TV, móvil o escritorio que navega la Home.
- `CMP-12` (Home), que consume la API para construir hero y raíles.
- `PRC-02` (Catalog Ingest), que usa el repositorio como punto de escritura tras validar el catálogo.

## Historia

> **Como** desarrollador de la capa de presentación,
> **quiero** consultar el catálogo local mediante un contrato tipado y asíncrono,
> **para** construir la Home sin depender del motor de base de datos ni duplicar consultas.

## Criterios de negocio

- `US-01`: la Home obtiene ítems destacados, por tag, por género, por tipo y mejor valorados con un límite de 20 por fila.
- `US-02`: un ítem se recupera completo, con sus variantes o temporadas, para poder reproducirlo.
- `US-03`: ninguna consulta devuelve ítems sin variantes reproducibles.
- `US-04`: los errores de almacenamiento se comunican con un código tipado, nunca con una excepción cruda de la base de datos.
- `US-05`: la presentación no accede a SQLite, `drift` ni rutas de archivo.

## Fuera de alcance

- Persistencia del progreso de visualización.
- Filtros combinados y paginación de Categoría (`CMP-13`).
- Descarga o transformación de carátulas.
- Sincronización remota de catálogo.
