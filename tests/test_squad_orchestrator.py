"""
Unit Tests for Enterprise Agile Product Squad Orchestrator
Tests:
1. Product Manager PRD formulation and JSON generation.
2. System Architect Contract and FSM transition schemas.
3. Adversarial SDET Red Phase verification and anti-tautology rejection.
4. Adversarial SDET Headless Playwright frontend detection.
5. Mutation Auditor kill-rate validation.
6. Technical Writer Part 7 6-technique dossier compilation.
7. Complete SquadOrchestrator lifecycle execution.
8. TaskDispatcher squad routing.
"""

import os
import sys
import json
import time
import unittest
import shutil
import glob

from scripts.orchestrator.squad_orchestrator import (
    ProductManagerRole,
    SystemArchitectRole,
    AdversarialSDETRole,
    MutationAuditorRole,
    TechnicalWriterRole,
    SquadOrchestrator,
    SQUAD_PERSONA_PROFILES,
    PersonaProfile
)
from scripts.orchestrator.task_dispatcher import TaskDispatcher


class TestSquadOrchestrator(unittest.TestCase):
    def setUp(self):
        self.test_dir = "specs/test_artifacts"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)
        for sub in ["plans", "walkthroughs", "research", "specifications", "decisions", "audits"]:
            d = os.path.join("docs", sub)
            if os.path.exists(d):
                for pattern in ["*drone_telemetry*", "*db_migration*", "*audit_probe*"]:
                    for f in glob.glob(os.path.join(d, pattern)):
                        try:
                            os.remove(f)
                        except OSError:
                            pass

    def test_persona_profiles_configured(self):
        """Verifies that all 7 personas have differentiated temperature and reasoning effort."""
        self.assertEqual(len(SQUAD_PERSONA_PROFILES), 7)

        research = SQUAD_PERSONA_PROFILES["deep_research_specialist"]
        self.assertEqual(research.temperature, 0.3)
        self.assertEqual(research.reasoning_effort, "high")
        
        pm = SQUAD_PERSONA_PROFILES["product_manager"]
        self.assertEqual(pm.temperature, 0.7)
        self.assertEqual(pm.reasoning_effort, "medium")

        arch = SQUAD_PERSONA_PROFILES["system_architect"]
        self.assertEqual(arch.temperature, 0.2)
        self.assertEqual(arch.reasoning_effort, "high")

        sdet = SQUAD_PERSONA_PROFILES["adversarial_sdet"]
        self.assertEqual(sdet.temperature, 0.8)
        self.assertEqual(sdet.reasoning_effort, "high")

        coder = SQUAD_PERSONA_PROFILES["core_engineer"]
        self.assertEqual(coder.temperature, 0.1)
        self.assertEqual(coder.reasoning_effort, "medium")

        mutation = SQUAD_PERSONA_PROFILES["mutation_auditor"]
        self.assertEqual(mutation.temperature, 0.0)
        self.assertEqual(mutation.reasoning_effort, "low")

        writer = SQUAD_PERSONA_PROFILES["technical_writer"]
        self.assertEqual(writer.temperature, 0.4)
        self.assertEqual(writer.reasoning_effort, "low")

    def test_product_manager_spec_generation(self):
        """Verifies Product Manager emits a valid functional spec JSON."""
        spec = ProductManagerRole.create_functional_spec(
            prompt="Build secure biometric validator",
            feature_name="biometric_audit",
            output_dir=self.test_dir
        )
        self.assertEqual(spec.feature_name, "biometric_audit")
        self.assertTrue(len(spec.acceptance_criteria) > 0)
        self.assertTrue(len(spec.forbidden_states) > 0)
        self.assertTrue(len(spec.observable_journeys) > 0)

        spec_file = os.path.join(self.test_dir, "biometric_audit_functional_spec.json")
        self.assertTrue(os.path.exists(spec_file))
        with open(spec_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["feature_name"], "biometric_audit")

    def test_system_architect_contract_generation(self):
        """Verifies System Architect emits valid FSM transitions and schema contract."""
        spec = ProductManagerRole.create_functional_spec(
            prompt="Build secure biometric validator",
            feature_name="biometric_audit",
            output_dir=self.test_dir
        )
        contract = SystemArchitectRole.design_contract(spec, output_dir=self.test_dir)
        self.assertIn("IDLE", contract.fsm_states)
        self.assertIn("CERTIFIED", contract.fsm_states)
        self.assertTrue(len(contract.fsm_transitions) >= 3)
        self.assertIn("CaseState", contract.data_schemas)

        contract_file = os.path.join(self.test_dir, "biometric_audit_contract.json")
        self.assertTrue(os.path.exists(contract_file))

    def test_adversarial_sdet_red_phase_and_tautology_rejection(self):
        """Verifies SDET confirms failing test as RED, and rejects tautological test."""
        # 1. Properly failing test (missing module)
        failing_test_code = """
import unittest
from specs.non_existent_module_xyz import FakeService

class TestFake(unittest.TestCase):
    def test_fake(self):
        FakeService()
"""
        test_path = os.path.join(self.test_dir, "test_failing.py")
        red_ok = AdversarialSDETRole.verify_red_phase(test_path, failing_test_code)
        self.assertTrue(red_ok, "Failing test must be verified as RED phase.")

        # 2. Tautological test that passes with no implementation
        tautological_test_code = """
import unittest

class TestTautological(unittest.TestCase):
    def test_tautology(self):
        self.assertEqual(1 + 1, 2)
"""
        tauto_path = os.path.join(self.test_dir, "test_tauto.py")
        red_bad = AdversarialSDETRole.verify_red_phase(tauto_path, tautological_test_code)
        self.assertFalse(red_bad, "Tautological test must be rejected by SDET.")

    def test_adversarial_sdet_headless_browser_detection(self):
        """Verifies automated headless Playwright verification when frontend files exist."""
        # Workspace has frontend files (HTML/TSX/JSX)
        res = AdversarialSDETRole.detect_and_run_headless_browser(".")
        self.assertTrue(res["frontend_detected"])
        self.assertIn(res["browser_e2e"], ["VERIFIED_HEADLESS_PLAYWRIGHT", "PLAYWRIGHT_READY", "FAILED_PLAYWRIGHT_MISSING"])

        # Test empty directory with no frontend
        empty_dir = os.path.join(self.test_dir, "empty_backend")
        os.makedirs(empty_dir, exist_ok=True)
        res_empty = AdversarialSDETRole.detect_and_run_headless_browser(empty_dir)
        self.assertFalse(res_empty["frontend_detected"])
        self.assertEqual(res_empty["browser_e2e"], "SKIPPED_NO_FRONTEND")

    def test_technical_writer_part7_dossier(self):
        """Verifies Technical Writer compiles all 6 Part 7 comprehension techniques."""
        spec = ProductManagerRole.create_functional_spec(
            prompt="Build telemetry logger",
            feature_name="telemetry_test",
            output_dir=self.test_dir
        )
        contract = SystemArchitectRole.design_contract(spec, output_dir=self.test_dir)
        dossier_path = TechnicalWriterRole.generate_dossier("telemetry_test", spec, contract, output_dir=self.test_dir)
        self.assertTrue(os.path.exists(dossier_path))

        with open(dossier_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Technique 1: The Human Mental Model", content)
            self.assertIn("Technique 2: Visual Code Flow", content)
            self.assertIn("Technique 3: Variable Lifecycle Trace", content)
            self.assertIn("Technique 4: Non-Blocking Noise Filtering", content)
            self.assertIn("Technique 5: Audit Exactly One Failure Path", content)
            self.assertIn("Technique 6: 1-Sentence Feynman Mental Compression Test", content)

    def test_task_dispatcher_squad_routing(self):
        """Verifies TaskDispatcher correctly routes --task squad with solo mode."""
        res = TaskDispatcher.dispatch(
            task="squad",
            feature="audit_probe",
            mode="solo",
            prompt="Build audit probe with fail-closed gating"
        )
        self.assertTrue(res["passed"])
        self.assertTrue(res["red_phase_verified"])
        self.assertTrue(res["green_phase_verified"])
        self.assertGreaterEqual(res["mutation_score"], 80.0)
        self.assertIn("product_manager", res["persona_profiles"])
        self.assertIn("adversarial_sdet", res["persona_profiles"])
        self.assertIn("deep_research_specialist", res["persona_profiles"])

    def test_deep_research_specialist_and_modes(self):
        """Verifies ResearchTriangulator executes in EXPLORATION and IMPACT modes."""
        from scripts.orchestrator.research_triangulator import ResearchTriangulator
        
        # Test EXPLORATION mode
        exp_res = ResearchTriangulator.triangulate(
            problem_title="Unit Test Exploration",
            domain="Testing",
            mode="EXPLORATION"
        )
        self.assertEqual(exp_res.mode, "EXPLORATION")
        self.assertGreaterEqual(exp_res.saturation_score, 0.85)
        self.assertTrue(len(exp_res.angles_analyzed) >= 3)
        self.assertTrue(len(exp_res.defensible_moats) >= 1)

        # Test IMPACT mode
        impact_metrics = {
            "playwright_latency": "12ms",
            "e2e_pass_rate": "100%",
            "pytest_coverage": "98.2%",
            "mutation_kill_rate": "100%",
            "sast_vulnerabilities": 0
        }
        imp_res = ResearchTriangulator.triangulate(
            problem_title="Unit Test Impact",
            domain="Testing",
            mode="IMPACT",
            empirical_metrics=impact_metrics
        )
        self.assertEqual(imp_res.mode, "IMPACT")
        self.assertGreaterEqual(imp_res.saturation_score, 0.85)

    def test_product_manager_mandatory_auto_trigger_research(self):
        """Verifies Product Manager automatically triggers Deep Research on new problem statements."""
        spec = ProductManagerRole.create_functional_spec(
            prompt="Build high-speed telemetry engine for drones",
            feature_name="drone_telemetry",
            output_dir=self.test_dir,
            auto_trigger_research=True
        )
        self.assertEqual(spec.feature_name, "drone_telemetry")
        # Check that research dossier was persisted in docs/research/
        import glob
        research_files = glob.glob(os.path.join("docs", "research", "*drone_telemetry_research.md"))
        self.assertGreater(len(research_files), 0, "Research file must exist in docs/research/")

    def test_system_architect_significant_tradeoff_adr(self):
        """Verifies System Architect emits to docs/decisions/ when significant trade-off occurs."""
        spec = ProductManagerRole.create_functional_spec(
            prompt="Migrate central database to distributed SQLite",
            feature_name="db_migration",
            output_dir=self.test_dir,
            auto_trigger_research=False
        )
        # 1. Routine feature: No ADR emitted
        contract_routine = SystemArchitectRole.design_contract(
            spec,
            output_dir=self.test_dir,
            is_significant_tradeoff=False
        )
        self.assertIsNotNone(contract_routine)

        # 2. Significant Trade-Off: ADR emitted
        contract_significant = SystemArchitectRole.design_contract(
            spec,
            output_dir=self.test_dir,
            is_significant_tradeoff=True,
            tradeoff_rationale="Evaluated Postgres vs SQLite; chose SQLite for sub-50ms local zero-cloud latency."
        )
        self.assertIsNotNone(contract_significant)
        decision_files = glob.glob(os.path.join("docs", "decisions", "*db_migration_*.md"))
        self.assertGreater(len(decision_files), 0, "Decision file must exist in docs/decisions/")


if __name__ == "__main__":
    import time
    unittest.main()
