# FLIK — Matriz de Plataformas

Restricciones y obligaciones por plataforma. Ninguna plataforma puede asumir comportamiento de otra.

---

## 1. Matriz general

| Plataforma | Entrada principal | Empaquetado | Foco obligatorio |
|---|---|---|---|
| Android TV | D-Pad / mando | APK/AAB con Leanback | Sí |
| Android móvil | Táctil | APK/AAB | Teclado externo opcional |
| Windows | Teclado / ratón | Instalador o MSIX | Flechas + Enter |
| macOS | Teclado / trackpad | App bundle / DMG | Flechas + Enter |
| Linux | Teclado / ratón | AppImage / Flatpak / paquete | Flechas + Enter |

---

## 2. Android TV

- Declarar Leanback launcher y banner de TV.
- Soportar `KEYCODE_DPAD_*`, `KEYCODE_DPAD_CENTER` y `KEYCODE_BACK`.
- No depender de hover, scroll táctil ni barra de estado.
- Respetar overscan y distancia de sofá.
- Cuidar memoria y almacenamiento: el búfer debe evictar.
- Verificar decodificación hardware por SoC; prever fallback software.
- Probar con mando real o emulador TV, no solo teléfono.

### 2.1 Emuladores (entorno local de desarrollo)

| AVD | Imagen | Uso | Estado |
|---|---|---|---|
| `FLIK_TV` | `android-36;android-tv;x86_64` | Maquetación, foco y D-Pad | **No sirve para vídeo**: incluso con `hw.gpu.mode=host`, la imagen Android TV 16 no compone la textura de `media_kit` (imagen negra con audio y subtítulos correctos). Usar solo para UI |
| `FLIK_PHONE_30` | `android-30;google_apis;x86_64` | Reproducción real (intro y película) | **Verificado**: intro de FLIK y película con imagen y audio, con `-gpu host` |
| Dispositivo físico `24094RAD4G` | `android-36` · `arm64-v8a` · USB | **Entorno de referencia para reproducción** | **Verificado**: intro de FLIK, película y OSD completos. Confirma que el fallo de vídeo de `FLIK_TV` es de la imagen del emulador, no de Android 16 |

- La imagen API 36 expone `ANDROID_EMU_gles_max_version_3_0` y su `libEGL` rechaza los
  atributos que pide `libmpv`; el reloj y el audio avanzan pero la superficie queda negra.
- La imagen API 30 acepta esos atributos: la misma APK reproduce Sintel con imagen y audio.
- Arrancar siempre con `-gpu host` (con `auto`/`swiftshader` el AVD cae en GL por software).
- Scripts: `.spikes/S0-libtorrent/launch-emulator.ps1` (TV) y `launch-emulator-phone30.ps1`
  (reproducción).


## 3. Android móvil

- Targets táctiles mínimos de 48×48 dp.
- Gestionar ciclo de vida, audio focus y interrupciones.
- No asumir D-Pad; permitir teclado externo.
- Adaptar el layout sin romper el árbol de foco.
- Verificar reproducción en pantalla pequeña y rotación.

## 4. Windows

- Ventana redimensionable y atajos de teclado.
- Verificar decodificación D3D11VA y fallback software.
- Empaquetar con firma y actualizaciones controladas.
- No asumir rutas POSIX ni permisos de administrador.

## 5. macOS

- Verificar VideoToolbox y fallback software.
- Revisar notarización, sandbox y permisos de red local.
- No asumir que el usuario ejecuta como administrador.
- Probar en Intel y Apple Silicon si se distribuye universal.

## 6. Linux

- Verificar VA-API y fallback software.
- Soportar Wayland y X11.
- Empaquetar dependencias de MPV/FFmpeg de forma reproducible.
- Documentar dependencias del sistema.

---

## 7. Códecs y contenedores

- Contenedores objetivo: MKV, MP4/M4V, WebM.
- Vídeo: H.264 y HEVC como base; VP9/AV1 según capacidad de plataforma.
- Audio: AAC, MP3, AC3, EAC3, DTS, FLAC, Opus.
- Subtítulos: SRT, WebVTT, ASS/SSA y PGS cuando el motor los soporte.
- El fallback software es obligatorio cuando el hardware falla.
- La matriz exacta de códecs por plataforma se fija en la spec del reproductor.

---

## 8. Almacenamiento

- Catálogo y progreso: almacenamiento local ligero.
- Búfer P2P: directorio temporal de sesión, acotado y evictable.
- Prohibido usar el almacenamiento de catálogo para piezas de vídeo.
- Limpiar sesiones huérfanas al arrancar.
- Respetar cuotas y permisos de Android TV.

---

## 9. Red

- El endpoint de vídeo es siempre `127.0.0.1:8888/stream`.
- El puerto debe comprobarse antes de abrir; si está ocupado, fallar con error explícito.
- No abrir el puerto a la LAN.
- UPnP/NAT-PMP desactivado por defecto.
- La app debe funcionar sin conexión para catálogo cacheado y progreso.

---

## 10. Verificación mínima por plataforma

- Compila y arranca.
- Navega todo el catálogo con la entrada principal.
- Abre un magnet de prueba y reproduce.
- Hace seeking y cambia pistas.
- Cierra la reproducción y libera el puerto.
- No deja procesos, sockets ni archivos temporales.
