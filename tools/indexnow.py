"""Tells IndexNow search engines (Bing, Yandex, Seznam, Naver) about every page in the live sitemap. Run after a deploy."""
import json
import re
import urllib.request

KEY = "ff1f2703606e012e996b813e773c3e37"
SITE = "https://xlunastudio.com/"

UA = {"User-Agent": "XLUNA-IndexNow/1.0 (+https://xlunastudio.com)"}
sitemap = urllib.request.urlopen(urllib.request.Request(SITE + "sitemap.xml", headers=UA)).read().decode("utf-8")
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
body = json.dumps({"host": "xlunastudio.com", "key": KEY, "keyLocation": f"{SITE}{KEY}.txt", "urlList": urls}).encode("utf-8")
request = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={**UA, "Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(request) as response:
    print(response.status, len(urls), "urls submitted")
