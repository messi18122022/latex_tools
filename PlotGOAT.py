# pip3 install pandas matplotlib numpy scipy seaborn
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import numpy as np
from scipy import stats
import json
import os
import webbrowser

# Globale Einstellungen für LaTeX und Computer Modern
plt.rcParams['text.usetex'] = True  # Aktiviert LaTeX für Textrenderung
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern']
plt.rcParams['text.latex.preamble'] = r'\usepackage{siunitx}'

class PlotGOAT:
    def __init__(self, root):
        self.root = root
        self.root.title("PlotGOAT")
        self.root.geometry("1500x1000")  # Set larger window size for better usability

        # Frame for file operations and buttons
        self.file_frame = tk.Frame(root, padx=10, pady=10)
        self.file_frame.grid(row=0, column=0, sticky="nw")

        self.upload_button = self.create_button(self.file_frame, "Upload Excel, CSV, TXT", self.load_csv, 0, 0)

        self.files_listbox = tk.Listbox(self.file_frame, selectmode=tk.SINGLE, height=7, width=50)
        self.files_listbox.grid(row=1, column=0, pady=5)

        self.remove_file_button = self.create_button(self.file_frame, "Remove Selected File", self.remove_file, 2, 0)
        self.add_row_button = self.create_button(self.file_frame, "Add Row", self.add_row, 0, 1)
        self.remove_row_button = self.create_button(self.file_frame, "Remove Last Row", self.remove_row, 1, 1)
        self.plot_button = self.create_button(self.file_frame, "Plot", self.plot_data, 3, 1)

        self.table_frame = tk.Frame(root, padx=10, pady=10)
        self.table_frame.grid(row=11, column=0, sticky="nw")  # Nach Caption und Label Felder

        # Placeholder for DataFrames and file names
        self.dataframes = {}
        self.rows = []
        self.canvas = None  # Store the canvas to update or clear it

        # Eingabefelder für Caption und Label
        self.caption_label = tk.Label(self.file_frame, text="Caption:")
        self.caption_label.grid(row=3, column=0, pady=5, sticky="w")
        self.caption_entry = self.create_entry(self.file_frame, 50, 4, 0, "Caption")


        self.label_label = tk.Label(self.file_frame, text="Label:")
        self.label_label.grid(row=5, column=0, pady=5, sticky="w")
        self.label_entry = self.create_entry(self.file_frame, 40, 6, 0, "Label")

        # Button für Tex-Export
        self.export_button = tk.Button(self.file_frame, text=".tex exportieren", command=self.export_tex, width=15)
        self.export_button.grid(row=6, column=1, pady=5)

        # Buttons in der Benutzeroberfläche für PNG und PDF Export
        self.export_png_button = tk.Button(self.file_frame, text=".png exportieren", command=self.export_png, width=15)
        self.export_png_button.grid(row=5, column=1, pady=5)

        self.export_pdf_button = tk.Button(self.file_frame, text=".pdf exportieren", command=self.export_pdf, width=15)
        self.export_pdf_button.grid(row=4, column=1, pady=5)

        # Button für Plot-Vorschau
        self.preview_button = tk.Button(self.file_frame, text="Plot-Vorschau", command=self.plot_preview, width=20)
        self.preview_button.grid(row=2, column=1, pady=5)

        self.save_project_button = tk.Button(self.file_frame, text="Projekt speichern", command=self.save_project, width=20)
        self.save_project_button.grid(row=0, column=3, pady=5)

        self.load_project_button = tk.Button(self.file_frame, text="Projekt laden", command=self.load_project, width=20)
        self.load_project_button.grid(row=1, column=3, pady=5)

        self.formel_button = tk.Button(self.file_frame, text="Formelzeichen generieren", command=self.open_formelzeichen_creator, width=20)
        self.formel_button.grid(row=0, column=4, pady=5)

        self.formel_button = tk.Button(self.file_frame, text="Einheiten generieren", command=self.open_einheiten_creator, width=20)
        self.formel_button.grid(row=1, column=4, pady=5)

        self.plot_settings = self.load_config()["plot_settings"]

    def open_formelzeichen_creator(self):
        html_file_path = os.path.join(os.path.dirname(__file__), "latex_formelzeichen_creator.html")
        webbrowser.open_new_tab(f"file://{html_file_path}")

    def open_einheiten_creator(self):
        html_file_path = os.path.join(os.path.dirname(__file__), "latex_einheiten_creator.html")
        webbrowser.open_new_tab(f"file://{html_file_path}")

    def load_config(self):
        """Lade Konfiguration aus config.json"""
        with open("resources/config.json", "r") as f:
            config = json.load(f)
        return config

    def create_button(self, frame, text, command, row, column, width=20):
        button = tk.Button(frame, text=text, command=command, width=width)
        button.grid(row=row, column=column, pady=5)
        return button

    def create_entry(self, frame, width, row, column, placeholder=""):
        entry = tk.Entry(frame, width=width)
        entry.insert(0, placeholder)
        entry.grid(row=row, column=column, pady=5)
        return entry

    def create_dropdown(self, frame, options, row, column, default_value=None, width=10):
        dropdown = ttk.Combobox(frame, state="readonly", values=options, width=width)
        if default_value:
            dropdown.set(default_value)
        dropdown.grid(row=row, column=column, padx=5)
        return dropdown

    def show_error(self, message):
        tk.messagebox.showerror("Fehler", message)

    def save_project(self):
        # Dialog zum Speichern des Projekts öffnen
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile="projekt.json")
        if not file_path:
            return  # Abbrechen, falls der Benutzer keinen Pfad angibt

        # Sammeln aller Projektdaten
        project_data = {
            "dataframes": {name: df.to_dict() for name, df in self.dataframes.items()},
            "plot_settings": self.plot_settings,
            "rows": [
                {
                    "file_x": file_dropdown_x.get(),
                    "file_y": file_dropdown_y.get(),
                    "x_column": x_dropdown.get(),
                    "y_column": y_dropdown.get(),
                    "visibility": visibility_dropdown.get(),
                    "legend_name": name_entry.get(),
                    "color": color_dropdown.get(),
                    "line_width": line_width_entry.get(),
                    "line_style": line_style_dropdown.get(),
                    "marker": marker_dropdown.get()
                }
                for file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_dropdown, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in self.rows
            ]
        }

        # Speichern in die JSON-Datei
        with open(file_path, 'w') as json_file:
            json.dump(project_data, json_file)
        
        tk.messagebox.showinfo("Erfolg", "Projekt wurde erfolgreich gespeichert.")

    def load_project(self):
        # Dialog zum Laden eines Projekts öffnen
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return  # Abbrechen, falls der Benutzer keinen Pfad angibt

        # Projekt-Daten aus der JSON-Datei laden
        with open(file_path, 'r') as json_file:
            project_data = json.load(json_file)

        # Daten in die App-Struktur zurückladen
        self.dataframes = {name: pd.DataFrame(data) for name, data in project_data["dataframes"].items()}
        self.plot_settings.update(project_data["plot_settings"])

        # Alle Zeilen neu erstellen und konfigurieren
        for row in self.rows:
            row[-1].destroy()  # Alle alten Row-Frames löschen
        self.rows.clear()

        for row_data in project_data["rows"]:
            self.add_row()
            last_row = self.rows[-1]
            last_row[0].set(row_data["file_x"])
            last_row[1].set(row_data["file_y"])
            last_row[2].set(row_data["x_column"])
            last_row[3].set(row_data["y_column"])
            last_row[4].set(row_data["visibility"])
            last_row[5].delete(0, tk.END)
            last_row[5].insert(0, row_data["legend_name"])
            last_row[6].set(row_data["color"])
            last_row[7].delete(0, tk.END)
            last_row[7].insert(0, row_data["line_width"])
            last_row[8].set(row_data["line_style"])
            last_row[9].set(row_data["marker"])

        tk.messagebox.showinfo("Erfolg", "Projekt wurde erfolgreich geladen.")

    def load_csv(self):
        # Open file dialog to select CSV, TXT, or Excel files
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV/TXT files", "*.csv *.txt"), ("Excel files", "*.xlsx")])
        for file_path in file_paths:
            if file_path:
                # Try loading the file with different encodings
                encodings = ['utf-8', 'ISO-8859-1', 'cp1252']  # Common encodings for data files
                for encoding in encodings:
                    try:
                        if file_path.endswith('.xlsx'):
                            # Load Excel file
                            df = pd.read_excel(file_path)
                        else:
                            # Load CSV or TXT file with automatic delimiter detection
                            df = pd.read_csv(file_path, sep=None, engine='python', encoding=encoding)
                        break  # Break if loading was successful
                    except Exception as e:
                        continue  # Try the next encoding if there's an error
                else:
                    # If all encodings fail, show an error
                    self.show_error(f"Die Datei {file_path} konnte nicht geladen werden. Bitte prüfen Sie das Dateiformat.")
                    continue

                file_name = file_path.split('/')[-1]  # Get the file name from path
                self.dataframes[file_name] = df

                # Update dropdown options in existing rows
                for file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_button, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in self.rows:
                    file_dropdown_x["values"] = list(self.dataframes.keys())
                    file_dropdown_y["values"] = list(self.dataframes.keys())

                # Update the listbox
                if file_name not in self.files_listbox.get(0, tk.END):
                    self.files_listbox.insert(tk.END, file_name)

    def remove_file(self):
        # Remove selected file from list
        selected_index = self.files_listbox.curselection()
        if selected_index:
            file_name = self.files_listbox.get(selected_index)
            self.files_listbox.delete(selected_index)
            if file_name in self.dataframes:
                del self.dataframes[file_name]

            # Update dropdown options in existing rows
            for file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_button, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in self.rows:
                file_dropdown_x["values"] = list(self.dataframes.keys())
                file_dropdown_y["values"] = list(self.dataframes.keys())

    def add_row(self):
        # Create new row for selecting file, x, and y columns
        row_frame = tk.Frame(self.table_frame)
        row_frame.pack(pady=5, fill="x")

        # File selection dropdowns
        file_dropdown_x = self.create_dropdown(row_frame, list(self.dataframes.keys()), 0, 0, width=20)
        x_dropdown = ttk.Combobox(row_frame, state="readonly", width=10)
        x_dropdown.grid(row=0, column=1, padx=5)

        file_dropdown_y = self.create_dropdown(row_frame, list(self.dataframes.keys()), 0, 2, width=20)
        y_dropdown = ttk.Combobox(row_frame, state="readonly", width=10)
        y_dropdown.grid(row=0, column=3, padx=5)

        # Bind update_columns to file selection change
        file_dropdown_x.bind("<<ComboboxSelected>>", lambda e: self.update_columns(file_dropdown_x, 'x'))
        file_dropdown_y.bind("<<ComboboxSelected>>", lambda e: self.update_columns(file_dropdown_y, 'y'))

        # Visibility dropdown
        visibility_dropdown = self.create_dropdown(row_frame, ["sichtbar", "unsichtbar"], 0, 4, default_value="sichtbar", width=7)

        # Legend name entry
        name_entry = tk.Entry(row_frame, width=20)
        name_entry.insert(0, "Legend Name")
        name_entry.grid(row=0, column=5, padx=5)

        # Color selection dropdown
        color_dropdown = ttk.Combobox(row_frame, state="readonly", width=5)
        color_dropdown["values"] = ["blue", "red", "teal", "orange", "darkgray", "cyan", "magenta", "brown", "purple"]
        color_dropdown.set("blue")  # Default color is blue
        color_dropdown.grid(row=0, column=6, padx=5)

        # Line width entry
        line_width_entry = tk.Entry(row_frame, width=2)
        line_width_entry.insert(0, "1")  # Default line width is 1
        line_width_entry.grid(row=0, column=7, padx=5)

        # Line style dropdown
        line_style_dropdown = self.create_dropdown(row_frame, ["|", ":", "keine"], 0, 8, default_value="|", width=3)

        # Marker style dropdown
        marker_dropdown = self.create_dropdown(row_frame, ["keine", "Kreis", "+", "Dreieck", "Quadrat"], 0, 9, default_value="keine", width=6)

        # Add to list of rows
        self.rows.append((file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_dropdown, line_width_entry, line_style_dropdown, marker_dropdown, row_frame))

        # Update file dropdown options if CSVs are already loaded
        file_dropdown_x["values"] = list(self.dataframes.keys())
        file_dropdown_y["values"] = list(self.dataframes.keys())

    def remove_row(self):
        # Remove the last added row
        if self.rows:
            file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_button, line_width_entry, line_style_dropdown, marker_dropdown, row_frame = self.rows.pop()
            row_frame.destroy()

    def update_columns(self, file_dropdown, axis):
        # Update x and y dropdown options based on selected file
        selected_file = file_dropdown.get()
        if selected_file in self.dataframes:
            columns = list(self.dataframes[selected_file].columns)
            for fd_x, fd_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_button, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in self.rows:
                if (axis == 'x' and fd_x == file_dropdown):
                    x_dropdown["values"] = columns
                elif (axis == 'y' and fd_y == file_dropdown):
                    y_dropdown["values"] = columns

    def plot_data(self):
        # Neues Fenster für Plot und Einstellungen erstellen
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Plot")
        plot_window.geometry("1000x600")  # Fenstergröße für Plot und Einstellungen

        # Frame für Plot-Einstellungen auf der linken Seite
        settings_frame = tk.Frame(plot_window, padx=10, pady=10)
        settings_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Funktion zur Anwendung und Aktualisierung der Einstellungen
        def apply_settings():
            def get_text_widget_value(text_widget):
                # Entferne Zeilenumbrüche aus dem Textfeld, damit sie für LaTeX richtig formatiert sind.
                return text_widget.get("1.0", "end-1c").replace("\n", "")

            # Aktualisiere plot_settings mit Werten aus Eingabefeldern
            self.plot_settings['x_label'] = get_text_widget_value(x_label_text)
            self.plot_settings['y_label'] = get_text_widget_value(y_label_text)
            self.plot_settings['x_min'] = float(x_min_entry.get()) if x_min_entry.get() else None
            self.plot_settings['x_max'] = float(x_max_entry.get()) if x_max_entry.get() else None
            self.plot_settings['y_min'] = float(y_min_entry.get()) if y_min_entry.get() else None
            self.plot_settings['y_max'] = float(y_max_entry.get()) if y_max_entry.get() else None
            self.plot_settings['width_cm'] = float(width_entry.get()) if width_entry.get() else 16
            self.plot_settings['height_cm'] = float(height_entry.get()) if height_entry.get() else 6.7
            self.plot_settings['legend_position'] = legend_position_dropdown.get()
            self.plot_settings['invert_x_axis'] = invert_x_axis_var.get()
            self.plot_settings['log_x_axis'] = log_x_axis_var.get()
            self.plot_settings['log_y_axis'] = log_y_axis_var.get()
            self.plot_settings['grid'] = grid_var.get()
            self.plot_settings['linreg'] = linreg_var.get()  # Hinzufügen der LinReg-Option
            self.plot_settings['corr_pos'] = corr_pos_dropdown.get()  # Position für Korrelationskoeffizienten
            
            def parse_ticks(ticks_input):
                if not ticks_input.strip():
                    return None  # Keine Eingabe, automatische Ticks verwenden
                try:
                    # Prüfen auf 'start:step:end' Format
                    if ":" in ticks_input:
                        parts = ticks_input.split(":")
                        if len(parts) == 3:
                            start, step, end = map(float, parts)
                            return list(np.arange(start, end + step, step))
                        else:
                            raise ValueError("Ungültiges Format. Verwenden Sie 'start:step:end' oder eine durch Kommas getrennte Liste.")
                    # Falls kein ':', versuchen, die Werte als durch Kommas getrennte Liste zu lesen
                    else:
                        return [float(tick) for tick in ticks_input.split(",") if tick.strip()]
                except ValueError as e:
                    raise ValueError("Ungültiges Format für Ticks. Verwenden Sie 'start:step:end' oder eine durch Kommas getrennte Liste.")

            # Aktualisieren der plot_settings für x_ticks und y_ticks
            try:
                self.plot_settings['x_ticks'] = parse_ticks(x_ticks_entry.get())
            except ValueError as ve:
                self.show_error(str(ve))

            try:
                self.plot_settings['y_ticks'] = parse_ticks(y_ticks_entry.get())
            except ValueError as ve:
                self.show_error(str(ve))


            # Plot aktualisieren
            try:
                update_plot()
            except Exception as e:
                self.show_error("Es gab einen Fehler in der LaTeX-Syntax. Bitte überprüfen Sie die Achsenbeschriftungen.")

        # "Plot aktualisieren" Button
        update_button = tk.Button(settings_frame, text="Plot aktualisieren", command=apply_settings)
        update_button.pack(pady=10)

        tk.Label(settings_frame, text="X-axis Label:").pack(anchor="w")
        x_label_text = tk.Text(settings_frame, height=3, width=30, wrap="none")
        x_label_text.insert("1.0", self.plot_settings['x_label'])
        x_label_text.pack(anchor="w")

        tk.Label(settings_frame, text="Y-axis Label:").pack(anchor="w")
        y_label_text = tk.Text(settings_frame, height=3, width=30, wrap="none")
        y_label_text.insert("1.0", self.plot_settings['y_label'])
        y_label_text.pack(anchor="w")

        # Min/Max Eingaben für Achsen und weitere Einstellungen
        tk.Label(settings_frame, text="X Min:").pack(anchor="w")
        x_min_entry = tk.Entry(settings_frame)
        x_min_entry.insert(0, str(self.plot_settings['x_min']) if self.plot_settings['x_min'] is not None else "")
        x_min_entry.pack(anchor="w")

        tk.Label(settings_frame, text="X Max:").pack(anchor="w")
        x_max_entry = tk.Entry(settings_frame)
        x_max_entry.insert(0, str(self.plot_settings['x_max']) if self.plot_settings['x_max'] is not None else "")
        x_max_entry.pack(anchor="w")

        tk.Label(settings_frame, text="Y Min:").pack(anchor="w")
        y_min_entry = tk.Entry(settings_frame)
        y_min_entry.insert(0, str(self.plot_settings['y_min']) if self.plot_settings['y_min'] is not None else "")
        y_min_entry.pack(anchor="w")

        tk.Label(settings_frame, text="Y Max:").pack(anchor="w")
        y_max_entry = tk.Entry(settings_frame)
        y_max_entry.insert(0, str(self.plot_settings['y_max']) if self.plot_settings['y_max'] is not None else "")
        y_max_entry.pack(anchor="w")

        tk.Label(settings_frame, text="Width (cm):").pack(anchor="w")
        width_entry = tk.Entry(settings_frame)
        width_entry.insert(0, str(self.plot_settings['width_cm']))
        width_entry.pack(anchor="w")

        tk.Label(settings_frame, text="Height (cm):").pack(anchor="w")
        height_entry = tk.Entry(settings_frame)
        height_entry.insert(0, str(self.plot_settings['height_cm']))
        height_entry.pack(anchor="w")

        # Plot-Einstellungen für Legendenposition
        tk.Label(settings_frame, text="Legend Position:").pack(anchor="w")
        legend_position_dropdown = ttk.Combobox(settings_frame, state="readonly")
        legend_position_dropdown["values"] = ["oben rechts", "oben links", "unten rechts", "unten links"]
        legend_position_dropdown.set(self.plot_settings['legend_position'])
        legend_position_dropdown.pack(anchor="w")

        invert_x_axis_var = tk.BooleanVar(value=self.plot_settings['invert_x_axis'])
        invert_x_axis_checkbox = tk.Checkbutton(settings_frame, text="Invert X-axis", variable=invert_x_axis_var)
        invert_x_axis_checkbox.pack(anchor="w")

        # Einstellungen für log-Skala, Gitter, Ticks
        log_x_axis_var = tk.BooleanVar(value=self.plot_settings['log_x_axis'])
        log_x_axis_checkbox = tk.Checkbutton(settings_frame, text="Logarithmic X-axis", variable=log_x_axis_var)
        log_x_axis_checkbox.pack(anchor="w")

        log_y_axis_var = tk.BooleanVar(value=self.plot_settings['log_y_axis'])
        log_y_axis_checkbox = tk.Checkbutton(settings_frame, text="Logarithmic Y-axis", variable=log_y_axis_var)
        log_y_axis_checkbox.pack(anchor="w")

        grid_var = tk.BooleanVar(value=self.plot_settings['grid'])
        grid_checkbox = tk.Checkbutton(settings_frame, text="Grid anzeigen", variable=grid_var)
        grid_checkbox.pack(anchor="w")

        linreg_var = tk.BooleanVar(value=self.plot_settings.get('linreg', False))
        linreg_checkbox = tk.Checkbutton(settings_frame, text="LinReg", variable=linreg_var)
        linreg_checkbox.pack(anchor="w")

        tk.Label(settings_frame, text="Position Korrelationskoeffizient:").pack(anchor="w")
        corr_pos_dropdown = ttk.Combobox(settings_frame, state="readonly")
        corr_pos_dropdown["values"] = ["oben rechts", "oben links", "unten rechts", "unten links"]
        corr_pos_dropdown.set(self.plot_settings.get('corr_pos', "oben rechts"))
        corr_pos_dropdown.pack(anchor="w")

        tk.Label(settings_frame, text="X Ticks (comma-separated):").pack(anchor="w")
        x_ticks_entry = tk.Entry(settings_frame)
        x_ticks_entry.insert(0, ','.join(map(str, self.plot_settings['x_ticks'])) if self.plot_settings['x_ticks'] else "")
        x_ticks_entry.pack(anchor="w")

        tk.Label(settings_frame, text="Y Ticks (comma-separated):").pack(anchor="w")
        y_ticks_entry = tk.Entry(settings_frame)
        y_ticks_entry.insert(0, ','.join(map(str, self.plot_settings['y_ticks'])) if self.plot_settings['y_ticks'] else "")
        y_ticks_entry.pack(anchor="w")

        # Erstelle das Plot-Fenster
        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def update_plot():
            ax.clear()
            
            # Zähle die sichtbaren Linien, um die Bedingung für die Legende zu prüfen
            visible_lines = 0
            for file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_dropdown, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in self.rows:
                selected_file_x = file_dropdown_x.get()
                selected_file_y = file_dropdown_y.get()
                x_column = x_dropdown.get()
                y_column = y_dropdown.get()
                legend_name = name_entry.get()
                visibility = visibility_dropdown.get()
                color = color_dropdown.get()
                line_width = float(line_width_entry.get())
                line_style = line_style_dropdown.get()
                marker = marker_dropdown.get()

                # Map line style and marker to matplotlib options
                line_style_map = {
                    "|": '-',
                    ":": '--',
                    "keine": ''
                }
                marker_map = {
                    "keine": '',
                    "Kreis": 'o',
                    "+": '+',
                    "Dreieck": '^',
                    "Quadrat": 's'
                }

                linestyle = line_style_map.get(line_style, '-')
                mark = marker_map.get(marker, '')

                if selected_file_x and selected_file_y and x_column and y_column and visibility == "sichtbar":
                    df_x = self.dataframes[selected_file_x]
                    df_y = self.dataframes[selected_file_y]
                    x_data = df_x[x_column].to_numpy()
                    y_data = df_y[y_column].to_numpy()

                    try:
                        # Plot the original data with settings
                        ax.plot(x_data, y_data, label=legend_name, color=color, linewidth=line_width, linestyle=linestyle, marker=mark)
                        visible_lines += 1

                        # Linear regression if selected
                        if self.plot_settings.get('linreg', False):
                            slope, intercept, r_value, _, _ = stats.linregress(x_data, y_data)
                            reg_line = slope * x_data + intercept
                            ax.plot(x_data, reg_line, color="black", linewidth=0.5, label=f"LinReg ({legend_name})")

                            # Display correlation coefficient
                            r_text = f"r = {r_value:.4f}"
                            corr_pos_map = {
                                "oben rechts": (0.8, 0.95),
                                "oben links": (0.1, 0.95),
                                "unten rechts": (0.8, 0.1),
                                "unten links": (0.1, 0.1)
                            }
                            pos_x, pos_y = corr_pos_map.get(self.plot_settings.get('corr_pos', 'oben rechts'))

                            # Add the correlation coefficient box
                            box_properties = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
                            ax.text(pos_x, pos_y, r_text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=box_properties)
                    
                    except Exception as e:
                        self.show_error(f"Fehlerhafte LaTeX-Syntax in der Legende: '{legend_name}'. Bitte überprüfen.")
                        return  # Abbrechen, um das fehlerhafte Plotten zu vermeiden

            # Apply axis labels and limits with LaTeX error handling
            try:
                ax.set_xlabel(self.plot_settings['x_label'])
                ax.set_ylabel(self.plot_settings['y_label'])
            except Exception as e:
                self.show_error("Fehlerhafte LaTeX-Syntax in den Achsenbeschriftungen. Bitte überprüfen.")
                return  # Abbrechen, um das fehlerhafte Plotten zu vermeiden

            if self.plot_settings['x_min'] is not None and self.plot_settings['x_max'] is not None:
                ax.set_xlim([self.plot_settings['x_min'], self.plot_settings['x_max']])

            if self.plot_settings['y_min'] is not None and self.plot_settings['y_max'] is not None:
                ax.set_ylim([self.plot_settings['y_min'], self.plot_settings['y_max']])

            if self.plot_settings['invert_x_axis']:
                ax.invert_xaxis()

            if self.plot_settings['log_x_axis']:
                ax.set_xscale('log')
            if self.plot_settings['log_y_axis']:
                ax.set_yscale('log')

            if self.plot_settings['x_ticks'] is not None:
                ax.set_xticks(self.plot_settings['x_ticks'])

            if self.plot_settings['y_ticks'] is not None:
                ax.set_yticks(self.plot_settings['y_ticks'])

            if self.plot_settings['grid']:
                ax.grid(True)

            # Show legend if more than one visible line exists
            if visible_lines > 1:
                try:
                    legend_position_map = {
                        "oben rechts": "upper right",
                        "oben links": "upper left",
                        "unten rechts": "lower right",
                        "unten links": "lower left"
                    }
                    legend_position = legend_position_map.get(self.plot_settings['legend_position'], 'upper right')
                    ax.legend(loc=legend_position)
                except Exception as e:
                    self.show_error("Fehlerhafte LaTeX-Syntax in der Legendenposition. Bitte überprüfen.")
                    return  # Abbrechen, um das fehlerhafte Plotten zu vermeiden

            canvas.draw()

        update_plot()

    def export_tex(self):
        # Öffne einen Speicherdialog mit vorgeschlagenem Dateinamen
        file_path = filedialog.asksaveasfilename(defaultextension=".tex", filetypes=[("TeX files", "*.tex")], initialfile="Plot.tex")
        if not file_path:
            return  # Falls der Benutzer abbricht

        # Hol die Caption und das Label aus den Eingabefeldern
        caption = self.caption_entry.get()
        label = self.label_entry.get()

        # Plot als TikZ-Code erstellen
        width_cm = self.plot_settings['width_cm']
        height_cm = self.plot_settings['height_cm']

        # Tex-Export mit LaTeX Formatierung
        xlabel_tex = self.plot_settings['x_label']  # Erlaubt LaTeX Formatierung
        ylabel_tex = self.plot_settings['y_label']  # Erlaubt LaTeX Formatierung

        # Mapping for legend position to TikZ/PGFPlots equivalent
        legend_position_map = {
            "oben rechts": "north east",
            "oben links": "north west",
            "unten rechts": "south east",
            "unten links": "south west"
        }
        
        legend_position_tikz = legend_position_map.get(self.plot_settings['legend_position'], 'north east')

        tikz_code = f"""
        \\begin{{figure}}[H]
            \\centering
            \\begin{{tikzpicture}}
            \\begin{{axis}}[
                width={width_cm}cm,
                height={height_cm}cm,
                xlabel={{{xlabel_tex}}},
                ylabel={{{ylabel_tex}}},
                xmode={'log' if self.plot_settings['log_x_axis'] else 'normal'},
                ymode={'log' if self.plot_settings['log_y_axis'] else 'normal'},
                grid={'major' if self.plot_settings['grid'] else 'none'},
                scaled ticks=false,  
                tick label style={{/pgf/number format/fixed}},
                xmin={self.plot_settings['x_min'] if self.plot_settings['x_min'] is not None else ''},
                xmax={self.plot_settings['x_max'] if self.plot_settings['x_max'] is not None else ''},
                ymin={self.plot_settings['y_min'] if self.plot_settings['y_min'] is not None else ''},
                ymax={self.plot_settings['y_max'] if self.plot_settings['y_max'] is not None else ''}
        """

        # Hinzufügen von xtick und ytick innerhalb der Achsen-Konfiguration
        if self.plot_settings['x_ticks'] is not None:
            tikz_code += f", xtick={{{','.join(map(str, self.plot_settings['x_ticks']))}}}"

        if self.plot_settings['y_ticks'] is not None:
            tikz_code += f", ytick={{{','.join(map(str, self.plot_settings['y_ticks']))}}}"

        # Hinzufügen der Invertierung, falls erforderlich
        if self.plot_settings['invert_x_axis']:
            tikz_code += f", x dir=reverse"

        # Zähle die sichtbaren Linien
        visible_lines = [row for row in self.rows if row[4].get() == "sichtbar"]

        # Nur eine Legende setzen, wenn mehr als eine sichtbare Linie vorhanden ist
        if len(visible_lines) > 1:
            tikz_code += f", legend pos={legend_position_tikz}\n"
        
        # Schließe die Achsen-Definition
        tikz_code += "]\n"

        # Daten für die Linien hinzufügen
        for file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_dropdown, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in visible_lines:
            df_x = self.dataframes[file_dropdown_x.get()]
            df_y = self.dataframes[file_dropdown_y.get()]
            x_data = df_x[x_dropdown.get()].to_list()
            y_data = df_y[y_dropdown.get()].to_list()

            # Nimm die Farbe direkt aus dem Dropdown-Menü
            color_latex = color_dropdown.get()

            line_width = float(line_width_entry.get())
            line_style = {'|': 'solid', ':': 'dashed', 'keine': 'only marks'}[line_style_dropdown.get()]
            marker = {'keine': '', 'Kreis': '*', '+': '+*', 'Dreieck': 'triangle*', 'Quadrat': 'square*'}[marker_dropdown.get()]
            legend_name = name_entry.get()

            tikz_code += f"""
            \\addplot[
                color={color_latex},
                line width={line_width}pt,
                mark={marker},
                style={line_style}
            ] coordinates {{
            {" ".join(f"({x},{y})" for x, y in zip(x_data, y_data))}
            }};"""

            # Füge nur eine Legende hinzu, wenn mehr als eine sichtbare Linie vorhanden ist
            if len(visible_lines) > 1 and legend_name:
                tikz_code += f"\\addlegendentry{{{legend_name}}}\n"

            # Lineare Regression hinzufügen, falls aktiviert
            if self.plot_settings.get('linreg', False):
                slope, intercept, r_value, _, _ = stats.linregress(x_data, y_data)
                reg_line = [(x, slope * x + intercept) for x in x_data]
                tikz_code += f"""
                \\addplot[
                    color=black,
                    line width=0.5pt,
                    solid
                ] coordinates {{
                {" ".join(f"({x},{y})" for x, y in reg_line)}
                }};"""

                # Position des Korrelationskoeffizienten in TikZ
                corr_pos_map = {
                    "oben rechts": "(rel axis cs:0.9,0.9)",
                    "oben links": "(rel axis cs:0.1,0.9)",
                    "unten rechts": "(rel axis cs:0.9,0.1)",
                    "unten links": "(rel axis cs:0.1,0.1)"
                }
                tikz_pos = corr_pos_map.get(self.plot_settings.get('corr_pos', 'oben rechts'))
                tikz_code += f"\\node[fill=white, draw, inner sep=3pt] at {tikz_pos} {{\\small $r = {r_value:.4f}$}};\n"

        tikz_code += """
        \\end{axis}
        \\end{tikzpicture}
        """

        # Caption und Label hinzufügen
        if caption:
            tikz_code += f"\\caption{{{caption}}}\n"
        if label:
            tikz_code += f"\\label{{fig:{label}}}\n"
        tikz_code += "\\end{figure}"

        # Schreibe den TikZ-Code in die Datei
        with open(file_path, 'w') as tex_file:
            tex_file.write(tikz_code)

        tk.messagebox.showinfo("Erfolg", "Die Datei wurde erfolgreich exportiert.")

        # Call the JSON export after saving the TeX
        self.export_json_for_plot(file_path)
        tk.messagebox.showinfo("Erfolg", "Die Datei und JSON wurden erfolgreich als TeX und JSON exportiert.")

    def export_plot(self, file_extension, file_format):
        # Öffne einen Speicherdialog basierend auf dem Dateiformat
        file_path = filedialog.asksaveasfilename(defaultextension=f".{file_extension}", filetypes=[(f"{file_extension.upper()} files", f"*.{file_extension}")], initialfile=f"Plot.{file_extension}")
        if not file_path:
            return  # Falls der Benutzer abbricht
        
        # Plot-Einstellungen für die Größe in cm und Konvertierung in Zoll
        width_inch = self.plot_settings['width_cm'] / 2.54
        height_inch = self.plot_settings['height_cm'] / 2.54

        # Erstelle den Plot
        fig, ax = plt.subplots(figsize=(width_inch, height_inch))

        for row in self.rows:
            # Extrahiere und konvertiere die Parameter aus den Widgets
            selected_file_x, selected_file_y = row[0].get(), row[1].get()
            x_column, y_column = row[2].get(), row[3].get()
            legend_name, visibility = row[5].get(), row[4].get()
            color, line_width = row[6].get(), float(row[7].get())
            line_style, marker = row[8].get(), row[9].get()

            # Konvertiere Zeichenstile und Marker
            line_style_map = {"|": '-', ":": '--', "keine": ''}
            marker_map = {"keine": '', "Kreis": 'o', "+": '+', "Dreieck": '^', "Quadrat": 's'}

            linestyle, mark = line_style_map.get(line_style, '-'), marker_map.get(marker, '')

            if selected_file_x and selected_file_y and x_column and y_column and visibility == "sichtbar":
                x_data, y_data = self.dataframes[selected_file_x][x_column].to_numpy(), self.dataframes[selected_file_y][y_column].to_numpy()
                ax.plot(x_data, y_data, label=legend_name, color=color, linewidth=line_width, linestyle=linestyle, marker=mark, markersize=2)
                
                # Lineare Regression und Korrelationskoeffizient, falls aktiviert
                if self.plot_settings.get('linreg', False):
                    slope, intercept, r_value, _, _ = stats.linregress(x_data, y_data)
                    reg_line = slope * x_data + intercept
                    ax.plot(x_data, reg_line, color="black", linewidth=0.5, label=f"LinReg ({legend_name})")

                    # Korrelationskoeffizient anzeigen in einer Box über dem Plot
                    r_text = f"r = {r_value:.4f}"
                    pos_x, pos_y = {
                        "oben rechts": (0.8, 0.95), "oben links": (0.1, 0.95),
                        "unten rechts": (0.8, 0.1), "unten links": (0.1, 0.1)
                    }.get(self.plot_settings.get('corr_pos', 'oben rechts'), (0.8, 0.95))

                    ax.text(pos_x, pos_y, r_text, transform=ax.transAxes, fontsize=10, verticalalignment='top',
                            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))

        # Setze Achsenbeschriftungen und andere Einstellungen
        ax.set_xlabel(self.plot_settings['x_label'])
        ax.set_ylabel(self.plot_settings['y_label'])
        if self.plot_settings['x_ticks'] is not None: ax.set_xticks(self.plot_settings['x_ticks'])
        if self.plot_settings['y_ticks'] is not None: ax.set_yticks(self.plot_settings['y_ticks'])
        if self.plot_settings['x_min'] is not None and self.plot_settings['x_max'] is not None: ax.set_xlim([self.plot_settings['x_min'], self.plot_settings['x_max']])
        if self.plot_settings['y_min'] is not None and self.plot_settings['y_max'] is not None: ax.set_ylim([self.plot_settings['y_min'], self.plot_settings['y_max']])
        if self.plot_settings['invert_x_axis']: ax.invert_xaxis()
        if self.plot_settings['log_x_axis']: ax.set_xscale('log')
        if self.plot_settings['log_y_axis']: ax.set_yscale('log')
        if self.plot_settings['grid']: ax.grid(True)

        # Zeige die Legende, wenn mehr als eine sichtbare Linie vorhanden ist
        if sum(1 for row in self.rows if row[4].get() == "sichtbar") > 1:
            legend_position = {
                "oben rechts": "upper right", "oben links": "upper left",
                "unten rechts": "lower right", "unten links": "lower left"
            }.get(self.plot_settings['legend_position'], 'upper right')
            ax.legend(loc=legend_position)

        # Speichere den Plot
        fig.savefig(file_path, dpi=300, bbox_inches='tight', transparent=True, format=file_format)
        plt.close(fig)  # Speicher freigeben
        tk.messagebox.showinfo("Erfolg", f"Der Plot wurde erfolgreich als {file_extension.upper()} gespeichert.")

        # Exportiere JSON für Plot
        self.export_json_for_plot(file_path)
        tk.messagebox.showinfo("Erfolg", f"Der Plot und JSON wurden erfolgreich als {file_extension.upper()} und JSON gespeichert.")

    def export_png(self):
        self.export_plot("png", "png")

    def export_pdf(self):
        self.export_plot("pdf", "pdf")

    def plot_preview(self):
        # Erstelle ein neues Fenster für den interaktiven Plot
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Plot Vorschau")
        preview_window.geometry("800x600")

        # Schließe-Button hinzufügen
        close_button = tk.Button(preview_window, text="Close", command=preview_window.destroy)
        close_button.pack(side=tk.BOTTOM, pady=10)

        # Interaktiver Plot wird erstellt
        fig, ax = plt.subplots()

        for file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_dropdown, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in self.rows:
            selected_file_x = file_dropdown_x.get()
            selected_file_y = file_dropdown_y.get()
            x_column = x_dropdown.get()
            y_column = y_dropdown.get()
            legend_name = name_entry.get()
            visibility = visibility_dropdown.get()
            color = color_dropdown.get()
            line_width = float(line_width_entry.get())
            line_style = line_style_dropdown.get()
            marker = marker_dropdown.get()

            # Plot-Daten, falls sichtbar
            if selected_file_x and selected_file_y and x_column and y_column and visibility == "sichtbar":
                df_x = self.dataframes[selected_file_x]
                df_y = self.dataframes[selected_file_y]
                ax.plot(df_x[x_column], df_y[y_column], label=legend_name, color=color, linewidth=line_width)

        # Übernahme der Achsenbeschriftungen, invertierten Achsen und Log-Skalierungen
        ax.set_xlabel(self.plot_settings['x_label'])
        ax.set_ylabel(self.plot_settings['y_label'])
        
        if self.plot_settings['invert_x_axis']:
            ax.invert_xaxis()
        if self.plot_settings['log_x_axis']:
            ax.set_xscale('log')
        if self.plot_settings['log_y_axis']:
            ax.set_yscale('log')

        # Toolbar für Interaktivität hinzufügen (Zoom, Pan, etc.)
        canvas = FigureCanvasTkAgg(fig, master=preview_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, preview_window)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def export_json_for_plot(self, file_path):
        """
        Save the visible data for the current plot as a JSON file, fully matching the project save format.
        """
        # Dictionary to hold visible data as per project save format
        visible_dataframes = {}
        visible_rows = []

        for file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_dropdown, line_width_entry, line_style_dropdown, marker_dropdown, row_frame in self.rows:
            if visibility_dropdown.get() == "sichtbar":
                selected_file_x = file_dropdown_x.get()
                selected_file_y = file_dropdown_y.get()
                x_column = x_dropdown.get()
                y_column = y_dropdown.get()
                legend_name = name_entry.get()
                color = color_dropdown.get()
                line_width = line_width_entry.get()
                line_style = line_style_dropdown.get()
                marker = marker_dropdown.get()

                # Check that selected files and columns exist
                if selected_file_x and selected_file_y and x_column and y_column:
                    df_x = self.dataframes[selected_file_x]
                    df_y = self.dataframes[selected_file_y]

                    # Include only the necessary columns in the dataframe dictionary
                    if selected_file_x not in visible_dataframes:
                        visible_dataframes[selected_file_x] = {}
                    if selected_file_y not in visible_dataframes:
                        visible_dataframes[selected_file_y] = {}

                    visible_dataframes[selected_file_x][x_column] = df_x[x_column].to_dict()
                    visible_dataframes[selected_file_y][y_column] = df_y[y_column].to_dict()

                    # Collect row settings
                    visible_rows.append({
                        "file_x": selected_file_x,
                        "file_y": selected_file_y,
                        "x_column": x_column,
                        "y_column": y_column,
                        "visibility": "sichtbar",
                        "legend_name": legend_name,
                        "color": color,
                        "line_width": line_width,
                        "line_style": line_style,
                        "marker": marker
                    })

        # JSON structure, closely matching the project save format
        json_data = {
            "dataframes": visible_dataframes,
            "plot_settings": self.plot_settings,
            "rows": visible_rows
        }

        # Define JSON filename based on the export file path
        json_file_path = os.path.splitext(file_path)[0] + ".json"

        # Write JSON file with detailed structure
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlotGOAT(root)
    root.mainloop()