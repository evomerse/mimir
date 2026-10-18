#!/usr/bin/env python3
"""Genere les themes integres de Mimir dans overlay/browser/themes/addons/mimir-*.

Chaque theme : manifest.json (couleurs WebExtension), icon.svg, preview.svg.
Palette tiree du logo (bleu -> cyan -> violet). Modifier THEMES puis relancer :
    python3 scripts/make-themes.py
Les themes sont ensuite declares dans la source Firefox par patches/0001-themes-integres.patch.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "overlay" / "browser" / "themes" / "addons"
VERSION = "1.0.0"
ID_SUFFIX = "@mimir.browser"

# fond : base de la fenetre ; barre : barres d'outils ; champ : barre d'adresse ;
# accent : couleur d'accentuation ; texte / texte2 : texte principal / secondaire
THEMES = {
    "nuit": dict(
        name="Mimir Nuit", scheme="dark",
        description="Le thème sombre par défaut : bleu nuit et reflets cyan.",
        fond="#0d1220", barre="#151c2c", champ="#1f2940", popup="#18213a",
        accent="#4f9dff", accent2="#5fd8f0", texte="#e8edf7", texte2="#9aa7c2",
        bord="#2a3552",
    ),
    "aube": dict(
        name="Mimir Aube", scheme="light",
        description="Le thème clair : blanc bleuté et accents azur.",
        fond="#e4eaf7", barre="#f6f8fd", champ="#ffffff", popup="#ffffff",
        accent="#2f6fe4", accent2="#19a7c9", texte="#14203a", texte2="#56627d",
        bord="#c9d3e6",
    ),
    "aurore": dict(
        name="Mimir Aurore", scheme="dark",
        description="Un thème sombre aux nuances violettes.",
        fond="#120d24", barre="#1b1433", champ="#281d4a", popup="#231a41",
        accent="#9a6bff", accent2="#d27bff", texte="#efe9ff", texte2="#a99bcf",
        bord="#38295f",
    ),
    "lagune": dict(
        name="Mimir Lagune", scheme="dark",
        description="Un thème sombre vert d'eau, pour changer du bleu.",
        fond="#08171a", barre="#0f2226", champ="#17343a", popup="#12292e",
        accent="#2fd4c0", accent2="#6be38f", texte="#e4f6f3", texte2="#8fb3ad",
        bord="#1f4249",
    ),
}

HEADER = (
    "<!-- This Source Code Form is subject to the terms of the Mozilla Public\n"
    "   - License, v. 2.0. If a copy of the MPL was not distributed with this\n"
    "   - file, You can obtain one at http://mozilla.org/MPL/2.0/. -->\n"
)


def colors_of(t: dict) -> dict:
    return {
        "frame": t["fond"],
        "frame_inactive": t["fond"],
        "toolbar": t["barre"],
        "toolbar_text": t["texte"],
        "toolbar_vertical_separator": t["bord"],
        "toolbar_top_separator": "transparent",
        "toolbar_bottom_separator": t["bord"],
        "toolbar_field": t["champ"],
        "toolbar_field_text": t["texte"],
        "toolbar_field_border": "transparent",
        "toolbar_field_focus": t["champ"],
        "toolbar_field_text_focus": t["texte"],
        "toolbar_field_border_focus": t["accent"],
        "toolbar_field_highlight": t["accent"] + "55",
        "toolbar_field_highlight_text": t["texte"],
        "button_background_hover": t["texte"] + "14",
        "button_background_active": t["texte"] + "26",
        "icons": t["texte2"],
        "icons_attention": t["accent2"],
        "bookmark_text": t["texte"],
        "tab_text": t["texte"],
        "tab_background_text": t["texte2"],
        "tab_selected": t["barre"],
        "tab_line": t["accent"],
        "tab_loading": t["accent"],
        "tab_background_separator": "transparent",
        "ntp_background": t["fond"],
        "ntp_text": t["texte"],
        "popup": t["popup"],
        "popup_text": t["texte"],
        "popup_border": t["bord"],
        "popup_highlight": t["accent"] + "33",
        "popup_highlight_text": t["texte"],
        "sidebar": t["barre"],
        "sidebar_text": t["texte"],
        "sidebar_border": t["bord"],
        "sidebar_highlight": t["accent"],
        "sidebar_highlight_text": "#ffffff",
        "focus_outline": t["accent"],
    }


def manifest(key: str, t: dict) -> dict:
    return {
        "manifest_version": 2,
        "browser_specific_settings": {"gecko": {"id": f"mimir-{key}{ID_SUFFIX}"}},
        "name": t["name"],
        "description": t["description"],
        "author": "Mimir",
        "version": VERSION,
        "icons": {"32": "icon.svg"},
        "theme": {
            "properties": {"color_scheme": t["scheme"]},
            "colors": colors_of(t),
        },
    }


def icon(t: dict) -> str:
    return HEADER + (
        '<svg width="63" height="62" viewBox="0 0 63 62" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
        '  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">\n'
        f'    <stop offset="0" stop-color="{t["accent2"]}"/><stop offset="1" stop-color="{t["accent"]}"/>\n'
        "  </linearGradient></defs>\n"
        f'  <circle cx="31.5" cy="31" r="31" fill="{t["fond"]}"/>\n'
        '  <circle cx="31.5" cy="31" r="22" fill="url(#g)"/>\n'
        "</svg>\n"
    )


def preview(t: dict) -> str:
    return HEADER + (
        '<svg width="680" height="92" viewBox="0 0 680 92" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
        f'  <rect width="680" height="92" fill="{t["fond"]}"/>\n'
        f'  <rect x="28" y="5" width="166" height="34" rx="9" fill="{t["barre"]}"/>\n'
        f'  <rect x="51" y="20" width="121" height="4" rx="2" fill="{t["texte"]}"/>\n'
        f'  <rect x="28" y="36" width="166" height="3" rx="1.5" fill="{t["accent"]}"/>\n'
        f'  <rect x="221" y="20" width="121" height="4" rx="2" fill="{t["texte2"]}"/>\n'
        f'  <rect y="44" width="680" height="48" fill="{t["barre"]}"/>\n'
        f'  <circle cx="24" cy="68" r="6" stroke="{t["texte2"]}" stroke-width="1.5"/>\n'
        f'  <circle cx="54" cy="68" r="6" stroke="{t["texte2"]}" stroke-width="1.5"/>\n'
        f'  <rect x="82" y="55" width="440" height="26" rx="13" fill="{t["champ"]}"/>\n'
        f'  <rect x="104" y="66" width="160" height="4" rx="2" fill="{t["texte2"]}"/>\n'
        f'  <circle cx="562" cy="68" r="7" fill="{t["accent"]}"/>\n'
        f'  <circle cx="592" cy="68" r="7" fill="{t["accent2"]}"/>\n'
        "</svg>\n"
    )


def main() -> None:
    for key, t in THEMES.items():
        d = OUT / f"mimir-{key}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "manifest.json").write_text(
            json.dumps(manifest(key, t), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (d / "icon.svg").write_text(icon(t), encoding="utf-8")
        (d / "preview.svg").write_text(preview(t), encoding="utf-8")
        print("OK", d.relative_to(OUT.parent.parent.parent.parent))


if __name__ == "__main__":
    main()
