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
- [ ] Vérifier que la version de MozillaBuild / VS / SDK est celle exigée par la source ESR choisie
- [ ] Cloner la source de Firefox ESR, produire un build non modifié (valide la chaîne)
- [ ] Créer `branding/mimir` (nom, logo, icônes), `mozconfig` Mimir
- [ ] Premier build Mimir lançable

## Phase 2 : patchs
- [ ] Retirer ou neutraliser : télémétrie, Pocket, sponsors, études, rapports de crash, Firefox Accounts (ou rendre optionnels)
- [ ] Valeurs par défaut privacy figées (`PRIVACY.md`)
- [ ] uBlock Origin en add-on système
- [ ] Page de démarrage locale

## Phase 3 : moteur de blocage natif (à décider)
- [ ] Prototype adblock-rust dans Gecko, mesure du gain face à uBO

## Phase 4 : distribution
- [ ] Installeur Windows, paquets Linux
- [ ] Mises à jour signées
- [ ] CI, builds reproductibles
- [ ] Site et documentation publics
