#!/bin/bash
# Fabrique l'archive Linux de Mimir a partir du build courant (voir scripts/build-wsl.sh) :
#   wsl -d Ubuntu-24.04 -- bash /mnt/d/Projets/mimir/scripts/package-linux.sh
# Resultat : ~/ff/dist/mimir-<VERSION>-linux-x86_64.tar.xz (VERSION = fichier VERSION du depot).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$HOME/ff/esr153"
OBJ="$SRC/obj-validate"
VERSION="$(tr -d '[:space:]' < "$REPO/VERSION")"
OUT="$HOME/ff/dist"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

source "$HOME/.cargo/env" 2>/dev/null || true
cd "$SRC"
export MOZCONFIG="$HOME/ff/mozconfig.mimir"
./mach -l "$HOME/ff/package-mimir.log" package

TAR="$(ls -t "$OBJ"/dist/mimir-*.tar.* | head -1)"
echo "archive Mozilla : $TAR"
tar -C "$STAGE" -xf "$TAR"
[ -d "$STAGE/mimir" ] || { echo "dossier mimir/ absent de l'archive" >&2; exit 1; }

# Configuration de distribution (politiques + autoconfig), comme dans dist/bin.
MIMIR_BIN="$STAGE/mimir" "$REPO/scripts/post-build.sh" "$OBJ"

mkdir -p "$OUT"
FINAL="$OUT/mimir-$VERSION-linux-x86_64.tar.xz"
tar -C "$STAGE" -cJf "$FINAL" mimir
( cd "$OUT" && sha256sum "$(basename "$FINAL")" > "$(basename "$FINAL").sha256" )
ls -lh "$FINAL"
cat "$FINAL.sha256"
