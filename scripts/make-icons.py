#!/usr/bin/env python3
"""Regenere les icones de branding/mimir a partir des PNG de branding/source.

Les PNG (mimir-mark*.png) viennent de scripts/prepare-logo.py (logo d'origine).

Chaque PNG deja present dans branding/mimir garde sa taille : le logo est rendu
au centre, le reste est transparent. Les fichiers dont le nom
contient "rivate" ou "pbmode" prennent la variante violette (navigation privee).
Les .ico sont reconstruits en multi-tailles.

Dependances : python3-pil.
Usage : scripts/make-icons.py [dossier branding/mimir]
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "branding" / "source"
DEST = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "branding" / "mimir"
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]
# Fichiers a ne pas toucher (fonds d'installeur, pas des logos).
SKIP = {"background.png"}


def render(src: Path, size: int) -> Image.Image:
    return Image.open(src).convert("RGBA").resize((size, size), Image.LANCZOS)


def is_private(path: Path) -> bool:
    name = path.name.lower()
    return "rivate" in name or "pbmode" in name


def logo_for(path: Path) -> Path:
    return SRC / ("mimir-mark-private.png" if is_private(path) else "mimir-mark.png")


def make_png(path: Path) -> None:
    with Image.open(path) as old:
        w, h = old.size
    side = min(w, h)  # la marge est deja dans le PNG source
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    logo = render(logo_for(path), side)
    canvas.paste(logo, ((w - side) // 2, (h - side) // 2), logo)
    canvas.save(path)


def make_ico(path: Path) -> None:
    big = render(logo_for(path), 256)
    big.save(path, format="ICO", sizes=[(s, s) for s in ICO_SIZES])


def make_svg(path: Path) -> None:
    """SVG qui embarque le PNG (en attendant une version vectorielle du logo)."""
    buf = io.BytesIO()
    render(logo_for(path), 512).save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode("ascii")
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="512" height="512" viewBox="0 0 512 512">'
        f'<image width="512" height="512" xlink:href="data:image/png;base64,{data}"/></svg>\n',
        encoding="utf-8",
    )


def main() -> None:
    for p in sorted(DEST.rglob("*")):
        if p.name in SKIP or "stubinstaller" in p.parts:
            continue
        if p.suffix == ".png":
            make_png(p)
        elif p.suffix == ".ico":
            make_ico(p)
        elif p.name == "about-logo.svg":
            make_svg(p)
        else:
            continue
        print("OK", p.relative_to(DEST))


if __name__ == "__main__":
    main()
