# Scope — Base Compartida (`block_app_core`)

> Solo define límites. Contratos e infraestructura se especifican en la SDD.
> Diseño visual fuera de ámbito: `ui-design-system.md`.

## Identidad

| Campo | Valor |
|---|---|
| Bloque | Base compartida de la aplicación |
| Dominio | Infraestructura transversal y configuración del proyecto |
| Rutas autorizadas | `lib/core/`, `pubspec.yaml`, `analysis_options.yaml`, `assets/`, `test/`, `integration_test/` |
| Consumidores | Todas las features y `lib/app/` |
| Estado | Límites cerrados |

## Propósito

Proporciona infraestructura transversal sin lógica de negocio: HTTP, almacenamiento compartido, logger, errores, constantes, utilidades puras y configuración del proyecto Flutter.

## Posee

- Cliente HTTP base para catálogo.
- Contratos de almacenamiento local compartido.
- Logger, errores tipados, constantes y helpers puros.
- `pubspec.yaml`, `analysis_options.yaml` y assets globales.
- Configuración de proyecto en `android/`, `windows/`, `macos/`, `linux/`.
- Fixtures y utilidades de test transversales.
- Scripts de build y configuración de CI.

## No posee

- Lógica de catálogo, P2P, player o navegación.
- Vistas, widgets, temas o tokens.
- Apertura de magnets, sockets o sesiones.
- Persistencia de catálogo o progreso.
- Código nativo del motor P2P (pertenece a `block_p2p_engine`).

## Rutas

```
lib/core/
├── http/
├── storage/
├── logging/
├── errors/
├── constants/
└── utils/

assets/
├── fonts/
├── images/
└── catalogs/        # semilla de catálogo; el parser es de catalog

test/
integration_test/
```

Prohibido escribir en `lib/features/*` o `lib/app/`.

## Dependencias

Permitidas: SDK de Flutter/Dart, paquetes de infraestructura declarados en `pubspec.yaml`, utilidades de test.

Prohibidas: lógica de features, UI de features, `media_kit` (salvo configuración de build), motor P2P, bases de datos de catálogo.

## Comprobaciones

- [ ] `lib/core/` no importa `lib/features/`.
- [ ] `lib/core/` no contiene lógica de negocio.
- [ ] `pubspec.yaml` no incluye SDKs de analítica, publicidad o backend.
- [ ] Los assets no incluyen vídeo, torrents ni datasets pesados.
- [ ] La configuración de plataforma no abre puertos ni permisos innecesarios.
