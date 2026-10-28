# Importable Catalog — Historia de Usuario

## Problema

El generador externo emite un array JSON con una cabecera de canal y cientos de películas. FLIK tiene su propio contrato interno, así que sin un parser explícito cada importación inventaría campos y los magnets llegarían sin validar.

## Actores

- **Usuario:** elige un catálogo y espera verlo como un canal.
- **Proceso de conexión (`PRC-07`):** consume el resultado.
- **Almacén (`CMP-03`):** recibe el documento ya normalizado.

## Historia

> **Como** capa de catálogo,
> **quiero** convertir el archivo del generador en datos válidos del dominio,
> **para** que el usuario pueda conectar un catálogo sin que la app interprete cada campo a su manera.

## Criterios de negocio

- `US-01`: el primer elemento describe el canal; sin él no se importa nada.
- `US-02`: el identificador del catálogo es estable entre regeneraciones.
- `US-03`: una película sin identificador externo se descarta sin tumbar el resto.
- `US-04`: los magnet inválidos no llegan nunca a la base de datos.
- `US-05`: la calidad se deduce del nombre del release cuando el formato no la declara.
- `US-06`: los textos se eligen por idioma con fallback, nunca se inventan.
- `US-07`: el usuario recibe un mensaje claro cuando el archivo no sirve.

## Fuera de alcance

- Descargar o leer el archivo.
- Decidir si el canal es nuevo o existente.
- Persistir, comprimir o cifrar.
- Series y YAML.
