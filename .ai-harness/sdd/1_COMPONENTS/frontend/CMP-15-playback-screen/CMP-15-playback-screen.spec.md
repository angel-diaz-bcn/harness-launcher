---
spec_id: CMP-15
spec_type: CMP
layer: frontend
name: Playback Screen
target: lib/features/tv_experience/presentation/screens/playback_screen.dart
block: tv_experience
status: APPROVED
version: 2.1
owner: UI Team
last_reviewed: 2026-10-25
approved_at: 2026-10-25
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-01]
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-06, CMP-18, CMP-19, CMP-20, CMP-21, CMP-22, CMP-23, CMP-24, CMP-25, CMP-26, CMP-27]
consumed_by: []
components: [CMP-18, CMP-19, CMP-20, CMP-21, CMP-22, CMP-23, CMP-24, CMP-25, CMP-26, CMP-27]
---

# 🎬 CMP-15 — Pantalla de reproducción

`CMP-15` · `APPROVED` · `v2.1` · `Flutter` · `tv_experience`

| 🧩 Tipo | 🚦 Estado | 🧭 Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `tv_experience` | `lib/features/tv_experience/presentation/screens/playback_screen.dart` |

**Target:** `lib/features/tv_experience/presentation/screens/playback_screen.dart`
**Bloque:** `tv_experience`
**Estado:** `APPROVED`

> [!IMPORTANT]
> La pantalla compone la superficie y el OSD, y traduce intenciones al `PlayerController`. No implementa P2P, decodificación ni catálogo.

> [!WARNING]
> Fuera de alcance: siguiente episodio, cambio de calidad, velocidad, capítulos, buffer real, gestos móviles, «omitir intro» y estilo de subtítulos.

## 🗺️ Mapa de lectura

| Bloque | Qué encontrarás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y errores |
| §7–§9 | API, contratos y dependencias |
| §10–§12 | Mapa, pruebas y BDD |
| §13 | DoD, decisiones y preguntas |

---

## 1. Contexto y objetivo

### 1.1 Problema

La pantalla actual solo pinta la superficie y una línea de estado. No hay controles navegables, no se puede buscar con precisión ni elegir pistas.

### 1.2 Objetivo medible

Una pantalla con OSD plano sobre el vídeo, controles al pie, acciones superiores de pistas, volumen y detalles, y cierre ordenado sin fugas.

### 1.3 No objetivos

- Catálogo, detalle o navegación entre pantallas.
- Persistencia real de progreso (se inyecta por callback).
- Cambio de variante o calidad.
- Gestión interna de P2P o del reproductor.

---

## 2. Alcance y límites

**Incluye:**

- Entrada por `PlaybackLaunchRequest`.
- Composición de `PlayerVideoSurface`, `PlayerOsd`, `PlayerStatusOverlay` y `PlayerErrorPanel`.
- Foco raíz, atajos globales y política de auto-hide.
- Cierre ordenado y callback de progreso.
- Reintento desde error.

**Excluye:**

- Lógica de negocio de catálogo, P2P o player.
- Up-next, calidad, velocidad, gestos, PiP.

**Invariantes aplicables:**

- `architecture_rules.md` §4.7 (foco), §4.10 (liberación determinista).
- `ui-design-system.md` §3 (sin estilos locales).

---

## 3. Actores e historia

> **Como** usuario,
> **quiero** ver y controlar la película a pantalla completa,
> **para** disfrutarla con la comodidad de un reproductor prémium.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Recibe un `PlaybackLaunchRequest` y arranca la sesión | Alta | `start` se llama una vez con el magnet y la posición inicial | `BR-01` |
| `FR-02` | Mapea las fases del coordinador a la UI | Alta | `preparing`, `buffering`, `playing`, `paused`, `completed`, `failed` tienen representación | `BR-02` |
| `FR-03` | Gestiona el foco raíz y los atajos globales | Alta | `Select`, flechas y `Back` funcionan según el OSD; `Back` cierra el overlay sin salir y sin procesarse dos veces | `BR-03` |
| `FR-04` | Muestra u oculta el OSD según la política del controlador | Alta | Auto-hide a los 3 s solo si reproduce | `BR-04` |
| `FR-05` | Cierra la sesión y notifica el progreso | Alta | `dispose` cierra P2P y player; el callback recibe posición y duración | `BR-05` |
| `FR-06` | Permite reintentar tras un fallo | Alta | El botón Reintentar vuelve a iniciar con el mismo magnet | `BR-06` |
| `FR-07` | Un error sustituye al OSD | Alta | En `failed` se muestra el panel de error y el foco va a Reintentar | `BR-07` |
| `FR-08` | La pantalla no importa `media_kit` ni P2P | Alta | Solo consume `PlaybackSession` y `PlayerController` | `INV-01` |
| `FR-09` | Reproduce intro cinematográfica local (`player-intro.mp4`) en cada arranque | Alta | Se ejecuta en paralelo a la preparación P2P; la película aguarda silenciada/oculta hasta finalizar la intro; transición con fade-out a negro | `BR-08`, `BR-09` |

## 5. Reglas de negocio e invariantes

| ID | Regla |
|---|---|
| `BR-01` | `start` se ejecuta una sola vez al montar; un nuevo magnet exige una pantalla nueva. |
| `BR-02` | `ready` se trata como `playing` para el OSD; `completed` muestra Repetir. |
| `BR-03` | Con el OSD oculto, `Select` alterna play/pausa y `Left`/`Right` buscan ±10 s. |
| `BR-04` | El OSD permanece visible en pausa, con menú abierto o en error. |
| `BR-05` | El progreso se notifica al pausar y al cerrar; nunca se envía a red. |
| `BR-06` | Reintentar reutiliza el magnet y la posición inicial de la petición. |
| `BR-07` | En `failed` no se muestran controles de reproducción. |
| `BR-08` | La intro cinematográfica se reproduce íntegra en cada sesión de reproducción (sin opción de omitir) mientras el stream de fondo se precarga; al concluir realiza un fadeout a negro hacia la película (o spinner si aún no terminó el buffer). |
| `BR-09` | Si el usuario pulsa `Back` durante la intro, se cancela la intro y la sesión, regresando de inmediato a la pantalla anterior. |
| `INV-01` | La pantalla no importa `package:media_kit`, `p2p_engine` ni almacenamiento. |

---

## 6. Errores y estados

| ID | Situación | Resultado exigido |
|---|---|---|
| `E-01` | Magnet inválido | Panel de error con Reintentar y Salir |
| `E-02` | Fallo de P2P o del reproductor | Panel de error; sesión cerrada |
| `E-03` | Progreso no disponible | El callback recibe duración cero; la UI no falla |
| `E-04` | `videoSurface` nulo antes de abrir | Fondo de lienzo y overlay de preparación |
| `E-05` | Cierre durante la preparación | Se cancela y se libera lo abierto |

---

## 7. API pública

```dart
final class PlaybackLaunchRequest {
  const PlaybackLaunchRequest({
    required this.magnetUri,
    required this.titleId,
    required this.title,
    this.subtitle,
    this.qualityLabel,
    this.initialPosition = Duration.zero,
    this.posterUri,
  });
}

final class PlaybackScreen extends StatefulWidget {
  const PlaybackScreen({
    super.key,
    required this.request,
    required this.session,
    this.onProgress,
    this.onExit,
  });
}

final class PlayerController extends ChangeNotifier {
  PlaybackState get state;
  bool get osdVisible;
  bool get optionsOpen;
  Future<void> start();
  void showOsd({bool autoHide = true});
  void hideOsd();
  Future<void> togglePlay();
  Future<void> seekBy(Duration offset);
  Future<void> seekTo(Duration position);
  Future<void> selectAudio(String trackId);
  Future<void> selectSubtitle(String? trackId);
  Future<void> retry();
  Future<void> close();
}
```

---

## 8. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `PlaybackLaunchRequest` | Datos inmutables de entrada |
| `CT-02` | `PlayerController` | `ChangeNotifier` de OSD, sesión y acciones |
| `CT-03` | `PlaybackSession` | Interfaz de sesión consumida por la pantalla |
| `CT-04` | `PlaybackProgressCallback` | `void Function(Duration position, Duration duration)` |

---

## 9. Dependencias

Permitidas: Flutter, `flik/features/tv_experience/application/playback_session.dart`, `flik/features/tv_experience/presentation/`, `flik/features/player/player.dart` (solo tipos de estado y pistas), tema y localización.

Prohibidas: `media_kit`, `p2p_engine`, SQLite, HTTP, navegación global desde widgets.

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `presentation/screens/playback_screen.dart::PlaybackScreen` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `presentation/controllers/player_controller.dart::PlayerController` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `presentation/screens/playback_screen.dart::_PlaybackScreenState` | `TC-03` | Verified |
| `FR-04` | `CT-02` | `presentation/controllers/player_controller.dart::PlayerController` | `TC-04` | Verified |
| `FR-05` | `CT-04` | `presentation/controllers/player_controller.dart::close` | `TC-05` | Verified |
| `FR-06` | `CT-03` | `presentation/screens/playback_screen.dart::_PlaybackScreenState` | `TC-06` | Verified |
| `FR-07` | `CT-02` | `presentation/screens/playback_screen.dart::_PlaybackScreenState` | `TC-07` | Verified |
| `FR-08` | `CT-03` | `presentation/screens/playback_screen.dart` | `TC-08` | Verified |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Widget | Arranque | Request válido + sesión falsa | `start` llamado con magnet y posición |
| `TC-02` | Unit | Mapeo de fases | Estados del coordinador | UI coherente por fase |
| `TC-03` | Widget | Atajos | `Select`, flechas, `Back`; el cierre de overlay no sale |
| `TC-04` | Unit | Auto-hide | Reproducción y pausa | Oculta a los 3 s solo reproduciendo |
| `TC-05` | Unit | Cierre y progreso | `close()` | Progreso notificado y sesión cerrada |
| `TC-06` | Widget | Reintento | Fase `failed` | Reintentar reinicia |
| `TC-07` | Widget | Error | `failure` | Panel visible, OSD oculto |
| `TC-08` | Static | Fronteras | Imports | Sin `media_kit` ni `p2p_engine` |

Comandos: `flutter analyze`, `flutter test test/widgets/tv_experience test/unit/tv_experience`.

---

## 12. Criterios BDD

```gherkin
@FR-01
Scenario: Iniciar la reproduccion
  Given una peticion valida con posicion inicial
  When se monta la pantalla
  Then la sesion arranca con el magnet de la peticion
  And la posicion inicial se respeta

@FR-04
Scenario: Ocultar el OSD al reproducir
  Given la reproduccion activa y el OSD visible
  When pasan 3 segundos sin entrada
  Then el OSD se oculta
  And al pulsar una tecla vuelve a mostrarse

@FR-07
Scenario: Fallo de reproduccion
  Given una sesion que falla al abrir
  When la pantalla recibe el estado failed
  Then se muestra el panel de error
  And el OSD no muestra controles de reproduccion
```

## 13. Definition of Done

- [x] Todos los `FR-*` tienen `CT-*`, `TC-*` y entrada en §10.
- [x] `flutter analyze` y las pruebas de pantalla pasan.
- [x] Todos los controles son alcanzables con D-Pad.
- [x] La sesión se cierra al salir y al fallar.
- [x] Sin imports prohibidos.
- [x] Sin preguntas bloqueantes.

---

## 14. Decisiones

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-25 | Nombre `PlaybackScreen` / «Pantalla de reproducción» | Coherencia con `PlaybackCoordinator` y `PRC-01` | `CT-01` | Product Owner |
| 2026-10-25 | El progreso se inyecta por callback; persistencia real en `CMP-02` | Evitar dependencia inexistente | `FR-05` | Product Owner |
| 2026-10-25 | Rediseño plano: sin tarjetas, gradientes, acciones superiores y controles al pie | Alinear el reproductor con una referencia prémium manteniendo solo acciones reales | `CMP-18..CMP-27` | Product Owner |

---

## 15. Preguntas abiertas

No hay preguntas bloqueantes.

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Pantalla de reproducción y reparto en componentes | Product Owner |
| 2.0 | 2026-10-25 | Rediseño | OSD plano, acciones superiores, popovers de volumen/detalles y controles al pie | Product Owner |
| 2.1 | 2026-10-25 | Corrección | `Back` con overlay abierto se procesa una sola vez y no sale del reproductor | Product Owner |



