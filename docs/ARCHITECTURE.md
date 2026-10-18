# Architecture

## Base : Firefox ESR

- **Pourquoi Firefox** : moteur indépendant de Chromium, code sous MPL-2.0, politique d'entreprise (`policies.json`) qui permet de configurer beaucoup sans patcher.
- **Pourquoi ESR** : cycle de maintenance plus stable pour un projet à faible effectif, avec correctifs de sécurité. À vérifier au moment du fork : version ESR courante et fin de support.

## Adblock intégré

Brave embarque son moteur de filtrage (adblock-rust, Rust, MPL-2.0) directement dans le navigateur, au niveau des requêtes réseau. Cette connaissance vient de la documentation publique de Brave, **pas** d'une rétro-ingénierie de ma part (voir [REA-NOTES.md](REA-NOTES.md)).

Pour Mimir, trois niveaux :

1. **Phase 0 / 1 : uBlock Origin forcé** par `ExtensionSettings` (installation `force_installed`, verrouillée). Fonctionne dès maintenant, listes éprouvées. Limite : reste une extension (visible dans about:addons, désinstallable si non verrouillé).
2. **uBlock Origin add-on intégré** (en place dans le build Mimir, patch 0003) : le xpi signé de l'auteur est téléchargé par `scripts/fetch-ublock.sh` (version et SHA-256 figés), décompressé par `scripts/prepare-ublock.sh` dans `browser/extensions/ublock-origin/` et compilé dans le navigateur. Il est actif dès le premier lancement, sans installation, et n'est pas désinstallable. Mise à jour : changer la version et l'empreinte dans `fetch-ublock.sh` (uBO est mis à jour avec le navigateur, pas séparément). Ses listes de filtres se mettent à jour d'elles-mêmes.
3. **Phase 3 (optionnel) : moteur natif** adblock-rust exposé à Gecko via un composant XPCOM en Rust et branché sur les observateurs de requêtes. Gain : blocage avant l'envoi de la requête, sans passer par l'API WebExtensions. Coût : gros travail d'intégration à maintenir à chaque rebase. À décider après la phase 2.

## Identité et personnalisation

- **Profil séparé** : `MOZ_APP_VENDOR=Mimir` (patch 0002) et `--with-app-basename=Mimir` (mozconfig). Le programme s'appelle `mimir` et son profil est `~/.config/mimir/mimir` (Linux), `%APPDATA%\Mimir\Mimir` (Windows) : Mimir et Firefox coexistent sans partager de profil.
- **Thèmes intégrés** : quatre thèmes aux couleurs du logo (Nuit par défaut, Aube, Aurore, Lagune), générés par `scripts/make-themes.py`, choisissables dans « Extensions et thèmes ». Les utilisateurs gardent aussi les thèmes Firefox habituels, la personnalisation de la barre d'outils, les onglets verticaux, etc.

## Page de démarrage

`about:home` et `about:newtab` chargent `chrome://browser/content/mimir-start.html` (patchs 0007 et 0008) à la place d'Activity Stream. Page locale, sans requête réseau au chargement : horloge, lecteur de musique, raccourcis, compteur de blocages.

- **Musique** : l'utilisateur choisit son service (Spotify, YouTube Music, Deezer, Apple Music, SoundCloud, TIDAL, Amazon Music, Bandcamp), mémorisé dans le profil. La page propose « Ouvrir le service » et six ambiances (concentration, détente, énergie, nuit, jazz, classique) qui ouvrent une recherche sur ce service. Aucun lecteur n'est intégré à la page : rien n'est contacté tant que l'utilisateur ne clique pas.
- **Raccourcis** : jusqu'à 8 sites, en `https` uniquement ; aucune icône n'est téléchargée, donc aucun appel réseau : une vingtaine de sites connus ont leur logo (Simple Icons, domaine public, chemins SVG embarqués dans `mimir-start.js`), les autres une pastille colorée avec l'initiale. Les 8 services de musique ont aussi leur logo.
- **Compteur** : `browser/modules/MimirStats.sys.mjs` observe les requêtes annulées par l'extension (`BLOCKING_REASON_EXTENSION_WEBREQUEST`), hors fenêtres privées, et ne garde que deux nombres (total, aujourd'hui) dans les préférences du profil.
- **Liaison page / navigateur** : acteur `MimirStart` (`browser/actors/MimirStart{Parent,Child}.sys.mjs`, patch 0009). La page envoie un événement `MimirStartQuery` (qui doit *remonter* : `bubbles: true`) et reçoit `MimirStartReply`. Le parent valide tout (service dans une liste fermée, raccourcis en `https`, taille bornée).
- Sources : `overlay/browser/base/content/mimir-start.{html,css,js}`. Textes en français ou anglais selon la langue du navigateur.

## Valeurs par défaut vie privée

Appliquées d'abord via `distribution/` (prefs verrouillées ou par défaut), puis figées dans le build (phase 2). Liste et justification dans [PRIVACY.md](PRIVACY.md).

## Mises à jour

Point critique : un navigateur sans mises à jour de sécurité est dangereux. Phase 4 : serveur de mises à jour auto-hébergé (ou GitHub Releases) avec signature. Tant que ce n'est pas en place, **ne pas distribuer de builds** publiquement.

## Ce qui est volontairement exclu

Compte Mimir, synchronisation propriétaire, publicité ou « sponsors » dans la page d'accueil, crypto-monnaie, VPN payant intégré. Chacun pourrait être discuté plus tard, mais pas par défaut.
