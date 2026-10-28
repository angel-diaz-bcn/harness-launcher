# CMP-04 — Catalog Seed

---
spec_id: CMP-04
spec_type: CMP
layer: backend
name: Catalog Seed
target: lib/features/catalog/data/seed/seed_catalog_source.dart
block: catalog
status: APPROVED
version: 1.0
owner: Architecture
last_reviewed: 2026-10-26
approved_at: 2026-10-26
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-02]
depends_on: [CMP-01]
consumed_by: [PRC-02]
---

`CMP-04` · `v1.0` · `catalog` · `Dart` · `DRAFT`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `catalog` | `lib/features/catalog/data/seed/seed_catalog_source.dart` |

> [!IMPORTANT]
> **Origen semilla del catálogo.** Lee un asset del bundle y lo valida con `CMP-01`. No escribe en la base de datos ni conoce SQLite: eso pertenece a `PRC-02`.

> [!WARNING]
> **Fuera de alcance:** catálogos remotos, edición manual, descarga o generación de carátulas y cualquier acceso a red.

> [!TIP]
> **Ruta de lectura:** §4 requisitos → §8 contratos → §10 trazabilidad.

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

1. Leer esta spec, `CMP-01`, `CMP-03` y `PRC-02`.
2. Implementar solo los `FR-*` y `CT-*` definidos aquí.
3. No añadir fuentes, cachés ni reintentos no especificados.
4. Si falta un dato, registrarlo en §15 y detener la implementación.
5. Actualizar §10 y §11 en el mismo cambio que el código.

**Jerarquía de verdad:** contexto → `ADR-0007` → `CMP-01` → esta spec → código.

---

## 1. Contexto y objetivo

### 1.1 Problema

La base de datos arranca vacía en una instalación nueva. Sin una fuente semilla validada, la Home no tiene contenido y `PRC-02` no tiene entrada que ingerir.

### 1.2 Objetivo medible

Leer `assets/catalogs/flik-seed.json`, validarlo con `CatalogContract.validate` y devolver el `CatalogDocument` completo o un fallo tipado, sin escribir nada y sin red.

### 1.3 No objetivos

- Persistir el catálogo (`PRC-02` + `CMP-03`).
- Sincronizar fuentes remotas.
- Decidir qué filas pinta la Home.
- Aportar imágenes.

---

## 2. Alcance y límites

**Incluye:**

- Lectura del asset declarado en `pubspec.yaml`.
- Validación completa con el contrato `CMP-01`.
- Resultado tipado con documento o errores de contrato.
- Reloj inyectable para pruebas de `generated_at`.

**Excluye:**

- Escritura en base de datos.
- HTTP, red o descarga.
- Caché del texto del asset entre llamadas.
- Corrección o tolerancia de documentos inválidos.

**Invariantes de arquitectura aplicables:**

- `architecture_rules.md` §4.8: offline-first; la semilla no depende de red.
- `architecture_rules.md` §4.9: cero telemetría.
- `FM-FLIK-010`: sin campos ni estados fuera de spec.
- `FM-FLIK-012`: el documento pasa por el contrato antes de cualquier uso.

---

## 3. Actores e historia de usuario

> **Como** sistema de arranque,
> **quiero** una fuente semilla validada incluida en el bundle,
> **para** que la primera pantalla tenga catálogo sin backend ni conexión.

**Actores secundarios:** `PRC-02` (consumidor), `CMP-01` (validador), `CMP-03` (destino).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | La ruta del asset es la constante `kSeedCatalogAssetPath = 'assets/catalogs/flik-seed.json'`. | Must | `AC-01`: ninguna otra ruta se usa en el código | `BR-01` |
| `FR-02` | `load` lee el asset con un `AssetBundle` inyectable; por defecto `rootBundle`. | Must | `AC-02`: test con un bundle falso devuelve el JSON configurado | `BR-02` |
| `FR-03` | El contenido se valida con `CatalogContract.validate(source, now: clock())`. | Must | `AC-03`: un documento inválido devuelve los errores de contrato | `BR-03` |
| `FR-04` | Un documento válido devuelve `SeedCatalogResult` con el `CatalogDocument`, la ruta del asset y la lista de errores vacía. | Must | `AC-04`: `result.document != null` y `result.errors.isEmpty` | `BR-04` |
| `FR-05` | Un asset ausente devuelve `SeedCatalogFailure` con `assetMissing`. | Must | `AC-05`: `FlutterError`/`Exception` de `loadString` → `assetMissing` | `BR-05` |
| `FR-06` | Un error de lectura distinto de ausencia devuelve `SeedCatalogFailure` con `readFailed`. | Must | `AC-06`: bundle que lanza `StateError` → `readFailed` | `BR-05` |
| `FR-07` | Un documento inválido devuelve `SeedCatalogResult` con `document == null` y los `CatalogContractError` recibidos. | Must | `AC-07`: magnet inválido del fixture produce errores con su ruta JSON | `BR-06` |
| `FR-08` | La fuente no modifica el documento: no corrige, no completa ni descarta campos. | Must | `AC-08`: el documento válido es idéntico al que valida `CMP-01` | `BR-07` |
| `FR-09` | La fuente no abre red, no escribe archivos y no accede a SQLite. | Must | `AC-09`: revisión de imports y dependencias | `BR-08` |
| `FR-10` | La llamada es determinista para el mismo asset y el mismo reloj inyectado. | Must | `AC-10`: dos llamadas devuelven el mismo `catalogId` y `generatedAt` | `BR-09` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | Solo existe una ruta de semilla en v1; cambiarla exige actualizar `pubspec.yaml` y esta spec. | Esta spec | `TC-01` |
| `BR-02` | `AssetBundle` es inyectable para pruebas; no se usa `rootBundle` directamente en los tests. | `testing_guidelines.md` | `TC-02` |
| `BR-03` | La validación es obligatoria y completa; no se aceptan documentos parciales. | `CMP-01` `FR-12` | `TC-03` |
| `BR-04` | El resultado expone la ruta del asset para trazabilidad de la ingesta. | `PRC-02` | `TC-04` |
| `BR-05` | Los fallos de lectura se distinguen de los fallos de contrato. | Esta spec | `TC-05` |
| `BR-06` | Los errores de contrato se conservan íntegros, con `code`, `message` y `path`. | `CMP-01` `CT-05` | `TC-06` |
| `BR-07` | La semilla no altera datos para «hacerlos pasar». | `sdd_framework.md` §2 | `TC-07` |
| `BR-08` | Prohibido `http`, `dio`, sockets, `path_provider` y `drift` en esta fuente. | `architecture_rules.md` §4.1 | `TC-08` |
| `BR-09` | El reloj de validación se inyecta para evitar fallos por `generated_at` futuro. | `CMP-01` `BR-13` | `TC-09` |

**Invariantes:**

- `INV-01`: la fuente es de solo lectura.
- `INV-02`: ningún byte sale del dispositivo.
- `INV-03`: un documento inválido nunca se convierte en `CatalogDocument`.

---

## 6. Estados y errores

| ID | Situación | Resultado |
|---|---|---|
| `E-01` | Asset no declarado en `pubspec.yaml` o inexistente | `SeedCatalogFailure(assetMissing)` |
| `E-02` | Error de lectura del bundle | `SeedCatalogFailure(readFailed)` |
| `E-03` | JSON malformado | `SeedCatalogResult` inválido con `CatalogErrorCode.invalidJson` |
| `E-04` | Violación de esquema, magnet, calidad o límites | `SeedCatalogResult` inválido con los errores de `CMP-01` |
| `E-05` | Documento válido | `SeedCatalogResult` con documento |

---

## 7. Datos y transformaciones

| Etapa | Entrada | Salida | Regla |
|---|---|---|---|
| Lectura | `kSeedCatalogAssetPath` | `String` JSON | Sin transformación |
| Validación | `String` JSON + `now` | `CatalogValidationResult` | Delegado en `CatalogContract.validate` |
| Resultado | `CatalogValidationResult` | `SeedCatalogResult` | `document` y `errors` se copian sin cambios |

---

## 8. Contratos

### 8.1 `CT-01` — `kSeedCatalogAssetPath`

```dart
/// Ruta del catálogo semilla incluido en el bundle.
/// Spec: CMP-04 / FR-01
const String kSeedCatalogAssetPath = 'assets/catalogs/flik-seed.json';
```

### 8.2 `CT-02` — `SeedCatalogSource`

```dart
/// Fuente de solo lectura del catálogo semilla.
/// Spec: CMP-04 / FR-02, FR-03, FR-04
final class SeedCatalogSource {
  SeedCatalogSource({AssetBundle? bundle, DateTime Function()? clock})
    : _bundle = bundle ?? rootBundle,
      _clock = clock ?? DateTime.now;

  /// Spec: CMP-04 / FR-02, FR-03, FR-04, FR-05, FR-06, FR-07
  Future<SeedCatalogResult> load();
}
```

### 8.3 `CT-03` — `SeedCatalogResult`

```dart
/// Resultado de cargar y validar la semilla.
/// Spec: CMP-04 / FR-04, FR-07
final class SeedCatalogResult {
  const SeedCatalogResult({
    required this.document,
    required this.assetPath,
    required this.errors,
  });

  final CatalogDocument? document;
  final String assetPath;
  final List<CatalogContractError> errors;

  /// Spec: CMP-04 / FR-04
  bool get isValid => document != null;
}
```

### 8.4 `CT-04` — `SeedCatalogFailure` y `SeedCatalogErrorCode`

```dart
/// Motivos de fallo de lectura de la semilla.
/// Spec: CMP-04 / FR-05, FR-06
enum SeedCatalogErrorCode { assetMissing, readFailed }

/// Error de lectura de la semilla; no cubre documentos inválidos.
/// Spec: CMP-04 / FR-05, FR-06
final class SeedCatalogFailure implements Exception {
  const SeedCatalogFailure({
    required this.code,
    required this.message,
    this.cause,
  });

  final SeedCatalogErrorCode code;
  final String message;
  final Object? cause;

  @override
  String toString() => 'SeedCatalogFailure($code): $message';
}
```

---

## 9. Dependencias y ciclo de vida

### 9.1 Dependencias permitidas

- `flutter/services.dart` únicamente para `AssetBundle` y `rootBundle`.
- `lib/features/catalog/domain/catalog_contract.dart` (`CMP-01`).

### 9.2 Prohibidas

- Red (`http`, `dio`), `drift`, `sqlite3`, `path_provider`.
- Escritura de archivos, telemetría y UI.
- `tv_experience`, `player`, `p2p_engine`.

### 9.3 Ciclo de vida

- **Creación:** en la composición de `lib/app/`, antes de `PRC-02`.
- **Suscripción:** sin streams; una llamada por ingesta.
- **Cancelación:** el `Future` puede ignorarse; no hay recursos abiertos.
- **Destrucción:** sin `dispose`; no retiene buffers ni suscripciones.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `lib/features/catalog/data/seed/seed_catalog_source.dart::kSeedCatalogAssetPath` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogSource.load` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogSource.load` | `TC-03` | Verified |
| `FR-04` | `CT-03` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogResult.isValid` | `TC-04` | Verified |
| `FR-05` | `CT-04` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogSource.load` | `TC-05` | Verified |
| `FR-06` | `CT-04` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogSource.load` | `TC-06` | Verified |
| `FR-07` | `CT-03` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogResult.errors` | `TC-07` | Verified |
| `FR-08` | `CT-03` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogSource.load` | `TC-08`, `TC-11` | Verified |
| `FR-09` | — | `lib/features/catalog/data/seed/seed_catalog_source.dart` (imports) | `TC-09` | Verified |
| `FR-10` | `CT-02` | `lib/features/catalog/data/seed/seed_catalog_source.dart::SeedCatalogSource.clock` | `TC-10` | Verified |

**Estados:** `Pending`, `Implemented`, `Verified`.

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Fixture / entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | `FR-01` | Constante pública | Vale exactamente `assets/catalogs/flik-seed.json` |
| `TC-02` | Unit | `FR-02` | Bundle falso con el fixture válido | Devuelve documento válido |
| `TC-03` | Unit | `FR-03` | Bundle con `invalid-magnet.json` | Errores de contrato con `path` |
| `TC-04` | Unit | `FR-04` | Fixture válido | `isValid == true`, `errors.isEmpty`, ruta correcta |
| `TC-05` | Unit | `FR-05` | Bundle que lanza al buscar el asset | `SeedCatalogFailure.assetMissing` |
| `TC-06` | Unit | `FR-06` | Bundle que lanza `StateError` | `SeedCatalogFailure.readFailed` |
| `TC-07` | Unit | `FR-07` | `invalid-magnet.json` | `document == null` y errores íntegros |
| `TC-08` | Unit | `FR-08` | Fixture válido comparado con `CatalogContract.validate` | Mismos `catalogId`, `generatedAt` e ítems |
| `TC-09` | Unit | `FR-09` | Análisis de imports | Sin `http`, `dio`, `drift`, `path_provider` |
| `TC-10` | Unit | `FR-10` | Reloj fijo inyectado, dos llamadas | Mismo `generatedAt` |
| `TC-11` | Unit | `FR-08` | `assets/catalogs/flik-seed.json` real | 48 ítems válidos (40 películas + 8 series) |

**Comandos:**

- `flutter analyze`
- `flutter test test/unit/catalog/seed_catalog_source_test.dart`

**Prohibido:** `rootBundle` real en tests, red, archivos temporales y temporizadores reales.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-04
Scenario: Cargar la semilla válida
  Given el asset assets/catalogs/flik-seed.json con 48 ítems válidos
  When SeedCatalogSource.load() se ejecuta con un reloj fijo
  Then devuelve SeedCatalogResult con document no nulo
  And errors está vacío
  And assetPath es la ruta canónica
```

```gherkin
@FR-05
Scenario: Semilla ausente en el bundle
  Given un bundle que no contiene el asset semilla
  When SeedCatalogSource.load() se ejecuta
  Then devuelve SeedCatalogFailure con código assetMissing
  And no se genera ningún CatalogDocument
  And PRC-02 puede continuar con el catálogo ya persistido
```

```gherkin
@FR-07
Scenario: Semilla con un magnet inválido
  Given un asset semilla con un magnet malformado
  When SeedCatalogSource.load() se ejecuta
  Then devuelve SeedCatalogResult inválido
  And document es nulo
  And los errores incluyen la ruta JSON del magnet
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` tienen `AC-*`, `TC-*` y entrada en §10.
- [ ] Todos los `CT-*` están implementados y referenciados por código.
- [ ] Los símbolos públicos llevan comentario `/// Spec: CMP-04 / FR-...`.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] El asset está declarado en `pubspec.yaml` y existe en el bundle.
- [ ] No hay placeholders ni secciones vacías.
- [ ] §15 no tiene preguntas bloqueantes.
- [ ] La spec está en `APPROVED` y `sync-sdd` no reporta `DIVERGED`.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-26 | Spec aprobada e implementada | Semilla real de 48 ítems validada contra `CMP-01` | Todos los `FR` | Product Owner |
| 2026-10-26 | Una única semilla `assets/catalogs/flik-seed.json` | MVP sin red ni gestor de fuentes | `FR-01` | Producto |
| 2026-10-26 | Los documentos inválidos devuelven resultado, no excepción | `PRC-02` necesita distinguir lectura de validación | `CT-03`, `FR-07` | Architecture |
| 2026-10-26 | El asset se entrega sin carátulas ni backdrops | El usuario aportará las imágenes después | Alcance | Producto |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿La semilla se actualizará por asset o por fuente remota en F3? | No | Producto | Se decidirá con `PRC-02` v2 |
| `Q-02` | ¿Se admite más de una semilla por espacio? | No | Producto | v1 usa un único espacio implícito |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Fuente semilla validada sin red | Pendiente |




