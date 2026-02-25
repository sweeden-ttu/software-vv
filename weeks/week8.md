---
layout: page
title: "Week 8: Model Checking"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Define **model checking**: exhaustive (or bounded) exploration of a finite-state model to verify properties.
- Model the CS5383 NFA as a state-transition system and express properties (e.g., “every accepting run ends in q2,” “no path from q0 to q2 has only 0s”).
- Use or describe how a model checker could verify such properties against the NFA specification.

## Lecture Notes
- **Model checking** explores all (or many) states and transitions of a finite model to check temporal or safety properties. The CS5383 NFA is already a finite-state model: states K, transition relation Δ, initial state q0, accept set F.
- Example properties: (1) “From any state, the set of next states for symbol σ matches Δ.” (2) “A string is accepted iff there exists a path from q0 to q2 consuming the string.” (3) “The language of accepted strings is non-empty” (q2 is reachable). Tools (e.g., SPIN, NuSMV, or custom exploration) can verify these against the formal description.

## Resources
- Clarke, Grumberg & Peled, *Model Checking*.
- [CS5383_Project_Machine.txt](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_Machine.txt) and [CS5383_Project_introduction.md](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md) – NFA as the model to check.

## Exercises
1. Write two formal properties (in words or logic) that the CS5383 NFA should satisfy: one about the transition relation and one about acceptance. Describe how a model checker could be used to verify them.
2. Build a small state-space representation (states and transitions) for the NFA and manually verify that for the input string 1101 there exists a path from q0 to q2. Document the path.
