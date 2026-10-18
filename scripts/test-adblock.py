#!/usr/bin/env python3
"""Verifie que l'adblock integre de Mimir est actif et bloque vraiment, y compris en navigation privee.

Lance Mimir en headless sur un profil jetable, le pilote par Marionette et affiche un rapport.
A executer dans WSL :  ~/ff/venv/bin/python scripts/test-adblock.py
(dependance : marionette_driver, dans le venv ~/ff/venv)
"""
import os
import shutil
import socket
import subprocess
import sys
import time

from marionette_driver.errors import UnsupportedOperationException
from marionette_driver.marionette import Marionette

FF = os.environ.get("MIMIR_EXE") or os.path.expanduser("~/ff/esr153/obj-validate/dist/bin/mimir")
PROFILE = os.path.expanduser("~/ff/profile-adblock-test")
UBO_ID = "uBlock0@raymondhill.net"
PORT = 2828

# Une requete vers un domaine publicitaire connu, une requete temoin vers un site normal.
FETCH_JS = """
const [url, done] = [arguments[0], arguments[arguments.length - 1]];
fetch(url, {mode: "no-cors", cache: "no-store"})
  .then(() => done("charge"), (e) => done("bloque (" + e.name + ")"));
"""
# Meme test avec une balise <script> : c'est ce que font les vraies pages publicitaires.
SCRIPT_JS = """
const [url, done] = [arguments[0], arguments[arguments.length - 1]];
const s = document.createElement("script");
const timer = setTimeout(() => done("timeout"), 15000);
s.onload = () => { clearTimeout(timer); done("charge"); };
s.onerror = () => { clearTimeout(timer); done("bloque"); };
s.src = url;
document.head.appendChild(s);
"""

# uBlock remplace certains scripts celebres (adsbygoogle.js, analytics.js) par une version
# neutralisee qui "se charge" : on les garde pour memoire, mais le verdict se lit sur les
# adresses bloquees franchement. "temoin" doit toujours etre "charge".
TARGETS = (
    ("pub (redirigee)", "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"),
    ("pub", "https://ad.doubleclick.net/favicon.ico"),
    ("pub", "https://static.ads-twitter.com/uwt.js"),
    ("pub", "https://securepubads.g.doubleclick.net/pagead/ppub_config"),
    ("traqueur", "https://connect.facebook.net/en_US/fbevents.js"),
    ("traqueur", "https://bat.bing.com/bat.js"),
    ("traqueur", "https://www.googleadservices.com/pagead/conversion.js"),
    ("temoin", "https://example.org/"),
)


def wait_port(timeout=90):
    end = time.time() + timeout
    while time.time() < end:
        try:
            socket.create_connection(("127.0.0.1", PORT), 1).close()
            return
        except OSError:
            time.sleep(1)
    raise SystemExit("Marionette ne repond pas")


def probe(client, label):
    client.navigate("https://example.org/")
    time.sleep(1)
    print(f"[{label}]")
    client.timeout.script = 30
    for name, url in TARGETS:
        by_fetch = client.execute_async_script(FETCH_JS, script_args=[url])
        by_script = client.execute_async_script(SCRIPT_JS, script_args=[url])
        print(f"  fetch: {by_fetch:20s} script: {by_script:8s} {name:16s} {url}")


def main():
    shutil.rmtree(PROFILE, ignore_errors=True)
    os.makedirs(PROFILE)
    proc = subprocess.Popen(
        [FF, "-no-remote", "-headless", "-marionette", "-remote-allow-system-access",
         "-profile", PROFILE, "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        wait_port()
        client = Marionette(host="127.0.0.1", port=PORT)
        client.start_session()

        client.set_context("chrome")
        info = client.execute_script(
            """
            const p = WebExtensionPolicy.getByID(arguments[0]);
            return p && { actif: p.active, prive: p.privateBrowsingAllowed, nom: p.name, version: p.extension?.version };
            """,
            script_args=[UBO_ID],
        )
        print("uBlock Origin :", info)
        print("theme actif   :", client.execute_script("return Services.prefs.getStringPref('extensions.activeThemeID', '?');"))
        print("profil        :", client.execute_script("return Services.dirsvc.get('ProfD', Ci.nsIFile).path;"))

        # laisser uBlock charger ses listes de filtres
        time.sleep(20)

        client.set_context("content")
        probe(client, "fenetre normale")

        client.set_context("chrome")
        handles_before = set(client.window_handles)
        try:
            client.open(type="window", private=True)
        except UnsupportedOperationException:
            # Marionette ne connait que « Firefox » comme nom d'application.
            print("[fenetre privee] non testable (Marionette ne reconnait pas « Mimir »),"
                  " voir « prive » ci-dessus")
        else:
            new = (set(client.window_handles) - handles_before).pop()
            client.switch_to_window(new)
            client.set_context("content")
            probe(client, "fenetre privee")
            client.close_chrome_window()
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    sys.exit(main())
