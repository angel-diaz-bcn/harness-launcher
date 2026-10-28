# ADR-0004 — `media_kit`/MPV: tamaño, licencias y empaquetado

- **Estado:** accepted
- **Fecha:** 2026-10-24
- **Autor:** Architecture
- **Specs afectadas:** `CMP-06` (Media Player), `PRC-01` (Magnet playback)

## Contexto

`CMP-06` necesita reproducir el flujo local de `CMP-05`. Se eligió `media_kit` (MIT) con
`media_kit_video` y `media_kit_libs_video`, que en Android descarga binarios
precompilados de **libmpv** (`media-kit/libmpv-android-video-build`, `v1.1.7`) desde
GitHub durante el build.

Eso introduce dos riesgos del arnés: tamaño del APK y licencias de MPV/FFmpeg
(`FM-FLIK-013`, `security_privacy.md` §5).

## Decisión

1. Se usa `media_kit` `1.2.6`, `media_kit_video` `2.0.1` y `media_kit_libs_video` `1.0.7`,
   con versiones **fijadas** en `pubspec.yaml`.
2. El adaptador real vive en `lib/features/player/data/media_kit/media_kit_adapter.dart`;
   ningún otro archivo de la app importa `media_kit`.
3. Para distribución se usa **APK por ABI** (`--split-per-abi`) y se excluye
   `armeabi-v7a` si no hay dispositivos objetivo, porque las libs de MPV se empaquetan
   para todas las ABIs presentes.
4. Antes de publicar hay que añadir el aviso de terceros con MPV/FFmpeg y revisar si la
   build de libmpv elegida es GPL o LGPL. **No se distribuye todavía.**
5. El build nativo de Android requiere red la primera vez (descarga de los jars de libmpv
   con MD5 fijado por el paquete). Se acepta como dependencia de build documentada.

## Medición (2026-10-24, APK debug `android-x64`)

| Métrica | Valor |
|---|---|
| APK debug total | **143,46 MB** |
| `lib/x86_64/libflutter.so` (debug) | 38,25 MB |
| `lib/x86_64/libmpv.so` | **15,08 MB** |
| `lib/x86_64/libflik_p2p.so` | 4,29 MB |
| `lib/x86_64/libmediakitandroidhelper.so` | 0,35 MB |
| Nativo `arm64-v8a` | 16,43 MB |
| Nativo `armeabi-v7a` | 11,48 MB |
| Nativo `x86_64` | 57,97 MB |

El APK debug incluye las tres ABIs y el motor Flutter de depuración; en release por ABI
el tamaño será sensiblemente menor (libmpv ~15 MB + P2P ~4,3 MB + Flutter release).

## Licencias

| Componente | Licencia declarada | Nota |
|---|---|---|
| `media_kit` / `media_kit_video` | MIT | Wrapper Dart/Flutter |
| `media_kit_libs_android_video` | MIT (paquete) | Solo empaqueta binarios |
| **libmpv / MPV** | **GPLv2+ por defecto** (build `default`) | Obliga a revisar distribución y código fuente |
| **FFmpeg** (incluido en la build de MPV) | LGPL/GPL según configuración | Verificar flags de la build `default` |

**Conclusión:** el empaquetado actual **no es apto para distribución comercial** sin
resolver la licencia de MPV/FFmpeg. Opciones: usar una build LGPL de libmpv, publicar el
código conforme a GPL, o cambiar de motor. Queda como bloqueo de release, no de
desarrollo.

## Alternativas descartadas

| Alternativa | Motivo |
|---|---|
| `video_player` (ExoPlayer) | No soporta MKV/HEVC de forma consistente ni el control de pistas requerido. |
| MPV embebido a mano | Repetiría el trabajo de `media_kit` y su empaquetado por plataforma. |
| Excluir `media_kit` del MVP | Deja el producto sin imagen. |

## Consecuencias

- El build de Android necesita red la primera vez.
- El APK crece; obligatorio `--split-per-abi` en release.
- Riesgo legal abierto hasta elegir build LGPL o publicar bajo GPL.
- El adaptador aísla el resto de la app: cambiar de motor solo afecta a `data/media_kit/`.
