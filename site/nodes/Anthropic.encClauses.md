---
id: Anthropic.encClauses
title: 'encClauses: how a k-CNF is written on the input tape'
summary: n in unary, then for each clause exactly k fixed-width slots of ⌊log₂(2n)⌋+1 bits. Its length is polynomial
  in n, which is what lets a 2^{o(n)} bound absorb the time to read the input.
review: draft
authors:
- grok-bot
quiz:
- q: How is n written?
  type: choice
  choices:
  - in binary
  - 'in unary: n ones then a zero'
  answer: 1
  explain: '`List.replicate n true ++ false :: …`.'
- q: How many bits does each clause take?
  type: choice
  choices:
  - k · (⌊log₂(2n)⌋ + 1)
  - its own length times log n
  - exactly 3
  answer: 0
  explain: k positions of `Nat.log2 (2 * n) + 1` bits each.
- q: Which slot number encodes x₃ (positive)?
  type: choice
  choices:
  - '7'
  - '8'
  - '6'
  answer: 1
  explain: '`2 * 3 + 1 + true.toNat = 8`. ¬x₃ is 7, and 0 means an empty position.'
---
## Plain English

`encClauses k φ` is the bit string: n ones, a zero, then for each clause, k positions of `Nat.log2 (2 * n) + 1` bits each, each holding the [slot](#/node/Anthropic.slot) number of that position (0 for empty, 2i+1 for ¬xᵢ, 2i+2 for xᵢ), lowest bit first. A clause with fewer than k literals is padded with empty positions.

Since clauses don't repeat and each has at most k literals, the length is at most n + 1 + (2n+1)^k · k · (log₂(2n)+1), which is polynomial in n for fixed k.
