"""
Design System Generator: Genera la suite completa de 6 documentos de diseño
con el estándar de calidad de FLIK + tokens.json estructurado.
"""

from __future__ import annotations

import json
from models import BootstrapManifest, StackType


class DesignSystemGenerator:
    """Genera .ai-harness/design-system/ con las 6 especificaciones y tokens.json."""

    def __init__(self, manifest: BootstrapManifest) -> None:
        self.manifest = manifest

    def generate_all(self) -> dict[str, str]:
        return {
            "01-foundations.md": self._foundations(),
            "02-tokens.md": self._tokens_doc(),
            "03-layout.md": self._layout(),
            "04-components.md": self._components(),
            "05-pages.md": self._pages(),
            "06-code-mapping.md": self._code_mapping(),
            "README.md": self._readme(),
            "tokens.json": self._tokens_json(),
        }

    def _tokens_json(self) -> str:
        m = self.manifest
        is_dark = m.ui.theme_preference == "dark"

        tokens = {
            "version": "1.0.0",
            "theme": m.ui.theme_preference,
            "colors": {
                "brand": {
                    "primary": "#2563EB",
                    "deep": "#1E40AF",
                    "glow": "#3B82F6"
                },
                "surface": {
                    "background": "#0B0F19" if is_dark else "#F8FAFC",
                    "panel": "#111827" if is_dark else "#FFFFFF",
                    "card": "#1F2937" if is_dark else "#F1F5F9",
                    "overlay": "rgba(0, 0, 0, 0.75)"
                },
                "accent": {
                    "active": "#3B82F6",
                    "hover": "#60A5FA",
                    "focus": "#93C5FD"
                },
                "border": {
                    "subtle": "#374151" if is_dark else "#E2E8F0",
                    "strong": "#4B5563" if is_dark else "#CBD5E1",
                    "focus": "#60A5FA"
                },
                "text": {
                    "primary": "#F9FAFB" if is_dark else "#0F172A",
                    "secondary": "#9CA3AF" if is_dark else "#475569",
                    "muted": "#6B7280" if is_dark else "#94A3B8",
                    "inverse": "#0B0F19" if is_dark else "#FFFFFF"
                },
                "status": {
                    "success": "#10B981",
                    "warning": "#F59E0B",
                    "error": "#EF4444",
                    "info": "#3B82F6"
                }
            },
            "typography": {
                "fontFamily": "Inter, system-ui, sans-serif",
                "scale": {
                    "display": {"size": 36, "lineHeight": 44, "weight": 700},
                    "titleLarge": {"size": 24, "lineHeight": 32, "weight": 700},
                    "titleMedium": {"size": 20, "lineHeight": 28, "weight": 600},
                    "bodyLarge": {"size": 16, "lineHeight": 24, "weight": 400},
                    "bodyMedium": {"size": 14, "lineHeight": 20, "weight": 400},
                    "label": {"size": 12, "lineHeight": 16, "weight": 600}
                }
            },
            "spacing": {
                "xs": 4,
                "sm": 8,
                "md": 16,
                "lg": 24,
                "xl": 32,
                "xxl": 48
            },
            "radii": {
                "sm": 4,
                "md": 8,
                "lg": 16,
                "pill": 999
            },
            "focus": {
                "borderWidth": 2,
                "scaleMultiplier": 1.05,
                "glowRadius": 8
            },
            "motion": {
                "durationFastMs": 150,
                "durationNormalMs": 250,
                "easing": "cubic-bezier(0.4, 0, 0.2, 1)"
            }
        }
        return json.dumps(tokens, indent=2, ensure_ascii=False)

    def _foundations(self) -> str:
        m = self.manifest
        return f"""# {m.identity.name} — Fundamentos Visuales y de Interacción

Principios visuales obligatorios. Los valores concretos viven en `tokens.json`; aquí se define el significado de cada rol.

---

## 1. Principios visuales de {m.identity.name}

1. **Claridad sobre adorno:** La información crítica manda; la interfaz se retira para dar protagonismo al contenido.
2. **Contraste accesible:** Ratios de contraste WCAG AA obligatorios (mínimo 4.5:1 para texto normal).
3. **Foco inequívoco:** Todo elemento interactivo tiene un estado enfocado nítido mediante borde, escala o halo.
4. **Respuesta inmediata:** Animaciones cortas y funcionales (150-250 ms), sin rebotes ni demoras.
5. **Consistencia semántica:** Los colores no se eligen por estética libre, sino por el rol funcional que desempeñan.

---

## 2. Roles de color

| Rol | Significado funcional | Dónde se usa |
|---|---|---|
| `brand` | Identidad corporativa de {m.identity.name} | Logo, iconos de marca, detalles destacados |
| `surface` | Elevación y planos de fondo | Lienzo principal, tarjetas, paneles laterales, modales |
| `accent` | Acción e interacción | Botones primarios (CTA), enlaces activos, indicadores de progreso |
| `border` | Delimitación estructural | Separadores, bordes de contenedor y anillo de foco |
| `text` | Jerarquía de lectura | Títulos, párrafos, subtítulos y textos secundarios |
| `status` | Comunicación del sistema | Mensajes de éxito, advertencia y error |

---

## 3. Modelo de foco y accesibilidad

- Todo control seleccionable debe soportar foco por teclado (Tab / Flechas) o mando a distancia (D-Pad).
- **Prohibido:** Indicar el foco únicamente con un sutil cambio de color. Debe haber un borde visible de al menos 2 px o elevación.
- Al navegar hacia atrás, el foco debe regresar al elemento que originó la apertura del diálogo o pantalla previa.
"""

    def _tokens_doc(self) -> str:
        m = self.manifest
        return f"""# {m.identity.name} — Especificación de Tokens

Catálogo descriptivo de las variables de diseño declaradas en `tokens.json`.

---

## 1. Tokens de Color

- `colors.surface.background`: Color del lienzo base de la aplicación.
- `colors.surface.panel`: Superficie para tarjetas, listas y contenedores.
- `colors.accent.active`: Color de la acción principal del usuario.
- `colors.border.focus`: Color reservado para el anillo de foco interactivo.
- `colors.status.error`: Color para validaciones fallidas y alertas de error.

---

## 2. Tokens de Espaciado

| Token | Valor (dp / px) | Uso habitual |
|---|---|---|
| `spacing.xs` | 4 | Separación interna entre iconos y texto |
| `spacing.sm` | 8 | Espaciado entre elementos compactos de una lista |
| `spacing.md` | 16 | Padding estándar de tarjetas y contenedores |
| `spacing.lg` | 24 | Márgenes entre secciones de una pantalla |
| `spacing.xl` | 32 | Márgenes exteriores de vista en escritorio / TV |

---

## 3. Tokens de Tipografía

- `display`: Títulos destacados y números de gran formato.
- `titleLarge`: Encabezados de pantalla principal.
- `titleMedium`: Títulos de tarjetas y secciones modulares.
- `bodyLarge`: Párrafos de lectura principal.
- `bodyMedium`: Metadatos, etiquetas secundarias y textos de ayuda.
"""

    def _layout(self) -> str:
        m = self.manifest
        return f"""# {m.identity.name} — Sistema de Layout y Zonas de Pantalla

Estructura de cuadrícula, zonas de navegación y diseño adaptativo.

---

## 1. Zonas estructurales de pantalla

```
┌────────────────────────────────────────────────────────┐
│ TopBar / Barra Superior (Logo, título, perfil/acciones)│
├──────────────┬─────────────────────────────────────────┤
│ SideNav      │ Área de Contenido Principal (Body)      │
│ (Navegación  │                                         │
│ lateral      │ - Sección Hero o Resumen                │
│ o filtros)   │ - Cuadrícula / Lista de tarjetas        │
│              │                                         │
├──────────────┴─────────────────────────────────────────┤
│ Barra inferior / Footer (Estado del sistema o acciones)│
└────────────────────────────────────────────────────────┘
```

---

## 2. Reglas de diseño adaptativo

1. **Móvil (< 600 dp):** Layout vertical a una sola columna; navegación inferior (`BottomNavigationBar`).
2. **Tablet / Escritorio (600 - 1200 dp):** Barra lateral de navegación compacta y cuadrícula de 2 a 3 columnas.
3. **Pantalla ancha / TV (> 1200 dp):** Márgenes laterales generosos (48 dp), foco espacial optimizado para lectura a 3 metros.
"""

    def _components(self) -> str:
        m = self.manifest
        return f"""# {m.identity.name} — Catálogo de Componentes de Interfaz

Especificación anatómica y estados interactivos de los componentes base.

---

## 1. Botón de Acción (`Button`)

- **Variantes:** `Primary`, `Secondary`, `Outline`, `Text`.
- **Estados obligatorios:**
  - `Default`: Fondo base según variante.
  - `Hover / Focused`: Borde exterior de 2 px (`border.focus`) y ligera escala (+5 %).
  - `Pressed`: Reducción visual sutil de elevación.
  - `Disabled`: Opacidad al 40 %, sin respuesta al foco ni eventos.

---

## 2. Tarjeta de Contenido (`Card`)

- **Anatomía:** Contenedor con `surface.panel`, radio `radii.md`, padding `spacing.md`.
- **Comportamiento:** Interactiva o informativa. Si es interactiva, adopta anillo de foco en selección.

---

## 3. Barra Superior (`TopBar`)

- **Contenido:** Logotipo de {m.identity.name}, título de pantalla actual y acciones principales.
- **Altura fija:** 56 dp en móvil, 64 dp en escritorio/TV.

---

## 4. Campo de Entrada (`InputField`)

- **Anatomía:** Borde `border.subtle`, texto en `text.primary`, placeholder en `text.muted`.
- **Estado de error:** Borde en `status.error` acompañado de mensaje de texto inferior explicativo.
"""

    def _pages(self) -> str:
        m = self.manifest
        return f"""# {m.identity.name} — Especificación de Pantallas (Pages)

Estructura de las vistas principales del sistema.

---

## 1. Pantalla Principal (`HomeScreen`)

- **Propósito:** Vista de entrada del usuario y presentación general del contenido.
- **Estructura:**
  - Header con identidad de {m.identity.name}.
  - Sección destacada con el elemento principal o estado del sistema.
  - Filas de tarjetas o lista de elementos recientes.

---

## 2. Pantalla de Detalle / Operación (`DetailScreen`)

- **Propósito:** Gestión o visualización detallada de una entidad del dominio.
- **Estructura:**
  - Botón de retorno (con foco inicial asegurado).
  - Bloque de información con tipografía `titleLarge`.
  - Panel de acciones (Guardar, Editar, Eliminar, Iniciar proceso).

---

## 3. Pantalla de Configuración (`SettingsScreen`)

- **Propósito:** Preferencias de usuario, política de privacidad y estado del sistema.
- **Estructura:**
  - Lista de opciones agrupadas por categoría (General, Privacidad, Conexión).
"""

    def _code_mapping(self) -> str:
        m = self.manifest
        is_flutter = m.stack.stack_type in (StackType.FLUTTER, StackType.DART)
        folder = "lib" if is_flutter else "src"

        code_example = ""
        if is_flutter:
            code_example = """```dart
// Mapeo a ThemeExtension en Flutter
class AppTokens extends ThemeExtension<AppTokens> {
  final Color background;
  final Color surface;
  final Color accent;
  // ...
}
```"""
        else:
            code_example = """```typescript
// Mapeo a constantes en TypeScript
export const AppTokens = {
  colors: {
    background: '#0B0F19',
    surface: '#111827',
    accent: '#3B82F6',
  },
  spacing: { md: 16 },
} as const;
```"""

        return f"""# {m.identity.name} — Mapeo de Tokens a Código

Guía para trasladar las especificaciones de `design-system/` a código ejecutable.

---

## 1. Ubicación de clases de tema

Todo el consumo de tokens debe centralizarse en:
`{folder}/core/theme/` o `{folder}/app/theme/`

{code_example}

---

## 2. Regla de oro para desarrolladores y agentes de IA

- **Prohibido:** Usar colores directos en widgets o componentes.
- **Obligatorio:** Consumir siempre el tema semántico del arnés.
"""

    def _readme(self) -> str:
        m = self.manifest
        return f"""# Sistema de Diseño de {m.identity.name}

Este directorio contiene las especificaciones visuales canónicas del producto:

1. `01-foundations.md` — Principios visuales, roles de color y foco.
2. `02-tokens.md` — Diccionario semántico de variables.
3. `03-layout.md` — Cuadrículas, márgenes y navegación adaptativa.
4. `04-components.md` — Especificación de botones, tarjetas, inputs y diálogos.
5. `05-pages.md` — Estructura de vistas principales de la aplicación.
6. `06-code-mapping.md` — Mapeo entre especificación y código de producción.
7. `tokens.json` — Valores exactos exportables para compilación o tooling.
"""
