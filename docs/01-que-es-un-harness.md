# 01 — Qué es un arnés y qué problema resuelve

## Qué es

Un arnés es el conjunto de reglas, contexto, especificaciones, memoria y
validadores que restringen y guían el trabajo de un agente de IA sobre un
repositorio. No es un prompt: es un sistema de archivos con reglas explícitas y
comprobaciones ejecutables.

## Por qué existe

Un agente sin arnés falla siempre de las mismas cinco formas:

| Fallo | Qué ocurre | Cómo lo evita el arnés |
|---|---|---|
| **Deriva** | El código crece y la documentación se queda atrás | Specs con trazabilidad y `sync-sdd` |
| **Invención** | El agente inventa campos, estados o dependencias | Protocolo de no invención y preguntas abiertas |
| **Amnesia** | Cada sesión empieza de cero y repite errores | `memory/failure_modes.md` y ADRs |
| **Dispersión** | Escribe en cualquier sitio del repositorio | `scopes/` con rutas autorizadas |
| **Contradicción** | Dos documentos dicen cosas distintas | Jerarquía de verdad y una regla por archivo |

El arnés no hace al agente más listo: hace que sus errores sean **visibles y
corregibles** antes de llegar al repositorio.

## Modelo mental: cuatro capas

```
1. Contrato       AGENTS.md + .clinerules/rules.md
                  → qué debe hacer el agente y en qué orden (Fast-Path vs OpenSpec)

2. Verdad         .ai-harness/context/ + scopes/ + sdd/modules/
                  → qué es cierto del sistema, módulos vivos y dónde se puede escribir

3. Plan           .ai-harness/sdd/changes/ (proposal.md + tasks.md)
                  → deltas aislados de lo que se propone cambiar antes de codificar

4. Verificación   .ai-harness/skills/ + memory/ + CI (.github/workflows)
                  → puertas deterministas y registro de fallos para evitar regresiones
```

Un arnés sano tiene las cuatro capas. Si falta la cuarta, las reglas son
sugerencias. Si falta la primera, el agente improvisa. Si falta la tercera,
el código es la única especificación.

## Qué valida el arnés

El propio arnés se valida a sí mismo: `harness-validator` comprueba que las
cuatro capas existen, están completas y son coherentes.

## Qué rompe si falta

- Sin contrato: el agente decide el orden de trabajo y salta la spec.
- Sin verdad: cada sesión inventa la arquitectura.
- Sin plan: el código se convierte en la especificación y nadie sabe qué sobra.
- Sin verificación: las reglas se degradan en la primera prisa.

## Anti-patrones

- **Arnés como prompt gigante:** todo en un archivo, sin validación, imposible
  de auditar.
- **Arnés decorativo:** documentación extensa que nadie ejecuta.
- **Arnés rígido:** reglas que impiden trabajar y se acaban desactivando.
- **Arnés duplicado:** la misma norma en tres archivos con matices distintos.

## Cómo saber si el tuyo funciona

1. Un agente nuevo puede trabajar sin explicaciones adicionales.
2. Cualquier cambio de comportamiento obliga a tocar una spec.
3. Un error repetido tiene una entrada en memoria.
4. Las comprobaciones se ejecutan en menos de un minuto.
5. Nadie discute qué documento manda: la jerarquía es explícita.

## Referencias

- `02-agents-md.md` — el contrato.
- `03-contexto.md` — la verdad normativa.
- `08-skills-y-validadores.md` — la verificación.
