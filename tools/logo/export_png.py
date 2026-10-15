"""Exports the XLUNA SVG logos to transparent PNGs (and favicon.ico) with headless Microsoft Edge.
Run: python tools/logo/export_png.py
"""
import os
import pathlib
import subprocess
import tempfile
import time

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
LOGO = ROOT / "assets" / "logo"
EDGE = next(p for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(p))


def shoot(html, w, h):
    tmp = pathlib.Path(tempfile.gettempdir())
    page, out = tmp / "xluna_export.html", tmp / "xluna_export.png"
    page.write_text(html, encoding="utf-8")
    if out.exists():
        out.unlink()
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--default-background-color=00000000", "--force-device-scale-factor=1",
                    "--user-data-dir=" + str(tmp / "xluna-edge"), f"--window-size={w},{h}",
                    "--screenshot=" + str(out), page.as_uri()], capture_output=True, timeout=120)
    for _ in range(60):
        if out.exists() and out.stat().st_size:
            break
        time.sleep(0.5)
    time.sleep(0.4)
    img = Image.open(out).convert("RGBA").crop((0, 0, w, h))
    out.unlink()
    return img


def svg(name, w, h, style=""):
    return f'<html><body style="margin:0;background:transparent"><img src="{(LOGO / name).as_uri()}" style="width:{w}px;height:{h}px;display:block;{style}"></body></html>'


def main():
    mark = shoot(svg("xluna-mark.svg", 1024, 1024), 1024, 1024)
    mark.save(LOGO / "xluna-mark-1024.png")
    for s in (512, 192, 180, 32):
        mark.resize((s, s), Image.LANCZOS).save(LOGO / f"xluna-mark-{s}.png")
    mark.resize((256, 256), Image.LANCZOS).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (256, 256)])
    lock_html = (f'<html><body style="margin:0;background:transparent;display:flex;align-items:center;gap:56px;width:2400px;height:560px">'
                 f'<img src="{(LOGO / "xluna-mark.svg").as_uri()}" style="width:560px;height:560px">'
                 f'<img src="{(LOGO / "xluna-wordmark.svg").as_uri()}" style="width:1700px;height:auto"></body></html>')
    shoot(lock_html, 2400, 560).save(LOGO / "xluna-lockup-2400.png")
    print("exported mark, favicon and lockup")


if __name__ == "__main__":
    main()
