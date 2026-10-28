# FLIK — Framework SDD y Gobernanza de Especificaciones

## 1. Protocolo SDD-First

En FLIK, ninguna línea de código de producción se escribe sin una especificación previa en `.ai-harness/sdd/`.

> **Regla de oro:** primero se especifica, después se contrata, después se implementa y finalmente se verifica.

Flujo unidireccional obligatorio:

1. **Especificación SDD:** historia de usuario, reglas de negocio, comportamiento, contratos y criterios BDD.
2. **Contrato:** modelos inmutables, interfaces y tipos compartidos.
3. **Implementación:** código Flutter/Dart en `lib/`.
4. **Verificación:** análisis estático, tests y validadores del arnés.

Si la implementación contradice la especificación, se corrige la implementación o se actualiza la especificación con aprobación explícita. Nunca se improvisa código fuera de spec.

---

## 2. Filosofía Zero-Assumption

Las especificaciones deben permitir reconstruir el sistema desde cero. Por tanto:

- Prohibidos los placeholders, descripciones vagas y fragmentos truncados.
- Prohibidos los marcadores de tarea pendiente en documentos aprobados.
- Todo comportamiento debe ser verificable.
- Todo dato de entrada y salida debe estar definido.
- Todo error relevante debe tener un estado o resultado explícito.
- Las decisiones visuales remiten a `ui-design-system.md`; no se duplican en cada spec.

---

## 3. Taxonomía y estructura

> **Nota:** la taxonomía física de carpetas por página/proceso se revisará en la fase de diseño de specs. La estructura siguiente es provisional y no debe usarse para crear specs nuevas hasta que se apruebe la estructura definitiva.

```
.ai-harness/sdd/
├── 1_COMPONENTS/                # Artefactos estáticos
│   ├── backend/                 # CMP-NN: dominio, datos y motores locales (sin servidor)
│   ├── bootstrap/               # CMP-00: proyecto, identidad y arranque
│   └── frontend/                # CMP-NN: widgets, pantallas, foco, OSD
├── 2_PROCESSES/                 # PRC-XX: flujos dinámicos y pipelines
│   ├── catalog/                 # Sincronización y parseo de catálogo
│   ├── playback/                # Streaming P2P y reproducción
│   └── navigation/              # Navegación, foco y reanudación
└── templates/                   # Plantillas canónicas y convención
    ├── README.md                # Nombrado .spec.md, IDs y anti-deriva
    ├── TEMPLATE_COMPONENT_SDD.md
    └── TEMPLATE_PROCESS_SDD.md
```

### 3.1 Componentes (`CMP-NN`)

| Capa (`layer`) | Ámbito | Ejemplos |
|---|---|---|
| `bootstrap` | Proyecto, identidad y arranque | `CMP-00` |
| `backend` | Dominio, datos y motores locales (sin servidor) | Parser de catálogo, sesión P2P, repositorios |
| `frontend` | Widgets, pantallas, foco y OSD | Billboard, tarjeta, OSD, pantalla de detalle |

> `CMP-00` es una excepción de infraestructura: bootstrap, identidad del proyecto y estructura inicial. Vive en `1_COMPONENTS/bootstrap/`, no en `backend/`.
>
> `backend/` no implica un servidor remoto: agrupa lógica local no visual (dominio, datos, motores P2P, almacenamiento). FLIK sigue siendo 100 % client-side.

### 3.2 Procesos (`PRC-XX`)

| Prefijo | Ámbito | Ejemplos |
|---|---|---|
| `PRC-01` | Apertura y reproducción de un magnet | Catálogo → magnet → P2P → HTTP local → reproductor |
| `PRC-02` | Sincronización de catálogo | Descarga → validación → caché → emisión de estado |
| `PRC-03` | Ciclo de vida de sesión | Abrir, pausar, buscar, cambiar pistas, cerrar |
| `PRC-04` | Navegación y foco | Entrada D-Pad → foco → ruta → restauración |
| `PRC-05` | Reanudación de visualización | Progreso local → decisión → inicio de sesión |

---

## 4. Orden canónico de una especificación de componente

1. **Descripción general:** ID, nombre, tipo, ubicación real en `lib/`, feature y capa.
2. **Historia de usuario:** Como… Quiero… Para…
3. **Racional:** problema que resuelve y necesidad cubierta.
4. **Reglas de negocio:** prefijo `[BS-CMP-XX-YY]`.
5. **Especificación visual:** solo para `layer: frontend`; referencia obligatoria a los tokens de `ui-design-system.md`.
6. **Comportamiento y flujo de interacción:** estados, transiciones y casos borde.
7. **Contrato técnico:** modelos Dart inmutables, interfaces y tipos de entrada/salida.
8. **Verificación determinista:** pruebas unitarias, de widget o de integración.
9. **Criterios de aceptación BDD:** al final, en formato Gherkin `Given-When-Then`.

---

## 5. Orden canónico de una especificación de proceso

1. **Descripción general:** ID, nombre, disparador y componentes participantes.
2. **Historia de usuario.**
3. **Racional.**
4. **Reglas de negocio del proceso:** prefijo `[BS-PRC-XX-YY]`.
5. **Diagrama de secuencia o estados:** Mermaid.
6. **Mapeo de datos y transformación de estados.**
7. **Contratos de entrada/salida:** eventos, modelos y errores.
8. **Verificación determinista.**
9. **Criterios de aceptación BDD:** al final, en Gherkin.

---

## 6. Convenciones de identificadores

- Componentes: `CMP-00`, `CMP-01`, `CMP-02`, … (numeración global; la capa se declara con `layer`).
- Procesos: `PRC-01`, `PRC-02`, …
- Reglas de negocio: `[BS-CMP-10-01]`, `[BS-CMP-01-01]`, `[BS-PRC-01-01]`.
- Cada ID es único y no se reutiliza.
- La capa (`bootstrap`, `backend`, `frontend`) se declara en el front matter y debe coincidir con la carpeta.
- Cada especificación vive en una carpeta `<ID>-<slug>/` con `user_story.md` y el archivo de spec.
- El archivo de spec se llama obligatoriamente `<nombre>.spec.md`, donde `<nombre>` es `<ID>-<slug>`.
- Ejemplos: `CMP-10-billboard-hero.spec.md`, `CMP-02-catalog-parser.spec.md`, `PRC-01-magnet-playback.spec.md`.
- La convención completa, el front matter obligatorio y el protocolo anti-deriva están en `.ai-harness/sdd/templates/README.md`.

Estados permitidos de una especificación (estado del contrato, no del trabajo):

| Estado | Significado |
|---|---|
| `DRAFT` | Borrador editable; no se implementa todavía. |
| `APPROVED` | Contrato aceptado; puede implementarse. No significa “hecho”. |
| `SUPERSEDED` | Reemplazado por otra spec; se conserva por historial. |

La implementación **no** se guarda en `status`. La calcula `sync-sdd`:

- `N/A`: spec en `DRAFT` o `SUPERSEDED`; no se espera implementación.
- `MISSING`: spec `APPROVED` y target inexistente.
- `PRESENT`: target existente y alineado con la última línea base.
- `DIVERGED`: la spec o el target cambiaron después de la última línea base.

`sync-sdd --baseline` registra una nueva línea base cuando el cambio es intencional.

### 6.0 Cambios y supersesión

- Cambio normativo: editar story/spec, incrementar `version`, registrar el cambio y volver a `DRAFT` hasta reaprobar.
- Cambio editorial: versión patch, se mantiene `APPROVED` y se registra como editorial.
- Nuevo contrato que reemplaza a otro: nueva spec con `supersedes`; la anterior pasa a `SUPERSEDED` con `superseded_by`.
- Las specs no se borran; se conservan como historial.
- Los tickets o tareas, si existen, referencian `CMP-NN`/`FR-NN`; su estado no se copia en la spec.

### 6.1 Front matter obligatorio

Toda spec comienza con YAML front matter con, al menos:

- `spec_id`
- `spec_type` (`CMP` o `PRC`)
- `name`
- `layer` (`bootstrap`, `backend` o `frontend`; solo componentes)
- `target` (ruta real o planificada en `lib/`)
- `block` (`app`, `catalog`, `player`, `p2p_engine`, `tv_experience`)
- `status` (`DRAFT`, `APPROVED` o `SUPERSEDED`)
- `version`
- `owner`
- `last_reviewed`
- `approved_at` (`null` mientras sea `DRAFT`)
- `approved_by` (`null` mientras sea `DRAFT`)
- `supersedes` (IDs reemplazados, si aplica)
- `superseded_by` (IDs que reemplazan, obligatorio en `SUPERSEDED`)
- `user_story: user_story.md`

Las specs con `layer: frontend` incluyen además `design_ref` apuntando a `ui-design-system.md`.

La presentación visual de las specs sigue la guía de `.ai-harness/sdd/templates/README.md` §11: cabecera con chips, callouts, mapa de lectura y diagramas Mermaid. La `user_story` es un brief de producto; la spec es el contrato ejecutable y mapea sus criterios `US-*` a `FR-*`/`ST-*`.

### 6.2 Trazabilidad spec ↔ código

Toda spec incluye un mapa de implementación con esta forma:

```
FR-* / ST-* → CT-* → archivo::símbolo → TC-* → estado
```

Reglas:

- Un requisito sin implementación y sin prueba no está terminado.
- Un símbolo público sin entrada en el mapa está fuera de spec.
- Todo símbolo público implementado incluye el comentario `/// Spec: <ID> / <FR|ST>`.
- Cualquier cambio de comportamiento actualiza spec, código, tests y mapa en el mismo cambio.

El detalle operativo está en `.ai-harness/sdd/templates/README.md`.

---

## 7. Criterios BDD

Todo componente y proceso termina con escenarios Gherkin:

```gherkin
Scenario: Reproducir una variante magnet
  Given un catálogo local con una variante magnet válida
  When el usuario selecciona la variante y confirma reproducir
  Then el motor P2P expone el flujo en 127.0.0.1:8888/stream
  And el reproductor inicia la reproducción sin transcodificación
```

Reglas:

- Un escenario por comportamiento relevante.
- Los pasos son observables y verificables.
- No se describen detalles internos de implementación.
- Los errores y casos borde también tienen escenario.

---

## 8. SDD y sistema de diseño

- Toda especificación con `layer: frontend` debe referenciar `ui-design-system.md`.
- Prohibido duplicar valores HEX, tamaños o tokens en las specs; se referencian por nombre.
- Las decisiones de foco, escala y OSD se especifican como comportamiento, no como estilo libre.
- Si una spec necesita un token nuevo, primero se actualiza el sistema de diseño.

---

## 9. Verificación y cierre

Antes de declarar una implementación alineada con la spec:

1. Existe la especificación aprobada en `.ai-harness/sdd/`.
2. El contrato de datos está definido e implementado sin divergencias.
3. `flutter analyze` y `flutter test` pasan.
4. Los criterios BDD están cubiertos por pruebas.
5. Se respetan las invariantes de `architecture_rules.md`.
6. Los validadores del arnés no reportan errores nuevos. `check_sdd` verifica el nombre `<nombre>.spec.md`, el front matter obligatorio y la presencia de trazabilidad `FR/ST → CT → TC`.

---

## 10. Prohibiciones

- Escribir código sin especificación previa.
- Usar placeholders o secciones vacías en specs aprobadas.
- Duplicar reglas de negocio entre capas.
- Introducir un servidor backend, proxy o transcodificación en una spec.
- Introducir telemetría de usuario.
- Especificar estilos fuera del sistema de diseño.
- Reutilizar identificadores o renombrar specs sin actualizar referencias.
