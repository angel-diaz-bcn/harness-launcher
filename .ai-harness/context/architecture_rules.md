# FLIK — Arquitectura y Guardarraíles del Sistema

## 1. Enfoque arquitectónico

FLIK aplica **Clean Architecture** con organización **Feature-First** en Flutter. Cada feature es una unidad vertical con sus propias capas internas:

```
lib/features/<feature>/
├── domain/          # Entidades, contratos y casos de uso puros
├── data/            # Repositorios, DTOs, fuentes locales/remotas
└── presentation/    # Controladores, estado y widgets de la feature
```

Las features sin interfaz propia, como `p2p_engine`, usan `application/` en lugar de `presentation/` para sus controladores de sesión y estado operativo.

Reglas de organización:

- `lib/app/` contiene inicialización, routing, tema global y composición de dependencias.
- `lib/core/` contiene infraestructura transversal: cliente HTTP, almacenamiento, logger, errores, constantes y utilidades sin lógica de negocio.
- `lib/features/` contiene exclusivamente slices funcionales.
- Una feature no importa archivos internos de otra; solo consume su API pública (`<feature>.dart` o carpeta `public/`).
- El dominio no importa Flutter, HTTP, almacenamiento ni paquetes de UI.
- La presentación no accede a red, base de datos, sockets ni al motor nativo.

---

## 2. Desacoplamiento de módulos

### 2.1 Capa P2P independiente de la UI

- El P2P Engine no importa widgets, rutas, temas ni estado de presentación.
- La UI se comunica con el P2P únicamente mediante:
  - el endpoint HTTP local `http://127.0.0.1:8888/stream`;
  - streams o controladores de estado de descarga, pares y disponibilidad.
- La UI nunca manipula piezas, sockets, trackers ni memoria nativa.
- El P2P Engine no conoce el catálogo ni el reproductor.

### 2.2 Reproducción desacoplada del catálogo

- El Media Player recibe del llamador la URL local del flujo y los metadatos mínimos para mostrarse.
- El Media Player no consulta catálogo, no resuelve magnets y no decide qué variante reproducir.
- El Catalog Service no importa `media_kit`, no abre flujos y no controla reproducción.
- La UI es el único componente que conoce a ambos y los coordina.

### 2.3 Catálogo desacoplado de la reproducción

- El Catalog Service entrega modelos de contenido y enlaces magnet; no valida la reproducibilidad real de un códec.
- La selección de calidad y la decisión de reproducir pertenecen a la capa de presentación.
- El progreso de visualización se persiste localmente y se consulta como dato, no como estado del reproductor.

### 2.4 Presentación delgada

- Los widgets solo pintan y emiten intenciones.
- La lógica de navegación, foco, reanudación y sesión vive en controladores de la feature.
- Ningún widget contiene llamadas HTTP, acceso a almacenamiento o manipulación de sockets.

---

## 3. Dirección de dependencias

```
app / composition root
        │
        ├──▶ features/tv_experience
        ├──▶ features/catalog ──▶ core
        ├──▶ features/player  ──▶ core
        └──▶ features/p2p_engine ──▶ core

core no depende de ninguna feature.
tv_experience consume las APIs públicas de catalog, player y p2p_engine.
catalog, player y p2p_engine no se importan entre sí.
```

Reglas:

- Las dependencias apuntan siempre hacia el dominio y hacia `core`.
- Prohibidas las dependencias circulares entre features.
- Prohibido que una feature importe la carpeta `presentation` de otra.
- La composición de dependencias ocurre en `lib/app/`, no dentro de los widgets.

---

## 4. Invariantes del sistema (Hard Invariants)

1. **Cero backend de vídeo:** prohibido servidor intermediario, proxy remoto, CDN propio o servicio de transcodificación. El vídeo circula del motor P2P local al reproductor.
2. **Endpoint local único:** el flujo se expone exclusivamente en `http://127.0.0.1:8888/stream`, accesible solo desde loopback.
3. **HTTP 206 obligatorio:** el endpoint debe soportar Range Requests y responder `206 Partial Content` para permitir seeking continuo sin descargar el archivo completo.
4. **Streaming secuencial estricto:** se priorizan las cabeceras del contenedor MKV/MP4 y los primeros megabytes antes que el resto de piezas.
5. **Búfer de anillo:** las piezas ya reproducidas deben poder evictarse; el almacenamiento y la memoria no pueden crecer sin límite en Android TV.
6. **Sin transcodificación:** se reproduce el archivo original. Un códec no soportado se reporta como error, no se convierte.
7. **Foco universal:** todo elemento interactivo debe ser navegable y activable con D-Pad o flechas de teclado. Ningún control puede depender exclusivamente de hover o toque.
8. **Catálogo offline-first:** la primera pantalla se sirve desde caché local; la red nunca bloquea el arranque.
9. **Privacidad:** cero telemetría de usuario, cero identificadores, cero historial remoto. La telemetría operativa es local y efímera.
10. **Liberación determinista:** al cerrar la reproducción se cancelan sockets, se libera el puerto local, se destruye el reproductor y se libera memoria nativa.

---

## 5. Fronteras por módulo

| Módulo | Puede | No puede |
|---|---|---|
| P2P Engine | Resolver magnets, descargar piezas, gestionar búfer, servir HTTP local, publicar estado | Reproducir, pintar, catalogar, persistir progreso de usuario |
| Media Player | Abrir el flujo local, decodificar, cambiar pistas, reportar estado | Descargar, resolver magnets, leer catálogo, navegar, persistir progreso |
| Catalog Service | Leer/validar JSON, cachear, sincronizar, guardar progreso | Reproducir, abrir magnets, pintar, gestionar foco |
| UI & TV Navigation | Rutas, foco, entrada, estado de presentación, orquestación de sesión | Implementar P2P, decodificar, parsear catálogo, acceder a sockets |

---

## 6. Reglas de recursos y rendimiento

- El motor P2P no bloquea el isolate de UI; el trabajo pesado y las operaciones nativas se aíslan.
- El catálogo se carga de forma paginada o incremental; prohibido materializar listas ilimitadas en memoria.
- Las imágenes de carátulas se cargan bajo demanda con caché acotada.
- El reproductor libera la sesión al salir de la vista de reproducción.
- El búfer descarta datos ya vistos antes de ampliar almacenamiento.
- En Android TV se asume presión de memoria; cualquier nueva caché debe declarar su límite y su política de evicción.

---

## 7. Verificación de arquitectura

Antes de cerrar un cambio:

1. `flutter analyze` sin errores ni warnings nuevos.
2. `flutter test` en verde.
3. Revisión de imports: ninguna feature importa otra fuera de su API pública.
4. Revisión de fronteras: ningún widget accede a red, almacenamiento, sockets o MPV.
5. Revisión de invariantes: endpoint local, 206, secuencialidad, evicción, foco y ausencia de telemetría.
6. Validadores del arnés SDD según `AGENTS.md`.

---

## 8. Prohibiciones explícitas

- Añadir un backend, proxy o servicio remoto para vídeo.
- Reproducir mediante URLs centralizadas cuando el diseño exige magnet.
- Descargar el archivo completo antes de reproducir.
- Mantener piezas ya vistas en disco indefinidamente.
- Exponer el endpoint local fuera de `127.0.0.1`.
- Duplicar lógica de negocio en widgets o pantallas.
- Hardcodear colores, tipografías o tokens visuales.
- Introducir telemetría, analítica o publicidad.
- Publicar en Git sin instrucción explícita del usuario.
