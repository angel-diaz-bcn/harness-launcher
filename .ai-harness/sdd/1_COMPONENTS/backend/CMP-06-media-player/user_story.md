# 🎬 CMP-06 — Media Player

`CMP-06` · `Product brief` · `v1.0` · `player` · `DRAFT`

> [!NOTE]
> **En una frase:** convertir la URL local del motor P2P en una sesión de reproducción controlable, sin descargar, sin catalogar y sin pintar controles.

---

## 🎯 Problema

El motor P2P ya entrega un flujo seekable en loopback, pero nada lo reproduce. Sin reproductor no hay imagen, no hay pistas y no hay posición que guardar.

---

## 👥 Actores

| Actor | Qué necesita |
|---|---|
| Usuario | Que el contenido se vea y responda a play, pausa y seek |
| Motor P2P | Que su flujo se consuma sin descargarlo dos veces ni transcodificarlo |
| Orquestador (`PRC-01`) | Abrir, observar estado y cerrar la sesión sin fugas |
| Sistema | Que no se abran conexiones fuera de la URL local dada |

---

## 🧑‍💻 Historia de usuario

> **Como** usuario de FLIK,
> **quiero** que el contenido empiece a reproducirse en cuanto el motor P2P tiene datos,
> **para** verlo, moverme por la película y cambiar de audio o subtítulos sin esperas ni cortes.

---

## ✅ Criterios de negocio

| ID | Criterio |
|---|---|
| `US-01` | Una URL local válida se convierte en una sesión reproducible. |
| `US-02` | Play, pausa y seek funcionan sin reiniciar el flujo. |
| `US-03` | La posición y la duración se publican de forma continua. |
| `US-04` | Se pueden listar y cambiar pistas de audio y subtítulos. |
| `US-05` | Al terminar o salir, el reproductor libera sus recursos. |
| `US-06` | No se transcodifica ni se descarga nada por cuenta propia. |

---

## 🚫 Qué NO es esta historia

> [!WARNING]
> No es el motor P2P, ni el catálogo, ni la navegación, ni el OSD. No descarga, no resuelve magnets, no guarda progreso y no decide qué contenido reproducir.

---

## 🔗 Spec técnica

[`CMP-06-media-player.spec.md`](CMP-06-media-player.spec.md) · Flujo consumido: [`CMP-05`](../CMP-05-p2p-engine/CMP-05-p2p-engine.spec.md)
