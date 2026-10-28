# CMP-29 — App Top Bar
 
---
spec_id: CMP-29
spec_type: CMP
layer: frontend
name: App Top Bar
target: lib/features/tv_experience/presentation/widgets/home/home_top_bar.dart
block: tv_experience
status: APPROVED
version: 2.0
owner: UI Team
last_reviewed: 2026-10-26
approved_at: 2026-10-26
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: []
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-07, CMP-17]
consumed_by: [CMP-12]
---

`CMP-29` · `v2.0` · `tv_experience` · `Flutter` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `tv_experience` | `lib/features/tv_experience/presentation/widgets/home/home_top_bar.dart` |

> [!IMPORTANT]
> Barra de navegación superior interactiva con estética FLIK estilo Netflix. Dispone el logotipo y destinos primarios (Inicio, Series, Películas, Novedades más vistas, Mi Flik) a la izquierda, y acciones de cabecera (Búsqueda, Notificaciones, Configuración) a la derecha, con navegación universal D-Pad.

> [!TIP]
> **Ruta de lectura:** §4 requisitos → §8 contratos → §10 trazabilidad → §11 pruebas.

### 🗺️ Mapa de lectura

| Bloque | Qué encontrarás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y estados |
| §7–§9 | Datos, contratos y dependencias |
| §10–§12 | Trazabilidad, pruebas y BDD |
| §13–§15 | Cierre, decisiones y preguntas |

---

## 0. Protocolo de lectura y no invención

1. Leer `CMP-12`, `design-system/03-layout.md` §4, `04-components.md` `DS-APP-BAR`, `DS-BUTTON-ICON`, `DS-CHIP` y `02-tokens.md`.
2. Implementar los `FR-*` y `CT-*` acordados sin omitir tokens ni utilizar HEX hardcodeados.
3. Todo texto proviene de ARB (`CMP-17`); sin cadenas de texto en crudo.

---

## 1. Contexto y objetivo

### 1.1 Problema

La cabecera actual de FLIK era meramente informativa y estática. Para proporcionar una experiencia de streaming de primer nivel tipo TV/Living Room (estilo Netflix), el usuario necesita conmutar entre los grandes bloques del catálogo (Inicio, Series, Películas, Novedades y Mi Flik) y acceder de forma inmediata a la búsqueda y configuración con el mando a distancia.

### 1.2 Objetivo medible

- Renderizar barra superior con altura tokenizada `layout.topBarHeight` y padding de seguridad.
- Elementos a la izquierda: Logo FLIK interactivo + 5 pestañas de navegación (Inicio, Series, Películas, Novedades más vistas, Mi Flik).
- Elementos a la derecha: 3 botones de acción con icono (Buscar, Notificaciones, Ajustes).
- Navegación D-Pad bidireccional horizontal con anillo de foco `border.focus` (`#2F6BFF`) y halo `accent.soft`.
- Respeto total de tokens de color y superficie (fondo scrim degradado a canvas sin tapar el hero).

### 1.3 No objetivos

- Implementación del modal de notificaciones o de la pantalla de búsqueda dentro de este widget (se exponen callbacks).
- Persistencia remota o backend de ajustes (FLIK es 100% cliente local).

---

## 2. Alcance y límites

**Incluye:**
- Logotipo FLIK.
- Enlaces de navegación con selección activa y soporte D-Pad.
- Botones de acción circular para Búsqueda, Notificaciones y Configuración.
- Scrim degradado vertical superior.
- Callbacks de selección y activación tipados.

**Excluye:**
- Páginas de destino de cada sección (responsabilidad del enrutador o controlador de pantalla).
- Animaciones complejas o rebotes que excedan los 250ms de `motion.base`.

---

## 3. Actores e historia de usuario

> **Como** usuario con mando de TV o teclado,
> **quiero** navegar por los apartados clave (Inicio, Series, Películas, Novedades, Mi Flik) y lanzar búsqueda o ajustes desde la cabecera,
> **para** explorar el catálogo cómodamente con control de foco claro e intuitivo.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Muestra el logotipo de FLIK en el extremo izquierdo. | Must | `AC-01`: Logo visible y con padding proporcional. | `BR-01` |
| `FR-02` | Muestra la lista de navegación: Inicio, Series, Películas, Novedades más vistas, Mi Flik. | Must | `AC-02`: Las 5 secciones se muestran en orden con textos de ARB. | `BR-02` |
| `FR-03` | Resalta visualmente la pestaña seleccionada según `HomeNavDestination`. | Must | `AC-03`: Elemento activo con `color.text.primary` y fondo/píldora distintiva. | `BR-03` |
| `FR-04` | Proporciona 3 botones de icono a la derecha: Búsqueda, Notificaciones y Configuración. | Must | `AC-04`: Iconos visibles, circulares con `target.tvMin` accesible. | `BR-04` |
| `FR-05` | Navegación D-Pad completa en toda la fila de controles. | Must | `AC-05`: `Focusable` con recorrido secuencial Left/Right y anillo `border.focus`. | `BR-05` |
| `FR-06` | Emite eventos al pulsar cada elemento (`onDestinationSelected`, `onSearchPressed`, etc.). | Must | `AC-06`: Invocación del callback correspondiente. | `BR-06` |
| `FR-07` | Altura y padding sujetos estrictamente a tokens (`layout.topBarHeight`, `contentPadding`). | Must | `AC-07`: Sin valores numéricos hardcodeados. | `BR-07` |
| `FR-08` | Degradado de fondo con scrim para garantizar contraste sobre hero visual. | Must | `AC-08`: Fondo con gradiente desde `canvas` con alpha hasta transparente. | `BR-08` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | El logo usa el asset oficial de branding. | `tokens.json` | `TC-01` |
| `BR-02` | Todos los textos provienen de localización ARB (`CMP-17`). | `ui-design-system.md` §3 | `TC-02` |
| `BR-03` | La pestaña activa se indica con texto de alto contraste y píldora `color.surface.elevated` o subrayado acento. | `04-components.md` `DS-CHIP` | `TC-03` |
| `BR-04` | Los iconos son botones interactivos con accesibilidad y semántica declarada. | `04-components.md` `DS-BUTTON-ICON` | `TC-04` |
| `BR-05` | Ningún control depende de hover para operar; foco D-Pad obligatorio. | `ui-design-system.md` §2.6 | `TC-05` |
| `BR-06` | Callbacks nulos no provocan excepciones; deshabilitan o ignoran el click limpiamente. | `coding_standards.md` | `TC-06` |
| `BR-07` | Prohibidos los colores literales o `Colors.*` en widgets. | `ui-design-system.md` §3 | `TC-07` |
| `BR-08` | Contraste de texto mínimo AA sobre el degradado. | `01-foundations.md` | `TC-08` |

**Invariantes:**
- `INV-01`: Accesibilidad universal con teclado y D-Pad en todos los controles del header.
- `INV-02`: Inmutabilidad del modelo de destinos.
- `INV-03`: Respeto absoluto a la paleta de tokens FLIK (azul acento `#215FE6` / foco `#2F6BFF` sobre `#070A11`).

---

## 6. Estados y errores

| ID | Situación | Resultado |
|---|---|---|
| `ST-01` | Destino seleccionado (`HomeNavDestination.home`, etc.) | Se resalta la pestaña correspondiente como activa. |
| `ST-02` | Foco en pestaña o botón de icono | Anillo de 2dp `border.focus` con halo suave `accent.soft`. |
| `ST-03` | Botón sin callback asignado | Se renderiza sin reaccionar a la pulsación. |
| `E-01` | Logo no encontrado | Fallback a icono de cine/play del tema sin romper layout. |

---

## 7. Datos y contratos

### 7.1 Enum de Destinos

```dart
enum HomeNavDestination {
  home,
  series,
  movies,
  popular,
  myFlik,
}
```

### 7.2 `CT-01` — `HomeTopBar`

```dart
/// Cabecera interactiva y de navegación superior de FLIK (estilo TV/Netflix).
/// Spec: CMP-29
final class HomeTopBar extends StatelessWidget {
  const HomeTopBar({
    super.key,
    this.currentDestination = HomeNavDestination.home,
    this.onDestinationSelected,
    this.onSearchPressed,
    this.onNotificationsPressed,
    this.onSettingsPressed,
  });

  /// Destino actualmente activo.
  final HomeNavDestination currentDestination;

  /// Callback al elegir un elemento de navegación.
  final ValueChanged<HomeNavDestination>? onDestinationSelected;

  /// Callback para el botón de búsqueda.
  final VoidCallback? onSearchPressed;

  /// Callback para el botón de notificaciones.
  final VoidCallback? onNotificationsPressed;

  /// Callback para el botón de configuración.
  final VoidCallback? onSettingsPressed;
}
```

---

## 8. Dependencias y ciclo de vida

- **Permitidas:** `FlikColors`, `FlikLayout`, `FlikSpacing`, `FlikTypography`, `AppLocalizations`.
- **Prohibidas:** dependencias externas no declaradas, telemetría, `Colors.*` directos.
- **Ciclo de vida:** `StatelessWidget` / presentación reactiva guiada por parámetros.

---

## 9. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `home_top_bar.dart::_TopBarLogo` | `TC-01` | Planned |
| `FR-02` | `CT-01` | `home_top_bar.dart::_TopBarNavLinks` | `TC-02` | Planned |
| `FR-03` | `CT-01` | `home_top_bar.dart::_NavItem` | `TC-03` | Planned |
| `FR-04` | `CT-01` | `home_top_bar.dart::_TopBarActions` | `TC-04` | Planned |
| `FR-05` | `CT-01` | `home_top_bar.dart::_FocusableIconButton` | `TC-05` | Planned |
| `FR-06` | `CT-01` | `home_top_bar.dart::HomeTopBar` | `TC-06` | Planned |
| `FR-07` | `CT-01` | `home_top_bar.dart::build` | `TC-07` | Planned |
| `FR-08` | `CT-01` | `home_top_bar.dart::_TopBarScrim` | `TC-08` | Planned |

---

## 10. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Widget | `FR-01`: Logo renderizado | — | Asset o fallback visible |
| `TC-02` | Widget | `FR-02`: 5 destinos mostrados | Contexto l10n | 5 textos presentes en el árbol |
| `TC-03` | Widget | `FR-03`: Destino activo destacado | `currentDestination: series` | Estado visual diferenciado |
| `TC-04` | Widget | `FR-04`: 3 acciones presentes | — | 3 botones de icono presentes |
| `TC-05` | Widget | `FR-05`: Navegación con foco | Envío de teclas D-Pad | Foco se desplaza ordenadamente |
| `TC-06` | Widget | `FR-06`: Invocación de callbacks | Tap / Enter | Callback invocado 1 vez |
| `TC-07` | Widget | `FR-07`: Dimensiones conformes a tokens | Diferentes breakpoints | Altura igual a `topBarHeight` |
| `TC-08` | Widget | `FR-08`: Fondo degradado aplicado | — | Decoración con `LinearGradient` |

---

## 11. Criterios de aceptación BDD

```gherkin
@FR-02 @FR-03
Scenario: Navegar y seleccionar una categoría del menú
  Given la HomeTopBar con destino activo "home"
  When el usuario pulsa en "Series" o navega con D-Pad hasta ella y pulsa Enter
  Then se invoca onDestinationSelected con HomeNavDestination.series
```

```gherkin
@FR-04 @FR-05
Scenario: Acceso rápido a búsqueda con D-Pad
  Given la barra superior de FLIK
  When el usuario desplaza el foco a la acción de búsqueda y la activa
  Then se invoca onSearchPressed
```

---

## 12. Definition of Done

- [ ] Spec `CMP-29` y `user_story.md` sincronizadas.
- [ ] Cadenas ARB incorporadas en `app_es.arb` y `app_en.arb`.
- [ ] Widget `HomeTopBar` implementado cumpliendo tokens y cero colores literales.
- [ ] Tests de widget en `test/widgets/tv_experience/home_top_bar_test.dart` verificando foco, renderizado y callbacks.
- [ ] `flutter analyze` y `flutter test` pasan sin fallos.

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Cabecera estática con marca y espacio | Product Owner |
| 2.0 | 2026-10-26 | Mayor | Rediseño interactivo estilo Netflix: navegación de 5 destinos y 3 acciones rápidas con foco D-Pad | Product Owner |


