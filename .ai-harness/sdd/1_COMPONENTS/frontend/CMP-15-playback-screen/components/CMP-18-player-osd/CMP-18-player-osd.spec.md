---
spec_id: CMP-18
spec_type: CMP
layer: frontend
name: Player OSD
target: lib/features/tv_experience/presentation/widgets/player/player_osd.dart
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
depends_on: [CMP-19, CMP-20, CMP-21, CMP-22, CMP-26, CMP-27]
consumed_by: [CMP-15]
---

# 🎛️ CMP-18 — OSD del reproductor

`CMP-18` · `APPROVED` · `v2.0` · `Flutter` · `tv_experience`

| 🧩 Tipo | 🚦 Estado | 🧭 Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `tv_experience` | `lib/features/tv_experience/presentation/widgets/player/player_osd.dart` |

**Target:** `lib/features/tv_experience/presentation/widgets/player/player_osd.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

> [!IMPORTANT]
> El OSD solo compone y presenta. No ejecuta play, seek ni cambios de pista: emite callbacks.

## 1. Objetivo

Componer la capa de controles plana sobre el vídeo: barra superior de contexto y acciones, timeline al pie con controles de reproducción y popovers de volumen y detalles, con visibilidad animada y foco predecible.

## 2. Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| `FR-01` | Compone barra superior, timeline, controles de reproducción al pie y las capas de opciones, volumen y detalles | Todos los bloques están presentes cuando el OSD es visible |
| `FR-02` | Anima la aparición y desaparición con fundido y sin alterar el layout | No hay saltos del vídeo |
| `FR-03` | Aplica una zona segura propia del reproductor: 1.5 % horizontal, 8 % superior y 2.5 % inferior | Ningún control queda pegado al borde ni bajo el overscan |
| `FR-04` | Mantiene el OSD visible si `paused` o hay un overlay abierto | La capa no se oculta en esos estados |
| `FR-05` | El foco inicial es Play/Pausa | Al mostrarse, el foco va al control central |
| `FR-06` | No captura el foco cuando está oculto o hay un overlay abierto | Los atajos globales y el overlay siguen funcionando |
| `FR-07` | Usa gradientes superior e inferior, sin tarjetas ni bordes de panel | El OSD flota sobre el vídeo |
| `FR-08` | Usa tokens `player.*` y foco blanco | Sin colores locales; foco visible sobre vídeo claro |
| `FR-09` | Las capas de opciones, volumen y detalles son excluyentes | Solo una puede estar abierta |
| `FR-10` | Los controles de reproducción se sitúan bajo la timeline | −10, play y +10 quedan al pie, centrados |

## 3. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlayerOsd` | `StatelessWidget` con estado y callbacks |
| `CT-02` | `PlayerOsdCallbacks` | Funciones de play, seek, opciones y salida |

## 4. Reglas

- Sin colores ni tamaños locales: solo tokens `player.*` para el OSD.
- `IgnorePointer` y `ExcludeFocus` cuando está oculto o hay un overlay abierto.
- La timeline y los botones usan `FlikFocusDecoration` con foco blanco.
- El OSD no se oculta si hay overlay o `phase == paused`.
- Sin tarjetas, bordes de panel ni fondos sólidos en la barra superior.

## 5. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `player_osd.dart::PlayerOsd` | `TC-01` | Verified |
| `FR-02` | `CT-01` | `player_osd.dart::PlayerOsd` | `TC-02` | Verified |
| `FR-03` | `CT-01` | `player_osd.dart::PlayerOsd` | `TC-03` | Verified |
| `FR-04` | `CT-02` | `player_osd.dart::PlayerOsd` | `TC-04` | Verified |
| `FR-05` | `CT-02` | `player_osd.dart::PlayerOsd` | `TC-05` | Verified |
| `FR-06` | `CT-01` | `player_osd.dart::PlayerOsd` | `TC-06` | Verified |
| `FR-07` | `CT-01` | `player_osd.dart::PlayerOsd`, `player_scrim.dart::PlayerScrim` | `TC-07` | Verified |
| `FR-08` | `CT-01` | `player_icon_button.dart::PlayerIconButton` | `TC-08` | Verified |
| `FR-09` | `CT-02` | `player_controller.dart::PlayerOverlay` | `TC-09` | Verified |
| `FR-10` | `CT-01` | `player_osd.dart::PlayerOsd` | `TC-10` | Verified |

## 6. Pruebas

| ID | Tipo | Verifica | Criterio |
|---|---|---|---|
| `TC-01` | Widget | Composición | Los cuatro bloques se renderizan |
| `TC-02` | Widget | Animación | Visible/oculto sin cambiar el tamaño del vídeo |
| `TC-03` | Widget | Overscan | Padding ≥ zona segura |
| `TC-04` | Widget | Visibilidad en pausa y menú | Permanece visible |
| `TC-05` | Widget | Foco inicial | Play/Pausa enfocado |
| `TC-06` | Widget | OSD oculto | No recibe foco |
| `TC-07` | Widget | Scrims | Gradientes sin tarjetas |
| `TC-08` | Widget | Foco blanco | Anillo visible sobre vídeo claro |
| `TC-09` | Unit | Overlays | Volumen y detalles excluyentes |
| `TC-10` | Widget | Controles al pie | −10/play/+10 bajo la timeline |

## 7. BDD

```gherkin
@FR-04
Scenario: OSD visible en pausa
  Given la reproduccion pausada
  When el OSD se oculta por inactividad
  Then el OSD permanece visible
```

## 8. Definition of Done

- [x] Todos los `FR-*` tienen mapa y prueba.
- [x] Sin estilos locales.
- [x] Foco correcto con OSD visible y oculto.
- [x] Sin preguntas bloqueantes.

## 9. Preguntas abiertas

No hay preguntas bloqueantes.

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | OSD con tarjeta superior y controles centrales | Product Owner |
| 2.0 | 2026-10-25 | Rediseño | OSD plano con gradientes, controles al pie y overlays | Product Owner |
