"""
Test Suite — Financial Unit Economics & Cloud COGS Estimator
Verifies:
1. CostEstimator computes infrastructure and model token costs per 1,000 requests.
2. CostEstimator evaluates monthly COGS across tiered request volumes (10k, 100k, 1M).
3. CostEstimator determines target SaaS subscription pricing to sustain >= 75% gross margin.
4. Generates verified markdown tables for executive review.
"""

import unittest
from scripts.orchestrator.cost_estimator import CostEstimator, UnitEconomicsModel


class TestCostEstimator(unittest.TestCase):
    """Verifies unit economics modeling and pricing formulas."""

    def test_unit_economics_calculation(self):
        """Verifies calculation of cost per 1k queries, COGS tiers, and gross margins."""
        model = CostEstimator.calculate_unit_economics(
            solution_name="Test Enterprise Solution",
            avg_tokens_input_per_query=1500,
            avg_tokens_output_per_query=400,
            vector_lookups_per_query=2,
            db_queries_per_op=4
        )

        self.assertIsInstance(model, UnitEconomicsModel)
        self.assertEqual(model.solution_name, "Test Enterprise Solution")
        self.assertGreater(model.cost_per_1k_queries, 0.0)
        self.assertGreater(model.monthly_cogs_10k, 0.0)
        self.assertGreater(model.monthly_cogs_100k, model.monthly_cogs_10k)
        self.assertGreater(model.monthly_cogs_1m, model.monthly_cogs_100k)

        # Software gross margin target should be >= 75%
        self.assertGreaterEqual(model.gross_margin_percentage, 75.0)

        # Breakdown checks
        self.assertIn("llm_inference_cogs", model.breakdown)
        self.assertIn("compute_db_cogs", model.breakdown)
        self.assertIn("fixed_monthly_base", model.breakdown)

    def test_markdown_table_formatting(self):
        """Verifies markdown table output renders proper financial headers and values."""
        model = CostEstimator.calculate_unit_economics("FinTech Classifier")
        md = CostEstimator.format_markdown_table(model)

        self.assertIn("### Financial Feasibility & Cloud Unit Economics (COGS)", md)
        self.assertIn("Total Cost per 1,000 Queries", md)
        self.assertIn("Monthly Infrastructure COGS", md)
        self.assertIn(f"{model.gross_margin_percentage}%", md)
        self.assertIn("VERIFIED SUSTAINABLE", md)


if __name__ == "__main__":
    unittest.main()
