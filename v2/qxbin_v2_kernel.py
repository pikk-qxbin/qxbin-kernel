#!/usr/bin/env python3
"""
QxBin v2.0 Kernel — Coordinate Power Recall Engine
Part of pikk-qxbin ecosystem

MIT License

Copyright (c) 2026 Rupesh Malpani / Pikk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

--------------------------------------------------------------------------------
QxBin v2.0 implements the Coordinate Power Recall primitive discovered in the
July 2026 notebook work:

    Binary Signature Grid (2x2 I/0) 
        → Probability Cloud (4-mass visualization)
        → Coordinate mapping + signed power degrees (positive = amplify, negative = suppress)
        → Recalled / Collapsed target superposition

This is the mathematical heart that replaces standard matrix multiplication with
steerable probability evolution — exactly as drawn in the handwritten notes.
"""

import numpy as np
from typing import List, Optional


class QxBinV2:
    """
    QxBin v2.0 — Coordinate Power Recall Kernel

    Core innovation:
    - Accepts your 2x2 binary signature grids directly
    - Maintains a live 4-state probability cloud
    - Uses signed coordinate powers to steer any current cloud
      toward a desired target superposition (the "recall" operation)

    Designed to be:
    - Extremely simple to understand and extend
    - GPU-portable (CuPy / CUDA next)
    - Hardware-mappable (probability → field strength in the schematic)
    """

    def __init__(self, n: int = 2):
        self.n = n
        self.num_states = 2 ** n
        self.probs = np.ones(self.num_states) / self.num_states
        self.signature: Optional[np.ndarray] = None
        self.history: List[np.ndarray] = []

    # ------------------------------------------------------------------
    # 1. INPUT: Load one of your handwritten 2x2 binary signatures
    # ------------------------------------------------------------------
    def set_signature(self, grid_2x2: List[List[int]]):
        """Load signature exactly as drawn in the notebook pages."""
        self.signature = np.array(grid_2x2, dtype=int).reshape(2, 2)
        flat = self.signature.flatten()

        # Expansion rule tuned to match the visual patterns you drew
        # (stronger 1s bias the initial probability mass)
        base = np.array([0.12, 0.12, 0.12, 0.12])
        for i, val in enumerate(flat):
            if val == 1:
                base[i] += 0.28
        self.probs = base / base.sum()
        self.history = [self.probs.copy()]

    # ------------------------------------------------------------------
    # 5. THE v2.0 CORE: Coordinate Power Recall
    # ------------------------------------------------------------------
    def apply_coordinate_power(self, powers: np.ndarray):
        """
        The key primitive from the July 2026 notes.

        powers: signed degrees, one per basis state
            Positive degree → amplify that component's probability mass
            Negative degree → suppress that component

        After update we always renormalize so we stay in valid probability space.
        """
        powers = np.asarray(powers, dtype=float)
        new_probs = self.probs.copy()

        for i, d in enumerate(powers):
            if d > 0:
                # Amplify — higher positive d gives stronger but controlled boost
                new_probs[i] = new_probs[i] ** (1.0 / (1.0 + 0.7 * d))
            elif d < 0:
                # Suppress
                new_probs[i] = new_probs[i] ** (1.0 - 0.5 * d)

        new_probs = np.clip(new_probs, 1e-12, 1.0)
        self.probs = new_probs / new_probs.sum()
        self.history.append(self.probs.copy())

    # ------------------------------------------------------------------
    # High-level recall loop (matches the flowchart exactly)
    # ------------------------------------------------------------------
    def recall(self,
               target: List[float],
               max_steps: int = 30,
               step_size: float = 0.55,
               tol: float = 0.012) -> bool:
        """
        Steer the current probability cloud toward any target superposition
        using the Coordinate Power mechanism.

        Returns True if we reached the target within tolerance.
        """
        target = np.asarray(target, dtype=float)
        target = target / target.sum()

        for _ in range(max_steps):
            error = target - self.probs
            # Coordinate power proportional to signed error
            powers = step_size * error * 14.0
            self.apply_coordinate_power(powers)

            if np.max(np.abs(error)) < tol:
                return True
        return False

    # ------------------------------------------------------------------
    # Visualization helpers (text version matches your circle clusters)
    # ------------------------------------------------------------------
    def visualize_text(self) -> str:
        labels = [f"|{format(i, f'0{self.n}b')}" for i in range(self.num_states)]
        lines = []
        for lab, p in zip(labels, self.probs):
            bar = "█" * int(round(p * 28))
            lines.append(f"{lab}  {bar:<28}  {p:.4f}")
        return "\n".join(lines)

    def get_current_cloud(self) -> np.ndarray:
        return self.probs.copy()

    def reset(self):
        """Reset to uniform superposition (maximum uncertainty)."""
        self.probs = np.ones(self.num_states) / self.num_states
        self.history = [self.probs.copy()]


# ----------------------------------------------------------------------
# Example usage matching the spirit of your notebook pages
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("QxBin v2.0 Kernel — Coordinate Power Recall Demo\n")

    qx = QxBinV2(n=2)

    # Example signature inspired by several of your 2x2 grids
    signature = [
        [1, 0],
        [0, 1]
    ]
    qx.set_signature(signature)

    print("Initial cloud from signature [1 0 / 0 1]:")
    print(qx.visualize_text())
    print()

    # Target: strong recall of |11> (example of "recalling a given superposition")
    target = [0.08, 0.12, 0.18, 0.62]

    reached = qx.recall(target, max_steps=25, step_size=0.52)

    print("After Coordinate Power Recall toward target:")
    print(qx.visualize_text())
    print(f"\nTarget reached within tolerance: {reached}")
    print(f"Final probability vector: {qx.get_current_cloud().round(4)}")
    print("\nKernel ready for GPU port, hardware mapper, and edge deployment.")