# QxBin Kernel Roadmap

**From simulation to real kernel primitives — shipping in public.**

## Phase 0: Foundation (Done)
- [x] Public repo + vision
- [x] Detailed DESIGN.md with C structs, integration points, and challenges
- [x] Reusable Python primitives (`prototypes/qxbin_primitives.py`)
- [x] Scheduler simulation prototype
- [x] Memory management simulation prototype
- [x] Power/thermal decision prototype
- [x] Clear commercial licensing (51% revenue share for commercial use)

## Phase 1: Simulation & Validation (In Progress)
- [x] Scheduler + baseline comparison (Jain's fairness, multiple patterns)
- [x] Memory probability matrices + eviction vs LRU baseline
- [x] Power/thermal evolution vs threshold policy
- [ ] Add visualization / plotting to outputs
- [ ] Integrated multi-subsystem simulation (scheduler + memory + power)
- [ ] Run on real workload traces
- [ ] Community feedback via issues

## Phase 2: Safe Kernel Experimentation (Next)
- [ ] eBPF-based advisor daemon (user-space QxBin + kernel telemetry)
- [ ] Sysfs / debugfs interface for cubit state inspection
- [ ] Per-CPU cubit state in a kernel module (prototype)
- [ ] Safety analysis (determinism modes, attack surface)

## Phase 3: In-Kernel Integration (Future)
- [ ] New `SCHED_QXBIN` scheduler class or extension to `fair_sched_class`
- [ ] Probability-aware page replacement policy (mm/)
- [ ] Integration points in power management and interrupt handling
- [ ] Upstream discussion / RFC on LKML (after solid benchmarks)

## Phase 4: Ecosystem & Hardware (Longer term)
- [ ] Pikkstops / edge deployment experiments
- [ ] Hardware acceleration hooks (use existing vector/SIMD or propose small matrix ops)
- [ ] Hybrid classical + quantum co-processor interfaces
- [ ] Educational materials + conceptual depth for students

## Guiding Principles
- First principles: Change the mathematical language of the kernel.
- Ship fast, iterate in public.
- Keep deterministic paths safe; make probabilistic paths the default for most workloads.
- Democratize advanced decision logic for edge and micro-enterprise use cases.
- Commercial clarity from day one (51% revenue share model).

## How to Help Right Now
- Run the three prototypes (scheduler, memory, power) with different patterns
- Compare QxBin vs baselines and share results in issues
- Suggest new workload patterns or metrics
- Prototype visualization or integrated simulation

This roadmap is living. We just completed the core simulation trio in Phase 1.

Let's make probabilistic kernels real. 🚀