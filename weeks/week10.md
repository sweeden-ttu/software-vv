---
layout: page
title: "Week 10: Performance & Security"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Consider **performance** of an NFA simulator: time and space as a function of input length and state set size; avoid unnecessary recomputation or state explosion in exploration.
- Identify **security-related** concerns: e.g., input validation (reject non-alphabet symbols), resource limits (very long strings), and integrity of the specification and test data.
- Relate performance and security to the CS5383 project and to the software-vv tooling (e.g., UI validation, agents).

## Lecture Notes
- **Performance**: NFA simulation is polynomial in the length of the input and the size of the state set; multiple runs (e.g., for many test strings) should be efficient. For model checking or exhaustive exploration, state space size is bounded by |K| and input length; discuss scalability.
- **Security**: Ensure the simulator only reads from the defined alphabet; handle malformed or maliciously long input without denial-of-service. The project’s machine and test files (CS5383_Project_Machine.txt, etc.) are trusted specifications; protect them from tampering in version control and CI.

## Resources
- [CS5383_Project_introduction.md](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md) – project scope and references.
- Course site – UI validation, agents, and Canvas integration as examples of tooling that touches security and performance.

## Exercises
1. For the CS5383 NFA, state the worst-case time complexity of “accepts(w)” in terms of |w| and |K|, and suggest one optimization (e.g., caching or early exit) that could improve typical performance.
2. List two security or robustness checks you would add to an NFA simulator (e.g., input validation, length limit) and how they relate to the formal specification (alphabet Σ, bounded input).
