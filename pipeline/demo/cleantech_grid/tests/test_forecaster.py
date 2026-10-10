import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from forecaster import forecast_grid_demand

class TestGridDemand(unittest.TestCase):
    def test_demand_forecasting(self):
        self.assertEqual(forecast_grid_demand(100.0, 35.0), 135.0)
        self.assertEqual(forecast_grid_demand(100.0, 20.0), 100.0)

if __name__ == "__main__":
    unittest.main()
