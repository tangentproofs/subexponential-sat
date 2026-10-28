---
id: OpenAI.Computation.PrimitiveMachine
title: 'PrimitiveMachine: OpenAI''s Turing machine model'
summary: A finite set of states, a fixed number of tapes over {0, 1, blank}, and in each state the machine looks
  at **one** tape and either halts with an answer, or moves that tape's head, or writes a symbol on it.
review: draft
authors:
- grok-bot
caveats:
- The model is defined in the comparator file, not taken from Mathlib, so its fairness must be checked by reading
  these few lines. We read them and found nothing unusual, but a second reader should check too.
quiz:
- q: How many tapes does one step act on?
  type: choice
  choices:
  - one
  - all of them
  answer: 0
  explain: '`scan q` picks one tape; only it is moved or written.'
- q: What is the tape alphabet?
  type: choice
  choices:
  - '`Option Bool`: 0, 1 or blank'
  - arbitrary
  answer: 0
  explain: '`Turing.Tape (Option Bool)`.'
- q: How does a run halt?
  type: choice
  choices:
  - '`transition` returns `.inl answer`'
  - by running out of tape
  answer: 0
  explain: Then the state becomes `.inl answer` and `step` returns `none` afterwards.
---
## Plain English

A `PrimitiveMachine` has `tapeCount` tapes and `stateCount` states, a designated input tape and start state, and for each state `q`:

- `scan q`: which tape it reads;
- `transition q s`, given the symbol s under that tape's head (`Option Bool`, `none` = blank): either `.inl answer` (halt with a Boolean answer), or `.inr (q', action)` (go to q' and do one `Turing.TM0.Stmt`: move left or right, or write a symbol).

[step](#/node/OpenAI.Computation.PrimitiveMachine.step) does one transition; [init](#/node/OpenAI.Computation.PrimitiveMachine.init) puts the input on the input tape. Everything else is Mathlib's `Turing.Tape`.

This is a standard (if spartan) multi-tape Turing machine: one tape touched per step, so it is no more powerful than a textbook machine.
