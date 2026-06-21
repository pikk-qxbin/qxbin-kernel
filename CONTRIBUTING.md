# Contributing to qxbin-kernel

Thank you for your interest in evolving the kernel with QxBin logic!

We move fast with first-principles thinking and ship in public.

## How to Contribute

1. **Fork** the repo and create a feature branch.
2. **Experiment** — run the prototypes, tweak biases, add new simulation modules.
3. **Open an issue** first for bigger changes (use the templates).
4. **Submit a PR** with clear description and before/after behavior.

## Focus Areas (High Impact)
- New simulation prototypes (memory, power, security)
- Better metrics and workload generators
- eBPF sketches and kernel module experiments
- Documentation and diagrams
- Benchmarks comparing against CFS / existing policies

## Code Style
- Python prototypes: Clean, well-commented, reusable via `qxbin_primitives.py`
- Keep grid sizes small (4–8) for performance intuition
- Document the "why" behind every bias / evolution choice

## License & Commercial Use
The repo uses a refined MIT license with a **51% revenue share** for any commercial tool, product, or API built on this work (enterprise terms negotiable). See LICENSE for details.

This keeps the project sustainable while staying open for research, education, and collaboration.

## Communication
- GitHub Issues & Discussions
- X: @rupeshmalpani
- Core QxBin framework: https://github.com/pikk-qxbin/qxbin

Ship it. Measure it. Iterate. 🚀

Happy to review early ideas — just open an issue or tag in a PR.