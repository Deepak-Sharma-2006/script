"""
Test Suite for Presentation Engine Phase 2: Native Vector Visuals & Diagram Generator
Tests multi-tier architecture layout math, chevron pipeline geometry, native tech grids,
and compiles a 100% native vector 6-slide championship presentation.
"""

import unittest
import os
import shutil

from scripts.engine.schema import (
    DeckConfig, SlideSpec, SlideArchetype, DeckManifest, ColorPalette,
    TaggedItem, TaggedBulletListSpec, SubSectionSpec, MultiSectionColumnSpec,
    CalloutCardSpec, ProjectLinksCardSpec, TableSpec, TechGridSpec, TechCategoryColumn, TechBadge,
    CompetitorMatrixSpec, CompetitorMatrixRow,
    ServiceNodeSpec, ArchitectureTierSpec, ArchitectureDiagramSpec,
    ChevronStepSpec, ChevronPipelineSpec, StatMetricSpec, StatGridSpec
)
from scripts.engine.layout_solver import LayoutSolver, Rect
from scripts.engine.diagram_generator import DiagramGenerator
from scripts.engine.pptx_compiler import PPTXCompiler
from scripts.engine.render_bridge import compile_and_render_deck


class TestEnginePhase2(unittest.TestCase):

    def test_architecture_geometry_solver(self):
        """Validates multi-tier architecture layout math and containment."""
        spec = ArchitectureDiagramSpec(
            title="PRAVAH MICROSERVICE TOPOLOGY",
            tiers=[
                ArchitectureTierSpec(
                    tier_name="Tier 1: Edge & Ingestion Layer",
                    header_bg="#0F3A70",
                    nodes=[
                        ServiceNodeSpec(name="RPC Ingestion", bullets=["FastAPI Gateway", "Kafka Event Bus"]),
                        ServiceNodeSpec(name="Ledger Poller", bullets=["Mempool Stream", "P2P Node Sync"]),
                    ]
                ),
                ArchitectureTierSpec(
                    tier_name="Tier 2: Deep Forensic Analytics",
                    header_bg="#1E293B",
                    nodes=[
                        ServiceNodeSpec(name="Neo4j Graph Engine", bullets=["50k+ Node Traversal", "<180s Hop Analysis"]),
                        ServiceNodeSpec(name="Clustering Heuristics", bullets=["Deposit-Sweep Engine", "Hawala Ring Attributor"]),
                    ]
                ),
                ArchitectureTierSpec(
                    tier_name="Tier 3: Sovereign Storage & Cryptography",
                    header_bg="#334155",
                    nodes=[
                        ServiceNodeSpec(name="Section 63 Vault", bullets=["SHA-256 Hash Chaining", "BSA Admissible Store"]),
                        ServiceNodeSpec(name="STIX 2.1 Feeds", bullets=["CERT-In & FIU Export", "IoC Bundle Cache"]),
                    ]
                ),
                ArchitectureTierSpec(
                    tier_name="Tier 4: Law Enforcement Operations",
                    header_bg="#0D5CA8",
                    nodes=[
                        ServiceNodeSpec(name="Analyst Workspace", bullets=["Interactive Canvas", "1-Click Case Dossier"]),
                        ServiceNodeSpec(name="Automated Freeze Notice", bullets=["BNSS Sec 94 Dispatch", "Indian Exchange Bridge"]),
                    ]
                )
            ]
        )

        container = Rect(x=6.80, y=1.35, w=6.10, h=5.45)
        layout = DiagramGenerator.solve_architecture_layout(container, spec)

        self.assertEqual(len(layout.tiers), 4)
        self.assertEqual(len(layout.inter_tier_connectors), 3)

        for i, tier in enumerate(layout.tiers):
            # Tier containment
            self.assertGreaterEqual(tier.tier_rect.y, container.y - 0.01)
            self.assertLessEqual(tier.tier_rect.y + tier.tier_rect.h, container.y + container.h + 0.01)
            self.assertEqual(len(tier.nodes), 2)
            for node in tier.nodes:
                # Node containment within tier
                self.assertGreaterEqual(node.rect.x, tier.tier_rect.x)
                self.assertLessEqual(node.rect.x + node.rect.w, tier.tier_rect.x + tier.tier_rect.w + 0.01)
                self.assertGreaterEqual(node.rect.y, tier.header_rect.y + tier.header_rect.h)
                self.assertLessEqual(node.rect.y + node.rect.h, tier.tier_rect.y + tier.tier_rect.h + 0.01)

    def test_chevron_pipeline_solver(self):
        """Validates horizontal chevron process pipeline solver."""
        spec = ChevronPipelineSpec(
            title="• 4-Stage Forensic Pipeline :-",
            steps=[
                ChevronStepSpec(step_num="1", title="Raw Ingestion", subtitle="Kafka & Mempool", color="#1D4ED8"),
                ChevronStepSpec(step_num="2", title="Graph Analytics", subtitle="Neo4j 6-Hop", color="#2563EB"),
                ChevronStepSpec(step_num="3", title="Heuristic Attribution", subtitle="Deposit-to-Sweep", color="#0D9488"),
                ChevronStepSpec(step_num="4", title="BSA Legal Seal", subtitle="Sec 63 Evidence", color="#10B981")
            ],
            summary_text="Resolves complex money laundering chains in under 180 seconds."
        )

        container = Rect(x=0.40, y=3.00, w=5.80, h=1.80)
        layout = DiagramGenerator.solve_chevron_pipeline(container, spec)

        self.assertEqual(len(layout.steps), 4)
        for i in range(len(layout.steps) - 1):
            s_curr = layout.steps[i]
            s_next = layout.steps[i + 1]
            self.assertLessEqual(s_curr.rect.x + s_curr.rect.w, s_next.rect.x + 0.01)
            self.assertIsNotNone(s_curr.arrow_rect)

        last_step = layout.steps[-1]
        self.assertLessEqual(last_step.rect.x + last_step.rect.w, container.x + container.w + 0.01)

    def test_tech_grid_solver(self):
        """Validates multi-column categorized tech stack grid solver."""
        spec = TechGridSpec(
            title="TECHNOLOGIES TO BE USED:",
            columns=[
                TechCategoryColumn(
                    category="Core Backend & Graph",
                    header_color="#0F3A70",
                    badges=[
                        TechBadge(name="FastAPI / Python 3.12", color="#1D4ED8"),
                        TechBadge(name="Neo4j Graph Database", color="#0284C7"),
                        TechBadge(name="Apache Kafka Streams", color="#0D9488"),
                    ]
                ),
                TechCategoryColumn(
                    category="Intelligence & AI",
                    header_color="#1E293B",
                    badges=[
                        TechBadge(name="PyTorch GNN Models", color="#EA580C"),
                        TechBadge(name="STIX 2.1 Threat Intel", color="#D97706"),
                        TechBadge(name="Tron TRC-20 Parser", color="#6366F1"),
                    ]
                ),
                TechCategoryColumn(
                    category="Frontend & Law Tools",
                    header_color="#334155",
                    badges=[
                        TechBadge(name="Next.js 15 & Cytoscape", color="#1D4ED8"),
                        TechBadge(name="Section 63 BSA Hash Vault", color="#10B981"),
                        TechBadge(name="TailwindCSS & Lucide", color="#0284C7"),
                    ]
                ),
            ]
        )

        container = Rect(x=6.80, y=1.35, w=6.10, h=3.30)
        layout = DiagramGenerator.solve_tech_grid(container, spec)

        self.assertEqual(len(layout.columns), 3)
        for col in layout.columns:
            self.assertEqual(len(col.badges), 3)
            for i in range(len(col.badges) - 1):
                b_curr = col.badges[i]
                b_next = col.badges[i + 1]
                self.assertLessEqual(b_curr.rect.y + b_curr.rect.h, b_next.rect.y + 0.01)

    def test_compile_full_native_vector_deck(self):
        """
        Compiles a complete 6-slide championship presentation deck where Slides 2, 3, and 6
        employ 100% native vector diagrams (no raster diagram PNGs).
        """
        manifest = DeckManifest(
            deck_config=DeckConfig(
                title="PRAVAH: Sovereign On-Chain Hawala & Financial Crime De-Anonymization Engine",
                team_name="PRAVAH",
                team_subtitle="(प्रवाह)",
                colors=ColorPalette(
                    bullet_blue="#1D4ED8",
                    title_black="#0F172A",
                    accent_purple="#6366F1"
                )
            ),
            slides=[
                # Slide 1: Title Page
                SlideSpec(
                    slide_number=1,
                    title="Idea Title: Sovereign On-Chain Hawala & Financial Crime De-Anonymization Engine",
                    archetype=SlideArchetype.TITLE_PAGE,
                    title_metadata=[
                        ("Problem Statement ID – ", "1736"),
                        ("Problem Statement Title", "De-Anonymizing Cross-Border Hawala & Multi-Hop Crypto Laundering"),
                        ("Theme", "Smart Automation / Law Enforcement & National Cyber Security"),
                        ("PS Category", "Software"),
                        ("Team ID", "SIH2026-SOV-042"),
                        ("Team Name :- ", "PRAVAH")
                    ]
                ),
                # Slide 2: Technical Architecture (Native Multi-Tier Vector Diagram)
                SlideSpec(
                    slide_number=2,
                    title="TECHNICAL ARCHITECTURE",
                    archetype=SlideArchetype.SPLIT_LEFT_RIGHT,
                    left_column={
                        "component": TaggedBulletListSpec(
                            title="",
                            items=[
                                TaggedItem("Real-time Ingestion:-", "Decodes mempool and Tron TRC-20 energy usage patterns in <30ms."),
                                TaggedItem("Multi-Hop Heuristics:-", "Traverses 6+ hops to uncover deposit-to-sweep aggregation trees."),
                                TaggedItem("Graph Database Cluster:-", "Neo4j distributed engine handling 50k+ nodes with sub-180s graph traversal."),
                                TaggedItem("Court Admissible Ledger:-", "Automated cryptographic hash-chaining compliant with Section 63 BSA 2023."),
                                TaggedItem("Sovereign Interoperability:-", "Zero third-party SaaS dependencies, 100% on-premise air-gapped readiness."),
                                TaggedItem("Asymmetric AI Filter:-", "Capped heuristic confidence prevents false-positive accusations in court."),
                                TaggedItem("Automated Production Orders:-", "Generates Section 94 BNSS legal notices for Indian crypto exchanges.")
                            ],
                            tag_font_size=10.0,
                            body_font_size=8.8,
                            space_after_pt=2.5
                        )
                    },
                    right_column={
                        "diagram_component": ArchitectureDiagramSpec(
                            title="PRAVAH MICROSERVICE TOPOLOGY",
                            tiers=[
                                ArchitectureTierSpec(
                                    tier_name="Tier 1: Edge & Ingestion Layer",
                                    header_bg="#0F3A70",
                                    nodes=[
                                        ServiceNodeSpec(name="FastAPI Ingestion", bullets=["Kafka Event Streaming", "Tron/ETH Poller"]),
                                        ServiceNodeSpec(name="P2P Mempool Sniffer", bullets=["Zero-delay TX Catch", "Gas Anomaly Alert"]),
                                    ]
                                ),
                                ArchitectureTierSpec(
                                    tier_name="Tier 2: Deep Forensic Analytics",
                                    header_bg="#1E293B",
                                    nodes=[
                                        ServiceNodeSpec(name="Neo4j Graph Cluster", bullets=["50,000+ Node Subgraph", "<180s 6-Hop Traversal"]),
                                        ServiceNodeSpec(name="Clustering Heuristics", bullets=["Deposit-Sweep Engine", "Hawala Syndicate Model"]),
                                    ]
                                ),
                                ArchitectureTierSpec(
                                    tier_name="Tier 3: Sovereign Storage & Cryptography",
                                    header_bg="#334155",
                                    nodes=[
                                        ServiceNodeSpec(name="Section 63 BSA Vault", bullets=["SHA-256 Hash Chaining", "Cryptographic Manifest"]),
                                        ServiceNodeSpec(name="STIX 2.1 Threat Intel", bullets=["Automated IoC Dispatch", "FIU-IND STR/SAR Format"]),
                                    ]
                                ),
                                ArchitectureTierSpec(
                                    tier_name="Tier 4: Law Enforcement Operations",
                                    header_bg="#0D5CA8",
                                    nodes=[
                                        ServiceNodeSpec(name="Investigator Canvas", bullets=["Cytoscape Visual Map", "1-Click PDF Dossier"]),
                                        ServiceNodeSpec(name="Exchange Bridge", bullets=["Sec 94 BNSS Notices", "NCRP Suspect Feed"]),
                                    ]
                                )
                            ]
                        )
                    }
                ),
                # Slide 3: Methodology (Native Chevron Flow + Native Tech Grid)
                SlideSpec(
                    slide_number=3,
                    title="METHODOLOGY",
                    archetype=SlideArchetype.SPLIT_STACK_AND_GRID,
                    left_column={
                        "top_component": TaggedBulletListSpec(
                            title="",
                            items=[
                                TaggedItem("Step 1: Ledger Ingestion:-", "Stream transaction blocks from RPC endpoints and high-volume TRC-20 nodes."),
                                TaggedItem("Step 2: Subgraph Expansion:-", "Run bi-directional graph walk across Neo4j to flag intermediary mule wallets."),
                                TaggedItem("Step 3: Hawala Ring Extraction:-", "Apply deposit-to-sweep aggregation heuristics to identify off-ramp points."),
                                TaggedItem("Step 4: Court Evidentiary Seal:-", "Generate cryptographic certificate signed under Section 63 BSA 2023.")
                            ],
                            tag_font_size=9.5,
                            body_font_size=8.5,
                            space_after_pt=1.5
                        ),
                        "flow_component": ChevronPipelineSpec(
                            title="• Process Flow :-",
                            steps=[
                                ChevronStepSpec(step_num="1", title="Raw Ingestion", subtitle="Kafka Streams", color="#1D4ED8"),
                                ChevronStepSpec(step_num="2", title="Graph Build", subtitle="Neo4j Subgraph", color="#2563EB"),
                                ChevronStepSpec(step_num="3", title="Heuristic ML", subtitle="Hawala Attribution", color="#0D9488"),
                                ChevronStepSpec(step_num="4", title="BSA Seal", subtitle="Court Evidence", color="#10B981")
                            ],
                            summary_text="Resolves complex money laundering chains in under 180 seconds."
                        ),
                        "bottom_text": "Live continuous streaming enables real-time freezing before mule cash-out occurs."
                    },
                    right_column={
                        "tech_grid_component": TechGridSpec(
                            title="TECHNOLOGIES TO BE USED:",
                            columns=[
                                TechCategoryColumn(
                                    category="Core Backend & Graph",
                                    header_color="#0F3A70",
                                    badges=[
                                        TechBadge(name="FastAPI / Python 3.12", color="#1D4ED8"),
                                        TechBadge(name="Neo4j Graph Database", color="#0284C7"),
                                        TechBadge(name="Apache Kafka Streams", color="#0D9488"),
                                    ]
                                ),
                                TechCategoryColumn(
                                    category="Intelligence & AI",
                                    header_color="#1E293B",
                                    badges=[
                                        TechBadge(name="PyTorch GNN Models", color="#EA580C"),
                                        TechBadge(name="STIX 2.1 Threat Intel", color="#D97706"),
                                        TechBadge(name="Tron TRC-20 Parser", color="#6366F1"),
                                    ]
                                ),
                                TechCategoryColumn(
                                    category="Frontend & Law Tools",
                                    header_color="#334155",
                                    badges=[
                                        TechBadge(name="Next.js 15 & Cytoscape", color="#1D4ED8"),
                                        TechBadge(name="Section 63 BSA Hash Vault", color="#10B981"),
                                        TechBadge(name="TailwindCSS & Lucide", color="#0284C7"),
                                    ]
                                ),
                            ]
                        ),
                        "bottom_component": ProjectLinksCardSpec(
                            title="• Project Links Demo:-",
                            github_url="https://github.com/pravah-fiu/hawala-attribution-engine",
                            demo_url="https://pravah.fiu-cyberdefense.gov.in"
                        )
                    }
                ),
                # Slide 4: Feasibility & Viability
                SlideSpec(
                    slide_number=4,
                    title="FEASIBILITY AND VIABILITY",
                    archetype=SlideArchetype.TWO_COLUMN_SECTIONS,
                    left_column={
                        "component": MultiSectionColumnSpec(
                            sections=[
                                SubSectionSpec(
                                    heading="Feasibility :-",
                                    items=[
                                        "Technical: Scalable microservices resolving 50k+ nodes in <180s via Neo4j",
                                        "Economic: 100% sovereign open-source stack saving ₹100Cr+ in annual vendor licenses",
                                        "Operational: Simple visual canvas and automated 1-click Section 63 BSA legal export",
                                        "Social: Prevents illicit capital flight and protects citizen financial integrity"
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="Potential Challenges:-",
                                    items=[
                                        "Multi-jurisdictional non-cooperative offshore shell entities",
                                        "Layered crypto mixers and P2P Hawala cash-out rings",
                                        "Investigating officers lacking deep blockchain forensic expertise"
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="Mitigation Strategies:-",
                                    items=[
                                        "Deposit-to-sweep aggregation heuristics linking mule wallets to VASPs",
                                        "Automated Section 94 BNSS production notices for domestic exchanges",
                                        "1-Click plain-English court reports with verified hash chains"
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="Viability:-",
                                    items=[
                                        "Validated against historical cross-border money laundering typologies",
                                        "100% compliant with Make in India & Atmanirbhar Bharat defense directives"
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="Business Potential:-",
                                    items=[
                                        "Strategic deployment across FIU-IND, Enforcement Directorate, and CBI",
                                        "Direct integration into National Cybercrime Reporting Portal (NCRP)"
                                    ]
                                )
                            ]
                        )
                    },
                    right_column={
                        "top_component": MultiSectionColumnSpec(
                            sections=[
                                SubSectionSpec(
                                    heading="Use Cases:-",
                                    items=[
                                        "Trade-based money laundering & Hawala syndicate tracking",
                                        "Crypto extortion and centralized exchange cash-out attribution",
                                        "Court evidentiary submissions with Section 63 BSA compliance"
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="Challenges:-",
                                    items=[
                                        "Decentralized bridges breaking transaction lineage across sovereign chains",
                                        "Unregulated offshore VASPs delaying international freeze requests"
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="Solutions:-",
                                    items=[
                                        "Burner contract and destination memo parsing linking cross-chain flows",
                                        "Automated FIU-IND STR/SAR escalation dossiers for non-compliant entities"
                                    ]
                                )
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
                ),
                # Slide 5: Impact & Benefits
                SlideSpec(
                    slide_number=5,
                    title="IMPACT AND BENEFITS",
                    archetype=SlideArchetype.TOP_SPLIT_BOTTOM_TABLE,
                    top_left={
                        "component": MultiSectionColumnSpec(
                            sections=[
                                SubSectionSpec(
                                    heading="• Potential impact on the target audience:-",
                                    items=[
                                        "IOs & Analysts: Resolves complex transaction trails in minutes with legal kits.",
                                        "FIU-IND & ED: Centralized command and control with unified sovereign intelligence.",
                                        "Registered VASPs: Machine-readable freeze notices and automated STR compliance.",
                                        "National Economy: Protects foreign exchange reserves and curbs illegal tax evasion."
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="• Key Intelligence & Laundering Insights",
                                    items=[
                                        "82% of cross-border illicit crypto routes through just 15 offshore cash-out desks.",
                                        "First 2 hours ('Golden Window') critical: fund recovery rate drops by 80% after 5 hops.",
                                        "100% court admissibility achieved when forensic artifacts meet Section 63 BSA standards."
                                    ]
                                )
                            ]
                        )
                    },
                    top_right={
                        "component": MultiSectionColumnSpec(
                            sections=[
                                SubSectionSpec(
                                    heading="• Unique Outcomes from Our Solution",
                                    items=[
                                        "Investigation Speedup: Traces complex trails in <3 minutes (70x faster than manual).",
                                        "Asset Recovery Rate: Projected to increase asset freeze success by 65-80% in Golden Window.",
                                        "Sovereign Autonomy: 100% reduction in licensing fees paid to foreign SaaS vendors.",
                                        "Judicial Rigor: Zero inadmissibility risk via automated SHA-256 hash-chained certificates."
                                    ]
                                )
                            ]
                        )
                    },
                    bottom_section={
                        "component": TableSpec(
                            title="• Benefits of the Solution (Social, Economic, Environmental)",
                            headers=["Type", "Benefit", "Supporting Example"],
                            rows=[
                                ["Social", "Protection of national economic integrity & citizen wealth", "Stops terror financing, narcotic syndicates, and large-scale bank fraud heists."],
                                ["", "Dismantling organized cross-border mule networks", "Exposes hawala kingpins and unhosted wallet syndicates across state lines."],
                                ["Economic", "Preservation of Forex reserves & seizure of criminal assets", "Saves ₹100 Cr+ in foreign software licenses; aids recovery of ₹2,000+ Cr in tax fraud."],
                                ["", "Strengthened AML/CFT regulatory compliance", "Empowers FIU-IND with real-time auditability of registered reporting entities."],
                                ["Environmental", "100% paperless sovereign digital intelligence pipeline", "Replaces physical courier memos and manual case files with automated STIX 2.1 e-notices."]
                            ],
                            col_width_ratios=[1.8, 4.2, 4.5]
                        )
                    }
                ),
                # Slide 6: Research & References (Native Competitor Matrix + Native 8-Step Chevron Pipeline)
                SlideSpec(
                    slide_number=6,
                    title="RESEARCH AND REFERENCES",
                    archetype=SlideArchetype.TOP_SPLIT_BOTTOM_FLOW,
                    top_left={
                        "component": MultiSectionColumnSpec(
                            sections=[
                                SubSectionSpec(
                                    heading="• Research Papers & Legal Frameworks:",
                                    items=[
                                        "a. Meiklejohn, S., et al., 'A Fistful of Bitcoins: Characterizing Payments,' ACM IMC, 2013.",
                                        "b. Biryukov, A., et al., 'Deanonymisation of Clients in Bitcoin P2P Network,' ACM CCS, 2014.",
                                        "c. Ministry of Law & Justice, Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63.",
                                        "d. Ministry of Home Affairs, Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023, Section 94."
                                    ]
                                ),
                                SubSectionSpec(
                                    heading="• Existing On-Chain Intelligence Platforms:",
                                    items=[
                                        "a. Palantir Gotham / Foundry: https://www.palantir.com",
                                        "b. Chainalysis Reactor: https://www.chainalysis.com",
                                        "c. TRM Labs Forensics: https://www.trmlabs.com"
                                    ]
                                )
                            ]
                        )
                    },
                    left_column={
                        "component": ProjectLinksCardSpec(
                            title="• Project Links Demo:-",
                            github_url="https://github.com/pravah-fiu/hawala-attribution-engine",
                            demo_url="https://pravah.fiu-cyberdefense.gov.in",
                            centered=True
                        )
                    },
                    top_right={
                        "matrix_component": CompetitorMatrixSpec(
                            headers=["Forensic Capability / Feature", "PRAVAH (I4C)", "Chainalysis", "TRM Labs", "Merkle Science"],
                            rows=[
                                CompetitorMatrixRow("1. Tron TRC-20 Energy Model Decoding", [True, False, False, False]),
                                CompetitorMatrixRow("2. Deposit-to-Sweep Clustering Heuristics", [True, True, True, True]),
                                CompetitorMatrixRow("3. Section 63 BSA 2023 Evidentiary Hash Chain", [True, False, False, False]),
                                CompetitorMatrixRow("4. Sub-180s Bounded Graph Traversal (<3 min)", [True, True, False, False]),
                                CompetitorMatrixRow("5. Sovereign Air-Gapped On-Premise (No Data Leak)", [True, False, False, False]),
                                CompetitorMatrixRow("6. Automated BNSS Sec 94/106 Notice Engine", [True, False, False, False]),
                                CompetitorMatrixRow("7. Zero Forex License Cost (100% Sovereign Open)", [True, False, False, False]),
                            ]
                        )
                    },
                    bottom_section={
                        "flow_component": ChevronPipelineSpec(
                            title="• Research Flow:",
                            steps=[
                                ChevronStepSpec(step_num="1", title="Threat Landscape", subtitle="Problem ID", color="#1D4ED8"),
                                ChevronStepSpec(step_num="2", title="Ledger Audit", subtitle="On-Chain Scans", color="#2563EB"),
                                ChevronStepSpec(step_num="3", title="Gap Analysis", subtitle="Tron & BSA 2023", color="#4F46E5"),
                                ChevronStepSpec(step_num="4", title="Architecture", subtitle="UTDM Topology", color="#6366F1"),
                                ChevronStepSpec(step_num="5", title="Red/Blue Teams", subtitle="Adversarial Ops", color="#0284C7"),
                                ChevronStepSpec(step_num="6", title="System Core", subtitle="Neo4j & Kafka", color="#0D9488"),
                                ChevronStepSpec(step_num="7", title="Benchmarking", subtitle="Evidentiary Lab", color="#059669"),
                                ChevronStepSpec(step_num="8", title="Deployment", subtitle="Sovereign I4C", color="#10B981")
                            ]
                        )
                    }
                )
            ]
        )

        out_pptx = "specs/presentations/test_engine_v2_vector.pptx"
        out_pdf = "specs/presentations/test_engine_v2_vector.pdf"
        render_dir = "specs/presentations/rendered/test_engine_v2"

        # 1. Compile deck
        compiler = PPTXCompiler(manifest)
        compiler.compile(out_pptx)
        self.assertTrue(os.path.exists(out_pptx))

        # 2. Render bridge (PPTX -> PDF -> PNGs)
        images = compile_and_render_deck(manifest, out_pptx, out_pdf, render_dir, dpi=200)
        self.assertTrue(os.path.exists(out_pdf))
        self.assertEqual(len(images), 6)
        for img in images:
            self.assertTrue(os.path.exists(img))

        # Cleanup transient test presentation & render directory
        for p in [out_pptx, out_pdf]:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(render_dir):
            shutil.rmtree(render_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
