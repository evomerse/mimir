#!/bin/bash
# Prepare le pack de langue francais : telecharge le xpi officiel de Mozilla (empreinte verifiee),
# remplace le nom de marque « Firefox » par « Mimir », retire la signature devenue invalide.
# Mimir etant base sur l'ESR, la signature des modules n'est pas exigee (toolkit/moz.configure).
# Usage : scripts/fetch-langpack.sh   -> affiche le chemin du xpi pret a l'emploi
set -euo pipefail
VERSION="153.5.0esr"
SHA256="313212b41d507c8dcfa57e2674c3d54c12dca63fe200605e66b209e50a05df69"
CACHE="$HOME/ff/cache"
ORIGINAL="$CACHE/langpack-fr-$VERSION.xpi"
READY="$CACHE/langpack-fr@firefox.mozilla.org.xpi"

mkdir -p "$CACHE"
if [ ! -f "$ORIGINAL" ]; then
    curl -fsSL -o "$ORIGINAL.part" \
        "https://archive.mozilla.org/pub/firefox/releases/$VERSION/win64/xpi/fr.xpi"
    mv "$ORIGINAL.part" "$ORIGINAL"
fi
echo "$SHA256  $ORIGINAL" | sha256sum -c - >&2

python3 - "$ORIGINAL" "$READY" <<'PY'
import re, sys, zipfile

src, dst = sys.argv[1:3]

BRAND_FTL = """\
-brand-shorter-name = Mimir
-brand-short-name = Mimir
-brand-shortcut-name = Mimir
-brand-full-name = Mimir
-brand-product-name = Mimir
-vendor-short-name = Mimir
trademarkInfo = { " " }
"""
BRAND_PROPERTIES = "brandShorterName=Mimir\nbrandShortName=Mimir\nbrandFullName=Mimir\n"
# Marques de fonctionnalites Mozilla : on ne garde le nom Firefox nulle part a l'ecran.
BRANDINGS = {
    "-firefox-suggest-brand-name": "Suggestions Mimir",
    "-firefox-home-brand-name": "Page d’accueil de Mimir",
    "-firefoxview-brand-name": "Mimir View",
    "-firefoxlabs-brand-name": "Mimir Labs",
}

def rebrand_brandings(text):
    for key, value in BRANDINGS.items():
        text = re.sub(rf"^{re.escape(key)} = .*$", f"{key} = {value}", text, flags=re.M)
    return text

with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        name = info.filename
        if name.startswith("META-INF/"):
            continue
        data = zin.read(name)
        if name == "browser/localization/fr/branding/brand.ftl":
            data = BRAND_FTL.encode()
        elif name == "browser/chrome/fr/locale/branding/brand.properties":
            data = BRAND_PROPERTIES.encode()
        elif name == "localization/fr/toolkit/branding/brandings.ftl":
            data = rebrand_brandings(data.decode()).encode()
        zout.writestr(name, data)
PY
echo "$READY"
