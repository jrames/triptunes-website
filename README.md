# Trip Tunes — Website & Press Kit

Static marketing site and press kit for **Trip Tunes**. No build step, no backend —
plain HTML/CSS/JS that can be served by any static host.

## Structure (this folder is the deploy root)

```
index.html        → the marketing homepage          (triptunes.xyz/)
press-kit/    → the press kit                    (triptunes.xyz/press-kit/)
assets/
  fonts/          → Delicious Handrawn (the app font)
  app/            → cassette + spool art, app icon
  screenshots/    → marketing screenshots (homepage)
  press/          → press-kit screenshots, feature images, app icon, asset .zip
CNAME             → custom domain for the host (triptunes.xyz)
.nojekyll         → tells GitHub Pages to serve files as-is (no Jekyll)
.gitignore        → excludes _archive/ and .DS_Store
_archive/         → earlier design demos (v2/v3) + the old stub; NOT deployed
```

## Deploy — Cloudflare Pages (recommended)

Cloudflare Pages' free plan covers this completely (unlimited sites/requests/
bandwidth, 500 builds/mo, custom domains). Since the domain and
`share.triptunes.xyz` already live on Cloudflare, this keeps everything in one place.

1. Put this folder in a git repo and push to GitHub/GitLab.
2. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git**,
   pick the repo.
3. Build settings: **Framework preset = None**, **Build command = (empty)**,
   **Build output directory = `/`** (the site is already built).
4. Deploy. You'll get a `*.pages.dev` URL to verify.
5. **Custom domain:** Pages project → **Custom domains → Set up** → add
   `triptunes.xyz` (and `www.triptunes.xyz`). Because DNS is already on Cloudflare,
   it adds the records and TLS automatically. (The `CNAME` file is for GitHub Pages;
   Cloudflare ignores it — harmless to keep.)

`share.triptunes.xyz` is untouched — only the apex + `www` point at Pages.

## Deploy — GitHub Pages (alternative)

1. Push this folder to a repo (e.g. a new `triptunes-site`, or under
   `jrames.github.io`). Settings → **Pages** → Source = your branch, root.
2. The `CNAME` file already contains `triptunes.xyz`, so Pages picks it up.
3. **DNS** (at your registrar / Cloudflare DNS):
   - Apex `triptunes.xyz` → four **A** records: `185.199.108.153`,
     `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     (and the matching AAAA records if you want IPv6).
   - `www` → **CNAME** to `<username>.github.io`.
   - If DNS is on Cloudflare, set those records to **DNS-only** (grey cloud) while
     GitHub provisions the certificate, then you can re-enable proxy.
4. Settings → Pages → **Enforce HTTPS**.

## Still to fill in

- Optional: a dedicated social-share image (1200×630) for `og:image` — currently
  uses the app icon.

## Local preview

`python3 -m http.server` from this folder, then visit http://localhost:8000
(homepage) and http://localhost:8000/press-kit/.
