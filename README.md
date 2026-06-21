# QxBin Kernel

**Probabilistic computing primitives at the operating system level, powered by QxBin logic.**

Democratizing quantum-inspired decision-making for scheduling, memory, power, and security on today's classical hardware.

Part of the [pikk-qxbin](https://github.com/pikk-qxbin/qxbin) ecosystem by Rupesh Malpani / pikk.company.

## Why This Matters

Modern kernels still speak the language of 1940s binary certainty. Workloads are uncertain, bursty, and mixed (AI + traditional). QxBin replaces rigid 0/1 with Binary Probability Matrices — grids of fractional states that evolve like a spinning coin until measured.

At kernel level this unlocks:
- Adaptive, uncertainty-aware scheduling
- Smarter memory & prefetch under real access patterns
- Probabilistic power/thermal decisions
- Fractional trust & anomaly detection

All without cryogenics or new silicon. Just better math running on what we have today.

## Current Status (June 2026)

**Phase 1 Simulations Complete** — Core trio ready:
- Scheduler with fairness metrics + baseline + optional visualization
- Memory probability matrices + eviction vs LRU
- Power/thermal evolution vs threshold policy

All prototypes use shared reusable primitives and support multiple workload patterns.

## Vision

Change the mathematical language of the kernel. Move from deterministic heuristics to calibrated probability evolution. Bridge classical OS to hybrid quantum-classical future. Make advanced logic accessible at the edge (Pikkstops, kiosks, micro-enterprises).

First principles: Question binary rigidity. Ship prototypes. Iterate in public. Accelerate progress for everyone.

## Quick Start

```bash
git clone https://github.com/pikk-qxbin/qxbin-kernel.git
cd qxbin-kernel/prototypes

# Scheduler (with optional plot)
python kernel_scheduler_sim.py --pattern bursty_ai --plot

# Memory
python memory_sim.py --pattern bursty

# Power
python power_sim.py --pattern bursty
```

Install matplotlib for visualization:
```bash
pip install matplotlib
```

## Repository Structure

- `README.md` - This file
- `DESIGN.md` - Detailed architecture, integration points, algorithms, challenges, roadmap
- `ROADMAP.md` - Phased plan and current status
- `prototypes/` - Runnable simulations (scheduler, memory, power)
- `CONTRIBUTING.md` + issue templates

## How to Contribute

Fork, run the prototypes, tweak workloads or biases, open issues with results or ideas.

All contributions MIT licensed (with 51% revenue share for commercial use — see LICENSE).

## Links

- Core QxBin: https://github.com/pikk-qxbin/qxbin
- Framework site: https://www.pikk.co.in/chain-test
- X: @rupeshmalpani

"Moving past the cooling barrier isn't about better hardware. We just have to change the mathematical language we use to talk to the computer."

Let's evolve the kernel. 🚀