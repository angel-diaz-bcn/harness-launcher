# Workflow — Inicialización y Adaptación del Arnés (Bootstrap)

## Propósito

Inicializa o adapta todo el arnés para un nuevo proyecto a partir de documentación previa en `.ai-harness/input/`, del análisis del código existente o mediante entrevista guiada asistida por el modelo de IA.

---

## Protocolo Asistido por Modelo de IA (Recomendado)

Cuando el agente de IA colabora con el usuario para montar el arnés:

1. **Paso 1: Ingesta del Dominio Real**
   - El agente lee la documentación depositada en `.ai-harness/input/` (o le pide al usuario una breve explicación del producto).
   - Extrae:
     - Nombre y propuesta de valor.
     - Stack tecnológico real (`Python`, `Node/TypeScript`, `Flutter/Dart`, `Go`).
     - Arquetipo: `GUI_APP`, `BACKEND_API`, `CLI_TOOL`, `LIBRARY`.
     - Features/Módulos reales del negocio (ej. `auth`, `catalog`, `orders`).
     - Identidad visual / tokens reales (si existen) o especificación de que no aplica UI.

2. **Paso 2: Generación del Manifiesto Enriquecido**
   - En lugar de forzar preguntas rígidas por terminal, la IA redacta un archivo de manifiesto canónico en `.ai-harness/input/manifest.yaml` con toda la información técnica real.

3. **Paso 3: Compilación Inicial del Andamiaje (Scaffolding)**
   - El agente lanza la generación automática:
   ```bash
   python .ai-harness/skills/bootstrap-harness/runner.py --manifest .ai-harness/input/manifest.yaml
   ```
   - El compilador genera la estructura completa del arnés, scopes, andamiaje de diseño y configuración estructural.

4. **Paso 4: Adaptación Semántica Profunda (OBLIGATORIO PARA EL AGENTE DE IA)**
   - **Regla de Oro:** Las plantillas generadas por el compilador sirven **únicamente como estructura y referencia de calidad** para evitar archivos incompletos o mal formateados. **El agente de IA DEBE modificar y adaptar totalmente los ficheros generados para incorporar todo el contenido real del proyecto** depositado en `.ai-harness/input/`:
     - **`context/project_overview.md` y `architecture_rules.md`:** Incorporar las reglas de arquitectura reales del PRD (invariantes, FSMs, topes de coste, kill switches, fronteras de capas, integraciones y persistencia).
     - **`context/security_privacy.md` y `platform_matrix.md`:** Detallar las políticas de seguridad, secretos y las plataformas y entornos reales.
     - **`context/glossary.md`:** Incorporar el vocabulario y términos del dominio del PRD en la sección correspondiente.
     - **`design-system/` (si el producto tiene UI):** Reescribir `03-layout.md` (filosofía de layout real, densidad por píxel, streaming/SSE si aplica), `04-components.md` (inventario de componentes visuales reales del PRD) y `05-pages.md` (blueprint exacto de las páginas/pantallas del producto, ej. Grid de 4 cuadrantes).
     - **`memory/failure_modes.md` y `ADR-0001` a `ADR-0003`:** Personalizar los modos de fallo y decisiones técnicas según el stack y la lógica de negocio real.
     - **`sdd/modules/*.md`:** Completar requerimientos (`FR-*`), tipos y contratos funcionales según la especificación del negocio.
   - **Cero plantillas vacías:** El bootstrap NO se considera completado si los documentos contienen descripciones esquemáticas o componentes genéricos no pertenecientes al producto.

5. **Paso 5: Verificación Inmediata con Quality Gates**
   - El agente ejecuta las puertas de calidad:
   ```bash
   python .ai-harness/skills/harness-validator/runner.py
   python .ai-harness/skills/preflight/runner.py
   python .ai-harness/skills/sync-sdd/runner.py
   ```
   - Todas las puertas deben devolver código de salida `0` (`PASSED`).

---

## Modo Manual Interactivo (Terminal)

Para desarrolladores que prefieran responder manualmente por consola:
```bash
python .ai-harness/skills/bootstrap-harness/runner.py --interactive
```

---

## Reglas de Gobernanza

- **Cero Invención:** Prohibido inventar colores, tipografías o paquetes que no hayan sido proporcionados por el usuario o extraídos del PRD.
- **SDD-First:** Las specs semilla iniciales se generan con todas las secciones de las plantillas canónicas completas.
- **AGENTS.md:** Se mantiene estrictamente como router sin reglas de negocio embebidas.
- **Git Push:** Solo se publica bajo instrucción explícita del usuario.
