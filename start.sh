#!/bin/bash

# Inicia el servidor Flask con Gunicorn
gunicorn --chdir app app:app -w 2 -b 0.0.0.0:5000 &

# Inicia el servidor Streamlit
streamlit run /app/dashboard.py --server.port=8501 --server.address=0.0.0.0
