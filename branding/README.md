# Branding

Identité de Mimir : nom, logo, icônes, chaînes de marque. Aucun asset Mozilla ou Firefox ne doit être copié ici : leurs marques ne sont pas sous licence libre.

```
source/   logo d'origine (logo-original.jpg) et le « M » extrait en PNG transparent
mimir/    dossier de branding au format Firefox (browser/branding/mimir dans la source)
```

## Chaîne de génération

```
logo-original.jpg --prepare-logo.py--> mimir-mark.png + mimir-mark-private.png --make-icons.py--> mimir/*.png, *.ico, about-logo.svg
```

Depuis Windows (les scripts s'exécutent dans WSL, Pillow et NumPy y sont installés) :

```
wsl -d Ubuntu-24.04 -- python3 /mnt/d/Projets/mimir/scripts/prepare-logo.py
wsl -d Ubuntu-24.04 -- python3 /mnt/d/Projets/mimir/scripts/make-icons.py
```

La variante violette (navigation privée) est obtenue par rotation de teinte du « M » bleu.

`mimir/` est dérivé de la structure du branding « unofficial » de Firefox (fichiers `moz.build`, `jar.mn`, `configure.sh`, préférences). Les noms (`Mimir`) sont dans `mimir/configure.sh` et `mimir/locales/en-US/brand.{ftl,properties}`. Le build copie `mimir/` dans la source Firefox via `scripts/sync-branding.sh` (appelé par `scripts/build-wsl.sh`).

## À faire

- Le logo d'origine est une image JPG : le « M » extrait garde un léger liseré sombre sur fond clair. Idéal : une version vectorielle (SVG) du logo, ce qui permettrait aussi de supprimer le PNG embarqué dans `content/about-logo.svg`.
- Les logos-texte `content/about-wordmark.svg` et `content/firefox-wordmark.svg` sont du texte SVG avec une police système, à remplacer par le « MIMIR » du logo (version vectorielle).
- Phase 4 (installeur Windows) : recréer les images d'installeur retirées (`wizHeader*.bmp`, `wizWatermark.bmp`, `stubinstaller/`, `background.png`) et vérifier `branding.nsi`.
- Fichiers macOS retirés (`*.icns`, `Assets.car`) : à recréer si un build macOS est un jour visé.
