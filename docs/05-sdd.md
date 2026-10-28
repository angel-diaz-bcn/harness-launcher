# 05 — SDD: especificaciones y trazabilidad

## Qué es

SDD (Spec-Driven Development) es el flujo por el que **primero se especifica,
después se contrata, después se implementa y finalmente se verifica**. La spec
es el contrato ejecutable: si el código hace algo que no está en la spec, el
código está fuera de contrato.

## Por qué existe

Sin specs, el código es la única fuente de verdad. Eso implica:

- nadie sabe si un comportamiento es intencional o un accidente;
- los cambios rompen cosas que nadie documentó;
- el agente rellena los huecos inventando;
- las pruebas verifican implementación, no requisitos.

La spec separa **qué** (requisito), **cómo** (contrato), **dónde** (target) y
**cómo se comprueba** (test).

## Archivos implicados

| Ruta | Contenido |
|---|---|
| `sdd/templates/TEMPLATE_COMPONENT_SDD.md` | Plantilla de componente |
| `sdd/templates/TEMPLATE_PROCESS_SDD.md` | Plantilla de proceso |
| `sdd/templates/README.md` | Convención completa |
| `sdd/1_COMPONENTS/<capa>/<ID>-<slug>/` | Spec e historia de componente |
| `sdd/2_PROCESSES/<ID>-<slug>/` | Spec e historia de proceso |

## Mecánica interna

### Dos documentos por unidad

| Archivo | Responde a | No contiene |
|---|---|---|
| `user_story.md` | Por qué, para quién y qué resultado | Contratos ni código |
| `<ID>-<slug>.spec.md` | Qué, cómo, con qué tipos y pruebas | Narrativa de producto |

### Anatomía de la spec

1. Front matter machine-readable (validado campo a campo).
2. Contexto y problema.
3. Requisitos `FR-*` (componentes) o pasos `ST-*` (procesos).
4. Reglas `BR-*` e invariantes `INV-*`.
5. Contratos `CT-*` con tipos completos.
6. Errores y estados.
7. Escenarios BDD.
8. **Mapa de implementación**.
9. Definition of Done y decisiones.

### Trazabilidad

```
FR-* / ST-*  →  CT-*  →  archivo::símbolo  →  TC-*  →  estado
```

Reglas asociadas:

- Un requisito sin implementación y sin prueba no está terminado.
- Un símbolo público sin entrada en el mapa está fuera de spec.
- El comentario `/// Spec: <ID> / <FR|ST>` ata el código a su requisito.
- `sync-sdd` compara spec y target contra un baseline y detecta deriva.

### Estados

| Estado | Implementación permitida |
|---|---|
| `DRAFT` | No |
| `APPROVED` | Sí |
| `SUPERSEDED` | Solo mantenimiento |

## Qué valida el arnés

`check_sdd` aplica, por spec:

| Regla | Qué detecta |
|---|---|
| `SDD-INVALID-SPEC-FILENAME` | Nombre fuera del patrón `<PREFIX>-NN-<slug>.spec.md` |
| `SDD-MISSING-FRONTMATTER` | Falta un campo obligatorio del front matter |
| `SDD-SPEC-ID-MISMATCH` | `spec_id` no coincide con el nombre del archivo |
| `SDD-INVALID-STATUS` | Estado fuera de `DRAFT`/`APPROVED`/`SUPERSEDED` |
| `SDD-MISSING-APPROVAL-DATE` / `-OWNER` | `APPROVED` sin fecha o sin responsable |
| `SDD-MISSING-SUPERSEDED-BY` | `SUPERSEDED` sin reemplazo declarado |
| `SDD-MISSING-LAYER` / `SDD-INVALID-LAYER` | Capa ausente o inválida en componentes |
| `SDD-MISSING-USER-STORY` | No hay `user_story.md` junto a la spec |
| `SDD-TARGET-MISSING` | El `target` de una spec aprobada no existe |
| `SDD-MISSING-TRACEABILITY` | Faltan `FR/ST`, `CT` o `TC` |
| `SDD-MISSING-IMPLEMENTATION-MAP` | No existe la sección de mapa |

`sync-sdd` añade el estado real de implementación: `N/A`, `MISSING`, `PRESENT`
o `DIVERGED`.

## Qué rompe si falta

- El agente implementa "lo que parece razonable" y lo llama terminado.
- Los tests verifican el código que hay, no el comportamiento acordado.
- Cualquier refactor es una ruleta: no hay contrato que respetar.
- Las revisiones se convierten en arqueología.

## Anti-patrón

Specs que describen la implementación:

```markdown
## FR-01
Crear la clase `CatalogRepositoryImpl` con un método `fetch()` que use Dio.
```

Eso es una decisión de implementación, no un requisito. La spec debe decir qué
comportamiento se garantiza; el cómo pertenece al diseño y puede cambiar sin
romper el contrato.

## Flujo de trabajo

1. `create-component-sdd` o `create-process-sdd` genera el esqueleto.
2. Se completa `user_story.md` (por qué).
3. Se completa la spec (qué y cómo).
4. Se revisa el checklist de `templates/README.md`.
5. Se pasa a `APPROVED` con fecha y responsable.
6. Se implementa, se prueban los `TC-*`.
7. `sync-sdd --baseline` fija el estado de referencia.

## Referencias

- `08-skills-y-validadores.md` — cómo se ejecutan las comprobaciones.
- `11-cierre-y-auditoria.md` — criterio de cierre.
