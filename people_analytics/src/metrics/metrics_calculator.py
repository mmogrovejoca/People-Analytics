import pandas as pd

def get_hires_by_period(df, period='M'):
    """
    Calcula el número total de contrataciones por período.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
        period (str): El período para agrupar ('M' para mes, 'Q' para trimestre, 'Y' para año).

    Returns:
        pandas.Series: Una serie con el número de contrataciones por período.
    """
    df_copy = df.copy()
    df_copy['FECHA_INGRESO'] = pd.to_datetime(df_copy['FECHA_INGRESO'])
    df_copy = df_copy.set_index('FECHA_INGRESO')
    return df_copy.resample(period).size()

def get_terminations_by_period(df, period='M'):
    """
    Calcula el número total de bajas por período.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
        period (str): El período para agrupar ('M' para mes, 'Q' para trimestre, 'Y' para año).

    Returns:
        pandas.Series: Una serie con el número de bajas por período.
    """
    df_copy = df.copy()
    df_copy = df_copy.dropna(subset=['FECHA_SALIDA'])
    df_copy['FECHA_SALIDA'] = pd.to_datetime(df_copy['FECHA_SALIDA'])
    df_copy = df_copy.set_index('FECHA_SALIDA')
    return df_copy.resample(period).size()

def get_turnover_rate(df, period='M'):
    """
    Calcula la tasa de rotación por período.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
        period (str): El período para agrupar ('M' para mes, 'Q' para trimestre, 'Y' para año).

    Returns:
        pandas.Series: Una serie con la tasa de rotación por período.
    """
    terminations = get_terminations_by_period(df, period)

    # Calcular el número de empleados al inicio y al final de cada período
    all_dates = pd.to_datetime(df['FECHA_INGRESO']).tolist() + pd.to_datetime(df['FECHA_SALIDA'].dropna()).tolist()
    date_range = pd.date_range(start=min(all_dates), end=max(all_dates), freq=period)

    avg_employees = []
    for i in range(len(date_range) - 1):
        start_date = date_range[i]
        end_date = date_range[i+1]

        employees_at_start = df[(df['FECHA_INGRESO'] <= start_date) & ((df['FECHA_SALIDA'] > start_date) | (df['FECHA_SALIDA'].isnull()))].shape[0]
        employees_at_end = df[(df['FECHA_INGRESO'] <= end_date) & ((df['FECHA_SALIDA'] > end_date) | (df['FECHA_SALIDA'].isnull()))].shape[0]

        avg_employees.append((employees_at_start + employees_at_end) / 2)

    # Alinear los índices para el cálculo
    terminations = terminations.reindex(date_range[:-1], fill_value=0)

    # Evitar la división por cero
    avg_employees_series = pd.Series(avg_employees, index=date_range[:-1])
    avg_employees_series = avg_employees_series.replace(0, 1) # Replace 0 with 1 to avoid division by zero

    turnover_rate = (terminations / avg_employees_series) * 100
    return turnover_rate.fillna(0)

def get_retention_rate(df, period='Y'):
    """
    Calcula la tasa de retención por período.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
        period (str): El período para agrupar ('Y' para año).

    Returns:
        pandas.Series: Una serie con la tasa de retención por período.
    """
    turnover_rate = get_turnover_rate(df, period)
    retention_rate = 100 - turnover_rate
    return retention_rate

def get_average_tenure(df):
    """
    Calcula la duración promedio del empleo en días.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.

    Returns:
        float: La duración promedio del empleo en días.
    """
    return df['DURACION_EMPLEO'].mean()

def get_tenure_distribution(df):
    """
    Obtiene la distribución de la antigüedad de los empleados salientes.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.

    Returns:
        pandas.Series: Una serie con la distribución de la antigüedad.
    """
    df_terminated = df.dropna(subset=['FECHA_SALIDA'])
    return df_terminated['DURACION_EMPLEO']

def get_metrics_by_department(df, metric_func, **kwargs):
    """
    Calcula una métrica agrupada por departamento.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
        metric_func (function): La función de la métrica a calcular.
        **kwargs: Argumentos adicionales para la función de la métrica.

    Returns:
        pandas.DataFrame: Un DataFrame con la métrica calculada para cada departamento.
    """
    results = {}
    for department in df['AREA'].unique():
        df_dept = df[df['AREA'] == department]
        results[department] = metric_func(df_dept, **kwargs)

    return pd.DataFrame(results)
