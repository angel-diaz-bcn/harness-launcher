# Catalog Seed — Historia de Usuario

## Problema

En el primer arranque la base de datos está vacía y la Home no tiene nada que mostrar. FLIK necesita un catálogo semilla incluido en el bundle, validado con el mismo contrato que cualquier otra fuente, y sin depender de red.

## Actores

- Usuario que instala FLIK por primera vez.
- `PRC-02` (Catalog Ingest), que orquesta la lectura y la escritura.
- `CMP-01` (Catalog JSON Contract), que valida el documento.

## Historia

> **Como** producto,
> **quiero** cargar un catálogo semilla desde `assets/catalogs/` y validarlo antes de persistirlo,
> **para** que la primera pantalla tenga contenido real sin backend ni conexión.

## Criterios de negocio

- `US-01`: la semilla se lee de un asset declarado y se valida con `CatalogContract.validate`.
- `US-02`: un asset ausente, ilegible o inválido devuelve un fallo tipado y no escribe nada.
- `US-03`: la fuente no realiza peticiones de red.
- `US-04`: el resultado expone el documento validado y el origen para trazabilidad.
- `US-05`: un documento inválido nunca reemplaza al catálogo ya persistido.

## Fuera de alcance

- Descarga de catálogos remotos.
- Edición manual del catálogo desde la interfaz.
- Carátulas y backdrops: el asset semilla se entrega sin imágenes.
