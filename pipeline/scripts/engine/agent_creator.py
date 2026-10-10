"""
Presentation Engine — Autonomous Agentic Deck Creator
Synthesizes championship-tier presentations from raw problem statements and ideas.
Orchestrates DSL synthesis, diagram generation, theme application, layout compilation, and visual QA.
"""

from typing import Dict, Any, List, Optional, Tuple
import os

from scripts.engine.schema import (
    DeckConfig, SlideSpec, SlideArchetype, DeckManifest, ColorPalette,
    TaggedItem, TaggedBulletListSpec, SubSectionSpec, MultiSectionColumnSpec,
    CalloutCardSpec, ProjectLinksCardSpec, TableSpec, TechGridSpec, TechCategoryColumn, TechBadge,
    CompetitorMatrixSpec, CompetitorMatrixRow,
    ServiceNodeSpec, ArchitectureTierSpec, ArchitectureDiagramSpec,
    ChevronStepSpec, ChevronPipelineSpec, StatMetricSpec, StatGridSpec
)
from scripts.engine.themes import get_theme, Theme
from scripts.engine.pptx_compiler import PPTXCompiler
from scripts.engine.visual_auditor import VisualAuditor, DeckAuditReport
from scripts.engine.render_bridge import compile_and_render_deck


class AgentDeckCreator:
    """
    Autonomous engine that translates structured or semi-structured problem specifications
    into production-grade presentation decks with zero manual coordinate adjustments.
    """

    @classmethod
    def synthesize_manifest_from_spec(cls, spec: Dict[str, Any], theme_name: str = "sih_institutional_light") -> DeckManifest:
        """
        Constructs a complete 6-slide championship presentation manifest from raw inputs.
        """
        theme = get_theme(theme_name)
        team_name = spec.get("team_name", "TEAM CHAMPION")
        team_sub = spec.get("team_subtitle", "")
        problem_id = spec.get("problem_id", "SIH-2026")
        problem_title = spec.get("problem_title", "Autonomous AI System")
        solution_title = spec.get("solution_title", "Next-Generation Intelligent Defense Platform")

        config = DeckConfig(
            title=f"{team_name}: {solution_title}",
            team_name=team_name,
            team_subtitle=team_sub,
            theme_name=theme_name,
            colors=ColorPalette(
                canvas_bg=theme.canvas_bg,
                bullet_blue=theme.bullet_accent,
                title_black=theme.title_primary,
                accent_purple=theme.team_badge_border,
                callout_bg=theme.callout_bg,
                callout_border=theme.callout_border,
                callout_text=theme.callout_text,
                success_green=theme.success_green,
                danger_red=theme.danger_red
            )
        )

        # Slide 1: Title Page
        slide_1 = SlideSpec(
            slide_number=1,
            title=f"Idea Title: {solution_title}",
            archetype=SlideArchetype.TITLE_PAGE,
            title_metadata=[
                ("Problem Statement ID – ", str(problem_id)),
                ("Problem Statement Title", problem_title),
                ("Theme", spec.get("theme_category", "Smart Automation / Advanced AI & Security")),
                ("PS Category", spec.get("ps_category", "Software")),
                ("Team ID", spec.get("team_id", f"SIH2026-{team_name}-01")),
                ("Team Name :- ", team_name)
            ]
        )

        # Slide 2: Technical Architecture
        arch_raw_tiers = spec.get("architecture_tiers", [])
        tiers = []
        for t in arch_raw_tiers:
            nodes = [ServiceNodeSpec(name=n["name"], bullets=n.get("bullets", [])) for n in t.get("nodes", [])]
            tiers.append(ArchitectureTierSpec(
                tier_name=t.get("name", "Tier"),
                header_bg=t.get("header_bg", theme.tier_header_bg),
                header_text_color=theme.tier_header_text,
                tier_bg=theme.tier_card_bg,
                border_color=theme.tier_card_border,
                nodes=nodes
            ))

        arch_bullets = spec.get("architecture_bullets", [
            TaggedItem("Core Innovation:-", "Distributed edge processing achieving sub-100ms response times."),
            TaggedItem("Graph Topology:-", "Scalable multi-hop linkage resolving complex entity relationships."),
            TaggedItem("Sovereign Security:-", "100% on-premise air-gapped deployment with zero external SaaS leakage."),
            TaggedItem("Judicial Compliance:-", "Cryptographic hash verification meeting strict evidentiary standards.")
        ])

        slide_2 = SlideSpec(
            slide_number=2,
            title="TECHNICAL ARCHITECTURE",
            archetype=SlideArchetype.SPLIT_LEFT_RIGHT,
            left_column={
                "component": TaggedBulletListSpec(
                    title="",
                    items=[TaggedItem(b[0], b[1]) if isinstance(b, (list, tuple)) else b for b in arch_bullets],
                    tag_font_size=10.0,
                    body_font_size=8.8,
                    space_after_pt=2.5
                )
            },
            right_column={
                "diagram_component": ArchitectureDiagramSpec(
                    title=f"{team_name} MICROSERVICE TOPOLOGY",
                    tiers=tiers,
                    flow_arrow_color=theme.flow_arrow_color,
                    container_bg=theme.arch_container_bg,
                    container_border=theme.arch_container_border
                )
            }
        )

        # Slide 3: Methodology & Tech Stack
        method_steps = spec.get("methodology_steps", [
            TaggedItem("Step 1: Input Ingestion:-", "Stream telemetry and transaction logs with real-time anomaly detection."),
            TaggedItem("Step 2: Subgraph Analysis:-", "Construct bi-directional linkage graph to identify risk nodes."),
            TaggedItem("Step 3: Core Attribution:-", "Apply machine learning heuristics to cluster malicious syndicates."),
            TaggedItem("Step 4: Evidence Sealing:-", "Generate immutable court-admissible audit reports with verified hashes.")
        ])

        flow_steps_raw = spec.get("process_flow", [
            ("1", "Ingestion", "Data Pipeline", theme.bullet_accent),
            ("2", "Processing", "Graph Analytics", theme.accent_purple),
            ("3", "ML Heuristics", "Pattern Match", theme.accent_cyan),
            ("4", "Sealing", "Court Evidence", theme.success_green)
        ])
        flow_steps = [ChevronStepSpec(s[0], s[1], s[2], s[3]) for s in flow_steps_raw]

        tech_cols_raw = spec.get("tech_stack", {
            "Core Backend": ["FastAPI", "Python 3.12", "Kafka Streams"],
            "Intelligence & DB": ["Neo4j Graph DB", "PyTorch Models", "Vector DB"],
            "Frontend & UI": ["Next.js 15", "Cytoscape.js", "TailwindCSS"]
        })
        tech_cols = []
        for cat, items in tech_cols_raw.items():
            tech_cols.append(TechCategoryColumn(
                category=cat,
                header_color=theme.tier_header_bg,
                badges=[TechBadge(name=it, color=theme.bullet_accent) for it in items]
            ))

        slide_3 = SlideSpec(
            slide_number=3,
            title="METHODOLOGY",
            archetype=SlideArchetype.SPLIT_STACK_AND_GRID,
            left_column={
                "top_component": TaggedBulletListSpec(
                    title="",
                    items=[TaggedItem(s[0], s[1]) if isinstance(s, (list, tuple)) else s for s in method_steps],
                    tag_font_size=9.5,
                    body_font_size=8.5,
                    space_after_pt=1.5
                ),
                "flow_component": ChevronPipelineSpec(
                    title="• Process Flow :-",
                    steps=flow_steps,
                    summary_text=spec.get("flow_summary", "Autonomous end-to-end pipeline executing in real-time.")
                ),
                "bottom_text": spec.get("flow_footer_note", "Live continuous execution ensures proactive intervention.")
            },
            right_column={
                "tech_grid_component": TechGridSpec(
                    title="TECHNOLOGIES TO BE USED:",
                    columns=tech_cols
                ),
                "bottom_component": ProjectLinksCardSpec(
                    title="• Project Links Demo:-",
                    github_url=spec.get("github_url", "https://github.com/sih-championship/solution-core"),
                    demo_url=spec.get("demo_url", "https://demo.sih-championship.gov.in")
                )
            }
        )

        # Slide 4: Feasibility & Viability
        slide_4 = SlideSpec(
            slide_number=4,
            title="FEASIBILITY AND VIABILITY",
            archetype=SlideArchetype.TWO_COLUMN_SECTIONS,
            left_column={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("Feasibility :-", spec.get("feasibility_bullets", [
                            "Technical: Scalable microservices handling peak load under 180s response times.",
                            "Economic: Open-source sovereign deployment eliminating recurring vendor licensing fees.",
                            "Operational: Intuitive operator canvas requiring zero deep specialized engineering training.",
                            "Social: Safeguards national critical infrastructure and citizens' digital security."
                        ])),
                        SubSectionSpec("Potential Challenges:-", spec.get("challenges_bullets", [
                            "Non-cooperative offshore hosting and obfuscated infrastructure.",
                            "Evolving adversarial tactics designed to evade conventional rule heuristics."
                        ])),
                        SubSectionSpec("Mitigation Strategies:-", spec.get("mitigation_bullets", [
                            "Continuous behavioral clustering and automated cross-border correlation.",
                            "1-Click verified audit kits ensuring full regulatory and legal admissibility."
                        ])),
                        SubSectionSpec("Viability & Business Potential:-", spec.get("viability_bullets", [
                            "Ready for deployment across central enforcement agencies and state departments.",
                            "100% aligned with national Make-in-India and digital sovereignty directives."
                        ]))
                    ]
                )
            },
            right_column={
                "top_component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("Use Cases:-", spec.get("use_cases", [
                            "Critical infrastructure monitoring and automated threat containment.",
                            "Cross-border financial forensics and sovereign asset recovery."
                        ])),
                        SubSectionSpec("Challenges & Solutions:-", [
                            "Offshore latency -> Local caching and asynchronous distributed streaming.",
                            "Regulatory reporting -> Automated 1-click legal compliance dossiers."
                        ])
                    ]
                ),
                "bottom_component": CalloutCardSpec(
                    title="SUPPORTING FACTS FOR FEASIBILITY AND VIABILITY",
                    facts=spec.get("supporting_facts", [
                        "Over ₹10,000+ Crore annual economic impact addressed by automated detection.",
                        "Solution reduces manual investigation timelines from 21+ days down to <3 minutes.",
                        "Zero foreign SaaS dependency eliminates hundreds of Crores in forex software outflows.",
                        "Cryptographic hash chaining guarantees 100% judicial evidentiary compliance."
                    ]),
                    bg_color=theme.callout_bg,
                    border_color=theme.callout_border
                )
            }
        )

        # Slide 5: Impact & Benefits
        table_rows = spec.get("benefits_table_rows", [
            ["Social", "Protection of national digital assets & citizen trust", "Prevents syndicates and large-scale digital fraud."],
            ["", "Strengthened public safety and rule of law", "Exposes illicit networks across regional jurisdictions."],
            ["Economic", "Preservation of foreign reserves & asset recovery", "Saves recurring SaaS fees and recovers defrauded assets."],
            ["", "Regulatory compliance and institutional agility", "Empowers government departments with real-time auditability."],
            ["Environmental", "100% paperless sovereign intelligence pipeline", "Replaces physical case binders with encrypted digital reports."]
        ])

        slide_5 = SlideSpec(
            slide_number=5,
            title="IMPACT AND BENEFITS",
            archetype=SlideArchetype.TOP_SPLIT_BOTTOM_TABLE,
            top_left={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("• Potential impact on the target audience:-", spec.get("impact_target_audience", [
                            "Investigating Officers: Automates complex forensic tracing in minutes.",
                            "Command Centers: Provides unified situational awareness and threat telemetry.",
                            "Regulated Entities: Machine-readable compliance notices and instant reporting."
                        ])),
                        SubSectionSpec("• Key Strategic Insights", spec.get("strategic_insights", [
                            "Early detection window is decisive: fund recovery drops by 80% after initial hops.",
                            "Rigorous evidentiary standards guarantee zero judicial dismissal in court."
                        ]))
                    ]
                )
            },
            top_right={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("• Unique Outcomes from Our Solution", spec.get("unique_outcomes", [
                            "Speed: 70x acceleration over manual workflows (<3 minutes vs days).",
                            "Recovery Rate: Projected 65-80% increase in timely asset freezes.",
                            "Sovereign Independence: Eliminates foreign SaaS vendor telemetry leakage.",
                            "Judicial Admissibility: Cryptographic SHA-256 verification on all artifacts."
                        ]))
                    ]
                )
            },
            bottom_section={
                "component": TableSpec(
                    title="• Benefits of the Solution (Social, Economic, Environmental)",
                    headers=["Type", "Benefit", "Supporting Example"],
                    rows=table_rows,
                    col_width_ratios=[1.8, 4.2, 4.5],
                    header_bg_color=theme.table_header_bg,
                    zebra_bg_color=theme.table_zebra_bg
                )
            }
        )

        # Slide 6: Research & References
        citations = spec.get("citations", [
            "a. Standard Reference Architecture for Distributed Systems, ACM / IEEE, 2023.",
            "b. Legal Evidentiary Standards & Digital Forensics, Ministry of Law & Justice, 2023.",
            "c. National Cybersecurity Guidelines and Threat Exchange Protocols, CERT-In."
        ])
        platforms = spec.get("existing_platforms", [
            "a. Enterprise Global Threat Systems: High cost, foreign telemetry.",
            "b. Commercial Off-The-Shelf Tools: Lack sovereign custom legal compliance."
        ])

        competitor_headers = spec.get("competitor_headers", ["Feature / Capability", team_name, "Competitor A", "Competitor B", "Competitor C"])
        competitor_rows = [
            CompetitorMatrixRow(r[0], r[1]) for r in spec.get("competitor_rows", [
                ("1. Sovereign Air-Gapped On-Premise Deployment", [True, False, False, False]),
                ("2. Sub-180s Real-Time Automated Correlation", [True, True, False, False]),
                ("3. Automated Court Evidentiary Hash Chain", [True, False, False, False]),
                ("4. Zero Forex Software Licensing Overhead", [True, False, False, False]),
                ("5. Domain-Specific Indian Regulatory Compliance", [True, False, False, False]),
                ("6. Machine-Readable Inter-Agency Notice Engine", [True, False, False, False])
            ])
        ]

        research_flow_steps = [
            ChevronStepSpec(str(i+1), s[0], s[1], s[2]) for i, s in enumerate(spec.get("research_flow", [
                ("Threat Landscape", "Problem Analysis", theme.bullet_accent),
                ("State of Art", "Literature Survey", theme.accent_purple),
                ("Gap Analysis", "Deficiency Audit", theme.accent_cyan),
                ("Architecture", "System Modeling", theme.tier_header_bg),
                ("Implementation", "Core Engine Build", theme.bullet_accent),
                ("Adversarial QA", "Red Team Testing", theme.accent_orange),
                ("Benchmarking", "Stress Testing", theme.success_green),
                ("Deployment", "Field Commissioning", theme.success_green)
            ]))
        ]

        slide_6 = SlideSpec(
            slide_number=6,
            title="RESEARCH AND REFERENCES",
            archetype=SlideArchetype.TOP_SPLIT_BOTTOM_FLOW,
            top_left={
                "component": MultiSectionColumnSpec(
                    sections=[
                        SubSectionSpec("• Research Papers & Legal Frameworks:", citations),
                        SubSectionSpec("• Existing Intelligence Platforms:", platforms)
                    ]
                )
            },
            left_column={
                "component": ProjectLinksCardSpec(
                    title="• Project Links Demo:-",
                    github_url=spec.get("github_url", "https://github.com/sih-championship/solution-core"),
                    demo_url=spec.get("demo_url", "https://demo.sih-championship.gov.in"),
                    centered=True
                )
            },
            top_right={
                "matrix_component": CompetitorMatrixSpec(
                    headers=competitor_headers,
                    rows=competitor_rows
                )
            },
            bottom_section={
                "flow_component": ChevronPipelineSpec(
                    title="• Research Flow:",
                    steps=research_flow_steps
                )
            }
        )

        return DeckManifest(deck_config=config, slides=[slide_1, slide_2, slide_3, slide_4, slide_5, slide_6])

    @classmethod
    def create_deck(
        cls,
        spec: Dict[str, Any],
        output_pptx_path: str,
        output_pdf_path: str,
        render_dir: str,
        theme_name: str = "sih_institutional_light",
        dpi: int = 200
    ) -> Tuple[DeckManifest, DeckAuditReport, List[str]]:
        """
        Executes end-to-end deck synthesis, automated visual QA, PPTX compilation,
        and headless PDF/PNG rendering.
        """
        # 1. Synthesize declarative manifest
        manifest = cls.synthesize_manifest_from_spec(spec, theme_name=theme_name)

        # 2. Automated Visual Quality Audit
        audit = VisualAuditor.audit_deck(manifest)
        print(audit.summary())

        # 3. Compile and Render
        images = compile_and_render_deck(
            manifest=manifest,
            pptx_path=output_pptx_path,
            pdf_path=output_pdf_path,
            render_dir=render_dir,
            dpi=dpi
        )

        return manifest, audit, images
