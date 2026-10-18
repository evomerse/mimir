#!/usr/bin/env python3
"""Genere les images de l'installeur Windows (NSIS) a partir du logo Mimir.

Sortie : branding/mimir/wizHeader.bmp, wizHeaderRTL.bmp (150x57), wizWatermark.bmp (164x314), 24 bits.
Depend de branding/source/mimir-mark.png (voir prepare-logo.py). Usage : python3 scripts/make-installer-art.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
MARK = Image.open(REPO / "branding/source/mimir-mark.png").convert("RGBA")
OUT = REPO / "branding/mimir"

NIGHT_TOP = (26, 34, 80)
NIGHT_BOTTOM = (13, 18, 32)


def fit(img, box):
    ratio = min(box[0] / img.width, box[1] / img.height)
    return img.resize((round(img.width * ratio), round(img.height * ratio)), Image.LANCZOS)


def header(rtl):
    # Bandeau blanc du haut des pages de l'assistant : logo du cote du texte inverse.
    img = Image.new("RGB", (150, 57), "white")
    mark = fit(MARK, (46, 46))
    x = 8 if rtl else 150 - mark.width - 8
    img.paste(mark, (x, (57 - mark.height) // 2), mark)
    return img


def watermark():
    # Panneau gauche des pages d'accueil et de fin : degrade nuit, logo en haut.
    img = Image.new("RGB", (164, 314))
    draw = ImageDraw.Draw(img)
    for y in range(314):
        t = y / 313
        draw.line(
            [(0, y), (164, y)],
            fill=tuple(round(a + (b - a) * t) for a, b in zip(NIGHT_TOP, NIGHT_BOTTOM)),
        )
    mark = fit(MARK, (96, 96))
    img.paste(mark, ((164 - mark.width) // 2, 56), mark)
    return img


def stub_background():
    # Fond de l'installeur web (stubinstaller) : degrade nuit, logo au centre-haut.
    # Le build l'exige meme si Mimir ne distribue que l'installeur complet.
    w, h = 1344, 822
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        draw.line(
            [(0, y), (w, y)],
            fill=tuple(round(a + (b - a) * t) for a, b in zip(NIGHT_TOP, NIGHT_BOTTOM)),
        )
    mark = fit(MARK, (160, 160))
    img.paste(mark, ((w - mark.width) // 2, 150), mark)
    return img


(OUT / "stubinstaller").mkdir(exist_ok=True)
stub_background().save(OUT / "stubinstaller/bgstub.jpg", quality=90)
print("ecrit", OUT / "stubinstaller/bgstub.jpg")

for name, img in (
    ("wizHeader.bmp", header(False)),
    ("wizHeaderRTL.bmp", header(True)),
    ("wizWatermark.bmp", watermark()),
):
    img.save(OUT / name, format="BMP")
    print("ecrit", OUT / name, img.size)
