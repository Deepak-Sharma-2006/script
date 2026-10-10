"""
Presentation Engine — Semantic Text-to-Visual Decision Engine
Analyzes raw technical specifications, solution blueprints, and problem briefs to decide:
1. What stays as punchy, dense technical text (statutory mandates, problem axioms, citations).
2. What translates into rich visual primitives (KPI stats, layered stacks, flow pipelines, matrices).
"""

from typing import Dict, Any, List
from enum import Enum
import re


class ContentType(str, Enum):
    TEXT_CALLOUT = "TEXT_CALLOUT"
    VISUAL_STAT_HERO = "VISUAL_STAT_HERO"
    VISUAL_ARCHITECTURE_STACK = "VISUAL_ARCHITECTURE_STACK"
    VISUAL_SWIMLANE_FLOW = "VISUAL_SWIMLANE_FLOW"
    VISUAL_COMPARISON_MATRIX = "VISUAL_COMPARISON_MATRIX"
    VISUAL_BENTO_CARD = "VISUAL_BENTO_CARD"


class VisualTranslator:
    """
    Transforms unstructured technical facts into structured visual vs. text representations
    for presentation slides, ensuring high cognitive density and Canva-level layout elegance.
    """

    @classmethod
    def analyze_and_translate(cls, section_title: str, raw_items: List[str]) -> Dict[str, Any]:
        """
        Classifies a block of technical information and returns structured rendering instructions.
        """
        joined_text = " ".join(raw_items).lower()

        # 1. Check for Metric / Stat Candidates (Numbers, Percentages, Latencies, Multipliers)
        stat_patterns = [
            r'(\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?|\d+x|\d+\s*(?:ms|seconds|minutes|hours|days|fps))'
        ]
        stat_matches = []
        for item in raw_items:
            found = re.findall(stat_patterns[0], item, re.IGNORECASE)
            if found:
                stat_matches.append((found[0], item))

        if len(stat_matches) >= 2 or ("metric" in section_title.lower() or "benchmark" in section_title.lower()):
            stats_payload = []
            for val, full_text in stat_matches:
                clean_label = re.sub(stat_patterns[0], '', full_text, flags=re.IGNORECASE).strip(' :-–')
                stats_payload.append({
                    "value": val,
                    "label": clean_label[:40] if clean_label else "Metric",
                    "trend": "+10x SOTA" if "%" in val or "x" in val else "Real-time"
                })
            return {
                "type": ContentType.VISUAL_STAT_HERO,
                "title": section_title,
                "data": stats_payload,
                "visual_rationale": "High-impact numerical facts translated to Stat Hero Cards"
            }

        # 2. Check for Process / Flow / Pipeline Candidates
        flow_keywords = ["step", "phase", "stage", "pipeline", "ingestion", "workflow", "lifecycle"]
        if any(k in section_title.lower() for k in flow_keywords) or any("->" in item or "=>" in item for item in raw_items):
            steps = []
            for i, item in enumerate(raw_items):
                clean_step = re.sub(r'^(?:step\s*\d+|phase\s*\d+|\d+\.)\s*[:\-]?', '', item, flags=re.IGNORECASE).strip()
                steps.append({
                    "step_num": i + 1,
                    "title": clean_step.split(':')[0] if ':' in clean_step else f"Stage {i+1}",
                    "detail": clean_step.split(':')[1].strip() if ':' in clean_step else clean_step
                })
            return {
                "type": ContentType.VISUAL_SWIMLANE_FLOW,
                "title": section_title,
                "data": steps,
                "visual_rationale": "Sequential workflow translated to Horizontal Swimlane Pipeline"
            }

        # 3. Check for Architecture / Multi-Tier System Candidates
        arch_keywords = ["architecture", "layer", "stack", "infrastructure", "tier", "engine"]
        if any(k in section_title.lower() for k in arch_keywords):
            layers = []
            for item in raw_items:
                parts = item.split(':')
                if len(parts) >= 2:
                    layers.append({"layer_name": parts[0].strip(), "components": [p.strip() for p in parts[1].split(',')]})
                else:
                    layers.append({"layer_name": item[:25], "components": [item]})
            return {
                "type": ContentType.VISUAL_ARCHITECTURE_STACK,
                "title": section_title,
                "data": layers,
                "visual_rationale": "Multi-tier system translated to Layered Architecture Stack"
            }

        # 4. Check for Comparison / Versus / Moat Matrix Candidates
        comp_keywords = ["vs", "comparison", "alternative", "competitor", "incumbent", "benchmark"]
        if any(k in section_title.lower() for k in comp_keywords):
            rows = []
            for item in raw_items:
                parts = item.split(':')
                feature = parts[0].strip()
                status = "Supported" if any(w in item.lower() for w in ["yes", "100%", "high", "native", "zero"]) else "Limited"
                rows.append({"feature": feature, "our_system": "100% Native", "incumbents": "Partial / High Latency"})
            return {
                "type": ContentType.VISUAL_COMPARISON_MATRIX,
                "title": section_title,
                "data": rows,
                "visual_rationale": "Competitive evaluation translated to Feature Comparison Matrix"
            }

        # 5. Default: Stays as High-Density Punchy Text (Executive Callout Cards)
        return {
            "type": ContentType.TEXT_CALLOUT,
            "title": section_title,
            "data": [{"tag": item.split(':')[0].strip(), "body": item.split(':')[1].strip()} if ':' in item else {"tag": "Axiom", "body": item} for item in raw_items],
            "visual_rationale": "Kept as high-density structured technical text to preserve statutory precision"
        }
