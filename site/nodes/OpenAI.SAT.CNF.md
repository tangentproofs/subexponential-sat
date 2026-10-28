---
id: OpenAI.SAT.CNF
title: 'SAT.CNF: a formula as a finite set of clauses'
summary: A formula is a **Finset** of clauses and a clause a **Finset** of literals, so nothing can repeat and order
  does not matter. That keeps the input size polynomial in n.
review: draft
authors:
- grok-bot
quiz:
- q: Can a clause appear twice in a `SAT.CNF`?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: It is a Finset.
- q: Compared to Anthropic's CNF (lists), which is more restrictive?
  type: choice
  choices:
  - OpenAI's (sets)
  - Anthropic's (lists)
  answer: 0
  explain: Anthropic allows repeated literals and different orders; only repeated clauses are forbidden.
- q: At most how many clauses can a width-3 CNF on n variables have?
  type: choice
  choices:
  - (2n+1)³ (roughly)
  - unbounded
  - 3n
  answer: 0
  explain: Each clause is a set of at most 3 of the 2n literals.
---
## Plain English

`CNF V := Finset (Clause V)` and [Clause](#/node/OpenAI.SAT.Clause) V := Finset ([Literal](#/node/OpenAI.SAT.Literal) V). The headline uses V = Fin n.
