# Create Channel Dialog — Historia de Usuario

## Problema

La pantalla de canales permite crear un canal, pero no existe la superficie para decir de dónde viene el catálogo. Sin ella, el usuario no puede conectar nada.

## Actores

- **Usuario de TV:** navega con D-Pad y puede o no tener teclado.
- **Usuario de escritorio/móvil:** escribe la URL o elige un archivo.
- **Servicio de conexión (`PRC-07`):** recibe la petición.

## Historia

> **Como** usuario,
> **quiero** indicar un archivo o una URL,
> **para** que FLIK cree un canal con ese catálogo.

## Criterios de negocio

- `US-01`: solo hay dos formas de aportar un catálogo, y se ven a la vez.
- `US-02`: si el dispositivo no puede abrir archivos, se dice claramente y no se deja un botón muerto.
- `US-03`: no se puede aceptar sin una fuente válida.
- `US-04`: mientras conecta, el usuario ve progreso y no puede salirse a medias.
- `US-05`: si falla, entiende por qué y puede reintentar sin volver a empezar.
- `US-06`: todo se recorre con el mando.

## Fuera de alcance

- Leer o descargar el catálogo.
- Parsear o validar el contenido.
- Elegir nombre del canal (lo trae la cabecera).
- Explorador de archivos propio.
