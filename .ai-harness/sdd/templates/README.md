# Convención de Especificaciones SDD — FLIK

Esta carpeta contiene las plantillas canónicas y las reglas de nombrado y trazabilidad de todas las especificaciones de FLIK.

---

## 1. Nombre de archivo obligatorio

Toda especificación se llama:

```
<nombre>.spec.md
```

Donde `<nombre>` es `<ID>-<slug>`:

- `ID`: `CMP-NN` o `PRC-NN`.
- `slug`: nombre corto en `kebab-case`, sin acentos, espacios ni mayúsculas.

**Patrón verificable:**

```regex
^(CMP-\d{2}|PRC-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.spec\.md$
```

**Ejemplos válidos:**

```
CMP-10-billboard-hero.spec.md
CMP-04-player-osd.spec.md
CMP-02-catalog-parser.spec.md
CMP-05-p2p-session-controller.spec.md
PRC-01-magnet-playback.spec.md
PRC-02-catalog-sync.spec.md
```

**Prohibido:**

- `spec.md` genérico.
- `CMP-10_spec.md`, `billboard hero.md`, `Billboard-Spec.md`.
- Nombres sin ID o sin sufijo `.spec.md`.
- Carpetas con nombres distintos al `<nombre>` del archivo.

---

## 2. Estructura de carpeta

> **Nota:** la taxonomía por pantalla está aprobada. Una pantalla puede agrupar sus componentes en `components/` según §2.1.

Cada especificación vive en su propia carpeta, junto a la historia de usuario:

```
.ai-harness/sdd/
├── 1_COMPONENTS/
│   ├── backend/
│   │   └── CMP-02-catalog-parser/
│   │       ├── user_story.md
│   │       └── CMP-02-catalog-parser.spec.md
│   ├── bootstrap/
│   │   └── CMP-00-app-bootstrap/
│   │       ├── user_story.md
│   │       └── CMP-00-app-bootstrap.spec.md
│   └── frontend/
│       └── CMP-10-billboard-hero/
│           ├── user_story.md
│           └── CMP-10-billboard-hero.spec.md
└── 2_PROCESSES/
    └── playback/
        └── PRC-01-magnet-playback/
            ├── user_story.md
            └── PRC-01-magnet-playback.spec.md
```

> `backend/` agrupa lógica local no visual; no implica un servidor remoto.

Reglas:

- La carpeta y el archivo comparten el mismo `<nombre>`.
- `user_story.md` contiene la historia de usuario y los criterios de negocio de alto nivel.
- La spec `.spec.md` contiene el contrato técnico y la trazabilidad.
- No se admiten specs sueltas en la raíz de `1_COMPONENTS/` o `2_PROCESSES/`.

---

### 2.1 Pantallas con componentes

Una spec de pantalla puede agrupar las specs de sus componentes en una subcarpeta `components/`:

```
1_COMPONENTS/frontend/
└── CMP-15-playback-screen/
    ├── README.md
    ├── user_story.md
    ├── CMP-15-playback-screen.spec.md
    └── components/
        ├── CMP-18-player-osd/
        │   ├── user_story.md
        │   └── CMP-18-player-osd.spec.md
        └── CMP-19-player-top-bar/
            ├── user_story.md
            └── CMP-19-player-top-bar.spec.md
```

Reglas:

- La spec de pantalla declara `components: [CMP-NN, ...]` en el front matter.
- Cada componente conserva su carpeta `<ID>-<slug>`, su `user_story.md` y su `target` propio.
- El `README.md` de la carpeta de pantalla es el mapa visual y de estados; no es una spec y no lleva front matter.
- Los componentes no dependen de la pantalla; la pantalla los compone.
- `layer` sigue siendo `frontend` para todas las specs del árbol; el validador resuelve la capa por `1_COMPONENTS/frontend/`.

---

## 3. Anatomía obligatoria

### 3.1 Front matter

Toda spec comienza con YAML front matter. Es la ficha machine-readable que valida el arnés y evita ambigüedad:

```yaml
---
spec_id: CMP-10
spec_type: CMP
layer: frontend
name: Billboard Hero
target: lib/features/tv_experience/presentation/widgets/billboard_hero.dart
block: tv_experience
status: DRAFT
version: 1.0
owner: UI Team
last_reviewed: 2026-10-23
approved_at: null
approved_by: null
supersedes: []
superseded_by: []
user_story: user_story.md
processes: [PRC-04]
design_ref: .ai-harness/context/ui-design-system.md
depends_on: []
consumed_by: [CMP-11]
---
```

Campos obligatorios: `spec_id`, `spec_type`, `name`, `layer`, `target`, `block`, `status`, `version`, `owner`, `last_reviewed`, `approved_at`, `approved_by`, `supersedes`, `superseded_by`, `user_story`.

- `spec_type` es `CMP` para componentes y `PRC` para procesos.
- `layer` solo admite `bootstrap`, `backend` o `frontend`, y debe coincidir con la carpeta bajo `1_COMPONENTS/`.
- `target` debe ser una ruta real o planificada dentro de `lib/`; no puede quedar vacía en una spec aprobada.
- `block` debe ser un bloque existente: `app`, `catalog`, `player`, `p2p_engine` o `tv_experience`.
- `design_ref` es obligatorio cuando `layer: frontend`; se omite en `bootstrap`, `backend` y `PRC`.
- `status` solo admite `DRAFT`, `APPROVED` o `SUPERSEDED`.
- En `APPROVED`, `approved_at` y `approved_by` no pueden ser `null`.
- En `SUPERSEDED`, `superseded_by` no puede estar vacío.
- Al cambiar un contrato existente, incrementar `version` y añadir una fila a `Historial de cambios`.

### 3.2 Cuerpo

El cuerpo sigue el orden de la plantilla correspondiente. No se pueden eliminar secciones obligatorias; si una no aplica, se escribe “No aplica” y se explica por qué.

---

## 4. Modelo de identificadores

| Prefijo | Significado | Dónde se usa |
|---|---|---|
| `FR-NN` | Requisito funcional | Spec de componente |
| `BR-NN` | Regla de negocio | Spec de componente o proceso |
| `INV-NN` | Invariante del sistema | Spec de componente o proceso |
| `CT-NN` | Contrato de datos o interfaz | Spec de componente o proceso |
| `ST-NN` | Paso de proceso | Spec de proceso |
| `TC-NN` | Caso de prueba | Spec de componente o proceso |
| `AC-NN` | Criterio de aceptación | Spec de componente |
| `Q-NN` | Pregunta abierta | Spec de componente o proceso |

Reglas:

- Los IDs son estables y únicos dentro de la spec.
- No se renumeran al añadir requisitos; se agregan al final.
- Un `FR-*` solo puede estar `Verified` si tiene `CT-*`, `TC-*` y una entrada real en el mapa de implementación.
- Un `ST-*` solo puede estar `Verified` si tiene contrato, implementación y prueba.

---

## 5. Jerarquía de verdad

1. `.ai-harness/context/project_overview.md`
2. `.ai-harness/context/architecture_rules.md`
3. `.ai-harness/context/ui-design-system.md` para cualquier decisión visual
4. La spec `.spec.md` del componente o proceso
5. El código

Si el código contradice la spec, el código está mal. Si la spec contradice el contexto, la spec está mal. En ambos casos se detiene el cambio y se resuelve la contradicción antes de continuar.

---

## 6. Protocolo anti-deriva

### 6.1 SDD-First

Ninguna línea de código se escribe antes de que exista la spec y esté en `APPROVED`.

### 6.2 Mapa de implementación

Toda spec incluye una tabla que une:

```
Requisito → Contrato → Archivo::Símbolo → Test → Estado
```

Sin esa tabla completa, la implementación no puede considerarse alineada con la spec.

### 6.3 Comentario de trazabilidad en código

Todo símbolo público implementado debe llevar:

```dart
/// Spec: CMP-02 / FR-01
```

Esto permite localizar la spec desde el código y detectar símbolos huérfanos.

### 6.4 Mismo cambio

Si cambia un `FR-*`, `BR-*`, `INV-*` o `CT-*`, en el mismo cambio deben actualizarse:

- la spec;
- el código;
- los tests;
- el mapa de implementación;
- la tabla de decisiones si cambió el alcance.

### 6.5 Sin código huérfano

Un símbolo público que no aparece en el mapa de implementación está fuera de spec. Debe eliminarse o especificarse.

### 6.6 Sin requisito huérfano

Un `FR-*` sin implementación o sin test no puede considerarse terminado.

### 6.7 Sin invención

La IA no puede añadir campos, estados, errores, tokens, pasos, endpoints ni dependencias que no estén en la spec o en los documentos de contexto. Si falta información, se registra en `Q-*` y se detiene la implementación.

---

## 7. Ciclo de vida

| Estado | Significado | Puede implementarse |
|---|---|---|
| `DRAFT` | Spec en redacción o pendiente de re-aprobación | No |
| `APPROVED` | Contrato, reglas y criterios aprobados | Sí |
| `SUPERSEDED` | Reemplazada por otra spec; solo historial | No |

`APPROVED` no significa “implementado”. La implementación se consulta en `sync-sdd`:

| Estado derivado | Significado |
|---|---|
| `N/A` | La spec no es implementable todavía. |
| `MISSING` | Aprobada, pero el target no existe. |
| `PRESENT` | Target existente y alineado con la línea base. |
| `DIVERGED` | Spec o target cambiaron después de la línea base. |

Una spec con preguntas bloqueantes en `Q-*` no puede pasar a `APPROVED`.

### 7.1 Cambios y supersesión

Una spec no es un ticket y no desaparece al implementarse.

- **Cambio normativo:** editar story/spec, incrementar `version`, añadir una fila a `Historial de cambios`, volver a `DRAFT` y reaprobar.
- **Cambio editorial:** incrementar la versión patch, mantener `APPROVED` y registrarlo como editorial.
- **Contrato reemplazado:** crear una spec nueva con `supersedes: [<ID>]`; la anterior pasa a `SUPERSEDED` con `superseded_by: [<ID-nuevo>]`.
- **Nunca borrar una spec:** se conserva como historial aunque esté supersedida.
- **Implementación:** no se escribe en la spec; se consulta en `sync-sdd` (`N/A`, `MISSING`, `PRESENT`, `DIVERGED`).

---

## 8. Cómo crear una spec

1. Crear la carpeta `<ID>-<slug>/` en la taxonomía correspondiente.
2. Escribir `user_story.md` con el problema, actores y criterios de negocio.
3. Copiar la plantilla `TEMPLATE_COMPONENT_SDD.md` o `TEMPLATE_PROCESS_SDD.md`.
4. Renombrar el archivo a `<ID>-<slug>.spec.md`.
5. Completar el front matter y **todas** las secciones obligatorias.
6. Definir `FR-*`/`ST-*`, `BR-*`, `INV-*`, `CT-*`, `TC-*` y `AC-*`.
7. Completar el mapa de implementación con rutas y símbolos reales.
8. Añadir los escenarios BDD.
9. Revisar el checklist de §9.
10. Cambiar el estado a `APPROVED` solo cuando el checklist esté completo y registrar `approved_at`/`approved_by`.

---

## 9. Checklist de revisión

- [ ] El nombre cumple el patrón `^...\.spec\.md$`.
- [ ] La carpeta coincide con el nombre del archivo.
- [ ] El front matter está completo y sin placeholders.
- [ ] Todos los `FR-*`/`ST-*` tienen criterio y prueba.
- [ ] Todos los `CT-*` están definidos con tipos Dart completos.
- [ ] El mapa de implementación tiene rutas y símbolos reales.
- [ ] Los escenarios BDD cubren éxito, error y caso borde.
- [ ] No hay tokens visuales hardcodeados.
- [ ] No hay referencias a backend, proxy o transcodificación.
- [ ] No hay preguntas bloqueantes sin respuesta.
- [ ] El estado es coherente con la implementación real.

---

## 10. Plantillas

- `TEMPLATE_COMPONENT_SDD.md` — componentes `CMP-NN`.
- `TEMPLATE_PROCESS_SDD.md` — procesos `PRC`.

Ambas plantillas son obligatorias. Cualquier spec que no las siga se considera inválida.

---

## 11. Estilo visual de las specs

Las specs se leen en el preview de VS Code y en GitHub. Deben ser legibles en crudo y atractivas en renderizado.

### Cabecera

- Título `# <ID> — <Nombre>`.
- Línea de chips: ID, estado, versión, formato, feature.
- Tabla de ficha rápida: tipo, estado, bloque y artefacto.
- Un callout `[!IMPORTANT]` con el resumen ejecutivo.
- Un callout `[!WARNING]` con lo que queda fuera de alcance.
- Un callout `[!TIP]` con la ruta de lectura.
- Un “Mapa de lectura” en tabla.
- Un diagrama Mermaid corto cuando aclare el flujo.

### Cuerpo

- Un solo nivel de `##` para secciones principales.
- Tablas para campos, reglas y errores; listas solo para pasos.
- Callouts de GitHub para decisiones, riesgos y notas.
- `<details>` solo para apéndices largos; nunca para contenido obligatorio.
- Sin imágenes externas obligatorias; los badges deben ser opcionales.
- Los emojis son apoyo visual, nunca el único portador de significado.

### Cierre

- Checklist de Definition of Done.
- Tabla de decisiones.
- Preguntas abiertas o frase explícita “No hay preguntas bloqueantes”.

---

## 12. Relación `user_story.md` ↔ spec

Se mantienen separados, pero con responsabilidades distintas:

| Archivo | Responde a | No debe contener |
|---|---|---|
| `user_story.md` | ¿Por qué? ¿Para quién? ¿Qué resultado de negocio? | Contratos, campos, estados, errores, código |
| `<ID>.spec.md` | ¿Qué? ¿Cómo? ¿Con qué contratos y pruebas? | Una segunda historia de usuario o duplicación del brief |

Reglas:

1. La spec declara `user_story: user_story.md` en el front matter.
2. Los criterios de negocio usan IDs `US-*`.
3. Cada `US-*` se mapea a uno o más `FR-*`/`ST-*` en la spec.
4. La historia no se actualiza con detalles técnicos; la spec no se actualiza con narrativa de producto.
5. Si un cambio afecta al “por qué”, se actualiza la historia; si afecta al “qué/cómo”, se actualiza la spec.

La historia es un brief de producto; la spec es el contrato ejecutable.
