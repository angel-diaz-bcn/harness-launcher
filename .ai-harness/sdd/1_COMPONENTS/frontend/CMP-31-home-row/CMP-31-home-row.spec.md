# CMP-31 — Home Row

---
spec_id: CMP-31
spec_type: CMP
layer: frontend
name: Home Row
target: lib/features/tv_experience/presentation/widgets/home/home_row.dart
block: tv_experience
status: APPROVED
version: 1.0
owner: UI Team
last_reviewed: 2026-10-26
approved_at: 2026-10-26
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: []
design_ref: .ai-harness/context/ui-design-system.md
depends_on: [CMP-07, CMP-32]
consumed_by: [CMP-12]
---

`CMP-31` · `v1.0` · `tv_experience` · `Flutter` · `DRAFT`

| 🧩 Tipo | 🚦 Estado | 🧭 Feature | 🎯 Target |
|---|---|---|---|
| `CMP` | `DRAFT` | `tv_experience` | `lib/features/tv_experience/presentation/widgets/home/home_row.dart` |

> [!IMPORTANT]
> Raíl horizontal con encabezado y tarjetas, navegable solo con foco. Sin scrollbar y sin paginación.

> [!WARNING]
> **Fuera de alcance:** «Ver todo», Categoría, filtros y carga incremental.

> [!TIP]
> **Ruta de lectura:** §4 → §8 → §10.

### 🗺️ Mapa de lectura

| Bloque | Qué encontrarás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y estados |
| §7–§9 | Datos, contratos y dependencias |
| §10–§12 | Trazabilidad, pruebas y BDD |
| §13–§15 | Cierre, decisiones y preguntas |

---

## 0. Protocolo de lectura y no invención

1. Leer `CMP-12`, `03-layout.md` §3 y `04-components.md` `DS-CAROUSEL`/`DS-SECTION-HEADER`.
2. Implementar solo lo definido; no añadir acciones.

---

## 1. Contexto y objetivo

### 1.1 Problema

La Home necesita raíles que se recorran con el mando y mantengan el foco visible.

### 1.2 Objetivo medible

Mostrar un título y hasta 20 tarjetas en una fila horizontal que se desplaza con `Left`/`Right` sin scrollbar.

### 1.3 No objetivos

- Paginación, «Ver todo» y filtros.

---

## 2. Alcance y límites

**Incluye:** encabezado, fila horizontal, traversal horizontal, desplazamiento por foco y disparo de activación.

**Excluye:** estado de carga propio, paginación y navegación a otras pantallas.

**Invariantes aplicables:** `ui-design-system.md` §5 (sin scrollbars) y `architecture_rules.md` §4.7.

---

## 3. Actores e historia de usuario

> **Como** usuario,
> **quiero** recorrer una fila con las flechas,
> **para** explorar sin ratón.

**Actores secundarios:** `CMP-12` (datos y orden), `CMP-32` (tarjetas).

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Muestra el título recibido por parámetro. | Must | `AC-01`: texto visible | `BR-01` |
| `FR-02` | Pinta las tarjetas en una fila horizontal con `layout.carouselGap`. | Must | `AC-02`: separación por token | `BR-02` |
| `FR-03` | No renderiza más de 20 tarjetas. | Must | `AC-03`: máximo 20 | `BR-03` |
| `FR-04` | `Left`/`Right` mueven el foco entre tarjetas. | Must | `AC-04`: foco secuencial | `BR-04` |
| `FR-05` | La tarjeta enfocada siempre queda visible. | Must | `AC-05`: `ensureVisible` al enfocar | `BR-05` |
| `FR-06` | Sin scrollbar visible ni desplazamiento por hover. | Must | `AC-06`: `Scrollbar` ausente | `BR-06` |
| `FR-07` | Una fila sin ítems no se pinta. | Must | `AC-07`: `SizedBox.shrink` | `BR-07` |
| `FR-08` | `Up`/`Down` salen y entran a la fila según el orden visual. | Must | `AC-08`: traversal vertical correcto | `BR-08` |
| `FR-09` | Activar una tarjeta delega en `onActivate`. | Must | `AC-09`: callback con el ítem | `BR-09` |
| `FR-10` | Expone semántica de lista y de encabezado. | Must | `AC-10`: etiquetas accesibles | `BR-10` |

---

## 5. Reglas de negocio e invariantes

| ID | Regla | Fuente | Verificación |
|---|---|---|---|
| `BR-01` | Título localizado por `CMP-12`. | `CMP-17` | `TC-01` |
| `BR-02` | Gap desde `layout.carouselGap`. | `03-layout.md` §3 | `TC-02` |
| `BR-03` | Límite 20. | `05-pages.md` §4.2 | `TC-03` |
| `BR-04` | Orden de foco igual al orden visual. | `FM-FLIK-007` | `TC-04` |
| `BR-05` | Sin desplazamiento manual. | `03-layout.md` §3 | `TC-05` |
| `BR-06` | Sin scrollbar. | `ui-design-system.md` §5 | `TC-06` |
| `BR-07` | Fila vacía oculta. | `05-pages.md` §4.2 | `TC-07` |
| `BR-08` | Orden vertical igual al visual. | `03-layout.md` §5.3 | `TC-08` |
| `BR-09` | El raíl no conoce el reproductor. | `architecture_rules.md` §2.4 | `TC-09` |
| `BR-10` | Semántica de lista. | `04-components.md` §2.4 | `TC-10` |

**Invariantes:** `INV-01` sin lógica de datos; `INV-02` sin tokens literales; `INV-03` sin foco atrapado.

---

## 6. Estados y errores

| ID | Situación | Resultado |
|---|---|---|
| `ST-01` | Fila con ítems | Título + tarjetas |
| `ST-02` | Fila vacía | No se pinta |
| `E-01` | Ítem no reproducible | Tarjeta deshabilitada |
| `E-02` | Título vacío | Espacio reservado del encabezado |

---

## 7. Datos y transformaciones

| Origen | Destino | Regla |
|---|---|---|
| `title` | Encabezado | Copia literal |
| `items` | Tarjetas | Recorte a 20 |
| `onActivate` | Tarjeta | Delegación directa |

---

## 8. Contratos

### 8.1 `CT-01` — `HomeRow`

```dart
/// Raíl horizontal con encabezado y tarjetas.
/// Spec: CMP-31 / FR-01 .. FR-10
final class HomeRow extends StatelessWidget {
  const HomeRow({
    super.key,
    required this.title,
    required this.items,
    required this.onActivate,
  });

  final String title;
  final List<CatalogItem> items;
  final ValueChanged<CatalogItem> onActivate;
}
```

**Comportamiento de foco:** `FocusTraversalGroup` con `OrderedTraversalPolicy`; cada tarjeta usa `Focus` y llama `Scrollable.ensureVisible` al recibir foco. Sin `Scrollbar`.

---

## 9. Dependencias y ciclo de vida

- **Permitidas:** `CatalogItem`, `PosterCard`, tokens y ARB del llamador.
- **Prohibidas:** repositorio, reproductor, red y literales.
- **Ciclo de vida:** stateless; sin recursos.

---

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `.../home/home_row.dart::_RowHeader` | `TC-01` | Implemented |
| `FR-02` | `CT-01` | `.../home_row.dart::_RowList` | `TC-02` | Implemented |
| `FR-03` | `CT-01` | `.../home_row.dart::HomeRow.build` | `TC-03` | Implemented |
| `FR-04` | `CT-01` | `.../home_row.dart::FocusTraversalGroup` | `TC-04` | Implemented |
| `FR-05` | `CT-01` | `.../home_row.dart::_ensureVisible` | `TC-05` | Implemented |
| `FR-06` | `CT-01` | `.../home_row.dart::_RowList` | `TC-06` | Implemented |
| `FR-07` | `CT-01` | `.../home_row.dart::HomeRow.build` | `TC-07` | Implemented |
| `FR-08` | `CT-01` | `.../home_row.dart::FocusTraversalGroup` | `TC-08` | Implemented |
| `FR-09` | `CT-01` | `.../home_row.dart::_RowList` | `TC-09` | Implemented |
| `FR-10` | `CT-01` | `.../home_row.dart::_RowSemantics` | `TC-10` | Implemented |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Widget | `FR-01` | Título «Tendencias» | Visible |
| `TC-02` | Widget | `FR-02` | 3 tarjetas | Filas con gap de token |
| `TC-03` | Widget | `FR-03` | 30 ítems | 20 tarjetas |
| `TC-04` | Widget | `FR-04` | `Right` | Foco en la siguiente |
| `TC-05` | Widget | `FR-05` | 10 tarjetas | Foco visible |
| `TC-06` | Widget | `FR-06` | Construcción | Sin `Scrollbar` |
| `TC-07` | Widget | `FR-07` | Lista vacía | Sin encabezado |
| `TC-08` | Widget | `FR-08` | Dos filas | `Down`/`Up` correctos |
| `TC-09` | Widget | `FR-09` | `Select` | Callback con ítem |
| `TC-10` | Widget | `FR-10` | Semántica | Rol de lista |

**Comandos:** `flutter analyze`, `flutter test test/widgets/tv_experience/home_row_test.dart`.

---

## 12. Criterios de aceptación BDD

```gherkin
@FR-04
Scenario: Recorrer un raíl con el mando
  Given una fila con 10 tarjetas y foco en la primera
  When el usuario pulsa Right cinco veces
  Then el foco está en la sexta tarjeta
  And la tarjeta enfocada permanece visible
```

```gherkin
@FR-07
Scenario: Raíl sin contenido
  Given una fila con cero ítems
  When la Home la compone
  Then no se pinta el encabezado
  And el foco salta a la siguiente fila
```

---

## 13. Definition of Done

- [ ] `FR-*` con `TC-*` y mapa completo.
- [ ] `CT-01` implementado.
- [ ] Sin scrollbar, literales ni tokens hardcodeados.
- [ ] `flutter analyze` y `flutter test` pasan.
- [ ] §15 sin bloqueos.

---

## 14. Decisiones y cambios

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-26 | Sin «Ver todo» | Categoría no existe | Alcance | Producto |
| 2026-10-26 | Desplazamiento solo por foco | Regla de TV | `FR-05`, `FR-06` | Diseño |

---

## 15. Preguntas abiertas

| ID | Pregunta | Bloqueante | Responsable | Respuesta |
|---|---|---|---|---|
| `Q-01` | ¿Se añadirán flechas visibles en los extremos? | No | Diseño | Requiere ficha `DS-CAROUSEL` |

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-26 | Inicial | Raíl con foco y límite 20 | Pendiente |

