---
id: Anthropic.Lit
title: 'Lit n: a literal xᵢ or ¬xᵢ'
summary: 'A literal is a pair (i, b): the variable xᵢ if b is true, its negation if b is false.'
review: draft
authors:
- grok-bot
quiz:
- q: What is (2, false)?
  type: choice
  choices:
  - x₂
  - ¬x₂
  - x₃
  answer: 1
  explain: b = false means the negated variable.
- q: How many literals are there on n variables?
  type: choice
  choices:
  - n
  - 2n
  - 2ⁿ
  answer: 1
  explain: n choices of i times 2 choices of b.
- q: Are the variables numbered from 0 or 1 in Lean?
  type: choice
  choices:
  - 0 (x₀ … x_{n−1})
  - 1 (x₁ … xₙ)
  answer: 0
  explain: '`Fin n` = {0, …, n−1}. The paper numbers from 1.'
---
## Plain English

`Lit n := Fin n × Bool`. The pair (i, true) is xᵢ and (i, false) is ¬xᵢ, for 0 ≤ i < n.
