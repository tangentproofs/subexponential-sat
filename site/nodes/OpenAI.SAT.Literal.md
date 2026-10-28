---
id: OpenAI.SAT.Literal
title: 'SAT.Literal: a variable with a sign'
summary: A record with a variable and a Boolean `positive`.
review: draft
authors:
- grok-bot
quiz:
- q: What does `positive = false` mean?
  type: choice
  choices:
  - the negated variable
  - the variable itself
  answer: 0
  explain: '`Literal.eval a l := a l.variable == l.positive`.'
- q: Does Literal derive DecidableEq?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: '`deriving DecidableEq`, needed to form Finsets of literals.'
- q: How many literals over Fin n?
  type: choice
  choices:
  - n
  - 2n
  answer: 1
  explain: n variables × 2 signs.
---
## Plain English

`structure Literal V where variable : V; positive : Bool`. It evaluates to true under `a` when `a variable == positive`.
