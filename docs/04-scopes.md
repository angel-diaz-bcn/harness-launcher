# 04 — Scopes: límites de escritura

## Qué es

Un scope es un documento que autoriza a escribir en **unas rutas concretas** y
prohíbe el resto. Es el equivalente a los permisos de un sistema de archivos,
pero aplicado al agente.

## Por qué existe

El contexto dice *qué* es correcto; el scope dice *dónde* se aplica. Sin scopes,
el agente puede:

- tocar código de otra feature "porque era más rápido";
- crear carpetas nuevas que nadie ha diseñado;
- editar la capa de presentación para arreglar un problema de datos.

Los scopes convierten esos atajos en violaciones detectables.

## Archivos implicados

| Archivo | Rutas autorizadas |
|---|---|
| `block_core.md` | `lib/core/` |
| `block_domain.md` | `lib/features/<feature>/domain`, `data`, `application` |
| `block_ui.md` | `lib/app/`, `lib/features/<feature>/presentation`, `assets/` |

La lista se declara en `scopes.required` de `harness.config.yaml`; las rutas
autorizadas, en `scopes.path_roots`.

## Mecánica interna

Cada scope tiene la misma estructura:

```
Identidad   → nombre, dominio, rutas autorizadas, consumidores, estado
Propósito   → para qué existe el bloque
Posee       → qué contiene y de qué es responsable
No posee    → qué le está explícitamente vedado
Rutas       → árbol de directorios autorizado
Comprobaciones → lista de verificación manual o automática
```

Regla de oro: **un archivo pertenece a un único scope**. Si dos scopes reclaman
la misma ruta, la arquitectura está mal definida.

## Qué valida el arnés

`check_context` aplica estas reglas a cada scope declarado:

| Regla | Qué detecta |
|---|---|
| `SCOPE-MISSING-AUTHORIZED-PATH` | El scope no cita ninguna ruta de `path_roots` |
| `SCOPE-FORBIDDEN-PATH` | El scope menciona una ruta prohibida del proyecto anterior |
| `SCOPE-INSUFFICIENT-CONTENT` | Documento vacío o de relleno |

Y en la capa de código, `preflight` verifica que las fronteras se respetan:

| Regla | Qué detecta |
|---|---|
| `ARCH-CORE-IMPORTS-FEATURE` | `lib/core/` importa una feature |
| `ARCH-CROSS-FEATURE-IMPORT` | Una feature importa los internals de otra |
| `ARCH-PERSISTENCE-LEAK` | Persistencia fuera de su feature propietaria |
| `ARCH-FRAMEWORK-LEAK` | Una feature framework-free importa el framework de UI |
| `TAMPER-HARNESS-MODIFIED` | Intento de modificar validadores, contextos o configuración del arnés |

## Qué rompe si falta

- El agente escribe en la capa que le resulta más cómoda.
- Las features se acoplan entre sí y aparecen dependencias circulares.
- La lógica de negocio se filtra a la presentación.
- Nadie puede revisar un cambio sin leer todo el repositorio.

## Anti-patrón

Un scope que autoriza "todo el repositorio":

```markdown
| Rutas autorizadas | `lib/` |
```

Eso no es un límite, es una declaración de intenciones. Un scope útil nombra
subcarpetas concretas y enumera lo que no posee.

## Cómo escribir un scope

1. Identifica el bloque funcional, no la carpeta.
2. Enumera las rutas exactas que posee.
3. Enumera explícitamente lo que **no** posee (esto es lo que más protege).
4. Define sus consumidores.
5. Añade comprobaciones verificables.

## Referencias

- `03-contexto.md` — las reglas que el scope acota.
- `08-skills-y-validadores.md` — cómo se aplican los checks.
