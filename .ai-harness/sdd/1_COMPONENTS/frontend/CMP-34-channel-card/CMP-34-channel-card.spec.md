# CMP-34 — Channel Card

---

spec_id: CMP-34
spec_type: CMP
layer: frontend
name: Channel Card
target: lib/features/tv_experience/presentation/widgets/channels/channel_card.dart
block: tv_experience
status: APPROVED
version: 1.1
owner: UI Team
last_reviewed: 2026-10-27
approved_at: 2026-10-27
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: []
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-07, CMP-17, CMP-35]
consumed_by: [CMP-33]
---

`CMP-34` · `v1.1` · `tv_experience` · `Flutter` · `APPROVED`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `tv_experience` | `lib/features/tv_experience/presentation/widgets/channels/channel_card.dart` |

> [!IMPORTANT]
> Tarjeta de canal 2:3 con arte procedural propio, contador de títulos, badge de estado, foco visible y activación por D-Pad. La tarjeta **es** la acción: no existe botón «Abrir».

> [!WARNING]
> **Fuera de alcance:** descarga de portadas, progreso, acciones secundarias, edición, borrado y reproducción directa.

> [!TIP]
> **Ruta de lectura:** §4 → §7 → §8 → §10.

### 🗺️ Mapa de lectura

| Bloque | Qué encontrarás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y estados |
| §7–§9 | UI, contratos y dependencias |
| §10–§12 | Trazabilidad, pruebas y BDD |
| §13–§15 | Cierre, decisiones y preguntas |

---

## 0. Protocolo de lectura y no invención

1. Leer `CMP-35`, `04-components.md` §4.8 y `01-foundations.md`.
2. Implementar solo lo definido; no añadir acciones ni metadatos.
3. Todo texto proviene de ARB (`CMP-17`); prohibido el literal en el widget.

---

## 1. Contexto y objetivo

### 1.1 Problema

Sin portadas todavía, la pantalla de entrada necesita representar cada canal con un arte propio, legible a tres metros y activable con el mando.

### 1.2 Objetivo medible

Renderizar una tarjeta 2:3 con arte-local-o-procedural, contador de títulos, badge de estado, foco de tres señales y activación por `Select`/`Enter`/`Space`/`gameButtonA`.

### 1.3 No objetivos

- Descargar imágenes.
- Mostrar progreso de visualización.
- Ofrecer acciones secundarias.

---

## 2. Alcance y límites

**Incluye:** arte, título, contador, badge de estado, scrim, foco, semántica y activación.

**Excluye:** selección central (la aplica `CMP-33`), navegación y datos de catálogo.

**Invariantes de arquitectura aplicables:**

- `architecture_rules.md` §2.4: el widget solo pinta y emite intenciones.
- `ui-design-system.md` §3 y §5; `FM-FLIK-007` y `FM-FLIK-011`.

---

## 3. Actores e historia de usuario

> **Como** usuario,
> **quiero** una tarjeta clara con foco evidente,
> **para** identificar y abrir un canal con el mando.

**Actores secundarios:** `CMP-33` (carrusel), `CMP-35` (datos), `CMP-17` (textos).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Mantiene proporción 2:3 con tamaño `layout.poster` del breakpoint. | Must | `AC-01`: relación 220:330 en TV | `BR-01` |
| `FR-02` | Si `coverUri` usa `asset:` y está declarado, pinta el asset con `BoxFit.cover`. | Must | `AC-02`: asset visible | `BR-02` |
| `FR-03` | Si no hay `coverUri` válido, pinta el arte procedural según `ChannelArt`. | Must | `AC-03`: sin red, sin HEX | `BR-03` |
| `FR-04` | Dos canales con `ChannelArt` distinto producen artes visualmente distintos. | Must | `AC-04`: geometría distinta | `BR-03` |
| `FR-05` | Muestra el nombre con máximo dos líneas y elipsis. | Must | `AC-05`: sin desbordamiento | `BR-04` |
| `FR-06` | Muestra el contador con `channelTitlesCount`, incluido el valor cero. | Must | `AC-06`: `0 títulos` visible | `BR-05` |
| `FR-07` | Muestra el badge de estado según la fuente: sin conectar, al día o error. | Must | `AC-07`: texto además de color | `BR-06` |
| `FR-08` | Recibe el foco del carrusel y aplica anillo `border.focus`, halo `accent.soft` y escala `focus.scale` sin reflow. | Must | `AC-08`: tres señales | `BR-07` |
| `FR-09` | `Select`, `Enter`, `Space` o `gameButtonA` invocan `onActivate` una sola vez. | Must | `AC-09`: callback una vez | `BR-08` |
| `FR-10` | Expone `Semantics(button: true)` con nombre, contador y estado. | Must | `AC-10`: etiqueta completa | `BR-09` |
| `FR-11` | El scrim inferior garantiza el contraste del texto sobre cualquier arte. | Must | `AC-11`: scrim presente | `BR-10` |
| `FR-12` | No conoce repositorio, reproductor, red ni estado de la pantalla. | Must | `AC-12`: solo recibe un `Channel` | `BR-11` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla / invariante | Fuente canónica | Verificación |
|---|---|---|---|
| `BR-01` | La tarjeta usa `layout.poster`; no inventa tamaños. | `03-layout.md` | `TC-01` |
| `BR-02` | Solo se pintan assets declarados; nunca red. | `CMP-32` FR-02 | `TC-02` |
| `BR-03` | El arte procedural usa superficies y `brand.tint` al 40 %; sin HEX ni degradados. | `04-components.md` §4.8 | `TC-03` |
| `BR-04` | Título a dos líneas con elipsis; nunca se reduce el estilo. | `01-foundations.md` §4.3 | `TC-04` |
| `BR-05` | El contador nunca se oculta, ni con cero. | `05-pages.md` §3 | `TC-05` |
| `BR-06` | El estado se comunica con texto, no solo con color. | `01-foundations.md` §3.2 | `TC-06` |
| `BR-07` | El foco combina anillo, halo y escala. | `01-foundations.md` §9 | `TC-07` |
| `BR-08` | `onActivate` se emite una única vez por pulsación. | `FM-FLIK-007` | `TC-08` |
| `BR-09` | La semántica describe la acción disponible. | `01-foundations.md` §10 | `TC-09` |
| `BR-10` | El texto sobre imagen descansa siempre sobre scrim. | `01-foundations.md` §3.2 | `TC-10` |
| `BR-11` | Presentación delgada: sin lógica de catálogo ni reproducción. | `architecture_rules.md` §2.4 | `TC-11` |
| `INV-01` | El arte por defecto no depende de aleatoriedad ni de hash. | `CMP-35` BR-03 | `TC-03` |

---

## 6. Estados, comportamiento y errores

### 6.1 Máquina de estados visuales

```mermaid
stateDiagram-v2
    [*] --> Default
    Default --> Focused: recibe foco
    Focused --> Pressed: Select
    Pressed --> Focused: onActivate emitido
    Focused --> Default: pierde foco
    Default --> Selected: seleccionada por el carrusel
    Selected --> Default: otra tarjeta seleccionada
```

### 6.2 Tabla de estados

| Estado | Entrada | Salida | UI / efecto observable |
|---|---|---|---|
| `Default` | Sin foco y sin selección | Foco o selección | Escala 1.0, borde `border.hairline` |
| `Selected` | Selección del carrusel | Otra selección | Escala `focus.scale` del contenedor |
| `Focused` | Foco de teclado o D-Pad | Pérdida de foco | Anillo, halo y escala |
| `Pressed` | `Select` | Emisión de `onActivate` | Sin cambio de layout |

### 6.3 Errores y casos borde

| Código | Condición | Resultado | Recuperable |
|---|---|---|---|
| `missingAsset` | `coverUri` con `asset:` inexistente | Se pinta el arte procedural | Sí |
| `remoteCover` | `coverUri` con `http(s)` | Se pinta el arte procedural; sin red | Sí |
| `emptyName` | `name` vacío | Se pinta arte y contador; sin título | No aplica |

---

## 7. UX/UI y foco

- **Tokens:** `layout.poster`, `radius.lg`, `border.hairline`, `border.focus`, `accent.soft`, `focus.scale`, `surface.base`, `surface.elevated`, `surface.inset`, `surface.overlay`, `brand.tint`, `text.primary`, `text.secondary`.
- **Jerarquía:** arte → título `title` (2 líneas) → pie con contador `caption` y badge de estado.
- **Foco inicial:** lo decide `CMP-33`; la tarjeta no se autoenfoca salvo `autofocus`.
- **Orden D-Pad:** `Left`/`Right` los gestiona `CMP-33`; la tarjeta solo consume `Select`/`Enter`/`Space`/`gameButtonA`.
- **Estado de foco:** anillo `border.focus` de 2 dp, halo `accent.soft`, escala `focus.scale`; transición `motion.base`; sin reflow.
- **Accesibilidad:** `Semantics(button: true, label: ...)` con nombre, contador y estado; contraste AA sobre el scrim.
- **Responsive:** en `compact` la tarjeta ocupa el ancho disponible manteniendo 2:3; sin cambios de jerarquía.

**Regla:** ninguna decisión visual puede contradecir `ui-design-system.md`.

---

## 8. Contratos de datos (`CT-*`)

### 8.1 Modelos e interfaces

```dart
// Ruta canónica: lib/features/tv_experience/presentation/widgets/channels/channel_card.dart
// Spec: CMP-34 / FR-01 .. FR-12

/// Tarjeta 2:3 de un canal.
/// Spec: CMP-34 / FR-01 .. FR-12
final class ChannelCard extends StatefulWidget {
  const ChannelCard({
    super.key,
    required this.channel,
    required this.selected,
    required this.focused,
    required this.onActivate,
  });

  final Channel channel;
  final bool selected;
  final bool focused;
  final VoidCallback onActivate;
}

/// Arte del canal: asset declarado o placeholder procedural.
/// Spec: CMP-34 / FR-02 .. FR-04
final class ChannelArtwork extends StatelessWidget {
  const ChannelArtwork({super.key, required this.channel});

  final Channel channel;
}
```

### 8.2 Tabla de campos

| Campo | Tipo | Obligatorio | Restricción | Origen |
|---|---|---|---|---|
| `channel` | `Channel` | Sí | Inmutable | `CMP-35` |
| `selected` | `bool` | Sí | — | `CMP-33` |
| `focused` | `bool` | Sí | Verdadero solo en la tarjeta seleccionada | `CMP-33` |
| `onActivate` | `VoidCallback` | Sí | Se invoca una vez | `CMP-33` |

### 8.3 Contratos expuestos

| ID | Símbolo público | Entrada | Salida | Errores |
|---|---|---|---|---|
| `CT-01` | `ChannelCard` | `channel`, `selected`, `focused`, `onActivate` | Widget | — |
| `CT-02` | `ChannelArtwork` | `channel` | Widget | — |

---

## 9. Interfaces y dependencias

### 9.1 Dependencias permitidas

- `CMP-35` (`Channel`, `ChannelArt`).
- `lib/app/theme/` (tokens) y `CMP-17` (ARB).
- Flutter SDK.

### 9.2 Dependencias prohibidas

- Repositorio de canales, reproductor, P2P, HTTP y sistema de archivos.
- Importar `catalog/presentation` o `player/presentation`.
- Colores, tamaños o duraciones literales.

### 9.3 Ciclo de vida

- **Creación:** una por canal visible en el carrusel.
- **Suscripción:** `FocusNode` propio; sin streams.
- **Cancelación:** sin timers.
- **Destrucción:** libera el `FocusNode`.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `.../channels/channel_card.dart::ChannelCard.build` | `TC-01` | Verified |
| `FR-02` | `CT-02` | `.../channels/channel_art.dart::ChannelArtwork` | `TC-02` | Verified |
| `FR-03` | `CT-02` | `.../channel_art.dart::ChannelArtwork` | `TC-03` | Verified |
| `FR-04` | `CT-02` | `.../channel_art.dart::_ArtPatternPainter` | `TC-03` | Verified |
| `FR-05` | `CT-01` | `.../channel_card.dart::_ChannelTitle` | `TC-04` | Verified |
| `FR-06` | `CT-01` | `.../channel_card.dart::_ChannelFooter` | `TC-05` | Verified |
| `FR-07` | `CT-01` | `.../channel_card.dart::_ChannelStatusBadge` | `TC-06` | Verified |
| `FR-08` | `CT-01` | `.../channel_card.dart::_ChannelFocusRing` | `TC-07` | Verified |
| `FR-09` | `CT-01` | `.../channel_card.dart::_ChannelCardState._onKey` | `TC-08` | Verified |
| `FR-10` | `CT-01` | `.../channel_card.dart::_ChannelSemantics` | `TC-09` | Verified |
| `FR-11` | `CT-01` | `.../channel_card.dart::_ChannelScrim` | `TC-10` | Verified |
| `FR-12` | `CT-01` | `.../channel_card.dart` (imports) | `TC-11` | Verified |

**Estados:** `Pending`, `Implemented`, `Verified`.

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Widget | `FR-01` | Canal cualquiera | Relación 2:3 con `layout.poster` |
| `TC-02` | Widget | `FR-02` | `coverUri` `asset:` | Asset visible |
| `TC-03` | Widget | `FR-03`, `FR-04` | Dos canales con arte distinto | Geometrías distintas; sin red |
| `TC-04` | Widget | `FR-05` | Nombre largo | Dos líneas y elipsis |
| `TC-05` | Widget | `FR-06` | Canal sin fuente | Contador «0 títulos» |
| `TC-06` | Widget | `FR-07` | Fuente `pending` y `error` | Badge con texto |
| `TC-07` | Widget | `FR-08` | Foco | Anillo, halo y escala |
| `TC-08` | Widget | `FR-09` | `Enter` | `onActivate` una vez |
| `TC-09` | Widget | `FR-10` | Semántica | Etiqueta con nombre, contador y estado |
| `TC-10` | Widget | `FR-11` | Arte claro | Scrim presente |
| `TC-11` | Unit | `FR-12` | Imports del archivo | Sin repositorio, red ni reproductor |

**Comandos:** `flutter analyze`; `flutter test test/widgets/tv_experience/channel_card_test.dart`.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-03
Scenario: Canal sin portada declarada
  Given un canal con art "wave" y sin cover_uri
  When se pinta la tarjeta
  Then se muestra el arte procedural de onda
  And no se realiza ninguna petición de red
```

```gherkin
@FR-09
Scenario: Activar un canal con el mando
  Given una tarjeta de canal enfocada
  When el usuario pulsa Select
  Then se invoca onActivate una vez
  And el foco permanece en la tarjeta
```

```gherkin
@FR-07
Scenario: Canal sin fuente conectada
  Given un canal con source nula
  When se pinta la tarjeta
  Then el pie muestra "0 títulos"
  And el badge muestra "Sin conectar"
```

---

## 13. Definition of Done

- [ ] Todos los `FR-*` tienen `AC-*`, `TC-*` y entrada en §10.
- [ ] `CT-01` y `CT-02` implementados.
- [ ] Los símbolos públicos llevan comentario `/// Spec: CMP-34 / FR-...`.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] Sin HEX, sin red y sin literales de interfaz.
- [ ] §15 sin preguntas bloqueantes.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-27 | El arte por defecto es procedural y declarado | Evita assets, red y aleatoriedad | `FR-03`, `FR-04` | Product Owner |
| 2026-10-27 | La tarjeta es la acción; no hay botón «Abrir» | El foco ES la selección en la pantalla de entrada | `FR-09` | Product Owner |
| 2026-10-27 | El pie muestra contador y estado, sin badge «CANAL» | El contexto ya es la pantalla de canales | `FR-06`, `FR-07` | Product Owner |
| 2026-10-27 | El foco lo inyecta el carrusel (`focused`), no un `FocusNode` propio | Un único nodo de foco evita traversal anidada y es testeable en TV | `FR-08`, `CT-01` | Arquitectura |
| 2026-10-27 | Arte procedural en cuatro capas y dos pesos de trazo | Las creatividades planas no daban jerarquía ni profundidad | `FR-03`, `FR-04` | Product Owner |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Se admitirán portadas remotas con caché acotada? | No | Arquitectura | Se decidirá antes de `PRC-07` |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-27 | Inicial | Tarjeta con arte procedural, contador, estado y foco | Pendiente |


