"""
Asymptotic Scale & FLOP Profiler (INV-02)
Performs mandatory 500-item micro-benchmarks before allowing execution of
large-scale data processing or inference jobs (>10,000 records).
Extrapolates total runtime and blocks execution if runtime exceeds the budget.
"""

import sys
import time
import math
import json
from typing import Dict, Any, Callable, Optional, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ScaleProfiler:
    """
    Evaluates algorithmic complexity and empirical throughput on micro-batches.
    Blocks execution if asymptotic extrapolation exceeds operational time budget.
    """

    DEFAULT_MICRO_BATCH_SIZE = 500
    DEFAULT_MAX_HOURS = 4.0

    @classmethod
    def benchmark_callable(
        cls,
        func: Callable[[List[Any]], Any],
        sample_items: List[Any],
        total_dataset_size: int,
        max_allowed_hours: float = DEFAULT_MAX_HOURS,
    ) -> Dict[str, Any]:
        """
        Runs func on sample_items (e.g. 500 items), measures elapsed time,
        and extrapolates to total_dataset_size.
        """
        batch_size = len(sample_items)
        if batch_size == 0:
            return {"error": "Sample items cannot be empty."}

        start_time = time.perf_counter()
        _ = func(sample_items)
        elapsed_sec = time.perf_counter() - start_time

        # Avoid zero division
        elapsed_sec = max(elapsed_sec, 0.00001)
        throughput = batch_size / elapsed_sec  # items per second

        # Extrapolate linear runtime
        extrapolated_seconds = (total_dataset_size / throughput)
        extrapolated_hours = extrapolated_seconds / 3600.0

        within_budget = extrapolated_hours <= max_allowed_hours

        return {
            "batch_size": batch_size,
            "elapsed_seconds": round(elapsed_sec, 4),
            "throughput_items_per_sec": round(throughput, 2),
            "total_dataset_size": total_dataset_size,
            "extrapolated_hours": round(extrapolated_hours, 2),
            "max_allowed_hours": max_allowed_hours,
            "within_budget": within_budget,
            "status": "APPROVED" if within_budget else "REJECTED_SCALE_BOTTLENECK",
            "recommendation": (
                "Throughput is sufficient for operational timeline."
                if within_budget
                else f"Extrapolated runtime ({extrapolated_hours:.1f}h) exceeds limit ({max_allowed_hours}h). "
                     "Vectorize computations, add blocking/indexing, or batch with multi-threading."
            ),
        }

    @classmethod
    def estimate_complexity(
        cls,
        batch_sizes: List[int],
        elapsed_times: List[float],
        total_dataset_size: int,
        max_allowed_hours: float = DEFAULT_MAX_HOURS
    ) -> Dict[str, Any]:
        """
        Given multiple (batch_size, elapsed_time) points, estimates whether
        complexity is O(N), O(N log N), or O(N^2).
        """
        if len(batch_sizes) < 2 or len(elapsed_times) < 2:
            return {"error": "Need at least 2 data points to estimate complexity curve."}

        n1, n2 = batch_sizes[0], batch_sizes[1]
        t1, t2 = elapsed_times[0], elapsed_times[1]

        if t1 <= 0 or t2 <= 0:
            return {"error": "Elapsed times must be positive."}

        # Ratio of times vs ratio of sizes: t2/t1 = (n2/n1)^alpha => alpha = log(t2/t1)/log(n2/n1)
        size_ratio = n2 / n1
        time_ratio = t2 / t1
        alpha = math.log(time_ratio) / math.log(size_ratio) if size_ratio > 1 else 1.0

        complexity_class = "O(N)"
        if alpha > 1.6:
            complexity_class = "O(N^2) or higher (Quadratic Explosion)"
        elif alpha > 1.1:
            complexity_class = "O(N log N)"

        # Extrapolate to total_dataset_size using estimated alpha
        scale_factor = (total_dataset_size / n2) ** alpha
        extrapolated_seconds = t2 * scale_factor
        extrapolated_hours = extrapolated_seconds / 3600.0
        within_budget = extrapolated_hours <= max_allowed_hours

        return {
            "estimated_exponent_alpha": round(alpha, 2),
            "complexity_class": complexity_class,
            "total_dataset_size": total_dataset_size,
            "extrapolated_hours": round(extrapolated_hours, 2),
            "max_allowed_hours": max_allowed_hours,
            "within_budget": within_budget,
            "status": "APPROVED" if within_budget else "REJECTED_SCALE_BOTTLENECK",
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.orchestrator.scale_profiler <sample_size> <elapsed_sec> <total_size> [max_hours]")
        sys.exit(1)

    batch_size = int(sys.argv[1])
    elapsed = float(sys.argv[2])
    total_size = int(sys.argv[3])
    max_h = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0

    throughput = batch_size / max(elapsed, 0.00001)
    extrapolated_hours = (total_size / throughput) / 3600.0
    within_budget = extrapolated_hours <= max_h

    result = {
        "batch_size": batch_size,
        "elapsed_seconds": elapsed,
        "throughput_items_per_sec": round(throughput, 2),
        "total_dataset_size": total_size,
        "extrapolated_hours": round(extrapolated_hours, 2),
        "max_allowed_hours": max_h,
        "status": "APPROVED" if within_budget else "REJECTED_SCALE_BOTTLENECK",
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if within_budget else 1)


if __name__ == "__main__":
    main()
