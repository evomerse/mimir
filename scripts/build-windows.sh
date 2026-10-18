#!/bin/bash
# Build Mimir pour Windows : prepare la source, compile, installe la configuration de
# distribution, signe (si un certificat est fourni) et fabrique l'installeur.
# A lancer dans un shell MozillaBuild (C:\mozilla-build\start-shell.bat) :
#   scripts/build-windows.sh [dossier source Firefox, defaut ~/ff/esr153]
#
# Signature (optionnelle) : MIMIR_SIGN_PFX=<fichier .pfx> et MIMIR_SIGN_PASSWORD=<mot de passe>.
# Sans certificat, l'installeur est produit mais non signe : Smart App Control le bloquera.
#
# Valide dans une VM Windows 11 sans Smart App Control (compilation complete 2 h 20 sur 8 coeurs).
# Voir docs/BUILD.md.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${1:-$HOME/ff/esr153}"
OBJ="$SRC/obj-mimir"

"$REPO/scripts/sync-branding.sh" "$SRC"
"$REPO/scripts/apply-patches.sh" "$SRC"
"$REPO/scripts/prepare-ublock.sh" "$SRC"
cp "$REPO/build/mozconfig.mimir-windows" "$SRC/mozconfig.mimir-windows"

cd "$SRC"
export MOZCONFIG="$SRC/mozconfig.mimir-windows"
./mach -l "$SRC/build-mimir.log" build
MIMIR_BIN="$OBJ/dist/bin" "$REPO/scripts/post-build.sh" "$OBJ"

# Signer avant d'empaqueter : l'installeur embarque les binaires tels qu'ils sont dans dist/bin.
SIGN=0
if [ -n "${MIMIR_SIGN_PFX:-}" ]; then
    SIGN=1
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "$REPO/scripts/sign-windows.ps1")" \
        -Path "$(cygpath -w "$OBJ/dist/bin")"
fi

# `mach package` produit l'archive puis l'installeur NSIS (dist/install/sea).
./mach -l "$SRC/package-mimir.log" package

INSTALLER="$(ls -t "$OBJ"/dist/*.installer.exe | head -1)"
if [ "$SIGN" = 1 ]; then
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "$REPO/scripts/sign-windows.ps1")" \
        -Path "$(cygpath -w "$INSTALLER")"
fi
echo "installeur : $INSTALLER"
sha256sum "$INSTALLER"
