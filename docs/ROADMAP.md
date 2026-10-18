# Feuille de route

## Phase 0 : prototype par configuration
- [x] Structure du dépôt, licence MPL-2.0
- [x] `policies.json` + autoconfig + script d'installation
- [x] Firefox ESR 153.4.0 installé, prototype copié (2026-10-17)
- [x] Testé sur profil vierge : uBlock Origin s'installe seul ; prefs de télémétrie à `false` et verrouillées (lues en direct via Marionette)
- [ ] Vérifier visuellement `about:policies` et que uBlock Origin ne peut pas être désinstallé
- [ ] Mesurer ce que Firefox contacte encore au démarrage (capture réseau)

## Phase 1 : build maison
- [x] Outils installés (2026-10-17) : MozillaBuild (`C:\mozilla-build`), VS 2022 Build Tools C++ + SDK Windows 11, Rust 1.99.1, Python 3.12, Git ; D: a ~200 Go libres
- [x] Source Firefox ESR 153.5.0 clonée (`D:\ff\esr153`), `mach bootstrap` réussi sous Windows
- [!] **Blocage Windows (2026-10-17)** : Smart App Control (actif) refuse les outils non signés de Mozilla (`llvm-lib.exe`, WinError 4551, événements CodeIntegrity 3077). Le build Windows ne passe pas sur cette machine sans désactiver Smart App Control (irréversible sans réinstaller Windows sur la plupart des versions).
- [x] Décision : compiler sous Linux via WSL2 (Ubuntu 24.04) ; source clonée dans `~/ff/esr153` (système de fichiers WSL, pas `/mnt/d`)
- [x] WSL2 configuré (`~/.wslconfig` : 24 Go RAM, 16 Go swap) ; sans swap, 16 jobs en parallèle gelaient la VM. Build avec `-j12`
- [ ] Build Windows plus tard : machine ou CI sans Smart App Control + signature de code
- [x] Build non modifié de Firefox ESR 153.5.0 produit sous WSL2 et lancé via WSLg (2026-10-17) ; `build/lancer-wsl.cmd` le lance (la fenêtre doit rester ouverte)
- [x] `branding/mimir` (nom, icônes générées par `scripts/make-icons.py`), `build/mozconfig.mimir`, `scripts/build-wsl.sh`
- [x] Vrai logo intégré (`branding/source/logo-original.jpg`, extraction par `scripts/prepare-logo.py`) ; [ ] version vectorielle du logo
- [ ] Premier build Mimir lançable

## Phase 2 : patchs
- [x] uBlock Origin intégré au build comme add-on intégré (`browser/extensions/ublock-origin`, non désinstallable) ; [ ] vérifier son fonctionnement en navigation privée et son blocage réel
- [x] Profil séparé de Firefox (vendor `Mimir`), thèmes Mimir (Nuit par défaut, Aube, Aurore, Lagune), page d'accueil sans météo/articles, DuckDuckGo par défaut (provisoire)
- [x] Retiré ou neutralisé dans le build : rapport de santé et Normandy non compilés (patch 0005), rapports de crash non compilés (`--disable-crashreporter`), télémétrie / sponsors / compte Firefox / sondes réseau désactivés par défaut (patch 0006)  ; [x] vérifié à l'exécution le 2026-10-18 par `scripts/test-privacy.py` (constantes, prefs, hôtes contactés au repos)
- [x] Valeurs par défaut privacy figées dans le build (patch 0006) ; `mimir.cfg` les verrouille encore (télémétrie)
- [ ] uBlock Origin en add-on système
- [x] Page de démarrage locale (patchs 0007-0008, vérifiée par `scripts/test-start-page.py`) ; [ ] compteur de pubs bloquées, raccourcis

## Phase 3 : moteur de blocage natif (à décider)
- [ ] Prototype adblock-rust dans Gecko, mesure du gain face à uBO

## Phase 4 : distribution
- [ ] Signature de code Windows : sans binaires signés, Smart App Control bloque Mimir chez les utilisateurs qui l'ont activé
- [ ] Installeur Windows, paquets Linux
- [ ] Mises à jour signées
- [ ] CI, builds reproductibles
- [ ] Site et documentation publics
