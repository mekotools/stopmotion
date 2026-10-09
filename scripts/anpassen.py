# Anpassungen am festgeschriebenen Quelltext von Eagle Animation.
#
# Aufruf: python3 anpassen.py <quellverzeichnis>
#
# Drei Änderungen, jede mit Ankerprüfung. Passt ein Anker nicht mehr, bricht
# dieses Skript ab, damit kein unbemerkt verändertes Original ausgeliefert
# wird. Ist eine Änderung schon upstream erledigt (Zieltext vorhanden, Alttext
# weg), wird das gemeldet und weitergemacht — eine rein sprachliche Korrektur
# soll den Bau nicht anhalten.
#
# 1. Analyse abschalten. Das Projekt selbst beschreibt den Weg in seiner README
#    (Abschnitt "Telemetry"): POSTHOG_TOKEN in src/config.js leeren. Mit leerer
#    Kennung läuft posthog.init() nie, der Anbieter wird nicht angesprochen.
# 2. Vier deutsche Beschriftungen der Startseite groß schreiben. Sie stehen im
#    Original klein ("projekte", "fotos", "der animation", "favoriten"), was im
#    Deutschen falsch ist; die Zahlen davor bleiben unberührt.
# 3. Die Sprachkennung des Dokuments beim Start setzen. Das Original setzt
#    <html lang> erst, wenn die Sprache in den Einstellungen gewechselt wird;
#    bis dahin steht bei deutscher Oberfläche "en" im Dokument, was
#    Vorlesehilfen in die falsche Sprache führt.

import pathlib
import sys

DEUTSCHE_BESCHRIFTUNGEN = [
    ('"projects": "projekte"', '"projects": "Projekte"'),
    ('"photos": "fotos"', '"photos": "Fotos"'),
    ('"of animation": "der animation"', '"of animation": "der Animation"'),
    ('"starred": "favoriten"', '"starred": "Favoriten"'),
]

SPRACHKENNUNG = (
    "\n// MekoTools: Sprachkennung des Dokuments gleich beim Start setzen,\n"
    "// damit Vorlesehilfen die richtige Sprache bekommen.\n"
    "document.documentElement.setAttribute('lang', currentLanguage());\n"
)


def pruefe(pfad):
    if not pfad.is_file():
        print("FEHLER: %s fehlt - der Quelltext hat sich geaendert." % pfad)
        sys.exit(1)


def analyse_abschalten(wurzel):
    config = wurzel / "src" / "config.js"
    pruefe(config)
    text = config.read_text(encoding="utf8")
    alt = "export const POSTHOG_TOKEN = '';"
    if alt in text:
        print("1) Analyse: bereits leer - nichts zu tun.")
        return
    zeilen = [z for z in text.splitlines() if z.startswith("export const POSTHOG_TOKEN = ")]
    if len(zeilen) != 1:
        print("FEHLER: POSTHOG_TOKEN-Zeile %d-mal gefunden (erwartet: genau 1)." % len(zeilen))
        print("Der Quelltext hat sich geaendert - die Aenderung am Original nachziehen.")
        sys.exit(1)
    config.write_text(text.replace(zeilen[0], alt), encoding="utf8")
    neu = config.read_text(encoding="utf8")
    if "phc_" in neu:
        print("FEHLER: es steht noch eine Kennung in src/config.js.")
        sys.exit(1)
    print("1) Analyse abgeschaltet: %s" % alt)


def deutsche_beschriftungen(wurzel):
    datei = wurzel / "resources" / "i18n" / "de.json"
    pruefe(datei)
    text = datei.read_text(encoding="utf8")
    offen = 0
    for alt, neu in DEUTSCHE_BESCHRIFTUNGEN:
        if neu in text and alt not in text:
            print("2) %s: schon korrigiert - nichts zu tun." % alt.split(":")[0].strip('"'))
            continue
        if text.count(alt) != 1:
            print("FEHLER: %r %d-mal gefunden (erwartet: genau 1)." % (alt, text.count(alt)))
            print("Der Quelltext hat sich geaendert - die Aenderung am Original nachziehen.")
            sys.exit(1)
        text = text.replace(alt, neu)
        offen += 1
        print("2) korrigiert: %s" % neu)
    datei.write_text(text, encoding="utf8")
    print("2) deutsche Beschriftungen: %d von %d korrigiert." % (offen, len(DEUTSCHE_BESCHRIFTUNGEN)))


def sprachkennung_setzen(wurzel):
    datei = wurzel / "src" / "renderer" / "i18n.js"
    pruefe(datei)
    text = datei.read_text(encoding="utf8")
    # Achtung: setLanguage() setzt die Kennung bereits beim Sprachwechsel.
    # Hier geht es um den Startzustand - deshalb genau auf diese Zeile prüfen.
    if "setAttribute('lang', currentLanguage())" in text:
        print("3) Sprachkennung beim Start: schon vorhanden - nichts zu tun.")
        return
    if "export const currentLanguage" not in text:
        print("FEHLER: currentLanguage() steht nicht mehr in src/renderer/i18n.js.")
        sys.exit(1)
    if not text.endswith("\n"):
        text += "\n"
    datei.write_text(text + SPRACHKENNUNG, encoding="utf8")
    neu = datei.read_text(encoding="utf8")
    if "setAttribute('lang', currentLanguage())" not in neu:
        print("FEHLER: die Sprachkennung wurde nicht gesetzt.")
        sys.exit(1)
    print("3) Sprachkennung beim Start gesetzt (currentLanguage()).")


def main():
    if len(sys.argv) != 2:
        print("Aufruf: anpassen.py <quellverzeichnis>")
        return 2
    wurzel = pathlib.Path(sys.argv[1])
    if not (wurzel / "package.json").is_file():
        print("FEHLER: %s sieht nicht nach dem Quellbaum aus (package.json fehlt)." % wurzel)
        return 1
    analyse_abschalten(wurzel)
    deutsche_beschriftungen(wurzel)
    sprachkennung_setzen(wurzel)
    print("Anpassungen fertig.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
