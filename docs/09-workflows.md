# 09 — Workflows: comandos invocables

## Qué es

Un workflow es un procedimiento corto que se invoca desde el menú `/` del editor
o del agente. No contiene lógica: describe el protocolo, la skill que se ejecuta
y cómo interpretar el resultado.

## Por qué existe

Las skills saben ejecutar; los workflows saben **cuándo** hacerlo y **qué hacer**
con la salida. Separarlos evita dos problemas:

- duplicar la lógica en cada llamada;
- obligar al agente a recordar el orden de las puertas de validación.

## Archivos implicados

| Archivo | Comando | Propósito |
|---|---|---|
| `bootstrap-harness.md` | `/bootstrap-harness.md` | Inicialización interactiva del arnés para un nuevo proyecto |
| `list-skills.md` | `/list-skills.md` | Inventario real de skills, sin listas hardcodeadas |
| `propose-change.md` | `/propose-change.md` | Propuesta de cambio aislada (delta OpenSpec) |
| `consolidate-change.md` | `/consolidate-change.md` | Consolidación y archivo de spec aprobada |
| `harness-validator.md` | `/harness-validator.md` | Validación estructural del arnés |
| `preflight.md` | `/preflight.md` | Validación de código y arquitectura |
| `sync-sdd.md` | `/sync-sdd.md` | Deriva spec ↔ implementación |
| `launch-app.md` | `/launch-app.md` | Arranque de la app (stack Flutter) |
| `git-publish.md` | `/git-publish.md` | Publicación bajo petición explícita |

## Mecánica interna

### Anatomía

```markdown
# Workflow — <nombre>

## Disparador
Cuándo debe usarse.

## Protocolo
1. Comando exacto.
2. Cómo interpretar la salida.
3. Qué hacer si falla.

## Reglas
Lo que no se puede hacer aunque parezca cómodo.
```

### Descubrimiento

El agente descubre los workflows en `.clinerules/workflows/`. El nombre del
comando incluye la extensión `.md`. Si un workflow no aparece en el menú, hay que
recargar la ventana del editor: no es un problema del archivo.

### Orden de las puertas

```
harness-validator  →  preflight  →  sync-sdd  →  (publicación)
```

`git-publish` ejecuta las puertas antes de publicar: no se puede saltar la
validación y subir.

### Guard de commit

`skills/pre-commit-hook.py` es un hook opcional que ejecuta `harness-validator`
y `preflight` antes de permitir un commit. Se instala copiándolo en
`.git/hooks/pre-commit` con permisos de ejecución.

## Qué valida el arnés

Los workflows no se validan como estructura, pero sí su coherencia:

- `check_skills` falla si un workflow cita una skill inexistente en el registro.
- `list-skills.md` exige leer `registry.yaml` en lugar de duplicar la lista.

## Qué rompe si falta

- Cada persona ejecuta las comprobaciones en un orden distinto.
- El agente invoca skills sin saber cuándo ni con qué parámetros.
- La publicación ocurre sin validar.
- Aparecen comandos documentados que no existen.

## Anti-patrón

Un workflow que reimplementa la lógica:

```markdown
## Protocolo
1. Ejecuta `flutter analyze`.
2. Ejecuta `flutter test`.
3. Revisa los imports...
```

Eso pertenece a la skill. El workflow solo debe decir: ejecuta `preflight` e
interpreta el resultado.

## Referencias

- `08-skills-y-validadores.md` — qué hace cada skill por dentro.
- `11-cierre-y-auditoria.md` — el cierre completo.
