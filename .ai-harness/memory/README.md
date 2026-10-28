# FLIK — Subsistema de Memoria y Decisiones

La memoria del arnés conserva lo aprendido y evita repetir errores.

---

## Componentes

```
memory/
├── failure_modes.md          # Errores recurrentes y su prevención
├── decisions/                # ADRs de arquitectura
├── ephemeral_feedback/       # Logs de la última ejecución fallida
├── sync-state.json           # Línea base generada por sync-sdd (no editar a mano)
└── README.md
```

## Ciclo de auto-corrección

1. `preflight` o `harness-validator` detectan un fallo.
2. El fallo se escribe en `ephemeral_feedback/` con archivo, regla y mensaje.
3. El agente lee el fallo, corrige la causa raíz y vuelve a validar.
4. Si el fallo es recurrente o viola una invariante, se añade a `failure_modes.md`.
5. Si la corrección cambia una decisión de arquitectura, se registra un ADR en `decisions/`.

## Reglas

- Los logs efímeros no sustituyen a `failure_modes.md`.
- Un modo de fallo debe tener síntoma, riesgo, prevención y verificación.
- No se borra un modo de fallo sin justificar que ya no aplica.
- Los ADRs son inmutables: una decisión nueva se añade, no se reescribe la anterior.
- Los logs no contienen tokens, magnets completos, rutas privadas ni datos personales.

## Ubicación de logs

Los logs de fallo van siempre a `memory/ephemeral_feedback/`, nunca a `fixtures/`. `fixtures/` es solo para datos deterministas de prueba.
