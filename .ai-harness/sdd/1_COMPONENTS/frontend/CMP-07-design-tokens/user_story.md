# Design Tokens y Tema — Historia de Usuario

## Problema

Hoy el color, la tipografía y el foco están descritos en un documento, pero no existen como código. Sin una implementación verificable, cada pantalla puede inventar valores y romper la coherencia entre TV, móvil y escritorio.

## Actores

- Equipo de UI que construye las pantallas de FLIK.
- Usuario de TV que necesita contraste y foco visible a tres metros.
- Usuario de móvil que necesita legibilidad y objetivos táctiles correctos.

## Necesidad

Como equipo de producto,
quiero un tema único generado a partir de los tokens aprobados,
para que ninguna pantalla defina estilos propios y todas se vean y se comporten igual.

## Resultado esperado

- Un único paquete de tema en `lib/app/theme/` que expone color, tipografía, espacio, radios, movimiento, foco y layout.
- Un test que falla si el tema y `tokens.json` divergen.
- Un test de contraste que impide combinaciones por debajo de AA.
- Cero valores de color fuera de `lib/app/theme/`.

## Criterios de negocio

| ID | Criterio |
|---|---|
| `US-01` | Cambiar un token en el sistema exige cambiar el tema y el test lo detecta. |
| `US-02` | Un widget no puede declarar color ni tamaño literal. |
| `US-03` | El foco se ve igual en todas las pantallas. |
| `US-04` | El tema funciona en TV, escritorio y móvil sin bifurcar la lógica. |

## Fuera de alcance

- Tema claro.
- Componentes de interfaz (van en `CMP-09`).
- Pantallas (van en `CMP-10` a `CMP-16`).
