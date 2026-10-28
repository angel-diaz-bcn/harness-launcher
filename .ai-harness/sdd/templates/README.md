# Convención de especificaciones SDD

Reglas de nombrado, estructura, front matter y trazabilidad de todas las specs
del arnés. Las plantillas de esta carpeta son obligatorias.

---

## 1. Nombre de archivo

```
<ID>-<slug>.spec.md
```

- `ID`: `CMP-NN` (componente) o `PRC-NN` (proceso).
- `slug`: `kebab-case`, sin acentos, espacios ni mayúsculas.

Patrón verificable:

```regex
^(CMP|PRC)-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.spec\.md$
```

Los prefijos y el front matter obligatorio se declaran en `harness.config.yaml`
(`sdd.component_prefix`, `sdd.process_prefix`, `sdd.frontmatter`). El validador
construye la regex a partir de esa configuración.

Prohibido: `spec.md` genérico, `CMP-01_spec.md`, nombres sin ID o sin sufijo.

---

## 2. Estructura de carpeta

```
.ai-harness/sdd/
├── 1_COMPONENTS/<capa>/<ID>-<slug>/
│   ├── user_story.md
│   └── <ID>-<slug>.spec.md
├── 2_PROCESSES/<ID>-<slug>/
│   ├── user_story.md
│   └── <ID>-<slug>.spec.md
└── templates/
```

- La carpeta y el archivo comparten el mismo `<ID>-<slug>`.
- Una pantalla puede agrupar componentes en `components/`.
- No se admiten specs sueltas en la raíz de `1_COMPONENTS/` ni `2_PROCESSES/`.

---

## 3. Front matter obligatorio

| Campo | Valor |
|---|---|
| `spec_id` | `<ID>-<slug>`; debe coincidir con el nombre del archivo |
| `spec_type` | `CMP` o `PRC` |
| `name` | Nombre legible |
| `layer` | `bootstrap`, `domain` o `ui` (solo componentes) |
| `target` | Ruta real o planificada en el repositorio |
| `block` | Bloque o feature propietaria |
| `status` | `DRAFT`, `APPROVED` o `SUPERSEDED` |
| `version` | Semver interno de la spec |
| `owner` | Responsable de la spec |
| `last_reviewed` | Fecha ISO |
| `approved_at` | Fecha ISO o `null` mientras sea `DRAFT` |
| `approved_by` | Persona o rol, o `null` |
| `supersedes` | IDs reemplazados |
| `superseded_by` | Obligatorio si `status: SUPERSEDED` |
| `user_story` | `user_story.md` |

Reglas que valida el arnés:

- `APPROVED` exige `approved_at` y `approved_by`.
- `SUPERSEDED` exige `superseded_by` no vacío.
- `target` de una spec aprobada debe existir en disco.

---

## 4. Trazabilidad obligatoria

```
FR-* / ST-* → CT-* → archivo::símbolo → TC-* → estado
```

- Componentes usan `FR-NN` (requisito funcional).
- Procesos usan `ST-NN` (paso).
- `CT-NN` son contratos de datos; `TC-NN` son casos de prueba.
- La sección `Mapa de implementación` es obligatoria y debe citar `FR|ST`,
  `CT` y `TC`.
- Todo símbolo público implementado lleva el comentario `/// Spec: <ID> / <FR|ST>`.

---

## 5. Relación `user_story.md` ↔ spec

| Archivo | Responde a | No contiene |
|---|---|---|
| `user_story.md` | ¿Por qué? ¿Para quién? ¿Qué resultado? | Contratos, campos, estados, código |
| `<ID>-<slug>.spec.md` | ¿Qué? ¿Cómo? ¿Con qué contratos y pruebas? | Una segunda historia de usuario |

La historia usa criterios `US-*`; cada `US-*` se mapea a uno o más `FR-*`/`ST-*`.

---

## 6. Checklist de aprobación

- [ ] El nombre cumple el patrón y coincide con la carpeta.
- [ ] El front matter está completo y sin marcadores pendientes.
- [ ] Cada `FR-*`/`ST-*` tiene criterio y prueba.
- [ ] Cada `CT-*` define tipos completos.
- [ ] El mapa de implementación apunta a rutas y símbolos reales.
- [ ] Los escenarios BDD cubren éxito, error y caso borde.
- [ ] No hay valores visuales literales.
- [ ] El estado es coherente con la implementación real.

---

## 7. Plantillas

- `TEMPLATE_COMPONENT_SDD.md` — componentes `CMP-NN`.
- `TEMPLATE_PROCESS_SDD.md` — procesos `PRC-NN`.

Una spec que no siga su plantilla se considera inválida.
