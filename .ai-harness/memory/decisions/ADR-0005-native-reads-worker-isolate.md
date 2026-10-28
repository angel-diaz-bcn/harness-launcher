# ADR-0005 — Lecturas nativas en isolate trabajador

- **Estado:** accepted
- **Fecha:** 2026-10-24
- **Specs afectadas:** `CMP-05` (P2P Engine), `PRC-01`

## Contexto

`flik_p2p_read` es una llamada nativa bloqueante: espera piezas y alertas de libtorrent
hasta 20 s. En el primer smoke con el reproductor, MPV entraba en `playing` pero la
posición se quedaba en 0 y el propio `HEAD` de autoprueba no respondía: el servidor HTTP
y la UI compartían el isolate bloqueado por la lectura nativa.

## Decisión

`FlikP2pWorkerSource` ejecuta **todas** las llamadas nativas (open, select, prioritize,
read, stats, close) en un isolate dedicado, con un protocolo de mensajes
(`[id, op, args]` → `[id, ok, payload]`). La UI y el `HttpServer` solo hacen `await` de
`Future`s.

## Consecuencias

- El isolate de UI nunca se bloquea (`FM-FLIK-006`, `BR-08`).
- Las lecturas se serializan en el trabajador; es el orden correcto para el shim.
- `FlikP2pSource` (bindings directos) se conserva solo para tests unitarios.

## Evidencia (smoke 2026-10-24, `FLIK_TV`)

```
FLIK_HTTP HEAD 200 len=129241752 accept=bytes type=video/mp4
FLIK_HTTP GET 206 range=bytes 0-1023/129241752 bytes=1024 hex=00000020
FLIK_PLAY playing pos=7s dur=888s peers=11 progress=0.98
```

Antes del cambio, el mismo escenario daba `pos=0s dur=0s` y ningún `HEAD` servido.
