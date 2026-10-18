#!/bin/bash
# Etape apres compilation : installe dans le build (dist/bin) la configuration de distribution.
#  - distribution/policies.json (sans le force-install uBO du prototype : uBO est integre au build)
#  - autoconfig (mimir.cfg) pour les prefs que les politiques ne couvrent pas
# A relancer apres chaque `mach build`. Usage : scripts/post-build.sh [objdir]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OBJ="${1:-$HOME/ff/esr153/obj-validate}"
BIN="$OBJ/dist/bin"
[ -d "$BIN" ] || { echo "dist/bin introuvable : $BIN" >&2; exit 1; }

mkdir -p "$BIN/distribution" "$BIN/defaults/pref"
python3 - "$REPO/distribution/policies.json" "$BIN/distribution/policies.json" <<'PY'
import json, sys
src, dst = sys.argv[1:3]
d = json.load(open(src, encoding="utf-8"))
d["policies"].get("ExtensionSettings", {}).pop("uBlock0@raymondhill.net", None)
if not d["policies"].get("ExtensionSettings"):
    d["policies"].pop("ExtensionSettings", None)
json.dump(d, open(dst, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
PY
cp "$REPO/distribution/mimir.cfg" "$BIN/mimir.cfg"
cp "$REPO/distribution/defaults/pref/autoconfig.js" "$BIN/defaults/pref/autoconfig.js"
rm -rf "$BIN/browser/features"
echo "policies + autoconfig installes dans $BIN"
