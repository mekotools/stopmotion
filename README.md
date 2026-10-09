# Stop Motion — MekoTools

Fertiges Abbild der Web-Fassung von **Eagle Animation** für den MekoTools-Katalog.

- **Werkzeug im Katalog:** <https://stopmotion.mekotools.de>
- **Original:** Eagle Animation, Brick à Brack — <https://eagle-animation.com>
- **Quelltext des Originals:** <https://github.com/brick-a-brack/eagle-animation>
- **Lizenz des Originals:** GPL-3.0 (die `LICENSE`-Datei im Quellbaum wurde
  gelesen, nicht die Kennung der Plattform geglaubt)

## Was dieses Repo enthält

| Datei | Zweck |
|---|---|
| `Dockerfile` | baut die Web-Fassung aus dem festgeschriebenen Quelltext-Abzug |
| `scripts/anpassen.py` | die Änderungen am Original, jede mit Ankerprüfung |
| `config/default.conf` | nginx-Regeln (eine Seite, Zwischenspeicher, CSP) |
| `.github/workflows/abbild-bauen.yml` | baut und schiebt `ghcr.io/mekotools/stopmotion` |
| `tool.yaml` | Katalogeintrag (Schema im Katalog-Repo) |
| `docs/` | Anleitung, Didaktik, Unterrichtsentwurf |

## Festgeschriebener Stand

Gebaut wird aus dem Archiv-Abzug des Originals, nicht aus einer Zweigspitze:

- Zweig `master` (dort liegen die Veröffentlichungen), Fassung **2.19.0**
- Kennung `8624b035ca5951d28cfceaf89931141cb3e1aac9` (2026-10-06)

Beim Nachziehen einer neuen Fassung: Kennung im `Dockerfile` an beiden Stellen
(`QUELLE`, `FASSUNG`) ändern, Bau laufen lassen, Werkzeugseite und
Katalogeintrag mit dem neuen Prüfdatum versehen.

## Änderungen gegenüber dem Original

Es gibt genau **eine** inhaltliche Änderung:

1. **Analyse abgeschaltet.** In `src/config.js` wird die PostHog-Kennung auf
   einen leeren Wert gesetzt. Damit läuft `posthog.init()` nie, und die
   Oberfläche spricht `us.i.posthog.com` nicht an. Das Projekt selbst
   beschreibt diesen Weg in seiner README (Abschnitt „Telemetry").
   Die Ankerprüfung in `scripts/anpassen.py` bricht ab, wenn die Zeile nicht
   mehr genau einmal gefunden wird — so kann kein unbemerkt veränderter
   Quelltext ausgeliefert werden.

**Sonst nichts.** Insbesondere wurde die deutsche Sprachdatei nicht angefasst:
alle im Programm benutzten Beschriftungen haben eine deutsche Fassung. Die acht
Schlüssel, die nur im englischen Bestand stehen, werden an keiner Stelle im
Quelltext verwendet (geprüft) und brauchen keine Übersetzung.

Der Name des Programms bleibt stehen (Titel, Logo, Fußzeile): wir liefern das
Original aus, keine umbenannte Kopie. Der Hinweis auf das Original ist Teil der
GPL-Pflicht und der Ehrlichkeit gegenüber den Machern.

## Keine Fremdaufrufe zur Laufzeit

Geprüft im Quelltext (nicht in der Beschreibung):

- **Analyse:** siehe oben, abgeschaltet.
- **Partnerschnittstelle** `api.brickfilms.com`: im Quelltext nur als
  Voreinstellung der „Workshop"-Funktionen vorhanden; sie wird nur benutzt,
  wenn diese Funktion eingeschaltet ist (Vorgabe: aus) **und** die Fähigkeit
  `BACKGROUND_SYNC` vorhanden ist. Die Web-Fassung kennt diese Fähigkeit nicht
  (`src/backend-web/actions/index.js`, `APP_CAPABILITIES`) — die Felder
  erscheinen in den Einstellungen also gar nicht.
- **Schriftarten und Symbole** kommen aus dem eigenen Paket.
- **Die Kamera** wird über den Browser angesprochen (`getUserMedia`); der
  „Toucan Camera Server" des Originals wird im Browser nur benutzt, wenn die
  Adresse beim Bau mitgegeben wird — wir geben keine mit.
- `config/default.conf` setzt zusätzlich eine Kopfzeile
  `Content-Security-Policy` mit `connect-src 'self'`, die Fremdaufrufe
  verbietet. Das ist am ausgelieferten Werkzeug nachprüfbar.

## Bauen und ausrollen

```sh
# Bau (lokal, nur zur Prüfung der Bauvorschrift):
docker build -t stopmotion:test .

# In der CI: Push auf main im GitHub-Repo (github.com/mekotools/stopmotion)
# oder von Hand anstoßen (workflow_dispatch) -> ghcr.io/mekotools/stopmotion

# Auf flip (Haushost):
#   /poolio/docker/mekotools-stopmotion/docker-compose.yml
#   docker compose up -d --pull always
```

Auf dem Zielhost wird **nicht** gebaut; dort läuft nur das Abbild.

## Wo die Daten der Nutzenden liegen

Alles bleibt im Browser: Die Anwendung legt Projekte und Bilder in einer
Datenbank im Browser ab (IndexedDB) und bedient die Bildabfragen über einen
Service Worker. Es gibt keinen Serveranteil, keine Anmeldung und keine
Übertragung von Aufnahmen. Folge für den Unterricht: ein Projekt liegt auf
einem Gerät in einem Browserprofil — exportieren ist das Sichern.

## Herkunft und Danksagung

- Programm: Eagle Animation von Brick à Brack (GPL-3.0), Quelltext über den
  Forge-Host des Projekts.
- Das Logo stammt von Nishant Shukla, die Klangdateien aus
  <https://zapsplat.com/> (Angaben aus der README des Originals). Sie werden
  unverändert mit dem Programm ausgeliefert, wie im Original.
