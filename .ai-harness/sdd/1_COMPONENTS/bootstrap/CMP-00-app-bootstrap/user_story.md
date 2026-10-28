# 🚀 CMP-00 — App Bootstrap

> [!NOTE]
> **Product brief.** Este documento explica *por qué* FLIK necesita una base técnica antes de implementar el contrato del catálogo. El contrato ejecutable vive en [`CMP-00-app-bootstrap.spec.md`](CMP-00-app-bootstrap.spec.md).

| Campo | Valor |
|---|---|
| **ID** | `CMP-00` |
| **Tipo** | Componente de infraestructura |
| **Bloque** | `app` |
| **Estado** | `DRAFT` |
| **Target** | `lib/app/bootstrap/bootstrap.dart` |
| **Spec** | [`CMP-00-app-bootstrap.spec.md`](CMP-00-app-bootstrap.spec.md) |

---

## 🎯 Resumen en una frase

Crear el esqueleto Flutter mínimo, reproducible y sin lógica de producto que permita compilar, analizar y probar FLIK en Android, Windows, macOS y Linux antes de implementar cualquier feature.

---

## 😣 El problema

Hoy el repositorio contiene el arnés de IA, las specs y los fixtures, pero no existe un proyecto Flutter:

- no hay `pubspec.yaml`;
- no hay `lib/`;
- no hay `test/`;
- no hay configuración de análisis;
- no hay identificadores de aplicación;
- no hay una pantalla mínima que arranque.

Eso bloquea la implementación de `CMP-01`, porque su target es un archivo Dart dentro de `lib/features/catalog/domain/`.

Sin bootstrap, cada feature tendría que inventar su propia base, duplicar configuración o introducir dependencias antes de que exista una spec que las justifique.

---

## 👥 Actores

| Actor | Necesidad |
|---|---|
| **Desarrollador** | Un proyecto que compile y ejecute tests sin configuración manual. |
| **Arquitecto** | Una base neutral que no imponga decisiones de producto. |
| **CI** | Comandos deterministas de análisis, test y build. |
| **Specs futuras** | Un lugar estable donde aterrizar `lib/features/*`. |

---

## 🧑‍💻 Historia de usuario

> **Como** responsable técnico de FLIK,
> **quiero** disponer de un proyecto Flutter mínimo con estructura, lints, identificadores y un arranque verificable,
> **para** poder implementar las specs de catálogo, reproducción, P2P y TV sin mezclar infraestructura con lógica de producto.

---

## ✅ Criterios de negocio

### US-01 — El proyecto existe y compila

El repositorio debe poder analizarse, probarse y compilarse con Flutter estable en las plataformas objetivo.

### US-02 — La identidad de la app es estable

La aplicación se llama **FLIK** y usa el identificador `com.flik.app` en Android, macOS y Linux.

### US-03 — La estructura prepara las features sin implementarlas

Deben existir los puntos de aterrizaje para `catalog`, `player`, `p2p_engine` y `tv_experience`, pero sin código de negocio.

### US-04 — El arranque es mínimo y reemplazable

La app debe arrancar con una shell neutral. La interfaz real se definirá en specs de UI posteriores.

### US-05 — No se contaminan las dependencias

El bootstrap solo puede añadir dependencias de Flutter, test y lints. Ninguna dependencia de P2P, player, base de datos o red puede entrar antes de su spec.

### US-06 — El bootstrap no implementa producto

No hay catálogo, parser, magnets, streaming, almacenamiento, navegación de TV ni reproducción en esta historia.

---

## 🚫 Qué no es esta historia

- No es el contrato del catálogo.
- No es el parser JSON.
- No es la pantalla principal.
- No es el motor P2P.
- No es el reproductor.
- No es la sincronización remota.
- No es una decisión de diseño visual.

---

## 📌 Resultado esperado

Un proyecto Flutter vacío pero correcto:

```text
FLIK/
├── android/
├── linux/
├── macos/
├── windows/
├── lib/
│   ├── main.dart
│   ├── app/
│   │   ├── bootstrap/
│   │   └── flik_app.dart
│   ├── core/
│   └── features/
│       ├── catalog/
│       ├── player/
│       ├── p2p_engine/
│       └── tv_experience/
├── test/
├── integration_test/
├── analysis_options.yaml
└── pubspec.yaml
```

La app debe abrir una shell vacía y no debe realizar ninguna operación de red, P2P o disco.

---

## 🔗 Trazabilidad

| Necesidad | Requisito en la spec |
|---|---|
| `US-01` | `FR-01`, `FR-09` |
| `US-02` | `FR-02`, `FR-08` |
| `US-03` | `FR-03` |
| `US-04` | `FR-06`, `FR-07` |
| `US-05` | `FR-05`, `FR-10` |
| `US-06` | `FR-11`, `FR-12` |
