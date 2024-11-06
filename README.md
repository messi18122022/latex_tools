# plot for latex App - Benutzerhandbuch

**CSV Plotter App** ist eine Anwendung, mit der Sie ganz einfach Diagramme aus CSV-Dateien erstellen, anpassen und exportieren können. Sie können Daten aus verschiedenen Quellen visualisieren und so Ihre Datenanalyse unterstützen, ohne programmieren zu müssen.

## Übersicht

Mit der CSV Plotter App können Sie:

- **CSV-Dateien laden** und im Programm verwalten
- **Datenreihen auswählen und vergleichen** – wählen Sie die Daten, die im Diagramm angezeigt werden sollen
- **Diagrammeinstellungen anpassen** wie Achsenbeschriftungen, Farben, Linienstile und mehr
- **Diagramme als Datei speichern** in verschiedenen Formaten, wie PDF, PNG oder TeX (für LaTeX-Nutzer)
- **Projekte speichern und laden** – Ihre Arbeit bleibt erhalten und kann später fortgesetzt werden

## Installation

Die App erfordert keine spezielle Installation. Doppelklicken Sie einfach auf die Programmdatei oder öffnen Sie das Programm im Terminal.

## Schritt-für-Schritt-Anleitung

### 1. Starten Sie das Programm

Öffnen Sie die Anwendung, um das Hauptfenster zu sehen. Dort finden Sie alle nötigen Bedienelemente zum Laden von Dateien, Anpassen des Diagramms und Speichern der Ergebnisse.

### 2. CSV-Dateien hochladen

- **CSV-Datei auswählen**: Klicken Sie auf den Button „Upload CSV“, um eine oder mehrere CSV-Dateien (Tabellen mit Daten) von Ihrem Computer zu laden.
- **Dateien verwalten**: Nach dem Hochladen sehen Sie die Datei im linken Fensterbereich. Sie können eine Datei durch Auswahl und Klicken auf „Remove Selected File“ wieder entfernen.

### 3. Daten für das Diagramm auswählen

- **Reihen hinzufügen**: Fügen Sie durch Klicken auf „Add Row“ eine neue Datenreihe für das Diagramm hinzu. Für jede Datenreihe können Sie eine Datei und die Spalten auswählen, die auf der X- und Y-Achse angezeigt werden sollen.
- **Reihe anpassen**: Sie können für jede Datenreihe die Farbe, den Linienstil und das Symbol (z. B. Punkte, Kreuze, Kreise) anpassen. Geben Sie außerdem einen Namen ein, der in der Legende des Diagramms angezeigt wird.
- **Reihe entfernen**: Klicken Sie auf „Remove Last Row“, um die zuletzt hinzugefügte Reihe zu entfernen.

### 4. Diagrammeinstellungen anpassen

- **Achsenbeschriftungen und Bereiche**: Geben Sie Beschriftungen für die X- und Y-Achsen ein. Sie können auch Min- und Max-Werte festlegen, um den angezeigten Bereich einzuschränken.
- **Logarithmische Skalen und Invertierung**: Wählen Sie aus, ob eine Achse logarithmisch skaliert oder umgekehrt (invertiert) werden soll.
- **Gitterlinien aktivieren**: Sie können das Gitternetz für das Diagramm aktivieren oder deaktivieren, um den Überblick zu erleichtern.
- **Automatische Trendlinie**: Aktivieren Sie die Option „LinReg“, um eine Trendlinie zu berechnen und eine Korrelation für die Datenreihe anzuzeigen.

### 5. Vorschau anzeigen und Diagramm aktualisieren

- **Plot-Vorschau**: Klicken Sie auf „Plot-Vorschau“, um eine erste Darstellung Ihres Diagramms anzuzeigen.
- **Einstellungen anpassen**: Ändern Sie die Einstellungen nach Bedarf und klicken Sie dann auf „Plot aktualisieren“, um das Diagramm zu aktualisieren.

### 6. Diagramm speichern

- **Als Bild oder PDF exportieren**: Speichern Sie das Diagramm als PNG oder PDF über die Buttons „.png exportieren“ und „.pdf exportieren“.
- **LaTeX-Export**: Für Nutzer von LaTeX kann das Diagramm als `.tex`-Datei gespeichert werden, um es direkt in wissenschaftlichen Dokumenten zu verwenden.
- **Projekt speichern und laden**: Speichern Sie Ihr gesamtes Projekt als `.json`-Datei, sodass Sie später an demselben Diagramm weiterarbeiten können. Zum Laden eines gespeicherten Projekts klicken Sie auf „Projekt laden“ und wählen die `.json`-Datei aus.

## Häufige Fragen

**Was ist eine CSV-Datei?**  
Eine CSV-Datei ist eine einfache Datei, die Daten in einer Tabellenstruktur speichert. Sie können CSV-Dateien aus Programmen wie Excel exportieren oder aus wissenschaftlichen Quellen herunterladen.

**Warum sehe ich nichts auf dem Diagramm?**  
Stellen Sie sicher, dass die ausgewählten Daten sichtbar sind („sichtbar“ im Auswahlfeld) und überprüfen Sie, ob die richtigen Spalten für die X- und Y-Achse ausgewählt wurden.

**Kann ich mehrere Diagramme speichern?**  
Ja, Sie können Projekte speichern und laden, sodass Sie mit verschiedenen Daten und Diagrammen arbeiten können.

**Wofür ist der TeX-Export gedacht?**  
Die `.tex`-Datei ist speziell für Nutzer von LaTeX gedacht und wird in wissenschaftlichen oder technischen Dokumenten verwendet. Wenn Sie LaTeX nicht verwenden, können Sie diese Funktion ignorieren.

Mit der CSV Plotter App können Sie schnell und einfach Ihre Daten visualisieren und als Diagramme speichern – perfekt für Analysen und Berichte!
