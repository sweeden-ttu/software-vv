---
layout: page
title: "Week 4: Integration Testing"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Combine **unit-level components** (e.g., transition step, accept check, main loop) and test their interaction.
- Identify **interfaces** between components and design integration tests that cross those boundaries.
- Use the specification to define expected behavior at integration level.

## Lecture Notes
- **Integration testing** verifies that units work together correctly. For an NFA simulator: the “step” function, the “is accept state?” function, and the main loop that applies steps and checks acceptance must be integrated and tested as a whole.
- Test scenarios: multi-step runs that use both q0→q1 and q1→q2, strings that require multiple transitions from q0, and strings that reject (e.g., end in q0 or q1). The CS5383 test inputs (1101, 0001, 1110) are integration-level tests once the full run is implemented.

## Resources
- Pezzè & Young, *Software Testing and Analysis* – integration strategies.
- [CS5383_Project_Machine.txt](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_Machine.txt) – machine and official test inputs.

## Exercises
1. Define an integration test suite for “NFA run from start to accept/reject” that includes the three project test strings plus at least two strings that are rejected. Specify the expected result for each from the NFA definition.
2. Describe one integration fault (e.g., wrong order of applying step vs. checking accept) and write a test that would expose it.
