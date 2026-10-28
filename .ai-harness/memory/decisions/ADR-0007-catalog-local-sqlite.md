# ADR-0007 — Persistencia local del catálogo con SQLite/Drift

- **Estado:** accepted
- **Fecha:** 2026-10-26
- **Autor:** Architecture
- **Specs afectadas:** `CMP-02` (Catalog Repository), `CMP-03` (Catalog Local Store), `CMP-04` (Catalog Seed), `PRC-02` (Catalog Ingest). `CMP-01` no cambia.

## Contexto

`CMP-01` define y valida el documento JSON del catálogo (hasta 20 000 ítems, 50 variantes por ámbito, 50 temporadas, 500 episodios por temporada), pero hoy no existe persistencia: `pubspec.yaml` solo declara `shared_preferences`.

La Home (`CMP-12`) necesita raíles derivados por `tags`, `genres`, `kind` y `rating`, con límite de 20 ítems por fila y sin materializar el catálogo completo en memoria (`architecture_rules.md` §6). La Categoría futura necesitará facetas y paginación. El arranque debe servir datos de caché sin bloquear por red (invariante 8), y Android TV impone presión de memoria y almacenamiento (`FM-FLIK-003`).

`block_catalog_service.md` fija que el motor de persistencia se decide en una ADR: Hive o SQLite.

## Decisión

1. Se usa **SQLite** como almacén local del catálogo, con el paquete **`drift`** como capa tipada.
2. Dependencias de producción: `drift`, `path_provider` y `sqlite3` (transitiva con assets nativos propios). Dependencias de desarrollo: `drift_dev`, `build_runner`. Las versiones se fijan en `pubspec.yaml` al implementar y se validan con `flutter pub get`; licencias esperadas MIT/BSD/Apache-2.0, revisadas contra `FM-FLIK-013` antes de distribuir. **`sqlite3_flutter_libs` queda excluido**: con `sqlite3` 3.x es un paquete obsoleto que no aporta binarios.
3. La base de datos vive en el directorio de soporte de la aplicación (`getApplicationSupportDirectory()`), archivo `catalog.sqlite`. La ruta es inyectable para pruebas (`NativeDatabase.memory()`).
4. El esquema se versiona con `schemaVersion = 1` y estrategia de migración explícita. Al detectar una versión desconocida se recrea el esquema, porque el catálogo es dato derivado y siempre se puede reingestar desde la fuente semilla.
5. La ingesta se ejecuta en **una única transacción**: si falla cualquier paso, se hace rollback y se conserva el catálogo válido anterior.
6. **No se almacenan imágenes** en la base de datos. Solo se persisten URIs (`asset:` o `http(s)`) y, en su defecto, `NULL`, que la UI resuelve con un placeholder del sistema de diseño.
7. Todo el acceso a SQLite vive en `lib/features/catalog/`. `tv_experience` solo consume la API pública del catálogo y nunca importa `drift` ni abre la base de datos.
8. La tabla de progreso de visualización se reserva para la fase F2.5 y **no** forma parte del esquema v1.

## Alternativas descartadas

| Alternativa | Motivo |
|---|---|
| `shared_preferences` o JSON completo en disco | No permite filtrar, ordenar ni paginar sin materializar 20 000 ítems; rompe `architecture_rules.md` §6. |
| Hive | Almacén clave-valor sin consultas ni índices por género/tag; obligaría a cargar colecciones enteras. |
| `sqflite` | No cubre Windows, macOS ni Linux sin plugins adicionales; FLIK es multiplataforma. |
| Isar | Menor actividad de mantenimiento y menor garantía de soporte en las cinco plataformas objetivo. |
| Backend o servicio remoto de catálogo | Prohibido por las invariantes 1 y 9 (`architecture_rules.md` §4). |

## Consecuencias

- Se añaden dos dependencias de producción, dos de desarrollo y un paso de generación de código (`dart run build_runner build --delete-conflicting-outputs`).
- Los tests usan SQLite en memoria; no requieren red ni ficheros reales.
- `flutter analyze` y `flutter test` necesitan el SDK de Flutter disponible; en este equipo está en `C:\Users\angel\Documents\DEV\.tools\flutter\bin`.
- En Windows, `flutter pub get`/`flutter run` exigen **Modo para desarrolladores** activado para crear symlinks de plugins. `dart pub get` y `flutter test --no-pub` funcionan sin activarlo.
- El catálogo deja de depender de la red para pintar la Home: la primera pantalla se sirve desde SQLite.
- El esquema v1 no cubre progreso, colecciones ni carátulas descargadas; esas ampliaciones exigirán migración de esquema y su propia actualización de specs.

## Invariantes respetadas

- `architecture_rules.md` §4.8: catálogo offline-first, la red nunca bloquea el arranque.
- `architecture_rules.md` §4.9: cero telemetría; la base de datos es estrictamente local.
- `architecture_rules.md` §6: catálogo paginado y recursos acotados.
- `FM-FLIK-003`: ninguna caché crece sin límite ni política de evicción declarada.
- `FM-FLIK-010`: toda la persistencia queda especificada en `CMP-02`, `CMP-03`, `CMP-04` y `PRC-02`.
- `FM-FLIK-013`: licencias de dependencias revisadas antes de distribuir.
