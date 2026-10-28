# FLIK — Overview Global del Producto

## 1. Resumen ejecutivo

**FLIK** (Package ID `com.flik.app`) es un cliente de streaming descentralizado y multiplataforma. Reproduce contenido a partir de enlaces magnet mediante un motor P2P embebido y un reproductor nativo, sin depender de un backend propio, de servidores de transcodificación ni de proxies remotos.

La aplicación es **100 % client-side**. El catálogo se obtiene de listas declarativas remotas o locales, se cachea en el dispositivo y se consume sin conexión. El vídeo nunca pasa por infraestructura de FLIK: el motor P2P descarga las piezas y las expone en un endpoint HTTP local; el reproductor consume ese endpoint directamente.

**Stack:** Flutter para Android TV, Android móvil, Windows, macOS y Linux; `media_kit` con MPV nativo para decodificación y reproducción.

---

## 2. Pilares del producto

1. **Descentralización real:** el contenido se obtiene de la red P2P, no de servidores de FLIK.
2. **Reproducción directa:** el archivo se reproduce sin transcodificar ni remuxear.
3. **Arranque inmediato:** el catálogo se sirve desde caché local antes de cualquier intento de red.
4. **Recursos acotados:** el motor P2P prioriza el streaming secuencial y libera las piezas ya vistas para proteger RAM y almacenamiento en Android TV.
5. **Privacidad por diseño:** no se recoge telemetría de usuario ni se envían hábitos de visualización a terceros.
6. **Experiencia de salón:** navegación espacial con D-Pad, foco visible y lectura a distancia de sofá; adaptación táctil y de escritorio sin romper el modelo de foco.

---

## 3. Arquitectura de los 4 Módulos Core

| Módulo | Responsabilidad | Frontera |
|---|---|---|
| **P2P Engine** | Resolver metadatos magnet, descargar piezas y servir el flujo local | No reproduce ni conoce la UI |
| **Media Player** | Reproducir el flujo local con MPV nativo y controlar pistas | No descarga, no cataloga, no navega |
| **Catalog Service** | Parsear JSON, validar, cachear y servir catálogo | No reproduce, no pinta, no abre magnets |
| **UI & TV Navigation** | Orquestar vistas, foco D-Pad, entrada y estado de reproducción | No implementa P2P, catálogo ni decodificación |

### 3.1 Módulo P2P Engine

- Resuelve el info-hash y los metadatos del enlace magnet.
- Conecta con trackers y DHT para descubrir pares.
- Descarga con prioridad secuencial: cabeceras del contenedor MKV/MP4, primeros megabytes y avance continuo.
- Gestiona un búfer de anillo y evicta piezas ya reproducidas para no agotar disco ni memoria.
- Expone el flujo en `http://127.0.0.1:8888/stream` con soporte de `HTTP 206 Partial Content` y Range Requests para seeking.
- Publica estado operativo: velocidad, pares, progreso y disponibilidad.
- Libera sockets, puerto y memoria nativa al cerrar la sesión.

### 3.2 Módulo Media Player

- Envuelve `media_kit` y el backend MPV nativo.
- Consume exclusivamente el flujo HTTP local del P2P Engine.
- Decodifica MKV, MP4 y los códecs soportados por la plataforma, con preferencia por hardware.
- Extrae y conmuta pistas de audio y subtítulos.
- Expone play, pause, seek, posición, duración y estado de reproducción.
- No transcodifica, no descarga y no conoce el catálogo.

### 3.3 Módulo Catalog Service

- Lee listas dinámicas remotas y locales en JSON.
- Valida títulos, metadatos, calidades y enlaces magnet.
- Persiste el catálogo en caché local ligera (Hive o SQLite) con estrategia offline-first.
- Sirve el catálogo desde disco sin bloquear el arranque por red.
- Sincroniza en segundo plano, reintenta y conserva el último catálogo válido.
- Almacena el progreso de visualización para reanudación local.

### 3.4 Módulo UI & TV Navigation

- Orquesta las vistas de catálogo, detalle y reproductor.
- Implementa navegación espacial para Android TV y navegación por teclado en escritorio.
- Adapta la interacción a táctil en móvil sin bifurcar la lógica de presentación.
- Gestiona el árbol de foco, la retención de selección y el contexto de entrada.
- Orquesta la sesión de reproducción: apertura y cierre de P2P y reproductor.
- Decide la reanudación a partir del progreso persistido.
- Aplica el sistema de diseño definido en `ui-design-system.md`.

---

## 4. Flujo extremo a extremo

1. La app arranca y muestra catálogo desde caché local.
2. El usuario selecciona un título y una calidad.
3. El Catalog Service entrega el enlace magnet de la variante elegida.
4. El P2P Engine resuelve metadatos y comienza la descarga secuencial.
5. El P2P Engine expone el flujo en `127.0.0.1:8888/stream` con Range Requests.
6. El Media Player abre el flujo y reproduce sin transcodificación.
7. La UI refleja estado, pistas y progreso; el OSD se oculta tras inactividad.
8. Al salir, se guarda el punto de visualización y se liberan P2P, sockets y reproductor.

---

## 5. Reglas inmutables del sistema

1. **100 % client-side:** prohibido backend propio, proxy remoto, CDN de vídeo o servidor de transcodificación.
2. **Streaming secuencial:** prohibido priorizar la descarga completa o piezas aleatorias sobre las cabeceras y el avance de reproducción.
3. **Búfer de anillo:** las piezas ya vistas deben poder evictarse; el almacenamiento no puede crecer sin límite en Android TV.
4. **Endpoint local:** el flujo se sirve exclusivamente en `http://127.0.0.1:8888/stream` con `206 Partial Content`.
5. **Cero telemetría de usuario:** no se recogen hábitos, identificadores, historiales ni datos de visualización.
6. **Sin transcodificación:** el reproductor consume el archivo original; si un códec no es soportado, se informa, no se convierte.
7. **Foco universal:** todo elemento interactivo debe ser alcanzable y activable con D-Pad o flechas de teclado.
8. **Catálogo offline-first:** la red nunca bloquea la primera pantalla ni la navegación.

---

## 6. Plataformas objetivo

| Plataforma | Entrada principal | Consideraciones |
|---|---|---|
| Android TV | D-Pad / control remoto | Leanback, foco espacial, memoria y disco limitados |
| Android móvil | Táctil | Gestos, targets táctiles, ciclo de vida |
| Windows | Teclado y ratón | Ventana, atajos, foco con flechas |
| macOS | Teclado y trackpad | Ventana, atajos, foco con flechas |
| Linux | Teclado y ratón | Ventana, atajos, foco con flechas |

---

## 7. Fuera de alcance

- Backend propio, cuentas de usuario, suscripciones o autenticación central.
- Servidores de transcodificación, proxies de vídeo o CDN.
- DRM, alquiler, compra o gestión de derechos.
- Recolección de telemetría, analítica de usuario o publicidad.
- Reproducción en segundo plano y Picture-in-Picture en esta fase.
- Sincronización de progreso entre dispositivos.
- Descarga permanente de contenido para consumo posterior.

---

## 8. Criterios de éxito del producto

- El catálogo es navegable desde el primer frame, incluso sin red.
- Un enlace magnet válido comienza a reproducirse sin intervención de servidores externos.
- El seeking funciona sobre el flujo local sin descargar el archivo completo.
- La app se mantiene fluida en Android TV con recursos acotados.
- Toda acción es alcanzable con D-Pad y muestra foco visible.
- Ningún dato de usuario sale del dispositivo.
