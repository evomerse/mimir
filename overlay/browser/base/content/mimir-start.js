/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Page de demarrage locale de Mimir : aucune requete reseau, aucun etat.

const STRINGS = {
  fr: {
    morning: "Bonjour",
    afternoon: "Bon après-midi",
    evening: "Bonsoir",
    hint: "Tapez dans la barre d’adresse pour chercher ou ouvrir un site.",
    "adblock-title": "Publicités bloquées",
    "adblock-text": "uBlock Origin est intégré à Mimir.",
    "telemetry-title": "Aucune télémétrie",
    "telemetry-text": "Mimir n’envoie rien à ses développeurs.",
    "account-title": "Aucun compte",
    "account-text": "Pas de compte, donc rien à vendre.",
  },
  en: {
    morning: "Good morning",
    afternoon: "Good afternoon",
    evening: "Good evening",
    hint: "Type in the address bar to search or open a site.",
    "adblock-title": "Ads blocked",
    "adblock-text": "uBlock Origin is built into Mimir.",
    "telemetry-title": "No telemetry",
    "telemetry-text": "Mimir sends nothing to its developers.",
    "account-title": "No account",
    "account-text": "No account, so nothing to sell.",
  },
};

const lang = navigator.language.startsWith("fr") ? "fr" : "en";
const strings = STRINGS[lang];

for (let el of document.querySelectorAll("[data-i18n]")) {
  el.textContent = strings[el.dataset.i18n];
}
document.documentElement.lang = lang;
document.getElementById("hint").textContent = strings.hint;

let now = new Date();
let hour = now.getHours();
document.getElementById("greeting").textContent =
  hour < 5 || hour >= 18
    ? strings.evening
    : hour < 12
      ? strings.morning
      : strings.afternoon;
document.getElementById("date").textContent = now.toLocaleDateString(lang, {
  weekday: "long",
  day: "numeric",
  month: "long",
});
