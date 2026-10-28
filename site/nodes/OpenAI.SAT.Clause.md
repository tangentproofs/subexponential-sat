---
id: OpenAI.SAT.Clause
title: 'SAT.Clause: a finite set of literals'
summary: An OR of finitely many literals, with no repeats.
review: draft
authors:
- grok-bot
quiz:
- q: Is the empty clause allowed?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: The empty Finset is a clause; it is false.
- q: Can a clause contain both x and ¬x?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: They are different literals.
- q: Is the order of literals meaningful?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: Finsets are unordered.
---
## Plain English

`Clause V := Finset (Literal V)`.
