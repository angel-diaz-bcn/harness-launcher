# App Top Bar — Historia de Usuario

## Problema

La cabecera de la aplicación necesita permitir navegación de primer nivel entre secciones (Inicio, Series, Películas, Novedades, Mi Flik) y acceso a acciones esenciales (búsqueda, notificaciones, configuración) con soporte completo de foco D-Pad y estética FLIK, sin competir visualmente con el hero.

## Actores

- Usuario que navega con mando a distancia, teclado o toque.
- `CMP-12` (Home Screen) y pantallas principales, que la componen.

## Historia

> **Como** usuario,
> **quiero** una barra superior con la marca FLIK, acceso a las categorías principales y accesos rápidos a búsqueda, notificaciones y configuración,
> **para** cambiar de sección y acceder a herramientas clave de manera rápida y cómoda con el mando.

## Criterios de negocio

- `US-01`: la barra muestra el logotipo FLIK y los destinos principales: Inicio, Series, Películas, Novedades más vistas, Mi Flik.
- `US-02`: ofrece a la derecha los iconos de Búsqueda, Notificaciones y Configuración.
- `US-03`: todos los elementos son navegables horizontalmente con D-Pad / flechas de teclado con anillos y halos de foco conformes al sistema de diseño.
- `US-04`: la navegación respeta la zona segura (`safe area`), altura por token (`layout.topBarHeight`) y no compite con el billboard mediante un scrim degradado.
- `US-05`: todas las etiquetas y textos provienen de ARB sin literales en el widget.

## Fuera de alcance

- Lógica interna del motor de búsqueda (solo emite callback o navega al destino).
- Panel de notificaciones detallado (solo callback o diálogo de aviso).
- Pantalla completa de Configuración (solo callback de activación).

