---
id: Anthropic.slot
title: 'slot: the number written for one position of a clause'
summary: 0 for an empty position, 2i+1 for ¬xᵢ, 2i+2 for xᵢ. Every number is below 2n+1, so ⌊log₂(2n)⌋+1 bits suffice.
review: draft
authors:
- grok-bot
quiz:
- q: slot (some (0, false)) = ?
  type: choice
  choices:
  - '0'
  - '1'
  - '2'
  answer: 1
  explain: 2·0 + 1 + 0 = 1.
- q: Why does 0 mean 'empty'?
  type: choice
  choices:
  - so short clauses can be padded to k positions
  - because x₀ is special
  answer: 0
  explain: '`encClauses` writes k positions per clause; missing ones are `none`, i.e. 0.'
- q: Largest slot value for n variables?
  type: choice
  choices:
  - 2n
  - 2n − 1
  - n
  answer: 0
  explain: x_{n−1} gives 2(n−1) + 2 = 2n.
---
## Plain English

`slot none = 0` and `slot (some (i, b)) = 2i + 1 + (if b then 1 else 0)`.
