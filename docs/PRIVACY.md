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
| Moteur de recherche par défaut | DuckDuckGo (décidé le 2026-10-18, vérifié par `scripts/test-privacy.py`) |
| Page de démarrage | page locale (`chrome://browser/content/mimir-start.html`), sans appel réseau ; le compteur de blocages (deux nombres, hors fenêtres privées) reste dans le profil |

## Connexions observées au repos (build du 2026-10-18)

`scripts/test-privacy.py` : profil vierge, 45 s sans navigation. Rien vers un service de télémétrie. Reste :

| Hôte | Pourquoi |
|------|----------|
| `firefox.settings.services.mozilla.com`, `firefox-settings-attachments.cdn.mozilla.net`, `content-signature-2.cdn.mozilla.net` | Remote Settings : listes de blocage de sécurité (add-ons, certificats). Sans état, pas d'identifiant. À garder |
| `cdn.jsdelivr.net`, `ublockorigin.github.io`, `ublockorigin.pages.dev`, `malware-filter.pages.dev`, `curbengh.github.io`, `pgl.yoyo.org`, `publicsuffix.org` | uBlock Origin télécharge ses listes de filtres au premier lancement |
| `aus5.mozilla.org`, `ciscobinary.openh264.org`, `update.googleapis.com`, `edgedl.me.gvt1.com`, `www.google.com` (téléchargement du module Widevine, fichier `chrome_component/....crx3`) | modules médias OpenH264 et Widevine, **gardés** (décision du 2026-10-18) : Widevine est nécessaire à la lecture protégée (Spotify, Netflix, etc.), OpenH264 à la visio H.264. Ils sont téléchargés au premier lancement ; `media.gmp-provider.enabled=false` supprimerait ces connexions mais casserait ces usages |

`a.nel.cloudflare.com` et `csp.withgoogle.com` apparaissent aussi dans le journal, mais seulement comme adresses de rapport annoncées dans des en-têtes de réponse (`report-to`, `report-uri`) : Mimir ne les contacte pas.

## Questions ouvertes

- **Résolveur DoH par défaut** ou DNS système.
- **Safe Browsing** : protège contre le phishing mais envoie des préfixes de hash à Google. Garder, remplacer ou désactiver ?
- **Financement** : dons, sponsoring, ou rien. Aucune solution ne doit passer par la monétisation des données.
