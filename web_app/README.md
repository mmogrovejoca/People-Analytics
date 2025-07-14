# People Analytics: Aplicación Web de Análisis de Rotación

Esta es una aplicación web completa para el análisis y la predicción de la rotación de personal. La aplicación ha sido desarrollada con una arquitectura de backend y frontend separados, utilizando Flask para el backend y HTML, CSS y JavaScript para el frontend.

## Características Principales

- **Dashboard Interactivo:** Visualiza las métricas clave de rotación de un vistazo.
- **Análisis Profundo:** Explora los datos con filtros por rango de fechas y departamento.
- **Visualizaciones Dinámicas:** Gráficos interactivos que se actualizan en tiempo real.
- **Predicción de Estado:** Utiliza un modelo de Machine Learning para predecir el estado futuro de la empresa.
- **Generación de Reportes:** Descarga reportes en PDF con un resumen de los análisis.
- **Análisis Avanzados:** Incluye análisis de motivos de salida, análisis de supervivencia y clustering de empleados.

## Estructura del Proyecto

- `backend/`: Contiene la lógica del backend desarrollada con Flask.
  - `src/`: Módulos de la lógica de negocio (ETL, métricas, ML, etc.).
  - `data/`: Datos de entrada.
  - `model.joblib`: Modelo de Machine Learning entrenado.
  - `app.py`: Aplicación principal de Flask.
- `frontend/`: Contiene los archivos del frontend.
  - `static/`: Archivos estáticos (CSS, JavaScript).
  - `templates/`: Plantillas HTML.
- `requirements.txt`: Dependencias del proyecto.

## Cómo Utilizar la Aplicación

### 1. Requisitos Previos

Asegúrate de tener Python 3 y pip instalados en tu sistema.

### 2. Instalación

1.  Clona este repositorio en tu máquina local.
2.  Navega al directorio `web_app`.
3.  Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Ejecución

1.  Abre una terminal y navega al directorio `web_app/backend`.
2.  Ejecuta la aplicación de Flask:
    ```bash
    python app.py
    ```
3.  Abre tu navegador web y visita la siguiente dirección:
    ```
    http://127.0.0.1:5000
    ```

### 4. Uso de la Interfaz

- **Dashboard Principal:** Al cargar la aplicación, verás un dashboard con las métricas más importantes y los gráficos principales.
- **Filtros:** En la barra lateral izquierda, puedes utilizar los filtros para seleccionar un rango de fechas y los departamentos que deseas analizar. Los datos y los gráficos se actualizarán automáticamente.
- **Predicción:** Haz clic en el botón "Predecir Estado" en la barra lateral para obtener una predicción del estado de la empresa para el próximo período, basada en los datos filtrados.
- **Reporte en PDF:** Haz clic en el botón "Generar Reporte PDF" para descargar un reporte completo con las métricas y los gráficos del análisis actual.
- **Carga de Datos:** Para utilizar tus propios datos, reemplaza el archivo `sample_data.csv` en la carpeta `web_app/backend/data` con tu propio archivo CSV, asegurándote de que tenga el mismo formato.
