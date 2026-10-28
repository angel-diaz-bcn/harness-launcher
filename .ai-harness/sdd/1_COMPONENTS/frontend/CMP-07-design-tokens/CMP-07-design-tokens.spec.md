---
spec_id: CMP-07
spec_type: CMP
layer: frontend
name: Design Tokens and Theme
target: lib/app/theme/flik_theme.dart
block: app
status: APPROVED
version: 1.0
owner: UI Team
last_reviewed: 2026-10-25
approved_at: 2026-10-25
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: []
design_ref: .ai-harness/context/ui-design-system.md
depends_on: []
consumed_by: [CMP-08, CMP-09, CMP-10, CMP-12, CMP-13, CMP-14, CMP-15, CMP-16, CMP-33, CMP-34]
---

# 🎨 CMP-07 — Design Tokens y Tema

`CMP-07` · `APPROVED` · `v1.0` · `Flutter` · `app`

| 🧩 Tipo | 🚦 Estado | 🧭 Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `app` | `lib/app/theme/flik_theme.dart` |

**Target:** `lib/app/theme/flik_theme.dart`
**Bloque:** `app`
**Estado:** `APPROVED`

> [!IMPORTANT]
> Esta spec materializa los tokens de `.ai-harness/design-system/tokens.json` en un tema Flutter verificable. No define componentes ni pantallas. El diseño es la autoridad; el código solo lo implementa.

> [!WARNING]
> Prohibido añadir tokens nuevos aquí: cualquier cambio de valor nace en `tokens.json`.

## 🗺️ Mapa de lectura

| Bloque | Qué encontrarás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y errores |
| §7–§9 | API, contratos y dependencias |
| §10–§12 | Mapa, pruebas y BDD |
| §13–§15 | DoD, decisiones y preguntas |

---

## 1. Contexto y objetivo

### 1.1 Problema

Los valores visuales existen solo como documentación. Sin una fuente Dart verificable, las pantallas pueden divergir y `preflight` no puede impedir estilos locales.

### 1.2 Objetivo medible

Un paquete de tema que reproduce exactamente `tokens.json`, con paridad verificada por test y cero colores fuera de `lib/app/theme/`.

### 1.3 No objetivos

- Componentes de interfaz.
- Pantallas o rutas.
- Localización.
- Tema claro.

---

## 2. Alcance y límites

**Incluye:**

- Constantes de color, tipografía, espacio, radios, bordes, movimiento, foco, layout, iconos y objetivos.
- `ThemeData` oscuro y `ThemeExtension` semántica.
- Utilidad de decoración de foco.
- Resolución de breakpoint.
- Tests de paridad, contraste, layout y foco.

**Excluye:**

- Cualquier widget de pantalla.
- Cualquier valor no presente en `tokens.json`.
- Cualquier acceso a red, almacenamiento o features.

**Invariantes aplicables:**

- `architecture_rules.md` §4.7 (foco universal).
- `ui-design-system.md` §3 (sin valores fuera de tokens).

---

## 3. Actores e historia

> **Como** equipo de UI,
> **quiero** un tema único derivado de los tokens,
> **para** que todas las pantallas compartan color, tipografía y foco sin estilos locales.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | `tokens.json` es la única fuente de valores | Alta | Cada valor tiene su constante Dart equivalente | `INV-01` |
| `FR-02` | El tema expone `ThemeData` oscuro con `ColorScheme` derivado | Alta | `FlikTheme.dark` no usa colores por defecto de Material | `BR-01` |
| `FR-03` | `FlikSemanticColors` expone texto y estados como `ThemeExtension` | Alta | `Theme.of(context).extension<FlikSemanticColors>()` nunca es nulo | `BR-02` |
| `FR-04` | La tipografía resuelve tamaño y altura por breakpoint | Alta | `FlikTypography.title` devuelve estilo distinto en `tv` y `compact` | `BR-03` |
| `FR-05` | `FlikLayout.of(context)` resuelve breakpoint y medidas | Alta | Devuelve el breakpoint correcto en 599, 1024 y 1600 dp | `BR-04` |
| `FR-06` | Existe una decoración de foco reutilizable | Alta | Anillo, halo y escala sin alterar el layout | `BR-05` |
| `FR-07` | Prohibidos colores fuera de `lib/app/theme/` | Alta | `preflight` no encuentra `Color(`, `Colors.` ni HEX | `INV-02` |
| `FR-08` | Se respetan escalado de texto y animaciones reducidas | Media | Escala limitada al máximo declarado; sin transición si `disableAnimations` | `BR-06` |

## 5. Reglas de negocio e invariantes

| ID | Regla |
|---|---|
| `BR-01` | Solo existe tema oscuro; `brightness` es `Brightness.dark`. |
| `BR-02` | La extensión semántica se registra en `extensions` y se resuelve con un acceso tipado, nunca con `!`. |
| `BR-03` | El breakpoint se decide por ancho lógico, nunca por `Platform`. |
| `BR-04` | `FlikLayout` usa los cortes de `layout.breakpoints`; no introduce cortes propios. |
| `BR-05` | El foco nunca cambia el tamaño del layout: se aplica con transformación. |
| `BR-06` | La escala de texto se limita al rango declarado en el sistema; el exceso se recorta, no se ignora. |
| `INV-01` | Ningún valor visual existe fuera de `tokens.json`. |
| `INV-02` | Ningún widget construye colores; solo consume `FlikColors`, `FlikSemanticColors` o `ThemeData`. |

---

## 6. Errores y estados

| ID | Situación | Resultado exigido |
|---|---|---|
| `E-01` | `tokens.json` ausente o ilegible | El test de paridad falla con mensaje de ruta |
| `E-02` | Valor de color no parseable | El test de paridad falla indicando token |
| `E-03` | Contraste por debajo de AA | El test de contraste falla indicando par de tokens |
| `E-04` | Token sin constante Dart o constante sin token | El test de paridad falla en ambos sentidos |
| `E-05` | `FlikSemanticColors` no registrada | El test de tema falla al resolver la extensión |

---

## 7. API pública

```dart
abstract final class FlikColors {
  static const Map<String, Color> values;
  static Color get brandPrimary;
  static Color get accent;
  static Color get canvas;
  static Color get surface;
}

@immutable
final class FlikSemanticColors extends ThemeExtension<FlikSemanticColors> {
  const FlikSemanticColors({
    required this.textPrimary,
    required this.textSecondary,
    required this.textDisabled,
    required this.textAccent,
    required this.textOnAccent,
    required this.success,
    required this.warning,
    required this.error,
    required this.info,
  });
}

abstract final class FlikTypography {
  static TextStyle of(FlikTextRole role, FlikBreakpoint breakpoint);
  static TextStyle display(BuildContext context);
  static TextStyle headline(BuildContext context);
  static TextStyle title(BuildContext context);
  static TextStyle section(BuildContext context);
  static TextStyle body(BuildContext context);
  static TextStyle label(BuildContext context);
  static TextStyle caption(BuildContext context);
  static TextStyle eyebrow(BuildContext context);
}

final class FlikLayout {
  const FlikLayout({required this.breakpoint, required this.size});
  static FlikLayout of(BuildContext context);
}

abstract final class FlikFocusDecoration {
  static BoxDecoration of(
    BuildContext context, {
    required bool focused,
    BorderRadius? borderRadius,
  });
}
```

---

## 8. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `FlikColors` | Clase abstracta final con mapa const de colores |
| `CT-02` | `FlikSemanticColors` | `ThemeExtension<FlikSemanticColors>` inmutable |
| `CT-03` | `FlikTypography` | Estilos resueltos por rol y breakpoint |
| `CT-04` | `FlikLayout` | Objeto inmutable con breakpoint y medidas |
| `CT-05` | `FlikFocusDecoration` | Fábrica de `BoxDecoration` y escala de foco |
| `CT-06` | `FlikTheme` | Construye `ThemeData` oscuro |

---

## 9. Dependencias

Permitidas: Flutter SDK, `dart:convert` y `dart:io` solo en tests.

Prohibidas: paquetes de UI externos, generadores de código, `media_kit`, bases de datos y cualquier feature.

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `lib/app/theme/flik_colors.dart::FlikColors` | `TC-01` | Verified |
| `FR-02` | `CT-06` | `lib/app/theme/flik_theme.dart::FlikTheme.dark` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `lib/app/theme/flik_theme.dart::FlikSemanticColors` | `TC-03` | Verified |
| `FR-04` | `CT-03` | `lib/app/theme/flik_typography.dart::FlikTypography` | `TC-04` | Verified |
| `FR-05` | `CT-04` | `lib/app/theme/flik_layout.dart::FlikLayout.of` | `TC-05` | Verified |
| `FR-06` | `CT-05` | `lib/app/theme/flik_focus.dart::FlikFocusDecoration` | `TC-06` | Verified |
| `FR-07` | `CT-01` | `lib/app/theme/` | `TC-07` | Verified |
| `FR-08` | `CT-04` | `lib/app/flik_app.dart::FlikApp` | `TC-08` | Verified |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | Paridad de tokens | `tokens.json` | Todos los valores coinciden y no sobran claves |
| `TC-02` | Unit | Tema oscuro | `FlikTheme.dark` | `brightness == dark` y esquema derivado de tokens |
| `TC-03` | Widget | Extensión semántica | `MaterialApp` con tema | La extensión se resuelve sin nulos |
| `TC-04` | Unit | Tipografía por breakpoint | Anchos 599 y 1600 | Tamaños distintos y pesos correctos |
| `TC-05` | Unit | Breakpoints | Anchos 599, 1024, 1600 | `compact`, `expanded`, `tv` |
| `TC-06` | Widget | Foco | Elemento enfocado | Anillo y halo presentes; layout sin desplazamiento |
| `TC-07` | Static | Sin colores fuera del tema | `lib/` | Cero coincidencias de `Color(`, `Colors.`, HEX |
| `TC-08` | Widget | Escala y animaciones | Escala 1.3 y `disableAnimations` | Sin overflow y sin transición |

Comandos: `flutter analyze`, `flutter test test/app/theme/`, `preflight`.

---

## 12. Criterios BDD

```gherkin
@FR-01
Scenario: Cambiar un token exige cambiar el tema
  Given el valor de color.accent.base en tokens.json
  When se modifica sin actualizar FlikColors
  Then el test de paridad falla indicando el token
  And la build no se considera valida

@FR-05
Scenario: Resolver breakpoint de TV
  Given una ventana logica de 1920 dp
  When se consulta FlikLayout.of(context)
  Then el breakpoint es tv
  And el padding de contenido es el de TV

@FR-07
Scenario: Widget con color literal
  Given un widget que declara un color literal
  When se ejecuta preflight
  Then la validacion falla con UI-HARDCODED-COLOR
```

## 13. Definition of Done

- [x] Todos los `FR-*` tienen `CT-*`, `TC-*` y entrada en §10.
- [x] `tokens.json` y el tema Dart coinciden en nombres y valores.
- [x] `flutter analyze` y `flutter test test/app/theme/` pasan.
- [x] `preflight` sin violaciones de tokens.
- [x] Sin valores de color fuera de `lib/app/theme/`.
- [x] Sin dependencias fuera de §9.
- [x] Sin preguntas bloqueantes en §15.

---

## 14. Decisiones

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-25 | Paleta derivada del logotipo oficial | Coherencia de marca y contraste | `FR-01` | Product Owner |
| 2026-10-25 | Solo tema oscuro en v1 | Producto cinematográfico y OLED | `FR-02` | Product Owner |
| 2026-10-25 | `accent` usa el azul de marca para cumplir AA con texto blanco | El azul más claro no alcanzaba 4.5:1 | `FR-01`, `FR-07` | Product Owner |
| 2026-10-25 | Escala de texto limitada a 130 % en el shell | Evitar desbordes en TV | `FR-08` | Product Owner |

---

## 15. Preguntas abiertas

No hay preguntas bloqueantes.

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Sistema de tokens y tema | Product Owner |



