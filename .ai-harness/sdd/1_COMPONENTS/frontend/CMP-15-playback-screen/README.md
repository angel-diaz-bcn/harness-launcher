# Playback Screen — Mapa de la pantalla

> Pantalla de reproducción de FLIK. Este README describe la anatomía, los estados y el reparto de responsabilidades entre specs. No es una spec.

---

## 1. Anatomía

```
┌──────────────────────────────────────────────────────────┐
│ X   Título · T2 E4                         CC  🔊  ◉     │  PlayerTopBar
│                                                          │
│                                                          │
│                                                          │
│  12:34  ──────────●───────────────────────  45:00        │  PlayerTimeline
│                 ◀10     ▶/❚❚     ▶▶10                     │  PlayerCenterControls
└──────────────────────────────────────────────────────────┘
```

Superposiciones:

- `PlayerOptionsSheet`: audio y subtítulos, abierto desde CC.
- `PlayerVolumeControl`: popover de mute y volumen, abierto desde el altavoz.
- `PlayerDetailsPopover`: calidad, pares, progreso y velocidad, abierto desde ◉.
- `PlayerStatusOverlay`: preparando, buffering, estado P2P y avisos de ±10 s.
- `PlayerErrorPanel`: error de flujo, códec o sesión.
- `PlayerOptionsSheet`: audio y subtítulos.

---

## 2. Estados

| Fase | Vídeo | OSD | Overlay | Foco |
|---|---|---|---|---|
| `preparing` | Fondo | Volver y estado | Preparando | Volver |
| `buffering` | Último fotograma | Visible | Buffering + P2P | Play/Pausa |
| `playing` | Reproduciendo | Auto-hide 3 s | — | Play/Pausa |
| `paused` | Congelado | Siempre visible | — | Play/Pausa |
| `completed` | Último fotograma | Visible | Repetir | Repetir |
| `failed` | Fondo | — | Error | Reintentar |

---

## 3. Foco

| Entrada | OSD oculto | OSD visible |
|---|---|---|
| `Select` | Play/pausa | Activa el control enfocado |
| `Left` / `Right` | −10 s / +10 s | Mueve el foco direccional |
| `Up` / `Down` | Muestra el OSD | Navega entre zonas |
| `Back` | Cierra sesión | Cierra sesión |

- Foco inicial: Play/Pausa.
- `paused` mantiene el OSD visible.
- Un menú abierto captura el foco y lo devuelve al cerrar.

---

## 4. Reparto de specs

| Spec | Responsabilidad |
|---|---|
| `CMP-15` | Composición, sesión, foco raíz, atajos, cierre y progreso |
| `CMP-18` | Capa OSD, visibilidad y zonas |
| `CMP-19` | Volver, título, calidad y estado de red |
| `CMP-20` | −10 s, play/pausa, +10 s |
| `CMP-21` | Progreso, tiempos, seek |
| `CMP-22` | Audio y subtítulos |
| `CMP-23` | Superficie de vídeo |
| `CMP-24` | Buffering, preparación, avisos |
| `CMP-25` | Error y recuperación |
| `CMP-26` | Volumen y silencio |
| `CMP-27` | Detalles de calidad y red P2P |

---

## 5. Fuera de v1

Siguiente episodio, cambio de calidad, velocidad, gestos móviles, «omitir intro» y estilo de subtítulos. Se especificarán cuando existan los datos o la configuración correspondiente.
