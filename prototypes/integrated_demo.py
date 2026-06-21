#!/usr/bin/env python3
"""
QxBin Integrated Multi-Subsystem Demo (Polished)

Scheduler + Memory + Power running together with tighter coupling.

Key improvements in this polished version:
- Stronger interaction between subsystems
- More realistic workload influence across all three
- Better combined scoring and clearer output
- Improved visualization

This is currently the best single script to demonstrate the QxBin kernel vision.

Run with --plot for a nice summary dashboard.
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
    steps: int = 400,
    pattern: str = "mixed",
    plot: bool = False
):
    print("\n" + "=" * 65)
    print(" QxBin INTEGRATED DEMO  |  Scheduler + Memory + Power")
    print("=" * 65)
    print(f" Tasks={num_tasks}  Pages={num_pages}  Cores={num_cores}  Steps={steps}  Pattern={pattern}")
    print("-" * 65)

    # === Initialize subsystems ===
    tasks = [QxBinCubit(grid_size=5, seed=i) for i in range(num_tasks)]
    pages = [QxBinCubit(grid_size=4, seed=i + 100) for i in range(num_pages)]
    cores = [QxBinCubit(grid_size=4, seed=i + 200) for i in range(num_cores)]

    in_memory = set(range(min(5, num_pages)))
    awake_cores = [True] * num_cores

    # === Metrics ===
    scheduler_runs = [0] * num_tasks
    memory_hits = 0
    memory_evictions = 0
    total_energy = 0.0
    total_perf = 0.0
    wake_events = 0
    load_history = []

    for step in range(steps):
        # === Generate correlated system load ===
        if pattern == "bursty":
            base_load = np.random.uniform(0.25, 0.9) if np.random.random() > 0.5 else np.random.uniform(0.08, 0.35)
        else:
            base_load = 0.35 + 0.45 * np.random.random()

        load_history.append(base_load)

        # === 1. SCHEDULER ===
        for tid, cubit in enumerate(tasks):
            bias = 0.35 + 0.5 * base_load
            cubit.apply_superposition(bias)

        scores = [(tid, tasks[tid].get_mean_probability() + 0.06 * np.random.random())
                  for tid in range(num_tasks)]
        chosen_task = max(scores, key=lambda x: x[1])[0]
        scheduler_runs[chosen_task] += 1

        # === 2. MEMORY (influenced by chosen task + load) ===
        page_id = (chosen_task * 3 + step) % num_pages   # task influences access pattern
        mem_bias = 0.6 + 0.25 * base_load if page_id in in_memory else 0.25 + 0.2 * base_load
        pages[page_id].apply_superposition(mem_bias)

        if page_id in in_memory:
            memory_hits += 1
        else:
            memory_evictions += 1
            # Evict page with lowest probability
            mem_scores = [(pid, pages[pid].get_mean_probability()) for pid in in_memory]
            victim = min(mem_scores, key=lambda x: x[1])[0]
            in_memory.remove(victim)
            in_memory.add(page_id)

        # === 3. POWER (influenced by memory pressure + load) ===
        mem_pressure = memory_evictions / (step + 1) if step > 10 else 0.1
        effective_load = min(1.0, base_load + 0.3 * mem_pressure)

        for i, cubit in enumerate(cores):
            power_bias = 0.3 + 0.55 * effective_load
            cubit.apply_superposition(power_bias)

            mean_p = cubit.get_mean_probability()
            should_awake = mean_p > 0.47

            if should_awake and not awake_cores[i]:
                awake_cores[i] = True
                wake_events += 1
            elif not should_awake and awake_cores[i]:
                awake_cores[i] = False

            if awake_cores[i]:
                total_energy += 1.0 + 0.75 * mean_p
                total_perf += mean_p
            else:
                total_energy += 0.1

    # === Final Results ===
    scheduler_fairness = (sum(scheduler_runs)**2) / (num_tasks * sum(x*x for x in scheduler_runs)) if sum(scheduler_runs) > 0 else 0
    mem_hit_rate = memory_hits / steps
    avg_energy = total_energy / steps
    avg_perf = total_perf / steps
    efficiency_score = (mem_hit_rate * 0.4) + (avg_perf * 0.35) + ((1 - min(avg_energy/12, 1)) * 0.25)

    print(f"\n Scheduler Fairness     : {scheduler_fairness:.3f}")
    print(f" Memory Hit Rate        : {mem_hit_rate:.1%}   (Evictions: {memory_evictions})")
    print(f" Avg Energy per step    : {avg_energy:.2f}")
    print(f" Avg Performance Score  : {avg_perf:.2f}")
    print(f" Core Wake Events       : {wake_events}")
    print(f" Final Awake Cores      : {sum(awake_cores)}/{num_cores}")
    print(f" Overall Efficiency     : {efficiency_score:.3f}  (higher is better)")
    print("=" * 65)

    if plot and HAS_MATPLOTLIB:
        plot_integrated_results(scheduler_runs, mem_hit_rate, avg_energy, avg_perf, efficiency_score, load_history)
    elif plot:
        print("(matplotlib not installed — install it for plots)")

    return {
        "fairness": round(scheduler_fairness, 3),
        "hit_rate": round(mem_hit_rate, 3),
        "energy": round(avg_energy, 2),
        "perf": round(avg_perf, 2),
        "efficiency": round(efficiency_score, 3)
    }


def plot_integrated_results(scheduler_runs, hit_rate, energy, perf, efficiency, load_history):
    fig, axs = plt.subplots(2, 2, figsize=(11, 7))

    # 1. Scheduler distribution
    axs[0, 0].bar([f"T{i}" for i in range(len(scheduler_runs))], scheduler_runs, color="#274263")
    axs[0, 0].set_title("Scheduler Task Distribution")
    axs[0, 0].set_ylabel("Times Scheduled")

    # 2. Load over time
    axs[0, 1].plot(load_history, color="#ff914d", alpha=0.7)
    axs[0, 1].set_title("System Load Over Time")
    axs[0, 1].set_xlabel("Step")
    axs[0, 1].set_ylabel("Load")

    # 3. Key metrics
    metrics = ["Hit Rate", "Perf Score", "Efficiency"]
    values = [hit_rate, perf, efficiency]
    colors = ["#ff914d", "#38b6ff", "#7ed957"]
    axs[1, 0].bar(metrics, values, color=colors)
    axs[1, 0].set_title("Key Performance Indicators")
    axs[1, 0].set_ylim(0, 1.1)

    # 4. Energy vs Performance trade-off (simple scatter)
    axs[1, 1].scatter([energy], [perf], s=200, c="#274263", alpha=0.8)
    axs[1, 1].set_title(f"Energy vs Performance\n(Efficiency: {efficiency:.3f})")
    axs[1, 1].set_xlabel("Energy Proxy")
    axs[1, 1].set_ylabel("Performance Score")
    axs[1, 1].grid(True, alpha=0.3)

    plt.suptitle("QxBin Integrated Demo — Polished View", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Integrated Demo (Polished)")
    parser.add_argument("--tasks", type=int, default=6)
    parser.add_argument("--pages", type=int, default=10)
    parser.add_argument("--cores", type=int, default=4)
    parser.add_argument("--steps", type=int, default=400)
    parser.add_argument("--pattern", choices=["mixed", "bursty"], default="mixed")
    parser.add_argument("--plot", action="store_true", help="Show polished visualization")
    args = parser.parse_args()

    run_integrated_demo(
        num_tasks=args.tasks,
        num_pages=args.pages,
        num_cores=args.cores,
        steps=args.steps,
        pattern=args.pattern,
        plot=args.plot
    )
