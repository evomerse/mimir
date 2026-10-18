#!/usr/bin/env python3
"""Verifie la page de demarrage locale de Mimir (about:home et about:newtab) sur un profil jetable.

Controle l'URL chargee, le contenu, l'absence de requete reseau, et enregistre des captures (clair et sombre).
A executer dans WSL :  ~/ff/venv/bin/python scripts/test-start-page.py [dossier de captures]
"""
import base64
import os
import shutil
import socket
import subprocess
import sys
import time

from marionette_driver.marionette import Marionette

FF = os.path.expanduser("~/ff/esr153/obj-validate/dist/bin/mimir")
PROFILE = os.path.expanduser("~/ff/profile-start-test")
PORT = 2828

PAGE_JS = """
return {
  url: document.documentURI,
  titre: document.title,
  salut: document.getElementById("greeting")?.textContent,
  date: document.getElementById("date")?.textContent,
  cartes: [...document.querySelectorAll(".promises li")].map(li => li.textContent),
  ressources: performance.getEntriesByType("resource").map(e => e.name),
};
"""


def wait_port(timeout=90):
    end = time.time() + timeout
    while time.time() < end:
        try:
            socket.create_connection(("127.0.0.1", PORT), 1).close()
            return
        except OSError:
            time.sleep(1)
    raise SystemExit("Marionette ne repond pas")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else None
    shutil.rmtree(PROFILE, ignore_errors=True)
    os.makedirs(PROFILE)
    proc = subprocess.Popen(
        [FF, "-no-remote", "-headless", "-marionette", "-remote-allow-system-access",
         "-profile", PROFILE, "about:home"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    bad = 0
    try:
        wait_port()
        client = Marionette(host="127.0.0.1", port=PORT)
        client.start_session()
        client.set_context("content")
        time.sleep(3)
        for url in ("about:home", "about:newtab"):
            client.navigate(url)
            time.sleep(2)
            info = client.execute_script(PAGE_JS)
            ok = (
                info["url"] == url
                and info["salut"]
                and len(info["cartes"]) == 3
                and all(r.startswith("chrome://") for r in info["ressources"])
            )
            bad += not ok
            print(f"[{url}] {'ok ' if ok else 'ERR'}")
            for k, v in info.items():
                print(f"  {k}: {v}")
            if out:
                os.makedirs(out, exist_ok=True)
                name = url.replace(":", "-")
                with open(os.path.join(out, f"{name}.png"), "wb") as f:
                    f.write(base64.b64decode(client.screenshot()))
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
