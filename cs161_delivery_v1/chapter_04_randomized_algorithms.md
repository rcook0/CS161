
# Chapter 04 — Randomized Algorithms

## 4.1 Model and Guarantees
We analyze algorithms in the randomized RAM model. Guarantees are stated as expected time or high-probability bounds.

## 4.2 Linearity of Expectation
**Theorem.** For random variables X_i, E[Σ X_i] = Σ E[X_i], independent of dependence.
**Proof.** Follows directly from definition of expectation.

**Pattern:** expectation

## 4.3 Randomized Quicksort
Algorithm chooses a pivot uniformly at random and partitions recursively.
**Theorem.** Expected comparisons ≤ 2n ln n.
**Proof Sketch.** Define indicator I_{ij} for comparison of i,j; sum expectations.

**Executable Witness:** `cs161lab.algorithms.sorting.rand_quicksort`
**Trace Events:** pivot, partition

## 4.4 Randomized Selection (QuickSelect)
Expected linear time via shrinking subproblem.
**Pattern:** expectation, induction
**Executable Witness:** `quickselect`

## 4.5 Amplification
Repeating an algorithm with constant success probability reduces failure exponentially.
**Pattern:** amplification

## 4.6 Karger’s Min-Cut
Random edge contraction yields success ≥ 2/(n(n−1)). Repetition boosts confidence.
**Executable Witness:** `cs161lab.algorithms.mincut.karger`
**Trace Events:** contract, trial, best

## 4.7 Failure Modes
Randomness does not replace proof; adversarial framing matters.

## Appendix A — Trace Events
Trace events provide proof witnesses aligning execution with invariants.
