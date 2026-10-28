---
id: OpenAI.BinaryArithmetic.toNat
title: 'BinaryArithmetic.toNat: read a bit list as a number'
summary: 'Lowest bit first: toNat (b :: bs) = b + 2·toNat bs.'
review: draft
authors:
- grok-bot
quiz:
- q: toNat [true, false, true] = ?
  type: choice
  choices:
  - '5'
  - '3'
  - '6'
  answer: 0
  explain: 1 + 2·(0 + 2·1) = 5.
- q: Lowest or highest bit first?
  type: choice
  choices:
  - lowest
  - highest
  answer: 0
  explain: The head is the units bit.
- q: toNat [] = ?
  type: choice
  choices:
  - '0'
  - '1'
  answer: 0
  explain: Base case.
---
## Plain English

`toNat [] = 0`, `toNat (b :: bs) = bitVal b + 2 * toNat bs`.
