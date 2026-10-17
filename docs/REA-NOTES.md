# Notes d'analyse REA (Firefox / Brave)

Date : 2026-10-17. Objectif demandé : utiliser REA sur Firefox et Brave pour s'inspirer de leur base.

## Observé

- **Brave** est installé : `C:\Program Files\BraveSoftware\Brave-Browser\Application`, dossier de version `155.1.97.59`.
  - Fichiers les plus gros : `chrome.dll` (312,8 Mo, moteur + code Brave), `brave_resources.pak` (25,7 Mo), `resources.pak` (25,3 Mo), `brave_vpn_wireguard_service.exe`, `brave_vpn_helper.exe`.
  - L'exécutable `brave.exe` (4,4 Mo) est un lanceur ; la logique est dans `chrome.dll`.
- **Firefox** n'est pas installé sur cette machine.
- **REA** : le fournisseur d'analyse native (Ghidra) n'est pas configuré (`GHIDRA_INSTALL_DIR` absent). La seule Java détectée est une JRE 1.8, très probablement trop ancienne pour la version de Ghidra attendue (12.1.x), non vérifié.

## Non observé

Aucune décompilation de Brave ni de Firefox n'a été faite. Tout ce que ces documents disent du fonctionnement interne de Brave (adblock-rust, blocage au niveau réseau) vient de la documentation publique, pas de cette analyse.

## Pourquoi REA n'est pas l'outil principal ici

Firefox et Brave sont open source : leur code source complet est disponible et plus fiable qu'une décompilation de `chrome.dll`. La doc de REA recommande d'ailleurs les outils normaux pour un dépôt source complet. REA reste utile pour **comparer le binaire installé au source** (vérifier qu'un build correspond), ou pour inspecter un build de Mimir plus tard (flux réseau, chaînes, appels sortants), ce qui sert directement l'engagement « zéro télémétrie ».

## Suites possibles avec REA

- Phase 1/2 : analyser le build Mimir pour prouver l'absence d'URL de télémétrie (`search_strings`, `inspect_web_network_capture` sur une capture de trafic).
- Si Ghidra 12.1 + JDK récent sont installés : cartographier comment `chrome.dll` appelle le moteur de filtres Brave, pour comparer avec le code source de Brave.
