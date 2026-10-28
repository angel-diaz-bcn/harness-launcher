---
spec_id: CMP-22
spec_type: CMP
layer: frontend
name: Player Options Sheet
target: lib/features/tv_experience/presentation/widgets/player/player_options_sheet.dart
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
consumed_by: [CMP-18]
---

# 🎚️ CMP-22 — Menú de pistas

`CMP-22` · `APPROVED` · `v1.1` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_options_sheet.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Permitir elegir audio y subtítulos durante la reproducción, abierto desde la acción de pistas de la barra superior.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Se abre desde la acción de pistas del OSD | El icono CC emite la apertura |
| `FR-02` | Muestra las pistas de audio disponibles | Una fila por pista, con la seleccionada marcada |
| `FR-03` | Muestra subtítulos y la opción Desactivado | La opción nula es seleccionable |
| `FR-04` | Emite `onAudioSelected` y `onSubtitleSelected` | El id correcto llega al callback |
| `FR-05` | Cierra con Back y devuelve el foco al disparador | El foco no se pierde |
| `FR-06` | Captura el foco mientras está abierto | No se navega al fondo |
| `FR-07` | No ofrece calidad ni velocidad | Fuera de alcance |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerOptionsSheet` | `StatelessWidget` |
| `CT-02` | `PlayerOptionsData` | Listas de pistas y selección |

## 4. Reglas

- Panel `player.panel`, radio `radius.md`, borde `player.track`.
- Cada opción es enfocable y muestra check en la seleccionada.
- Sin hover; `Select` activa.
- `track.title` o `track.language` como etiqueta; no se traduce contenido.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_options_sheet.dart::PlayerOptionsSheet` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_options_sheet.dart::PlayerOptionsSheet` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `player_options_sheet.dart::PlayerOptionsSheet` | `TC-03` | Verified |
| `FR-04` | `CT-01` | `player_options_sheet.dart::PlayerOptionsSheet` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `player_options_sheet.dart::PlayerOptionsSheet` | `TC-05` | Verified |
| `FR-06` | `CT-01` | `player_options_sheet.dart::PlayerOptionsSheet` | `TC-06` | Verified |
| `FR-07` | `CT-02` | `player_options_sheet.dart::PlayerOptionsSheet` | `TC-07` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Lista de audio |
| `TC-02` | Widget | Desactivar subtítulos |
| `TC-03` | Widget | Callbacks de selección |
| `TC-04` | Widget | Cierre y foco restaurado |
| `TC-05` | Widget | Foco atrapado |
| `TC-06` | Widget | Sin calidad/velocidad |
| `TC-07` | Widget | Apertura desde CC | Icono de pistas |

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Panel de audio y subtítulos | Product Owner |
| 1.1 | 2026-10-25 | Ajuste | Apertura desde CC y estilo de reproductor | Product Owner |

## 7. BDD

```gherkin
@FR-02
Scenario: Desactivar subtitulos
  Given subtitulos activos
  When el usuario elige Desactivado
  Then se solicita subtitulo nulo
  And la marca de seleccion se mueve
```

## 8. Definition of Done

- [x] Foco atrapado y restaurado.
- [x] Sin calidad ni velocidad.
- [x] Sin estilos locales.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
