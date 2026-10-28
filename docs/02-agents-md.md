# 02 — `AGENTS.md`: el contrato con el agente

## Qué es

`AGENTS.md` es el punto de entrada obligatorio para cualquier agente de IA.
Contiene **solo** el orden de carga, la tabla de enrutamiento, las reglas de
trabajo y el criterio de cierre. No contiene reglas de producto.

## Por qué existe

Un agente necesita saber tres cosas antes de tocar nada:

1. **Qué leer primero** — sin orden, carga archivos al azar y se queda sin
   contexto útil.
2. **Dónde está cada verdad** — sin mapa, busca en el sitio equivocado.
3. **Cuándo ha terminado** — sin criterio, declara éxito sin comprobar nada.

`AGENTS.md` responde a esas tres preguntas en una página. Si crece, algo se ha
puesto donde no toca.

## Archivos implicados

| Archivo | Responsabilidad |
|---|---|
| `AGENTS.md` | Enrutador: carga JIT, mapa de tareas, reglas de trabajo, cierre |
| `.clinerules/rules.md` | Reglas de integración del agente con el arnés |
| `.clinerules/workflows/*.md` | Procedimientos invocables con `/` |

## Mecánica interna

### Carga JIT

La sección §1 define un orden de lectura que va de lo general a lo concreto:

```
identidad → gobernanza → producto → arquitectura → diseño
   → scope de la tarea → framework SDD → spec activa → fallos conocidos
```

Es **just-in-time**: se carga lo necesario para la tarea, en ese orden, no todo
el repositorio. Si falta el scope o la spec, el agente se detiene.

### Enrutamiento

La tabla §2 asocia cada tipo de tarea con su fuente de verdad y su herramienta.
Esto evita dos fallos frecuentes: inventar una fuente nueva y duplicar reglas.

### Regla de tamaño

`AGENTS.md` no debe superar una pantalla y media. Cuando una sección crece, se
mueve a `context/`. El enrutador enruta; no legisla.

## Qué valida el arnés

- `check_context` exige que `AGENTS.md` exista, tenga contenido y reference
  `system_identity.md` y `harness_governance.md` (lista configurable en
  `context.agents_must_reference`).

## Qué rompe si falta

- El agente empieza leyendo código y deduce la arquitectura de los imports.
- Cada sesión elige un orden distinto y omite pasos.
- Las reglas se copian dentro del contrato y se desincronizan.
- Nadie sabe cuándo una tarea está realmente terminada.

## Anti-patrón

```markdown
# AGENTS.md
- Usa siempre el patrón Repository.
- No uses colores hardcodeados.
- La arquitectura es clean architecture con 3 capas.
- Los tests son obligatorios.
```

Esto parece un contrato, pero es una lista de deseos: no dice qué leer, ni
dónde está la verdad, ni cómo se comprueba. Todo eso debe estar en `context/`
y validarse con un check.

## Cómo escribir el tuyo

1. Define el orden de carga (máximo 9 elementos).
2. Haz una tabla tarea → fuente de verdad → herramienta.
3. Enumera 5-10 reglas de trabajo que no puedan vivir en otro sitio.
4. Define el cierre con comandos concretos.
5. Comprueba que ningún párrafo duplica una regla de `context/`.

## Referencias

- `03-contexto.md` — qué contiene cada documento de contexto.
- `09-workflows.md` — cómo se invocan los procedimientos.
