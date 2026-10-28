# CMP-32 — Poster Card

---
spec_id: CMP-32
spec_type: CMP
layer: frontend
name: Poster Card
target: lib/features/tv_experience/presentation/widgets/home/poster_card.dart
block: tv_experience
status: APPROVED
version: 1.0
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
consumed_by: [CMP-30, CMP-31]
---

`CMP-32` · `v1.0` · `tv_experience` · `Flutter` · `DRAFT`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `tv_experience` | `lib/features/tv_experience/presentation/widgets/home/poster_card.dart` |

> [!IMPORTANT]
> Tarjeta 2:3 enfocable con arte local o placeholder, título, metadato y activación por teclado.

> [!WARNING]
> **Fuera de alcance:** descarga de carátulas, progreso, badges de calidad y acciones secundarias.

> [!TIP]
> **Ruta de lectura:** §4 → §8 → §10.

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

1. Leer `CMP-31`, `04-components.md` `DS-POSTER-CARD` y `01-foundations.md`.
2. Implementar solo lo definido; no añadir acciones.

---

## 1. Contexto y objetivo

### 1.1 Problema

Sin carátulas todavía, la Home necesita una tarjeta que represente cada título y sea navegable y activable con el mando.

### 1.2 Objetivo medible

Renderizar una tarjeta 2:3 con foco visible y activación por `Select`/`Enter`/`Space`, usando `asset:` si existe y placeholder si no.

### 1.3 No objetivos

- Progreso, badges, hover y menús.

---

## 2. Alcance y límites

**Incluye:** arte o placeholder, título, metadato, foco y activación.

**Excluye:** descarga de imágenes, lógica de reproducción y estado de selección.

**Invariantes aplicables:** `ui-design-system.md` §3 y §5; `FM-FLIK-007`.

---

## 3. Actores e historia de usuario

> **Como** usuario,
> **quiero** una tarjeta clara con foco visible,
> **para** identificar y abrir un título.

**Actores secundarios:** `CMP-31` (contenedor), `CMP-12` (activación).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Mantiene proporción 2:3 con ancho de token `layout.poster.width`. | Must | `AC-01`: aspect ratio 2/3 | `BR-01` |
| `FR-02` | Si `posterUri` usa `asset:` y el asset existe, lo muestra; si es `http(s)` o nulo, usa placeholder. | Must | `AC-02`: sin descarga de red | `BR-02` |
| `FR-03` | Muestra el título con máximo dos líneas. | Must | `AC-03`: elipsis tras dos líneas | `BR-03` |
| `FR-04` | Muestra un metadato: año en película, número de temporadas en serie. | Must | `AC-04`: al menos un metadato | `BR-04` |
| `FR-05` | En foco aplica anillo `border.focus`, halo `accent.soft` y escala `focus.scale` sin reflow. | Must | `AC-05`: tres señales de foco | `BR-05` |
| `FR-06` | `Select`, `Enter` o `Space` invocan `onActivate` si `enabled`. | Must | `AC-06`: callback una vez | `BR-06` |
| `FR-07` | Con `enabled == false` no es enfocable ni activable. | Must | `AC-07`: `canRequestFocus` falso | `BR-07` |
| `FR-08` | Expone etiqueta semántica con título y tipo. | Must | `AC-08`: lector anuncia título | `BR-08` |
| `FR-09` | El placeholder usa solo tokens y un icono del tema. | Must | `AC-09`: sin HEX ni gradientes decorativos | `BR-09` |
| `FR-10` | No conoce el reproductor ni el catálogo. | Must | `AC-10`: solo recibe `CatalogItem` y callbacks | `BR-10` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | Tamaño desde tokens. | `04-components.md` §3 | `TC-01` |
| `BR-02` | Prohibido cargar `http(s)` en v1. | `block_ui_navigation_engine.md` | `TC-02` |
| `BR-03` | Dos líneas máximo. | `04-components.md` `DS-POSTER-CARD` | `TC-03` |
| `BR-04` | Metadato real; nunca inventado. | `CMP-01` | `TC-04` |
| `BR-05` | Foco no solo color. | `ui-design-system.md` §3.4 | `TC-05` |
| `BR-06` | Activación por teclado. | `architecture_rules.md` §4.7 | `TC-06` |
| `BR-07` | Deshabilitada si no es reproducible. | `CMP-12` `BR-10` | `TC-07` |
| `BR-08` | Semántica con rol de botón. | `04-components.md` §2.4 | `TC-08` |
| `BR-09` | Placeholder con tokens. | `FM-FLIK-011` | `TC-09` |
| `BR-10` | Sin dependencias de reproducción. | `architecture_rules.md` §2.4 | `TC-10` |

**Invariantes:** `INV-01` sin red; `INV-02` sin literales; `INV-03` sin estado propio.

---

## 6. Estados y errores

| ID | Situación | Resultado |
|---|---|---|
| `ST-01` | Normal | Arte o placeholder + textos |
| `ST-02` | Foco | Anillo + halo + escala |
| `ST-03` | Deshabilitada | Opacidad reducida, sin foco |
| `E-01` | Asset declarado pero ausente | Placeholder |
| `E-02` | Año y temporadas nulos | Se omite el metadato |
| `E-03` | Título vacío (imposible por contrato) | No ocurre |

---

## 7. Datos y transformaciones

| Origen | Destino | Regla |
|---|---|---|
| `item.posterUri` con `asset:` | Arte | `Image.asset` con `cacheWidth` de token |
| `item.posterUri` `http(s)` o `null` | Placeholder | No se descarga |
| `item.title` | Título | Máximo 2 líneas |
| `metaLabel` | Metadato | Texto ya localizado por `CMP-12` |

---

## 8. Contratos

### 8.1 `CT-01` — `PosterCard`

```dart
/// Tarjeta 2:3 de un título del catálogo.
/// Spec: CMP-32 / FR-01 .. FR-10
final class PosterCard extends StatefulWidget {
  const PosterCard({
    super.key,
    required this.item,
    required this.metaLabel,
    required this.enabled,
    required this.onActivate,
  });

  final CatalogItem item;

  /// Año o número de temporadas, ya localizado.
  final String metaLabel;

  final bool enabled;
  final VoidCallback onActivate;
}
```

**Resolución del arte:**

```dart
String? posterAssetOf(CatalogItem item) {
  final Uri? uri = item.posterUri;
  if (uri == null || uri.scheme != 'asset') {
    return null;
  }
  return uri.path;
}
```

---

## 9. Dependencias y ciclo de vida

- **Permitidas:** `CatalogItem`, tokens, `Image.asset`, `FocusableActionDetector`.
- **Prohibidas:** `Image.network`, repositorio, reproductor, literales.
- **Ciclo de vida:** estado propio solo para foco/pressed; sin recursos externos.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `.../home/poster_card.dart::_PosterArtwork` | `TC-01` | Implemented |
| `FR-02` | `CT-01` | `.../poster_card.dart::posterAssetOf` | `TC-02` | Implemented |
| `FR-03` | `CT-01` | `.../poster_card.dart::_PosterTitle` | `TC-03` | Implemented |
| `FR-04` | `CT-01` | `.../poster_card.dart::_PosterMeta` | `TC-04` | Implemented |
| `FR-05` | `CT-01` | `.../poster_card.dart::_PosterFocusRing` | `TC-05` | Implemented |
| `FR-06` | `CT-01` | `.../poster_card.dart::_PosterActions` | `TC-06` | Implemented |
| `FR-07` | `CT-01` | `.../poster_card.dart::PosterCard.build` | `TC-07` | Implemented |
| `FR-08` | `CT-01` | `.../poster_card.dart::_PosterSemantics` | `TC-08` | Implemented |
| `FR-09` | `CT-01` | `.../poster_card.dart::_PosterPlaceholder` | `TC-09` | Implemented |
| `FR-10` | `CT-01` | `.../poster_card.dart` | `TC-10` | Implemented |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Widget | `FR-01` | Película | Relación 2:3 |
| `TC-02` | Widget | `FR-02` | URI `http(s)` y nula | Placeholder; sin red |
| `TC-03` | Widget | `FR-03` | Título largo | Dos líneas y elipsis |
| `TC-04` | Widget | `FR-04` | Año / temporadas | Metadato visible |
| `TC-05` | Widget | `FR-05` | Foco | Anillo, halo y escala |
| `TC-06` | Widget | `FR-06` | `Enter` | `onActivate` una vez |
| `TC-07` | Widget | `FR-07` | `enabled == false` | No enfocable |
| `TC-08` | Widget | `FR-08` | Semántica | Etiqueta con título |
| `TC-09` | Widget | `FR-09` | Sin póster | Placeholder con tokens |
| `TC-10` | Widget | `FR-10` | Construcción | Sin reproductor |

**Comandos:** `flutter analyze`, `flutter test test/widgets/tv_experience/poster_card_test.dart`.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-02
Scenario: Tarjeta sin carátula local
  Given un ítem con poster_uri https
  When se pinta la tarjeta
  Then se muestra el placeholder
  And no se realiza ninguna petición de red
```

```gherkin
@FR-06
Scenario: Activar una tarjeta con el mando
  Given una tarjeta enfocada y habilitada
  When el usuario pulsa Select
  Then se invoca onActivate una vez
  And el foco permanece en la tarjeta
```

---

## 13. Definition of Done

- [ ] `FR-*` con `TC-*` y mapa completo.
- [ ] `CT-01` implementado.
- [ ] Sin descarga de imágenes, literales ni HEX.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] §15 sin bloqueos.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-26 | Solo `asset:` se pinta; `http(s)` usa placeholder | La UI no descarga carátulas | `FR-02` | Arquitectura |
| 2026-10-26 | Metadato preparado por `CMP-12` | Evitar concatenación en el widget | `CT-01` | Arquitectura |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Qué componente poseerá la caché de carátulas remotas? | No | Arquitectura | Se decidirá antes de F3 |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Tarjeta con placeholder y foco | Pendiente |

