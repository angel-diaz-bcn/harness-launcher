# CMP-12 — Home Screen

---
spec_id: CMP-12
spec_type: CMP
layer: frontend
name: Home Screen
target: lib/features/tv_experience/presentation/screens/home_screen.dart
block: tv_experience
status: APPROVED
version: 3.0
owner: UI Team
last_reviewed: 2026-10-27
approved_at: 2026-10-27
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: []
design_ref: .ai-harness/context/ui-design-system.md
components: [CMP-29, CMP-30, CMP-31, CMP-32]
depends_on: [CMP-02, CMP-15, CMP-29, CMP-30, CMP-31, CMP-32, CMP-35]
consumed_by: [CMP-00]
---

`CMP-12` · `v3.0` · `tv_experience` · `Flutter` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `tv_experience` | `lib/features/tv_experience/presentation/screens/home_screen.dart` |

> [!IMPORTANT]
> **Home del espacio implícito «Mi FLIK».** Compone hero y raíles desde `CatalogRepository`, gestiona foco D-Pad y abre el reproductor con la mejor variante disponible.

> [!WARNING]
> **Fuera de alcance:** Detalle, Categoría, Perfiles, Espacios, «Continuar viendo», progreso, descarga de carátulas y autoplay.

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

1. Leer esta spec, `CMP-02`, `CMP-15`, `CMP-29`–`CMP-32` y `design-system/05-pages.md` §4.
2. Implementar solo los `FR-*` y `CT-*` definidos aquí.
3. No añadir filas, estados, acciones ni textos fuera de ARB.
4. Si falta un dato, registrarlo en §15 y detener la implementación.
5. Actualizar §10 y §11 en el mismo cambio que el código.

**Jerarquía de verdad:** contexto → arquitectura → specs de componentes → esta spec → código.

---

## 1. Contexto y objetivo

### 1.1 Problema

El catálogo está persistido, pero `main.dart` solo abre `SamplePlayback`. No existe una pantalla que consuma `CatalogRepository` ni una ruta hacia el reproductor desde el catálogo.

### 1.2 Objetivo medible

Mostrar en el primer frame, sin red, un hero y hasta ocho raíles de 20 tarjetas como máximo; recorrerlos completos con D-Pad; y abrir `PlaybackScreen` con una petición válida al activar cualquier tarjeta.

### 1.3 No objetivos

- Resolver progreso o reanudar.
- Elegir idioma de pistas.
- Navegar a Detalle o Categoría.
- Descargar carátulas.

---

## 2. Alcance y límites

**Incluye:**

- Carga de filas desde `CatalogRepository`.
- Composición de hero y raíles.
- Foco inicial, recorrido D-Pad y retorno al hero.
- Selección de variante y construcción de `PlaybackLaunchRequest`.
- Estados de carga, vacío y error con reintento.
- Localización de todos los textos con ARB.

**Excluye:**

- Escritura en catálogo o base de datos.
- Lógica de reproducción o P2P.
- Perfiles, espacios y configuración.
- Carrusel automático o autoplay.

**Invariantes de arquitectura aplicables:**

- `architecture_rules.md` §2.4: widgets solo pintan y emiten intenciones.
- `architecture_rules.md` §4.7: todo control alcanzable con D-Pad.
- `architecture_rules.md` §4.8: primera pantalla desde caché, sin red.
- `block_ui_navigation_engine.md`: prohibido importar `drift`, bases de datos o `media_kit`.

---

## 3. Actores e historia de usuario

> **Como** usuario,
> **quiero** ver un destacado y raíles de títulos,
> **para** elegir qué ver y reproducirlo con el mando.

**Actores secundarios:** `CMP-02` (datos), `CMP-15` (reproductor), `CMP-29`–`CMP-32` (UI).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Al montar, la pantalla consulta el repositorio una sola vez por fila y compone el estado `ready` cuando terminan todas. | Must | `AC-01`: una llamada por fila; estado final `ready` | `BR-01` |
| `FR-02` | El hero es el primer ítem de `itemsByTag('featured')`; si no hay, el primer ítem de `topRated()`. | Must | `AC-02`: con featured usa el primero; sin featured usa el mejor valorado | `BR-02` |
| `FR-03` | Se componen los raíles derivados del contenido real del canal y se omiten los vacíos. | Must | `AC-03`: solo aparecen filas con al menos un ítem | `BR-03` |
| `FR-04` | Cada raíl solicita como máximo 20 ítems. | Must | `AC-04`: ninguna fila supera 20 tarjetas | `BR-04` |
| `FR-05` | El foco inicial es el CTA del hero; si no hay hero, la primera tarjeta del primer raíl. | Must | `AC-05`: foco en «Ver ahora» | `BR-05` |
| `FR-06` | `Down` desde el hero lleva a la primera tarjeta del primer raíl; `Up` desde la primera fila vuelve al hero. | Must | `AC-06`: recorrido vertical correcto | `BR-06` |
| `FR-07` | `Left`/`Right` recorren las tarjetas del raíl y desplazan la fila para mantener el foco visible. | Must | `AC-07`: el foco nunca queda fuera de pantalla | `BR-07` |
| `FR-08` | `Back` vuelve a Canales cuando existe pantalla anterior; en la raíz cierra la aplicación. | Must | `AC-08`: `Back` no deja una pantalla vacía | `BR-08` |
| `FR-09` | Activar una tarjeta de película resuelve la variante de mayor calidad y abre `PlaybackScreen`. | Must | `AC-09`: `PlaybackLaunchRequest` con magnet, título, calidad y póster | `BR-09` |
| `FR-10` | Activar una tarjeta de serie resuelve el primer episodio de la primera temporada y su mejor variante. | Must | `AC-10`: subtítulo «T1 E1» y magnet del episodio | `BR-10` |
| `FR-11` | La posición inicial es siempre `Duration.zero` en v1. | Must | `AC-11`: request con `initialPosition` cero | `BR-11` |
| `FR-12` | Un fallo del repositorio muestra el estado de error con acción «Reintentar» enfocada. | Must | `AC-12`: error visible y reintento recarga | `BR-12` |
| `FR-13` | Un catálogo sin ítems muestra el estado vacío con acción «Reintentar». | Must | `AC-13`: mensaje de catálogo vacío | `BR-13` |
| `FR-14` | Todo texto visible proviene de ARB (`es`, `en`). | Must | `AC-14`: sin literales en widgets | `BR-14` |
| `FR-15` | Recibe el canal activo y lo usa como contexto de la barra y del catálogo mostrado. | Must | `AC-15`: la barra muestra el nombre del canal | `BR-15` |
| `FR-16` | Si el canal no declara fuente, no consulta el repositorio y muestra el estado vacío de canal. | Must | `AC-16`: cero consultas; mensaje de canal vacío | `BR-16` |
| `FR-17` | La acción «Conectar una lista» del estado vacío de canal está deshabilitada, es visible y explica el motivo. | Must | `AC-17`: control no enfocable con explicación visible | `BR-17` |

### 4.1 Raíles

Los raíles se derivan del contenido real del canal, no de un vocabulario fijo.

| Orden | Fila | Fuente | Condición |
|---|---|---|---|
| 1 | Destacados | `itemsByTag(channelId, 'featured')` | Solo si el catálogo declara el tag |
| 2 | Tendencias | `itemsByTag(channelId, 'trending')` | Solo si el catálogo declara el tag |
| 3 | Géneros | `genresByChannel(channelId)` + `itemsByGenre(channelId, género)` | Hasta seis géneros, por número de ítems descendente |
| 4 | Series | `itemsByKind(channelId, series)` | Solo si hay series |
| 5 | Mejor valoradas | `topRated(channelId)` | Siempre que haya ítems con nota |

> El hero se muestra además como primer ítem de su fila; no se deduplica.
>
> `genresByChannel` devuelve el nombre del género tal como lo declara el catálogo. No se traduce ni se normaliza.

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | La carga es de solo lectura y no bloquea el isolate de UI. | `architecture_rules.md` §6 | `TC-01` |
| `BR-02` | El hero nunca se inventa: sale de un ítem real del catálogo. | `05-pages.md` §4.1 | `TC-02` |
| `BR-03` | Ningún raíl vacío se pinta. | `05-pages.md` §4.2 | `TC-03` |
| `BR-04` | Límite de 20 ítems por raíl. | `CMP-02` `BR-02` | `TC-04` |
| `BR-05` | El foco inicial siempre existe en el primer frame útil. | `FM-FLIK-007` | `TC-05` |
| `BR-06` | El orden vertical del foco coincide con el orden visual. | `design-system/03-layout.md` §5.3 | `TC-06` |
| `BR-07` | Sin scrollbars visibles; el desplazamiento lo provoca el foco. | `ui-design-system.md` §5 | `TC-07` |
| `BR-08` | `Back` en la raíz no deja una pantalla en blanco. | `05-pages.md` §1 | `TC-08` |
| `BR-09` | La calidad elegida es la mayor de `2160p > 1080p > 720p > 480p > unknown`. | `CMP-01` §8.3 | `TC-09` |
| `BR-10` | Si la serie no tiene episodios reproducibles, la tarjeta no se activa. | `CMP-02` `BR-05` | `TC-10` |
| `BR-11` | Sin progreso persistido en v1. | Decisión de producto | `TC-11` |
| `BR-12` | Un error de una fila invalida la carga completa y permite reintentar. | Esta spec | `TC-12` |
| `BR-13` | Catálogo vacío no es error. | Esta spec | `TC-13` |
| `BR-14` | Prohibido literal de texto en widgets. | `CMP-17` | `TC-14` |
| `BR-15` | La Home solo muestra el catálogo del canal activo. | `05-pages.md` §4 | `TC-15` |
| `BR-16` | Un canal sin fuente no dispara consultas ni pinta hero. | `05-pages.md` §4 | `TC-16` |
| `BR-17` | Un control deshabilitado no recibe foco y su motivo es visible. | `01-foundations.md` §10 | `TC-17` |

**Invariantes:**

- `INV-01`: la Home no importa `drift`, `sqlite3`, `path_provider` ni `media_kit`.
- `INV-02`: la Home no escribe en el catálogo.
- `INV-03`: ninguna tarjeta depende de hover o toque para descubrirse.

---

## 6. Estados y errores

| ID | Estado | Contenido | Foco |
|---|---|---|---|
| `ST-01` | `loading` | Esqueleto de hero y dos filas | Ninguno hasta `ready` |
| `ST-02` | `ready` | Hero + raíles no vacíos | CTA del hero |
| `ST-03` | `empty` | Mensaje y acción «Reintentar` | Acción |
| `ST-04` | `error` | Mensaje, detalle local no visible y «Reintentar» | Acción |

| ID | Situación | Resultado |
|---|---|---|
| `E-01` | `CatalogRepositoryFailure` | Estado `error`; el mensaje técnico no se muestra |
| `E-02` | Ítem sin variante al activar | Tarjeta deshabilitada; sin apertura |
| `E-03` | Serie sin episodios | Tarjeta deshabilitada |
| `E-04` | Fila sin datos | Se omite |
| `E-05` | Sin hero | La primera fila sube; foco en su primera tarjeta |

---

## 7. Datos y transformaciones

| Origen | Destino | Transformación |
|---|---|---|
| `CatalogRepository.itemsByTag('featured')` | `HomeSection(featured)` | Copia hasta 20 |
| `itemsByTag('trending')` | `HomeSection(trending)` | Copia hasta 20 |
| `itemsByTag('original')` | `HomeSection(originals)` | Copia hasta 20 |
| `itemsByGenre('sci-fi')` | `HomeSection(sciFi)` | Copia hasta 20 |
| `itemsByGenre('action')` | `HomeSection(action)` | Copia hasta 20 |
| `itemsByGenre('drama')` | `HomeSection(drama)` | Copia hasta 20 |
| `itemsByGenre('animation')` | `HomeSection(animation)` | Copia hasta 20 |
| `itemsByKind(CatalogKind.series)` | `HomeSection(series)` | Copia hasta 20 |
| `topRated()` | `HomeSection(topRated)` | Copia hasta 20 |
| `sections.first.items.first` | `HomeController.hero` | `null` si no hay filas |
| `CatalogItem` + variante elegida | `PlaybackLaunchRequest` | Ver §8.3 |

---

## 8. Contratos

### 8.1 `CT-01` — `HomeScreen`

```dart
/// Pantalla raíz del espacio implícito «Mi FLIK».
/// Spec: CMP-12 / FR-01, FR-05
final class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
    required this.repository,
    required this.onPlay,
    required this.onExit,
  });

  final CatalogRepository repository;

  /// Emite la petición; la navegación la decide `lib/app/`.
  final ValueChanged<PlaybackLaunchRequest> onPlay;

  /// Cierre de la aplicación cuando no hay pantalla anterior.
  final VoidCallback onExit;
}
```

### 8.2 `CT-02` — `HomeController`

```dart
/// Estado de carga de la Home.
/// Spec: CMP-12 / §6
enum HomeStatus { loading, ready, empty, error }

/// Identificador de cada raíl.
/// Spec: CMP-12 / §4.1
enum HomeRowId {
  featured,
  trending,
  originals,
  sciFi,
  action,
  drama,
  animation,
  series,
  topRated,
}

/// Raíl resuelto con sus ítems.
/// Spec: CMP-12 / FR-03
final class HomeSection {
  const HomeSection({required this.id, required this.items});

  final HomeRowId id;
  final List<CatalogItem> items;
}

/// Controlador de la Home; única lógica de carga y composición.
/// Spec: CMP-12 / FR-01 .. FR-04, FR-12, FR-13
final class HomeController extends ChangeNotifier {
  HomeController({required CatalogRepository repository});

  HomeStatus get status;
  CatalogItem? get hero;
  List<HomeSection> get sections;
  Object? get failure;

  /// Carga todas las filas; idempotente mientras está en curso.
  /// Spec: CMP-12 / FR-01
  Future<void> load();
}
```

### 8.3 `CT-03` — Resolución de reproducción

```dart
/// Devuelve la petición o `null` si el ítem no es reproducible.
/// Spec: CMP-12 / FR-09, FR-10, FR-11
PlaybackLaunchRequest? resolvePlaybackRequest(CatalogItem item);

/// Calidad de mayor a menor.
/// Spec: CMP-12 / BR-09
const List<CatalogQuality> kPlaybackQualityPreference = <CatalogQuality>[
  CatalogQuality.uhd2160,
  CatalogQuality.fhd1080,
  CatalogQuality.hd720,
  CatalogQuality.sd480,
  CatalogQuality.unknown,
];
```

**Reglas de resolución:**

1. Película: variante de `item.variants` según `kPlaybackQualityPreference`.
2. Serie: primera temporada, primer episodio y su mejor variante.
3. `titleId`: `item.id` en película; `episode.id` en serie.
4. `subtitle`: `null` en película; `T{temporada} E{episodio}` en serie.
5. `qualityLabel`: `variant.quality.wireName`.
6. `posterUri`: `item.posterUri`.
7. `initialPosition`: `Duration.zero`.

---

## 9. Dependencias y ciclo de vida

### 9.1 Dependencias permitidas

- `package:flik/features/catalog/catalog.dart` (API pública).
- `PlaybackLaunchRequest` de `tv_experience`.
- Widgets `CMP-29`–`CMP-32` y tema/tokens de `lib/app/theme/`.
- `flutter/material.dart` y `flutter/services.dart` para teclas.

### 9.2 Prohibidas

- `drift`, `sqlite3`, `path_provider`, `media_kit`, `p2p_engine`.
- HTTP, descarga de imágenes y telemetría.
- Textos literales fuera de ARB.

### 9.3 Ciclo de vida

- **Creación:** `HomeController` en `initState`; `load()` una vez.
- **Suscripción:** `ChangeNotifier` escuchado por la pantalla.
- **Cancelación:** comprobar `mounted` tras cada `await`.
- **Destrucción:** `dispose()` del controlador; sin timers ni sockets.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-02` | `.../presentation/controllers/home_controller.dart::HomeController.load` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `.../home_controller.dart::HomeController._resolveHero` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `.../home_controller.dart::HomeController.load` | `TC-03` | Verified |
| `FR-04` | `CT-02` | `.../home_controller.dart::HomeController.load` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `.../screens/home_screen.dart::_HomeScreenState._focusHero` | `TC-05` | Verified |
| `FR-06` | `CT-01` | `.../screens/home_screen.dart::FocusTraversalGroup` | `TC-06` | Implemented |
| `FR-07` | `CT-01` | `.../widgets/home/home_row.dart::HomeRow` | `TC-07` | Implemented |
| `FR-08` | `CT-01` | `.../screens/home_screen.dart::PopScope` | `TC-08` | Implemented |
| `FR-09` | `CT-03` | `.../domain/playback_selection.dart::resolvePlaybackRequest` | `TC-09` | Verified |
| `FR-10` | `CT-03` | `.../domain/playback_selection.dart::resolvePlaybackRequest` | `TC-10` | Verified |
| `FR-11` | `CT-03` | `.../domain/playback_selection.dart::resolvePlaybackRequest` | `TC-11` | Verified |
| `FR-12` | `CT-02` | `.../home_controller.dart::HomeController._fail` | `TC-12` | Verified |
| `FR-13` | `CT-02` | `.../home_controller.dart::HomeController.load` | `TC-13` | Verified |
| `FR-14` | `CT-01` | `lib/app/l10n/app_es.arb` · `app_en.arb` | `TC-14` | Verified |
| `FR-15` | `CT-01` | `.../screens/home_screen.dart::HomeScreen.channel` | `TC-15` | Implemented |
| `FR-16` | `CT-01` | `.../screens/home_screen.dart::_ChannelEmptyPanel` | `TC-16` | Verified |
| `FR-17` | `CT-01` | `.../screens/home_screen.dart::_ChannelEmptyPanel` | `TC-17` | Implemented |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | `FR-01` | Repositorio falso | Una llamada por raíl; `ready` |
| `TC-02` | Unit | `FR-02` | Con y sin `featured` | Hero correcto |
| `TC-03` | Unit | `FR-03` | Filas vacías y llenas | Solo secciones con ítems |
| `TC-04` | Unit | `FR-04` | 30 ítems por fila | Máximo 20 |
| `TC-05` | Widget | `FR-05` | Home lista | Foco en «Ver ahora» |
| `TC-06` | Widget | `FR-06` | Home lista | `Down` y `Up` correctos |
| `TC-07` | Widget | `FR-07` | 10 tarjetas | Foco visible al avanzar |
| `TC-08` | Widget | `FR-08` | `Back` | `onExit` invocado |
| `TC-09` | Unit | `FR-09` | Película 1080p/2160p | Elige 2160p |
| `TC-10` | Unit | `FR-10` | Serie 2 temporadas | Usa T1E1 |
| `TC-11` | Unit | `FR-11` | Cualquier ítem | Posición cero |
| `TC-12` | Unit | `FR-12` | Repositorio con `queryFailed` | `error` y reintento |
| `TC-13` | Unit | `FR-13` | Repositorio vacío | `empty` |
| `TC-14` | Widget | `FR-14` | Textos de la Home | Provenientes de ARB |

**Comandos:**

- `flutter analyze`
- `flutter test test/unit/tv_experience/home_controller_test.dart`
- `flutter test test/unit/tv_experience/playback_selection_test.dart`
- `flutter test test/widgets/tv_experience/home_screen_test.dart`

**Prohibido:** red real, SQLite real, temporizadores reales y expectativas de píxeles.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-01
Scenario: Abrir la Home con catálogo local
  Given un catálogo con títulos en todas las filas
  When HomeScreen monta con el repositorio local
  Then el controlador carga nueve consultas como máximo
  And el estado pasa a ready
  And el foco queda en el CTA «Ver ahora»
```

```gherkin
@FR-09
Scenario: Reproducir una película desde la Home
  Given una tarjeta con variantes 1080p y 2160p
  When el usuario pulsa Select sobre la tarjeta
  Then se emite PlaybackLaunchRequest con la variante 2160p
  And la posición inicial es cero
```

```gherkin
@FR-12
Scenario: Fallo de almacenamiento al cargar la Home
  Given un repositorio que devuelve databaseUnavailable
  When la Home intenta cargar
  Then el estado es error
  And se muestra «Reintentar» enfocado
  And al reintentar se ejecuta una nueva carga
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` tienen `AC-*`, `TC-*` y entrada en §10.
- [ ] Todos los `CT-*` están implementados y referenciados.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] No hay literales de texto ni tokens hardcodeados.
- [ ] §15 no tiene preguntas bloqueantes.
- [ ] La spec está en `APPROVED` y `sync-sdd` no reporta `DIVERGED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-26 | Home sobre espacio implícito «Mi FLIK» | No hay Perfiles/Espacios en v1 | `FR-08` | Producto |
| 2026-10-26 | `Back` sale de la app | Evita una pantalla vacía sin Espacios | `FR-08` | Producto |
| 2026-10-26 | Serie → T1E1 y sin progreso | Decisión de producto para el MVP | `FR-10`, `FR-11` | Producto |
| 2026-10-26 | Calidad máxima por defecto | No existe aún ajuste de calidad | `BR-09` | Producto |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Se añadirá «Ver todo» cuando exista Categoría? | No | Producto | F3 |
| `Q-02` | ¿Se deduplicará el hero con la fila Destacados? | No | Diseño | v1 no deduplica |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Home con hero, raíles, foco y apertura del reproductor | Pendiente |



