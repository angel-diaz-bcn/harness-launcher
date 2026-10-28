---
spec_id: CMP-27
spec_type: CMP
layer: frontend
name: Player Details Popover
target: lib/features/tv_experience/presentation/widgets/player/player_details_popover.dart
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
depends_on: []
consumed_by: [CMP-18, CMP-19]
---

# 📊 CMP-27 — Detalles de reproducción

`CMP-27` · `APPROVED` · `v1.0` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_details_popover.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

> [!IMPORTANT]
> Solo presenta datos existentes del estado. No calcula ni inventa calidad, pares o velocidad.

## 1. Objetivo

Mostrar la calidad, el estado P2P y la velocidad de descarga en un popover discreto, sin ocupar la barra superior.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Se abre desde la acción de detalles del OSD | El popover queda visible bajo la barra |
| `FR-02` | Muestra la calidad si existe | Se omite la fila si es nula |
| `FR-03` | Muestra pares con plural localizado | Usa `playerPeers` |
| `FR-04` | Muestra el progreso P2P en porcentaje | `0–100 %` |
| `FR-05` | Muestra la velocidad de descarga | `MB/s` con un decimal |
| `FR-06` | No muestra datos inventados | Sin ceros ni calidad ficticia |
| `FR-07` | Es de solo lectura y se cierra con Back | No captura foco propio |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerDetailsPopover` | `StatelessWidget` |
| `CT-02` | `PlayerDetailsData` | Calidad, pares, progreso, velocidad |

## 4. Reglas

- Panel `color.player.panel`, radio `radius.md`, borde `color.player.track`.
- Texto principal `color.player.control`; etiquetas `color.player.textSecondary`.
- Sin acciones dentro del panel; Back lo cierra desde la pantalla.
- Sin estilos locales ni datos derivados no disponibles.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_details_popover.dart::PlayerDetailsPopover` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_details_popover.dart::PlayerDetailsPopover` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `player_details_popover.dart::PlayerDetailsPopover` | `TC-03` | Verified |
| `FR-04` | `CT-02` | `player_details_popover.dart::PlayerDetailsPopover` | `TC-04` | Verified |
| `FR-05` | `CT-02` | `player_details_popover.dart::PlayerDetailsPopover` | `TC-05` | Verified |
| `FR-06` | `CT-02` | `player_details_popover.dart::PlayerDetailsPopover` | `TC-06` | Verified |
| `FR-07` | `CT-01` | `player_details_popover.dart::PlayerDetailsPopover` | `TC-07` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Apertura desde el OSD |
| `TC-02` | Widget | Calidad opcional |
| `TC-03` | Widget | Pares localizados |
| `TC-04` | Widget | Progreso porcentual |
| `TC-05` | Widget | Velocidad MB/s |
| `TC-06` | Widget | Sin datos inventados |
| `TC-07` | Widget | Back cierra sin salir |

## 7. BDD

```gherkin
@FR-01
Scenario: Consultar detalles
  Given la reproduccion activa con pares y calidad
  When el usuario activa el icono de red
  Then se muestra la calidad, los pares y el progreso
  And Back cierra el popover sin salir del reproductor
```

## 8. Definition of Done

- [x] Todos los `FR-*` tienen mapa y prueba.
- [x] Solo datos existentes del estado.
- [x] Back cierra sin salir.
- [x] Sin estilos locales.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Popover de calidad y red P2P | Product Owner |
