#!/usr/bin/env python3
"""
QxBin v2.0 CuPy GPU Kernel — Coordinate Power Recall Engine (GPU accelerated)

Drop-in GPU version of v2/qxbin_v2_kernel.py using CuPy.
Same API, same math, massive speed-up for large batches or real-time loops.

Requires: cupy-cuda12x (or matching your CUDA version)

Part of pikk-qxbin ecosystem
MIT License (same as CPU kernel)
"""

import cupy as cp
from typing import List, Optional


class QxBinV2CuPy:
    """
    QxBin v2.0 GPU Kernel (CuPy backend)

    Exact same interface and behavior as QxBinV2 (CPU), but all heavy lifting
    (power, clip, normalize, vector ops) happens on the GPU.

    Use this when you need:
    - Large numbers of parallel simulations
    - Real-time interactive recall loops
    - Feeding the hardware mapper at high frequency
    """

    def __init__(self, n: int = 2):
        self.n = n
        self.num_states = 2 ** n
        self.probs = cp.ones(self.num_states, dtype=cp.float32) / self.num_states
        self.signature: Optional[cp.ndarray] = None
        self.history: List[cp.ndarray] = []

    def set_signature(self, grid_2x2: List[List[int]]):
        """Load signature (same as CPU version)."""
        self.signature = cp.array(grid_2x2, dtype=cp.int32).reshape(2, 2)
        flat = self.signature.flatten()

        base = cp.array([0.12, 0.12, 0.12, 0.12], dtype=cp.float32)
        for i, val in enumerate(flat):
            if val == 1:
                base[i] += 0.28
        self.probs = base / base.sum()
        self.history = [self.probs.copy()]

    def apply_coordinate_power(self, powers: cp.ndarray):
        """Core v2.0 primitive on GPU."""
        powers = cp.asarray(powers, dtype=cp.float32)
        new_probs = self.probs.copy()

        # Positive degree → amplify
        pos_mask = powers > 0
        if cp.any(pos_mask):
            new_probs[pos_mask] = new_probs[pos_mask] ** (1.0 / (1.0 + 0.7 * powers[pos_mask]))

        # Negative degree → suppress
        neg_mask = powers < 0
        if cp.any(neg_mask):
            new_probs[neg_mask] = new_probs[neg_mask] ** (1.0 - 0.5 * powers[neg_mask])

        new_probs = cp.clip(new_probs, 1e-12, 1.0)
        self.probs = new_probs / new_probs.sum()
        self.history.append(self.probs.copy())

    def recall(self,
               target: List[float],
               max_steps: int = 30,
               step_size: float = 0.55,
               tol: float = 0.012) -> bool:
        target = cp.asarray(target, dtype=cp.float32)
        target = target / target.sum()

        for _ in range(max_steps):
            error = target - self.probs
            powers = step_size * error * 14.0
            self.apply_coordinate_power(powers)

            if cp.max(cp.abs(error)) < tol:
                return True
        return False

    def visualize_text(self) -> str:
        # Move to CPU only for printing
        probs_cpu = cp.asnumpy(self.probs)
        labels = [f"|{format(i, f'0{self.n}b')}" for i in range(self.num_states)]
        lines = []
        for lab, p in zip(labels, probs_cpu):
            bar = "█" * int(round(p * 28))
            lines.append(f"{lab}  {bar:<28}  {p:.4f}")
        return "\n".join(lines)

    def get_current_cloud(self) -> cp.ndarray:
        return self.probs.copy()

    def reset(self):
        self.probs = cp.ones(self.num_states, dtype=cp.float32) / self.num_states
        self.history = [self.probs.copy()]


if __name__ == "__main__":
    print("QxBin v2.0 CuPy GPU Kernel Demo\n")
    print("(Requires cupy-cudaXX installed and NVIDIA GPU)\n")

    try:
        qx = QxBinV2CuPy(n=2)
        signature = [[1, 0], [0, 1]]
        qx.set_signature(signature)

        print("Initial cloud:")
        print(qx.visualize_text())

        target = [0.08, 0.12, 0.18, 0.62]
        reached = qx.recall(target, max_steps=25, step_size=0.52)

        print("\nAfter GPU Coordinate Power Recall:")
        print(qx.visualize_text())
        print(f"\nTarget reached: {reached}")
    except Exception as e:
        print(f"CuPy not available or no GPU: {e}")
        print("Falling back to CPU kernel is recommended for development.")