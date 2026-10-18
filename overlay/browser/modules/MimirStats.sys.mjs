/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Compteur local de requetes bloquees par l'adblock integre.
 *
 * Il observe les requetes annulees par une extension (webRequest) et ne garde
 * que deux nombres : le total et celui du jour. Ni adresse, ni site, ni date
 * autre que le jour courant. Les fenetres privees ne sont pas comptees.
 * Rien ne quitte le profil.
 */

const PREF_TOTAL = "mimir.stats.blocked.total";
const PREF_DAY = "mimir.stats.blocked.day";
const PREF_TODAY = "mimir.stats.blocked.today";
const FLUSH_DELAY_MS = 10000;

function dayKey(date = new Date()) {
  let pad = n => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

export const MimirStats = {
  _started: false,
  _total: 0,
  _today: 0,
  _day: "",
  _timer: null,
  // Une requete annulee peut etre signalee par deux notifications.
  _seen: new WeakSet(),

  init() {
    if (this._started) {
      return;
    }
    this._started = true;
    this._total = Services.prefs.getIntPref(PREF_TOTAL, 0);
    this._day = Services.prefs.getStringPref(PREF_DAY, "");
    this._today = Services.prefs.getIntPref(PREF_TODAY, 0);
    this._rollDay();
    Services.obs.addObserver(this, "http-on-failed-opening-request");
    Services.obs.addObserver(this, "http-on-stop-request");
    Services.obs.addObserver(this, "quit-application-granted");
  },

  /** @returns {{total: number, today: number}} */
  get() {
    this._rollDay();
    return { total: this._total, today: this._today };
  },

  _rollDay() {
    let today = dayKey();
    if (this._day !== today) {
      this._day = today;
      this._today = 0;
      this._dirty();
    }
  },

  observe(subject, topic) {
    if (topic === "quit-application-granted") {
      this._flush();
      Services.obs.removeObserver(this, "http-on-failed-opening-request");
      Services.obs.removeObserver(this, "http-on-stop-request");
      Services.obs.removeObserver(this, "quit-application-granted");
      this._started = false;
      return;
    }

    let channel;
    try {
      channel = subject.QueryInterface(Ci.nsIChannel);
    } catch (e) {
      return;
    }
    let loadInfo = channel.loadInfo;
    if (
      !loadInfo ||
      loadInfo.requestBlockingReason !==
        Ci.nsILoadInfo.BLOCKING_REASON_EXTENSION_WEBREQUEST ||
      loadInfo.originAttributes.privateBrowsingId ||
      this._seen.has(channel)
    ) {
      return;
    }
    this._seen.add(channel);
    this._rollDay();
    this._total++;
    this._today++;
    this._dirty();
  },

  _dirty() {
    if (this._timer) {
      return;
    }
    this._timer = Cc["@mozilla.org/timer;1"].createInstance(Ci.nsITimer);
    this._timer.initWithCallback(
      () => this._flush(),
      FLUSH_DELAY_MS,
      Ci.nsITimer.TYPE_ONE_SHOT
    );
  },

  _flush() {
    if (this._timer) {
      this._timer.cancel();
      this._timer = null;
    }
    Services.prefs.setIntPref(PREF_TOTAL, this._total);
    Services.prefs.setStringPref(PREF_DAY, this._day);
    Services.prefs.setIntPref(PREF_TODAY, this._today);
  },
};
