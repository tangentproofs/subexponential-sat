---
id: Anthropic.DecidesKSat
title: 'DecidesKSat: the machine answers k-SAT correctly and on time'
summary: Started on the code of any k-CNF φ, the machine halts within t(n) steps with one output bit, which is 1
  exactly when φ is satisfiable. k is fixed, not part of the input.
review: draft
authors:
- grok-bot
quiz:
- q: Is k part of the input word for `DecidesKSat`?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: 'The input is `encClauses k φ`: n in unary, then the clauses. k is fixed by the statement.'
- q: Which formulas must the machine handle?
  type: choice
  choices:
  - only those with every variable occurring
  - every φ with `IsKCNF k φ`, any number of clauses
  - only 3-CNFs with at least 2 clauses
  answer: 1
  explain: '`∀ (n : ℕ) (φ : CNF n), IsKCNF k φ → …`. No other condition.'
- q: What does the output look like?
  type: choice
  choices:
  - a satisfying assignment
  - one bit
  - the number of solutions
  answer: 1
  explain: '`some ([b].map M.outputAlphabet.invFun)`: one bit.'
---
## Plain English

`DecidesKSat k M t`: for every n and every φ with [IsKCNF](#/node/Anthropic.IsKCNF) k φ, there is a bit b with (b = true ↔ φ is [satisfiable](#/node/Anthropic.Satisfiable)) such that `M`, started on [encClauses](#/node/Anthropic.encClauses) k φ (translated through the machine's input alphabet), outputs `[b]` within t(n) steps (`TM2OutputsInTime`).

`TM2OutputsInTime` is Mathlib's: started with the input on the input stack and every other stack empty, the machine halts after at most t steps with the output on its output stack, every other stack empty, and its internal state back at its initial value.
