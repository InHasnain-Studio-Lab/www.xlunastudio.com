"""Guides: one HTML file per article in tools/guides, each opening with an XLUNA:GUIDE JSON header.
Builds the article pages, the /guides index, their structured data and their place in the sitemap.
"""
import json
import os
import re
from datetime import date
from html import escape

import apps

SITE = "https://xlunastudio.com/"
SRC = os.path.join(os.path.dirname(__file__), "guides")
HEADER = re.compile(r"<!--XLUNA:GUIDE\s*(\{.*?\})\s*-->", re.S)


def load():
    guides = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".html"):
            continue
        text = open(os.path.join(SRC, name), encoding="utf-8").read()
        meta = json.loads(HEADER.search(text).group(1))
        meta["slug"] = name[:-5]
        meta["html"] = HEADER.sub("", text, count=1).strip()
        guides.append(meta)
    # Newest first on the index.
    return sorted(guides, key=lambda g: g["published"], reverse=True)


GUIDES = load()


def page_file(g):
    return f"guides/{g['slug']}.html"


def page_url(g):
    return f"{SITE}guides/{g['slug']}"


def nice_date(iso):
    return date.fromisoformat(iso).strftime("%d %B %Y").lstrip("0")


def related(g):
    by_slug = {a["slug"]: a for a in apps.APPS}
    blocks = []
    for slug in g.get("apps", []):
        a = by_slug[slug]
        blocks.append(f"""      <a class="art-app" href="/apps/{a['slug']}">
        <img src="/assets/apps/{a['slug']}/icon.png" alt="" width="48" height="48">
        <span><b>{escape(a['name'])}</b><span>{escape(a['tagline'])} {escape(a['kind'])} for Windows, from the Microsoft Store.</span></span>
      </a>""")
    if not blocks:
        return ""
    return """    <aside class="art-related" aria-label="Related XLUNA app">
      <span class="eyebrow">From XLUNA&trade;</span>
""" + "\n".join(blocks) + "\n    </aside>\n"


def body(g):
    others = [o for o in GUIDES if o["slug"] != g["slug"]][:3]
    more = ""
    if others:
        items = "".join(f'<li><a href="/guides/{o["slug"]}">{escape(o["nav"])}</a></li>' for o in others)
        more = f"""
  <section aria-labelledby="more-h" style="padding-top:30px">
    <span class="eyebrow">More guides</span>
    <h2 id="more-h">Keep reading</h2>
    <ul class="art-more">{items}</ul>
  </section>
"""
    return f"""  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/guides">Guides</a><span aria-hidden="true">/</span><span aria-current="page">{escape(g['nav'])}</span></nav>

  <article class="art" aria-labelledby="art-h">
    <header class="art-head">
      <span class="eyebrow">{escape(g['section'])} guide</span>
      <h1 id="art-h">{escape(g['h1'])}</h1>
      <p class="lede">{escape(g['standfirst'])}</p>
      <p class="coord">By Hasnain Butt Akhtar · XLUNA&trade; Studio · <time datetime="{g['published']}">{nice_date(g['published'])}</time></p>
    </header>
    <div class="art-body">
{g['html']}
    </div>
{related(g)}  </article>
{more}"""


def jsonld(g):
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": page_url(g) + "#article",
                "headline": g["h1"],
                "description": g["description"],
                "datePublished": g["published"],
                "dateModified": g.get("updated", g["published"]),
                "keywords": g.get("keywords", []),
                "articleSection": g["section"],
                "inLanguage": "en",
                "mainEntityOfPage": page_url(g),
                "image": f"{SITE}assets/logo/xluna-mark-1024.png",
                "author": {"@type": "Person", "name": "Hasnain Butt Akhtar", "url": "https://inhasnain.com"},
                "publisher": {"@type": "Organization", "@id": SITE + "#org", "name": "XLUNA™",
                              "logo": {"@type": "ImageObject", "url": SITE + "assets/logo/xluna-mark-512.png"}},
                "about": [{"@id": apps.page_url(a) + "#app"} for a in apps.APPS if a["slug"] in g.get("apps", [])],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "guides"},
                    {"@type": "ListItem", "position": 3, "name": g["nav"], "item": page_url(g)},
                ],
            },
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data) + "</script>\n"


def index_body():
    cards = "\n".join(f"""      <a class="guide-card" href="/guides/{g['slug']}">
        <span class="eyebrow">{escape(g['section'])}</span>
        <h2>{escape(g['nav'])}</h2>
        <p>{escape(g['standfirst'])}</p>
        <span class="coord"><time datetime="{g['published']}">{nice_date(g['published'])}</time></span>
      </a>""" for g in GUIDES)
    return f"""  <section class="hero short" aria-labelledby="guides-h">
    <span class="eyebrow phase-line" data-moon-phase>Tonight's moon</span>
    <h1 id="guides-h">XLUNA&trade; <em>guides</em></h1>
    <p class="lede">Plain, practical guides to getting more from your Windows PC: what really affects speed, sound and the look of your desk, written by the studio behind XLUNA's premium limited edition apps.</p>
  </section>

  <section aria-label="All guides" style="padding-top:10px">
    <div class="guide-grid">
{cards}
    </div>
  </section>
"""


def index_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "XLUNA™ guides",
        "url": SITE + "guides",
        "publisher": {"@id": SITE + "#org"},
        "hasPart": [{"@type": "Article", "headline": g["h1"], "url": page_url(g)} for g in GUIDES],
    }
    return '<script type="application/ld+json">' + json.dumps(data) + "</script>\n"
