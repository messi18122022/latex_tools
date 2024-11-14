from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PLOT_FOLDER'] = 'static/plots/'  # Ordner für gespeicherte Diagramme

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['PLOT_FOLDER']):
    os.makedirs(app.config['PLOT_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Erzeuge Diagramm
        plot_filename = create_plot(file_path)
        
        # Zeige das Diagramm dem Benutzer an
        return render_template('index.html', plot_url=url_for('static', filename=f'plots/{plot_filename}'))

def create_plot(file_path):
    # Daten laden und Diagramm erstellen
    df = pd.read_csv(file_path)  # Annahme: es ist eine CSV-Datei
    plt.figure()
    df.plot()  # Einfache Diagrammfunktion für die gesamte Tabelle
    
    plot_filename = 'plot.png'
    plot_path = os.path.join(app.config['PLOT_FOLDER'], plot_filename)
    plt.savefig(plot_path)  # Diagramm als PNG speichern
    plt.close()  # Diagramm schließen, um Speicher freizugeben
    
    return plot_filename

if __name__ == "__main__":
    app.run(debug=True)
