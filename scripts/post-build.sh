#!/bin/bash
# Etape apres compilation : installe dans le build (dist/bin) la configuration de distribution.
#  - distribution/policies.json (sans le force-install uBO du prototype : uBO est integre au build)
#  - autoconfig (mimir.cfg) pour les prefs que les politiques ne couvrent pas
# A relancer apres chaque `mach build`. Usage : scripts/post-build.sh [objdir]
# MIMIR_BIN=<dossier> vise un autre dossier que <objdir>/dist/bin (archive en preparation).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OBJ="${1:-$HOME/ff/esr153/obj-validate}"
BIN="${MIMIR_BIN:-$OBJ/dist/bin}"
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
# Pack de langue francais : Firefox l'installe au demarrage si la langue demandee est le francais.
LANGPACK="$("$REPO/scripts/fetch-langpack.sh")"
mkdir -p "$BIN/distribution/extensions/locale-fr"
cp "$LANGPACK" "$BIN/distribution/extensions/locale-fr/langpack-fr@firefox.mozilla.org.xpi"
rm -rf "$BIN/browser/features"
echo "policies + autoconfig + langue francaise installes dans $BIN"
