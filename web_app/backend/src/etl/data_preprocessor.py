import pandas as pd
from datetime import datetime

def preprocess_data(df):
    """
    Realiza el preprocesamiento de los datos de los empleados.

    Args:
        df (pandas.DataFrame): El DataFrame con los datos de los empleados.

    Returns:
        pandas.DataFrame: El DataFrame preprocesado.
    """
    if df is None:
        return None

    # Convertir columnas de fecha a datetime
    df['FECHA_INGRESO'] = pd.to_datetime(df['FECHA_INGRESO'])
    df['FECHA_SALIDA'] = pd.to_datetime(df['FECHA_SALIDA'])

    # Calcular la duración del empleo
    # Si la fecha de salida es nula, el empleado sigue activo. Usamos la fecha actual para el cálculo.
    df['DURACION_EMPLEO'] = (df['FECHA_SALIDA'].fillna(datetime.now()) - df['FECHA_INGRESO']).dt.days

    # Extraer mes y año
    df['MES_INGRESO'] = df['FECHA_INGRESO'].dt.month
    df['ANIO_INGRESO'] = df['FECHA_INGRESO'].dt.year
    df['MES_SALIDA'] = df['FECHA_SALIDA'].dt.month
    df['ANIO_SALIDA'] = df['FECHA_SALIDA'].dt.year

    return df
