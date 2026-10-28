# FLIK — Guías y Estándares de Testing

Pirámide de pruebas, criterios y metodología obligatoria para el código de FLIK.

---

## 1. Principios generales

1. **Determinismo:** prohibido depender de red real, trackers públicos, tiempo real o condiciones del entorno.
2. **Aislamiento:** los tests unitarios y de widget no abren sockets externos, no descargan contenido y no usan el reproductor real.
3. **Fixtures versionados:** todo parser y flujo local se prueba con archivos JSON y medios de corta duración incluidos en el repositorio.
4. **Reloj y azar controlados:** usar reloj inyectable y semillas fijas cuando aplique.
5. **Reproducibilidad:** un test que falla debe fallar de la misma forma en local y en integración continua.

---

## 2. Pruebas unitarias

### 2.1 Parsers de catálogo

- JSON válido con títulos, metadatos, series y múltiples calidades.
- JSON corrupto: sintaxis inválida, claves duplicadas, tipos incorrectos.
- JSON con campos desconocidos: debe rechazarse completo.
- JSON con magnet inválido o `info_hash` explícito: debe rechazarse.
- Documentos con magnet inválido, info-hash malformado o variantes vacías.
- Documentos con IDs duplicados o caracteres no permitidos.
- Verificar que un documento inválido se rechaza completo y no deja datos parciales.

### 2.2 Lógica de búfer P2P

- Cálculo de ventana de descarga secuencial.
- Prioridad de cabeceras de contenedor MKV/MP4 y primeros megabytes.
- Búfer de anillo: tamaño máximo respetado.
- Evicción de piezas ya reproducidas.
- Prohibición de evictar la pieza en reproducción o la ventana inmediata.
- Comportamiento ante huecos, piezas faltantes y reinicio de sesión.
- Liberación de recursos y reinicio de contadores al cerrar.

### 2.3 Otros dominios

- Resolución y normalización de enlaces magnet.
- Selección de variante de calidad.
- Persistencia y recuperación de progreso local.
- Sincronización de catálogo: éxito, error de red, documento inválido y conservación del último catálogo válido.
- Búsqueda y filtrado de catálogo.

---

## 3. Pruebas de widgets y foco

- Recepción de eventos D-Pad: `Up`, `Down`, `Left`, `Right` y `Select`.
- Navegación entre tarjetas de un carrusel horizontal.
- Navegación vertical entre filas y secciones.
- El foco no se pierde al cambiar de pantalla y se restaura al volver.
- El foco no queda fuera del viewport; el contenedor hace scroll.
- Todo elemento interactivo es alcanzable solo con D-Pad.
- El estado de foco activo aplica el tratamiento visual definido: escala 108 %, borde de 2 px y halo azul.
- El OSD se oculta a los 3 segundos de inactividad y reaparece con cualquier entrada.
- El OSD permanece visible en pausa.
- La navegación táctil y por teclado produce las mismas acciones semánticas.
- Los estados vacío, error y carga muestran una acción enfocable.

---

## 4. Pruebas de integración de streaming

- Levantar un servidor HTTP local de prueba en `127.0.0.1` y solicitar `Range: bytes=0-1024`.
- Verificar respuesta `206 Partial Content`.
- Verificar `Content-Range`, `Content-Length` y bytes exactos.
- Verificar respuesta `200` para una petición sin `Range`.
- Verificar `416` para un rango fuera de límites.
- Verificar que un rango no descargado se atiende cuando las piezas están disponibles.
- Verificar seeking continuo sobre un archivo fixture.
- Verificar que el búfer evicta piezas vistas sin afectar la reproducción.
- Verificar que al cerrar la sesión se libera el puerto y se cancelan los sockets.
- Verificar que el endpoint no responde fuera de loopback.
- Verificar la integración con un reproductor fake que consume la URL local.

Los tests de integración no usan trackers públicos ni contenido externo. Los medios de prueba son fixtures cortos y deterministas.

---

## 5. Pirámide y cobertura

| Nivel | Proporción objetivo | Alcance |
|---|---|---|
| Unitario | ~70 % | Dominio, parsers, búfer, repositorios |
| Widget | ~20 % | Foco, navegación, OSD, estados |
| Integración | ~10 % | Servidor local, Range Requests, reproducción simulada |

- Cobertura global mínima: **80 %**.
- Parsers de catálogo y lógica de búfer: **95 %**.
- No se acepta cobertura inflada con tests triviales; se prioriza comportamiento.

---

## 6. Estructura de tests

```
test/
├── unit/
│   ├── catalog/
│   ├── p2p_engine/
│   └── player/
├── widget/
│   ├── focus/
│   ├── catalog/
│   └── player/
└── fixtures/
    ├── catalogs/       # JSON válidos e inválidos
    └── media/          # MKV/MP4 cortos

integration_test/
├── streaming_range_test.dart
├── session_lifecycle_test.dart
└── playback_smoke_test.dart
```

---

## 7. Comandos de verificación

- `flutter analyze`
- `flutter test`
- `flutter test integration_test`
- Validadores del arnés SDD definidos en `AGENTS.md`

---

## 8. Prohibiciones

- Tests que dependan de Internet, trackers o servidores externos.
- Tests con esperas arbitrarias (`sleep`) para sincronizar.
- Tests que abran el reproductor real en la suite unitaria.
- Tests que hardcodeen colores o tamaños visuales fuera de los tokens.
- Mocks que reimplementen la lógica bajo prueba.
- Aceptar un bug sin una prueba que lo reproduzca.
