# Chapter 09 — Dynamic Programming Core

Dynamic programming is what happens when recursion *learns to remember*.

**Primary pattern:** DP optimal substructure [P8] + (often) induction [P1] on subproblem size.

This chapter standardizes DP proofs into a repeatable template:

1. **State** definition (what subproblem means)
2. **Recurrence** (how optimal solution decomposes)
3. **Base cases**
4. **Order of evaluation** (top-down memo or bottom-up)
5. **Correctness proof** (usually induction on state)
6. **Reconstruction** (how to recover an optimal solution)

---

## 9.1 DP Proof Template [P8]

### Step A — State
Define a function $F(s)$ for each state $s$ capturing the optimal value of some subproblem.

### Step B — Optimal substructure
Show: any optimal solution to $s$ can be decomposed into optimal solutions of smaller states.

### Step C — Recurrence
Write $F(s)$ as a min/max over transitions:
$$
F(s) = \min_{a \in Actions(s)} \{ cost(s,a) + F(next(s,a)) \}
$$

### Step D — Base cases
Identify smallest states where answer is immediate.

### Step E — Evaluation order
Argue that when computing $F(s)$, all needed $F(s')$ are already computed.

### Step F — Correctness
Induction on "size" of state or topological order of dependency graph.

### Step G — Reconstruction
Maintain predecessor/choice pointers to reconstruct optimal solution.

---

## 9.2 Example: Longest Increasing Subsequence (LIS) [P8, P1]

Given sequence $a_1,\dots,a_n$.

### State
Let $dp[i]$ = length of LIS ending at position $i$.

### Recurrence
$$
dp[i] = 1 + \max\{ dp[j] : j<i \text{ and } a_j < a_i \}
$$
If no such $j$, then $dp[i]=1$.

### Answer
$\max_i dp[i]$.

### Correctness sketch [P1]
Induct on $i$. Any LIS ending at $i$ must choose a previous element $j<i$ with $a_j<a_i$ as predecessor, and the best such choice is captured by the max.

### Complexity
$O(n^2)$ time, $O(n)$ space.
(Extension: patience sorting gives $O(n\log n)$, but the DP proof is the canonical CS161 form.)

---

## 9.3 Example: Longest Common Subsequence (LCS) [P8, P1]

Strings $X[1..n]$, $Y[1..m]$.

### State
$dp[i][j]$ = length of LCS of prefixes $X[1..i]$ and $Y[1..j]$.

### Recurrence
If $X[i]=Y[j]$:
$$
dp[i][j] = 1 + dp[i-1][j-1]
$$
Else:
$$
dp[i][j] = \max\{ dp[i-1][j],\ dp[i][j-1] \}
$$

### Base cases
Row 0 and column 0 are 0.

### Correctness sketch [P1]
Induct on $i+j$. If last chars match, any LCS must include them; if not, drop one char and take best.

### Complexity
$O(nm)$ time, $O(nm)$ space.
(Space optimization to $O(\min(n,m))$ exists.)

---

## 9.4 Example: 0/1 Knapsack [P8, P1]

Items $1..n$ with weight $w_i$ and value $v_i$, capacity $W$.

### State
$dp[i][c]$ = max value using items $1..i$ within capacity $c$.

### Recurrence
If $w_i > c$:
$$
dp[i][c] = dp[i-1][c]
$$
Else:
$$
dp[i][c] = \max\{ dp[i-1][c],\ v_i + dp[i-1][c-w_i] \}
$$

### Correctness sketch [P8]
Optimal solution either excludes item $i$ or includes it; both subproblems are optimal substructure cases.

### Complexity
$O(nW)$ time, $O(nW)$ space (or $O(W)$ with rolling array).

---

## 9.5 Reconstruction Hooks [P8]

For each recurrence, store a *choice pointer*:
- LIS: predecessor index
- LCS: direction (diag/up/left)
- Knapsack: include/exclude decision

Then backtrack from the best terminal state.

---

## 9.6 Meta: DP as Shortest Path in DAG (optional bridge)

Many DP problems can be reframed as shortest/longest path in a DAG of states.
This unifies DP [P8] with relaxation ideas [P5], but DP’s proof story is still the recurrence + induction template.
