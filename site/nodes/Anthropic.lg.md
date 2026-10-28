---
id: Anthropic.lg
title: 'lg: logarithm to base 2'
summary: 'The paper''s log: Real.logb 2 x, not rounded.'
review: draft
authors:
- grok-bot
quiz:
- q: lg 8 = ?
  type: choice
  choices:
  - '3'
  - '2.08'
  - '8'
  answer: 0
  explain: 2³ = 8, so log₂ 8 = 3.
- q: Is lg rounded?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: It is the real logarithm.
- q: What is `Real.logb 2 0` in Lean?
  type: choice
  choices:
  - undefined, so Lean rejects it
  - 0, by Mathlib's convention (log 0 = 0)
  answer: 1
  explain: Mathlib's `Real.log 0 = 0`. The Main Theorem's hypotheses avoid such inputs.
---
## Plain English

`lg x := Real.logb 2 x`, the real base-2 logarithm, not rounded, and of x itself.
