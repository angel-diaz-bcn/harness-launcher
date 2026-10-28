# Reglas de Integración de Cline con el Arnés de FLIK

## 1. Autoridad

`AGENTS.md` es el enrutador operativo del repositorio. Cline no puede contradecir, omitir ni relajar las reglas de `AGENTS.md`, del contexto ni de los scopes activos.

## 2. Modus operandi

- Antes de leer código o proponer cambios, ejecutar la carga JIT de `AGENTS.md` §1.
- Identificar el scope de la tarea y no escribir fuera de sus rutas autorizadas.
- No implementar sin spec `.spec.md` aprobada.
- Si falta información, detenerse y preguntar; no inventar contratos, campos, estados ni dependencias.

## 3. Despacho de workflows

Cline descubre los workflows en `.clinerules/workflows/`. El comando del menú `/` es el nombre del archivo, incluida la extensión `.md`.

- Descubrimiento de herramientas: `.clinerules/workflows/list-skills.md` (`/list-skills.md`).
- Creación de especificaciones: `.clinerules/workflows/create-component-sdd.md` (`/create-component-sdd.md`) y `.clinerules/workflows/create-process-sdd.md` (`/create-process-sdd.md`).
- Validación del arnés: `.clinerules/workflows/harness-validator.md` (`/harness-validator.md`).
- Sincronización spec↔código: `.clinerules/workflows/sync-sdd.md` (`/sync-sdd.md`).
- Validación de producto: `.clinerules/workflows/preflight.md` (`/preflight.md`).
- Arranque de la app: `.clinerules/workflows/launch-app.md` (`/launch-app.md`).
- Publicación Git: `.clinerules/workflows/git-publish.md` (`/git-publish.md`), solo bajo petición explícita.

## 4. Terminal y salida

- Ejecutar comandos atómicos y no interactivos.
- No encadenar diagnósticos largos en PowerShell salvo error explícito.
- No volcar trazas completas; resumir el resultado.
- Usar las herramientas nativas de lectura y edición de archivos.
- No usar paginadores interactivos ni redirecciones innecesarias.

## 5. Pruebas y corrección

- Ejecutar `flutter test` y `flutter test integration_test` de forma atómica.
- Si un comando falla, leer el archivo señalado por el stack trace antes de proponer una corrección.
- Diagnosticar la causa raíz, editar y volver a verificar sin pedir asistencia manual.
- Iterar hasta que la suite pase o se alcance un límite evidente.

## 6. Prohibiciones

- Backend, proxy remoto, CDN de vídeo o transcodificación.
- Telemetría de usuario, analítica remota o publicidad.
- `git push` o publicación automática sin instrucción explícita.
- Colores o estilos fuera de `ui-design-system.md`.
- Código de producción sin spec aprobada.
