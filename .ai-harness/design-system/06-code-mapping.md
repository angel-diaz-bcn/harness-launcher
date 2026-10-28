# FLIK — Code Mapping

Correspondencia entre el sistema de diseño y el código. Sin este mapa, un token o un componente está fuera de sistema.

---

## 1. Cadena de materialización

```
tokens.json
   ↓ (constantes escritas a mano + test de paridad)
lib/app/theme/*.dart
   ↓ (ThemeData + ThemeExtension)
widgets DS-*  ←  specs CMP-08/09/14/15
   ↓
pantallas CMP-10 … CMP-16
```

Reglas:

- Ningún widget importa `tokens.json` ni lee JSON en runtime.
- Ningún widget declara colores, tamaños o duraciones literales.
- `lib/app/theme/` es el **único** lugar donde puede aparecer un valor de color.
- `preflight` bloquea `Color(...)`, `Color.fromARGB` y `Colors.*` fuera de ese directorio.
- Cada símbolo público implementado lleva `/// Spec: <ID> / <FR>`.

---

## 2. Tokens → Dart

| Grupo JSON | Clase / API | Archivo | Notas |
|---|---|---|---|
| `color.brand.*` | `FlikColors.brandPrimary`, `brandDeep`, `brandTint` | `lib/app/theme/flik_colors.dart` | Constantes `Color` |
| `color.accent.*` | `FlikColors.accent`, `accentHover`, `accentPressed`, `accentSoft`, `onAccent` | `lib/app/theme/flik_colors.dart` | `accentSoft` se construye una vez |
| `color.surface.*` | `FlikColors.canvas`, `surface`, `surfaceElevated`, `surfaceInset`, `overlay`, `overlayStrong` | `lib/app/theme/flik_colors.dart` | |
| `color.border.*` | `FlikColors.borderSubtle`, `borderStrong`, `borderFocus` | `lib/app/theme/flik_colors.dart` | |
| `color.text.*` | `FlikSemanticColors.textPrimary`, `textSecondary`, `textDisabled`, `textAccent`, `textOnAccent` | `lib/app/theme/flik_theme.dart` | `ThemeExtension` |
| `color.status.*` | `FlikSemanticColors.success`, `warning`, `error`, `info` | `lib/app/theme/flik_theme.dart` | `ThemeExtension` |
| `typography.families` | `FlikTypography.displayFamily`, `bodyFamily` | `lib/app/theme/flik_typography.dart` | Nombres declarados en `pubspec.yaml` |
| `typography.styles.*` | `FlikTypography.display`, `headline`, `title`, `section`, `body`, `label`, `caption`, `eyebrow` | `lib/app/theme/flik_typography.dart` | Devuelven `TextStyle` según breakpoint |
| `space.*` | `FlikSpacing.s0` … `s12` | `lib/app/theme/flik_spacing.dart` | `double` |
| `radius.*` | `FlikRadii.sm`, `md`, `lg`, `xl`, `pill` | `lib/app/theme/flik_spacing.dart` | `BorderRadius` |
| `border.*` | `FlikBorders.hairline`, `focus` | `lib/app/theme/flik_spacing.dart` | `double` |
| `motion.*` | `FlikMotion.fast`, `base`, `slow`, `easingIn`, `easingOut` | `lib/app/theme/flik_motion.dart` | `Duration` y `Curve` |
| `focus.*` | `FlikFocus.scale`, `ringWidth`, `ringOffset`, `haloBlur` | `lib/app/theme/flik_motion.dart` | |
| Escalado de texto | `FlikTextScale.clamp` | `lib/app/theme/flik_theme.dart` | Límite 100–130 % |
| `layout.*` | `FlikLayout.of(context)` | `lib/app/theme/flik_layout.dart` | Resuelve breakpoint |
| `icon.*` | `FlikIconSizes.sm`, `md`, `lg`, `xl` | `lib/app/theme/flik_icons.dart` | `double` |
| `target.*` | `FlikTargets.minTouch`, `tvMin` | `lib/app/theme/flik_icons.dart` | `double` |

`FlikLayout` expone: `breakpoint`, `contentPadding`, `gridColumns`, `gridGutter`, `topBarHeight`, `heroHeight`, `posterSize`, `backdropCardSize`, `sectionGap`, `isTv`.

---

## 3. Tema

| Elemento | Archivo | Responsabilidad |
|---|---|---|
| `FlikTheme.dark` | `lib/app/theme/flik_theme.dart` | Construye `ThemeData` con `ColorScheme`, `TextTheme` y extensiones |
| `FlikSemanticColors` | `lib/app/theme/flik_theme.dart` | `ThemeExtension` con texto y estados |
| `FlikFocusDecoration` | `lib/app/theme/flik_focus.dart` | Decoración reutilizable de foco (anillo + halo) |
| `FlikThemeScope` | `lib/app/theme/flik_theme.dart` | Acceso tipado a tokens desde widgets |

En v1 solo existe tema oscuro. `ColorScheme` se deriva de los tokens; no se usan colores por defecto de Material.

## 4. Componentes → código

| Componente | Widget | Archivo | Spec | Fase |
|---|---|---|---|---|
| `DS-APP-BAR` | `FlikAppBar` | `presentation/widgets/flik_app_bar.dart` | `CMP-09` | F1 |
| `DS-LOGO` | `FlikLogo` | `presentation/widgets/flik_logo.dart` | `CMP-09` | F1 |
| `DS-BACK` | `FlikBackButton` | `presentation/widgets/flik_back_button.dart` | `CMP-09` | F1 |
| `DS-BUTTON-PRIMARY` | `FlikPrimaryButton` | `presentation/widgets/flik_buttons.dart` | `CMP-09` | F1 |
| `DS-BUTTON-SECONDARY` | `FlikSecondaryButton` | `presentation/widgets/flik_buttons.dart` | `CMP-09` | F1 |
| `DS-BUTTON-ICON` | `FlikIconButton` | `presentation/widgets/flik_buttons.dart` | `CMP-09` | F1 |
| `DS-CHIP` | `FlikChip` | `presentation/widgets/flik_chip.dart` | `CMP-09` | F1 |
| `DS-BADGE` | `FlikBadge` | `presentation/widgets/flik_badge.dart` | `CMP-09` | F1 |
| `DS-RATING` | `FlikRating` | `presentation/widgets/flik_rating.dart` | `CMP-09` | F2 |
| `DS-POSTER-CARD` | `PosterCard` | `presentation/widgets/poster_card.dart` | `CMP-09` | F2 |
| `DS-LANDSCAPE-CARD` | `LandscapeCard` | `presentation/widgets/landscape_card.dart` | `CMP-09` | F4 |
| `DS-PAGE-HEADER` | `PageHeader` | `presentation/widgets/channels/page_header.dart` | `CMP-33` | F1 |
| `DS-CHANNEL-CARD` | `ChannelCard` | `presentation/widgets/channels/channel_card.dart` | `CMP-34` | F1 |
| `DS-CHANNEL-ART` | `ChannelArt` | `presentation/widgets/channels/channel_art.dart` | `CMP-34` | F1 |
| `DS-CHANNEL-CAROUSEL` | `ChannelCarousel` | `presentation/widgets/channels/channel_carousel.dart` | `CMP-33` | F1 |
| `DS-PAGE-INDICATOR` | `PageIndicator` | `presentation/widgets/channels/page_indicator.dart` | `CMP-33` | F1 |
| `DS-PROFILE-AVATAR` | `ProfileAvatar` | `presentation/widgets/profile_avatar.dart` | `CMP-10` | F1 |
| `DS-HERO` | `BillboardHero` | `presentation/widgets/billboard_hero.dart` | `CMP-12` | F2 |
| `DS-SECTION-HEADER` | `SectionHeader` | `presentation/widgets/section_header.dart` | `CMP-09` | F2 |
| `DS-CAROUSEL` | `FlikCarousel` | `presentation/widgets/flik_carousel.dart` | `CMP-09` | F2 |
| `DS-GRID` | `PosterGrid` | `presentation/widgets/poster_grid.dart` | `CMP-13` | F3 |
| `DS-PERSON-CARD` | `PersonCard` | `presentation/widgets/person_card.dart` | `CMP-14` | F4 |
| `DS-INFO-PANEL` | `InfoPanel` | `presentation/widgets/info_panel.dart` | `CMP-14` | F4 |
| `DS-LANGUAGE-PANEL` | `LanguagePanel` | `presentation/widgets/language_panel.dart` | `CMP-14` | F4 |
| `DS-MATCH-METER` | `MatchMeter` | `presentation/widgets/match_meter.dart` | `CMP-14` | F4 |
| `DS-PROGRESS` | `FlikProgressBar` | `presentation/widgets/flik_progress.dart` | `CMP-09` | F2 |
| `DS-SKELETON` | `FlikSkeleton` | `presentation/widgets/flik_states.dart` | `CMP-09` | F1 |
| `DS-EMPTY-STATE` | `FlikEmptyState` | `presentation/widgets/flik_states.dart` | `CMP-09` | F1 |
| `DS-ERROR-STATE` | `FlikErrorState` | `presentation/widgets/flik_states.dart` | `CMP-09` | F1 |
| `DS-DIALOG` | `FlikDialog` | `presentation/widgets/flik_dialog.dart` | `CMP-09` | F1 |
| `DS-SETTINGS-ROW` | `SettingsRow` | `presentation/widgets/settings_row.dart` | `CMP-16` | F6 |
| `DS-SELECT` | `SettingsSelect` | `presentation/widgets/settings_controls.dart` | `CMP-16` | F6 |
| `DS-TOGGLE` | `SettingsToggle` | `presentation/widgets/settings_controls.dart` | `CMP-16` | F6 |
| `DS-SLIDER` | `SettingsSlider` | `presentation/widgets/settings_controls.dart` | `CMP-16` | F6 |
| `DS-OSD` | `PlayerOsd` | `presentation/widgets/player/player_osd.dart` | `CMP-18` | F5 |
| `DS-PLAYER-FOCUS-BUTTON` | `PlayerFocusButton` | `presentation/widgets/player/player_focus_button.dart` | `CMP-20` | F5 |
| `DS-PLAYER-ICON-BUTTON` | `PlayerIconButton` | `presentation/widgets/player/player_icon_button.dart` | `CMP-18` | F5 |
| `DS-PLAYER-SCRIM` | `PlayerScrim` | `presentation/widgets/player/player_scrim.dart` | `CMP-18` | F5 |
| `DS-PLAYER-VIDEO-SURFACE` | `PlayerVideoSurface` | `presentation/widgets/player/player_video_surface.dart` | `CMP-23` | F5 |
| `DS-PLAYER-TOP-BAR` | `PlayerTopBar` | `presentation/widgets/player/player_top_bar.dart` | `CMP-19` | F5 |
| `DS-PLAYER-CENTER` | `PlayerCenterControls` | `presentation/widgets/player/player_center_controls.dart` | `CMP-20` | F5 |
| `DS-PLAYER-TIMELINE` | `PlayerTimeline` | `presentation/widgets/player/player_timeline.dart` | `CMP-21` | F5 |
| `DS-PLAYER-OPTIONS` | `PlayerOptionsSheet` | `presentation/widgets/player/player_options_sheet.dart` | `CMP-22` | F5 |
| `DS-PLAYER-STATUS` | `PlayerStatusOverlay` | `presentation/widgets/player/player_status_overlay.dart` | `CMP-24` | F5 |
| `DS-PLAYER-ERROR` | `PlayerErrorPanel` | `presentation/widgets/player/player_error_panel.dart` | `CMP-25` | F5 |
| `DS-PLAYER-VOLUME` | `PlayerVolumeControl` | `presentation/widgets/player/player_volume_control.dart` | `CMP-26` | F5 |
| `DS-PLAYER-DETAILS` | `PlayerDetailsPopover` | `presentation/widgets/player/player_details_popover.dart` | `CMP-27` | F5 |

`presentation/` abrevia `lib/features/tv_experience/presentation/`.

---

## 5. Páginas → código

| Página | Archivo | Ruta | Spec | Proceso |
|---|---|---|---|---|
| Canales | `screens/channels_screen.dart` | `/channels` | `CMP-33` | — |
| Home del canal | `screens/home_screen.dart` | `/channels/:channelId` | `CMP-12` | `PRC-02` |
| Categoría | `screens/category_screen.dart` | `/channels/:channelId/category` | `CMP-13` | `PRC-04` |
| Detalle | `screens/title_detail_screen.dart` | `/channels/:channelId/title/:titleId` | `CMP-14` | `PRC-04` |
| Reproducción | `screens/playback_screen.dart` | `/play/:sessionId` | `CMP-15` | `PRC-01`, `PRC-03` |
| Configuración | `screens/settings_screen.dart` | `/settings` | `CMP-16` | `PRC-04` |

El router vive en `lib/app/routing/flik_router.dart` y la composición de dependencias en `lib/app/bootstrap/`. Ninguna pantalla construye sus dependencias.

## 6. Assets

| Asset | Ruta | Formato | Uso |
|---|---|---|---|
| Logotipo | `assets/branding/flik-logo.png` (1×, 2×, 3×) | PNG | `FlikLogo` |
| Fuente de marca | `assets/branding/flik-logo.svg` | SVG | Solo referencia, no runtime |
| Barlow Condensed | `assets/fonts/BarlowCondensed-*.ttf` | TTF | `display` |
| Barlow Semi Condensed | `assets/fonts/BarlowSemiCondensed-*.ttf` | TTF | `body` |
| Licencias de fuentes | `assets/fonts/OFL-*.txt` | TXT | Registro en «Acerca de» (`CMP-16`) |
| Placeholder de póster | `assets/images/poster_placeholder.webp` | WebP | Estado de carga y error |
| Placeholder de backdrop | `assets/images/backdrop_placeholder.webp` | WebP | Estado de carga y error |
| Avatar por defecto | `assets/images/avatar_default.webp` | WebP | Perfiles |
| Catálogo semilla | `assets/catalogs/` | JSON | Primer arranque offline |

Declaración en `pubspec.yaml`:

```yaml
flutter:
  uses-material-design: true
  assets:
    - assets/branding/
    - assets/images/
    - assets/catalogs/
  fonts:
    - family: BarlowCondensed
      fonts:
        - asset: assets/fonts/BarlowCondensed-Regular.ttf
        - asset: assets/fonts/BarlowCondensed-SemiBold.ttf
          weight: 600
        - asset: assets/fonts/BarlowCondensed-Bold.ttf
          weight: 700
    - family: BarlowSemiCondensed
      fonts:
        - asset: assets/fonts/BarlowSemiCondensed-Regular.ttf
        - asset: assets/fonts/BarlowSemiCondensed-Medium.ttf
          weight: 500
        - asset: assets/fonts/BarlowSemiCondensed-SemiBold.ttf
          weight: 600
```

---

## 7. Pruebas

| Test | Archivo | Verifica |
|---|---|---|
| Paridad de tokens | `test/app/theme/token_parity_test.dart` | Cada valor de `tokens.json` coincide con la constante Dart y no sobran tokens |
| Contraste | `test/app/theme/contrast_test.dart` | Pares texto/fondo cumplen AA en `canvas` y `surface` |
| Foco | `test/app/theme/focus_test.dart` | `FlikFocusDecoration` aplica anillo y halo sin alterar el layout |
| Layout | `test/app/theme/layout_test.dart` | `FlikLayout.of` resuelve breakpoint y tamaños correctos |
| Localización | `test/app/l10n/localization_test.dart` | `es` y `en` cubren las mismas claves; fallback y formatos |
| Recorrido D-Pad | `test/features/tv_experience/<pantalla>_focus_test.dart` | Todo control alcanzable y activable |
| Estados | `test/features/tv_experience/<pantalla>_states_test.dart` | Cargando, vacío y error son navegables |

El test de paridad lee `.ai-harness/design-system/tokens.json` con `dart:io` desde la raíz del proyecto. Si el archivo no existe, el test falla: el sistema de diseño es una dependencia de verificación, no opcional.

---

## 8. Reglas de cambio

1. Un token o componente nuevo se añade aquí **antes** de escribirse.
2. Cambiar un nombre de token exige actualizar `tokens.json`, `02-tokens.md`, el tema Dart, esta tabla y los consumidores.
3. Un widget nuevo sin fila en §4 está fuera de spec y `preflight` debe poder detectarlo por revisión.
4. Un símbolo público nuevo necesita comentario `/// Spec:` y entrada en el mapa de implementación de su `CMP-*`.
5. Prohibido añadir dependencias de UI (por ejemplo, un set de iconos alternativo) sin actualizar el sistema de diseño y el `pubspec.yaml` en el mismo cambio.

---

## 9. Estado de implementación

| Elemento | Estado | Fase |
|---|---|---|
| Documentación del sistema | Completa | F0 |
| `tokens.json` | Completo | F0 |
| `lib/app/theme/*` | Verificado con `flutter analyze` y `flutter test` | F0 |
| `lib/app/l10n/*` | Verificado con `flutter analyze` y `flutter test` | F0 |
| Assets de marca y fuentes | Completos (PNG 1×/2×/3×, Barlow y OFL) | F0 |
| Reproducción (`CMP-15`…`CMP-27`) | Verificada en Android 11 (AVD `FLIK_PHONE_30`) con Sintel y en `FLIK_TV` 1920×1080 para layout | F5 |
| Componentes `DS-*` | Familia del reproductor verificada; resto pendiente | F1–F6 |
| Pantallas | Reproducción verificada; resto pendiente | F1–F6 |

Ningún elemento «Pendiente» puede implementarse sin su spec en `APPROVED`.


