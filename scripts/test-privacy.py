#!/usr/bin/env python3
"""Verifie les engagements de vie privee du build Mimir sur un profil jetable.

 1. fonctions retirees a la compilation (AppConstants) et prefs effectives ;
 2. hotes contactes par le navigateur seul pendant ~45 s (journal nsHttp), sans aucune navigation.

A executer dans WSL :  ~/ff/venv/bin/python scripts/test-privacy.py
"""
import os
import re
import shutil
import socket
import subprocess
import sys
import time

from marionette_driver.marionette import Marionette

FF = os.path.expanduser("~/ff/esr153/obj-validate/dist/bin/mimir")
PROFILE = os.path.expanduser("~/ff/profile-privacy-test")
LOG = os.path.expanduser("~/ff/privacy-http.log")
PORT = 2828
IDLE = 45

# pref -> valeur attendue
PREFS = {
    "datareporting.healthreport.uploadEnabled": False,
    "datareporting.policy.dataSubmissionEnabled": False,
    "datareporting.usage.uploadEnabled": False,
    "toolkit.telemetry.enabled": False,
    "toolkit.telemetry.unified": False,
    "toolkit.telemetry.archive.enabled": False,
    "app.shield.optoutstudies.enabled": False,
    "app.normandy.enabled": False,
    "browser.urlbar.quicksuggest.enabled": False,
    "identity.fxaccounts.enabled": False,
    "network.captive-portal-service.enabled": False,
    "network.connectivity-service.enabled": False,
    "browser.region.update.enabled": False,
    "privacy.fingerprintingProtection": True,
}
# constantes de compilation attendues a faux
CONSTANTS = ("MOZ_TELEMETRY_REPORTING", "MOZ_SERVICES_HEALTHREPORT", "MOZ_NORMANDY", "MOZ_CRASHREPORTER", "MOZ_UPDATER")

JS = """
const out = {consts: {}, prefs: {}};
const {AppConstants} = ChromeUtils.importESModule("resource://gre/modules/AppConstants.sys.mjs");
for (const k of arguments[0]) out.consts[k] = AppConstants[k];
for (const k of arguments[1]) {
  const t = Services.prefs.getPrefType(k);
  out.prefs[k] = t == Services.prefs.PREF_BOOL ? Services.prefs.getBoolPref(k) : "(absente)";
}
return out;
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
    shutil.rmtree(PROFILE, ignore_errors=True)
    os.makedirs(PROFILE)
    if os.path.exists(LOG):
        os.remove(LOG)
    env = dict(os.environ, MOZ_LOG="nsHttp:3,timestamp", MOZ_LOG_FILE=LOG)
    proc = subprocess.Popen(
        [FF, "-no-remote", "-headless", "-marionette", "-remote-allow-system-access",
         "-profile", PROFILE, "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env,
    )
    bad = 0
    try:
        wait_port()
        client = Marionette(host="127.0.0.1", port=PORT)
        client.start_session()
        client.set_context("chrome")
        res = client.execute_script(JS, script_args=[list(CONSTANTS), list(PREFS)])

        print("[constantes de compilation]")
        for k, v in res["consts"].items():
            ok = not v
            bad += not ok
            print(f"  {'ok ' if ok else 'ERR'} {k} = {v}")
        print("[preferences effectives]")
        for k, want in PREFS.items():
            got = res["prefs"][k]
            ok = got == want
            bad += not ok
            print(f"  {'ok ' if ok else 'ERR'} {k} = {got}")

        print(f"[attente {IDLE} s sans navigation]")
        time.sleep(IDLE)
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()

    hosts = {}
    for name in sorted(os.listdir(os.path.dirname(LOG))):
        if not name.startswith(os.path.basename(LOG)):
            continue
        with open(os.path.join(os.path.dirname(LOG), name), errors="replace") as f:
            for line in f:
                for m in re.finditer(r"https?://([A-Za-z0-9.-]+)", line):
                    hosts[m.group(1)] = hosts.get(m.group(1), 0) + 1
    print("[hotes apparus dans le journal HTTP]")
    for h, n in sorted(hosts.items()):
        print(f"  {n:4d}  {h}")
    if not hosts:
        print("  (aucun)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
