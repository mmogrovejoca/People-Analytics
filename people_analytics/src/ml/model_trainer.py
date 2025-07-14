import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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

def train_and_save_model(model_df, model_path='model.joblib'):
    """
    Entrena un modelo de clasificación y lo guarda en un archivo.

    Args:
        model_df (pandas.DataFrame): DataFrame con los datos para el entrenamiento.
        model_path (str): Ruta donde se guardará el modelo.
    """
    X = model_df.drop('status', axis=1)
    y = model_df['status']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Entrenar el modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Guardar el modelo
    joblib.dump(model, model_path)
    print(f"Modelo guardado en {model_path}")
