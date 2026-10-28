---
id: OpenAI.Encoding.encodeNat
title: 'encodeNat: unary numbers'
summary: n ones followed by a zero.
review: draft
authors:
- grok-bot
quiz:
- q: encodeNat 2 = ?
  type: choice
  choices:
  - '[true, true, false]'
  - '[true, false]'
  - '[false, true, false]'
  answer: 0
  explain: Two ones then a zero.
- q: Length of encodeNat n?
  type: choice
  choices:
  - n
  - n + 1
  - log n
  answer: 1
  explain: n ones plus the terminating zero.
- q: Is this binary?
  type: choice
  choices:
  - No, unary
  - 'Yes'
  answer: 0
  explain: 'It is unary: the value is the number of ones.'
---
## Plain English

`encodeNat n := List.replicate n true ++ [false]`.
