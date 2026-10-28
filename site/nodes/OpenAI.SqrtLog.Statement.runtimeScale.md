---
id: OpenAI.SqrtLog.Statement.runtimeScale
title: runtimeScale n = n·(log log(n+16))²/√(log(n+16))
summary: The o(n) exponent. Natural logs, shifted by 16 so that small n behave.
review: draft
authors:
- grok-bot
quiz:
- q: Which log?
  type: choice
  choices:
  - natural
  - base 2
  answer: 0
  explain: '`Real.log`.'
- q: Why n + 16?
  type: choice
  choices:
  - so log log is positive for every n ≥ 0
  - arbitrary
  answer: 0
  explain: log 16 ≈ 2.77 and log log 16 ≈ 1.02 > 0.
- q: Is this the paper's sharpest exponent?
  type: choice
  choices:
  - No, the paper claims n log log n/√log n; this is the (log log n)² version
  - 'Yes'
  answer: 0
  explain: See lean/docs/378.md.
---
## Plain English

`runtimeScale n := n * (log (log (n + 16)))^2 / √(log (n + 16))` with `Real.log` (natural log).
