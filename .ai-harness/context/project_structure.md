# FLIK — Estructura del Proyecto y Mapa de Directorios

Topología física del repositorio Flutter y responsabilidades de cada directorio.

---

## 1. Árbol del repositorio

```
flik/
├── .ai-harness/                 # Gobernanza SDD, contexto, scopes y validadores
├── android/                     # Android TV (Leanback launcher) y Android móvil
├── windows/                     # Contenedor y configuración de escritorio Windows
├── macos/                       # Contenedor y configuración de escritorio macOS
├── linux/                       # Contenedor y configuración de escritorio Linux
├── assets/
│   ├── fonts/                   # Barlow Condensed / Barlow Semi Condensed
│   ├── images/                  # Placeholders, iconos y fondos estáticos
│   └── catalogs/                # Catálogos semilla JSON incluidos en el bundle
├── lib/
│   ├── main.dart                # Punto de entrada
│   ├── app/                     # Inicialización, tema global, routing y composición
│   ├── core/                    # HTTP, almacenamiento, logger, errores y helpers
│   └── features/
│       ├── catalog/             # Parser JSON, modelos, persistencia y repositorios
│       ├── player/              # Integración media_kit (MPV), OSD y pistas
│       ├── p2p_engine/          # Motor torrent local y servidor HTTP 127.0.0.1
│       └── tv_experience/       # Billboard, carruseles y navegación D-Pad
├── test/                        # Tests unitarios y de widgets
├── integration_test/            # Flujos de streaming e integración local
├── analysis_options.yaml        # Reglas de lint
├── pubspec.yaml                 # Dependencias y assets
└── README.md
```

---

## 2. Responsabilidades por directorio

### 2.1 `.ai-harness/`

- Fuente de verdad de gobernanza: contexto, scopes, memoria de fallos, plantillas y skills.
- Sistema de diseño en `design-system/`: foundations, tokens, layout, componentes, páginas y code-mapping.
- Contiene las especificaciones SDD de componentes y procesos.
- No contiene código de producción.

### 2.2 `android/`

- Configuración de Android TV: manifiesto Leanback, banner, categoría de launcher y permisos.
- Configuración de Android móvil.
- Código nativo específico del motor P2P cuando la plataforma lo requiera.
- No contiene lógica de catálogo, UI ni reproducción.

### 2.3 `windows/`, `macos/`, `linux/`

- Contenedores de escritorio y configuración de ventana.
- Integración nativa del motor P2P cuando aplique.
- No contienen lógica de negocio.

### 2.4 `assets/`

- Fuentes tipográficas del sistema de diseño.
- Imágenes estáticas y placeholders.
- Catálogos semilla incluidos en el bundle para el primer arranque offline.
- Prohibido incluir vídeo, torrents o contenido pesado.

### 2.5 `lib/app/`

- `bootstrap/`: composición de dependencias y arranque.
- `theme/`: implementación de los tokens de `ui-design-system.md`.
- `routing/`: rutas y transiciones de alto nivel.
- `lifecycle/`: observadores de ciclo de vida de la app.
- No contiene lógica de features.

### 2.6 `lib/core/`

- Cliente HTTP para catálogos.
- Almacenamiento local compartido y contratos de caché.
- Logger, errores tipados, constantes y utilidades puras.
- No conoce features concretas ni widgets.

### 2.7 `lib/features/catalog/`

```
catalog/
├── domain/          # Entidades, contratos de repositorio y casos de uso
├── data/            # Parser JSON, DTOs, Hive/SQLite, fuentes remotas
└── presentation/    # Controladores de catálogo y estado de sincronización
```

- Único lugar donde se parsean documentos de catálogo.
- Único lugar donde se accede a la base local de catálogo y progreso.
- No importa `player` ni `p2p_engine`.

### 2.8 `lib/features/player/`

```
player/
├── domain/          # Contratos de reproducción, pistas y estado
├── data/            # Adaptador media_kit/MPV y carga de subtítulos
└── presentation/    # OSD, controles y estado de reproducción
```

- Único lugar donde se importa `media_kit`.
- Consume la URL local del P2P; no la genera.
- No importa `catalog`.

### 2.9 `lib/features/p2p_engine/`

```
p2p_engine/
├── domain/          # Contratos de sesión, estado y telemetría operativa
├── data/            # Puente nativo, servidor HTTP local y cliente de estado
└── application/     # Controladores de sesión consumidos por tv_experience
```

- Único lugar donde se abre el endpoint `127.0.0.1:8888/stream`.
- Único lugar donde se manipula el runtime BitTorrent.
- No importa `player`, `catalog` ni widgets.

### 2.10 `lib/features/tv_experience/`

```
tv_experience/
├── domain/          # Rutas, intenciones de navegación y contratos de foco
├── data/            # Adaptadores de entrada D-Pad, teclado y táctil
└── presentation/    # Billboard, carruseles, detalle, foco y pantallas
```

- Único lugar que conoce a las tres features anteriores y las coordina.
- Contiene la navegación espacial y el árbol de foco.
- No implementa P2P, catálogo ni decodificación.
- Consume el sistema de diseño; no define tokens.

### 2.11 `test/`

- Tests unitarios de dominio, parsers, repositorios y controladores.
- Widget tests de foco, navegación y pantallas.
- Fixtures JSON válidos e inválidos.
- Prohibido usar red real o temporizadores reales.

### 2.12 `integration_test/`

- Flujos end-to-end con P2P y reproductor simulados o locales.
- Verificación de Range Requests y reproducción de fixtures cortos.
- No depende de trackers públicos ni de contenido externo.

---

## 3. Reglas de dependencia

- `app` puede importar cualquier feature y `core`.
- `tv_experience` puede importar las APIs públicas de `catalog`, `player` y `p2p_engine`.
- `catalog`, `player` y `p2p_engine` no se importan entre sí.
- `core` no importa features.
- Ninguna feature importa `app`.
- Prohibido importar carpetas internas de otra feature; solo su archivo público.
- Prohibidas las dependencias circulares.

---

## 4. Convenciones de archivos

- Archivos en `snake_case.dart`.
- Una clase pública principal por archivo.
- Barrel file por feature: `lib/features/<feature>/<feature>.dart`.
- DTOs en `data/models/`; entidades en `domain/entities/`.
- Contratos en `domain/repositories/` y `domain/services/`.
- Widgets reutilizables en `presentation/widgets/`.
- Pantallas en `presentation/screens/`.
- Controladores en `presentation/controllers/`.

---

## 5. Prohibiciones de estructura

- Crear carpetas `backend/`, `server/` o `api/` para lógica de vídeo.
- Colocar lógica de negocio en `main.dart` o `app/`.
- Acceder a Hive/SQLite desde `tv_experience`.
- Importar `media_kit` fuera de `features/player/`.
- Exponer el motor P2P fuera de `features/p2p_engine/`.
- Incluir assets de vídeo, torrents o datasets pesados en el bundle.
