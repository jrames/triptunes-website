#!/usr/bin/env python3
"""Generate the static /tapes/ gift-tape pages.

Inputs:
  tools/tapes.json              editorial table (slug, key, title, h1, blurb, ...)
  tools/tape-payloads/<slug>.json   the raw share-link JSON for each tape

Outputs (self-contained static HTML; the served site stays no-build):
  tapes/index.html              the hub gallery
  tapes/<slug>/index.html       one page per tape

To add a tape: drop its payload at tools/tape-payloads/<slug>.json, add a
matching entry to tools/tapes.json, then run:  python3 tools/build_tapes.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAYLOADS = os.path.join(ROOT, "tools", "tape-payloads")
TAPES = json.load(open(os.path.join(ROOT, "tools", "tapes.json")))
APP_STORE = "https://apps.apple.com/app/id6467522749"


def songs_for(slug):
    data = json.load(open(os.path.join(PAYLOADS, slug + ".json")))
    out = []
    for s in data.get("basicSongs", []):
        url = (s.get("artwork") or {}).get("url")
        if not (url and s.get("previewUrl") and s.get("id")):
            continue
        out.append({"t": s.get("title", ""), "a": s.get("artistName", ""),
                    "id": str(s.get("id")), "art": url, "p": s.get("previewUrl")})
    return out


def embed(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>@@TITLE@@</title>
  <meta name="description" content="@@META@@" />
  <link rel="canonical" href="https://triptunes.xyz/tapes/@@SLUG@@/" />
  <link rel="icon" href="../../assets/app/app-icon.png" />
  <meta property="og:title" content="@@H1@@ — Trip Tunes" />
  <meta property="og:description" content="@@META@@" />
  <meta property="og:image" content="https://triptunes.xyz/assets/app/app-icon.png" />
  <meta property="og:type" content="article" />
  <style>
    @font-face { font-family:"Delicious Handrawn"; src:url("../../assets/fonts/DeliciousHandrawn-Regular.ttf") format("truetype"); font-display:swap; }
    :root { --coral:#FA8E85; --rust:#C9462F; --cream:#F6F1E4; --paper:#FBF7EC; --navy:#011E2D; --gold:#F4C20D; --ink:#2c2620; --muted:#7a6c5f; --line:#e2d8c4; --hand:"Delicious Handrawn","Marker Felt",cursive; --mono:"Courier New",monospace; }
    * { box-sizing:border-box; margin:0; padding:0; }
    body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; color:var(--ink); line-height:1.6;
      background: radial-gradient(circle at 15% 6%, rgba(250,142,133,.16), transparent 42%),
                  radial-gradient(circle at 85% 5%, rgba(244,194,13,.14), transparent 40%),
                  repeating-linear-gradient(0deg, transparent 0 33px, rgba(58,42,34,.045) 33px 34px), var(--cream); }
    a { color:var(--rust); }
    .wrap { max-width:860px; margin:0 auto; padding:0 24px; }
    .ph { display:flex; align-items:center; gap:20px; padding:30px 0 14px; }
    .ph .iconlink { flex:none; line-height:0; border-radius:17px; transition:transform .15s ease; }
    .ph .iconlink:hover { transform:translateY(-2px); }
    .ph .iconlink img { width:78px; height:78px; border-radius:17px; box-shadow:0 6px 16px rgba(1,30,45,.2); }
    .ph .titles { min-width:0; }
    .kicker { font-family:var(--mono); text-transform:uppercase; letter-spacing:2px; font-size:.74rem; color:var(--rust); }
    .ph h1 { font-family:var(--hand); font-size:3rem; color:var(--navy); line-height:1.02; margin:4px 0 0; text-shadow:2px 2px 0 var(--coral); }
    .blurb { font-size:1.08rem; }
    .blurb p { margin:10px 0; }
    .stat { color:var(--muted); font-size:.9rem; margin-top:12px; }
    .cta-row { display:flex; gap:12px; flex-wrap:wrap; align-items:center; margin:20px 0 6px; }
    .btn-open { display:inline-flex; align-items:center; gap:8px; background:var(--coral); color:var(--navy); font-weight:700; text-decoration:none; padding:12px 20px; border-radius:10px; }
    .btn-open:hover { background:#f7766b; }
    .btn-store { color:var(--rust); text-decoration:none; font-size:.92rem; align-self:center; }
    ol.tracks { list-style:none; margin:18px 0 6px; }
    ol.tracks li { display:flex; align-items:center; gap:13px; padding:9px 8px; border-radius:10px; border-top:1px solid var(--line); }
    ol.tracks li:first-child { border-top:none; }
    ol.tracks li:hover { background:rgba(1,30,45,.035); }
    .num { color:var(--muted); width:22px; text-align:right; font-variant-numeric:tabular-nums; font-size:.85rem; flex:none; }
    .play { flex:none; width:42px; height:42px; border-radius:50%; border:none; cursor:pointer; background:var(--navy); color:#fff; display:grid; place-items:center; }
    .play.playing { background:var(--rust); }
    .art { width:52px; height:52px; border-radius:8px; object-fit:cover; flex:none; box-shadow:0 2px 6px rgba(1,30,45,.2); }
    .tk { flex:1; min-width:0; }
    .tk .t { font-weight:600; color:var(--navy); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .tk .a { color:var(--muted); font-size:.86rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .am { flex:none; font-size:.8rem; text-decoration:none; color:var(--rust); white-space:nowrap; opacity:.85; }
    .am:hover { opacity:1; text-decoration:underline; }
    .attribution { color:var(--muted); font-size:.78rem; margin:14px 0 0; max-width:64ch; }
    footer { text-align:center; color:var(--muted); font-size:.85rem; padding:30px 24px 44px; }
    footer a { color:var(--rust); }
    @media (max-width:520px){ .ph h1{font-size:2.2rem;} .ph .iconlink img{width:62px;height:62px;} .am{display:none;} }
  </style>
</head>
<body>
  <div class="wrap">
    <header class="ph">
      <a class="iconlink" href="/" aria-label="Trip Tunes home"><img src="../../assets/app/app-icon.png" alt="Trip Tunes"></a>
      <div class="titles">
        <div class="kicker">@@KICKER@@</div>
        <h1>@@H1@@</h1>
      </div>
    </header>
    <div class="blurb">@@BLURB@@</div>
    <div class="stat" id="stat"></div>
    <div class="cta-row">
      <a class="btn-open" data-goatcounter-click="tape-open-@@SLUG@@" href="@@OPEN_URL@@">&#9654; Open in Trip Tunes</a>
      <a class="btn-store" data-goatcounter-click="tape-store-@@SLUG@@" href="@@APP_STORE@@">Don't have it? Get Trip Tunes &rarr;</a>
    </div>
    <ol class="tracks" id="tracks"></ol>
    <p class="attribution">Song previews are streamed and provided courtesy of iTunes / Apple Music &mdash; tap any track to open it on Apple Music. Album artwork belongs to the respective rights holders. Trip Tunes isn't affiliated with Apple.</p>
  </div>
  <footer>
    <a href="/tapes/">&larr; All gift tapes</a> &middot; <a href="/">Trip Tunes</a> &middot; <a href="/privacy/">Privacy</a><br/><br/>
    &copy; 2026 Trip Tunes
  </footer>
  <script>
    const SONGS = @@SONGS@@;
    const gc = name => { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: name, title: name, event: true }); };
    const art = (tpl, px) => tpl.replace("{w}x{h}", px + "x" + px);
    const appleMusic = id => "https://music.apple.com/us/song/" + id;
    const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    document.getElementById('stat').textContent = SONGS.length + " songs · about " + Math.round(SONGS.length*3.7) + " min";
    const tracks = document.getElementById('tracks');
    const audio = new Audio(); let playingBtn = null;
    function stop(){ audio.pause(); if(playingBtn){ playingBtn.classList.remove('playing'); playingBtn.textContent='▶'; playingBtn=null; } }
    audio.addEventListener('ended', stop);
    tracks.innerHTML = SONGS.map((s,i)=>`
      <li>
        <span class="num">${i+1}</span>
        <button class="play" data-i="${i}" aria-label="Preview ${esc(s.t)}">▶</button>
        <img class="art" loading="lazy" src="${art(s.art,128)}" alt="${esc(s.t)} album art">
        <div class="tk"><div class="t">${esc(s.t)}</div><div class="a">${esc(s.a)}</div></div>
        <a class="am" href="${appleMusic(s.id)}" target="_blank" rel="noopener">Apple Music &#8599;</a>
      </li>`).join('');
    tracks.querySelectorAll('.play').forEach(btn=>{
      btn.onclick = () => {
        const i = +btn.dataset.i;
        if (playingBtn === btn) { stop(); return; }
        stop(); audio.src = SONGS[i].p; audio.play().catch(()=>{});
        gc("tape-play-@@SLUG@@");
        playingBtn = btn; btn.classList.add('playing'); btn.textContent='❚❚';
      };
    });
  </script>
  <!-- Printed-sticker QR attribution. The QR links here with ?ref=sticker, which
       GoatCounter records as a referrer automatically; this also fires a
       dedicated scan-sticker-@@SLUG@@ event so scans are countable on their own.
       Fires on load and retries until the async count.js loader is ready. -->
  <script>
    addEventListener('load', function () {
      if (new URLSearchParams(location.search).get('ref') !== 'sticker') return;
      (function fire(n) {
        if (window.goatcounter && window.goatcounter.count)
          window.goatcounter.count({ path: 'scan-sticker-@@SLUG@@', title: 'Sticker scan', event: true });
        else if (n < 50) setTimeout(function () { fire(n + 1); }, 100);
      })(0);
    });
  </script>
  <!-- GoatCounter — privacy-friendly analytics: counts pageviews + referrers
       automatically, plus tagged clicks (tape-open-*, tape-store-*) and the
       tape-play-* event fired on preview playback. -->
  <script data-goatcounter="https://triptunes.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""

HUB = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Free Road-Trip Mixtapes — Gift Tapes | Trip Tunes</title>
  <meta name="description" content="Free, hand-picked road-trip mixtapes from Trip Tunes — summer, fall, spring break, and the all-time classics. Preview every track, then open the playlist in the app." />
  <link rel="canonical" href="https://triptunes.xyz/tapes/" />
  <link rel="icon" href="../assets/app/app-icon.png" />
  <meta property="og:title" content="Free Road-Trip Mixtapes — Trip Tunes" />
  <meta property="og:description" content="Hand-picked road-trip mixtapes you can preview here and open in Trip Tunes." />
  <meta property="og:image" content="https://triptunes.xyz/assets/app/app-icon.png" />
  <meta property="og:type" content="website" />
  <style>
    @font-face { font-family:"Delicious Handrawn"; src:url("../assets/fonts/DeliciousHandrawn-Regular.ttf") format("truetype"); font-display:swap; }
    :root { --coral:#FA8E85; --rust:#C9462F; --cream:#F6F1E4; --paper:#FBF7EC; --navy:#011E2D; --gold:#F4C20D; --ink:#2c2620; --muted:#7a6c5f; --line:#e2d8c4; --hand:"Delicious Handrawn","Marker Felt",cursive; --mono:"Courier New",monospace; }
    * { box-sizing:border-box; margin:0; padding:0; }
    body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; color:var(--ink); line-height:1.6;
      background: radial-gradient(circle at 15% 8%, rgba(250,142,133,.18), transparent 42%),
                  radial-gradient(circle at 85% 6%, rgba(244,194,13,.16), transparent 40%),
                  repeating-linear-gradient(0deg, transparent 0 33px, rgba(58,42,34,.045) 33px 34px), var(--cream); }
    a { color:var(--rust); }
    .wrap { max-width:860px; margin:0 auto; padding:0 24px; }
    .ph { display:flex; align-items:center; gap:20px; padding:30px 0 8px; }
    .ph .iconlink { flex:none; line-height:0; border-radius:17px; transition:transform .15s ease; }
    .ph .iconlink:hover { transform:translateY(-2px); }
    .ph .iconlink img { width:78px; height:78px; border-radius:17px; box-shadow:0 6px 16px rgba(1,30,45,.2); }
    .ph .titles { min-width:0; }
    .kicker { font-family:var(--mono); text-transform:uppercase; letter-spacing:2px; font-size:.74rem; color:var(--rust); }
    .ph h1 { font-family:var(--hand); font-size:3.2rem; color:var(--navy); line-height:1.02; margin:4px 0 0; text-shadow:2px 2px 0 var(--coral); }
    .lead { margin:12px 0 0; }
    .gallery { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:26px; padding:28px 0 10px; }
    .tape-card { display:block; text-decoration:none; color:inherit; background:var(--paper); border:1px solid var(--line); border-radius:14px; overflow:hidden;
      transition:transform .15s ease, box-shadow .15s ease; box-shadow:0 8px 22px rgba(1,30,45,.10); }
    .tape-card:hover { transform:translateY(-4px); box-shadow:0 16px 34px rgba(1,30,45,.18); }
    .mosaic { display:grid; grid-template-columns:1fr 1fr; aspect-ratio:1; }
    .mosaic img { width:100%; height:100%; object-fit:cover; display:block; }
    .meta { padding:14px 16px 16px; }
    .meta h2 { font-family:var(--hand); font-size:1.9rem; color:var(--navy); line-height:1; }
    .meta .teaser { color:var(--ink); font-size:.9rem; margin-top:6px; }
    .meta .sub { color:var(--muted); font-size:.8rem; margin-top:6px; }
    footer { text-align:center; color:var(--muted); font-size:.85rem; padding:30px 24px 44px; }
    footer a { color:var(--rust); }
    @media (max-width:520px){ .ph h1{font-size:2.4rem;} .ph .iconlink img{width:62px;height:62px;} }
  </style>
</head>
<body>
  <main class="wrap">
    <header class="ph">
      <a class="iconlink" href="/" aria-label="Trip Tunes home"><img src="../assets/app/app-icon.png" alt="Trip Tunes"></a>
      <div class="titles">
        <div class="kicker">Free Gift Tapes</div>
        <h1>Mixtapes, on the house.</h1>
      </div>
    </header>
    <p class="lead">Hand-picked road-trip mixtapes from Trip Tunes. Press play right on the page, then open the whole thing in the app &mdash; every track, ready for the drive.</p>
    <div class="gallery" id="gallery"></div>
  </main>
  <footer>
    <a href="/">&larr; Back to Trip Tunes</a> &middot; <a href="/privacy/">Privacy</a><br/><br/>
    &copy; 2026 Trip Tunes &middot; Previews &amp; artwork courtesy of iTunes / Apple Music, &copy; their respective owners.
  </footer>
  <script>
    const art = (tpl,px) => tpl.replace("{w}x{h}", px+"x"+px);
    const TAPES = @@INDEX@@;
    const g = document.getElementById('gallery');
    TAPES.forEach(t => {
      const a = document.createElement('a');
      a.className = 'tape-card'; a.href = `/tapes/${t.slug}/`;
      a.innerHTML = `<div class="mosaic">${t.cover.map(c=>`<img loading="lazy" src="${art(c,240)}" alt="">`).join('')}</div>
        <div class="meta"><h2>${t.name}</h2><div class="teaser">${t.teaser}</div><div class="sub">${t.count} songs &middot; preview &amp; open in the app</div></div>`;
      g.appendChild(a);
    });
  </script>
  <!-- GoatCounter — privacy-friendly analytics: counts pageviews + referrers. -->
  <script data-goatcounter="https://triptunes.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)


index = []
for t in TAPES:
    songs = songs_for(t["slug"])
    blurb_html = "".join(f"<p>{p}</p>" for p in t["blurb"])
    page = (PAGE
        .replace("@@TITLE@@", html.escape(t["title"], quote=True))
        .replace("@@META@@", html.escape(t["meta"], quote=True))
        .replace("@@SLUG@@", t["slug"])
        .replace("@@H1@@", html.escape(t["h1"]))
        .replace("@@KICKER@@", html.escape(t["kicker"]))
        .replace("@@BLURB@@", blurb_html)
        .replace("@@OPEN_URL@@", f"https://share.triptunes.xyz/p/{t['key']}")
        .replace("@@APP_STORE@@", APP_STORE)
        .replace("@@SONGS@@", embed(songs)))
    write(os.path.join(ROOT, "tapes", t["slug"], "index.html"), page)
    index.append({"slug": t["slug"], "name": t["h1"], "teaser": t["teaser"],
                  "count": len(songs), "cover": [s["art"] for s in songs[:4]]})
    print(f"  wrote tapes/{t['slug']}/  ({len(songs)} songs)")

write(os.path.join(ROOT, "tapes", "index.html"), HUB.replace("@@INDEX@@", embed(index)))
print(f"  wrote tapes/  (hub, {len(index)} tapes)")
