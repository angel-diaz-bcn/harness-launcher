# FLIK — Sistema de Diseño

> Autoridad de diseño de FLIK. Define marca, fundamentos, tokens, layout, componentes y su correspondencia con el código.
> Versión **2.0.0** · 2026-10-25.

---

## 1. Qué es y qué no es

Este directorio es el **detalle normativo** del sistema de diseño. `context/ui-design-system.md` es el **índice normativo** que enruta aquí y conserva las reglas transversales.

- `tokens.json` es la **única fuente de valores** (color, tipografía, espacio, radios, movimiento, layout).
- `02-tokens.md` define **semántica y uso**, nunca valores.
- Las specs de UI referencian tokens **por nombre**; nunca copian HEX ni tamaños.
- El código de producción materializa estos tokens en `lib/app/theme/`.

Este sistema **no** define comportamiento de producto, contratos de catálogo, P2P ni reproducción.

---

## 2. Orden de lectura

| # | Archivo | Responde a |
|---|---|---|
| 1 | `01-foundations.md` | Identidad, principios, color, tipografía, forma, iconos, foco, movimiento, accesibilidad y microcopy |
| 2 | `02-tokens.md` | Convención de nombres, rol de cada token y reglas de cambio |
| 3 | `tokens.json` | Valores canónicos machine-readable |
| 4 | `03-layout.md` | Breakpoints, rejilla, overscan, plantillas de página y scroll con foco |
| 5 | `04-components.md` | Inventario `DS-*`: anatomía, estados, tamaños y comportamiento D-Pad |
| 6 | `05-pages.md` | Blueprint funcional de Perfiles, Espacios, Home, Categoría, Detalle, Reproducción y Configuración |
| 7 | `06-code-mapping.md` | Token → clase Dart → widget → spec → test |

---

## 3. Reglas duras

1. **Prohibido** escribir `Color(0x...)`, `Color.fromARGB`, `Colors.*` o tamaños literales fuera de `lib/app/theme/`. `preflight` lo bloquea.
2. Un token que no existe en `tokens.json` **no se usa**: primero se añade al sistema, después al código.
3. Los valores de `tokens.json` y el tema Dart deben coincidir exactamente; un test de paridad lo verifica.
4. El foco es comportamiento, no decoración: todo control tiene estado de foco visible y navegable por D-Pad.
5. Los specs de UI declaran `design_ref: .ai-harness/context/ui-design-system.md` y referencian tokens por nombre.
6. Este árbol no duplica reglas de producto ni contratos de catálogo.
7. Ningún cambio visual entra sin actualizar `tokens.json`, el tema Dart, `06-code-mapping.md` y la versión del sistema.

---

## 4. Versionado

| Versión | Fecha | Cambio |
|---|---|---|
| 2.0.0 | 2026-10-25 | Nace el sistema documental. Paleta derivada del logotipo oficial: azul de marca y azul profundo exactos del SVG. Se ajusta `accent` al azul de marca para cumplir contraste AA con texto blanco; `accentHover` conserva el azul más luminoso del diseño de referencia. Se añaden escala tipográfica, layout, componentes, páginas y mapeo de código. |
| 3.0.0 | 2026-10-27 | **Cambio mayor.** Se sanciona el degradado ambiente (`color.surface.ambientStart` / `ambientEnd`) para páginas de entrada. Se sustituye «Espacio» por «Canal» en el blueprint de páginas y en el mapeo de código. Nuevos componentes `DS-PAGE-HEADER`, `DS-CHANNEL-CARD`, `DS-CHANNEL-CAROUSEL`, `DS-CHANNEL-ART` y `DS-PAGE-INDICATOR`. |
| 3.1.0 | 2026-10-27 | **Cambio menor.** El carrusel de canales pasa a coverflow con profundidad continua: se sustituyen `carouselSideScale` / `carouselSideOpacity` por la escalera `channelCenterScale`, `channelScaleRatio`, `channelOpacityRatio`, `channelMinScale` y `channelMinOpacity`. |

Cambio mayor: altera valores existentes. Cambio menor: añade tokens sin romper. Parche: corrige documentación sin cambiar valores.

---

## 5. Validación

- `python .ai-harness/skills/harness-validator/runner.py` — integridad del arnés.
- `python .ai-harness/skills/preflight/runner.py` — disciplina de tokens en `lib/`.
- `flutter test test/app/theme/` — paridad `tokens.json` ↔ tema Dart y contraste.
- `python .ai-harness/skills/sync-sdd/runner.py` — deriva spec ↔ código.

Un fallo de validación se corrige en la causa raíz; no se silencia ni se desactiva.
