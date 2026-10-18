#!/bin/bash
# Copie branding/mimir du depot vers la source Firefox (cote WSL).
# Usage : scripts/sync-branding.sh [dossier source Firefox, defaut ~/ff/esr153]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${1:-$HOME/ff/esr153}"
DEST="$SRC/browser/branding/mimir"

rm -rf "$DEST"
cp -r "$REPO/branding/mimir" "$DEST"
echo "branding synchronise : $DEST"
