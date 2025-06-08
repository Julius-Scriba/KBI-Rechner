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
