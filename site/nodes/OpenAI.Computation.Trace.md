---
id: OpenAI.Computation.Trace
title: 'Trace step t a b: b is reached from a in exactly t steps'
summary: 'An inductive relation: t successful steps of `step` lead from a to b.'
review: draft
authors:
- grok-bot
quiz:
- q: Can a Trace pass through a halted configuration?
  type: choice
  choices:
  - only at its end, since step returns none there
  - 'yes'
  answer: 0
  explain: Each step must be `some`.
- q: Is t exact or an upper bound?
  type: choice
  choices:
  - exact
  - upper bound
  answer: 0
  explain: Exactly t steps.
- q: In the headline, is the final configuration halted?
  type: choice
  choices:
  - Yes, its state is `Sum.inl …`
  - Not necessarily
  answer: 0
  explain: '`final.config.state = Sum.inl (decide (0 < count F))`.'
---
## Plain English

`Trace step 0 a a`, and if `step a = some b` and `Trace step n b c` then `Trace step (n+1) a c`.
