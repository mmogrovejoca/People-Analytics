import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def cluster_terminated_employees(df, n_clusters=3):
    """
    Agrupa a los empleados salientes en clusters utilizando K-Means.

    Args:
        df (pandas.DataFrame): DataFrame con los datos de los empleados.
        n_clusters (int): Número de clusters a crear.

    Returns:
        pandas.DataFrame: DataFrame de empleados salientes con una columna adicional 'cluster'.
    """
    df_terminated = df.dropna(subset=['FECHA_SALIDA']).copy()

    # Seleccionar características para el clustering
    features = ['DURACION_EMPLEO', 'MES_SALIDA', 'ANIO_SALIDA']
    X = df_terminated[features]

    # Estandarizar las características
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Aplicar K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_terminated['cluster'] = kmeans.fit_predict(X_scaled)

    return df_terminated

def plot_clusters(df_clustered):
    """
    Visualiza los clusters de empleados salientes.

    Args:
        df_clustered (pandas.DataFrame): DataFrame de empleados salientes con clusters.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_clustered, x='DURACION_EMPLEO', y='ANIO_SALIDA', hue='cluster', palette='viridis', s=100)
    plt.title('Clusters de Empleados Salientes')
    plt.xlabel('Duración del Empleo (días)')
    plt.ylabel('Año de Salida')
    plt.legend(title='Cluster')
    plt.grid(True)
    fig = plt.gcf()
    plt.close()
    return fig
