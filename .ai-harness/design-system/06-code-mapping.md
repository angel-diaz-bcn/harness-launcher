# 06 — Correspondencia con el código

Traza cómo cada token llega al código y cómo se verifica. Esta tabla es la
prueba de que el sistema de diseño no es documentación muerta.

---

## 1. Cadena de trazabilidad

```
tokens.json → clase del tema → componente → spec → test
```

| Token | Clase del tema | Widget de ejemplo | Spec | Test |
|---|---|---|---|---|
| `color.surface.canvas` | `AppColors.surfaceCanvas` | `Scaffold` | `MOD-ui` | `<TC-NN>` |
| `color.text.primary` | `AppColors.textPrimary` | `Text` | `MOD-ui` | `<TC-NN>` |
| `color.accent.base` | `AppColors.accent` | `FilledButton` | `MOD-ui` | `<TC-NN>` |
| `space.md` | `AppSpacing.md` | `Padding` | `MOD-ui` | `<TC-NN>` |
| `radius.md` | `AppRadius.md` | `Container` | `MOD-ui` | `<TC-NN>` |
| `type.body.size` | `AppTypography.body` | `Text` | `MOD-ui` | `<TC-NN>` |

## 2. Reglas de mapeo

1. Toda fila de la tabla apunta a un símbolo real del código.
2. Un token sin clase asociada es un token muerto: se elimina o se implementa.
3. Un valor en el código sin token es una violación: `preflight` la bloquea.
4. La tabla se actualiza en el mismo cambio que el token o el tema.
5. Los nombres de clase y de token se corresponden de forma mecánica: mismo rol,
   distinta notación (`color.surface.canvas` → `surfaceCanvas`).

## 3. Verificación

| Comprobación | Herramienta |
|---|---|
| Tokens ↔ tema (paridad) | test de paridad |
| Ausencia de literales | `preflight` → `UI-HARDCODED-COLOR` |
| Foco navegable | widget test de recorrido |
| Contraste AA | test de contraste sobre tokens |

## 4. Cuándo se rompe esta cadena

- Se añade un valor directo en un widget.
- Se renombra un token sin tocar el tema.
- Se duplica un componente con estilos propios en lugar de usar `DS-*`.
- Se modifica `tokens.json` sin ejecutar los tests de paridad y contraste.

Cualquiera de los cuatro casos es un fallo de validación, no un detalle de estilo.
