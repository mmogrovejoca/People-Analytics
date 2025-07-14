import streamlit as st
import pandas as pd
import joblib
from src.etl.data_loader import load_data
from src.etl.data_preprocessor import preprocess_data
from src.metrics.metrics_calculator import *
from src.visualization.plotter import *
from src.ml.model_trainer import prepare_data_for_model
from src.ml.clustering import cluster_terminated_employees, plot_clusters

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

    st.subheader('Análisis por Grupo')
    group_by_col = st.selectbox('Seleccionar Grupo', ['AREA', 'TIPO_CONTRATO'])

    if group_by_col:
        hires_by_group = get_metrics_by_group(df_processed, group_by_col, get_hires_by_period, period='Y')
        st.write(f'Contrataciones por {group_by_col}:')
        st.dataframe(hires_by_group)

        terminations_by_group = get_metrics_by_group(df_processed, group_by_col, get_terminations_by_period, period='Y')
        st.write(f'Bajas por {group_by_col}:')
        st.dataframe(terminations_by_group)

    st.subheader('Distribución de Motivos de Salida')
    termination_reasons = get_termination_reason_distribution(df_processed)
    if not termination_reasons.empty:
        plot_termination_reason_distribution(termination_reasons)
        st.pyplot(plt)
    else:
        st.info("No hay datos sobre los motivos de salida.")

    st.subheader('Análisis de Supervivencia')
    plot_survival_curve(df_processed)
    st.pyplot(plt)

    st.subheader('Clustering de Empleados Salientes')
    n_clusters = st.slider('Número de Clusters', 2, 10, 3)
    df_clustered = cluster_terminated_employees(df_processed, n_clusters)
    plot_clusters(df_clustered)
    st.pyplot(plt)
    st.write("Datos de Empleados Salientes con Clusters:")
    st.dataframe(df_clustered[['ID_EMPLEADO', 'DURACION_EMPLEO', 'AREA', 'cluster']])

    # Predicción
    if model is not None:
        st.header('Predicción del Estado de la Empresa')

        try:
            # Preparar datos para predicción
            model_data = prepare_data_for_model(df_processed)

            if not model_data.empty:
                st.subheader("Comparación de Modelos")

                # Re-entrenar y evaluar para mostrar resultados
                from src.ml.model_trainer import train_and_evaluate_models
                results = train_and_evaluate_models(model_data)

                for name, result in results.items():
                    st.write(f"**{name}**")
                    st.text(f"Accuracy: {result['accuracy']:.4f}")
                    st.text(result['classification_report'])

                # Usar la última fila para la predicción con el mejor modelo
                last_period_features = model_data.drop('status', axis=1).iloc[-1].values.reshape(1, -1)

                # Convertir la predicción numérica a etiqueta
                y_pred_encoded = model.predict(last_period_features)

                # Cargar las clases guardadas o re-factorizar
                _, class_names = pd.factorize(model_data['status'], sort=True)
                prediction = class_names[y_pred_encoded][0]

                st.success(f'El estado predicho para el próximo período es: **{prediction}**')
            else:
                st.warning("No hay suficientes datos para hacer una predicción.")
        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")

else:
    st.info("Por favor, cargue un archivo CSV para comenzar.")
