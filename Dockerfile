# Stop Motion (Eagle Animation) — Auslieferung als fertiges Abbild
#
# Gebaut wird aus dem festgeschriebenen Quelltext-Abzug des Originals (FASSUNG
# unten). Die einzige Änderung am Original ist das Abschalten der Analyse —
# scripts/anpassen.py prüft den Anker und bricht bei Abweichung ab.
#
# Zwei Stufen wie in der Hausordnung: bauen (Node), ausliefern (nginx).
# Zur Laufzeit ruft das Werkzeug keine fremde Adresse auf: keine Analyse,
# keine Schriftarten von fremden Servern, keine Inhalte von fremden Ablagen.

FROM node:22-alpine AS bau

# Festgeschriebener Stand: master, Version 2.19.0 (2026-10-06).
ARG QUELLE=https://github.com/brick-a-brack/eagle-animation/archive/8624b035ca5951d28cfceaf89931141cb3e1aac9.tar.gz
ARG FASSUNG=8624b035ca5951d28cfceaf89931141cb3e1aac9

WORKDIR /src
RUN apk add --no-cache curl tar python3 \
 && curl -fsSL "$QUELLE" | tar xz -C /src --strip-components=1

# Änderungen am Original — mit Ankerprüfung, bricht bei Abweichung ab.
COPY scripts/anpassen.py /anpassen.py
RUN python3 /anpassen.py /src

# Fassungskennung im Bündel; sie erscheint in der Oberfläche (z. B. "web-8624b03").
RUN printf 'VITE_COMMIT_HASH=%s\n' "$FASSUNG" > .env

ENV CI=1
# Die Nachinstallationsschritte des Projekts laden Electron (~150 MB) und
# werden für die Web-Fassung nicht gebraucht — deshalb --ignore-scripts.
RUN npm ci --ignore-scripts --no-audit --no-fund \
 || npm install --ignore-scripts --no-audit --no-fund

RUN npm run build:web \
 && test -s out/web/index.html \
 && test -s out/web/sw.js \
 && test -s out/web/i18n/de.json \
 && echo "--- Buendelgroesse:" && du -sh out/web \
 && echo "--- Analyse-Kennung im Buendel (erwartet: keine):" \
 && (grep -rl 'phc_' out/web/ || echo "keine gefunden")

FROM nginx:alpine-slim
COPY --from=bau /src/out/web/ /usr/share/nginx/html/
COPY config/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
