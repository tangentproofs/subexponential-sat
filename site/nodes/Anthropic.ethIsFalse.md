---
id: Anthropic.ethIsFalse
title: ETH is false (Anthropic)
summary: '**The surprise:** a famous hardness assumption, which hundreds of papers rely on, is stated in Lean from
  scratch and proved *false*, using only Lean''s three standard axioms. For every δ > 0, some Turing machine decides
  3-SAT on n variables within c·2^{δn} steps.'
review: draft
authors:
- grok-bot
caveats:
- The link from Mathlib's Turing machines to 'an algorithm in the usual sense' is an argument in the comment at
  the top of MainResults.lean (a RAM simulates the machine with bounded overhead, and re-encoding the formula takes
  polynomial time). It is standard, but it is not part of the Lean statements or proofs.
- Clauses are lists, and no clause may be written twice (`IsKCNF` uses `List.Nodup`), so a 3-CNF on n variables
  has at most (2n+1)³ clauses. That is why a time bound in n alone makes sense.
- ETH is stated for deterministic machines. The authors note (outside Lean) that refuting the deterministic form
  also refutes the randomized form.
- This site has not built the Lean. The claim that it checks rests on the authors' CI run (passed, 26 Oct 2026,
  11:31 PM ET) and on our grep for `sorry`/`axiom` (none outside Challenge.lean).
widgets:
- type: walkthrough
  title: How Solution.lean proves it (Solution.lean, lines 36-40)
  config:
    steps:
    - text: 'Start from the Main Theorem: one machine counts the satisfying assignments of every k-CNF within 2^{C·min{km/√log
        m, k²n·log log n/√log n}} steps'
      lean: CountedRoute.mainTheoremHolds
      link: Anthropic.mainTheorem
      note: 'This is where all the work is: about 150,000 lines under proof/. It needs the formula''s variables
        to be named x₀ … x_{n−1} in order of use, and every variable to occur.'
    - text: 'Rename variables: a front end that renames the variables that occur gives the same bound for formulas
        with any names, plus a polynomial in the input length'
      lean: NamesInOrder.generalFormFollowsAsPropositions
      note: proof/maintheorem/NamesInOrder/General.lean lines 61-69. It wraps the machine with a renaming front
        end and absorbs the overhead into the constant.
    - text: 'Wrap the counter: a front end, a simulation and a last step give one machine that decides 3-SAT within
        c·2^{δn} steps for every δ > 0'
      lean: Wrap.countingBoundImpliesFailureOfETH
      note: proof/machines/Wrap/Main.lean lines 113-117. 'Count > 0' answers satisfiability; the polynomial is absorbed
        because 2^{o(n)}·poly(n) is below c·2^{δn}.
    - text: 'Pick the third of five conclusions: ¬ ETH'
      lean: .2.2.1
      note: '`Wrap.OneMachineEveryDeltaAndETHFails` bundles five statements. The third, `¬ Sat3.ETH_TM`, unfolds
        to `MainResults.ETHIsFalse`. Lean checks that by unfolding definitions.'
quiz:
- q: What does `ETHIsFalse` say about s₃, the infimum of the achievable exponents δ for 3-SAT?
  type: choice
  choices:
  - s₃ > 0
  - s₃ = 0
  - s₃ = 1
  - s₃ is infinite
  answer: 1
  explain: '`ETHIsFalse := ¬ ETH` and `ETH := 0 < s 3`. As s₃ is an infimum of non-negative numbers, ¬(0 < s₃) means
    s₃ = 0.'
- q: Which model of computation does the Lean statement use?
  type: choice
  choices:
  - a random-access machine
  - Mathlib's finite multi-stack Turing machines (`FinTM2`)
  - Boolean circuits
  - a Lean function, with its evaluation steps counted
  answer: 1
  explain: '`InTime` asks for a `TM2ComputableAux Bool Bool`, i.e. a `FinTM2` machine, with every stack alphabet
    finite.'
- q: Must one machine work for every δ > 0?
  type: choice
  choices:
  - Yes, one machine for all δ
  - No, the machine may depend on δ (and on k)
  answer: 1
  explain: '`InTime k δ` starts with `∃ M`, after δ is fixed. The Main Theorem is stronger (one machine for everything),
    but `ETHIsFalse` only needs a machine for each δ.'
- q: Which axioms does the proof use, according to `scripts/PrintAxioms.lean` and the project's CI?
  type: choice
  choices:
  - propext, Classical.choice, Quot.sound only
  - those three plus `sorryAx`
  - those three plus a custom axiom for the Turing-machine simulation
  - '`native_decide`'
  answer: 0
  explain: The README says the axiom check prints exactly the three standard axioms, and the repository's CI (Comparator
    with the independent `nanoda` kernel) passed on commit 16a5ce4. This site has not rebuilt it itself; see the
    Trust page.
---
## Plain English

**Theorem (`MainResults.ethIsFalse`).** The Exponential Time Hypothesis, as defined in [ETH](#/node/Anthropic.ETH), is false.

Unfolded: let s₃ be the infimum of all δ ≥ 0 such that *some* deterministic multi-stack Turing machine decides 3-SAT on n variables within c·2^{δn} steps, for some constant c and every n (see [s](#/node/Anthropic.s) and [InTime](#/node/Anthropic.InTime)). ETH says s₃ > 0. The theorem says s₃ = 0: **for every δ > 0 there is such a machine**.

In the authors' words (Challenge.lean line 11): *"The hypothesis (Impagliazzo and Paturi) says s₃ > 0. The theorem says that this fails: s₃ = 0, that is, for every δ > 0 there is such a machine."*

Why this matters: ETH is the standard assumption behind most "this problem needs exponential time" results in fine-grained complexity. The paper reports a literature search that found more than 800 papers with at least one result proved only under ETH or a stronger hypothesis.

What the result is **not**: the paper itself stresses that the bound is "purely asymptotic". For 3-CNFs with m = 5n clauses, it beats the 2ⁿ of brute force only when n > 10^10000. It says nothing about solving formulas in practice, and it does not touch P vs NP.

### How the Lean proof is put together

The proof in `Solution.lean` is one line (Solution.lean line 40). It takes the [Main Theorem](#/node/Anthropic.mainTheorem) and applies two general arguments to it, each proved for *every* machine with the right bound. The outline below follows them.
