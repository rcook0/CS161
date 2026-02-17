\
# Chapter 11 — NP & Reductions

This chapter is about **how to prove problems are hard** (under standard assumptions).
The central tool is the **polynomial-time reduction** pattern.

**Primary pattern:** Reduction [P10].

---

## 11.1 Decision vs Optimization (always reduce to decision)

Most NP-completeness statements are about **decision problems**:
- “Is there a solution of cost ≤ K?”
not
- “Find the best solution.”

Optimization problems are often NP-hard because their decision versions are NP-complete.

---

## 11.2 Classes: P, NP, NP-hard, NP-complete

### Definition (P)
P is the class of decision problems solvable in polynomial time.

### Definition (NP)
NP is the class of decision problems where a “yes” instance has a certificate (witness) verifiable in polynomial time.

Equivalently: solvable by a nondeterministic polynomial-time TM.

### Definition (NP-hard)
A problem $B$ is NP-hard if every problem $A$ in NP reduces to $B$ in polynomial time.

### Definition (NP-complete)
$B$ is NP-complete if:
1. $B \in NP$
2. $B$ is NP-hard

If any NP-complete problem is in P, then P = NP.

---

## 11.3 Polynomial-time reductions [P10]

### Definition (Karp reduction)
A polynomial-time many-one reduction $A \le_p B$ is a function $f$ computable in poly-time such that:
$$
x \in A \iff f(x) \in B.
$$

### Why reductions work
If $A \le_p B$ and $B \in P$, then $A \in P$ (compose: compute $f(x)$ then solve $B$).

So to show $B$ is hard, we reduce a known-hard $A$ to $B$.

---

## 11.4 Reduction proof template [P10]

To prove $B$ is NP-complete:

1. **Membership:** Show $B\in NP$ (give a certificate + verifier).
2. **Choose source:** pick known NP-complete problem $A$.
3. **Map instances:** define $f$ from instances of $A$ to instances of $B$.
4. **Correctness (iff):** prove:
   - If $x \in A$, then $f(x)\in B$.
   - If $f(x)\in B$, then $x \in A$.
5. **Polynomial bound:** argue $f$ runs in poly-time and size blowup is polynomial.

Common failure modes:
- proving only one direction
- hiding exponential blowups in the mapping
- mapping a "yes" to a weaker condition than needed

---

## 11.5 Canonical NP-complete problem: 3SAT

### 3SAT
Input: CNF formula with exactly 3 literals per clause.
Question: Is it satisfiable?

3SAT is NP-complete (Cook–Levin gives SAT, then SAT → 3SAT).

We’ll use 3SAT as a reduction source.

---

## 11.6 Example reduction: 3SAT → Vertex Cover [P10]

### Target problem: Vertex Cover (decision)
Input: graph $G=(V,E)$ and integer $k$.
Question: is there a subset $C\subseteq V$ with $|C|\le k$ such that every edge has at least one endpoint in $C$?

### Step 1: Vertex Cover ∈ NP
Certificate: the set $C$.
Verifier: check $|C|\le k$ and every edge is covered. Runs in $O(|E|)$.

### Step 2: Build the reduction
Given a 3CNF formula with variables $x_1..x_n$ and clauses $C_1..C_m$.

Construct graph:

**Variable gadgets**
For each variable $x_i$, create two vertices $(x_i)$ and $(\neg x_i)$ with an edge between them.
Intuition: cover must pick at least one of them (represents assignment).

**Clause gadgets**
For each clause $(\ell_1 \vee \ell_2 \vee \ell_3)$, create a triangle among vertices $\ell_1,\ell_2,\ell_3$.
A vertex cover of a triangle must include at least 2 vertices.

**Consistency edges**
Connect each clause literal vertex to its corresponding variable literal vertex (so choosing literals consistently matters).

Set:
$$
k = n + 2m
$$

### Step 3: Correctness (⇐⇒)

#### (⇒) If formula is satisfiable, then G has a VC of size ≤ k
Given satisfying assignment:
- For each variable gadget, choose the literal vertex that is TRUE. That covers the variable edge: contributes $n$.
- For each clause triangle: since clause is satisfied, at least one literal is TRUE; leave that literal **out** of the cover and include the other two vertices. That covers all triangle edges: contributes $2m$.
- Consistency edges are covered because any clause vertex included is itself in the cover; and if a clause literal is excluded, it is TRUE and its variable literal vertex was selected among the $n$ picks.

Total size = $n + 2m = k$.

#### (⇐) If G has a VC of size ≤ k, then formula is satisfiable
Assume a vertex cover $C$ of size ≤ $n+2m$.
- In each variable gadget edge, at least one endpoint must be in $C$. With total budget $n+2m$, we can afford **at most** 1 per gadget on average, so we may assume exactly 1 chosen per variable edge (otherwise we'd exceed budget or steal from clause triangles).
Define assignment: if $(x_i)\in C$ set $x_i=TRUE$ else set $x_i=FALSE$.

- In each clause triangle, at least 2 vertices must be chosen to cover the triangle edges. With budget $2m$ for all clauses, each triangle must contribute exactly 2 chosen vertices, leaving exactly 1 literal vertex outside the cover.

Let that excluded literal in clause $j$ be $\ell$.
We claim $\ell$ evaluates to TRUE under the assignment.
If it were FALSE, then its corresponding variable literal vertex would not be selected in the variable gadget, forcing the consistency edge incident to $\ell$ to be uncovered (since $\ell$ is excluded). Contradiction.
Therefore each clause has a TRUE literal → formula is satisfied.

### Step 4: Polynomial bound
Graph size is $O(n+m)$ vertices and edges. Construction is polynomial.

Thus Vertex Cover is NP-complete. □

---

## 11.7 A second classic equivalence: Vertex Cover ↔ Independent Set [P10]

- $C$ is a vertex cover iff $V\setminus C$ is an independent set.
- So VC is NP-complete ⇔ IS is NP-complete (easy reductions both ways).

---

## 11.8 Where to go next
Common CS161 continuation reductions:
- 3SAT → Clique
- 3SAT → Hamiltonian Cycle
- 3SAT → Subset Sum / Partition

The pattern remains identical: gadget design + iff proof + polynomial bound.
