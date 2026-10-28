---
spec_id: CMP-23
spec_type: CMP
layer: frontend
name: Player Video Surface
target: lib/features/tv_experience/presentation/widgets/player/player_video_surface.dart
block: tv_experience
status: APPROVED
version: 1.0
owner: UI Team
last_reviewed: 2026-10-25
approved_at: 2026-10-25
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-01]
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-06]
consumed_by: [CMP-15]
---

# 🖼️ CMP-23 — Superficie de vídeo

`CMP-23` · `APPROVED` · `v1.0` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_video_surface.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Pintar la superficie que entrega el reproductor y un fondo neutro cuando aún no existe.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Pinta `videoSurface(context)` cuando existe | Ocupa el área disponible |
| `FR-02` | Usa `color.surface.canvas` como fondo | Sin destellos blancos |
| `FR-03` | Muestra un placeholder no interactivo si la superficie es nula | Sin excepción |
| `FR-04` | No contiene controles ni texto de estado | Solo vídeo y fondo |
| `FR-05` | No importa `media_kit` ni conoce MPV | Solo usa el builder público |
| `FR-06` | Respeta la relación de aspecto que impone el reproductor | Sin deformación |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerVideoSurface` | `StatelessWidget` |
| `CT-02` | `MediaSurfaceBuilder? surface` | Builder público de `CMP-06` |

## 4. Reglas

- `ColoredBox` + `Center` + superficie.
- Nada de `AspectRatio` propio que recorte el vídeo.
- Sin `setState` ni lógica.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_video_surface.dart::PlayerVideoSurface` | `TC-01` | Verified |
| `FR-02` | `CT-01` | `player_video_surface.dart::PlayerVideoSurface` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `player_video_surface.dart::PlayerVideoSurface` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `player_video_surface.dart::PlayerVideoSurface` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `player_video_surface.dart` | `TC-05` | Verified |
| `FR-06` | `CT-02` | `player_video_surface.dart::PlayerVideoSurface` | `TC-06` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Superficie visible |
| `TC-02` | Widget | Fondo de lienzo |
| `TC-03` | Widget | Placeholder sin superficie |
| `TC-04` | Widget | Sin controles |
| `TC-05` | Static | Sin import de media_kit |
| `TC-06` | Widget | Sin deformación |

## 7. BDD

```gherkin
@FR-03
Scenario: Superficie aun no disponible
  Given una sesion en preparacion
  When se pinta la superficie
  Then se muestra el fondo de lienzo
  And no se lanza ninguna excepcion
```

## 8. Definition of Done

- [x] Sin controles.
- [x] Sin imports de media_kit.
- [x] Fondo de lienzo correcto.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
