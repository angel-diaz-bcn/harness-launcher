---
spec_id: CMP-25
spec_type: CMP
layer: frontend
name: Player Error Panel
target: lib/features/tv_experience/presentation/widgets/player/player_error_panel.dart
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
consumed_by: [CMP-15]
---

# ⚠️ CMP-25 — Panel de error

`CMP-25` · `APPROVED` · `v1.0` · `Flutter` · `tv_experience`

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_error_panel.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

## 1. Objetivo

Transformar un fallo en un mensaje accionable.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Muestra título y mensaje del fallo | Texto legible, sin trazas |
| `FR-02` | Ofrece Reintentar y Salir | Ambos enfocables |
| `FR-03` | El foco inicial es Reintentar | `autofocus` |
| `FR-04` | `Back` equivale a Salir | Cierra la sesión |
| `FR-05` | No usa colores fuera de tokens | Fondo `surface`, borde `error` |
| `FR-06` | Permite un callback de salida aunque falle el reintento | Salir siempre disponible |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerErrorPanel` | `StatelessWidget` |
| `CT-02` | `PlayerErrorData` | Título, mensaje, callbacks |

## 4. Reglas

- Panel centrado, `radius.lg`, padding `space.6`.
- El mensaje técnico del coordinador ya es apto para usuario; no se añade stack.
- Botones con `FlikFocusDecoration`.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_error_panel.dart::PlayerErrorPanel` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `player_error_panel.dart::PlayerErrorPanel` | `TC-02` | Verified |
| `FR-03` | `CT-01` | `player_error_panel.dart::PlayerErrorPanel` | `TC-03` | Verified |
| `FR-04` | `CT-02` | `player_error_panel.dart::PlayerErrorPanel` | `TC-04` | Verified |
| `FR-05` | `CT-01` | `player_error_panel.dart::PlayerErrorPanel` | `TC-05` | Verified |
| `FR-06` | `CT-02` | `player_error_panel.dart::PlayerErrorPanel` | `TC-06` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica |
|---|---|---|
| `TC-01` | Widget | Mensaje visible |
| `TC-02` | Widget | Dos acciones |
| `TC-03` | Widget | Foco en Reintentar |
| `TC-04` | Widget | Back sale |
| `TC-05` | Widget | Tokens de error |
| `TC-06` | Widget | Salir siempre disponible |

## 7. BDD

```gherkin
@FR-02
Scenario: Fallo de codec
  Given un error de codec no soportado
  When se muestra el panel
  Then el usuario ve Reintentar y Salir
  And el foco esta en Reintentar
```

## 8. Definition of Done

- [x] Sin trazas técnicas.
- [x] Foco inicial correcto.
- [x] Salir siempre disponible.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.
