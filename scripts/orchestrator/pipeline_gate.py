"""
Generalized Pipeline Gate: Upstream Cascade Quality & Production Parity Gate (Tier B: INV-06 & INV-09)
Enforces:
1. Upstream Cascade Stage Recall Gate: Stage N+1 is blocked unless Stage N recall
   satisfies R_upstream >= Target_Score + 0.05.
2. Production Parity & Distractor Verifier: Validation datasets must match production
   negative distractor density (rejects toy benchmarks).
"""

import sys
import os
import json
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class PipelineGate:
    """
    Generalized quality gate for multi-stage ML/data pipelines and validation splits.
    """

    DEFAULT_RECALL_BUFFER = 0.05

    @classmethod
    def evaluate_upstream_recall(
        cls,
        upstream_recall: float,
        target_score: float,
        stage_name: str = "Candidate Generator",
        downstream_stage: str = "Classifier Training",
        buffer: float = DEFAULT_RECALL_BUFFER
    ) -> Dict[str, Any]:
        """
        Assesses if upstream stage recall provides sufficient theoretical ceiling
        for downstream models to achieve the target score.
        Formula: Upstream Recall >= Target Score + 0.05
        """
        required_recall = min(target_score + buffer, 1.0)
        passed = upstream_recall >= required_recall

        return {
            "stage_name": stage_name,
            "downstream_stage": downstream_stage,
            "upstream_recall": round(upstream_recall, 4),
            "target_score": round(target_score, 4),
            "required_recall_ceiling": round(required_recall, 4),
            "gate_passed": passed,
            "status": "APPROVED" if passed else "GATE_REJECTED_INSUFFICIENT_UPSTREAM_RECALL",
            "message": (
                f"Upstream recall {upstream_recall:.3f} satisfies requirement (>= {required_recall:.3f}). "
                f"Downstream {downstream_stage} permitted to proceed."
                if passed
                else f"CASCADE GATE BREACH: Upstream recall {upstream_recall:.3f} is lower than required ceiling "
                     f"{required_recall:.3f} (target {target_score:.3f} + buffer {buffer:.2f}). "
                     f"Downstream {downstream_stage} blocked to prevent training on truncated candidate pools."
            ),
        }

    @classmethod
    def evaluate_distractor_parity(
        cls,
        val_negatives: int,
        val_positives: int,
        prod_negatives: int,
        prod_positives: int,
        tolerance: float = 0.35
    ) -> Dict[str, Any]:
        """
        Compares negative-to-positive ratio between validation testbed and production.
        Prevents 'Toy Mirage' where models achieve 99% accuracy on sanitized small test sets.
        """
        if val_positives <= 0 or prod_positives <= 0:
            return {"error": "Positive counts must be greater than zero."}

        val_ratio = val_negatives / val_positives
        prod_ratio = prod_negatives / prod_positives

        # Validation ratio should be at least (1 - tolerance) * production ratio
        min_allowed_ratio = prod_ratio * (1.0 - tolerance)
        has_parity = val_ratio >= min_allowed_ratio

        return {
            "validation_negative_ratio": round(val_ratio, 2),
            "production_negative_ratio": round(prod_ratio, 2),
            "min_allowed_validation_ratio": round(min_allowed_ratio, 2),
            "parity_passed": has_parity,
            "status": "APPROVED" if has_parity else "TOY_MIRAGE_DETECTED",
            "message": (
                f"Validation distractor density ({val_ratio:.1f}:1) matches production distribution ({prod_ratio:.1f}:1)."
                if has_parity
                else f"TOY BENCHMARK REJECTED: Validation negative-to-positive ratio ({val_ratio:.1f}:1) is severely "
                     f"diluted compared to production ({prod_ratio:.1f}:1). Add production distractors before validating."
            ),
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.orchestrator.pipeline_gate --recall <upstream_recall> <target_score>")
        print("   or: python -m scripts.orchestrator.pipeline_gate --parity <val_neg> <val_pos> <prod_neg> <prod_pos>")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "--recall" and len(sys.argv) >= 4:
        rec = float(sys.argv[2])
        target = float(sys.argv[3])
        res = PipelineGate.evaluate_upstream_recall(rec, target)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["gate_passed"] else 1)
    elif arg == "--parity" and len(sys.argv) >= 6:
        vn = int(sys.argv[2])
        vp = int(sys.argv[3])
        pn = int(sys.argv[4])
        pp = int(sys.argv[5])
        res = PipelineGate.evaluate_distractor_parity(vn, vp, pn, pp)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["parity_passed"] else 1)
    else:
        print("Invalid arguments.")
        sys.exit(1)


if __name__ == "__main__":
    main()
