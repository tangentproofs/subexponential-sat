---
id: Anthropic.numSat
title: 'numSat φ: the number of satisfying assignments'
summary: Count, among all 2ⁿ assignments, those that make some literal of every clause true.
review: draft
authors:
- grok-bot
quiz:
- q: At most how large is numSat φ?
  type: choice
  choices:
  - n
  - 2ⁿ
  - m
  answer: 1
  explain: There are 2ⁿ assignments.
- q: numSat φ > 0 iff…
  type: choice
  choices:
  - φ is satisfiable
  - φ has a clause
  - every variable occurs
  answer: 0
  explain: Same condition as `Satisfiable`.
- q: Over which variables are assignments counted?
  type: choice
  choices:
  - only those that occur
  - all of x₀ … x_{n−1}
  answer: 1
  explain: '`a : Fin n → Bool`, all n variables.'
---
## Plain English

`numSat φ := (Finset.univ.filter fun a : Fin n → Bool => ∀ C ∈ φ, ∃ l ∈ C, a l.1 = l.2).card`.
