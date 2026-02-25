---
layout: page
title: "Week 1: Introduction to V&V"
sidebar:
  nav: weeks
aside:
  toc: true
---

## Learning Objectives
- Distinguish **verification** (building the product right) from **validation** (building the right product).
- Identify **fault**, **error**, and **failure** in the context of software behavior.
- Describe how specifications (e.g., formal models like finite automata) serve as the basis for verification.

## Lecture Notes
- **Verification** checks that the implementation conforms to the specification (e.g., does our NFA simulator accept exactly the strings the specification says it should?).
- **Validation** checks that the specification meets stakeholder needs (e.g., does the chosen NFA model the intended language?).
- A **specification** can be formal (state machine, pre/post conditions) or informal (requirements doc). The [CS5383 project](../data-structures/tot/CS5383_Project_introduction.md) in the data-structures repo provides a concrete formal specification (an NFA) and test inputs used throughout this course.

## Resources
- [Introduction to Software Verification](/2024/12/27/introduction-to-software-verification.html) (course blog).
- [Syllabus](/syllabus.html).
- [CS5383 project introduction](https://github.com/sweeden-ttu/data-structures/blob/master/tot/CS5383_Project_introduction.md) – NFA specification and test inputs used as a running example.

## Exercises
1. For the CS5383 NFA (alphabet {0,1}, states q0,q1,q2, start q0, accept q2, transitions as in the project): list three strings that should be accepted and three that should be rejected. Compare with the given test inputs (1101, 0001, 1110).
2. Give one example each of a **fault**, an **error**, and a **failure** that could occur in an incorrect implementation of that NFA.
