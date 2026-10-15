"""Renders the XLUNA brand mark: a photoreal waxing-crescent moon crossed by two glowing orbits on a deep-space badge.

Outputs (assets/logo): xluna-badge-{2048,1024,512,192,180,32}.png and favicon.ico at the site root.
Run: python tools/logo/render_logo.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "logo")
S = 2048
rng = np.random.default_rng(7)

# Major near-side features in selenographic degrees: (lat, lon, lat radius, lon radius, darkness).
MARIA = [
    (10, -56, 30, 21, 0.55), (33, -16, 16, 18, 0.62), (28, 17, 10, 11, 0.6), (8, 30, 11, 13, 0.6),
    (17, 59, 7, 9, 0.62), (-7, 51, 10, 8, 0.55), (-15, 35, 6, 6, 0.55), (-21, -17, 11, 12, 0.5),
    (-24, -39, 6, 6, 0.55), (56, 0, 5, 38, 0.45), (13, 4, 4, 5, 0.5), (-10, -23, 5, 5, 0.45), (7, -31, 7, 8, 0.45),
]
CRATERS = [(-43, -11, 3.2, 0.9), (9.6, -20, 3.0, 0.55), (8, -38, 1.6, 0.5), (23.7, -47.4, 1.3, 1.0)]


def albedo(lat, lon):
    a = np.full(lat.shape, 0.78)
    for la, lo, rla, rlo, dark in MARIA:
        d = ((lat - la) / rla) ** 2 + ((lon - lo) / rlo) ** 2
        a -= dark * 0.55 * np.clip(1.2 - d, 0, 1) ** 1.4
    for la, lo, r, glow in CRATERS:
        d = np.sqrt((lat - la) ** 2 + ((lon - lo) * np.cos(np.radians(la))) ** 2)
        a += glow * 0.35 * np.exp(-(d / r) ** 2)
    # Tycho's ray system across the southern highlands.
    ty_la, ty_lo = -43, -11
    ang = np.arctan2(lat - ty_la, (lon - ty_lo) * np.cos(np.radians(ty_la)))
    dist = np.hypot(lat - ty_la, lon - ty_lo)
    rays = np.clip(np.cos(ang * 9 + 0.7) ** 40 + np.cos(ang * 13 + 2.1) ** 60, 0, 1)
    a += 0.12 * rays * np.exp(-dist / 45)
    return np.clip(a, 0.1, 1.0)


def noise(h, w, scale, seed):
    r = np.random.default_rng(seed).random((h // scale + 2, w // scale + 2))
    img = Image.fromarray((r * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(img, dtype=np.float32) / 255.0


def moon_layer(size, radius, phase_e):
    """phase_e: elongation in radians (0 new, pi full). Waxing phases light the right limb."""
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    nx = (x - size / 2) / radius
    ny = -(y - size / 2) / radius
    r2 = nx ** 2 + ny ** 2
    inside = r2 <= 1
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    lat = np.degrees(np.arcsin(np.clip(ny, -1, 1)))
    lon = np.degrees(np.arctan2(nx, nz))
    alb = albedo(lat, lon)
    tex = 0.86 + 0.14 * noise(size, size, 6, 1) * 0.6 + 0.14 * noise(size, size, 2, 2) * 0.4
    craters = 1 - 0.18 * np.clip(noise(size, size, 18, 3) - 0.62, 0, 1) * 3
    alb = alb * tex * craters
    L = np.array([math.sin(phase_e), 0.18, -math.cos(phase_e)])
    L /= np.linalg.norm(L)
    lambert = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    # Soft terminator, lunar-like flat limb brightness.
    lit = np.clip(lambert * 1.6, 0, 1) ** 0.75
    earthshine = 0.075 * (1 - lit)
    lum = alb * (lit * 1.08 + earthshine)
    rgb = np.stack([lum * 0.97, lum * 0.99, lum * 1.04], -1)
    rgb += np.stack([0.0 * lit, 0.10 * lit, 0.16 * lit], -1) * (1 - nz)[..., None] * 0.9  # ice rim on the lit limb
    rgb += np.stack([0.02, 0.035, 0.07], -1) * (1 - lit)[..., None] * inside[..., None]  # cool earthshine tint
    edge = np.clip((1 - np.sqrt(r2)) * radius / 1.6, 0, 1)
    alpha = (edge * 255).astype(np.uint8)
    img = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    out = Image.fromarray(img, "RGB").convert("RGBA")
    out.putalpha(Image.fromarray(alpha))
    return out


def squircle_mask(size, inset, n=5.0):
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    half = size / 2 - inset
    u = np.abs((x - size / 2) / half)
    v = np.abs((y - size / 2) / half)
    d = (u ** n + v ** n) ** (1 / n)
    a = np.clip((1 - d) * half / 1.5, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8))


def background(size):
    y, x = np.mgrid[0:size, 0:size].astype(np.float32) / size
    d = np.hypot(x - 0.5, y - 0.42)
    base = np.stack([0.016 + 0.06 * np.exp(-d * 3.2), 0.024 + 0.085 * np.exp(-d * 3.0), 0.05 + 0.15 * np.exp(-d * 2.8)], -1)
    neb = noise(size, size, 160, 11) * noise(size, size, 60, 12)
    base += np.stack([0.0, 0.05, 0.08], -1) * neb[..., None] * np.exp(-np.hypot(x - 0.72, y - 0.25) * 3)[..., None]
    img = Image.fromarray(np.clip(base * 255, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d2 = ImageDraw.Draw(img)
    for _ in range(int(size * 0.18)):
        sx, sy = rng.random() * size, rng.random() * size
        b = rng.random() ** 3
        r = 0.6 + b * size / 900
        c = int(120 + 135 * b)
        d2.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(c, c, min(255, c + 20), int(90 + 165 * b)))
    return img


def ring_points(cx, cy, rx, ry, rot_deg, front, steps=900):
    rot = math.radians(rot_deg)
    pts = []
    rng_t = np.linspace(0, math.pi, steps) if front else np.linspace(math.pi, 2 * math.pi, steps)
    for t in rng_t:
        px, py = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + px * math.cos(rot) - py * math.sin(rot), cy + px * math.sin(rot) + py * math.cos(rot)))
    return pts


def rings_layer(size, front):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cx = cy = size / 2
    w = size * 0.016
    for rot in (-34, 34):
        pts = ring_points(cx, cy, size * 0.43, size * 0.095, rot, front)
        dg = ImageDraw.Draw(glow)
        dg.line(pts, fill=(143, 230, 255, 200 if front else 90), width=int(w * 3.2), joint="curve")
        dl = ImageDraw.Draw(layer)
        # Bright core that shades from white to ice along the ring.
        for i in range(len(pts) - 1):
            k = i / (len(pts) - 1)
            col = (int(255 - 112 * k), int(255 - 25 * k), 255, 255 if front else 120)
            dl.line([pts[i], pts[i + 1]], fill=col, width=int(w))
        hl = [p for j, p in enumerate(pts) if 0.18 < j / len(pts) < 0.42] if front else []
        if hl:
            dl.line(hl, fill=(255, 255, 255, 255), width=max(2, int(w * 0.35)))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.012))
    return Image.alpha_composite(glow, layer)


def render():
    os.makedirs(OUT, exist_ok=True)
    bg = background(S)
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse((S * 0.24, S * 0.24, S * 0.76, S * 0.76), fill=(143, 230, 255, 70))
    bg = Image.alpha_composite(bg, halo.filter(ImageFilter.GaussianBlur(S * 0.06)))
    bg = Image.alpha_composite(bg, rings_layer(S, front=False))
    moon_r = S * 0.245
    moon = moon_layer(int(moon_r * 2 + 8), moon_r, phase_e=math.radians(58))
    bg.alpha_composite(moon, (int(S / 2 - moon.width / 2), int(S / 2 - moon.height / 2)))
    bg = Image.alpha_composite(bg, rings_layer(S, front=True))

    # Glass rim: a thin highlight along the badge edge, brighter at the top.
    rim = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    outer = squircle_mask(S, S * 0.02)
    inner = squircle_mask(S, S * 0.02 + 5)
    edge = np.asarray(outer, np.float32) - np.asarray(inner, np.float32)
    yy = np.linspace(1.0, 0.25, S)[:, None]
    rim_a = np.clip(edge * yy * 0.9, 0, 255).astype(np.uint8)
    rim.putalpha(Image.fromarray(rim_a))
    rim_rgb = Image.new("RGBA", (S, S), (200, 240, 255, 0))
    rim_rgb.putalpha(Image.fromarray(rim_a))
    bg = Image.alpha_composite(bg, rim_rgb)

    mask = squircle_mask(S, S * 0.02)
    badge = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    badge.paste(bg, (0, 0), mask)
    badge.save(os.path.join(OUT, "xluna-badge-2048.png"))
    for s in (1024, 512, 192, 180, 32):
        badge.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, f"xluna-badge-{s}.png"))
    badge.resize((256, 256), Image.LANCZOS).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (256, 256)])
    print("badge written")


if __name__ == "__main__":
    render()
