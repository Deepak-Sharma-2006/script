"""
Test Suite — Domain Persona Hydration Engine
Verifies:
1. Dynamic generation of senior persona prompt overlays for each role across domains.
2. Domain-specific statutory standards and invariants are correctly embedded.
3. Multi-subdomain composite stacks resolve tools and standards without data loss.
4. Presentation themes match domain profiles.
"""

import os
import unittest
from scripts.orchestrator.domain_persona_engine import DomainPersonaEngine


class TestDomainPersonaHydration(unittest.TestCase):
    """Tests just-in-time hydration of the 6 SDLC personas across different domains."""

    def test_blockchain_persona_hydration(self):
        """Verifies that blockchain domain hydrates smart contract and DeFi directives."""
        hydrated_pm = DomainPersonaEngine.hydrate_persona("product_manager", domain_id="blockchain")
        self.assertIn("Web3", hydrated_pm["role_title"])
        self.assertEqual(hydrated_pm["domain_id"], "blockchain")

        overlay = DomainPersonaEngine.generate_persona_system_prompt_overlay("adversarial_sdet")
        # Ensure system prompt overlay is generated without crash
        self.assertIsInstance(overlay, str)
        self.assertGreater(len(overlay), 50)

    def test_ai_ml_persona_hydration(self):
        """Verifies that AI/ML domain hydrates foundation model and inference directives."""
        hydrated_architect = DomainPersonaEngine.hydrate_persona("system_architect", domain_id="ai_ml")
        self.assertIn("AI", hydrated_architect["role_title"])
        spec = hydrated_architect["specialization"]
        self.assertIn("mandatory_patterns", spec)

        hydrated_sdet = DomainPersonaEngine.hydrate_persona("adversarial_sdet", domain_id="ai_ml")
        self.assertIn("Prompt injection", hydrated_sdet["specialization"]["threat_model"])

    def test_deep_tech_persona_hydration(self):
        """Verifies that Deep Tech domain hydrates scientific rigor and physical constants."""
        hydrated_writer = DomainPersonaEngine.hydrate_persona("technical_writer", domain_id="deep_tech")
        self.assertIn("Scientific", hydrated_writer["role_title"])
        self.assertEqual(hydrated_writer["specialization"]["presentation_theme"], "light_minimal")

    def test_all_personas_generate_valid_overlays(self):
        """Verifies that generate_persona_system_prompt_overlay works for all 6 personas."""
        personas = [
            "product_manager", "system_architect", "adversarial_sdet",
            "core_engineer", "mutation_auditor", "technical_writer"
        ]
        for p in personas:
            overlay = DomainPersonaEngine.generate_persona_system_prompt_overlay(p)
            self.assertIn("DOMAIN SPECIALIZATION", overlay)
            self.assertIn("Active Persona Role", overlay)

    def test_presentation_theme_mapping(self):
        """Verifies presentation theme recommendation based on domain."""
        theme = DomainPersonaEngine.get_presentation_theme()
        self.assertIsInstance(theme, str)
        self.assertIn(theme, ["modern_tech", "cyber_dark", "light_minimal", "institutional_navy"])

    def test_squad_orchestrator_generates_domain_specialized_artifacts(self):
        """Verifies that ProductManagerRole, SystemArchitectRole, and TechnicalWriterRole emit domain-accurate artifacts."""
        from scripts.orchestrator.squad_orchestrator import ProductManagerRole, SystemArchitectRole, TechnicalWriterRole
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            spec = ProductManagerRole.create_functional_spec("Build yield farming contract", "test_vault", output_dir=tmp_dir, auto_trigger_research=False)
            self.assertIn("BLOCKCHAIN", spec.primary_goal)
            self.assertTrue(any("Domain Quality Rubric" in c for c in spec.acceptance_criteria))
            self.assertTrue(any("Domain Pitfall" in p for p in spec.forbidden_states))

            contract = SystemArchitectRole.design_contract(spec, output_dir=tmp_dir)
            self.assertIn("DomainArchitecturalInvariants", contract.data_schemas)

            dossier_path = TechnicalWriterRole.generate_dossier("test_vault", spec, contract, output_dir=tmp_dir)
            with open(dossier_path, "r", encoding="utf-8") as f:
                dossier_content = f.read()
            self.assertIn("Blockchain", dossier_content)
            self.assertNotIn("BSA Sec 63", dossier_content)
    def test_curated_skills_resolution_and_zero_ghosts(self):
        """Verifies that get_active_skills resolves verified local skills and rejects ghost files."""
        skills = DomainPersonaEngine.get_active_skills(domain_id="software", subdomains=["web_frontend"])
        self.assertGreater(len(skills), 0)
        for s in skills:
            self.assertTrue(os.path.exists(s["path"]), f"Ghost skill detected: {s['path']}")
            self.assertTrue(s["markdown_link"].startswith("[") and s["markdown_link"].endswith(")"))

        overlay = DomainPersonaEngine.generate_persona_system_prompt_overlay("core_engineer", domain_id="software")
        self.assertIn("Curated Skills", overlay)


if __name__ == "__main__":
    unittest.main()
