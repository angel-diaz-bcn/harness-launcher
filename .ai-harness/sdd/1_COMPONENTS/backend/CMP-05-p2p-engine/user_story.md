# 🧲 CMP-05 — P2P Engine

`CMP-05` · `Product brief` · `v1.0` · `p2p_engine` · `DRAFT`

> [!NOTE]
> **En una frase:** convertir un magnet en un flujo HTTP local reproducible y seekable, sin backend y sin descargar el archivo completo.

---

## 🎯 Problema

Sin motor P2P, FLIK no puede reproducir nada: el reproductor solo sabe consumir una URL local, y el catálogo solo aporta magnets. Nadie convierte hoy un magnet en bytes servibles por rangos.

Sin esta pieza:

- el reproductor no tiene fuente;
- el seeking no existe;
- la app no puede empezar a reproducir hasta descargar todo el archivo;
- Android TV se queda sin memoria si no hay búfer acotado.

---

## 👥 Actores

| Actor | Qué necesita |
|---|---|
| Usuario de TV, móvil o escritorio | Que el contenido empiece pronto y que pueda avanzar y retroceder |
| Media Player | Una URL local que responda `206` y bytes exactos |
| Orquestador de reproducción | Abrir, observar estado y cerrar la sesión sin fugas |
| Sistema operativo | Que no se abran puertos fuera de loopback ni queden procesos vivos |

---

## 🧑‍💻 Historia de usuario

> **Como** usuario de FLIK,
> **quiero** que al abrir un magnet el contenido empiece a reproducirse en segundos y pueda moverme por la película,
> **para** verlo sin esperar la descarga completa y sin que la app consuma memoria sin control.

---

## ✅ Criterios de negocio

| ID | Criterio |
|---|---|
| `US-01` | Un magnet válido se convierte en un flujo local disponible en `127.0.0.1:8888/stream`. |
| `US-02` | El flujo soporta rangos: se puede pedir cualquier tramo sin descargar el archivo completo. |
| `US-03` | El arranque prioriza las cabeceras del contenedor y los primeros megabytes. |
| `US-04` | La memoria y el disco quedan acotados: las piezas ya vistas se pueden descartar. |
| `US-05` | Al cerrar la reproducción, el puerto y los recursos nativos quedan libres. |
| `US-06` | El endpoint solo es accesible desde el propio dispositivo y exige token de sesión. |
| `US-07` | Ningún dato de uso sale del dispositivo. |

---

## 🚫 Qué NO es esta historia

> [!WARNING]
> No es el reproductor, ni el catálogo, ni la pantalla de reproducción, ni el OSD. No transcodifica, no descarga de forma permanente y no expone el puerto a la red local.

---

## 🔗 Spec técnica

[`CMP-05-p2p-engine.spec.md`](CMP-05-p2p-engine.spec.md) · Decisión de runtime: [`ADR-0001`](../../../../memory/decisions/ADR-0001-libtorrent-runtime.md)
