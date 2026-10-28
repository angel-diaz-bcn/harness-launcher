# 10 — `.gitignore` y `.aiignore`: dos públicos distintos

## Qué es

Son dos archivos con sintaxis parecida y propósito diferente:

| Archivo | Responde a | Lo lee |
|---|---|---|
| `.gitignore` | Qué no debe entrar en el control de versiones | Git |
| `.aiignore` | Qué no debe entrar en el contexto del agente | El asistente de IA |

## Por qué existen por separado

No son intercambiables:

- Un archivo puede **versionarse** y no ser útil para el agente (por ejemplo,
  imágenes de diseño).
- Un archivo puede **no versionarse** y ser necesario para el agente (por
  ejemplo, una nota local con el plan del día).
- Un binario pesado no debe versionarse **ni** leerse: va en ambos.
- Un secreto nunca debe aparecer en ninguno de los dos públicos.

Si usas solo `.gitignore`, el agente leerá artefactos de build y perderá
contexto. Si usas solo `.aiignore`, el repositorio acumulará basura.

## Archivos implicados

| Archivo | Secciones |
|---|---|
| `.gitignore` | Secretos, sistema operativo, IDE, Python, Dart/Flutter, Android, escritorio, builds, medios, logs, estado del arnés |
| `.aiignore` | Las mismas, más el estado local del arnés y `.tools/` |

## Mecánica interna

### Base + apéndices

Ambos archivos siguen el mismo patrón:

```
1. Secretos y credenciales        ← nunca se elimina
2. Sistema operativo y editores
3. Tooling del arnés (Python)
4. Apéndice del stack            ← eliminar si no aplica
5. Builds y binarios
6. Medios y paquetes grandes
7. Logs y volcados
8. Estado local del arnés
```

Al copiar la plantilla a un proyecto con otro stack, se eliminan los apéndices
que no apliquen y se añaden los del stack real.

### Qué debe estar siempre

- `.env` y variantes, salvo `.env.example`.
- Claves, certificados y keystores.
- `*.log`, volcados y artefactos de build.
- `memory/sync-state.json` y `memory/ephemeral_feedback/*`.
- Dependencias instaladas (`.venv/`, `__pycache__/`, `.dart_tool/`).

### Qué no debe estar nunca

- La documentación del producto.
- Las specs y el contexto.
- Los fixtures pequeños y deterministas.

## Qué valida el arnés

No hay check automático de estos archivos, pero sí consecuencias verificables:

- Si un secreto entra en el repositorio, se detecta tarde y caro: la rotación es
  obligatoria.
- Si el agente lee `.dart_tool/` o `node_modules/`, consume contexto inútil y
  responde peor.
- Si `sync-state.json` se versiona, el baseline de `sync-sdd` se contamina entre
  máquinas.

La auditoría es manual y está en `11-cierre-y-auditoria.md`.

## Qué rompe si falta

- Repositorios con binarios de cientos de megabytes.
- Secretos filtrados en el historial.
- El agente pierde el hilo leyendo código generado.
- Diferencias falsas en cada commit por archivos de estado local.

## Anti-patrón

Copiar `.gitignore` a `.aiignore` y no volver a mirarlos.

Son públicos distintos: `.aiignore` debe excluir además todo lo que no aporte
contexto (generados, cachés, artefactos) y `.gitignore` debe excluir todo lo que
no deba publicarse. Mantener ambos con criterio independiente es parte del
trabajo.

## Reglas prácticas

1. Toda excepción (`!ruta`) se documenta en su línea.
2. Un patrón nuevo se añade a la sección de su tecnología, no al final.
3. Un archivo ignorado que haga falta se versiona con `!` y un motivo.
4. Nunca se ignora un archivo necesario para reproducir el build.
5. Los secretos se referencian con `.env.example`, nunca con valores reales.

## Referencias

- `02-agents-md.md` — el contrato que hace relevante `.aiignore`.
- `07-memoria.md` — estado local que no se versiona.
