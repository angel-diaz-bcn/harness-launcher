---
spec_id: CMP-19
spec_type: CMP
layer: frontend
name: Player Top Bar
target: lib/features/tv_experience/presentation/widgets/player/player_top_bar.dart
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

# ⬅️ CMP-19 — Barra superior del reproductor

`CMP-19` · `APPROVED` · `v2.0` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_top_bar.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Mostrar contexto y acciones: cierre, título, subtítulo, pistas, volumen y detalles, sin tarjeta y sin datos P2P permanentes.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Muestra el cierre con icono `X` y emite `onClose` | `Select` y `Enter` lo activan |
| `FR-02` | Muestra el título en una línea con elipsis | No desborda |
| `FR-03` | Muestra el subtítulo (temporada/episodio) si existe | Se oculta si es nulo |
| `FR-04` | No muestra calidad ni pares en la barra | Esos datos viven en `CMP-27` |
| `FR-05` | No usa hover para revelar acciones | Todo visible o enfocable |
| `FR-06` | Muestra acciones de pistas, volumen y detalles | Cada una emite su callback |
| `FR-07` | Usa iconos blancos sin fondo y foco blanco | Legible sobre vídeo claro |
| `FR-08` | En compacto mantiene cierre, título y las tres acciones sin overflow | El título se elide |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerTopBar` | `StatelessWidget` |
| `CT-02` | `PlayerTopBarData` | Título, subtítulo, calidad, pares, progreso |

## 4. Reglas

- Sin fondo de tarjeta; solo el gradiente del OSD.
- Texto `color.player.control`; metadatos `color.player.textSecondary`.
- El cierre y las acciones usan `PlayerIconButton` con foco blanco.
- Sin iconos sin etiqueta semántica.
- La calidad y los pares se delegan a `PlayerDetailsPopover`.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_top_bar.dart::PlayerTopBar` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_top_bar.dart::PlayerTopBar` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `player_top_bar.dart::PlayerTopBar` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `player_top_bar.dart::PlayerTopBar` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `player_top_bar.dart::PlayerTopBar` | `TC-05` | Verified |
| `FR-06` | `CT-02` | `player_top_bar.dart::PlayerTopBar` | `TC-06` | Verified |
| `FR-07` | `CT-01` | `player_icon_button.dart::PlayerIconButton` | `TC-07` | Verified |
| `FR-08` | `CT-01` | `player_top_bar.dart::PlayerTopBar` | `TC-08` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Volver dispara callback |
| `TC-02` | Widget | Título con elipsis |
| `TC-03` | Widget | Subtítulo opcional |
| `TC-04` | Widget | Sin calidad en la barra | Solo título/subtítulo y acciones |
| `TC-05` | Widget | Detalles | Calidad y pares en el popover |
| `TC-06` | Widget | Acciones | Pistas, volumen y detalles |
| `TC-07` | Widget | Foco blanco | Anillo visible |
| `TC-08` | Widget | Compacto | Sin overflow a 640×320 |

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Barra con volver, título, calidad y pares | Product Owner |
| 2.0 | 2026-10-25 | Rediseño | Barra plana con cierre X y acciones reales | Product Owner |

## 7. BDD

```gherkin
@FR-01
Scenario: Volver al detalle
  Given el OSD visible
  When el usuario activa Volver
  Then la pantalla cierra la sesion
```

## 8. Definition of Done

- [x] Sin estilos locales.
- [x] Título truncado sin overflow.
- [x] Volver enfocable y semántico.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
