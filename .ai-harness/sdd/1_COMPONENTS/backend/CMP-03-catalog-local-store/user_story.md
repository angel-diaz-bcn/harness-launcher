# Catalog Local Store — Historia de Usuario

## Problema

El catálogo validado debe persistir en el dispositivo para que la Home arranque sin red y para poder consultar por género, tag, tipo y valoración sin cargar todo el documento en memoria.

## Actores

- Usuario que abre FLIK sin conexión.
- `CMP-02` (Catalog Repository), que traduce consultas de dominio a SQL.
- `PRC-02` (Catalog Ingest), que reemplaza el catálogo de forma atómica.

## Historia

> **Como** producto,
> **quiero** un almacén local indexado y transaccional del catálogo,
> **para** servir la primera pantalla desde caché y conservar el último catálogo válido ante un fallo de ingesta.

## Criterios de negocio

- `US-01`: el esquema almacena ítems, géneros, tags, temporadas, episodios y variantes con sus magnets e info-hash.
- `US-02`: el reemplazo del catálogo es atómico: o se guarda completo o se conserva el anterior.
- `US-03`: las consultas por género, tag, tipo y valoración usan índices y devuelven como máximo 20 filas por petición.
- `US-04`: la base de datos no almacena imágenes ni datos de usuario.
- `US-05`: una versión de esquema desconocida se recrea sin romper el arranque.

## Fuera de alcance

- Progreso de visualización y ajustes de usuario.
- Sincronización remota o multi-dispositivo.
- Búsqueda de texto completo.
- Almacenamiento de carátulas en `BLOB`.
