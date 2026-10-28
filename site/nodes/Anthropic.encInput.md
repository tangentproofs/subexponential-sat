---
id: Anthropic.encInput
title: 'encInput: the Main Theorem''s input, with k in it'
summary: 1ᵏ 0 followed by encClauses k φ. Putting k in the input is what lets one machine handle every width.
review: draft
authors:
- grok-bot
quiz:
- q: How is k written?
  type: choice
  choices:
  - unary
  - binary
  answer: 0
  explain: k ones, then a zero.
- q: Why is k part of the input here but not in DecidesKSat?
  type: choice
  choices:
  - the Main Theorem has one machine for all k
  - for no reason
  answer: 0
  explain: In `InTime`, k is fixed before the machine is chosen.
- q: What follows 1ᵏ 0?
  type: choice
  choices:
  - the formula's code, starting with 1ⁿ 0
  - the count
  answer: 0
  explain: '`encClauses k φ` starts with n in unary.'
---
## Plain English

`encInput k φ := List.replicate k true ++ false :: encClauses k φ`. See [encClauses](#/node/Anthropic.encClauses).
