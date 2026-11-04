# Reglas de integración del agente con el arnés

## 1. Autoridad y Jerarquía
`AGENTS.md` es el enrutador maestro del repositorio. El agente no puede
contradecir, omitir ni relajar las reglas de `AGENTS.md`, del contexto normativo
ni de los scopes activos.

---

## 2. Modus operandi

1. **Carga JIT obligatoria:** Antes de leer código o proponer cambios, ejecutar en orden estricto la secuencia de lectura de `AGENTS.md` §1.
2. **Fronteras de Escritura:** Identificar el scope correspondiente en `.ai-harness/scopes/block_*.md` y escribir **exclusivamente** dentro de sus rutas autorizadas.
3. **SDD-First estricto:** Prohibido implementar código de producción sin una spec `.spec.md` en estado `APPROVED`.
4. **Cero asunciones:** Si falta un dato o requerimiento, registrarlo como pregunta abierta en §15/§16 y detener la implementación hasta aclararlo.
5. **Cambios estructurales:** Si la tarea modifica la estructura del arnés (scopes, prefijos o reglas), empezar siempre por `harness.config.yaml`.

---

## 3. Despacho de workflows

El agente descubre los workflows en `.clinerules/workflows/`. El comando del
menú `/` es el nombre del archivo, incluida la extensión `.md`:

- `/list-skills.md`: Descubrimiento e inventario de herramientas.
- `/create-component-sdd.md`: Andamiaje para nuevos componentes.
- `/create-process-sdd.md`: Andamiaje para flujos y procesos.
- `/harness-validator.md`: Validación de integridad normativa del arnés.
- `/sync-sdd.md`: Sincronización criptográfica entre specs y código.
- `/preflight.md`: Puerta de calidad de arquitectura y código.
- `/launch-app.md`: Arranque de la aplicación localmente.
- `/git-publish.md`: Publicación segura en Git (solo bajo demanda explícita).

---

## 4. Terminal, herramientas y salida

- Ejecutar comandos atómicos y no interactivos.
- No encadenar diagnósticos largos en una sola orden salvo error explícito.
- No volcar trazas completas innecesariamente; resumir el resultado para mantener limpio el contexto.
- Usar las herramientas nativas del entorno para lectura y edición de archivos.
- No usar paginadores interactivos (`less`, `more`) ni redirecciones complejas innecesarias.

---

## 5. Pruebas, diagnóstico y corrección autónoma

- Ejecutar los tests de forma atómica y con salida acotada.
- Si un comando o validador falla, leer el archivo señalado por la traza antes de proponer una corrección.
- Diagnosticar la causa raíz, editar y volver a verificar sin pedir asistencia manual innecesaria.
- Iterar hasta que la suite pase o se alcance un límite arquitectónico evidente y se justifique.

---

## 6. Prohibiciones no negociables

- Prohibido código de producción sin spec aprobada.
- Prohibido el uso de librerías de backend, proxy remoto o servicios que la arquitectura no declara.
- Prohibida la telemetría de usuario, tracking de eventos o analítica invasiva.
- Prohibido ejecutar `git push` o publicación remota sin instrucción explícita del usuario.
- Prohibido el uso de colores HEX o estilos visuales literales fuera de `design-system/tokens.json`.
- Prohibido desactivar o puentear validadores (`--no-verify`) para hacer pasar un cambio.
