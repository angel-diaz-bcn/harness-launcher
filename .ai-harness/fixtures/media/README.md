# Fixtures de Medios

Aquí se colocan archivos MKV/MP4 cortos y redistribuibles para:

- probar apertura y seeking;
- probar cambio de pistas de audio/subtítulo;
- probar fallback de decodificación;
- probar rangos HTTP contra el servidor local.

Requisitos:

- Duración corta (segundos, no minutos).
- Sin DRM.
- Sin contenido con derechos.
- Nombres estables: `sample.mkv`, `sample.mp4`.
- Documentar códecs y pistas en la spec del reproductor.
