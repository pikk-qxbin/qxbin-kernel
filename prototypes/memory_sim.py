#!/usr/bin/env python3
"""
QxBin Memory Management Simulation Prototype (with Visualization)

Models page access probability using Binary Probability Matrices.
- Each 'page' is represented by a QxBinCubit
- On access: evolve the matrix
- Eviction: probabilistic selection of low-probability pages
- Comparison to simple LRU baseline
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


def simulate_memory(
    num_pages: int = 12,
    steps: int = 400,
    working_set_size: int = 5,
    pattern: str = "mixed",
    plot: bool = False
):
    print(f"\n=== QxBin Memory Simulation ===")
    print(f"Pages: {num_pages} | Steps: {steps} | Working set: {working_set_size} | Pattern: {pattern}\n")

    pages = [QxBinCubit(grid_size=4, seed=i) for i in range(num_pages)]
    in_memory = set(range(min(working_set_size, num_pages)))
    hits = 0
    evictions = 0
    hit_history = []

    for step in range(steps):
        if pattern == "sequential":
            page_id = step % num_pages
        elif pattern == "bursty":
            if np.random.random() < 0.7:
                page_id = np.random.randint(0, working_set_size)
            else:
                page_id = np.random.randint(working_set_size, num_pages)
        else:
            if np.random.random() < 0.75:
                page_id = np.random.randint(0, min(working_set_size + 2, num_pages))
            else:
                page_id = np.random.randint(0, num_pages)

        bias = 0.7 if page_id in in_memory else 0.35
        pages[page_id].apply_superposition(bias)

        if page_id in in_memory:
            hits += 1
        else:
            evictions += 1
            scores = [(pid, pages[pid].get_mean_probability()) for pid in in_memory]
            victim = min(scores, key=lambda x: x[1])[0]
            in_memory.remove(victim)
            in_memory.add(page_id)

        if step % 20 == 0:
            hit_history.append(hits / (step + 1) if step > 0 else 0)

    hit_rate = hits / steps if steps > 0 else 0
    print(f"Hits: {hits} | Evictions: {evictions} | Hit rate: {hit_rate:.2%}")

    if plot and HAS_MATPLOTLIB:
        plot_memory_results(hit_history, hit_rate, evictions, "QxBin Memory")
    elif plot:
        print("(matplotlib not installed — skipping plots)")

    return hit_rate, evictions


def simulate_lru_baseline(
    num_pages: int = 12,
    steps: int = 400,
    working_set_size: int = 5,
    pattern: str = "mixed",
    plot: bool = False
):
    print(f"\n=== Simple LRU-style Baseline ===")
    in_memory = list(range(min(working_set_size, num_pages)))
    recency = {pid: 0 for pid in in_memory}
    hits = 0
    evictions = 0
    hit_history = []

    for step in range(steps):
        if pattern == "sequential":
            page_id = step % num_pages
        elif pattern == "bursty":
            page_id = np.random.randint(0, working_set_size) if np.random.random() < 0.7 else np.random.randint(working_set_size, num_pages)
        else:
            page_id = np.random.randint(0, num_pages)

        if page_id in in_memory:
            hits += 1
            recency[page_id] = step
        else:
            evictions += 1
            victim = min(in_memory, key=lambda pid: recency[pid])
            in_memory.remove(victim)
            in_memory.append(page_id)
            recency[page_id] = step

        if step % 20 == 0:
            hit_history.append(hits / (step + 1) if step > 0 else 0)

    hit_rate = hits / steps if steps > 0 else 0
    print(f"Hits: {hits} | Evictions: {evictions} | Hit rate: {hit_rate:.2%}")

    if plot and HAS_MATPLOTLIB:
        plot_memory_results(hit_history, hit_rate, evictions, "LRU Baseline")
    elif plot:
        print("(matplotlib not installed — skipping plots)")

    return hit_rate, evictions


def plot_memory_results(hit_history, final_hit_rate, evictions, title):
    plt.figure(figsize=(8, 4))
    plt.plot(hit_history, color="#ff914d", linewidth=2)
    plt.title(f"{title} — Hit Rate Over Time (Final: {final_hit_rate:.1%}, Evictions: {evictions})")
    plt.xlabel("Sample (every 20 steps)")
    plt.ylabel("Cumulative Hit Rate")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Memory Simulation")
    parser.add_argument("--pages", type=int, default=12)
    parser.add_argument("--steps", type=int, default=400)
    parser.add_argument("--working-set", type=int, default=5)
    parser.add_argument("--pattern", choices=["mixed", "bursty", "sequential"], default="mixed")
    parser.add_argument("--plot", action="store_true", help="Show matplotlib visualization")
    args = parser.parse_args()

    qx_hit, qx_evict = simulate_memory(args.pages, args.steps, args.working_set, args.pattern, args.plot)
    lru_hit, lru_evict = simulate_lru_baseline(args.pages, args.steps, args.working_set, args.pattern, args.plot)

    print("\n=== Memory Comparison ===")
    print(f"QxBin Hit Rate: {qx_hit:.2%}   |   LRU Hit Rate: {lru_hit:.2%}")
