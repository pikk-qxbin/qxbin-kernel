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

**Phase 1 Simulations Complete** with visualization:
- Scheduler (fairness + baseline + plotting)
- Memory (hit rate + baseline + plotting)
- Power (energy/perf + baseline + plotting)

All three core kernel subsystems now have runnable prototypes with baseline comparison and optional matplotlib charts.

## Vision

Change the mathematical language of the kernel. Move from deterministic heuristics to calibrated probability evolution. Bridge classical OS to hybrid quantum-classical future.

## Quick Start

```bash
git clone https://github.com/pikk-qxbin/qxbin-kernel.git
cd qxbin-kernel/prototypes

pip install matplotlib   # for visualization

# Scheduler with chart
python kernel_scheduler_sim.py --pattern bursty_ai --plot

# Memory with chart
python memory_sim.py --pattern bursty --plot

# Power with chart
python power_sim.py --pattern bursty --plot
```

## Repository Structure

- `README.md`
- `DESIGN.md`
- `ROADMAP.md`
- `prototypes/` — scheduler, memory, power (all with --plot)
- `CONTRIBUTING.md` + issue templates

## How to Contribute

Run the prototypes, compare results, open issues with findings or ideas.

MIT licensed with 51% revenue share for commercial use (see LICENSE).

## Links

- Core QxBin: https://github.com/pikk-qxbin/qxbin
- X: @rupeshmalpani

Let's evolve the kernel. 🚀