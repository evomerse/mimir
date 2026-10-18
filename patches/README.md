# Patchs et overlay

Deux mécanismes pour modifier Firefox sans en garder une copie complète. Les deux sont appliqués par `scripts/apply-patches.sh` (appelé par `scripts/build-wsl.sh`), de façon idempotente.

- **`../overlay/`** : fichiers *nouveaux*, copiés tels quels dans la source (même arborescence). Exemple : `overlay/browser/themes/addons/mimir-nuit/`.
- **`*.patch`** (ici) : modifications de fichiers Firefox *existants*, au format `git diff`, un fichier par sujet, numérotés. Ils doivent être rejoués à chaque mise à jour de la base ESR.

| Patch | Rôle |
|-------|------|
| `0001-themes-integres.patch` | déclare les thèmes Mimir (Nuit, Aube, Aurore, Lagune) dans `jar.mn` et `BuiltInThemeConfig` |
| `0002-vendor-mimir.patch` | `MOZ_APP_VENDOR=Mimir` : profil séparé de Firefox (`~/.config/mimir/mimir`, `%APPDATA%\Mimir\Mimir`) ; avec `--with-app-basename=Mimir`, l'exécutable devient `mimir` |
| `0003-ublock-origin-integre.patch` | enregistre `browser/extensions/ublock-origin` : uBlock Origin devient un add-on intégré du navigateur (sources dans `overlay/`, contenu du xpi décompressé par `scripts/prepare-ublock.sh`) |
| `0004-theme-premier-lancement.patch` | au premier lancement d'un profil, Mimir Nuit est le thème actif (la préférence par défaut ne suffit pas : le thème par défaut de Firefox est activé en premier) |
| `0005-sans-sante-ni-etudes.patch` | `browser/moz.configure` : ne compile plus le rapport de santé (`MOZ_SERVICES_HEALTHREPORT`) ni Normandy/études (`MOZ_NORMANDY`) ; ces flags ne se désactivent que là (`project_flag` n'accepte que l'origine « implied ») |
| `0006-prefs-vie-privee.patch` | bloc final de `browser/app/profile/firefox.js` : télémétrie, contenu sponsorisé, compte Firefox, sondes réseau (portail captif, région, géolocalisation) désactivés par défaut |
| `0007-page-de-demarrage.patch` | enregistre la page de démarrage locale (`overlay/browser/base/content/mimir-start.{html,css,js}`) dans `browser/base/jar.mn` |
| `0008-about-home-local.patch` | `about:home` et `about:newtab` chargent cette page au lieu d'Activity Stream (aucune requête réseau, aucun état) |
| `0009-stats-et-acteur-demarrage.patch` | enregistre le module `MimirStats` (compteur de blocages, démarré par `BrowserGlue`) et l'acteur `MimirStart` (dialogue page de démarrage / navigateur) ; sources dans `overlay/browser/modules/` et `overlay/browser/actors/` |

## Ajouter un patch

Modifier le fichier dans `~/ff/esr153`, puis `git diff -- <fichier> > patches/NNNN-sujet.patch`, puis `git checkout -- <fichier>` et relancer `scripts/apply-patches.sh` pour vérifier qu'il s'applique depuis zéro.
