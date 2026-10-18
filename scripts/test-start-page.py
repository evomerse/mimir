#!/usr/bin/env python3
"""Verifie la page de demarrage locale de Mimir sur un profil jetable :
about:home / about:newtab, compteur de blocages, choix du service de musique, raccourcis,
persistance apres rechargement, ouverture d'un lien, captures d'ecran.

A executer dans WSL :  ~/ff/venv/bin/python scripts/test-start-page.py [dossier de captures]
"""
import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import time

from marionette_driver.marionette import Marionette

FF = os.environ.get("MIMIR_EXE") or os.path.expanduser("~/ff/esr153/obj-validate/dist/bin/mimir")
PROFILE = os.path.expanduser("~/ff/profile-start-test")
PORT = 2828

PAGE_JS = """
return {
  url: document.documentURI,
  salut: document.getElementById("greeting").textContent,
  horloge: document.getElementById("clock").textContent,
  services: document.querySelectorAll(".service").length,
  logos: document.querySelectorAll(".service svg path").length,
  logos_raccourcis: document.querySelectorAll("#shortcuts .tile.has-logo svg path").length,
  choisi: document.querySelector('.service[aria-checked="true"]')?.textContent ?? null,
  ouvrir: document.getElementById("music-open").hidden ? null : document.getElementById("music-open").href,
  ambiances: document.querySelectorAll("#moods a").length,
  raccourcis: [...document.querySelectorAll("#shortcuts a")].map(a => a.href),
  stats: document.getElementById("stats").textContent,
  reseau: performance.getEntriesByType("resource").map(e => e.name).filter(n => !n.startsWith("chrome://")),
};
"""

BLOCK_JS = """
const done = arguments[arguments.length - 1];
const urls = [
  "https://static.ads-twitter.com/uwt.js",
  "https://connect.facebook.net/en_US/fbevents.js",
  "https://bat.bing.com/bat.js",
  "https://www.googleadservices.com/pagead/conversion.js",
];
Promise.all(urls.map(u => new Promise(r => {
  const s = document.createElement("script");
  s.onload = s.onerror = () => r();
  s.src = u;
  document.head.appendChild(s);
}))).then(() => done(urls.length));
"""

CLICK_SERVICE_JS = "document.querySelectorAll('.service')[arguments[0]].click();"

ADD_SHORTCUT_JS = """
document.querySelector('#shortcuts .add').click();
const input = document.getElementById('shortcut-url');
input.value = arguments[0];
document.getElementById('shortcut-form').requestSubmit();
"""

CHROME_JS = """
const {MimirStats} = ChromeUtils.importESModule("resource:///modules/MimirStats.sys.mjs");
return {
  stats: MimirStats.get(),
  musique: Services.prefs.getStringPref("mimir.start.music.service", ""),
  raccourcis: Services.prefs.getStringPref("mimir.start.shortcuts", ""),
};
"""

failures = []


def check(label, ok, detail=""):
    print(f"  {'ok ' if ok else 'ERR'} {label}" + (f" : {detail}" if detail else ""))
    if not ok:
        failures.append(label)


def wait_port(timeout=90):
    end = time.time() + timeout
    while time.time() < end:
        try:
            socket.create_connection(("127.0.0.1", PORT), 1).close()
            return
        except OSError:
            time.sleep(1)
    raise SystemExit("Marionette ne repond pas")


def shot(client, out, name):
    if out:
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, name + ".png"), "wb") as f:
            f.write(base64.b64decode(client.screenshot()))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else None
    shutil.rmtree(PROFILE, ignore_errors=True)
    os.makedirs(PROFILE)
    proc = subprocess.Popen(
        [FF, "-no-remote", "-headless", "-marionette", "-remote-allow-system-access",
         "-profile", PROFILE, "about:home"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        wait_port()
        client = Marionette(host="127.0.0.1", port=PORT)
        client.start_session()
        client.timeout.script = 60
        time.sleep(3)

        print("[about:home et about:newtab]")
        for url in ("about:home", "about:newtab"):
            client.set_context("content")
            client.navigate(url)
            time.sleep(2)
            info = client.execute_script(PAGE_JS)
            check(f"{url} charge la page Mimir", info["url"] == url and info["services"] == 8, json.dumps(info)[:200])
            check(f"{url} : aucune requete reseau", info["reseau"] == [], str(info["reseau"]))

        print("[etat initial]")
        client.navigate("about:home")
        time.sleep(2)
        info = client.execute_script(PAGE_JS)
        check("aucun service choisi, pas de bouton", info["choisi"] is None and info["ouvrir"] is None)
        check("compteur affiche", "0" in info["stats"], info["stats"])
        shot(client, out, "1-premier-lancement")

        print("[choix du service de musique]")
        client.execute_script(CLICK_SERVICE_JS, script_args=[1])
        time.sleep(1.5)
        info = client.execute_script(PAGE_JS)
        check("YouTube Music choisi", info["choisi"] == "YouTube Music", str(info["choisi"]))
        check("un logo par service", info["logos"] == 8, str(info["logos"]))
        check("bouton ouvrir", info["ouvrir"] == "https://music.youtube.com/", str(info["ouvrir"]))
        check("6 ambiances", info["ambiances"] == 6)
        client.set_context("chrome")
        check("preference enregistree", client.execute_script(CHROME_JS)["musique"] == "youtube-music")
        client.set_context("content")

        print("[raccourcis]")
        client.execute_script(ADD_SHORTCUT_JS, script_args=["wikipedia.org"])
        time.sleep(1.5)
        client.execute_script(ADD_SHORTCUT_JS, script_args=["http://example.com/page"])
        time.sleep(1.5)
        info = client.execute_script(PAGE_JS)
        check("deux raccourcis (http force en https)",
              info["raccourcis"] == ["https://wikipedia.org/", "https://example.com/page"], str(info["raccourcis"]))
        client.execute_script(ADD_SHORTCUT_JS, script_args=["pas une adresse"])
        time.sleep(1)
        check("adresse invalide refusee", len(client.execute_script(PAGE_JS)["raccourcis"]) == 2)

        print("[persistance apres rechargement]")
        client.navigate("about:newtab")
        time.sleep(2.5)
        info = client.execute_script(PAGE_JS)
        check("service et raccourcis retrouves",
              info["choisi"] == "YouTube Music" and len(info["raccourcis"]) == 2, str(info["choisi"]))
        check("logo du raccourci connu (Wikipedia)", info["logos_raccourcis"] == 1, str(info["logos_raccourcis"]))
        shot(client, out, "2-personnalise-sombre")
        client.set_context("chrome")
        client.execute_script("Services.prefs.setIntPref('layout.css.prefers-color-scheme.content-override', 1);")
        client.set_context("content")
        time.sleep(1)
        shot(client, out, "3-personnalise-clair")
        client.set_context("chrome")
        client.execute_script("Services.prefs.clearUserPref('layout.css.prefers-color-scheme.content-override');")
        client.set_context("content")

        print("[compteur de blocages]")
        time.sleep(20)  # uBlock charge ses listes
        client.navigate("https://example.org/")
        time.sleep(1)
        n = client.execute_async_script(BLOCK_JS)
        time.sleep(1)
        client.set_context("chrome")
        res = client.execute_script(CHROME_JS)
        check("requetes bloquees comptees", res["stats"]["total"] >= 3 and res["stats"]["today"] >= 3, str(res["stats"]))
        client.set_context("content")
        client.navigate("about:home")
        time.sleep(7)  # la page se rafraichit toutes les 5 s
        info = client.execute_script(PAGE_JS)
        check("page affiche le compteur", str(res["stats"]["total"]) in info["stats"], info["stats"])
        shot(client, out, "4-avec-compteur")

        print("[ouverture d'un lien]")
        client.execute_script("document.getElementById('music-open').click();")
        end = time.time() + 20
        # YouTube peut rediriger vers consent.youtube.com selon la region.
        while time.time() < end and "youtube.com" not in client.get_url():
            time.sleep(1)
        check("le bouton ouvre le service", "youtube.com" in client.get_url(), client.get_url())
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("\nechecs :", failures or "aucun")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
