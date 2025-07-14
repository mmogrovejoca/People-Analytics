import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
import pandas as pd
import joblib
from io import BytesIO

# Importar módulos de la lógica de negocio
from backend.src.etl.data_loader import load_data
from backend.src.etl.data_preprocessor import preprocess_data
from backend.src.metrics.metrics_calculator import *
from backend.src.ml.model_trainer import prepare_data_for_model
from backend.src.reporting.pdf_reporter import generate_pdf_report
from backend.src.visualization import plotter # Importar el módulo plotter

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# Cargar modelo
try:
    model = joblib.load('model.joblib')
except FileNotFoundError:
    model = None

# Cargar y preprocesar datos al inicio
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sample_data.csv')
df = load_data(DATA_PATH)
df_processed = preprocess_data(df.copy())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'El backend funciona!'})

@app.route('/api/metrics', methods=['POST'])
def get_metrics():
    filters = request.json
    filtered_df = apply_filters(df_processed, filters)

    period = filters.get('period', 'M')

    hires = get_hires_by_period(filtered_df, period)
    terminations = get_terminations_by_period(filtered_df, period)

    metrics = {
        'total_hires': int(hires.sum()),
        'total_terminations': int(terminations.sum()),
        'retention_rate': get_retention_rate(filtered_df, 'Y').iloc[-1] if not get_retention_rate(filtered_df, 'Y').empty else 'N/A',
        'average_tenure': get_average_tenure(filtered_df)
    }

    return jsonify(metrics)

def apply_filters(df, filters):
    # Lógica para aplicar filtros al dataframe
    # (se implementará en el siguiente paso)
    df_copy = df.copy()

    if 'start_date' in filters and 'end_date' in filters and filters['start_date'] and filters['end_date']:
        start_date = pd.to_datetime(filters['start_date'])
        end_date = pd.to_datetime(filters['end_date'])
        df_copy = df_copy[(df_copy['FECHA_INGRESO'] >= start_date) & (df_copy['FECHA_INGRESO'] <= end_date)]

    if 'departments' in filters and filters['departments']:
        df_copy = df_copy[df_copy['AREA'].isin(filters['departments'])]

    return df_copy

@app.route('/api/chart-data', methods=['POST'])
def get_chart_data():
    filters = request.json
    chart_type = filters.get('chart_type')
    filtered_df = apply_filters(df_processed, filters)

    if chart_type == 'hires_terminations_timeline':
        period = filters.get('period', 'M')
        hires = get_hires_by_period(filtered_df, period)
        terminations = get_terminations_by_period(filtered_df, period)
        data = {
            'labels': hires.index.strftime('%Y-%m').tolist(),
            'hires': hires.values.tolist(),
            'terminations': terminations.values.tolist()
        }
        return jsonify(data)

    if chart_type == 'termination_reason_distribution':
        reasons = get_termination_reason_distribution(filtered_df)
        data = {
            'labels': reasons.index.tolist(),
            'values': reasons.values.tolist()
        }
        return jsonify(data)

    # Añadir más tipos de gráficos aquí...

    return jsonify({'error': 'Chart type not found'}), 404

@app.route('/api/predict', methods=['POST'])
def predict_status():
    if model is None:
        return jsonify({'error': 'Modelo no encontrado'}), 500

    filters = request.json
    filtered_df = apply_filters(df_processed, filters)

    try:
        model_data = prepare_data_for_model(filtered_df)
        if not model_data.empty:
            last_period_features = model_data.drop('status', axis=1).iloc[-1].values.reshape(1, -1)

            y_pred_encoded = model.predict(last_period_features)

            _, class_names = pd.factorize(model_data['status'], sort=True)
            prediction = class_names[y_pred_encoded][0]

            return jsonify({'prediction': prediction})
        else:
            return jsonify({'prediction': 'No hay suficientes datos para predecir'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report', methods=['POST'])
def generate_report():
    filters = request.json
    filtered_df = apply_filters(df_processed, filters)

    period = filters.get('period', 'M')
    hires = get_hires_by_period(filtered_df, period)
    terminations = get_terminations_by_period(filtered_df, period)

    metrics_to_report = {
        "Total de Contrataciones": hires.sum(),
        "Total de Bajas": terminations.sum(),
        "Tasa de Retención Anual (%)": get_retention_rate(filtered_df, 'Y').iloc[-1] if not get_retention_rate(filtered_df, 'Y').empty else 'N/A',
        "Antigüedad Promedio (días)": get_average_tenure(filtered_df)
    }

    figures_to_report = {
        "Línea de Tiempo de Contrataciones y Bajas": plotter.plot_hires_terminations_timeline(hires, terminations),
        "Distribución de Antigüedad": plotter.plot_tenure_distribution(get_tenure_distribution(filtered_df)),
    }

    pdf_bytes = generate_pdf_report(filtered_df, metrics_to_report, figures_to_report)

    return send_file(
        BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='reporte_rotacion.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
