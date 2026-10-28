# FLIK — Foundations

Fundamentos visuales y de interacción. Los valores concretos viven en `tokens.json`; aquí se define qué significa cada rol y cómo se usa.

---

## 1. Identidad de marca

- **Logotipo:** FLIK en azul de marca, geométrico, con degradado interno hacia azul profundo. Fuente vectorial: `assets/branding/flik-logo.svg`.
- **Versiones:** positiva sobre fondo oscuro (principal), monocroma blanca (sobre imagen o vídeo) y marca mínima «F» para espacios reducidos.
- **Área de respeto:** altura de la «F» por cada lado. Ningún texto, borde o control puede invadirla.
- **Tamaño mínimo:** 24 dp de alto en interfaz; 32 dp en la barra superior de TV.
- **Prohibido:** deformar, rotar, recolorear fuera de los tokens de marca, añadir sombra, contorno o efectos, o colocar el logo sobre fondos de bajo contraste.
- **En la app** se consume como PNG exportado del SVG (1×, 2×, 3×). El SVG queda como fuente de marca, no como asset de runtime.

---

## 2. Principios visuales

1. **Cine, no productividad.** El contenido manda; la interfaz se retira.
2. **Oscuro con profundidad.** Lienzo casi negro azulado, superficies grafito; nunca negro absoluto.
3. **Acento con propósito.** El azul señala acción, foco y progreso. No decora.
4. **Lectura a 3 metros.** Tamaños y contrastes pensados para sofá antes que para escritorio.
5. **Foco inequívoco.** Borde, escala y halo; nunca solo color.
6. **Movimiento contenido.** Transiciones breves, sin rebote ni espectáculo.

---

## 3. Color

### 3.1 Roles

| Rol | Qué comunica | Dónde se usa |
|---|---|---|
| `brand` | Identidad FLIK | Logo, marca de agua, degradado de marca |
| `accent` | Acción e interacción | CTA principal, foco, tab activo, progreso |
| `surface` | Planos y elevación | Lienzo, tarjetas, paneles, overlays |
| `border` | Separación y estado | Bordes inactivos, separadores, anillo de foco |
| `text` | Jerarquía de lectura | Títulos, metadatos, deshabilitado |
| `status` | Estado del sistema | Éxito, aviso, error, información |

### 3.2 Reglas

- `brand` no se usa como color de interacción; `accent` no se usa como identidad.
- El acento ocupa menos del 10 % de la superficie visible.
- El texto sobre imagen siempre descansa sobre scrim de legibilidad.
- Los estados de error y aviso usan color **y** texto o icono; nunca solo color.
- Prohibidos degradados decorativos. Solo se admiten: el degradado de marca del logo, los scrims de legibilidad y el **degradado ambiente** de §3.3.

### 3.3 Degradado ambiente

Fondo de página que va de `color.surface.ambientStart` (arriba) a `color.surface.ambientEnd` (abajo), siempre en vertical y a sangre.

- **Permitido solo** en páginas de entrada con vacío estructural: Canales. Cualquier otra página nueva requiere aprobación explícita y actualización de este documento.
- **Prohibido** detrás de listas de texto, formularios, vídeo, overlays, modales y en el reproductor.
- El texto de la zona superior mantiene contraste AA sobre el color resultante.
- No sustituye a un scrim: si hay imagen de fondo, se sigue usando `color.surface.overlay`.

## 4. Tipografía

### 4.1 Familias

- **Display:** Barlow Condensed (600/700/800) para títulos, secciones y cifras grandes.
- **Body:** Barlow Semi Condensed (400/500/600) para sinopsis, metadatos y controles.
- **Fallback:** Roboto Condensed, Arial Narrow, sans-serif.
- Licencia OFL; se empaquetan en `assets/fonts/` y se declaran en `pubspec.yaml`.

### 4.2 Escala

Ocho estilos con nombre: `display`, `headline`, `title`, `section`, `body`, `label`, `caption`, `eyebrow`. Cada uno tiene tamaño y altura de línea para TV (`tv`) y para compacto (`compact`).

### 4.3 Reglas

- Máximo **dos pesos por bloque**, más un peso de énfasis dentro del mismo bloque.
- `eyebrow` va en mayúsculas con tracking amplio; nunca para sinopsis.
- Títulos en una o dos líneas; truncar con elipsis, jamás comprimir ni reducir por debajo del mínimo del estilo.
- El cuerpo nunca baja de 16 dp en compacto ni de 20 dp en TV.
- Prohibido texto incrustado en imágenes para información crítica.
- El escalado de texto del sistema se respeta hasta 130 % sin romper el layout.

---

## 5. Espacio, forma y elevación

- Rejilla base de 8 dp; 4 dp reservado para iconos, separadores y ajustes ópticos.
- Escala de espacio cerrada (`space.0`…`space.12`). No se inventan valores intermedios.
- Radios: tarjeta y póster `md`, panel y hoja `lg`, botón `sm`, chip y avatar `pill`.
- Bordes: 1 dp inactivo, 2 dp en foco.
- Elevación: sin sombras decorativas. Solo halo de foco y scrim de legibilidad.
- Separación entre secciones: `sectionGap` del breakpoint activo.

---

## 6. Iconografía

- Set único: **Material Icons** (ya incluido por `uses-material-design`). Prohibido mezclar sets ni importar iconos SVG sueltos.
- Tamaños: `icon.sm` para metadatos, `icon.md` para controles, `icon.lg` para acciones destacadas, `icon.xl` para estados vacíos.
- Trazo consistente y mismo peso óptico por bloque.
- Todo icono accionable lleva etiqueta semántica y estado de foco.
- Un icono solo no comunica una acción crítica: siempre acompañado de texto o tooltip accesible.

---

## 7. Imágenes y scrims

- Póster en 2:3, backdrop en 16:9. Se recortan con `BoxFit.cover`, nunca se deforman.
- Placeholder local obligatorio mientras carga o si falla la URL.
- Scrim inferior en hero y en la base de tarjetas para garantizar contraste del texto.
- Prohibido usar una imagen como fondo de toda la app o detrás de formularios.

---

## 8. Movimiento

- Duraciones: `fast` para microestados, `base` para foco y transiciones, `slow` para entrada de overlays.
- Curvas: salida suave al entrar, entrada suave al salir. Sin rebotes.
- El foco escala y desplaza sin alterar el layout.
- El OSD aparece y desaparece con fundido.
- Se respeta `MediaQuery.disableAnimations`: en ese caso, cambios instantáneos.

---

## 9. Foco

- Composición del foco: anillo de 2 dp en `border.focus`, halo `accent.soft`, escala 108 %.
- El foco nunca se comunica solo por color.
- Foco inicial de cada pantalla: el primer elemento accionable visible.
- El contenedor hace scroll para revelar el foco; nunca queda oculto.
- Al volver de una pantalla se restaura el último elemento enfocado.
- Prohibido depender de hover o de toque para descubrir acciones.

---

## 10. Accesibilidad

- Contraste mínimo AA sobre `surface` y `canvas`.
- Objetivo táctil mínimo `target.minTouch`; en TV `target.tvMin`.
- Etiqueta semántica y estado en todo control.
- Los estados vacíos y de error ofrecen una acción de recuperación enfocable.
- No se transmite información solo por color, forma o posición.
- El texto puede crecer hasta 130 % sin solapamientos ni recortes críticos.

---

## 11. Microcopy y localización

- Idiomas de lanzamiento: `es` y `en`. Fallback: `es`.
- Idioma por defecto del producto: `es`. Hasta que exista el selector de idioma (`CMP-16`), la app arranca en castellano en lugar de heredar el idioma del dispositivo.
- Todo texto de interfaz nace en ARB; **prohibido** literal en el widget.
- Sin concatenación de cadenas: se usan mensajes ICU con placeholders y plurales.
- Fechas, números y duraciones se formatean con `intl` según el locale activo.
- Los textos de datos (títulos, sinopsis) se muestran en el idioma de origen del catálogo; no se traducen en v1.
- Diseñar con margen para textos 40 % más largos que el español y probar con seudolocalización.
- Nombres de acción en verbo + objeto: «Ver ahora», «Añadir fuente», «Borrar caché».

---

## 12. Densidad por plataforma

| Plataforma | Densidad | Regla |
|---|---|---|
| Android TV | Amplia | 5–6 pósters visibles; texto grande; sin scrollbar; foco siempre visible |
| Escritorio | Media | Hover sutil; atajos de teclado; ventana mínima soportada |
| Móvil | Compacta | 2–3 pósters; scroll natural; foco solo con teclado externo |

