"""Stamps the shared head, header and footer around each page body in tools/pages and writes the site's HTML files.
Run: python tools/build_pages.py
"""
import json
import os
from datetime import date

import apps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "tools", "pages")

PAGES = [
    ("index.html", "Home", "XLUNA™ | Windows apps studio: XLUNA OS and XFidelity Ultra", "XLUNA™ is an independent software studio making Windows apps you own outright: XLUNA OS, a moonlit 3D desktop, and XFidelity Ultra, a surround sound enhancer. Pay once, try free for 24 hours.", "home"),
    ("store.html", "Store", "XLUNA™ Store | XLUNA OS and XFidelity Ultra for Windows", "The XLUNA launch bay: XLUNA OS and XFidelity Ultra, available now on the Microsoft Store. Pay once, try free for 24 hours.", "store"),
    ("about.html", "About", "About XLUNA™ | Founder, story and concept", "XLUNA™ is an independent software studio founded by Hasnain Butt Akhtar in England, named for the new moon and the orbits around it.", "about"),
    ("contact.html", "Contact", "Contact XLUNA™", "Reach XLUNA™ at contact@xlunastudio.com for app ideas, support, partnerships and press.", "contact"),
    ("privacy.html", "Privacy", "XLUNA™ Privacy Policy", "How XLUNA™ handles information on xlunastudio.com and in its apps.", "privacy"),
    ("privacy/xluna-os.html", "Privacy", "XLUNA OS Privacy Policy | XLUNA™", "How XLUNA OS keeps your desk, settings and readings on your own PC.", "privacy-xluna-os"),
    ("privacy/xfidelity-ultra.html", "Privacy", "XFidelity Ultra Privacy Policy | XLUNA™", "How XFidelity Ultra processes your sound on your own PC and keeps nothing but its settings.", "privacy-xfidelity-ultra"),
]
SITE = "https://xlunastudio.com/"
STORE_PUBLISHER = "https://apps.microsoft.com/search/publisher?name=XLUNA"
JSONLD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": SITE + "#org", "name": "XLUNA", "alternateName": ["XLUNA™", "XLUNA Studio", "xlunastudio"],
         "description": "XLUNA is an independent software studio founded in England in 2026, making Windows apps that run on your own PC, need no account and are paid for once.",
         "url": SITE, "foundingDate": "2026", "foundingLocation": {"@type": "Place", "name": "England, United Kingdom"},
         "logo": {"@type": "ImageObject", "url": SITE + "assets/logo/xluna-mark-512.png", "width": 512, "height": 512},
         "email": "contact@xlunastudio.com",
         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": "contact@xlunastudio.com", "url": SITE + "contact"},
         "founder": {"@type": "Person", "name": "Hasnain Butt Akhtar"},
         "sameAs": [STORE_PUBLISHER] + [apps.store_url(a) for a in apps.APPS]},
        {"@type": "WebSite", "@id": SITE + "#site", "name": "XLUNA", "alternateName": ["XLUNA™", "XLUNA Studio"], "url": SITE, "inLanguage": "en", "publisher": {"@id": SITE + "#org"}},
        {"@type": "ItemList", "@id": SITE + "#apps", "name": "XLUNA apps for Windows",
         "itemListElement": [{"@type": "ListItem", "position": i, "url": apps.page_url(a), "name": a["name"]} for i, a in enumerate(apps.APPS, 1)]},
    ],
}) + "</script>\n"
PAGES += [(apps.page_file(a), "Store", a["title"], a["description"], "app:" + a["slug"]) for a in apps.APPS]
APP_BY_SCENE = {"app:" + a["slug"]: a for a in apps.APPS}
APP_LINKS = "".join(f'<a href="/apps/{a["slug"]}">{a["name"]}</a>' for a in apps.APPS)
CLEAN = {**{apps.page_file(a): "/apps/" + a["slug"] for a in apps.APPS}, "index.html": "/", "store.html": "/store", "about.html": "/about", "contact.html": "/contact", "privacy.html": "/privacy", "privacy/xluna-os.html": "/privacy/xluna-os", "privacy/xfidelity-ultra.html": "/privacy/xfidelity-ultra"}
NAV = ("index.html", "store.html", "about.html", "contact.html")

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{canonical}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="XLUNA">
<meta name="application-name" content="XLUNA">
<meta name="apple-mobile-web-app-title" content="XLUNA">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta name="theme-color" content="#04060c">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/logo/xluna-mark-32.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/logo/xluna-mark-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700&family=Manrope:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{jsonld}</head>
<body data-scene="{scene}">
<canvas id="universe" aria-hidden="true"></canvas>
<div class="veil" aria-hidden="true"></div>

<header class="site-head">
  <a class="brand" href="/" aria-label="XLUNA home">
    <img class="badge" src="/assets/logo/xluna-mark.svg" alt="" width="38" height="38">
    <img class="word" src="/assets/logo/xluna-wordmark.svg" alt="XLUNA" width="80" height="18">
  </a>
  <nav class="site-nav" aria-label="Main">
{nav}
  </nav>
</header>

<main>
"""

FOOT = """</main>

<footer class="site-foot">
  <div style="display:grid;gap:10px">
    <a class="brand" href="/" aria-label="XLUNA home"><img class="badge" src="/assets/logo/xluna-mark.svg" alt="" width="38" height="38"><img class="word" src="/assets/logo/xluna-wordmark.svg" alt="XLUNA" width="80" height="18"></a>
    <p>&copy; 2026 XLUNA&trade;. Developed by Hasnain Butt Akhtar.</p>
    <p>XLUNA&trade; and Hasnain Studio X&trade; are trademarks of Hasnain Butt Akhtar.</p>
    <p>No cookies. No analytics. Nothing tracked.</p>
  </div>
  <nav class="links" aria-label="Footer">
    <a href="/">Home</a><a href="/store">Store</a>{app_links}<a href="/about">About</a><a href="/contact">Contact</a><a href="/privacy">Privacy</a>
  </nav>
</footer>
{scripts}
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="/assets/universe.js"></script>
</body>
</html>
"""


def noindex(file):
    # Policies stay reachable from the footer, the apps and their Store listings, but are kept out of search.
    return file.startswith("privacy")


def build():
    for file, label, title, desc, scene in PAGES:
        current = "store.html" if scene in APP_BY_SCENE else file
        nav = "\n".join(
            f'    <a href="{CLEAN[f]}"' + (' aria-current="page"' if f == current else "") + f">{n}</a>" for f, n, *_ in PAGES if f in NAV
        )
        image = "https://xlunastudio.com/assets/logo/xluna-mark-1024.png"
        if scene in APP_BY_SCENE:
            app = APP_BY_SCENE[scene]
            body, scripts, jsonld = apps.body(app), "", apps.jsonld(app)
            image = f"{SITE}assets/apps/{app['slug']}/hero.jpg"
            scene = "store"
        else:
            body = open(os.path.join(SRC, scene + ".body.html"), encoding="utf-8").read()
            body = body.replace("<!--APP_CARDS-->", "".join(apps.card(a) for a in apps.APPS))
            script_path = os.path.join(SRC, scene + ".script.html")
            scripts = open(script_path, encoding="utf-8").read() if os.path.exists(script_path) else ""
            jsonld = JSONLD if file == "index.html" else ""
        canonical = SITE + CLEAN[file].lstrip("/")
        robots = '<meta name="robots" content="noindex, follow">\n' if noindex(file) else ""
        html = HEAD.format(title=title, desc=desc, scene=scene, nav=nav, canonical=canonical, jsonld=jsonld, robots=robots, image=image) + body + FOOT.format(scripts=scripts, app_links=APP_LINKS)
        os.makedirs(os.path.dirname(os.path.join(ROOT, file)), exist_ok=True)
        open(os.path.join(ROOT, file), "w", encoding="utf-8", newline="\n").write(html)
        print("wrote", file)
    urls = "\n".join(f"  <url><loc>{SITE + CLEAN[f].lstrip('/')}</loc><lastmod>{date.today().isoformat()}</lastmod></url>" for f, *_ in PAGES if not noindex(f))
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sitemap)
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    build()
