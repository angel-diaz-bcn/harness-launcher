# FLIK — Glosario de Dominio

Términos canónicos. Si una spec usa un término distinto, debe mapearlo aquí.

---

## Contenido y catálogo

| Término | Definición |
|---|---|
| **Catálogo** | Documento JSON con títulos, metadatos, variantes y enlaces magnet. |
| **Fuente de catálogo** | Origen remoto o local del que se obtiene un catálogo. |
| **Ítem** | Entrada de catálogo que representa una película, serie o contenido. |
| **Variante** | Calidad o release concreto de un ítem; contiene el magnet que se reproduce. |
| **Magnet** | URI que identifica contenido P2P mediante un info-hash y trackers opcionales. |
| **Info-hash** | Huella que identifica un torrent. Se normaliza a 40 caracteres hex. |
| **Tracker** | Servicio que ayuda a descubrir peers. |
| **DHT** | Red distribuida de descubrimiento de peers sin tracker central. |
| **Peer** | Nodo conectado que intercambia piezas. |
| **Seeder** | Peer que tiene todas las piezas. |
| **Leecher** | Peer que aún no tiene todas las piezas. |
| **Pieza** | Unidad de descarga y verificación de BitTorrent. |
| **Prebuffer** | Datos mínimos que deben estar disponibles antes de iniciar la reproducción. |
| **Perfil** | Identidad local del dispositivo, sin cuenta ni servidor. Agrupa canales y progreso. |
| **Canal** | Unidad de entrada de FLIK: contenedor de una o más listas de catálogo, con nombre, arte y estado de fuente. **No** es un canal de TV en directo, **no** es un `kind` del contrato de catálogo y **no** implica emisión lineal. |
| **Fuente de un canal** | Lista JSON local o remota a la que está conectado un canal. |
| **Home del canal** | Portada del canal activo: hero, filas y colecciones derivadas de sus fuentes. |
| **Colección** | Fila declarada en el catálogo con título, tipo y lista ordenada de ítems. |
| **Progreso** | Punto de visualización guardado localmente por perfil, ítem y episodio. |

## Streaming y reproducción

| Término | Definición |
|---|---|
| **Streaming secuencial** | Descarga priorizando cabeceras y avance continuo desde el punto de reproducción. |
| **Búfer de anillo** | Búfer acotado que evicta datos ya vistos para liberar memoria/disco. |
| **Endpoint local** | Servidor HTTP interno en `127.0.0.1:8888/stream`. |
| **Range Request** | Petición HTTP de un intervalo de bytes. |
| **206** | Respuesta `Partial Content` que habilita seeking sobre el flujo local. |
| **Seeking** | Salto a otra posición temporal del contenido. |
| **OSD** | On-Screen Display: controles superpuestos del reproductor. |
| **Pista** | Flujo de audio o subtítulo dentro del contenedor. |
| **Fallback** | Cambio de decodificación hardware a software cuando la primera falla. |

## Interfaz y TV

| Término | Definición |
|---|---|
| **D-Pad** | Cruceta del mando de TV. |
| **Foco** | Elemento que recibe las acciones de D-Pad/teclado. |
| **Focus trap** | Estado en el que el foco no puede salir de una zona o control. |
| **Billboard** | Bloque destacado con backdrop, título y acciones. |
| **Carrusel** | Fila horizontal de tarjetas. |
| **Leanback** | Modo de Android TV para experiencias de sofá. |
| **Safe area / overscan** | Zona segura que evita que la TV recorte la interfaz. |
| **Pantalla de reproducción** | Vista a pantalla completa del reproductor con su OSD. No se denomina «visualización». |
| **Tarjeta** | Componente que representa un ítem o espacio en una fila o rejilla. |
| **Afinidad local** | Coincidencia calculada en el dispositivo entre los géneros de un ítem y el progreso del perfil. Nunca proviene de un servidor. |

## Arquitectura y proceso

| Término | Definición |
|---|---|
| **Feature** | Unidad vertical de `lib/features/` con dominio, datos y presentación. |
| **Scope** | Documento que limita qué puede modificar un bloque. |
| **Spec `.spec.md`** | Especificación SDD canónica de un componente o proceso. |
| **FR** | Requisito funcional de una spec de componente. |
| **ST** | Paso de una spec de proceso. |
| **CT** | Contrato de datos o interfaz. |
| **TC** | Caso de prueba. |
| **AC** | Criterio de aceptación. |
| **INV** | Invariante que nunca puede violarse. |
| **ADR** | Registro de decisión de arquitectura. |

-----


## 2. Convenio de carátulas (lo que me pediste)

No voy a introducir ninguna imagen. El catálogo semilla irá __sin `poster_uri` ni `backdrop_uri`__, y la UI mostrará un __placeholder__ conforme a tokens (`surface.base` / `surface.elevated` + icono `FlikIconSizes.lg`, sin HEX ni degradados decorativos).

Cuando tú aportes las imágenes, el convenio será:

assets/
├── covers/     → carátula vertical 2:3   →  <id>.jpg   (recomendado 1000×1500)
└── backdrops/  → fondo horizontal 16:9   →  <id>.jpg   (recomendado 1920×1080)

- `<id>` es __exactamente__ el `id` del catálogo (minúsculas, guiones, sin acentos): `blade-runner-2049.jpg`, `the-expanse.jpg`, `sintel.jpg`.
- Formato único `.jpg` (si algún día quieres `.webp`, se decide antes de cargar los archivos).
- El contrato __ya soporta__ rutas locales: `poster_uri: "asset:assets/covers/<id>.jpg"` (verificado en `CMP-01` y en el parser, que admite `asset:` además de `http(s)`).
- Flujo previsto: tú dejas los archivos → yo actualizo el JSON semilla con los `asset:` URIs → `pubspec.yaml` declara `assets/covers/` y `assets/backdrops/` → la UI deja de usar el placeholder para esos ítems.
- __Importante:__ `assets/covers/` debe existir en el repo aunque esté vacío (con `.gitkeep`), porque Flutter falla si un directorio declarado en `pubspec.yaml` no existe.


 
