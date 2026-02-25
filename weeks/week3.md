---
layout: page
title: "Week 3: Unit Testing"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Write **unit tests** that exercise a single component in isolation (e.g., transition function, accept check).
- Use **stubs/mocks** where the unit under test depends on other modules.
- Automate tests and interpret pass/fail with respect to the specification.

## Lecture Notes
- **Unit testing** focuses on the smallest testable units: e.g., a function that computes one step of the NFA, or a predicate that checks whether the current state is accepting.
- For an NFA simulator, natural units include: (1) “given state and symbol, return set of next states”; (2) “given state, is it in F?”; (3) “given string, run the NFA and return accept/reject.” Units (1) and (2) can be tested without the full run logic.
- The CS5383 project specification defines the transition relation and accept set; unit tests should assert behavior against that specification.

## Resources
- [Syllabus](/syllabus.html) – Unit Testing in Part 2.
- [CS5383 project introduction](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md) – formal NFA definition for test oracles.

## Exercises
1. Design unit tests for a function `nextStates(state, symbol)` that returns the set of successor states for the CS5383 NFA. Cover every transition in Δ.
2. Design unit tests for a function `accepts(string)` that returns true iff the NFA accepts the string. Use the supplied test inputs 1101, 0001, 1110 and your derived expected outcomes from Week 2.
