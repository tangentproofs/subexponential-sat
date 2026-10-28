---
id: OpenAI.BinaryArithmetic.bitVal
title: bitVal
summary: true ↦ 1, false ↦ 0.
review: draft
authors:
- grok-bot
quiz:
- q: bitVal true?
  type: choice
  choices:
  - '1'
  - '0'
  answer: 0
  explain: '`if true then 1 else 0` = 1.'
- q: bitVal false?
  type: choice
  choices:
  - '1'
  - '0'
  answer: 1
  explain: '`if false then 1 else 0` = 0.'
- q: Type of the result?
  type: choice
  choices:
  - ℕ
  - Bool
  answer: 0
  explain: '`def bitVal (b : Bool) : ℕ`.'
---
## Plain English

`bitVal b := if b then 1 else 0`.
