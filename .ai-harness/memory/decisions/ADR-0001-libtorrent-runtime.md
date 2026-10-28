# ADR-0001 — Runtime P2P nativo basado en libtorrent

- **Estado:** accepted
- **Fecha:** 2026-10-24
- **Autor:** Architecture
- **Specs afectadas:** `CMP-05` (P2P Engine), `CMP-06` (Media Player), `PRC-01` (Magnet playback)

## Contexto

FLIK debe convertir un enlace magnet en un flujo HTTP local reproducible y seekable en `http://127.0.0.1:8888/stream` con `206 Partial Content` ([`architecture_rules.md` §4](../../context/architecture_rules.md)). Hoy no existe ningún runtime P2P en el proyecto: `lib/features/p2p_engine/` está vacío y `pubspec.yaml` no declara dependencias de producto.

Restricciones que condicionan la decisión:

- 100 % client-side: prohibido daemon externo, backend o servicio remoto (`FM-FLIK-001`).
- Descarga secuencial con prioridad de cabeceras, nunca el archivo completo antes de reproducir (`FM-FLIK-002`).
- Búfer acotado con evicción en Android TV con 2 GB de RAM (`FM-FLIK-003`).
- Endpoint exclusivamente en loopback, con token de sesión y puerto verificado (`SEC-01`, `SEC-02`, `SEC-03`).
- UPnP desactivado por defecto; DHT configurable (`SEC-09`).
- Licencia redistribuible y binarios por plataforma antes de empaquetar (`FM-FLIK-013`, `security_privacy.md` §5).
- Host de desarrollo: Windows 11 sin workload C++ de Visual Studio; emulador Android TV `FLIK_TV` (API 36, **x86_64**, 2 GB) disponible.

## Decisión

1. **Motor:** se embebe **libtorrent** como runtime BitTorrent del producto, **en proceso**, sin daemon ni CLI externa.
2. **Ubicación:** el código nativo y su adaptador viven solo en `lib/features/p2p_engine/data/native/` y en las carpetas nativas por plataforma autorizadas por `block_p2p_engine.md`.
3. **Enlace con Dart:** el *binding* concreto (canal de plataforma/JNI o `dart:ffi`) **no se fija en esta ADR**. Se decide con la evidencia del spike **S0** y, si difiere de lo previsto, se registra en `ADR-0002` sin reescribir esta.
4. **Sin paquete de terceros asumido:** no se declara ninguna dependencia de pub.dev para P2P hasta que S0 verifique que existe, compila y cumple los criterios de abajo.
5. **Política de red por defecto:** UPnP desactivado, sin exposición del puerto 8888 fuera de `127.0.0.1`, DHT activa salvo configuración en contra.

## Alternativas evaluadas

| Alternativa | Motivo de descarte |
|---|---|
| Cliente WebTorrent sobre JS embebido | Añade una VM JS al proceso, complica el control de memoria y el acceso a piezas en TV; el mapeo a `Range`/`206` queda fuera de nuestro control. |
| Cliente BitTorrent en Dart puro | No hay evidencia de madurez para streaming secuencial, DHT y verificación de piezas; riesgo alto de reimplementar el protocolo. |
| Daemon o CLI externa (transmission, aria2) | Viola `FM-FLIK-001` y el scope: proceso separado y dependencia de binarios del sistema. |
| Backend/proxy que sirva el vídeo | Prohibido por las invariantes del producto. |

## Consecuencias

**Ventajas**

- Motor maduro con selección de piezas, prioridades y lectura por rangos: encaja con streaming secuencial y seeking.
- Un único motor para Android, Windows, macOS y Linux (con compilación por plataforma).
- Control total del ciclo de vida: sesión, límites, cierre y liberación de memoria.

**Costes y riesgos**

| ID | Riesgo | Mitigación |
|---|---|---|
| `R-1` | Compilación nativa por plataforma (NDK/CMake/Boost) y ABI: arm64-v8a, armeabi-v7a y **x86_64** para el emulador | S0 compila y ejecuta en `FLIK_TV`; si x86_64 no es viable, la primera prueba pasa a un dispositivo ARM real |
| `R-2` | Tamaño del APK y de los binarios | Compilar solo ABIs objetivo, enlazado dinámico y `strip`; medir en S0 |
| `R-3` | Consumo de memoria en Android TV | Límite de caché explícito y evicción (`FM-FLIK-003`); medir RSS en S0 |
| `R-4` | Inestabilidad del binding (JNI/FFI) y cierres sucios | Aislar el adaptador, traducir todo error nativo a error tipado, prueba de abrir/cerrar N veces |
| `R-5` | Bloqueo del isolate de UI | Todo el trabajo nativo fuera del isolate de UI (`FM-FLIK-006`) |
| `R-6` | Licencias y atribución (libtorrent, Boost, OpenSSL y dependencias transitivas) | Verificar licencias y generar aviso de terceros antes de distribuir (`FM-FLIK-013`) |

## Criterios de verificación (spike S0, previo a implementar `CMP-05`)

S0 es un prototipo **desechable**: no se integra en `lib/` ni cuenta como implementación.

1. Compila el runtime para `android-x86_64` y `android-arm64-v8a`.
2. Abre un magnet legal y resuelve metadatos en menos de 30 s con red disponible.
3. Sirve `Range: bytes=0-1023` y responde `206` con `Content-Range` y bytes exactos.
4. Cierra la sesión y el puerto 8888 queda libre; repetir 10 ciclos sin fugas.
5. Registra RSS pico y tamaño de artefacto por ABI.
6. Confirma licencias y genera la lista de atribuciones.
7. Documenta el binding elegido y sus motivos.

Si S0 no cumple los criterios 1–4, esta ADR queda `superseded` por `ADR-0002` con la alternativa viable.

## Invariantes respetadas

- `architecture_rules.md` §4.1 (sin backend), §4.2 (loopback único), §4.3 (`206` obligatorio), §4.4 (secuencial), §4.5 (búfer de anillo), §4.10 (liberación determinista).
- `security_privacy.md` `SEC-01`, `SEC-02`, `SEC-03`, `SEC-05`, `SEC-09`, `SEC-10` y §5 (licencias).
- `platform_matrix.md` §2 (memoria y almacenamiento en Android TV).
