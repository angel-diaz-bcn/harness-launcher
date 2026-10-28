---
spec_id: CMP-26
spec_type: CMP
layer: frontend
name: Player Volume Control
target: lib/features/tv_experience/presentation/widgets/player/player_volume_control.dart
block: tv_experience
status: APPROVED
version: 2.0
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
consumed_by: [CMP-18, CMP-15]
---

# 🔊 CMP-26 — Control de volumen

`CMP-26` · `APPROVED` · `v2.0` · `Flutter` · `tv_experience`

| 🧩 Tipo | 🚦 Estado | 🧭 Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `tv_experience` | `lib/features/tv_experience/presentation/widgets/player/player_volume_control.dart` |

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_volume_control.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Permitir ajustar y silenciar el volumen desde un popover del OSD, con volumen inicial al 100 %.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | El altavoz de la barra superior abre un popover con mute y barra | El popover solo aparece al activarlo |
| `FR-02` | La barra ajusta el volumen entre 0.0 y 1.0 | El valor llega a `PlaybackSession.setVolume` |
| `FR-03` | El botón de mute silencia y restaura el último volumen audible | Silenciar deja 0.0; restaurar vuelve al valor previo |
| `FR-04` | El icono refleja el estado | `volume_off` a 0; `volume_up` con sonido |
| `FR-05` | La barra es navegable con D-Pad | Izquierda/derecha cambian el valor |
| `FR-06` | No guarda estado propio fuera del controlador | El valor viene de `PlayerController` |
| `FR-07` | El adaptador traduce 0.0–1.0 a la escala 0–100 de `media_kit` | Volumen 1.0 produce 100 |
| `FR-08` | El popover usa tokens `player.*` y no deja una barra permanente en el OSD | Estilo plano y limpio |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerVolumeControl` | `StatelessWidget` con volumen y callbacks |
| `CT-02` | `PlaybackSession.setVolume` | `Future<void> Function(double)` |
| `CT-03` | `PlayerController.setVolume` / `toggleMute` | Acciones de presentación |

## 4. Reglas

- Tokens `player.panel`, `player.track`, `player.progress` y `player.surface`; sin colores locales.
- Semántica de slider con porcentaje.
- El volumen no cambia al pausar, buscar ni cambiar de pista.
- El valor inicial es 1.0 (100 %).
- El popover se cierra con Back y mantiene el OSD visible.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_volume_control.dart::PlayerVolumeControl` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_volume_control.dart::PlayerVolumeControl` | `TC-02` | Verified |
| `FR-03` | `CT-03` | `player_controller.dart::toggleMute` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `player_volume_control.dart::PlayerVolumeControl` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `player_volume_control.dart::PlayerVolumeControl` | `TC-05` | Verified |
| `FR-06` | `CT-03` | `player_controller.dart::volume` | `TC-06` | Verified |
| `FR-07` | `CT-02` | `media_kit_adapter.dart::MediaKitAdapter.setVolume` | `TC-07` | Verified |
| `FR-08` | `CT-01` | `player_volume_control.dart::PlayerVolumeControl` | `TC-08` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Botón y slider visibles |
| `TC-02` | Unit | `setVolume` llega a la sesión |
| `TC-03` | Unit | Silenciar y restaurar |
| `TC-04` | Widget | Icono según estado |
| `TC-05` | Widget | Slider enfocable |
| `TC-06` | Unit | El controlador conserva el volumen |
| `TC-07` | Emulador | Audio audible al 100 % y ajuste en caliente |
| `TC-08` | Widget | Popover | Sin barra permanente; Back cierra |

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Altavoz y barra de volumen | Product Owner |
| 2.0 | 2026-10-25 | Rediseño | Volumen en popover y tokens de reproductor | Product Owner |

## 7. BDD

```gherkin
@FR-03
Scenario: Silenciar y restaurar
  Given un volumen de 0.8
  When el usuario pulsa el altavoz
  Then el volumen es 0.0
  And al volver a pulsarlo el volumen es 0.8
```

## 8. Definition of Done

- [x] Todos los `FR-*` tienen mapa y prueba.
- [x] Escala 0.0–1.0 traducida a media_kit.
- [x] Control accesible con D-Pad.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
