# Construire Mimir

Mimir = source de Firefox ESR (hors du dépôt) + `overlay/` (fichiers nouveaux) + `patches/` (modifications) + `branding/` + `distribution/`. Le dépôt ne contient jamais la source de Firefox.

La version de Mimir est dans le fichier `VERSION` ; la base est Firefox ESR 153.5.0 (tag `FIREFOX_153_5_0esr_BUILD1` de `github.com/mozilla-firefox/firefox`).

## Linux (testé, y compris sous WSL2)

C'est le chemin utilisé au quotidien. Sous Windows, passer par WSL2 (Ubuntu 24.04) : le build Windows natif est bloqué sur la machine de développement par Smart App Control.

1. Cloner la source dans le système de fichiers Linux (pas sous `/mnt/d`) : `git clone --depth 1 --branch FIREFOX_153_5_0esr_BUILD1 https://github.com/mozilla-firefox/firefox.git ~/ff/esr153`, puis `./mach bootstrap`.
2. Sous WSL2, `~/.wslconfig` doit donner assez de mémoire : 24 Go de RAM et 16 Go de swap, sinon la VM gèle (voir ROADMAP).
3. Compiler : `wsl -d Ubuntu-24.04 -- bash /mnt/d/Projets/mimir/scripts/build-wsl.sh`
   - synchronise le branding, applique `overlay/` et `patches/` (idempotent), intègre uBlock Origin, lance `mach build -j12`, installe la configuration de distribution dans `dist/bin`.
   - Premier build à partir de zéro : plus d'une heure (non chronométré). Rebuild après un changement de defines (réactivation ou retrait d'une fonction) : ~27 min mesurées. Après un changement de JS/CSS ou de fichiers `moz.build` : moins de 10 min.
4. Lancer : `build/lancer-wsl.cmd` (la fenêtre doit rester ouverte, sinon WSL tue le navigateur).
5. Archive distribuable : `wsl -d Ubuntu-24.04 -- bash /mnt/d/Projets/mimir/scripts/package-linux.sh` produit `~/ff/dist/mimir-<VERSION>-linux-x86_64.tar.xz` et son `.sha256` (~5 à 10 min).

### Tests

À lancer dans WSL avec le venv Marionette (`~/ff/venv`) :

| Script | Vérifie |
|--------|---------|
| `scripts/test-adblock.py` | uBlock Origin actif, pubs et traqueurs bloqués, site témoin chargé |
| `scripts/test-privacy.py` | constantes de compilation, préférences, moteur par défaut, hôtes contactés au repos |
| `scripts/test-start-page.py [dossier]` | page de démarrage : musique, raccourcis, compteur, persistance, ouverture d'un lien, captures |

## Windows

Validé le 2026-10-18 dans une VM VirtualBox Windows 11 (8 cœurs, 16 Go de RAM, Smart App Control désactivé). Compilation complète : 2 h 20 ; reconstruction après un changement de patch ou de branding : 10 à 30 min.

Pourquoi une VM : Smart App Control bloque les outils non signés de Mozilla (`llvm-lib.exe`, WinError 4551), et le désactiver est quasi irréversible. Dans une VM jetable, on le désactive sans conséquence.

1. Préparer la machine (administrateur, 30 à 60 min) : `scripts/setup-windows-vm.ps1` installe Git, Visual Studio 2022 Build Tools (C++, SDK Windows 11, ATL), MozillaBuild et clone la source de Firefox ESR 153.5.0 dans `C:\ff\esr153`.
2. Une fois : `scripts/run-in-mozillabuild.cmd /c/mimir/scripts/bootstrap-windows.sh` (`mach bootstrap` : Clang, Rust, etc.).
3. Compiler : `scripts/run-in-mozillabuild.cmd /c/mimir/scripts/build-windows.sh /c/ff/esr153` (dépôt copié dans `C:\mimir`). Le script applique branding, overlay et patchs, prépare uBlock Origin, compile, installe la configuration de distribution, signe si `MIMIR_SIGN_PFX` est défini, puis `mach package`.
4. Résultat : `C:\ff\esr153\obj-mimir\dist\mimir-<version>.en-US.win64.installer.exe` (installeur) et `.zip` (archive).

Pièges rencontrés :

- **Mémoire** : avec 16 Go, `rustc` s'arrête (« out of memory ») sur `gkrust` à cause du LTO et des infos de débogage ; `build/mozconfig.mimir-windows` fixe `RUSTFLAGS="-C debuginfo=0"`.
- **Branding** : l'installeur web exige `branding/mimir/stubinstaller/` (image de fond et deux feuilles de style).
- **Empaquetage** : la commande est `mach package` (pas `mach build installer`). Sans le patch 0010, `distribution/` n'est pas empaqueté (condition `BUILT_BY_MOZILLA`) : l'installeur partait avec Google comme moteur par défaut.
- **Icône de l'installeur** : l'icône Firefox est une ressource du module SFX précompilé ; `scripts/patch-sfx-icon.ps1` (rcedit) la remplace, le résultat est dans `overlay/other-licenses/7zstub/`. L'Explorateur garde l'ancienne icône en cache (`ie4uinit.exe -show`).
- **Git** : `core.autocrlf=false` sur la machine de build (les patchs sont en fins de ligne LF).

Sans certificat, l'installeur n'est pas signé : Smart App Control le bloquera sur une machine où il est actif. L'installeur et l'archive Windows n'ont été lancés que dans la VM.

`.github/workflows/build-windows.yml` (lancement manuel, confirmation « OUI ») reprend la même chaîne ; il n'a jamais tourné.

## Signature de code (Windows)

Sans signature, Smart App Control et SmartScreen bloquent ou avertissent à l'installation. `scripts/sign-windows.ps1` signe avec `signtool` (SHA-256, horodatage) : tous les `.exe` et `.dll` non signés de `dist/bin` avant l'empaquetage, puis l'installeur. Il lit `MIMIR_SIGN_PFX` et `MIMIR_SIGN_PASSWORD` ; le workflow les remplit depuis les secrets GitHub `WINDOWS_SIGN_PFX_BASE64` et `WINDOWS_SIGN_PASSWORD`.

Décision à prendre : le certificat. Un certificat de signature de code d'une autorité reconnue par Windows (payant, quelques centaines d'euros par an) ou Azure Trusted Signing (sans fichier de clé). À vérifier à ce moment-là : les conditions de réputation SmartScreen ont changé ces dernières années.

## Adresses à remplacer

Mimir n'a pas encore de site : `branding/mimir/branding.nsi` pointe vers `https://mimir.invalid` (domaine réservé qui ne résout jamais). À remplacer dès qu'il existe, avant toute distribution.
