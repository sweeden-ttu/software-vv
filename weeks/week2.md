---
layout: page
title: "Week 2: Testing Basics"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Define **test case**, **test suite**, **coverage**, and **oracle**.
- Choose inputs and expected outputs from a specification (e.g., NFA accept/reject).
- Relate testing to verification: tests provide evidence that the implementation matches the specification.

## Lecture Notes
- A **test case** is a pair (input, expected output). For the CS5383 NFA, inputs are strings over {0,1}; the oracle is “accepted” or “rejected” according to the formal definition of the NFA.
- **Coverage** (e.g., state coverage, transition coverage) measures how much of the specification or code is exercised. For the NFA, we can aim to cover every state and every transition.
- The project supplies **test inputs** (1101, 0001, 1110) in `CS5383_Project_Machine.txt`; deriving expected outcomes and adding more tests to improve coverage is part of testing basics.

## Resources
- Ammann & Offutt, *Introduction to Software Testing* – testing terminology and test design.
- [CS5383 project machine and test inputs](https://github.com/sweeden-ttu/data-structures/tree/master/tot) – `CS5383_Project_Machine.txt`, `CS5383_Project_introduction.md`.

## Exercises
1. For the CS5383 NFA, determine the expected outcome (accept/reject) for each of 1101, 0001, 1110 by tracing the transition relation. Document these as a small test suite with an oracle.
2. Add three more test strings that together help cover all states and all transitions. Specify expected outcome for each.
