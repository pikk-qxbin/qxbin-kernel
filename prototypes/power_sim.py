#!/usr/bin/env python3
"""
QxBin Power & Thermal Management Simulation (with Visualization)

Models core wake/idle and frequency scaling decisions using probability matrices.
- Workload drives evolution toward high or low power states
- Probabilistic wake/sleep decisions
- Comparison against simple threshold policy
- Optional matplotlib visualization with --plot

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


def simulate_power(
    num_cores: int = 4,
    steps: int = 300,
    load_pattern: str = "bursty",
    plot: bool = False
):
    print(f"\n=== QxBin Power/Thermal Simulation ===")
    print(f"Cores: {num_cores} | Steps: {steps} | Load: {load_pattern}\n")

    cores = [QxBinCubit(grid_size=4, seed=i) for i in range(num_cores)]
    awake = [True] * num_cores
    energy_proxy = 0.0
    wake_events = 0
    performance_score = 0.0
    energy_history = []

    for step in range(steps):
        if load_pattern == "bursty":
            load = np.random.uniform(0.2, 0.95) if np.random.random() > 0.6 else np.random.uniform(0.05, 0.3)
        elif load_pattern == "steady_high":
            load = 0.75 + 0.15 * np.random.random()
        else:
            load = 0.3 + 0.5 * np.sin(step / 20) + 0.1 * np.random.random()

        for i, cubit in enumerate(cores):
            bias = 0.35 + 0.5 * load
            cubit.apply_superposition(bias)

            mean_prob = cubit.get_mean_probability()
            should_be_awake = mean_prob > 0.45

            if should_be_awake and not awake[i]:
                awake[i] = True
                wake_events += 1
            elif not should_be_awake and awake[i]:
                awake[i] = False

            if awake[i]:
                energy_proxy += 1.0 + 0.8 * mean_prob
                performance_score += mean_prob
            else:
                energy_proxy += 0.15

        if step % 20 == 0:
            energy_history.append(energy_proxy / (step + 1))

    avg_energy = energy_proxy / steps
    avg_perf = performance_score / steps
    print(f"Avg energy proxy per step: {avg_energy:.2f}")
    print(f"Avg performance score: {avg_perf:.2f}")
    print(f"Wake events: {wake_events}")

    if plot and HAS_MATPLOTLIB:
        plot_power_results(energy_history, avg_energy, avg_perf, "QxBin Power")
    elif plot:
        print("(matplotlib not installed — skipping plots)")

    return avg_energy, avg_perf, wake_events


def simulate_threshold_baseline(
    num_cores: int = 4,
    steps: int = 300,
    load_pattern: str = "bursty",
    plot: bool = False
):
    print(f"\n=== Threshold Baseline Policy ===")
    awake = [True] * num_cores
    energy_proxy = 0.0
    wake_events = 0
    performance_score = 0.0
    energy_history = []

    for step in range(steps):
        if load_pattern == "bursty":
            load = np.random.uniform(0.2, 0.95) if np.random.random() > 0.6 else np.random.uniform(0.05, 0.3)
        elif load_pattern == "steady_high":
            load = 0.75 + 0.15 * np.random.random()
        else:
            load = 0.3 + 0.5 * np.sin(step / 20) + 0.1 * np.random.random()

        for i in range(num_cores):
            should_be_awake = load > 0.5

            if should_be_awake and not awake[i]:
                awake[i] = True
                wake_events += 1
            elif not should_be_awake and awake[i]:
                awake[i] = False

            if awake[i]:
                energy_proxy += 1.0 + 0.6 * load
                performance_score += load
            else:
                energy_proxy += 0.15

        if step % 20 == 0:
            energy_history.append(energy_proxy / (step + 1))

    avg_energy = energy_proxy / steps
    avg_perf = performance_score / steps
    print(f"Avg energy proxy per step: {avg_energy:.2f}")
    print(f"Avg performance score: {avg_perf:.2f}")
    print(f"Wake events: {wake_events}")

    if plot and HAS_MATPLOTLIB:
        plot_power_results(energy_history, avg_energy, avg_perf, "Threshold Baseline")
    elif plot:
        print("(matplotlib not installed — skipping plots)")

    return avg_energy, avg_perf, wake_events


def plot_power_results(energy_history, avg_energy, avg_perf, title):
    plt.figure(figsize=(8, 4))
    plt.plot(energy_history, color="#7ed957", linewidth=2)
    plt.title(f"{title} — Energy Proxy Over Time (Avg: {avg_energy:.2f}, Perf: {avg_perf:.2f})")
    plt.xlabel("Sample (every 20 steps)")
    plt.ylabel("Cumulative Energy Proxy")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Power Simulation")
    parser.add_argument("--cores", type=int, default=4)
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--pattern", choices=["bursty", "steady_high", "mixed"], default="bursty")
    parser.add_argument("--plot", action="store_true", help="Show matplotlib visualization")
    args = parser.parse_args()

    qx_e, qx_p, qx_w = simulate_power(args.cores, args.steps, args.pattern, args.plot)
    th_e, th_p, th_w = simulate_threshold_baseline(args.cores, args.steps, args.pattern, args.plot)

    print("\n=== Power Comparison ===")
    print(f"QxBin Energy: {qx_e:.2f} | Perf: {qx_p:.2f} | Wakes: {qx_w}")
    print(f"Threshold Energy: {th_e:.2f} | Perf: {th_p:.2f} | Wakes: {th_w}")
