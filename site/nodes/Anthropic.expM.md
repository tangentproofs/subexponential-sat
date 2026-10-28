---
id: Anthropic.expM
title: expM k m = km/√(log m)
summary: The exponent in the number of clauses.
review: draft
authors:
- grok-bot
quiz:
- q: Which log?
  type: choice
  choices:
  - natural
  - base 2
  answer: 1
  explain: '`lg = Real.logb 2`.'
- q: What happens at m = 1?
  type: choice
  choices:
  - √(log 1) = 0, so Lean's x/0 = 0 would make the bound 1 step; the Main Theorem assumes m ≥ 2
  - nothing special
  answer: 0
  explain: See the MainTheorem docstring.
- q: Does expM grow slower than m for fixed k?
  type: choice
  choices:
  - Yes, by a factor √(log m)
  - 'No'
  answer: 0
  explain: km/√log m = o(m).
---
## Plain English

`expM k m := k * m / √(lg m)`, with [lg](#/node/Anthropic.lg) = log₂.
