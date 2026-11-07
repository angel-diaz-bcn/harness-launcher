"""
Design System Generator: Genera la suite completa de .ai-harness/design-system/ y tokens.json
adaptada al 100% al producto, arquetipo y stack tecnológico (Web, Tailwind, CSS nativo o Flutter).
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from models import BootstrapManifest, StackType


class DesignSystemGenerator:
    """Genera la suite completa de diseño totalmente adaptada al producto y stack."""

    def __init__(self, manifest: BootstrapManifest, harness_dir: Path | None = None) -> None:
        self.manifest = manifest
        launcher_root = Path(__file__).resolve().parents[3]
        self.canonical_ds_dir = launcher_root / "design-system"
        self.harness_dir = Path(harness_dir).resolve() if harness_dir else launcher_root

    def _get_ui_scope_slug(self) -> str:
        m = self.manifest
        for s in m.scopes:
            s_name = s.name.lower()
            s_desc = (s.description or "").lower()
            if any(k in s_name or k in s_desc for k in ("console", "ui", "presentation", "dashboard", "frontend", "visual")):
                return s.name
        return m.scopes[0].name if m.scopes else "ui"

    def generate_all(self) -> dict[str, str]:
        m = self.manifest
        today = datetime.now().strftime("%Y-%m-%d")

        if not m.ui.has_ui:
            return {
                "README.md": f"# Sistema de Diseño y Contratos — {m.identity.name}\n\nEste producto es un `{m.identity.archetype.value}` sin interfaz gráfica. No aplica tokens.json visual.\n",
                "01-foundations.md": f"# Fundaciones de API — {m.identity.name}\n\nDiseño centrado en contratos tipados, idempotencia y respuestas HTTP/CLI predecibles.\n",
                "02-tokens.md": f"# Diccionario de Formatos — {m.identity.name}\n\nConvención de serialización JSON, timestamps UTC en ISO-8601 y errores RFC 7807.\n",
                "03-layout.md": "# No aplica (sin UI)\n",
                "04-components.md": "# Controladores y Adaptadores (sin UI)\n",
                "05-pages.md": "# Endpoints y Comandos (sin UI)\n",
                "06-code-mapping.md": "# Mapeo de Contratos a Código\n",
                "tokens.json": json.dumps({"version": "1.0.0", "has_ui": False, "note": "Backend / CLI API - No visual tokens required"}, indent=2),
            }

        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        ui_scope = self._get_ui_scope_slug()

        files = {
            "README.md": self._build_readme(today, is_flutter, ui_scope),
            "01-foundations.md": self._build_foundations(is_flutter),
            "02-tokens.md": self._build_tokens_doc(is_flutter),
            "03-layout.md": self._build_layout(is_flutter),
            "04-components.md": self._build_components(is_flutter),
            "05-pages.md": self._build_pages(is_flutter),
            "06-code-mapping.md": self._build_code_mapping(is_flutter, ui_scope),
            "tokens.json": self._resolve_tokens_json(),
        }

        # Aplicar overrides semánticos enriquecidos de la IA si existen en el manifiesto
        overrides: dict[str, str] = {}
        if hasattr(m, "custom_design_overrides") and m.custom_design_overrides:
            overrides.update(m.custom_design_overrides)
        if hasattr(m.ui, "custom_design_overrides") and m.ui.custom_design_overrides:
            overrides.update(m.ui.custom_design_overrides)

        for doc_key, custom_text in overrides.items():
            clean_key = Path(doc_key).name
            if clean_key in files and custom_text and custom_text.strip():
                # Reemplazar variables comunes si las hubiera
                resolved = custom_text.strip()
                resolved = resolved.replace("<PROYECTO>", m.identity.name)
                resolved = resolved.replace("<YYYY-MM-DD>", today)
                files[clean_key] = resolved

        return files

    def _build_readme(self, today: str, is_flutter: str, ui_scope: str) -> str:
        m = self.manifest
        css_fw = getattr(m.ui, "css_framework", "tailwind")
        tech_desc = "Flutter (Widgets canónicos)" if is_flutter else f"Web ({css_fw.capitalize()} / Variables CSS)"
        nav_desc = "D-Pad y cruceta de control remoto" if m.ui.focus_navigation_required else "teclado estándar accesible (Tab, Shift+Tab, Enter) y puntero táctil"

        return f"""# Sistema de Diseño — {m.identity.name}

> Autoridad de diseño y presentación visual del proyecto. Define fundamentos, tokens, layout responsivo,
> componentes reutilizables (`DS-*`) y su correspondencia con el código fuente ({tech_desc}).

---

## 1. Qué es y qué no es

Este directorio es el **detalle normativo** del sistema de diseño para **{m.identity.name}**.
`context/ui-design-system.md` es el índice normativo que enruta aquí y conserva las reglas transversales de calidad.

- `tokens.json` es la **única fuente de valores** (color, tipografía, espacio, radios, movimiento, layout).
- `02-tokens.md` define **semántica y roles**, nunca valores numéricos directos.
- Las especificaciones de UI referencian tokens **por nombre**; nunca copian HEX ni tamaños literales.
- El código de producción materializa estos tokens en la capa de estilos/tema (`{m.ui.css_framework}`).

Este sistema **no** define comportamiento de producto ni contratos de datos; estos viven en OpenSpec (`.ai-harness/sdd/modules/{ui_scope}.md`).

---

## 2. Orden de Lectura

| # | Archivo | Responde a |
|---|---|---|
| 1 | `01-foundations.md` | Identidad, color, tipografía, forma, foco, movimiento y accesibilidad |
| 2 | `02-tokens.md` | Convención de nombres, rol de cada token y reglas de cambio |
| 3 | `tokens.json` | Valores canónicos estructurados machine-readable |
| 4 | `03-layout.md` | Breakpoints responsivos, rejilla y márgenes seguros |
| 5 | `04-components.md` | Inventario `DS-*`: anatomía, estados y comportamiento |
| 6 | `05-pages.md` | Blueprint funcional de cada pantalla y distribución espacial |
| 7 | `06-code-mapping.md` | Token → clase/variable → elemento web/widget → spec → test |

---

## 3. Reglas Duras de Diseño

1. **Prohibido** escribir colores o tamaños literales fuera de la capa de tema. `preflight` lo bloquea de inmediato (`UI-HARDCODED-COLOR`).
2. Un token que no existe en `tokens.json` **no se usa**: primero se añade formalmente al sistema, después al código.
3. Los valores de `tokens.json` y el tema del código deben coincidir exactamente; un test de paridad lo verifica.
4. El foco es comportamiento, no decoración: todo control tiene estado de foco visible y navegable mediante {nav_desc}.
5. Las specs de UI declaran `design_ref: .ai-harness/context/ui-design-system.md` y referencian tokens por nombre.
6. Ningún cambio visual se fusiona sin actualizar atómicamente `tokens.json`, el mapeo de código y la versión del sistema.

---

## 4. Versionado

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | {today} | Inicialización del sistema de diseño de {m.identity.name}: fundamentos, tokens, componentes y mapeo. |
"""

    def _build_foundations(self, is_flutter: bool) -> str:
        m = self.manifest
        nav_text = """- Todo control interactivo es alcanzable con teclado estándar (Tab, Enter, Escape, Flechas) o puntero táctil según WCAG AA.
- El estado de foco es visible con un indicador nítido de alto contraste mientras el elemento permanezca activo.
- El orden de tabulación sigue el flujo visual lógico; nunca se salta contenido ni se atrapa al usuario en un bucle.""" if not m.ui.focus_navigation_required else """- Todo control interactivo es alcanzable mediante D-Pad / mando a distancia direccional y activable con Enter o Select.
- La matriz de foco bidimensional no contiene callejones sin salida ni saltos asimétricos."""

        return f"""# 01 — Fundamentos de Diseño — {m.identity.name}

Principios visuales y directrices semánticas del sistema. Los valores numéricos viven exclusivamente en `tokens.json`; aquí se especifica **qué significa cada rol**.

---

## 1. Principios Rectores

1. **Contraste antes que estética:** Todo texto cumple WCAG AA (ratio mínimo 4.5:1) sobre su superficie de fondo.
2. **Jerarquía por escala, no por color:** La escala tipográfica y el peso semántico ordenan la lectura visual.
3. **Superficies en capas:** Fondo base (`canvas`), superficie contenedora (`surface`) y elementos elevados (`elevated`). Nada flota sin motivo.
4. **Color semántico acotado:** Paleta optimizada para modo `{m.ui.theme_preference}`, reservando el color de acento para acciones primarias e interacción.
5. **Movimiento con propósito:** Transiciones cortas (120ms - 240ms) para retroalimentar cambios de estado sin retrasar al usuario.
6. **Foco visible permanente:** El indicador de foco es un requisito funcional de accesibilidad, nunca un adorno prescindible.

---

## 2. Jerarquía de Color por Rol Semántico

| Rol | Propósito |
|---|---|
| `colors.background.primary` | Fondo base de la aplicación |
| `colors.background.surface` | Contenedores, tarjetas, paneles y barras laterales |
| `colors.background.surface_hover` | Estado interactivo sobre superficies elevadas |
| `colors.background.border` | Separadores y líneas divisorias de baja intensidad |
| `colors.text.primary` | Texto principal de alta legibilidad |
| `colors.text.secondary` | Etiquetas, descripciones secundarias y metadatos |
| `colors.text.muted` | Elementos inactivos o deshabilitados |
| `colors.brand.primary` | Color maestro de marca y acciones principales |
| `colors.brand.danger` | Alertas destructivas, kill switches y errores fatales |
| `colors.brand.success` | Confirmaciones de estado positivo y métricas en alza |
| `colors.brand.warning` | Avisos de riesgo o advertencias presupuestarias |

---

## 3. Tipografía

- Familia tipográfica principal sans-serif de alta densidad de información.
- Familia monoespaciada para logs, datos cuantitativos, claves y comandos.
- Escala tipográfica cerrada: `display`, `title`, `headline`, `body`, `caption`.
- Interlineado mínimo de 1.2 en titulares y 1.4 en texto de lectura continuo.

---

## 4. Forma y Radios

- Radios declarados en tokens: `sm` (4px), `md` (8px), `lg` (12px), `full` (9999px).
- La elevación espacial se transmite mediante contraste cromático de superficies y sombras suaves, no mediante bordes excesivamente gruesos.

---

## 5. Foco y Accesibilidad

{nav_text}
- Prohibido depender exclusivamente de estados `hover` para revelar información crítica o disparar acciones principales.
- Todos los iconos con significado funcional cuentan con etiqueta descriptiva accesible (`aria-label`).
"""

    def _build_tokens_doc(self, is_flutter: bool) -> str:
        m = self.manifest
        antipatterns = """- Códigos HEX (`#...`) o valores RGB literales hardcodeados en HTML, componentes o estilos en línea.
- Clases utilitarias con valores arbitrarios (ej. `text-[17px]` o `bg-[#0B0E14]`) fuera de la escala de `tokens.json`.
- Margen o espaciado arbitrario fuera de la escala `space.*`.
- Uso de colores de marca para fondos de grandes bloques de texto afectando la legibilidad.""" if not is_flutter else """- `Color(0xFF...)` hardcodeado directamente en un Widget.
- `fontSize: 17` fuera de la escala tipográfica de `tokens.json`.
- `EdgeInsets.all(13)` con valores arbitrarios no alineados a la escala de espaciado.
- Duplicar el mismo valor cromático en dos tokens con nombres distintos."""

        return f"""# 02 — Tokens Semánticos — {m.identity.name}

Semántica y reglas de uso de los tokens. **Este documento no contiene valores**: los valores viven en `tokens.json`.

---

## 1. Convención de Nombres

```
<grupo>.<subgrupo>.<rol>
```

Ejemplos: `colors.background.primary`, `spacing.md`, `typography.font_family_sans`, `radius.lg`.

Reglas de nomenclatura:
- Los identificadores describen el **rol semántico**, nunca el valor literal (`primary`, no `blue600`).
- Un token nuevo no puede duplicar el propósito de otro existente.
- Prohibido renombrar un token sin actualizar simultáneamente `06-code-mapping.md` y la capa de estilos.

---

## 2. Grupos de Tokens

| Grupo | Contenido Semántico | Prohibición |
|---|---|---|
| `colors` | Superficies, texto, bordes, marcas y estados | Valores sueltos sin rol asignado |
| `typography` | Familias, escala de tamaños, pesos e interlineados | Tamaños puntuales inventados para una sola vista |
| `spacing` | Escala modular de márgenes y paddings | Márgenes asimétricos no justificados |
| `radius` | Curvaturas de borde estandarizadas | Radios caprichosos por elemento |
| `motion` | Duraciones y curvas de transición | Animaciones bloqueantes o infinitas |

---

## 3. Anti-Patrones Estrictamente Prohibidos

{antipatterns}
"""

    def _build_layout(self, is_flutter: bool) -> str:
        m = self.manifest
        return f"""# 03 — Layout y Distribución Espacial — {m.identity.name}

Breakpoints responsivos, cuadrícula y comportamiento del contenido para {m.identity.name}.

---

## 1. Breakpoints Responsivos

El sistema está diseñado para adaptarse fluidamente a tres anchos de pantalla fundamentales:

| Dispositivo / Pantalla | Ancho de Referencia | Disposición de Columnas | Margen Lateral Seguro |
|---|---|---|---|
| **Móvil (Smartphones)** | `< 640px` | 1 columna vertical | `16px` (`spacing.md`) |
| **Tablet / Portátil compacto** | `640px - 1024px` | 2 a 4 columnas | `24px` (`spacing.lg`) |
| **Escritorio / Monitor amplio** | `> 1024px` | 12 columnas (máx. 1440px) | `32px` (`spacing.xl`) |

---

## 2. Rejilla y Espaciado

- La rejilla se basa en un múltiplo modular de **4px / 8px**.
- Todo espaciado entre contenedores, botones y campos se deriva de `spacing.xs`, `spacing.sm`, `spacing.md`, `spacing.lg` o `spacing.xl`.
- Ancho de contenido óptimo acotado para mantener la legibilidad de textos largos (máximo 75 caracteres por línea).

---

## 3. Comportamiento del Scroll

- El contenedor principal desplaza el contenido verticalmente de forma suave.
- Prohibido el scroll horizontal accidental o no intencionado en resoluciones estándar.
- Las cabeceras de navegación y paneles de control permanecen anclados o accesibles durante el scroll.
"""

    def _build_components(self, is_flutter: bool) -> str:
        m = self.manifest
        rows = [
            "| `DS-LAYOUT-CONTAINER` | Contenedor Principal | Envoltura responsiva con ancho máximo y padding seguro | `default` |",
            "| `DS-NAV-HEADER` | Barra Superior de Navegación | Cabecera con logotipo, estado operativo y accesos principales | `default`, `sticky` |",
            "| `DS-INPUT-BUTTON` | Botón de Acción | Disparador de acciones primarias, secundarias y destructivas | `default`, `hover`, `focus`, `disabled`, `loading` |",
            "| `DS-FEEDBACK-ALERT` | Banner Contextual | Notificación con variante semántica (info, warning, danger, success) | `info`, `warning`, `danger`, `success` |",
            "| `DS-DATA-TABLE` | Tabla de Datos | Lista estructurada de registros con cabecera y ordenación | `default`, `empty`, `loading` |",
        ]

        if m.ui.key_components:
            for kc in m.ui.key_components:
                slug_kc = re.sub(r"([A-Z])", r"-\1", kc).strip("-").upper()
                rows.append(f"| `DS-DATA-{slug_kc}` | {kc} | Componente especializado del producto para {m.identity.name} | `default`, `active`, `loading` |")

        table_content = "\n".join(rows)

        return f"""# 04 — Componentes Visuales del Sistema (`DS-*`) — {m.identity.name}

Inventario canónico de componentes reutilizables de {m.identity.name}.
Cada componente define su propósito, anatomía, estados y tokens consumidos.

---

## 1. Convención de Identificadores

```
DS-<ÁMBITO>-<NOMBRE>
```

Ámbitos: `LAYOUT` (estructura), `NAV` (navegación), `INPUT` (acciones y controles),
`FEEDBACK` (alertas, loaders, estados vacíos), `DATA` (métricas, tablas, feeds).

---

## 2. Inventario de Componentes Canónicos

| ID | Nombre | Propósito | Estados |
|---|---|---|---|
{table_content}

---

## 3. Reglas de Construcción

1. **Aislamiento Funcional:** Los componentes `DS-*` no contienen lógica de red ni acceso directo a bases de datos; reciben datos y eventos vía propiedades/atributos.
2. **Accesibilidad Obligatoria:** Todo control interactivo (`BUTTON`, `INPUT`) cuenta con atributos `aria-label`, foco visible con outline nítido y ratio de contraste mínimo 4.5:1 (WCAG AA).
"""

    def _build_pages(self, is_flutter: bool) -> str:
        m = self.manifest
        kc_names = ", ".join([f"`{c}`" for c in m.ui.key_components]) if m.ui.key_components else "Paneles principales"

        return f"""# 05 — Estructura de Páginas y Vistas — {m.identity.name}

Distribución espacial, blueprints de pantalla y flujos de usuario para {m.identity.name}.

---

## 1. Blueprint de Pantalla Principal

```
┌────────────────────────────────────────────────────────────────────────┐
│ DS-NAV-HEADER (Logo, Estado de Servicio, Acciones Rápidas)            │
├────────────────────────────────────────┬───────────────────────────────┤
│ PANEL PRINCIPAL DE ACTIVIDAD / DATOS   │ PANEL LATERAL DE TELEMETRÍA   │
│ - Indicadores KPI de estado            │ - Feeds de actividad en vivo  │
│ - Controles operativos principales     │ - Notificaciones de sistema   │
├────────────────────────────────────────┴───────────────────────────────┤
│ VISTA DETALLADA / TABLA / COMPONENTES CLAVE ({kc_names})              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Principios de Interacción

- **Diseño Libre de Fricción:** Toda acción crítica debe ser ejecutable con un número mínimo de interacciones.
- **Feedback Inmediato:** Las operaciones que impliquen llamadas asíncronas deben reflejar de inmediato un estado de carga visual (`loading`).
- **Resiliencia de Interfaz:** Si un servicio secundario no responde, el resto de la interfaz permanece interactivo con degradación elegante.
"""

    def _build_code_mapping(self, is_flutter: bool, ui_scope: str) -> str:
        m = self.manifest
        css_fw = getattr(m.ui, "css_framework", "tailwind")

        if is_flutter:
            return f"""# 06 — Correspondencia con el Código (Flutter)

Traza cómo cada token visual llega a los Widgets de Flutter.

---

## 1. Cadena de Trazabilidad

```
tokens.json → ThemeData / AppColors → Widget de UI → spec (MOD-{ui_scope}) → test
```

| Token | Propiedad Flutter | Widget | Spec | Test de Paridad |
|---|---|---|---|---|
| `colors.background.primary` | `Theme.of(context).scaffoldBackgroundColor` | `Scaffold` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `colors.text.primary` | `Theme.of(context).textTheme.bodyMedium` | `Text` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `colors.brand.primary` | `Theme.of(context).colorScheme.primary` | `FilledButton` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
"""

        return f"""# 06 — Correspondencia con el Código (Web / {css_fw.capitalize()})

Traza cómo cada token visual llega al código fuente web y cómo se verifica.

---

## 1. Cadena de Trazabilidad

```
tokens.json → variables CSS / clases utilitarias ({css_fw}) → componente web → spec (MOD-{ui_scope}) → test
```

| Token | Clase / Variable ({css_fw}) | Elemento Web | Spec | Test de Paridad |
|---|---|---|---|---|
| `colors.background.primary` | `var(--color-bg-primary)` / `bg-background-primary` | `<body>`, `<main>` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `colors.background.surface` | `var(--color-bg-surface)` / `bg-background-surface` | `<section>`, `.card` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `colors.text.primary` | `var(--color-text-primary)` / `text-text-primary` | `<h1>`, `<p>`, `<span>` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `colors.brand.primary` | `var(--color-brand-primary)` / `bg-brand-primary` | `.btn-primary` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `colors.brand.danger` | `var(--color-brand-danger)` / `text-brand-danger` | `.alert-danger`, `.btn-kill` | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `spacing.md` | `var(--spacing-md)` / `p-4`, `gap-4` | Contenedores y grillas | `MOD-{ui_scope}` | `test_theme_tokens_parity` |
| `typography.font_family_sans` | `var(--font-sans)` / `font-sans` | Raíz tipográfica | `MOD-{ui_scope}` | `test_theme_tokens_parity` |

---

## 2. Reglas de Mapeo

1. **Cero HEX literal en HTML/JS/CSS:** Prohibido escribir códigos de color hexadecimales directos en archivos `.html`, `.vue`, `.tsx`, `.py` o plantillas. Deben consumirse siempre a través de las variables CSS de tokens o clases configuradas.
2. **Actualización atómica:** Cualquier adición o modificación en `tokens.json` debe reflejarse en la hoja de estilos raíz (`tokens.css` o `tailwind.config.js`) y en este documento en el mismo commit.
3. **Verificación automatizada:** El check 04_ui_tokens de `preflight` analiza el código buscando expresiones regulares de color literal y falla la build si se detectan transgresiones.
"""

    def _resolve_tokens_json(self) -> str:
        m = self.manifest
        today = datetime.now().strftime("%Y-%m-%d")
        if m.ui.custom_tokens:
            return json.dumps(m.ui.custom_tokens, indent=2)

        template_tokens = self.canonical_ds_dir / "tokens.json"
        if template_tokens.exists():
            try:
                raw = template_tokens.read_text(encoding="utf-8", errors="ignore")
                raw = raw.replace("<PROYECTO>", m.identity.name).replace("<YYYY-MM-DD>", today)
                data = json.loads(raw)
                if "meta" in data and isinstance(data["meta"], dict):
                    data["meta"]["name"] = f"{m.identity.name} Design Tokens"
                    data["meta"]["updated"] = today
                return json.dumps(data, indent=2)
            except Exception:
                pass

        neutral = {
            "version": "1.0.0",
            "theme": m.ui.theme_preference,
            "has_ui": True,
            "meta": {
                "name": f"{m.identity.name} Design Tokens"
            },
            "colors": {
                "background": {
                    "primary": "#0B0E14" if m.ui.theme_preference == "dark" else "#FFFFFF",
                    "surface": "#121722" if m.ui.theme_preference == "dark" else "#F8FAFC",
                    "border": "#242C3B" if m.ui.theme_preference == "dark" else "#E2E8F0"
                },
                "text": {
                    "primary": "#F8FAFC" if m.ui.theme_preference == "dark" else "#0F172A",
                    "secondary": "#94A3B8" if m.ui.theme_preference == "dark" else "#64748B"
                },
                "brand": {
                    "primary": "#2563EB",
                    "success": "#10B981",
                    "danger": "#EF4444"
                }
            },
            "spacing": {
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px"
            },
            "typography": {
                "font_family_sans": "Inter, system-ui, sans-serif"
            }
        }
        return json.dumps(neutral, indent=2)
