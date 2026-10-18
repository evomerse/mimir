#!/bin/bash
# Installe les outils de compilation de Firefox (Clang, Rust, ...) via mach bootstrap.
# A lancer dans MozillaBuild (voir scripts/run-in-mozillabuild.cmd).
# Usage : scripts/bootstrap-windows.sh [dossier source, defaut /c/ff/esr153]
set -euo pipefail
SRC="${1:-/c/ff/esr153}"
cd "$SRC"
./mach --no-interactive bootstrap --application-choice browser
