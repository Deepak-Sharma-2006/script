"""
Test Suite for Presentation Engine Phase 3 & 4: Multi-Theme System & Autonomous Agentic Creator
Tests theme registries, visual auditor heuristics, and compiles complete presentations
in both SIH Light and Cyber Dark themes from raw technical problem specifications.
"""

import unittest
import os
import shutil

from scripts.engine.themes import THEMES, get_theme
from scripts.engine.visual_auditor import VisualAuditor
from scripts.engine.agent_creator import AgentDeckCreator


class TestEngineMultiTheme(unittest.TestCase):

    def test_themes_registry(self):
        """Verifies that all registered themes have valid color tokens and attributes."""
        expected_themes = [
            "sih_institutional_light",
            "cyber_dark_terminal",
            "enterprise_slate",
            "modern_fintech"
        ]
        for name in expected_themes:
            self.assertIn(name, THEMES)
            theme = get_theme(name)
            self.assertTrue(theme.canvas_bg.startswith("#"))
            self.assertTrue(theme.bullet_accent.startswith("#"))
            self.assertTrue(theme.title_primary.startswith("#"))
            self.assertIsNotNone(theme.font_title)
            self.assertIsNotNone(theme.font_body)

    def test_visual_auditor_heuristics(self):
        """Validates automated visual layout and density auditing."""
        raw_spec = {
            "team_name": "BHEDAK",
            "team_subtitle": "(भेदक)",
            "problem_id": "SIH-1740",
            "problem_title": "Deepfake Video & Audio Detection for National Cyber Defense",
            "solution_title": "Autonomous Forensic AI for Real-time Media Authentication",
            "architecture_tiers": [
                {
                    "name": "Tier 1: Multimodal Ingestion",
                    "nodes": [
                        {"name": "Video Frame Extractor", "bullets": ["4K 60fps Pipeline", "Face Crop Alignment"]},
                        {"name": "Audio Spectral Slicer", "bullets": ["Mel-Spectrogram", "Phase Inconsistency"]}
                    ]
                },
                {
                    "name": "Tier 2: Neural Forensic Engine",
                    "nodes": [
                        {"name": "Spatiotemporal GNN", "bullets": ["Facial Muscle Jitter", "Eye Blinking Cadence"]},
                        {"name": "Voice Bio-Acoustic NN", "bullets": ["Synthetic Vocoder Detection", "Formant Analysis"]}
                    ]
                },
                {
                    "name": "Tier 3: Judicial Seal & Vault",
                    "nodes": [
                        {"name": "SHA-256 Chain Store", "bullets": ["Section 63 BSA Hash", "Immutable Audit"]},
                        {"name": "CERT-In IoC Dispatch", "bullets": ["STIX 2.1 Bundles", "NCRP Live Feed"]}
                    ]
                }
            ]
        }

        manifest = AgentDeckCreator.synthesize_manifest_from_spec(raw_spec, theme_name="cyber_dark_terminal")
        audit_report = VisualAuditor.audit_deck(manifest)

        self.assertEqual(audit_report.total_slides, 6)
        self.assertTrue(audit_report.passed, f"Audit failed with violations: {audit_report.violations}")
        self.assertEqual(len(audit_report.violations), 0)

    def test_agent_creator_end_to_end_sih_light(self):
        """
        Synthesizes, audits, and renders a complete 6-slide deck in SIH Institutional Light theme.
        """
        spec = {
            "team_name": "PRAVAH",
            "team_subtitle": "(प्रवाह)",
            "problem_id": "1736",
            "problem_title": "De-Anonymizing Cross-Border Hawala & Multi-Hop Crypto Laundering",
            "solution_title": "Sovereign On-Chain Hawala Attribution Engine",
            "architecture_tiers": [
                {
                    "name": "Tier 1: Edge & Ingestion Layer",
                    "nodes": [
                        {"name": "FastAPI Ingestion", "bullets": ["Kafka Event Streaming", "Tron/ETH Poller"]},
                        {"name": "P2P Mempool Sniffer", "bullets": ["Zero-delay TX Catch", "Gas Anomaly Alert"]}
                    ]
                },
                {
                    "name": "Tier 2: Deep Forensic Analytics",
                    "nodes": [
                        {"name": "Neo4j Graph Cluster", "bullets": ["50,000+ Node Subgraph", "<180s 6-Hop Traversal"]},
                        {"name": "Clustering Heuristics", "bullets": ["Deposit-Sweep Engine", "Hawala Syndicate Model"]}
                    ]
                },
                {
                    "name": "Tier 3: Sovereign Storage & Vault",
                    "nodes": [
                        {"name": "Section 63 BSA Vault", "bullets": ["SHA-256 Hash Chaining", "Cryptographic Manifest"]},
                        {"name": "STIX 2.1 Threat Intel", "bullets": ["Automated IoC Dispatch", "FIU-IND STR/SAR Format"]}
                    ]
                },
                {
                    "name": "Tier 4: Law Enforcement Operations",
                    "nodes": [
                        {"name": "Investigator Canvas", "bullets": ["Cytoscape Visual Map", "1-Click PDF Dossier"]},
                        {"name": "Exchange Bridge", "bullets": ["Sec 94 BNSS Notices", "NCRP Suspect Feed"]}
                    ]
                }
            ],
            "supporting_facts": [
                "Over ₹30,000 Crore laundered annually through illicit trade & crypto mule corridors in India.",
                "PRAVAH resolves complex cross-border 6-hop chains in <180s vs 21+ days for manual requests.",
                "Strict 0.65 asymmetric AI cap prevents false-positive accusations in court.",
                "100% sovereign deployment eliminates ₹100+ Crore annual forex outflow to foreign vendors."
            ]
        }

        out_pptx = "specs/presentations/deck_sih_light_agent.pptx"
        out_pdf = "specs/presentations/deck_sih_light_agent.pdf"
        render_dir = "specs/presentations/rendered/multitheme_sih"

        manifest, audit, images = AgentDeckCreator.create_deck(
            spec=spec,
            output_pptx_path=out_pptx,
            output_pdf_path=out_pdf,
            render_dir=render_dir,
            theme_name="sih_institutional_light",
            dpi=200
        )

        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_pdf))
        self.assertEqual(len(images), 6)
        self.assertTrue(audit.passed)

        # Cleanup transient test presentation & render directory
        for p in [out_pptx, out_pdf]:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(render_dir):
            shutil.rmtree(render_dir, ignore_errors=True)

    def test_agent_creator_end_to_end_cyber_dark(self):
        """
        Synthesizes, audits, and renders a complete 6-slide deck in Cyber Dark Terminal theme.
        """
        spec = {
            "team_name": "BHEDAK",
            "team_subtitle": "(भेदक)",
            "problem_id": "SIH-1740",
            "problem_title": "Deepfake Video & Audio Detection for National Cyber Defense",
            "solution_title": "Autonomous Forensic AI for Real-time Media Authentication",
            "architecture_tiers": [
                {
                    "name": "Tier 1: Multimodal Ingestion Layer",
                    "nodes": [
                        {"name": "Video Stream Demuxer", "bullets": ["4K 60fps Real-Time", "Facial Landmark Crop"]},
                        {"name": "Acoustic Signal Slicer", "bullets": ["Mel-Spectrogram Analysis", "Phase Inconsistency"]}
                    ]
                },
                {
                    "name": "Tier 2: Neural Forensic Core",
                    "nodes": [
                        {"name": "Spatiotemporal GNN", "bullets": ["Blood Flow Photoplethysmography", "Biological Micro-Tremor"]},
                        {"name": "Vocoder Artifact Detector", "bullets": ["Diffusion Spectral Leak", "TTS Fingerprint Match"]}
                    ]
                },
                {
                    "name": "Tier 3: Sovereign Cryptography & Vault",
                    "nodes": [
                        {"name": "Section 63 BSA Hash Chain", "bullets": ["SHA-256 Evidence Manifest", "Tamper-Proof Ledger"]},
                        {"name": "STIX 2.1 Threat Intel", "bullets": ["CERT-In IoC Feeds", "Law Enforcement Dispatch"]}
                    ]
                },
                {
                    "name": "Tier 4: Operational Defense Dashboard",
                    "nodes": [
                        {"name": "Analyst Triage Canvas", "bullets": ["Heatmap Anomaly Overlay", "1-Click Court Kit"]},
                        {"name": "Takedown Dispatch Engine", "bullets": ["IT Act Sec 79 Notices", "Social Media API Bridge"]}
                    ]
                }
            ],
            "supporting_facts": [
                "Over 840,000 deepfake impersonation attacks detected in financial & defense fraud in 2025-26.",
                "BHEDAK achieves 98.6% adversarial accuracy on unseen diffusion and voice-cloning models.",
                "Sub-250ms latency allows live stream interdiction before virality occurs.",
                "100% sovereign air-gapped architecture guarantees zero defense biometric leaks to foreign clouds."
            ]
        }

        out_pptx = "specs/presentations/deck_cyber_dark_agent.pptx"
        out_pdf = "specs/presentations/deck_cyber_dark_agent.pdf"
        render_dir = "specs/presentations/rendered/multitheme_cyber_dark"

        manifest, audit, images = AgentDeckCreator.create_deck(
            spec=spec,
            output_pptx_path=out_pptx,
            output_pdf_path=out_pdf,
            render_dir=render_dir,
            theme_name="cyber_dark_terminal",
            dpi=200
        )

        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_pdf))
        self.assertEqual(len(images), 6)
        self.assertTrue(audit.passed)

        # Cleanup transient test presentation & render directory
        for p in [out_pptx, out_pdf]:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(render_dir):
            shutil.rmtree(render_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
