# 🎬 CMP-01 — Catalog JSON Contract

`CMP-01` · `Product brief` · `v1.0` · `catalog` · `DRAFT`

> [!NOTE]
> **En una frase:** FLIK necesita un único contrato JSON para que películas, series, variantes y magnets se interpreten igual en toda la app.

---

## 🎯 Problema

Sin un contrato cerrado, cada módulo podría interpretar el catálogo de forma distinta:

- la UI podría esperar campos que el motor P2P no entiende;
- el parser podría aceptar documentos incompletos;
- un magnet inválido podría llegar hasta la reproducción;
- una serie podría modelarse de forma incompatible con la navegación por temporadas.

El resultado sería una app impredecible y difícil de mantener.

---

## 👥 Actores

| Actor | Qué necesita |
|---|---|
| Usuario de TV, móvil o escritorio | Ver títulos, series, temporadas y variantes sin ambigüedad |
| Catalog Service | Validar y persistir un documento único |
| P2P Engine | Recibir un magnet válido por variante |
| Media Player | Reproducir el flujo local de la variante elegida |
| TV Experience | Presentar películas, series y episodios de forma consistente |

---

## 🧑‍💻 Historia de usuario

> **Como** usuario de FLIK,
> **quiero** que el catálogo tenga una estructura JSON fija y validada,
> **para** que la app muestre siempre los mismos títulos, variantes y magnets sin que cada módulo invente su propio formato.

---

## ✅ Criterios de negocio

| ID | Criterio |
|---|---|
| `US-01` | El catálogo es un documento JSON versionado con un identificador de catálogo y una fecha de generación. |
| `US-02` | Una película puede ofrecer varias variantes para que el usuario tenga alternativas si una falla. |
| `US-03` | Una serie se organiza en temporadas y episodios, y cada episodio puede tener varias variantes. |
| `US-04` | Cada variante contiene un magnet; la identidad P2P se deriva de ese magnet y no se duplica. |
| `US-05` | Un documento con campos desconocidos, datos obligatorios ausentes o magnets inválidos se rechaza completo. |
| `US-06` | El contrato no incluye descarga, caché, sincronización ni reproducción; esas responsabilidades tienen sus propias specs. |

---

## 🚫 Qué NO es esta historia

> [!WARNING]
> No es el parser, ni el repositorio, ni la sincronización, ni la pantalla de catálogo, ni el reproductor. Tampoco incluye canales de TV en directo.

---

## 🔗 Spec técnica

[`CMP-01-catalog-json-contract.spec.md`](CMP-01-catalog-json-contract.spec.md)
