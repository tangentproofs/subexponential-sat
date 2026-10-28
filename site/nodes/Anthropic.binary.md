---
id: Anthropic.binary
title: 'binary n c: the lowest n+1 bits of c'
summary: The count is output as exactly n + 1 bits, lowest first. Since the count is at most 2ⁿ, nothing is lost.
review: draft
authors:
- grok-bot
quiz:
- q: binary 2 5 = ?
  type: choice
  choices:
  - '[true, false, true]'
  - '[true, false, true, false]'
  - '[false, true, true]'
  answer: 0
  explain: 5 = 101₂; bits 0, 1, 2 are 1, 0, 1.
- q: Why n + 1 bits rather than n?
  type: choice
  choices:
  - the count can be 2ⁿ itself, which needs n + 1 bits
  - for a parity bit
  answer: 0
  explain: 2ⁿ = 1 followed by n zeros.
- q: Lowest or highest bit first?
  type: choice
  choices:
  - lowest
  - highest
  answer: 0
  explain: '`List.range` starts at bit 0.'
---
## Plain English

`binary n c := (List.range (n + 1)).map c.testBit`: bit 0, bit 1, …, bit n of c.
