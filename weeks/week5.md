---
layout: page
title: "Week 5: System Testing"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Treat the **entire system** (e.g., NFA simulator plus CLI or API) as the test target.
- Define **system-level test cases** from user-facing behavior and the specification.
- Relate system tests to acceptance criteria and requirements.

## Lecture Notes
- **System testing** exercises the complete system end-to-end. For the NFA project, that might mean: “user supplies a string (or a file of strings); system runs the NFA and outputs accept/reject for each.” Correctness is still defined by the CS5383 NFA specification; system testing adds I/O, error handling, and format checks.
- Scenarios: valid inputs (1101, 0001, 1110, and others), invalid inputs (non-{0,1} characters, empty input if applicable), and batch runs. The project PDF and algorithm-ideas PDF may describe intended usage and boundaries.

## Resources
- [CS5383_Project.pdf](https://github.com/sweeden-ttu/data-structures/blob/master/tot/) and [CS5383_Project_algorithm_ideas.pdf](https://github.com/sweeden-ttu/data-structures/blob/master/tot/) – full project and algorithm context.
- [CS5383_Project_introduction.md](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md) – summary and alignment with V&V.

## Exercises
1. Write system-level test cases for a command-line NFA simulator: (a) one string as argument, output “accept” or “reject”; (b) file of strings, one result per line. Use the project test inputs.
2. List two non-functional aspects you would test at system level (e.g., behavior on very long strings, or malformed input) and the expected outcome.
