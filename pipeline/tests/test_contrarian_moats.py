"""
Unit Tests — Contrarian 4-Moat Matrix & Council Hardening
Tests that SolutionCouncil embeds the 4-moat matrix, anti-tamper specs,
and 5-advisor council hardening section in every generated dossier.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.orchestrator.solution_council import SolutionCouncil


class TestContrarian4MoatMatrix(unittest.TestCase):
    """Verifies SolutionCouncil synthesizes all 4 moats in the output."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="moat_test_")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _run_solution(self, problem_text: str, domain: str = "AI / Defense") -> dict:
        return SolutionCouncil.formulate_solution(
            problem_title="Test Solution",
            problem_text=problem_text,
            domain=domain,
            output_dir=self.tmpdir
        )

    def test_cyber_domain_returns_four_moats(self) -> None:
        """Cyber/Defense domain should produce 4-moat dict with all keys."""
        result = self._run_solution("Tor darknet forensic analysis")
        self.assertIn("four_moats", result)
        moats = result["four_moats"]
        for key in ("data_ingestion", "algorithmic", "sovereign_statutory", "economic"):
            self.assertIn(key, moats, f"Missing moat key: {key}")
            self.assertTrue(len(moats[key]) > 10, f"Moat '{key}' is too short: {moats[key]}")

    def test_agri_domain_returns_four_moats(self) -> None:
        """Agriculture domain should produce agriculture-specific 4 moats."""
        result = self._run_solution("Crop disease detection via drone swarm imaging")
        moats = result["four_moats"]
        self.assertIn("drone", moats["data_ingestion"].lower())
        self.assertIn("icar", moats["sovereign_statutory"].lower())

    def test_health_domain_returns_four_moats(self) -> None:
        """Health domain should produce clinical-specific 4 moats."""
        result = self._run_solution("Real-time sepsis prediction in ICU patients")
        moats = result["four_moats"]
        self.assertIn("waveform", moats["data_ingestion"].lower())
        self.assertIn("hipaa", moats["sovereign_statutory"].lower())


class TestAntiTamperSpecification(unittest.TestCase):
    """Verifies anti-tamper cryptographic specs are embedded in output."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="tamper_spec_test_")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_anti_tamper_spec_has_three_components(self) -> None:
        """Output should include merkle_chain, constant_time, and enclave_isolation."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet cyber forensic",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        self.assertIn("anti_tamper_spec", result)
        spec = result["anti_tamper_spec"]
        for key in ("merkle_chain", "constant_time", "enclave_isolation"):
            self.assertIn(key, spec, f"Missing anti-tamper component: {key}")
            self.assertTrue(len(spec[key]) > 10, f"Anti-tamper spec '{key}' is too short")

    def test_merkle_chain_mentions_sha256(self) -> None:
        """Merkle chain spec should reference SHA-256."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet forensics",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        self.assertIn("sha-256", result["anti_tamper_spec"]["merkle_chain"].lower())

    def test_constant_time_mentions_timing_safe(self) -> None:
        """Constant-time spec should reference timingSafeEqual or compare_digest."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet forensics",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        ct_spec = result["anti_tamper_spec"]["constant_time"].lower()
        self.assertTrue(
            "timingsafeequal" in ct_spec or "compare_digest" in ct_spec,
            f"Constant-time spec lacks safe comparison references: {ct_spec}"
        )


class TestCouncilHardeningInOutput(unittest.TestCase):
    """Verifies the 5-advisor council hardening is present in output dict and dossier file."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="council_test_")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_council_hardening_dict_structure(self) -> None:
        """Output should include council_hardening with advisors and verdict."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet cyber forensic",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        self.assertIn("council_hardening", result)
        ch = result["council_hardening"]
        self.assertIn("advisors", ch)
        self.assertIn("verdict", ch)
        self.assertEqual(len(ch["advisors"]), 5)
        self.assertIn("UNANIMOUS", ch["verdict"])

    def test_dossier_file_contains_council_section(self) -> None:
        """Generated dossier markdown should contain the 5-advisor council table."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet cyber forensic",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        dossier_path = result["dossier_path"]
        self.assertTrue(os.path.exists(dossier_path))
        with open(dossier_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("5-Advisor Claude Council Hardening Review", content)
        self.assertIn("01-Contrarian", content)
        self.assertIn("02-First-Principles", content)
        self.assertIn("03-Expansionist", content)
        self.assertIn("04-Naive Outsider", content)
        self.assertIn("05-Pragmatic Executor", content)
        self.assertIn("UNANIMOUS CONSENSUS", content)

    def test_dossier_contains_4_moat_section(self) -> None:
        """Generated dossier should have the Contrarian 4-Moat section."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet cyber forensic",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        with open(result["dossier_path"], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Contrarian 4-Moat Defensibility Matrix", content)
        self.assertIn("Data Ingestion Moat", content)
        self.assertIn("Algorithmic / Architectural Moat", content)
        self.assertIn("Sovereign / Statutory Moat", content)
        self.assertIn("Financial & Unit Economics Moat", content)

    def test_dossier_contains_anti_tamper_section(self) -> None:
        """Generated dossier should have the anti-tamper enclave topology."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet cyber forensic",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        with open(result["dossier_path"], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Cryptographic Anti-Tamper", content)
        self.assertIn("Merkle Chain State Machine", content)
        self.assertIn("Asymmetric Enclave", content)


class TestSolutionReturnPayload(unittest.TestCase):
    """Verifies the full return payload structure from formulate_solution."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="payload_test_")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_all_required_keys_present(self) -> None:
        """Return dict should contain all required top-level keys."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet forensic",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        expected_keys = [
            "solution_name", "dossier_path", "moat_thesis",
            "four_moats", "anti_tamper_spec", "council_hardening",
            "tiers", "pipeline_steps", "kpis", "assets", "unit_economics"
        ]
        for key in expected_keys:
            self.assertIn(key, result, f"Missing key in result: {key}")

    def test_unit_economics_has_margin(self) -> None:
        """Unit economics should include gross margin percentage."""
        result = SolutionCouncil.formulate_solution(
            problem_title="Test",
            problem_text="Tor darknet forensic",
            domain="Cyber",
            output_dir=self.tmpdir
        )
        econ = result["unit_economics"]
        self.assertIn("gross_margin_pct", econ)
        self.assertGreater(econ["gross_margin_pct"], 0)


if __name__ == "__main__":
    unittest.main()
