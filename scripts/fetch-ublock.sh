#!/bin/bash
# Telecharge uBlock Origin (xpi signe par Mozilla, publie par son auteur) et verifie son empreinte.
# Version et SHA-256 sont figes ici : pour mettre a jour, changer les deux lignes ci-dessous
# apres avoir verifie la release sur https://github.com/gorhill/uBlock/releases
# Usage : scripts/fetch-ublock.sh   -> affiche le chemin du xpi
set -euo pipefail
VERSION="1.75.0"
SHA256="5b74415860456370644bd80f16125e865b0e6c356bb5dfcfb84069967eaa5287"
CACHE="$HOME/ff/cache"
XPI="$CACHE/uBlock0_${VERSION}.firefox.signed.xpi"

mkdir -p "$CACHE"
if [ ! -f "$XPI" ]; then
    curl -fsSL -o "$XPI.part" \
        "https://github.com/gorhill/uBlock/releases/download/${VERSION}/uBlock0_${VERSION}.firefox.signed.xpi"
    mv "$XPI.part" "$XPI"
fi
echo "$SHA256  $XPI" | sha256sum -c - >&2
echo "$XPI"
