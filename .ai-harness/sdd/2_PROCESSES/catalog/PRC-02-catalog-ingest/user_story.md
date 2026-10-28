# Catalog Ingest — Historia de Usuario

## Problema

La semilla validada debe llegar a SQLite de forma atómica y solo cuando aporte algo nuevo. Un fallo a mitad de escritura no puede dejar la Home sin catálogo ni con datos parciales.

## Actores

- `CMP-04` (Catalog Seed), que entrega el documento validado.
- `CMP-03` (Catalog Local Store), que ejecuta la transacción.
- `CMP-02` (Catalog Repository), que expone el catálogo a la presentación.

## Historia

> **Como** sistema de arranque,
> **quiero** ingerir la semilla en una transacción y omitirla si ya está al día,
> **para** que la Home tenga catálogo consistente desde el primer frame y sin trabajo repetido.

## Criterios de negocio

- `US-01`: la ingesta se ejecuta al arrancar cuando la base de datos está vacía o la semilla es más reciente.
- `US-02`: si la semilla ya está aplicada, el proceso termina como `skippedUpToDate` sin reescribir datos.
- `US-03`: cualquier fallo hace rollback y conserva el catálogo anterior.
- `US-04`: el resultado informa del estado final y del número de ítems persistidos.
- `US-05`: el proceso no descarga nada ni envía datos fuera del dispositivo.

## Fuera de alcance

- Sincronización periódica con fuentes remotas.
- Resolución de magnets o apertura de sesiones P2P.
- Progreso de visualización y ajustes.
