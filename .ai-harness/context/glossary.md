# Glosario

Vocabulario compartido. Un término ambiguo genera specs contradictorias, así que
cada palabra con significado de negocio o de arquitectura se define aquí.

---

## 1. Términos de arnés

| Término | Definición |
|---|---|
| **Arnés** | Conjunto de reglas, contexto, specs, memoria y validadores que restringen y guían el trabajo del agente |
| **Contexto** | Documento normativo de `context/`; es la verdad del sistema |
| **Scope** | Límite de escritura de un bloque: qué rutas puede tocar y cuáles no |
| **Spec** | Contrato técnico en `<ID>-<slug>.spec.md` con front matter y trazabilidad |
| **Historia de usuario** | Brief de producto (`user_story.md`); responde al porqué |
| **Trazabilidad** | Cadena `FR/ST → CT → archivo::símbolo → TC` que une requisito, contrato, código y prueba |
| **Modo de fallo** | Error recurrente documentado con síntoma, riesgo, prevención y verificación |
| **ADR** | Registro inmutable de una decisión de arquitectura |
| **Skill** | Herramienta ejecutable del arnés con manifiesto, runner y documentación |
| **Puerta de validación** | Validador que debe pasar para cerrar un cambio |

## 2. Términos de SDD

| Término | Definición |
|---|---|
| `CMP-NN` | Identificador de componente |
| `PRC-NN` | Identificador de proceso |
| `FR-NN` | Requisito funcional de un componente |
| `ST-NN` | Paso observable de un proceso |
| `BR-NN` | Regla de negocio |
| `INV-NN` | Invariante que nunca puede violarse |
| `CT-NN` | Contrato de datos |
| `TC-NN` | Caso de prueba |
| `AC-NN` | Criterio de aceptación |
| `US-NN` | Criterio de negocio de la historia de usuario |
| `DRAFT` | Spec en elaboración; no se implementa |
| `APPROVED` | Spec aprobada; el código debe cumplirla |
| `SUPERSEDED` | Spec reemplazada; apunta a su sustituta |

## 3. Términos de arquitectura

| Término | Definición |
|---|---|
| **Feature** | Slice funcional vertical con sus capas internas |
| **Core** | Infraestructura transversal sin lógica de negocio |
| **Composition root** | Punto único donde se ensamblan dependencias |
| **API pública** | Superficie que una feature expone a otras: barrel o carpeta `public/` |
| **DTO** | Objeto de transferencia entre fuente de datos y dominio |
| **Entidad** | Objeto del dominio con identidad y reglas |
| **Caso de uso** | Operación de negocio con entrada y salida tipadas |
| **Contrato** | Interfaz o tipo que define qué se promete, no cómo se cumple |
| **Invariante** | Propiedad que debe cumplirse siempre, en todo estado |

## 4. Términos de diseño

| Término | Definición |
|---|---|
| **Token** | Valor visual con nombre y rol, definido en `tokens.json` |
| **Foco** | Elemento que recibe la entrada del teclado o D-Pad |
| **Área segura** | Zona donde el contenido no se recorta por overscan o notch |
| **Blueprint** | Estructura funcional de una pantalla, sin valores visuales |

## 5. Términos de producto

`<Añadir aquí el vocabulario específico del dominio: entidades, roles, estados,
unidades de medida y sinónimos aceptados.>`

## 6. Regla de uso

- Si un término del código no aparece aquí, o falta el término o sobra el
  concepto.
- Prohibido usar dos palabras para el mismo concepto en documentos distintos.
- Un sinónimo aceptado se registra explícitamente como tal.
