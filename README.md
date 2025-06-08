# KBI-Rechner

Dieses Repository beinhaltet die vom ursprünglichen CustomTkinter-Programm extrahierte Logik. Die Berechnungen rund um Münzen, Scheine und Berichte sind nun unabhängig von einer GUI implementiert und können über eine Flask API angesprochen werden.

## Projektstruktur

```
logic/
    calculation.py  - Kernberechnungen (z.B. Gewichts‐zu‐Wert Umrechnung)
    models.py       - Datenstrukturen für Münzen und Scheine
    report.py       - Funktionen für Berichte und Wechselgeldberechnung
app.py             - Einstiegspunkt der Flask API
```

## Nutzung

Die Flask-Anwendung kann lokal gestartet werden:

```bash
python app.py
```

Danach ist die Weboberfläche unter `http://localhost:5000/` erreichbar.
Die Seite nutzt Bootstrap 5 und kommuniziert per Fetch-API mit dem
Endpunkt `/calculate`.

Die weiteren Module können separat in eigenen Skripten importiert und verwendet werden.

## API-Endpunkte

### `POST /calculate`

JSON-Eingabe::

```json
{
  "coin_value": float,
  "measured_weight": float,
  "tare_weight": float
}
```

Antwort::

```json
{
  "calculated_value": float,
  "coin_count": int
}
```

## Weboberfläche

Unter `http://localhost:5000/` wird ein kleines Formular bereitgestellt,
mit dem sich der Münzwert bequem berechnen lässt. Die Seite ist
responsiv aufgebaut und nutzt Bootstrap 5. Die Berechnung erfolgt per
Fetch-Aufruf an den Endpunkt `/calculate`.

## Deployment Guide

Folgende Schritte richten den Dienst auf einem Ubuntu 22.04 Server ein.

1. Kopiere das Repository auf den Server und wechsle in das Projektverzeichnis.
2. Führe das bereitgestellte Skript `deploy.sh` aus:
   ```bash
   ./deploy.sh
   ```
   Das Skript erstellt eine Python-Umgebung, installiert die Abhängigkeiten
   und legt die systemd‑Unit `kbi-rechner.service` an.
3. Nach erfolgreicher Ausführung lauscht der Gunicorn‑Server auf Port 5000.
4. Für den Reverse Proxy kann folgende Beispiel-Konfiguration in nginx
   eingebunden werden:
   ```nginx
   include /path/to/project/nginx.conf;
   ```

Die Anwendung läuft im Produktionsmodus (`FLASK_ENV=production`). Änderungen
an den Quellen benötigen einen Neustart des Dienstes:

```bash
sudo systemctl restart kbi-rechner.service
```


## Deployment für Märkischer Hofladen

Die Anwendung kann unter dem Benutzer `hofladen` betrieben werden. Das Projekt liegt in
`/home/hofladen/maerkischerhofladen/`.

1. Wechsle in das Verzeichnis und führe das Skript `deploy-hofladen.sh` aus:
   ```bash
   ./deploy-hofladen.sh
   ```
   Das Skript erstellt eine virtuelle Umgebung, installiert die Abhängigkeiten
   inklusive `gunicorn` und legt die systemd-Unit `maerkischerhofladen.service`
   an.
2. Nach dem Start lauscht Gunicorn auf Port `5001`.
3. Für den Reverse Proxy kann folgende nginx-Konfiguration genutzt werden:
   ```nginx
   include /home/hofladen/maerkischerhofladen/maerkischerhofladen.conf;
   ```

Ein Neustart des Dienstes ist nach Änderungen an den Quellen nötig:
```bash
sudo systemctl restart maerkischerhofladen.service
```

## SSL Setup

Um HTTPS für die Domain maerkischerhofladen.de zu aktivieren, kann das Skript
`enable-ssl-hofladen.sh` genutzt werden. Es installiert bei Bedarf Certbot, legt
ein Backup der vorhandenen nginx-Konfiguration an und richtet anschließend das
Zertifikat sowie einen automatischen Redirect von HTTP auf HTTPS ein. Zusätzlich
wird eine sichere Mozilla-Konfiguration eingebunden.

Ausführen auf dem Server:

```bash
./enable-ssl-hofladen.sh
```

Das Skript erstellt auch eine Diffie-Hellman-Datei und legt
`/etc/nginx/snippets/ssl-params.conf` mit den empfohlenen TLS-Optionen an.
Nach erfolgreichem Zertifikatserwerb wird nginx neu geladen.
