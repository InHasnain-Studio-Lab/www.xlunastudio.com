"""The apps on sale: one record each, which builds the app's own page and its card on the store page.
Every claim matches the app's Store listing and privacy page.
"""
import json
from html import escape

SITE = "https://xlunastudio.com/"

APPS = [
    {
        "slug": "xluna-os",
        "name": "XLUNA OS",
        "store": "9MXJ3LXCT264",
        "kind": "Desktop shell",
        "category": "DesktopEnhancementApplication",
        "tagline": "Your desktop, lit by the moon.",
        "title": "XLUNA OS | Live 3D wallpapers, App Hub and dock for Windows",
        "description": "XLUNA OS turns Windows into a moonlit desk: live 3D wallpapers that move with your PC, an App Hub for every app, a dock with live previews and real-time widgets. Pay once, try free for 24 hours.",
        "brief": "A moonlit desktop for Windows: live 3D wallpapers that move with your PC, an App Hub for every app, a dock with live window previews and widgets that report the real numbers.",
        "overview": [
            "Want a desktop that feels alive instead of a flat picture, and to see what your PC is doing without opening a single tool? XLUNA OS turns your screen into a moonlit desk.",
            "Its live wallpapers move with your processor, memory and network, from a 3D Moon drawn from NASA's lunar maps to Saturn, a solar eclipse and a spiral galaxy. The App Hub gathers every desktop and Microsoft Store app on your PC, the dock keeps your pinned apps and every open window with live previews, and the widgets report the real numbers.",
            "Replacing the Windows taskbar with its dock is your choice on first run, and Windows comes back the moment you exit.",
        ],
        "tags": ["Desktop shell", "Live wallpapers", "App Hub", "Widgets"],
        "highlights": [
            "Live 3D wallpapers, from a NASA-mapped Moon to Saturn, that move with your PC",
            "App Hub with every desktop and Microsoft Store app, pin any in a click",
            "A dock with pinned apps, every open window and live previews",
            "Clocks, system gauges, a 7-day forecast, media and notes",
            "Frosted Glass or Moonlight Glass in five luminous inks",
            "Command palette, focus countdown, Zen mode and screen capture",
        ],
        "shots": [
            "The XLUNA OS particle wallpaper with widgets and the dock",
            "The App Hub over a live wallpaper",
            "The 3D Moon wallpaper with the control centre",
            "About, with the licence and integrity badges",
        ],
        "net": "Two requests only: the Microsoft Store licence check and the weather forecast for the city you choose.",
        "faq": [
            ("Does XLUNA OS collect any data about me?", "No. XLUNA OS has no telemetry, no analytics and no advertising code. The processor, memory and network readings it shows are read on your PC to draw your widgets and wallpaper, and are never sent anywhere."),
            ("Do I need an account?", "No. There is nothing to sign up for or sign in to. You install it from the Microsoft Store and it works."),
            ("Does XLUNA OS work offline?", "Yes. Everything except the weather forecast works without a connection. The app goes online only for the Microsoft Store licence check and for the forecast for the city you choose."),
            ("Where are my settings and notes kept?", "In the app's own folder on your PC. Screen captures go to your Pictures folder, only when you take one. Uninstalling the app removes its folder."),
        ],
        "files": "Settings and notes stay in the app's own folder; screen captures go to your Pictures folder, only when you take one.",
    },
    {
        "slug": "xfidelity-ultra",
        "name": "XFidelity Ultra",
        "store": "9P76NLF7K78F",
        "kind": "Audio enhancer",
        "category": "MultimediaApplication",
        "tagline": "Make everything you play sound bigger.",
        "title": "XFidelity Ultra | Surround, 8D and bass enhancer for Windows",
        "description": "XFidelity Ultra makes every app your PC plays sound wider, deeper and clearer: cinema surround, Orbit 8D, deep bass and clear voices on the speakers or headphones you own. Pay once, try free for 24 hours.",
        "brief": "One power button and every app your PC plays sounds wider, deeper and clearer, from the speakers or headphones you already own.",
        "overview": [
            "Want cinema sound from your PC without buying new gear, or headphone audio that stops sitting flat inside your head? XFidelity Ultra answers both with one press of the power button.",
            "Every app you play sounds wider, deeper and clearer, processed live on your own PC. Fifteen experiences cover films, music and games, from Cinema and Surround to Orbit 8D, Hyper 3D and Bass Titan, and Vocal Focus brings dialogue to the front.",
            "Shape the result with Intensity, Bass, Width, Space and Clarity, a ten band equalizer and an adjustable limiter, and hold Hear the original to compare at the same loudness.",
        ],
        "tags": ["Audio", "Surround", "8D", "Equalizer"],
        "highlights": [
            "Every app Windows plays is enhanced automatically",
            "Fifteen experiences: Cinema, Surround, Orbit 8D, Hyper 3D, Bass Titan and more",
            "Dialogue brought forward with Vocal Focus and Crystal Air",
            "Intensity, Bass, Width, Space and Clarity controls",
            "Ten band equalizer and an adjustable limiter",
            "Hear the original to compare at the same loudness",
        ],
        "shots": [
            "The Surround experience with the live reactor and spectrum",
            "Settings, with output device, glass mode and inks",
            "Help and tips",
            "About, with the licence and integrity details",
        ],
        "net": "One request only: the Microsoft Store licence check. Your audio is never recorded or sent anywhere.",
        "faq": [
            ("Does XFidelity Ultra record or upload my audio?", "No. Your sound is enhanced live in memory on your PC. It is never recorded, saved or sent anywhere."),
            ("Do I need an account?", "No. There is nothing to sign up for or sign in to. You install it from the Microsoft Store and it works."),
            ("Does XFidelity Ultra work offline?", "Yes. The only time it goes online is the Microsoft Store licence check that confirms your trial or purchase."),
            ("Does it collect any data?", "No. XFidelity Ultra has no telemetry, no analytics and no advertising code. It keeps only its own settings, in its folder on your PC."),
        ],
        "files": "Only the app's settings are kept, in its own folder on your PC.",
    },
]


def store_url(app):
    return f"https://apps.microsoft.com/detail/{app['store']}"


def page_file(app):
    return f"apps/{app['slug']}.html"


def page_url(app):
    return f"{SITE}apps/{app['slug']}"


def card(app):
    a = {k: escape(v) if isinstance(v, str) else v for k, v in app.items()}
    tags = "".join(f"<li>{escape(t)}</li>" for t in app["tags"])
    return f"""      <article class="launch">
        <a class="launch-shot" href="/apps/{a['slug']}" aria-label="{a['name']} details"><img src="/assets/apps/{a['slug']}/hero.jpg" alt="{a['name']} promotional artwork" loading="lazy" width="1920" height="1080"></a>
        <div class="launch-body">
          <div class="launch-id"><img src="/assets/apps/{a['slug']}/icon.png" alt="" width="56" height="56"><div><span class="eyebrow">{a['kind']}</span><h3><a href="/apps/{a['slug']}">{a['name']}</a></h3></div><span class="soon live">Available now</span></div>
          <p class="launch-tag">{a['tagline']}</p>
          <p>{a['brief']}</p>
          <ul class="slot-tags">{tags}</ul>
          <div class="cta"><a class="btn primary" href="{store_url(app)}" target="_blank" rel="noopener">Get it on Microsoft Store</a><a class="btn ghost" href="/apps/{a['slug']}">View details</a></div>
        </div>
      </article>
"""


def body(app):
    a = {k: escape(v) if isinstance(v, str) else v for k, v in app.items()}
    overview = "\n".join(f"      <p>{escape(p)}</p>" for p in app["overview"])
    highlights = "".join(f"<li>{escape(h)}</li>" for h in app["highlights"])
    faq = "\n".join(f'      <details><summary>{escape(q)}</summary><p>{escape(ans)}</p></details>' for q, ans in app["faq"])
    shots = "\n".join(
        f'      <a class="frame shot" href="/assets/apps/{a["slug"]}/shot-{i}.jpg" target="_blank" rel="noopener"><img src="/assets/apps/{a["slug"]}/shot-{i}.jpg" alt="{escape(c)}" loading="lazy"><span class="coord">{escape(c)}</span></a>'
        for i, c in enumerate(app["shots"], 1))
    return f"""  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/store">Store</a><span aria-hidden="true">/</span><span aria-current="page">{a['name']}</span></nav>

  <section class="hero short app-top" aria-labelledby="app-h">
    <div class="app-id"><img src="/assets/apps/{a['slug']}/icon.png" alt="" width="64" height="64"><div><span class="eyebrow">{a['kind']} · Available now</span><h1 id="app-h">{a['name']}</h1></div></div>
    <p class="lede"><strong>{a['tagline']}</strong> {a['brief']}</p>
    <div class="app-badges"><a class="badge-pf" href="/privacy-first">Privacy-first</a><span>Pay once</span><span>24h free trial</span><span>No account</span><span>Windows 10 &amp; 11</span></div>
    <div class="cta"><a class="btn primary" href="{store_url(app)}" target="_blank" rel="noopener">Get it on Microsoft Store</a><a class="btn ghost" href="/store">All apps</a></div>
  </section>

  <section class="app-hero-shot" aria-label="{a['name']} artwork">
    <img src="/assets/apps/{a['slug']}/hero.jpg" alt="{a['name']} promotional artwork" width="1920" height="1080">
  </section>

  <section aria-labelledby="ov-h">
    <span class="eyebrow">Overview</span>
    <h2 id="ov-h">What {a['name']} does for you</h2>
    <div class="app-copy">
{overview}
    </div>
  </section>

  <section aria-labelledby="hl-h">
    <span class="eyebrow">Highlights</span>
    <h2 id="hl-h">What you get in version 1.0</h2>
    <ul class="highlights" style="margin-top:20px">{highlights}</ul>
  </section>

  <section aria-labelledby="sh-h">
    <span class="eyebrow">Screenshots</span>
    <h2 id="sh-h">See it on a real desktop</h2>
    <div class="preview-frames">
{shots}
    </div>
  </section>

  <section aria-labelledby="sp-h">
    <span class="eyebrow">Specs</span>
    <h2 id="sp-h">Before you install</h2>
    <dl class="ledger" style="margin-top:20px;max-width:780px">
      <div><dt>Platforms</dt><dd>Windows 10 (version 2004 or later) and Windows 11, x64</dd></div>
      <div><dt>Pricing</dt><dd>Single purchase, lifetime licence · the Store shows your local price</dd></div>
      <div><dt>Trial</dt><dd>24 hours with every feature</dd></div>
      <div><dt>Updates</dt><dd>Included</dd></div>
      <div><dt>Account</dt><dd>Not required</dd></div>
      <div><dt>Get it from</dt><dd><a href="{store_url(app)}" target="_blank" rel="noopener">Microsoft Store</a></dd></div>
      <div><dt>Developer</dt><dd>XLUNA&trade;</dd></div>
    </dl>
  </section>

  <section aria-labelledby="pv-h">
    <span class="eyebrow">Privacy</span>
    <h2 id="pv-h">Your data stays on your PC</h2>
    <div class="privacy-label" style="margin-top:20px">
      <div><b>Data collected</b><span>None. No telemetry or analytics.</span></div>
      <div><b>Account</b><span>None. Nothing to sign up for or sign in to.</span></div>
      <div><b>Your files</b><span>{a['files']}</span></div>
      <div><b>Internet use</b><span>{a['net']}</span></div>
    </div>
    <p class="note" style="margin-top:12px">Read the full <a href="/privacy/{a['slug']}">{a['name']} privacy policy</a>, or the studio's <a href="/privacy-first">privacy-first promise</a>.</p>
  </section>

  <section aria-labelledby="faq-h">
    <span class="eyebrow">Questions</span>
    <h2 id="faq-h">{a['name']} and your privacy</h2>
    <div class="faq">
{faq}
    </div>
  </section>
"""


def jsonld(app):
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "@id": page_url(app) + "#app",
                "name": app["name"],
                "description": app["description"],
                "url": page_url(app),
                "applicationCategory": app["category"],
                "operatingSystem": "Windows 10, Windows 11",
                "image": f"{SITE}assets/apps/{app['slug']}/hero.jpg",
                "screenshot": [f"{SITE}assets/apps/{app['slug']}/shot-{i}.jpg" for i in range(1, len(app["shots"]) + 1)],
                "installUrl": store_url(app),
                "publisher": {"@type": "Organization", "name": "XLUNA", "url": SITE},
                "author": {"@type": "Person", "name": "Hasnain Butt Akhtar"},
            },
            {
                "@type": "FAQPage",
                "@id": page_url(app) + "#faq",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in app["faq"]],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "Store", "item": SITE + "store"},
                    {"@type": "ListItem", "position": 3, "name": app["name"], "item": page_url(app)},
                ],
            },
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data) + "</script>\n"
