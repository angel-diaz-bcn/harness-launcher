# FLIK — Componentes

Inventario de componentes de interfaz. Cada `DS-*` describe anatomía, estados, tokens por nombre y comportamiento de foco. La implementación vive en `lib/features/tv_experience/presentation/widgets/` y se especifica en `CMP-09`.

---

## 1. Convención

- ID de componente: `DS-<GRUPO>-<NOMBRE>` (por ejemplo `DS-BUTTON-PRIMARY`).
- Un componente implementado sin ficha aquí está fuera de sistema.
- Los componentes no contienen lógica de catálogo, P2P ni reproducción: reciben datos y emiten intenciones.
- Cada ficha declara en qué fase se implementa.
- Los nombres de tokens se refieren a `02-tokens.md`; nunca se copian valores.

---

## 2. Reglas comunes

1. **Foco:** anillo `border.focus`, halo `accent.soft`, escala `focus.scale`, sin reflow.
2. **Estados mínimos:** `default`, `focus`, `pressed`, `disabled`. Añaden `hover` solo en escritorio y `selected`/`loading` cuando aplique.
3. **Objetivo:** altura mínima `target.tvMin` en TV y `target.minTouch` en táctil.
4. **Semántica:** todo componente interactivo expone etiqueta, rol y estado.
5. **Sin hover obligatorio:** ninguna acción se descubre solo al pasar el ratón.
6. **Sin estilos locales:** nada de colores, tamaños o duraciones literales.
7. **Carga:** imágenes con placeholder y `cacheWidth` acotado; nunca se descarga arte a resolución completa para una miniatura.
8. **Texto:** cadenas desde ARB; el componente no concatena ni forma frases.

---

## 3. Inventario

| ID | Componente | Fase | Usado en |
|---|---|---|---|
| `DS-APP-BAR` | Barra superior contextual | F1 | Todas |
| `DS-LOGO` | Logotipo FLIK | F0 | Perfiles, Espacios |
| `DS-BACK` | Acción volver | F1 | Home, Categoría, Detalle |
| `DS-TABS` | Tabs tipo píldora | F4 | Detalle |
| `DS-BUTTON-PRIMARY` | Botón de acción principal | F1 | Todas |
| `DS-BUTTON-SECONDARY` | Botón de acción secundaria | F1 | Hero, Detalle |
| `DS-BUTTON-ICON` | Botón circular de icono | F1 | Barra, OSD |
| `DS-CHIP` | Etiqueta seleccionable o informativa | F1 | Detalle, Categoría |
| `DS-BADGE` | Distintivo compacto | F1 | Tarjetas, Detalle |
| `DS-RATING` | Valoración con estrella | F2 | Tarjetas, Detalle |
| `DS-META-ROW` | Fila de metadatos | F2 | Hero, Detalle |
| `DS-HERO` | Billboard destacado | F2 | Home |
| `DS-SECTION-HEADER` | Encabezado de sección | F2 | Home, Detalle |
| `DS-POSTER-CARD` | Tarjeta 2:3 | F2 | Home, Categoría, Similares |
| `DS-LANDSCAPE-CARD` | Tarjeta 16:9 con play | F4 | Extras |
| `DS-PAGE-HEADER` | Cabecera centrada de página de entrada | F1 | Canales |
| `DS-CHANNEL-CARD` | Tarjeta de canal con arte y estado | F1 | Canales |
| `DS-CHANNEL-CAROUSEL` | Carrusel con selección central | F1 | Canales |
| `DS-CHANNEL-ART` | Arte de canal: asset o placeholder procedural | F1 | Canales |
| `DS-PAGE-INDICATOR` | Puntos de posición del carrusel | F1 | Canales |
| `DS-PROFILE-AVATAR` | Avatar de perfil | F1 | Perfiles, Espacios |
| `DS-PERSON-CARD` | Ficha de reparto | F4 | Detalle |
| `DS-INFO-PANEL` | Panel de metadatos agrupados | F4 | Detalle |
| `DS-LANGUAGE-PANEL` | Panel de idiomas y accesibilidad | F4 | Detalle |
| `DS-MATCH-METER` | Indicador de afinidad local | F4 | Detalle, Tarjetas |
| `DS-CAROUSEL` | Carrusel horizontal con foco | F2 | Home, Detalle |
| `DS-GRID` | Rejilla paginada | F3 | Categoría |
| `DS-PROGRESS` | Barra de progreso | F2 | Hero, Tarjetas, OSD |
| `DS-SKELETON` | Esqueleto de carga | F1 | Todas |
| `DS-EMPTY-STATE` | Estado vacío con acción | F1 | Todas |
| `DS-ERROR-STATE` | Estado de error con reintento | F1 | Todas |
| `DS-DIALOG` | Diálogo modal | F1 | Espacios, Configuración |
| `DS-SETTINGS-ROW` | Fila de ajuste | F6 | Configuración |
| `DS-SELECT` | Selector de opción única | F6 | Configuración |
| `DS-TOGGLE` | Interruptor booleano | F6 | Configuración |
| `DS-SLIDER` | Ajuste numérico | F6 | Configuración |
| `DS-OSD` | Controles de reproducción | F5 | Reproducción |
| `DS-PLAYER-FOCUS-BUTTON` | Botón enfocable del reproductor | F5 | Reproducción |
| `DS-PLAYER-VIDEO-SURFACE` | Superficie de vídeo con fondo de lienzo | F5 | Reproducción |
| `DS-PLAYER-TOP-BAR` | Volver, título, calidad y red | F5 | Reproducción |
| `DS-PLAYER-CENTER` | −10 s, play/pausa, +10 s | F5 | Reproducción |
| `DS-PLAYER-TIMELINE` | Posición, duración y seek | F5 | Reproducción |
| `DS-PLAYER-OPTIONS` | Audio y subtítulos | F5 | Reproducción |
| `DS-PLAYER-STATUS` | Preparación, buffering y avisos | F5 | Reproducción |
| `DS-PLAYER-ERROR` | Error con reintento y salida | F5 | Reproducción |
| `DS-PLAYER-VOLUME` | Altavoz, silencio y barra de volumen | F5 | Reproducción |
| `DS-FOCUS-RING` | Utilidad de foco | F1 | Todos |
| `DS-SCRIM` | Velo de legibilidad | F1 | Hero, Detalle, OSD |

## 4. Fichas

### 4.1 Botones

**`DS-BUTTON-PRIMARY`**
- Anatomía: icono opcional + etiqueta.
- Altura mínima: `target.tvMin` en TV, `target.minTouch` en táctil.
- Fondo `color.accent.base`, texto `color.text.onAccent`, radio `radius.sm`.
- Estados: `focus` (anillo + halo + escala), `pressed` (`color.accent.pressed`), `disabled` (opacidad `opacity.disabled`, sin foco).
- Uso: una sola acción principal por bloque visible (Play, Entrar, Crear).

**`DS-BUTTON-SECONDARY`**
- Fondo `color.surface.elevated`, borde `color.border.subtle`, texto `color.text.primary`.
- Misma geometría y estados que el primario; nunca compite en color.
- Uso: «Ver tráiler», «Cancelar», «Volver a Espacios».

**`DS-BUTTON-ICON`**
- Círculo de `target.tvMin` en TV, fondo `color.surface.elevated`, icono `icon.md`.
- Siempre con etiqueta semántica; prohibido icono sin nombre accesible.
- Uso: acciones de barra, navegación de carrusel, cierre de OSD.

### 4.2 Etiquetas

**`DS-CHIP`**
- Anatomía: etiqueta corta, opcional icono.
- Altura `space.7`, radio `radius.pill`, padding horizontal `space.3`.
- Estados: `default` (borde `border.subtle`), `selected` (fondo `color.brand.deep`, texto `color.text.accent`, borde `border.focus`), `focus` (anillo).
- En Categoría es seleccionable; en Detalle es informativo y no recibe foco.

**`DS-BADGE`**
- No interactivo, sin foco.
- Variantes: `brand` (fondo `color.brand.deep`, texto `color.text.accent`), `solid` (fondo `color.accent.base`, texto `onAccent`), `outline` (borde `border.strong`).
- Uso: «ORIGINAL FLIK», «98 % MATCH», «16+», calidad, «NUEVO».
- Máximo dos badges por tarjeta.

### 4.3 Tarjetas

**`DS-POSTER-CARD`**
- Arte 2:3 con `layout.poster` según breakpoint, radio `radius.md`, borde `border.hairline`.
- Scrim inferior; título `label` a dos líneas; metadatos `caption`.
- Badge opcional arriba a la izquierda; barra de progreso opcional abajo.
- `focus`: escala `focus.scale` + anillo + halo, sin cambiar el layout.
- `pressed`: abre detalle. Sin acciones secundarias ocultas.

**`DS-LANDSCAPE-CARD`**
- Arte 16:9 con `layout.backdropCard`, botón Play superpuesto y duración.
- Título y descripción breve bajo la imagen.
- Usada en extras y tráilers; si el extra no es reproducible, no muestra Play.

**`DS-SPACE-CARD`** sustituida en v3.0.0 por `DS-CHANNEL-CARD`; ver §4.8.

**`DS-PROFILE-AVATAR`**
- Avatar circular `radius.pill`, nombre `label` debajo.
- `focus`: anillo alrededor del círculo, no del nombre.
- Acción «Crear perfil» reutiliza la misma geometría con icono `+`.

**`DS-PERSON-CARD`**
- Retrato circular o cuadrado redondeado, nombre `label`, personaje `caption`, rol en `eyebrow` con `color.text.accent`.
- No interactivo; si se añade biografía en el futuro, pasará a enfocable.

### 4.4 Encabezados, heroes y carruseles

**`DS-PAGE-HEADER`**
- Cabecera de página de entrada: eyebrow en `eyebrow` con `color.text.accent`, titular en `display` centrado.
- Máximo dos líneas de titular; truncar con elipsis, nunca comprimir el estilo.
- Prohibidos controles dentro del bloque: las acciones viven en la barra.
- Permitida solo en páginas de entrada (Canales). Prohibida en Home, Categoría, Detalle, Configuración y Reproducción.
- Sin animación de entrada propia.

**`DS-CHANNEL-CAROUSEL`**
- Fila horizontal de `DS-CHANNEL-CARD` con selección central y `layout.carouselGap`.
- La tarjeta activa va a `layout.channelCenterScale` y recibe además la escala de foco.
- Cada vecina interpola escala y opacidad con `channelScaleRatio` / `channelOpacityRatio`, con suelos `channelMinScale` / `channelMinOpacity`.
- La posición se anima como valor continuo, no como índice: la fila se desliza y las tarjetas crecen o se encogen de forma progresiva.
- El contenedor reserva la altura de la tarjeta central escalada más la escala de foco; el foco nunca se recorta.
- Sin perspectiva 3D, sin desenfoque y sin rotación: solo transformación y opacidad.
- `Left`/`Right` mueven la selección; no hay desplazamiento por scroll.
- Las flechas laterales no son parada de foco: replican la acción del D-Pad para puntero.
- Sin scrollbar en ninguna plataforma.

**`DS-PAGE-INDICATOR`**
- Puntos que reflejan el canal activo sobre el total.
- No interactivo, no enfocable, sin semántica de botón.
- Visible solo en `compact` y `medium`, donde se ve una tarjeta a la vez.

**`DS-HERO`**
- Backdrop a sangre, alto `layout.heroHeight`, scrim inferior.
- Contenido: badge de marca, título `display`, fila de metadatos, sinopsis `body` a tres líneas, CTA primario y secundario.
- El arte nunca queda tapado por el texto: el scrim garantiza contraste.
- Foco inicial de la pantalla en el CTA primario.
- Prohibido carrusel automático dentro del hero.

**`DS-SECTION-HEADER`**
- Barra vertical de acento, título `section`, contador o acción a la derecha.
- La acción derecha es enfocable y se alcanza con `Right` desde la última tarjeta.
- Sin iconos decorativos.

**`DS-CAROUSEL`**
- Fila horizontal con `layout.carouselGap`; desplazamiento por foco.
- Flechas circulares enfocables en los extremos visibles.
- Sin scrollbar. Al llegar al extremo, el foco permanece visible.

### 4.5 Paneles

**`DS-INFO-PANEL`**
- Fondo `surface.base`, radio `radius.lg`, padding `space.6`, borde `border.subtle`.
- Título `eyebrow`, contenido en chips o filas.
- Agrupa géneros, temáticas y reconocimientos.

**`DS-LANGUAGE-PANEL`**
- Filas de audio con idioma, calidad y badge `ORIGINAL` cuando corresponda.
- Chips de subtítulos y accesibilidad.
- Datos derivados de las variantes; si una variante no declara idioma, la fila no se inventa.

**`DS-MATCH-METER`**
- Etiqueta de porcentaje y barra de progreso `radius.pill` sobre `surface.inset`.
- Solo se muestra si existe cálculo local aprobado; nunca datos de servidor.
- Acompañado de texto explicativo breve.

### 4.6 Reproductor

**`DS-OSD`**
- Capa superior plana: cierre, título/subtítulo y acciones de pistas, volumen y detalles.
- Capa inferior: timeline con tiempos laterales y controles −10/play/+10 al pie.
- Gradientes superior e inferior; sin tarjetas ni fondos sólidos.
- Auto-oculta tras 3 s sin entrada; permanece visible en pausa, con un overlay abierto o mientras se navega.
- Todos los controles son enfocables y respetan la zona segura.
- Texto `player.control`; metadatos `player.textSecondary`; progreso `player.progress`; foco `player.focus`.

**Familia del reproductor (`DS-PLAYER-*`)**
- `DS-PLAYER-VIDEO-SURFACE`: solo vídeo y `canvas`; sin controles propios.
- `DS-PLAYER-TOP-BAR`: cierre `X` + título/subtítulo y acciones CC, volumen y detalles; sin calidad ni pares permanentes.
- Zona segura del reproductor: 1.5 % horizontal, 8 % superior y 2.5 % inferior; el vídeo ocupa el resto.
- `DS-PLAYER-ICON-BUTTON`: acción icónica plana o en círculo translúcido, con foco blanco.
- `DS-PLAYER-CENTER`: −10 s, play/pausa y +10 s bajo la timeline; play en círculo translúcido; oculto mientras prepara o hace buffering.
- `DS-PLAYER-TIMELINE`: pista fina, progreso blanco, tiempos a los lados; foco con anillo blanco; `Left`/`Right` ±10 s.
- `DS-PLAYER-OPTIONS`: panel lateral con Audio, «Desactivado» y Subtítulos; check en la selección; foco atrapado.
- `DS-PLAYER-VOLUME`: altavoz en la barra y popover con mute + slider; icono según mute.
- `DS-PLAYER-DETAILS`: popover de calidad, pares, progreso P2P y velocidad; solo lectura.
- `DS-PLAYER-STATUS`: preparación, buffering, pares, porcentaje P2P y aviso de ±10 s; `IgnorePointer`.
- `DS-PLAYER-ERROR`: título, mensaje, Reintentar y Salir; foco inicial en Reintentar.
- `DS-PLAYER-FOCUS-BUTTON`: botón circular o con etiqueta para paneles; `Select`/`Enter`/`Space`.

### 4.7 Estados

**`DS-SKELETON`**: bloques con `surface.base` y opacidad reducida; sin animación infinita en TV.
**`DS-EMPTY-STATE`**: icono `icon.xl`, título `title`, explicación `body` y acción principal enfocada.
**`DS-ERROR-STATE`**: mensaje claro, acción «Reintentar» enfocada y detalle técnico solo en log local.
**`DS-DIALOG`**: captura el foco, devuelve el foco al cerrar, `Back` cancela. Sin diálogos anidados.

### 4.8 Canales

**`DS-CHANNEL-CARD`**
- Arte `DS-CHANNEL-ART` a `layout.poster` según breakpoint, radio `radius.lg`, borde `border.hairline`.
- Scrim inferior `color.surface.overlay` para garantizar contraste del texto.
- Título `title` a dos líneas; pie con contador `channelTitlesCount` y badge de estado.
- Badge de estado: `pending` (`outline`), `ready` (`brand`), `error` (`outline` sobre `status.error`).
- Contador: `0 títulos` cuando no hay fuente; nunca se oculta el número.
- `focus`: escala `focus.scale` + anillo `border.focus` + halo `accent.soft`, sin reflow.
- Activación con `Select`, `Enter`, `Space` o `gameButtonA`; no hay acción «Abrir».
- `Semantics(button: true)` con nombre, contador y estado.

**`DS-CHANNEL-ART`**
- Si el canal declara `coverUri` con `asset:` y el asset existe, se pinta con `BoxFit.cover`.
- En cualquier otro caso, composición procedural en cuatro capas: degradado vertical de superficie, patrón geométrico, foco de luz radial en `brand.deep` y brillo interior superior.
- Cinco variantes de trazo: `rings`, `grid`, `wave`, `prism`, `orbit`, dibujadas con dos pesos (`border.focus` al 30 % y `border.hairline` al 14 %).
- Monograma centrado en `text.primary` sobre el foco de luz.
- Determinista: el patrón lo declara el manifiesto, no se calcula por hash.
- Sin red, sin HEX literal y sin degradados decorativos.

---

## 5. Composición y límites

- Máximo un CTA principal por bloque.
- Máximo dos badges por tarjeta y un `eyebrow` por bloque.
- Un panel no contiene otro panel con borde.
- No se anidan carruseles.
- Cada pantalla declara sus componentes en `05-pages.md`; un componente nuevo exige ficha y actualización del inventario.

