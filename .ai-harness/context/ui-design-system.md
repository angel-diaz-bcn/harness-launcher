# FLIK — Sistema de Diseño y Experiencia Visual

> Índice normativo. El detalle vive en `.ai-harness/design-system/`; los **valores** viven exclusivamente en `.ai-harness/design-system/tokens.json`.

Versión del sistema: **2.0.0** (2026-10-25).

---

## 1. Autoridad

- Este documento define **qué es obligatorio** en la interfaz de FLIK y enruta al detalle.
- `design-system/01-foundations.md` define marca, color, tipografía, forma, iconos, movimiento, foco y accesibilidad.
- `design-system/02-tokens.md` define la semántica y el uso de cada token.
- `design-system/tokens.json` contiene los valores canónicos; ningún otro archivo los repite.
- `design-system/03-layout.md` define rejilla, breakpoints, overscan y plantillas de página.
- `design-system/04-components.md` define el inventario `DS-*`, sus estados y su comportamiento D-Pad.
- `design-system/05-pages.md` define el blueprint funcional de las siete pantallas.
- `design-system/06-code-mapping.md` define la correspondencia con `lib/app/theme/` y los widgets.

Toda spec con `layer: frontend` declara `design_ref: .ai-harness/context/ui-design-system.md`.

---

## 2. Filosofía

FLIK debe sentirse como una experiencia cinematográfica prémium, no como una aplicación de productividad. El diseño está optimizado para pantallas OLED de gran formato en salas oscuras, lectura a tres metros y navegación con mando. El contenido es el protagonista; la interfaz se retira.

Principios:

1. **Oscuro con profundidad**, nunca negro absoluto.
2. **Contraste controlado** entre planos; las superficies separan sin competir con el contenido.
3. **Acento con propósito**: el azul señala acción, foco y progreso; nunca decora.
4. **Movimiento contenido**: transiciones breves, sin rebotes ni animaciones decorativas.
5. **Legibilidad primero**: tamaños generosos, jerarquía clara y metadatos sin ruido.
6. **Foco universal**: todo control es alcanzable y activable con D-Pad o teclado.

---

## 3. Reglas duras

1. **Sin valores fuera de tokens.** Prohibido escribir HEX, RGB, `Colors.*`, tamaños, radios, gaps o duraciones literales en widgets. `preflight` solo admite construcción de color dentro de `lib/app/theme/`.
2. **Sin tokens inventados.** Un token que no existe en `tokens.json` no se usa: primero se añade al sistema y a su documentación.
3. **Sin estilos locales.** Los widgets consumen el tema y las extensiones semánticas; no crean variantes ad hoc.
4. **Foco visible siempre.** Anillo, halo y escala; nunca solo color. Ningún control depende de hover o de toque para descubrirse.
5. **Contraste AA** en texto y controles sobre las superficies del sistema.
6. **Escalado de texto** hasta el máximo declarado sin romper el layout; se respeta `disableAnimations`.
7. **Una sola familia tipográfica de display y una de cuerpo**, con los pesos declarados en `01-foundations.md`.
8. **Localización obligatoria.** Todo texto de interfaz nace en ARB (`CMP-17`); prohibido el literal en el widget.
9. **Contenido en su idioma de origen** en v1; la traducción de metadatos del catálogo queda fuera de alcance.
10. **Sin sombras decorativas ni degradados** que no sean el degradado de marca o un scrim de legibilidad.

---

## 4. Mapa de enrutamiento

| Si necesitas… | Consulta |
|---|---|
| Identidad, color, tipografía, foco, accesibilidad | `design-system/01-foundations.md` |
| Nombre y uso de un token | `design-system/02-tokens.md` |
| Valor exacto | `design-system/tokens.json` |
| Rejilla, breakpoints, plantilla de pantalla | `design-system/03-layout.md` |
| Anatomía y estados de un componente | `design-system/04-components.md` |
| Secciones, datos y estados de una página | `design-system/05-pages.md` |
| Clase Dart, widget, ruta o test | `design-system/06-code-mapping.md` |

---

## 5. Prohibiciones visuales

- Fondo negro puro; se usa el token de lienzo.
- Acentos neón, gradientes decorativos o sombras difusas.
- Más de dos pesos tipográficos por bloque, más un énfasis.
- Tarjetas sin foco visible en TV.
- Controles accesibles solo por hover o toque.
- Scrollbars visibles en TV.
- Texto incrustado en imágenes para información crítica.
- Colores, tamaños o estilos hardcodeados fuera del tema.
- Animaciones de más de 300 ms o con rebote.
- Cualquier dato de telemetría o analítica visual.

---

## 6. Validación

- `python .ai-harness/skills/preflight/runner.py` bloquea colores fuera de `lib/app/theme/`.
- `flutter test test/app/theme/` verifica paridad `tokens.json` ↔ Dart, contraste, layout y foco.
- `flutter test test/app/l10n/` verifica paridad ARB ↔ Dart, plurales y controlador de idioma.
- `flutter test` y `flutter analyze` deben pasar antes de cerrar cualquier cambio visual.
- `python .ai-harness/skills/harness-validator/runner.py` valida la integridad del arnés.
- Un fallo de validación se corrige en la causa raíz; no se desactiva.
