# 🎬 PRC-01 — Magnet playback

`PRC-01` · `Product brief` · `v1.0` · `playback` · `DRAFT`

> [!NOTE]
> **En una frase:** que elegir un magnet termine en vídeo en pantalla, y que salir deje todo cerrado.

---

## 🎯 Problema

`CMP-05` sabe servir el flujo y `CMP-06` sabe reproducirlo, pero nadie los conecta: falta el orden de apertura, el estado combinado y, sobre todo, el cierre en orden inverso sin dejar el puerto ocupado ni el reproductor vivo.

---

## 👥 Actores

| Actor | Qué necesita |
|---|---|
| Usuario | Elegir un magnet y ver el contenido |
| Motor P2P | Que se cierre después del reproductor |
| Reproductor | Que se le entregue la URL local y se destruya al salir |
| Pantalla | Un estado combinado que pintar y acciones de D-Pad |

---

## 🧑‍💻 Historia de usuario

> **Como** usuario de FLIK,
> **quiero** elegir un magnet y verlo reproducirse,
> **para** disfrutar del contenido sin saber qué es un info-hash ni un puerto local.

---

## ✅ Criterios de negocio

| ID | Criterio |
|---|---|
| `US-01` | Elegir un magnet válido lleva a imagen en pantalla. |
| `US-02` | El estado combinado refleja carga, reproducción, pausa y fin. |
| `US-03` | Salir libera reproductor, sesión P2P y puerto. |
| `US-04` | Un fallo se muestra como error, no como pantalla colgada. |

---

## 🚫 Qué NO es esta historia

> [!WARNING]
> No es el motor P2P, ni el reproductor, ni el catálogo, ni el OSD. No descarga, no decodifica y no decide qué contenido existe.

---

## 🔗 Spec técnica

[`PRC-01-magnet-playback.spec.md`](PRC-01-magnet-playback.spec.md) · Participantes: [`CMP-05`](../../1_COMPONENTS/backend/CMP-05-p2p-engine/CMP-05-p2p-engine.spec.md), [`CMP-06`](../../1_COMPONENTS/backend/CMP-06-media-player/CMP-06-media-player.spec.md)
