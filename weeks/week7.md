---
layout: page
title: "Week 7: Static Analysis"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Explain **static analysis**: analyzing code or models without executing them (syntax, control flow, data flow, type checking).
- Use static analysis to find potential bugs (e.g., unreachable states, dead code) in an implementation or in a model of the NFA.
- Relate static analysis to specifications: e.g., check that every transition in the code matches the specification Δ.

## Lecture Notes
- **Static analysis** includes compilers (syntax, types), linters, and deeper analyses (unreachable code, null dereferences). For an NFA simulator, static checks might include: “every (state, symbol) pair in the code appears in Δ,” “no transition to a non-existent state,” “start state and accept set match the specification.”
- Model-level static analysis: the NFA itself can be analyzed (e.g., is q2 reachable from q0? are there dead states?). This supports validation of the specification before or alongside implementation.

## Resources
- Course blog and syllabus – Static Analysis in Part 4.
- [CS5383 project introduction](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md) – NFA structure (states, Δ) to compare against code or tools.

## Exercises
1. For the CS5383 NFA, list all (state, symbol) pairs that have a transition in Δ. Describe a static check that would fail if the implementation had an extra transition not in Δ.
2. Perform a simple reachability analysis on the NFA: from q0, which states are reachable? Is every state in K reachable? Is q2 reachable? Document the result.
