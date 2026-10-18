#!/usr/bin/env python3
"""Remplace les illustrations de la mascotte Firefox (renard) par la marque Mimir.

Ecrit dans overlay/ des fichiers du meme nom que ceux de Firefox ; apply-patches.sh les copie par-dessus.
Les illustrations decoratives (queue du renard) deviennent transparentes.
Depend de branding/source/mimir-mark.png (voir prepare-logo.py). Usage : python3 scripts/make-mascot-replacements.py
"""
import base64
import io
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
OVERLAY = REPO / "overlay"
MARK = Image.open(REPO / "branding/source/mimir-mark.png").convert("RGBA")

# Illustrations qui montrent la mascotte : remplacees par la marque.
MASCOT = """
browser/components/aboutwelcome/assets/br-amo-fox-paint.svg
browser/components/aboutwelcome/assets/br-fxa-fox-mirror.svg
browser/components/aboutwelcome/assets/br-gratitude-fox-rock.svg
browser/components/aboutwelcome/assets/br-import-fox-house.svg
browser/components/aboutwelcome/assets/br-set-default-fox-heart.svg
browser/components/aboutwelcome/assets/fox-doodle-backup-restore.svg
browser/components/aboutwelcome/assets/fox-doodle-backup.svg
browser/components/aboutwelcome/assets/fox-doodle-waving-static.png
browser/components/aboutwelcome/assets/mr-kit-smart-window.svg
browser/components/aiwindow/ui/assets/kit.svg
browser/components/asrouter/content/assets/fox-with-box-on-cloud.svg
browser/components/asrouter/content/assets/fox-with-checkmark.svg
browser/components/asrouter/content/assets/fox-with-devices.svg
browser/components/asrouter/content/assets/fox-with-locked-box.svg
browser/components/asrouter/content/assets/fox-with-mobile.svg
browser/components/asrouter/content/assets/fox-with-profiles.svg
browser/components/asrouter/content/assets/smiling-fox-icon.svg
browser/components/controlcenter/content/assets/fox-concern.svg
browser/extensions/newtab/data/content/assets/kit-in-circle.svg
browser/extensions/newtab/data/content/assets/kit.png
browser/extensions/newtab/data/content/assets/puzzle-fox.svg
browser/themes/shared/fxa/avatar-fox-circle.svg
browser/themes/shared/fxa/avatar-fox.svg
browser/themes/shared/preferences/fox-ai.svg
browser/themes/shared/sidebar/foxy.svg
browser/themes/shared/sidebar/firefox.svg
devtools/client/themes/images/fox-smiling.svg
toolkit/components/satchel/megalist/content/icons/cpm-fox-illustration.svg
toolkit/themes/shared/illustrations/kit-concerned.svg
toolkit/themes/shared/illustrations/kit-happy.svg
toolkit/themes/shared/illustrations/kit-in-circle.svg
""".split()

# Decor sans la mascotte : rien a afficher.
DECOR = """
browser/components/aboutwelcome/assets/fox-doodle-tail.png
browser/themes/shared/privatebrowsing/fox-tail.svg
""".split()


def png_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


MARK_192 = MARK.resize((192, 192 * MARK.height // MARK.width), Image.LANCZOS)
MARK_B64 = base64.b64encode(png_bytes(MARK_192)).decode()
SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{MARK_192.width}" height="{MARK_192.height}" viewBox="0 0 {MARK_192.width} {MARK_192.height}">'
    f'<image width="{MARK_192.width}" height="{MARK_192.height}" xlink:href="data:image/png;base64,{MARK_B64}"/>'
    "</svg>\n"
)
SVG_EMPTY = '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 1 1"></svg>\n'
PNG_MARK = png_bytes(MARK.resize((256, 256 * MARK.height // MARK.width), Image.LANCZOS))
PNG_EMPTY = png_bytes(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))


def write(rel, svg, png):
    dest = OVERLAY / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if rel.endswith(".svg"):
        dest.write_text(svg, encoding="utf-8", newline="\n")
    else:
        dest.write_bytes(png)


for rel in MASCOT:
    write(rel, SVG, PNG_MARK)
for rel in DECOR:
    write(rel, SVG_EMPTY, PNG_EMPTY)
print(len(MASCOT) + len(DECOR), "illustrations ecrites dans", OVERLAY)
