# QxBin Kernel Roadmap

**From simulation to real kernel primitives — shipping in public.**

## Phase 0: Foundation (Done)
- [x] Public repo + vision
- [x] Detailed DESIGN.md
- [x] Reusable Python primitives
- [x] Scheduler, Memory, Power simulations + visualization
- [x] Clear commercial licensing (51% revenue share)

## Phase 1: Simulation & Validation (Complete)
- [x] All three core subsystems with baseline comparison and plotting
- [ ] Integrated multi-subsystem demo
- [ ] Real workload traces
- [ ] More advanced metrics

## Phase 2: Safe Kernel Experimentation (Next)
- [ ] eBPF advisor daemon
- [ ] Sysfs interface
- [ ] Kernel module prototype

## Phase 3: In-Kernel Integration
- [ ] SCHED_QXBIN class
- [ ] Probability-aware memory policy
- [ ] Power management hooks

## Phase 4: Ecosystem
- [ ] Pikkstops deployment
- [ ] Hardware acceleration
- [ ] Hybrid quantum-classical experiments

## How to Help Right Now
- Run all three with --plot and different patterns
- Share results and observations
- Help with integrated simulation or eBPF sketch

Phase 1 visualization layer is now complete across scheduler, memory, and power.

Let's make probabilistic kernels real. 🚀