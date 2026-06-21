#!/usr/bin/env python3
"""
Enhanced QxBin Kernel Scheduler Simulation (with Visualization)

Now uses the reusable primitives from qxbin_primitives.py.
Includes:
- Probabilistic task selection via QxBinCubit
- Jain's fairness index + run distribution metrics
- Simple baseline comparison (round-robin style)
- Multiple workload patterns
- Optional matplotlib visualization (--plot)

Run with --plot to generate charts showing fairness and task distribution.

Part of qxbin-kernel exploration.
"""

import numpy as np
import argparse
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from qxbin_primitives import QxBinCubit


def jains_fairness(counts: list) -> float:
    """Jain's fairness index (0 to 1, higher is fairer)."""
    if not counts:
        return 0.0
    s = sum(counts)
    if s == 0:
        return 0.0
    return (s ** 2) / (len(counts) * sum(c * c for c in counts))


def run_qxbin_scheduler(num_tasks: int = 8, steps: int = 300, pattern: str = "mixed", plot: bool = False):
    print(f"\n=== QxBin Probabilistic Scheduler ===")
    print(f"Tasks: {num_tasks} | Steps: {steps} | Workload: {pattern}\n")

    tasks = [QxBinCubit(grid_size=5, seed=i) for i in range(num_tasks)]
    run_counts = [0] * num_tasks
    total_runtime = [0.0] * num_tasks

    for step in range(steps):
        for tid, cubit in enumerate(tasks):
            if pattern == "bursty_ai":
                rt = np.random.uniform(0.1, 2.5) if np.random.random() > 0.65 else 0.03
                io = np.random.uniform(0.0, 0.9)
            elif pattern == "sequential":
                rt = 0.8 if (step + tid) % 4 == 0 else 0.1
                io = 0.1
            else:
                rt = np.random.uniform(0.05, 1.2)
                io = np.random.uniform(0.0, 0.4)

            effective_bias = 0.45 + 0.35 * min(rt / 1.5, 1.0) - 0.15 * io
            cubit.apply_superposition(effective_bias)

        scores = []
        for tid, cubit in enumerate(tasks):
            score = cubit.get_mean_probability() + 0.08 * np.random.random()
            scores.append((tid, score))

        chosen = max(scores, key=lambda x: x[1])[0]
        run_counts[chosen] += 1
        total_runtime[chosen] += 0.1

    fairness = jains_fairness(run_counts)
    print("QxBin Scheduler Results:")
    print(f"  Run counts: {run_counts}")
    print(f"  Jain's Fairness: {fairness:.3f}")

    if plot and HAS_MATPLOTLIB:
        plot_results(run_counts, "QxBin Scheduler", fairness)
    elif plot:
        print("(matplotlib not installed — skipping plots)")

    return fairness, run_counts


def run_baseline_scheduler(num_tasks: int = 8, steps: int = 300, pattern: str = "mixed", plot: bool = False):
    print(f"\n=== Baseline (Round-Robin style) ===")
    run_counts = [0] * num_tasks
    idx = 0
    for _ in range(steps):
        run_counts[idx] += 1
        idx = (idx + 1) % num_tasks

    fairness = jains_fairness(run_counts)
    print(f"  Run counts: {run_counts}")
    print(f"  Jain's Fairness: {fairness:.3f}")

    if plot and HAS_MATPLOTLIB:
        plot_results(run_counts, "Baseline Scheduler", fairness)
    elif plot:
        print("(matplotlib not installed — skipping plots)")

    return fairness, run_counts


def plot_results(run_counts: list, title: str, fairness: float):
    """Generate simple bar chart for task distribution."""
    plt.figure(figsize=(8, 4))
    tasks = [f"T{i}" for i in range(len(run_counts))]
    plt.bar(tasks, run_counts, color="#274263")
    plt.title(f"{title} — Run Distribution (Fairness: {fairness:.3f})")
    plt.xlabel("Task")
    plt.ylabel("Times Scheduled")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Scheduler Simulation")
    parser.add_argument("--tasks", type=int, default=8, help="Number of tasks")
    parser.add_argument("--steps", type=int, default=300, help="Simulation steps")
    parser.add_argument("--pattern", choices=["mixed", "bursty_ai", "sequential"], default="mixed")
    parser.add_argument("--plot", action="store_true", help="Show matplotlib visualization")
    args = parser.parse_args()

    qx_fair, qx_counts = run_qxbin_scheduler(args.tasks, args.steps, args.pattern, args.plot)
    base_fair, base_counts = run_baseline_scheduler(args.tasks, args.steps, args.pattern, args.plot)

    print("\n=== Comparison ===")
    print(f"QxBin Fairness: {qx_fair:.3f}   |   Baseline Fairness: {base_fair:.3f}")
