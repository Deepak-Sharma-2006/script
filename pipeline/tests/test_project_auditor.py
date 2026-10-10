"""
Unit Tests — ProjectAuditor (Cases B & C)
Tests the multi-pillar diagnostic engine, auto-remediation, and markdown blueprint auditing.
"""

import os
import sys
import shutil
import tempfile
import unittest
from typing import Optional
from unittest.mock import patch, MagicMock

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.orchestrator.project_auditor import ProjectAuditor, ProjectAuditReport, AuditFinding


class TestProjectAuditorCaseBFull(unittest.TestCase):
    """Tests Case B: Audit an existing project directory."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="audit_test_")
        # Create a minimal project structure
        src_dir = os.path.join(self.tmpdir, "src")
        tests_dir = os.path.join(self.tmpdir, "tests")
        os.makedirs(src_dir)
        os.makedirs(tests_dir)

        # A clean Python module
        with open(os.path.join(src_dir, "clean_module.py"), "w") as f:
            f.write('def add(a: int, b: int) -> int:\n    return a + b\n')

        # A module with NotImplementedError stub
        with open(os.path.join(src_dir, "stub_module.py"), "w") as f:
            f.write('def process_data(data: list) -> dict:\n    raise NotImplementedError("TODO")\n')

        # A test file
        with open(os.path.join(tests_dir, "test_clean.py"), "w") as f:
            f.write('import unittest\nclass TestClean(unittest.TestCase):\n    def test_add(self): self.assertEqual(1+1, 2)\n')

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_audit_detects_not_implemented_stub(self) -> None:
        """P0 critical finding should fire for NotImplementedError stubs."""
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        self.assertIsInstance(report, ProjectAuditReport)
        p0_findings = [f for f in report.findings if f.severity == "P0_CRITICAL"]
        self.assertGreaterEqual(len(p0_findings), 1, "Should detect at least one P0 NotImplementedError stub")

    def test_audit_counts_modules_and_tests(self) -> None:
        """Module and test detection should classify files correctly."""
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        self.assertGreaterEqual(len(report.modules_detected), 1)
        self.assertGreaterEqual(len(report.test_suites_detected), 1)

    def test_audit_health_score_penalizes_p0(self) -> None:
        """Health score should drop below 100 for P0 findings."""
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        self.assertLess(report.overall_health_score, 100)

    def test_audit_emits_markdown_report(self) -> None:
        """Audit should write a markdown report to disk."""
        out = os.path.join(self.tmpdir, "audit.md")
        ProjectAuditor.audit_project(target_dir=self.tmpdir, output_report_path=out)
        self.assertTrue(os.path.exists(out))
        with open(out, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Enterprise Health Score", content)

    def test_audit_report_pillars_assessed(self) -> None:
        """All 5 pillars should be listed in the report."""
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        self.assertEqual(len(report.pillars_assessed), 5)


class TestProjectAuditorSecurityPillar(unittest.TestCase):
    """Tests Pillar 3: AppSec & Secret Safety."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="sec_test_")
        src_dir = os.path.join(self.tmpdir, "src")
        os.makedirs(src_dir)

        # Create a file with a timing-unsafe comparison on tokens (detectable by Pillar 3)
        with open(os.path.join(src_dir, "config.py"), "w") as f:
            f.write('def check_auth(token: str) -> bool:\n    if token == "expected_password":\n        return True\n    return False\n')

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_detects_hardcoded_secrets(self) -> None:
        """Should detect timing-unsafe token comparisons in source files."""
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        sec_findings = [f for f in report.findings if "AppSec" in f.pillar]
        self.assertGreaterEqual(len(sec_findings), 1, "Should flag at least one timing-unsafe token comparison")


class TestProjectAuditorTypeSafety(unittest.TestCase):
    """Tests Pillar 1: TypeScript any detection."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="ts_test_")
        src_dir = os.path.join(self.tmpdir, "src")
        os.makedirs(src_dir)

        # TypeScript file with forbidden 'any' type
        with open(os.path.join(src_dir, "handler.ts"), "w") as f:
            f.write('function handle(data: any): void {\n  console.log(data);\n}\n')

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_detects_any_type_in_typescript(self) -> None:
        """Should flag ': any' in TypeScript files."""
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        any_findings = [f for f in report.findings if "'any'" in f.message]
        self.assertGreaterEqual(len(any_findings), 1)


class TestProjectAuditorAntiTamperPillar(unittest.TestCase):
    """Tests Pillar 5: Anti-Tamper cryptographic state attestation."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="tamper_test_")
        src_dir = os.path.join(self.tmpdir, "src")
        os.makedirs(src_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_flags_missing_crypto_attestation(self) -> None:
        """Should flag P1 if no sha256/merkle/timingsafe found in codebase."""
        with open(os.path.join(self.tmpdir, "src", "plain.py"), "w") as f:
            f.write('def simple(): return True\n')
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        tamper_findings = [f for f in report.findings if "Anti-Tamper" in f.pillar]
        self.assertGreaterEqual(len(tamper_findings), 1)

    def test_passes_when_merkle_present(self) -> None:
        """Should not flag when sha256/merkle references exist."""
        with open(os.path.join(self.tmpdir, "src", "integrity.py"), "w") as f:
            f.write('import hashlib\ndef verify(data):\n    return hashlib.sha256(data).hexdigest()\n')
        report = ProjectAuditor.audit_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        self.assertTrue(report.anti_tamper_compliant)


class TestProjectAuditorMarkdownBlueprint(unittest.TestCase):
    """Tests standalone solution document auditing."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="md_test_")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_flags_missing_moats_in_blueprint(self) -> None:
        """Blueprint lacking 4-moat matrix triggers P1 findings."""
        md_path = os.path.join(self.tmpdir, "solution.md")
        with open(md_path, "w") as f:
            f.write("# My Solution\n\nJust a basic approach without moats.\n")
        report = ProjectAuditor.audit_project(
            target_dir=md_path,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        moat_findings = [f for f in report.findings if "Moat" in f.pillar]
        self.assertGreaterEqual(len(moat_findings), 1)

    def test_passes_complete_blueprint(self) -> None:
        """Blueprint with data ingestion moat, statutory, and COGS achieves high score."""
        md_path = os.path.join(self.tmpdir, "solution.md")
        with open(md_path, "w") as f:
            f.write(
                "# Solution\n\n## Data Ingestion Moat\nRaw protobufs\n\n"
                "## Statutory compliance\nBSA Section 63\n\n"
                "## Unit Economics\nCOGS is $0.0008/query with 85% margin.\n\n"
                "## Anti-Tamper\nSHA-256 Merkle chain attestation.\n"
            )
        report = ProjectAuditor.audit_project(
            target_dir=md_path,
            output_report_path=os.path.join(self.tmpdir, "audit.md")
        )
        self.assertGreaterEqual(report.overall_health_score, 70)


class TestProjectAuditorCaseC(unittest.TestCase):
    """Tests Case C: onboard_and_continue hybrid workflow."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="casec_test_")
        src_dir = os.path.join(self.tmpdir, "src")
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "service.py"), "w") as f:
            f.write('def run(): return "ok"\n')

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_onboard_returns_correct_structure(self) -> None:
        """onboard_and_continue should return lifecycle metadata dict."""
        result = ProjectAuditor.onboard_and_continue(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "remediation_audit.md")
        )
        self.assertIn("onboarded_repo", result)
        self.assertIn("baseline_stabilized", result)
        self.assertTrue(result["baseline_stabilized"])
        self.assertEqual(result["lifecycle_mode"], "CASE_C_ONBOARD_AND_CONTINUE")


class TestProjectAuditorRemediation(unittest.TestCase):
    """Tests Case B remediation flow."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="remed_test_")
        src_dir = os.path.join(self.tmpdir, "src")
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "clean.py"), "w") as f:
            f.write('def clean_func(): return True\n')

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_remediation_returns_status(self) -> None:
        """Remediation result should include status key."""
        result = ProjectAuditor.remediate_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "remediation_audit.md")
        )
        self.assertIn("status", result)
        self.assertEqual(result["status"], "REMEDIATION_COMPLETE")

    def test_remediation_reports_initial_score(self) -> None:
        """Remediation result should report the initial audit score."""
        result = ProjectAuditor.remediate_project(
            target_dir=self.tmpdir,
            output_report_path=os.path.join(self.tmpdir, "remediation_audit.md")
        )
        self.assertIn("initial_score", result)
        self.assertIsInstance(result["initial_score"], int)


class TestProjectAuditorFileNotFound(unittest.TestCase):
    """Edge case: nonexistent target path."""

    def test_raises_on_nonexistent_path(self) -> None:
        """Should raise FileNotFoundError for a target that doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            ProjectAuditor.audit_project(target_dir="/nonexistent/path/xyz123")


if __name__ == "__main__":
    unittest.main()
