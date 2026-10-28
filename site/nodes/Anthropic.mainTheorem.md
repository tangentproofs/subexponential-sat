---
id: Anthropic.mainTheorem
title: 'Main Theorem (Anthropic): one machine counts k-SAT solutions in time 2^o(n)'
summary: '**The surprise:** a *single* Turing machine, with *one* constant C that does not depend on k, counts the
  satisfying assignments of every k-CNF within 2^{C·min{km/√(log m), k²·n·log log n/√(log n)}} steps, which is 2^{o(n)}
  for each fixed k.'
review: draft
authors:
- grok-bot
caveats:
- The bound is stated for formulas in which every variable occurs, with variables x₀ … x_{n−1}. The step to formulas
  with arbitrary variable names (with a polynomial added) is proved in Lean on the way to `ethIsFalse`, but it is
  not this statement.
- log is `Real.logb 2`, of x itself (not x + 1). At m = 1 the term km/√(log m) would divide by zero, which is why
  m ≥ 2 is assumed; at n < 4, log log n < 1.
- The authors say a reader should compare MainResults.lean with the paper by hand, and the paper's Appendix E lists
  the differences. This site's review has not yet gone through Appendix E line by line.
- The README notes that a condensed prompt lets a model 'rederive the refutation of ETH'. That is a claim about
  AI models, not part of the mathematics, and this site has not tested it.
widgets:
- type: walkthrough
  title: The proof route, as the paper is organised
  config:
    steps:
    - text: '§3–5: count solutions as the value of a tensor network on a complete graph, and bound the cost of computing
        that value (Lemma 1, Lemma 2, Proposition 3)'
      note: 'Lean: proof/networks (Groundwork, Paper, Eight, Value, Variance). The ''eight-square identity'' supplies
        the low-rank pieces (Lemma 2).'
    - text: '§6: Theorem 2, for every δ > 0, 3-SAT in time O(2^{δn}). This already refutes ETH, with a simpler argument'
      note: 'Lean: proof/threesat. Not used by Solution.lean''s route to the Main Theorem, but proved separately.'
    - text: 'Appendices A–B: the bound 2^{O(km/√log m)} in the number of clauses, via a recursion (Theorem A) on
        pieces with parameters (ρ, c)'
      note: 'Lean: proof/rates (PaddedDescent, ClauseBound, PiecesCounted, CountedRecursion …).'
    - text: 'Appendix C: count-preserving sparsification'
      note: 'Lean: proof/sparsification. Reduces general formulas to ones where each variable occurs in few clauses.'
    - text: 'Appendix D: the bound 2^{O(k²n log log n/√log n)} in the number of variables'
      note: 'Lean: proof/variables (parity checks, the cut-off lemma, RecursionToBound …).'
    - text: Take the smaller of the two bounds, on one machine, and convert operation counts to Turing-machine steps
      lean: CountedRoute.mainTheoremHolds
      note: proof/maintheorem/CountedRoute/Main.lean line 92, then Solution.lean line 44. Lean accepts the term
        by unfolding definitions to `MainResults.MainTheorem`.
quiz:
- q: 'Which comes first in the statement: the machine M, or the width k?'
  type: choice
  choices:
  - k, so each k gets its own machine
  - M (and C), so one machine serves every k
  answer: 1
  explain: '`∃ (M …) (C : ℕ), … ∀ (k n : ℕ) (φ : CNF n), …`. The existential is outside the universal.'
- q: Which formulas does the Main Theorem say nothing about?
  type: choice
  choices:
  - formulas with a variable that does not occur, or with fewer than 2 clauses, or fewer than 4 variables
  - formulas with an empty clause
  - formulas with both x and ¬x in a clause
  - 3-CNFs
  answer: 0
  explain: 'The hypotheses are `1 ≤ k`, `IsKCNF k φ`, `2 ≤ φ.length`, `4 ≤ n`, `AllOccur φ`. An empty clause or
    a clause with x and ¬x is still allowed. The docstring says: ''Nothing is said about any other input word.'''
- q: What is the output?
  type: choice
  choices:
  - 'one bit: satisfiable or not'
  - the number of satisfying assignments, in n + 1 bits, lowest bit first
  - a satisfying assignment
  - the count modulo 2
  answer: 1
  explain: '`CountsWithin` asks for output `binary n (numSat φ)`: the lowest n + 1 bits of the count, which is at
    most 2ⁿ, so nothing is lost.'
- q: Is k part of the input?
  type: choice
  choices:
  - 'Yes: the input starts with 1ᵏ 0'
  - 'No: k is fixed in advance'
  answer: 0
  explain: '`encInput k φ = 1ᵏ 0 ++ encClauses k φ`. This is what lets one machine handle every k.'
---
## Plain English

**Theorem (`MainResults.mainTheorem`).** There is one deterministic multi-stack Turing machine (all stack alphabets finite) and one constant C, both chosen *before* k and the formula, such that:

for every k ≥ 1, every n ≥ 4, and every formula φ on the variables x₀ … x_{n−1} in which

- every variable occurs ([AllOccur](#/node/Anthropic.AllOccur)),
- every clause has at most k literals and no clause is written twice ([IsKCNF](#/node/Anthropic.IsKCNF)),
- there are m ≥ 2 clauses,

the machine, started on the code of (k, φ) ([encInput](#/node/Anthropic.encInput)), halts with the number of satisfying assignments of φ ([numSat](#/node/Anthropic.numSat)), written in n + 1 bits, lowest bit first ([binary](#/node/Anthropic.binary)), within [timeMin](#/node/Anthropic.timeMin) C k m n = ⌊2^{C·min{km/√(log m), k²·n·log log n/√(log n)}}⌋ steps ([CountsWithin](#/node/Anthropic.CountsWithin)). Here log is log₂.

The paper's wording (Theorem 1): *"There is a deterministic algorithm that, given a k-CNF with m clauses in which n variables occur, computes the number of satisfying assignments of these n variables in time 2^{O(min{k²n log log n/√log n, km/√log m})}, where the O(·) hides an absolute constant."*

Two things are stronger than refuting ETH needs. First, the machine is **universal**: one machine for every k and every formula, not one per δ. Second, the bound has an explicit o(n) **rate**, and the time has **no extra polynomial factor**.

### The idea, in the authors' condensed form (README)

> Let 2^{e(K)·K²λ}·poly(λ) be the time to contract tensor networks on K_K with λ bits per edge and arbitrary node tensors. Then e(9K^16) ≤ 0.9·e(K) + O(1/K). Put the nodes on a grid: the two diagonals of each rectangle form a swap. Per bit, SWAP = I − 2·singlet; grouping by the number of singlets gives λ+1 operators with (row rank)·(column rank) ≤ 12^λ. …

In plain words: counting solutions is a *tensor network contraction* on a complete graph. The proof finds a way to lower the exponent of contracting such networks by a constant factor each time it zooms out, which compounds to a subexponential bound.
