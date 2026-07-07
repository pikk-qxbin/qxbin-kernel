# QxBin Kernel

**Probabilistic computing primitives at the operating system level, powered by QxBin logic.**

Democratizing quantum-inspired decision-making for scheduling, memory, power, and security on today's classical hardware.

Part of the [pikk-qxbin](https://github.com/pikk-qxbin/qxbin) ecosystem.

## 🚀 QxBin v2.0 — Coordinate Power Recall (Just Landed)

**New mathematical primitive** from the July 2026 notebook work:

- Binary Signature Grids (your 2×2 I/0 patterns) → live Probability Clouds
- **Coordinate Power Recall**: signed positive/negative power degrees along coordinates to steer and *recall* any target superposition
- Replaces rigid matrix multiplication with steerable probability evolution
- Exactly matches the 7-step flowchart and 3-layer hardware schematic we generated from the notes

**File**: `v2/qxbin_v2_kernel.py`

```bash
python v2/qxbin_v2_kernel.py
```

This is the core engine that will feed the Probability ↔ Field Mapper and the room-temperature hardware prototype.

---

## Current Best Demo

**`prototypes/integrated_demo.py`** — The main showcase right now.

It runs **Scheduler + Memory + Power** together with trend tracking and produces combined metrics + rich visualization.

```bash
cd prototypes
python integrated_demo.py --pattern bursty --steps 600 --plot
```

This is currently the best single script to understand and demonstrate the QxBin kernel vision.

## Why This Matters

Modern kernels still speak the language of 1940s binary certainty. Workloads today are uncertain, bursty, and mixed (AI + traditional). QxBin replaces rigid 0/1 logic with Binary Probability Matrices that evolve like a spinning coin until measured.

At the kernel level, this enables:
- Adaptive, uncertainty-aware scheduling
- Smarter memory & prefetch decisions
- Probabilistic power/thermal management
- Better handling of mixed workloads on edge devices

All on today's classical hardware.

## Quick Start

```bash
pip install matplotlib   # for visualization

# Run the main integrated demo
python prototypes/integrated_demo.py --pattern bursty --plot

# Individual subsystems (if you want to explore separately)
python prototypes/kernel_scheduler_sim.py --plot
python prototypes/memory_sim.py --plot
python prototypes/power_sim.py --plot
```

## What's in the Repo

- `v2/qxbin_v2_kernel.py` — **NEW** QxBin v2.0 Coordinate Power Recall kernel
- `prototypes/integrated_demo.py` — Main showcase (Scheduler + Memory + Power with trends)
- `prototypes/qxbin_primitives.py` — Reusable core logic (v1 foundation)
- Individual subsystem simulations (scheduler, memory, power)
- `DESIGN.md` — Technical architecture and integration points
- `ROADMAP.md` — Current status and future direction

## Status (July 2026)

**Phase 1 (Simulation Layer)**: Complete
- Reusable primitives
- Three subsystem simulations with visualization
- Integrated demo with trend tracking
- **v2.0 Coordinate Power Recall kernel** (new mathematical primitive)

**Next**: GPU/CUDA port of v2 kernel + Probability ↔ Field Mapper for hardware prototype.

## Vision

Change the mathematical language of the kernel from rigid binary decisions to calibrated probability evolution.

Ship fast. Iterate in public. Make advanced logic accessible.

## Links

- Core QxBin: https://github.com/pikk-qxbin/qxbin
- X: @rupeshmalpani

Let's evolve the kernel. 🚀