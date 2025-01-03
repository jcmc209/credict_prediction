# Documentación del Proyecto: Predicción de Préstamos

Este documento detalla la estructura, funcionalidad y uso de la aplicación desarrollada, que consta de una API (usando Flask) y un dashboard interactivo (usando Streamlit). La aplicación permite realizar predicciones sobre un modelo de regresión logística previamente entrenado.

---

## **1. Estructura del Proyecto**

La estructura del proyecto es la siguiente:

```plaintext
creditPrediction/
├── app/
│   ├── app.py                # Código principal de la API Flask
│   ├── templates/            # Plantillas HTML para la API
│   │   └── index.html        # Formulario HTML
│   ├── static/
│   │   └── model/            # Archivo del modelo
│   │       └── logistic_model_with_columns.pkl
│   └── logs/                 # Carpeta de logs
│       └── api_logs.json     # Logs de las solicitudes
├── dashboard.py              # Código del dashboard interactivo (Streamlit)
├── Dockerfile                # Archivo Docker para construir la imagen
├── docker-compose.yml        # Configuración de Docker Compose
├── requirements.txt          # Dependencias del proyecto
├── start.sh                  # Script para iniciar API y dashboard
└── README.md                 # Documentación del proyecto
```

---

## **2. Descripción del Código**

### **2.1. API Flask (`app/app.py`)**

#### **EndPoints**

1. **`GET /`**

   - Ruta principal que renderiza el formulario HTML para ingresar los datos necesarios para realizar la predicción.
   - Dinámicamente genera los campos del formulario basándose en las columnas requeridas por el modelo.

2. **`POST /predict`**
   - Recibe los datos ingresados en el formulario HTML.
   - Carga el modelo entrenado desde `static/model/logistic_model_with_columns.pkl`.
   - Procesa los datos recibidos y realiza una predicción.
   - Devuelve la predicción como un objeto JSON o un error si algo falla.

2. **`GET /columns`**
   - Devuelve los datos de las columnas del modelo, con las cual se monta el formulario de datos entrada.

#### **Funciones Principales**

- **`load_model()`**:
  Carga el modelo y las columnas necesarias desde el archivo pickle (`.pkl`).

- **`log_request(data)`**:
  Guarda cada solicitud (datos de entrada, predicciones, y errores) en un archivo de logs (`logs/api_logs.json`).

---

### **2.2. Dashboard Streamlit (`dashboard.py`)**

#### **Funcionalidades**

1. **Formulario de Entrada de Datos**:

   - Permite a los usuarios ingresar datos y enviarlos al endpoint `/predict` de la API Flask.
   - Muestra la predicción generada por el modelo directamente en la interfaz del dashboard.

2. **Visualización de Métricas**:
   - Muestra el número total de solicitudes realizadas, predicciones exitosas y errores registrados.
   - Presenta un registro detallado de todas las solicitudes en formato tabular.
   - Genera gráficos de distribución de las predicciones.

#### **Estructura del Dashboard**

El dashboard está dividido en dos pestañas:

1. **Formulario de Predicción**:

   - Incluye un formulario que envía datos al servidor Flask.
   - Muestra los resultados devueltos por la API.

2. **Dashboard de Métricas**:
   - Incluye:
     - Estadísticas generales (total de solicitudes, predicciones exitosas, errores).
     - Registros de solicitudes (inputs, predicciones, errores).
     - Gráficos interactivos.

---

## **3. Manual de Usuario**

### **Requisitos Previos**

1. **Instalaciones Necesarias**:

   - Docker y Docker Compose.

2. **Archivos y Configuración**:
   - El archivo del modelo (`logistic_model_with_columns.pkl`) debe estar ubicado en `static/model/`.
   - Los archivos necesarios (como `start.sh` y `Dockerfile`) deben estar en las ubicaciones correspondientes.

---

### **Pasos para Iniciar la Aplicación**

1. **Construir la Imagen Docker**
   Desde la carpeta principal del proyecto, ejecuta:

   ```bash
   docker compose build
   ```

2. **Levantar los Servicios**
   Ejecuta el siguiente comando:

   ```bash
   docker compose up
   ```

3. **Acceso a la Aplicación**

   - API Flask: [http://localhost:5000](http://localhost:5000)
   - Dashboard Streamlit: [http://localhost:8501](http://localhost:8501)

4. **Detener los Servicios**
   Para detener todos los servicios, usa:
   ```bash
   docker compose down
   ```

---

## **4. Detalles Técnicos**

### **Requerimientos del Sistema**

- Python 3.9 o superior.
- Docker y Docker Compose.
- Al menos 4 GB de RAM.

### **Dependencias del Proyecto**

Las dependencias del proyecto se encuentran listadas en el archivo `requirements.txt`:

```plaintext
Flask==2.2.3
pandas==1.3.5
gunicorn==20.1.0
streamlit==1.25.0
scikit-learn==1.0.2
requests==2.28.2
```

Instaladas automáticamente durante la construcción del contenedor.

---
## **5. Manual de Usuario**

Para levantar la aplicación en local necesitaremos ejecutar el siguiente comando sobre la raiz del proyecto:
  ```bash
   docker compose build
   ```
Esto lanzará el proceso de instalación de dependencias y construcción de la aplicación, una vez terminado
ejcutar el siguiente comando para levantar la app.
  ```bash
   docker compose up
   ```
Ahora con poner en el buscador localhost:8501, dispondremos de la aplicación lista para usarla.

