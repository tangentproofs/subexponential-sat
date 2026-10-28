---
id: OpenAI.Encoding.cnfNumbers
title: 'cnfNumbers: the formula as sorted lists of numbers'
summary: Each clause becomes a sorted list of literal codes; the clauses are then sorted.
review: draft
authors:
- grok-bot
quiz:
- q: Order used for lists of numbers?
  type: choice
  choices:
  - lexicographic (≤ on lists)
  - by length
  answer: 0
  explain: '`sort (· ≤ ·)` on `List ℕ` is lexicographic.'
- q: Can two clauses give the same list?
  type: choice
  choices:
  - No, literal codes determine the literals
  - 'Yes'
  answer: 0
  explain: literalCode is injective.
- q: Is it canonical?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: Sorted output.
---
## Plain English

`cnfNumbers F := (F.image clauseNumbers).sort (· ≤ ·)` using [clauseNumbers](#/node/OpenAI.Encoding.clauseNumbers).
