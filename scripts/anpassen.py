# Anpassungen am festgeschriebenen Quelltext von Eagle Animation.
#
# Aufruf: python3 anpassen.py <quellverzeichnis>
#
# Es gibt genau eine Änderung: die Analyse wird abgeschaltet. Der Quelltext
# wird an der Stelle geprüft — passt der Anker nicht mehr, bricht dieses
# Skript ab, damit kein unbemerkt verändertes Original ausgeliefert wird.
#
# Warum das der richtige Weg ist: das Projekt selbst beschreibt ihn in seiner
# README (Abschnitt "Telemetry") — POSTHOG_TOKEN in src/config.js auf einen
# leeren Wert setzen und neu bauen. Mit leerer Kennung läuft posthog.init()
# nie, die Oberfläche spricht den Anbieter also nicht an.

import pathlib
import re
import sys


def main():
    if len(sys.argv) != 2:
        print("Aufruf: anpassen.py <quellverzeichnis>")
        return 2

    wurzel = pathlib.Path(sys.argv[1])
    config = wurzel / "src" / "config.js"
    if not config.is_file():
        print("FEHLER: %s fehlt - der Quelltext hat sich geaendert." % config)
        return 1

    text = config.read_text(encoding="utf8")
    muster = re.compile(r"export const POSTHOG_TOKEN = '[^']*';")
    treffer = muster.findall(text)
    if len(treffer) != 1:
        print("FEHLER: POSTHOG_TOKEN-Zeile %d-mal gefunden (erwartet: genau 1)." % len(treffer))
        print("Der Quelltext hat sich geaendert - die Aenderung am Original nachziehen.")
        return 1

    neu = muster.sub("export const POSTHOG_TOKEN = '';", text)
    config.write_text(neu, encoding="utf8")

    if "phc_" in neu:
        print("FEHLER: es steht noch eine Kennung in src/config.js.")
        return 1

    zeile = [z.strip() for z in neu.splitlines() if "POSTHOG_TOKEN" in z]
    print("Analyse abgeschaltet: " + " | ".join(zeile))
    print("Kontrolle: %d leere Kennung, 0 gefuellte." % neu.count("POSTHOG_TOKEN = ''"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
