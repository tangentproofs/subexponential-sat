---
id: Anthropic.expN
title: expN k n = k²·n·log log n/√(log n)
summary: 'The exponent in the number of variables: o(n) for fixed k.'
review: draft
authors:
- grok-bot
quiz:
- q: Is expN k n = o(n) for fixed k?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: log log n / √log n → 0.
- q: How does it depend on k?
  type: choice
  choices:
  - k
  - k²
  - 2^k
  answer: 1
  explain: '`(k : ℝ) ^ 2`.'
- q: Why n ≥ 4 in the Main Theorem?
  type: choice
  choices:
  - so log log n ≥ 1
  - so n is even
  answer: 0
  explain: log₂ log₂ 4 = 1. At n = 2, log log n = 0 and the bound would be one step.
---
## Plain English

`expN k n := k^2 * n * lg (lg n) / √(lg n)`, with [lg](#/node/Anthropic.lg) = log₂.
