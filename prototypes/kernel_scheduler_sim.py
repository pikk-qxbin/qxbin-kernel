#!/usr/bin/env python3
"""
Enhanced QxBin Kernel Scheduler Simulation

Now uses the reusable primitives from qxbin_primitives.py.
Includes:
- Probabilistic task selection via QxBinCubit
- Jain's fairness index + run distribution metrics
- Simple baseline comparison (round-robin style)
- Multiple workload patterns (mixed, bursty_ai, sequential)

Run it to see how probability-matrix scheduling behaves vs traditional heuristics.

Part of qxbin-kernel exploration.
"""

import numpy as np
import argparse
from qxbin_primitives import QxBinCubit, QxBinEnsemble


def jains_fairness(counts: list) -> float:
    """Jain's fairness index (0 to 1, higher is fairer)."""
    if not counts:
        return 0.0
    s = sum(counts)
    if s == 0:
        return 0.0
    return (s ** 2) / (len(counts) * sum(c * c for c in counts))


def run_qxbin_scheduler(num_tasks: int = 8, steps: int = 300, pattern: str = "mixed"):
    print(f"\n=== QxBin Probabilistic Scheduler ===")
    print(f"Tasks: {num_tasks} | Steps: {steps} | Workload: {pattern}\n")

    tasks = [QxBinCubit(grid_size=5, seed=i) for i in range(num_tasks)]
    run_counts = [0] * num_tasks
    total_runtime = [0.0] * num_tasks

    for step in range(steps):
        # Simulate feedback based on workload pattern
        for tid, cubit in enumerate(tasks):
            if pattern == "bursty_ai":
                rt = np.random.uniform(0.1, 2.5) if np.random.random() > 0.65 else 0.03
                io = np.random.uniform(0.0, 0.9)
            elif pattern == "sequential":
                rt = 0.8 if (step + tid) % 4 == 0 else 0.1
                io = 0.1
            else:  # mixed
                rt = np.random.uniform(0.05, 1.2)
                io = np.random.uniform(0.0, 0.4)

            # Update bias based on observed behavior
            effective_bias = 0.45 + 0.35 * min(rt / 1.5, 1.0) - 0.15 * io
            cubit.apply_superposition(effective_bias)

        # Probabilistic selection using mean probability + small noise
        scores = []
        for tid, cubit in enumerate(tasks):
            score = cubit.get_mean_probability() + 0.08 * np.random.random()
            scores.append((tid, score))

        # Pick highest scoring task (could also use full measure() collapse)
        chosen = max(scores, key=lambda x: x[1])[0]
        run_counts[chosen] += 1
        total_runtime[chosen] += 0.1

    fairness = jains_fairness(run_counts)
    print("QxBin Scheduler Results:")
    print(f"  Run counts: {run_counts}")
    print(f"  Jain's Fairness: {fairness:.3f}")
    print(f"  Total runtime proxy: {sum(total_runtime):.1f}")
    return fairness, run_counts


def run_baseline_scheduler(num_tasks: int = 8, steps: int = 300, pattern: str = "mixed"):
    """Simple round-robin baseline for comparison."""
    print(f"\n=== Baseline (Round-Robin style) ===")
    run_counts = [0] * num_tasks
    idx = 0
    for _ in range(steps):
        run_counts[idx] += 1
        idx = (idx + 1) % num_tasks

    fairness = jains_fairness(run_counts)
    print(f"  Run counts: {run_counts}")
    print(f"  Jain's Fairness: {fairness:.3f}")
    return fairness, run_counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Scheduler Simulation")
    parser.add_argument("--tasks", type=int, default=8, help="Number of tasks")
    parser.add_argument("--steps", type=int, default=300, help="Simulation steps")
    parser.add_argument("--pattern", choices=["mixed", "bursty_ai", "sequential"], default="mixed")
    args = parser.parse_args()

    qx_fair, qx_counts = run_qxbin_scheduler(args.tasks, args.steps, args.pattern)
    base_fair, base_counts = run_baseline_scheduler(args.tasks, args.steps, args.pattern)

    print("\n=== Comparison ===")
    print(f"QxBin Fairness: {qx_fair:.3f}   |   Baseline Fairness: {base_fair:.3f}")
    if qx_fair > base_fair:
        print("QxBin showed better fairness in this run.")
    else:
        print("Baseline was fairer this time (try different seed or more steps).")
