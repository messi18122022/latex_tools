# pip3 install pandas matplotlib numpy scipy seaborn
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
        self.root.geometry("1500x1000")

        # Initialisierung der Datenstrukturen
        self.dataframes = {}
        self.rows = []
        self.canvas = None
        self.plot_settings = {
            "x_label": "X-axis Label",
            "y_label": "Y-axis Label",
            "x_min": None,
            "x_max": None,
            "y_min": None,
            "y_max": None,
            "width_cm": 16,
            "height_cm": 6.7,
            "legend_position": "oben rechts",
            "invert_x_axis": False,
            "invert_y_axis": False,
            "log_x_axis": False,
            "log_y_axis": False,
            "grid": True,
            "x_ticks": None,
            "y_ticks": None,
            "linreg": False,
            "corr_pos": "oben rechts"
        }

        self._create_ui()

    def _create_ui(self):
        """Erstellt alle GUI-Elemente und ordnet sie im Layout an."""
        self.file_frame = tk.Frame(self.root, padx=10, pady=10)
        self.file_frame.grid(row=0, column=0, sticky="nw")

        self.upload_button = self._create_button(self.file_frame, "Upload Excel, CSV, TXT", self.load_csv, 0, 0)
        self.files_listbox = tk.Listbox(self.file_frame, selectmode=tk.SINGLE, height=7, width=50)
        self.files_listbox.grid(row=1, column=0, pady=5)
        self.remove_file_button = self._create_button(self.file_frame, "Remove Selected File", self.remove_file, 2, 0)

        self.add_row_button = self._create_button(self.file_frame, "Add Row", self.add_row, 0, 1)
        self.remove_row_button = self._create_button(self.file_frame, "Remove Last Row", self.remove_row, 1, 1)

        self.preview_button = self._create_button(self.file_frame, "Plot-Vorschau", self.plot_preview, 2, 1)
        self.plot_button = self._create_button(self.file_frame, "Plot", self.plot_data, 3, 1)

        self.export_png_button = self._create_button(self.file_frame, ".png exportieren", self.export_png, 4, 1, width=15)
        self.export_pdf_button = self._create_button(self.file_frame, ".pdf exportieren", self.export_pdf, 5, 1, width=15)
        self.export_tex_button = self._create_button(self.file_frame, ".tex exportieren", self.export_tex, 6, 1, width=15)

        self.save_project_button = self._create_button(self.file_frame, "Projekt speichern", self.save_project, 0, 3)
        self.load_project_button = self._create_button(self.file_frame, "Projekt laden", self.load_project, 1, 3)
        self.export_json_button = self._create_button(self.file_frame, "Daten als JSON exportieren", self.export_json_for_plot, 2, 3)

        self.formel_button = self._create_button(self.file_frame, "Formelzeichen generieren", self.open_formelzeichen_creator, 0, 4)
        self.einheiten_button = self._create_button(self.file_frame, "Einheiten generieren", self.open_einheiten_creator, 1, 4)

        self.caption_label = tk.Label(self.file_frame, text="Caption:")
        self.caption_label.grid(row=3, column=0, pady=5, sticky="w")
        self.caption_entry = self._create_entry(self.file_frame, 50, 4, 0, "Caption")

        self.label_label = tk.Label(self.file_frame, text="Label:")
        self.label_label.grid(row=5, column=0, pady=5, sticky="w")
        self.label_entry = self._create_entry(self.file_frame, 40, 6, 0, "Label")

        self.table_frame = tk.Frame(self.root, padx=10, pady=10)
        self.table_frame.grid(row=1, column=0, sticky="nw")

    def _create_button(self, frame, text, command, row, column, width=20):
        """Hilfsfunktion zum Erstellen eines Buttons."""
        button = tk.Button(frame, text=text, command=command, width=width)
        button.grid(row=row, column=column, pady=5)
        return button

    def _create_entry(self, frame, width, row, column, placeholder=""):
        """Hilfsfunktion zum Erstellen eines Eingabefelds."""
        entry = tk.Entry(frame, width=width)
        entry.insert(0, placeholder)
        entry.grid(row=row, column=column, pady=5)
        return entry

    def _create_dropdown(self, frame, options, row, column, default_value=None, width=10):
        """Hilfsfunktion zum Erstellen eines Dropdown-Menüs."""
        dropdown = ttk.Combobox(frame, state="readonly", values=options, width=width)
        if default_value:
            dropdown.set(default_value)
        dropdown.grid(row=row, column=column, padx=5)
        return dropdown

    def show_error(self, message):
        """Zeigt eine Fehlermeldung in einem MessageBox-Fenster an."""
        tk.messagebox.showerror("Fehler", message)

    def open_formelzeichen_creator(self):
        """Öffnet den Formelzeichen-Creator im Webbrowser."""
        html_file_path = os.path.join(os.path.dirname(__file__), "latex_formelzeichen_creator.html")
        webbrowser.open_new_tab(f"file://{html_file_path}")

    def open_einheiten_creator(self):
        """Öffnet den Einheiten-Creator im Webbrowser."""
        html_file_path = os.path.join(os.path.dirname(__file__), "latex_einheiten_creator.html")
        webbrowser.open_new_tab(f"file://{html_file_path}")

    def save_project(self):
        """Speichert den aktuellen Projektstatus in einer JSON-Datei."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile="projekt.json")
        if not file_path:
            return

        project_data = {
            "dataframes": {name: df.to_dict() for name, df in self.dataframes.items()},
            "plot_settings": self.plot_settings,
            "rows": [
                {
                    "file_x": row[0].get(), "file_y": row[1].get(),
                    "x_column": row[2].get(), "y_column": row[3].get(),
                    "visibility": row[4].get(),
                    "legend_name": row[5].get(),
                    "color": row[6].get(),
                    "line_width": row[7].get(),
                    "line_style": row[8].get(),
                    "marker": row[9].get()
                } for row in self.rows
            ]
        }
        with open(file_path, 'w') as json_file:
            json.dump(project_data, json_file, indent=4)
        messagebox.showinfo("Erfolg", "Projekt wurde erfolgreich gespeichert.")

    def load_project(self):
        """Lädt ein gespeichertes Projekt aus einer JSON-Datei."""
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'r') as json_file:
            project_data = json.load(json_file)

        # Daten laden
        self.dataframes = {name: pd.DataFrame(data) for name, data in project_data["dataframes"].items()}
        self.plot_settings.update(project_data["plot_settings"])

        # UI leeren und neu aufbauen
        for row_frame in [row[-1] for row in self.rows]:
            row_frame.destroy()
        self.rows.clear()
        self.files_listbox.delete(0, tk.END)
        for name in self.dataframes:
            self.files_listbox.insert(tk.END, name)

        # Zeilen und Einstellungen wiederherstellen
        for row_data in project_data["rows"]:
            self.add_row()
            last_row_widgets = self.rows[-1]
            last_row_widgets[0].set(row_data["file_x"])
            last_row_widgets[1].set(row_data["file_y"])
            last_row_widgets[2]["values"] = list(self.dataframes[row_data["file_x"]].columns)
            last_row_widgets[2].set(row_data["x_column"])
            last_row_widgets[3]["values"] = list(self.dataframes[row_data["file_y"]].columns)
            last_row_widgets[3].set(row_data["y_column"])
            last_row_widgets[4].set(row_data["visibility"])
            last_row_widgets[5].delete(0, tk.END)
            last_row_widgets[5].insert(0, row_data["legend_name"])
            last_row_widgets[6].set(row_data["color"])
            last_row_widgets[7].delete(0, tk.END)
            last_row_widgets[7].insert(0, row_data["line_width"])
            last_row_widgets[8].set(row_data["line_style"])
            last_row_widgets[9].set(row_data["marker"])
        messagebox.showinfo("Erfolg", "Projekt wurde erfolgreich geladen.")

    def load_csv(self):
        """Lädt Excel-, CSV- oder TXT-Dateien in Pandas DataFrames."""
        file_paths = filedialog.askopenfilenames(filetypes=[("Data files", "*.csv *.txt *.xlsx")])
        for file_path in file_paths:
            if file_path:
                try:
                    if file_path.endswith('.xlsx'):
                        df = pd.read_excel(file_path)
                    else:
                        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')
                except Exception as e:
                    self.show_error(f"Fehler beim Laden von {file_path}: {e}")
                    continue

                file_name = os.path.basename(file_path)
                self.dataframes[file_name] = df
                self.files_listbox.insert(tk.END, file_name)

                for row in self.rows:
                    row[0]["values"] = list(self.dataframes.keys())
                    row[1]["values"] = list(self.dataframes.keys())

    def remove_file(self):
        """Entfernt die ausgewählte Datei aus der Liste und den Daten."""
        selected_index = self.files_listbox.curselection()
        if selected_index:
            file_name = self.files_listbox.get(selected_index)
            del self.dataframes[file_name]
            self.files_listbox.delete(selected_index)
            # Aktualisiert die Dropdown-Menüs
            for row in self.rows:
                row[0]["values"] = list(self.dataframes.keys())
                row[1]["values"] = list(self.dataframes.keys())

    def add_row(self):
        """Fügt eine neue Zeile zur Konfiguration einer Datenreihe hinzu."""
        row_frame = tk.Frame(self.table_frame)
        row_frame.pack(pady=5, fill="x")

        file_dropdown_x = self._create_dropdown(row_frame, list(self.dataframes.keys()), 0, 0, width=20)
        x_dropdown = self._create_dropdown(row_frame, [], 0, 1, width=10)
        file_dropdown_y = self._create_dropdown(row_frame, list(self.dataframes.keys()), 0, 2, width=20)
        y_dropdown = self._create_dropdown(row_frame, [], 0, 3, width=10)

        file_dropdown_x.bind("<<ComboboxSelected>>", lambda e: self._update_columns_for_row(file_dropdown_x, x_dropdown))
        file_dropdown_y.bind("<<ComboboxSelected>>", lambda e: self._update_columns_for_row(file_dropdown_y, y_dropdown))

        visibility_dropdown = self._create_dropdown(row_frame, ["sichtbar", "unsichtbar"], 0, 4, default_value="sichtbar", width=7)
        name_entry = tk.Entry(row_frame, width=20)
        name_entry.insert(0, "Legend Name")
        name_entry.grid(row=0, column=5, padx=5)
        color_dropdown = self._create_dropdown(row_frame, ["blue", "red", "teal", "orange", "darkgray", "cyan", "magenta", "brown", "purple"], 0, 6, default_value="blue", width=5)
        line_width_entry = tk.Entry(row_frame, width=2)
        line_width_entry.insert(0, "1")
        line_width_entry.grid(row=0, column=7, padx=5)
        line_style_dropdown = self._create_dropdown(row_frame, ["-", "--", ":", "keine"], 0, 8, default_value="-", width=4)
        marker_dropdown = self._create_dropdown(row_frame, ["keine", "o", "+", "^", "s"], 0, 9, default_value="keine", width=6)

        self.rows.append((file_dropdown_x, file_dropdown_y, x_dropdown, y_dropdown, visibility_dropdown, name_entry, color_dropdown, line_width_entry, line_style_dropdown, marker_dropdown, row_frame))

    def remove_row(self):
        """Entfernt die zuletzt hinzugefügte Zeile."""
        if self.rows:
            row_frame = self.rows.pop()[-1]
            row_frame.destroy()

    def _update_columns_for_row(self, file_dropdown, column_dropdown):
        """Aktualisiert die Spalten-Dropdowns basierend auf der Dateiauswahl."""
        selected_file = file_dropdown.get()
        if selected_file in self.dataframes:
            columns = list(self.dataframes[selected_file].columns)
            column_dropdown["values"] = columns
            column_dropdown.set('')

    def _generate_plot_figure(self, ax):
        """Zentrale Funktion zum Erstellen des Matplotlib-Plots."""
        ax.clear()
        visible_lines = 0
        for row in self.rows:
            selected_file_x, selected_file_y = row[0].get(), row[1].get()
            x_column, y_column = row[2].get(), row[3].get()
            visibility = row[4].get()

            if selected_file_x and selected_file_y and x_column and y_column and visibility == "sichtbar":
                try:
                    df_x, df_y = self.dataframes[selected_file_x], self.dataframes[selected_file_y]
                    x_data, y_data = df_x[x_column].to_numpy(), df_y[y_column].to_numpy()
                    
                    legend_name = row[5].get()
                    color = row[6].get()
                    line_width = float(row[7].get())
                    line_style = {'keine': ''}.get(row[8].get(), row[8].get())
                    marker = {'keine': ''}.get(row[9].get(), row[9].get())

                    ax.plot(x_data, y_data, label=legend_name, color=color, linewidth=line_width, linestyle=line_style, marker=marker)
                    visible_lines += 1

                    if self.plot_settings.get('linreg', False):
                        slope, intercept, r_value, _, _ = stats.linregress(x_data, y_data)
                        reg_line = slope * x_data + intercept
                        ax.plot(x_data, reg_line, color="black", linewidth=0.5, linestyle='-', label=f"LinReg ({legend_name})")

                        r_text = f"r = {r_value:.4f}"
                        corr_pos_map = {"oben rechts": (0.8, 0.95), "oben links": (0.1, 0.95), "unten rechts": (0.8, 0.1), "unten links": (0.1, 0.1)}
                        pos_x, pos_y = corr_pos_map.get(self.plot_settings.get('corr_pos', 'oben rechts'))
                        ax.text(pos_x, pos_y, r_text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))
                
                except Exception as e:
                    self.show_error(f"Fehler beim Plotten der Daten: {e}")
                    return None, None # Rückgabe bei Fehlern

        try:
            ax.set_xlabel(self.plot_settings['x_label'])
            ax.set_ylabel(self.plot_settings['y_label'])
        except Exception as e:
            self.show_error("Fehlerhafte LaTeX-Syntax in den Achsenbeschriftungen. Bitte überprüfen.")
            return None, None
        
        # Apply limits, scales, and ticks
        if self.plot_settings['x_min'] is not None and self.plot_settings['x_max'] is not None:
            ax.set_xlim([self.plot_settings['x_min'], self.plot_settings['x_max']])
        if self.plot_settings['y_min'] is not None and self.plot_settings['y_max'] is not None:
            ax.set_ylim([self.plot_settings['y_min'], self.plot_settings['y_max']])

        if self.plot_settings['invert_x_axis']:
            ax.invert_xaxis()
        if self.plot_settings.get('invert_y_axis', False):
            ax.invert_yaxis()

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

        if visible_lines > 1:
            try:
                legend_position_map = {"oben rechts": "upper right", "oben links": "upper left", "unten rechts": "lower right", "unten links": "lower left"}
                ax.legend(loc=legend_position_map.get(self.plot_settings['legend_position'], 'upper right'))
            except Exception as e:
                self.show_error("Fehlerhafte LaTeX-Syntax in der Legende. Bitte überprüfen.")
                return None, None
        
        return ax.figure, ax

    def plot_data(self):
        """Öffnet ein Fenster mit Plot und Einstellungsoptionen."""
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Plot")
        plot_window.geometry("1000x600")

        settings_frame = tk.Frame(plot_window, padx=10, pady=10)
        settings_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        def apply_settings():
            """Nimmt die Einstellungen aus der UI und aktualisiert den Plot."""
            def get_text_widget_value(text_widget):
                return text_widget.get("1.0", "end-1c").replace("\n", "")
            
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
            self.plot_settings['invert_y_axis'] = invert_y_axis_var.get()
            self.plot_settings['log_x_axis'] = log_x_axis_var.get()
            self.plot_settings['log_y_axis'] = log_y_axis_var.get()
            self.plot_settings['grid'] = grid_var.get()
            self.plot_settings['linreg'] = linreg_var.get()
            self.plot_settings['corr_pos'] = corr_pos_dropdown.get()
            
            try:
                self.plot_settings['x_ticks'] = self._parse_ticks(x_ticks_entry.get())
                self.plot_settings['y_ticks'] = self._parse_ticks(y_ticks_entry.get())
            except ValueError as ve:
                self.show_error(str(ve))
            
            self._update_plot_ui()

        # UI-Elemente für die Einstellungen
        tk.Button(settings_frame, text="Plot aktualisieren", command=apply_settings).pack(pady=10)
        tk.Label(settings_frame, text="X-axis Label:").pack(anchor="w")
        x_label_text = tk.Text(settings_frame, height=3, width=30, wrap="none")
        x_label_text.insert("1.0", self.plot_settings['x_label'])
        x_label_text.pack(anchor="w")
        tk.Label(settings_frame, text="Y-axis Label:").pack(anchor="w")
        y_label_text = tk.Text(settings_frame, height=3, width=30, wrap="none")
        y_label_text.insert("1.0", self.plot_settings['y_label'])
        y_label_text.pack(anchor="w")
        
        x_min_entry = self._create_setting_entry(settings_frame, "X Min:", self.plot_settings['x_min'])
        x_max_entry = self._create_setting_entry(settings_frame, "X Max:", self.plot_settings['x_max'])
        y_min_entry = self._create_setting_entry(settings_frame, "Y Min:", self.plot_settings['y_min'])
        y_max_entry = self._create_setting_entry(settings_frame, "Y Max:", self.plot_settings['y_max'])
        width_entry = self._create_setting_entry(settings_frame, "Width (cm):", self.plot_settings['width_cm'])
        height_entry = self._create_setting_entry(settings_frame, "Height (cm):", self.plot_settings['height_cm'])
        
        tk.Label(settings_frame, text="Legend Position:").pack(anchor="w")
        legend_position_dropdown = self._create_dropdown(settings_frame, ["oben rechts", "oben links", "unten rechts", "unten links"], 0, 0, default_value=self.plot_settings['legend_position'])
        legend_position_dropdown.pack(anchor="w")
        
        invert_x_axis_var = tk.BooleanVar(value=self.plot_settings['invert_x_axis'])
        tk.Checkbutton(settings_frame, text="Invert X-axis", variable=invert_x_axis_var).pack(anchor="w")
        invert_y_axis_var = tk.BooleanVar(value=self.plot_settings['invert_y_axis'])
        tk.Checkbutton(settings_frame, text="Invert Y-axis", variable=invert_y_axis_var).pack(anchor="w")
        log_x_axis_var = tk.BooleanVar(value=self.plot_settings['log_x_axis'])
        tk.Checkbutton(settings_frame, text="Logarithmic X-axis", variable=log_x_axis_var).pack(anchor="w")
        log_y_axis_var = tk.BooleanVar(value=self.plot_settings['log_y_axis'])
        tk.Checkbutton(settings_frame, text="Logarithmic Y-axis", variable=log_y_axis_var).pack(anchor="w")
        grid_var = tk.BooleanVar(value=self.plot_settings['grid'])
        tk.Checkbutton(settings_frame, text="Grid anzeigen", variable=grid_var).pack(anchor="w")
        linreg_var = tk.BooleanVar(value=self.plot_settings['linreg'])
        tk.Checkbutton(settings_frame, text="LinReg", variable=linreg_var).pack(anchor="w")
        tk.Label(settings_frame, text="Position Korrelationskoeffizient:").pack(anchor="w")
        corr_pos_dropdown = self._create_dropdown(settings_frame, ["oben rechts", "oben links", "unten rechts", "unten links"], 0, 0, default_value=self.plot_settings['corr_pos'])
        corr_pos_dropdown.pack(anchor="w")
        
        x_ticks_entry = self._create_setting_entry(settings_frame, "X Ticks (comma-separated):", ','.join(map(str, self.plot_settings['x_ticks'])) if self.plot_settings['x_ticks'] else "")
        y_ticks_entry = self._create_setting_entry(settings_frame, "Y Ticks (comma-separated):", ','.join(map(str, self.plot_settings['y_ticks'])) if self.plot_settings['y_ticks'] else "")
        
        self.plot_figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.plot_figure, master=plot_window)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self._update_plot_ui()

    def _create_setting_entry(self, frame, label_text, default_value):
        """Erstellt ein Label und ein Eingabefeld für die Plot-Einstellungen."""
        tk.Label(frame, text=label_text).pack(anchor="w")
        entry = tk.Entry(frame)
        entry.insert(0, str(default_value) if default_value is not None else "")
        entry.pack(anchor="w")
        return entry

    def _parse_ticks(self, ticks_input):
        """Parst die Eingabe für Ticks."""
        if not ticks_input.strip():
            return None
        try:
            if ":" in ticks_input:
                start, step, end = map(float, ticks_input.split(":"))
                return list(np.arange(start, end + step, step))
            else:
                return [float(tick) for tick in ticks_input.split(",") if tick.strip()]
        except ValueError as e:
            raise ValueError(f"Ungültiges Format für Ticks: '{ticks_input}'. Verwenden Sie 'start:step:end' oder eine durch Kommas getrennte Liste.")

    def _update_plot_ui(self):
        """Aktualisiert den Plot in der UI basierend auf den Einstellungen."""
        fig, ax = self._generate_plot_figure(self.ax)
        if fig and ax:
            self.canvas.draw()
    
    def export_tex(self):
        """Exportiert den Plot als TikZ/PGFPlots Code."""
        file_path = filedialog.asksaveasfilename(defaultextension=".tex", filetypes=[("TeX files", "*.tex")], initialfile="Plot.tex")
        if not file_path:
            return

        caption = self.caption_entry.get()
        label = self.label_entry.get()

        tikz_code = self._generate_tikz_code(caption, label)
        if tikz_code:
            with open(file_path, 'w') as tex_file:
                tex_file.write(tikz_code)
            messagebox.showinfo("Erfolg", "Die Datei wurde erfolgreich als .tex exportiert.")

    def _generate_tikz_code(self, caption, label):
        """Generiert den TikZ-Code basierend auf den Einstellungen."""
        try:
            width_cm = self.plot_settings['width_cm']
            height_cm = self.plot_settings['height_cm']
            legend_position_map = {"oben rechts": "north east", "oben links": "north west", "unten rechts": "south east", "unten links": "south west"}
            legend_position_tikz = legend_position_map.get(self.plot_settings['legend_position'], 'north east')

            tikz_code = f"""
        \\begin{{figure}}[H]
            \\centering
            \\begin{{tikzpicture}}
            \\begin{{axis}}[
                width={width_cm}cm,
                height={height_cm}cm,
                xlabel={{{self.plot_settings['x_label']}}},
                ylabel={{{self.plot_settings['y_label']}}},
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
            if self.plot_settings['x_ticks'] is not None:
                tikz_code += f", xtick={{{','.join(map(str, self.plot_settings['x_ticks']))}}}"
            if self.plot_settings['y_ticks'] is not None:
                tikz_code += f", ytick={{{','.join(map(str, self.plot_settings['y_ticks']))}}}"
            if self.plot_settings['invert_x_axis']:
                tikz_code += f", x dir=reverse"
            if self.plot_settings['invert_y_axis']:
                tikz_code += f", y dir=reverse"

            visible_lines = [row for row in self.rows if row[4].get() == "sichtbar"]
            if len(visible_lines) > 1:
                tikz_code += f", legend pos={legend_position_tikz}\n"
            
            tikz_code += "]\n"

            for row in visible_lines:
                df_x, df_y = self.dataframes[row[0].get()], self.dataframes[row[1].get()]
                x_data, y_data = df_x[row[2].get()].to_list(), df_y[row[3].get()].to_list()
                
                color = row[6].get()
                line_width = float(row[7].get())
                line_style = {'-': 'solid', '--': 'dashed', ':': 'dotted', 'keine': 'only marks'}.get(row[8].get(), 'solid')
                marker = {'keine': '', 'o': 'o', '+': '+', '^': 'triangle*', 's': 'square*'}.get(row[9].get(), '')
                legend_name = row[5].get()

                tikz_code += f"""
            \\addplot[
                color={color},
                line width={line_width}pt,
                mark={marker},
                style={line_style}
            ] coordinates {{
            {" ".join(f"({x},{y})" for x, y in zip(x_data, y_data))}
            }};"""
                if len(visible_lines) > 1 and legend_name:
                    tikz_code += f"\\addlegendentry{{{legend_name}}}\n"

                if self.plot_settings.get('linreg', False):
                    slope, intercept, r_value, _, _ = stats.linregress(x_data, y_data)
                    reg_line = [(x, slope * x + intercept) for x in x_data]
                    tikz_code += f"""
                \\addplot[color=black, line width=0.5pt, solid] coordinates {{
                {" ".join(f"({x},{y})" for x, y in reg_line)}}};"""

                    corr_pos_map = {"oben rechts": "(rel axis cs:0.9,0.9)", "oben links": "(rel axis cs:0.1,0.9)", "unten rechts": "(rel axis cs:0.9,0.1)", "unten links": "(rel axis cs:0.1,0.1)"}
                    tikz_pos = corr_pos_map.get(self.plot_settings.get('corr_pos', 'oben rechts'))
                    tikz_code += f"\\node[fill=white, draw, inner sep=3pt] at {tikz_pos} {{\\small $r = {r_value:.4f}$}};\n"

            tikz_code += """
        \\end{axis}
        \\end{tikzpicture}
        """
            if caption:
                tikz_code += f"\\caption{{{caption}}}\n"
            if label:
                tikz_code += f"\\label{{fig:{label}}}\n"
            tikz_code += "\\end{figure}"
            return tikz_code

        except Exception as e:
            self.show_error(f"Fehler beim Erstellen des TikZ-Codes: {e}")
            return None

    def export_plot(self, file_extension, file_format):
        """Generische Methode zum Exportieren des Plots als Bilddatei."""
        file_path = filedialog.asksaveasfilename(defaultextension=f".{file_extension}", filetypes=[(f"{file_extension.upper()} files", f"*.{file_extension}")], initialfile=f"Plot.{file_extension}")
        if not file_path:
            return

        width_inch = self.plot_settings['width_cm'] / 2.54
        height_inch = self.plot_settings['height_cm'] / 2.54

        fig, ax = plt.subplots(figsize=(width_inch, height_inch))
        
        self._generate_plot_figure(ax)

        fig.savefig(file_path, dpi=300, bbox_inches='tight', transparent=True, format=file_format)
        plt.close(fig)
        messagebox.showinfo("Erfolg", f"Der Plot wurde erfolgreich als {file_extension.upper()} gespeichert.")

    def export_png(self):
        """Exportiert den Plot als PNG-Datei."""
        self.export_plot("png", "png")

    def export_pdf(self):
        """Exportiert den Plot als PDF-Datei."""
        self.export_plot("pdf", "pdf")

    def plot_preview(self):
        """Zeigt eine interaktive Vorschau des Plots in einem separaten Fenster."""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Plot Vorschau")
        preview_window.geometry("800x600")

        fig, ax = self._generate_plot_figure(plt.subplots())
        if fig and ax:
            canvas = FigureCanvasTkAgg(fig, master=preview_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            toolbar = NavigationToolbar2Tk(canvas, preview_window)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            tk.Button(preview_window, text="Close", command=preview_window.destroy).pack(side=tk.BOTTOM, pady=10)

    def export_json_for_plot(self):
        """Speichert die sichtbaren Daten und Einstellungen in einer JSON-Datei."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile="plot_data.json")
        if not file_path:
            return

        visible_dataframes = {}
        visible_rows = []

        for row in self.rows:
            if row[4].get() == "sichtbar":
                selected_file_x, selected_file_y = row[0].get(), row[1].get()
                x_column, y_column = row[2].get(), row[3].get()

                if selected_file_x and selected_file_y and x_column and y_column:
                    if selected_file_x not in visible_dataframes:
                        visible_dataframes[selected_file_x] = self.dataframes[selected_file_x].to_dict()
                    if selected_file_y not in visible_dataframes:
                        visible_dataframes[selected_file_y] = self.dataframes[selected_file_y].to_dict()

                    visible_rows.append({
                        "file_x": selected_file_x, "file_y": selected_file_y,
                        "x_column": x_column, "y_column": y_column,
                        "visibility": "sichtbar",
                        "legend_name": row[5].get(),
                        "color": row[6].get(),
                        "line_width": row[7].get(),
                        "line_style": row[8].get(),
                        "marker": row[9].get()
                    })

        json_data = {
            "dataframes": visible_dataframes,
            "plot_settings": self.plot_settings,
            "rows": visible_rows
        }

        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        messagebox.showinfo("Erfolg", "Sichtbare Daten und Einstellungen als JSON exportiert.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PlotGOAT(root)
    root.mainloop()
