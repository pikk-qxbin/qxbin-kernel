#!/usr/bin/env python3
"""
QxBin Integrated Multi-Subsystem Demo (Enhanced with Trends)

Scheduler + Memory + Power with trend tracking.

New in this version:
- History tracking for key metrics over time
- Much richer visualization showing trends
- Better insight into system behavior

This version is significantly more useful for analysis and demos.
"""

import numpy as np
import argparse
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from qxbin_primitives import QxBinCubit


def run_integrated_demo(
    num_tasks: int = 6,
    num_pages: int = 10,
    num_cores: int = 4,
    steps: int = 500,
    pattern: str = "mixed",
    plot: bool = False
):
    print("\n" + "=" * 70)
    print(" QxBin INTEGRATED DEMO  |  Scheduler + Memory + Power + Trends")
    print("=" * 70)
    print(f" Tasks={num_tasks} | Pages={num_pages} | Cores={num_cores} | Steps={steps} | Pattern={pattern}")
    print("-" * 70)

    # Initialize
    tasks = [QxBinCubit(grid_size=5, seed=i) for i in range(num_tasks)]
    pages = [QxBinCubit(grid_size=4, seed=i + 100) for i in range(num_pages)]
    cores = [QxBinCubit(grid_size=4, seed=i + 200) for i in range(num_cores)]

    in_memory = set(range(min(5, num_pages)))
    awake_cores = [True] * num_cores

    # History tracking
    fairness_history = []
    hit_rate_history = []
    energy_history = []
    perf_history = []
    efficiency_history = []
    load_history = []

    scheduler_runs = [0] * num_tasks
    memory_hits = 0
    memory_evictions = 0
    total_energy = 0.0
    total_perf = 0.0
    wake_events = 0

    for step in range(steps):
        # Workload
        if pattern == "bursty":
            base_load = np.random.uniform(0.25, 0.92) if np.random.random() > 0.52 else np.random.uniform(0.08, 0.38)
        else:
            base_load = 0.32 + 0.48 * np.random.random()

        load_history.append(base_load)

        # SCHEDULER
        for tid, cubit in enumerate(tasks):
            cubit.apply_superposition(0.35 + 0.5 * base_load)

        scores = [(tid, tasks[tid].get_mean_probability() + 0.06 * np.random.random())
                  for tid in range(num_tasks)]
        chosen_task = max(scores, key=lambda x: x[1])[0]
        scheduler_runs[chosen_task] += 1

        # MEMORY
        page_id = (chosen_task * 3 + step) % num_pages
        mem_bias = 0.58 + 0.28 * base_load if page_id in in_memory else 0.22 + 0.25 * base_load
        pages[page_id].apply_superposition(mem_bias)

        if page_id in in_memory:
            memory_hits += 1
        else:
            memory_evictions += 1
            mem_scores = [(pid, pages[pid].get_mean_probability()) for pid in in_memory]
            victim = min(mem_scores, key=lambda x: x[1])[0]
            in_memory.remove(victim)
            in_memory.add(page_id)

        # POWER
        mem_pressure = memory_evictions / max(step, 1)
        effective_load = min(1.0, base_load + 0.35 * mem_pressure)

        for i, cubit in enumerate(cores):
            cubit.apply_superposition(0.28 + 0.58 * effective_load)
            mean_p = cubit.get_mean_probability()

            should_awake = mean_p > 0.46
            if should_awake and not awake_cores[i]:
                awake_cores[i] = True
                wake_events += 1
            elif not should_awake and awake_cores[i]:
                awake_cores[i] = False

            if awake_cores[i]:
                total_energy += 1.0 + 0.72 * mean_p
                total_perf += mean_p
            else:
                total_energy += 0.1

        # Record history every 25 steps
        if step % 25 == 0 and step > 0:
            current_fairness = (sum(scheduler_runs)**2) / (num_tasks * sum(x*x for x in scheduler_runs)) if sum(scheduler_runs) > 0 else 0
            current_hit_rate = memory_hits / (step + 1)
            current_energy = total_energy / (step + 1)
            current_perf = total_perf / (step + 1)
            current_eff = (current_hit_rate * 0.4) + (current_perf * 0.35) + ((1 - min(current_energy/12, 1)) * 0.25)

            fairness_history.append(current_fairness)
            hit_rate_history.append(current_hit_rate)
            energy_history.append(current_energy)
            perf_history.append(current_perf)
            efficiency_history.append(current_eff)

    # Final metrics
    final_fairness = (sum(scheduler_runs)**2) / (num_tasks * sum(x*x for x in scheduler_runs)) if sum(scheduler_runs) > 0 else 0
    final_hit_rate = memory_hits / steps
    final_energy = total_energy / steps
    final_perf = total_perf / steps
    final_efficiency = (final_hit_rate * 0.4) + (final_perf * 0.35) + ((1 - min(final_energy/12, 1)) * 0.25)

    print(f"\n Final Scheduler Fairness : {final_fairness:.3f}")
    print(f" Final Memory Hit Rate   : {final_hit_rate:.1%}   (Evictions: {memory_evictions})")
    print(f" Final Avg Energy        : {final_energy:.2f}")
    print(f" Final Avg Performance   : {final_perf:.2f}")
    print(f" Core Wake Events        : {wake_events}")
    print(f" Overall Efficiency      : {final_efficiency:.3f}")
    print("=" * 70)

    if plot and HAS_MATPLOTLIB:
        plot_trends(fairness_history, hit_rate_history, energy_history, perf_history, efficiency_history)
    elif plot:
        print("(matplotlib not installed)")

    return {
        "fairness": round(final_fairness, 3),
        "hit_rate": round(final_hit_rate, 3),
        "energy": round(final_energy, 2),
        "perf": round(final_perf, 2),
        "efficiency": round(final_efficiency, 3)
    }


def plot_trends(fairness_h, hit_h, energy_h, perf_h, eff_h):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    x = range(len(fairness_h))

    # Fairness trend
    axs[0, 0].plot(x, fairness_h, color="#274263", linewidth=2)
    axs[0, 0].set_title("Scheduler Fairness Over Time")
    axs[0, 0].set_ylabel("Jain's Fairness")
    axs[0, 0].grid(True, alpha=0.3)

    # Hit rate + Efficiency
    axs[0, 1].plot(x, hit_h, label="Memory Hit Rate", color="#ff914d", linewidth=2)
    axs[0, 1].plot(x, eff_h, label="Overall Efficiency", color="#7ed957", linewidth=2)
    axs[0, 1].set_title("Memory Hit Rate & Efficiency Trend")
    axs[0, 1].legend()
    axs[0, 1].grid(True, alpha=0.3)

    # Energy vs Performance
    axs[1, 0].plot(x, energy_h, label="Energy Proxy", color="#38b6ff", linewidth=2)
    axs[1, 0].plot(x, perf_h, label="Performance Score", color="#ff914d", linewidth=2)
    axs[1, 0].set_title("Energy vs Performance Trade-off")
    axs[1, 0].legend()
    axs[1, 0].grid(True, alpha=0.3)

    # Final comparison bar
    final_vals = [fairness_h[-1], hit_h[-1], eff_h[-1]]
    axs[1, 1].bar(["Fairness", "Hit Rate", "Efficiency"], final_vals, color=["#274263", "#ff914d", "#7ed957"])
    axs[1, 1].set_title("Final Key Metrics")
    axs[1, 1].set_ylim(0, 1.1)

    plt.suptitle("QxBin Integrated Demo — Trend Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Integrated Demo with Trends")
    parser.add_argument("--tasks", type=int, default=6)
    parser.add_argument("--pages", type=int, default=10)
    parser.add_argument("--cores", type=int, default=4)
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--pattern", choices=["mixed", "bursty"], default="mixed")
    parser.add_argument("--plot", action="store_true", help="Show trend visualization")
    args = parser.parse_args()

    run_integrated_demo(
        num_tasks=args.tasks,
        num_pages=args.pages,
        num_cores=args.cores,
        steps=args.steps,
        pattern=args.pattern,
        plot=args.plot
    )
