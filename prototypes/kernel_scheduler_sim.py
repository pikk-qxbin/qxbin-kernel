#!/usr/bin/env python3
"""
QxBin Kernel Scheduler Simulation Prototype

Simulates a QxBin-inspired probabilistic scheduler vs simple CFS-like baseline.
Uses the same Binary Probability Matrix logic as qxbin_edge.py.

Run standalone to explore scheduling behavior under mixed/uncertain workloads.
Extend with real telemetry later.

Part of qxbin-kernel exploration.
"""

import numpy as np
import random
from typing import List, Dict

# Reuse / adapt core QxBin logic (small grid for speed)
class QxBinCubit:
    def __init__(self, grid_size: int = 5):
        self.grid_size = grid_size
        self.state = np.random.rand(grid_size, grid_size).astype(np.float64)
        self.state /= self.state.sum()
        self.bias = 0.6
        self.power_n = 2
        self.power_m = 1

    def apply_superposition(self, new_bias: float = None):
        if new_bias is not None:
            self.bias = new_bias
        frac_heads = self.bias ** self.power_n
        frac_tails = (1 - self.bias) ** self.power_m
        x = np.linspace(frac_heads, frac_tails, self.grid_size)
        prob_matrix = np.outer(x, x)
        self.state = (self.state + prob_matrix) / 2.0
        self.state /= self.state.sum()
        return self.state

    def measure(self) -> int:
        """Weighted random collapse -> index in flattened grid (maps to action/priority)"""
        flat = self.state.flatten()
        idx = np.random.choice(len(flat), p=flat)
        return idx

    def get_priority_score(self) -> float:
        """Aggregate for deterministic fallback or ranking"""
        return float(self.state.mean())


class QxBinSchedulerSim:
    def __init__(self, num_tasks: int = 8):
        self.tasks: Dict[int, QxBinCubit] = {i: QxBinCubit() for i in range(num_tasks)}
        self.time = 0

    def update_task(self, task_id: int, runtime_delta: float, io_wait: float = 0.0):
        """Simulate feedback: adjust bias based on observed behavior"""
        cubit = self.tasks[task_id]
        # Simple heuristic: more runtime -> slightly lower bias (more 'ready' lean?)
        # io_wait increases uncertainty / different lean
        effective_bias = 0.5 + 0.3 * (runtime_delta / (runtime_delta + 1)) - 0.2 * io_wait
        effective_bias = np.clip(effective_bias, 0.2, 0.9)
        cubit.apply_superposition(effective_bias)

    def pick_next_task(self, runnable: List[int]) -> int:
        """Probabilistic pick using measure on each cubit"""
        if not runnable:
            return -1
        scores = []
        for tid in runnable:
            cubit = self.tasks[tid]
            # Could use full measure() or mean for softer ranking
            score = cubit.get_priority_score() + 0.1 * random.random()  # small jitter
            scores.append((tid, score))
        # Pick highest score (or full probabilistic collapse across all)
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[0][0]

    def simulate(self, steps: int = 100, workload_pattern: str = "mixed"):
        print(f"Simulating {steps} steps with {len(self.tasks)} tasks ({workload_pattern} workload)...")
        runnable = list(self.tasks.keys())
        stats = {tid: {"runs": 0, "total_runtime": 0.0} for tid in runnable}

        for step in range(steps):
            # Simulate workload feedback (vary by pattern)
            for tid in runnable:
                if workload_pattern == "bursty_ai":
                    rt = random.uniform(0.1, 2.0) if random.random() > 0.7 else 0.05
                    io = random.uniform(0.0, 0.8)
                else:  # mixed
                    rt = random.uniform(0.05, 1.0)
                    io = random.uniform(0.0, 0.3)
                self.update_task(tid, rt, io)

            # Pick and "run"
            chosen = self.pick_next_task(runnable)
            if chosen >= 0:
                stats[chosen]["runs"] += 1
                stats[chosen]["total_runtime"] += 0.1  # fake slice

            self.time += 1

        print("\nResults (runs per task):")
        for tid, s in stats.items():
            print(f"  Task {tid}: {s['runs']} runs, runtime ~{s['total_runtime']:.1f}")
        print(f"Fairness (std of runs): {np.std([s['runs'] for s in stats.values()]):.2f}")


if __name__ == "__main__":
    print("=== QxBin Kernel Scheduler Simulation ===\n")
    sim = QxBinSchedulerSim(num_tasks=6)
    sim.simulate(steps=200, workload_pattern="mixed")
    print("\nTry bursty_ai pattern for more variance...")
    sim2 = QxBinSchedulerSim(num_tasks=6)
    sim2.simulate(steps=200, workload_pattern="bursty_ai")
