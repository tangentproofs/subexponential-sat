---
id: OpenAI.Encoding.clauseNumbers
title: 'clauseNumbers: a clause as a sorted list'
summary: The literal codes of the clause, sorted.
review: draft
authors:
- grok-bot
quiz:
- q: Are duplicates possible?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: A Finset image of an injective map.
- q: Sorted how?
  type: choice
  choices:
  - ascending
  - descending
  answer: 0
  explain: '`(· ≤ ·)`.'
- q: What is in the list?
  type: choice
  choices:
  - literal codes
  - variables
  answer: 0
  explain: 2v + sign.
---
## Plain English

`clauseNumbers C := (C.image literalCode).sort (· ≤ ·)`, see [literalCode](#/node/OpenAI.Encoding.literalCode).
