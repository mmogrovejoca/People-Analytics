import streamlit as st
import pandas as pd
import joblib
from io import BytesIO
from src.etl.data_loader import load_data
from src.etl.data_preprocessor import preprocess_data
from src.metrics.metrics_calculator import *
from src.visualization.plotter import *
from src.ml.model_trainer import prepare_data_for_model
from src.ml.clustering import cluster_terminated_employees, plot_clusters
from src.reporting.pdf_reporter import generate_pdf_report

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

    st.sidebar.header('Filtros')

    # Filtro por rango de fechas
    min_date = df_processed['FECHA_INGRESO'].min()
    max_date = datetime.now().date()
    start_date, end_date = st.sidebar.date_input(
        'Seleccionar Rango de Fechas',
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filtro por departamento
    departments = st.sidebar.multiselect(
        'Seleccionar Departamento(s)',
        options=df_processed['AREA'].unique(),
        default=df_processed['AREA'].unique()
    )

    # Aplicar filtros
    filtered_df = df_processed[
        (df_processed['FECHA_INGRESO'] >= start_date) & (df_processed['FECHA_INGRESO'] <= end_date) &
        (df_processed['AREA'].isin(departments))
    ]

    st.header('Datos de Empleados (Filtrados)')
    st.write(filtered_df.head())

    # Métricas
    st.header('Métricas de Rotación')
    period = st.selectbox('Seleccionar Periodo', ['Mes', 'Trimestre', 'Año'], index=0)
    period_map = {'Mes': 'M', 'Trimestre': 'Q', 'Año': 'Y'}

    hires = get_hires_by_period(filtered_df, period_map[period])
    terminations = get_terminations_by_period(filtered_df, period_map[period])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Contrataciones", hires.sum())
    with col2:
        st.metric("Total de Bajas", terminations.sum())

    # Visualizaciones
    st.header('Visualizaciones')

    def show_plot(plot_function, *args, **kwargs):
        fig = plot_function(*args, **kwargs)
        st.pyplot(fig)

        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="Descargar gráfico",
            data=buf.getvalue(),
            file_name=f"{plot_function.__name__}.png",
            mime="image/png"
        )

    show_plot(plot_hires_terminations_timeline, hires, terminations)

    st.subheader('Estacionalidad')
    show_plot(plot_seasonality, filtered_df, 'FECHA_INGRESO', 'Estacionalidad de Contrataciones')

    show_plot(plot_seasonality, filtered_df.dropna(subset=['FECHA_SALIDA']), 'FECHA_SALIDA', 'Estacionalidad de Bajas')

    st.subheader('Distribución de Antigüedad')
    tenure_dist = get_tenure_distribution(filtered_df)
    show_plot(plot_tenure_distribution, tenure_dist)

    st.subheader('Mapa de Calor de Rotación')
    show_plot(plot_turnover_heatmap, filtered_df)

    st.subheader('Análisis por Grupo')
    group_by_col = st.selectbox('Seleccionar Grupo', ['AREA', 'TIPO_CONTRATO'])

    if group_by_col:
        hires_by_group = get_metrics_by_group(filtered_df, group_by_col, get_hires_by_period, period='Y')
        st.write(f'Contrataciones por {group_by_col}:')
        st.dataframe(hires_by_group)

        terminations_by_group = get_metrics_by_group(filtered_df, group_by_col, get_terminations_by_period, period='Y')
        st.write(f'Bajas por {group_by_col}:')
        st.dataframe(terminations_by_group)

    st.subheader('Distribución de Motivos de Salida')
    termination_reasons = get_termination_reason_distribution(filtered_df)
    if not termination_reasons.empty:
        show_plot(plot_termination_reason_distribution, termination_reasons)
    else:
        st.info("No hay datos sobre los motivos de salida.")

    st.subheader('Análisis de Supervivencia')
    show_plot(plot_survival_curve, filtered_df)

    st.subheader('Clustering de Empleados Salientes')
    n_clusters = st.slider('Número de Clusters', 2, 10, 3)
    df_clustered = cluster_terminated_employees(filtered_df, n_clusters)
    show_plot(plot_clusters, df_clustered)
    st.write("Datos de Empleados Salientes con Clusters:")
    st.dataframe(df_clustered[['ID_EMPLEADO', 'DURACION_EMPLEO', 'AREA', 'cluster']])

    # Predicción
    if model is not None:
        st.header('Predicción del Estado de la Empresa')

        try:
            # Preparar datos para predicción
            model_data = prepare_data_for_model(filtered_df)

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

    # Generar reporte PDF
    if st.button('Generar Reporte PDF'):
        st.info("Generando reporte... por favor espere.")

        # Recolectar métricas y figuras
        metrics_to_report = {
            "Total de Contrataciones": hires.sum(),
            "Total de Bajas": terminations.sum(),
            "Tasa de Retención Anual (%)": get_retention_rate(df_processed, 'Y').iloc[-1] if not get_retention_rate(df_processed, 'Y').empty else 'N/A',
            "Antigüedad Promedio (días)": get_average_tenure(df_processed)
        }

        figures_to_report = {
            "Línea de Tiempo de Contrataciones y Bajas": plot_hires_terminations_timeline(hires, terminations),
            "Distribución de Antigüedad": plot_tenure_distribution(get_tenure_distribution(df_processed)),
            "Mapa de Calor de Rotación": plot_turnover_heatmap(df_processed),
            "Distribución de Motivos de Salida": plot_termination_reason_distribution(get_termination_reason_distribution(df_processed)),
            "Curva de Supervivencia": plot_survival_curve(df_processed)
        }

        pdf_bytes = generate_pdf_report(df_processed, metrics_to_report, figures_to_report)

        st.download_button(
            label="Descargar Reporte PDF",
            data=pdf_bytes,
            file_name="reporte_rotacion.pdf",
            mime="application/pdf"
        )
