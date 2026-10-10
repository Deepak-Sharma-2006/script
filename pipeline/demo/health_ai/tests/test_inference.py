import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from inference import HealthRiskClassifier

class TestHealthRisk(unittest.TestCase):
    def test_classification_boundaries(self):
        c = HealthRiskClassifier()
        self.assertEqual(c.classify(145, 95), "STAGE_2_HYPERTENSION")
        self.assertEqual(c.classify(135, 85), "STAGE_1_HYPERTENSION")
        self.assertEqual(c.classify(118, 76), "NORMAL")

if __name__ == "__main__":
    unittest.main()
