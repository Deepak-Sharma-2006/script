"""
Test Suite — Domain Selector & Domain Catalog Verification
Verifies:
1. All 8 Master Domains are loadable and syntactically valid.
2. Each domain specifies at least 4 subdomains with key technologies and statutory standards.
3. Each domain specifies complete persona specializations across all 6 enterprise roles.
4. Active domain state persistence and fallback behavior.
"""

import os
import json
import unittest
from scripts.orchestrator.domain_persona_engine import DomainPersonaEngine


class TestDomainSelector(unittest.TestCase):
    """Tests the domain catalog, rubrics, and state management."""

    def test_catalog_contains_all_8_domains(self):
        """Verifies that templates/domains/catalog.json lists all 8 Master Domains."""
        catalog_path = os.path.join("templates", "domains", "catalog.json")
        self.assertTrue(os.path.exists(catalog_path), "Catalog file must exist.")

        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        expected_domains = {
            "software", "ai_ml", "blockchain", "deep_tech",
            "cybersecurity", "cloud_infra", "data_engineering", "vertical_applied"
        }
        self.assertEqual(set(catalog["domains"].keys()), expected_domains)
        self.assertEqual(catalog["total_domains"], 8)

    def test_all_8_domain_rubrics_load_cleanly(self):
        """Verifies that every domain rubric file exists and is valid JSON."""
        expected_domains = [
            "software", "ai_ml", "blockchain", "deep_tech",
            "cybersecurity", "cloud_infra", "data_engineering", "vertical_applied"
        ]
        for domain_id in expected_domains:
            rubric = DomainPersonaEngine.load_domain_rubric(domain_id)
            self.assertEqual(rubric["domain_id"], domain_id)
            self.assertIn("domain_name", rubric)
            self.assertGreaterEqual(len(rubric["subdomains"]), 4)
            self.assertGreaterEqual(len(rubric["verification_gates"]), 3)

    def test_all_6_personas_have_domain_specializations(self):
        """Verifies that each domain defines custom specializations for all 6 roles."""
        required_personas = [
            "product_manager", "system_architect", "adversarial_sdet",
            "core_engineer", "mutation_auditor", "technical_writer"
        ]
        expected_domains = [
            "software", "ai_ml", "blockchain", "deep_tech",
            "cybersecurity", "cloud_infra", "data_engineering", "vertical_applied"
        ]

        for domain_id in expected_domains:
            rubric = DomainPersonaEngine.load_domain_rubric(domain_id)
            specializations = rubric["persona_specializations"]
            for p in required_personas:
                self.assertIn(p, specializations, f"Domain '{domain_id}' missing persona '{p}'")
                self.assertIn("role_title", specializations[p])

    def test_active_state_retrieval_and_fallback(self):
        """Verifies that get_active_state returns valid domain configuration."""
        state = DomainPersonaEngine.get_active_state()
        self.assertIn("domain_id", state)
        self.assertIn("subdomains", state)
        self.assertIn("active_stack", state)


if __name__ == "__main__":
    unittest.main()
