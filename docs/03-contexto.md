# 03 — El contexto normativo

## Qué es

`context/` contiene los documentos que describen **cómo es el sistema y qué
reglas no se pueden violar**. Es la verdad del repositorio: si el código
contradice el contexto, el código está mal.

## Por qué existe

Sin contexto normativo, el agente deduce la arquitectura de lo que ve: imports,
nombres de carpetas y comentarios sueltos. Eso produce tres problemas:

1. **Normaliza la deuda:** si el código tiene un atajo, el agente lo repite.
2. **No distingue intención de realidad:** no sabe qué es un error y qué una
   decisión.
3. **No tiene criterio de rechazo:** no puede decir "esto no encaja aquí".

El contexto le da criterio: qué es inmutable, qué es negociable y qué está
prohibido.

## Archivos implicados

| Archivo | Responde a | Obligatorio |
|---|---|---|
| `system_identity.md` | Qué rol adopta el agente y cómo decide | Sí |
| `harness_governance.md` | Reglas del propio arnés | Sí |
| `project_overview.md` | Qué es el producto y qué queda fuera | Sí |
| `architecture_rules.md` | Fronteras, dependencias e invariantes | Sí |
| `project_structure.md` | Topología física del repositorio | Sí |
| `coding_standards.md` | Estilo, tipos y errores | Sí |
| `testing_guidelines.md` | Qué se prueba y qué es evidencia | Sí |
| `security_privacy.md` | Datos, secretos y superficie | Sí |
| `platform_matrix.md` | Plataformas y restricciones | Sí |
| `glossary.md` | Vocabulario compartido | Sí |
| `sdd_framework.md` | Gobernanza de especificaciones | Sí |
| `ui-design-system.md` | Índice del sistema de diseño | Sí |

La lista es configurable en `context.required` de `harness.config.yaml`.

## Mecánica interna

### Jerarquía de verdad

```
context/ y scopes/  →  módulo vivo y propuesta aprobada  →  contratos y código  →  documentación auxiliar
```

La contradicción se resuelve hacia arriba, nunca inventando una tercera regla.

### Una regla, un archivo

Cada norma vive en un único documento. El resto la referencia. Si una regla
aparece dos veces, una de las dos copias está mintiendo y se borra.

### Longitud útil

Un documento de contexto debe poder leerse en menos de cinco minutos. Si crece
por encima, se divide por tema, no se convierte en un manual.

## Qué valida el arnés

`check_context` comprueba, para cada archivo declarado:

| Regla | Qué detecta |
|---|---|
| `CONTEXT-MISSING-FILE` | Falta un documento obligatorio |
| `CONTEXT-INSUFFICIENT-CONTENT` | Documento vacío o de relleno (< 200 caracteres) |
| `CONTEXT-PENDING-MARKERS` | Marcadores de trabajo sin resolver |
| `CONTEXT-LEGACY-TERMS` | Términos del proyecto anterior |
| `AGENTS-MISSING-REFERENCE` | El enrutador no apunta a la gobernanza |

## Qué rompe si falta

- El agente no sabe qué está prohibido y propone soluciones inválidas.
- Dos sesiones distintas producen arquitecturas distintas.
- Las revisiones discuten gustos en lugar de reglas.
- Los errores de diseño se repiten con nombres nuevos.

## Anti-patrón

Contexto written como tutorial: párrafos explicativos, ejemplos de código
extensos y motivación. Eso pertenece a `docs/`. El contexto es normativo:
afirmaciones cortas, verificables y accionables.

## Cómo escribir un documento de contexto

1. Una frase que diga qué decide ese documento.
2. Una lista de reglas en imperativo, cada una verificable.
3. Una tabla de "puede / no puede" cuando haya fronteras.
4. Un cierre con prohibiciones explícitas.
5. Cero ejemplos de código salvo que el tipo exacto sea la regla.

## Referencias

- `04-scopes.md` — el contexto dice qué; los scopes dicen dónde.
- `11-cierre-y-auditoria.md` — cómo se audita el contexto.
