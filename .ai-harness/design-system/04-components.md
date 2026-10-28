# 04 — Componentes

Inventario de componentes del sistema (`DS-*`). Cada componente declara
anatomía, estados, tamaños y comportamiento de foco. Los valores concretos se
referencian por token.

---

## 1. Convención

```
DS-<ÁMBITO>-<NOMBRE>
```

Ámbitos: `LAYOUT` (estructura), `NAV` (navegación), `INPUT` (entrada),
`FEEDBACK` (estado), `CONTENT` (presentación de datos).

## 2. Ficha obligatoria por componente

| Campo | Contenido |
|---|---|
| ID | `DS-<ÁMBITO>-<NOMBRE>` |
| Propósito | Qué problema resuelve, en una frase |
| Anatomía | Partes que lo componen |
| Estados | `default`, `focus`, `pressed`, `disabled`, `loading`, `error` |
| Tamaños | Variantes permitidas y su uso |
| Tokens | Tokens consumidos, por nombre |
| Foco | Cómo entra, cómo se mueve y cómo se activa |
| Accesibilidad | Etiqueta, rol y anuncio de estado |

## 3. Inventario mínimo

| ID | Propósito |
|---|---|
| `DS-LAYOUT-PAGE` | Contenedor de pantalla con área segura y cabecera opcional |
| `DS-LAYOUT-SECTION` | Agrupación con título y acción opcional |
| `DS-NAV-RAIL` | Navegación principal persistente |
| `DS-NAV-TABS` | Navegación entre vistas hermanas |
| `DS-INPUT-BUTTON` | Acción primaria, secundaria y destructiva |
| `DS-INPUT-FIELD` | Entrada de texto con etiqueta y error |
| `DS-INPUT-TOGGLE` | Alternancia booleana |
| `DS-FEEDBACK-EMPTY` | Estado vacío con explicación y acción |
| `DS-FEEDBACK-ERROR` | Error con causa y recuperación |
| `DS-FEEDBACK-LOADING` | Carga con esqueleto o indicador |
| `DS-CONTENT-CARD` | Elemento de lista con imagen, título y metadatos |
| `DS-CONTENT-LIST` | Secuencia navegable de tarjetas |

## 4. Reglas de componentes

1. Un componente no conoce reglas de negocio ni acceso a datos.
2. Todo componente interactivo define su estado de foco.
3. Un componente nuevo se documenta antes de usarse en una pantalla.
4. Prohibido crear un componente que duplique la función de otro del inventario.
5. Los estados `loading` y `error` son obligatorios si el componente depende de
   datos asíncronos.

## 5. Anatomía de referencia

```
[contenedor]
├── [icono]          opcional
├── [etiqueta]       obligatoria
├── [descripción]    opcional
└── [acción]         opcional
```

El orden es estable; las variantes cambian tamaño y énfasis, no la estructura.
