# FLIK — Layout

Composición, rejilla y comportamiento responsive. Las medidas concretas son tokens de `layout.*` en `tokens.json`.

---

## 1. Breakpoints

| Nombre | Rango | Plataforma típica | Escala tipográfica |
|---|---|---|---|
| `compact` | < 600 dp | Móvil vertical | `compact` |
| `medium` | 600–1023 dp | Móvil horizontal, tablet | `compact` con márgenes ampliados |
| `expanded` | 1024–1599 dp | Escritorio, ventana grande | `tv` con densidades reducidas |
| `tv` | ≥ 1600 dp | Android TV 1080p/4K | `tv` |

Reglas:

- El breakpoint se decide por **ancho lógico**, no por plataforma.
- Nunca se bifurca la lógica de presentación por plataforma; solo cambian densidad y entrada.
- Un cambio de breakpoint no altera el orden de lectura ni el árbol de foco.
- `tv` es el objetivo prioritario: si una decisión de diseño mejora escritorio pero rompe TV, se descarta.

---

## 2. Zona segura y overscan

- Se reserva `layout.overscanRatio` por cada lado en TV para evitar recortes del panel.
- El contenido nunca se pega al borde: `layout.contentPadding` se suma a la zona segura.
- Los elementos de acción (botones, tabs, chips) viven siempre dentro de la zona segura.
- Los fondos a sangre (hero, backdrop de detalle, vídeo) sí pueden invadir el overscan.
- En móvil se respetan notch, barras del sistema y gestos mediante `SafeArea`.

---

## 3. Rejilla

| Contexto | Columnas | Gutter | Margen |
|---|---|---|---|
| TV | `layout.grid.tv.columns` | `layout.grid.tv.gutter` | `layout.contentPadding.tv` |
| Compacto | `layout.grid.compact.columns` | `layout.grid.compact.gutter` | `layout.contentPadding.compact` |

- El ritmo vertical usa la escala `space.*`.
- Entre secciones se aplica `layout.sectionGap`.
- Los carruseles rompen la rejilla a propósito: sangran hasta el borde derecho para insinuar continuidad.
- Prohibidas columnas de ancho fijo fuera de tokens.

---

## 4. Barra superior y navegación

- Altura: `layout.topBarHeight` según breakpoint.
- Contenido: logo, nombre del contexto (espacio o sección), acciones globales (buscar cuando exista, configuración, perfil).
- En Espacios y Perfiles la barra muestra el logo y el perfil activo.
- En Home muestra el nombre del espacio y la acción de volver a Espacios.
- En Detalle y Categoría se sustituye por una barra contextual con «Volver».
- En Reproducción la barra desaparece; el OSD la reemplaza.
- La barra nunca tapa contenido: el scroll aplica el padding correspondiente.
- Sin scrollbar visible en TV.

---

## 5. Plantillas de página

### 5.1 Perfiles

- Contenido centrado, ancho máximo de `layout.settingsMaxWidth`.
- Fila de avatares circulares con foco; nombre debajo.
- Acción «Crear perfil» al final de la fila.
- Sin scroll si caben hasta cinco perfiles; con scroll si hay más.

### 5.2 Canales

- Barra superior con logo, título «Canales» y acción «Crear canal».
- Cabecera centrada `DS-PAGE-HEADER`: eyebrow y titular `display`, sin controles dentro.
- Carrusel en coverflow: la tarjeta central crece a `layout.channelCenterScale` y cada vecina se reduce y atenúa según su distancia con `channelScaleRatio` / `channelOpacityRatio`, con suelo en `channelMinScale` / `channelMinOpacity`.
- El contenedor reserva la altura de la tarjeta central escalada más la escala de foco, para que el anillo y el halo nunca se recorten.
- Bloque de información bajo el carrusel: nombre `title`, descripción `body`, estado en chip.
- Indicador de página solo en `compact` y `medium`.
- Fondo con el degradado ambiente; el resto de la página mantiene el lienzo.
- Foco inicial: la tarjeta del canal abierto más recientemente; si no existe, la primera.
- Sin scroll vertical: la pantalla nunca desplaza contenido.

### 5.3 Home del canal

- Hero a alto `layout.heroHeight`, a sangre, con scrim inferior y contenido alineado a la izquierda.
- El hero ocupa el 100 % del ancho; el texto se limita a la mitad izquierda para no competir con el arte.
- Debajo, secciones verticales con separación `layout.sectionGap`.
- Cada sección: encabezado con barra de acento + carrusel horizontal.
- Primera sección tras el hero: «Continuar viendo» cuando hay progreso; si no, «Destacados».
- Foco inicial: CTA del hero. `Down` baja a la primera tarjeta; `Up` vuelve al hero.

### 5.4 Categoría

- Barra de filtros fija bajo la barra superior: tipo, género, año, calidad y orden.
- Rejilla de pósters con gap `layout.carouselGap`.
- Pósters por fila: 6 en TV, 4 en expanded, 3 en medium, 2 en compacto.
- Contador de resultados alineado a la derecha del título.
- Carga incremental al acercarse al final; sin listas completas en memoria.
- Foco inicial: primer filtro. `Down` entra en la rejilla.

### 5.5 Detalle

- Backdrop a sangre en la parte superior, con scrim y degradado hacia `surface.canvas`.
- Bloque de identidad: eyebrow, título `headline`, fila de metadatos, sinopsis, CTA principal y secundario.
- Tabs de contenido debajo del bloque de identidad.
- Cuerpo en dos columnas en `tv` y `expanded`: principal (reparto, paneles de metadatos, extras, similares) y lateral fija de `layout.detailSidebarWidth` (idiomas y accesibilidad).
- En `compact` las columnas se apilan: idiomas después de la sinopsis.
- Foco inicial: CTA «Ver ahora». El lateral es alcanzable con `Right` desde el cuerpo.
- La columna lateral mantiene su posición al hacer scroll solo si el contenido principal es más alto; si no, comparte scroll.

### 5.6 Pantalla de reproducción

- Vídeo a pantalla completa, sin barras ni safe area visible sobre la imagen.
- OSD inferior con progreso, tiempos, pistas y subtítulos.
- OSD superior con «Volver» y título del contenido.
- Controles centrales de play/pausa y seek al enfocar la zona media.
- Todo el OSD respeta la zona segura de overscan.
- Sin scroll: la pantalla nunca desplaza contenido.

### 5.7 Configuración

- Columna centrada de ancho máximo `layout.settingsMaxWidth`.
- Secciones por categoría con encabezado y filas de ajuste.
- Cada fila: etiqueta, descripción corta y control a la derecha.
- En TV, el control se abre en un panel lateral o diálogo enfocable; nunca en un desplegable dependiente de hover.
- Foco inicial: primera fila. `Back` sale al contexto anterior.

## 6. Carruseles

- Altura determinada por el tipo de tarjeta: póster 2:3 o backdrop 16:9.
- Gap horizontal: `layout.carouselGap`.
- El carrusel muestra al menos 5 tarjetas completas en TV y 3 en compacto.
- Al mover el foco horizontalmente, el contenedor desplaza para mantener la tarjeta enfocada dentro del viewport con margen visible.
- Las flechas de desplazamiento son controles enfocables, no elementos de hover.
- Sin barra de scroll visible en ninguna plataforma dentro del carrusel.
- Al llegar al final, el foco no desaparece: se detiene en la última tarjeta y se mantiene visible.

---

## 7. Scroll y foco

1. El foco nunca queda fuera del viewport: el contenedor hace scroll hasta revelarlo con margen.
2. El scroll por foco usa la misma curva y duración que el movimiento base.
3. Al entrar en una pantalla se restaura el foco previo si el contexto sigue existiendo; si no, se aplica el foco inicial declarado en `05-pages.md`.
4. Ningún contenedor puede atrapar el foco: siempre existe una salida con `Back` o con movimiento en la dirección opuesta.
5. Los overlays (diálogos, paneles, OSD) capturan el foco mientras están abiertos y lo devuelven al cerrarse.
6. Prohibido usar `ListView` anidados en la misma dirección sin control explícito de foco.

---

## 8. Responsive y adaptación

| Elemento | TV | Escritorio | Móvil |
|---|---|---|---|
| Hero | Alto completo, texto a la izquierda | Reducido en altura | 16:9 con texto superpuesto y CTA a ancho completo |
| Carrusel | 5–6 tarjetas | 4–5 tarjetas | 2–3 tarjetas, swipe |
| Detalle | Dos columnas con lateral fija | Dos columnas | Una columna apilada |
| Canales | Carrusel central con vecinas | Carrusel central con vecinas | Una tarjeta con asomo lateral |
| Configuración | Columna centrada | Columna centrada | A ancho completo |
| Barra superior | 72 dp | 64 dp | 56 dp |

Reglas:

- Se adapta la densidad, no la jerarquía.
- Ningún elemento crítico se oculta en compacto; se reordena.
- Los textos largos se truncan con elipsis y se ofrece el texto completo en detalle o tooltip accesible.

---

## 9. Localización y robustez del layout

- Los contenedores se dimensionan por contenido con mínimos de token, no por longitudes fijas de cadena.
- Prohibido `maxLines: 1` en títulos de detalle; se permiten dos líneas con elipsis.
- Etiquetas de botón admiten hasta 24 caracteres antes de truncar; si superan, se acorta el texto en ARB, no en el widget.
- Los formatos de duración y fecha cambian por locale: el ancho del bloque se calcula, no se fija.
- Se valida con seudolocalización (cadenas 40 % más largas) antes de cerrar una pantalla.

---

## 10. Prohibiciones de layout

- Márgenes, gaps, radios o alturas literales fuera de `tokens.json`.
- Scrollbars visibles en TV.
- Contenido interactivo dentro del overscan.
- Columnas que cambian de orden entre breakpoints sin regla declarada.
- Hero con texto centrado o a la derecha.
- Listas completas renderizadas de una vez en Categoría o Home.
- Layouts que dependan de hover para revelar acciones.

