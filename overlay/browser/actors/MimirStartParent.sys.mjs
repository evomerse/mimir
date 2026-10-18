/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

import { MimirStats } from "resource:///modules/MimirStats.sys.mjs";

const PREF_MUSIC = "mimir.start.music.service";
const PREF_SHORTCUTS = "mimir.start.shortcuts";
const MAX_SHORTCUTS = 8;

// Les services de musique proposes ; la page choisit l'un d'eux par son id.
const MUSIC_SERVICES = [
  "spotify",
  "youtube-music",
  "deezer",
  "apple-music",
  "soundcloud",
  "tidal",
  "amazon-music",
  "bandcamp",
];

function readShortcuts() {
  try {
    let list = JSON.parse(Services.prefs.getStringPref(PREF_SHORTCUTS, "[]"));
    return Array.isArray(list) ? list.filter(isValidShortcut) : [];
  } catch (e) {
    return [];
  }
}

function isValidShortcut(s) {
  if (!s || typeof s.url !== "string" || typeof s.title !== "string") {
    return false;
  }
  try {
    return new URL(s.url).protocol === "https:";
  } catch (e) {
    return false;
  }
}

/**
 * Cote processus parent de la page de demarrage de Mimir : statistiques de
 * blocage, service de musique choisi, raccourcis. Les messages viennent d'une
 * page locale mais sont tous valides ici avant d'etre enregistres.
 */
export class MimirStartParent extends JSWindowActorParent {
  receiveMessage({ name, data }) {
    switch (name) {
      case "MimirStart:Get":
        return {
          stats: MimirStats.get(),
          music: Services.prefs.getStringPref(PREF_MUSIC, ""),
          shortcuts: readShortcuts(),
        };
      case "MimirStart:SetMusic":
        if (MUSIC_SERVICES.includes(data)) {
          Services.prefs.setStringPref(PREF_MUSIC, data);
        }
        return null;
      case "MimirStart:SetShortcuts": {
        let list = (Array.isArray(data) ? data : [])
          .filter(isValidShortcut)
          .slice(0, MAX_SHORTCUTS)
          .map(({ url, title }) => ({
            url,
            title: String(title).slice(0, 40),
          }));
        Services.prefs.setStringPref(PREF_SHORTCUTS, JSON.stringify(list));
        return list;
      }
    }
    return null;
  }
}
