---
spec_id: CMP-24
spec_type: CMP
layer: frontend
name: Player Status Overlay
target: lib/features/tv_experience/presentation/widgets/player/player_status_overlay.dart
block: tv_experience
status: APPROVED
version: 1.1
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
consumed_by: [CMP-15]
---

# ⏳ CMP-24 — Overlay de estado

`CMP-24` · `APPROVED` · `v1.1` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_status_overlay.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Comunicar preparación, buffering, estado P2P y avisos efímeros sin bloquear la entrada.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Muestra «Preparando» en `preparing` | Indicador visible |
| `FR-02` | Muestra «Buffering» y pares/progreso en `buffering` | Datos del estado |
| `FR-03` | Muestra un aviso breve de ±10 s | Se desvanece sin interacción |
| `FR-04` | No captura foco ni punteros | `IgnorePointer` |
| `FR-05` | No muestra datos si no existen | Sin ceros inventados |
| `FR-06` | Usa `status.warning` solo para buffering | Color semántico correcto |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerStatusOverlay` | `StatelessWidget` |
| `CT-02` | `PlayerStatusData` | Fase, pares, progreso, feedback |

## 4. Reglas

- Fondo `player.panel`, texto `player.control`, indicador blanco.
- Sin animaciones infinitas pesadas en TV.
- Progreso P2P en porcentaje; velocidad en MB/s.
- Estilo plano del reproductor, sin bordes de marca.

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Overlay de preparación y buffering | Product Owner |
| 1.1 | 2026-10-25 | Ajuste | Estilo plano con tokens de reproductor | Product Owner |

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_status_overlay.dart::PlayerStatusOverlay` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_status_overlay.dart::PlayerStatusOverlay` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `player_status_overlay.dart::PlayerStatusOverlay` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `player_status_overlay.dart::PlayerStatusOverlay` | `TC-04` | Verified |
| `FR-05` | `CT-02` | `player_status_overlay.dart::PlayerStatusOverlay` | `TC-05` | Verified |
| `FR-06` | `CT-01` | `player_status_overlay.dart::PlayerStatusOverlay` | `TC-06` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Preparando |
| `TC-02` | Widget | Buffering con datos |
| `TC-03` | Widget | Aviso de seek |
| `TC-04` | Widget | Sin foco |
| `TC-05` | Widget | Sin datos inventados |
| `TC-06` | Widget | Color de warning |

## 7. BDD

```gherkin
@FR-04
Scenario: El overlay no bloquea el mando
  Given el overlay de buffering visible
  When el usuario pulsa Select
  Then la accion llega al reproductor
  And el overlay no consume el evento
```

## 8. Definition of Done

- [x] No captura entrada.
- [x] Sin datos inventados.
- [x] Textos en ARB.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
