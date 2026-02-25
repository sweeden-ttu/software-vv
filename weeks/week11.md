---
layout: page
title: "Week 11: Final Project"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Integrate **verification and validation** techniques from the course: specification (CS5383 NFA), testing (unit, integration, system, regression), static analysis, model checking, and formal reasoning.
- Deliver an **NFA simulator** (or equivalent artifact) that implements the CS5383 project machine, with tests and documentation that align with the software-vv syllabus.
- Document how the project aligns with the course and with the [data-structures/tot](https://github.com/sweeden-ttu/data-structures/tree/master/tot) project and [software-vv](https://github.com/sweeden-ttu/software-vv) repository (collaboration with Professor Namin).

## Lecture Notes
- The **final project** ties together the course: use the CS5383 NFA (see [CS5383_Project_introduction.md](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md)) as the specification. Implement a simulator (or validator) that accepts/rejects strings according to the machine definition in `CS5383_Project_Machine.txt`.
- Apply techniques from each part: **Fundamentals** (V&V, fault/error/failure); **Testing** (unit tests for step/accept, integration for full run, system tests for I/O, regression suite); **Static analysis** (consistency of implementation with Δ); **Model checking** (reachability, property checking); **Formal methods** (invariants, correctness argument); **Performance & security** (complexity, input validation).
- Reference the project PDF and algorithm-ideas PDF for full requirements; use the supplied test inputs (1101, 0001, 1110) and extend with your own tests.

## Resources
- [CS5383_Project.pdf](https://github.com/sweeden-ttu/data-structures/tree/master/tot), [CS5383_Project_algorithm_ideas.pdf](https://github.com/sweeden-ttu/data-structures/tree/master/tot), [CS5383_Project_Machine.txt](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_Machine.txt), [CS5383_Project_introduction.md](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md).
- [Software Verification and Validation (software-vv)](https://github.com/sweeden-ttu/software-vv) – course site, syllabus, and weekly modules (Weeks 1–11).

## Exercises
1. **Deliverable**: Implement the CS5383 NFA simulator (or a validator that checks acceptance for given strings). Provide a test suite that includes the three project test strings and covers all states and transitions; document expected outcomes from the specification.
2. **Report**: In one to two pages, summarize how you applied at least one technique from each of Parts 1–4 (Fundamentals, Unit/Integration/System, Regression, Static Analysis, Model Checking, Formal Methods) to your implementation. Reference the data-structures/tot project and the software-vv course.
