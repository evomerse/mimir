# Mimir

> Le puits de la connaissance. Un navigateur open source qui ne vend pas tes données.

Dans la mythologie nordique, Mímir garde le puits de la sagesse (Mímisbrunnr) : Odin y sacrifie un œil pour boire sa connaissance. Le navigateur reprend l'idée : l'accès à la connaissance du web, sans que ton regard soit revendu.

## Objectifs

1. **Respect de la vie privée par construction** : aucune télémétrie, aucune vente ni partage de données, aucun compte obligatoire.
2. **Bloqueur de pubs et de traqueurs intégré**, actif dès le premier lancement (comme Brave), sans installation.
3. **Base Firefox** (moteur Gecko) : un vrai navigateur complet, pas une coque autour d'un autre moteur.
4. **Open source**, licence MPL-2.0 (celle de Firefox).

## Approche

Mimir est une *distribution* de Firefox ESR, comme LibreWolf ou Floorp, développée par étapes :

| Phase | Contenu | État |
|-------|---------|------|
| 0 | Prototype : Firefox officiel + `policies.json` + autoconfig + uBlock Origin forcé | squelette prêt |
| 1 | Build maison de Firefox ESR avec branding Mimir | à faire |
| 2 | Patchs : retrait télémétrie/Pocket/sponsors, valeurs par défaut privacy, adblock système | à faire |
| 3 | Moteur de blocage natif (adblock-rust) à la place de l'extension | à étudier |
| 4 | Installeur, mises à jour, CI, builds reproductibles | à faire |

Détails : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/PRIVACY.md](docs/PRIVACY.md), [docs/ROADMAP.md](docs/ROADMAP.md).

## Structure

```
distribution/   configuration appliquée à un Firefox installé (phase 0)
branding/       logo, icônes, noms (phase 1)
patches/        patchs appliqués au code source de Firefox (phase 2)
scripts/        installation du prototype, outils de build
docs/           architecture, vie privée, feuille de route, notes d'analyse
```

## Essayer le prototype (phase 0)

Nécessite Firefox ESR installé. Voir [scripts/install-prototype.ps1](scripts/install-prototype.ps1) : il copie `distribution/` dans le dossier d'installation de Firefox (droits administrateur requis). Le script affiche ce qu'il va faire et demande confirmation.

## Marques

« Firefox » et son logo sont des marques de Mozilla. Un navigateur modifié distribué sous le nom Mimir ne doit pas utiliser ces marques : le branding de la phase 1 les remplace entièrement. Mimir n'est pas affilié à Mozilla ni à Brave.
