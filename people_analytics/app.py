import streamlit as st
import pandas as pd
import joblib
from src.etl.data_loader import load_data
from src.etl.data_preprocessor import preprocess_data
from src.metrics.metrics_calculator import *
from src.visualization.plotter import *
from src.ml.model_trainer import prepare_data_for_model

# Cargar modelo
try:
    model = joblib.load('model.joblib')
except FileNotFoundError:
    st.error("No se encontró el archivo del modelo. Por favor, entrene el modelo primero.")
    model = None

st.title('Análisis de Rotación de Personal y Predicción del Estado de la Empresa')

# Carga de datos
uploaded_file = st.sidebar.file_uploader("Cargar archivo CSV", type=['csv'])
if uploaded_file is not None:
    df = load_data(uploaded_file)
    df_processed = preprocess_data(df.copy())

    st.header('Datos de Empleados')
    st.write(df_processed.head())

    # Métricas
    st.header('Métricas de Rotación')
    period = st.selectbox('Seleccionar Periodo', ['Mes', 'Trimestre', 'Año'], index=0)
    period_map = {'Mes': 'M', 'Trimestre': 'Q', 'Año': 'Y'}

    hires = get_hires_by_period(df_processed, period_map[period])
    terminations = get_terminations_by_period(df_processed, period_map[period])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Contrataciones", hires.sum())
    with col2:
        st.metric("Total de Bajas", terminations.sum())

    # Visualizaciones
    st.header('Visualizaciones')
    plot_hires_terminations_timeline(hires, terminations)
    st.pyplot(plt)

    st.subheader('Estacionalidad')
    plot_seasonality(df_processed, 'FECHA_INGRESO', 'Estacionalidad de Contrataciones')
    st.pyplot(plt)

    plot_seasonality(df_processed.dropna(subset=['FECHA_SALIDA']), 'FECHA_SALIDA', 'Estacionalidad de Bajas')
    st.pyplot(plt)

    st.subheader('Distribución de Antigüedad')
    tenure_dist = get_tenure_distribution(df_processed)
    plot_tenure_distribution(tenure_dist)
    st.pyplot(plt)

    st.subheader('Mapa de Calor de Rotación')
    plot_turnover_heatmap(df_processed)
    st.pyplot(plt)

    # Predicción
    if model is not None:
        st.header('Predicción del Estado de la Empresa')

        try:
            # Preparar datos para predicción
            model_data = prepare_data_for_model(df_processed)

            if not model_data.empty:
                # Usar la última fila para la predicción
                last_period_features = model_data.drop('status', axis=1).iloc[-1].values.reshape(1, -1)

                prediction = model.predict(last_period_features)
                st.success(f'El estado predicho para el próximo período es: **{prediction[0]}**')
            else:
                st.warning("No hay suficientes datos para hacer una predicción.")
        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")

else:
    st.info("Por favor, cargue un archivo CSV para comenzar.")
