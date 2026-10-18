#!/bin/bash
# Applique overlay/ (fichiers nouveaux) et patches/*.patch (fichiers Firefox modifies)
# sur la source Firefox. Idempotent : un patch deja applique est ignore.
# Usage : scripts/apply-patches.sh [dossier source Firefox, defaut ~/ff/esr153]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${1:-$HOME/ff/esr153}"

if [ -d "$REPO/overlay" ]; then
    cp -r "$REPO/overlay/." "$SRC/"
    echo "overlay copie dans $SRC"
fi

cd "$SRC"
for p in "$REPO"/patches/*.patch; do
    [ -e "$p" ] || continue
    # Le sens inverse d'abord : pour une simple insertion, le test direct reussit
    # meme si le patch est deja la (le contexte n'a pas change) et l'empilerait.
    if git apply --check -R "$p" 2>/dev/null; then
        echo "patch deja applique : $(basename "$p")"
    elif git apply --check "$p" 2>/dev/null; then
        git apply "$p"
        echo "patch applique : $(basename "$p")"
    else
        echo "ERREUR : $(basename "$p") ne s'applique pas" >&2
        exit 1
    fi
done
