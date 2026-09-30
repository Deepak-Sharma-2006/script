"""
Objective-Loss Calibration & Posterior Probability Auditor (Tier C: INV-08)
Evaluates classification probability calibration (Brier Score, Expected Calibration Error)
to prevent setting optimal decision thresholds on distorted pseudo-margin outputs.
"""

import sys
import json
import math
from typing import Dict, Any, List, Tuple, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CalibrationAuditor:
    """
    Audits predicted probability distributions and calibration error (ECE).
    """

    DEFAULT_MAX_ECE = 0.15  # 15% calibration error threshold

    @classmethod
    def calculate_brier_score(
        cls, probabilities: List[float], labels: List[int]
    ) -> float:
        """Calculates mean squared error between probabilities and binary labels."""
        if len(probabilities) != len(labels) or len(probabilities) == 0:
            return 1.0
        total_sq_err = sum((p - y) ** 2 for p, y in zip(probabilities, labels))
        return total_sq_err / len(probabilities)

    @classmethod
    def calculate_ece(
        cls, probabilities: List[float], labels: List[int], num_bins: int = 10
    ) -> Dict[str, Any]:
        """
        Calculates Expected Calibration Error (ECE) across probability bins.
        """
        n = len(probabilities)
        if n == 0 or n != len(labels):
            return {"error": "Probabilities and labels must have equal non-zero length."}

        bin_boundaries = [i / num_bins for i in range(num_bins + 1)]
        total_ece = 0.0
        bins_data = []

        for i in range(num_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]

            # Collect items in bin
            bin_indices = [
                idx for idx, p in enumerate(probabilities)
                if (bin_lower <= p < bin_upper) or (i == num_bins - 1 and bin_lower <= p <= bin_upper)
            ]
            bin_size = len(bin_indices)
            if bin_size > 0:
                bin_conf = sum(probabilities[idx] for idx in bin_indices) / bin_size
                bin_acc = sum(labels[idx] for idx in bin_indices) / bin_size
                bin_err = abs(bin_acc - bin_conf)
                total_ece += (bin_size / n) * bin_err

                bins_data.append({
                    "bin_range": f"[{bin_lower:.2f}, {bin_upper:.2f}]",
                    "count": bin_size,
                    "avg_confidence": round(bin_conf, 4),
                    "empirical_accuracy": round(bin_acc, 4),
                    "calibration_error": round(bin_err, 4),
                })

        brier = cls.calculate_brier_score(probabilities, labels)
        is_well_calibrated = total_ece <= cls.DEFAULT_MAX_ECE

        return {
            "num_samples": n,
            "num_bins": num_bins,
            "brier_score": round(brier, 4),
            "expected_calibration_error": round(total_ece, 4),
            "max_allowed_ece": cls.DEFAULT_MAX_ECE,
            "is_well_calibrated": is_well_calibrated,
            "status": "APPROVED" if is_well_calibrated else "DISTORTED_PROBABILITIES_DETECTED",
            "recommendation": (
                "Probabilities are well-calibrated; Bayes-optimal threshold calibration permitted."
                if is_well_calibrated
                else f"ECE ({total_ece:.3f}) exceeds threshold ({cls.DEFAULT_MAX_ECE}). "
                     "Model outputs are distorted margins, not true posterior probabilities. "
                     "Apply Platt scaling or Isotonic Regression before threshold tuning."
            ),
            "bins": bins_data,
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.orchestrator.calibration_auditor <probs_json_list> <labels_json_list>")
        sys.exit(1)

    probs = json.loads(sys.argv[1])
    labels = json.loads(sys.argv[2])
    res = CalibrationAuditor.calculate_ece(probs, labels)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res.get("is_well_calibrated") else 1)


if __name__ == "__main__":
    main()
