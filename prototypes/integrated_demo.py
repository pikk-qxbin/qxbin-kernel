#!/usr/bin/env python3
"""
QxBin Integrated Multi-Subsystem Demo

Scheduler + Memory + Power decisions running together under the same workload.
This shows how QxBin probability evolution can coordinate across kernel subsystems.

Features:
- Shared workload drives all three subsystems
- Scheduler uses QxBin for task selection
- Memory uses probability matrices for page decisions
- Power uses probability for core wake/idle
- Combined metrics + optional summary visualization

Run this to see the holistic view of probabilistic kernel thinking.

Part of qxbin-kernel exploration.
"""

import numpy as np
import argparse
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from qxbin_primitives import QxBinCubit, QxBinEnsemble


def run_integrated_demo(
    num_tasks: int = 6,
    num_pages: int = 10,
    num_cores: int = 4,
    steps: int = 300,
    pattern: str = "mixed",
    plot: bool = False
):
    print("\n" + "="*60)
    print("QxBin INTEGRATED DEMO: Scheduler + Memory + Power")
    print("="*60)
    print(f"Tasks: {num_tasks} | Pages: {num_pages} | Cores: {num_cores} | Steps: {steps}")
    print(f"Workload pattern: {pattern}\n")

    # Initialize subsystems
    tasks = [QxBinCubit(grid_size=5, seed=i) for i in range(num_tasks)]
    pages = [QxBinCubit(grid_size=4, seed=i+100) for i in range(num_pages)]
    cores = [QxBinCubit(grid_size=4, seed=i+200) for i in range(num_cores)]

    in_memory = set(range(min(5, num_pages)))
    awake_cores = [True] * num_cores

    # Metrics
    scheduler_runs = [0] * num_tasks
    memory_hits = 0
    memory_evictions = 0
    energy_proxy = 0.0
    performance_proxy = 0.0
    wake_events = 0

    for step in range(steps):
        # === 1. Generate system load from pattern ===
        if pattern == "bursty":
            sys_load = np.random.uniform(0.3, 0.95) if np.random.random() > 0.55 else np.random.uniform(0.1, 0.4)
        else:  # mixed
            sys_load = 0.4 + 0.4 * np.random.random()

        # === 2. SCHEDULER: Decide which task runs ===
        for tid, cubit in enumerate(tasks):
            bias = 0.4 + 0.4 * sys_load
            cubit.apply_superposition(bias)

        scores = [(tid, tasks[tid].get_mean_probability() + 0.05 * np.random.random())
                  for tid in range(num_tasks)]
        chosen_task = max(scores, key=lambda x: x[1])[0]
        scheduler_runs[chosen_task] += 1

        # === 3. MEMORY: Access pattern influenced by chosen task ===
        page_id = (chosen_task + step) % num_pages
        mem_bias = 0.65 if page_id in in_memory else 0.3
        pages[page_id].apply_superposition(mem_bias)

        if page_id in in_memory:
            memory_hits += 1
        else:
            memory_evictions += 1
            # Evict lowest probability page
            scores_mem = [(pid, pages[pid].get_mean_probability()) for pid in in_memory]
            victim = min(scores_mem, key=lambda x: x[1])[0]
            in_memory.remove(victim)
            in_memory.add(page_id)

        # === 4. POWER: Core wake/idle based on overall load ===
        for i, cubit in enumerate(cores):
            power_bias = 0.3 + 0.55 * sys_load
            cubit.apply_superposition(power_bias)
            mean_p = cubit.get_mean_probability()

            should_awake = mean_p > 0.48
            if should_awake and not awake_cores[i]:
                awake_cores[i] = True
                wake_events += 1
            elif not should_awake and awake_cores[i]:
                awake_cores[i] = False

            if awake_cores[i]:
                energy_proxy += 1.0 + 0.7 * mean_p
                performance_proxy += mean_p
            else:
                energy_proxy += 0.12

    # Final metrics
    scheduler_fairness = (sum(scheduler_runs) ** 2) / (num_tasks * sum(x*x for x in scheduler_runs)) if sum(scheduler_runs) > 0 else 0
    mem_hit_rate = memory_hits / steps
    avg_energy = energy_proxy / steps
    avg_perf = performance_proxy / steps

    print("\n=== INTEGRATED RESULTS ===")
    print(f"Scheduler Fairness     : {scheduler_fairness:.3f}")
    print(f"Memory Hit Rate        : {mem_hit_rate:.1%}")
    print(f"Memory Evictions       : {memory_evictions}")
    print(f"Avg Energy Proxy       : {avg_energy:.2f}")
    print(f"Avg Performance Score  : {avg_perf:.2f}")
    print(f"Core Wake Events       : {wake_events}")
    print(f"Final Awake Cores      : {sum(awake_cores)} / {num_cores}")

    if plot and HAS_MATPLOTLIB:
        plot_integrated_summary(scheduler_runs, mem_hit_rate, avg_energy, avg_perf)
    elif plot:
        print("(matplotlib not installed — skipping plot)")

    return {
        "scheduler_fairness": scheduler_fairness,
        "mem_hit_rate": mem_hit_rate,
        "energy": avg_energy,
        "perf": avg_perf
    }


def plot_integrated_summary(scheduler_runs, mem_hit_rate, energy, perf):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.5))

    # Scheduler distribution
    axs[0].bar([f"T{i}" for i in range(len(scheduler_runs))], scheduler_runs, color="#274263")
    axs[0].set_title("Scheduler Run Distribution")
    axs[0].set_ylabel("Times Scheduled")

    # Memory & Power summary bars
    axs[1].bar(["Memory Hit Rate", "Energy", "Perf Score"], 
               [mem_hit_rate, energy/10, perf], color=["#ff914d", "#7ed957", "#38b6ff"])
    axs[1].set_title("Key Metrics (normalized)")
    axs[1].set_ylim(0, 1.1)

    # Simple combined score
    combined = (mem_hit_rate + (perf / 1.2) + (1 - energy/15)) / 3
    axs[2].bar(["Overall Balance"], [combined], color="#274263")
    axs[2].set_title("Combined Efficiency Score")
    axs[2].set_ylim(0, 1)

    plt.suptitle("QxBin Integrated Demo Summary", fontsize=14)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Integrated Demo")
    parser.add_argument("--tasks", type=int, default=6)
    parser.add_argument("--pages", type=int, default=10)
    parser.add_argument("--cores", type=int, default=4)
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--pattern", choices=["mixed", "bursty"], default="mixed")
    parser.add_argument("--plot", action="store_true", help="Show summary visualization")
    args = parser.parse_args()

    run_integrated_demo(
        num_tasks=args.tasks,
        num_pages=args.pages,
        num_cores=args.cores,
        steps=args.steps,
        pattern=args.pattern,
        plot=args.plot
    )
