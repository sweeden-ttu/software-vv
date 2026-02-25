---
layout: page
title: "Week 9: Formal Methods"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Use **formal methods** (e.g., pre/post conditions, invariants, or simple proofs) to reason about the NFA and its implementation.
- State and prove (informally or formally) a property of the NFA (e.g., characterization of accepted strings).
- Relate formal reasoning to testing and model checking: proofs give assurance; tests and model checking provide evidence.

## Lecture Notes
- **Formal methods** include specification languages, invariants, and mathematical proofs. For the CS5383 NFA, we can define the language L(M) formally and prove statements such as: “w ∈ L(M) iff there exists a run from q0 to q2 on w,” or “every string in L(M) has at least one 1” (since the only way to reach q2 is via (q1,1,q2), and q1 is reached only after reading 0 from q0).
- Implementation-level formal methods: specify the step function with pre/post conditions (e.g., “post: result = { q' | (q,σ,q') ∈ Δ }”) and use tests or model checking to validate the implementation against the spec.

## Resources
- Hoare logic, specification by contract; course syllabus – Formal Methods.
- [CS5383_Project.pdf](https://github.com/sweeden-ttu/data-structures/blob/master/tot/) and [CS5383_Project_introduction.md](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md) – NFA as the formal specification.

## Exercises
1. Give an informal proof that the CS5383 NFA accepts the string 0001 (trace the run and conclude acceptance). Then state a simple property that holds for all accepted strings (e.g., “contains at least one 1”) and argue why it holds from the structure of Δ and F.
2. Write a post-condition for a function `nextStates(q, σ)` that returns the set of successor states, and show that the specification Δ satisfies this post-condition for each (q, σ).
