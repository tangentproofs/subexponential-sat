---
id: OpenAI.Encoding.literalCode
title: 'literalCode: 2v + (1 if positive)'
summary: x_v ↦ 2v+1, ¬x_v ↦ 2v.
review: draft
authors:
- grok-bot
quiz:
- q: Code of ¬x₀?
  type: choice
  choices:
  - '0'
  - '1'
  - '2'
  answer: 0
  explain: 2·0 + 0 = 0 (positive = false adds nothing).
- q: Code of x₃?
  type: choice
  choices:
  - '6'
  - '7'
  - '8'
  answer: 1
  explain: 2·3 + 1 = 7 (positive adds 1).
- q: Is literalCode injective?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: v = code / 2, sign = code mod 2.
---
## Plain English

`literalCode l := 2 * l.variable.val + if l.positive then 1 else 0`.
