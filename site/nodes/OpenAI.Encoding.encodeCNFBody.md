---
id: OpenAI.Encoding.encodeCNFBody
title: 'encodeCNFBody: the clauses part of the code'
summary: The sorted list of sorted literal-code lists, as nested self-delimiting lists.
review: draft
authors:
- grok-bot
quiz:
- q: How many list levels?
  type: choice
  choices:
  - one
  - 'two: clauses, then literals'
  answer: 1
  explain: '`encodeList (encodeList encodeNat)`.'
- q: What is encoded at the innermost level?
  type: choice
  choices:
  - literal codes, in unary
  - variable names
  answer: 0
  explain: '`encodeNat` of each literal code.'
- q: Which order are clauses in?
  type: choice
  choices:
  - sorted
  - insertion order
  answer: 0
  explain: '`cnfNumbers` sorts.'
---
## Plain English

`encodeCNFBody F := encodeList (encodeList encodeNat) (cnfNumbers F)`.
