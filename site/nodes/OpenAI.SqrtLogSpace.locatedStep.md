---
id: OpenAI.SqrtLogSpace.locatedStep
title: locatedStep
summary: One machine step, also updating the visited range.
review: draft
authors:
- grok-bot
quiz:
- q: When does locatedStep return none?
  type: choice
  choices:
  - exactly when step does
  - never
  answer: 0
  explain: It is `Option.map` of step.
- q: What does monitor update?
  type: choice
  choices:
  - position, lower, upper of the scanned tape
  - all tapes
  answer: 0
  explain: Only tape `scan q`.
- q: Does it change the config itself?
  type: choice
  choices:
  - It replaces it by step's result
  - 'No'
  answer: 0
  explain: '`{ config … }`.'
---
## Plain English

`locatedStep machine c := (machine.step c.config).map c.monitor`.
