#!/usr/bin/env python3
"""
QxBin Memory Management Simulation Prototype

Models page access probability using Binary Probability Matrices.
- Each 'page' is represented by a QxBinCubit (access likelihood landscape)
- On access: evolve the matrix with workload bias
- Eviction / replacement: probabilistic selection of low-probability pages
- Simple comparison to LRU-like baseline

Useful for exploring how probability evolution can reduce thrashing
on irregular / bursty access patterns common in AI + edge workloads.

Part of qxbin-kernel exploration.
"""

import numpy as np
import argparse
from qxbin_primitives import QxBinCubit


def simulate_memory(
    num_pages: int = 12,
    steps: int = 400,
    working_set_size: int = 5,
    pattern: str = "mixed"
):
    print(f"\n=== QxBin Memory Simulation ===")
    print(f"Pages: {num_pages} | Steps: {steps} | Working set: {working_set_size} | Pattern: {pattern}\n")

    pages = [QxBinCubit(grid_size=4, seed=i) for i in range(num_pages)]
    in_memory = set(range(min(working_set_size, num_pages)))
    hits = 0
    evictions = 0
    access_log = []

    for step in range(steps):
        # Generate access according to pattern
        if pattern == "sequential":
            page_id = step % num_pages
        elif pattern == "bursty":
            if np.random.random() < 0.7:
                page_id = np.random.randint(0, working_set_size)
            else:
                page_id = np.random.randint(working_set_size, num_pages)
        else:  # mixed / random-ish
            if np.random.random() < 0.75:
                page_id = np.random.randint(0, min(working_set_size + 2, num_pages))
            else:
                page_id = np.random.randint(0, num_pages)

        access_log.append(page_id)

        # Access the page -> evolve its probability matrix
        bias = 0.7 if page_id in in_memory else 0.35  # higher bias if already resident
        pages[page_id].apply_superposition(bias)

        if page_id in in_memory:
            hits += 1
        else:
            # Page fault -> decide eviction
            evictions += 1
            # Find candidate to evict: lowest mean probability (or use measure)
            scores = [(pid, pages[pid].get_mean_probability()) for pid in in_memory]
            victim = min(scores, key=lambda x: x[1])[0]
            in_memory.remove(victim)
            in_memory.add(page_id)

    hit_rate = hits / steps if steps > 0 else 0
    print(f"Hits: {hits} | Evictions: {evictions} | Hit rate: {hit_rate:.2%}")
    print(f"Final in-memory set size: {len(in_memory)}")
    return hit_rate, evictions


def simulate_lru_baseline(
    num_pages: int = 12,
    steps: int = 400,
    working_set_size: int = 5,
    pattern: str = "mixed"
):
    """Very simple LRU approximation using a recency list."""
    print(f"\n=== Simple LRU-style Baseline ===")
    in_memory = list(range(min(working_set_size, num_pages)))
    recency = {pid: 0 for pid in in_memory}
    hits = 0
    evictions = 0

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
            # Evict least recently used
            victim = min(in_memory, key=lambda pid: recency[pid])
            in_memory.remove(victim)
            in_memory.append(page_id)
            recency[page_id] = step

    hit_rate = hits / steps if steps > 0 else 0
    print(f"Hits: {hits} | Evictions: {evictions} | Hit rate: {hit_rate:.2%}")
    return hit_rate, evictions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QxBin Memory Simulation")
    parser.add_argument("--pages", type=int, default=12)
    parser.add_argument("--steps", type=int, default=400)
    parser.add_argument("--working-set", type=int, default=5)
    parser.add_argument("--pattern", choices=["mixed", "bursty", "sequential"], default="mixed")
    args = parser.parse_args()

    qx_hit, qx_evict = simulate_memory(args.pages, args.steps, args.working_set, args.pattern)
    lru_hit, lru_evict = simulate_lru_baseline(args.pages, args.steps, args.working_set, args.pattern)

    print("\n=== Memory Comparison ===")
    print(f"QxBin Hit Rate: {qx_hit:.2%}   |   LRU Hit Rate: {lru_hit:.2%}")
    print(f"QxBin Evictions: {qx_evict}     |   LRU Evictions: {lru_evict}")
    if qx_hit > lru_hit:
        print("QxBin probability evolution performed better on this access pattern.")
    else:
        print("LRU was competitive. Try bursty or sequential patterns.")
