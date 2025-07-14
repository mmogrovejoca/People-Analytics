import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_hires_terminations_timeline(hires, terminations):
    """
    Dibuja una línea de tiempo de contrataciones y bajas.

    Args:
        hires (pandas.Series): Serie de datos de contrataciones a lo largo del tiempo.
        terminations (pandas.Series): Serie de datos de bajas a lo largo del tiempo.
    """
    plt.figure(figsize=(12, 6))
    hires.plot(label='Contrataciones', color='blue')
    terminations.plot(label='Bajas', color='red')
    plt.title('Línea de Tiempo de Contrataciones y Bajas')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Empleados')
    plt.legend()
    plt.grid(True)
    fig = plt.gcf()
    plt.close()
    return fig

def plot_seasonality(data, date_column, title):
    """
    Dibuja la estacionalidad de los datos a lo largo de los meses.

    Args:
        data (pandas.DataFrame): DataFrame que contiene los datos.
        date_column (str): Nombre de la columna de fecha a utilizar.
        title (str): Título del gráfico.
    """
    df = data.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df['month'] = df[date_column].dt.month

    monthly_counts = df.groupby('month').size()

    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_counts.index, y=monthly_counts.values, palette='viridis')
    plt.title(title)
    plt.xlabel('Mes')
    plt.ylabel('Número de Eventos')
    fig = plt.gcf()
    plt.close()
    return fig

def plot_tenure_distribution(tenure_series, bins=20):
    """
    Dibuja un histograma y un gráfico de densidad de la duración del empleo.

    Args:
        tenure_series (pandas.Series): Serie que contiene la duración del empleo.
        bins (int): Número de bins para el histograma.
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(tenure_series, bins=bins, kde=True, color='purple')
    plt.title('Distribución de la Antigüedad de los Empleados Salientes')
    plt.xlabel('Duración del Empleo (días)')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    fig = plt.gcf()
    plt.close()
    return fig

def plot_turnover_heatmap(df):
    """
    Dibuja un mapa de calor de la rotación por departamento y mes.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
    """
    df_terminated = df.dropna(subset=['FECHA_SALIDA']).copy()
    df_terminated['mes_salida'] = df_terminated['FECHA_SALIDA'].dt.month

    turnover_by_dept_month = df_terminated.groupby(['AREA', 'mes_salida']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 8))
    sns.heatmap(turnover_by_dept_month, cmap='Reds', annot=True, fmt='d')
    plt.title('Mapa de Calor de Bajas por Departamento y Mes')
    plt.xlabel('Mes de Salida')
    plt.ylabel('Departamento')
    fig = plt.gcf()
    plt.close()
    return fig

def plot_termination_reason_distribution(termination_reasons):
    """
    Dibuja un gráfico de barras de la distribución de los motivos de salida.

    Args:
        termination_reasons (pandas.Series): Serie con la distribución de los motivos de salida.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x=termination_reasons.index, y=termination_reasons.values, palette='plasma')
    plt.title('Distribución de Motivos de Salida')
    plt.xlabel('Motivo de Salida')
    plt.ylabel('Número de Empleados')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

from lifelines import KaplanMeierFitter

def plot_survival_curve(df):
    """
    Dibuja la curva de supervivencia de los empleados.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
    """
    kmf = KaplanMeierFitter()

    # Se necesita una columna que indique si el evento (salida) ocurrió.
    df['observed'] = df['FECHA_SALIDA'].notna()

    kmf.fit(durations=df['DURACION_EMPLEO'], event_observed=df['observed'])

    plt.figure(figsize=(10, 6))
    kmf.plot_survival_function()
    plt.title('Curva de Supervivencia de Empleados')
    plt.xlabel('Días en la Empresa')
    plt.ylabel('Probabilidad de Supervivencia')
    plt.grid(True)
    fig = plt.gcf()
    plt.close()
    return fig
