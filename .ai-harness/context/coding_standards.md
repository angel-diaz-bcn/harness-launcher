# FLIK — Estándares de Código y Directrices de Implementación

Estándares obligatorios para el desarrollo, revisión y mantenimiento del código de FLIK.

---

## 1. Flutter y Dart

- **Versión:** Flutter estable actual y Dart estable compatible.
- **Tipado estricto:** `analysis_options.yaml` con linter riguroso y sin warnings nuevos.
- **Reglas mínimas de lint:**
  - `prefer_const_constructors`
  - `prefer_const_literals_to_create_immutables`
  - `avoid_print`
  - `always_declare_return_types`
  - `prefer_final_locals`
  - `use_super_parameters`
  - `unawaited_futures`
  - `cancel_subscriptions`
  - `close_sinks`
- **Formato:** `dart format` antes de cada entrega.
- **Prohibido `dynamic`** salvo fronteras de serialización justificadas y confinadas a `data/`.
- **Prohibido `print`:** usar el logger de `core/`.
- **Prohibido `catch` vacío o silencioso:** todo error se tipa y se propaga o se registra con contexto.
- **Nombres:** `snake_case` para archivos, `PascalCase` para tipos, `camelCase` para miembros, `k` para constantes.

---

## 2. Arquitectura de código

- Cada feature respeta `domain/`, `data/` y `presentation/`; las features sin UI, como `p2p_engine`, usan `application/` en lugar de `presentation/`.
- El dominio contiene entidades, contratos y casos de uso; no importa Flutter, HTTP, almacenamiento ni paquetes de UI.
- `data/` implementa repositorios y fuentes; traduce DTOs a entidades.
- `presentation/` contiene controladores de estado y widgets; no accede a red, base de datos ni sockets.
- La composición de dependencias vive en `lib/app/`.
- Una feature solo expone su API pública; prohibido importar rutas internas de otra feature.
- Prohibidas las dependencias circulares.

---

## 3. Modelos inmutables y serialización

- Todos los modelos de dominio y DTO son inmutables.
- Usar `freezed` para uniones, copias e igualdad estructural; `json_serializable` para JSON.
- Los modelos no exponen colecciones mutables; se usan `List.unmodifiable` o tipos inmutables.
- Los campos obligatorios se validan en el constructor o en el parser; nunca se aceptan valores inválidos silenciosamente.
- El parseo de JSON se realiza en `data/`; el dominio recibe entidades ya validadas.
- Prohibido `Map<String, dynamic>` fuera de la capa de serialización.
- Los enums se serializan por nombre explícito, no por índice.

---

## 4. Reglas del motor P2P

- La memoria nativa se maneja con ciclos de vida explícitos: abrir, usar y liberar.
- Prohibido retener punteros, buffers o handles nativos más allá de la sesión.
- El servidor HTTP local se aísla del isolate de UI.
- El socket escucha exclusivamente en `127.0.0.1:8888`; prohibido `0.0.0.0` o interfaces de red.
- Al cerrar la reproducción se cancelan sockets, se liberan puertos y se destruyen recursos nativos.
- Todo error nativo se traduce a un error tipado de Dart; prohibido propagar códigos crudos a la UI.
- La descarga es secuencial y con prioridad de cabeceras; prohibido descargar el archivo completo antes de reproducir.
- El búfer de anillo debe declarar límite y política de evicción; prohibido crecimiento ilimitado.
- Prohibido bloquear el hilo principal con operaciones de disco, red o cómputo.

---

## 5. Reglas del reproductor

- `media_kit` y MPV quedan confinados a `features/player/`; prohibido exponer sus tipos al resto de la app.
- El reproductor recibe la URL local y metadatos mínimos; no consulta catálogo ni resuelve magnets.
- Cada sesión de reproducción se destruye al salir de la vista.
- La conmutación de pistas no reinicia el flujo ni pierde la posición.
- Prohibida la transcodificación o el remuxing.
- Los errores de códec o de flujo se reportan como estados tipados, no como excepciones sin contexto.

---

## 6. Reglas de catálogo

- Los documentos JSON se validan contra el contrato antes de persistir.
- Prohibido usar parsers que instancien objetos arbitrarios o acepten campos fuera del contrato.
- La caché local se accede solo a través de repositorios; prohibido abrir Hive/SQLite desde widgets.
- La primera lectura se sirve desde caché; la red se intenta después.
- Los catálogos inválidos se rechazan completos; no se aplican parcialmente.
- El progreso de visualización se guarda localmente y no se envía a ningún servidor.

---

## 7. Reglas de UI

- Usar exclusivamente los tokens de `ui-design-system.md`; prohibido hardcodear colores HEX en widgets.
- Todo componente interactivo debe usar `FocusNode` y `FocusScope` cuando corresponda.
- Prohibido depender solo de hover o toque para accionar un control.
- El foco debe ser visible y no puede quedar fuera del viewport.
- El estado de negocio vive en controladores; `setState` solo para estado efímero de un widget.
- Los widgets no contienen lógica de catálogo, P2P, reproducción ni acceso a datos.
- Los textos deben soportar escalado hasta 130 % sin romper el layout.
- Prohibidas animaciones de más de 300 ms o con rebote.

---

## 8. Manejo de errores y estado

- Usar errores tipados y estados explícitos: cargando, disponible, vacío y error.
- Prohibido `catch (_) {}` o tragar excepciones sin registro.
- Los mensajes de error de UI son claros y accionables; los detalles técnicos van al logger.
- Prohibido usar excepciones para control de flujo normal.
- Las operaciones asíncronas deben ser cancelables cuando dependan de una pantalla o sesión.

---

## 9. Seguridad y privacidad

- No registrar tokens, rutas privadas, enlaces magnet completos ni datos personales.
- Validar esquemas y URLs antes de abrir recursos externos.
- El endpoint local no se expone fuera de loopback.
- Prohibido incluir SDKs de analítica, publicidad o crash reporting remoto.
- Las credenciales de fuentes, si existen, se guardan en el almacén seguro de la plataforma.

---

## 10. Pruebas y revisión

- Todo cambio funcional incluye pruebas unitarias o de widget.
- Los parsers y la lógica de búfer requieren cobertura alta y fixtures representativos.
- `flutter analyze` y `flutter test` deben pasar antes de cerrar la tarea.
- Los tests no dependen de red real, tiempo real ni servicios externos.
- Toda corrección de bug incluye una prueba que lo reproduce.

---

## 11. Prohibiciones

- Backend, proxy o transcodificación.
- Telemetría de usuario.
- Colores o estilos fuera del sistema de diseño.
- Widgets con lógica de negocio.
- Dependencias circulares entre features.
- `print`, `dynamic` injustificado o `catch` silencioso.
- Descarga completa antes de reproducir o búfer sin evicción.
- Publicación Git sin instrucción explícita del usuario.
