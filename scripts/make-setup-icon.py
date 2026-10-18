#!/usr/bin/env python3
"""Genere l'icone de l'installeur Windows a partir du logo Mimir.

Ecrit overlay/toolkit/mozapps/installer/windows/nsis/setup.ico (icone de setup.exe, NSIS)
et branding/source/setup.ico (copie de travail pour le module SFX, voir scripts/patch-sfx-icon.ps1).
Depend de branding/source/mimir-mark.png. Usage : python3 scripts/make-setup-icon.py
"""
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
mark = Image.open(REPO / "branding/source/mimir-mark.png").convert("RGBA")
side = max(mark.size)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2), mark)
canvas = canvas.resize((256, 256), Image.LANCZOS)

# Images BMP (pas PNG) : NSIS et les modules SFX attendent le format ICO classique.
SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)]
for dest in (
    REPO / "overlay/toolkit/mozapps/installer/windows/nsis/setup.ico",
    REPO / "branding/source/setup.ico",
):
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, format="ICO", sizes=SIZES, bitmap_format="bmp")
    print("ecrit", dest, dest.stat().st_size, "octets")
