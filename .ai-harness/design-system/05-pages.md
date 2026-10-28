# 05 — Páginas

Blueprint funcional de cada pantalla: qué muestra, en qué orden, con qué
estados y cómo se navega. No contiene valores visuales.

---

## 1. Ficha obligatoria por página

| Campo | Contenido |
|---|---|
| Nombre | Ruta o identificador de la pantalla |
| Objetivo | Qué consigue el usuario aquí |
| Plantilla | `single`, `list-detail`, `hub` o `immersive` |
| Componentes | `DS-*` que la componen |
| Datos | Contratos de los que depende |
| Estados | Carga, vacío, error, sin permisos |
| Foco | Entrada, recorrido y salida |
| Salida | A dónde puede ir el usuario |

## 2. Estructura de una página `single`

```
[área segura]
├── [cabecera]      título + acción opcional
├── [contenido]     secciones apiladas
└── [acción fija]   opcional
```

## 3. Estructura de una página `list-detail`

```
[lista]  →  [detalle]
             ├── [cabecera]      volver + título
             ├── [resumen]
             └── [acciones]
```

Regla: la selección en la lista se conserva al volver del detalle.

## 4. Estructura de una página `hub`

```
[cabecera]
├── [sección destacada]
├── [sección horizontal]  ← foco se mueve en un eje
└── [sección horizontal]
```

Regla: el foco nunca salta entre secciones sin pasar por sus elementos.

## 5. Estados obligatorios

Toda pantalla que consume datos remotos declara:

1. **Carga:** qué se muestra mientras no hay datos.
2. **Vacío:** por qué no hay datos y qué puede hacer el usuario.
3. **Error:** causa legible y acción de recuperación.
4. **Sin permisos:** qué falta y cómo obtenerlo.

## 6. Reglas de páginas

1. Una página compone componentes; no implementa lógica de negocio.
2. La página declara sus dependencias de datos; no las crea.
3. Prohibido duplicar una página con variantes mínimas: se parametriza.
4. La navegación de salida es explícita y reversible.
5. El blueprint se mantiene actualizado: es la referencia de la spec de pantalla.
