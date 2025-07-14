import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def define_company_status(hires, terminations, threshold=0.05):
    """
    Define el estado de la empresa en función de las contrataciones y bajas.

    Args:
        hires (int): Número de contrataciones en el período.
        terminations (int): Número de bajas en el período.
        threshold (float): Umbral para determinar si la rotación es alta o baja.

    Returns:
        str: El estado de la empresa ('Estable', 'En riesgo', 'En expansión', 'En contracción').
    """
    if hires > terminations * (1 + threshold):
        return 'En expansión'
    elif terminations > hires * (1 + threshold):
        return 'En contracción'
    elif terminations / (hires + 1) > threshold: # Evitar división por cero
        return 'En riesgo'
    else:
        return 'Estable'

def prepare_data_for_model(df, period='M'):
    """
    Prepara los datos para el entrenamiento del modelo de predicción.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
        period (str): El período para agrupar ('M' para mes, 'Q' para trimestre, 'Y' para año).

    Returns:
        pandas.DataFrame: Un DataFrame listo para el entrenamiento del modelo.
    """
    from metrics.metrics_calculator import get_hires_by_period, get_terminations_by_period, get_turnover_rate

    hires = get_hires_by_period(df, period)
    terminations = get_terminations_by_period(df, period)
    turnover = get_turnover_rate(df, period)

    # Crear el DataFrame para el modelo
    model_df = pd.DataFrame({'hires': hires, 'terminations': terminations, 'turnover': turnover})

    # Añadir el número de empleados al inicio del período como característica
    all_dates = pd.to_datetime(df['FECHA_INGRESO']).tolist() + pd.to_datetime(df['FECHA_SALIDA'].dropna()).tolist()
    date_range = pd.date_range(start=min(all_dates), end=max(all_dates), freq=period)

    employees_at_start = []
    for i in range(len(date_range) - 1):
        start_date = date_range[i]
        employees = df[(df['FECHA_INGRESO'] <= start_date) & ((df['FECHA_SALIDA'] > start_date) | (df['FECHA_SALIDA'].isnull()))].shape[0]
        employees_at_start.append(employees)

    model_df['employees_at_start'] = pd.Series(employees_at_start, index=date_range[:-1])

    # Crear lag features
    for i in range(1, 4):
        model_df[f'hires_lag_{i}'] = model_df['hires'].shift(i)
        model_df[f'terminations_lag_{i}'] = model_df['terminations'].shift(i)

    model_df = model_df.dropna()

    # Definir el estado de la empresa
    model_df['status'] = model_df.apply(lambda row: define_company_status(row['hires'], row['terminations']), axis=1)

    return model_df

def train_and_evaluate_models(model_df):
    """
    Entrena y evalúa diferentes modelos de clasificación.

    Args:
        model_df (pandas.DataFrame): DataFrame con los datos para el entrenamiento.

    Returns:
        dict: Un diccionario con los modelos entrenados y sus métricas.
    """
    X = model_df.drop('status', axis=1)
    y = model_df['status']

    # Convertir etiquetas a números
    y, class_names = pd.factorize(y, sort=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=class_names)

        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'classification_report': report
        }
        print(f"--- {name} ---")
        print("Accuracy:", accuracy)
        print("Classification Report:\n", report)

    return results

def save_best_model(results, model_path='model.joblib'):
    """
    Guarda el mejor modelo en un archivo.

    Args:
        results (dict): Diccionario con los resultados de los modelos.
        model_path (str): Ruta donde se guardará el modelo.
    """
    best_model_name = max(results, key=lambda name: results[name]['accuracy'])
    best_model = results[best_model_name]['model']

    joblib.dump(best_model, model_path)
    print(f"Mejor modelo ({best_model_name}) guardado en {model_path}")
