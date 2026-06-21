#!/usr/bin/env python3
"""
Reusable QxBin Primitives for Kernel Experiments

Clean, importable core logic extracted from the original framework.
Use this as the foundation for all future scheduler, memory, power, and
security simulation prototypes in qxbin-kernel.

Mirrors the spirit and math of qxbin_edge.py / qxbin_cloud.py but
optimized for easy extension into OS concepts.

Part of the qxbin-kernel exploration.
"""

import numpy as np
from typing import Optional, Tuple


class QxBinCubit:
    """
    A single Binary Probability Matrix cubit.
    Represents a multi-dimensional probabilistic state that can evolve
    under bias and collapse via measurement.
    """

    def __init__(self, grid_size: int = 6, seed: Optional[int] = None):
        if seed is not None:
            np.random.seed(seed)
        self.grid_size = grid_size
        self.state = np.random.rand(grid_size, grid_size).astype(np.float64)
        self.state /= self.state.sum()  # Normalize
        self.bias = 0.65
        self.power_n = 2
        self.power_m = 1
        self.history = []  # Optional: track evolution for analysis

    def apply_superposition(self, new_bias: Optional[float] = None) -> np.ndarray:
        """
        Simulate superposition by blending fractional contributions.
        This is the core 'spinning coin' operation.
        """
        if new_bias is not None:
            self.bias = np.clip(new_bias, 0.05, 0.95)

        frac_heads = self.bias ** self.power_n
        frac_tails = (1.0 - self.bias) ** self.power_m

        # Create probability vector and outer product for 2D matrix
        x = np.linspace(frac_heads, frac_tails, self.grid_size)
        prob_matrix = np.outer(x, x)

        # Blend with current state (multi-dimensional chain evolution)
        self.state = (self.state + prob_matrix) / 2.0
        self.state /= self.state.sum()  # Renormalize

        if hasattr(self, 'history'):
            self.history.append(self.state.copy())
        return self.state

    def measure(self) -> Tuple[int, float]:
        """
        Probabilistic collapse (measurement).
        Returns (flattened_index, probability_of_chosen)
        """
        flat = self.state.flatten()
        idx = np.random.choice(len(flat), p=flat)
        return int(idx), float(flat[idx])

    def get_mean_probability(self) -> float:
        """Aggregate scalar for ranking or deterministic fallback."""
        return float(self.state.mean())

    def reset(self):
        self.state = np.random.rand(self.grid_size, self.grid_size).astype(np.float64)
        self.state /= self.state.sum()
        self.history = []


class QxBinEnsemble:
    """
    Collection of cubits for ensemble / cloud-tier style optimization.
    Useful for global scheduler decisions or multi-core coordination.
    """

    def __init__(self, num_cubits: int = 8, grid_size: int = 6):
        self.cubits = [QxBinCubit(grid_size) for _ in range(num_cubits)]
        self.num_cubits = num_cubits

    def evolve_all(self, biases: Optional[list] = None):
        if biases is None:
            biases = [0.6 + 0.1 * np.random.randn() for _ in range(self.num_cubits)]
        for i, cubit in enumerate(self.cubits):
            cubit.apply_superposition(biases[i])

    def measure_ensemble(self) -> list:
        return [c.measure() for c in self.cubits]

    def get_aggregate_view(self) -> np.ndarray:
        """Mean probability landscape across all cubits."""
        return np.mean([c.state for c in self.cubits], axis=0)


# Convenience functions for quick use in other prototypes
def create_cubit(grid_size: int = 6) -> QxBinCubit:
    return QxBinCubit(grid_size)


def create_ensemble(num: int = 8) -> QxBinEnsemble:
    return QxBinEnsemble(num)
