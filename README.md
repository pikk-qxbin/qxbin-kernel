# QxBin Kernel

**Probabilistic computing primitives at the operating system level, powered by QxBin logic.**

Democratizing quantum-inspired decision-making for scheduling, memory, power, and security on today's classical hardware.

Part of the [pikk-qxbin](https://github.com/pikk-qxbin/qxbin) ecosystem.

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

- `prototypes/integrated_demo.py` — Main showcase (Scheduler + Memory + Power with trends)
- `prototypes/qxbin_primitives.py` — Reusable core logic
- Individual subsystem simulations (scheduler, memory, power)
- `DESIGN.md` — Technical architecture and integration points
- `ROADMAP.md` — Current status and future direction

## Status (June 2026)

**Phase 1 (Simulation Layer)**: Complete
- Reusable primitives
- Three subsystem simulations with visualization
- Integrated demo with trend tracking

**Next**: Move toward eBPF advisor and real kernel experimentation.

## Vision

Change the mathematical language of the kernel from rigid binary decisions to calibrated probability evolution.

Ship fast. Iterate in public. Make advanced logic accessible.

## Links

- Core QxBin: https://github.com/pikk-qxbin/qxbin
- X: @rupeshmalpani

Let's evolve the kernel. 🚀