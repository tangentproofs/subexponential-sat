---
id: OpenAI.SqrtLogSpace.compiled_exact_count_and_sat
title: The compiled form of the main theorem
summary: The same statement as the headline, with the machine given as a compiled bit program with 1220 stacks,
  the count on stack 256 and the answer on stack 1216.
review: draft
authors:
- grok-bot
quiz:
- q: How many stacks does the compiled program use?
  type: choice
  choices:
  - '2'
  - '80'
  - '1220'
  answer: 2
  explain: '`BitProgram.Program 80 1220 labels`: 80 registers, 1220 stacks.'
- q: Where is the count written?
  type: choice
  choices:
  - stack 256
  - stack 1216
  - stack 0
  answer: 0
  explain: '`final.config.tapes (256 : Fin 1220) = Tape.mk₁ (countWord …)`.'
- q: Is this a weaker statement than the headline?
  type: choice
  choices:
  - No, the headline is a repackaging of it
  - 'Yes'
  answer: 0
  explain: '`exact_count_and_sat` is proved by `refine` from this theorem.'
---
## Plain English

This is the version proved first in SqrtLogSpace/Final.lean lines 10-69. The headline [exact_count_and_sat](#/node/OpenAI.SqrtLogSpace.exact_count_and_sat) is obtained from it by naming the machine `GuardedCompiler.primitive program` and its two tapes.
