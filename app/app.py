from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import logging
import json
from datetime import datetime

# Ruta del modelo como constante
MODEL_PATH = 'static/model/logistic_model_with_columns.pkl'

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración para logging
LOG_FILE = "logs/api_logs.json"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(message)s'
)

def log_request(data):
    """Registrar las peticiones en un archivo de logs."""
    with open(LOG_FILE, "a") as log:
        log.write(json.dumps(data) + "\n")

def load_model():
    """Cargar el modelo y las columnas desde el archivo."""
    with open(MODEL_PATH, 'rb') as file:
        return pickle.load(file)

# Ruta principal
@app.route('/')
def home():
    try:
        # Cargar columnas del modelo
        data = load_model()
        columnas = data['columnas']
        print(f'columnas:{columnas}')
        return render_template('index.html', columns=columnas)
    except Exception as e:
        return f"Error loading model: {e}", 500

# Ruta para predicción
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Cargar el modelo y las columnas
        data = load_model()
        model = data['modelo']
        columnas = data['columnas']

        # Recoger datos del formulario
        input_data = {col: float(request.form[col]) for col in columnas}
        print(f'valor de datos de entrada:{input_data}')

        # Convertir a DataFrame
        df = pd.DataFrame([input_data])

        # Asegurar el orden correcto de las columnas
        df = df[columnas]

        # Realizar predicción
        prediction = model.predict(df)

        # Registrar la solicitud y el resultado
        log_request({
            'timestamp': datetime.now().isoformat(),
            'input_data': input_data,
            'prediction': int(prediction[0])
        })

        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        # Registrar el error
        log_request({
            'timestamp': datetime.now().isoformat(),
            'input_data': request.form.to_dict(),
            'error': str(e)
        })
        return jsonify({'error': str(e)}), 500

@app.route('/columns', methods=['GET'])
def get_columns():
    try:
        data = load_model()
        return jsonify({'columns': data['columnas']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
