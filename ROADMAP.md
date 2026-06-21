# QxBin Kernel Roadmap

**From simulation to real kernel primitives — shipping in public.**

## Phase 0: Foundation (Done)
- [x] Public repo + vision
- [x] Detailed DESIGN.md with C structs, integration points, and challenges
- [x] Reusable Python primitives (`prototypes/qxbin_primitives.py`)
- [x] Scheduler simulation prototype
- [x] Clear commercial licensing (51% revenue share for commercial use)

## Phase 1: Simulation & Validation (Now — Next 2–4 weeks)
- [ ] Enhance scheduler prototype with real workload traces + comparison to CFS
- [ ] New memory management simulation prototype (page probability matrices)
- [ ] Power/thermal decision prototype
- [ ] Add metrics: Jain's fairness index, tail latency proxy, energy estimate
- [ ] Benchmark suite (synthetic + real Linux traces)
- [ ] Community feedback via issues

## Phase 2: Safe Kernel Experimentation (1–3 months)
- [ ] eBPF-based advisor daemon (user-space QxBin + kernel telemetry)
- [ ] Sysfs / debugfs interface for cubit state inspection
- [ ] Per-CPU cubit state in a kernel module (prototype)
- [ ] Safety analysis (determinism modes, attack surface)

## Phase 3: In-Kernel Integration (3–6 months)
- [ ] New `SCHED_QXBIN` scheduler class or extension to `fair_sched_class`
- [ ] Probability-aware page replacement policy (mm/)
- [ ] Integration points in power management and interrupt handling
- [ ] Upstream discussion / RFC on LKML (after solid benchmarks)

## Phase 4: Ecosystem & Hardware (6–12 months+)
- [ ] Pikkstops / edge deployment experiments
- [ ] Hardware acceleration hooks (use existing vector/SIMD or propose small matrix ops)
- [ ] Hybrid classical + quantum co-processor interfaces
- [ ] Educational materials + JEE-style conceptual depth for students

## Guiding Principles
- First principles: Change the mathematical language of the kernel.
- Ship fast, iterate in public.
- Keep deterministic paths safe; make probabilistic paths the default for most workloads.
- Democratize advanced decision logic for edge and micro-enterprise use cases.
- Commercial clarity from day one (51% revenue share model).

## How to Help Right Now
- Run and extend the prototypes
- Open issues with workload ideas or benchmark suggestions
- Prototype the memory or power modules
- Review DESIGN.md and suggest improvements

This roadmap is living. Update it as we learn.

Let's make probabilistic kernels real. 🚀