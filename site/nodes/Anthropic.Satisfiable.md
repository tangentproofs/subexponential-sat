---
id: Anthropic.Satisfiable
title: Satisfiable φ
summary: Some assignment of true/false to the variables makes at least one literal of every clause true.
review: draft
authors:
- grok-bot
quiz:
- q: Is a formula with an empty clause satisfiable?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: An empty clause has no literal to make true.
- q: When is the literal (i, b) true under a?
  type: choice
  choices:
  - when a i = true
  - when a i = b
  - when a i ≠ b
  answer: 1
  explain: '`a l.1 = l.2`.'
- q: Is the empty formula satisfiable (for any n)?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: There are no clauses, so `∀ C ∈ []` holds; any assignment works (for n = 0 there is exactly one).
---
## Plain English

`Satisfiable φ := ∃ a : Fin n → Bool, ∀ C ∈ φ, ∃ l ∈ C, a l.1 = l.2`.

A literal (i, b) is true under `a` when `a i = b`.
