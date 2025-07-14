import pandas as pd

def load_data(filepath):
    """
    Carga los datos de un archivo CSV y los convierte a un DataFrame de pandas.

    Args:
        filepath (str): La ruta al archivo CSV.

    Returns:
        pandas.DataFrame: El DataFrame con los datos cargados.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en la ruta: {filepath}")
        return None
    except Exception as e:
        print(f"Ocurrió un error al cargar el archivo: {e}")
        return None
