# FLIK — Fixtures Deterministas

Datos de prueba sin red, sin trackers públicos y sin servicios externos.

## Estructura

```
fixtures/
├── catalogs/
│   ├── valid/          # JSON válidos
│   └── invalid/        # JSON corruptos o incompletos
├── http/               # Casos de Range Requests
├── p2p/                # Torrents sintéticos (metadatos y archivos)
└── media/              # MKV/MP4 cortos para integración
```

## Reglas

- Los fixtures no contienen datos personales ni contenido con derechos.
- Los catálogos usan el esquema versionado que se fije en la spec de catálogo.
- Los medios deben ser cortos, deterministas y redistribuibles.
- Los tests no descargan fixtures de Internet.
- Los logs de fallo no se guardan aquí; van a `memory/ephemeral_feedback/`.
