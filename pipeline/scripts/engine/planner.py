"""
Presentation Engine — Dynamic Agentic Spatial Planner
Translates open-ended natural language prompts or technical solution docs
into structured multi-slide presentation plans across any domain (Healthcare, Agriculture, Defense, FinTech, AI).
Incorporates learned DesignGrammar when available.
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from scripts.engine.cognitive_analyzer import DesignGrammar


@dataclass
class OmniSlidePlan:
    """Specification for an individual slide layout and content."""
    slide_number: int
    title: str
    subtitle: Optional[str] = None
    category_badge: Optional[str] = None
    archetype: str = "bento_features"  # title, split_tension, swimlane_architecture, bento_features, kpi_metrics, roadmap, radial_ecosystem
    content_payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OmniDeckPlan:
    """Complete presentation plan containing all slide specifications and design tokens."""
    project_title: str
    team_name: str
    theme_name: str
    slides: List[OmniSlidePlan] = field(default_factory=list)
    custom_theme_overrides: Optional[Dict[str, Any]] = None


class PromptDeconstructor:
    """
    Deconstructs raw technical prompts into key narrative beats,
    extracting metrics, architecture tiers, problem-solution pairs, and roadmap phases.
    """

    @classmethod
    def deconstruct(cls, text: str) -> Dict[str, Any]:
        """Extracts structured entities from open-ended natural language text."""
        # 1. Project Title & Team
        title = "INNOVATION ARCHITECTURE"
        team = "TEAM INNOVATOR"

        # Check for explicit title or first line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            first_line = lines[0].lstrip('#').strip()
            if ":" in first_line:
                title = first_line.split(":", 1)[0].strip()
            elif len(first_line) < 100:
                title = first_line

        # Check for team name
        for line in lines:
            if line.lower().startswith("team:"):
                team = line.split(":", 1)[1].strip()
                break

        # Match percentages or metrics
        metrics = re.findall(r'(\d+(?:\.\d+)?%|\d+ms|\d+[xX]|\d+\+)', text)
        top_metrics = metrics[:3] if metrics else ["99.4%", "<45ms", "10x"]

        # Extract problem vs solution statements
        problem_points = []
        solution_points = []
        in_prob = False
        in_sol = False

        for line in lines:
            l_lower = line.lower()
            if "problem" in l_lower or "challenge" in l_lower:
                in_prob = True; in_sol = False; continue
            elif "solution" in l_lower or "approach" in l_lower:
                in_sol = True; in_prob = False; continue

            if line.startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                clean_pt = re.sub(r'^[-*•\d\.]+\s*', '', line).strip()
                if in_prob and len(clean_pt) > 5:
                    problem_points.append(clean_pt)
                elif in_sol and len(clean_pt) > 5:
                    solution_points.append(clean_pt)

        if not problem_points:
            problem_points = [
                f"Manual operational workflows in {title} create severe turnaround bottlenecks and delay triage",
                f"Fragmented data silos prevent unified real-time correlation and situational awareness for {title}",
                f"High false-positive rates drain operational resources and reduce human operator confidence"
            ]
        if not solution_points:
            solution_points = [
                f"Autonomous edge intelligence processes incoming {title} data streams in under 50 milliseconds",
                f"Neural correlation engine maps cross-domain dependencies into unified actionable representations",
                f"Deterministic tamper-evident audit logging guarantees 100% statutory and operational compliance"
            ]

        return {
            "title": title,
            "team": team,
            "metrics": top_metrics,
            "problem_points": problem_points[:4],
            "solution_points": solution_points[:4]
        }


class OmniDeckPlanner:
    """
    Synthesizes a complete multi-slide championship deck plan from any prompt or solution document.
    """

    @classmethod
    def plan_from_prompt(
        cls,
        prompt: str,
        theme_name: str = "cyber_dark_terminal",
        grammar: Optional[DesignGrammar] = None,
        num_slides: int = 6,
        custom_slide_specs: Optional[List[Dict[str, Any]]] = None
    ) -> OmniDeckPlan:
        """Translates raw prompt into an OmniDeckPlan with guaranteed slide rhythm."""
        entities = PromptDeconstructor.deconstruct(prompt)
        title = entities["title"]
        team = entities["team"]

        slides: List[OmniSlidePlan] = []

        # Slide 1: Title Page
        slides.append(OmniSlidePlan(
            slide_number=1,
            title=title,
            subtitle="Autonomous High-Impact Solution Architecture",
            category_badge="ENTERPRISE HACKATHON 2026",
            archetype="title",
            content_payload={"team_name": team, "ps_category": "Software / AI", "ps_id": "INNO-2026"}
        ))

        # Slide 2: Problem Tension / Before vs After
        slides.append(OmniSlidePlan(
            slide_number=2,
            title="THE PROBLEM & PROPOSED PARADIGM SHIFT",
            subtitle="Contrasting Current Industry Vulnerabilities with Our Autonomous Solution",
            category_badge="CHALLENGE & SOLUTION",
            archetype="split_tension",
            content_payload={
                "problem_title": "Current Operational Reality & Bottlenecks",
                "problem_bullets": entities["problem_points"],
                "solution_title": f"{title} Core Innovation",
                "solution_bullets": entities["solution_points"]
            }
        ))

        # Slide 3: Multi-Tier Swimlane Architecture
        slides.append(OmniSlidePlan(
            slide_number=3,
            title="SYSTEM ARCHITECTURE & TECHNICAL TOPOLOGY",
            subtitle="End-to-End Modular Microservice Data Flow & Ingestion Pipeline",
            category_badge="TECHNICAL ARCHITECTURE",
            archetype="swimlane_architecture",
            content_payload={
                "lanes": [
                    {"name": "Tier 1: Ingestion", "icon": "cloud", "nodes": ["Edge Sensors / APIs", "Stream Feeder", "Kafka Queue"]},
                    {"name": "Tier 2: Intelligence", "icon": "brain", "nodes": ["Inference Model", "Feature Extractor", "Graph Engine"]},
                    {"name": "Tier 3: Persistence", "icon": "database", "nodes": ["Time-Series DB", "ChromaDB Vectors", "Postgres Cluster"]},
                    {"name": "Tier 4: Egress & UI", "icon": "chart", "nodes": ["SOC Dashboard", "REST / gRPC API", "Audit Export"]}
                ]
            }
        ))

        # Slide 4: Modular Bento Feature Grid
        slides.append(OmniSlidePlan(
            slide_number=4,
            title="CORE CAPABILITIES & ARCHITECTURAL PILLARS",
            subtitle="Key Technical Differentiators and High-Performance Engineering Highlights",
            category_badge="TECHNICAL APPROACH",
            archetype="bento_features",
            content_payload={
                "cards": [
                    {
                        "title": "Real-Time Neural Inference",
                        "badge": "Sub-50ms",
                        "icon": "cpu",
                        "bullets": [
                            "Latency Budget: Optimized PyTorch C++ runtime with TensorRT acceleration",
                            "High Throughput: Scales to 100,000 requests/sec with horizontal load balancing"
                        ]
                    },
                    {
                        "title": "Decentralized Entity Graph",
                        "badge": "Graph AI",
                        "icon": "network",
                        "bullets": [
                            "Heterogeneous GNN: Cross-correlates multi-modal data streams automatically",
                            "Dynamic Link Prediction: Uncovers hidden correlations and latent clusters"
                        ]
                    },
                    {
                        "title": "Cryptographic Auditability",
                        "badge": "Zero-Trust",
                        "icon": "shield",
                        "bullets": [
                            "Merkle Tree Proofs: Immutable audit log preventing data tampering",
                            "Regulatory Ready: Built-in compliance report generation on demand"
                        ]
                    },
                    {
                        "title": "Distributed Storage Fabric",
                        "badge": "Fault-Tolerant",
                        "icon": "database",
                        "bullets": [
                            "Hybrid Architecture: Low-latency caching paired with cold object storage",
                            "Automated Recovery: Raft consensus with automatic partition healing"
                        ]
                    }
                ]
            }
        ))

        # Slide 5: KPI Stat Heroes & Benchmark Impact
        metrics = entities["metrics"]
        slides.append(OmniSlidePlan(
            slide_number=5,
            title="EMPIRICAL BENCHMARKS & REAL-WORLD IMPACT",
            subtitle="Quantitative Field Performance and Scalability Metrics",
            category_badge="FEASIBILITY & IMPACT",
            archetype="kpi_metrics",
            content_payload={
                "kpis": [
                    {
                        "number": metrics[0] if len(metrics) > 0 else "99.4%",
                        "label": "Operational Precision",
                        "delta": "+5.2% vs Baseline",
                        "caption": "Validated on production benchmark suite",
                        "icon": "chart"
                    },
                    {
                        "number": metrics[1] if len(metrics) > 1 else "42ms",
                        "label": "End-to-End Latency",
                        "delta": "12x Faster",
                        "caption": "Average p99 turnaround time under peak load",
                        "icon": "cpu"
                    },
                    {
                        "number": metrics[2] if len(metrics) > 2 else "10M+",
                        "label": "Scalability Horizon",
                        "delta": "Enterprise Scale",
                        "caption": "Concurrent records processed with zero drop",
                        "icon": "database"
                    }
                ]
            }
        ))

        # Slide 6: Execution Roadmap & Milestones
        slides.append(OmniSlidePlan(
            slide_number=6,
            title="DEPLOYMENT ROADMAP & IMPLEMENTATION PHASES",
            subtitle="Structured Engineering Milestones from Prototyping to Full Enterprise Release",
            category_badge="ROADMAP & VIABILITY",
            archetype="roadmap",
            content_payload={
                "phases": [
                    {"title": "Phase 1: Architecture Core", "date": "Month 1 - 2", "status": "COMPLETED", "deliverable": "MVP core engine & ingestion pipeline"},
                    {"title": "Phase 2: Model Hardening", "date": "Month 3 - 4", "status": "IN PROGRESS", "deliverable": "GNN tuning & sub-50ms latency validation"},
                    {"title": "Phase 3: Pilot Deployment", "date": "Month 5 - 6", "status": "PLANNED", "deliverable": "Live testbed rollout with partner agencies"},
                    {"title": "Phase 4: Full Enterprise Release", "date": "Month 7+", "status": "PLANNED", "deliverable": "Multi-region high-availability release"}
                ]
            }
        ))

        # Extended archetypes if num_slides > 6
        if num_slides > 6:
            # Slide 7: Ecosystem & Stakeholder Integrations
            slides.append(OmniSlidePlan(
                slide_number=7,
                title="ECOSYSTEM ARCHITECTURE & PARTNER INTEGRATION",
                subtitle="Radial Interoperability Across Public Sector, Industry & Sensor Networks",
                category_badge="INTEGRATIONS & ECOSYSTEM",
                archetype="radial_ecosystem",
                content_payload={
                    "center_title": f"{title} CORE",
                    "nodes": [
                        {"name": "Gov Portals", "role": "Data Ingestion & Regulatory Audit", "icon": "shield"},
                        {"name": "Edge Devices", "role": "Distributed Field Telemetry", "icon": "cpu"},
                        {"name": "Emergency SOC", "role": "Live Dispatch & Incident HUD", "icon": "chart"},
                        {"name": "Cloud Fabric", "role": "Elastic High-Throughput Cluster", "icon": "cloud"}
                    ]
                }
            ))
            # Slide 8: Business Viability & Market Impact
            slides.append(OmniSlidePlan(
                slide_number=8,
                title="COMMERCIAL VIABILITY & ADOPTION STRATEGY",
                subtitle="Cost Efficiency, Financial Sustainability, and Go-To-Market Execution",
                category_badge="BUSINESS IMPACT",
                archetype="split_tension",
                content_payload={
                    "problem_title": "Legacy Enterprise Cost Burdens",
                    "problem_bullets": [
                        "Prohibitive per-seat licensing ($50k+/year per terminal)",
                        "High vendor lock-in on proprietary closed-source silos",
                        "Manual compliance certification consuming weeks of engineering"
                    ],
                    "solution_title": "Autonomous Operating Paradigm",
                    "solution_bullets": [
                        "Zero marginal licensing overhead via modern open standards",
                        "Self-hosted sovereign deployment on commodity hardware",
                        "Automated Section 63 BSA audit report generation in sub-seconds"
                    ]
                }
            ))

        # Handle user-specified custom slide specifications
        if custom_slide_specs:
            custom_slides_list: List[OmniSlidePlan] = []
            for idx, c_spec in enumerate(custom_slide_specs):
                c_slide = OmniSlidePlan(
                    slide_number=idx + 1,
                    title=c_spec.get("title", f"SLIDE {idx + 1}"),
                    subtitle=c_spec.get("subtitle", "Technical Architecture Overview"),
                    category_badge=c_spec.get("category_badge", "EXECUTIVE DECK"),
                    archetype=c_spec.get("archetype", "bento_features"),
                    content_payload=c_spec.get("content_payload", {})
                )
                custom_slides_list.append(c_slide)
            selected_slides = custom_slides_list
        else:
            selected_slides = slides[:num_slides]
            for i, s in enumerate(selected_slides):
                s.slide_number = i + 1

        overrides = None
        if grammar:
            overrides = {
                "font_heading": grammar.heading_font,
                "font_body": grammar.body_font,
                "canvas_bg": grammar.primary_bg,
                "card_bg": grammar.primary_card_bg,
                "accent": grammar.accent_color
            }

        return OmniDeckPlan(
            project_title=title,
            team_name=team,
            theme_name=theme_name,
            slides=selected_slides,
            custom_theme_overrides=overrides
        )
