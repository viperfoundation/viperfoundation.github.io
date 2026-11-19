# viperfoundation.github.io

The open-source landing page of **Viper Messenger**: <https://viperfoundation.github.io/>

Viper Messenger is a private messenger built on TON. Messages go device to device whenever they can, everything is
end-to-end encrypted, and your account is a key: no phone number, no email.
[Viper Messenger on the App Store](https://apps.apple.com/us/app/viper-messenger/id6754181968) ·
[Docs](https://github.com/viperfoundation/Viper) · [Telegram](https://t.me/viperfoundation)

| Desktop, dark | Desktop, light |
|---|---|
| ![Landing, desktop, dark](docs/screenshots/desktop-dark.png) | ![Landing, desktop, light](docs/screenshots/desktop-light.png) |

| Mobile, dark | Mobile, light |
|---|---|
| <img src="docs/screenshots/mobile-dark.png" alt="Landing, mobile, dark" width="300"> | <img src="docs/screenshots/mobile-light.png" alt="Landing, mobile, light" width="300"> |

## What it is

One static page, no build step: `index.html` with inline CSS and JS, images in `img/`, animations in `lotties/noto/`.
It follows the system light/dark theme and works at phone width.

- **Sections:** what Viper does today, TON Drop (what works now and what is in progress), on-device AI, app screens.
- **Animations:** Google Noto Animated Emoji, the same ones Viper uses in onboarding, played with
  [lottie-web](https://github.com/airbnb/lottie-web) 5.12.2, served from `js/` (no third-party requests). They load only when scrolled into view
  and stay still when the system asks for reduced motion.
- **Screenshots:** Viper 1.5.34 screens rendered in the iOS simulator with sample data, and AI Chat on a Mac.

## Run it locally

```sh
git clone https://github.com/viperfoundation/viperfoundation.github.io
cd viperfoundation.github.io
python3 -m http.server 8765
# open http://localhost:8765/
```

## Languages

`index.html` (English) is the only template. Translations live in `i18n/<lang>.txt`; after editing English or a translation run `python3 i18n/build.py`, which rewrites `ru/ pt-br/ es/ uk/` and the switcher, hreflang links and footer language line. Screenshots per language: `docs/screenshots/i18n/`. Each page links to its own App Store storefront (us, ru, br, mx, ua). /ru/ shows the Russian app screens (`img/ru/`); the app has no es/uk/pt UI, /es/, /uk/ and /pt-br/ show localized app screens from the l10n-es-uk-pt build (`img/<lang>/l10n-framed-*`, hero `img/<lang>/iphone-4-chat.jpg`); Route and People Nearby have no localized screen yet and stay English screens with translated headlines (`img/<lang>/framed-*`). The footer app-language list switches with `APP_L10N_SHIPPED` in `i18n/build.py`. de/fr/it/tr are parked in `i18n/parked/` (see NOTE.txt there).

## Deploy

GitHub Pages serves `main` from the repository root. Push to `main` and the site updates.
`404.html` keeps old links (such as `/landing`) landing on the home page.

## Credits

- Animated emoji: [Google Noto Emoji](https://googlefonts.github.io/noto-emoji-animation/), CC BY 4.0, unmodified
  (see `lotties/noto/NOTICE.md`).
- `lotties/ton-pack/` is left from the previous React build and is not used. That build itself is not published.

© Viper Foundation
