# Scope — Catálogo (`block_catalog_service`)

> Solo define límites. Esquema, validación y persistencia se especifican en la SDD.
> Diseño visual fuera de ámbito: `ui-design-system.md`.

## Identidad

| Campo | Valor |
|---|---|
| Bloque | Servicio de catálogo |
| Dominio | Ingesta, validación, caché y progreso |
| Ruta autorizada | `lib/features/catalog/` |
| Formatos | JSON remoto/local |
| Persistencia | Hive o SQLite, decidido en ADR |
| Consumidor | `lib/features/tv_experience/` |
| Estado | Límites cerrados |

## Propósito

Es la autoridad local sobre catálogo y progreso. Ingesta, valida, normaliza y sirve datos sin bloquear por red. No presenta, no reproduce y no descarga carátulas.

## Posee

- Lectura de fuentes remotas y locales.
- Validación e interpretación del esquema.
- Normalización de títulos, metadatos, calidades y magnets.
- Persistencia y caché offline-first.
- Sincronización, reintentos y conservación del último catálogo válido.
- Alta, baja y prioridad de fuentes.
- Almacenamiento del progreso de visualización.
- Telemetría local de ingesta.

## No posee

- Presentación, carátulas o layouts.
- Navegación, foco o entrada.
- Descarga o transformación de imágenes.
- Reproducción, decodificación o control del player.
- Apertura de magnets o sesiones P2P.
- Decisión de reanudar o completar.
- Sincronización entre dispositivos o backend.
- Estilos o tokens visuales.

## Rutas

```
lib/features/catalog/
├── domain/
├── data/
├── presentation/
└── test/
```

Assets semilla permitidos: `assets/catalogs/` (solo catálogos JSON pequeños).

Prohibido escribir en `lib/features/player/`, `p2p_engine/`, `tv_experience/`, `lib/app/` o `lib/core/`.

## Dependencias

Permitidas: cliente HTTP, parser JSON estricto, almacenamiento local y utilidades de rutas/criptografía.

Prohibidas: UI, `media_kit`, motor P2P, navegación, servicios de imágenes, analítica o parsers que instancien objetos arbitrarios.

## Comprobaciones

- [ ] No importa UI, navegación, P2P ni reproducción.
- [ ] No descarga ni transforma carátulas.
- [ ] No abre magnets ni inicia reproducción.
- [ ] No guarda secretos en texto plano.
- [ ] Sirve catálogo desde caché sin bloquear por red.
