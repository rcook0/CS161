\
# Chapter 10 — Amortized Analysis + Data Structures

Amortized analysis is how we prove an operation is *usually cheap* even when individual operations can be expensive.

**Primary pattern:** Amortized analysis [P9].
Three equivalent proof tools (choose the one that fits):
1. **Aggregate method**
2. **Accounting method**
3. **Potential method**

This chapter also pins amortized proofs to concrete data structures:
- Dynamic array doubling
- Stack with multipop
- Union-Find (intuition + where inverse-Ackermann lives)

---

## 10.1 Aggregate Method [P9]

Show that for any sequence of $m$ operations, total cost is $O(f(m))$.
Then amortized cost per op is $O(f(m)/m)$.

### Example: Stack with MultiPop
Operations:
- `push(x)` costs 1
- `pop()` costs 1
- `multipop(k)` pops up to k elements, costing number actually popped.

**Claim.** Any sequence of $m$ ops costs $O(m)$ total. [P9]

**Proof (aggregate).** Each element pushed can be popped at most once (by pop or multipop).
So total number of pops ≤ number of pushes ≤ m.
Total cost = pushes + pops = O(m). □

---

## 10.2 Accounting Method [P9]

Assign each operation an amortized charge; store “credits” to pay future expensive steps.

### Theorem 10.1 (Dynamic array doubling is O(1) amortized) [P9]

Maintain an array with capacity `cap` and size `n`.
When inserting into a full array, allocate new array of size `2*cap` and copy `cap` elements.

**Claim.** `append` runs in O(1) amortized time. [P9]

**Proof (accounting).**
Charge each append 3 credits:
- 1 credit pays the actual write into current array.
- Save 2 credits on the inserted element.

When a resize happens (copying `cap` elements), each copied element uses 1 saved credit to pay for being copied.
Since every element gets at least 1 saved credit at insertion, all copies are paid for.
Thus amortized cost is constant. □

---

## 10.3 Potential Method [P9]

Define a potential function $\Phi$ mapping state to nonnegative reals.
Amortized cost:
$$
\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})
$$
Sum telescopes, giving a bound on total cost.

### Theorem 10.2 (Dynamic array doubling via potential) [P9]

Let size be $n$ and capacity be $cap$.
Use potential:
$$
\Phi = 2n - cap \quad (\text{clamped at } \ge 0)
$$

- Regular insert: $c_i=1$, $cap$ unchanged, $\Phi$ increases by at most 2 ⇒ $\hat c_i \le 3$.
- Resize insert: actual cost $c_i = cap + 1$ (copy cap + write).
After doubling, $cap' = 2cap$ and $n' = cap + 1$:
potential drops enough to pay for the copy, yielding constant amortized cost.

(Exact arithmetic depends on your clamp convention; the core idea is: potential stores “prepaid work” as slack in capacity.) □

---

## 10.4 Union-Find (Disjoint Set Union)

Operations:
- `make_set(x)`
- `find(x)` returns representative
- `union(x,y)` merges sets

Heuristics:
- **Union by rank/size**
- **Path compression**

### Lemma 10.3 (Rank is logarithmic) [P9-ish]
With union-by-rank, a node’s rank increases only when two equal-rank trees merge.
So a node can increase rank at most O(log n) times.

### Theorem 10.4 (Near-constant amortized time) [P9]
Union-by-rank + path compression yields amortized time per operation
$$
O(\alpha(n))
$$
where $\alpha$ is the inverse Ackermann function (grows slower than log*).

We treat this as:
- **CS161-level fact** (proof is advanced)
- but the *shape* of the argument is amortized: compressing paths “pays back” future finds.

---

## 10.5 Proof hooks for code (what to instrument)

To make amortized proofs feel real, collect trace metrics:
- dynamic array: number of copies per append
- stack multipop: total pops across operations
- union-find: path lengths before/after compression

Then compare:
- empirical average cost vs theoretical amortized bound.
