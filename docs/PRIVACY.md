# Engagements vie privée

## Principes

1. Mimir n'envoie aucune donnée d'usage à ses développeurs. Pas de télémétrie, pas de rapport d'erreurs automatique, pas d'études à distance.
2. Mimir ne vend ni ne partage aucune donnée. Il n'y a pas de compte, donc rien à vendre.
3. Les seules connexions initiées par le navigateur lui-même sont celles nécessaires à son fonctionnement et listées ici : mises à jour (phase 4), mise à jour des listes de filtres, Safe Browsing si activé.
4. Tout est vérifiable dans le code.

## Réglages visés (phase 0 via policies.json, phase 2 figés dans le build)

| Domaine | Choix |
|---------|-------|
| Télémétrie / études / Normandy | désactivées |
| Pocket, sponsors, suggestions Firefox Suggest | désactivés |
| Protection contre le pistage | stricte, verrouillée |
| Fingerprinting | protection activée (FPP) ; `resistFingerprinting` complet laissé en option car il casse des sites |
| DNS | DNS-over-HTTPS proposé, résolveur à choisir (voir questions ouvertes) |
| Moteur de recherche par défaut | à choisir (voir questions ouvertes) |
| Page de démarrage | page locale, sans appel réseau |

## Questions ouvertes

- **Moteur de recherche par défaut** : DuckDuckGo, Brave Search, Startpage, une instance SearXNG ? Les accords de moteur par défaut sont la principale source de revenus de Mozilla ; Mimir doit décider s'il en veut ou non.
- **Résolveur DoH par défaut** ou DNS système.
- **Safe Browsing** : protège contre le phishing mais envoie des préfixes de hash à Google. Garder, remplacer ou désactiver ?
- **Financement** : dons, sponsoring, ou rien. Aucune solution ne doit passer par la monétisation des données.
