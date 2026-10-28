# FLIK — Catálogo de Modos de Fallo

Memoria persistente de errores que no deben repetirse. Cada entrada tiene síntoma, riesgo, regla de prevención y verificación.

---

## FM-FLIK-001 — Backend o proxy encubierto

- **Síntoma:** aparece un servicio intermedio, un proxy de vídeo, una CDN propia o una API de reproducción.
- **Riesgo:** rompe el modelo 100 % client-side y añade coste, latencia y superficie de ataque.
- **Prevención:** todo vídeo va de P2P a `127.0.0.1:8888/stream` y de ahí al player.
- **Verificación:** `preflight` bloquea URLs/proveedores de backend en `lib/`.

## FM-FLIK-002 — Descarga completa antes de reproducir

- **Síntoma:** el reproductor espera a que el torrent termine o descarga el archivo entero.
- **Riesgo:** arranque lento, consumo de disco y mala experiencia en TV.
- **Prevención:** prioridad secuencial de cabeceras y primeros megabytes; reproducción en cuanto el flujo es válido.
- **Verificación:** prueba de integración con `Range` y arranque antes de completar el torrent.

## FM-FLIK-003 — Búfer sin evicción

- **Síntoma:** memoria o disco crecen durante la reproducción.
- **Riesgo:** cierre por OOM o almacenamiento lleno en Android TV.
- **Prevención:** búfer de anillo con límite y evicción de piezas ya vistas.
- **Verificación:** prueba de sesión larga con límite de capacidad.

## FM-FLIK-004 — Endpoint fuera de loopback o sin 206

- **Síntoma:** el servidor escucha en `0.0.0.0`, no responde `206` o no soporta `Range`.
- **Riesgo:** exposición en LAN y seeking roto.
- **Prevención:** bind a `127.0.0.1`, token de sesión y soporte explícito de `Range`.
- **Verificación:** `preflight` + test `bytes=0-1024` → `206`.

## FM-FLIK-005 — Fuga de sockets, puerto o procesos

- **Síntoma:** cerrar el reproductor deja el puerto 8888 ocupado o procesos nativos vivos.
- **Riesgo:** siguientes sesiones fallan y el dispositivo consume recursos.
- **Prevención:** cierre determinista de player, servidor, sockets y runtime.
- **Verificación:** abrir/cerrar sesión N veces y comprobar que el puerto queda libre.

## FM-FLIK-006 — Bloqueo del isolate de UI

- **Síntoma:** la interfaz se congela durante la descarga, el parseo o la decodificación.
- **Riesgo:** la app parece rota y el D-Pad no responde.
- **Prevención:** trabajo pesado fuera del isolate de UI; operaciones acotadas y cancelables.
- **Verificación:** test de latencia de entrada durante carga.

## FM-FLIK-007 — Foco atrapado o control inalcanzable

- **Síntoma:** un control solo se activa con ratón/táctil o el foco no puede salir de una zona.
- **Riesgo:** la app es inutilizable en TV.
- **Prevención:** todo control interactivo con `FocusNode`/`FocusScope` y orden D-Pad probado.
- **Verificación:** widget test de recorrido completo con `Up/Down/Left/Right/Select`.

## FM-FLIK-008 — Telemetría o datos de usuario

- **Síntoma:** se añade analítica, crash reporting remoto o envío de historial.
- **Riesgo:** viola la privacidad por diseño y la promesa del producto.
- **Prevención:** cero SDKs de analítica; logs locales y efímeros.
- **Verificación:** `preflight` bloquea dependencias y endpoints de telemetría.

## FM-FLIK-009 — Publicación Git no autorizada

- **Síntoma:** `git push` o publicación automática sin instrucción del usuario.
- **Riesgo:** contaminar el remoto.
- **Prevención:** publicar solo bajo petición explícita y tras `preflight`.
- **Verificación:** revisión del workflow `run_git_publish.md`.

## FM-FLIK-010 — Deriva spec ↔ código

- **Síntoma:** el código añade campos, estados, reglas o estilos que no están en la spec.
- **Riesgo:** documentación falsa y comportamiento impredecible.
- **Prevención:** mapa de implementación, IDs `FR/ST`, comentarios `/// Spec:` y `sync-sdd`.
- **Verificación:** `sync-sdd` y revisión de spec en el mismo cambio.

## FM-FLIK-011 — Colores o estilos hardcodeados

- **Síntoma:** `Color(0xFF...)`, HEX o estilos fuera del sistema de diseño.
- **Riesgo:** inconsistencia visual y dificultad de mantener TV/móvil/escritorio.
- **Prevención:** solo tokens de `ui-design-system.md`.
- **Verificación:** `preflight` de tokens.

## FM-FLIK-012 — Magnet o ruta maliciosa

- **Síntoma:** nombres de archivo con `..`, rutas absolutas, enlaces o torrents anómalos.
- **Riesgo:** escritura fuera del directorio de sesión o consumo de recursos.
- **Prevención:** validar magnet, confinar rutas y limitar tamaño/número de archivos.
- **Verificación:** tests con fixtures maliciosos.

## FM-FLIK-013 — Dependencia no redistribuible

- **Síntoma:** se añade una librería sin revisar su licencia.
- **Riesgo:** incumplimiento legal al distribuir la app.
- **Prevención:** revisar licencias de `media_kit`, MPV/FFmpeg y runtime P2P antes de empaquetar.
- **Verificación:** checklist de licencias en `security_privacy.md`.
