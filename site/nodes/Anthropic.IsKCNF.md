---
id: Anthropic.IsKCNF
title: 'IsKCNF k φ: clauses of width at most k, none written twice'
summary: A k-CNF here is a list of clauses, each of at most k literals, with **no clause repeated**. The no-repeat
  condition is what makes a time bound in n alone possible.
review: draft
authors:
- grok-bot
quiz:
- q: Is the formula `[[x₀, x₁], [x₁, x₀]]` allowed by `IsKCNF 2`?
  type: choice
  choices:
  - 'Yes: the two clauses are different lists'
  - 'No: they are the same clause'
  answer: 0
  explain: Lists in a different order are different, so `Nodup` holds.
- q: Why forbid repeated clauses?
  type: choice
  choices:
  - to make the problem easier
  - otherwise the input could be arbitrarily long for fixed n, and no bound in n alone could hold
  - Mathlib requires it
  answer: 1
  explain: The machine must read its input, so the input length must be bounded in n.
- q: Is an empty clause allowed?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: Its length is 0 ≤ k. An empty clause is false, so the formula is unsatisfiable.
---
## Plain English

`IsKCNF k φ := (∀ C ∈ φ, C.length ≤ k) ∧ φ.Nodup`.

The docstring explains the choices. A clause is a list, so it may be empty (then it is false), may repeat a literal or hold both x and ¬x, and the same literals in another order make a different clause. So a k-CNF on n variables has at most (2n+1)^k clauses. And: *"Without this, no time bound in n alone could hold: before halting, a machine must pop nearly all of its input, a bounded number of symbols per step."*
