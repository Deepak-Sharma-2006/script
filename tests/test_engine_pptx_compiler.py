"""
Test Suite — Presentation Engine Phase 1 Verification
Validates:
1. Mathematical text-fitting and dynamic font scaling.
2. Collision-free archetype geometry validation.
3. End-to-end declarative manifest compilation to PPTX, COM export to PDF, and PyMuPDF rendering.
"""

import os
import sys
import shutil
import unittest

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath("."))

from scripts.engine import (
    DeckConfig, SlideSpec, SlideArchetype, DeckManifest, ColorPalette,
    TaggedItem, TaggedBulletListSpec, SubSectionSpec, MultiSectionColumnSpec,
    CalloutCardSpec, ProjectLinksCardSpec, TableSpec,
    LayoutSolver, Rect, PPTXCompiler, compile_and_render_deck
)


class TestLayoutSolver(unittest.TestCase):

    def test_text_height_estimation(self):
        """Validates that text height estimation increases with character count."""
        short_txt = "Short title text."
        long_txt = "This is a much longer paragraph describing multi-tier architecture, sovereign cyber intelligence, and on-chain graph traversal across 10,000+ nodes in under 180 seconds with Section 63 BSA compliance."

        h_short = LayoutSolver.estimate_text_height(short_txt, container_width_inches=5.8, font_size_pt=10.0)
        h_long = LayoutSolver.estimate_text_height(long_txt, container_width_inches=5.8, font_size_pt=10.0)

        self.assertGreater(h_long, h_short)
        self.assertGreater(h_short, 0.15)
        self.assertLess(h_long, 2.0)

    def test_fit_text_block_shrink_to_fit(self):
        """Validates that fit_text_block dynamically reduces font size to fit bounded height."""
        long_items = [
            {"text": f"Item {i}: Advanced high-throughput telemetry ingestion normalizing multi-chain UTXO and account ledgers into canonical graph schemas.", "is_bold": False}
            for i in range(8)
        ]

        container_width = 5.8
        max_height = 2.50 # Bounded height

        opt_font, opt_space, computed_h = LayoutSolver.fit_text_block(
            long_items,
            container_width=container_width,
            max_height=max_height,
            base_font_size=11.0,
            min_font_size=7.5,
            base_space_after=2.0
        )

        self.assertLessEqual(computed_h, max_height + 0.10)
        self.assertLessEqual(opt_font, 10.0)
        self.assertGreaterEqual(opt_font, 7.5)

    def test_archetype_geometries_zero_collision(self):
        """Validates that all standard slide archetypes have zero internal bounding box collisions."""
        for arch in [
            SlideArchetype.TITLE_PAGE,
            SlideArchetype.SPLIT_LEFT_RIGHT,
            SlideArchetype.SPLIT_STACK_AND_GRID,
            SlideArchetype.TWO_COLUMN_SECTIONS,
            SlideArchetype.TOP_SPLIT_BOTTOM_TABLE,
            SlideArchetype.TOP_SPLIT_BOTTOM_FLOW
        ]:
            regions = LayoutSolver.get_archetype_layout(arch)
            errors = LayoutSolver.validate_slide_geometry(regions)
            self.assertEqual(len(errors), 0, f"Archetype {arch} has geometry errors: {errors}")


class TestEndToEndPresentationCompilation(unittest.TestCase):

    def test_full_6_slide_manifest_compilation(self):
        """Builds, compiles, exports to PDF, and renders a 6-slide test presentation."""
        config = DeckConfig(
            title="PRAVAH – Autonomous Cross-Border Financial Intelligence",
            team_name="PRAVAH",
            team_subtitle="(प्रवाह)",
            footer_text="@SIH Idea submission- Template",
            sih_logo_small="specs/presentations/assets/sih_logo_header.png",
            sih_logo_large="specs/presentations/assets/sih_logo_large.png"
        )

        # Slide 1: Title Page
        slide1 = SlideSpec(
            slide_number=1,
            title="TITLE PAGE",
            archetype=SlideArchetype.TITLE_PAGE,
            title_metadata=[
                ("Problem Statement ID – ", "SIH2026-MHA-FIN-03"),
                ("Problem Statement Title – ", "Autonomous Multi-Jurisdictional Cross-Border Hawala & Crypto Laundering Attribution Engine"),
                ("Theme – ", "National Security & Economic Intelligence"),
                ("PS Category – ", "Software"),
                ("Team ID – ", "69110"),
                ("Team Name :- ", "PRAVAH (प्रवाह)"),
                ("Target Organization :- ", "Enforcement Directorate (ED) | Financial Intelligence Unit (FIU-IND)")
            ]
        )

        # Slide 2: Idea Title & Proposed Solution
        slide2 = SlideSpec(
            slide_number=2,
            title="IDEA TITLE",
            archetype=SlideArchetype.SPLIT_LEFT_RIGHT,
            left_column={
                "component": TaggedBulletListSpec(
                    title="• Proposed Solution :-",
                    title_font_size=21.0,
                    body_font_size=9.5,
                    items=[
                        TaggedItem("Cross-Border Settlement Aggregator:-", "Reconstructs informal money transfer corridors by correlating banking SWIFT telemetry with on-chain VDA liquidity pools."),
                        TaggedItem("Peeling Chain & Mixer Filter:-", "Unmasks nested intermediary mule hops and strips CoinJoin/Whirlpool taint in <180s."),
                        TaggedItem("Asymmetric Confidence Scorer:-", "Applies strict 0.65 hard cap on probabilistic AI signals, requiring deterministic cryptographic links for High Confidence."),
                        TaggedItem("Section 63 BSA 2023 Evidentiary Dossier:-", "Generates court-admissible forensic packages with SHA-256 hash chains, RFC 3161 timestamps, and Section 94 BNSS notices.")
                    ]
                )
            },
            right_column={
                "image_path": "specs/presentations/assets/chakra_architecture_diagram.png"
            }
        )

        # Slide 3: Technical Approach
        slide3 = SlideSpec(
            slide_number=3,
            title="TECHNICAL APPROACH",
            archetype=SlideArchetype.SPLIT_STACK_AND_GRID,
            left_column={
                "top_component": TaggedBulletListSpec(
                    title="• Technologies to be Used:-",
                    title_font_size=20.0,
                    body_font_size=9.0,
                    space_after_pt=1.5,
                    items=[
                        TaggedItem("Ingestion & Telemetry:-", "Go RPC workers, Python Celery async queues, Kafka event streaming"),
                        TaggedItem("Databases:-", "Neo4j 5 Graph DB, TimescaleDB, Elasticsearch 8 vector store"),
                        TaggedItem("AI & Graph Neural Nets:-", "PyTorch Geometric, NetworkX volume entropy, RoBERTa embeddings"),
                        TaggedItem("Legal & Forensics:-", "OpenSSL SHA-256, RFC 3161 TSP, ReportLab court report generator")
                    ]
                ),
                "mid_image_path": "specs/presentations/assets/chakra_process_flow.png",
                "bottom_text": "SWIFT Telemetry Ingestion → UTDM Schema Normalization → Neo4j Bounded BFS → Hawala Mule Attribution → BSA Sec 63 Court Dossier"
            },
            right_column={
                "top_image_path": "specs/presentations/assets/chakra_tech_stack_grid.png",
                "bottom_component": ProjectLinksCardSpec(
                    github_url="https://github.com/pravah-fiu/hawala-attribution-engine",
                    demo_url="https://pravah.fiu-cyberdefense.gov.in"
                )
            }
        )

        # Slide 4: Feasibility and Viability
        slide4 = SlideSpec(
            slide_number=4,
            title="FEASIBILITY AND VIABILITY",
            archetype=SlideArchetype.TWO_COLUMN_SECTIONS,
            left_column={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("Feasibility :-", [
                            "Technical: Scalable microservices resolving 50k+ nodes in <180s via Neo4j",
                            "Economic: 100% sovereign open-source stack saving ₹100Cr+ in annual vendor licenses",
                            "Operational: Simple visual canvas and automated 1-click Section 63 BSA legal export",
                            "Social: Prevents illicit capital flight and protects citizen financial integrity"
                        ]),
                        SubSectionSpec("Potential Challenges:-", [
                            "Multi-jurisdictional non-cooperative offshore shell entities",
                            "Layered crypto mixers and P2P Hawala cash-out rings",
                            "Investigating officers lacking deep blockchain forensic expertise"
                        ]),
                        SubSectionSpec("Mitigation Strategies:-", [
                            "Deposit-to-sweep aggregation heuristics linking mule wallets to VASPs",
                            "Automated Section 94 BNSS production notices for domestic exchanges",
                            "1-Click plain-English court reports with verified hash chains"
                        ]),
                        SubSectionSpec("Viability:-", [
                            "Validated against historical cross-border money laundering typologies",
                            "100% compliant with Make in India & Atmanirbhar Bharat defense directives"
                        ]),
                        SubSectionSpec("Business Potential:-", [
                            "Strategic deployment across FIU-IND, Enforcement Directorate, and CBI",
                            "Direct integration into National Cybercrime Reporting Portal (NCRP)"
                        ])
                    ]
                )
            },
            right_column={
                "top_component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("Use Cases:-", [
                            "Trade-based money laundering & Hawala syndicate tracking",
                            "Crypto extortion and centralized exchange cash-out attribution",
                            "Court evidentiary submissions with Section 63 BSA compliance"
                        ]),
                        SubSectionSpec("Challenges:-", [
                            "Decentralized bridges breaking transaction lineage across sovereign chains",
                            "Unregulated offshore VASPs delaying international freeze requests"
                        ]),
                        SubSectionSpec("Solutions:-", [
                            "Burner contract and destination memo parsing linking cross-chain flows",
                            "Automated FIU-IND STR/SAR escalation dossiers for non-compliant entities"
                        ])
                    ]
                ),
                "bottom_component": CalloutCardSpec(
                    title="SUPPORTING FACTS FOR FEASIBILITY AND VIABILITY",
                    facts=[
                        "Over ₹30,000 Crore laundered annually through illicit trade & crypto mule corridors in India.",
                        "PRAVAH resolves complex cross-border 6-hop chains in <180s vs 21+ days for manual requests.",
                        "Strict 0.65 asymmetric AI cap prevents false-positive accusations in court.",
                        "100% sovereign deployment eliminates ₹100+ Crore annual forex outflow to foreign vendors."
                    ]
                )
            }
        )

        # Slide 5: Impact and Benefits
        slide5 = SlideSpec(
            slide_number=5,
            title="IMPACT AND BENEFITS",
            archetype=SlideArchetype.TOP_SPLIT_BOTTOM_TABLE,
            top_left={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("• Potential impact on the target audience:-", [
                            "IOs & Analysts: Resolves complex transaction trails in minutes with legal kits.",
                            "FIU-IND & ED: Centralized command and control with unified sovereign intelligence.",
                            "Registered VASPs: Machine-readable freeze notices and automated STR compliance.",
                            "National Economy: Protects foreign exchange reserves and curbs illegal tax evasion."
                        ], heading_font_size=16.0),
                        SubSectionSpec("• Key Intelligence & Laundering Insights", [
                            "82% of cross-border illicit crypto routes through just 15 offshore cash-out desks.",
                            "First 2 hours ('Golden Window') critical: fund recovery rate drops by 80% after 5 hops.",
                            "100% court admissibility achieved when forensic artifacts meet Section 63 BSA standards."
                        ], heading_font_size=15.0)
                    ]
                )
            },
            top_right={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("• Unique Outcomes from Our Solution", [
                            "Investigation Speedup: Traces complex trails in <3 minutes (70x faster than manual).",
                            "Asset Recovery Rate: Projected to increase asset freeze success by 65-80% in Golden Window.",
                            "Sovereign Autonomy: 100% reduction in licensing fees paid to foreign SaaS vendors.",
                            "Judicial Rigor: Zero inadmissibility risk via automated SHA-256 hash-chained certificates."
                        ], heading_font_size=16.0)
                    ]
                )
            },
            bottom_section={
                "component": TableSpec(
                    title="• Benefits of the Solution (Social, Economic, Environmental)",
                    headers=["Type", "Benefit", "Supporting Example"],
                    col_width_ratios=[2.2, 4.8, 5.333],
                    rows=[
                        ["Social", "Protection of national economic integrity & citizen wealth", "Stops terror financing, narcotic syndicates, and large-scale bank fraud heists."],
                        ["", "Dismantling organized cross-border mule networks", "Exposes hawala kingpins and unhosted wallet syndicates across state lines."],
                        ["Economic", "Preservation of Forex reserves & seizure of criminal assets", "Saves ₹100 Cr+ in foreign software licenses; aids recovery of ₹2,000+ Cr in tax fraud."],
                        ["", "Strengthened AML/CFT regulatory compliance", "Empowers FIU-IND with real-time auditability of registered reporting entities."],
                        ["Environmental", "100% paperless sovereign digital intelligence pipeline", "Replaces physical courier memos and manual case files with automated STIX 2.1 e-notices."]
                    ]
                )
            }
        )

        # Slide 6: Research and References
        slide6 = SlideSpec(
            slide_number=6,
            title="RESEARCH AND REFERENCES",
            archetype=SlideArchetype.TOP_SPLIT_BOTTOM_FLOW,
            top_left={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("• Research Papers & Legal Frameworks:", [
                            "a. Meiklejohn, S., et al., 'A Fistful of Bitcoins: Characterizing Payments,' ACM IMC, 2013.",
                            "b. Biryukov, A., et al., 'Deanonymisation of Clients in Bitcoin P2P Network,' ACM CCS, 2014.",
                            "c. Ministry of Law & Justice, Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63.",
                            "d. Ministry of Home Affairs, Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023, Section 94."
                        ], heading_font_size=16.0),
                        SubSectionSpec("• Existing On-Chain Intelligence Platforms:", [
                            "a. Palantir Gotham / Foundry: https://www.palantir.com",
                            "b. Chainalysis Reactor: https://www.chainalysis.com",
                            "c. TRM Labs Forensics: https://www.trmlabs.com"
                        ], heading_font_size=15.0)
                    ]
                )
            },
            left_column={
                "component": ProjectLinksCardSpec(
                    title="• Project Links Demo:-",
                    github_url="https://github.com/pravah-fiu/hawala-attribution-engine",
                    demo_url="https://pravah.fiu-cyberdefense.gov.in"
                )
            },
            top_right={
                "image_path": "specs/presentations/assets/chakra_competitor_matrix.png"
            },
            bottom_section={
                "title": "• Research Flow:",
                "flow_image_path": "specs/presentations/assets/chakra_research_flow.png"
            }
        )

        manifest = DeckManifest(
            deck_config=config,
            slides=[slide1, slide2, slide3, slide4, slide5, slide6]
        )

        pptx_path = "specs/presentations/test_engine_deck.pptx"
        pdf_path = "specs/presentations/test_engine_deck.pdf"
        render_dir = "specs/presentations/rendered/test_engine"

        rendered_images = compile_and_render_deck(
            manifest,
            pptx_path=pptx_path,
            pdf_path=pdf_path,
            render_dir=render_dir,
            slide_prefix="test_slide",
            dpi=200
        )

        self.assertTrue(os.path.exists(pptx_path))
        self.assertTrue(os.path.exists(pdf_path))
        self.assertEqual(len(rendered_images), 6)
        for img in rendered_images:
            self.assertTrue(os.path.exists(img))
            self.assertGreater(os.path.getsize(img), 50000)
            print(f"Verified test slide image: {img} ({os.path.getsize(img)} bytes)")

        # Cleanup transient test presentation & render directory
        for p in [pptx_path, pdf_path]:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(render_dir):
            shutil.rmtree(render_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
