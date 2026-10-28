---
spec_id: CMP-20
spec_type: CMP
layer: frontend
name: Player Center Controls
target: lib/features/tv_experience/presentation/widgets/player/player_center_controls.dart
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
depends_on: []
consumed_by: [CMP-18]
---

# ⏯️ CMP-20 — Controles centrales

`CMP-20` · `APPROVED` · `v2.0` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_center_controls.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Ofrecer −10 s, play/pausa y +10 s con estados claros y foco, al pie del OSD y bajo la timeline.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Muestra −10 s, play/pausa y +10 s | Los tres botones son visibles |
| `FR-02` | Emite `onSeek(-10 s)` y `onSeek(+10 s)` | El callback recibe el delta exacto |
| `FR-03` | Emite `onTogglePlay` | Un `Select` alterna el estado |
| `FR-04` | Refleja `playing`, `paused`, `buffering` y `completed` | Icono y etiqueta correctos |
| `FR-05` | Oculta o deshabilita las acciones en `preparing` y `buffering`; deshabilita en `failed` | No se puede activar un control inválido |
| `FR-06` | El botón central recibe el foco inicial | `autofocus` del grupo |
| `FR-07` | El play es un círculo translúcido; −10/+10 son iconos sin círculo | Estilo plano de la referencia |
| `FR-08` | Los objetivos miden al menos 56 dp y el foco es blanco | D-Pad usable sobre vídeo claro |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerCenterControls` | `StatelessWidget` |
| `CT-02` | `PlayerCenterControlsCallbacks` | `onTogglePlay`, `onSeek` |

## 4. Reglas

- Botones con objetivo mínimo `target.tvMin`.
- Icono `play_arrow`/`pause`/`replay`.
- Etiquetas accesibles desde ARB.
- `+10`/`−10` se muestran como icono (sin texto) con etiqueta semántica.
- El play usa fondo `color.player.surface`; el resto, sin fondo.
- El foco usa `color.player.focus` y se dibuja con `FlikFocusDecoration`.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_center_controls.dart::PlayerCenterControls` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_center_controls.dart::PlayerCenterControls` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `player_center_controls.dart::PlayerCenterControls` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `player_center_controls.dart::PlayerCenterControls` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `player_center_controls.dart::PlayerCenterControls` | `TC-05` | Verified |
| `FR-06` | `CT-01` | `player_center_controls.dart::PlayerCenterControls` | `TC-06` | Verified |
| `FR-07` | `CT-01` | `player_center_controls.dart::PlayerCenterControls` | `TC-07` | Verified |
| `FR-08` | `CT-01` | `player_icon_button.dart::PlayerIconButton` | `TC-08` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Tres botones |
| `TC-02` | Widget | Deltas de seek |
| `TC-03` | Widget | Toggle play |
| `TC-04` | Widget | Iconos por fase |
| `TC-05` | Widget | Deshabilitado en preparing |
| `TC-06` | Widget | Foco inicial |
| `TC-07` | Widget | Estilo plano | Play translúcido, seek sin círculo |
| `TC-08` | Widget | Foco blanco | Anillo visible |

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | −10, play/pausa y +10 centrados | Product Owner |
| 2.0 | 2026-10-25 | Rediseño | Controles al pie, play translúcido y seek plano | Product Owner |

## 7. BDD

```gherkin
@FR-02
Scenario: Retroceder diez segundos
  Given la reproduccion activa
  When el usuario activa -10 s
  Then la sesion recibe un seek de menos diez segundos
```

## 8. Definition of Done

- [x] Sin estilos locales.
- [x] Semántica y etiquetas en ARB.
- [x] Foco y activación con D-Pad.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
