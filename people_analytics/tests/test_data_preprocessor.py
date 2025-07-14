import unittest
import pandas as pd
import sys
sys.path.append('.')
from people_analytics.src.etl.data_preprocessor import preprocess_data

class TestDataPreprocessor(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'FECHA_INGRESO': ['2022-01-01'],
            'FECHA_SALIDA': [pd.NaT],
            'AREA': ['Test'],
            'CARGO': ['Tester'],
            'MOTIVO_SALIDA': [None],
            'TIPO_CONTRATO': ['Permanente'],
            'ID_EMPLEADO': [1]
        })

    def test_preprocess_data(self):
        df_processed = preprocess_data(self.df.copy())

        self.assertIn('DURACION_EMPLEO', df_processed.columns)
        self.assertIn('MES_INGRESO', df_processed.columns)
        self.assertIn('ANIO_INGRESO', df_processed.columns)

        self.assertEqual(df_processed['MES_INGRESO'][0], 1)
        self.assertEqual(df_processed['ANIO_INGRESO'][0], 2022)

if __name__ == '__main__':
    unittest.main()
