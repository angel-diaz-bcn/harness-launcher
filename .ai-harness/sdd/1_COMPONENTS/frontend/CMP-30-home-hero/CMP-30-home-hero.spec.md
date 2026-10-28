# CMP-30 — Home Hero

---
spec_id: CMP-30
spec_type: CMP
layer: frontend
name: Home Hero
target: lib/features/tv_experience/presentation/widgets/home/home_hero.dart
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
depends_on: [CMP-07, CMP-17, CMP-32]
consumed_by: [CMP-12]
---

`CMP-30` · `v1.0` · `tv_experience` · `Flutter` · `DRAFT`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `tv_experience` | `lib/features/tv_experience/presentation/widgets/home/home_hero.dart` |

> [!IMPORTANT]
> Bloque destacado de la Home: arte a sangre, scrim, identidad del título, metadatos y CTA «Ver ahora».

> [!WARNING]
> **Fuera de alcance:** tráiler, tabs, reparto, acciones secundarias y rotación automática.

> [!TIP]
> **Ruta de lectura:** §4 requisitos → §8 contratos → §10 trazabilidad.

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

1. Leer `CMP-12`, `05-pages.md` §4.1, `03-layout.md` §5.3 y `04-components.md` `DS-HERO`.
2. Implementar solo los `FR-*` definidos; no inventar campos ni acciones.
3. Registrar dudas en §15.

---

## 1. Contexto y objetivo

### 1.1 Problema

La Home necesita un destacado que permita decidir qué ver en un solo paso, con lectura a distancia.

### 1.2 Objetivo medible

Renderizar un `CatalogItem` real con fondo, título, sinopsis de dos líneas, metadatos y un CTA enfocable, en altura `layout.heroHeight`.

### 1.3 No objetivos

- Reproducir vídeo de fondo.
- Mostrar reparto, idiomas o extras.

---

## 2. Alcance y límites

**Incluye:** backdrop o placeholder, scrim, título original, sinopsis, metadatos, badge `ORIGINAL` y CTA.

**Excluye:** acciones secundarias, tabs y navegación a Detalle.

**Invariantes aplicables:** `architecture_rules.md` §4.7 (foco universal) y `ui-design-system.md` §3 (tokens).

---

## 3. Actores e historia de usuario

> **Como** usuario,
> **quiero** un destacado con acción clara,
> **para** empezar a ver sin explorar.

**Actores secundarios:** `CMP-12` (selección del ítem), `CMP-32` (arte de respaldo).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Recibe un `CatalogItem` y pinta su información. | Must | `AC-01`: título visible | `BR-01` |
| `FR-02` | Usa `backdropUri` con esquema `asset:` o `http(s)`; si es `null`, placeholder del sistema. | Must | `AC-02`: sin backdrop → placeholder | `BR-02` |
| `FR-03` | Sinopsis limitada a dos líneas con `maxLines` y elipsis. | Must | `AC-03`: no desborda | `BR-03` |
| `FR-04` | Muestra año, valoración y duración o número de temporadas. | Must | `AC-04`: al menos un metadato | `BR-04` |
| `FR-05` | El CTA «Ver ahora» es enfocable y activable con `Select`/`Enter`/`Space`. | Must | `AC-05`: invoca `onPlay` | `BR-05` |
| `FR-06` | Muestra el badge `ORIGINAL` solo si el ítem tiene tag `original`. | Must | `AC-06`: badge condicionado | `BR-06` |
| `FR-07` | No reproduce vídeo ni anima el fondo. | Must | `AC-07`: sin `VideoPlayer` ni autoplay | `BR-07` |
| `FR-08` | Altura desde `layout.heroHeight`; el texto vive en la mitad izquierda en `tv`/`expanded`. | Must | `AC-08`: cumple la plantilla | `BR-08` |
| `FR-09` | `Down` desde el CTA delega en el siguiente foco (sin capturarlo). | Must | `AC-09`: foco baja a la primera fila | `BR-09` |
| `FR-10` | Todos los textos vienen de ARB. | Must | `AC-10`: sin literales | `BR-10` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | El hero muestra un ítem real del catálogo. | `CMP-12` `FR-02` | `TC-01` |
| `BR-02` | Sin imagen no se inventa URL; se usa placeholder local. | `ADR-0007` §6 | `TC-02` |
| `BR-03` | Sinopsis como máximo dos líneas. | `05-pages.md` §6.1 | `TC-03` |
| `BR-04` | Los metadatos salen del modelo; nunca se rellenan con ceros. | `CMP-01` | `TC-04` |
| `BR-05` | Un único CTA principal. | `04-components.md` §5 | `TC-05` |
| `BR-06` | Badge solo con tag `original`. | `05-pages.md` §6.1 | `TC-06` |
| `BR-07` | Sin autoplay de vídeo. | `05-pages.md` §4.2 | `TC-07` |
| `BR-08` | Altura y alineación desde tokens. | `03-layout.md` §5.3 | `TC-08` |
| `BR-09` | El hero no atrapa el foco. | `FM-FLIK-007` | `TC-09` |
| `BR-10` | Sin literales. | `CMP-17` | `TC-10` |

**Invariantes:** `INV-01` sin red; `INV-02` sin `media_kit`; `INV-03` sin estados propios de reproducción.

---

## 6. Estados y errores

| ID | Situación | Resultado |
|---|---|---|
| `ST-01` | Ítem con backdrop | Arte + scrim |
| `ST-02` | Ítem sin backdrop | Placeholder + scrim |
| `E-01` | Sinopsis nula | Se omite el bloque |
| `E-02` | Sin metadatos | Se pinta solo título y CTA |
| `E-03` | Ítem no reproducible | CTA deshabilitado |

---

## 7. Datos y transformaciones

| Origen | Destino | Regla |
|---|---|---|
| `item.title` | Texto principal | Tal cual |
| `item.backdropUri` | Imagen de fondo | `asset:` o `http(s)`; `null` → placeholder |
| `item.synopsis` | Párrafo | Máximo 2 líneas |
| `item.year` / `rating` / `runtimeMinutes` | Fila de metadatos | Omitir nulos |
| `item.tags.contains('original')` | Badge | Booleano |
| `item.kind == series` | Texto de duración | `{n} temporadas` |

---

## 8. Contratos

### 8.1 `CT-01` — `HomeHero`

```dart
/// Bloque destacado de la Home.
/// Spec: CMP-30 / FR-01 .. FR-10
final class HomeHero extends StatelessWidget {
  const HomeHero({
    super.key,
    required this.item,
    required this.playLabel,
    required this.originalBadgeLabel,
    required this.seasonsLabelBuilder,
    required this.enabled,
    required this.onPlay,
    this.ctaFocusNode,
  });

  final CatalogItem item;
  final String playLabel;
  final String originalBadgeLabel;

  /// Construye «N temporadas» con el plural de ARB.
  final String Function(int seasons) seasonsLabelBuilder;

  final bool enabled;
  final VoidCallback onPlay;

  /// Nodo del CTA, propiedad de `CMP-12` para el foco inicial.
  final FocusNode? ctaFocusNode;
}
```

---

## 9. Dependencias y ciclo de vida

- **Permitidas:** `CatalogItem`, tema/tokens, `Image.asset`/`Image.network` solo lectura, ARB del llamador.
- **Prohibidas:** `media_kit`, `p2p_engine`, `drift`, HTTP propio y literales.
- **Ciclo de vida:** widget sin estado propio; el `FocusNode` lo gestiona `CMP-12`.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `.../home/home_hero.dart::HomeHero.build` | `TC-01` | Implemented |
| `FR-02` | `CT-01` | `.../home_hero.dart::_HeroArtwork` | `TC-02` | Implemented |
| `FR-03` | `CT-01` | `.../home_hero.dart::_Synopsis` | `TC-03` | Implemented |
| `FR-04` | `CT-01` | `.../home_hero.dart::_MetaRow` | `TC-04` | Implemented |
| `FR-05` | `CT-01` | `.../home_hero.dart::_HeroCta` | `TC-05` | Implemented |
| `FR-06` | `CT-01` | `.../home_hero.dart::_OriginalBadge` | `TC-06` | Implemented |
| `FR-07` | `CT-01` | `.../home_hero.dart::build` | `TC-07` | Implemented |
| `FR-08` | `CT-01` | `.../home_hero.dart::_HeroLayout` | `TC-08` | Implemented |
| `FR-09` | `CT-01` | `.../home_hero.dart::_HeroCta` | `TC-09` | Implemented |
| `FR-10` | `CT-01` | `lib/app/l10n/app_es.arb` · `app_en.arb` | `TC-10` | Implemented |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Widget | `FR-01` | Película del fixture | Título visible |
| `TC-02` | Widget | `FR-02` | Ítem sin backdrop | Placeholder presente |
| `TC-03` | Widget | `FR-03` | Sinopsis larga | No desborda |
| `TC-04` | Widget | `FR-04` | Año y rating | Fila visible |
| `TC-05` | Widget | `FR-05` | Pulsación `Enter` | `onPlay` invocado |
| `TC-06` | Widget | `FR-06` | Con y sin tag | Badge condicionado |
| `TC-07` | Widget | `FR-07` | Construcción | Sin reproductor |
| `TC-08` | Widget | `FR-08` | Breakpoint tv | Altura del token |
| `TC-09` | Widget | `FR-09` | `Down` | Foco baja |
| `TC-10` | Widget | `FR-10` | Textos | Desde ARB |

**Comandos:** `flutter analyze`, `flutter test test/widgets/tv_experience/home_hero_test.dart`.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-05
Scenario: Reproducir el destacado
  Given un hero con un ítem reproducible
  When el usuario pulsa Select sobre «Ver ahora»
  Then se invoca onPlay una vez
  And no se abre ninguna otra acción
```

```gherkin
@FR-02
Scenario: Destacado sin carátula
  Given un ítem con backdrop_uri nulo
  When se pinta el hero
  Then se muestra el placeholder del sistema
  And no se realiza ninguna petición de red
```

---

## 13. Definition of Done

- [ ] `FR-*` con `TC-*` y mapa completo.
- [ ] `CT-01` implementado.
- [ ] Sin literales ni valores fuera de tokens.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] §15 sin bloqueos.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-26 | Sin tráiler ni rotación | `05-pages.md` §4.2 | Alcance | Producto |
| 2026-10-26 | Placeholder local sin red | No hay carátulas todavía | `FR-02` | Producto |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿El hero rotará cuando existan varios destacados? | No | Producto | v2 |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Hero con CTA y metadatos | Pendiente |

