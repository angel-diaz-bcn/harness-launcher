# Localización de la Interfaz — Historia de Usuario

## Problema

La interfaz debe estar disponible en español e inglés desde el primer día. Si los textos se escriben directamente en los widgets, añadir un idioma obliga a reescribir todas las pantallas y el layout se rompe con cadenas más largas.

## Actores

- Usuario que usa FLIK en español.
- Usuario que usa FLIK en inglés.
- Equipo de producto que añadirá idiomas en el futuro.

## Necesidad

Como usuario,
quiero que toda la interfaz esté en mi idioma,
para entender las acciones y los estados sin ambigüedad.

## Resultado esperado

- Cadenas de interfaz en ARB para `es` y `en`, con fallback a `es`.
- Selector de idioma en Configuración, aplicado sin reiniciar.
- Fechas, duraciones y números formateados según el idioma activo.
- Cero literales de interfaz en widgets.
- Layout validado con textos largos.

## Criterios de negocio

| ID | Criterio |
|---|---|
| `US-01` | Cambiar el idioma no requiere reiniciar la app. |
| `US-02` | Un idioma sin una clave no rompe la pantalla: se usa el fallback. |
| `US-03` | Los textos largos no provocan desbordes en TV. |
| `US-04` | El contenido del catálogo se muestra en su idioma de origen. |

## Fuera de alcance

- Traducción de títulos y sinopsis del catálogo (v1.1).
- Idiomas distintos de `es` y `en`.
- RTL.
