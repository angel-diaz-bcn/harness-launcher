# 06 — Sistema de diseño y tokens

## Qué es

El sistema de diseño es la autoridad visual del proyecto. `tokens.json` contiene
los **únicos valores** admitidos (color, tipografía, espacio, radio, movimiento,
layout) y los seis documentos de `design-system/` explican su semántica y su
correspondencia con el código.

## Por qué existe

Sin sistema de diseño:

- cada pantalla inventa su escala de espaciado;
- el foco se implementa de cinco maneras distintas;
- cambiar un color requiere buscar y reemplazar en todo el repositorio;
- el agente elige valores "razonables" que rompen el contraste.

Con tokens, un cambio visual es un cambio de dato con una única fuente.

## Archivos implicados

| Archivo | Contiene | No contiene |
|---|---|---|
| `design-system/tokens.json` | Valores canónicos | Semántica |
| `design-system/README.md` | Reglas duras y versionado | Valores |
| `01-foundations.md` | Principios, roles y accesibilidad | Valores |
| `02-tokens.md` | Convención de nombres y reglas de cambio | Valores |
| `03-layout.md` | Breakpoints, rejilla, área segura | Valores |
| `04-components.md` | Inventario `DS-*` y estados | Estilos concretos |
| `05-pages.md` | Blueprint funcional por pantalla | Estilos |
| `06-code-mapping.md` | Token → clase → widget → spec → test | Tokens nuevos |
| `context/ui-design-system.md` | Índice normativo y reglas transversales | Anatomías |

## Mecánica interna

### Cadena de autoridad

```
tokens.json  →  tema del código  →  componente  →  módulo de UI  →  test
   valores          clases            DS-*          MOD-ui         TC-*
```

Cada eslabón es verificable:

- un token sin clase en el tema es un token muerto;
- una clase sin token es una invención;
- un componente sin ficha en `04-components.md` está fuera de inventario;
- una spec de UI sin `design_ref` está incompleta;
- un token sin test de paridad está sin verificar.

### Foco como requisito

El foco no es decoración: es cómo se usa el producto sin ratón. Por eso:

- todo control declara su comportamiento de foco;
- el orden de foco sigue el orden visual;
- el foco nunca queda atrapado ni se pierde al navegar;
- el estado de foco es visible sin hover.

## Qué valida el arnés

`preflight/04_ui_tokens` aplica:

| Regla | Qué detecta |
|---|---|
| `UI-HARDCODED-COLOR` | Colores literales fuera de la capa de tema |
| `UI-FOCUS-MISSING` | La feature de navegación no implementa foco |

La feature que concentra la navegación se declara en `ui.token_feature` de
`harness.config.yaml`; si está vacía, el segundo check se desactiva.

Complementariamente, el proyecto debe mantener un **test de paridad** que compare
`tokens.json` con el tema y un **test de contraste** que verifique AA.

## Qué rompe si falta

- Inconsistencia visual entre pantallas y plataformas.
- El agente introduce valores nuevos en cada cambio.
- El foco deja de funcionar en TV o con teclado y nadie lo detecta.
- Cambiar la marca se convierte en una auditoría manual.

## Anti-patrón

```dart
// Mal
color: const Color(0xFF3B7BF6),
fontSize: 17,
```

```dart
// Bien
color: AppColors.accent,
textStyle: AppTypography.body,
```

El segundo ejemplo no es "más limpio": es la única forma de que el cambio de
marca sea un cambio de dato.

## Cómo adaptarlo a tu proyecto

1. Define los roles antes que los valores (qué significa `surface.elevated`).
2. Rellena `tokens.json` con valores reales y verifica contraste.
3. Materializa los tokens en el tema del código.
4. Escribe `06-code-mapping.md` con símbolos reales.
5. Añade el test de paridad.
6. Declara `ui.token_feature` si hay navegación por foco.
7. Versiona el sistema en `design-system/README.md`.

## Referencias

- `08-skills-y-validadores.md` — cómo se ejecuta `preflight`.
- `03-contexto.md` — el índice normativo del diseño.
