# Framework SDD y gobernanza de especificaciones

## 1. Protocolo SDD-First

Ninguna línea de código de producción se escribe sin una especificación previa
en `.ai-harness/sdd/`.

> **Regla de oro:** primero se especifica, después se contrata, después se
> implementa y finalmente se verifica.

Flujo unidireccional obligatorio:

1. **Especificación:** historia de usuario, reglas de negocio, comportamiento,
   contratos y criterios BDD.
2. **Contrato:** modelos inmutables, interfaces y tipos compartidos.
3. **Implementación:** código en `lib/`.
4. **Verificación:** análisis estático, tests y validadores del arnés.

Si la implementación contradice la especificación, se corrige la implementación
o se actualiza la especificación con aprobación explícita. Nunca se improvisa
código fuera de spec.

## 2. Filosofía Zero-Assumption

Las especificaciones deben permitir reconstruir el sistema desde cero:

- Prohibidos los marcadores pendientes, descripciones vagas y fragmentos truncados.
- Todo comportamiento es verificable.
- Todo dato de entrada y salida está definido.
- Todo error relevante tiene un estado o resultado explícito.
- Las decisiones visuales remiten al sistema de diseño; no se duplican.

## 3. Taxonomía

```
.ai-harness/sdd/
├── 1_COMPONENTS/            # Artefactos estáticos
│   ├── bootstrap/           # CMP-00: proyecto, identidad y arranque
│   ├── domain/              # CMP-NN: dominio, datos y motores sin interfaz
│   └── ui/                  # CMP-NN: widgets, pantallas, foco
├── 2_PROCESSES/             # PRC-NN: flujos dinámicos y pipelines
└── templates/               # Plantillas canónicas y convención
```

### 3.1 Componentes (`CMP-NN`)

| Capa | Ámbito | Ejemplos |
|---|---|---|
| `bootstrap` | Proyecto, identidad y arranque | composición de dependencias, punto de entrada |
| `domain` | Dominio, datos y motores | repositorios, parsers, servicios |
| `ui` | Presentación y foco | pantallas, tarjetas, estados |

### 3.2 Procesos (`PRC-NN`)

| Tipo | Ámbito | Ejemplos |
|---|---|---|
| Pipeline | Ingesta, validación y publicación de datos | importación, sincronización |
| Ciclo de vida | Abrir, pausar, reanudar, cerrar un recurso | sesión, reproducción, conexión |
| Interacción | Entrada, foco y navegación | recorrido completo de una pantalla |

La lista concreta de procesos se decide al crear la primera spec; no se
predeclaran identificadores sin contenido.

## 4. Anatomía de una spec

1. Front matter machine-readable (campos en `harness.config.yaml`).
2. Contexto y problema.
3. Alcance y fuera de alcance.
4. Requisitos `FR-*` o pasos `ST-*`.
5. Reglas de negocio `BR-*` e invariantes `INV-*`.
6. Contratos `CT-*` con tipos completos.
7. Errores y estados.
8. Escenarios BDD.
9. Mapa de implementación.
10. Definition of Done y decisiones.

La convención completa está en `.ai-harness/sdd/templates/README.md`.

## 5. Estados de una spec

| Estado | Significado | Implementación permitida |
|---|---|---|
| `DRAFT` | En elaboración | No |
| `APPROVED` | Aprobada con `approved_at` y `approved_by` | Sí |
| `SUPERSEDED` | Reemplazada; exige `superseded_by` | Solo mantenimiento |

Un cambio normativo devuelve la spec a `DRAFT` hasta su reaprobación.

## 6. Trazabilidad spec ↔ código

```
FR-* / ST-* → CT-* → archivo::símbolo → TC-* → estado
```

Reglas:

- Un requisito sin implementación y sin prueba no está terminado.
- Un símbolo público sin entrada en el mapa está fuera de spec.
- Todo símbolo público implementado lleva el comentario `/// Spec: <ID> / <FR|ST>`.
- Cualquier cambio de comportamiento actualiza spec, código, tests y mapa en el
  mismo cambio.

## 7. Criterios BDD

```gherkin
Scenario: <comportamiento observable>
  Given <estado inicial verificable>
  When <acción del usuario o del sistema>
  Then <resultado observable>
  And <efecto secundario observable>
```

Reglas: un escenario por comportamiento relevante, pasos observables, sin
detalles internos, y escenarios explícitos para error y caso borde.

## 8. SDD y sistema de diseño

- Toda spec de capa `ui` referencia `ui-design-system.md` en `design_ref`.
- Prohibido duplicar valores HEX, tamaños o tokens en las specs.
- Las decisiones de foco y escala se especifican como comportamiento.
- Si una spec necesita un token nuevo, primero se actualiza el sistema de diseño.

## 9. Verificación y cierre

1. Existe la especificación aprobada.
2. El contrato está definido e implementado sin divergencias.
3. El análisis estático y la suite de tests pasan.
4. Los criterios BDD están cubiertos.
5. Se respetan las invariantes de `architecture_rules.md`.
6. Los validadores del arnés no reportan errores nuevos.

## 10. Prohibiciones

- Escribir código sin especificación previa.
- Dejar secciones vacías o marcadores pendientes en una spec aprobada.
- Duplicar reglas de negocio entre capas.
- Introducir telemetría de usuario en una spec.
- Especificar estilos fuera del sistema de diseño.
- Reutilizar identificadores o renombrar specs sin actualizar referencias.
