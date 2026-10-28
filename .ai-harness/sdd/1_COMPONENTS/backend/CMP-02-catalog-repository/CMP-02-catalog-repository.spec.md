# CMP-02 — Catalog Repository

---
spec_id: CMP-02
spec_type: CMP
layer: backend
name: Catalog Repository
target: lib/features/catalog/domain/catalog_repository.dart
block: catalog
status: APPROVED
version: 2.0
owner: Architecture
last_reviewed: 2026-10-27
approved_at: 2026-10-27
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-02]
depends_on: [CMP-01, CMP-03, CMP-35]
consumed_by: [CMP-04, CMP-12]
---

`CMP-02` · `v2.0` · `catalog` · `Dart` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `catalog` | `lib/features/catalog/domain/catalog_repository.dart` |

> [!IMPORTANT]
> **Contrato de lectura del catálogo local.** Toda la presentación lee el catálogo a través de esta interfaz. Ningún widget, controlador de `tv_experience` ni pantalla puede importar `drift`, abrir SQLite ni conocer rutas de archivo.

> [!WARNING]
> **Fuera de alcance:** progreso de visualización, filtros combinados de Categoría, sincronización remota, descarga de carátulas y cualquier escritura desde la presentación.

> [!TIP]
> **Ruta de lectura:** §4 requisitos → §8 contratos → §10 trazabilidad → §11 pruebas.

### 🗺️ Mapa de lectura

| Bloque | Qué encontrarás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y errores |
| §7–§9 | Datos, contratos y dependencias |
| §10–§12 | Trazabilidad, pruebas y BDD |
| §13–§15 | Cierre, decisiones y preguntas |

---

## 0. Protocolo de lectura y no invención

1. Leer esta spec, `CMP-01`, `CMP-03` y `architecture_rules.md` §2.3 y §6.
2. Implementar solo los `FR-*` y `CT-*` definidos aquí.
3. No añadir consultas, campos, estados ni cachés que no estén especificados.
4. Si falta un dato, registrarlo en §15 y detener la implementación.
5. Actualizar §10 y §11 en el mismo cambio que el código.

**Jerarquía de verdad:** contexto → arquitectura → `CMP-01` → esta spec → código.

---

## 1. Contexto y objetivo

### 1.1 Problema

La Home necesita leer el catálogo persistido sin acoplarse a SQLite. Hoy la feature `catalog` solo contiene el contrato JSON; no existe una API de lectura ni un adaptador de base de datos.

### 1.2 Objetivo medible

Exponer una interfaz asíncrona que devuelva como máximo 20 ítems por consulta de fila, con orden determinista y errores tipados, y que sea la única puerta de lectura para `tv_experience`.

### 1.3 No objetivos

- Decidir qué fila pinta la Home ni en qué orden.
- Elegir la variante a reproducir.
- Persistir el catálogo (lo hace `CMP-03` vía `PRC-02`).
- Gestionar progreso de visualización.

---

## 2. Alcance y límites

**Incluye:**

- Lectura de un ítem completo por `id`.
- Lectura de ítems por tag, por género, por tipo y mejor valorados.
- Límite obligatorio por consulta (1–20) con valor por defecto 20.
- Orden determinista y filtro de ítems sin variantes reproducibles.
- Error tipado ante fallo de almacenamiento.

**Excluye:**

- Escritura de catálogo y migraciones: `CMP-03` y `PRC-02`.
- Validación de documentos JSON: `CMP-01`.
- Cálculo de facetas, contadores y filtros combinados: `CMP-13`.
- Progreso, ajustes y carátulas.

**Invariantes de arquitectura aplicables:**

- `architecture_rules.md` §2.3: el catálogo no conoce reproducción ni presentación.
- `architecture_rules.md` §2.4: los widgets no acceden a almacenamiento.
- `architecture_rules.md` §6: prohibido materializar listas ilimitadas.
- `FM-FLIK-010`: sin campos ni estados fuera de spec.

---

## 3. Actores e historia de usuario

> **Como** capa de presentación,
> **quiero** consultar el catálogo de **un canal concreto** por tag, género, tipo y valoración,
> **para** construir la Home de ese canal sin conocer SQLite.

**Actores secundarios:** `CMP-12` (consumidor), `PRC-02` (ingesta), `CMP-03` (almacén).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | `itemById(channelId, id)` devuelve el ítem completo con variantes o temporadas, o `null` si no existe **en ese canal**. | Must | `AC-01`: `MovieItem` con sus `MediaVariant`; ítem de otro canal → `null` | `BR-01` |
| `FR-02` | `itemsByTag(channelId, tag)` devuelve hasta `limit` ítems del canal que contienen exactamente el tag indicado. | Must | `AC-02`: solo ítems del canal con ese tag; máximo `limit` | `BR-02`, `BR-03` |
| `FR-03` | `itemsByGenre(channelId, genre)` devuelve hasta `limit` ítems del canal que contienen exactamente el género indicado. | Must | `AC-03`: solo ítems del canal con ese género; máximo `limit` | `BR-02`, `BR-03` |
| `FR-04` | `itemsByKind(channelId, kind)` devuelve hasta `limit` ítems del canal del tipo indicado. | Must | `AC-04`: solo `movie` o solo `series` del canal | `BR-02`, `BR-03` |
| `FR-05` | `topRated(channelId)` devuelve hasta `limit` ítems del canal ordenados por valoración descendente. | Must | `AC-05`: orden no creciente por `rating`; los `null` van al final | `BR-02`, `BR-04` |
| `FR-06` | Toda consulta de fila aplica el mismo orden de desempate. | Must | `AC-06`: rating desc, año desc, id asc | `BR-04` |
| `FR-07` | Las consultas de fila excluyen ítems sin variantes reproducibles. | Must | `AC-07`: un ítem sin variantes no aparece | `BR-05` |
| `FR-08` | Un `limit` fuera de rango produce `CatalogRepositoryFailure` con código `invalidLimit` y no consulta la base. | Must | `AC-08`: `limit = 0` o `21` → fallo tipado | `BR-06` |
| `FR-09` | Cualquier fallo del almacén se traduce a `CatalogRepositoryFailure` con `databaseUnavailable` o `queryFailed`. | Must | `AC-09`: excepción de Drift → fallo tipado, sin filtrar detalles | `BR-07` |
| `FR-10` | El repositorio no expone tipos de `drift` ni rutas de archivo. | Must | `AC-10`: la API pública solo usa tipos de `catalog_contract.dart` y del propio archivo | `BR-08` |
| `FR-11` | `genresByChannel(channelId)` devuelve los géneros presentes con su número de ítems, ordenados por cantidad descendente y después por nombre ascendente. | Must | `AC-11`: 6 géneros máximo, sin repetidos | `BR-09` |
| `FR-12` | Todas las consultas exigen `channelId` no vacío; un valor vacío produce `CatalogRepositoryFailure` con código `invalidChannel`. | Must | `AC-12`: `channelId` vacío → fallo tipado sin consultar | `BR-10` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | Un `id` inexistente devuelve `null`; no lanza error. | Esta spec | `TC-01` |
| `BR-02` | `limit` por defecto 20; rango permitido 1–20. | `05-pages.md` §4.2 | `TC-06` |
| `BR-03` | El filtro por tag/género es igualdad exacta sobre los valores normalizados por `CMP-01`. | `CMP-01` §8 | `TC-02`, `TC-03` |
| `BR-04` | Orden: `rating` descendente con `null` al final, después `year` descendente con `null` al final, después `id` ascendente. | Esta spec | `TC-05` |
| `BR-05` | «Reproducible» = película con al menos una variante, o serie con al menos un episodio con al menos una variante. | `CMP-01` `BR-04`, `BR-05` | `TC-07` |
| `BR-06` | Un `limit` inválido es error de programación controlado, nunca una consulta sin límite. | `architecture_rules.md` §6 | `TC-06` |
| `BR-07` | Los mensajes de error no incluyen SQL, rutas ni trazas. | `security_privacy.md` | `TC-08` |
| `BR-08` | La presentación no importa `drift`, `sqflite`, `sqlite3` ni `path_provider`. | `block_ui_navigation_engine.md` | Revisión de imports + `preflight` |
| `BR-09` | Los géneros se devuelven tal como los declara el catálogo, sin traducir ni normalizar. | `CMP-36` `BR-08` | `TC-09` |
| `BR-10` | Sin `channelId` no hay consulta: el aislamiento entre canales es total. | `CMP-03` `BR-13` | `TC-10` |

**Invariantes:**

- `INV-01`: ninguna consulta de fila devuelve más de 20 ítems.
- `INV-02`: ninguna consulta abre red ni escribe en disco.
- `INV-03`: el repositorio no modifica datos.

---

## 6. Estados y errores

| ID | Situación | Código | Resultado |
|---|---|---|---|
| `E-01` | `limit` fuera de 1–20 | `invalidLimit` | `CatalogRepositoryFailure`; ninguna consulta |
| `E-02` | Base de datos no inicializada o cerrada | `databaseUnavailable` | `CatalogRepositoryFailure` |
| `E-03` | Error de consulta o mapeo | `queryFailed` | `CatalogRepositoryFailure` |
| `E-04` | `id` inexistente | — | `null` |
| `E-05` | Tag o género sin resultados | — | lista vacía |

---

## 7. Datos y transformaciones

| Origen (SQLite) | Destino (dominio) | Regla |
|---|---|---|
| `catalog_items` | `MovieItem` / `SeriesItem` | `kind` decide el tipo; `cast`, `directors` y `external_ids` se deserializan de JSON textual |
| `item_genres` | `CatalogItem.genres` | orden alfabético ascendente |
| `item_tags` | `CatalogItem.tags` | orden alfabético ascendente |
| `variants` | `MediaVariant` | `quality` se convierte con `CatalogQuality.wireName`; `magnet_uri` a `Uri` |
| `seasons` + `episodes` | `SeriesSeason` / `SeriesEpisode` | temporadas por `season_number` asc; episodios por `episode_number` asc |
| `poster_uri` / `backdrop_uri` / `still_uri` | `Uri?` | `NULL` permanece `null`; nunca se inventa una URI |

---

## 8. Contratos

### 8.1 `CT-01` — `CatalogRepository`

```dart
/// Límite máximo por fila de Home.
const int kCatalogMaxRowLimit = 20;

/// Límite por defecto de las consultas de fila.
const int kCatalogHomeRowLimit = kCatalogMaxRowLimit;

/// Género presente en un canal, con su número de ítems.
/// Spec: CMP-02 / FR-11
final class GenreFacet {
  const GenreFacet({required this.genre, required this.itemCount});

  final String genre;
  final int itemCount;
}

/// Única puerta de lectura del catálogo local, siempre por canal.
/// Spec: CMP-02 / FR-01, FR-02, FR-03, FR-04, FR-05, FR-11
abstract interface class CatalogRepository {
  /// Spec: CMP-02 / FR-01
  Future<CatalogItem?> itemById(String channelId, String id);

  /// Spec: CMP-02 / FR-02
  Future<List<CatalogItem>> itemsByTag(
    String channelId,
    String tag, {
    int limit = kCatalogHomeRowLimit,
  });

  /// Spec: CMP-02 / FR-03
  Future<List<CatalogItem>> itemsByGenre(
    String channelId,
    String genre, {
    int limit = kCatalogHomeRowLimit,
  });

  /// Spec: CMP-02 / FR-04
  Future<List<CatalogItem>> itemsByKind(
    String channelId,
    CatalogKind kind, {
    int limit = kCatalogHomeRowLimit,
  });

  /// Spec: CMP-02 / FR-05
  Future<List<CatalogItem>> topRated(
    String channelId, {
    int limit = kCatalogHomeRowLimit,
  });

  /// Spec: CMP-02 / FR-11
  Future<List<GenreFacet>> genresByChannel(String channelId);
}
```

**Regla:** `kCatalogGenreFacetLimit = 6` acota los géneros devueltos por `genresByChannel`.

### 8.2 `CT-02` — `CatalogRepositoryErrorCode`

```dart
/// Motivos de fallo del repositorio de catálogo.
/// Spec: CMP-02 / FR-08, FR-09
enum CatalogRepositoryErrorCode {
  invalidLimit,
  invalidChannel,
  databaseUnavailable,
  queryFailed,
}
```

### 8.3 `CT-03` — `CatalogRepositoryFailure`

```dart
/// Error tipado del repositorio de catálogo.
/// Spec: CMP-02 / FR-08, FR-09
final class CatalogRepositoryFailure implements Exception {
  const CatalogRepositoryFailure({
    required this.code,
    required this.message,
    this.cause,
  });

  final CatalogRepositoryErrorCode code;
  final String message;

  /// Causa original para diagnóstico local; nunca se muestra en UI.
  final Object? cause;

  @override
  String toString() => 'CatalogRepositoryFailure($code): $message';
}
```

---

## 9. Dependencias y ciclo de vida

### 9.1 Dependencias permitidas

- `lib/features/catalog/domain/catalog_contract.dart` (`CMP-01`).
- Implementación de `CMP-03` solo en `data/repositories/sqlite_catalog_repository.dart`.
- `dart:async` y utilidades puras de Dart.

### 9.2 Prohibidas

- `drift` fuera de `lib/features/catalog/data/`.
- Flutter (`widgets`, `material`, `services`) en `domain/`.
- `media_kit`, `player`, `p2p_engine`, `tv_experience`.
- Red, `path_provider` en la interfaz de dominio y telemetría.

### 9.3 Ciclo de vida

- **Creación:** en la composición de dependencias de `lib/app/`, junto a `CMP-03`.
- **Suscripción:** sin streams; cada método es una lectura puntual.
- **Cancelación:** el llamador puede ignorar el `Future`; no hay recursos abiertos.
- **Destrucción:** el repositorio no cierra la base de datos; lo hace su propietario (`CMP-03`).

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `lib/features/catalog/domain/catalog_repository.dart::CatalogRepository.itemById` · `lib/features/catalog/data/repositories/sqlite_catalog_repository.dart::SqliteCatalogRepository.itemById` | `TC-01` | Verified |
| `FR-02` | `CT-01` | `lib/features/catalog/data/repositories/sqlite_catalog_repository.dart::SqliteCatalogRepository.itemsByTag` | `TC-02` | Verified |
| `FR-03` | `CT-01` | `lib/features/catalog/data/repositories/sqlite_catalog_repository.dart::SqliteCatalogRepository.itemsByGenre` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `lib/features/catalog/data/repositories/sqlite_catalog_repository.dart::SqliteCatalogRepository.itemsByKind` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `lib/features/catalog/data/repositories/sqlite_catalog_repository.dart::SqliteCatalogRepository.topRated` | `TC-05` | Verified |
| `FR-06` | `CT-01` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.selectItems` | `TC-05` | Verified |
| `FR-07` | `CT-01` | `lib/features/catalog/data/local/catalog_database.dart::_playableClause` | `TC-07` | Verified |
| `FR-08` | `CT-02`, `CT-03` | `lib/features/catalog/domain/catalog_repository.dart::validateCatalogLimit` | `TC-06` | Verified |
| `FR-09` | `CT-03` | `lib/features/catalog/data/repositories/sqlite_catalog_repository.dart::_guard` | `TC-08` | Verified |
| `FR-10` | `CT-01` | `lib/features/catalog/catalog.dart` | `TC-09` | Verified |

**Estados:** `Pending`, `Implemented`, `Verified`.

**Regla anti-deriva:** todo símbolo público del repositorio que no aparezca en esta tabla está fuera de spec.

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | `FR-01` | Catálogo de prueba con una película y una serie | Devuelve los modelos completos; un id inexistente devuelve `null` |
| `TC-02` | Unit | `FR-02` | Ítems con tags `featured`, `trending`, `original` | Solo devuelve los que tienen el tag pedido |
| `TC-03` | Unit | `FR-03` | Géneros `sci-fi`, `action`, `drama` | Solo devuelve los del género pedido |
| `TC-04` | Unit | `FR-04` | Mezcla de películas y series | `CatalogKind.movie` devuelve solo películas |
| `TC-05` | Unit | `FR-05`, `FR-06` | Ratings `8.5`, `9.0`, `null`, años distintos | Orden correcto y desempate estable |
| `TC-06` | Unit | `FR-08` | `limit = 0`, `limit = 21` | `CatalogRepositoryFailure.invalidLimit` |
| `TC-07` | Unit | `FR-07` | Serie con temporada sin episodios | No aparece en la fila |
| `TC-08` | Unit | `FR-09` | Base de datos cerrada | `databaseUnavailable`, mensaje sin SQL |
| `TC-09` | Unit | `FR-10` | Análisis de imports | `domain/catalog_repository.dart` no importa `drift` ni Flutter |

**Comandos:**

- `flutter analyze`
- `flutter test test/unit/catalog/catalog_repository_test.dart`

**Prohibido:** red real, temporizadores reales, SQLite en archivo y expectativas de píxeles.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-02
Scenario: Obtener los destacados de la Home
  Given un catálogo local con 5 ítems etiquetados "featured" y 3 sin esa etiqueta
  When la Home solicita itemsByTag("featured")
  Then el repositorio devuelve exactamente 5 ítems
  And todos contienen el tag "featured"
  And el resultado respeta el orden rating desc, year desc, id asc
```

```gherkin
@FR-08
Scenario: Límite de fila inválido
  Given una Home que solicita 21 ítems para un raíl
  When el repositorio recibe limit = 21
  Then devuelve CatalogRepositoryFailure con código invalidLimit
  And no ejecuta ninguna consulta sobre la base de datos
  And la Home puede mostrar el estado de error sin caerse
```

```gherkin
@FR-07
Scenario: Serie sin episodios reproducibles
  Given una serie persistida con una temporada sin episodios
  When la Home solicita itemsByKind(CatalogKind.series)
  Then la serie no aparece en el resultado
  And el resto de series reproducibles se mantiene
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` tienen `AC-*`, `TC-*` y entrada en §10.
- [ ] Todos los `CT-*` están implementados y referenciados por código.
- [ ] Los símbolos públicos llevan comentario `/// Spec: CMP-02 / FR-...`.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] No hay placeholders ni secciones vacías.
- [ ] No se añadieron dependencias fuera de §9.
- [ ] §15 no tiene preguntas bloqueantes.
- [ ] La spec está en `APPROVED` y `sync-sdd` no reporta `DIVERGED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-26 | Spec aprobada e implementada | Validación de las specs de datos por el usuario | Todos los `FR` | Product Owner |
| 2026-10-26 | El orden de fila es rating desc, year desc, id asc | Determinismo entre plataformas y pruebas estables | `FR-06`, `BR-04` | Architecture |
| 2026-10-26 | `limit` máximo 20 por consulta | `05-pages.md` §4.2 y `architecture_rules.md` §6 | `FR-08`, `INV-01` | Architecture |
| 2026-10-26 | La selección de variante no vive aquí | `architecture_rules.md` §2.3 | Alcance | Architecture |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿La Home deduplica ítems repetidos entre raíles? | No | Producto | Se decide en `CMP-12`; no afecta a este contrato |
| `Q-02` | ¿Se añadirá búsqueda de texto completo en v2? | No | Producto | Fuera de alcance; requeriría FTS5 y migración |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Contrato de lectura del catálogo para la Home | Pendiente |

