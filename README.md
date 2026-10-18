# Mimir

> Le puits de la connaissance. Un navigateur open source qui ne vend pas tes données.

Dans la mythologie nordique, Mímir garde le puits de la sagesse (Mímisbrunnr) : Odin y sacrifie un œil pour boire sa connaissance. Le navigateur reprend l'idée : l'accès à la connaissance du web, sans que ton regard soit revendu.

Mimir est une *distribution* de [Firefox ESR](https://www.mozilla.org/firefox/enterprise/) 153.5.0 (comme LibreWolf ou Floorp) : le moteur Gecko, sans la télémétrie, avec un bloqueur de pubs intégré. Licence MPL-2.0.

## Ce que Mimir fait de plus (ou de moins) que Firefox

- **Aucune télémétrie** : rapports de santé, études Normandy et rapports de crash ne sont pas compilés ; les sponsors, suggestions et comptes sont coupés. Détail, y compris ce que le navigateur contacte encore : [docs/PRIVACY.md](docs/PRIVACY.md).
- **uBlock Origin intégré**, actif dès le premier lancement, non désinstallable, autorisé en navigation privée.
- **DuckDuckGo** comme moteur de recherche par défaut.
- **Page de démarrage locale** (aucune requête réseau) : horloge, ton lecteur de musique préféré au choix (Spotify, YouTube Music, Deezer, Apple Music, SoundCloud, TIDAL, Amazon Music, Bandcamp), raccourcis, compteur de pubs et traqueurs bloqués.
- **Identité propre** : nom, logo, thèmes, installeur ; aucune mascotte ni marque de Mozilla.
- **Français** : l'interface suit la langue du système (pack de langue officiel de Mozilla).
- Les modules médias OpenH264 et Widevine sont gardés (visio, Spotify, Netflix) ; ils sont téléchargés au premier lancement.

## Installer

Les fichiers sont dans la page [**Releases**](https://github.com/evomerse/mimir/releases) du dépôt, avec un fichier `SHA256SUMS.txt` pour vérifier les téléchargements. Vous pouvez aussi [compiler soi-même](#compiler-soi-même).

### Windows 10 / 11 (64 bits)

1. Télécharger `mimir-<version>-windows-x86_64-installer.exe` et vérifier son empreinte : `Get-FileHash <fichier> -Algorithm SHA256`, à comparer à la ligne correspondante de `SHA256SUMS.txt`.
2. Lancer l'installeur et suivre l'assistant.
3. Au premier lancement, si l'interface reste en anglais alors que Windows est en français, fermer puis rouvrir Mimir une fois : le pack de langue s'installe au premier démarrage.

**L'installeur n'est pas signé** (pas de certificat de signature de code pour l'instant) :

- Windows SmartScreen peut afficher « Windows a protégé votre ordinateur » : cliquer sur **Informations complémentaires**, puis **Exécuter quand même**.
- Si **Smart App Control** est activé, Windows refuse l'installeur sans proposer de contournement, et le désactiver est irréversible sans réinstaller Windows. Mimir n'est donc pas utilisable sur ces machines pour le moment.

Une archive `mimir-<version>-windows-x86_64.zip` sans installation est aussi fournie (mêmes remarques).

### Linux (x86_64)

Construit sur Ubuntu 24.04 : une distribution plus ancienne peut manquer de bibliothèques système.

```sh
tar xf mimir-<version>-linux-x86_64.tar.xz
./mimir/mimir
```

Pour vérifier le téléchargement : `sha256sum -c SHA256SUMS.txt --ignore-missing` dans le dossier des fichiers. Il n'y a pas encore de paquet `.deb`, Flatpak ni raccourci de menu : l'archive se décompresse n'importe où et se lance directement. Le profil est dans `~/.config/mimir`.

### macOS

Pas disponible pour le moment (voir [docs/ROADMAP.md](docs/ROADMAP.md)).

## Compiler soi-même

Mimir = source de Firefox ESR (cloner à part) + `overlay/` + `patches/` + `branding/` + `distribution/`. Un build complet prend 2 à 3 heures et plus de 80 Go de disque. Le pas-à-pas pour Linux (y compris sous WSL2) et pour Windows (dans une VM) est dans [docs/BUILD.md](docs/BUILD.md).

## État du projet

| Phase | Contenu | État |
|-------|---------|------|
| 0 | Prototype : Firefox officiel + `policies.json` + autoconfig + uBlock Origin | fait (`scripts/install-prototype.ps1`) |
| 1 | Build maison de Firefox ESR, branding Mimir | fait (Linux, Windows) |
| 2 | Patchs : retrait de la télémétrie, valeurs par défaut vie privée, page de démarrage | fait |
| 3 | Moteur de blocage natif (adblock-rust) à la place de l'extension | à étudier |
| 4 | Installeur, mises à jour, signature, CI, macOS, builds reproductibles | en cours |

Détails : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/PRIVACY.md](docs/PRIVACY.md), [docs/ROADMAP.md](docs/ROADMAP.md).

## Structure

```
overlay/        fichiers nouveaux ajoutés à la source de Firefox (page de démarrage, acteurs, illustrations)
patches/        modifications des fichiers de Firefox (patchs numérotés, voir patches/README.md)
branding/       logo, icônes, thèmes, images de l'installeur
distribution/   politiques (policies.json) et autoconfig embarqués dans le paquet
build/          fichiers de configuration de compilation (mozconfig)
scripts/        build, empaquetage, tests, outils
docs/           architecture, vie privée, compilation, feuille de route
```

## Marques

« Firefox » et son logo sont des marques de Mozilla. Un navigateur modifié distribué sous le nom Mimir ne doit pas utiliser ces marques : le branding de Mimir les remplace. Mimir n'est pas affilié à Mozilla, ni à Brave. Les logos des services de musique et des sites affichés sur la page de démarrage (jeu d'icônes [Simple Icons](https://simpleicons.org), domaine public) appartiennent à leurs propriétaires et ne servent qu'à les désigner.
