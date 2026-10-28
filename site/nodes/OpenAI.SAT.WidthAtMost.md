---
id: OpenAI.SAT.WidthAtMost
title: SAT.WidthAtMost k F
summary: Every clause has at most k literals.
review: draft
authors:
- grok-bot
quiz:
- q: Does width ≤ 3 allow a clause with 2 literals?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: The condition is C.card ≤ k, not = k.
- q: Is it about clauses or variables?
  type: choice
  choices:
  - clauses
  - variables
  answer: 0
  explain: '`C.card` is the number of literals in a clause.'
- q: Which k does the headline require?
  type: choice
  choices:
  - k ≥ 2
  - k ≥ 3
  - k = 3
  answer: 0
  explain: '`(hk : 2 ≤ k)`.'
---
## Plain English

`WidthAtMost k F := ∀ C ∈ F, C.card ≤ k`.
