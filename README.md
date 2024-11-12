## Einrichten in Windows
### 1. Visual Studio Code (VSCode) installieren:
1. Drücke [hier](https://code.visualstudio.com/Download)
2. **Klicke auf:** "Download for Windows".
3. **Öffne die Datei:** Doppelklick auf die heruntergeladene Datei.
4. **Akzeptiere** alle Standardoptionen und klicke immer auf **"Weiter"**, dann auf **"Installieren"**.
5. **Warte,** bis die Installation abgeschlossen ist, und öffne anschließend Visual Studio Code.

### 2. Python in Visual Studio Code installieren (über den Microsoft Store):
1. **Öffne Visual Studio Code.**
2. **Installiere die Python-Erweiterung:**
   - Klicke links auf das **Puzzle-Symbol (Erweiterungen)**.
   - **Suche nach "Python"** und klicke auf **"Installieren"** bei der Erweiterung von Microsoft.
3. **Python-Datei erstellen:**
   - Klicke auf "File" → "New File".
   - Speichere die Datei als `test.py`.
4. **Python aus dem Microsoft Store installieren:**
   - Schreibe z. B. `print("Hallo, Welt!")` in die Datei.
   - **Rechtsklick** in die Datei und wähle **"Run Python File"**.
   - Visual Studio Code erkennt, dass Python fehlt, und bietet an, **Python aus dem Microsoft Store** zu installieren.
   - **Klicke auf "Install"**, und folge den Anweisungen, um Python aus dem Store zu installieren.
### 3. Git einrichten, um immer auf die neueste Version zugreifen zu können
1. **Git installieren**:
   - Lade Git von [hier](https://git-scm.com/downloads/win) herunter und installiere es (immer auf „Weiter“ klicken).

2. **GitHub-Repository klonen**:
   - **Git Bash öffnen**: Drücke die **Windows-Taste**, suche nach „Git Bash“ und öffne das Programm.
   - **Zum Ordner wechseln, wo du die Verknüpfung speichern willst**:
     - Kopiere diesen Befehl, füge ihn in Git Bash ein und drücke **Enter**:
       ```bash
       cd /Pfad/zum/Ordner
       ```
     - Ersetze `/Pfad/zum/Ordner` durch den Ordner, in dem du die Dateien haben willst (z. B. `C:/Benutzer/DeinName/Downloads`).
   - **Repository klonen**:
     - Kopiere diesen Befehl, füge ihn in Git Bash ein und drücke **Enter**:
       ```bash
       git clone https://github.com/messi18122022/latex_tools.git
       ```
## 4. Latex installieren
Lade [Latex](https://miktex.org/download) (die Programmiersprache) runter, sonst geht der Plotter NICHT.

## 5. In VSCode das Programm öffnen und benutzen
1. Öffne **VSCode** und gehe zu „Datei > Ordner öffnen“. Wähle den Ordner `latex_tools` aus.
2. Öffne links beim Ordnersymbol die Ansicht für die Dateien
3. Öffne PlotGOAT.py
4. **Öffne ein neues Terminal** oben in der Leiste auf `Terminal` drücken, und `Neues Terminal` klicken
5. Gib im Terminal von VSCode folgenden befehl ein und drücke Enter:
```bash
pip3 install pandas matplotlib numpy scipy seaborn
```
6. **Um immer die neuesten Updates zu bekommen:** Jedes mal kurz im Terminal ausführen, um die neueste Version der App runterzuladen:
   ```bash
     git pull
     ```
7. Python Skript ausführen (oben rechts)

Damit ist die Einrichtung abgeschlossen.

---
## Einrichten in macOS
### 1. Visual Studio Code (VSCode) installieren:
1. Drücke [hier](https://code.visualstudio.com/Download)
2. **Klicke auf:** "Download for Mac".
3. **Akzeptiere** alle Standardoptionen und klicke immer auf **"Weiter"**, dann auf **"Installieren"**.
4. **Warte,** bis die Installation abgeschlossen ist, und öffne anschließend Visual Studio Code.

### 2. Python in Visual Studio Code installieren (über den Microsoft Store):
1. **Öffne Visual Studio Code.**
2. **Installiere die Python-Erweiterung:**
   - Klicke links auf das **Puzzle-Symbol (Erweiterungen)**.
   - **Suche nach "Python"** und klicke auf **"Installieren"** bei der Erweiterung von Microsoft.
3. **Python-Datei erstellen:**
   - Klicke auf "File" → "New File".
   - Speichere die Datei als `test.py`.
4. **Python aus dem Microsoft Store installieren:**
   - Schreibe z. B. `print("Hallo, Welt!")` in die Datei.
   - **Rechtsklick** in die Datei und wähle **"Run Python File"**.
   - Visual Studio Code erkennt, dass Python fehlt, und bietet an, **Python aus dem Microsoft Store** zu installieren.
   - **Klicke auf "Install"**, und folge den Anweisungen, um Python aus dem Store zu installieren.
### 3. Git einrichten, um immer auf die neueste Version zugreifen zu können
1. **Git installieren**:
   - **Überprüfen, es sollte schon installiert sein**:
     - Öffne das **Terminal** (über die Lupe rechts oben in macOS) und kopiere diesen Befehl, drücke dann **Enter**:
       ```bash
       git --version
       ```
       Wenn du eine Version siehst, ist alles gut. Sonst musst du es noch installieren.
2. **GitHub-Repository klonen**:
   - **Terminal öffnen** und zum Ordner wechseln, wo du die Verknüpfung speichern willst:
     - Kopiere diesen Befehl, füge ihn ins Terminal ein und drücke **Enter**:
       ```bash
       cd /Pfad/zum/Ordner
       ```
     - Ersetze `/Pfad/zum/Ordner` durch den Pfad deines Ordners.
   - **Repository klonen**:
     - Kopiere diesen Befehl, füge ihn ins Terminal ein und drücke **Enter**:
       ```bash
       git clone https://github.com/messi18122022/latex_tools.git
       ```
## 4. Latex installieren
Lade [Latex](https://miktex.org/download) (die Programmiersprache) runter, sonst geht der Plotter NICHT.

## 5. In VSCode das Programm öffnen und benutzen
1. Öffne **VSCode** und gehe zu „Datei > Ordner öffnen“. Wähle den Ordner `latex_tools` aus.
2. Öffne links beim Ordnersymbol die Ansicht für die Dateien
3. Öffne PlotGOAT.py
4. **Öffne ein neues Terminal** oben in der Leiste auf `Terminal` drücken, und `Neues Terminal` klicken
5. Gib im Terminal von VSCode folgenden befehl ein und drücke Enter:
```bash
pip3 install pandas matplotlib numpy scipy seaborn
```
6. **Um immer die neuesten Updates zu bekommen:** Jedes mal kurz im Terminal ausführen, um die neueste Version der App runterzuladen:
   ```bash
     git pull
     ```
7. Python Skript ausführen (oben rechts)

Damit ist die Einrichtung abgeschlossen.

**Wofür ist der TeX-Export gedacht?**  
Die `.tex`-Datei ist speziell für Nutzer von LaTeX gedacht und wird in wissenschaftlichen oder technischen Dokumenten verwendet. Wenn Sie LaTeX nicht verwenden, können Sie diese Funktion ignorieren.

Mit der PlotGOAT App können Sie schnell und einfach Ihre Daten visualisieren und als Diagramme speichern – perfekt für Analysen und Berichte!
