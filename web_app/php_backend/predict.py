import sys
import pandas as pd
import joblib
import json

# Añadir la ruta a los módulos de la lógica de negocio
sys.path.insert(0, 'src')

from src.etl.data_preprocessor import preprocess_data
from src.ml.model_trainer import prepare_data_for_model

def predict(data_json):
    try:
        # Cargar el modelo
        model = joblib.load('../../model.joblib') # Ajustar ruta

        # Cargar y preprocesar los datos
        df = pd.read_json(data_json)
        df_processed = preprocess_data(df)

        # Preparar datos para el modelo
        model_data = prepare_data_for_model(df_processed)

        if not model_data.empty:
            last_period_features = model_data.drop('status', axis=1).iloc[-1].values.reshape(1, -1)

            y_pred_encoded = model.predict(last_period_features)

            _, class_names = pd.factorize(model_data['status'], sort=True)
            prediction = class_names[y_pred_encoded][0]

            print(json.dumps({'prediction': prediction}))
        else:
            print(json.dumps({'prediction': 'No hay suficientes datos para predecir'}))

    except Exception as e:
        print(json.dumps({'error': str(e)}))

if __name__ == '__main__':
    # Los datos se pasarán como un string JSON en el primer argumento
    predict(sys.argv[1])
