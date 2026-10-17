# Architecture

## Base : Firefox ESR

- **Pourquoi Firefox** : moteur indépendant de Chromium, code sous MPL-2.0, politique d'entreprise (`policies.json`) qui permet de configurer beaucoup sans patcher.
- **Pourquoi ESR** : cycle de maintenance plus stable pour un projet à faible effectif, avec correctifs de sécurité. À vérifier au moment du fork : version ESR courante et fin de support.

## Adblock intégré

Brave embarque son moteur de filtrage (adblock-rust, Rust, MPL-2.0) directement dans le navigateur, au niveau des requêtes réseau. Cette connaissance vient de la documentation publique de Brave, **pas** d'une rétro-ingénierie de ma part (voir [REA-NOTES.md](REA-NOTES.md)).

Pour Mimir, trois niveaux :

1. **Phase 0 / 1 : uBlock Origin forcé** par `ExtensionSettings` (installation `force_installed`, verrouillée). Fonctionne dès maintenant, listes éprouvées. Limite : reste une extension (visible dans about:addons, désinstallable si non verrouillé).
2. **Phase 2 : uBlock Origin en add-on système** embarqué dans le build (dossier `browser/features` ou `distribution/extensions`), non désinstallable, mis à jour avec le navigateur. À valider dans le code source de la version ESR choisie.
3. **Phase 3 (optionnel) : moteur natif** adblock-rust exposé à Gecko via un composant XPCOM en Rust et branché sur les observateurs de requêtes. Gain : blocage avant l'envoi de la requête, sans passer par l'API WebExtensions. Coût : gros travail d'intégration à maintenir à chaque rebase. À décider après la phase 2.

## Valeurs par défaut vie privée

Appliquées d'abord via `distribution/` (prefs verrouillées ou par défaut), puis figées dans le build (phase 2). Liste et justification dans [PRIVACY.md](PRIVACY.md).

## Mises à jour

Point critique : un navigateur sans mises à jour de sécurité est dangereux. Phase 4 : serveur de mises à jour auto-hébergé (ou GitHub Releases) avec signature. Tant que ce n'est pas en place, **ne pas distribuer de builds** publiquement.

## Ce qui est volontairement exclu

Compte Mimir, synchronisation propriétaire, publicité ou « sponsors » dans la page d'accueil, crypto-monnaie, VPN payant intégré. Chacun pourrait être discuté plus tard, mais pas par défaut.
