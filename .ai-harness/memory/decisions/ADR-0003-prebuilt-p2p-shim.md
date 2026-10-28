# ADR-0003 — Binarios del shim P2P precompilados por ABI

- **Estado:** accepted
- **Fecha:** 2026-10-24
- **Autor:** Architecture
- **Specs afectadas:** `CMP-05` (P2P Engine), `CMP-06` (Media Player)

## Contexto

`ADR-0002` fijó un shim con ABI C (`android/app/src/main/cpp/p2p_engine/`) enlazado
estáticamente con libtorrent. Compilar libtorrent dentro de cada build de la app
exigiría versionar o descargar ~200 MB de libtorrent + Boost y añadir varios
minutos por ABI; el proyecto no tiene todavía pipeline nativo ni CI.

## Decisión

1. El `.so` del shim (`libflik_p2p.so`) se **precompila con un script reproducible**
   (`build_shim.ps1`) y se **versiona** en `android/app/src/main/jniLibs/<abi>/`.
2. El build de Flutter **no compila** libtorrent: empaqueta el binario ya presente.
3. Versiones fijadas: libtorrent `2.1.2`, Boost `1.92.0` (headers), NDK `28.2.13676358`,
   `android-24`, ABIs `x86_64` y `arm64-v8a`.
4. Cualquier cambio de versión de libtorrent/Boost obliga a recompilar **ambas**
   ABIs, actualizar el tamaño documentado y repetir el smoke de `FLIK_TV`.
5. Escritorio (Windows/macOS/Linux) queda fuera de esta decisión: se resolverá
   con el mismo shim y un build por plataforma cuando se aborde `CMP-06`.

## Evidencia (smoke 2026-10-24, con el código del repo)

APK debug con el paquete `flik` como dependencia de path y el `.so` en `jniLibs`,
ejecutado en `FLIK_TV`:

```
streamUrl=http://127.0.0.1:44107/stream
infoHash=08ada5a7a6183aae1e09d831df6748d566095a10
fileIndex=5                       # Sintel/Sintel.mp4 elegido automáticamente
fileLength=129241752
http=206
contentRange=bytes 0-1023/129241752
bytes=1024
hex=00000020                      # cabecera ftyp del MP4 real
peers=36  rate=1394735  progress=0.124
closed=closed
```

| Artefacto | Tamaño |
|---|---|
| `libflik_p2p.so` x86_64 (stripped) | 4,29 MB |
| `libflik_p2p.so` arm64-v8a (stripped) | 4,26 MB |
| APK debug completo | 83,25 MB |

## Alternativas descartadas

| Alternativa | Motivo |
|---|---|
| Compilar libtorrent en cada build (CMake/NDK) | Requiere cientos de MB de fuentes y minutos por ABI; sin CI nativo todavía. |
| Descargar binarios en tiempo de build | Build dependiente de red y de un servidor externo; rompe la reproducibilidad. |
| Submódulo con libtorrent y Boost | Mismo coste de compilación, más superficie de mantenimiento. |

## Consecuencias

- Repositorio +8,6 MB de binarios, aceptable frente a la alternativa.
- Build de la app rápido y offline.
- Riesgo de binario obsoleto si se olvida recompilar: el `README.md` del shim lo
  documenta y el número de versión de libtorrent se expone en `flik_p2p_version()`.
- Obligación de mantener el aviso de licencias (libtorrent BSD-3, Boost BSL-1.0).
- CI no reconstruye el binario todavía; queda como `Q-06` en `CMP-05`.

## Invariantes respetadas

- `architecture_rules.md` §4.1–§4.5 y §4.10.
- `security_privacy.md` §5 (licencias) y `SEC-10` (dependencias fijadas).
- `FM-FLIK-013` (revisión de licencias antes de distribuir).
