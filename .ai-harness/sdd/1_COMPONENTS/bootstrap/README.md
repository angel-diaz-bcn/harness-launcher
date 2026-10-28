# 🧱 bootstrap — Infraestructura de arranque

> [!NOTE]
> Esta subcategoría de `1_COMPONENTS` agrupa la base ejecutable de FLIK: proyecto Flutter, identidad, estructura, lints y shell neutral. No contiene producto: ni catálogo, ni P2P, ni reproductor, ni UI real.
>
> No es `backend` porque no implementa dominio ni datos. No es `frontend` porque no define pantallas ni tema. Es el punto de arranque que habilita ambos.

| Spec | Estado | Target | Propósito |
|---|---|---|---|
| [`CMP-00 — App Bootstrap`](CMP-00-app-bootstrap/CMP-00-app-bootstrap.spec.md) | `DRAFT` | `lib/app/bootstrap/bootstrap.dart` | Proyecto Flutter, identidad, estructura, lints y shell neutral. |

## 📚 Orden de lectura

1. [`CMP-00`](CMP-00-app-bootstrap/CMP-00-app-bootstrap.spec.md) — base ejecutable.
2. `CMP-01` — contrato del catálogo.

> [!IMPORTANT]
> `CMP-00` no implementa ninguna feature. Su cierre habilita que las specs de `catalog`, `player`, `p2p_engine` y `tv_experience` tengan un proyecto donde aterrizar.
