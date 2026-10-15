"""Stamps the shared head, header and footer around each page body in tools/pages and writes the site's HTML files.
Run: python tools/build_pages.py
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "tools", "pages")

PAGES = [
    ("index.html", "Home", "XLUNA Studio", "XLUNA Studio designs apps that run on your own machine and belong to you from the first purchase.", "home"),
    ("store.html", "Store", "XLUNA Store", "The XLUNA launch bay: seven charted orbits, their first apps in development, each docking with a full dossier.", "store"),
    ("about.html", "About", "About XLUNA Studio", "XLUNA is an independent studio founded by Hasnain Butt Akhtar, named for the moon and the orbits around it.", "about"),
    ("contact.html", "Contact", "Contact XLUNA Studio", "Reach XLUNA Studio at contact@xlunastudio.com for app ideas, support, partnerships and press.", "contact"),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://xlunastudio.com/assets/logo/xluna-badge-1024.png">
<meta name="theme-color" content="#04060c">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="assets/logo/xluna-badge-32.png" type="image/png">
<link rel="apple-touch-icon" href="assets/logo/xluna-badge-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700&family=Manrope:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body data-scene="{scene}">
<canvas id="universe" aria-hidden="true"></canvas>
<div class="veil" aria-hidden="true"></div>

<header class="site-head">
  <a class="brand" href="index.html" aria-label="XLUNA Studio home">
    <img class="badge" src="assets/logo/xluna-badge-192.png" alt="" width="38" height="38">
    <img class="word" src="assets/logo/xluna-wordmark.svg" alt="XLUNA" width="80" height="18">
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
    <a class="brand" href="index.html" aria-label="XLUNA Studio home"><img class="badge" src="assets/logo/xluna-badge-192.png" alt="" width="38" height="38"><img class="word" src="assets/logo/xluna-wordmark.svg" alt="XLUNA" width="80" height="18"></a>
    <p>&copy; 2026 XLUNA Studio. Developed by Hasnain Butt Akhtar.</p>
    <p>No cookies. No analytics. Nothing tracked.</p>
  </div>
  <nav class="links" aria-label="Footer">
    <a href="index.html">Home</a><a href="store.html">Store</a><a href="about.html">About</a><a href="contact.html">Contact</a>
  </nav>
</footer>
{scripts}
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="assets/universe.js"></script>
</body>
</html>
"""


def build():
    for file, label, title, desc, scene in PAGES:
        nav = "\n".join(
            f'    <a href="{f}"' + (' aria-current="page"' if f == file else "") + f">{n}</a>" for f, n, *_ in PAGES
        )
        body = open(os.path.join(SRC, scene + ".body.html"), encoding="utf-8").read()
        script_path = os.path.join(SRC, scene + ".script.html")
        scripts = open(script_path, encoding="utf-8").read() if os.path.exists(script_path) else ""
        html = HEAD.format(title=title, desc=desc, scene=scene, nav=nav) + body + FOOT.format(scripts=scripts)
        open(os.path.join(ROOT, file), "w", encoding="utf-8", newline="\n").write(html)
        print("wrote", file)


if __name__ == "__main__":
    build()
