# FLIK — Tokens

Contrato semántico de los tokens. **Los valores están exclusivamente en `tokens.json`.** Este documento no los repite.

---

## 1. Convención de nombres

```
<grupo>.<rol>[.<variante>]
```

| Grupo | Ejemplo de nombre | Naturaleza |
|---|---|---|
| `color.brand` | `color.brand.primary` | Identidad |
| `color.accent` | `color.accent.base` | Interacción |
| `color.surface` | `color.surface.elevated` | Planos |
| `color.border` | `color.border.subtle` | Separación |
| `color.text` | `color.text.secondary` | Lectura |
| `color.status` | `color.status.error` | Estado |
| `typography.styles` | `typography.styles.title` | Tipografía |
| `space` | `space.6` | Ritmo |
| `radius` | `radius.md` | Forma |
| `motion` | `motion.base` | Tiempo |
| `focus` | `focus.scale` | Interacción |
| `layout` | `layout.heroHeight` | Composición |
| `icon` | `icon.md` | Iconografía |
| `target` | `target.tvMin` | Accesibilidad |

Reglas:

- Nombres en inglés, semánticos, sin referencia al valor (`accent`, no `blue600`).
- `color.accent.*` y `color.brand.*` no son intercambiables.
- Los tokens de layout dependen del breakpoint (`tv` o `compact`).
- Prohibido crear alias ad hoc en widgets; los alias viven en el tema Dart.

---

## 2. Catálogo por grupo

### 2.1 Color

| Token | Rol | Restricciones |
|---|---|---|
| `color.brand.primary` | Azul de marca del logotipo | Solo identidad; no como color de acción |
| `color.brand.deep` | Azul profundo del degradado del logotipo | Fondos de badge y estado pressed |
| `color.brand.tint` | Azul claro legible sobre oscuro | Eyebrows, texto de acento, roles |
| `color.brand.gradientStart` / `gradientEnd` | Degradado de marca | Solo marca y logo |
| `color.accent.base` | Acción principal | CTA, foco, progreso, tab activo |
| `color.accent.hover` | Hover y énfasis | Escritorio; en TV no existe hover |
| `color.accent.pressed` | Presión | Coincide con el profundo de marca |
| `color.accent.soft` | Halo y selección suave | Foco y fondo de selección |
| `color.accent.onAccent` | Texto sobre azul | Contraste AA sobre `accent.base` |
| `color.surface.canvas` | Fondo base | Toda pantalla |
| `color.surface.base` | Tarjetas y paneles | Contenedores de contenido |
| `color.surface.elevated` | Overlays y hover | Capas por encima de `surface.base` |
| `color.surface.inset` | Inputs y barras | Áreas hundidas |
| `color.surface.ambientStart` | Inicio del degradado ambiente | Solo fondo de páginas de entrada (§3.3 de `01-foundations`) |
| `color.surface.ambientEnd` | Fin del degradado ambiente | Coincide con el lienzo |
| `color.surface.overlay` | Velo de legibilidad | Sobre imagen o vídeo |
| `color.surface.overlayStrong` | Velo de OSD | Controles sobre vídeo |
| `color.border.subtle` | Borde inactivo | 1 dp |
| `color.border.strong` | Separador de sección | 1 dp |
| `color.border.focus` | Anillo de foco | 2 dp |
| `color.text.primary` | Títulos y datos | Sobre superficies oscuras |
| `color.text.secondary` | Metadatos y sinopsis | Nunca para acciones |
| `color.text.disabled` | No disponible | Acompañado de estado semántico |
| `color.text.onAccent` | Texto sobre azul | Botones llenos |
| `color.text.accent` | Texto azul legible | Chips, roles, enlaces |
| `color.status.success` | Confirmación | Con icono o texto |
| `color.status.warning` | Aviso y buffering | Con icono o texto |
| `color.status.error` | Fallo | Con icono o texto |
| `color.status.info` | Información neutra | Con icono o texto |

### 2.2 Tipografía

| Token | Uso |
|---|---|
| `typography.styles.display` | Título del hero |
| `typography.styles.headline` | Título de detalle |
| `typography.styles.title` | Título de pantalla o diálogo |
| `typography.styles.section` | Encabezado de sección y carrusel |
| `typography.styles.body` | Sinopsis y descripciones |
| `typography.styles.label` | Botones, chips y metadatos |
| `typography.styles.caption` | Año, duración, calidad |
| `typography.styles.eyebrow` | Etiquetas en mayúsculas con tracking |

Cada estilo declara familia, tamaño por breakpoint, altura de línea, peso y tracking.

### 2.3 Espacio, forma y movimiento

| Token | Uso |
|---|---|
| `space.0`…`space.12` | Márgenes, padding y gaps |
| `radius.none`…`radius.pill` | Esquinas |
| `border.hairline` / `border.focus` | Grosor de borde |
| `elevation.focusHaloBlur` | Difuminado del halo de foco |
| `opacity.disabled` / `hover` / `pressed` / `scrim` | Capas de estado |
| `focus.scale` / `ringWidth` / `ringOffset` | Composición del foco |
| `motion.fast` / `base` / `slow` | Duración de transición |
| `motion.easingIn` / `easingOut` | Curvas |

### 2.4 Layout, icono y objetivo

| Token | Uso |
|---|---|
| `layout.breakpoints.*` | Cortes de breakpoint |
| `layout.overscanRatio` | Zona segura de TV |
| `layout.contentPadding.*` | Margen de contenido |
| `layout.grid.*` | Columnas y gutter |
| `layout.topBarHeight.*` | Altura de barra superior |
| `layout.heroHeight.*` | Altura del hero |
| `layout.poster.*` / `backdropCard.*` | Tamaño de tarjetas |
| `layout.detailSidebarWidth` | Columna lateral del detalle |
| `layout.settingsMaxWidth` | Ancho máximo de ajustes |
| `layout.carouselGap` / `sectionGap` | Separación |
| `layout.channelCenterScale` | Escala de la tarjeta central del carrusel de canales |
| `layout.channelScaleRatio` / `channelOpacityRatio` | Factor de reducción por distancia al centro |
| `layout.channelMinScale` / `channelMinOpacity` | Suelo de escala y opacidad para tarjetas lejanas |
| `icon.sm`…`icon.xl` | Tamaño de icono |
| `target.minTouch` / `tvMin` | Objetivo mínimo |

---

## 3. Token ↔ tema Dart

| Token JSON | API Dart | Archivo |
|---|---|---|
| `color.*` | `FlikColors.*` | `lib/app/theme/flik_colors.dart` |
| `typography.*` | `FlikTypography.*` | `lib/app/theme/flik_typography.dart` |
| `space.*` | `FlikSpacing.*` | `lib/app/theme/flik_spacing.dart` |
| `radius.*` / `border.*` | `FlikRadii.*` | `lib/app/theme/flik_spacing.dart` |
| `motion.*` | `FlikMotion.*` | `lib/app/theme/flik_motion.dart` |
| `focus.*` | `FlikFocus.*` | `lib/app/theme/flik_motion.dart` |
| `layout.*` | `FlikLayout.of(context)` | `lib/app/theme/flik_layout.dart` |
| `icon.*` | `FlikIconSizes.*` | `lib/app/theme/flik_icons.dart` |
| `color.status.*` / `color.text.*` | `FlikSemanticColors` (`ThemeExtension`) | `lib/app/theme/flik_theme.dart` |

El detalle completo está en `06-code-mapping.md`.

---

## 4. Reglas de cambio

1. Un token nuevo se añade primero a `tokens.json`, después a `02-tokens.md` y al tema Dart, en el mismo cambio.
2. Renombrar un token exige actualizar todos los consumidores; no se dejan alias permanentes.
3. Cambiar un valor es cambio **mayor** de versión del sistema y requiere revisar contraste y capturas de referencia.
4. Eliminar un token exige que ningún widget ni spec lo referencie.
5. `preflight` y el test de paridad fallan si `tokens.json` y el tema Dart divergen.
6. Los tokens se referencian por nombre en specs y revisiones; nunca por valor.

---

## 5. Prohibiciones

- HEX, RGB o `Colors.*` en widgets, specs o documentación de componentes.
- Tamaños literales de tipografía, radio, gap o duración fuera de los tokens.
- Tokens «temporales» o alias locales en un widget.
- Tokens con nombre de valor (`blue600`) en lugar de rol (`accent`).
- Sombras decorativas o degradados que no sean de marca o scrim.

