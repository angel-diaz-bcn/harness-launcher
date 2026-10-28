# FLIK — Seguridad, Privacidad y Límites de Confianza

FLIK descarga contenido de una red P2P y lo sirve en un endpoint HTTP local. Esa combinación exige un modelo de amenazas explícito.

---

## 1. Activos a proteger

- El dispositivo del usuario y sus archivos.
- La red local y el endpoint `127.0.0.1`.
- La biblioteca, el progreso y las preferencias locales.
- Las fuentes de catálogo y sus credenciales, si existen.
- La reputación y la integridad del contenido descargado.

---

## 2. Amenazas principales

| ID | Amenaza | Control obligatorio |
|---|---|---|
| `SEC-01` | Endpoint local accesible desde la red | Bind exclusivo a `127.0.0.1`; prohibido `0.0.0.0` o interfaces LAN |
| `SEC-02` | Otro proceso local consume el stream | Token de sesión por reproducción, comparado en tiempo constante |
| `SEC-03` | Conflicto o secuestro del puerto 8888 | Verificar disponibilidad; fallar de forma explícita; no reutilizar una sesión ajena |
| `SEC-04` | Path traversal desde nombres de archivo del torrent | Normalizar y confinar rutas a un directorio de sesión; rechazar `..`, rutas absolutas y enlaces |
| `SEC-05` | Magnet o torrent malicioso | Validar info-hash, tamaño, número de archivos y metadatos antes de abrir |
| `SEC-06` | Archivo de vídeo corrupto o malicioso | Ejecutar MPV/FFmpeg actualizados; no confiar en el contenedor; aislar fallos |
| `SEC-07` | Catálogo remoto con URLs maliciosas | Allowlist de esquemas; rechazar `file:`, `javascript:` y credenciales embebidas |
| `SEC-08` | Fuga de hábitos o telemetría | Cero telemetría de usuario; logs locales y efímeros |
| `SEC-09` | DHT/UPnP expone la IP o abre puertos | UPnP desactivado por defecto; DHT configurable; aviso explícito |
| `SEC-10` | Dependencia comprometida | Versiones fijadas, auditoría de dependencias y licencias |

---

## 3. Invariantes de seguridad

1. El endpoint de vídeo nunca escucha fuera de loopback.
2. Toda sesión local usa un token efímero y no lo escribe en logs.
3. El contenido descargado se escribe solo en el directorio de sesión.
4. Prohibido ejecutar binarios o scripts descargados.
5. Prohibido enviar a la red nombres de archivo, historial, progreso o identificadores del usuario.
6. Prohibido incluir SDKs de analítica, publicidad o crash reporting remoto.
7. Prohibido desactivar la validación TLS del catálogo.
8. Prohibido abrir el puerto 8888 a la LAN “para probar”.
9. Prohibido confiar en el `Content-Type` de un peer o catálogo sin validación local.
10. Prohibido usar contenido o metadatos sin verificar su origen y sus derechos.

---

## 4. Privacidad

- No se recoge telemetría de usuario.
- No se envía historial de visualización a ningún servidor.
- Los logs de diagnóstico son locales, rotativos y sin datos personales.
- Las fuentes de catálogo pueden ser remotas; el usuario decide cuáles añade.
- El progreso y las preferencias se guardan localmente.
- Cualquier futura función de sync entre dispositivos requiere una spec y una revisión de privacidad.

---

## 5. Licencias y distribución

Antes de distribuir FLIK:

- Verificar la licencia de `media_kit`, MPV/FFmpeg y del runtime P2P elegido.
- Confirmar obligaciones de atribución, código fuente y distribución dinámica/estática.
- Revisar compatibilidad con Android TV, Windows, macOS y Linux.
- Documentar avisos de terceros en la app y en el repositorio.
- No asumir que una dependencia es redistribuible solo porque sea open source.

---

## 6. Contenido y cumplimiento

FLIK no aloja contenido ni opera un backend. Aun así:

- El usuario es responsable de las fuentes que añade.
- La app no debe incluir catálogos con contenido ilícito.
- La política de contenido y jurisdicción debe revisarse antes de publicar.
- No se implementa DRM ni elusión de DRM.

---

## 7. Respuesta a incidentes

1. Detener la sesión y cerrar el endpoint.
2. No borrar logs locales antes de capturar el fallo.
3. Identificar si el problema es de peer, contenedor, catálogo o dependencia.
4. Registrar el modo de fallo en `memory/failure_modes.md`.
5. Añadir una prueba que reproduzca el incidente antes de corregirlo.
