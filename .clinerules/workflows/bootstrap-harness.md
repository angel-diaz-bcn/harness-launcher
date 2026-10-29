# Workflow — Inicialización del Arnés (Bootstrap)

## Propósito

Inicializa o reconstruye la configuración y contexto de todo el arnés para un nuevo proyecto a partir de documentación o de una entrevista guiada paso a paso.

## Protocolo

1. Preguntar al usuario si dispone de documentación previa para colocar en `.ai-harness/input/`.
2. Ejecutar la skill en modo interactivo:

```bash
python .ai-harness/skills/bootstrap-harness/runner.py --interactive
```

3. Seguir las 5 fases de descubrimiento:
   - Visión del producto y propuesta de valor.
   - Stack tecnológico y plataformas objetivo.
   - Descomposición modular y scopes autorizados.
   - Sistema de diseño / contratos e invariantes de privacidad.
   - Prevención de fallos (modos de fallo iniciales) y primer ADR.
4. Tras la escritura atómica, la skill ejecuta `harness-validator` y `preflight`.
5. Si alguna validación reporta fallos, resolver la causa raíz de inmediato.

## Reglas

- `AGENTS.md` nunca debe contener reglas de negocio ni de interfaz.
- No ejecutar `git push` tras el bootstrap salvo instrucción explícita del usuario.

