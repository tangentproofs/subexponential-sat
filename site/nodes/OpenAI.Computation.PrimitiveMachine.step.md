---
id: OpenAI.Computation.PrimitiveMachine.step
title: 'PrimitiveMachine.step: one step'
summary: Read the scanned tape's head symbol; halt with an answer, or move/write on that tape and change state.
review: draft
authors:
- grok-bot
quiz:
- q: What does step return on a halted configuration?
  type: choice
  choices:
  - none
  - the same configuration
  answer: 0
  explain: '`| .inl _ => none`.'
- q: Does halting cost a step?
  type: choice
  choices:
  - 'Yes: the step that returns `.inl answer`'
  - 'No'
  answer: 0
  explain: That transition is itself a step to the halted configuration.
- q: How many tapes change per step?
  type: choice
  choices:
  - at most one
  - all
  answer: 0
  explain: '`Function.update c.tapes tapeIndex nextTape`.'
---
## Plain English

From a halted configuration, `step` returns `none`. Otherwise it applies `transition` to the current state and the symbol under the scanned tape's head, and updates only that tape (`Function.update`).
