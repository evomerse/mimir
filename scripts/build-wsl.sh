#!/bin/bash
# Build Mimir sous WSL2. A lancer depuis Windows :
#   wsl -d Ubuntu-24.04 -- bash /mnt/d/Projets/mimir/scripts/build-wsl.sh
# 12 jobs : 16 faisaient geler la VM (voir docs/ROADMAP.md).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$HOME/ff/esr153"

# shellcheck disable=SC1090
source "$HOME/.cargo/env" 2>/dev/null || true
"$REPO/scripts/sync-branding.sh" "$SRC"
"$REPO/scripts/apply-patches.sh" "$SRC"
"$REPO/scripts/prepare-ublock.sh" "$SRC"
cp "$REPO/build/mozconfig.mimir" "$HOME/ff/mozconfig.mimir"

cd "$SRC"
export MOZCONFIG="$HOME/ff/mozconfig.mimir"
./mach -l "$HOME/ff/build-mimir.log" build -j12
"$REPO/scripts/post-build.sh" "$SRC/obj-validate"
