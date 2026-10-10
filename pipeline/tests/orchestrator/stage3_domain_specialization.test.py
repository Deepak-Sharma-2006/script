"""
Unit & Adversarial Test Suite for Stage 3: The 8 Master Domains & 46 Subdomains Deep Specialization Engine
"""

import os
import sys
import json
import unittest

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.getcwd())

from scripts.orchestrator.domain_persona_engine import DomainPersonaEngine

class TestStage3DomainSpecialization(unittest.TestCase):

    def setUp(self):
        self.workspace_root = os.getcwd()
        self.templates_dir = os.path.join(self.workspace_root, "templates", "domains")
        self.catalog_path = os.path.join(self.templates_dir, "catalog.json")

    def test_gate1_catalog_integrity(self):
        """Gate 1: Verifies that catalog.json exists and defines 8 domains with 46 subdomains."""
        self.assertTrue(os.path.exists(self.catalog_path), "catalog.json must exist")
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        domains = data.get("domains", {})
        self.assertEqual(len(domains), 8, "Must contain exactly 8 master domains")

        total_subdomains = sum(len(d.get("subdomains", [])) for d in domains.values())
        self.assertEqual(total_subdomains, 46, "Must contain exactly 46 subdomains across all domains")

    def test_gate2_all_domain_rubrics_exist(self):
        """Gate 2: Verifies that each domain folder contains a valid rubric.json."""
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for d_id in data.get("domains", {}).keys():
            rubric_file = os.path.join(self.templates_dir, d_id, "rubric.json")
            self.assertTrue(os.path.exists(rubric_file), f"Rubric for domain '{d_id}' must exist at {rubric_file}")

            with open(rubric_file, "r", encoding="utf-8") as rf:
                rubric = json.load(rf)
                self.assertIn("domain_id", rubric)
                self.assertIn("subdomains", rubric)
                self.assertIn("persona_specializations", rubric)

    def test_gate3_persona_hydration_ai_ml(self):
        """Gate 3: Verifies deep persona hydration for ai_ml domain."""
        hydrated = DomainPersonaEngine.hydrate_persona("core_engineer", domain_id="ai_ml")
        self.assertEqual(hydrated["domain_id"], "ai_ml")
        self.assertIn("Senior", hydrated["role_title"])
        self.assertIn("coding_idioms", hydrated["specialization"])

    def test_gate4_persona_hydration_cybersecurity(self):
        """Gate 4: Verifies deep persona hydration for cybersecurity domain."""
        hydrated = DomainPersonaEngine.hydrate_persona("adversarial_sdet", domain_id="cybersecurity")
        self.assertEqual(hydrated["domain_id"], "cybersecurity")
        self.assertIn("threat_model", hydrated["specialization"])

    def test_gate5_system_prompt_overlay_density(self):
        """Gate 5: Verifies that prompt overlays contain high-density technical keywords."""
        overlay = DomainPersonaEngine.generate_persona_system_prompt_overlay("core_engineer", domain_id="ai_ml")
        self.assertIn("=== [DOMAIN SPECIALIZATION", overlay)
        self.assertIn("Statutory Standards", overlay)
        self.assertIn("Coding Idioms", overlay)
        # Verify file:// links in curated skills
        self.assertIn("file:///", overlay)

    def test_gate6_active_domain_context_disk_persistence(self):
        """Gate 6: Verifies that writing active domain context creates valid file on disk."""
        overlay = DomainPersonaEngine.generate_persona_system_prompt_overlay("core_engineer")
        out_path = os.path.join(self.workspace_root, ".agents", "state", "active-domain-context.md")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(overlay)

        self.assertTrue(os.path.exists(out_path), "active-domain-context.md must exist on disk")
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DOMAIN SPECIALIZATION", content)

if __name__ == "__main__":
    unittest.main()
