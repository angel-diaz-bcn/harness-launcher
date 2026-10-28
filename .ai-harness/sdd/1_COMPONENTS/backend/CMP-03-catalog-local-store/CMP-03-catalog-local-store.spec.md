# CMP-03 — Catalog Local Store

---
spec_id: CMP-03
spec_type: CMP
layer: backend
name: Catalog Local Store
target: lib/features/catalog/data/local/catalog_database.dart
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
depends_on: [CMP-01]
consumed_by: [CMP-02, CMP-04]
---

`CMP-03` · `v2.0` · `catalog` · `Dart` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `catalog` | `lib/features/catalog/data/local/catalog_database.dart` |

> [!IMPORTANT]
> **Almacén local del catálogo.** SQLite mediante `drift`, con esquema versionado y reemplazo transaccional. Es el único lugar de la aplicación que abre la base de datos y ejecuta SQL.

> [!WARNING]
> **Fuera de alcance:** progreso de visualización, ajustes de usuario, colecciones curadas, búsqueda full-text, carátulas en `BLOB` y cualquier acceso remoto.

> [!TIP]
> **Ruta de lectura:** §4 requisitos → §7 esquema → §8 contratos → §10 trazabilidad.

### 🗺️ Mapa de lectura

| Bloque | Qué encontrarás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y errores |
| §7–§9 | Esquema, contratos y dependencias |
| §10–§12 | Trazabilidad, pruebas y BDD |
| §13–§15 | Cierre, decisiones y preguntas |

---

## 0. Protocolo de lectura y no invención

1. Leer esta spec, `ADR-0007`, `CMP-01` y `CMP-02`.
2. Implementar solo las tablas, columnas, índices y métodos aquí definidos.
3. No añadir tablas, campos ni migraciones fuera de spec.
4. Si falta un dato, registrarlo en §15 y detener la implementación.
5. Actualizar §10 y §11 en el mismo cambio que el código.

**Jerarquía de verdad:** contexto → `ADR-0007` → `CMP-01` → esta spec → código.

---

## 1. Contexto y objetivo

### 1.1 Problema

`ADR-0007` decide SQLite/Drift, pero no existe esquema, base de datos ni capa de consultas. Sin ellas, el repositorio no puede servir la Home y `PRC-02` no tiene destino transaccional.

### 1.2 Objetivo medible

Persistir un catálogo validado de hasta 20 000 ítems con sus relaciones, en una base de datos local reabrible, con reemplazo atómico y consultas indexadas de como máximo 20 filas.

### 1.3 No objetivos

- Validar documentos JSON (`CMP-01`).
- Exponer tipos de almacén a la presentación (`CMP-02` los encapsula).
- Guardar progreso, colecciones o ajustes.
- Sincronizar con fuentes remotas.

---

## 2. Alcance y límites

**Incluye:**

- Apertura de la base de datos en el directorio de soporte de la app.
- Esquema v1 con ítems, géneros, tags, temporadas, episodios, variantes y metadatos.
- Índices para las consultas de fila.
- Reemplazo transaccional del catálogo completo.
- Lectura de metadatos de ingesta.
- Cierre determinista de la base de datos.

**Excluye:**

- Mapeo a entidades de dominio (`CatalogMapper`, en `CMP-02`).
- Decisiones de qué fila pintar.
- Caché de imágenes.
- Copias de seguridad o exportación.

**Invariantes de arquitectura aplicables:**

- `ADR-0007` §Decisión.
- `architecture_rules.md` §4.8 y §6.
- `FM-FLIK-003`: ninguna caché crece sin límite declarado.
- `FM-FLIK-012`: los datos persistidos provienen de un documento ya validado; no se concatenan rutas de archivo.

---

## 3. Actores e historia de usuario

> **Como** capa de datos del catálogo,
> **quiero** un almacén SQLite tipado y transaccional,
> **para** servir la Home sin red y conservar el último catálogo válido.

**Actores secundarios:** `CMP-02` (lectura), `PRC-02` (escritura), `CMP-04` (origen validado).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | La base se abre con un `QueryExecutor` inyectable; en producción usa `getApplicationSupportDirectory()` y el archivo `catalog.sqlite`. | Must | `AC-01`: test con `NativeDatabase.memory()`; producción crea el archivo en soporte | `BR-01` |
| `FR-02` | El esquema v2 contiene las tablas `channels`, `catalog_items`, `item_genres`, `item_tags`, `seasons`, `episodes`, `variants` y `catalog_meta`. | Must | `AC-02`: las ocho tablas existen tras abrir | `BR-02` |
| `FR-03` | Se aplican restricciones: `kind` ∈ {`movie`, `series`}; `quality` ∈ {`2160p`,`1080p`,`720p`,`480p`,`unknown`}; cada variante pertenece a un ítem **o** a un episodio, nunca a ambos ni a ninguno. | Must | `AC-03`: insertar una variante sin dueño falla | `BR-03` |
| `FR-04` | Existen índices para `kind`, `rating`, `item_genres.genre`, `item_tags.tag`, `variants.item_id`, `variants.episode_id` y `episodes(item_id, season_number)`. | Must | `AC-04`: las consultas de fila usan índice | `BR-04` |
| `FR-05` | `replaceCatalog` reemplaza el catálogo completo en una sola transacción y devuelve el número de ítems escritos. | Must | `AC-05`: tras un fallo simulado, el catálogo anterior sigue íntegro | `BR-05` |
| `FR-06` | `selectItem` devuelve el registro completo del ítem (campos, géneros, tags, variantes y temporadas/episodios) o `null`. | Must | `AC-06`: película con variantes y serie con temporadas | `BR-06` |
| `FR-07` | `selectItems` filtra por `kind`, `tag` o `genre` con `limit` obligatorio entre 1 y 20 y orden `rating desc, year desc, id asc`. | Must | `AC-07`: máximo 20 filas y orden estable | `BR-07` |
| `FR-08` | `selectTopRated` ordena por `rating` descendente y aplica el mismo desempate. | Must | `AC-08`: ratings nulos al final | `BR-07` |
| `FR-09` | `readMeta`, `writeMeta` e `isCatalogEmpty` permiten a `PRC-02` decidir si la semilla está al día. | Must | `AC-09`: escribir y leer `seed.generated_at` | `BR-08` |
| `FR-10` | `close` es idempotente y libera el archivo; tras cerrar, cualquier consulta falla. | Must | `AC-10`: dos llamadas a `close` no lanzan | `BR-09` |
| `FR-11` | El esquema no contiene columnas `BLOB` ni datos personales. | Must | `AC-11`: revisión del esquema | `BR-10` |
| `FR-12` | Una versión de esquema desconocida recrea las tablas y registra `schema.reset = true` en `catalog_meta`. | Must | `AC-12`: abrir con `user_version = 99` deja la base vacía y marcada | `BR-11` |
| `FR-13` | `countItems` devuelve el número de ítems persistidos. | Must | `AC-13`: 48 ítems persistidos → `48` | `BR-08` |
| `FR-14` | La tabla `channels` persiste cada canal con `id`, `catalog_id` único, `name` único, `description`, `art`, `cover_uri`, `source_type`, `source_location`, `state`, `item_count`, `generated_at`, `last_synced_at`, `sort_order`, `is_default` y `created_at`. | Must | `AC-14`: dos canales con el mismo `catalog_id` son rechazados | `BR-12` |
| `FR-15` | `catalog_items.channel_id` es obligatorio, referencia `channels(id)` con borrado en cascada y está indexado junto a `kind` y `rating`. | Must | `AC-15`: borrar un canal elimina sus ítems | `BR-13` |
| `FR-16` | El `id` de cada ítem incluye el `catalog_id`, de modo que dos canales nunca colisionan. | Must | `AC-16`: mismo `imdb_id` en dos canales convive | `BR-13` |
| `FR-17` | `replaceChannelCatalog` reemplaza el contenido de **un** canal en una transacción y deja intactos los demás. | Must | `AC-17`: tras el reemplazo, los otros canales conservan su contador | `BR-14` |
| `FR-18` | `upsertChannel` inserta o actualiza un canal por `catalog_id` y devuelve su identificador interno. | Must | `AC-18`: dos llamadas seguidas no duplican el canal | `BR-12` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | La ruta de producción no se escribe a mano fuera de `CMP-03`. | `ADR-0007` §5 | `TC-01` |
| `BR-02` | Los nombres de tabla y columna son los de §7; no se renombran sin migración. | Esta spec | `TC-02` |
| `BR-03` | Una variante con `item_id` y `episode_id` nulos, o con ambos informados, es rechazada por la base. | `CMP-01` §8.3 | `TC-03` |
| `BR-04` | Toda consulta de fila debe apoyarse en un índice declarado. | `architecture_rules.md` §6 | `TC-04` |
| `BR-05` | El reemplazo usa `transaction { ... }`; nunca se borra fuera de la transacción. | `FM-FLIK-003`, `PRC-02` | `TC-05` |
| `BR-06` | `selectItem` no inventa relaciones: si no hay filas hijas, devuelve listas vacías. | `CMP-01` | `TC-06` |
| `BR-07` | `limit` se valida en la base como red de seguridad (1–20) y en `CMP-02` como contrato público. | `CMP-02` `BR-02` | `TC-07` |
| `BR-08` | Las claves de `catalog_meta` son las de `CatalogMetaKeys`, nunca literales dispersos. | Esta spec | `TC-08` |
| `BR-09` | `close` se llama desde el propietario; el doble cierre es seguro. | `FM-FLIK-005` | `TC-09` |
| `BR-10` | Solo se persisten URIs de texto; las imágenes viven en `assets/` o en caché de UI. | `ADR-0007` §6 | `TC-10` |
| `BR-11` | El catálogo es dato derivado: ante versión desconocida se recrea antes que migrar a ciegas. | `ADR-0007` §4 | `TC-11` |
| `BR-12` | `catalog_id` y `name` son únicos en `channels`; un `catalog_id` repetido actualiza el canal existente. | `CMP-36` `INV-01` | `TC-14` |
| `BR-13` | Todo ítem pertenece a un canal; no existen ítems huérfanos. | `PRC-07` | `TC-15` |
| `BR-14` | Reemplazar el catálogo de un canal nunca toca los datos de otro canal. | `PRC-07` | `TC-16` |

**Invariantes:**

- `INV-01`: la base de datos es estrictamente local; no abre sockets ni red.
- `INV-02`: no existe ninguna tabla de progreso, perfiles o ajustes en v1.
- `INV-03`: el contenido persistido proviene siempre de un `CatalogDocument` validado.

---

## 6. Estados y errores

| ID | Situación | Comportamiento |
|---|---|---|
| `E-01` | Error de apertura o ruta no accesible | La excepción sube a `CMP-02`, que la traduce a `databaseUnavailable` |
| `E-02` | Fallo durante `replaceCatalog` | Rollback completo; se propaga la excepción; el catálogo anterior permanece |
| `E-03` | `limit` fuera de 1–20 | `ArgumentError` de programación; no ejecuta SQL |
| `E-04` | Consulta después de `close` | La excepción sube a `CMP-02`, que la traduce a `databaseUnavailable` |
| `E-05` | `user_version` desconocida | Recreación de tablas + `schema.reset = true` |
| `E-06` | Documento con `id` duplicado | Imposible: `CMP-01` lo rechaza antes de llegar aquí |
| `E-07` | `catalog_id` ya existente en otro canal | No es error: `upsertChannel` actualiza ese canal y refresca su origen |
| `E-08` | Borrado de un canal | Sus ítems, géneros, tags, temporadas, episodios y variantes caen en cascada |

---

## 7. Esquema

### 7.1 `catalog_items`

| Columna | Tipo | Nulo | Notas |
|---|---|---|---|
| `id` | `TEXT` | No | PK; patrón de `CMP-01` |
| `channel_id` | `TEXT` | No | FK a `channels(id)` con `ON DELETE CASCADE` |
| `kind` | `TEXT` | No | `movie` o `series` |
| `title` | `TEXT` | No | — |
| `original_title` | `TEXT` | Sí | — |
| `synopsis` | `TEXT` | Sí | — |
| `year` | `INTEGER` | Sí | — |
| `rating` | `REAL` | Sí | 0–10 |
| `runtime_minutes` | `INTEGER` | Sí | — |
| `poster_uri` | `TEXT` | Sí | `asset:` o `http(s)` |
| `backdrop_uri` | `TEXT` | Sí | `asset:` o `http(s)` |
| `cast_json` | `TEXT` | No | Lista JSON de nombres |
| `directors_json` | `TEXT` | No | Lista JSON de nombres |
| `external_ids_json` | `TEXT` | No | Objeto JSON de claves texto |

### 7.2 `item_genres` e `item_tags`

| Tabla | Columnas | PK | Índice |
|---|---|---|---|
| `item_genres` | `item_id TEXT`, `genre TEXT` | (`item_id`,`genre`) | `item_genres_genre_idx (genre)` |
| `item_tags` | `item_id TEXT`, `tag TEXT` | (`item_id`,`tag`) | `item_tags_tag_idx (tag)` |

Ambas con `ON DELETE CASCADE` sobre `catalog_items(id)`.

### 7.3 `seasons`, `episodes`, `variants`

| Tabla | Columnas | PK / FK |
|---|---|---|
| `seasons` | `item_id TEXT`, `season_number INTEGER`, `title TEXT NULL` | PK (`item_id`,`season_number`); FK `item_id` |
| `episodes` | `id TEXT`, `item_id TEXT`, `season_number INTEGER`, `episode_number INTEGER`, `title TEXT`, `synopsis TEXT NULL`, `runtime_minutes INTEGER NULL`, `still_uri TEXT NULL` | PK `id`; FK (`item_id`,`season_number`) |
| `variants` | `id TEXT`, `item_id TEXT NULL`, `episode_id TEXT NULL`, `quality TEXT`, `magnet_uri TEXT`, `info_hash TEXT`, `file_index INTEGER NULL`, `size_bytes INTEGER NULL`, `video_codec TEXT NULL`, `audio_codecs_json TEXT`, `audio_languages_json TEXT`, `subtitle_languages_json TEXT`, `release_label TEXT NULL` | PK `id`; CHECK exactamente uno de `item_id`/`episode_id`; FK a `catalog_items` o `episodes` |

### 7.4 `catalog_meta`

| Columna | Tipo | Notas |
|---|---|---|
| `key` | `TEXT` | PK |
| `value` | `TEXT` | Valor serializado como texto |

Claves canónicas: `catalog.id`, `catalog.generated_at`, `seed.asset`, `seed.generated_at`, `seed.applied_at`, `schema.version`, `schema.reset`.

### 7.5 Índices

`catalog_items_kind_idx (kind)`, `catalog_items_rating_idx (rating)`, `catalog_items_channel_kind_idx (channel_id, kind)`, `catalog_items_channel_rating_idx (channel_id, rating)`, `item_genres_genre_idx (genre)`, `item_tags_tag_idx (tag)`, `variants_item_idx (item_id)`, `variants_episode_idx (episode_id)`, `episodes_season_idx (item_id, season_number)`.

### 7.6 `channels`

| Columna | Tipo | Nulo | Notas |
|---|---|---|---|
| `id` | `TEXT` | No | PK; kebab-case estable, derivado de `catalog_id` |
| `catalog_id` | `TEXT` | No | Único; identidad del catálogo (`CMP-36`) |
| `name` | `TEXT` | No | Único; nombre visible, desduplicado con sufijo numérico |
| `description` | `TEXT` | No | Texto del bloque de información |
| `art` | `TEXT` | No | `rings`, `grid`, `wave`, `prism` u `orbit` |
| `cover_uri` | `TEXT` | Sí | Solo `asset:` se pinta |
| `source_type` | `TEXT` | No | `asset`, `local_file` o `remote_url` |
| `source_location` | `TEXT` | No | Ruta o URL de donde se obtuvo |
| `state` | `TEXT` | No | `pending`, `syncing`, `ready` o `error` |
| `item_count` | `INTEGER` | No | Se recalcula al terminar cada sincronización |
| `generated_at` | `TEXT` | Sí | ISO-8601 del catálogo aplicado |
| `last_synced_at` | `TEXT` | Sí | ISO-8601 de la última sincronización correcta |
| `sort_order` | `INTEGER` | No | Orden en el carrusel |
| `is_default` | `INTEGER` | No | `1` para los cinco canales por defecto |
| `created_at` | `TEXT` | No | ISO-8601 |

Índices: `channels_catalog_idx (catalog_id)` único, `channels_name_idx (name)` único.

---

## 8. Contratos

### 8.1 `CT-01` — `CatalogDatabase`

```dart
/// Versión del esquema local del catálogo.
/// Spec: CMP-03 / FR-12
const int kCatalogLocalSchemaVersion = 2;

/// Nombre del archivo de base de datos en el directorio de soporte.
/// Spec: CMP-03 / FR-01
const String kCatalogDatabaseFileName = 'catalog.sqlite';

/// Base de datos SQLite del catálogo; generada por drift.
/// Spec: CMP-03 / FR-01, FR-02
@DriftDatabase(
  tables: [
    CatalogItems,
    ItemGenres,
    ItemTags,
    Seasons,
    Episodes,
    Variants,
    CatalogMeta,
  ],
)
final class CatalogDatabase extends _$CatalogDatabase {
  CatalogDatabase(super.executor);

  /// Spec: CMP-03 / FR-05
  Future<int> replaceCatalog(
    CatalogDocument document, {
    Map<String, String> meta = const <String, String>{},
  });

  /// Spec: CMP-03 / FR-06
  Future<CatalogItemRecord?> selectItem(String id);

  /// Spec: CMP-03 / FR-07
  Future<List<CatalogItemRecord>> selectItems({
    CatalogKind? kind,
    String? tag,
    String? genre,
    required int limit,
  });

  /// Spec: CMP-03 / FR-08
  Future<List<CatalogItemRecord>> selectTopRated({required int limit});

  /// Spec: CMP-03 / FR-09
  Future<String?> readMeta(String key);

  /// Spec: CMP-03 / FR-09
  Future<void> writeMeta(String key, String value);

  /// Spec: CMP-03 / FR-09
  Future<bool> isCatalogEmpty();

  /// Spec: CMP-03 / FR-13
  Future<int> countItems();

  /// Spec: CMP-03 / FR-10
  Future<void> close();
}
```

### 8.2 `CT-02` — `CatalogItemRecord`

```dart
/// Instantánea de un ítem y sus relaciones, lista para mapear a dominio.
/// Spec: CMP-03 / FR-06, FR-07, FR-08
final class CatalogItemRecord {
  const CatalogItemRecord({
    required this.id,
    required this.kind,
    required this.title,
    required this.originalTitle,
    required this.synopsis,
    required this.year,
    required this.rating,
    required this.runtimeMinutes,
    required this.posterUri,
    required this.backdropUri,
    required this.genres,
    required this.tags,
    required this.cast,
    required this.directors,
    required this.externalIds,
    required this.variants,
    required this.seasons,
  });

  final String id;
  final CatalogKind kind;
  final String title;
  final String? originalTitle;
  final String? synopsis;
  final int? year;
  final double? rating;
  final int? runtimeMinutes;
  final Uri? posterUri;
  final Uri? backdropUri;
  final List<String> genres;
  final List<String> tags;
  final List<String> cast;
  final List<String> directors;
  final Map<String, String> externalIds;
  final List<MediaVariant> variants;
  final List<SeriesSeason> seasons;
}
```

### 8.3 `CT-03` — `CatalogMetaKeys`

```dart
/// Claves canónicas de catalog_meta.
/// Spec: CMP-03 / FR-09
abstract final class CatalogMetaKeys {
  static const String catalogId = 'catalog.id';
  static const String catalogGeneratedAt = 'catalog.generated_at';
  static const String seedAsset = 'seed.asset';
  static const String seedGeneratedAt = 'seed.generated_at';
  static const String seedAppliedAt = 'seed.applied_at';
  static const String schemaVersion = 'schema.version';
  static const String schemaReset = 'schema.reset';
}
```

---

## 9. Dependencias y ciclo de vida

### 9.1 Dependencias permitidas

- `drift`, `drift/native` y utilidades de `dart:convert`.
- `path_provider` y `path` solo en el abridor de producción (`catalog_database_opener.dart`).
- `catalog_contract.dart` (`CMP-01`) para tipos de entrada.

### 9.2 Prohibidas

- `lib/features/tv_experience/`, `player`, `p2p_engine` y `media_kit`.
- Red, `http`, descarga de imágenes y telemetría.
- Tablas de progreso, perfiles o ajustes en v1.

### 9.3 Ciclo de vida

- **Creación:** una instancia por proceso, compuesta en `lib/app/`.
- **Suscripción:** sin streams en v1; consultas puntuales.
- **Cancelación:** `replaceCatalog` no es cancelable; si el proceso muere, SQLite revierte la transacción abierta.
- **Destrucción:** `close()` idempotente; libera el archivo y las sentencias preparadas.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `lib/features/catalog/data/local/catalog_database_opener.dart::openCatalogDatabase` | `TC-01` | Verified |
| `FR-02` | `CT-01` | `lib/features/catalog/data/local/catalog_tables.dart::CatalogItems` y tablas relacionadas | `TC-02` | Verified |
| `FR-03` | `CT-01` | `lib/features/catalog/data/local/catalog_tables.dart::Variants` (CHECK y enums) | `TC-03` | Verified |
| `FR-04` | `CT-01` | `lib/features/catalog/data/local/catalog_tables.dart` (anotaciones de índice) | `TC-04` | Verified |
| `FR-05` | `CT-01` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.replaceCatalog` | `TC-05` | Verified |
| `FR-06` | `CT-01`, `CT-02` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.selectItem` | `TC-06` | Verified |
| `FR-07` | `CT-01`, `CT-02` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.selectItems` | `TC-07` | Verified |
| `FR-08` | `CT-01` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.selectTopRated` | `TC-08` | Verified |
| `FR-09` | `CT-01`, `CT-03` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.readMeta` · `writeMeta` · `isCatalogEmpty` | `TC-09` | Verified |
| `FR-10` | `CT-01` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.close` | `TC-10` | Verified |
| `FR-11` | `CT-02` | `lib/features/catalog/data/local/catalog_records.dart::CatalogItemRecord` | `TC-11` | Verified |
| `FR-12` | `CT-01`, `CT-03` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.migration` | `TC-12` | Verified |
| `FR-13` | `CT-01` | `lib/features/catalog/data/local/catalog_database.dart::CatalogDatabase.countItems` | `TC-05` | Verified |

**Estados:** `Pending`, `Implemented`, `Verified`.

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | `FR-01` | `NativeDatabase.memory()` | Abre sin tocar disco; el esquema se crea |
| `TC-02` | Unit | `FR-02` | `sqlite_master` tras abrir | Las siete tablas existen |
| `TC-03` | Unit | `FR-03` | Inserción directa de variante sin dueño | La restricción rechaza la fila |
| `TC-04` | Unit | `FR-04` | `EXPLAIN QUERY PLAN` de cada consulta de fila | Usa el índice esperado |
| `TC-05` | Unit | `FR-05` | Fixture `catalog-v1-movies-series.json` + fallo inyectado | Catálogo anterior intacto tras el fallo |
| `TC-06` | Unit | `FR-06` | Película y serie del fixture | Registro completo; id inexistente → `null` |
| `TC-07` | Unit | `FR-07` | Catálogo con 30 ítems por tag | Máximo 20 y orden estable |
| `TC-08` | Unit | `FR-08` | Ratings nulos y distintos | Nulos al final |
| `TC-09` | Unit | `FR-09` | `writeMeta` + `readMeta` | Devuelve el valor escrito |
| `TC-10` | Unit | `FR-10` | Doble `close` | Sin excepción; consulta posterior falla |
| `TC-11` | Unit | `FR-11` | Inspección de columnas | Ningún `BLOB`; sin tablas de usuario |
| `TC-12` | Unit | `FR-12` | `PRAGMA user_version = 99` | Tablas recreadas y `schema.reset = true` |

**Comandos:**

- `dart run build_runner build --delete-conflicting-outputs`
- `flutter analyze`
- `flutter test test/unit/catalog/catalog_database_test.dart`

**Prohibido:** SQLite en archivo, red real, temporizadores reales y datos de usuario.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-05
Scenario: Reemplazar el catálogo completo de forma atómica
  Given una base con el catálogo semilla de 48 ítems
  When PRC-02 llama a replaceCatalog con un documento válido de 12 ítems
  Then el catálogo anterior queda eliminado
  And la base contiene exactamente 12 ítems con sus relaciones
  And replaceCatalog devuelve 12
```

```gherkin
@FR-05
Scenario: Fallo a mitad de reemplazo
  Given una base con el catálogo anterior de 48 ítems
  When la escritura falla después de borrar las tablas
  Then la transacción hace rollback
  And el catálogo anterior sigue disponible con sus 48 ítems
  And la excepción se propaga a PRC-02 como fallo de almacenamiento
```

```gherkin
@FR-12
Scenario: Esquema de versión desconocida
  Given un archivo con user_version = 99
  When se abre la base de datos
  Then el esquema v1 se recrea vacío
  And catalog_meta registra schema.reset = true
  And PRC-02 puede reingestar la semilla
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` tienen `AC-*`, `TC-*` y entrada en §10.
- [ ] Todos los `CT-*` están implementados y referenciados por código.
- [ ] Los símbolos públicos llevan comentario `/// Spec: CMP-03 / FR-...`.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] El esquema coincide exactamente con §7.
- [ ] No hay placeholders ni secciones vacías.
- [ ] §15 no tiene preguntas bloqueantes.
- [ ] La spec está en `APPROVED` y `sync-sdd` no reporta `DIVERGED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-26 | Spec aprobada e implementada | Esquema SQLite verificado con pruebas en memoria | Todos los `FR` | Product Owner |
| 2026-10-26 | SQLite + Drift con esquema v1 de siete tablas | `ADR-0007` | `FR-01`–`FR-12` | Architecture |
| 2026-10-26 | Cast, directores e IDs externos como JSON textual | Evitar tablas sin consultas y mantener el esquema mínimo | `CT-02` | Architecture |
| 2026-10-26 | Sin tablas de progreso ni ajustes en v1 | Se implementan en F2.5 con migración propia | `INV-02` | Producto |
| 2026-10-26 | Recreación ante versión desconocida | El catálogo es dato derivado y siempre reingestable | `FR-12` | Architecture |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Se añadirá una tabla de colecciones curadas en v1.1? | No | Producto | Se decidirá con `CMP-13` y Detalle |
| `Q-02` | ¿Se necesita `VACUUM` tras reemplazos? | No | Architecture | Se medirá con el catálogo semilla; fuera de v1 |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Esquema SQLite v1 y contrato de almacén | Pendiente |


