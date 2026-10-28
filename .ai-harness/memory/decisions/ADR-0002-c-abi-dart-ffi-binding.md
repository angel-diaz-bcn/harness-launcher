# ADR-0002 — Binding de libtorrent: ABI C + `dart:ffi`

- **Estado:** accepted
- **Fecha:** 2026-10-24
- **Autor:** Architecture
- **Sustituye a:** —
- **Desarrolla:** [`ADR-0001`](ADR-0001-libtorrent-runtime.md) (dejaba el binding abierto)
- **Specs afectadas:** `CMP-05` (P2P Engine), `CMP-06` (Media Player)

## Contexto

`ADR-0001` decidió embeber libtorrent en proceso, pero dejó abierto el mecanismo de enlace: canal de plataforma/JNI, `dart:ffi` o `libtorrent4j`. El spike `S0` compiló libtorrent 2.1.2 para `android-x86_64` y `android-arm64-v8a`; `S0b` añadió un shim con ABI C y lo ejercitó desde Dart en el AVD `FLIK_TV`.

## Decisión

El adaptador nativo se expone mediante **funciones con ABI C** (`extern "C"`), compiladas en `libflik_p2p.so`, y se consume desde Dart con **`dart:ffi`** y `package:ffi` exclusivamente para conversión de cadenas.

Consecuencias de forma:

1. El shim C es la única superficie nativa; libtorrent queda enlazado estáticamente (`libtorrent-rasterbar.a`) dentro del `.so`.
2. El código Dart del adaptador vive en `lib/features/p2p_engine/data/native/flik_p2p_ffi.dart` y no expone `Pointer` fuera de esa carpeta.
3. El `.so` se empaqueta por ABI en `jniLibs` de Android y, en escritorio, junto al ejecutable.
4. Se prohíbe `JNI` y `libtorrent4j`: obligarían a un segundo adaptador solo para Android.

## Evidencia (S0b, 2026-10-24)

Ejecutado en `FLIK_TV` (Android TV API 36, x86_64, 2 GB), APK debug con `libflik_p2p.so` en `jniLibs/x86_64`:

```
libtorrent=2.1.2.0
selftest=0
cycles10=0
{"ok":true,"name":"Sintel","files":11,"bytes":129302391,
 "metadataMs":2043,"havePiece0":true,"firstPieceBytes":131072,
 "firstBytesHex":"0a310a30","pieceMs":526}
readFirst=4096
httpStatus=206 contentRange=bytes 0-1023/4096 bytes=1024 firstBytesHex=0a310a30
```

| Medición | Valor |
|---|---|
| Metadatos de un magnet legal | 2 043 ms |
| Primera pieza (128 KiB) descargada y leída | 526 ms |
| `Range: bytes=0-1023` sobre bytes del torrent | `206`, 1 024 bytes, `Content-Range: bytes 0-1023/4096` |
| Ciclos de sesión crear/destruir | 10 sin fallo |
| `.so` stripped | 4,28 MB (x86_64) / 4,26 MB (arm64-v8a) |
| APK debug completo | 83,21 MB (incluye motor Flutter debug) |
| RSS del proceso en la prueba | 337 MB (build debug; no representativo de release) |
| Licencias | libtorrent BSD-3, try_signal BSD-3, Boost BSL-1.0 |

## Alternativas descartadas

| Alternativa | Motivo |
|---|---|
| JNI / canal de plataforma | Solo Android; obligaría a mantener dos adaptadores (Android y escritorio). |
| `libtorrent4j` | Añade una capa Java y limita el enlace a Android. |
| Proceso daemon + HTTP interno | Viola `FM-FLIK-001` y añade un proceso que gestionar. |

## Consecuencias

- Un único shim C sirve para Android, Windows, macOS y Linux.
- Hay que construir y empaquetar el `.so` por plataforma y ABI; el pipeline de build pasa a ser parte del producto.
- Los errores del shim se traducen a `P2pFailure`; el shim nunca expone códigos de libtorrent.
- Sin TLS activado (`encryption=OFF`): los trackers/peers HTTPS no funcionan todavía (`R-7`). Se resolverá en una ADR posterior si el producto los exige.
- `dart:ffi` obliga a usar `Pointer` y a liberar memoria manualmente: se confina en `data/native/` y se cubre con pruebas.

## Invariantes respetadas

- `architecture_rules.md` §4.1 (sin backend), §4.2 (loopback), §4.3 (`206`), §4.4 (secuencial), §4.5 (búfer acotado), §4.10 (liberación determinista).
- `security_privacy.md` `SEC-01`–`SEC-05`, `SEC-09`, `SEC-10`.
- `FM-FLIK-006` (nada de trabajo nativo en el isolate de UI: la llamada se ejecuta con `Isolate.run`).
