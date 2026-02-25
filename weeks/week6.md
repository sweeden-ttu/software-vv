---
layout: page
title: "Week 6: Regression Testing"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Define **regression testing**: re-running tests after changes to ensure existing behavior remains correct.
- Build a **regression test suite** from specification-based tests (e.g., NFA accept/reject) and maintain it as the implementation evolves.
- Automate regression tests (e.g., via CI or a test runner) so they run on every change.

## Lecture Notes
- **Regression testing** guards against regressions: new code or fixes should not break previously passing tests. The CS5383 test inputs (1101, 0001, 1110) and any additional strings you derived form a regression suite; every change to the NFA simulator should re-run these tests.
- Organize tests by level (unit, integration, system) and run the full suite before release or after refactoring. The specification (NFA definition) is the stable oracle; tests that encode that oracle should be versioned with the code.

## Resources
- Ammann & Offutt – regression test selection and prioritization.
- [CS5383_Project_Machine.txt](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_Machine.txt) – canonical test inputs for the NFA project.

## Exercises
1. List a minimal set of regression test cases for the CS5383 NFA implementation (strings + expected outcome) that you would run after any code change. Justify why this set is sufficient for the given specification.
2. Sketch a CI step (e.g., GitHub Actions) that runs the NFA test suite on every push to the main branch.
