---
id: OpenAI.Encoding.encodeCNF
title: 'Encoding.encodeCNF: the canonical input word'
summary: n in unary, then the formula as a sorted list of sorted clauses of literal codes, all numbers in **unary**.
  Unary makes the input longer but still polynomial in n for fixed k.
review: draft
authors:
- grok-bot
quiz:
- q: How are numbers written?
  type: choice
  choices:
  - binary
  - unary
  answer: 1
  explain: '`encodeNat n = replicate n true ++ [false]`.'
- q: Why sort clauses and literals?
  type: choice
  choices:
  - so each Finset formula has exactly one code
  - for speed
  answer: 0
  explain: Finsets have no order; sorting makes the code canonical.
- q: Is L polynomial in n for fixed k?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: At most (2n+1)^k clauses, each with ≤ k codes of size O(n), plus framing overhead.
---
## Plain English

`encodeCNF F := encodeNat n ++ encodeCNFBody F`. [encodeNat](#/node/OpenAI.Encoding.encodeNat) writes n as n ones and a zero. [encodeCNFBody](#/node/OpenAI.Encoding.encodeCNFBody) writes the sorted list of clauses ([cnfNumbers](#/node/OpenAI.Encoding.cnfNumbers)), each a sorted list of [literal codes](#/node/OpenAI.Encoding.literalCode) 2v + (1 if positive), using [encodeList](#/node/OpenAI.Encoding.encodeList) and [frame](#/node/OpenAI.Encoding.frame) for self-delimiting lists.
