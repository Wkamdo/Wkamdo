#!/usr/bin/env python3
"""Membuat banner animasi (GIF) + versi statis (PNG) untuk profil GitHub.

Jalankan:  python3 tools/generate_banner.py
Keluaran:  assets/banner.gif, assets/banner.png

Semua digambar dengan PIL (tanpa layanan pihak ketiga), jadi tidak ada
gambar hotlink yang bisa mati. Palet dibuat 64 warna agar berkas kecil.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 336
FRAMES = 24
BG = (13, 17, 23)          # GitHub dark
FG = (230, 237, 243)
DIM = (110, 118, 129)
ACCENT = (255, 176, 59)     # amber
ACCENT2 = (88, 166, 255)    # biru
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(AKAR, "assets")

NAMA = "WKAMDO"
TAGLINE = "Information Systems student  ·  Linux & WSL2  ·  Docker  ·  Python"
BARIS = [
    "currently: thesis, work in progress",
    "usually found in: terminal, docker-compose, and error logs",
]


def font(path, size):
    return ImageFont.truetype(path, size)


def gambar_frame(t, alpha_hint=False):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im, "RGBA")

    # --- latar: kisi titik yang bergeser pelan ---
    pergeseran = (t / FRAMES) * 24
    for x in range(-24, W + 24, 24):
        for y in range(0, H, 24):
            px = x + pergeseran
            jarak = math.hypot(px - W / 2, y - H / 2) / (W / 2)
            a = max(0, int(26 - jarak * 22))
            if a:
                d.ellipse([px, y, px + 1.6, y + 1.6], fill=(88, 166, 255, a))

    # --- sapuan cahaya diagonal ---
    sapu = (t / FRAMES) * (W + 400) - 200
    for i in range(-160, 160, 2):
        x = sapu + i
        kekuatan = max(0, 1 - abs(i) / 160)
        d.line([(x, 0), (x - 160, H)], fill=(255, 176, 59, int(26 * kekuatan)), width=2)

    # --- bingkai panel ---
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=18, outline=(48, 54, 61), width=2)  # panel
    d.rounded_rectangle([40, 40, W - 40, 92], radius=18, fill=(22, 27, 34))
    d.rectangle([40, 74, W - 40, 92], fill=(22, 27, 34))
    for i, w in enumerate((60, 60, 60)):
        warna = [(255, 95, 86), (255, 189, 46), (39, 201, 63)][i]
        d.ellipse([64 + i * 22, 60, 76 + i * 22, 72], fill=warna)
    d.text((140, 58), "~/wkamdo — zsh", font=font(FONT_R, 17), fill=DIM)

    # --- baris perintah + nama ---
    kurung = ">" if (t // 7) % 2 == 0 else " "
    d.text((80, 112), "wkamdo@github:~$", font=font(FONT_R, 20), fill=(126, 231, 135))
    d.text((294, 110), "whoami" + kurung, font=font(FONT_R, 20), fill=DIM)

    f_nama = font(FONT_B, 56)
    x_nama, y_nama = 80, 146
    # bayangan berdenyut
    denyut = 6 + int(4 * math.sin(t / FRAMES * 2 * math.pi))
    d.text((x_nama + 3, y_nama + 3), NAMA, font=f_nama, fill=(0, 0, 0))
    d.text((x_nama, y_nama), NAMA, font=f_nama, fill=FG)
    lebar = d.textlength(NAMA, font=f_nama)
    d.rectangle([x_nama, y_nama + 68, x_nama + lebar + denyut, y_nama + 72], fill=ACCENT)

    # --- tagline ---
    d.text((80, 236), TAGLINE, font=font(FONT_R, 19), fill=ACCENT2)

    # --- dua baris status, bergantian muncul ---
    aktif = (t // (FRAMES // 2)) % len(BARIS)
    d.text((80, 264), "// " + BARIS[aktif], font=font(FONT_R, 18), fill=DIM)

    return im


def main():
    os.makedirs(ASSETS, exist_ok=True)
    frames = [gambar_frame(t) for t in range(FRAMES)]

    gif = os.path.join(ASSETS, "banner.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=120,
                   loop=0, optimize=True, colors=48)

    png = os.path.join(ASSETS, "banner.png")
    gambar_frame(0).save(png, optimize=True)

    for p in (gif, png):
        print(f"{os.path.relpath(p, AKAR)}  {os.path.getsize(p)/1024:.0f} KB")
    print(f"gif: {len(frames)} frame, {W}x{H}")


if __name__ == "__main__":
    main()
