---
spec_id: CMP-17
spec_type: CMP
layer: frontend
name: UI Localization
target: lib/app/l10n/flik_localizations.dart
block: app
status: APPROVED
version: 1.0
owner: UI Team
last_reviewed: 2026-10-25
approved_at: 2026-10-25
approved_by: Product Owner
supersedes: []
superseded_by: []
user_story: user_story.md
processes: []
design_ref: .ai-harness/context/ui-design-system.md
depends_on: []
consumed_by: [CMP-10, CMP-12, CMP-13, CMP-14, CMP-15, CMP-16, CMP-33, CMP-34]
---

# 🌐 CMP-17 — Localización de la Interfaz

`CMP-17` · `APPROVED` · `v1.0` · `Flutter` · `app`

| 🧩 Tipo | 🚦 Estado | 🧭 Bloque | 🎯 Target |
|---|---|---|---|
| `CMP` | `APPROVED` | `app` | `lib/app/l10n/flik_localizations.dart` |

**Target:** `lib/app/l10n/flik_localizations.dart`
**Bloque:** `app`
**Estado:** `APPROVED`

> [!IMPORTANT]
> Toda cadena visible de FLIK nace en ARB. Esta spec define locales, fallback, selector, formatos y reglas de composición. No traduce el contenido del catálogo.

> [!WARNING]
> Prohibido añadir literales de interfaz en widgets. La implementación usa un catálogo tipado en Dart con paridad verificada contra los ARB, sin generador de código.

## 🗺️ Mapa de lectura

| Bloque | Qué encontrás |
|---|---|
| §1–§3 | Problema, alcance y actores |
| §4–§6 | Requisitos, reglas y errores |
| §7–§9 | API, contratos y dependencias |
| §10–§12 | Mapa, pruebas y BDD |
| §13–§15 | DoD, decisiones y preguntas |

---

## 1. Contexto y objetivo

### 1.1 Problema

Sin infraestructura de localización, cada pantalla escribe texto en su idioma y el producto no puede cambiar de idioma ni crecer a nuevos mercados sin reescribirse.

### 1.2 Objetivo medible

Toda pantalla renderiza sus textos desde ARB en `es` y `en`, el cambio de idioma se aplica en caliente y ninguna clave falta en ninguno de los dos locales.

### 1.3 No objetivos

- Traducir metadatos del catálogo.
- Soportar RTL.
- Traducir contenido generado por el usuario.

---

## 2. Alcance y límites

**Incluye:**

- Locales `es` y `en`, con `es` como fallback.
- Catálogo tipado de cadenas con paridad verificada contra los ARB.
- Selector de idioma persistido en ajustes.
- Formatos de fecha, duración y número.
- Mensajes con plurales.
- Prueba de paridad de claves y de layout con textos largos.

**Excluye:**

- Traducción de títulos, sinopsis o cualquier campo del catálogo.
- Idiomas adicionales.
- Detección por IP o servidor.

**Invariantes aplicables:**

- `architecture_rules.md` §4.9 (privacidad: el idioma no sale del dispositivo).
- `ui-design-system.md` §3.8 (localización obligatoria).

---

## 3. Actores e historia

> **Como** usuario,
> **quiero** ver la interfaz en mi idioma,
> **para** entender acciones y estados sin ambigüedad.

---

## 4. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación | Regla |
|---|---|---|---|---|
| `FR-01` | Locales `es` y `en` con fallback `es` | Alta | Un locale no soportado resuelve a `es` | `BR-01` |
| `FR-02` | Todas las claves existen en ambos ARB | Alta | El test de paridad no encuentra claves ausentes | `BR-02` |
| `FR-03` | El idioma se selecciona y persiste localmente | Alta | Reiniciar conserva el idioma elegido | `BR-03` |
| `FR-04` | El cambio de idioma se aplica sin reiniciar | Alta | `MaterialApp` reconstruye con el nuevo locale | `BR-04` |
| `FR-05` | Fechas y números se formatean según el locale; la duración usa un formato estable | Media | El formato cambia con el locale salvo la duración, que es `m:ss` o `h:mm:ss` | `BR-05` |
| `FR-06` | Mensajes con plurales y placeholders usan ICU | Alta | No existe concatenación de cadenas | `BR-06` |
| `FR-07` | El contenido del catálogo no se traduce | Alta | El título se muestra tal como llega | `BR-07` |
| `FR-08` | La interfaz resiste textos 40 % más largos | Media | Sin overflow en anchos de TV y compacto | `BR-08` |
| `FR-09` | Cero literales de interfaz en widgets | Alta | Revisión y test de claves usadas | `BR-09` |

## 5. Reglas de negocio e invariantes

| ID | Regla |
|---|---|
| `BR-01` | El locale del sistema se usa solo si está soportado; si no, `es`. |
| `BR-02` | Una clave nueva se añade a todos los ARB y a las implementaciones Dart en el mismo cambio. |
| `BR-03` | La preferencia se guarda en ajustes locales; nunca en red. |
| `BR-04` | El locale activo vive en un controlador de `lib/app/`; los widgets no lo mutan. |
| `BR-05` | Fechas y números se formatean con `intl`/`MaterialLocalizations`; la duración usa un formato numérico estable `m:ss` o `h:mm:ss`. |
| `BR-06` | Prohibido componer frases con `+` o interpolación de fragmentos traducibles. |
| `BR-07` | Los datos del catálogo se muestran en su idioma de origen en v1. |
| `BR-08` | Los botones y chips admiten truncado con elipsis; nunca reducen la fuente por debajo del estilo. |
| `BR-09` | Los textos de interfaz solo se obtienen del catálogo tipado. |
| `INV-01` | Ningún texto de interfaz se envía fuera del dispositivo. |
| `INV-02` | El idioma no altera el comportamiento del catálogo, del P2P ni del reproductor. |

---

## 6. Errores y estados

| ID | Situación | Resultado exigido |
|---|---|---|
| `E-01` | Clave ausente en un ARB | El test de paridad falla indicando clave y locale |
| `E-02` | Locale no soportado | Se aplica `es` sin error visible |
| `E-03` | Almacén de preferencias corrupto | Se aplica el locale del sistema o `es` |
| `E-04` | Clave ausente en el catálogo Dart | El test de paridad falla; no se muestra la clave cruda |
| `E-05` | Texto que desborda el contenedor | Truncado con elipsis; nunca overflow visible |

---

## 7. API pública

```dart
abstract class FlikStrings {
  Locale get locale;
  Map<String, String> get values;
  String text(String key);
  static FlikStrings of(BuildContext context);
}

final class FlikStringsEs extends FlikStrings {}
final class FlikStringsEn extends FlikStrings {}

abstract final class FlikLocalizations {
  static const List<Locale> supportedLocales;
  static const Locale fallbackLocale;
  static const LocalizationsDelegate<FlikStrings> delegate;
  static final List<LocalizationsDelegate<dynamic>> delegates;
}

enum AppLocale { system, es, en }

final class LocaleController extends ChangeNotifier {
  Locale? get locale;
  AppLocale get preference;
  Locale resolve(Locale systemLocale);
  Future<void> load();
  Future<void> select(AppLocale value);
}

abstract interface class LocalePreferenceStore {
  Future<AppLocale> read();
  Future<void> write(AppLocale value);
}

abstract final class FlikFormatters {
  static String duration(BuildContext context, Duration value);
  static String date(BuildContext context, DateTime value);
  static String number(BuildContext context, num value);
}
```

---

## 8. Contratos

| ID | Contrato | Tipo |
|---|---|---|
| `CT-01` | `AppLocale` | Enum con `system`, `es`, `en` |
| `CT-02` | `LocaleController` | `ChangeNotifier` con locale activo y persistencia |
| `CT-03` | `FlikStrings` + `FlikStringsEs` + `FlikStringsEn` | Catálogo tipado con paridad ARB |
| `CT-04` | `LocalePreferenceStore` | Contrato de lectura/escritura de la preferencia |
| `CT-05` | `FlikFormatters` | Formatos de duración, fecha y número |
| `CT-06` | `FlikLocalizations` | Locales soportados y delegados |

---

## 9. Dependencias

Permitidas: Flutter SDK, `flutter_localizations`, `intl`, `shared_preferences` solo a través de `LocalePreferenceStore`.

Prohibidas: traducción automática, servicios remotos, `easy_localization` u otros paquetes de localización, literales en widgets.

## 10. Mapa de implementación y trazabilidad

| Requisito | Contrato | Implementación (archivo::símbolo) | Test | Estado |
|---|---|---|---|---|
| `FR-01` | `CT-01` | `lib/app/l10n/app_locale.dart::AppLocale` | `TC-01` | Verified |
| `FR-02` | `CT-03` | `lib/app/l10n/app_es.arb`, `app_en.arb`, `flik_strings_es.dart`, `flik_strings_en.dart` | `TC-02` | Verified |
| `FR-03` | `CT-04` | `lib/app/l10n/locale_preference_store.dart::LocalePreferenceStore` | `TC-03` | Verified |
| `FR-04` | `CT-02` | `lib/app/l10n/locale_controller.dart::LocaleController` | `TC-04` | Verified |
| `FR-05` | `CT-05` | `lib/app/l10n/flik_formatters.dart::FlikFormatters` | `TC-05` | Verified |
| `FR-06` | `CT-03` | `lib/app/l10n/flik_strings_es.dart::FlikStringsEs` | `TC-06` | Verified |
| `FR-07` | `CT-03` | Pendiente en `CMP-14` al renderizar títulos | `TC-07` | Pending |
| `FR-08` | `CT-02` | `lib/app/flik_app.dart::FlikApp` | `TC-08` | Verified |
| `FR-09` | `CT-03` | Pendiente en `CMP-10` a `CMP-16` | `TC-09` | Pending |

---

## 11. Plan de pruebas

| ID | Tipo | Qué verifica | Entrada | Criterio |
|---|---|---|---|---|
| `TC-01` | Unit | Fallback de locale | `Locale('fr')` | Resuelve `es` |
| `TC-02` | Unit | Paridad de claves | `app_es.arb`, `app_en.arb`, catálogos Dart | Mismo conjunto de claves y mismos valores |
| `TC-03` | Unit | Persistencia | `LocalePreferenceStore` en memoria | Conserva `en` tras reinicio simulado |
| `TC-04` | Widget | Cambio en caliente | `LocaleController.select(en)` | Los textos cambian sin recrear la app |
| `TC-05` | Unit | Formatos | `Duration` y `DateTime` | Duración estable; fecha y número por locale |
| `TC-06` | Unit | Plurales | Mensajes con `count` | Cero, uno y varios correctos |
| `TC-07` | Widget | Contenido no traducido | Título con caracteres propios | Se muestra sin alterar |
| `TC-08` | Widget | Texto largo | Cadena +40 % | Sin overflow; elipsis donde aplique |
| `TC-09` | Static | Sin literales | `lib/` | Ningún `Text('...')` con texto de interfaz |

Comandos: `flutter analyze`, `flutter test test/app/l10n/`.

---

## 12. Criterios BDD

```gherkin
@FR-04
Scenario: Cambiar idioma sin reiniciar
  Given la app abierta en espanol
  When el usuario selecciona English en Configuracion
  Then la interfaz se muestra en ingles
  And la seleccion persiste al reiniciar

@FR-02
Scenario: Clave ausente en un idioma
  Given una clave presente solo en app_es.arb
  When se ejecuta el test de paridad
  Then el test falla indicando la clave y el locale

@FR-07
Scenario: Contenido en idioma de origen
  Given un titulo del catalogo escrito en japones
  When se muestra en la interfaz en ingles
  Then el titulo se muestra sin traducir
```

## 13. Definition of Done

- [x] Todos los `FR-*` tienen `CT-*`, `TC-*` y entrada en §10.
- [x] `es` y `en` tienen el mismo conjunto de claves y valores.
- [x] `flutter analyze` y `flutter test test/app/l10n/` pasan.
- [ ] Cero literales de interfaz en `lib/` (se completa al implementar las pantallas).
- [x] El controlador persiste y resuelve el locale.
- [x] Sin dependencias fuera de §9.
- [x] Sin preguntas bloqueantes en §15.

---

## 14. Decisiones

| Fecha | Decisión | Motivo | Impacto | Aprobado por |
|---|---|---|---|---|
| 2026-10-25 | `es` y `en` con fallback `es` | Alcance acordado con producto | `FR-01` | Product Owner |
| 2026-10-25 | Contenido del catálogo sin traducir en v1 | Evitar inventar datos | `FR-07` | Product Owner |
| 2026-10-25 | Catálogo tipado en Dart con test de paridad ARB, sin generador | El entorno de validación no dispone de SDK; evita dependencia de `gen-l10n` | `FR-02`, `FR-09` | Product Owner |
| 2026-10-25 | Duración con formato estable y fecha/número localizados | `intl` no aporta valor para `m:ss` y evita inicialización de datos de fecha | `FR-05` | Product Owner |

---

## 15. Preguntas abiertas

No hay preguntas bloqueantes.

---

## Historial de cambios

| Versión | Fecha | Tipo | Cambio | Aprobado por |
|---|---|---|---|---|
| 1.0 | 2026-10-25 | Inicial | Localización de interfaz es/en | Product Owner |



