---
spec_id: CMP-21
spec_type: CMP
layer: frontend
name: Player Timeline
target: lib/features/tv_experience/presentation/widgets/player/player_timeline.dart
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

# 📏 CMP-21 — Timeline del reproductor

`CMP-21` · `APPROVED` · `v2.0` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_timeline.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Representar posición y duración a los lados de una pista fina, y emitir seek sin ejecutarlo.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Dibuja una pista fina con la posición sobre la duración | Proporción correcta y sin overflow |
| `FR-02` | Muestra tiempo actual y total a los lados de la pista | `m:ss` o `h:mm:ss` |
| `FR-03` | Emite `onSeekRequested` al arrastrar o tocar | La posición pedida queda en `[0, duration]` |
| `FR-04` | Con foco, `Left`/`Right` buscan ±10 s | Emite el delta |
| `FR-05` | Expone semántica de slider con valor y máximo | Lectores anuncian el tiempo |
| `FR-06` | Se deshabilita si `duration == 0` | No emite seek |
| `FR-07` | No dibuja buffer falso | Solo progreso real |
| `FR-08` | Usa progreso blanco, pista blanca al 28 % y foco blanco | Estilo plano de la referencia |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerTimeline` | `StatelessWidget` |
| `CT-02` | `PlayerTimelineData` | Posición, duración, enfocado |

## 4. Reglas

- Pista de `radius.pill`, fondo `color.player.track`, relleno `color.player.progress`.
- Tiempos `caption` a los lados con `color.player.textSecondary`.
- Altura visual fina con área táctil ampliada (36–44 dp).
- El foco usa `FlikFocusDecoration` blanco sin cambiar el layout.
- Sin miniaturas, capítulos ni buffer inventado.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_timeline.dart::PlayerTimeline` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_timeline.dart::PlayerTimeline` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `player_timeline.dart::PlayerTimeline` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `player_timeline.dart::PlayerTimeline` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `player_timeline.dart::PlayerTimeline` | `TC-05` | Verified |
| `FR-06` | `CT-02` | `player_timeline.dart::PlayerTimeline` | `TC-06` | Verified |
| `FR-07` | `CT-01` | `player_timeline.dart::PlayerTimeline` | `TC-07` | Verified |
| `FR-08` | `CT-01` | `player_timeline.dart::PlayerTimeline` | `TC-08` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Proporción de la barra |
| `TC-02` | Unit | Formato de tiempos |
| `TC-03` | Widget | Seek por arrastre |
| `TC-04` | Widget | Seek por teclado |
| `TC-05` | Widget | Semántica de slider |
| `TC-06` | Widget | Deshabilitado sin duración |
| `TC-07` | Widget | Sin buffer ficticio |
| `TC-08` | Widget | Estilo plano | Tiempos laterales y pista fina |

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Barra con tiempos debajo | Product Owner |
| 2.0 | 2026-10-25 | Rediseño | Tiempos laterales, pista fina y progreso blanco | Product Owner |

## 7. BDD

```gherkin
@FR-03
Scenario: Buscar una posicion
  Given una duracion de 100 segundos
  When el usuario arrastra al 50 por ciento
  Then se solicita un seek a 50 segundos
```

## 8. Definition of Done

- [x] Seek acotado a la duración.
- [x] Semántica correcta.
- [x] Sin capítulos ni miniaturas inventados.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
