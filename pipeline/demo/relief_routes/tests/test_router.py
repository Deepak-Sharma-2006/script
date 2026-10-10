import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from router import shortest_distance

class TestReliefRouter(unittest.TestCase):
    def test_routing(self):
        edges = {("depot", "sector_1"): 15}
        self.assertEqual(shortest_distance(edges, "depot", "sector_1"), 15)
        self.assertEqual(shortest_distance(edges, "depot", "sector_9"), -1)

if __name__ == "__main__":
    unittest.main()
