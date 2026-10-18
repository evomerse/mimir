#!/bin/bash
# Decompresse uBlock Origin (xpi verifie par fetch-ublock.sh) dans la source Firefox,
# dans browser/extensions/ublock-origin/xpi/, pour qu'il soit integre au build.
# Usage : scripts/prepare-ublock.sh [dossier source Firefox, defaut ~/ff/esr153]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${1:-$HOME/ff/esr153}"
DEST="$SRC/browser/extensions/ublock-origin/xpi"

XPI="$("$REPO/scripts/fetch-ublock.sh")"
rm -rf "$DEST"
mkdir -p "$DEST"
unzip -q "$XPI" -x 'META-INF/*' -d "$DEST"
echo "uBlock Origin integre : $(python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); print(m["version"], m["browser_specific_settings"]["gecko"]["id"])' "$DEST/manifest.json")"
