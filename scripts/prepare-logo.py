#!/usr/bin/env python3
"""Extrait le « M » du logo d'origine (JPG, fond bleu nuit) en PNG transparent.

Entree  : branding/source/logo-original.jpg
Sortie  : branding/source/mimir-mark.png          (carre 1024, fond transparent)
          branding/source/mimir-mark-private.png  (meme forme, teinte violette)

Le fond est estime sur le pourtour de la zone recadree, puis retire par un alpha
progressif (distance a la couleur de fond) ; la couleur des bords est « de-melangee »
pour ne pas garder de halo sombre.

Dependances : python3-pil, python3-numpy.
"""
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path(__file__).resolve().parent.parent / "branding" / "source"
# Zone du « M » dans l'image d'origine (x0, y0, x1, y1), texte « MIMIR » exclu.
MARK_BOX = (480, 150, 900, 430)
ALPHA_LO, ALPHA_HI = 14.0, 70.0  # distance au fond : en dessous transparent, au dessus opaque
OUT = 1024
MARGIN = 0.06
PRIVATE_HUE_SHIFT = 36  # en 0..255 (~ +50 degres : bleu -> violet)


def extract() -> Image.Image:
    im = Image.open(SRC / "logo-original.jpg").convert("RGB").crop(MARK_BOX)
    px = np.asarray(im).astype(np.float64)
    border = np.concatenate([px[0], px[-1], px[:, 0], px[:, -1]])
    bg = np.median(border, axis=0)

    dist = np.sqrt(((px - bg) ** 2).sum(axis=2))
    alpha = np.clip((dist - ALPHA_LO) / (ALPHA_HI - ALPHA_LO), 0.0, 1.0)
    a = alpha[..., None]
    color = np.where(a > 0.02, (px - bg * (1 - a)) / np.maximum(a, 0.02), 0.0)
    color = np.clip(color, 0, 255)

    rgba = np.dstack([color, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def square(mark: Image.Image) -> Image.Image:
    box = mark.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    mark = mark.crop(box)
    w, h = mark.size
    inner = round(OUT * (1 - 2 * MARGIN))
    scale = inner / max(w, h)
    mark = mark.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (OUT, OUT), (0, 0, 0, 0))
    canvas.paste(mark, ((OUT - mark.width) // 2, (OUT - mark.height) // 2), mark)
    return canvas


def purple(mark: Image.Image) -> Image.Image:
    r, g, b, a = mark.split()
    h, s, v = Image.merge("RGB", (r, g, b)).convert("HSV").split()
    h = h.point(lambda x: (x + PRIVATE_HUE_SHIFT) % 256)
    rgb = Image.merge("HSV", (h, s, v)).convert("RGB")
    return Image.merge("RGBA", (*rgb.split(), a))


def main() -> None:
    mark = square(extract())
    mark.save(SRC / "mimir-mark.png")
    purple(mark).save(SRC / "mimir-mark-private.png")
    print("OK", SRC / "mimir-mark.png", SRC / "mimir-mark-private.png")


if __name__ == "__main__":
    main()
