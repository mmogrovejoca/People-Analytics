import unittest
import pandas as pd
import sys
sys.path.append('.')
from people_analytics.src.metrics.metrics_calculator import get_hires_by_period, get_terminations_by_period

class TestMetricsCalculator(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'FECHA_INGRESO': pd.to_datetime(['2022-01-15', '2022-02-20']),
            'FECHA_SALIDA': pd.to_datetime([pd.NaT, '2023-01-10']),
            'AREA': ['Ventas', 'Marketing'],
            'CARGO': ['Vendedor', 'Analista'],
            'MOTIVO_SALIDA': [None, 'Renuncia'],
            'TIPO_CONTRATO': ['Permanente', 'Temporal'],
            'ID_EMPLEADO': [1, 2]
        })

    def test_get_hires_by_period(self):
        hires = get_hires_by_period(self.df, 'M')
        self.assertEqual(hires['2022-01-31'], 1)
        self.assertEqual(hires['2022-02-28'], 1)

    def test_get_terminations_by_period(self):
        terminations = get_terminations_by_period(self.df, 'M')
        self.assertEqual(terminations['2023-01-31'], 1)

if __name__ == '__main__':
    unittest.main()
