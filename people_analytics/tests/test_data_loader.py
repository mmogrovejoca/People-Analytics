import unittest
import pandas as pd
import sys
sys.path.append('.')
from people_analytics.src.etl.data_loader import load_data

class TestDataLoader(unittest.TestCase):

    def test_load_data_success(self):
        # Crear un archivo CSV de prueba
        with open('test_data.csv', 'w') as f:
            f.write('col1,col2\n')
            f.write('1,a\n')
            f.write('2,b\n')

        df = load_data('test_data.csv')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)

        # Limpiar
        import os
        os.remove('test_data.csv')

    def test_load_data_file_not_found(self):
        df = load_data('non_existent_file.csv')
        self.assertIsNone(df)

if __name__ == '__main__':
    unittest.main()
