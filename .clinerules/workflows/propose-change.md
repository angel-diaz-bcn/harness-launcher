# Workflow — Proponer cambio OpenSpec (propose-change)

## Disparador

Solicitud de una nueva funcionalidad, cambio de regla de negocio o modificación de contrato.

## Protocolo

1. Consultar el módulo afectado en `.ai-harness/sdd/modules/<modulo>.md`.
2. Ejecutar el runner para crear la propuesta aislada:

```bash
python .ai-harness/skills/propose-change/runner.py <slug> --module <MOD-id> --title "<Título>"
```

3. Completar el delta en `.ai-harness/sdd/changes/[YYYY-MM]-[slug]/proposal.md`.
4. Revisar la propuesta con el desarrollador humano antes de escribir código.

## Reglas

- Prohibido tocar los módulos maestros sin propuesta previa aprobada.
- No inventar contratos ni dependencias fuera del scope.
- La revisión de la propuesta debe poder realizarse en menos de 2 minutos.

