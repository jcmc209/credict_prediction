import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# URL de la API Flask (actualiza si usas una URL distinta)
FLASK_API_URL = "http://localhost:5000/predict"

# Inicializar el estado de métricas en Streamlit
if "metrics" not in st.session_state:
    st.session_state["metrics"] = {
        "total_requests": 0,
        "successful_predictions": 0,
        "errors": 0,
        "logs": []
    }

# Título del Dashboard
st.title("Modelo de Predicción - Dashboard")

# Tabs para el formulario y las métricas
tab1, tab2 = st.tabs(["Formulario de Predicción", "Dashboard de Métricas"])

### Tab 1: Formulario de Predicción
with tab1:
    st.subheader("Formulario de Entrada de Datos")

    # Primero obtenemos las columnas del modelo haciendo una petición GET a la ruta principal
    try:
        response = requests.get("http://localhost:5000/columns")
        if response.status_code == 200:
            columns = response.json()['columns']
        else:
            st.error("No se pudieron obtener las columnas del modelo")
            columns = []
    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
        columns = []

    # Crear un formulario para los datos de entrada
    with st.form("prediction_form"):
        # Crear campos dinámicamente basados en las columnas del modelo
        input_data = {}
        for column in columns:
            input_data[column] = st.number_input(f"{column}", value=0.0)

        # Botón de envío
        submitted = st.form_submit_button("Hacer Predicción")

        if submitted:
            try:
                # Enviar los datos a la API Flask
                response = requests.post(FLASK_API_URL, data=input_data)
                response_data = response.json()

                # Actualizar métricas
                st.session_state["metrics"]["total_requests"] += 1

                if "prediction" in response_data:
                    st.session_state["metrics"]["successful_predictions"] += 1
                    st.session_state["metrics"]["logs"].append({
                        "timestamp": datetime.now().isoformat(),
                        "input_data": input_data,
                        "prediction": response_data["prediction"]
                    })
                    st.success(f"Predicción: {response_data['prediction']}")
                else:
                    st.session_state["metrics"]["errors"] += 1
                    st.session_state["metrics"]["logs"].append({
                        "timestamp": datetime.now().isoformat(),
                        "input_data": input_data,
                        "error": response_data.get("error", "Error desconocido")
                    })
                    st.error(f"Error: {response_data.get('error', 'Error desconocido')}")
            except Exception as e:
                st.session_state["metrics"]["errors"] += 1
                st.session_state["metrics"]["logs"].append({
                    "timestamp": datetime.now().isoformat(),
                    "input_data": input_data,
                    "error": str(e)
                })
                st.error(f"Error conectando con la API: {e}")

### Tab 2: Dashboard de Métricas
with tab2:
    st.subheader("Métricas de la API")

    # Mostrar estadísticas generales
    st.metric("Total de Solicitudes", st.session_state["metrics"]["total_requests"])
    st.metric("Predicciones Exitosas", st.session_state["metrics"]["successful_predictions"])
    st.metric("Errores", st.session_state["metrics"]["errors"])

    # Tabla de logs
    st.write("Historial de Logs")
    if st.session_state["metrics"]["logs"]:
        log_df = pd.DataFrame(st.session_state["metrics"]["logs"])
        st.dataframe(log_df)
    else:
        st.write("No hay logs disponibles aún.")

    # Gráfica de distribución de predicciones
    st.subheader("Distribución de Predicciones")
    if st.session_state["metrics"]["logs"]:
        predictions = [
            log["prediction"] for log in st.session_state["metrics"]["logs"] if "prediction" in log
        ]
        if predictions:
            st.bar_chart(pd.Series(predictions).value_counts())
        else:
            st.write("No hay predicciones disponibles.")
