# 08 — Skills y validadores

## Qué es

Las skills son el mecanismo por el que el arnés **deja de ser documentación y
pasa a ser verificación**. Cada skill es un comando determinista con manifiesto,
runner, salida interpretable y documentación.

## Por qué existe

Un arnés solo de Markdown se degrada: nadie lo lee, nadie lo actualiza y las
reglas se contradicen. Las skills dan tres garantías:

1. **Ejecutables:** la regla se comprueba con un comando, no con buena voluntad.
2. **Deterministas:** mismo repositorio, mismo resultado.
3. **Acotadas:** cada skill hace una cosa y devuelve un estado claro.

## Archivos implicados

```
.ai-harness/skills/
├── registry.yaml                 # Inventario canónico
├── harness_config.py             # Carga de configuración y guard de dependencias
├── pre-commit-hook.py            # Guard opcional de commit
└── <skill>/
    ├── skill.yaml                # Manifiesto
    ├── models.py                 # Tipos de resultado (pydantic)
    ├── runner.py                 # CLI
    └── checks/                   # Checks internos
        └── profiles/             # Checks de perfil (opcional)

.agents/skills/<skill>/SKILL.md   # Documentación de uso
```

## Mecánica interna

### Las cinco piezas de una skill

| Pieza | Función | Sin ella |
|---|---|---|
| `skill.yaml` | Declara nombre, versión, entradas, salidas y comando | La skill no es descubrible |
| `runner.py` | Ejecuta y devuelve código de salida | No hay automatización |
| `models.py` | Tipa el resultado y la serialización | La salida es texto libre |
| `checks/` | Divide la lógica por regla | El runner se vuelve inmantenible |
| `SKILL.md` | Explica uso, parámetros y reglas | Nadie sabe invocarla |

Y una sexta, fuera de la carpeta: la entrada en `registry.yaml`. Una skill sin
registro no existe para el arnés.

### Configuración compartida

`harness_config.py` centraliza:

- resolver la ruta de `harness.config.yaml` subiendo desde la raíz;
- fusionar valores por defecto;
- verificar dependencias con un mensaje accionable antes de importar pydantic.

Regla de diseño: **un check nunca hardcodea listas**. Si un check necesita
nombres de contextos, prefijos, features o tokens prohibidos, los lee de la
configuración.

### Contrato de salida

| Campo | Significado |
|---|---|
| `PASSED` | No hay violaciones |
| `WARNING` | Aviso no bloqueante (por ejemplo, check no aplicable) |
| `FAILED` | Violación que bloquea el cierre |
| exit 0 | Sin fallos (o solo warnings) |
| exit 1 | Hay fallos |
| exit 2 | Faltan dependencias del tooling |

Los tres códigos son distintos a propósito: un fallo de entorno no es un fallo
de código.

### Cómo añadir un check

1. Crear `checks/NN_nombre.py` con una función `run(scope_path, strict)`.
2. Devolver un `CheckResult` con `check_name`, `status` y `violations`.
3. Leer todo lo configurable de `harness_config`.
4. Registrar el check en `CATALOG` del runner.
5. Añadir la regla a la documentación: `SKILL.md` y este documento.
6. Verificar que un repositorio sin proyecto devuelve `WARNING`, no `FAILED`.

## Qué valida el arnés

`check_skills` aplica:

| Regla | Qué detecta |
|---|---|
| `SKILL-MISSING-FILE` | Falta `skill.yaml` o `runner.py` |
| `SKILL-MISSING-DOC` | Falta `SKILL.md` en `.agents/skills/` |
| `SKILL-UNREGISTERED` | Skill sin entrada en `registry.yaml` |
| `SKILL-REGISTRY-ORPHAN` | Entrada de registro sin carpeta |
| `SKILL-RUNNER-NO-ENTRYPOINT` | Runner sin `main()` ni `__main__` |
| `SKILL-RUNNER-SYNTAX` | Runner con error de sintaxis |
| `SKILL-COMMAND-MISSING` | El comando del manifiesto apunta a un archivo inexistente |

## Qué rompe si falta

- Las reglas se convierten en recomendaciones.
- Aparecen skills documentadas que nadie puede ejecutar.
- Cada persona valida a mano cosas distintas.
- El agente declara éxito sin evidencia.

## Anti-patrón

Un runner que imprime "OK" sin comprobar nada:

```python
print("✔ Todo correcto")
```

Es peor que no tener skill: genera confianza falsa y desactiva la revisión
humana. Un validador debe poder fallar.

## Catálogo actual

| Skill | Devuelve fallo cuando |
|---|---|
| `harness-validator` | Falta estructura, contenido, front matter o registro |
| `preflight` | Hay violaciones de código, arquitectura, tokens o dependencias |
| `sync-sdd` | Una spec aprobada diverge de su implementación |
| `create-component-sdd` | El identificador, la capa o el target no son válidos |
| `create-process-sdd` | El identificador, el target o la plantilla no son válidos |
| `launch-app` | El proyecto o el dispositivo no están disponibles |
| `git-publish` | Alguna puerta falla o no hay instrucción explícita |

## Referencias

- `09-workflows.md` — cómo se exponen como comandos.
- `11-cierre-y-auditoria.md` — Definition of Done.
