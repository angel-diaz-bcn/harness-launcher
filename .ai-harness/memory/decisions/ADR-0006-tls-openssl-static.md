# ADR-0006 — TLS en el motor P2P con OpenSSL estático

- **Estado:** accepted
- **Fecha:** 2026-10-24
- **Specs afectadas:** `CMP-05` (`Q-04`, `FR-01`, `FR-15`)

## Contexto

El catálogo de dominio público usa *web seeds* HTTPS. Con `xs=` la sesión abría y
los metadatos llegaban, pero la lectura devolvía 0 bytes (`slow read ... got=0`,
`peers=0`): `libtorrent` se compilaba con `-Dencryption=OFF` y sin OpenSSL.

Compilar OpenSSL desde fuente no es viable en este equipo: no hay `make` POSIX,
`perl` funcional ni WSL, y el `Configure` de OpenSSL exige ambos.

## Decisión

1. Usar los binarios estáticos de **OpenSSL 3.1.8** publicados por
   [`KDAB/android_openssl`](https://github.com/KDAB/android_openssl) (`ssl_3`,
   `x86_64` y `arm64-v8a`), fijados por commit y verificados con `llvm-nm`.
2. Reconfigurar `libtorrent` con `-Dencryption=ON -Dgnutls=OFF` y enlazar
   `libssl.a`/`libcrypto.a` en el shim (`build-shim.ps1`).
3. Reconstruir `libflik_p2p.so` para cada ABI.

## Consecuencias

- TLS queda disponible para trackers y web seeds HTTPS; el enlace es estático, así
  que la app no necesita `.so` adicionales.
- `libflik_p2p.so` pasa de **4,29 MB a 9,90 MB** por ABI (stripped). El APK de
  debug sigue en ~145 MB; la release debe usar `--split-per-abi`.
- El build nativo depende ahora de un artefacto de terceros: queda registrada su
  procedencia, licencia (Apache-2.0) y la alternativa de compilarlo en CI Linux.

## Evidencia (2026-10-24, `FLIK_PHONE_30`)

```
FLIK_PLAY playing pos=8s dur=5796s peers=1 progress=0.02
FLIK_SRV slow read at 13828572 (840ms) got=262144
FLIK_SRV slow read at 17825792 (878ms) got=262144
```

`dur=5796s` corresponde a la película de dominio público de 96 min; los rangos
lejanos son el `moov` al final del MP4, servido por el web seed HTTPS.

## Alternativa descartada por ahora

Compilar OpenSSL con el NDK desde fuente en Windows (frágil) o depender de
`make`/WSL. En CI Linux es la opción preferida y sustituiría a los binarios
precompilados sin cambiar el código.
