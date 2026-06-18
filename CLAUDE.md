# Trip Tunes — Website

Marketing site, press kit, and privacy policy for **Trip Tunes**, the iOS
road-trip playlist app. Static HTML/CSS/JS — **no build step, no backend** —
served by Cloudflare Pages at **https://triptunes.xyz**.

> The app itself lives in a **separate repo** (`../triptunes`, the iOS/Swift
> project). Sessions have often edited this site from that repo's directory, but
> this site is its own Git repo (`jrames/triptunes-website`) and deploys on its
> own. Keep app vs. site changes in their respective repos.

## Structure (this folder is the deploy root)

```
index.html        homepage                      → triptunes.xyz/
press-kit/        press kit                     → triptunes.xyz/press-kit/
privacy/          privacy policy (iOS app)      → triptunes.xyz/privacy/
assets/
  app/            cassette + spool art, app icon (real assets from the app)
  fonts/          DeliciousHandrawn-Regular.ttf  (the app font)
  screenshots/    framed-*.png device-framed shots used on the homepage
  press/          press-kit screenshots + feature images
  video/          demo video + poster + mask     (see "Demo video" below)
CNAME / .nojekyll / README.md
_archive/         earlier design demos — NOT deployed
```

Each page is a **single self-contained file** with an inline `<style>` and
(homepage) inline `<script>`. No shared CSS/JS files — if you change a brand
token or the footer, update each page. Shared design language: CSS vars
`--coral #FA8E85 / --cream #F6F1E4 / --navy #011E2D / --gold #F4C20D /
--rust #C9462F`, headings in the **Delicious Handrawn** hand font (`@font-face`),
body in system serif/sans.

## Build, preview, deploy

- **No build.** Preview locally: `python3 -m http.server 8080` from this folder,
  then http://localhost:8080/ (and `/press-kit/`, `/privacy/`).
- **Deploy:** Cloudflare Pages, auto-builds on **push to `main`** (preset = None,
  build command empty, output dir `/`). A push redeploys the live site in ~1–2
  min. There is no staging — `main` is production.
- **Domain:** apex `triptunes.xyz` and `www` are Cloudflare Pages custom domains
  (apex DNS is a proxied CNAME → `triptunes-website.pages.dev`). The `CNAME` file
  is for GitHub Pages and ignored by Cloudflare.
- App Store ID `6467522749`; YouTube demo `youtube.com/shorts/nXyg_qppDD8`.

## Gotchas (most are hard-won)

- **Worker routes shadow Pages.** `share.triptunes.xyz` is a separate Cloudflare
  **Worker** (the share-links backend) — do not break it. A Worker *route* that
  matched the apex (`triptunes.xyz/*`) once intercepted the homepage and returned
  the worker's plain-text "Not found" even though the Pages domain was "Active" —
  **Worker routes take priority over Pages.** If the apex 404s, check Worker
  routes, not DNS.
- **Demo video must stay H.264 *level*-conformant** or Safari/iOS silently refuse
  to play it (Chrome is lenient, so headless renders look fine while real Safari
  is broken). Keep the frame size within the encoded level's macroblock limit
  (the current 814×1724 fits level 4.0; 1350×2760 did **not** and broke). Always
  `-pix_fmt yuv420p -color_range tv -movflags +faststart`, no audio, and bound the
  duration with `-t` (a looped-image filter input will otherwise encode forever).
- **The demo video is CSS-masked to the phone shape** via
  `-webkit-mask-image`/`mask-image` (`assets/video/demo-phone-mask.png`) so the
  page shows through the corners. This is deliberate: Safari **ignores**
  `overflow:hidden`+`border-radius` for clipping `<video>`, but **respects
  `mask-image`**. Don't "simplify" it back to border-radius clipping.
- The big source mockup `assets/video/Detail Mockup *.MP4` is **gitignored**
  (kept local, transcoded to `triptunes-demo-framed.mp4`). Same for `*.mov`,
  `raw-*`, `Simulator Screenshot*`, `_archive/`, and secrets.
- **Privacy policy is the iOS-app policy, verbatim.** Canonical copy is a GitHub
  gist; `/privacy/` is a styled duplicate — keep them in sync, and keep it
  app-focused (no website/analytics language, to avoid confusing App Store
  review).
- **Analytics: GoatCounter** (privacy-friendly, cookie-free, no consent banner).
  Script is on each page; click events use `data-goatcounter-click` (`appstore`,
  `press-kit`). It is intentionally **not** on `/privacy/`.

## Working style

- **Verify visual changes yourself** before asking the user: headless Chrome
  (`--headless=new --screenshot`) + `ffmpeg` to crop/extract frames + sample
  pixels with a small Swift/AppKit script, then view the PNGs. Caveat: **Chrome
  only** — you cannot render Safari, which is exactly where the `<video>` quirks
  bite, so reason about Safari explicitly.
- Match each file's existing inline style; don't introduce a build tool, a
  framework, or external CSS/JS without a reason.
