# Catalog Connect — Historia de Usuario

## Problema

El usuario tiene un catálogo en un archivo o en una URL y quiere verlo dentro de FLIK como un canal más, con sus películas disponibles sin volver a elegir el archivo.

## Actores

- **Usuario:** elige el origen y confirma.
- **Diálogo «Nuevo canal» (`CMP-37`):** emite la petición.
- **Catálogo (`CMP-03`, `CMP-36`):** valida y persiste.
- **Pantalla de canales (`CMP-33`):** muestra el resultado.

## Historia

> **Como** usuario,
> **quiero** conectar un catálogo indicando un archivo o una URL,
> **para** tener un canal con su contenido listo para ver.

## Criterios de negocio

- `US-01`: al aceptar, el canal aparece con el nombre que declara el catálogo.
- `US-02`: el contador refleja los títulos realmente escritos.
- `US-03`: conectar el mismo catálogo dos veces no crea dos canales.
- `US-04`: dos catálogos con el mismo nombre conviven con sufijo numérico.
- `US-05`: un archivo inválido no crea ni modifica nada.
- `US-06`: un fallo a mitad de proceso no destruye el catálogo anterior.

## Fuera de alcance

- Comparar catálogos para aplicar solo diferencias.
- Sincronización diaria automática.
- Carátulas remotas.
- Cifrado o compresión del archivo.
