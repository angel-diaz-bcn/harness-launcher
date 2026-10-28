# Registro de Decisiones de Arquitectura (ADR)

Cada decisión relevante se registra en un archivo `ADR-XXXX-<slug>.md`.

## Formato

```markdown
# ADR-XXXX — <Título>

- **Estado:** proposed | accepted | superseded | rejected
- **Fecha:** YYYY-MM-DD
- **Contexto:** <problema y restricciones>
- **Decisión:** <qué se decide>
- **Alternativas:** <opciones evaluadas>
- **Consecuencias:** <ventajas, costes y riesgos>
- **Specs afectadas:** <CMP-NN/PRC-NN>
```

## Reglas

- Una decisión aceptada no se reescribe; se sustituye por otra ADR.
- Toda ADR debe citar las invariantes de `architecture_rules.md` que respeta.
- Las decisiones de producto pendientes se registrarán en la fase de specs.
