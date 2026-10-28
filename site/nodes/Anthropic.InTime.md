---
id: Anthropic.InTime
title: 'InTime k δ: some machine decides k-SAT in time O(2^{δn})'
summary: One machine with finite alphabets and one constant c decide every k-CNF on n variables within ⌊c·2^{δn}⌋
  steps, for **every** n. The machine and c may depend on k and δ.
review: draft
authors:
- grok-bot
quiz:
- q: Can the machine in `InTime k δ` depend on δ?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: '`InTime k δ := ∃ M c, …`, so M is chosen after k and δ.'
- q: Does the time bound depend on the number of clauses m?
  type: choice
  choices:
  - 'Yes'
  - No, only on n
  answer: 1
  explain: The bound is `fun n => ⌊c * 2^(δ n)⌋₊`. That works because no clause may repeat, so m ≤ (2n+1)^k.
- q: Why is `∀ i, Finite (M.tm.Γ i)` there?
  type: choice
  choices:
  - Mathlib already requires it, so it is redundant
  - Mathlib only requires the input alphabet to be finite; this makes every stack alphabet finite, as for a textbook
    machine
  - it bounds the number of states
  answer: 1
  explain: 'The head comment of MainResults.lean explains: ''Of the stack alphabets, Mathlib requires only that
    of the input stack to be finite.'''
---
## Plain English

`InTime k δ` holds when there are a machine `M` (a `TM2ComputableAux Bool Bool`, every stack alphabet finite) and a natural number `c` such that `M` [decides k-SAT](#/node/Anthropic.DecidesKSat) within ⌊c·2^{δn}⌋ steps on every formula with n variables.

There is no "for large enough n" and no extra polynomial factor: the bound c·2^{δn} must hold for every n. That is equivalent to the usual O(2^{δn}), since finitely many small cases are absorbed into c.
