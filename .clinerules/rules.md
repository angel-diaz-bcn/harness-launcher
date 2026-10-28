# Reglas de integración del agente con el arnés

## 1. Autoridad

`AGENTS.md` es el enrutador operativo del repositorio. El agente no puede
contradecir, omitir ni relajar las reglas de `AGENTS.md`, del contexto ni de los
scopes activos.

## 2. Modus operandi

- Antes de leer código o proponer cambios, ejecutar la carga JIT de `AGENTS.md` §1.
- Identificar el scope de la tarea y no escribir fuera de sus rutas autorizadas.
- No implementar sin spec `.spec.md` aprobada.
- Si falta información, detenerse y preguntar; no inventar contratos, campos,
  estados ni dependencias.
- Si la tarea cambia la estructura del arnés, empezar por `harness.config.yaml`.

## 3. Despacho de workflows

El agente descubre los workflows en `.clinerules/workflows/`. El comando del
menú `/` es el nombre del archivo, incluida la extensión `.md`.

- Descubrimiento de herramientas: `.clinerules/workflows/list-skills.md`.
- Creación de especificaciones: `create-component-sdd.md` y `create-process-sdd.md`.
- Validación del arnés: `harness-validator.md`.
- Sincronización spec↔código: `sync-sdd.md`.
- Validación de producto: `preflight.md`.
- Arranque de la app: `launch-app.md`.
- Publicación Git: `git-publish.md`, solo bajo petición explícita.

## 4. Terminal y salida

- Ejecutar comandos atómicos y no interactivos.
- No encadenar diagnósticos largos en una sola orden salvo error explícito.
- No volcar trazas completas; resumir el resultado.
- Usar las herramientas nativas de lectura y edición de archivos.
- No usar paginadores interactivos ni redirecciones innecesarias.

## 5. Pruebas y corrección

- Ejecutar los tests de forma atómica y con salida acotada.
- Si un comando falla, leer el archivo señalado por el stack trace antes de
  proponer una corrección.
- Diagnosticar la causa raíz, editar y volver a verificar sin pedir asistencia
  manual.
- Iterar hasta que la suite pase o se alcance un límite evidente y se explique.

## 6. Prohibiciones

- Backend, proxy remoto o servicios que la arquitectura no declara.
- Telemetría de usuario, analítica remota o publicidad.
- `git push` o publicación automática sin instrucción explícita.
- Colores o estilos fuera de `ui-design-system.md`.
- Código de producción sin spec aprobada.
- Desactivar un validador para hacer pasar un cambio.
